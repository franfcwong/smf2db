import datetime as dt
import time

import numpy as np
import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from smf2db import SUCCESS
from smf2db.api.util import (agg_boost, df_upsert, UploadResult, create_int_dtypedict, is_bit_set, sum_up_by_partition)
from smf2db.db_models.smf71_da_model import Base71Da, Smf71PagDa, Smf71ProDa
from smf2db.db_models.smf71_hr_model import Base71Hr, Smf71PagHr, Smf71ProHr
from smf2db.db_models.smf71_model import Smf71Pag, Smf71Pro


tbls = {'pro': Smf71Pro,
        'pag': Smf71Pag}
tbls_hr = {'pro': Smf71ProHr,
           'pag': Smf71PagHr}
tbls_da = {'pro': Smf71ProDa,
           'pag': Smf71PagDa}
tblnames = {'pro': 'smf71_pro',
            'pag': 'smf71_pag'}
tblnames_hr = {'pro': 'smf71_pro_hr',
               'pag': 'smf71_pag_hr'}
tblnames_da = {'pro': 'smf71_pro_da',
               'pag': 'smf71_pag_da'}
int_dtypedict = create_int_dtypedict(tbls)

agg_pro = {'smf71flg': 'first',
           'smf71gie': 'last', 'smf71mfv': 'last',
           'smf71int': 'sum', 'smf71sam': 'sum', 'smf71cyc': 'last', 'smf71mvs': 'last',
           'smf71iml': 'last', 'smf71ptn': 'last', 'smf71srl': 'last', 'smf71lgo': 'last',
           'smf71oil': 'last', 'smf71syn': 'last', 'smf71xnm': 'last', 'smf71snm': 'last',
           'speed_boost': agg_boost, 'ziip_boost': agg_boost,
           'smf71prd': 'last', 'smf71fla': 'last', 'smf71prf': 'last'}
agg_pag = {'smf71pin': 'sum', 'total_nvio_pgout_nswap': 'sum', 'smf71ssq': 'sum', 'smf71sin': 'sum', 'smf71sot': 'sum',
           'smf71vin': 'sum', 'smf71vot': 'sum', 'smf71sni': 'sum', 'sys_sum_pgout_nswap': 'sum', 'smf71lni': 'sum',
           'smf71afc': 'sum', 'smf71tfc': 'sum', 'smf71tsc': 'sum', 'smf71blp': 'sum',
           'smf71dsc': 'sum', 'smf71vsc': 'sum', 'smf71nsc': 'sum', 'smf71fin': 'sum', 'smf71mnf': 'min',
           'smf71mxf': 'max', 'smf71avf': 'mean', 'smf71mnp': 'min', 'smf71mxp': 'max', 'smf71avp': 'mean',
           'smf71mns': 'min', 'smf71mxs': 'max', 'smf71avs': 'mean', 'smf71mnt': 'min', 'smf71mxt': 'max',
           'smf71avt': 'mean', 'smf71mnq': 'min', 'smf71mxq': 'max', 'smf71avq': 'mean', 'smf71mnc': 'min',
           'smf71mxc': 'max', 'smf71avc': 'mean', 'smf71mnr': 'min', 'smf71mxr': 'max', 'smf71avr': 'mean',
           'smf71mnx': 'min', 'smf71mxx': 'max', 'smf71avx': 'mean', 'smf71mnu': 'min', 'smf71mxu': 'max',
           'smf71avu': 'mean', 'smf71mnv': 'min', 'smf71mxv': 'max', 'smf71avv': 'mean', 'smf71mnm': 'min',
           'smf71mxm': 'max', 'smf71avm': 'mean', 'smf71mnb': 'min', 'smf71mxb': 'max', 'smf71avb': 'mean',
           'smf71mna': 'min', 'smf71mxa': 'max', 'smf71is1': 'sum', 'smf71is2': 'sum', 'smf71nlp': 'min',
           'smf71xlp': 'max', 'smf71alp': 'mean', 'smf71nlf': 'min', 'smf71xlf': 'max', 'smf71alf': 'mean',
           'smf71nls': 'min', 'smf71xls': 'max', 'smf71als': 'mean', 'smf71mnl': 'min', 'smf71mxl': 'max',
           'smf71avl': 'mean', 'pg_mv_within_cs': 'sum',  'smf71opt': 'first', 'smf71lic': 'min', 'smf71hic': 'max',
           'smf71aca': 'mean', 'smf71msr': 'min', 'smf71xsr': 'max', 'smf71asr': 'mean', 'smf71xlr': 'max',
           'smf71mlr': 'min', 'smf71alr': 'mean', 'smf71isc': 'sum', 'smf71hot': 'sum', 'smf71hin': 'sum',
           'total_nvio_pgin_nswap_blk': 'sum', 'total_sum_pgin_nswap_blk': 'sum', 'total_sum_pgin_nswap_nblk': 'sum',
           'smf71pmt': 'sum', 'smf71sbi': 'sum', 'smf71lbi': 'sum', 'smf71asi': 'sum', 'smf71aso': 'sum',
           'smf71mgt': 'min', 'smf71xgt': 'max', 'smf71agt': 'mean', 'smf71mgc': 'min', 'smf71xgc': 'max',
           'smf71agc': 'mean', 'smf71mga': 'min', 'smf71xga': 'max', 'smf71aga': 'mean', 'smf71mgf': 'min',
           'smf71xgf': 'max', 'smf71agf': 'mean', 'smf71mgb': 'min', 'smf71xgb': 'max', 'smf71agb': 'mean',
           'smf71cam': 'min', 'smf71cax': 'max', 'smf71caa': 'mean', 'smf71clm': 'min', 'smf71clx': 'max',
           'smf71cla': 'mean', 'smf71cmm': 'min', 'smf71cmx': 'max', 'smf71cma': 'mean', 'smf71chm': 'min',
           'smf71chx': 'max', 'smf71cha': 'mean', 'smf71mvi': 'min', 'smf71xvi': 'max', 'smf71avi': 'mean',
           'smf71mhi': 'min', 'smf71xhi': 'max', 'smf71ahi': 'mean', 'smf71vws': 'sum', 'smf71vrs': 'sum',
           'smf71hws': 'sum', 'smf71hrs': 'sum', 'smf71mfb': 'min', 'smf71xfb': 'max', 'smf71afb': 'mean',
           'smf71pth': 'mean', 'smf71pch': 'mean', 'smf71pah': 'mean', 'smf71blg': 'max', 'smf71pih': 'sum',
           'smf71poh': 'sum', 'smf71ulm': 'min', 'smf71ulc': 'min', 'smf71uhc': 'min', 'smf71uhx': 'min',
           'smf71uam': 'mean', 'smf71uac': 'mean', 'smf71uax': 'mean', 'smf71lom': 'min', 'smf71lox': 'max',
           'smf71loa': 'mean', 'smf71lrm': 'min', 'smf71lrx': 'max', 'smf71lra': 'mean', 'smf71com': 'min',
           'smf71cox': 'max', 'smf71coa': 'mean', 'smf71crm': 'min', 'smf71crx': 'max', 'smf71cra': 'mean',
           'smf71cfm': 'min', 'smf71cfx': 'max', 'smf71cfa': 'mean', 'smf71csm': 'min', 'smf71csx': 'max',
           'smf71csa': 'mean', 'smf71som': 'min', 'smf71sox': 'max', 'smf71soa': 'mean', 'smf71srm': 'min',
           'smf71srx': 'max', 'smf71sra': 'mean', 'smf71grn': 'sum', 'smf71fbn': 'sum', 'smf71frn': 'sum',
           'smf71ffn': 'sum', 'smf711rn': 'sum', 'smf71nrn': 'sum', 'smf71rfl': 'last',
           'smf71lfa': 'max', 'smf71l1m': 'min', 'smf71l1x': 'max', 'smf71l1a': 'mean', 'smf71l2m': 'min',
           'smf71l2x': 'max', 'smf71l2a': 'mean', 'smf71l3m': 'min', 'smf71l3x': 'max', 'smf71l3a': 'mean',
           'smf71l7m': 'min', 'smf71l7x': 'max', 'smf71l7a': 'mean', 'smf71s1m': 'min', 'smf71s1x': 'max',
           'smf71s1a': 'mean', 'smf71s2m': 'min', 'smf71s2x': 'max', 'smf71s2a': 'mean', 'smf71s3m': 'min',
           'smf71s3x': 'max', 'smf71s3a': 'mean', 'smf71s4m': 'min', 'smf71s4x': 'max', 'smf71s4a': 'mean',
           'smf71s5m': 'min', 'smf71s5x': 'max', 'smf71s5a': 'mean', 'smf71s6m': 'min', 'smf71s6x': 'max',
           'smf71s6a': 'mean', 'smf71c1m': 'min', 'smf71c1x': 'max', 'smf71c1a': 'mean', 'smf71c2m': 'min',
           'smf71c2x': 'max', 'smf71c2a': 'mean', 'smf71c3m': 'min', 'smf71c3x': 'max', 'smf71c3a': 'mean',
           'smf71c4m': 'min', 'smf71c4x': 'max', 'smf71c4a': 'mean', 'smf71tsm': 'min', 'smf71tsx': 'max',
           'smf71tsa': 'mean', 'smf71asm': 'min', 'smf71asx': 'max', 'smf71asv': 'mean', 'smf71bsm': 'min',
           'smf71bsx': 'max', 'smf71bsa': 'mean', 'smf71usm': 'min', 'smf71usx': 'max', 'smf71usa': 'mean',
           'smf71tls': 'sum', 'smf71s7m': 'min', 'smf71s7x': 'max', 'smf71s7a': 'mean', 'smf71lvf': 'mean',
           'smf71lvs': 'mean', 'smf71lvt': 'mean', 'smf71lvr': 'mean', 'smf71lvx': 'mean', 'smf71lvu': 'mean',
           'smf71lvv': 'mean', 'smf71lvm': 'mean', 'smf71lvb': 'mean', 'smf71mcf': 'first', 'smf71cpm': 'min',
           'smf71cpx': 'max', 'smf71cpa': 'mean', 'smf71plm': 'min', 'smf71plx': 'max', 'smf71pla': 'mean',
           'smf71gom': 'min', 'smf71gox': 'max', 'smf71goa': 'mean', 'smf71grm': 'min', 'smf71grx': 'max',
           'smf71gra': 'mean', 'smf71gum': 'min', 'smf71gux': 'max', 'smf71gua': 'mean', 'smf71guh': 'max',
           'smf71gam': 'min', 'smf71gax': 'max', 'smf71gaa': 'mean', 'smf71gfm': 'min', 'smf71gfx': 'max',
           'smf71gfa': 'mean', 'smf71nnf': 'mean', 'smf71lsi': 'mean', 'smf71lri': 'mean', 'smf71mhw': 'max',
           'smf71pis': 'mean', 'smf71pos': 'mean', 'smf71pi1': 'mean', 'smf71po1': 'mean', 'smf71l8m': 'min',
           'smf71l8x': 'max', 'smf71l8a': 'mean', 'smf71l9m': 'min', 'smf71l9x': 'max', 'smf71l9a': 'mean',
           'smf71l10m': 'min', 'smf71l10x': 'max', 'smf71l10a': 'mean', 'smf71m6c': 'min', 'smf71x6c': 'max',
           'smf71a6c': 'mean', 'smf71m6f': 'min', 'smf71x6f': 'max', 'smf71a6f': 'mean', 'smf71m6b': 'min',
           'smf71x6b': 'max', 'smf71a6b': 'mean', 'smf71m6a': 'min', 'smf71x6a': 'max', 'smf71a6a': 'mean',
           'smf71m6s': 'min', 'smf71x6s': 'max', 'smf71a6s': 'mean', 'smf71m6t': 'min', 'smf71x6t': 'max',
           'smf71a6t': 'mean', 'smf71pmv': 'sum', 'smf71sno': 'sum', 'smf71blk': 'sum', 'smf71pot': 'sum',
           'pg_mv_rate': 'mean', 'pg_mv_time_percentage': 'mean', 'avg_pg_per_blk': 'mean', 'blk_per_seconds': 'mean',
           'pg_fault_rate': 'mean', 'sys_csa_pgin_nswap_blk': 'sum', 'sys_csa_pgin_nswap_nblk': 'sum',
           'as_nvio_pgin_nswap_nblk': 'sum', 'as_sum_pgout_nswap': 'sum', 'total_vio_pgout_nswap': 'sum',
           'as_sum_pgin_swap': 'sum', 'as_sum_pgin_nswap_blk': 'sum', 'as_sum_pgin_nswap_nblk': 'sum',
           'as_sum_pgout_swap': 'sum', 'total_hspace_pgin_nswap_blk': 'sum', 'total_hspace_pgout_nswap': 'sum',
           'total_vio_pgin_nswap_blk': 'sum', 'total_nvio_pgin_swap': 'sum', 'total_nvio_pgout_swap': 'sum',
           'total_sum_pgin_swap': 'sum', 'total_sum_pgout_swap': 'sum', 'total_sum_pgout_nswap': 'sum',
           'smf71_dmemassignable2g': 'sum', 'smf71_dmemnumberofjobsusingdmem_m': 'min',
           'smf71_dmemnumberofjobsusingdmem_x': 'max', 'smf71_dmemnumberofjobsusingdmem_a': 'mean',
           'smf71_dmemtotal2g_m': 'min', 'smf71_dmemtotal2g_x': 'max', 'smf71_dmemtotal2g_a': 'mean',
           'smf71_dmemtotalonline2g_m': 'min', 'smf71_dmemtotalonline2g_x': 'max',
           'smf71_dmemtotalonline2g_a': 'mean', 'smf71_dmemavailable2g_m': 'min',
           'smf71_dmemavailable2g_x': 'max', 'smf71_dmemavailable2g_a': 'mean',
           'smf71_dmemrequested2g_m': 'min', 'smf71_dmemrequested2g_x': 'max',
           'smf71_dmemrequested2g_a': 'mean', 'smf71_dmemminrequested2g_m': 'min',
           'smf71_dmemminrequested2g_x': 'max', 'smf71_dmemminrequested2g_a': 'mean',
           'smf71_dmemassigned2g_m': 'min', 'smf71_dmemassigned2g_x': 'max',
           'smf71_dmemassigned2g_a': 'mean', 'smf71_dmeminuseas2g_m': 'min',
           'smf71_dmeminuseas2g_x': 'max', 'smf71_dmeminuseas2g_a': 'mean',
           'smf71_dmeminuseas1mfixed_m': 'min', 'smf71_dmeminuseas1mfixed_x': 'max',
           'smf71_dmeminuseas1mfixed_a': 'mean', 'smf71_dmeminuseas1mpageable_m': 'min',
           'smf71_dmeminuseas1mpageable_x': 'max', 'smf71_dmeminuseas1mpageable_a': 'mean',
           'smf71_dmeminuseas4k_m': 'min', 'smf71_dmeminuseas4k_x': 'max', 'smf71_dmeminuseas4k_a': 'mean',
           'smf71_dmeminuseasdattables4k_m': 'min', 'smf71_dmeminuseasdattables4k_x': 'max',
           'smf71_dmeminuseasdattables4k_a': 'mean'}

def sum_71db(db_engines: dict, db_session: Session, summary_level: str, start_time_str: str, end_time_str: str,
             partitions_scheme: str, db_driver: str = 'postgresql+psycopg2') -> UploadResult:
    """Summarize smf71 interval database to the hourly or daily database.

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

    insert_dict = {'pag': 0, 'pro': 0}
    summary_class = {'hourly': tbls_hr, 'daily': tbls_da}
    summary_tblname = {'hourly': tblnames_hr, 'daily': tblnames_da}
    summary_engine = {'hourly': '71.hourly', 'daily': '71.daily'}

    result_list = []
    st = time.time()
    current_time = dt.datetime.now()

    # Summing up Smf71Pag
    insert_dict['pag'] = sum_up_by_partition(tbls['pag'], summary_class[summary_level]['pag'],
                                             summary_tblname[summary_level]['pag'],
                                             start, end, current_time, agg_pag, int_dtypedict['pag'],
                                             partitions_scheme, summary_engine[summary_level],
                                             db_engines, '71', 'smf71', db_session, db_driver)

    df_pro_list = []
    pro_stmt = select(Smf71Pro).where(Smf71Pro.datetime.between(start, end))
    for part in partitions_range:
        df_pro = pd.read_sql(pro_stmt, db_engines[f'71.{part}'])
        if not df_pro.empty:
            df_pro['date'] = df_pro['datetime'].dt.date
            df_pro_list.append(df_pro)
    if len(df_pro_list) > 0:
        df_pros = pd.concat(df_pro_list)
        df_pros['speed_boost'] = df_pros['smf71fla'].apply(lambda x: is_bit_set(x, 16, 10) if pd.notna(x) else np.nan)
        df_pros['ziip_boost'] = df_pros['smf71fla'].apply(
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
                                       'smf71',
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

