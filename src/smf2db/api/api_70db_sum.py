import datetime as dt
import time

import numpy as np
import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from smf2db import SUCCESS
from smf2db.api.util import (UploadResult, weighted_avg, agg_wait_completion_status, any_1, round_, agg_boost,
                             create_int_dtypedict, is_bit_set, df_upsert, sum_up_by_partition)
from smf2db.db_models.smf70_da_model import (Smf70ProDa, Smf70CtlDa, Smf70TrgDa, Smf70BctDa, Smf70AidDa,
                                             Smf70CpuDa, Smf70BpdDa, Smf70BctCpuDa, Smf70CcfDa, Smf70Typ3Da,
                                             Smf70Typ4Da, Smf70Typ5Da)
from smf2db.db_models.smf70_hr_model import (Smf70ProHr, Smf70CtlHr, Smf70TrgHr, Smf70BctHr, Smf70AidHr,
                                             Smf70CpuHr, Smf70BpdHr, Smf70BctCpuHr, Smf70CcfHr, Smf70Typ3Hr,
                                             Smf70Typ4Hr, Smf70Typ5Hr)
from smf2db.db_models.smf70_model import (Smf70Pro, Smf70Ctl, Smf70Aid,
                                          Smf70Cpu, Smf70Bct, Smf70BctCpu, Smf70Bpd,
                                          Smf70Trg, Smf70Ccf, Smf70Typ3, Smf70Typ4, Smf70Typ5, )

smf70typ_cpu_type = {0: 'CP', 1: 'IFA', 2: 'IIP'}

tbls = {'pro': Smf70Pro,
        'ctl': Smf70Ctl,
        'cpu': Smf70Cpu,
        'bct': Smf70Bct,
        'bpd': Smf70Bpd,
        'bct_cpu': Smf70BctCpu,
        'aid': Smf70Aid,
        'trg': Smf70Trg,
        'typ3': Smf70Typ3,
        'typ4': Smf70Typ4,
        'typ5': Smf70Typ5,
        'ccf': Smf70Ccf}
tbls_hr = {'pro': Smf70ProHr,
           'ctl': Smf70CtlHr,
           'cpu': Smf70CpuHr,
           'bct': Smf70BctHr,
           'bpd': Smf70BpdHr,
           'bct_cpu': Smf70BctCpuHr,
           'aid': Smf70AidHr,
           'trg': Smf70TrgHr,
           'typ3': Smf70Typ3Hr,
           'typ4': Smf70Typ4Hr,
           'typ5': Smf70Typ5Hr,
           'ccf': Smf70CcfHr}
tbls_da = {'pro': Smf70ProDa,
           'ctl': Smf70CtlDa,
           'cpu': Smf70CpuDa,
           'bct': Smf70BctDa,
           'bpd': Smf70BpdDa,
           'bct_cpu': Smf70BctCpuDa,
           'aid': Smf70AidDa,
           'trg': Smf70TrgDa,
           'typ3': Smf70Typ3Da,
           'typ4': Smf70Typ4Da,
           'typ5': Smf70Typ5Da,
           'ccf': Smf70CcfDa}
tblnames_hr = {'pro': 'smf70_pro_hr',
               'ctl': 'smf70_ctl_hr',
               'cpu': 'smf70_cpu_hr',
               'bct': 'smf70_bct_hr',
               'bpd': 'smf70_bpd_hr',
               'bct_cpu': 'smf70_bct_cpu_hr',
               'aid': 'smf70_aid_hr',
               'trg': 'smf70_trg_hr',
               'typ3': 'smf70_typ3_hr',
               'typ4': 'smf70_typ4_hr',
               'typ5': 'smf70_typ5_hr',
               'ccf': 'smf70_ccf_hr'}
tblnames_da = {'pro': 'smf70_pro_da',
               'ctl': 'smf70_ctl_da',
               'cpu': 'smf70_cpu_da',
               'bct': 'smf70_bct_da',
               'bpd': 'smf70_bpd_da',
               'bct_cpu': 'smf70_bct_cpu_da',
               'aid': 'smf70_aid_da',
               'trg': 'smf70_trg_da',
               'typ3': 'smf70_typ3_da',
               'typ4': 'smf70_typ4_da',
               'typ5': 'smf70_typ5_da',
               'ccf': 'smf70_ccf_da'}
tblnames = {'pro': 'smf70_pro',
            'ctl': 'smf70_ctl',
            'cpu': 'smf70_cpu',
            'bct': 'smf70_bct',
            'bpd': 'smf70_bpd',
            'bct_cpu': 'smf70_bct_cpu',
            'aid': 'smf70_aid',
            'trg': 'smf70_trg',
            'typ3': 'smf70_typ3',
            'typ4': 'smf70_typ4',
            'typ5': 'smf70_typ5',
            'ccf': 'smf70_ccf'}

int_dtypedict = create_int_dtypedict(tbls)


def agg_next(series):
    return next((item for item in series if item is not None), None)


agg_dict = {
    'cpu': {'smf70_core_id': 'first', 'sub_core_idx': 'first', 'smf70_cpu_num': 'first',
            'smf70typ': 'first', 'smf70ser': 'first', 'smf70bps': 'first', 'cpu_polarization': 'last',
            'smf70int': 'sum', 'smf70_lpar_busy': 'sum', 'smf70wat': 'sum', 'time_range': 'sum',
            'cpu_time': 'sum', 'smf70slh': 'sum', 'smf70tpi': 'sum', 'smf70vfs': 'sum',
            'smf70pat': 'sum', 'cpu_unparked_time': 'sum', 'cpu_busy_time': 'sum',
            'smf70tcb': 'sum', 'smf70srb': 'sum', 'smf70nio': 'sum', 'smf70sig': 'sum',
            'smf70wtd': 'sum', 'smf70wts': 'sum', 'smf70wtu': 'sum', 'smf70wti': 'sum',
            'smf70pdt': 'sum', 'smf70edt': 'sum', 'smf70ont': 'sum', 'smf70wst': 'sum',
            'smf70mtit': 'sum',
            'rate_io_interrupt': 'mean', 'rate_tcb': 'mean', 'rate_srb': 'mean', 'rate_io': 'mean',
            'smf70_prod': 'mean', 'mt_util': 'mean', 'cpu_is_online': 'max',  # 'data_invalid': 'max',
            'wait_completion_status': 'max',
            'smf70v': 'last', 'smf70_core_flg': 'last', 'smf70vpf': 'last', 'smf70pof': 'last',
            'smf70cnf': 'last', 'lpb_valid': 'last', },
    'aid': {'smf70rmn': 'min', 'smf70rmm': 'max', 'smf70rtt': 'sum', 'smf70r00': 'sum',
            'smf70r01': 'sum', 'smf70r02': 'sum', 'smf70r03': 'sum', 'smf70r04': 'sum',
            'smf70r05': 'sum', 'smf70r06': 'sum', 'smf70r07': 'sum', 'smf70r08': 'sum',
            'smf70r09': 'sum', 'smf70r10': 'sum', 'smf70r11': 'sum', 'smf70r12': 'sum',
            'smf70r13': 'sum', 'smf70r14': 'sum', 'smf70r15': 'sum', 'smf70imn': 'min',
            'smf70imm': 'max', 'smf70itt': 'sum', 'smf70i00': 'sum', 'smf70i01': 'sum',
            'smf70i02': 'sum', 'smf70i03': 'sum', 'smf70i04': 'sum', 'smf70i05': 'sum',
            'smf70i06': 'sum', 'smf70i07': 'sum', 'smf70i08': 'sum', 'smf70i09': 'sum',
            'smf70i10': 'sum', 'smf70i11': 'sum', 'smf70omn': 'min', 'smf70omm': 'max',
            'smf70ott': 'sum', 'smf70o00': 'sum', 'smf70o01': 'sum', 'smf70o02': 'sum',
            'smf70o03': 'sum', 'smf70o04': 'sum', 'smf70o05': 'sum', 'smf70o06': 'sum',
            'smf70o07': 'sum', 'smf70o08': 'sum', 'smf70o09': 'sum', 'smf70o10': 'sum',
            'smf70o11': 'sum', 'smf70wmn': 'min', 'smf70wmm': 'max', 'smf70wtt': 'sum',
            'smf70w00': 'sum', 'smf70w01': 'sum', 'smf70w02': 'sum', 'smf70w03': 'sum',
            'smf70w04': 'sum', 'smf70w05': 'sum', 'smf70w06': 'sum', 'smf70w07': 'sum',
            'smf70w08': 'sum', 'smf70w09': 'sum', 'smf70w10': 'sum', 'smf70w11': 'sum',
            'smf70bmn': 'min', 'smf70bmm': 'max', 'smf70btt': 'sum', 'smf70b00': 'sum',
            'smf70b01': 'sum', 'smf70b02': 'sum', 'smf70b03': 'sum', 'smf70b04': 'sum',
            'smf70b05': 'sum', 'smf70b06': 'sum', 'smf70b07': 'sum', 'smf70b08': 'sum',
            'smf70b09': 'sum', 'smf70b10': 'sum', 'smf70b11': 'sum', 'smf70smn': 'min',
            'smf70smm': 'max', 'smf70stt': 'sum', 'smf70s00': 'sum', 'smf70s01': 'sum',
            'smf70s02': 'sum', 'smf70s03': 'sum', 'smf70s04': 'sum', 'smf70s05': 'sum',
            'smf70s06': 'sum', 'smf70s07': 'sum', 'smf70s08': 'sum', 'smf70s09': 'sum',
            'smf70s10': 'sum', 'smf70s11': 'sum', 'smf70tmn': 'min', 'smf70tmm': 'max',
            'smf70ttt': 'sum', 'smf70t00': 'sum', 'smf70t01': 'sum', 'smf70t02': 'sum',
            'smf70t03': 'sum', 'smf70t04': 'sum', 'smf70t05': 'sum', 'smf70t06': 'sum',
            'smf70t07': 'sum', 'smf70t08': 'sum', 'smf70t09': 'sum', 'smf70t10': 'sum',
            'smf70t11': 'sum', 'smf70lmn': 'min', 'smf70lmm': 'max', 'smf70ltt': 'sum',
            'smf70l00': 'sum', 'smf70l01': 'sum', 'smf70l02': 'sum', 'smf70l03': 'sum',
            'smf70l04': 'sum', 'smf70l05': 'sum', 'smf70l06': 'sum', 'smf70l07': 'sum',
            'smf70l08': 'sum', 'smf70l09': 'sum', 'smf70l10': 'sum', 'smf70l11': 'sum',
            'smf70amn': 'min', 'smf70amm': 'max', 'smf70att': 'sum', 'smf70a00': 'sum',
            'smf70a01': 'sum', 'smf70a02': 'sum', 'smf70a03': 'sum', 'smf70a04': 'sum',
            'smf70a05': 'sum', 'smf70a06': 'sum', 'smf70a07': 'sum', 'smf70a08': 'sum',
            'smf70a09': 'sum', 'smf70a10': 'sum', 'smf70a11': 'sum', 'smf70pmn': 'min',
            'smf70pmm': 'max', 'smf70ptt': 'sum', 'smf70p00': 'sum', 'smf70p01': 'sum',
            'smf70p02': 'sum', 'smf70p03': 'sum', 'smf70p04': 'sum', 'smf70p05': 'sum',
            'smf70p06': 'sum', 'smf70p07': 'sum', 'smf70p08': 'sum', 'smf70p09': 'sum',
            'smf70p10': 'sum', 'smf70p11': 'sum', 'smf70xmn': 'min', 'smf70xmm': 'max',
            'smf70xtt': 'sum', 'smf70x00': 'sum', 'smf70x01': 'sum', 'smf70x02': 'sum',
            'smf70x03': 'sum', 'smf70x04': 'sum', 'smf70x05': 'sum', 'smf70x06': 'sum',
            'smf70x07': 'sum', 'smf70x08': 'sum', 'smf70x09': 'sum', 'smf70x10': 'sum',
            'smf70x11': 'sum', 'smf70q00': 'sum', 'smf70q01': 'sum', 'smf70q02': 'sum',
            'smf70q03': 'sum', 'smf70q04': 'sum', 'smf70q05': 'sum', 'smf70q06': 'sum',
            'smf70q07': 'sum', 'smf70q08': 'sum', 'smf70q09': 'sum', 'smf70q10': 'sum',
            'smf70q11': 'sum', 'smf70q12': 'sum', 'smf70srm': 'sum', 'smf70cmn': 'min',
            'smf70cmm': 'max', 'smf70ctt': 'sum', 'smf70dmn': 'min', 'smf70dmm': 'max',
            'smf70dtt': 'sum', 'smf70emn': 'min', 'smf70emm': 'max', 'smf70ett': 'sum',
            'smf70u00': 'sum', 'smf70u01': 'sum', 'smf70u02': 'sum', 'smf70u03': 'sum',
            'smf70u04': 'sum', 'smf70u05': 'sum', 'smf70u06': 'sum', 'smf70u07': 'sum',
            'smf70u08': 'sum', 'smf70u09': 'sum', 'smf70u10': 'sum', 'smf70u11': 'sum',
            'smf70u12': 'sum', 'smf70u13': 'sum', 'smf70u14': 'sum', 'smf70u15': 'sum'},
    'bpd': {'sysplex_name': 'first', 'system_name': 'first', 'smf70cix': 'first',
            'cpu_count': 'first', 'physical_cpu_count': 'first',
            'msu_physical': 'sum', 'smf70bps': 'last', 'processor_weight_online': 'sum',
            'msu_effective': 'sum', 'smf70acs': 'mean', 'share_current': 'last',
            'logical_processor_is_online': 'last',
            'utilization_per_cpu_physical': 'mean', 'lpar_management_per_cpu': 'mean',
            'smf70mis': 'min', 'smf70mas': 'max', 'smf70nsi': 'sum', 'smf70nsa': 'sum',
            'smf70ont': 'sum', 'smf70edt': 'sum', 'smf70pdt': 'sum', 'smf70wst': 'sum',
            'smf70pma': 'last', 'smf70nsw': 'last', 'smf70pow': 'last', 'smf70nca': 'last',
            'smf70mtit': 'sum', 'smf70hw_cap_limit': 'last', 'smf70hwgr_cap_limit': 'last',
            'smf70vpf': 'last', 'smf70pof': 'last', 'smf70lpf': 'last',
            'smf70maxnl': 'last', 'smf70cordl1': 'last', 'smf70cordl2': 'last', 'smf70cordl3': 'last',
            'smf70cordl4': 'last', 'smf70cordl5': 'last', 'smf70cordl6': 'last', 'smf70lpm': 'last',
            'smf70stn': 'last', 'smf70lpn': 'last'},
    'bct_cpu': {'cpu_count': 'first', 'physical_cpu_count': 'first',
                'wait_completion_status': agg_wait_completion_status,
                'wgt': 'last', 'initial_cap_indicator': any_1, 'cap_absolute_indicator': any_1,
                'cap_absolute_group_indicator': any_1, 'msu_physical': 'mean', 'smf70bps': 'max',
                'processor_weight_online': 'max', 'msu_effective': 'mean', 'smf70acs': 'mean',
                'share_current': 'mean', 'logical_processor_is_online': 'sum',
                'utilization_per_cpu_physical': 'mean', 'lpar_management_per_cpu': 'mean',
                'smf70mis': 'min', 'smf70mas': 'max', 'smf70nsi': 'mean', 'smf70nsa': 'mean',
                'smf70ont': 'sum', 'smf70edt': 'sum', 'smf70pdt': 'sum', 'smf70wst': 'sum',
                'smf70pma': 'first', 'smf70nsw': 'first', 'smf70pow': 'first', 'smf70nca': 'first',
                'smf70mtit': 'sum', 'smf70hw_cap_limit': 'first', 'smf70hwgr_cap_limit': 'first',
                'physical_processor_effective': 'mean', 'physical_processor_total': 'mean',
                'actual_consumed_msu': 'mean', 'effective_consumed_msu': 'mean',
                'logical_processor_effective': 'mean', 'logical_processor_total': 'mean',
                'smf70vpf': 'last', 'smf70pof': 'last', 'smf70lpf': 'last',
                'smf70maxnl': 'last', 'smf70cordl1': 'last', 'smf70cordl2': 'last',
                'smf70cordl3': 'last', 'smf70cordl4': 'last', 'smf70cordl5': 'last',
                'smf70cordl6': 'last', 'smf70lpm': 'last', 'smf70stn': 'last', 'smf70lpn': 'last'},
    'ccf': {'smf70ptn': 'first', 'r702snec': 'sum', 'r702sneb': 'sum', 'r702snei': 'sum',
            'r702tnec': 'sum', 'r702tneb': 'sum', 'r702tnei': 'sum',
            'r702sndc': 'sum', 'r702sndb': 'sum', 'r702sndi': 'sum', 'r702tndc': 'sum',
            'r702tndb': 'sum', 'r702tndi': 'sum', 'r702nmgc': 'sum',
            'r702nmgb': 'sum', 'r702nmgi': 'sum', 'r702nmvc': 'sum', 'r702nmvb': 'sum',
            'r702nmvi': 'sum', 'r702nhac': 'sum', 'r702nhab': 'sum',
            'r702nhai': 'sum', 'r702nptc': 'sum', 'r702npvc': 'sum', 'r702nh2c': 'sum',
            'r702nh2b': 'sum', 'r702nh2i': 'sum', 'r702nh5c': 'sum',
            'r702nh5b': 'sum', 'r702nh5i': 'sum', 'r702cdlv': 'first', 'r702aesc': 'sum',
            'r702aesb': 'sum', 'r702aesi': 'sum', 'r702asdc': 'sum',
            'r702asdb': 'sum', 'r702asdi': 'sum', 'r702drgc': 'sum', 'r702drvc': 'sum',
            'r702degc': 'sum', 'r702devc': 'sum', 'r702amgc': 'sum',
            'r702amgb': 'sum', 'r702amgi': 'sum', 'r702amvc': 'sum', 'r702amvb': 'sum',
            'r702amvi': 'sum', 'r702fpec': 'sum', 'r702fpeb': 'sum',
            'r702fpei': 'sum', 'r702fpdc': 'sum', 'r702fpdb': 'sum', 'r702fpdi': 'sum',
            'r702fptc': 'sum', 'r702fptb': 'sum', 'r702fpti': 'sum',
            'r702fxec': 'sum', 'r702fxeb': 'sum', 'r702fxei': 'sum', 'r702fxdc': 'sum',
            'r702fxdb': 'sum', 'r702fxdi': 'sum', 'r702fxtc': 'sum',
            'r702fxtb': 'sum', 'r702fxti': 'sum', 'r702dqgc': 'sum', 'r702dqvc': 'sum',
            'smf_type': 'first'},
    'typ3': {'smf_type': 'first', 'smf70ptn': 'first', 'r7023ct': 'first', 'r7023msk': 'first',
             'r7023sf': 'mean', 'r7023t0': 'mean', 'r7023c0': 'mean', 'r7023mt': 'first',
             'r7023c1': 'mean', 'smf70int': 'mean', 'r7023did': 'first'},
    'typ4': {'smf_type': 'first', 'smf70ptn': 'first', 'r7024ct': 'first', 'r7024msk': 'first',
             'r7024en': 'first', 'r7024sf': 'mean', 'r7021met_1': 'mean', 'r7021mec_1': 'mean',
             'r7022met_1': 'mean', 'r7022mec_1': 'mean', 'r7021crt_1': 'mean', 'r7021crc_1': 'mean',
             'r7022crt_1': 'mean', 'r7022crc_1': 'mean',
             'r7021met_2': 'mean', 'r7021mec_2': 'mean', 'r7022met_2': 'mean', 'r7022mec_2': 'mean',
             'r7021crt_2': 'mean', 'r7021crc_2': 'mean',
             'r7022crt_2': 'mean', 'r7022crc_2': 'mean', 'r7021met_3': 'mean', 'r7021mec_3': 'mean',
             'r7022met_3': 'mean', 'r7022mec_3': 'mean',
             'r7021crt_3': 'mean', 'r7021crc_3': 'mean', 'r7022crt_3': 'mean', 'r7022crc_3': 'mean',
             'r7021met_4': 'mean', 'r7021mec_4': 'mean',
             'r7022met_4': 'mean', 'r7022mec_4': 'mean', 'r7021crt_4': 'mean', 'r7021crc_4': 'mean',
             'r7022crt_4': 'mean', 'r7022crc_4': 'mean',
             'r7021met_5': 'mean', 'r7021mec_5': 'mean', 'r7022met_5': 'mean', 'r7022mec_5': 'mean',
             'r7021crt_5': 'mean', 'r7021crc_5': 'mean',
             'r7022crt_5': 'mean', 'r7022crc_5': 'mean', 'r7023met': 'mean', 'r7023mec': 'mean',
             'r7023crt': 'mean', 'r7023crc': 'mean', 'smf70int': 'mean',
             'r7024did': 'first', 'r7024mt': 'first'},
    'typ5': {'smf_type': 'first', 'smf70ptn': 'first', 'r7025ct': 'first', 'r7025msk': 'first',
             'r7025sf': 'mean', 'r7025sat': 'mean', 'r7025sac': 'mean',
             'r7025fat': 'mean', 'r7025fac': 'mean', 'r7025spt': 'mean', 'r7025spc': 'mean',
             'r7025sct': 'mean', 'r7025scc': 'mean', 'r7025agt': 'mean',
             'r7025agc': 'mean', 'smf70int': 'mean', 'r7025did': 'first',
             'r7025mt': 'first'},
    'bct': {'smf70csf': 'last', 'smf70esf': 'last', 'smf70int': 'sum',
            'smf70lpm': 'last', 'smf70bdn': 'last', 'sysplex_name': 'last', 'system_name': 'last',
            'smf70msu': 'last', 'smf70upi': 'last', 'smf70mtid': 'last', 'smf70spn': 'last',
            'smf70gnm': 'last', 'smf70gmu': 'last', 'smf70hwgr_name': 'last', 'smf70cpa_actual': 'last',
            'smf70cpa_scaling_factor': agg_next, 'wgt_cp': 'last', 'wgt_ifl': 'last', 'wgt_iip': 'last',
            'wgt_icf': 'last', 'wgt_ifa': 'last', 'wgt_cbp': 'last', 'total_weight_cp': 'last',
            'total_weight_ifl': 'last', 'total_weight_iip': 'last', 'total_weight_icf': 'last',
            'total_weight_aap': 'last', 'smf70edt_total_cp': 'sum', 'smf70edt_total_ifl': 'sum',
            'smf70edt_total_iip': 'sum', 'smf70edt_total_icf': 'sum', 'smf70edt_total_aap': 'sum',
            'smf70pdt_cp': 'sum', 'smf70pdt_ifl': 'sum', 'smf70pdt_iip': 'sum', 'smf70pdt_icf': 'sum',
            'smf70pdt_aap': 'sum', 'lpar_management_total_cp': 'mean',
            'lpar_management_total_ifl': 'mean', 'lpar_management_total_iip': 'mean',
            'lpar_management_total_icf': 'mean', 'lpar_management_total_aap': 'mean',
            'physical_processor_effective_total_cp': 'mean',
            'physical_processor_effective_total_ifl': 'mean',
            'physical_processor_effective_total_iip': 'mean',
            'physical_processor_effective_total_icf': 'mean',
            'physical_processor_effective_total_aap': 'mean',
            'physical_processor_total_total_cp': 'mean',
            'physical_processor_total_total_ifl': 'mean',
            'physical_processor_total_total_iip': 'mean',
            'physical_processor_total_total_icf': 'mean',
            'physical_processor_total_total_aap': 'mean',
            'defined_cpu_count_cp': 'last', 'defined_cpu_count_iip': 'last',
            'defined_cpu_count_icf': 'last',
            'smf70acs_cp': 'last', 'total_smf70acs_cp': 'last', 'min_entitlement': 'last',
            'max_entitlement': 'last',
            'smf70lpn': 'last', 'smf70pfg': 'last', 'smf70bds': 'last', 'smf70stn': 'last',
            'smf70pfl': 'last', 'smf70_boostinfo': 'last', 'smf70xnm': 'last',
            'smf70bda': 'last'},
    'ctl': {'smf_type': 'first', 'smf70int': 'sum', 'lpar_system_name': 'last', 'smf70lpm': 'last',
            'smf70ptn': 'last', 'smf70xnm': 'last', 'smf70snm': 'last',
            'smf70gjt': 'last', 'smf70inb': 'last', 'smf70stf': 'last', 'smf70csc': 'last',
            'smf70hhf': 'last', 'lpar_number': 'first',
            'smf70mdl_cbp': 'last', 'smf70mcr_cbp': 'last', 'smf70ncr_cbp': 'last',
            'smf70lac_cbp': 'mean', 'smf70cpa_actual_cbp': 'last', 'smf70_ipl_time': 'last',
            'smf70mdl_var': 'last', 'smf70mvcr': 'last', 'smf70nvcr': 'last',
            'smf70zsu_on_ziip': 'sum', 'smf70zsu_on_cp': 'sum', 'smf70jsu_on_ziip': 'sum',
            'smf70jsu_on_cp': 'sum', 'smf70cpe_lo': 'last', 'smf70cpe_hi': 'last',
            'smf70mdl_rep': 'last', 'smf70mrcr': 'last', 'smf70nrcr': 'last',
            'smf70_cpupower': 'sum', 'smf70_storagepower': 'sum', 'smf70_iopower': 'sum',
            'smf70_cpctotalpower': 'sum', 'smf70_cpcunassrespower': 'sum',
            'smf70_cpcinfrapower': 'sum', 'smf70_numpowersamples': 'sum',
            'smf70_powerpartitionname': 'last',
            'smf70mod': 'last', 'smf70ver': 'last', 'smf70bnp': 'last',
            'smf70gts': 'sum', 'smf70mdl': 'last', 'smf70dsa': 'mean', 'smf70ifa': 'last',
            'smf70cpa': 'last', 'cpu_adjustment_factor_effective': 'last', 'smf70wla': 'last',
            'smf70lac': 'mean', 'smf70hof': 'last', 'smf70hwm': 'last', 'smf70sup': 'last',
            'smf70pom': 'last', 'smf70pmi': 'sum', 'smf70pmu': 'sum', 'smf70pmw': 'sum',
            'smf70pmp': 'max', 'smf70pmt': 'last', 'smf70pml': 'last', 'smf70mpc': 'last',
            'smf70mtc': 'last', 'smf70mcr': 'last', 'smf70mpr': 'last', 'smf70mtr': 'last',
            'smf70nrm': 'last', 'smf70gau': 'last', 'smf70ncr': 'last', 'smf70npr': 'last',
            'smf70ntr': 'last', 'smf70cai': 'max', 'smf70ccr': 'max', 'smf70mcp': 'max',
            'smf70icp': 'max', 'smf70ccp': 'max', 'smf70cpc_type': 'last', 'smf70cpa_actual': 'last',
            'smf70cpa_scaling_factor': 'last', 'cpa_scaling_factor_effective': 'last',
            'multithreading': 'last', 'smf70lacm': 'mean', 'smf70laca': 'mean', 'smf70lacb': 'mean',
            'smf70adj': 'last', 'smf70laccr': 'mean', 'smf70maxpu': 'last', 'smf70os_prtct': 'last',
            'smf70_trg_m_cnt': 'sum', 'cpu_count_CP': 'last',
            'cpu_count_accumulated_CP': 'last', 'cpu_count_IFL': 'last',
            'cpu_count_accumulated_IFL': 'last', 'cpu_count_ICF': 'last',
            'cpu_count_accumulated_ICF': 'last', 'cpu_count_IIP': 'last',
            'cpu_count_accumulated_IIP': 'last', 'cpu_count_CBP': 'last',
            'cpu_count_accumulated_CBP': 'last', 'cpu_count_IFA': 'last',
            'cpu_count_accumulated_IFA': 'last', 'wgt_cp': 'last',
            'wgt_ifl': 'last', 'wgt_icf': 'last', 'wgt_iip': 'last', 'wgt_cbp': 'last',
            'wgt_ifa': 'last', 'total_weight_cp': 'last', 'total_weight_ifl': 'last',
            'total_weight_iip': 'last', 'total_weight_icf': 'last', 'total_weight_aap': 'last',
            'smf70mtid': 'last', 'rate_io_interrupt_total': 'mean',
            'med_log_proc_share_cp': 'last', 'med_log_proc_share_iip': 'last',
            'med_log_proc_share_aap': 'last',
            'total_log_proc_share_cp': 'last', 'total_log_proc_share_iip': 'last',
            'total_log_proc_share_aap': 'last',
            'smf70edt_total_cp': 'sum', 'smf70edt_total_ifl': 'sum', 'smf70edt_total_iip': 'sum',
            'smf70edt_total_icf': 'sum', 'smf70edt_total_aap': 'sum', 'smf70pdt_cp': 'sum',
            'smf70pdt_ifl': 'sum', 'smf70pdt_iip': 'sum', 'smf70pdt_icf': 'sum', 'smf70pdt_aap': 'sum',
            'lpar_management_total_cp': 'mean', 'lpar_management_total_ifl': 'mean',
            'lpar_management_total_iip': 'mean',
            'lpar_management_total_icf': 'mean', 'lpar_management_total_aap': 'mean',
            'physical_processor_effective_total_cp': 'mean',
            'physical_processor_effective_total_ifl': 'mean',
            'physical_processor_effective_total_iip': 'mean',
            'physical_processor_effective_total_icf': 'mean',
            'physical_processor_effective_total_aap': 'mean',
            'physical_processor_total_total_cp': 'mean',
            'physical_processor_total_total_ifl': 'mean',
            'physical_processor_total_total_iip': 'mean',
            'physical_processor_total_total_icf': 'mean',
            'physical_processor_total_total_aap': 'mean'},
    'pro': {'smf70flg': 'first',
            'smf70gie': 'last', 'smf70mfv': 'last',
            'smf70sam': 'sum', 'smf70cyc': 'last', 'smf70mvs': 'last',
            'smf70iml': 'last', 'smf70ptn': 'last', 'smf70srl': 'last', 'smf70lgo': 'last',
            'smf70oil': 'last', 'smf70syn': 'last', 'smf70xnm': 'last', 'smf70snm': 'last',
            'speed_boost': agg_boost, 'ziip_boost': agg_boost,
            'smf70prd': 'last', 'smf70int': 'sum', 'smf70fla': 'last', 'smf70prf': 'last'},
    'trg': {'smf70_trg_tntname': 'first', 'smf70_trg_dsc': 'first', 'smf70_trg_sbid': 'first',
            'smf70_trg_sucp': 'sum', 'smf70_trg_suifa': 'sum',
            'smf70_trg_susup': 'sum', 'smf70_trg_lac': 'mean', 'smf70_trg_mem': 'sum'}
}


def sum_70db(db_engines: dict, db_session: Session, summary_level: str, start_time_str: str, end_time_str: str,
             partitions_scheme: str, db_driver: str = 'postgresql+psycopg2') -> UploadResult:
    """Summarize smf70 database.

    Args:
        db_engines: A dictionary of all the db_engines in the database.
        db_session: SQLAlchemy session.
        summary_level: Summary level of data (hourly, daily).
        start_time_str: Start time of summary.
        end_time_str: End time of summary.
        partitions_scheme: Partitions scheme.
        db_driver: 'psycopg2' or 'sqlite'.

    Returns:
        A NamedTuple including the insert dictionary, total elapsed time of the summarization and the return code.
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

    insert_dict = {'pro': 0, 'ctl': 0, 'cpu': 0, 'aid': 0, 'bct': 0, 'bct_cpu': 0, 'bpd': 0, 'trg': 0,
                   'ccf': 0, 'typ3': 0, 'typ4': 0, 'typ5': 0, 'wc': 0}
    summary_class = {'hourly': tbls_hr, 'daily': tbls_da}
    summary_tblname = {'hourly': tblnames_hr, 'daily': tblnames_da}
    summary_engine = {'hourly': '70.hourly', 'daily': '70.daily'}

    result_list = []

    st = time.time()
    current_time = dt.datetime.now()

    round2int = np.vectorize(round_)

    # Summing up Smf70Pro
    df_pro_list = []
    pro_stmt = select(Smf70Pro).where(Smf70Pro.datetime.between(start, end))
    for part in partitions_range:
        df_pro = pd.read_sql(pro_stmt, db_engines[f'70.{part}'])
        if not df_pro.empty:
            df_pro['date'] = df_pro['datetime'].dt.date
            df_pro_list.append(df_pro)
    if len(df_pro_list) > 0:
        df_pros = pd.concat(df_pro_list)
        df_pros['speed_boost'] = df_pros['smf70fla'].apply(lambda x: is_bit_set(x, 16, 10) if pd.notna(x) else np.nan)
        df_pros['ziip_boost'] = df_pros['smf70fla'].apply(lambda x: is_bit_set(x, 16, 9) if pd.notna(x) else np.nan)
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
                                       'smf70',
                                       [col.name for col in
                                        summary_class[summary_level]['pro'].__table__.primary_key.columns.values()],
                                       int_dtypedict['pro'], shard_id=summary_engine[summary_level]
                                       )

        # Summing up Smf70Ctl
        df_ctl_list = []
        null_column_list = []
        ctl_stmt = select(Smf70Ctl).where(Smf70Ctl.datetime.between(start, end))
        ctl_stmt1b = select(Smf70Cpu).where(Smf70Cpu.datetime.between(start, end))
        for part in partitions_range:
            df_ctl = pd.read_sql(ctl_stmt, db_engines[f'70.{part}'])
            if not df_ctl.empty:
                df_ctl['date'] = df_ctl['datetime'].dt.date
                df_ctl_list.append(df_ctl)
                null_columns = df_ctl.columns[df_ctl.isna().all()].tolist()
                for col in null_columns:
                    if col not in null_column_list:
                        null_column_list.append(col)
        if len(df_ctl_list) > 0:
            df_ctls = pd.concat([df.dropna(axis=1, how='all') for df in df_ctl_list])
            if len(null_column_list) > 0:
                new_cols = df_ctls.columns.tolist()
                for col in null_column_list:
                    if col not in new_cols:
                        new_cols.append(col)
                df_ctls = df_ctls.reindex(columns=new_cols)
            df_ctl_sum = df_ctls.groupby(
                [col.name for col in summary_class[summary_level]['ctl'].__table__.primary_key.columns.values()]).agg(
                agg_dict['ctl']).copy().reset_index()
            if 'date' not in df_ctl_sum.columns:
                df_ctl_sum['date'] = df_ctl_sum['datetime'].dt.date
            df_ctl_sum['last_update_time'] = current_time
            df_ctl_sum['smf70lac'] = round2int(df_ctl_sum['smf70lac'])
            df_ctl_sum['smf70lacm'] = round2int(df_ctl_sum['smf70lacm'])
            df_ctl_sum['smf70laca'] = round2int(df_ctl_sum['smf70laca'])
            df_ctl_sum['smf70lacb'] = round2int(df_ctl_sum['smf70lacb'])
            df_ctl_sum['smf70laccr'] = round2int(df_ctl_sum['smf70laccr'])

            df_ctl_sum.set_index(
                [col.name for col in summary_class[summary_level]['ctl'].__table__.primary_key.columns.values()],
                inplace=True)
            df_cpu_list = []
            null_column_list = []
            for part in partitions_range:
                df_cpu = pd.read_sql(ctl_stmt1b, db_engines[f'70.{part}'])
                if not df_cpu.empty:
                    df_cpu['date'] = df_cpu['datetime'].dt.date
                    df_cpu_list.append(df_cpu)
                    null_columns = df_cpu.columns[df_cpu.isna().all()].tolist()
                    for col in null_columns:
                        if col not in null_column_list:
                            null_column_list.append(col)
            df_cpus = pd.concat([df.dropna(axis=1, how='all') for df in df_cpu_list])
            if len(null_column_list) > 0:
                new_cols = df_cpus.columns.tolist()
                for col in null_column_list:
                    if col not in new_cols:
                        new_cols.append(col)
                df_cpus = df_cpus.reindex(columns=new_cols)
            # format Smf7Cpu
            df_cpus['cpu_is_online'] = df_cpus['smf70cnf'].apply(
                lambda x: is_bit_set(int(x), 8, 7) if not pd.isna(x) else np.nan)
            core_df_cpus = df_cpus[(df_cpus['cpu_is_online'] == 1) & (df_cpus['sub_core_idx'] == 0)].copy()
            core_df_cpus['cpu_online_time'] = np.where(core_df_cpus['smf70ont'] > 0,
                                                       core_df_cpus['smf70ont'],
                                                       core_df_cpus['smf70int'])
            core_df_cpus['cpu_core_busy_pct'] = core_df_cpus['smf70pdt'] / core_df_cpus[
                'cpu_online_time']

            df_cpu_sum = df_cpus.groupby(
                [col.name for col in summary_class[summary_level]['cpu'].__table__.primary_key.columns.values()]).agg(
                agg_dict['cpu']).reset_index()
            if 'date' not in df_cpu_sum.columns:
                df_cpu_sum['date'] = df_cpu_sum['datetime'].dt.date
            df_cpu_sum['rate_io_interrupt_by_tpi'] = (
                    100 * df_cpu_sum['smf70tpi'] / (df_cpu_sum['smf70slh'] + df_cpu_sum['smf70tpi'])).where(
                (df_cpu_sum['smf70typ'] == 'CP') & ((df_cpu_sum['smf70slh'] + df_cpu_sum['smf70tpi']) > 0),
                np.nan)
            df_cpu_sum['lpar_busy_percentage'] = np.where(df_cpu_sum['cpu_time'].notnull(),
                                                          df_cpu_sum['cpu_time'] / df_cpu_sum['smf70int'] * 100,
                                                          np.nan)
            df_cpu_sum['cpu_parked_percentage'] = (
                    df_cpu_sum['smf70pat'] / df_cpu_sum['smf70int'] * 100).clip(upper=100)
            df_cpu_sum['cpu_unparked_percentage'] = (
                    df_cpu_sum['cpu_unparked_time'] / df_cpu_sum['smf70int'] * 100).clip(upper=100)
            df_cpu_sum['mvs_busy_percentage'] = np.where(df_cpu_sum['cpu_unparked_percentage'] > 0.1,
                                                         (df_cpu_sum['time_range'] - df_cpu_sum['smf70wat']) /
                                                         df_cpu_sum['time_range'] * 100, np.nan)
            df_cpu_sum['cpu_busy_percentage'] = (
                    df_cpu_sum['cpu_busy_time'] * df_cpu_sum['cpu_unparked_percentage'] / df_cpu_sum[
                'cpu_unparked_time'] * 100).where(
                df_cpu_sum['cpu_unparked_time'] > 0, 0)

            df_cpu_sum['mvs_busy_unpark_total'] = (df_cpu_sum['cpu_unparked_percentage'] / 100).where(
                df_cpu_sum['cpu_is_online'] == 1, np.nan)
            df_cpu_sum['mvs_busy_total'] = (
                    df_cpu_sum['mvs_busy_percentage'] * df_cpu_sum['cpu_unparked_percentage'] / 100).where(
                df_cpu_sum['cpu_is_online'] == 1, np.nan)

            df_cpu_sum.set_index(
                [col.name for col in summary_class[summary_level]['cpu'].__table__.primary_key.columns.values()],
                inplace=True)
            df_cpu_sum['mt_prod'] = weighted_avg(core_df_cpus, 'smf70_prod', 'cpu_core_busy_pct',
                                                 [col.name for col in
                                                  summary_class[summary_level][
                                                      'cpu'].__table__.primary_key.columns.values()]) / 1024 * 100
            # end of formatting
            cpus_group_columns = [col.name for col in
                                  summary_class[summary_level]['ctl'].__table__.primary_key.columns.values()] + [
                                     'smf70typ']
            df_cpus_gp = df_cpus.groupby(cpus_group_columns).agg(
                mvs_busy_unpark_total=('cpu_unparked_percentage', 'sum'),
                mvs_busy_total=('mvs_busy_total', 'sum'))
            df_cpus_gp['mvs_busy_unpark_total'] = df_cpus_gp['mvs_busy_unpark_total'] / 100
            df_cpus_gp['mvs_busy_total'] = df_cpus_gp['mvs_busy_total'] / df_cpus_gp['mvs_busy_unpark_total']
            df_cpus_gp['intervals'] = df_cpus[df_cpus['sub_core_idx'] == 0].groupby(cpus_group_columns)[
                'smf70ist'].unique().count()
            df_cpus_gp['mt_prod_total'] = df_cpus[df_cpus['sub_core_idx'] == 0].groupby(cpus_group_columns)[
                'mt_prod'].mean()
            df_cpus_gp['mt_util_total'] = df_cpus[df_cpus['sub_core_idx'] == 0].groupby(cpus_group_columns)[
                'mt_util'].mean()
            df_cpus_gp['lpar_busy_total'] = df_cpus[df_cpus['sub_core_idx'] == 0].groupby(cpus_group_columns)[
                'lpar_busy_percentage'].mean()
            df_cpus_gp['rate_io_interrupt_by_tpi_total'] = \
                df_cpu_sum[df_cpu_sum['sub_core_idx'] == 0].groupby(cpus_group_columns)[
                    'rate_io_interrupt_by_tpi'].sum()

            cpus_piv_columns = ['mt_util_total', 'mt_prod_total', 'lpar_busy_total', 'mvs_busy_unpark_total',
                                'mvs_busy_total',
                                'rate_io_interrupt_by_tpi_total', 'intervals']
            cpus_gp_piv = df_cpus_gp.copy().reset_index().pivot(
                index=[col.name for col in summary_class[summary_level]['ctl'].__table__.primary_key.columns.values()],
                columns='smf70typ', values=cpus_piv_columns).reset_index().set_index(
                [col.name for col in summary_class[summary_level]['ctl'].__table__.primary_key.columns.values()])
            cpus_gp_piv.columns = ['_'.join(str(s.lower()).strip() for s in col if s) for col in
                                   cpus_gp_piv.columns]
            df_ctl_sum = df_ctl_sum.join(cpus_gp_piv.rename(
                columns={'rate_io_interrupt_by_tpi_total_cp': 'rate_io_interrupt_by_tpi_total'}))
            if 'mvs_busy_unpark_total_iip' in df_ctl_sum.columns:
                df_ctl_sum['numproc'] = (df_ctl_sum['mvs_busy_unpark_total_cp'] / df_ctl_sum['intervals_cp'] +
                                         df_ctl_sum['mvs_busy_unpark_total_iip'] / df_ctl_sum['intervals_iip'])
            else:
                df_ctl_sum['numproc'] = df_ctl_sum['mvs_busy_unpark_total_cp'] / df_ctl_sum['intervals_cp']

            df_ctl_sum['smf70mcf'] = weighted_avg(df_ctls,
                                                  'smf70mcf',
                                                  'lpar_busy_total_cp',
                                                  [col.name for col in
                                                   summary_class[summary_level][
                                                       'ctl'].__table__.primary_key.columns.values()])
            df_ctl_sum['smf70mcfs'] = weighted_avg(df_ctls,
                                                   'smf70mcfs',
                                                   'lpar_busy_total_iip',
                                                   [col.name for col in
                                                    summary_class[summary_level][
                                                        'ctl'].__table__.primary_key.columns.values()])

            df_ctl_sum['smf70cf'] = weighted_avg(df_ctls,
                                                 'smf70cf',
                                                 'lpar_busy_total_cp',
                                                 [col.name for col in
                                                  summary_class[summary_level][
                                                      'ctl'].__table__.primary_key.columns.values()])
            df_ctl_sum['smf70cfs'] = weighted_avg(df_ctls,
                                                  'smf70cfs',
                                                  'lpar_busy_total_iip',
                                                  [col.name for col in
                                                   summary_class[summary_level][
                                                       'ctl'].__table__.primary_key.columns.values()])

            df_ctl_sum['smf70atd'] = weighted_avg(df_ctls, 'smf70atd', 'lpar_busy_total_cp',
                                                  [col.name for col in
                                                   summary_class[summary_level][
                                                       'ctl'].__table__.primary_key.columns.values()])
            df_ctl_sum['smf70atds'] = weighted_avg(df_ctls, 'smf70atds', 'lpar_busy_total_iip',
                                                   [col.name for col in
                                                    summary_class[summary_level][
                                                        'ctl'].__table__.primary_key.columns.values()])
            if not df_ctls['lpar_busy_total_aap'].isnull().all():
                df_ctl_sum['smf70mcfi'] = weighted_avg(df_ctls, 'smf70mcfi', 'lpar_busy_total_aap',
                                                       [col.name for col in
                                                        summary_class[summary_level][
                                                            'ctl'].__table__.primary_key.columns.values()])
                df_ctl_sum['smf70cfi'] = weighted_avg(df_ctls, 'smf70cfi', 'lpar_busy_total_aap',
                                                      [col.name for col in
                                                       summary_class[summary_level][
                                                           'ctl'].__table__.primary_key.columns.values()])
                df_ctl_sum['smf70atdi'] = weighted_avg(df_ctls, 'smf70atdi', 'lpar_busy_total_iip',
                                                       [col.name for col in
                                                        summary_class[summary_level][
                                                            'ctl'].__table__.primary_key.columns.values()])

            insert_dict['ctl'] = df_upsert(db_driver, db_engines[summary_engine[summary_level]], db_session,
                                           df_ctl_sum.reset_index()[
                                               [col for col in
                                                summary_class[summary_level]['ctl'].__table__.columns.keys()
                                                if col in df_ctl_sum.reset_index().columns]],
                                           summary_tblname[summary_level]['ctl'], summary_class[summary_level]['ctl'],
                                           'smf70',
                                           [col.name for col in
                                            summary_class[summary_level]['ctl'].__table__.primary_key.columns.values()],
                                           int_dtypedict['ctl'], shard_id=summary_engine[summary_level]
                                           )

    # Summing up Smf70Cpu
    df_cpu_list = []
    null_column_list = []
    cpu_stmt = select(Smf70Cpu).where(Smf70Cpu.datetime.between(start, end))
    for part in partitions_range:
        df_cpu = pd.read_sql(cpu_stmt, db_engines[f'70.{part}'])
        if not df_cpu.empty:
            df_cpu['date'] = df_cpu['datetime'].dt.date
            df_cpu_list.append(df_cpu)
            null_columns = df_cpu.columns[df_cpu.isna().all()].tolist()
            for col in null_columns:
                if col not in null_column_list:
                    null_column_list.append(col)
    if len(df_cpu_list) > 0:
        df_cpus = pd.concat([df.dropna(axis=1, how='all') for df in df_cpu_list])
        if len(null_column_list) > 0:
            new_cols = df_cpus.columns.tolist()
            for col in null_column_list:
                if col not in new_cols:
                    new_cols.append(col)
            df_cpus = df_cpus.reindex(columns=new_cols)
        df_cpus['cpu_is_online'] = df_cpus['smf70cnf'].apply(
            lambda x: is_bit_set(int(x), 8, 7) if not pd.isna(x) else np.nan)
        core_df_cpus = df_cpus[(df_cpus['cpu_is_online'] == 1) & (df_cpus['sub_core_idx'] == 0)].copy()
        core_df_cpus['cpu_online_time'] = np.where(core_df_cpus['smf70ont'] > 0,
                                                   core_df_cpus['smf70ont'],
                                                   core_df_cpus['smf70int'])
        core_df_cpus['cpu_core_busy_pct'] = core_df_cpus['smf70pdt'] / core_df_cpus[
            'cpu_online_time']
        df_cpus['date'] = df_cpus['datetime'].dt.date

        df_cpu_sum = df_cpus.groupby(
            [col.name for col in summary_class[summary_level]['cpu'].__table__.primary_key.columns.values()]).agg(
            agg_dict['cpu']).reset_index()
        if 'date' not in df_cpu_sum.columns:
            df_cpu_sum['date'] = df_cpu_sum['datetime'].dt.date
        df_cpu_sum['last_update_time'] = current_time
        df_cpu_sum['rate_io_interrupt_by_tpi'] = (
                100 * df_cpu_sum['smf70tpi'] / (df_cpu_sum['smf70slh'] + df_cpu_sum['smf70tpi'])).where(
            (df_cpu_sum['smf70typ'] == 'CP') & ((df_cpu_sum['smf70slh'] + df_cpu_sum['smf70tpi']) > 0),
            np.nan)
        df_cpu_sum['lpar_busy_percentage'] = np.where(df_cpu_sum['cpu_time'].notnull(),
                                                      df_cpu_sum['cpu_time'] / df_cpu_sum['smf70int'] * 100,
                                                      np.nan)
        df_cpu_sum['cpu_parked_percentage'] = (
                df_cpu_sum['smf70pat'] / df_cpu_sum['smf70int'] * 100).clip(upper=100)
        df_cpu_sum['cpu_unparked_percentage'] = (
                df_cpu_sum['cpu_unparked_time'] / df_cpu_sum['smf70int'] * 100).clip(upper=100)
        df_cpu_sum['mvs_busy_percentage'] = np.where(df_cpu_sum['cpu_unparked_percentage'] > 0.1,
                                                     (df_cpu_sum['time_range'] - df_cpu_sum['smf70wat']) /
                                                     df_cpu_sum['time_range'] * 100, np.nan)
        df_cpu_sum['cpu_busy_percentage'] = (
                df_cpu_sum['cpu_busy_time'] * df_cpu_sum['cpu_unparked_percentage'] / df_cpu_sum[
            'cpu_unparked_time'] * 100).where(
            df_cpu_sum['cpu_unparked_time'] > 0, 0)

        df_cpu_sum['mvs_busy_unpark_total'] = (df_cpu_sum['cpu_unparked_percentage'] / 100).where(
            df_cpu_sum['cpu_is_online'] == 1, np.nan)
        df_cpu_sum['mvs_busy_total'] = (
                df_cpu_sum['mvs_busy_percentage'] * df_cpu_sum['cpu_unparked_percentage'] / 100).where(
            df_cpu_sum['cpu_is_online'] == 1, np.nan)

        df_cpu_sum.set_index(
            [col.name for col in summary_class[summary_level]['cpu'].__table__.primary_key.columns.values()],
            inplace=True)
        df_cpu_sum['mt_prod'] = weighted_avg(core_df_cpus, 'smf70_prod', 'cpu_core_busy_pct',
                                             [col.name for col in
                                              summary_class[summary_level][
                                                  'cpu'].__table__.primary_key.columns.values()]) / 1024 * 100
        insert_dict['cpu'] = df_upsert(db_driver, db_engines[summary_engine[summary_level]], db_session,
                                       df_cpu_sum.reset_index()[
                                           [col for col in summary_class[summary_level]['cpu'].__table__.columns.keys()
                                            if col in df_cpu_sum.reset_index().columns]],
                                       summary_tblname[summary_level]['cpu'], summary_class[summary_level]['cpu'],
                                       'smf70',
                                       [col.name for col in
                                        summary_class[summary_level]['cpu'].__table__.primary_key.columns.values()],
                                       int_dtypedict['cpu'], shard_id=summary_engine[summary_level]
                                       )

    # Summing up Smf70Aid
    insert_dict['aid'] = sum_up_by_partition(tbls['aid'], summary_class[summary_level]['aid'],
                                             summary_tblname[summary_level]['aid'],
                                             start, end, current_time, agg_dict['aid'], int_dtypedict['aid'],
                                             partitions_scheme, summary_engine[summary_level],
                                             db_engines, '70', 'smf70', db_session, db_driver)

    # Summing up Smf70Bct
    insert_dict['bct'] = sum_up_by_partition(tbls['bct'], summary_class[summary_level]['bct'],
                                             summary_tblname[summary_level]['bct'],
                                             start, end, current_time, agg_dict['bct'], int_dtypedict['bct'],
                                             partitions_scheme, summary_engine[summary_level],
                                             db_engines, '70', 'smf70', db_session, db_driver)

    # Summing up Smf70BctCpu
    insert_dict['bct_cpu'] = sum_up_by_partition(tbls['bct_cpu'], summary_class[summary_level]['bct_cpu'],
                                                 summary_tblname[summary_level]['bct_cpu'],
                                                 start, end, current_time, agg_dict['bct_cpu'], int_dtypedict['bct_cpu'],
                                                 partitions_scheme, summary_engine[summary_level],
                                                 db_engines, '70', 'smf70', db_session, db_driver)

    # Summing up Smf70Bpd
    insert_dict['bpd'] = sum_up_by_partition(tbls['bpd'], summary_class[summary_level]['bpd'],
                                             summary_tblname[summary_level]['bpd'],
                                             start, end, current_time, agg_dict['bpd'], int_dtypedict['bpd'],
                                             partitions_scheme, summary_engine[summary_level],
                                             db_engines, '70', 'smf70', db_session, db_driver)

    # SUming up Smf70Trg
    insert_dict['trg'] = sum_up_by_partition(tbls['trg'], summary_class[summary_level]['trg'],
                                             summary_tblname[summary_level]['trg'],
                                             start, end, current_time, agg_dict['trg'], int_dtypedict['trg'],
                                             partitions_scheme, summary_engine[summary_level],
                                             db_engines, '70','smf70', db_session, db_driver)

    # Summing up ccf
    insert_dict['ccf'] = sum_up_by_partition(tbls['ccf'], summary_class[summary_level]['ccf'],
                                             summary_tblname[summary_level]['ccf'],
                                             start, end, current_time, agg_dict['ccf'], int_dtypedict['ccf'],
                                             partitions_scheme, summary_engine[summary_level],
                                             db_engines, '70', 'smf70', db_session, db_driver)

    # Summing up Smf70Typ3
    insert_dict['typ3'] = sum_up_by_partition(tbls['typ3'], summary_class[summary_level]['typ3'],
                                              summary_tblname[summary_level]['typ3'],
                                              start, end, current_time, agg_dict['typ3'], int_dtypedict['typ3'],
                                              partitions_scheme, summary_engine[summary_level],
                                              db_engines, '70', 'smf70', db_session, db_driver)

    # Summing up Smf70Typ4
    insert_dict['typ4'] = sum_up_by_partition(tbls['typ4'], summary_class[summary_level]['typ4'],
                                              summary_tblname[summary_level]['typ4'],
                                              start, end, current_time, agg_dict['typ4'], int_dtypedict['typ4'],
                                              partitions_scheme, summary_engine[summary_level],
                                              db_engines, '70', 'smf70', db_session, db_driver)

    # Summing up Smf70Typ5
    insert_dict['typ5'] = sum_up_by_partition(tbls['typ5'], summary_class[summary_level]['typ5'],
                                              summary_tblname[summary_level]['typ5'],
                                              start, end, current_time, agg_dict['typ5'], int_dtypedict['typ5'],
                                              partitions_scheme, summary_engine[summary_level],
                                              db_engines, '70', 'smf70', db_session, db_driver)


    result_list.append({summary_tblname[summary_level][k]:v for k,v in insert_dict.items() if k in summary_tblname[summary_level].keys()})

    et = time.time()  # get the end time
    # get the execution time
    elapsed_time = (et - st) / 60
    print(f'Execution time ({summary_level}):', elapsed_time, 'minutes')

    overall_et = time.time()
    overall_elapsed_time = (overall_et - overall_st) / 60
    return UploadResult(result_list, overall_elapsed_time, SUCCESS)
