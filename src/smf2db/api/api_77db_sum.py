import datetime as dt
import time

import numpy as np
import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from smf2db import SUCCESS
from smf2db.api.util import (agg_boost, UploadResult, create_int_dtypedict,
                             df_upsert, sum_up_by_partition, is_bit_set)
from smf2db.db_models.smf77_da_model import Base77Da, Smf77ProDa, Smf77CtlDa, Smf77EnqDa
from smf2db.db_models.smf77_hr_model import Base77Hr, Smf77ProHr, Smf77CtlHr, Smf77EnqHr
from smf2db.db_models.smf77_model import Smf77Pro, Smf77Ctl, Smf77Enq

tbls = {'pro': Smf77Pro,
        'ctl': Smf77Ctl,
        'enq': Smf77Enq}
tbls_hr = {'pro': Smf77ProHr,
           'ctl': Smf77CtlHr,
           'enq': Smf77EnqHr}
tbls_da = {'pro': Smf77ProDa,
           'ctl': Smf77CtlDa,
           'enq': Smf77EnqDa}
tblnames = {'pro': 'smf77_pro',
           'ctl': 'smf77_ctl',
           'enq': 'smf77_enq'}
tblnames_hr = {'pro': 'smf77_pro_hr',
               'ctl': 'smf77_ctl_hr',
               'enq': 'smf77_enq_hr'}
tblnames_da = {'pro': 'smf77_pro_da',
               'ctl': 'smf77_ctl_da',
               'enq': 'smf77_enq_da'}

int_dtypedict = create_int_dtypedict(tbls)

agg_dict = {
    'pro': {'smf77flg': 'first',
           'smf77gie': 'last', 'smf77mfv': 'last', 'smf77int': 'sum', 'smf77sam': 'sum', 'smf77cyc': 'last',
           'smf77mvs': 'last', 'smf77iml': 'last', 'smf77ptn': 'last', 'smf77srl': 'last', 'smf77lgo': 'last',
           'smf77oil': 'last', 'smf77syn': 'last', 'smf77xnm': 'last', 'smf77snm': 'last', 'speed_boost': agg_boost,
           'ziip_boost': agg_boost,
           'smf77prd': 'last', 'smf77fla': 'last', 'smf77prf': 'last'},
    'ctl': {'resource_no_contention': 'last', 'enqueue_bad_cpu_clock': 'last', 'enqueue_processing_abend': 'last',
               'detail_data_req': 'last', 'grs_none': 'last', 'grs_ring': 'last', 'grs_mode': 'last',
               'grs_sys_problem': 'last', 'grs_interface_problem': 'last',
               'smf_type': 'first', 'smf77fg1': 'last', 'smf77rf2': 'last'},
    'enq': {'smf77wtm': 'min', 'smf77wtx': 'max', 'smf77wtt': 'sum', 'smf77ql1': 'max', 'smf77ql2': 'max',
               'smf77ql3': 'max', 'smf77ql4': 'max', 'smf77exm': 'min', 'smf77exx': 'max', 'smf77shm': 'min',
               'smf77shx': 'max', 'smf77evt': 'sum', 'smf77dow': 'sum', 'smf77dwr': 'sum', 'smf77aql': 'sum',
               'smf77csc': 'sum', 'smf77nod': 'sum'}
}


def sum_77db(db_engines: dict, db_session: Session, summary_level: str, start_time_str: str, end_time_str: str,
             partitions_scheme: str, db_driver: str = 'postgresql+psycopg2') -> UploadResult:
    """Summarize smf77 interval database to the hourly or daily database.

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

    insert_dict = {'ctl': 0, 'enq': 0, 'pro': 0}
    summary_class = {'hourly': tbls_hr, 'daily': tbls_da}
    summary_tblname = {'hourly': tblnames_hr, 'daily': tblnames_da}
    summary_engine = {'hourly': '77.hourly', 'daily': '77.daily'}

    result_list = []

    st = time.time()
    current_time = dt.datetime.now()

    # Summing up Smf77Ctl
    insert_dict['ctl'] = sum_up_by_partition(tbls['ctl'], summary_class[summary_level]['ctl'],
                                             summary_tblname[summary_level]['ctl'],
                                             start, end, current_time, agg_dict['ctl'], int_dtypedict['ctl'],
                                             partitions_scheme, summary_engine[summary_level],
                                             db_engines, '77', 'smf77', db_session, db_driver)

    # Summing up Smf77Pro
    df_pro_list = []
    pro_stmt = select(Smf77Pro).where(Smf77Pro.datetime.between(start, end))
    for part in partitions_range:
        df_pro = pd.read_sql(pro_stmt, db_engines[f'77.{part}'])
        if not df_pro.empty:
            df_pro['date'] = df_pro['datetime'].dt.date
            df_pro_list.append(df_pro)
    if len(df_pro_list) > 0:
        df_pros = pd.concat(df_pro_list)
        df_pros['speed_boost'] = df_pros['smf77fla'].apply(lambda x: is_bit_set(x, 16, 10) if pd.notna(x) else np.nan)
        df_pros['ziip_boost'] = df_pros['smf77fla'].apply(
            lambda x: is_bit_set(x, 16, 9) if pd.notna(x) else np.nan)
        df_pro_sum = df_pros.groupby(
            [col.name for col in summary_class[summary_level]['pro'].__table__.primary_key.columns.values()]).agg(
            agg_dict['pro']).reset_index()
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
                                       'smf77',
                                       [col.name for col in
                                        summary_class[summary_level]['pro'].__table__.primary_key.columns.values()],
                                       int_dtypedict['pro'], shard_id=summary_engine[summary_level]
                                       )
    # Summing up Smf77Enq
    insert_dict['enq'] = sum_up_by_partition(tbls['enq'], summary_class[summary_level]['enq'],
                                             summary_tblname[summary_level]['enq'],
                                             start, end, current_time, agg_dict['enq'], int_dtypedict['enq'],
                                             partitions_scheme, summary_engine[summary_level],
                                             db_engines, '77', 'smf77', db_session, db_driver)

    result_list.append({summary_tblname[summary_level][k]:v for k,v in insert_dict.items() if k in summary_tblname[summary_level].keys()})

    et = time.time()  # get the end time
    # get the execution time
    elapsed_time = (et - st) / 60
    print(f'Execution time ({summary_level}):', elapsed_time, 'minutes')

    overall_et = time.time()
    overall_elapsed_time = (overall_et - overall_st) / 60
    return UploadResult(result_list, overall_elapsed_time, SUCCESS)

