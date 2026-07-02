import ast
import math
from collections.abc import Callable
from statistics import fmean
from typing import Union, NamedTuple, List, Dict, Any

import click
import pandas as pd
import numpy as np
import datetime as dt
import binascii

import sqlalchemy
from sqlalchemy import select, and_, INTEGER, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.horizontal_shard import set_shard_id
from sqlalchemy.orm import Session

from smf2db.db_models.smf7x_model import SmfLpar, SmfCpc


class UploadResult(NamedTuple):
    insert_dict_list: List[Dict[str, Any]]
    elapsed_time: float
    error: int


def get_csc(csc, db_session):
    stmt = select(SmfCpc).where(SmfCpc.csc == csc).options(set_shard_id('smf.0'))
    try:
        target = db_session.execute(stmt).scalar()
        # target = db_session.get(SmfCpc, {'csc': csc})
        if pd.isna(target):
            target = SmfCpc(csc)
            db_session.add(target)
            db_session.commit()
        return target
    except Exception as e:
        click.secho(
            f"\nThe database for Smf70 needs to be initialized to continue the processing.",
            err=True,
            fg="red"
        )
        raise SystemExit(1)


def get_csc_in_db(sysplex_name, system_name, lpar_number, db_session):
    try:
        csc = db_session.execute(select(SmfLpar.csc).filter(
            and_(SmfLpar.sysplex_name == sysplex_name,
                 SmfLpar.system_name == system_name,
                 SmfLpar.lpar_number == lpar_number.astype(INTEGER))).options(set_shard_id('smf.0'))).scalar()
        return csc
    except Exception as e:
        click.secho(
            f"\nThis smf type cannot be processed until Smf70 have been initialized and the corresponding Smf70 Subtype 1 records have been processed.",
            err=True,
            fg="red"
            )
        raise SystemExit(1)


def get_lpar(csc, lpar_number, session):
    stmt = select(SmfLpar).where(SmfLpar.csc == csc and SmfLpar.lpar_number == int(lpar_number)).options(set_shard_id('smf.0'))
    try:
        target = session.execute(stmt).scalar()
        return target
    except Exception as e:
        click.secho(
            f"\nThe database for Smf70 needs to be initialized to continue the processing.",
            err=True,
            fg="red"
        )
        raise SystemExit(1)


def get_lpar_in_db(csc, lpar_name, system_name, lpar_number, sysplex_name, effective_timestamp, db_session, is_cf=0):
    # target = db_session.get(SmfLpar, {"csc": csc, "lpar_number": lpar_number})
    stmt = select(SmfLpar).where(SmfLpar.csc == csc and SmfLpar.lpar_number == lpar_number).options(set_shard_id('smf.0'))
    try:
        target = db_session.execute(stmt).scalar()
        if pd.isna(target):
            target = SmfLpar(csc, lpar_name, system_name, lpar_number, sysplex_name, is_cf, effective_timestamp)
            db_session.add(target)
        elif target.last_update_time != effective_timestamp:
            target.last_update_time = effective_timestamp
        return target
    except Exception as e:
        click.secho(
            f"\nThis smf type cannot be processed until Smf70 have been initialized and the corresponding Smf70 Subtype 1 records have been processed.",
            err=True,
            fg="red"
            )
        raise SystemExit(1)


def is_bit_set(num, length, pos):
    if not pd.isna(num):
        binary = "{0:0{l}b}".format(num, l=length)
        return int(binary[pos])
    else:
        return np.nan


def to_datetime(datetime_value):
    if not pd.isna(datetime_value):
        try:
            return pd.to_datetime(datetime_value, errors='coerce', format='%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            try:
                return pd.to_datetime(datetime_value, errors='coerce', format='%Y-%m-%d %H:%M:%S')
            except ValueError:
                return pd.NaT
    else:
        return pd.NaT


def to_localtime(t, o):
    if not pd.isnull(t):
        return pd.to_datetime(t) + pd.to_timedelta(o)
    else:
        return pd.NaT


def setdatetime(timestamp):
    return pd.to_datetime(timestamp).replace(minute=0, second=0, microsecond=0)


def getjobclass(sub_sys_id, job_class):
    if sub_sys_id[0:3] == 'JES':
        return bytearray.fromhex(job_class[2:]).decode('cp500')
    else:
        return ' '


def ebcdic2ascii(value):
    if len(value) > 0 and value != '0x00':
        return binascii.unhexlify(value[2:]).decode('cp500')
    else:
        return ''


def substr_x(value, start, end=None, default=np.nan):
    if not pd.isna(value):
        if pd.isna(end):
            return value[start:]
        else:
            return value[start:end]
    else:
        return default


def x_divided_by_y(x, y):
    if y > 0:
        return x/y
    else:
        return np.nan


def setwkl(subtype, sub_sys_id, smf30pgm, smf30scn):
    if subtype == 6:
        return 'SYS_STC'
    elif smf30scn == 'SYSTEM':
        return 'SYS'
    elif smf30pgm in ['DFSRRC00', 'DFSMVRC0', 'BPEINI00']:
        return 'IMS'
    elif smf30pgm in ['DSNYASCP', 'DXRRLM00', 'DSNX9STP', 'ASNLRP25', 'DSNX9WLM']:
        return 'DB2'
    elif smf30pgm in ['DFHSIP']:
        return 'CICS'
    elif smf30pgm in ['CSQYASCP', 'CSQXJST']:
        return 'MQS'
    elif sub_sys_id[0:3] == 'STC':
        return 'STC'
    elif sub_sys_id[0:3] == 'JES':
        return 'JOB'
    elif sub_sys_id[0:3] == 'TSO':
        return 'TSO'
    elif sub_sys_id[0:4] == 'OMVS':
        return 'OMVS'
    else:
        return 'OTHER'


def cal_tcb_time(step_time, cpu_sdc_10, cpu_sus_l, rmctadjc_copy):
    if (step_time > 0) or (cpu_sdc_10 == 0):
        return step_time
    else:
        return (cpu_sus_l * 10) / cpu_sdc_10 * rmctadjc_copy / 16 / 1e6


def cal_srb_time(srb_step_cpu_time, srb_sdc_10, srb_sus_l, rmctadjc_copy):
    if (srb_step_cpu_time > 0) or (srb_sdc_10 == 0):
        return srb_step_cpu_time
    else:
        return (srb_sus_l * 10) / srb_sdc_10 * rmctadjc_copy / 16 / 1e6


def cal_msu(rctpcpua_actual, cpu_total, rctpcpua_scaling_factor):
    if not pd.isna(rctpcpua_actual) and rctpcpua_actual > 0:
        return cpu_total * 3600 * 16 * rctpcpua_scaling_factor / (rctpcpua_actual * 300)
    else:
        return 0.


def cal_duration(subtype, interval_end_tod, interval_start_tod, timestamp, initiator_job_time, stc_interval_value):
    if subtype != 6 and not pd.isna(interval_end_tod) and not pd.isna(interval_start_tod):
        return (pd.to_datetime(interval_end_tod) - pd.to_datetime(interval_start_tod)) / np.timedelta64(1, 's')
    elif subtype != 6 and not pd.isna(initiator_job_time):
        return (pd.to_datetime(timestamp) - pd.to_datetime(initiator_job_time)) / np.timedelta64(1, 's')
    elif subtype == 6 and not pd.isna(stc_interval_value):
        return stc_interval_value / np.timedelta64(1, 's')
    else:
        return None


def to_int(value):
    return int(value, 0)


def hex2int(hex_value):
    if not pd.isna(hex_value):
        return int(hex_value, 16)
    else:
        return None


def converttolist(item):
    if not isinstance(item, list):
        return [item]
    else:
        return item


def is_list_of_list(test_list):
    return any(isinstance(sub, list) for sub in test_list)


def col_to_frame(df_d, col, df_index):
    convert_to_list = np.vectorize(converttolist)
    z = df_d[col].to_frame().set_index(df_index)
    z.dropna(how='all', inplace=True)
    z[col] = convert_to_list(z[col])
    x = z.explode(col)
    return pd.json_normalize(x[col]).set_index(x.index).reset_index()


def cols_to_frame(df_d, cols, df_index):
    convert_to_list = np.vectorize(converttolist)
    df_list = []
    z = df_d[cols].set_index(df_index)
    z.dropna(how='all', inplace=True)
    for col in cols:
        z[col] = convert_to_list(z[col])
    x = z.explode(cols)
    for col in cols:
        _df = pd.json_normalize(x[col]).set_index(x.index)
        df_list.append(_df)
    return pd.concat(df_list, axis=1).reset_index()


def combine_list_of_dict(ld1, ld2):
    # return [sublist[0] | sublist[1] for sublist in zip(ld1, ld2)]
    return [sublist[0] | sublist[1] if not pd.isna(sublist[1]) else sublist[0] for sublist in zip(ld1, ld2)]


def list_max(listx):
    if len(listx) > 0:
        return max(listx)
    return np.nan


def v_index(alist):
    if any(alist):
        for ix, a in enumerate(alist):
            if a == max(alist):
                return ix
    return np.nan


def list_loc(listx, loc):
    if len(listx) > 0 and not pd.isna(loc):
        return listx[int(loc)]
    return np.nan


def count_items(series, target):
    return series.count(target)


def mean_items(series):
    if not all(pd.isna(item) for item in series):
        return fmean(item for item in series if not pd.isna(item))
    return np.nan


def max_items(series: pd.Series):
    if not all(pd.isna(item) for item in series):
        return max(item for item in series if not pd.isna(item))
    return np.nan


def min_items(series):
    if not all(pd.isna(item) for item in series):
        return min(item for item in series if not pd.isna(item))
    return np.nan


def max_index(alist):
    if not all(pd.isna(item) for item in alist):
        for ix, a in enumerate(alist):
            if a == max(alist):
                return ix
    return np.nan


def min_index(alist):
    if not all(pd.isna(item) for item in alist):
        for ix, a in enumerate(alist):
            if a == min(alist):
                return ix
    return np.nan


def calrate(x, y):
    if y > 0:
        return x / y
    else:
        return np.nan


def str2dict(strdict):
    return ast.literal_eval(strdict)


def setcpupolarization(flags_polarization):
    if flags_polarization[0:2] == '00':
        cpu_polarization = 'N/A'
    elif flags_polarization[0:2] == '01':
        cpu_polarization = 'LOW'
    elif flags_polarization[0:2] == '10':
        cpu_polarization = 'MED'
    elif flags_polarization[0:2] == '11':
        cpu_polarization = 'HIGH'
    else:
        cpu_polarization = 'UNKN'
    return cpu_polarization


def getcputype(cpu_id_index, cisdict):
    if cpu_id_index > 0:
        return cisdict[(cpu_id_index - 1)]
    else:
        return np.nan


def cputypedict(cpu_type):
    smf70typ_cpu_type = {0: 'CP', 1: 'IFA', 2: 'IIP'}
    return smf70typ_cpu_type[cpu_type]


def round_(n, decimals=0):
    if not pd.isna(n):
        multiplier = 10 ** decimals
        return math.floor(n * multiplier + 0.5) / multiplier
    else:
        return np.nan


def weighted_avg(df, values, weights, groupby):
    df[values] = df[values].astype(float)
    df[weights] = df[weights].astype(float)
    # df = df.copy().astype({values: float, weights: float})
    grouped = df.groupby(groupby)
    new_df = pd.DataFrame()
    new_df['weighted_average'] = df[values] / grouped[weights].transform('sum') * df[weights]
    return new_df['weighted_average'].sum(min_count=1)


def agg_next(series: pd.Series):
    return next((item for item in series if not pd.isna(item)), np.nan)


def agg_boost_class(series: pd.Series):
    if len(set(series)) == 1:
        return series.iloc[0]
    else:
        return 'XXX'


def agg_boost(series):
    if len(set(series)) == 1:
        return 0, series.iloc[0]
    else:
        return 1, series.iloc[-1]


def agg_tolist(series: pd.Series):
    return series.tolist()


def agg_hex_sum(series):
    convert_2_int = np.vectorize(to_int)
    if not series.empty:
        if isinstance(series, list):
            int_series = convert_2_int(series)
            return hex(sum(int_series))
        elif isinstance(series, str):
            int_series = int(series, 0)
            return int_series
    return np.nan


def agg_wait_completion_status(series: pd.Series):
    if len(set(series)) == 1:
        if series.iloc[0] == 1:
            return 'YES'
        else:
            return 'NO'
    else:
        return 'MIX'


def max_processor_weight(series: pd.Series):
    if (series != 65535).any():
        return str(series[series != 65535].max())
    else:
        return np.nan


def any_1(series: pd.Series):
    if (series == 1).any():
        return 'Y'
    else:
        return 'N'


def any_gt_0(series: pd.Series):
    if (series > 0).any():
        return 'Y'
    else:
        return 'N'


def agg_sum_processor_weight(series):
    return sum([int(x) for x in series if not pd.isna(x) and x != 65535 and x not in ('DED', 'DMX', 'WMX')])

def calculate_std_dev(count: int, sum_of_square_x: Union[int, float, str], val: Union[int, float], unit=1) -> float:
    if pd.isna(sum_of_square_x):
        return np.nan
    elif count <= 1:
        return 0.
    else:
        if not isinstance(sum_of_square_x, str):
            sum_of_square = sum_of_square_x
        else:
            sum_of_square = int(sum_of_square_x, 0)
        if ((count * sum_of_square) - val ** 2) > 0:
            return math.sqrt((count * sum_of_square - val ** 2) / (count * (count - 1))) / unit
        else:
            return 0.


def time_diff(t1, t2):
    if (t1 is not pd.NaT) and (t2 is not pd.NaT):
        return pd.to_timedelta(t1 - t2)/np.timedelta64(1, 's')
    else:
        return np.nan


def get_lpar_info_in_db(sysplex_name, system_name, lpar_number, db_session):
    try:
        lpar_info = db_session.execute(select(SmfLpar).filter(
            and_(SmfLpar.sysplex_name == sysplex_name,
                 SmfLpar.system_name == system_name,
                 SmfLpar.lpar_number == lpar_number.astype(INTEGER))).options(set_shard_id('smf.0'))).scalar()
        if lpar_info is not None:
            return lpar_info.csc, lpar_info.smf70cpa_actual, lpar_info.smf70cpa_scaling_factor
        else:
            return np.nan, np.nan, np.nan
    except Exception as e:
        click.secho(
            f"\nThis smf type cannot be processed until Smf70 have been initialized and the corresponding Smf70 Subtype 1 records have been processed.",
            err=True,
            fg="red"
            )
        raise SystemExit(1)



def check_changed_dtypes(dtype_dict: dict, df: pd.DataFrame) -> list:
    """
    Check for changed dtypes in a DataFrame
    """
    _df = df.copy(deep=True)

    changed_dtypes: list = []
    if dtype_dict is not None:
        for column in _df.columns:
            if column in dtype_dict.keys():
                if (isinstance(dtype_dict[column], sqlalchemy.types.INTEGER) or
                        isinstance(dtype_dict[column], sqlalchemy.types.BIGINT)):
                    if pd.api.types.is_object_dtype(_df[column].dtype) or _df[column].dtype == np.float64:
                        changed_dtypes.append(column)
    return changed_dtypes

def insert_on_conflict_do_update(table, conn, keys, data_iter):
    data = [dict(zip(keys, row)) for row in data_iter]

    insert_statement = sqlalchemy.dialects.postgresql.insert(table.table).values(data)
    upsert_statement = insert_statement.on_conflict_do_update(
        constraint=f"pk__{table.table.name}",
        set_={col.key: col for col in insert_statement.excluded},
    )
    conn.execute(upsert_statement)

def get_sqlite_max_variable_number(db_engine):
    try:
        with db_engine.connect() as conn:
            cursor = conn.connection.cursor()
            options = cursor.execute("PRAGMA compile_options").fetchall()
            for option in options:
                if "MAX_VARIABLE_NUMBER" in option[0]:
                    return int(option[0].split("=")[1])
            return 32766
    except Exception as e:
        raise click.ClickException(
            f"An error occurred while getting the sqlite maximum variable number: {str(e)}"
        )


def df_upsert(db_driver, db_engine, db_session, df, table_name, table_class, schema, index_cols,
              dtype_dict=None, shard_id=None):
    _df = df.copy().dropna(axis=1, how='all')
    if 'pg8000' in db_driver:
        int_cols = [k for k in dtype_dict.keys() if k in _df.columns]
        int_dtype_dict = _df[int_cols].dtypes.to_dict()
        if len(set(int_dtype_dict.values())) != 1 or next(iter(int_dtype_dict.values()), None) != np.dtype('int64'):
            target_cols = []
            for col in int_dtype_dict.keys():
                if int_dtype_dict[col] != np.dtype('int64'):
                    target_cols.append(col)
            if len(target_cols) > 0:
                for col in target_cols:
                    try:
                        _df[col] = _df[col].astype(np.int64)
                    except Exception as e:
                        try:
                            _df[col] = _df[col].astype('Int64')
                        except Exception as e:
                            raise click.ClickException(
                                f'An error occurred while converting {col} to integers in table {table_name}: {str(e)}')
    columns_count = len(_df.columns)
    if db_driver == 'sqlite':
        max_variable_number = get_sqlite_max_variable_number(db_engine)
    else:
        max_variable_number = 65535
    chunk_size = max_variable_number // columns_count
    data = _df.replace([np.nan], [None], regex=False).to_dict('records')
    chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
    for chunk in chunks:
        if db_driver == 'sqlite':
            insert_statement = sqlalchemy.dialects.sqlite.insert(table_class).values(chunk)
        else:
            insert_statement = sqlalchemy.dialects.postgresql.insert(table_class).values(chunk)
        upsert_statement = insert_statement.on_conflict_do_update(
            index_elements=index_cols,
            set_={col: getattr(insert_statement.excluded, col) for col in _df.columns},
        )
        if shard_id is not None:
            try:
                db_session.execute(upsert_statement.options(set_shard_id(shard_id)))
                db_session.commit()
            except Exception as e:
                db_session.rollback()
                raise click.ClickException(
                    f"An error occurred while upserting the records to table {table_name}: {str(e)}")
        else:
            try:
                db_session.execute(upsert_statement)
                db_session.commit()
            except Exception as e:
                db_session.rollback()
                raise click.ClickException(
                    f"An error occurred while upserting the records to table {table_name}: {str(e)}")
    result = len(data)
    return result #_df.shape[0]

def df_upsert_by_partitions(db_driver, db_engines, db_session, input_df, table_name, table_class, schema, index_cols,
                            smf_type, parts='weekday', dtype_dict=None):
    _df = input_df.copy().dropna(axis=1, how='all')
    if 'pg8000' in db_driver:
        int_cols = [k for k in dtype_dict.keys() if k in _df.columns]
        int_dtype_dict = _df[int_cols].dtypes.to_dict()
        if len(set(int_dtype_dict.values())) != 1 or next(iter(int_dtype_dict.values()), None) != np.dtype('int64'):
            target_cols = []
            for col in int_dtype_dict.keys():
                if int_dtype_dict[col] != np.dtype('int64'):
                    target_cols.append(col)
            if len(target_cols) > 0:
                for col in target_cols:
                    try:
                        _df[col] = _df[col].astype(np.int64)
                    except Exception as e:
                        try:
                            _df[col] = _df[col].astype('Int64')
                        except Exception as e:
                            raise click.ClickException(f'An error occurred while converting {col} to integers in table {table_name}: {str(e)}')
    df_columns = _df.columns
    if parts == 'weekday':
        _df['partition'] = _df['datetime'].dt.isocalendar().day
        df_gp = _df.groupby(['partition'])
    elif parts == 'week':
        _df['partition'] = _df['datetime'].dt.isocalendar().week
        df_gp = _df.groupby(['partition'])
    elif parts == 'day':
        _df['partition'] = _df['datetime'].dt.day
        df_gp = _df.groupby(['partition'])
    else:
        _df['partition'] = 1  # single partition
        df_gp = _df.groupby(['partition'])
    total_recs = 0
    for group, df in df_gp:
        part = group[0]
        columns_count = len(df_columns)
        if db_driver == 'sqlite':
            max_variable_number = get_sqlite_max_variable_number(db_engines['smf.0'])
        else:
            max_variable_number = 65535
        chunk_size = max_variable_number // columns_count

        data = df.drop('partition', axis=1).replace([np.nan], [None], regex=False).to_dict('records')
        chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
        i_chunk = 0
        for chunk in chunks:
            if db_driver == 'sqlite':
                insert_statement = sqlalchemy.dialects.sqlite.insert(table_class).values(chunk)
            else:
                insert_statement = sqlalchemy.dialects.postgresql.insert(table_class).values(chunk)
            upsert_statement = insert_statement.on_conflict_do_update(
                index_elements=index_cols,
                set_={col: getattr(insert_statement.excluded, col) for col in df_columns},
            )

            try:
                db_session.execute(upsert_statement.options(set_shard_id(f'{smf_type}.{part}')))
                db_session.commit()
                i_chunk += 1
            except IntegrityError:
                db_session.rollback()
                raise click.ClickException(
                    f'Duplicate records found while upserting the records of chunk {i_chunk} in table {table_name}.')
            except Exception as e:
                db_session.rollback()
                raise click.ClickException(
                    f"An error occurred while upserting the records of chunk {i_chunk} in table {table_name}: {str(e)}")
        total_recs += len(data)
    return _df.shape[0]

def df_insert_by_partitions(db_driver, db_engines, db_session, input_df, table_name, table_class, schema, dtype_dict,
                            smf_type, parts='weekday', drop_duplicate=False):
    _df = input_df.copy().dropna(axis=1, how='all')
    if 'pg8000' in db_driver:
        int_cols = [k for k in dtype_dict.keys() if k in _df.columns]
        int_dtype_dict = _df[int_cols].dtypes.to_dict()
        if len(set(int_dtype_dict.values())) != 1 or next(iter(int_dtype_dict.values()), None) != np.dtype('int64'):
            target_cols = []
            for col in int_dtype_dict.keys():
                if int_dtype_dict[col] != np.dtype('int64'):
                    target_cols.append(col)
            if len(target_cols) > 0:
                for col in target_cols:
                    try:
                        _df[col] = _df[col].astype(np.int64)
                    except Exception as e:
                        try:
                            _df[col] = _df[col].astype('Int64')
                        except Exception as e:
                            raise click.ClickException(f'An error occurred while converting {col} to integers in table {table_name}: {str(e)}')
    if parts == 'weekday':
        _df['partition'] = _df['datetime'].dt.isocalendar().day
        df_gp = _df.groupby(['partition'])
    elif parts == 'week':
        _df['partition'] = _df['datetime'].dt.isocalendar().week
        df_gp = _df.groupby(['partition'])
    elif parts == 'day':
        _df['partition'] = _df['datetime'].dt.day
        df_gp = _df.groupby(['partition'])
    else:
        _df['partition'] = 1 # single partition
        df_gp = _df.groupby(['partition'])
    total_recs = 0
    if db_driver == 'sqlite':
        max_variable_number = get_sqlite_max_variable_number(db_engines['smf.0'])
    elif 'postgresql' in db_driver:
        max_variable_number = 65535
    else:
        max_variable_number = 32766
    for group, df in df_gp:
        part = group[0]
        columns_count = len(_df.columns)
        chunk_size = max_variable_number // columns_count

        if drop_duplicate:
            data = df[[column for column in df.columns if column in
                       table_class.__table__.columns.keys()]].drop_duplicates().replace(
                [np.nan], [None], regex=False).to_dict('records')
        else:
            data = df[[column for column in df.columns if column in
                table_class.__table__.columns.keys()]].replace([np.nan], [None], regex=False).to_dict('records')
        chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
        i_chunk = 0
        for chunk in chunks:
            try:
                stmt = table_class.__table__.insert().values(chunk).options(set_shard_id(f'{smf_type}.{part}'))
                db_session.execute(stmt.execution_options(render_nulls=True))
                db_session.commit()
                i_chunk += 1
            except IntegrityError:
                db_session.rollback()
                raise click.ClickException(f'Duplicate records found while adding the records of chunk {i_chunk} in table {table_name}.')
            except Exception as e:
                db_session.rollback()
                raise click.ClickException(f"An error occurred while adding the records of chunk {i_chunk} in table {table_name}: {str(e)}")
        total_recs += len(data)
    return total_recs


def sum_up_by_partition(tbl_class: Callable, summary_class: Callable, summary_tbl_name: str,
                        start: dt.datetime, end: dt.datetime, update_time: dt.datetime,
                        target_agg_dict: dict, dtype_dict: dict, partitions_scheme: str, summary_engine: str,
                        db_engines: dict, smf_type: str, schema: str,
                        db_session: Session, db_driver: str ='sqlite'):
    """Summing up interval data from JSON files to the summary tables.

    Args:
        tbl_class (Class): Target interval table class.
        summary_class (Class): Target summary class.
        summary_tbl_name (str): Target summary table name.
        start (dt.datetime): Start summary time.
        end (dt.datetime): End summary time.
        update_time (dt.datetime): current update time.
        target_agg_dict (dict): Target table aggregation dict.
        dtype_dict (dict): Target table dtype dict.
        partitions_scheme (str): Target partitions scheme ('weekday', 'day').
        summary_engine (str): Target summary engine identifier.
        db_engines (dict): Dictionary of SQLAlchemy engine instance.
        smf_type (str): Target smf type.
        schema (str): Target table schema name.
        db_session (sqlalchemy.orm.session.Session): SQLAlchemy session instance.
        db_driver (str): Target database driver name.
    """
    set_datetime = np.vectorize(setdatetime)
    df_sum_list = []
    result = 0
    if partitions_scheme == 'weekday':
        partitions = range(1, 8)
    elif partitions_scheme == 'day':
        partitions = range(1, 32)
    elif partitions_scheme == 'week':
        partitions = range(1, 53)
    else:
        partitions = range(1, 2)
    null_column_list = []
    for part in partitions:
        stmt = select(tbl_class).where(tbl_class.datetime.between(start, end))
        df_interval = pd.read_sql(stmt, db_engines[f'{smf_type}.{part}'])
        if not df_interval.empty:
            df_interval['date'] = df_interval['datetime'].dt.date
            null_columns = df_interval.columns[df_interval.isna().all()].tolist()
            df_sum_list.append(df_interval)
            for col in null_columns:
                if col not in null_column_list:
                    null_column_list.append(col)
    if len(df_sum_list) > 0:
        if len(df_sum_list) > 1:
            cleaned_list_of_dfs = [df.dropna(axis=1, how='all') for df in df_sum_list]
            df_intervals = pd.concat(cleaned_list_of_dfs)
            if len(null_column_list) > 0:
                new_cols = df_intervals.columns.tolist()
                for col in null_column_list:
                    if col not in new_cols:
                        new_cols.append(col)
                df_intervals = df_intervals.reindex(columns=new_cols)
        else:
            df_intervals = df_sum_list[0]

        df_sum = df_intervals.groupby(
            [col.name for col in summary_class.__table__.primary_key.columns.values()]).agg(
            target_agg_dict).copy().reset_index()
        if 'datetime_15m' in df_sum.columns:
            if 'datetime' not in df_sum.columns:
                df_sum['datetime'] = set_datetime(df_sum['datetime_15m'])
        if 'date' not in df_sum.columns:
            if 'datetime' in df_sum.columns:
                df_sum['date'] = df_sum['datetime'].dt.date
            else:  # 'datetime_15m' in df_sum.columns:
                df_sum['date'] = df_sum['datetime_15m'].dt.date

        df_sum['last_update_time'] = update_time
        result = df_upsert(db_driver, db_engines[f'{summary_engine}'], db_session,
                           df_sum[summary_class.__table__.columns.keys()],
                           summary_tbl_name, summary_class, schema,
                           [col.name for col in summary_class.__table__.primary_key.columns.values()],
                           dtype_dict, shard_id=summary_engine
                           )
    return result


def create_dtypedict(tbls: dict):
    dtypedict = {}
    for tbl in tbls.keys():
        dtypedict[tbl] = {}
        for c in tbls[tbl].__table__.columns:
            if 'INTEGER' in str(c.type):
                dtypedict[tbl].update({c.name: sqlalchemy.types.INTEGER()})
            elif 'REAL' in str(c.type):
                dtypedict[tbl].update({c.name: sqlalchemy.types.REAL()})
            elif 'BIGINT' in str(c.type):
                dtypedict[tbl].update({c.name: sqlalchemy.types.BIGINT()})
            elif 'VARCHAR' in str(c.type):
                dtypedict[tbl].update({c.name: sqlalchemy.types.VARCHAR()})
    return dtypedict

def create_int_dtypedict(tbls: dict):
    dtypedict = {}
    for tbl in tbls.keys():
        dtypedict[tbl] = {}
        for c in tbls[tbl].__table__.columns:
            if 'INTEGER' in str(c.type):
                dtypedict[tbl].update({c.name: sqlalchemy.types.INTEGER()})
            # elif 'REAL' in str(c.type):
            #     dtypedict[tbl].update({c.name: sqlalchemy.types.REAL()})
            elif 'BIGINT' in str(c.type):
                dtypedict[tbl].update({c.name: sqlalchemy.types.BIGINT()})
            # elif 'VARCHAR' in str(c.type):
            #     dtypedict[tbl].update({c.name: sqlalchemy.types.VARCHAR()})
    return dtypedict

def format_time(t_str: str) -> str:
    hh, mm, ss, ff = t_str.split('.')
    if hh == '00':
        if mm == '00':
            if ss == '00':
                return f"{ff.lstrip('0'):01}"
            else:
                return f"{ss.lstrip('0'):01}.{ff:06}"
        else:
            return f"{mm.lstrip('0'):01}.{ss:02}.{ff:06}"
    else:
        return f"{hh.lstrip('0')}.{mm}.{ss:02}.{ff:06}"
