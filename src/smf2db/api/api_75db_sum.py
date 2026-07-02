import datetime as dt
import time

import numpy as np
import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from smf2db import SUCCESS
from smf2db.api.util import (agg_boost, UploadResult, create_int_dtypedict,
                             df_upsert, is_bit_set)
from smf2db.db_models.smf75_da_model import Smf75ProDa, Smf75PsdDa
from smf2db.db_models.smf75_hr_model import Smf75ProHr, Smf75PsdHr
from smf2db.db_models.smf75_model import Smf75Pro, Smf75Psd

tbls = {'pro': Smf75Pro,
        'psd': Smf75Psd}
tbls_hr = {'pro': Smf75ProHr,
           'psd': Smf75PsdHr}
tbls_da = {'pro': Smf75ProDa,
           'psd': Smf75PsdDa}
tblnames = {'pro': 'smf75_pro',
            'psd': 'smf75_psd'}
tblnames_hr = {'pro': 'smf75_pro_hr',
               'psd': 'smf75_psd_hr'}
tblnames_da = {'pro': 'smf75_pro_da',
               'psd': 'smf75_psd_da'}

int_dtypedict = create_int_dtypedict(tbls)


agg_pro = {'smf75flg': 'first',
           'smf75gie': 'last', 'smf75mfv': 'last', 'smf75int': 'sum', 'smf75sam': 'sum', 'smf75cyc': 'last',
           'smf75mvs': 'last', 'smf75iml': 'last', 'smf75ptn': 'last', 'smf75srl': 'last', 'smf75lgo': 'last',
           'smf75oil': 'last', 'smf75syn': 'last', 'smf75xnm': 'last', 'smf75snm': 'last', 'speed_boost': agg_boost,
           'ziip_boost': agg_boost, 'smf75prd': 'last', 'smf75fla': 'last', 'smf75prf': 'last',
           }
agg_psd = {'smf75int': 'sum', 'smf75sam': 'sum', 'lpa': 'first', 'com': 'first', 'loc': 'first', 'dsb': 'first',
           'onl': 'first', 'ofl': 'first', 'ds_accepts_vio': 'first', 'ds_on_alt_control_unit': 'first',
           'device_name_valid': 'first', 'page_space_scm': 'first', 'smf75typ': 'first', 'smf75cha': 'first',
           'smf75vol': 'first', 'smf75scs': 'first', 'smf75sla': 'first', 'smf75mxu': 'max', 'smf75mnu': 'min',
           'smf75avu': 'mean', 'smf75bds': 'last', 'smf75use': 'sum', 'smf75req': 'sum', 'smf75sio': 'sum',
           'smf75pgx': 'sum', 'smf75dev': 'first', 'smf75cu': 'first', 'smf75lvu': 'mean', 'smf_type': 'first',
           'smf75pst': 'first', 'smf75fl2': 'first'}

def sum_75db(db_engines: dict, db_session: Session, summary_level: str, start_time_str: str, end_time_str: str,
             partitions_scheme: str, db_driver: str = 'postgresql+psycopg2') -> UploadResult:
    """Summarize smf75 interval database to the hourly or daily database.

    Args:
        db_engines: A dictionary of all the db_engines in the database.
        db_session: SQLAlchemy session.
        summary_level: Summary level of data (hourly, daily).
        start_time_str: Start time of summary.
        end_time_str: End time of summary.
        partitions_scheme: Partitions scheme.
        db_driver: Db driver to connect to database.

    Returns:
        A NamedTuple including the insert dictionary, total elapsed time of the upload and the return code.
    """
    overall_st = time.time()

    start = pd.to_datetime(start_time_str)
    end = pd.to_datetime(end_time_str)

    if partitions_scheme == 'weekday':
        partitions_range = range(1, 8)
    elif partitions_scheme == 'day':
        partitions_range = range(1, 32)
    elif partitions_scheme == 'week':
        partitions_range = range(1, 53)
    else:
        partitions_range = range(1, 2)

    insert_dict = {'pro': 0, 'psd': 0}
    summary_class = {'hourly': tbls_hr, 'daily': tbls_da}
    summary_tblname = {'hourly': tblnames_hr, 'daily': tblnames_da}
    summary_engine = {'hourly': '75.hourly', 'daily': '75.daily'}

    result_list = []

    st = time.time()
    current_time = dt.datetime.now()

    # Summing up Smf75Pro
    df_pro_list = []
    pro_stmt = select(Smf75Pro).where(Smf75Pro.datetime.between(start, end))
    for part in partitions_range:
        df_pro = pd.read_sql(pro_stmt, db_engines[f'75.{part}'])
        if not df_pro.empty:
            df_pro['date'] = df_pro['datetime'].dt.date
            df_pro_list.append(df_pro)
    if len(df_pro_list) > 0:
        df_pros = pd.concat(df_pro_list)
        df_pros['speed_boost'] = df_pros['smf75fla'].apply(lambda x: is_bit_set(x, 16, 10) if pd.notna(x) else np.nan)
        df_pros['ziip_boost'] = df_pros['smf75fla'].apply(
            lambda x: is_bit_set(x, 16, 9) if pd.notna(x) else np.nan)
        df_pro_sum = df_pros.groupby(
            [col.name for col in summary_class[summary_level]['pro'].__table__.primary_key.columns.values()]).agg(
            agg_pro).reset_index()
        if 'date' not in df_pro_sum.columns:
            df_pro_sum['date'] = df_pro_sum['datetime'].dt.date
        df_pro_sum['last_update_time'] = current_time
        df_pro_sum[['speed_boost', 'speed_boost_change']] = pd.DataFrame(df_pro_sum['speed_boost'].tolist(),
                                                                         index=df_pro_sum.index)
        df_pro_sum[['ziip_boost', 'ziip_boost_change']] = pd.DataFrame(df_pro_sum['ziip_boost'].tolist(),
                                                                       index=df_pro_sum.index)
        insert_dict['pro'] = df_upsert(db_driver, db_engines[summary_engine[summary_level]], db_session,
                                       df_pro_sum[summary_class[summary_level]['pro'].__table__.columns.keys()],
                                       summary_tblname[summary_level]['pro'], summary_class[summary_level]['pro'],
                                       'smf75',
                                       [col.name for col in
                                        summary_class[summary_level]['pro'].__table__.primary_key.columns.values()],
                                       int_dtypedict['pro'], shard_id=summary_engine[summary_level]
                                       )
    # Summing up Smf75Psd
    df_psd_list = []
    null_column_list = []
    psd_stmt = select(Smf75Psd).where(Smf75Psd.datetime.between(start, end))
    for part in partitions_range:
        psd = pd.read_sql(psd_stmt, db_engines[f'75.{part}'])
        if not psd.empty:
            psd['date'] = psd['datetime'].dt.date
            df_psd_list.append(psd)
            null_columns = psd.columns[psd.isna().all()].tolist()
            for col in null_columns:
                if col not in null_column_list:
                    null_column_list.append(col)
    if len(df_psd_list) > 0:
        df_psds = pd.concat([df.dropna(axis=1, how='all') for df in df_psd_list])
        if len(null_column_list) > 0:
            new_cols = df_psds.columns.tolist()
            for col in null_column_list:
                if col not in new_cols:
                    new_cols.append(col)
            df_psds = df_psds.reindex(columns=new_cols)
        df_psd_sum = df_psds.groupby(
            [col.name for col in summary_class[summary_level]['psd'].__table__.primary_key.columns.values()]).agg(
            agg_psd).reset_index()
        if 'date' not in df_psd_sum.columns:
            df_psd_sum['date'] = df_psd_sum['datetime'].dt.date
        df_psd_sum['last_update_time'] = current_time
        df_psd_sum['psbsy'] = df_psd_sum['smf75use'] * 100 / df_psd_sum['smf75sam']
        df_psd_sum['psptt'] = ((df_psd_sum['smf75req'] * df_psd_sum['smf75int']) / df_psd_sum['smf75sam']) / df_psd_sum[
            'smf75pgx']
        df_psd_sum['pspt'] = df_psd_sum['smf75pgx'] / df_psd_sum['smf75int']
        df_psd_sum['psart'] = df_psd_sum['smf75sio'] / df_psd_sum['smf75int']
        insert_dict['psd'] = df_upsert(db_driver, db_engines[summary_engine[summary_level]], db_session,
                                       df_psd_sum[summary_class[summary_level]['psd'].__table__.columns.keys()],
                                       summary_tblname[summary_level]['psd'], summary_class[summary_level]['psd'],
                                       'smf75',
                                       [col.name for col in
                                        summary_class[summary_level]['psd'].__table__.primary_key.columns.values()],
                                       int_dtypedict['psd'], shard_id=summary_engine[summary_level]
                                       )

    result_list.append({summary_tblname[summary_level][k]:v for k,v in insert_dict.items() if k in summary_tblname[summary_level].keys()})

    et = time.time()  # get the end time
    # get the execution time
    elapsed_time = (et - st) / 60
    print(f'Execution time ({summary_level}):', elapsed_time, 'minutes')

    overall_et = time.time()
    overall_elapsed_time = (overall_et - overall_st) / 60
    return UploadResult(result_list, overall_elapsed_time, SUCCESS)

