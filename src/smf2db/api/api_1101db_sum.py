import datetime as dt
import time

import numpy as np
import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from smf2db import SUCCESS
from smf2db.api.util import UploadResult, create_int_dtypedict, df_upsert, setdatetime
from smf2db.db_models.smf1101_15m_model import Smf110115m
from smf2db.db_models.smf1101_agg_dict import agg_110
from smf2db.db_models.smf1101_da_model import Smf1101Da
from smf2db.db_models.smf1101_hr_model import Smf1101Hr
from smf2db.db_models.smf1101_model import Smf1101

tbls = {'dfhmntds': Smf1101}
tbls_15m = {'dfhmntds': Smf110115m}
tbls_hr = {'dfhmntds': Smf1101Hr}
tbls_da = {'dfhmntds': Smf1101Da}
tblnames = {'dfhmntds': 'smf110_1'}
tblnames_15m = {'dfhmntds': 'smf110_1_15m'}
tblnames_hr = {'dfhmntds': 'smf110_1_hr'}
tblnames_da = {'dfhmntds': 'smf110_1_da'}

int_dtypedict = create_int_dtypedict(tbls_15m)


def sum_1101db(db_engines: dict, db_session: Session, summary_level: str, start_time_str: str, end_time_str: str,
             partitions_scheme: str, db_driver: str = 'postgresql+psycopg2') -> UploadResult:
    """Summarize smf110 Subtype 1 interval database to the 15-minutes, hourly or daily database.

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
    set_datetime = np.vectorize(setdatetime)

    if partitions_scheme == 'weekday':
        partitions_range = range(1, 8)
    elif partitions_scheme == 'day':
        partitions_range = range(1, 32)
    elif partitions_scheme == 'week':
        partitions_range = range(1, 53)
    else:
        partitions_range = range(1, 2)

    insert_dict = {'dfhmntds': 0}
    summary_class = {'15min': tbls_15m, 'hourly': tbls_hr, 'daily': tbls_da}
    summary_tblname = {'15min': tblnames_15m, 'hourly': tblnames_hr, 'daily': tblnames_da}
    summary_engine = {'15min': '110_1.15min', 'hourly': '110_1.hourly', 'daily': '110_1.daily'}

    result_list = []

    st = time.time()
    current_time = dt.datetime.now()

    df_110_list = []
    null_column_list = []
    stmt_110 = select(Smf1101).where(Smf1101.datetime.between(start, end))
    for part in partitions_range:
        df_110 = pd.read_sql(stmt_110, db_engines[f'110_1.{part}'])
        if not df_110.empty:
            df_110['date'] = df_110['datetime'].dt.date
            df_110_list.append(df_110)
            null_columns = df_110.columns[df_110.isna().all()].tolist()
            for col in null_columns:
                if col not in null_column_list:
                    null_column_list.append(col)
    if len(df_110_list) > 0:
        df_110s = pd.concat([df.dropna(axis=1, how='all') for df in df_110_list])
        if len(null_column_list) > 0:
            new_cols = df_110s.columns.tolist()
            for col in null_column_list:
                if col not in new_cols:
                    new_cols.append(col)
            df_110s = df_110s.reindex(columns=new_cols)
        df_110_sum = df_110s.groupby(
            [col.name for col in summary_class[summary_level]['dfhmntds'].__table__.primary_key.columns.values()]
            ).agg(agg_110).copy().reset_index().rename(columns={'cics_start': 'tasks'})
        if 'datetime_15m' in df_110_sum.columns:
            if 'datetime' not in df_110_sum.columns:
                df_110_sum['datetime'] = set_datetime(df_110_sum['datetime_15m'])
        if 'date' not in df_110_sum.columns:
            if 'datetime' in df_110_sum.columns:
                df_110_sum['date'] = df_110_sum['datetime'].dt.date
            else: #'datetime_15m' in df_110_sum.columns:
                df_110_sum['date'] = df_110_sum['datetime_15m'].dt.date

        df_110_sum['last_update_time'] = current_time
        insert_dict['dfhmntds'] = df_upsert(db_driver, db_engines[summary_engine[summary_level]], db_session,
                                            df_110_sum[summary_class[summary_level]['dfhmntds'].__table__.columns.keys()],
                                            summary_tblname[summary_level]['dfhmntds'],
                                            summary_class[summary_level]['dfhmntds'],'smf110',
                                            [col.name for col in
                                             summary_class[summary_level]['dfhmntds'].__table__.primary_key.columns.values()],
                                            int_dtypedict['dfhmntds'], shard_id=summary_engine[summary_level],
                                            )

        result_list.append({summary_tblname[summary_level][k]:v for k,v in insert_dict.items() if k in summary_tblname[summary_level].keys()})

    et = time.time()  # get the end time
    # get the execution time
    elapsed_time = (et - st) / 60
    print(f'Execution time ({summary_level}):', elapsed_time, 'minutes')

    overall_et = time.time()
    overall_elapsed_time = (overall_et - overall_st) / 60
    return UploadResult(result_list, overall_elapsed_time, SUCCESS)

