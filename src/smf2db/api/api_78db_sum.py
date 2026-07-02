import datetime as dt
import time

import numpy as np
import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from smf2db import SUCCESS
from smf2db.api.util import (agg_boost,
                             agg_tolist, min_index, max_items, min_items,
                             list_loc, max_index, UploadResult, create_int_dtypedict, df_upsert, is_bit_set)
from smf2db.db_models.smf78_da_model import (Smf78ProDa, Smf78ComnDa, Smf78IoqDa, Smf78IopDa, Smf78AmgDa,
                                             Smf78ChaDa, Smf78LcuDa, Smf78ChapDa, Smf78PvtDa, Smf78PvspDa)
from smf2db.db_models.smf78_hr_model import (Smf78ProHr, Smf78ComnHr, Smf78IoqHr, Smf78IopHr, Smf78AmgHr,
                                             Smf78ChaHr, Smf78LcuHr, Smf78ChapHr, Smf78PvtHr, Smf78PvspHr)
from smf2db.db_models.smf78_model import (Smf78Pro, Smf78Comn, Smf78Ioq, Smf78Iop, Smf78Amg, Smf78Cha, Smf78Lcu,
                                          Smf78Chap, Smf78Pvt, Smf78Pvsp)

tbls = {'pro': Smf78Pro,
        'comn': Smf78Comn,
        'pvt': Smf78Pvt,
        'pvsp': Smf78Pvsp,
        'ioq': Smf78Ioq,
        'amg': Smf78Amg,
        'cha': Smf78Cha,
        'iop': Smf78Iop,
        'lcu': Smf78Lcu,
        'chap': Smf78Chap}
tbls_hr = {'pro': Smf78ProHr,
           'comn': Smf78ComnHr,
           'pvt': Smf78PvtHr,
           'pvsp': Smf78PvspHr,
           'ioq': Smf78IoqHr,
           'amg': Smf78AmgHr,
           'cha': Smf78ChaHr,
           'iop': Smf78IopHr,
           'lcu': Smf78LcuHr,
           'chap': Smf78ChapHr}
tbls_da = {'pro': Smf78ProDa,
           'comn': Smf78ComnDa,
           'pvt': Smf78PvtDa,
           'pvsp': Smf78PvspDa,
           'ioq': Smf78IoqDa,
           'amg': Smf78AmgDa,
           'cha': Smf78ChaDa,
           'iop': Smf78IopDa,
           'lcu': Smf78LcuDa,
           'chap': Smf78ChapDa}
tblnames = {'pro': 'smf78_pro',
            'comn': 'smf78_comn',
            'pvt': 'smf78_pvt',
            'pvsp': 'smf78_pvsp',
            'ioq': 'smf78_ioq',
            'amg': 'smf78_amg',
            'cha': 'smf78_cha',
            'iop': 'smf78_iop',
            'lcu': 'smf78_lcu',
            'chap': 'smf78_chap'}
tblnames_hr = {'pro': 'smf78_pro_hr',
               'comn': 'smf78_comn_hr',
               'pvt': 'smf78_pvt_hr',
               'pvsp': 'smf78_pvsp_hr',
               'ioq': 'smf78_ioq_hr',
               'amg': 'smf78_amg_hr',
               'cha': 'smf78_cha_hr',
               'iop': 'smf78_iop_hr',
               'lcu': 'smf78_lcu_hr',
               'chap': 'smf78_chap_hr'}
tblnames_da = {'pro': 'smf78_pro_da',
               'comn': 'smf78_comn_da',
               'pvt': 'smf78_pvt_da',
               'pvsp': 'smf78_pvsp_da',
               'ioq': 'smf78_ioq_da',
               'amg': 'smf78_amg_da',
               'cha': 'smf78_cha_da',
               'iop': 'smf78_iop_da',
               'lcu': 'smf78_lcu_da',
               'chap': 'smf78_chap_da'}

int_dtypedict = create_int_dtypedict(tbls)

agg_dict = {
    'pro': {'smf78flg': 'first',
           'smf78gie': 'last', 'smf78mfv': 'last', 'smf78int': 'sum', 'smf78sam': 'sum', 'smf78cyc': 'last',
           'smf78mvs': 'last', 'smf78iml': 'last', 'smf78ptn': 'last', 'smf78srl': 'last', 'smf78lgo': 'last',
           'smf78oil': 'last', 'smf78syn': 'last', 'smf78xnm': 'last', 'smf78snm': 'last', 'speed_boost': agg_boost,
           'ziip_boost': agg_boost,
           'smf78prd': 'last', 'smf78fla': 'last', 'smf78prf': 'last'
           },
    'pvt': {'r782rdtm': 'last', 'r782step': 'last', 'r782pgmn': 'last', 'r782actv': 'max',
           'r782term': 'max', 'r782glch': 'max', 'r782invl': 'max', 'r782shra': 'last', 'r782samp': 'sum',
           'r782regr': 'last', 'r782rgab': 'last', 'r782rgaa': 'last', 'r782gmlb': 'last', 'r782gmla': 'last',
           'r782urab': 'last', 'r782uraa': 'last', 'r782meml': 'last', 'smf_type': 'first', 'r782flgs': 'last'},
    'pvsp': {'spd_vsdbmin': agg_tolist, 'spd_vsdbntme': agg_tolist, 'spd_vsdbmax': agg_tolist,
             'spd_vsdbxtme': agg_tolist, 'spd_vsdbtotl': 'sum'},
    'iop': {'smf78int': 'sum', 'iop_installed': 'last', 'r783iqsm': 'sum', 'r783iqct': 'sum', 'r783iipb': 'sum',
           'r783iipi': 'sum', 'r783iifs': 'sum', 'r783ipii': 'sum', 'r783icpb': 'sum', 'r783idpb': 'sum',
           'r783icub': 'sum', 'r783idvb': 'sum', 'r783iscb': 'sum', 'r783iecb': 'sum', 'r783iflg': 'last'},
    'ioq': {'data_invalid_ch_failure': 'last', 'diagnose_failed': 'last', 'store_primary_not_supported': 'last',
           'dcm_hw_supported': 'last', 'dcm_managed_ch': 'last', 'iop_util_data_supported': 'last',
           'command_response_time_supported': 'last', 'transfer_ready_disabled_aval': 'last',
           'alias_management_aval': 'last', 'eadm_compression_aval': 'last', 'scm_aval': 'last', 'r783gntr': 'last',
           'r783tsr': 'sum', 'r783tot': 'sum', 'config_changed': 'last', 'config_changed_since_ipl': 'last',
           'ipl_iodf': 'last', 'io_config_token_valid': 'last', 'multi_ch_subsys_allowed': 'last',
           'r783css': 'last', 'r783tnm': 'last', 'r783tsf': 'last', 'r783tdt': 'last', 'r783ttm': 'last',
           'r783tdy': 'last', 'smf_type': 'first', 'r783gflg': 'last', 'r783gflx': 'last', 'r783cfl': 'last',},
    'cha': {'smf78int': 'sum', 'ch_path_installed': 'first', 'ch_path_online': 'first', 'ch_path_varied': 'first',
           'ch_path_offline': 'first', 'vary_path_action': 'first', 'ch_path_data_invalid': 'first',
           'ch_path_dcm': 'first', 'chpid_manipulated': 'first', 'r783cun': 'first', 'r783cu1': 'first',
           'r783cu2': 'first', 'r783cu3': 'first', 'r783cu4': 'first', 'r783cub': 'sum', 'r783pt': 'sum',
           'r783dpb': 'sum', 'r783cbt': 'sum', 'r783cmr': 'sum', 'r783sbs': 'sum',
           'extended_io_measurement1': 'first', 'extended_io_measurement2': 'first',
           'first_transfer_ready_disabled': 'first', 'r783cpat': 'first', 'r783ctmw': 'sum',
           'r783ctrd': 'sum', 'r783amgs': 'first', 'r783cpst': 'first', 'r783cpxf': 'first',},
    'chap': {'r783mcmn': 'last', 'r783mcmx': 'last', 'r783mcdf': 'last', 'smf78int': 'sum',
            'ch_path_installed': 'first', 'ch_path_online': 'first', 'ch_path_varied': 'first',
            'ch_path_offline': 'first', 'vary_path_action': 'first', 'ch_path_data_invalid': 'first',
            'ch_path_dcm': 'first', 'chpid_manipulated': 'first', 'r783cun': 'first', 'r783cu1': 'first',
            'r783cu2': 'first', 'r783cu3': 'first', 'r783cu4': 'first', 'r783cub': 'sum', 'r783pt': 'sum',
            'r783dpb': 'sum', 'r783cbt': 'sum', 'r783cmr': 'sum', 'r783sbs': 'sum',
            'extended_io_measurement1': 'first', 'extended_io_measurement2': 'first',
            'first_transfer_ready_disabled': 'first', 'r783cpat': 'first', 'r783ctmw': 'sum',
            'r783ctrd': 'sum', 'r783cpst': 'first', 'r783cpxf': 'first'},
    'lcu': {'r783cun': 'last', 'r783cu1': 'last', 'r783cu2': 'last', 'r783cu3': 'last', 'r783cu4': 'last',
           'smf78int': 'sum', 'r783amgs': 'last', 'no_hw_measurement': 'last', 'dynamically_changed': 'last',
           'dynamically_added': 'last', 'config_change_attempt': 'last', 'lcu_has_dcm_ch': 'last',
           'path_attr_valid': 'last', 'lcu_has_hyperpav': 'last', 'lcu_has_superpav': 'last',
           'lcu_has_ficon': 'last', 'connect_time_invalid': 'last', 'disconnect_time_invalid': 'last',
           'r783qsm': 'sum', 'r783qct': 'sum', 'r783mcmn': 'min', 'r783mcmx': 'max', 'r783mcdf': 'last',
           'r783ptm': 'max', 'r783dpbm': 'sum', 'r783cubm': 'sum', 'r783cbtm': 'sum', 'r783cmrm': 'sum',
           'r783sbsm': 'sum', 'r783dctm': 'sum', 'r783ddtm': 'sum', 'r783csst': 'sum', 'r783tmwm': 'sum',
           'r783trdm': 'sum', 'r783hcu': 'last', 'r783hnai': 'sum', 'r783htio': 'sum', 'r783haiu': 'max',
           'r783hcad': 'max', 'r783hioq': 'max', 'r783xanc': 'sum', 'r783xauc': 'sum', 'r783xnhc': 'sum',
           'r783xabc': 'sum', 'r783xcbc': 'sum', 'r783xhbc': 'max', 'r783xalc': 'sum', 'r783xclc': 'sum',
           'r783xhlc': 'max', 'r783xnag': 'sum', 'r783xcqd': 'max', 'r783xciu': 'max', 'iohmax': 'max',
           'iohdmax': 'max', 'iohioqc': 'max', 'ioxhcba': 'max', 'ioxhcla': 'max', 'r783dst': 'last',
           'r783dstx': 'last'},
    'amg': {'smf78int': 'sum', 'r783amgc': 'first'}
}

def sum_78db(db_engines: dict, db_session: Session, summary_level: str, start_time_str: str, end_time_str: str,
             partitions_scheme: str, db_driver: str = 'postgresql+psycopg2') -> UploadResult:
    """Summarize smf78 interval database to the hourly or daily database.

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

    insert_dict = {'pro': 0, 'comn': 0, 'pvt': 0, 'pvsp': 0,
                   'ioq': 0, 'iop': 0, 'amg': 0, 'lcu': 0, 'cha': 0, 'chap': 0}
    summary_class = {'hourly': tbls_hr, 'daily': tbls_da}
    summary_tblname = {'hourly': tblnames_hr, 'daily': tblnames_da}
    summary_engine = {'hourly': '78.hourly', 'daily': '78.daily'}

    result_list = []
    st = time.time()
    current_time = dt.datetime.now()

    # Summing up Smf78Pro
    df_pro_list = []
    pro_stmt = select(Smf78Pro).where(Smf78Pro.datetime.between(start, end))
    for part in partitions_range:
        df_pro = pd.read_sql(pro_stmt, db_engines[f'78.{part}'])
        if not df_pro.empty:
            df_pro['date'] = df_pro['datetime'].dt.date
            df_pro_list.append(df_pro)
    if len(df_pro_list) > 0:
        df_pros = pd.concat(df_pro_list)
        df_pros['speed_boost'] = df_pros['smf78fla'].apply(lambda x: is_bit_set(x, 16, 10) if pd.notna(x) else np.nan)
        df_pros['ziip_boost'] = df_pros['smf78fla'].apply(
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
                                       'smf78',
                                       [col.name for col in
                                        summary_class[summary_level]['pro'].__table__.primary_key.columns.values()],
                                       int_dtypedict['pro'], shard_id=summary_engine[summary_level]
                                       )
    # Summing up Smf78Comn
    get_max_index = np.vectorize(max_index, otypes=[object])
    get_min_index = np.vectorize(min_index, otypes=[object])
    get_maxs = np.vectorize(max_items)
    get_mins = np.vectorize(min_items)
    get_list_loc = np.vectorize(list_loc, otypes=[object])
    agg_comn = {}

    df_comn_list = []
    comn_stmt = select(Smf78Comn).where(Smf78Comn.datetime.between(start, end))
    null_column_list = []
    for part in partitions_range:
        df_comn = pd.read_sql(comn_stmt, db_engines[f'78.{part}'])
        if not df_comn.empty:
            df_comn['date'] = df_comn['datetime'].dt.date
            null_columns = df_comn.columns[df_comn.isna().all()].tolist()
            df_comn_list.append(df_comn)
            for col in null_columns:
                if col not in null_column_list:
                    null_column_list.append(col)
    if len(df_comn_list) > 0:
        df_comns = pd.concat([df.dropna(axis=1, how='all') for df in df_comn_list])
        if len(null_column_list) > 0:
            new_cols = df_comns.columns.tolist()
            for col in null_column_list:
                if col not in new_cols:
                    new_cols.append(col)
            df_comns = df_comns.reindex(columns=new_cols)
        for name in summary_class[summary_level]['comn'].__table__.columns.keys():
            if 'tot' in name:
                agg_comn[name] = 'sum'
            elif 'min' in name or 'max' in name or 'tme' in name:
                agg_comn[name] = agg_tolist
            elif (name not in [
                col.name for col in summary_class[summary_level]['comn'].__table__.primary_key.columns.values()] and
                  name not in ['date', 'last_update_time']):
                agg_comn[name] = 'first'
        df_comn_sum = df_comns.groupby([
            col.name for col in summary_class[summary_level]['comn'].__table__.primary_key.columns.values()]).agg(
            agg_comn).copy().reset_index()
        if 'date' not in df_comn_sum.columns:
            df_comn_sum['date'] = df_comn_sum['datetime'].dt.date
        df_comn_sum['last_update_time'] = current_time
        df_comn_min = pd.DataFrame(index=df_comn_sum.index)
        df_comn_max = pd.DataFrame(index=df_comn_sum.index)

        for name in summary_class[summary_level]['comn'].__table__.columns.keys():
            if 'min' in name:
                tme_col = name.replace('min', 'ntme')
                idx_col = tme_col + '_idx'
                df_comn_min[idx_col] = get_min_index(df_comn_sum[name])
                df_comn_sum[name] = get_mins(df_comn_sum[name])
                df_comn_sum[tme_col] = get_list_loc(df_comn_sum[tme_col], df_comn_min[idx_col])
            if 'max' in name:
                tme_col = name.replace('max', 'xtme')
                idx_col = tme_col + '_idx'
                df_comn_max[idx_col] = get_max_index(df_comn_sum[name])
                df_comn_sum[name] = get_maxs(df_comn_sum[name])
                df_comn_sum[tme_col] = get_list_loc(df_comn_sum[tme_col], df_comn_max[idx_col])
        insert_dict['comn'] = df_upsert(db_driver, db_engines[summary_engine[summary_level]], db_session,
                                        df_comn_sum[[column for column in df_comn_sum.columns if column in
                                                     summary_class[summary_level]['comn'].__table__.columns.keys()]],
                                        summary_tblname[summary_level]['comn'], summary_class[summary_level]['comn'],
                                        'smf78',
                                        [col.name for col in
                                         summary_class[summary_level]['comn'].__table__.primary_key.columns.values()],
                                        int_dtypedict['comn'], shard_id=summary_engine[summary_level]
                                       )
    # Summing up Smf78Pvt
    agg_pvt = {'r782rdtm': 'last', 'r782step': 'last', 'r782pgmn': 'last', 'r782actv': 'max',
               'r782term': 'max', 'r782glch': 'max', 'r782invl': 'max', 'r782shra': 'last', 'r782samp': 'sum',
               'r782regr': 'last', 'r782rgab': 'last', 'r782rgaa': 'last', 'r782gmlb': 'last', 'r782gmla': 'last',
               'r782urab': 'last', 'r782uraa': 'last', 'r782meml': 'last', 'smf_type': 'first', 'r782flgs': 'last'}
    for name in summary_class[summary_level]['pvt'].__table__.columns.keys():
        if 'tot' in name:
            agg_pvt[name] = 'sum'
        elif 'min' in name or 'max' in name or 'tme' in name:
            agg_pvt[name] = agg_tolist
        elif 'hwm' in name:
            agg_pvt[name] = 'max'
    df_pvt_list = []
    pvt_stmt = select(Smf78Pvt).where(Smf78Pvt.datetime.between(start, end))
    null_column_list = []
    for part in partitions_range:
        df_pvt = pd.read_sql(pvt_stmt, db_engines[f'78.{part}'])
        if not df_pvt.empty:
            df_pvt['date'] = df_pvt['datetime'].dt.date
            df_pvt_list.append(df_pvt)
            null_columns = df_pvt.columns[df_pvt.isna().all()].tolist()
            for col in null_columns:
                if col not in null_column_list:
                    null_column_list.append(col)
    if len(df_pvt_list) > 0:
        df_pvts = pd.concat([df.dropna(axis=1, how='all') for df in df_pvt_list])
        if len(null_column_list) > 0:
            new_cols = df_pvts.columns.tolist()
            for col in null_column_list:
                if col not in new_cols:
                    new_cols.append(col)
            df_pvts = df_pvts.reindex(columns=new_cols)
        df_pvt_sum = df_pvts.groupby(
            [col.name for col in summary_class[summary_level]['pvt'].__table__.primary_key.columns.values()]).agg(
            agg_pvt).copy().reset_index()
        if 'date' not in df_pvt_sum.columns:
            df_pvt_sum['date'] = df_pvt_sum['datetime'].dt.date
        df_pvt_sum['last_update_time'] = current_time
        df_pvt_min = pd.DataFrame(index=df_pvt_sum.index)
        df_pvt_max = pd.DataFrame(index=df_pvt_sum.index)
        for name in summary_class[summary_level]['pvt'].__table__.columns.keys():
            if 'min' in name:
                tme_col = name.replace('min', 'ntme')
                idx_col = tme_col + '_idx'
                df_pvt_min[idx_col] = get_min_index(df_pvt_sum[name])
                df_pvt_sum[name] = get_mins(df_pvt_sum[name])
                df_pvt_sum[tme_col] = get_list_loc(df_pvt_sum[tme_col], df_pvt_min[idx_col])
            if 'max' in name:
                tme_col = name.replace('max', 'xtme')
                idx_col = tme_col + '_idx'
                df_pvt_max[idx_col] = get_max_index(df_pvt_sum[name])
                df_pvt_sum[name] = get_maxs(df_pvt_sum[name])
                df_pvt_sum[tme_col] = get_list_loc(df_pvt_sum[tme_col], df_pvt_max[idx_col])
        insert_dict['pvt'] = df_upsert(db_driver, db_engines[summary_engine[summary_level]], db_session,
                                       df_pvt_sum[summary_class[summary_level]['pvt'].__table__.columns.keys()],
                                       summary_tblname[summary_level]['pvt'], summary_class[summary_level]['pvt'],
                                       'smf78',
                                       [col.name for col in
                                        summary_class[summary_level]['pvt'].__table__.primary_key.columns.values()],
                                       int_dtypedict['pvt'], shard_id=summary_engine[summary_level]
                                       )
    # Summing up Smf78Pvsp
    df_pvsp_list = []
    null_column_list = []
    pvsp_stmt = select(Smf78Pvsp).where(Smf78Pvsp.datetime.between(start, end))
    for part in partitions_range:
        df_pvsp = pd.read_sql(pvsp_stmt, db_engines[f'78.{part}'])
        if not df_pvsp.empty:
            df_pvsp['date'] = df_pvsp['datetime'].dt.date
            df_pvsp_list.append(df_pvsp)
            null_columns = df_pvsp.columns[df_pvsp.isna().all()].tolist()
            for col in null_columns:
                if col not in null_column_list:
                    null_column_list.append(col)
    if len(df_pvsp_list) > 0:
        df_pvsps = pd.concat([df.dropna(axis=1, how='all') for df in df_pvsp_list])
        if len(null_column_list) > 0:
            new_cols = df_pvsps.columns.tolist()
            for col in null_column_list:
                if col not in new_cols:
                    new_cols.append(col)
            df_pvsps = df_pvsps.reindex(columns=new_cols)
        df_pvsp_sum = df_pvsps.groupby(
            [col.name for col in summary_class[summary_level]['pvsp'].__table__.primary_key.columns.values()]).agg(
            agg_dict['pvsp']).copy().reset_index()
        if 'date' not in df_pvsp_sum.columns:
            df_pvsp_sum['date'] = df_pvsp_sum['datetime'].dt.date
        df_pvsp_sum['last_update_time'] = current_time
        df_pvsp_sum['vsdbmin_idx'] = get_min_index(df_pvsp_sum['spd_vsdbmin'])
        df_pvsp_sum['spd_vsdbmin'] = get_mins(df_pvsp_sum['spd_vsdbmin'])
        df_pvsp_sum['spd_vsdbntme'] = get_list_loc(df_pvsp_sum['spd_vsdbntme'], df_pvsp_sum['vsdbmin_idx'])
        df_pvsp_sum['vsdbmax_idx'] = get_max_index(df_pvsp_sum['spd_vsdbmax'])
        df_pvsp_sum['spd_vsdbmax'] = get_maxs(df_pvsp_sum['spd_vsdbmax'])
        df_pvsp_sum['spd_vsdbxtme'] = get_list_loc(df_pvsp_sum['spd_vsdbxtme'], df_pvsp_sum['vsdbmax_idx'])

        insert_dict['pvsp'] = df_upsert(db_driver, db_engines[summary_engine[summary_level]], db_session,
                                        df_pvsp_sum[summary_class[summary_level]['pvsp'].__table__.columns.keys()],
                                        summary_tblname[summary_level]['pvsp'], summary_class[summary_level]['pvsp'],
                                        'smf78',
                                        [col.name for col in
                                         summary_class[summary_level]['pvsp'].__table__.primary_key.columns.values()],
                                        int_dtypedict['pvsp'], shard_id=summary_engine[summary_level]
                                        )
    # Summing up Smf78Ioq
    agg_iop = {'smf78int': 'last', 'iop_installed': 'last', 'r783iqsm': 'sum', 'r783iqct': 'sum', 'r783iipb': 'sum',
               'r783iipi': 'sum', 'r783iifs': 'sum', 'r783ipii': 'sum', 'r783icpb': 'sum', 'r783idpb': 'sum',
               'r783icub': 'sum', 'r783idvb': 'sum', 'r783iscb': 'sum', 'r783iecb': 'sum', 'r783iflg': 'last'}
    df_ioq_list = []
    df_iop_list = []
    null_column_list1 = []
    null_column_list2 = []
    ioq_stmt = select(Smf78Ioq).where(Smf78Ioq.datetime.between(start, end))
    ioq_stmt2 = select(Smf78Iop).join_from(Smf78Ioq, Smf78Ioq.smf78_iops).where(
        Smf78Iop.datetime.between(start, end))
    for part in partitions_range:
        df_ioq = pd.read_sql(ioq_stmt, db_engines[f'78.{part}'])
        if not df_ioq.empty:
            df_ioq['date'] = df_ioq['datetime'].dt.date
            df_ioq_list.append(df_ioq)
            null_columns = df_ioq.columns[df_ioq.isna().all()].tolist()
            for col in null_columns:
                if col not in null_column_list1:
                    null_column_list1.append(col)
            df_iop = pd.read_sql(ioq_stmt2, db_engines[f'78.{part}'])
            if not df_iop.empty:
                df_iop['date'] = df_iop['datetime'].dt.date
                df_iop_list.append(df_iop)
                null_columns = df_ioq.columns[df_ioq.isna().all()].tolist()
                for col in null_columns:
                    if col not in null_column_list2:
                        null_column_list2.append(col)
    if len(df_ioq_list) > 0:
        df_ioqs = pd.concat([df.dropna(axis=1, how='all') for df in df_ioq_list])
        if len(null_column_list1) > 0:
            new_cols = df_ioqs.columns.tolist()
            for col in null_column_list1:
                if col not in new_cols:
                    new_cols.append(col)
            df_ioqs = df_ioqs.reindex(columns=new_cols)
        df_ioq_sum = df_ioqs.groupby(
            [col.name for col in summary_class[summary_level]['ioq'].__table__.primary_key.columns.values()]).agg(
            agg_dict['ioq']).copy().reset_index()
        if 'date' not in df_ioq_sum.columns:
            df_ioq_sum['date'] = df_ioq_sum['datetime'].dt.date
        df_ioq_sum['last_update_time'] = current_time
        df_ioq_sum.set_index(
            [col.name for col in summary_class[summary_level]['ioq'].__table__.primary_key.columns.values()],
            inplace=True)
        if len(df_iop_list) > 0:
            df_iops = pd.concat([df.dropna(axis=1, how='all') for df in df_iop_list])
            if len(null_column_list2) > 0:
                new_cols = df_iops.columns.tolist()
                for col in null_column_list2:
                    if col not in new_cols:
                        new_cols.append(col)
                df_iops = df_iops.reindex(columns=new_cols)
            df_iop_sum = df_iops.groupby(
                [col.name for col in
                 summary_class[summary_level]['ioq'].__table__.primary_key.columns.values()]).agg(
                agg_iop)
            df_ioq_sum = pd.concat([df_ioq_sum, df_iop_sum], axis=1)

        df_ioq_sum['iopac'] = df_ioq_sum['r783iqct'] / df_ioq_sum['smf78int']
        df_ioq_sum['iopipb'] = df_ioq_sum['r783iipb'] * 100 / (df_ioq_sum['r783iipb'] + df_ioq_sum['r783iipi'])
        df_ioq_sum['iopecb'] = df_ioq_sum['r783iecb'] * 100 / (df_ioq_sum['r783iipb'] + df_ioq_sum['r783iipi'])
        df_ioq_sum['iopscb'] = df_ioq_sum['r783iscb'] * 100 / (df_ioq_sum['r783iipb'] + df_ioq_sum['r783iipi'])
        df_ioq_sum['iopipi'] = df_ioq_sum['r783iipi'] * 100 / (df_ioq_sum['r783iipb'] + df_ioq_sum['r783iipi'])
        df_ioq_sum['iorifs'] = df_ioq_sum['r783iifs'] / df_ioq_sum['smf78int']
        df_ioq_sum['iorpii'] = df_ioq_sum['r783ipii'] / df_ioq_sum['smf78int']
        df_ioq_sum['iopalb'] = (
                (df_ioq_sum['r783icpb'] + df_ioq_sum['r783idpb'] + df_ioq_sum['r783icub'] + df_ioq_sum[
                    'r783idvb']) * 100 /
                (df_ioq_sum['r783iifs'] + df_ioq_sum['r783icpb'] + df_ioq_sum['r783idpb'] + df_ioq_sum['r783icub'] +
                 df_ioq_sum['r783idvb']))
        df_ioq_sum['iopchb'] = df_ioq_sum['r783icpb'] * 100 / (
                df_ioq_sum['r783iifs'] + df_ioq_sum['r783icpb'] + df_ioq_sum['r783idpb'] +
                df_ioq_sum['r783icub'] + df_ioq_sum['r783idvb'])
        df_ioq_sum['iopdpb'] = df_ioq_sum['r783idpb'] * 100 / (
                df_ioq_sum['r783iifs'] + df_ioq_sum['r783icpb'] + df_ioq_sum['r783idpb'] +
                df_ioq_sum['r783icub'] + df_ioq_sum['r783idvb'])
        df_ioq_sum['iopcub'] = df_ioq_sum['r783icub'] * 100 / (
                df_ioq_sum['r783iifs'] + df_ioq_sum['r783icpb'] + df_ioq_sum['r783idpb'] +
                df_ioq_sum['r783icub'] + df_ioq_sum['r783idvb'])
        df_ioq_sum['iopdvb'] = df_ioq_sum['r783idvb'] * 100 / (
                df_ioq_sum['r783iifs'] + df_ioq_sum['r783icpb'] + df_ioq_sum['r783idpb'] +
                df_ioq_sum['r783icub'] + df_ioq_sum['r783idvb'])
        df_ioq_sum['ionalb'] = (df_ioq_sum['r783icpb'] + df_ioq_sum['r783idpb'] + df_ioq_sum['r783icub'] +
                                df_ioq_sum[
                                    'r783idvb']) / df_ioq_sum['r783iifs']
        df_ioq_sum['ionchb'] = df_ioq_sum['r783icpb'] / df_ioq_sum['r783iifs']
        df_ioq_sum['iondpb'] = df_ioq_sum['r783idpb'] / df_ioq_sum['r783iifs']
        df_ioq_sum['ioncub'] = df_ioq_sum['r783icub'] / df_ioq_sum['r783iifs']
        df_ioq_sum['iondvb'] = df_ioq_sum['r783idvb'] / df_ioq_sum['r783iifs']
        df_ioq_sum['iopql'] = (df_ioq_sum['r783iqsm'] - df_ioq_sum['r783iqct']) / df_ioq_sum['r783iqct']
        insert_dict['ioq'] = df_upsert(db_driver, db_engines[summary_engine[summary_level]], db_session,
                                       df_ioq_sum.reset_index()[
                                           summary_class[summary_level]['ioq'].__table__.columns.keys()],
                                       summary_tblname[summary_level]['ioq'], summary_class[summary_level]['ioq'],
                                       'smf78',
                                       [col.name for col in
                                        summary_class[summary_level]['ioq'].__table__.primary_key.columns.values()],
                                       int_dtypedict['ioq'], shard_id=summary_engine[summary_level]
                                       )

    # Summing up Smf78Iop
    agg_iop = {'smf78int': 'sum', 'iop_installed': 'last', 'r783iqsm': 'sum', 'r783iqct': 'sum', 'r783iipb': 'sum',
               'r783iipi': 'sum', 'r783iifs': 'sum', 'r783ipii': 'sum', 'r783icpb': 'sum', 'r783idpb': 'sum',
               'r783icub': 'sum', 'r783idvb': 'sum', 'r783iscb': 'sum', 'r783iecb': 'sum', 'r783iflg': 'last'}
    df_iop_list = []
    null_column_list = []
    iop_stmt = select(Smf78Iop).where(Smf78Iop.datetime.between(start, end))
    for part in partitions_range:
        df_iop = pd.read_sql(iop_stmt, db_engines[f'78.{part}'])
        if not df_iop.empty:
            df_iop['date'] = df_iop['datetime'].dt.date
            df_iop_list.append(df_iop)
            null_columns = df_iop.columns[df_iop.isna().all()].tolist()
            for col in null_columns:
                if col not in null_column_list:
                    null_column_list.append(col)
    if len(df_iop_list) > 0:
        df_iops = pd.concat([df.dropna(axis=1, how='all') for df in df_iop_list])
        if len(null_column_list) > 0:
            new_cols = df_iops.columns.tolist()
            for col in null_column_list:
                if col not in new_cols:
                    new_cols.append(col)
            df_iops = df_iops.reindex(columns=new_cols)
        df_iop_sum = df_iops.groupby(
            [col.name for col in summary_class[summary_level]['iop'].__table__.primary_key.columns.values()]).agg(
            agg_dict['iop']).reset_index()
        if 'date' not in df_iop_sum.columns:
            df_iop_sum['date'] = df_iop_sum['datetime'].dt.date
        df_iop_sum['last_update_time'] = current_time
        df_iop_sum['iopac'] = df_iop_sum['r783iqct'] / df_iop_sum['smf78int']
        df_iop_sum['iopipb'] = df_iop_sum['r783iipb'] * 100 / (df_iop_sum['r783iipb'] + df_iop_sum['r783iipi'])
        df_iop_sum['iopecb'] = df_iop_sum['r783iecb'] * 100 / (df_iop_sum['r783iipb'] + df_iop_sum['r783iipi'])
        df_iop_sum['iopscb'] = df_iop_sum['r783iscb'] * 100 / (df_iop_sum['r783iipb'] + df_iop_sum['r783iipi'])
        df_iop_sum['iopipi'] = df_iop_sum['r783iipi'] * 100 / (df_iop_sum['r783iipb'] + df_iop_sum['r783iipi'])
        df_iop_sum['iorifs'] = df_iop_sum['r783iifs'] / df_iop_sum['smf78int']
        df_iop_sum['iorpii'] = df_iop_sum['r783ipii'] / df_iop_sum['smf78int']
        df_iop_sum['iopalb'] = (
                (df_iop_sum['r783icpb'] + df_iop_sum['r783idpb'] + df_iop_sum['r783icub'] + df_iop_sum['r783idvb']) * 100 /
                (df_iop_sum['r783iifs'] + df_iop_sum['r783icpb'] + df_iop_sum['r783idpb'] + df_iop_sum['r783icub'] +
                 df_iop_sum['r783idvb']))
        df_iop_sum['iopchb'] = df_iop_sum['r783icpb'] * 100 / (
                df_iop_sum['r783iifs'] + df_iop_sum['r783icpb'] + df_iop_sum['r783idpb'] +
                df_iop_sum['r783icub'] + df_iop_sum['r783idvb'])
        df_iop_sum['iopdpb'] = df_iop_sum['r783idpb'] * 100 / (
                df_iop_sum['r783iifs'] + df_iop_sum['r783icpb'] + df_iop_sum['r783idpb'] +
                df_iop_sum['r783icub'] + df_iop_sum['r783idvb'])
        df_iop_sum['iopcub'] = df_iop_sum['r783icub'] * 100 / (
                df_iop_sum['r783iifs'] + df_iop_sum['r783icpb'] + df_iop_sum['r783idpb'] +
                df_iop_sum['r783icub'] + df_iop_sum['r783idvb'])
        df_iop_sum['iopdvb'] = df_iop_sum['r783idvb'] * 100 / (
                df_iop_sum['r783iifs'] + df_iop_sum['r783icpb'] + df_iop_sum['r783idpb'] +
                df_iop_sum['r783icub'] + df_iop_sum['r783idvb'])
        df_iop_sum['ionalb'] = (df_iop_sum['r783icpb'] + df_iop_sum['r783idpb'] + df_iop_sum['r783icub'] + df_iop_sum[
            'r783idvb']) / df_iop_sum['r783iifs']
        df_iop_sum['ionchb'] = df_iop_sum['r783icpb'] / df_iop_sum['r783iifs']
        df_iop_sum['iondpb'] = df_iop_sum['r783idpb'] / df_iop_sum['r783iifs']
        df_iop_sum['ioncub'] = df_iop_sum['r783icub'] / df_iop_sum['r783iifs']
        df_iop_sum['iondvb'] = df_iop_sum['r783idvb'] / df_iop_sum['r783iifs']
        df_iop_sum['iopql'] = (df_iop_sum['r783iqsm'] - df_iop_sum['r783iqct']) / df_iop_sum['r783iqct']
        insert_dict['iop'] = df_upsert(db_driver, db_engines[summary_engine[summary_level]], db_session,
                                       df_iop_sum[summary_class[summary_level]['iop'].__table__.columns.keys()],
                                       summary_tblname[summary_level]['iop'], summary_class[summary_level]['iop'],
                                       'smf78',
                                       [col.name for col in
                                        summary_class[summary_level]['iop'].__table__.primary_key.columns.values()],
                                       int_dtypedict['iop'], shard_id=summary_engine[summary_level]
                                       )
    # Summing up Smf78Lcu
    agg_cha = {'r783cub': 'sum', 'r783pt': 'sum', 'r783dpb': 'sum', 'iocbt': 'sum', 'iocmr': 'sum'}
    df_lcu_list = []
    df_cha_list = []
    lcu_stmt = select(Smf78Lcu).where(Smf78Lcu.datetime.between(start, end))
    lcu_stmt1 = select(Smf78Cha).join_from(Smf78Lcu, Smf78Lcu.smf78_chas).where(
        Smf78Cha.datetime.between(start, end))
    null_column_list = []
    null_column_list2 = []
    for part in partitions_range:
        df_lcu = pd.read_sql(lcu_stmt, db_engines[f'78.{part}'])
        if not df_lcu.empty:
            df_lcu['date'] = df_lcu['datetime'].dt.date
            df_lcu_list.append(df_lcu)
            null_columns = df_lcu.columns[df_lcu.isna().all()].tolist()
            for col in null_columns:
                if col not in null_column_list:
                    null_column_list.append(col)
            df_cha = pd.read_sql(lcu_stmt1, db_engines[f'78.{part}'])
            if not df_cha.empty:
                df_cha['date'] = df_cha['datetime'].dt.date
                df_cha_list.append(df_cha)
                null_columns = df_cha.columns[df_cha.isna().all()].tolist()
                for col in null_columns:
                    if col not in null_column_list2:
                        null_column_list2.append(col)
    if len(df_lcu_list) > 0:
        df_lcus = pd.concat([df.dropna(axis=1, how='all') for df in df_lcu_list])
        if len(null_column_list) > 0:
            new_cols = df_lcus.columns.tolist()
            for col in null_column_list:
                if col not in new_cols:
                    new_cols.append(col)
            df_lcus = df_lcus.reindex(columns=new_cols)
        df_lcu_sum = df_lcus.groupby(
            [col.name for col in summary_class[summary_level]['lcu'].__table__.primary_key.columns.values()]).agg(
            agg_dict['lcu']).reset_index()
        df_lcu_sum = df_lcu_sum.astype({'r783hnai': float, 'r783htio': float, 'r783xauc': float, 'r783xanc': float,
                                        'r783xnhc': float, 'r783xcqd': float, 'r783xciu': float})
        if 'date' not in df_lcu_sum.columns:
            df_lcu_sum['date'] = df_lcu_sum['datetime'].dt.date
        df_lcu_sum['last_update_time'] = current_time
        df_lcu_sum['iohwait'] = df_lcu_sum['r783hnai'] / df_lcu_sum['r783htio']
        df_lcu_sum['ioxsareq'] = df_lcu_sum['r783xauc'] / df_lcu_sum['r783xanc']
        df_lcu_sum['ioxuahrq'] = df_lcu_sum['r783xnhc'] / df_lcu_sum['r783xanc']
        df_lcu_sum['ioxcqd'] = df_lcu_sum['r783xcqd'] / df_lcu_sum['r783xanc']
        df_lcu_sum['ioxiuac'] = df_lcu_sum['r783xciu'] / df_lcu_sum['r783xanc']
        df_lcu_sum['ioxabc'] = df_lcu_sum['r783xabc'] / df_lcu_sum['smf78int']
        df_lcu_sum['ioxalc'] = df_lcu_sum['r783xalc'] / df_lcu_sum['smf78int']
        df_lcu_sum['ioctr'] = df_lcu_sum['r783qct'] / df_lcu_sum['smf78int']
        df_lcu_sum['iodlq'] = (df_lcu_sum['r783qsm'] - df_lcu_sum['r783qct']) / df_lcu_sum['r783qct']
        df_lcu_sum = df_lcu_sum.set_index(
            [col.name for col in summary_class[summary_level]['lcu'].__table__.primary_key.columns.values()])

        if len(df_cha_list) > 0:
            df_chas = pd.concat([df.dropna(axis=1, how='all') for df in df_cha_list])
            if len(null_column_list2) > 0:
                new_cols = df_chas.columns.tolist()
                for col in null_column_list2:
                    if col not in new_cols:
                        new_cols.append(col)
                df_chas = df_chas.reindex(columns=new_cols)
            df_cha_sum = df_chas.rename(columns={'r783id1': 'r783id2'}).groupby(
                [col.name for col in
                 summary_class[summary_level]['lcu'].__table__.primary_key.columns.values()]).agg(
                agg_cha)
        else:
            df_cha_sum = pd.DataFrame()

        if not df_cha_sum.empty:
            df_lcu_sum = pd.concat([df_lcu_sum, df_cha_sum], axis=1)
            df_lcu_sum['iocss'] = df_lcu_sum['r783csst'] * 1000 / df_lcu_sum['r783pt']
            df_lcu_sum['total_requests'] = df_lcu_sum['r783pt'] + df_lcu_sum['r783dpb'] + df_lcu_sum['r783cub']
            df_lcu_sum['ioart'] = df_lcu_sum['r783pt'] / df_lcu_sum['smf78int']
            df_lcu_sum['iocub'] = df_lcu_sum['r783cub'] * 100 / df_lcu_sum['total_requests']
            df_lcu_sum['iodpb'] = df_lcu_sum['r783dpb'] * 100 / df_lcu_sum['total_requests']
        else:
            new_lcu_cols = df_lcu_sum.columns.tolist()
            for col in ['ioart', 'iocub', 'iodpb', 'iocbt', 'iocmr', 'iocss']:
                if col not in new_lcu_cols:
                    new_lcu_cols.append(col)
            df_lcu_sum = df_lcu_sum.reindex(columns=new_lcu_cols)

        insert_dict['lcu'] = df_upsert(db_driver, db_engines[summary_engine[summary_level]], db_session,
                                       df_lcu_sum.reset_index()[
                                           summary_class[summary_level]['lcu'].__table__.columns.keys()],
                                       summary_tblname[summary_level]['lcu'], summary_class[summary_level]['lcu'],
                                       'smf78',
                                       [col.name for col in
                                        summary_class[summary_level]['lcu'].__table__.primary_key.columns.values()],
                                       int_dtypedict['lcu'], shard_id=summary_engine[summary_level]
                                       )
    # Summing up Smf78Cha
    df_cha_list = []
    null_column_list = []
    cha_stmt = select(Smf78Cha).where(Smf78Cha.datetime.between(start, end))
    for part in partitions_range:
        df_cha = pd.read_sql(cha_stmt, db_engines[f'78.{part}'])
        if not df_cha.empty:
            df_cha['date'] = df_cha['datetime'].dt.date
            df_cha_list.append(df_cha)
            null_columns = df_cha.columns[df_cha.isna().all()].tolist()
            for col in null_columns:
                if col not in null_column_list:
                    null_column_list.append(col)
    if len(df_cha_list) > 0:
        df_chas = pd.concat([df.dropna(axis=1, how='all') for df in df_cha_list])
        if len(null_column_list) > 0:
            new_cols = df_chas.columns.tolist()
            for col in null_column_list:
                if col not in new_cols:
                    new_cols.append(col)
            df_chas = df_chas.reindex(columns=new_cols)
        df_cha_sum = df_chas.groupby(
            [col.name for col in summary_class[summary_level]['cha'].__table__.primary_key.columns.values()]).agg(
            agg_dict['cha']).reset_index()
        if 'date' not in df_cha_sum.columns:
            df_cha_sum['date'] = df_cha_sum['datetime'].dt.date
        df_cha_sum['last_update_time'] = current_time
        df_cha_sum['iotmdinh'] = (df_cha_sum['r783ctmw'] - df_cha_sum['r783ctrd']) / df_cha_sum['r783ctmw']
        df_cha_sum['ioart'] = df_cha_sum['r783pt'] / df_cha_sum['smf78int']
        df_cha_sum['total_requests'] = df_cha_sum['r783pt'] + df_cha_sum['r783dpb'] + df_cha_sum['r783cub']
        df_cha_sum['iocub'] = df_cha_sum['r783cub'] * 100 / df_cha_sum['total_requests']
        df_cha_sum['iodpb'] = df_cha_sum['r783dpb'] * 100 / df_cha_sum['total_requests']
        df_cha_sum['iocbt'] = df_cha_sum['r783cbt'] * 1000 / df_cha_sum['r783pt']
        df_cha_sum['iocmr'] = df_cha_sum['r783cmr'] * 1000 / df_cha_sum['r783pt']
        insert_dict['cha'] = df_upsert(db_driver, db_engines[summary_engine[summary_level]], db_session,
                                       df_cha_sum[summary_class[summary_level]['cha'].__table__.columns.keys()],
                                       summary_tblname[summary_level]['cha'], summary_class[summary_level]['cha'],
                                       'smf78',
                                       [col.name for col in
                                        summary_class[summary_level]['cha'].__table__.primary_key.columns.values()],
                                       int_dtypedict['cha'], shard_id=summary_engine[summary_level]
                                       )
    # Summing up Smf78Amg
    agg_lcu = {'r783qsm': 'sum', 'r783qct': 'sum', 'r783mcmn': 'min', 'r783mcmx': 'max', 'r783mcdf': 'last',
               'r783ptm': 'max', 'r783dpbm': 'sum', 'r783cubm': 'sum', 'r783cbtm': 'sum', 'r783cmrm': 'sum',
               'r783sbsm': 'sum', 'r783dctm': 'sum', 'r783ddtm': 'sum', 'r783csst': 'sum', 'r783tmwm': 'sum',
               'r783trdm': 'sum', 'r783hcu': 'last', 'r783hnai': 'sum', 'r783htio': 'sum', 'r783haiu': 'max',
               'r783hcad': 'max', 'r783hioq': 'max', 'r783xanc': 'sum', 'r783xauc': 'sum', 'r783xnhc': 'sum',
               'r783xabc': 'sum', 'r783xcbc': 'sum', 'r783xhbc': 'max', 'r783xalc': 'sum', 'r783xclc': 'sum',
               'r783xhlc': 'max', 'r783xnag': 'sum', 'r783xcqd': 'max', 'r783xciu': 'max', 'iohmax': 'max',
               'iohdmax': 'max', 'iohioqc': 'max', 'ioxhcba': 'max', 'ioxhcla': 'max'}
    agg_cha = {'r783cub': 'sum', 'r783pt': 'sum', 'r783dpb': 'sum', 'iocbt': 'sum', 'iocmr': 'sum'}
    df_amg_list = []
    df_lcu_list = []
    df_cha_list = []
    amg_stmt = select(Smf78Amg).where(Smf78Amg.datetime.between(start, end))
    amg_stmt1 = select(Smf78Lcu).join_from(Smf78Amg, Smf78Amg.smf78_lcus).where(
        Smf78Lcu.datetime.between(start, end))
    amg_stmt2 = select(Smf78Cha).join_from(Smf78Amg, Smf78Amg.smf78_chas).where(
        Smf78Cha.datetime.between(start, end))
    null_column_list1 = []
    null_column_list2 = []
    null_column_list3 = []
    for part in partitions_range:
        df_amg = pd.read_sql(amg_stmt, db_engines[f'78.{part}'])
        if not df_amg.empty:
            df_amg['date'] = df_amg['datetime'].dt.date
            df_amg_list.append(df_amg)
            null_columns = df_amg.columns[df_amg.isna().all()].tolist()
            for col in null_columns:
                if col not in null_column_list1:
                    null_column_list1.append(col)
            df_lcu = pd.read_sql(amg_stmt1, db_engines[f'78.{part}'])
            if not df_lcu.empty:
                df_lcu['date'] = df_lcu['datetime'].dt.date
                df_lcu_list.append(df_lcu)
                null_columns = df_lcu.columns[df_lcu.isna().all()].tolist()
                for col in null_columns:
                    if col not in null_column_list2:
                        null_column_list2.append(col)
            df_cha = pd.read_sql(amg_stmt2, db_engines[f'78.{part}'])
            if not df_cha.empty:
                df_cha['date'] = df_cha['datetime'].dt.date
                df_cha_list.append(df_cha)
                null_columns = df_cha.columns[df_cha.isna().all()].tolist()
                for col in null_columns:
                    if col not in null_column_list3:
                        null_column_list3.append(col)
    if len(df_amg_list) > 0:
        df_amgs = pd.concat([df.dropna(axis=1, how='all') for df in df_amg_list])
        if len(null_column_list1) > 0:
            new_cols = df_amgs.columns.tolist()
            for col in null_column_list1:
                if col not in new_cols:
                    new_cols.append(col)
            df_amgs = df_amgs.reindex(columns=new_cols)
        df_amg_sum = df_amgs.groupby(
            [col.name for col in summary_class[summary_level]['amg'].__table__.primary_key.columns.values()]).agg(
            agg_dict['amg']).reset_index()
        if 'date' not in df_amg_sum.columns:
            df_amg_sum['date'] = df_amg_sum['datetime'].dt.date
        df_amg_sum['last_update_time'] = current_time
        df_amg_sum.set_index(
            [col.name for col in summary_class[summary_level]['amg'].__table__.primary_key.columns.values()],
            inplace=True)
        if len(df_lcu_list) > 0:
            df_lcus = pd.concat([df.dropna(axis=1, how='all') for df in df_lcu_list])
            if len(null_column_list2) > 0:
                new_cols = df_lcus.columns.tolist()
                for col in null_column_list2:
                    if col not in new_cols:
                        new_cols.append(col)
                df_lcus = df_lcus.reindex(columns=new_cols)
            df_lcu_sum = df_lcus.groupby(
                [col.name for col in
                 summary_class[summary_level]['amg'].__table__.primary_key.columns.values()]).agg(
                agg_lcu)
        else:
            df_lcu_sum = pd.DataFrame()
        if len(df_cha_list) > 0:
            df_chas = pd.concat([df.dropna(axis=1, how='all') for df in df_cha_list])
            if len(null_column_list3) > 0:
                new_cols = df_chas.columns.tolist()
                for col in null_column_list3:
                    if col not in new_cols:
                        new_cols.append(col)
                df_chas = df_chas.reindex(columns=new_cols)
            df_cha_sum = df_chas.groupby(
                [col.name for col in
                 summary_class[summary_level]['amg'].__table__.primary_key.columns.values()]).agg(
                agg_cha)
        else:
            df_cha_sum = pd.DataFrame()
        df_amg_sum = pd.concat([df_amg_sum, df_lcu_sum, df_cha_sum], axis=1)
        df_amg_sum['ioctr'] = df_amg_sum['r783qct'] / df_amg_sum['smf78int']
        df_amg_sum['iodlq'] = (df_amg_sum['r783qsm'] - df_amg_sum['r783qct']) / df_amg_sum['r783qct']
        df_amg_sum['iohwait'] = df_amg_sum['r783hnai'] / df_amg_sum['r783htio']
        df_amg_sum['ioxsareq'] = df_amg_sum['r783xauc'] / df_amg_sum['r783xanc']
        df_amg_sum['ioxuahrq'] = df_amg_sum['r783xnhc'] / df_amg_sum['r783xanc']
        df_amg_sum['ioxcqd'] = df_amg_sum['r783xcqd'] / df_amg_sum['r783xanc']
        df_amg_sum['ioxiuac'] = df_amg_sum['r783xciu'] / df_amg_sum['r783xanc']
        df_amg_sum['ioxabc'] = df_amg_sum['r783xabc'] / df_amg_sum['smf78int']
        df_amg_sum['ioxalc'] = df_amg_sum['r783xalc'] / df_amg_sum['smf78int']
        df_amg_sum['iocss'] = df_amg_sum['r783csst'] * 1000 / df_amg_sum['r783pt']
        df_amg_sum['total_requests'] = df_amg_sum['r783pt'] + df_amg_sum['r783dpb'] + df_amg_sum['r783cub']
        df_amg_sum['ioart'] = df_amg_sum['r783pt'] / df_amg_sum['smf78int']
        df_amg_sum['iocub'] = df_amg_sum['r783cub'] * 100 / df_amg_sum['total_requests']
        df_amg_sum['iodpb'] = df_amg_sum['r783dpb'] * 100 / df_amg_sum['total_requests']
        insert_dict['amg'] = df_upsert(db_driver, db_engines[summary_engine[summary_level]], db_session,
                                       df_amg_sum.reset_index()[
                                           summary_class[summary_level]['amg'].__table__.columns.keys()],
                                       summary_tblname[summary_level]['amg'], summary_class[summary_level]['amg'],
                                       'smf78',
                                       [col.name for col in
                                        summary_class[summary_level]['amg'].__table__.primary_key.columns.values()],
                                       int_dtypedict['amg'], shard_id=summary_engine[summary_level]
                                       )
    # Summing up Smf78Chap
    df_chap_list = []
    null_column_list = []
    chap_stmt = select(Smf78Chap).where(Smf78Chap.datetime.between(start, end))
    for part in partitions_range:
        df_chap = pd.read_sql(chap_stmt, db_engines[f'78.{part}'])
        if not df_chap.empty:
            df_chap['date'] = df_chap['datetime'].dt.date
            df_chap_list.append(df_chap)
            null_columns = df_chap.columns[df_chap.isna().all()].tolist()
            for col in null_columns:
                if col not in null_column_list:
                    null_column_list.append(col)
    if len(df_chap_list) > 0:
        df_chaps = pd.concat([df.dropna(axis=1, how='all') for df in df_chap_list])
        if len(null_column_list) > 0:
            new_cols = df_chaps.columns.tolist()
            for col in null_column_list:
                if col not in new_cols:
                    new_cols.append(col)
            df_chaps = df_chaps.reindex(columns=new_cols)
        df_chap_sum = df_chaps.groupby(
            [col.name for col in summary_class[summary_level]['chap'].__table__.primary_key.columns.values()]).agg(
            agg_dict['chap']).reset_index()
        if 'date' not in df_chap_sum.columns:
            df_chap_sum['date'] = df_chap_sum['datetime'].dt.date
        df_chap_sum['last_update_time'] = current_time
        df_chap_sum['iotmdinh'] = (df_chap_sum['r783ctmw'] - df_chap_sum['r783ctrd']) / df_chap_sum['r783ctmw']
        df_chap_sum['ioart'] = df_chap_sum['r783pt'] / df_chap_sum['smf78int']
        df_chap_sum['total_requests'] = df_chap_sum['r783pt'] + df_chap_sum['r783dpb'] + df_chap_sum['r783cub']
        df_chap_sum['iocub'] = df_chap_sum['r783cub'] * 100 / df_chap_sum['total_requests']
        df_chap_sum['iodpb'] = df_chap_sum['r783dpb'] * 100 / df_chap_sum['total_requests']
        df_chap_sum['iocbt'] = df_chap_sum['r783cbt'] * 1000 / df_chap_sum['r783pt']
        df_chap_sum['iocmr'] = df_chap_sum['r783cmr'] * 1000 / df_chap_sum['r783pt']
        insert_dict['chap'] = df_upsert(db_driver, db_engines[summary_engine[summary_level]], db_session,
                                        df_chap_sum[summary_class[summary_level]['chap'].__table__.columns.keys()],
                                        summary_tblname[summary_level]['chap'], summary_class[summary_level]['chap'],
                                        'smf78',
                                        [col.name for col in
                                         summary_class[summary_level]['chap'].__table__.primary_key.columns.values()],
                                        int_dtypedict['chap'], shard_id=summary_engine[summary_level]
                                        )

    result_list.append({summary_tblname[summary_level][k]:v for k,v in insert_dict.items() if k in summary_tblname[summary_level].keys()})

    et = time.time()  # get the end time
    # get the execution time
    elapsed_time = (et - st) / 60
    print(f'Execution time ({summary_level}):', elapsed_time, 'minutes')

    overall_et = time.time()
    overall_elapsed_time = (overall_et - overall_st) / 60
    return UploadResult(result_list, overall_elapsed_time, SUCCESS)

