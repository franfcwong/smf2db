import datetime as dt
import time

import numpy as np
import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from smf2db import SUCCESS
from smf2db.api.api_72 import (cal_performance_index, agg_scs_group_by, agg_rts)
from smf2db.api.util import (UploadResult,
                             create_int_dtypedict, is_bit_set, df_upsert, sum_up_by_partition)
from smf2db.db_models.smf72_da_model import (Smf72ProDa, Smf72PolicyDa, Smf72DnsxDa, Smf72WorkloadDa,
                                             Smf72WrsxDa, Smf72ScsDa, Smf72DataDa, Smf72SctlDa, Smf72WmsDa, Smf72SssDa,
                                             Smf72RgsDa, Smf72RtsDa, Smf72WrsDa, Smf72DnsDa, Smf72CmssDa, Smf72CedsDa,
                                             Smf72ClodDa, Smf72ClrdDa, Smf72LotdDa, Smf72LascDa, Smf72LareDa,
                                             Smf72EnseDa, Smf72EnsyDa, Smf72EnssDa, Smf72QsadDa, Smf72ClasDa,
                                             Smf72CsmsDa)
from smf2db.db_models.smf72_hr_model import (Smf72ProHr, Smf72PolicyHr, Smf72DnsxHr, Smf72WorkloadHr,
                                             Smf72WrsxHr, Smf72ScsHr, Smf72DataHr, Smf72SctlHr, Smf72WmsHr, Smf72SssHr,
                                             Smf72RgsHr, Smf72RtsHr, Smf72WrsHr, Smf72DnsHr, Smf72CmssHr, Smf72CedsHr,
                                             Smf72ClodHr, Smf72ClrdHr, Smf72LotdHr, Smf72LascHr, Smf72LareHr,
                                             Smf72EnseHr, Smf72EnsyHr, Smf72EnssHr, Smf72QsadHr, Smf72ClasHr,
                                             Smf72CsmsHr)
from smf2db.db_models.smf72_model import (Smf72Pro, Smf72Policy, Smf72Dnsx, Smf72Workload, Smf72Wrsx, Smf72Scs,
                                          Smf72Data, Smf72Sctl, Smf72Wms, Smf72Sss, Smf72Rgs, Smf72Rts, Smf72Wrs,
                                          Smf72Dns, Smf72Cmss, Smf72Ceds, Smf72Clod, Smf72Clrd, Smf72Lotd, Smf72Lasc,
                                          Smf72Lare, Smf72Ense, Smf72Ensy, Smf72Enss, Smf72Qsad, Smf72Clas, Smf72Csms)

tbls = {'pro': Smf72Pro,
        'policy': Smf72Policy,
        'workload': Smf72Workload,
        'wms': Smf72Wms,
        'sss': Smf72Sss,
        'rgs': Smf72Rgs,
        'rts': Smf72Rts,
        'wrs': Smf72Wrs,
        'wrsx': Smf72Wrsx,
        'dns': Smf72Dns,
        'dnsx': Smf72Dnsx,
        'cmss': Smf72Cmss,
        'ceds': Smf72Ceds,
        'clas': Smf72Clas,
        'csms': Smf72Csms,
        'clod': Smf72Clod,
        'clrd': Smf72Clrd,
        'lotd': Smf72Lotd,
        'lare': Smf72Lare,
        'lasc': Smf72Lasc,
        'ense': Smf72Ense,
        'enss': Smf72Enss,
        'ensy': Smf72Ensy,
        'qsad': Smf72Qsad,
        'scs': Smf72Scs,
        'data': Smf72Data,
        'sctl': Smf72Sctl}
tbls_hr = {'pro': Smf72ProHr,
           'policy': Smf72PolicyHr,
           'workload': Smf72WorkloadHr,
           'wms': Smf72WmsHr,
           'sss': Smf72SssHr,
           'rgs': Smf72RgsHr,
           'rts': Smf72RtsHr,
           'wrs': Smf72WrsHr,
           'wrsx': Smf72WrsxHr,
           'dns': Smf72DnsHr,
           'dnsx': Smf72DnsxHr,
           'cmss': Smf72CmssHr,
           'ceds': Smf72CedsHr,
           'clas': Smf72ClasHr,
           'csms': Smf72CsmsHr,
           'clod': Smf72ClodHr,
           'clrd': Smf72ClrdHr,
           'lotd': Smf72LotdHr,
           'lare': Smf72LareHr,
           'lasc': Smf72LascHr,
           'ense': Smf72EnseHr,
           'enss': Smf72EnssHr,
           'ensy': Smf72EnsyHr,
           'qsad': Smf72QsadHr,
           'scs': Smf72ScsHr,
           'data': Smf72DataHr,
           'sctl': Smf72SctlHr}
tblnames = {'pro': 'smf72_pro',
            'policy': 'smf72_policy',
            'workload': 'smf72_workload',
            'wms': 'smf72_wms',
            'sss': 'smf72_sss',
            'rgs': 'smf72_rgs',
            'rts': 'smf72_rts',
            'wrs': 'smf72_wrs',
            'wrsx': 'smf72_wrsx',
            'dns': 'smf72_dns',
            'dnsx': 'smf72_dnsx',
            'cmss': 'smf72_cmss',
            'ceds': 'smf72_ceds',
            'clas': 'smf72_clas',
            'csms': 'smf72_csms',
            'clod': 'smf72_clod',
            'clrd': 'smf72_clrd',
            'lotd': 'smf72_lotd',
            'lare': 'smf72_lare',
            'lasc': 'smf72_lasc',
            'ense': 'smf72_ense',
            'enss': 'smf72_enss',
            'ensy': 'smf72_ensy',
            'qsad': 'smf72_qsad',
            'scs': 'smf72_scs',
            'data': 'smf72_data',
            'sctl': 'smf72_sctl'}
tblnames_hr = {'pro': 'smf72_pro_hr',
               'policy': 'smf72_policy_hr',
               'workload': 'smf72_workload_hr',
               'wms': 'smf72_wms_hr',
               'sss': 'smf72_sss_hr',
               'rgs': 'smf72_rgs_hr',
               'rts': 'smf72_rts_hr',
               'wrs': 'smf72_wrs_hr',
               'wrsx': 'smf72_wrsx_hr',
               'dns': 'smf72_dns_hr',
               'dnsx': 'smf72_dnsx_hr',
               'cmss': 'smf72_cmss_hr',
               'ceds': 'smf72_ceds_hr',
               'clas': 'smf72_clas_hr',
               'csms': 'smf72_csms_hr',
               'clod': 'smf72_clod_hr',
               'clrd': 'smf72_clrd_hr',
               'lotd': 'smf72_lotd_hr',
               'lare': 'smf72_lare_hr',
               'lasc': 'smf72_lasc_hr',
               'ense': 'smf72_ense_hr',
               'enss': 'smf72_enss_hr',
               'ensy': 'smf72_ensy_hr',
               'qsad': 'smf72_qsad_hr',
               'scs': 'smf72_scs_hr',
               'data': 'smf72_data_hr',
               'sctl': 'smf72_sctl_hr'}
tbls_da = {'pro': Smf72ProDa,
           'policy': Smf72PolicyDa,
           'workload': Smf72WorkloadDa,
           'wms': Smf72WmsDa,
           'sss': Smf72SssDa,
           'rgs': Smf72RgsDa,
           'rts': Smf72RtsDa,
           'wrs': Smf72WrsDa,
           'wrsx': Smf72WrsxDa,
           'dns': Smf72DnsDa,
           'dnsx': Smf72DnsxDa,
           'cmss': Smf72CmssDa,
           'ceds': Smf72CedsDa,
           'clas': Smf72ClasDa,
           'csms': Smf72CsmsDa,
           'clod': Smf72ClodDa,
           'clrd': Smf72ClrdDa,
           'lotd': Smf72LotdDa,
           'lare': Smf72LareDa,
           'lasc': Smf72LascDa,
           'ense': Smf72EnseDa,
           'enss': Smf72EnssDa,
           'ensy': Smf72EnsyDa,
           'qsad': Smf72QsadDa,
           'scs': Smf72ScsDa,
           'data': Smf72DataDa,
           'sctl': Smf72SctlDa}
tblnames_da = {'pro': 'smf72_pro_da',
               'policy': 'smf72_policy_da',
               'workload': 'smf72_workload_da',
               'wms': 'smf72_wms_da',
               'sss': 'smf72_sss_da',
               'rgs': 'smf72_rgs_da',
               'rts': 'smf72_rts_da',
               'wrs': 'smf72_wrs_da',
               'wrsx': 'smf72_wrsx_da',
               'dns': 'smf72_dns_da',
               'dnsx': 'smf72_dnsx_da',
               'cmss': 'smf72_cmss_da',
               'ceds': 'smf72_ceds_da',
               'clas': 'smf72_clas_da',
               'csms': 'smf72_csms_da',
               'clod': 'smf72_clod_da',
               'clrd': 'smf72_clrd_da',
               'lotd': 'smf72_lotd_da',
               'lare': 'smf72_lare_da',
               'lasc': 'smf72_lasc_da',
               'ense': 'smf72_ense_da',
               'enss': 'smf72_enss_da',
               'ensy': 'smf72_ensy_da',
               'qsad': 'smf72_qsad_da',
               'scs': 'smf72_scs_da',
               'data': 'smf72_data_da',
               'sctl': 'smf72_sctl_da'}

int_dtypedict = create_int_dtypedict(tbls)

agg_wms = {'r723ggnm': 'last', 'r723mcde': 'first', 'r723mscf': 'last', 'r723mflg': 'last', 'r723mfl2': 'last',
           'stor_protection': 'first', 'cpu_protection': 'first',
           'velocity_io_delays': 'first', 'svpol_unaval': 'first', 'rcaa_unaval': 'first',
           'tenant_report_class': 'first', 'honor_prio': 'max', 'hismt_failure': 'max', 'ziip_honor_prio': 'max',
           'zaap_honor_prio': 'max', 'zaap_crossover': 'max',
           'r723mtvl': 'first', 'r723mtv_': 'sum',
           'r723mcpg': 'first', 'r723msub': 'first', 'r723clsc': 'first', 'smf72int': 'sum',
           'appl_percentage_cp_time': 'mean', 'appl_percentage_iipcp_time': 'mean', 'appl_percentage_iip_time': 'mean',
           'appl_percentage_aapcp_time': 'mean', 'appl_percentage_aap_time': 'mean',
           'transaction_total_percentage_cp_time': 'mean', 'transaction_total_percentage_sp_on_cp_time': 'mean',
           'transaction_total_percentage_sp_time': 'mean', 'transaction_mobile_percentage_cp_time': 'mean',
           'transaction_mobile_percentage_sp_on_cp_time': 'mean', 'transaction_mobile_percentage_sp_time': 'mean',
           'transaction_cata_percentage_cp_time': 'mean', 'transaction_cata_percentage_sp_on_cp_time': 'mean',
           'transaction_cata_percentage_sp_time': 'mean', 'transaction_catb_percentage_cp_time': 'mean',
           'transaction_catb_percentage_sp_on_cp_time': 'mean', 'transaction_catb_percentage_sp_time': 'mean'}
agg_scs = {'smf_type': 'first', 'r723cimp': 'first', 'r723crs1': 'last', 'r723cadf': 'last', 'r723crtf': 'last',
           'r723crgf': 'last',
           'is_heterogeneous': 'first', 'r723ceda': 'first',
           'r723crta': 'first', 'r723crca': 'first', 'response_time_hours': 'first', 'response_time_minutes': 'first',
           'response_time_seconds': 'first', 'response_time_millisec': 'first', 'r723cstm': 'first',
           'r723cdsc': 'first', 'r723cvel': 'first', 'r723cavg': 'first', 'r723cprc': 'first',
           'class_goal_type': 'first', 'r723cval': 'first', 'r723cpct': 'first', 'r723cdur': 'first',
           'r723rtdm': 'last', 'r723csrv': 'sum', 'r723ccpu': 'sum', 'r723cioc': 'sum', 'r723cmso': 'sum',
           'r723csrb': 'sum', 'r723cpir': 'sum', 'r723chpi': 'sum', 'r723cbpi': 'sum', 'r723cpie': 'sum',
           'r723cbpe': 'sum', 'r723cbka': 'sum', 'r723cbke': 'sum', 'r723cprs': 'sum', 'r723cers': 'sum',
           'r723ctrr': 'sum', 'r723ctat': 'sum', 'r723crct': 'sum', 'r723ciit': 'sum', 'r723chst': 'sum',
           'r723cswc': 'sum', 'r723ccrm': 'sum', 'r723crcp': 'sum', 'r723carc': 'sum', 'r723cncp': 'sum',
           'r723canc': 'sum', 'r723ctet': 'sum', 'r723ctetx': 'sum', 'transaction_execution_time': 'sum',
           'r723cxetx': 'sum', 'r723cets': 'sum', 'r723cetsx': 'sum', 'r723ccus': 'sum', 'r723ctot': 'sum',
           'r723ccde': 'sum', 'r723ccca': 'sum', 'r723cswi': 'sum', 'r723cmpl': 'sum', 'r723capr': 'sum',
           'r723caco': 'sum', 'r723caxm': 'sum', 'r723cvio': 'sum', 'r723chsp': 'sum', 'r723cchs': 'sum',
           'sample_storage_delay': 'sum', 'r723cunk': 'sum', 'r723cidl': 'sum', 'r723cpde': 'sum', 'r723cpqu': 'sum',
           'r723csac': 'sum', 'r723csrs': 'sum', 'r723cspa': 'sum', 'r723cspe': 'sum', 'r723cict': 'sum',
           'r723ciwt': 'sum', 'r723cidt': 'sum', 'r723circ': 'sum', 'r723ctou': 'sum', 'r723ciou': 'sum',
           'r723ciod': 'sum', 'r723cq': 'sum', 'r723cspv': 'sum', 'r723csvi': 'sum', 'r723cshs': 'sum',
           'r723csmp': 'sum', 'r723cssw': 'sum', 'sample_server_delay': 'sum', 'r723cndi': 'sum', 'r723ctdq': 'sum',
           'r723ctsa': 'sum', 'r723ciot': 'sum', 'transaction_queue_delay_time': 'sum',
           'transaction_aff_delay_time': 'sum', 'transaction_jcl_time': 'sum', 'transaction_inel_delay_time': 'sum',
           'r723ciea': 'sum', 'r723cxea': 'sum', 'r723cfea': 'sum', 'r723apu': 'sum', 'r723apd': 'sum',
           'r723fqd': 'sum', 'sample_crypto_using': 'sum', 'sample_crypto_delay': 'sum', 'r723plsc': 'last',
           'r723rcod': 'sum', 'r723rcou': 'sum', 'r723ectc': 'sum', 'r723ifau': 'sum', 'r723ifcu': 'sum',
           'r723cifa': 'sum', 'r723cifc': 'sum', 'r723ifad': 'sum', 'r723supu': 'sum', 'r723sucu': 'sum',
           'r723supd': 'sum', 'r723csup': 'sum', 'r723csuc': 'sum', 'r723tpdp': 'sum', 'r723cpdp': 'sum',
           'r723lpdp': 'sum', 'r723spdp': 'sum', 'r723rtdc': 'sum', 'r723rtdt': 'last', 'r723tsucp': 'sum',
           'r723tsusp': 'sum', 'r723tsuocp': 'sum', 'r723msucp': 'sum', 'r723msusp': 'sum', 'r723msuocp': 'sum',
           'r723asucp': 'sum', 'r723asusp': 'sum', 'r723asuocp': 'sum', 'r723bsucp': 'sum', 'r723bsusp': 'sum',
           'r723bsuocp': 'sum', 'r723cqdtx': 'sum', 'r723cadtx': 'sum', 'r723ccvtx': 'sum', 'r723ciqtx': 'sum',
           'r723rtyp': 'first',
           'r723ress': 'sum', 'r723ract': 'sum', 'r723rrdy': 'sum', 'r723ridl': 'sum',
           'r723rwlo': 'sum', 'r723rwio': 'sum', 'r723rwco': 'sum', 'r723rwds': 'sum', 'r723rwsl': 'sum',
           'r723rwsn': 'sum', 'r723rwss': 'sum', 'r723rwtm': 'sum', 'r723rwo': 'sum', 'r723rwms': 'sum',
           'r723rssl': 'sum', 'r723rsss': 'sum', 'r723rssn': 'sum', 'r723rwst': 'sum', 'r723rwrt': 'sum',
           'r723rwwr': 'sum', 'r723rapp': 'sum', 'r723rwnl': 'sum', 'r723rbpm': 'sum', 'r723rw01': 'sum',
           'r723rw02': 'sum', 'r723rw03': 'sum', 'r723rw04': 'sum', 'r723rw05': 'sum', 'r723rw06': 'sum',
           'r723rw07': 'sum', 'r723rw08': 'sum', 'r723rw09': 'sum', 'r723rw10': 'sum', 'r723rw11': 'sum',
           'r723rw12': 'sum', 'r723rw13': 'sum', 'r723rw14': 'sum', 'r723rw15': 'sum', 'is_report_class': 'first',
           'sample_rate': 'first', 'r723madj': 'first', 'r723nffs': 'first', 'r723nffi': 'first', 'r723mcpu': 'first',
           'r723msrb': 'first', 'r723cpa_scaling_factor': 'first', 'r723cpa_actual': 'first', 'r723mcf': 'first',
           'r723mcfs': 'first', 'r723mcfi': 'first', 'r723mtv_': 'sum',
           'r723cxet': 'sum', 'r723cqdt': 'sum', 'r723cadt': 'sum', 'r723ccvt': 'sum', 'r723ciqt': 'sum',
           'r723enctrxnum': 'sum', 'r723enctrxcalls': 'sum', 'r723enctrxet': 'sum', 'r723enctrxets': 'sum'}


def sum_72db(db_engines: dict, db_session: Session, summary_level: str, start_time_str: str, end_time_str: str,
             partitions_scheme: str, db_driver: str = 'postgresql+psycopg2') -> UploadResult:
    """Summarize smf72 interval database to the hourly or daily database.

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

    get_performance_index = np.vectorize(cal_performance_index)

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

    insert_dict = {'pro': 0, 'policy': 0, 'workload': 0, 'rgs': 0, 'wms': 0, 'scs': 0, 'data': 0, 'sctl': 0,
                   'sss': 0, 'rts': 0, 'wrsx': 0, 'wrs': 0, 'dnsx': 0, 'dns': 0,
                   'cmss': 0, 'ceds': 0, 'clas': 0, 'csms': 0, 'lotd': 0, 'clod': 0, 'clrd': 0,
                   'lasc': 0, 'lare': 0, 'ense': 0, 'ensy': 0, 'enss': 0, 'qsad': 0}
    summary_class = {'hourly': tbls_hr, 'daily': tbls_da}
    summary_tblname = {'hourly': tblnames_hr, 'daily': tblnames_da}
    summary_engine = {'hourly': '72.hourly', 'daily': '72.daily'}

    result_list = []

    st = time.time()
    current_time = dt.datetime.now()

    # Summing up Smf72Pro
    def agg_boost(series):
        if len(set(series)) == 1:
            return 0, series.iloc[0]
        else:
            return 1, series.iloc[-1]

    agg_pro = {'smf72flg': 'first', 'smf72fla': 'last', 'smf72prf': 'last',
               'smf72gie': 'last', 'smf72mfv': 'last', 'smf72prd': 'last',
               'smf72int': 'sum', 'smf72sam': 'sum', 'smf72cyc': 'last', 'smf72mvs': 'last',
               'smf72iml': 'last', 'smf72ptn': 'last', 'smf72srl': 'last', 'smf72lgo': 'last',
               'smf72oil': 'last', 'smf72syn': 'last', 'csc': 'first', 'smf72snm': 'last',
               'speed_boost': agg_boost, 'ziip_boost': agg_boost,
               }
    df_pro_list = []
    pro_stmt = select(Smf72Pro).where(Smf72Pro.datetime.between(start, end))
    for part in partitions_range:
        df_pro = pd.read_sql(pro_stmt, db_engines[f'72.{part}'])
        if not df_pro.empty:
            df_pro['date'] = df_pro['datetime'].dt.date
            df_pro_list.append(df_pro)
    if len(df_pro_list) > 0:
        df_pros = pd.concat(df_pro_list)
        df_pros['speed_boost'] = df_pros['smf72fla'].apply(
            lambda x: is_bit_set(x, 16, 10) if pd.notna(x) else np.nan)
        df_pros['ziip_boost'] = df_pros['smf72fla'].apply(
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
                                       'smf72',
                                       [col.name for col in
                                        summary_class[summary_level]['pro'].__table__.primary_key.columns.values()],
                                       int_dtypedict['pro'], shard_id=summary_engine[summary_level]
                                       )
    # Summing up Smf72Policy
    agg_policy = {'smf_type': 'first', 'smf72mvs': 'first', 'smf72mfv': 'first', 'smf72int': 'sum',
                 'smf72ist': 'first', 'smf72prf': 'last', 'r723mdsp': 'first', #'r723mflg': 'last',
                 'r723mdis': 'first', 'io_high': 'first',
                 'velocity_io_delays': 'first', 'dynamic_alias': 'first',
                 'r723mtpa': 'last',
                 'r723mcpu': 'last', 'r723mioc': 'last', 'r723mmso': 'last', 'r723msrb': 'last',
                 'r723mopt': 'first', 'r723merf': 'first', 'r723madj': 'first', 'r723midn': 'first',
                 'r723midd': 'first', 'r723mtdi': 'last', 'r723midu': 'last', 'r723nffi': 'last',
                 'r723nffs': 'last', 'r723nadj': 'last', 'r723ceca': 'last', 'r723mcf': 'last',
                 'r723mcfs': 'last', 'r723mcfi': 'last', 'r723cpa_actual': 'last',
                 'r723cpa_scaling_factor': 'last', 'cpu_service_coefficient_adjusted': 'last',
                 'srb_service_coefficient_adjusted': 'last', 'smf70cai': 'last', 'ziip_inst': 'last',
                 'zaap_inst': 'last'}
    df_policy_list = []
    null_column_list = []
    policy_stmt = select(Smf72Policy).where(Smf72Policy.datetime.between(start, end))
    for part in partitions_range:
        df_policy = pd.read_sql(policy_stmt, db_engines[f'72.{part}'])
        if not df_policy.empty:
            df_policy['date'] = df_policy['datetime'].dt.date
            df_policy_list.append(df_policy)
            null_columns = df_policy.columns[df_policy.isna().all()].tolist()
            for col in null_columns:
                if col not in null_column_list:
                    null_column_list.append(col)
    if len(df_policy_list) > 0:
        df_policys = pd.concat([df.dropna(axis=1, how='all') for df in df_policy_list])
        if len(null_column_list) > 0:
            new_cols = df_policys.columns.tolist()
            for col in null_column_list:
                if col not in new_cols:
                    new_cols.append(col)
            df_policys = df_policys.reindex(columns=new_cols)
        df_policy_sum = df_policys.groupby(
            [col.name for col in summary_class[summary_level]['policy'].__table__.primary_key.columns.values()]).agg(
            agg_policy).reset_index().rename(
            columns={'smf72ist': 'interval_start_time'})
        if 'date' not in df_policy_sum.columns:
            df_policy_sum['date'] = df_policy_sum['datetime'].dt.date
        df_policy_sum['last_update_time'] = current_time
        insert_dict['policy'] = df_upsert(db_driver, db_engines[summary_engine[summary_level]], db_session,
                                          df_policy_sum[summary_class[summary_level]['policy'].__table__.columns.keys()],
                                          summary_tblname[summary_level]['policy'],
                                          summary_class[summary_level]['policy'],'smf72',
                                          [col.name for col in
                                           summary_class[summary_level]['policy'].__table__.primary_key.columns.values()],
                                          int_dtypedict['policy'], shard_id=summary_engine[summary_level]
                                         )
    # Summing up Smf72Workload
    agg_workload = {'r723mwde': 'last'}
    insert_dict['workload'] = sum_up_by_partition(tbls['workload'], summary_class[summary_level]['workload'],
                                                  summary_tblname[summary_level]['workload'],
                                                  start, end, current_time, agg_workload, int_dtypedict['workload'],
                                                  partitions_scheme, summary_engine[summary_level],
                                                  db_engines, '72', 'smf72', db_session, db_driver)
    # Summing up Smf72rgs
    agg_rgs1 = {'r723ggde': 'first', 'r723gisp': 'max', 'r723ggms': 'max',
                'has_memory_limit': 'max', 'r723ggpc': 'max', 'r723ggpv': 'max',
                'has_min_capacity': 'max', 'has_max_capacity': 'max', 'is_tenant': 'max',
                'r723ggmn': 'last', 'r723ggmx': 'last', 'r723ggml': 'last',
                'r723gglt': 'last', 'r723ggtf': 'last'}
    agg_rgs2 = {'r723ggde': 'first', 'r723gisp': 'max', 'r723ggms': 'max',
                'has_memory_limit': 'max', 'r723ggpc': 'max', 'r723ggpv': 'max',
                'has_min_capacity': 'max', 'has_max_capacity': 'max', 'is_tenant': 'max',
                'r723ggmn': 'last', 'r723ggmx': 'last', 'r723ggml': 'last',
                'r723ggti': 'last', 'r723ggtn': 'last', 'r723ggky': 'last',
                'r723gglt': 'last', 'r723ggtf': 'last'}
    insert_dict['rgs'] = sum_up_by_partition(tbls['rgs'], summary_class[summary_level]['rgs'],
                                             summary_tblname[summary_level]['rgs'],
                                             start, end, current_time, agg_rgs2, int_dtypedict['rgs'],
                                             partitions_scheme, summary_engine[summary_level],
                                             db_engines, '72', 'smf72', db_session, db_driver)

    # Summing up Smf72Wms
    wms_stmt = (select(Smf72Wms, Smf72Scs, Smf72Rts).outerjoin(Smf72Wms.smf72_scss).outerjoin(Smf72Wms.smf72_rtss)
                .where(Smf72Wms.datetime.between(start, end)))
    df_wms_list = []
    null_column_list = []
    for part in partitions_range:
        df_wms = pd.read_sql(wms_stmt, db_engines[f'72.{part}'])
        if not df_wms.empty:
            df_wms['date'] = df_wms['datetime'].dt.date
            df_wms_list.append(df_wms)
            null_columns = df_wms.columns[df_wms.isna().all()].tolist()
            for col in null_columns:
                if col not in null_column_list:
                    null_column_list.append(col)
    if len(df_wms_list) > 0:
        df_wmss = pd.concat([df.dropna(axis=1, how='all') for df in df_wms_list])
        if len(null_column_list) > 0:
            new_cols = df_wmss.columns.tolist()
            for col in null_column_list:
                if col not in new_cols:
                    new_cols.append(col)
            df_wmss = df_wmss.reindex(columns=new_cols)
        df_wms_sum1 = df_wmss.groupby(
            [col.name for col in
             summary_class[summary_level]['wms'].__table__.primary_key.columns.values()]).agg(agg_wms)
        df_wms_sum2 = agg_scs_group_by(df_wmss,
                                       [col.name for col in
                                        summary_class[summary_level]['wms'].__table__.primary_key.columns.values()],
                                       df_wms_sum1['smf72int'].values,
                                       not df_wmss['r723ctetx'].isna().all()
                                       )
        df_wms_sum3 = df_wmss.groupby([col.name for col in
                                       summary_class[summary_level]['wms'].__table__.primary_key.columns.values()]
                                      ).agg(agg_rts)
        df_wms_sum = pd.concat([df_wms_sum1, df_wms_sum2.drop(columns=['r723mtv_', 'smf72int']), df_wms_sum3], axis=1)
        df_wms_sum['performance_index'] = get_performance_index(df_wms_sum['class_goal_type'],
                                                                df_wms_sum['execution_velocity'],
                                                                df_wms_sum['r723cval'],
                                                                df_wms_sum['r723cpct'],
                                                                df_wms_sum['class_rt_bucket_1'],
                                                                df_wms_sum['class_rt_bucket_2'],
                                                                df_wms_sum['class_rt_bucket_3'],
                                                                df_wms_sum['class_rt_bucket_4'],
                                                                df_wms_sum['class_rt_bucket_5'],
                                                                df_wms_sum['class_rt_bucket_6'],
                                                                df_wms_sum['class_rt_bucket_7'],
                                                                df_wms_sum['class_rt_bucket_8'],
                                                                df_wms_sum['class_rt_bucket_9'],
                                                                df_wms_sum['class_rt_bucket_10'],
                                                                df_wms_sum['class_rt_bucket_11'],
                                                                df_wms_sum['class_rt_bucket_12'],
                                                                df_wms_sum['class_rt_bucket_13'],
                                                                df_wms_sum['class_rt_bucket_14'])
        df_wms_sum = df_wms_sum.copy().reset_index()
        if 'date' not in df_wms_sum.columns:
            df_wms_sum['date'] = df_wms_sum['datetime'].dt.date
        df_wms_sum['last_update_time'] = dt.datetime.now()
        insert_dict['wms'] = df_upsert(db_driver, db_engines[summary_engine[summary_level]], db_session,
                                       df_wms_sum[summary_class[summary_level]['wms'].__table__.columns.keys()],
                                       summary_tblname[summary_level]['wms'],
                                       summary_class[summary_level]['wms'], 'smf72',
                                       [col.name for col in
                                        summary_class[summary_level]['wms'].__table__.primary_key.columns.values()],
                                       int_dtypedict['wms'], shard_id=summary_engine[summary_level]
                                       )

    # Summing up Smf72Sss
    agg_sss = {'r723scs_': 'sum'}
    insert_dict['sss'] = sum_up_by_partition(tbls['sss'], summary_class[summary_level]['sss'],
                                             summary_tblname[summary_level]['sss'],
                                             start, end, current_time, agg_sss, int_dtypedict['sss'],
                                             partitions_scheme, summary_engine[summary_level],
                                             db_engines, '72', 'smf72', db_session, db_driver)
    # Summing up Smf72Scs
    df_scs_list = []
    null_column_list = []
    scs_stmt = select(Smf72Scs, Smf72Rts).outerjoin(Smf72Scs.smf72_rts).where(Smf72Scs.datetime.between(start, end))
    for part in partitions_range:
        df_scs = pd.read_sql(scs_stmt, db_engines[f'72.{part}'])
        if not df_scs.empty:
            df_scs['date'] = df_scs['datetime'].dt.date
            df_scs_list.append(df_scs)
            null_columns = df_scs.columns[df_scs.isna().all()].tolist()
            for col in null_columns:
                if col not in null_column_list:
                    null_column_list.append(col)
    if len(df_scs_list) > 0:
        df_scss = pd.concat([df.dropna(axis=1, how='all') for df in df_scs_list])
        if len(null_column_list) > 0:
            new_cols = df_scss.columns.tolist()
            for col in null_column_list:
                if col not in new_cols:
                    new_cols.append(col)
            df_scss = df_scss.reindex(columns=new_cols)
        df_scs_sum1 = agg_scs_group_by(df_scss,
                                       [col.name for col in
                                        summary_class[summary_level]['scs'].__table__.primary_key.columns.values()],
                                       'sum',
                                       not df_scss['r723ctetx'].isna().all()
                                       )
        df_scs_sum2 = df_scss.groupby([col.name for col in
                                       summary_class[summary_level]['scs'].__table__.primary_key.columns.values()]
                                      ).agg(agg_rts)
        df_scs_sum = pd.concat([df_scs_sum1, df_scs_sum2], axis=1)

        df_scs_sum['performance_index'] = get_performance_index(df_scs_sum['class_goal_type'],
                                                                df_scs_sum['execution_velocity'],
                                                                df_scs_sum['r723cval'],
                                                                df_scs_sum['r723cpct'],
                                                                df_scs_sum['class_rt_bucket_1'],
                                                                df_scs_sum['class_rt_bucket_2'],
                                                                df_scs_sum['class_rt_bucket_3'],
                                                                df_scs_sum['class_rt_bucket_4'],
                                                                df_scs_sum['class_rt_bucket_5'],
                                                                df_scs_sum['class_rt_bucket_6'],
                                                                df_scs_sum['class_rt_bucket_7'],
                                                                df_scs_sum['class_rt_bucket_8'],
                                                                df_scs_sum['class_rt_bucket_9'],
                                                                df_scs_sum['class_rt_bucket_10'],
                                                                df_scs_sum['class_rt_bucket_11'],
                                                                df_scs_sum['class_rt_bucket_12'],
                                                                df_scs_sum['class_rt_bucket_13'],
                                                                df_scs_sum['class_rt_bucket_14'])
        df_scs_sum = df_scs_sum.reset_index()
        if 'date' not in df_scs_sum.columns:
            df_scs_sum['date'] = df_scs_sum['datetime'].dt.date
        df_scs_sum['last_update_time'] = dt.datetime.now()

        insert_dict['scs'] = df_upsert(db_driver, db_engines[summary_engine[summary_level]], db_session,
                                       df_scs_sum[summary_class[summary_level]['scs'].__table__.columns.keys()],
                                       summary_tblname[summary_level]['scs'],
                                       summary_class[summary_level]['scs'], 'smf72',
                                       [col.name for col in
                                        summary_class[summary_level]['scs'].__table__.primary_key.columns.values()],
                                       int_dtypedict['scs'], shard_id=summary_engine[summary_level]
                                       )

    # Summing up Smf72Rts
    insert_dict['rts'] = sum_up_by_partition(tbls['rts'], summary_class[summary_level]['rts'],
                                             summary_tblname[summary_level]['rts'],
                                             start, end, current_time, agg_rts, int_dtypedict['rts'],
                                             partitions_scheme, summary_engine[summary_level],
                                             db_engines, '72', 'smf72', db_session, db_driver)
    # Summing up Smf72Wrs and Smf72Wrsx
    agg_wrsx = {'r723rexe': 'max', 'r723rdbe': 'max', 'r723ress': 'sum', 'r723ract': 'sum',
               'r723rrdy': 'sum', 'r723ridl': 'sum', 'r723rwlo': 'sum',
               'r723rwio': 'sum', 'r723rwco': 'sum', 'r723rwds': 'sum', 'r723rwsl': 'sum',
               'r723rwsn': 'sum', 'r723rwss': 'sum', 'r723rwtm': 'sum',
               'r723rwo': 'sum', 'r723rwms': 'sum', 'r723rssl': 'sum', 'r723rsss': 'sum',
               'r723rssn': 'sum', 'r723rwst': 'sum', 'r723rwrt': 'sum',
               'r723rwwr': 'sum', 'r723rapp': 'sum', 'r723rwnl': 'sum', 'r723rbpm': 'sum',
               'r723rw01': 'sum', 'r723rw02': 'sum', 'r723rw03': 'sum',
               'r723rw04': 'sum', 'r723rw05': 'sum', 'r723rw06': 'sum', 'r723rw07': 'sum',
               'r723rw08': 'sum', 'r723rw09': 'sum', 'r723rw10': 'sum',
               'r723rw11': 'sum', 'r723rw12': 'sum', 'r723rw13': 'sum', 'r723rw14': 'sum',
               'r723rw15': 'sum'}
    insert_dict['wrsx'] = sum_up_by_partition(tbls['wrsx'], summary_class[summary_level]['wrsx'],
                                              summary_tblname[summary_level]['wrsx'],
                                              start, end, current_time, agg_wrsx, int_dtypedict['wrsx'],
                                              partitions_scheme, summary_engine[summary_level],
                                              db_engines, '72', 'smf72', db_session, db_driver)
    insert_dict['wrs'] = sum_up_by_partition(tbls['wrs'], summary_class[summary_level]['wrs'],
                                             summary_tblname[summary_level]['wrs'],
                                             start, end, current_time, agg_wrsx, int_dtypedict['wrs'],
                                             partitions_scheme, summary_engine[summary_level],
                                             db_engines, '72', 'smf72', db_session, db_driver)

    # Summing up Smf72Dns and Smf72Dnsx
    agg_dnsx = {'r723rwnn': 'sum'}
    insert_dict['dnsx'] = sum_up_by_partition(tbls['dnsx'], summary_class[summary_level]['dnsx'],
                                              summary_tblname[summary_level]['dnsx'],
                                              start, end, current_time, agg_dnsx, int_dtypedict['dnsx'],
                                              partitions_scheme, summary_engine[summary_level],
                                              db_engines, '72', 'smf72', db_session, db_driver)
    insert_dict['dns'] = sum_up_by_partition(tbls['dns'], summary_class[summary_level]['dns'],
                                             summary_tblname[summary_level]['dns'],
                                             start, end, current_time, agg_dnsx, int_dtypedict['dns'],
                                             partitions_scheme, summary_engine[summary_level],
                                             db_engines, '72', 'smf72', db_session, db_driver)

    # Summing up Smf72Data
    agg_data = {'smf_type': 'first', 'csc': 'first', 'r724ptm': 'first', 'r724user': 'sum',
                'r724actv': 'sum', 'r724acts': 'sum', 'r724idls': 'sum', 'r724page': 'sum',
                'r724swap': 'sum', 'r724outr': 'sum', 'r724pgin': 'sum', 'r724divs': 'sum',
                'r724lssa': 'sum', 'r724pssa': 'sum', 'r724upro': 'sum',
                'r724udev': 'sum', 'r724dpro': 'sum', 'r724ddev': 'sum', 'r724dsto': 'sum',
                'r724djes': 'sum', 'r724dhsm': 'sum', 'r724dxcf': 'sum',
                'r724denq': 'sum', 'r724dmnt': 'sum', 'r724dmsg': 'sum', 'r724unkn': 'sum',
                'r724vald': 'sum', 'r724lsct': 'sum', 'r724esct': 'sum',
                'r724psct': 'sum', 'r724actf': 'sum', 'r724idle': 'sum', 'r724slot': 'sum',
                'r724div': 'sum', 'r724fix': 'sum', 'r724lscf': 'sum',
                'r724lsef': 'sum', 'r724psef': 'sum', 'r724vect': 'sum', 'r724et': 'sum',
                'r724etx': 'sum', 'r724qt': 'sum', 'r724qtx': 'sum',
                'r724end': 'sum', 'r724tsv': 'sum', 'r724vin': 'sum', 'r724vlc': 'sum',
                'r724gpi': 'sum', 'r724or1': 'sum', 'r724or2': 'sum',
                'r724or3': 'sum', 'r724or4': 'sum', 'r724or5': 'sum', 'r724or6': 'sum',
                'r724or7': 'sum', 'r724or8': 'sum', 'r724or9': 'sum',
                'r724or10': 'sum', 'r724or11': 'sum', 'r724or12': 'sum', 'r724or13': 'sum',
                'r724or14': 'sum', 'r724or15': 'sum', 'r724or16': 'sum',
                'r724or17': 'sum', 'r724or18': 'sum', 'r724or7a': 'sum'}
    insert_dict['data'] = sum_up_by_partition(tbls['data'], summary_class[summary_level]['data'],
                                              summary_tblname[summary_level]['data'],
                                              start, end, current_time, agg_data, int_dtypedict['data'],
                                              partitions_scheme, summary_engine[summary_level],
                                              db_engines, '72', 'smf72', db_session, db_driver)
    # Summing up Smf72Sctl
    agg_sctl = {'smf_type': 'first', 'csc': 'first', 'r725sgmo': 'first', 'r725scms': 'sum',
                'r725scma': 'sum', 'r725scmt': 'sum', 'r725seds': 'sum', 'r725seda': 'sum',
                'r725sedt': 'sum', 'r725slas': 'sum', 'r725slrs': 'sum', 'r725slaa': 'sum',
                'r725slat': 'sum', 'r725ssms': 'sum', 'r725ssma': 'sum',
                'r725ssmt': 'sum', 'r725slos': 'sum', 'r725sloa': 'sum', 'r725slot': 'sum',
                'r725scls': 'sum', 'r725scla': 'sum', 'r725sclt': 'sum',
                'r725slrt': 'sum', 'r725slrq': 'sum', 'r725sstr': 'sum', 'r725ssts': 'sum',
                'r725sstt': 'sum', 'r725sstq': 'sum', 'r725ssyr': 'sum',
                'r725ssys': 'sum', 'r725ssyt': 'sum', 'r725ssyq': 'sum', 'r725sssr': 'sum',
                'r725ssss': 'sum', 'r725ssst': 'sum', 'r725sssq': 'sum'}
    insert_dict['sctl'] = sum_up_by_partition(tbls['sctl'], summary_class[summary_level]['sctl'],
                                              summary_tblname[summary_level]['sctl'],
                                              start, end, current_time, agg_sctl, int_dtypedict['sctl'],
                                              partitions_scheme, summary_engine[summary_level],
                                              db_engines, '72', 'smf72', db_session, db_driver)
    # Summing up Smf72Cmss
    agg_cmss = {'csc': 'first', 'r725cmas': 'first', 'r725cmsu': 'sum', 'r725cmal': 'sum',
                'r725cmti': 'sum'}
    insert_dict['cmss'] = sum_up_by_partition(tbls['cmss'], summary_class[summary_level]['cmss'],
                                              summary_tblname[summary_level]['cmss'],
                                              start, end, current_time, agg_cmss, int_dtypedict['cmss'],
                                              partitions_scheme, summary_engine[summary_level],
                                              db_engines, '72', 'smf72', db_session, db_driver)
    # Summing up Smf72Ceds
    agg_ceds = {'csc': 'first', 'r725cmas': 'first', 'r725cmsu': 'sum', 'r725cmal': 'sum',
                'r725cmti': 'sum'}
    insert_dict['ceds'] = sum_up_by_partition(tbls['ceds'], summary_class[summary_level]['ceds'],
                                              summary_tblname[summary_level]['ceds'],
                                              start, end, current_time, agg_ceds, int_dtypedict['ceds'],
                                              partitions_scheme, summary_engine[summary_level],
                                              db_engines, '72', 'smf72', db_session, db_driver)
    # Summing up Smf72Clas
    agg_clas = {'csc': 'first', 'r725cmas': 'first', 'r725cmsu': 'sum', 'r725cmal': 'sum',
                'r725cmti': 'sum'}
    insert_dict['clas'] = sum_up_by_partition(tbls['clas'], summary_class[summary_level]['clas'],
                                              summary_tblname[summary_level]['clas'],
                                              start, end, current_time, agg_cmss, int_dtypedict['clas'],
                                              partitions_scheme, summary_engine[summary_level],
                                              db_engines, '72', 'smf72', db_session, db_driver)
    # Summing up Smf72Csms
    agg_csms = {'csc': 'first', 'r725cmas': 'first', 'r725cmsu': 'sum', 'r725cmal': 'sum',
                'r725cmti': 'sum'}
    insert_dict['csms'] = sum_up_by_partition(tbls['csms'], summary_class[summary_level]['csms'],
                                              summary_tblname[summary_level]['csms'],
                                              start, end, current_time, agg_csms, int_dtypedict['csms'],
                                              partitions_scheme, summary_engine[summary_level],
                                              db_engines, '72', 'smf72', db_session, db_driver)
    # Summing up Smf72Lotd
    agg_lotd = {'csc': 'first', 'r725loas': 'first', 'r725losu': 'sum', 'r725loal': 'sum',
                'r725loti': 'sum', 'r725lcsu': 'sum', 'r725lcal': 'sum',
                'r725lcti': 'sum'}
    insert_dict['lotd'] = sum_up_by_partition(tbls['lotd'], summary_class[summary_level]['lotd'],
                                              summary_tblname[summary_level]['lotd'],
                                              start, end, current_time, agg_lotd, int_dtypedict['lotd'],
                                              partitions_scheme, summary_engine[summary_level],
                                              db_engines, '72', 'smf72', db_session, db_driver)
    # Summing up Smf72Clod
    agg_clod = {'csc': 'first', 'r725coas': 'first', 'r725cosu': 'sum', 'r725coal': 'sum',
                'r725coti': 'sum', 'r725clsu': 'sum', 'r725clal': 'sum',
                'r725clti': 'sum'}
    insert_dict['clod'] = sum_up_by_partition(tbls['clod'], summary_class[summary_level]['clod'],
                                              summary_tblname[summary_level]['clod'],
                                              start, end, current_time, agg_clod, int_dtypedict['clod'],
                                              partitions_scheme, summary_engine[summary_level],
                                              db_engines, '72', 'smf72', db_session, db_driver)
    # Summing up Smf72Clrd
    agg_clrd = {'csc': 'first', 'r725cras': 'first', 'r725crsu': 'sum', 'r725cral': 'sum',
                'r725crti': 'sum'}
    insert_dict['clrd'] = sum_up_by_partition(tbls['clrd'], summary_class[summary_level]['clrd'],
                                              summary_tblname[summary_level]['clrd'],
                                              start, end, current_time, agg_clrd, int_dtypedict['clrd'],
                                              partitions_scheme, summary_engine[summary_level],
                                              db_engines, '72', 'smf72', db_session, db_driver)
    # Summing up Smf72Lasc
    agg_lasc = {'csc': 'first', 'r725laas': 'first', 'r725lasu': 'sum', 'r725lati': 'sum',
                'r725lasq': 'sum'}
    insert_dict['lasc'] = sum_up_by_partition(tbls['lasc'], summary_class[summary_level]['lasc'],
                                              summary_tblname[summary_level]['lasc'],
                                              start, end, current_time, agg_lasc, int_dtypedict['lasc'],
                                              partitions_scheme, summary_engine[summary_level],
                                              db_engines, '72', 'smf72', db_session, db_driver)
    # Summing up Smf72Lare
    agg_lare = {'csc': 'first', 'r725laas': 'first', 'r725lasu': 'sum', 'r725lati': 'sum',
                'r725lasq': 'sum'}
    insert_dict['lare'] = sum_up_by_partition(tbls['lare'], summary_class[summary_level]['lare'],
                                              summary_tblname[summary_level]['lare'],
                                              start, end, current_time, agg_lare, int_dtypedict['lare'],
                                              partitions_scheme, summary_engine[summary_level],
                                              db_engines, '72', 'smf72', db_session, db_driver)
    # Summing up Smf72Ense
    agg_ense = {'csc': 'first', 'r725enas': 'first', 'r725enrc': 'sum', 'r725ensu': 'sum',
                'r725enti': 'sum', 'r725ensq': 'sum'}
    insert_dict['ense'] = sum_up_by_partition(tbls['ense'], summary_class[summary_level]['ense'],
                                              summary_tblname[summary_level]['ense'],
                                              start, end, current_time, agg_ense, int_dtypedict['ense'],
                                              partitions_scheme, summary_engine[summary_level],
                                              db_engines, '72', 'smf72', db_session, db_driver)
    # Summing up Smf72Ensy
    agg_ensy = {'csc': 'first', 'r725enas': 'first', 'r725enrc': 'sum', 'r725ensu': 'sum',
                'r725enti': 'sum', 'r725ensq': 'sum'}
    insert_dict['ensy'] = sum_up_by_partition(tbls['ensy'], summary_class[summary_level]['ensy'],
                                              summary_tblname[summary_level]['ensy'],
                                              start, end, current_time, agg_ensy, int_dtypedict['ensy'],
                                              partitions_scheme, summary_engine[summary_level],
                                              db_engines, '72', 'smf72', db_session, db_driver)
    # Summing up Smf72Enss
    agg_enss = {'csc': 'first', 'r725enas': 'first', 'r725enrc': 'sum', 'r725ensu': 'sum',
                'r725enti': 'sum', 'r725ensq': 'sum'}
    insert_dict['enss'] = sum_up_by_partition(tbls['enss'], summary_class[summary_level]['enss'],
                                              summary_tblname[summary_level]['enss'],
                                              start, end, current_time, agg_enss, int_dtypedict['enss'],
                                              partitions_scheme, summary_engine[summary_level],
                                              db_engines, '72', 'smf72', db_session, db_driver)
    # Summing up Smf72Qsad
    agg_qsad = {'csc': 'first', 'r725qsas': 'first', 'r725qsrc': 'sum', 'r725qssc': 'sum',
                'r725qsrr': 'sum', 'r725qsrq': 'sum', 'r725qsti': 'sum',
                'r725qstq': 'sum'}
    insert_dict['qsad'] = sum_up_by_partition(tbls['qsad'], summary_class[summary_level]['qsad'],
                                              summary_tblname[summary_level]['qsad'],
                                              start, end, current_time, agg_qsad, int_dtypedict['qsad'],
                                              partitions_scheme, summary_engine[summary_level],
                                              db_engines, '72', 'smf72', db_session, db_driver)


    result_list.append({summary_tblname[summary_level][k]:v for k,v in insert_dict.items() if k in summary_tblname[summary_level].keys()})

    et = time.time()  # get the end time
    # get the execution time
    elapsed_time = (et - st) / 60
    print(f'Execution time ({summary_level}):', elapsed_time, 'minutes')

    overall_et = time.time()
    overall_elapsed_time = (overall_et - overall_st) / 60
    return UploadResult(result_list, overall_elapsed_time, SUCCESS)

