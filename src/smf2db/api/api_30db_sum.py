import datetime as dt
import time

import numpy as np
import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from smf2db import SUCCESS
from smf2db.api.util import (list_max, v_index, list_loc, agg_next, agg_tolist, agg_boost_class,
                             UploadResult, agg_hex_sum, df_upsert, sum_up_by_partition,
                             create_int_dtypedict)
from smf2db.db_models.smf30_da_model import (Smf30IdDa, Smf30UraDa, Smf30PrfDa, Smf30CasDa, Smf30SapDa, Smf30OpsDa,
                                             Smf30ExpDa, Smf30OpDa, Smf30UdDa, Smf30UssDa, Smf306Da)
from smf2db.db_models.smf30_hr_model import (Smf30IdHr, Smf30UraHr, Smf30PrfHr, Smf30CasHr, Smf30SapHr,
                                             Smf30OpsHr, Smf30ExpHr, Smf30OpHr, Smf30UdHr, Smf30UssHr, Smf306Hr)
from smf2db.db_models.smf30_model import (Smf30Id, Smf30Ura, Smf30Prf, Smf30Cas, Smf30Sap, Smf30Ops, Smf30Exp, Smf30Op,
                                          Smf30Ud, Smf30Uss, Smf306)

agg_prf = {'smf30srv': 'sum', 'smf30csu': 'sum', 'smf30srb': 'sum', 'smf30io': 'sum', 'smf30mso': 'sum',
           'smf30tat': 'sum', 'smf30sus': agg_next, 'smf30res': 'sum', 'smf30trs': 'sum', 'smf30eta': 'sum',
           'smf30esu': 'sum', 'smf30etc': 'sum', 'smf30jqt': 'sum', 'smf30rqt': 'sum', 'smf30hqt': 'sum',
           'smf30sqt': 'sum', 'smf30msc': agg_next, 'smf30cpc': agg_next, 'smf30loc': agg_next, 'smf30src': agg_next,
           'smf30znf': agg_next, 'smf30snf': agg_next, 'smf30srv_l': 'sum', 'smf30csu_l': 'sum', 'smf30srb_l': 'sum',
           'smf30io_l': 'sum', 'smf30mso_l': 'sum', 'smf30esu_l': 'sum', 'smf30_capacity_change_cnt': 'sum',
           'smf30_rctpcpua_actual': agg_next, 'smf30_rctpcpua_nominal': agg_next,
           'smf30_rctpcpua_scaling_factor': agg_next, 'smf30_capacity_adjustment_ind': agg_next,
           'smf30_rmctadjn_nominal': agg_next}
agg_ura = {'smf30inp': 'sum', 'smf30tep': 'sum', 'smf30tpt': 'sum', 'smf30tgt': 'sum', 'smf30tcn': 'sum',
           'smf30trr': 'sum', 'smf30aic': 'sum', 'smf30aid': 'sum', 'smf30aiw': 'sum', 'smf30ais': 'sum',
           'smf30eic': 'sum', 'smf30eid': 'sum', 'smf30eiw': 'sum', 'smf30eis': 'sum', 'smf30tex': 'sum',
           'smf30das': 'sum'}
agg_cas = {'smf30cpt': 'sum', 'smf30cps': 'sum', 'smf30icu': 'sum', 'smf30isb': 'sum', 'smf30jvu': 'sum',
           'smf30ivu': 'sum', 'smf30jva': 'sum', 'smf30iva': 'sum', 'smf30iip': 'sum', 'smf30rct': 'sum',
           'smf30hpt': 'sum', 'smf30csc': 'sum', 'smf30dmi': 'sum', 'smf30dmo': 'sum', 'smf30asr': 'sum',
           'smf30enc': 'sum', 'smf30det': 'sum', 'smf30cep': 'sum', 'ziipboost_active': 'max',
           'speedboost_active': 'max', 'boostclass': agg_boost_class, 'smf30_time_on_ifa': 'sum',
           'smf30_enclave_time_on_ifa': 'sum', 'smf30_dep_enclave_time_on_ifa': 'sum', 'smf30_time_ifa_on_cp': 'sum',
           'smf30_enclave_time_ifa_on_cp': 'sum', 'smf30_dep_enclave_time_ifa_on_cp': 'sum', 'smf30cepi': 'sum',
           'smf30_time_on_ziip': 'sum', 'smf30_enclave_time_on_ziip': 'sum', 'smf30_depenc_time_on_ziip': 'sum',
           'smf30_time_ziip_on_cp': 'sum', 'smf30_enclave_time_ziip_on_cp': 'sum','smf30_depenc_time_ziip_on_cp': 'sum',
           'smf30_enclave_time_ziip_qual': 'sum', 'smf30_depenc_time_ziip_qual': 'sum', 'smf30_time_java_on_ziip': 'sum',
           'smf30_enclave_time_java_on_ziip': 'sum', 'smf30_depenc_time_java_on_ziip': 'sum',
           'smf30_time_java_on_cp': 'sum', 'smf30_enclave_time_java_on_cp': 'sum',
           'smf30_depenc_time_java_on_cp': 'sum', 'smf30crp': 'sum', 'smf30icu_step_term': 'sum',
           'smf30icu_step_init': 'sum', 'smf30isb_step_term': 'sum', 'smf30isb_step_init': 'sum',
           'smf30_missed_smf30blk': 'sum', 'smf30_missed_smf30dct': 'sum', 'smf30_highest_task_cpu_percent': agg_tolist,
           'smf30_highest_task_cpu_program': agg_tolist, 'smf30_boostinfo': 'last', 'smf30cas_flag': 'last',}
agg_sap = {'smf30pgi': 'sum', 'smf30pgo': 'sum', 'smf30cpm': 'sum', 'smf30nsw': 'sum', 'smf30psi': 'sum',
           'smf30pso': 'sum', 'smf30vpi': 'sum', 'smf30vpo': 'sum', 'smf30vpr': 'sum', 'smf30cpi': 'sum',
           'smf30hpi': 'sum', 'smf30lpi': 'sum', 'smf30hpo': 'sum', 'smf30pst': 'sum', 'smf30psc': 'sum',
           'smf30pie': 'sum', 'smf30poe': 'sum', 'smf30bia': 'sum', 'smf30boa': 'sum', 'smf30bie': 'sum',
           'smf30boe': 'sum', 'smf30kia': 'sum', 'smf30koa': 'sum', 'smf30kie': 'sum', 'smf30koe': 'sum',
           'smf30psf': 'sum', 'smf30pai': 'sum', 'smf30pei': 'sum', 'smf30ers': 'sum', 'smf30hvr': 'max',
           'smf30hva': 'max', 'smf30tih': 'sum', 'smf30numberofdataspaceshwm': 'max',
           'smf30userdataspacecreatereqcount': 'sum', 'smf30_dmemrequested2g': 'sum',
           'smf30_dmemminrequested2g': 'sum','smf30_dmemassigned2g': 'sum',
           'smf30_dmemnuminuseas2g': 'sum', 'smf30_dmemnuminuseasfixed1m': 'sum',
           'smf30_dmemnuminuseaspageable1m': 'sum', 'smf30_dmemnuminuseas4k': 'sum',
           'smf30_dmemnuminuseasdattables': 'sum', 'smf30_dmemnuminuseas4khwm': 'max',
           'smf30_dmemnuminuseaspageable1mhwm': 'max', 'smf30_dmemnuminuseasfixed1mhwm': 'max',
           'smf30_dmemnuminuseas2ghwm': 'max', 'smf30_dmemnuminuseasdattableshwm': 'max',
           'smf30_dmemnuminusehwm': 'max', 'smf30_dmemnum2gfailed': 'sum', 'smf30_dmemnum1mfailed': 'sum',
           'smf30_dmemnum4kfailed': 'sum', 'smf30_numinuseas2ghwm': 'max', 'smf30_num2gfailed': 'sum',
           'smf30_obtainshomespace': 'sum', 'smf30_iarv64obtainshomespace': 'sum',
           'smf30_framesfirstreferencebacking': 'sum', 'smf30_sumreal1m': 'sum',
           'smf30_sumsquaresreal1m':agg_hex_sum,'smf30_numsamples': 'sum', 'smf30_hwmhvreal1m': 'sum'}
agg_uss = {'smf30_us_comprreq': 'sum', 'smf30_us_comprreq_prob': 'sum', 'smf30_us_queuetime': 'sum',
           'smf30_us_exectime': 'sum', 'smf30_us_def_uncomprin': 'sum', 'smf30_us_def_comprout': 'sum',
           'smf30_us_inf_comprin': 'sum', 'smf30_us_inf_decomprout': 'sum'}
agg_exp = {'smf30dct': 'sum'}
agg_ops = {'smf30pdm': 'sum', 'smf30prd': 'sum', 'smf30ptm': 'sum', 'smf30tpr': 'sum', 'smf30mtm': 'sum',
           'smf30msr': 'sum'}
agg_op = {'smf30osc': 'sum', 'smf30ost': 'sum', 'smf30odr': 'sum', 'smf30ofr': 'sum', 'smf30ofw': 'sum',
          'smf30opr': 'sum', 'smf30opw': 'sum', 'smf30oll': 'sum', 'smf30olp': 'sum', 'smf30ogl': 'sum',
          'smf30ogp': 'sum', 'smf30osy': 'sum'}
agg_ud = {'smf30uct': 'sum', 'smf30ucs': 'sum'}
agg_core_hr = {'duration': 'sum', 'tcb_time': 'sum', 'srb_time': 'sum', 'smf30_time_on_ziip': 'sum', 'cpu_total': 'sum',
               'smf30tex': 'sum', 'smf30_rctpcpua_actual': agg_next, 'smf30_rctpcpua_nominal': agg_next,
               'smf30_rctpcpua_scaling_factor': agg_next, 'smf30_capacity_adjustment_ind': agg_next,
               'smf30_rmctadjn_nominal': agg_next, 'smf30pgi': 'sum', 'smf30pgo': 'sum', 'smf30nsw': 'sum'}
agg_core_da = {'duration': 'sum', 'tcb_time': 'sum', 'srb_time': 'sum', 'smf30_time_on_ziip': 'sum', 'cpu_total': 'sum',
               'smf30tex': 'sum', 'smf30_rctpcpua_actual': agg_next, 'smf30_rctpcpua_nominal': agg_next,
               'smf30_rctpcpua_scaling_factor': agg_next, 'smf30_capacity_adjustment_ind': agg_next,
               'smf30_rmctadjn_nominal': agg_next, 'smf30pgi': 'sum', 'smf30pgo': 'sum', 'smf30nsw': 'sum',
               'consumed_msu': 'mean'}
agg_smf306_hr = {'duration': 'sum', 'tcb_time': 'sum', 'srb_time': 'sum', 'smf30_time_on_ziip': 'sum', 'cpu_total': 'sum',
                 'smf30rvn': 'last', 'smf30pnm': 'last', 'smf30osl': 'last', 'smf30cls': 'last', 'smf30jpt': 'last',
                 'smf30stn': 'last', 'smf30ear': 'last', 'smf30arb': 'last', 'smf30eur': 'last', 'smf30urb': 'last',
                 'smf30hvo': 'last',
                 # io activity
                 'smf30inp': 'sum', 'smf30tep': 'sum', 'smf30tpt': 'sum', 'smf30tgt': 'sum', 'smf30tcn': 'sum',
                 'smf30trr': 'sum', 'smf30aic': 'sum', 'smf30aid': 'sum', 'smf30aiw': 'sum', 'smf30ais': 'sum',
                 'smf30eic': 'sum', 'smf30eid': 'sum', 'smf30eiw': 'sum', 'smf30eis': 'sum', 'smf30tex': 'sum',
                 'smf30das': 'sum',
                 # Performance section
                 'smf30srv': 'sum', 'smf30csu': 'sum', 'smf30srb': 'sum', 'smf30io': 'sum', 'smf30mso': 'sum',
                 'smf30tat': 'sum', 'smf30sus': agg_next, 'smf30res': 'sum', 'smf30trs': 'sum', 'smf30eta': 'sum',
                 'smf30esu': 'sum', 'smf30etc': 'sum', 'smf30jqt': 'sum', 'smf30rqt': 'sum', 'smf30hqt': 'sum',
                 'smf30sqt': 'sum', 'smf30msc': agg_next, 'smf30cpc': agg_next, 'smf30loc': agg_next,
                 'smf30src': agg_next, 'smf30znf': agg_next, 'smf30snf': agg_next, 'smf30srv_l': 'sum',
                 'smf30csu_l': 'sum', 'smf30srb_l': 'sum', 'smf30io_l': 'sum', 'smf30mso_l': 'sum', 'smf30esu_l': 'sum',
                 'smf30_capacity_change_cnt': 'sum', 'smf30_rctpcpua_actual': agg_next,
                 'smf30_rctpcpua_nominal': agg_next, 'smf30_rctpcpua_scaling_factor': agg_next,
                 'smf30_capacity_adjustment_ind': agg_next, 'smf30_rmctadjn_nominal': agg_next,
                 # Process Accounting section
                 'smf30cpt': 'sum', 'smf30cps': 'sum', 'smf30icu': 'sum', 'smf30isb': 'sum', 'smf30jvu': 'sum',
                 'smf30ivu': 'sum', 'smf30jva': 'sum', 'smf30iva': 'sum', 'smf30iip': 'sum', 'smf30rct': 'sum',
                 'smf30hpt': 'sum', 'smf30csc': 'sum', 'smf30dmi': 'sum', 'smf30dmo': 'sum', 'smf30asr': 'sum',
                 'smf30enc': 'sum', 'smf30det': 'sum', 'smf30cep': 'sum', 'ziipboost_active': 'max',
                 'speedboost_active': 'max', 'boostclass': agg_boost_class, 'smf30_time_on_ifa': 'sum',
                 'smf30_enclave_time_on_ifa': 'sum', 'smf30_dep_enclave_time_on_ifa': 'sum',
                 'smf30_time_ifa_on_cp': 'sum', 'smf30_enclave_time_ifa_on_cp': 'sum',
                 'smf30_dep_enclave_time_ifa_on_cp': 'sum', 'smf30cepi': 'sum', 'smf30_enclave_time_on_ziip': 'sum',
                 'smf30_depenc_time_on_ziip': 'sum', 'smf30_time_ziip_on_cp': 'sum', 'smf30_enclave_time_ziip_on_cp': 'sum',
                 'smf30_depenc_time_ziip_on_cp': 'sum', 'smf30_enclave_time_ziip_qual': 'sum',
                 'smf30_depenc_time_ziip_qual': 'sum','smf30_time_java_on_ziip': 'sum',
                 'smf30_enclave_time_java_on_ziip': 'sum', 'smf30_depenc_time_java_on_ziip': 'sum',
                 'smf30_time_java_on_cp': 'sum', 'smf30_enclave_time_java_on_cp': 'sum',
                 'smf30_depenc_time_java_on_cp': 'sum', 'smf30crp': 'sum', 'smf30icu_step_term': 'sum',
                 'smf30icu_step_init': 'sum', 'smf30isb_step_term': 'sum', 'smf30isb_step_init': 'sum',
                 'smf30_missed_smf30blk': 'sum', 'smf30_missed_smf30dct': 'sum',
                 'smf30_highest_task_cpu_percent': agg_tolist, 'smf30_highest_task_cpu_program': agg_tolist,
                 'smf30_boostinfo': 'last', 'smf30cas_flag': 'last',
                 # Storage and Paging section
                 'smf30pgi': 'sum', 'smf30pgo': 'sum', 'smf30cpm': 'sum', 'smf30nsw': 'sum', 'smf30psi': 'sum',
                 'smf30pso': 'sum', 'smf30vpi': 'sum', 'smf30vpo': 'sum', 'smf30vpr': 'sum', 'smf30cpi': 'sum',
                 'smf30hpi': 'sum', 'smf30lpi': 'sum', 'smf30hpo': 'sum', 'smf30pst': 'sum', 'smf30psc': 'sum',
                 'smf30pie': 'sum', 'smf30poe': 'sum', 'smf30bia': 'sum', 'smf30boa': 'sum', 'smf30bie': 'sum',
                 'smf30boe': 'sum', 'smf30kia': 'sum', 'smf30koa': 'sum', 'smf30kie': 'sum', 'smf30koe': 'sum',
                 'smf30psf': 'sum', 'smf30pai': 'sum', 'smf30pei': 'sum', 'smf30ers': 'sum', 'smf30hvr': 'max',
                 'smf30hva': 'max', 'smf30tih': 'sum', 'smf30numberofdataspaceshwm': 'max',
                 'smf30userdataspacecreatereqcount': 'sum', 'smf30_dmemrequested2g': 'sum',
                 'smf30_dmemminrequested2g': 'sum','smf30_dmemassigned2g': 'sum',
                 'smf30_dmemnuminuseas2g': 'sum', 'smf30_dmemnuminuseasfixed1m': 'sum',
                 'smf30_dmemnuminuseaspageable1m': 'sum', 'smf30_dmemnuminuseas4k': 'sum',
                 'smf30_dmemnuminuseasdattables': 'sum', 'smf30_dmemnuminuseas4khwm': 'max',
                 'smf30_dmemnuminuseaspageable1mhwm': 'max', 'smf30_dmemnuminuseasfixed1mhwm': 'max',
                 'smf30_dmemnuminuseas2ghwm': 'max', 'smf30_dmemnuminuseasdattableshwm': 'max',
                 'smf30_dmemnuminusehwm': 'max', 'smf30_dmemnum2gfailed': 'sum', 'smf30_dmemnum1mfailed': 'sum',
                 'smf30_dmemnum4kfailed': 'sum', 'smf30_numinuseas2ghwm': 'max','smf30_num2gfailed': 'sum',
                 'smf30_obtainshomespace': 'sum', 'smf30_iarv64obtainshomespace': 'sum',
                 'smf30_framesfirstreferencebacking': 'sum', 'smf30_sumreal1m': 'sum',
                 'smf30_sumsquaresreal1m':agg_hex_sum, 'smf30_numsamples': 'sum', 'smf30_hwmhvreal1m': 'sum',
                 # operator section
                 'smf30pdm': 'sum', 'smf30prd': 'sum', 'smf30ptm': 'sum', 'smf30tpr': 'sum', 'smf30mtm': 'sum',
                 'smf30msr': 'sum'}
agg_smf306_da = {'duration': 'sum', 'tcb_time': 'sum', 'srb_time': 'sum', 'smf30_time_on_ziip': 'sum', 'cpu_total': 'sum',
                 'smf30rvn': 'last', 'smf30pnm': 'last', 'smf30osl': 'last', 'smf30cls': 'last', 'smf30jpt': 'last',
                 'smf30stn': 'last', 'smf30ear': 'last', 'smf30arb': 'last', 'smf30eur': 'last', 'smf30urb': 'last',
                 'smf30hvo': 'last',
                 # io activity
                 'smf30inp': 'sum', 'smf30tep': 'sum', 'smf30tpt': 'sum', 'smf30tgt': 'sum', 'smf30tcn': 'sum',
                 'smf30trr': 'sum', 'smf30aic': 'sum', 'smf30aid': 'sum', 'smf30aiw': 'sum', 'smf30ais': 'sum',
                 'smf30eic': 'sum', 'smf30eid': 'sum', 'smf30eiw': 'sum', 'smf30eis': 'sum', 'smf30tex': 'sum',
                 'smf30das': 'sum',
                 # Performance section
                 'smf30srv': 'sum', 'smf30csu': 'sum', 'smf30srb': 'sum', 'smf30io': 'sum', 'smf30mso': 'sum',
                 'smf30tat': 'sum', 'smf30sus': agg_next, 'smf30res': 'sum', 'smf30trs': 'sum', 'smf30eta': 'sum',
                 'smf30esu': 'sum', 'smf30etc': 'sum', 'smf30jqt': 'sum', 'smf30rqt': 'sum', 'smf30hqt': 'sum',
                 'smf30sqt': 'sum', 'smf30msc': agg_next, 'smf30cpc': agg_next, 'smf30loc': agg_next,
                 'smf30src': agg_next, 'smf30znf': agg_next, 'smf30snf': agg_next, 'smf30srv_l': 'sum',
                 'smf30csu_l': 'sum', 'smf30srb_l': 'sum', 'smf30io_l': 'sum', 'smf30mso_l': 'sum', 'smf30esu_l': 'sum',
                 'smf30_capacity_change_cnt': 'sum', 'smf30_rctpcpua_actual': agg_next,
                 'smf30_rctpcpua_nominal': agg_next, 'smf30_rctpcpua_scaling_factor': agg_next,
                 'smf30_capacity_adjustment_ind': agg_next, 'smf30_rmctadjn_nominal': agg_next,
                 # Process Accounting section
                 'smf30cpt': 'sum', 'smf30cps': 'sum', 'smf30icu': 'sum', 'smf30isb': 'sum', 'smf30jvu': 'sum',
                 'smf30ivu': 'sum', 'smf30jva': 'sum', 'smf30iva': 'sum', 'smf30iip': 'sum', 'smf30rct': 'sum',
                 'smf30hpt': 'sum', 'smf30csc': 'sum', 'smf30dmi': 'sum', 'smf30dmo': 'sum', 'smf30asr': 'sum',
                 'smf30enc': 'sum', 'smf30det': 'sum', 'smf30cep': 'sum', 'ziipboost_active': 'max',
                 'speedboost_active': 'max', 'boostclass': agg_boost_class, 'smf30_time_on_ifa': 'sum',
                 'smf30_enclave_time_on_ifa': 'sum', 'smf30_dep_enclave_time_on_ifa': 'sum',
                 'smf30_time_ifa_on_cp': 'sum', 'smf30_enclave_time_ifa_on_cp': 'sum',
                 'smf30_dep_enclave_time_ifa_on_cp': 'sum', 'smf30cepi': 'sum', 'smf30_enclave_time_on_ziip': 'sum',
                 'smf30_depenc_time_on_ziip': 'sum', 'smf30_time_ziip_on_cp': 'sum', 'smf30_enclave_time_ziip_on_cp': 'sum',
                 'smf30_depenc_time_ziip_on_cp': 'sum', 'smf30_enclave_time_ziip_qual': 'sum',
                 'smf30_depenc_time_ziip_qual': 'sum', 'smf30_time_java_on_ziip': 'sum',
                 'smf30_enclave_time_java_on_ziip': 'sum', 'smf30_depenc_time_java_on_ziip': 'sum',
                 'smf30_time_java_on_cp': 'sum', 'smf30_enclave_time_java_on_cp': 'sum',
                 'smf30_depenc_time_java_on_cp': 'sum', 'smf30crp': 'sum', 'smf30icu_step_term': 'sum',
                 'smf30icu_step_init': 'sum', 'smf30isb_step_term': 'sum', 'smf30isb_step_init': 'sum',
                 'smf30_missed_smf30blk': 'sum', 'smf30_missed_smf30dct': 'sum',
                 'smf30_highest_task_cpu_percent': agg_tolist, 'smf30_highest_task_cpu_program': agg_tolist,
                 'smf30_boostinfo': 'last', 'smf30cas_flag': 'last',
                 # Storage and Paging section
                 'smf30pgi': 'sum', 'smf30pgo': 'sum', 'smf30cpm': 'sum', 'smf30nsw': 'sum', 'smf30psi': 'sum',
                 'smf30pso': 'sum', 'smf30vpi': 'sum', 'smf30vpo': 'sum', 'smf30vpr': 'sum', 'smf30cpi': 'sum',
                 'smf30hpi': 'sum', 'smf30lpi': 'sum', 'smf30hpo': 'sum', 'smf30pst': 'sum', 'smf30psc': 'sum',
                 'smf30pie': 'sum', 'smf30poe': 'sum', 'smf30bia': 'sum', 'smf30boa': 'sum', 'smf30bie': 'sum',
                 'smf30boe': 'sum', 'smf30kia': 'sum', 'smf30koa': 'sum', 'smf30kie': 'sum', 'smf30koe': 'sum',
                 'smf30psf': 'sum', 'smf30pai': 'sum', 'smf30pei': 'sum', 'smf30ers': 'sum', 'smf30hvr': 'max',
                 'smf30hva': 'max', 'smf30tih': 'sum', 'smf30numberofdataspaceshwm': 'max',
                 'smf30userdataspacecreatereqcount': 'sum', 'smf30_dmemrequested2g': 'sum',
                 'smf30_dmemminrequested2g': 'sum','smf30_dmemassigned2g': 'sum', 'smf30_dmemnuminuseas2g': 'sum',
                 'smf30_dmemnuminuseasfixed1m': 'sum', 'smf30_dmemnuminuseaspageable1m': 'sum',
                 'smf30_dmemnuminuseas4k': 'sum', 'smf30_dmemnuminuseasdattables': 'sum',
                 'smf30_dmemnuminuseas4khwm': 'max', 'smf30_dmemnuminuseaspageable1mhwm': 'max',
                 'smf30_dmemnuminuseasfixed1mhwm': 'max', 'smf30_dmemnuminuseas2ghwm': 'max',
                 'smf30_dmemnuminuseasdattableshwm': 'max', 'smf30_dmemnuminusehwm': 'max',
                 'smf30_dmemnum2gfailed': 'sum', 'smf30_dmemnum1mfailed': 'sum', 'smf30_dmemnum4kfailed': 'sum',
                 'smf30_numinuseas2ghwm': 'max','smf30_num2gfailed': 'sum', 'smf30_obtainshomespace': 'sum',
                 'smf30_iarv64obtainshomespace': 'sum', 'smf30_framesfirstreferencebacking': 'sum',
                 'smf30_sumreal1m': 'sum', 'smf30_sumsquaresreal1m':agg_hex_sum, 'smf30_numsamples': 'sum',
                 'smf30_hwmhvreal1m': 'sum',
                 # operator section
                 'smf30pdm': 'sum', 'smf30prd': 'sum', 'smf30ptm': 'sum', 'smf30tpr': 'sum', 'smf30mtm': 'sum',
                 'smf30msr': 'sum', 'consumed_msu': 'mean'}
tbls = {'smf30_id': Smf30Id,
        'smf30_6': Smf306,
        'smf30_ura': Smf30Ura,
        'smf30_prf': Smf30Prf,
        'smf30_cas': Smf30Cas,
        'smf30_sap': Smf30Sap,
        'smf30_ops': Smf30Ops,
        'smf30_exp': Smf30Exp,
        'smf30_op': Smf30Op,
        'smf30_ud': Smf30Ud,
        'smf30_uss': Smf30Uss}
tbls_da = {'smf30_id': Smf30IdDa,
           'smf30_6': Smf306Da,
           'smf30_ura': Smf30UraDa,
           'smf30_prf': Smf30PrfDa,
           'smf30_cas': Smf30CasDa,
           'smf30_sap': Smf30SapDa,
           'smf30_ops': Smf30OpsDa,
           'smf30_exp': Smf30ExpDa,
           'smf30_op': Smf30OpDa,
           'smf30_ud': Smf30UdDa,
           'smf30_uss': Smf30UssDa}
tbls_hr = {'smf30_id': Smf30IdHr,
           'smf30_6': Smf306Hr,
           'smf30_ura': Smf30UraHr,
           'smf30_prf': Smf30PrfHr,
           'smf30_cas': Smf30CasHr,
           'smf30_sap': Smf30SapHr,
           'smf30_ops': Smf30OpsHr,
           'smf30_exp': Smf30ExpHr,
           'smf30_op': Smf30OpHr,
           'smf30_ud': Smf30UdHr,
           'smf30_uss': Smf30UssHr}
tblnames = {'smf30_id': 'smf30_id',
            'smf30_6': 'smf30_6',
            'smf30_ura': 'smf30_ura',
            'smf30_prf': 'smf30_prf',
            'smf30_cas': 'smf30_cas',
            'smf30_sap': 'smf30_sap',
            'smf30_ops': 'smf30_ops',
            'smf30_exp': 'smf30_exp',
            'smf30_op': 'smf30_op',
            'smf30_ud': 'smf30_ud',
            'smf30_uss': 'smf30_uss'}
tblnames_da = {'smf30_id': 'smf30_id_da',
               'smf30_6': 'smf30_6_da',
               'smf30_ura': 'smf30_ura_da',
               'smf30_prf': 'smf30_prf_da',
               'smf30_cas': 'smf30_cas_da',
               'smf30_sap': 'smf30_sap_da',
               'smf30_ops': 'smf30_ops_da',
               'smf30_exp': 'smf30_exp_da',
               'smf30_op': 'smf30_op_da',
               'smf30_ud': 'smf30_ud_da',
               'smf30_uss': 'smf30_uss_da'}
tblnames_hr = {'smf30_id': 'smf30_id_hr',
               'smf30_6': 'smf30_6_hr',
               'smf30_ura': 'smf30_ura_hr',
               'smf30_prf': 'smf30_prf_hr',
               'smf30_cas': 'smf30_cas_hr',
               'smf30_sap': 'smf30_sap_hr',
               'smf30_ops': 'smf30_ops_hr',
               'smf30_exp': 'smf30_exp_hr',
               'smf30_op': 'smf30_op_hr',
               'smf30_ud': 'smf30_ud_hr',
               'smf30_uss': 'smf30_uss_hr'}
tbldict = {'hourly':{'core': 'smf30_id_hr',
                     'core6': 'smf30_6_hr',
                     'ura': 'smf30_ura_hr',
                     'prf': 'smf30_prf_hr',
                     'cas': 'smf30_cas_hr',
                     'sap': 'smf30_sap_hr',
                     'ops': 'smf30_ops_hr',
                     'exp': 'smf30_exp_hr',
                     'op': 'smf30_op_hr',
                     'ud': 'smf30_ud_hr',
                     'uss': 'smf30_uss_hr'},
           'daily':{'core': 'smf30_id_da',
                    'core6': 'smf30_6_da',
                    'ura': 'smf30_ura_da',
                    'prf': 'smf30_prf_da',
                    'cas': 'smf30_cas_da',
                    'sap': 'smf30_sap_da',
                    'ops': 'smf30_ops_da',
                    'exp': 'smf30_exp_da',
                    'op': 'smf30_op_da',
                    'ud': 'smf30_ud_da',
                    'uss': 'smf30_uss_da'},
           }
int_dtypedict = create_int_dtypedict(tbls)

def sum_30db(db_engines: dict, db_session: Session, summary_level: str, start_time_str: str, end_time_str: str,
             partitions_scheme: str, db_driver: str = 'postgresql+psycopg2') -> UploadResult:
    """Summarize Smf30 database.

    Args:
        db_engines: A dictionary of all the db_engines in the database.
        db_session: SQLAlchemy session.
        summary_level: Summary level of data (hourly, daily).
        start_time_str: Start time of summary.
        end_time_str: End time of summary.
        partitions_scheme: Partitions scheme.
        db_driver: Db driver is used to connect to the database.

    Returns:
        A NamedTuple including the insert dictionary, total elapsed time of the upload and the return code.
    """
    get_list_max = np.vectorize(list_max, otypes=[object])
    get_v_index = np.vectorize(v_index, otypes=[object])
    get_list_loc = np.vectorize(list_loc, otypes=[object])
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

    insert_dict = {'core': 0, 'core6': 0, 'ura': 0, 'prf': 0, 'cas': 0, 'uss': 0, 'exp': 0, 'sap': 0, 'op': 0,
                   'ops': 0, 'ud': 0}
    summary_class = {'hourly': tbls_hr, 'daily': tbls_da}
    summary_tblname = {'hourly': tblnames_hr, 'daily': tblnames_da}
    summary_engine = {'hourly': '30.hourly', 'daily': '30.daily'}



    result_list = []

    st = time.time()
    # session start
    current_time = dt.datetime.now()

    #sum hr & da tbls
    # Summing up Smf30Id
    df_core_list = []
    null_column_list = []
    core_stmt = select(Smf30Id).where(Smf30Id.datetime.between(start, end))
    if summary_level == 'hourly':
        agg_core = agg_core_hr
    else:
        agg_core = agg_core_da
    for part in partitions_range:
        df_core = pd.read_sql(core_stmt, db_engines[f'30.{part}'])
        if not df_core.empty:
            df_core['date'] = df_core['datetime'].dt.date
            df_core_list.append(df_core)
            null_columns = df_core.columns[df_core.isna().all()].tolist()
            for col in null_columns:
                if col not in null_column_list:
                    null_column_list.append(col)
    if len(df_core_list) > 0:
        df_cores = pd.concat([df.dropna(axis=1, how='all') for df in df_core_list])
        if len(null_column_list) > 0:
            new_cols = df_cores.columns.tolist()
            for col in null_column_list:
                if col not in new_cols:
                    new_cols.append(col)
            df_cores = df_cores.reindex(columns=new_cols)
        df_core_sum = df_cores.groupby(
            [col.name for col in summary_class[summary_level]['smf30_id'].__table__.primary_key.columns.values()]).agg(
            agg_core).reset_index()
        if 'date' not in df_core_sum.columns:
            df_core_sum['date'] = df_core_sum['datetime'].dt.date
            df_core_sum['consumed_msu'] = df_core_sum['cpu_total'] * 16 * df_core_sum['smf30_rctpcpua_scaling_factor'] / \
                                          df_core_sum['smf30_rctpcpua_actual']
        df_core_sum['last_update_time'] = current_time
        insert_dict['core'] = df_upsert(db_driver, db_engines[summary_engine[summary_level]], db_session,
                                        df_core_sum[summary_class[summary_level]['smf30_id'].__table__.columns.keys()],
                                        summary_tblname[summary_level]['smf30_id'],
                                        summary_class[summary_level]['smf30_id'], 'smf30',
                                        [col.name for col in summary_class[summary_level][
                                            'smf30_id'].__table__.primary_key.columns.values()],
                                        int_dtypedict['smf30_id'], shard_id=summary_engine[summary_level]
                                        )

    insert_dict['prf'] = sum_up_by_partition(tbls['smf30_prf'], summary_class[summary_level]['smf30_prf'],
                                             summary_tblname[summary_level]['smf30_prf'],
                                             start, end, current_time, agg_prf, int_dtypedict['smf30_prf'],
                                             partitions_scheme, summary_engine[summary_level],
                                             db_engines,'30', 'smf30', db_session, db_driver)

    insert_dict['ura']  = sum_up_by_partition(tbls['smf30_ura'], summary_class[summary_level]['smf30_ura'],
                                              summary_tblname[summary_level]['smf30_ura'],
                                              start, end, current_time, agg_ura, int_dtypedict['smf30_ura'],
                                              partitions_scheme, summary_engine[summary_level],
                                              db_engines,'30', 'smf30', db_session, db_driver)

    # Summing up Smf30Cas
    df_cas_list = []
    null_column_list = []
    cas_stmt = select(Smf30Cas).where(Smf30Cas.datetime.between(start, end))
    for part in partitions_range:
        df_cas = pd.read_sql(cas_stmt, db_engines[f'30.{part}'])
        if not df_cas.empty:
            df_cas['date'] = df_cas['datetime'].dt.date
            df_cas_list.append(df_cas)
            null_columns = df_cas.columns[df_cas.isna().all()].tolist()
            for col in null_columns:
                if col not in null_column_list:
                    null_column_list.append(col)
    if len(df_cas_list) > 0:
        df_cass = pd.concat([df.dropna(axis=1, how='all') for df in df_cas_list])
        if len(null_column_list) > 0:
            new_cols = df_cass.columns.tolist()
            for col in null_column_list:
                if col not in new_cols:
                    new_cols.append(col)
            df_cass = df_cass.reindex(columns=new_cols)
        df_cas_sum = df_cass.groupby(
            [col.name for col in summary_class[summary_level]['smf30_cas'].__table__.primary_key.columns.values()]).agg(
            agg_cas).reset_index()
        if 'date' not in df_cas_sum.columns:
            df_cas_sum['date'] = df_cas_sum['datetime'].dt.date
        df_cas_sum['last_update_time'] = current_time
        df_cas_sum['percent_max_idx'] = get_v_index(df_cas_sum['smf30_highest_task_cpu_percent'])
        df_cas_sum['smf30_highest_task_cpu_program'] = get_list_loc(df_cas_sum['smf30_highest_task_cpu_program'],
                                                                    df_cas_sum['percent_max_idx'])
        df_cas_sum['smf30_highest_task_cpu_percent'] = get_list_max(df_cas_sum['smf30_highest_task_cpu_percent'])
        insert_dict['cas'] = df_upsert(db_driver, db_engines[summary_engine[summary_level]], db_session,
                                       df_cas_sum[summary_class[summary_level]['smf30_cas'].__table__.columns.keys()],
                                       summary_tblname[summary_level]['smf30_cas'],
                                       summary_class[summary_level]['smf30_cas'], 'smf30',
                                       [col.name for col in summary_class[summary_level]['smf30_cas'].__table__.primary_key.columns.values()],
                                       int_dtypedict['smf30_cas'], shard_id=summary_engine[summary_level]
                                      )

    # Summing up Smf30Sap
    df_sap_list = []
    null_column_list = []
    sap_stmt = select(Smf30Sap).where(Smf30Sap.datetime.between(start, end))
    for part in partitions_range:
        df_sap = pd.read_sql(sap_stmt, db_engines[f'30.{part}'])
        if not df_sap.empty:
            df_sap['date'] = df_sap['datetime'].dt.date
            df_sap_list.append(df_sap)
            null_columns = df_sap.columns[df_sap.isna().all()].tolist()
            for col in null_columns:
                if col not in null_column_list:
                    null_column_list.append(col)

    if len(df_sap_list) > 0:
        df_saps = pd.concat([df.dropna(axis=1, how='all') for df in df_sap_list])

        if len(null_column_list) > 0:
            new_cols = df_saps.columns.tolist()
            for col in null_column_list:
                if col not in new_cols:
                    new_cols.append(col)
            df_saps = df_saps.reindex(columns=new_cols)

        # if 'date' not in df_saps.columns:
        #     df_saps['date'] = df_saps['datetime'].dt.date

        df_sap_sum = df_saps.groupby(
            [col.name for col in
             summary_class[summary_level]['smf30_sap'].__table__.primary_key.columns.values()]).agg(
             dict((k, v) for k, v in agg_sap.items() if k in
                 summary_class[summary_level]['smf30_sap'].__table__.columns.keys())).reset_index()
        if 'date' not in df_sap_sum.columns:
            df_sap_sum['date'] = df_sap_sum['datetime'].dt.date

        df_sap_sum['last_update_time'] = current_time
        insert_dict['sap'] = df_upsert(db_driver, db_engines[summary_engine[summary_level]], db_session,
                                       df_sap_sum[summary_class[summary_level]['smf30_sap'].__table__.columns.keys()],
                                       summary_tblname[summary_level]['smf30_sap'],
                                       summary_class[summary_level]['smf30_sap'], 'smf30',
                                       [col.name for col in summary_class[summary_level]['smf30_sap'].__table__.primary_key.columns.values()],
                                       int_dtypedict['smf30_sap'], shard_id=summary_engine[summary_level]
                                      )

    # Summing up Smf30Uss
    insert_dict['uss'] = sum_up_by_partition(tbls['smf30_uss'], summary_class[summary_level]['smf30_uss'],
                                             summary_tblname[summary_level]['smf30_uss'],
                                             start, end, current_time, agg_uss, int_dtypedict['smf30_uss'],
                                             partitions_scheme, summary_engine[summary_level],
                                             db_engines, '30', 'smf30', db_session, db_driver)

    # Summing up Smf30Exp
    insert_dict['exp'] = sum_up_by_partition(tbls['smf30_exp'], summary_class[summary_level]['smf30_exp'],
                                             summary_tblname[summary_level]['smf30_exp'],
                                             start, end, current_time, agg_exp, int_dtypedict['smf30_exp'],
                                             partitions_scheme, summary_engine[summary_level],
                                             db_engines, '30','smf30', db_session, db_driver)

    # Summing up Smf30Ops
    insert_dict['ops'] = sum_up_by_partition(tbls['smf30_ops'], summary_class[summary_level]['smf30_ops'],
                                             summary_tblname[summary_level]['smf30_ops'],
                                             start, end, current_time, agg_ops, int_dtypedict['smf30_ops'],
                                             partitions_scheme, summary_engine[summary_level],
                                             db_engines,'30', 'smf30', db_session, db_driver)

    # Summing up Smf30Op
    insert_dict['op'] = sum_up_by_partition(tbls['smf30_op'], summary_class[summary_level]['smf30_op'],
                                            summary_tblname[summary_level]['smf30_op'],
                                            start, end, current_time, agg_op, int_dtypedict['smf30_op'],
                                            partitions_scheme, summary_engine[summary_level],
                                            db_engines,'30', 'smf30', db_session, db_driver)

    # Summing up Smf30Ud
    insert_dict['ud'] = sum_up_by_partition(tbls['smf30_ud'], summary_class[summary_level]['smf30_ud'],
                                            summary_tblname[summary_level]['smf30_ud'],
                                            start, end, current_time, agg_ud, int_dtypedict['smf30_ud'],
                                            partitions_scheme, summary_engine[summary_level],
                                            db_engines,'30', 'smf30', db_session, db_driver)

    # Start process subtype 6
    smf306_stmt = select(Smf306).where(Smf306.datetime.between(start, end))
    df_smf306_list = []
    null_column_list = []
    if summary_level == 'hourly':
        agg_smf306 = agg_smf306_hr
    else:
        agg_smf306 = agg_smf306_da
    for part in partitions_range:
        df_smf306 = pd.read_sql(smf306_stmt, db_engines[f'30.{part}'])
        if not df_smf306.empty:
            df_smf306['date'] = df_smf306['datetime'].dt.date
            df_smf306_list.append(df_smf306)
            null_columns = df_smf306.columns[df_smf306.isna().all()].tolist()
            for col in null_columns:
                if col not in null_column_list:
                    null_column_list.append(col)
    if len(df_smf306_list) > 0:
        df_smf306s = pd.concat([df.dropna(axis=1, how='all') for df in df_smf306_list])
        if len(null_column_list) > 0:
            new_cols = df_smf306s.columns.tolist()
            for col in null_column_list:
                if col not in new_cols:
                    new_cols.append(col)
            df_smf306s = df_smf306s.reindex(columns=new_cols)
        df_smf306_sum = df_smf306s.groupby(
            [col.name for col in summary_class[summary_level]['smf30_6'].__table__.primary_key.columns.values()]).agg(
            agg_smf306).copy().reset_index()
        if 'date' not in df_smf306_sum.columns:
            df_smf306_sum['date'] = df_smf306_sum['datetime'].dt.date
            df_smf306_sum['consumed_msu'] = df_smf306_sum['cpu_total'] * 16 * df_smf306_sum[
                'smf30_rctpcpua_scaling_factor'] / df_smf306_sum['smf30_rctpcpua_actual']
        df_smf306_sum['last_update_time'] = current_time
        df_smf306_sum['percent_max_idx'] = get_v_index(df_smf306_sum['smf30_highest_task_cpu_percent'])
        df_smf306_sum['smf30_highest_task_cpu_program'] = get_list_loc(
            df_smf306_sum['smf30_highest_task_cpu_program'], df_smf306_sum['percent_max_idx'])
        df_smf306_sum['smf30_highest_task_cpu_percent'] = get_list_max(
            df_smf306_sum['smf30_highest_task_cpu_percent'])
        insert_dict['core6'] = df_upsert(db_driver, db_engines[summary_engine[summary_level]], db_session,
                                          df_smf306_sum[summary_class[summary_level]['smf30_6'].__table__.columns.keys()],
                                          summary_tblname[summary_level]['smf30_6'],
                                          summary_class[summary_level]['smf30_6'], 'smf30',
                                          [col.name for col in summary_class[summary_level][
                                              'smf30_6'].__table__.primary_key.columns.values()],
                                          int_dtypedict['smf30_6'], shard_id=summary_engine[summary_level]
                                          )

    result_list.append({tbldict[summary_level][k]:v for k,v in insert_dict.items() if k in tbldict[summary_level].keys()})

    et = time.time()  # get the end time
    # get the execution time
    elapsed_time = (et - st) / 60
    print(f'Execution time ({summary_level}):', elapsed_time, 'minutes.')

    overall_et = time.time()
    overall_elapsed_time = (overall_et - overall_st) / 60
    return UploadResult(result_list, overall_elapsed_time, SUCCESS)

