import datetime as dt
import time

import numpy as np
import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from smf2db import SUCCESS
from smf2db.api.util import (setdatetime, v_index, agg_tolist, list_loc, count_items, mean_items, max_items,
                             UploadResult, create_int_dtypedict, df_upsert, sum_up_by_partition)
from smf2db.db_models.smf1101_agg_dict import agg_110
from smf2db.db_models.smf123_15m_model import Smf110Smf12315m, Smf123Server15m, Smf123RequestData15m
from smf2db.db_models.smf123_da_model import Smf110Smf123Da, Smf123ServerDa, Smf123RequestDataDa
from smf2db.db_models.smf123_hr_model import Smf110Smf123Hr, Smf123ServerHr, Smf123RequestDataHr
from smf2db.db_models.smf123_model import Smf110Smf123, Smf123Server, Smf123RequestData


def agg_fail(series):
    s_bool = (series > 299)
    return s_bool.sum()

tbls = {'server': Smf123Server,
        'data': Smf123RequestData,
        'cics': Smf110Smf123}
tbls_da = {'server': Smf123ServerDa, 'data': Smf123RequestDataDa, 'cics': Smf110Smf123Da}
tbls_hr = {'server': Smf123ServerHr, 'data': Smf123RequestDataHr, 'cics': Smf110Smf123Hr}
tbls_15m = {'server': Smf123Server15m, 'data': Smf123RequestData15m, 'cics': Smf110Smf12315m}
tblnames = {'server': 'smf123_server', 'data': 'smf123_request_data', 'cics': 'smf110_123'}
tblnames_da = {'server': 'smf123_server_da', 'data': 'smf123_request_data_da', 'cics': 'smf110_123_da'}
tblnames_hr = {'server': 'smf123_server_hr', 'data': 'smf123_request_data_hr', 'cics': 'smf110_123_hr'}
tblnames_15m = {'server': 'smf123_server_15m', 'data': 'smf123_request_data_15m', 'cics': 'smf110_123_15m'}
dtypedict = create_int_dtypedict(tbls)
dtypedict_15m = create_int_dtypedict(tbls_15m)
agg_server = {'smf123_ssi': 'last', 'smf123_subtype': 'last', 'smf123_subtype_version': 'last',
              'smf123_datetime_offset': 'last', 'smf123_server_sect_version': 'last',
              'smf123_server_feature_major': 'last', 'smf123_server_feature_minor': 'last',
              'smf123_server_system': 'last', 'smf123_server_stoken': 'last',
              'smf123_server_config_dir': 'last', 'smf123_server_version': 'last', }
agg_data = {'tasks': 'sum', 'smf123s1_tracking_token': 'count', 'smf123s1_http_resp_code': agg_fail,
            'timed_out': 'count',
            'smf123s1_req_method': agg_tolist, 'smf123s1_time_zc_entry': agg_tolist,
            'smf123s1_time_zc_exit': agg_tolist, 'smf123s1_time_sor_sent': agg_tolist,
            'smf123s1_time_sor_recv': agg_tolist, 'sent_late': agg_tolist, 'exit_late': agg_tolist,
            'sor_resp': agg_tolist, 'zc_resp': agg_tolist, 'zc_time': agg_tolist, 'smf123s1_req_id': agg_tolist}
agg_data_ = {'requests': 'sum', 'tasks': 'sum', 'fail': 'sum',
             'timed_out': 'sum', 'gets': 'sum', 'posts': 'sum', 'puts': 'sum', 'deletes': 'sum',
             'sor_sent_latency_avg': 'mean', 'sor_sent_latency_max': agg_tolist, 'sor_sent_latency_reqid': agg_tolist,
             'sor_sent_latency_zc_entry': agg_tolist, 'sor_response_avg': 'mean', 'sor_response_max': agg_tolist,
             'sor_response_reqid': agg_tolist, 'sor_response_zc_entry': agg_tolist, 'zc_exit_latency_avg': 'mean',
             'zc_exit_latency_max': agg_tolist, 'zc_exit_latency_reqid': agg_tolist,
             'zc_exit_latency_zc_entry': agg_tolist, 'zc_response_avg': 'mean', 'zc_response_max': agg_tolist,
             'zc_response_reqid': agg_tolist, 'zc_response_zc_entry': agg_tolist, 'zc_time_avg': 'mean',
             'zc_time_max': agg_tolist, 'zc_time_reqid': agg_tolist, 'zc_time_zc_entry': agg_tolist}


def sum_123db(db_engines: dict, db_session: Session, summary_level: str, start_time_str: str, end_time_str: str,
             partitions_scheme: str, db_driver: str = 'postgresql+psycopg2') -> UploadResult:
    """Summarize smf123 interval database to the 15-minutes, hourly or daily database.

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
    get_v_index = np.vectorize(v_index, otypes=[object])
    get_list_loc = np.vectorize(list_loc, otypes=[object])
    get_maxs = np.vectorize(max_items)
    get_counts = np.vectorize(count_items)
    get_means = np.vectorize(mean_items)

    if partitions_scheme == 'weekday':
        partitions_range = range(1, 8)
    elif partitions_scheme == 'day':
        partitions_range = range(1, 32)
    elif partitions_scheme == 'week':
        partitions_range = range(1, 53)
    else:
        partitions_range = range(1, 2)

    insert_dict = {'server': 0, 'data': 0, 'cics': 0}
    summary_class = {'15min': tbls_15m, 'hourly': tbls_hr, 'daily': tbls_da}
    summary_tblname = {'15min': tblnames_15m, 'hourly': tblnames_hr, 'daily': tblnames_da}
    summary_engine = {'15min': '123.15min', 'hourly': '123.hourly', 'daily': '123.daily'}

    update_agg_110 = agg_110.copy()
    update_agg_110.pop('cics_start', None)
    update_agg_110['tasks'] = 'sum'
    agg_data_sum = agg_data | update_agg_110

    result_list = []

    st = time.time()
    current_time = dt.datetime.now()

    # Summing up Smf110Smf123
    df_110_list = []
    null_column_list = []
    stmt_110 = select(Smf110Smf123).where(Smf110Smf123.datetime.between(start, end))
    for part in partitions_range:
        df_110 = pd.read_sql(stmt_110, db_engines[f'123.{part}'])
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
            [col.name for col in summary_class[summary_level]['cics'].__table__.primary_key.columns.values()]
        ).agg(agg_110).copy().reset_index().rename(columns={'cics_start': 'tasks'})
        if 'datetime_15m' in df_110_sum.columns:
            if 'datetime' not in df_110_sum.columns:
                df_110_sum['datetime'] = set_datetime(df_110_sum['datetime_15m'])
        if 'date' not in df_110_sum.columns:
            if 'datetime' in df_110_sum.columns:
                df_110_sum['date'] = df_110_sum['datetime'].dt.date
            else:  # 'datetime_15m' in df_110_sum.columns:
                df_110_sum['date'] = df_110_sum['datetime_15m'].dt.date

        df_110_sum['last_update_time'] = current_time
        insert_dict['cics'] = df_upsert(db_driver, db_engines[summary_engine[summary_level]], db_session,
                                        df_110_sum[summary_class[summary_level]['cics'].__table__.columns.keys()],
                                        summary_tblname[summary_level]['cics'],
                                        summary_class[summary_level]['cics'], 'smf123',
                                        [col.name for col in summary_class[summary_level]['cics'].__table__.primary_key.columns.values()],
                                        dtypedict['cics'], shard_id=summary_engine[summary_level],
                                        )
    # Summing up Server
    insert_dict['server'] = sum_up_by_partition(tbls['server'], summary_class[summary_level]['server'],
                                                summary_tblname[summary_level]['server'],
                                                start, end, current_time, agg_server, dtypedict['server'],
                                                partitions_scheme, summary_engine[summary_level],
                                                db_engines,'123', 'smf123', db_session, db_driver)

    # Summing up Data
    df_data_list = []
    null_column_list = []
    data_stmt = select(tbls['data']).where(tbls['data'].datetime.between(start, end))
    for part in partitions_range:
        df_data = pd.read_sql(data_stmt, db_engines[f'123.{part}'])
        if not df_data.empty:
            df_data['date'] = df_data['datetime'].dt.date
            df_data_list.append(df_data)
            null_columns = df_data.columns[df_data.isna().all()].tolist()
            for col in null_columns:
                if col not in null_column_list:
                    null_column_list.append(col)
    if len(df_data_list) > 0:
        df_datas = pd.concat([df.dropna(axis=1, how='all') for df in df_data_list])
        if len(null_column_list) > 0:
            new_cols = df_datas.columns.tolist()
            for col in null_column_list:
                if col not in new_cols:
                    new_cols.append(col)
            df_datas = df_datas.reindex(columns=new_cols)
        df_data_sum = df_datas.groupby(
            [col.name for col in summary_class[summary_level]['data'].__table__.primary_key.columns.values()]
            ).agg(agg_data_sum).copy().reset_index().rename(
                columns={'smf123s1_tracking_token': 'requests', 'smf123s1_http_resp_code': 'fail'})
        if 'datetime_15m' in df_data_sum.columns:
            if 'datetime' not in df_data_sum.columns:
                df_data_sum['datetime'] = set_datetime(df_data_sum['datetime_15m'])
        if 'date' not in df_data_sum.columns:
            if 'datetime' in df_data_sum.columns:
                df_data_sum['date'] = df_data_sum['datetime'].dt.date
            else:  # 'datetime_15m' in df_data_sum.columns:
                df_data_sum['date'] = df_data_sum['datetime_15m'].dt.date
        df_data_sum['gets'] = get_counts(df_data_sum['smf123s1_req_method'], 'GET')
        df_data_sum['posts'] = get_counts(df_data_sum['smf123s1_req_method'], 'POST')
        df_data_sum['puts'] = get_counts(df_data_sum['smf123s1_req_method'], 'PUT')
        df_data_sum['deletes'] = get_counts(df_data_sum['smf123s1_req_method'], 'DELETE')
        df_data_sum['sor_sent_latency_avg'] = get_means(df_data_sum['sent_late'])
        df_data_sum['sor_sent_latency_max'] = get_maxs(df_data_sum['sent_late'])
        df_data_sum['sor_sent_max_idx'] = get_v_index(df_data_sum['sent_late'])
        df_data_sum['sor_sent_latency_reqid'] = get_list_loc(df_data_sum['smf123s1_req_id'], df_data_sum['sor_sent_max_idx'])
        df_data_sum['sor_sent_latency_zc_entry'] = get_list_loc(df_data_sum['smf123s1_time_zc_entry'],
                                                              df_data_sum['sor_sent_max_idx'])
        df_data_sum['sor_response_avg'] = get_means(df_data_sum['sor_resp'])
        df_data_sum['sor_response_max'] = get_maxs(df_data_sum['sor_resp'])
        df_data_sum['sor_response_max_idx'] = get_v_index(df_data_sum['sor_resp'])
        df_data_sum['sor_response_reqid'] = get_list_loc(df_data_sum['smf123s1_req_id'], df_data_sum['sor_response_max_idx'])
        df_data_sum['sor_response_zc_entry'] = get_list_loc(df_data_sum['smf123s1_time_zc_entry'],
                                                          df_data_sum['sor_response_max_idx'])
        df_data_sum['zc_exit_latency_avg'] = get_means(df_data_sum['exit_late'])
        df_data_sum['zc_exit_latency_max'] = get_maxs(df_data_sum['exit_late'])
        df_data_sum['zc_exit_max_idx'] = get_v_index(df_data_sum['exit_late'])
        df_data_sum['zc_exit_latency_reqid'] = get_list_loc(df_data_sum['smf123s1_req_id'], df_data_sum['zc_exit_max_idx'])
        df_data_sum['zc_exit_latency_zc_entry'] = get_list_loc(df_data_sum['smf123s1_time_zc_entry'],
                                                             df_data_sum['zc_exit_max_idx'])
        df_data_sum['zc_response_avg'] = get_means(df_data_sum['zc_resp'])
        df_data_sum['zc_response_max'] = get_maxs(df_data_sum['zc_resp'])
        df_data_sum['zc_response_max_idx'] = get_v_index(df_data_sum['zc_resp'])
        df_data_sum['zc_response_reqid'] = get_list_loc(df_data_sum['smf123s1_req_id'], df_data_sum['zc_response_max_idx'])
        df_data_sum['zc_response_zc_entry'] = get_list_loc(df_data_sum['smf123s1_time_zc_entry'],
                                                         df_data_sum['zc_response_max_idx'])
        df_data_sum['zc_time_avg'] = get_means(df_data_sum['zc_time'])
        df_data_sum['zc_time_max'] = get_maxs(df_data_sum['zc_time'])
        df_data_sum['zc_time_max_idx'] = get_v_index(df_data_sum['zc_time'])
        df_data_sum['zc_time_reqid'] = get_list_loc(df_data_sum['smf123s1_req_id'], df_data_sum['zc_time_max_idx'])
        df_data_sum['zc_time_zc_entry'] = get_list_loc(df_data_sum['smf123s1_time_zc_entry'], df_data_sum['zc_time_max_idx'])
        df_data_sum['last_update_time'] = current_time
        insert_dict['data'] = df_upsert(db_driver, db_engines[summary_engine[summary_level]], db_session,
                                        df_data_sum[summary_class[summary_level]['data'].__table__.columns.keys()],
                                        summary_tblname[summary_level]['data'],
                                        summary_class[summary_level]['data'], 'smf123',
                                        [col.name for col in
                                         summary_class[summary_level]['data'].__table__.primary_key.columns.values()],
                                        dtypedict['data'], shard_id=summary_engine[summary_level],
                                        )

    result_list.append({summary_tblname[summary_level][k]:v for k,v in insert_dict.items() if k in summary_tblname[summary_level].keys()})

    et = time.time()  # get the end time
    # get the execution time
    elapsed_time = (et - st) / 60
    print(f'Execution time ({summary_level}):', elapsed_time, 'minutes')

    overall_et = time.time()
    overall_elapsed_time = (overall_et - overall_st) / 60
    return UploadResult(result_list, overall_elapsed_time, SUCCESS)

