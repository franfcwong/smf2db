import datetime as dt
import time

import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from smf2db import SUCCESS
from smf2db.api.util import (agg_boost, UploadResult, create_int_dtypedict, df_upsert, sum_up_by_partition)
from smf2db.db_models.smf73_da_model import (Smf73ProDa, Smf73CtlDa, Smf73Cha1Da, Smf73Cha2Da, Smf73Cha3Da,
                                             Smf73Cha4Da, Smf73Cha5Da)
from smf2db.db_models.smf73_hr_model import (Smf73ProHr, Smf73CtlHr, Smf73Cha1Hr, Smf73Cha2Hr, Smf73Cha3Hr,
                                             Smf73Cha4Hr, Smf73Cha5Hr)
from smf2db.db_models.smf73_model import (Smf73Pro, Smf73Ctl, Smf73Cha1, Smf73Cha2, Smf73Cha3, Smf73Cha4,
                                          Smf73Cha5)

tbls = {'pro': Smf73Pro,
        'ctl': Smf73Ctl,
        'cha1': Smf73Cha1,
        'cha2': Smf73Cha2,
        'cha3': Smf73Cha3,
        'cha4': Smf73Cha4,
        'cha5': Smf73Cha5,}
tbls_hr = {'pro': Smf73ProHr,
           'ctl': Smf73CtlHr,
           'cha1': Smf73Cha1Hr,
           'cha2': Smf73Cha2Hr,
           'cha3': Smf73Cha3Hr,
           'cha4': Smf73Cha4Hr,
           'cha5': Smf73Cha5Hr}
tbls_da = {'pro': Smf73ProDa,
           'ctl': Smf73CtlDa,
           'cha1': Smf73Cha1Da,
           'cha2': Smf73Cha2Da,
           'cha3': Smf73Cha3Da,
           'cha4': Smf73Cha4Da,
           'cha5': Smf73Cha5Da}
tblnames = {'pro': 'smf73_pro',
            'ctl': 'smf73_ctl',
            'cha1': 'smf73_cha1',
            'cha2': 'smf73_cha2',
            'cha3': 'smf73_cha3',
            'cha4': 'smf73_cha4',
            'cha5': 'smf73_cha5'}
tblnames_hr = {'pro': 'smf73_pro_hr',
               'ctl': 'smf73_ctl_hr',
               'cha1': 'smf73_cha1_hr',
               'cha2': 'smf73_cha2_hr',
               'cha3': 'smf73_cha3_hr',
               'cha4': 'smf73_cha4_hr',
               'cha5': 'smf73_cha5_hr'}
tblnames_da = {'pro': 'smf73_pro_da',
               'ctl': 'smf73_ctl_da',
               'cha1': 'smf73_cha1_da',
               'cha2': 'smf73_cha2_da',
               'cha3': 'smf73_cha3_da',
               'cha4': 'smf73_cha4_da',
               'cha5': 'smf73_cha5_da'}

int_dtypedict = create_int_dtypedict(tbls)


agg_ctl = {'smf73smp': 'sum', 'config_changed': 'max', 'config_changed_since_ipl': 'last', 'ipl_iodf': 'last',
           'io_token_valid': 'last', 'invalid_ds': 'max', 'cpmf': 'last', 'cpmf_changed': 'max',
           'dcm_supported': 'last', 'dcm_ch': 'last', 'mcs': 'last', 'ench_ch_measurement': 'last', 'smf73tnm': 'last',
           'smf73tsf': 'last', 'smf73tdy': 'last', 'smf73crc': 'sum', 'smf73csc': 'last', 'smf73cmi': 'last',
           'smf73css': 'last', 'smf73tdt': 'last', 'smf73cfl': 'last', 'smf73sfl': 'last'}
agg_cha1 = {'smf73tut': 'sum', 'smf73put': 'sum', 'block_multiplexor': 'first', 'byte_multiplexor': 'first',
            'partial_stat': 'first', 'data_invalid': 'first', 'ch_path_online': 'first', 'es_connection_ch': 'first',
            'es_connection_dir': 'first', 'es_conv_ch': 'first', 'ch_path_modified': 'first',
            'ch_path_deleted': 'first', 'ch_path_inserted': 'first', 'valid_path': 'first', 'ch_path_shared': 'first',
            'cpmb_invalid': 'first', 'ctc_defined': 'first', 'ch_conversion': 'first', 'ch_path_dcm': 'first',
            'ch_charact_changed': 'first', 'ch_path_extended': 'first', 'physical_network': 'first', 'smf73bsy': 'sum',
            'smf73pby': 'sum', 'smf73pti': 'first', 'smf73cpd': 'first', 'smf73acr': 'first', 'smf73cmg': 'first',
            'cpmf_word1': 'first', 'cpmf_word2': 'first', 'cpmf_word3': 'first', 'cpmf_word4': 'first',
            'cpmf_word5': 'first', 'smf73cpp': 'first', 'smf73gen': 'first', 'smf73eix': 'first', 'smf73spd': 'last',
            'smf73msc': 'last', 'smf73nt1': 'first', 'smf73nt2': 'first', 'part_utilization_pct': 'mean',
            'total_utilization_pct': 'mean', 'bus_utilization_pct': 'mean',
            'smf73fg2': 'last', 'smf73fg3': 'last', 'smf73fg4': 'last', 'smf73fg5': 'last', 'smf73ioen': 'last'}
agg_cha2 = {'block_multiplexor': 'first', 'byte_multiplexor': 'first', 'partial_stat': 'first', 'data_invalid': 'first',
            'ch_path_online': 'first', 'es_connection_ch': 'first', 'es_connection_dir': 'first', 'es_conv_ch': 'first',
            'ch_path_modified': 'first', 'ch_path_deleted': 'first', 'ch_path_inserted': 'first', 'valid_path': 'first',
            'ch_path_shared': 'first', 'cpmb_invalid': 'first', 'ctc_defined': 'first', 'ch_conversion': 'first',
            'ch_path_dcm': 'first', 'ch_charact_changed': 'first', 'ch_path_extended': 'first',
            'physical_network': 'first', 'smf73bsy': 'sum', 'smf73pby': 'sum', 'smf73pti': 'first', 'smf73cpd': 'first',
            'smf73acr': 'first', 'smf73cmg': 'first', 'cpmf_word1': 'first', 'cpmf_word2': 'first',
            'cpmf_word3': 'first', 'cpmf_word4': 'first', 'cpmf_word5': 'first', 'smf73cpp': 'first',
            'smf73gen': 'first', 'smf73eix': 'first', 'smf73spd': 'last', 'smf73msc': 'last', 'smf73nt1': 'first',
            'smf73nt2': 'first', 'smf73mbc': 'max', 'smf73mcu': 'max', 'smf73mwu': 'max', 'smf73mru': 'max',
            'smf73us': 'first', 'smf73tbc': 'sum', 'smf73tuc': 'sum', 'smf73puc': 'sum', 'smf73twu': 'sum',
            'smf73pwu': 'sum', 'smf73tru': 'sum', 'smf73pru': 'sum', 'smf73eoc': 'sum', 'smf73eod': 'sum',
            'smf73eos': 'sum', 'smf73etc': 'sum', 'smf73etd': 'sum', 'smf73ets': 'sum', 'part_utilization_pct': 'mean',
            'total_utilization_pct': 'mean', 'bus_utilization_pct': 'mean', 'part_read_rate': 'mean',
            'total_read_rate': 'mean', 'part_write_rate': 'mean', 'total_write_rate': 'mean',
            'ficon_operations_rate': 'mean', 'ficon_operations_active': 'mean', 'ficon_operations_defer': 'mean',
            'zhpf_operations_rate': 'mean', 'zhpf_operations_active': 'mean', 'zhpf_operations_defer': 'mean',
            'smf73fg2': 'last', 'smf73fg3': 'last', 'smf73fg4': 'last', 'smf73fg5': 'last', 'smf73ioen': 'last'}
agg_cha3 = {'block_multiplexor': 'first', 'byte_multiplexor': 'first', 'partial_stat': 'first', 'data_invalid': 'first',
            'ch_path_online': 'first', 'es_connection_ch': 'first', 'es_connection_dir': 'first', 'es_conv_ch': 'first',
            'ch_path_modified': 'first', 'ch_path_deleted': 'first', 'ch_path_inserted': 'first', 'valid_path': 'first',
            'ch_path_shared': 'first', 'cpmb_invalid': 'first', 'ctc_defined': 'first', 'ch_conversion': 'first',
            'ch_path_dcm': 'first', 'ch_charact_changed': 'first', 'ch_path_extended': 'first',
            'physical_network': 'first', 'smf73bsy': 'sum', 'smf73pby': 'sum', 'smf73pti': 'first', 'smf73cpd': 'first',
            'smf73acr': 'first', 'smf73cmg': 'first', 'cpmf_word1': 'first', 'cpmf_word2': 'first',
            'cpmf_word3': 'first', 'cpmf_word4': 'first', 'cpmf_word5': 'first', 'smf73cpp': 'first',
            'smf73gen': 'first', 'smf73eix': 'first', 'smf73spd': 'last', 'smf73msc': 'last', 'smf73nt1': 'first',
            'smf73nt2': 'first', 'smf73pdu': 'sum', 'smf73tdu': 'sum', 'smf73pum': 'sum', 'smf73tum': 'sum',
            'smf73pms': 'sum', 'smf73tms': 'sum', 'smf73pus': 'sum', 'smf73pub': 'sum', 'smf73tub': 'sum',
            'smf73pds': 'sum', 'smf73tds': 'sum', 'part_read_rate': 'mean', 'total_read_rate': 'mean',
            'part_write_rate': 'mean', 'total_write_rate': 'mean', 'message_rate_part': 'mean',
            'message_rate_total': 'mean', 'message_size_part': 'mean', 'message_size_total': 'mean',
            'send_fail_part': 'mean', 'receive_fail_part': 'mean', 'receive_fail_total': 'mean',
            'smf73fg2': 'last', 'smf73fg3': 'last', 'smf73fg4': 'last', 'smf73fg5': 'last', 'smf73ioen': 'last'}
agg_cha4 = {'block_multiplexor': 'first', 'byte_multiplexor': 'first', 'partial_stat': 'first', 'data_invalid': 'first',
            'ch_path_online': 'first', 'es_connection_ch': 'first', 'es_connection_dir': 'first', 'es_conv_ch': 'first',
            'ch_path_modified': 'first', 'ch_path_deleted': 'first', 'ch_path_inserted': 'first', 'valid_path': 'first',
            'ch_path_shared': 'first', 'cpmb_invalid': 'first', 'ctc_defined': 'first', 'ch_conversion': 'first',
            'ch_path_dcm': 'first', 'ch_charact_changed': 'first', 'ch_path_extended': 'first',
            'physical_network': 'first', 'smf73bsy': 'sum', 'smf73pby': 'sum', 'smf73pti': 'first', 'smf73cpd': 'first',
            'smf73acr': 'first', 'smf73cmg': 'first', 'cpmf_word1': 'first', 'cpmf_word2': 'first',
            'cpmf_word3': 'first', 'cpmf_word4': 'first', 'cpmf_word5': 'first', 'smf73cpp': 'first',
            'smf73gen': 'first', 'smf73eix': 'first', 'smf73spd': 'last', 'smf73msc': 'last', 'smf73nt1': 'first',
            'smf73nt2': 'first', 'smf73g4mbc': 'max', 'smf73g4mcu': 'max', 'smf73g4mwu': 'max', 'smf73g4mru': 'max',
            'smf73g4ioec': 'last', 'smf73g4us': 'first', 'smf73g4tbc': 'sum', 'smf73g4tuc': 'sum', 'smf73g4puc': 'sum',
            'smf73g4twu': 'sum', 'smf73g4pwu': 'sum', 'smf73g4tru': 'sum', 'smf73g4pru': 'sum', 'smf73g4ecet': 'sum',
            'smf73g4eioet': 'sum',
            'total_utilization_pct': 'mean', 'bus_utilization_pct': 'mean', 'part_read_rate': 'mean',
            'total_read_rate': 'mean', 'part_write_rate': 'mean', 'total_write_rate': 'mean',
            'smf73fg2': 'last', 'smf73fg3': 'last', 'smf73fg4': 'last', 'smf73fg5': 'last', 'smf73ioen': 'last'
            }
agg_cha5 = {'block_multiplexor': 'first', 'byte_multiplexor': 'first', 'partial_stat': 'first', 'data_invalid': 'first',
            'ch_path_online': 'first', 'es_connection_ch': 'first', 'es_connection_dir': 'first', 'es_conv_ch': 'first',
            'ch_path_modified': 'first', 'ch_path_deleted': 'first', 'ch_path_inserted': 'first', 'valid_path': 'first',
            'ch_path_shared': 'first', 'cpmb_invalid': 'first', 'ctc_defined': 'first', 'ch_conversion': 'first',
            'ch_path_dcm': 'first', 'ch_charact_changed': 'first', 'ch_path_extended': 'first',
            'physical_network': 'first', 'smf73bsy': 'sum', 'smf73pby': 'sum', 'smf73pti': 'first', 'smf73cpd': 'first',
            'smf73acr': 'first', 'smf73cmg': 'first', 'cpmf_word1': 'first', 'cpmf_word2': 'first',
            'cpmf_word3': 'first', 'cpmf_word4': 'first', 'cpmf_word5': 'first', 'smf73cpp': 'first',
            'smf73gen': 'first', 'smf73eix': 'first', 'smf73spd': 'last', 'smf73msc': 'last', 'smf73nt1': 'first',
            'smf73nt2': 'first', 'smf73g5mbc': 'max', 'smf73g5mcu': 'max', 'smf73g5mwu': 'max', 'smf73g5mru': 'max',
            'smf73g5ioec': 'last', 'smf73g5us': 'first', 'smf73g5tbc': 'sum', 'smf73g5tuc': 'sum', 'smf73g5puc': 'sum',
            'smf73g5twu': 'sum', 'smf73g5pwu': 'sum', 'smf73g5tru': 'sum', 'smf73g5pru': 'sum', 'smf73g5ecet': 'sum',
            'smf73g5eioet': 'sum', 'smf73g5eoc': 'sum', 'smf73g5eod': 'sum', 'smf73g5eos': 'sum', 'smf73g5etc': 'sum',
            'smf73g5etd': 'sum', 'smf73g5ets': 'sum',
            'total_utilization_pct': 'mean', 'bus_utilization_pct': 'mean', 'part_read_rate': 'mean',
            'total_read_rate': 'mean', 'part_write_rate': 'mean', 'total_write_rate': 'mean',
            'ficon_operations_rate': 'mean', 'ficon_operations_active': 'mean', 'ficon_operations_defer': 'mean',
            'zhpf_operations_rate': 'mean', 'zhpf_operations_active': 'mean', 'zhpf_operations_defer': 'mean',
            'smf73fg2': 'last', 'smf73fg3': 'last', 'smf73fg4': 'last', 'smf73fg5': 'last', 'smf73ioen': 'last'
            }

agg_pro = {'smf73flg': 'first',
           'smf73gie': 'last', 'smf73mfv': 'last', 'smf73int': 'sum',
           'smf73sam': 'sum', 'smf73cyc': 'last', 'smf73mvs': 'last', 'smf73iml': 'last', 'smf73ptn': 'last',
           'smf73srl': 'last', 'smf73lgo': 'last', 'smf73oil': 'last', 'smf73syn': 'last', 'smf73xnm': 'last',
           'smf73snm': 'last', 'speed_boost': agg_boost, 'ziip_boost': agg_boost,
           'smf73prd': 'last', 'smf73fla': 'last', 'smf73prf': 'last'}


def sum_73db(db_engines: dict, db_session: Session, summary_level: str, start_time_str: str, end_time_str: str,
             partitions_scheme: str, db_driver: str = 'postgresql+psycopg2') -> UploadResult:
    """Summarize smf73 interval database to the hourly or daily database.

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

    insert_dict = {'ctl': 0, 'cha1': 0, 'cha2': 0, 'cha3': 0, 'cha4': 0, 'cha5': 0, 'pro': 0}
    summary_class = {'hourly': tbls_hr, 'daily': tbls_da}
    summary_tblname = {'hourly': tblnames_hr, 'daily': tblnames_da}
    summary_engine = {'hourly': '73.hourly', 'daily': '73.daily'}

    result_list = []

    st = time.time()
    current_time = dt.datetime.now()

    # sum up hr tbls
    insert_dict['ctl'] = sum_up_by_partition(tbls['ctl'], summary_class[summary_level]['ctl'],
                                             summary_tblname[summary_level]['ctl'],
                                             start, end, current_time, agg_ctl, int_dtypedict['ctl'],
                                             partitions_scheme, summary_engine[summary_level],
                                             db_engines,'73', 'smf73', db_session, db_driver)

    insert_dict['cha1']  = sum_up_by_partition(tbls['cha1'], summary_class[summary_level]['cha1'],
                                             summary_tblname[summary_level]['cha1'],
                                             start, end, current_time, agg_cha1, int_dtypedict['cha1'],
                                             partitions_scheme, summary_engine[summary_level],
                                             db_engines, '73', 'smf73', db_session, db_driver)

    insert_dict['cha2'] = sum_up_by_partition(tbls['cha2'], summary_class[summary_level]['cha2'],
                                              summary_tblname[summary_level]['cha2'],
                                              start, end, current_time, agg_cha2, int_dtypedict['cha2'],
                                              partitions_scheme, summary_engine[summary_level],
                                              db_engines, '73', 'smf73', db_session, db_driver)

    insert_dict['cha3'] = sum_up_by_partition(tbls['cha3'], summary_class[summary_level]['cha3'],
                                              summary_tblname[summary_level]['cha3'],
                                              start, end, current_time, agg_cha3, int_dtypedict['cha3'],
                                              partitions_scheme, summary_engine[summary_level],
                                              db_engines, '73', 'smf73', db_session, db_driver)

    insert_dict['cha4'] = sum_up_by_partition(tbls['cha4'], summary_class[summary_level]['cha4'],
                                              summary_tblname[summary_level]['cha4'],
                                              start, end, current_time, agg_cha4, int_dtypedict['cha4'],
                                              partitions_scheme, summary_engine[summary_level],
                                              db_engines, '73', 'smf73', db_session, db_driver)

    insert_dict['cha5'] = sum_up_by_partition(tbls['cha5'], summary_class[summary_level]['cha5'],
                                              summary_tblname[summary_level]['cha5'],
                                              start, end, current_time, agg_cha5, int_dtypedict['cha5'],
                                              partitions_scheme, summary_engine[summary_level],
                                              db_engines, '73', 'smf73', db_session, db_driver)

    df_pro_list = []
    pro_stmt = select(Smf73Pro).where(Smf73Pro.datetime.between(start, end))
    for part in partitions_range:
        df_pro = pd.read_sql(pro_stmt, db_engines[f'73.{part}'])
        if not df_pro.empty:
            df_pro['date'] = df_pro['datetime'].dt.date
            df_pro_list.append(df_pro)
    if len(df_pro_list) > 0:
        df_pros = pd.concat(df_pro_list)
        df_pro_sum = df_pros.groupby(
            [col.name for col in summary_class[summary_level]['pro'].__table__.primary_key.columns.values()]).agg(
            agg_pro).reset_index()
        if 'date' not in df_pro_sum.columns:
            df_pro_sum['date'] = df_pro_sum['datetime'].dt.date

        df_pro_sum['last_update_time'] = current_time
        df_pro_sum[['speed_boost', 'speed_boost_change']] = pd.DataFrame(
            df_pro_sum['speed_boost'].tolist(), index=df_pro_sum.index)
        df_pro_sum[['ziip_boost', 'ziip_boost_change']] = pd.DataFrame(df_pro_sum['ziip_boost'].tolist(),
                                                                      index=df_pro_sum.index)
        insert_dict['pro'] = df_upsert(db_driver, db_engines[summary_engine[summary_level]], db_session,
                                       df_pro_sum[summary_class[summary_level]['pro'].__table__.columns.keys()],
                                       summary_tblname[summary_level]['pro'], summary_class[summary_level]['pro'],
                                       'smf73',
                                       [col.name for col in
                                        summary_class[summary_level]['pro'].__table__.primary_key.columns.values()],
                                       int_dtypedict['pro'], shard_id=summary_engine[summary_level]
                                       )
    result_list.append({summary_tblname[summary_level][k]:v for k,v in insert_dict.items() if k in summary_tblname[summary_level].keys()})

    et = time.time()  # get the end time
    # get the execution time
    elapsed_time = (et - st) / 60
    print(f'Execution time ({summary_level}):', elapsed_time, 'minutes')

    overall_et = time.time()
    overall_elapsed_time = (overall_et - overall_st) / 60
    return UploadResult(result_list, overall_elapsed_time, SUCCESS)

