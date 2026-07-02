from typing import Union

import click
import numpy as np
import pandas as pd
import tabulate as tb

from smf2db.api.report_util import convert_bi, format_s2hr, extractKBits
from smf2db.api.util import (setdatetime, setwkl, substr_x, ebcdic2ascii, to_datetime,
                             getjobclass, cal_tcb_time, cal_srb_time, cal_msu, cal_duration, hex2int,
                             create_dtypedict, is_bit_set, converttolist)
from smf2db.db_models.smf30_model import (Smf30Id, Smf30Ura, Smf30Prf, Smf30Cas, Smf30Sap, Smf30Ops, Smf30Exp, Smf30Op,
                                          Smf30Ud, Smf30Uss, Smf306)

DB_30 = "db_30"
tb.PRESERVE_WHITESPACE = True
col_dict = {'ura': ['smf30inp', 'smf30tep', 'smf30tpt', 'smf30tgt', 'smf30tcn', 'smf30trr', 'smf30aic', 'smf30aid',
                    'smf30aiw', 'smf30ais', 'smf30eic', 'smf30eid', 'smf30eiw', 'smf30eis', 'smf30tex', 'smf30das'],
            'prf': ['smf30srv', 'smf30csu', 'smf30srb', 'smf30io', 'smf30mso', 'smf30eta', 'smf30esu', 'smf30etc',
                    'smf30jqt', 'smf30rqt', 'smf30hqt', 'smf30sqt', 'smf30srv_l', 'smf30csu_l', 'smf30srb_l',
                    'smf30io_l', 'smf30mso_l', 'smf30esu_l', 'smf30_capacity_change_cnt'],
            'cas': ['smf30cpt', 'smf30cps', 'smf30icu', 'smf30isb', 'smf30jvu', 'smf30ivu', 'smf30jva', 'smf30iva',
                    'smf30iip', 'smf30rct', 'smf30hpt', 'smf30csc', 'smf30dmi', 'smf30dmo', 'smf30asr', 'smf30enc',
                    'smf30det', 'smf30cep', 'smf30_time_on_ifa', 'smf30_enclave_time_on_ifa',
                    'smf30_dep_enclave_time_on_ifa', 'smf30_time_ifa_on_cp', 'smf30_enclave_time_ifa_on_cp',
                    'smf30_dep_enclave_time_ifa_on_cp', 'smf30cepi', 'smf30_time_on_ziip', 'smf30_enclave_time_on_ziip',
                    'smf30_depenc_time_on_ziip', 'smf30_time_ziip_on_cp', 'smf30_enclave_time_ziip_on_cp',
                    'smf30_depenc_time_ziip_on_cp', 'smf30_enclave_time_ziip_qual', 'smf30_depenc_time_ziip_qual',
                    'smf30crp', 'smf30_time_java_on_ziip', 'smf30_enclave_time_java_on_ziip',
                    'smf30_depenc_time_java_on_ziip', 'smf30_time_java_on_cp', 'smf30_enclave_time_java_on_cp',
                    'smf30_depenc_time_java_on_cp', 'smf30icu_step_term', 'smf30icu_step_init', 'smf30isb_step_term',
                    'smf30isb_step_init', 'smf30_missed_smf30blk', 'smf30_missed_smf30dct'],
            'sap': ['smf30pgi', 'smf30pgo', 'smf30cpm', 'smf30nsw', 'smf30psi', 'smf30pso', 'smf30vpi', 'smf30vpo',
                    'smf30vpr', 'smf30cpi', 'smf30hpi', 'smf30lpi', 'smf30hpo', 'smf30pst', 'smf30psc', 'smf30pie',
                    'smf30poe', 'smf30bia', 'smf30boa', 'smf30bie', 'smf30boe', 'smf30kia', 'smf30koa', 'smf30kie',
                    'smf30koe', 'smf30psf', 'smf30pai', 'smf30pei', 'smf30ers', 'smf30tih',
                    'smf30userdataspacecreatereqcount'],
            'ops': ['smf30pdm', 'smf30prd', 'smf30ptm', 'smf30tpr', 'smf30mtm', 'smf30msr']}
cur_dict = {'ops': [],
            'ura': [],
            'sap': ['smf30hvr', 'smf30hva', 'smf30numberofdataspaceshwm'],
            'cas': ['ziipboost_active', 'speedboost_active', 'boostclass', 'smf30_highest_task_cpu_percent',
                    'smf30_highest_task_cpu_program'],
            'prf': ['smf30tat', 'smf30res', 'smf30trs', 'smf30msc', 'smf30loc', 'smf30znf', 'smf30snf']}
tbls = {'id': Smf30Id,
        '6': Smf306,
        'ura': Smf30Ura,
        'prf': Smf30Prf,
        'cas': Smf30Cas,
        'sap': Smf30Sap,
        'ops': Smf30Ops,
        'exp': Smf30Exp,
        'op': Smf30Op,
        'ud': Smf30Ud,
        'uss': Smf30Uss}
tblnames = {'id': 'smf30_id',
            '6': 'smf30_6',
            'ura': 'smf30_ura',
            'prf': 'smf30_prf',
            'cas': 'smf30_cas',
            'sap': 'smf30_sap',
            'ops': 'smf30_ops',
            'exp': 'smf30_exp',
            'op': 'smf30_op',
            'ud': 'smf30_ud',
            'uss': 'smf30_uss'}
dtypedict = create_dtypedict(tbls)


def build_df_core(df: pd.DataFrame, df_id: pd.DataFrame) -> pd.DataFrame:
    """Build the dataframe for Core Table hich will be uploaded to smf30_id table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_id: The dataframe of the Subsystem Section and Identification Section.

    Returns:
        The dataframe for the smf30 Core Table which contains Subsystem Section and Identification section.
    """
    hex_2_int = np.vectorize(hex2int)
    substr = np.vectorize(substr_x)
    tcb_time = np.vectorize(cal_tcb_time)
    srb_time = np.vectorize(cal_srb_time)
    consumed_msu = np.vectorize(cal_msu)
    set_wkl = np.vectorize(setwkl)
    if 'smf30cmp' in df.columns:
        df_core = pd.concat([df_id[df_id.index.get_level_values('no_smf30cas') == False],
                               df[df.index.get_level_values('no_smf30cas') == False]['smf30cmp'].apply(
                                   pd.Series)[['smf30scc', 'smf30sti', 'smf30arc']],
                               df[df.index.get_level_values('no_smf30cas') == False]['smf30ura'].apply(
                                   pd.Series)[['smf30tex']],
                               df[df.index.get_level_values('no_smf30cas') == False]['smf30prf'].apply(
                                   pd.Series)[['smf30scn', 'smf30_rctpcpua_actual', 'smf30_rctpcpua_nominal',
                                               'smf30_rctpcpua_scaling_factor', 'smf30_capacity_adjustment_ind',
                                               'smf30_rmctadjn_nominal', 'smf30cpc', 'smf30csu_l', 'smf30sus',
                                               'smf30src',
                                               'smf30srb_l']],
                               df[df.index.get_level_values('no_smf30cas') == False]['smf30sap'].apply(
                                   pd.Series)[
                                   ['smf30arb', 'smf30ear', 'smf30urb', 'smf30eur', 'smf30hvo', 'smf30pgi', 'smf30pgo',
                                    'smf30nsw']],
                               df[df.index.get_level_values('no_smf30cas') == False]['smf30cas'].apply(
                                   pd.Series)[
                                   ['smf30cpt', 'smf30cps', 'smf30hpt', 'smf30iip', 'smf30rct', 'smf30icu_step_term',
                                    'smf30icu_step_init', 'smf30isb_step_term', 'smf30isb_step_init',
                                    'smf30_time_on_ziip']]],
                              axis=1)
    elif 'smf30cas' in df.columns:
        df_core = pd.concat([df_id[df_id.index.get_level_values('no_smf30cas') == False],
                               df[df.index.get_level_values('no_smf30cas') == False]['smf30ura'].apply(
                                   pd.Series)[['smf30tex']],
                               df[df.index.get_level_values('no_smf30cas') == False]['smf30prf'].apply(
                                   pd.Series)[['smf30scn', 'smf30_rctpcpua_actual', 'smf30_rctpcpua_nominal',
                                               'smf30_rctpcpua_scaling_factor', 'smf30_capacity_adjustment_ind',
                                               'smf30_rmctadjn_nominal', 'smf30cpc', 'smf30csu_l', 'smf30sus',
                                               'smf30src', 'smf30srb_l']],
                               df[df.index.get_level_values('no_smf30cas') == False]['smf30sap'].apply(
                                   pd.Series)[
                                   ['smf30arb', 'smf30ear', 'smf30urb', 'smf30eur', 'smf30hvo', 'smf30pgi', 'smf30pgo',
                                    'smf30nsw']],
                               df[df.index.get_level_values('no_smf30cas') == False]['smf30cas'].apply(
                                   pd.Series)[
                                   ['smf30cpt', 'smf30cps', 'smf30hpt', 'smf30iip', 'smf30rct', 'smf30icu_step_term',
                                    'smf30icu_step_init', 'smf30isb_step_term', 'smf30isb_step_init',
                                    'smf30_time_on_ziip']]],
                              axis=1)
        if df_core.shape[0] > 0:
            df_core['smf30scc'] = np.nan
            df_core['smf30sti'] = np.nan
            df_core['smf30arc'] = np.nan
    else:  # empty df_core
        df_core = pd.DataFrame(columns=Smf30Id.__table__.columns.keys())

    if df_core.shape[0] > 0:
        df_core['smf30_capacity_adjustment_ind'] = hex_2_int(df_core['smf30_capacity_adjustment_ind'])
        df_core['smf30cpt'] = pd.to_timedelta(df_core['smf30cpt']) / np.timedelta64(1, 's')
        df_core['smf30cps'] = pd.to_timedelta(df_core['smf30cps']) / np.timedelta64(1, 's')
        df_core['smf30iip'] = pd.to_timedelta(df_core['smf30iip']) / np.timedelta64(1, 's')
        df_core['smf30rct'] = pd.to_timedelta(df_core['smf30rct']) / np.timedelta64(1, 's')
        df_core['smf30hpt'] = pd.to_timedelta(df_core['smf30hpt']) / np.timedelta64(1, 's')
        df_core['smf30icu_step_term'] = pd.to_timedelta(df_core['smf30icu_step_term']) / np.timedelta64(1, 's')
        df_core['smf30icu_step_init'] = pd.to_timedelta(df_core['smf30icu_step_init']) / np.timedelta64(1, 's')
        df_core['smf30isb_step_term'] = pd.to_timedelta(df_core['smf30isb_step_term']) / np.timedelta64(1, 's')
        df_core['smf30isb_step_init'] = pd.to_timedelta(df_core['smf30isb_step_init']) / np.timedelta64(1, 's')
        df_core['smf30_time_on_ziip'] = pd.to_timedelta(df_core['smf30_time_on_ziip']) / np.timedelta64(1, 's')
        df_core['smf30scc'] = substr(df_core['smf30scc'], 2)
        df_core['smf30sti'] = substr(df_core['smf30sti'], 2)
        df_core['smf30arc'] = substr(df_core['smf30arc'], 2)
        df_core['tcb_time'] = tcb_time(df_core['smf30cpt'], df_core['smf30cpc'], df_core['smf30csu_l'],
                                         df_core['smf30sus'])
        df_core['srb_time'] = srb_time(df_core['smf30cps'], df_core['smf30src'], df_core['smf30srb_l'],
                                         df_core['smf30sus'])
        df_core['cpu_total'] = (df_core['smf30cpt'] + df_core['smf30cps'] + df_core['smf30hpt'] + df_core['smf30iip']
                                + df_core['smf30rct'] + df_core['smf30icu_step_term'] + df_core['smf30icu_step_init']
                                + df_core['smf30isb_step_term'] + df_core['smf30isb_step_init'])
        df_core['consumed_msu'] = consumed_msu(df_core['smf30_rctpcpua_actual'], df_core['cpu_total'],
                                                 df_core['smf30_rctpcpua_scaling_factor'])
        df_core['wkl'] = set_wkl(df_core.index.get_level_values('smf30typ'), df_core['subSysId'],
                                   df_core['smf30pgm'],
                                   df_core['smf30scn'])
    return df_core


def build_ura(df_core_shape: tuple[int, int], df: pd.DataFrame, df_main: pd.DataFrame) -> pd.DataFrame:
    """Build the dataframe for I/O Activity Section which will be uploaded to smf30_ura table.

    Args:
        df_core_shape: The df_core dataframe shape.
        df: The master dataframe which is created from the JSON file.
        df_main: The dataframe of the Subsystem Section and Identification Section.

    Returns:
        The dataframe for the smf30 I/O Activity section.
    """
    if df_core_shape[0] > 0:
        df_ura = pd.json_normalize(df[df.index.get_level_values('no_smf30cas') == False]['smf30ura']).set_index(
            df_main.index)
        df_ura['datetime'] = df_main['datetime']
        df_ura['smf30tme'] = df_main['smf30tme']
        df_ura['smf30rdr'] = df_ura['smf30rdr'].str[2:]
        df_ura['smf30rdt'] = df_ura['smf30rdt'].str[2:]
        df_ura['smf30tcn'] = pd.to_timedelta(df_ura['smf30tcn']) / np.timedelta64(1, 's')
        df_ura['smf30dcf'] = df_ura['smf30dcf'].apply(lambda x: int(str(x), 16))
        df_ura['device_connect_time_incorrect'] = df_ura['smf30dcf'].apply(lambda x: is_bit_set(x, 8, 0))
        df_ura['dcf_incomplete'] = df_ura['smf30dcf'].apply(lambda x: is_bit_set(x, 8, 1))
        df_ura['smf30tep_inv'] = df_ura['smf30dcf'].apply(lambda x: is_bit_set(x, 8, 2))
        df_ura['smf30aic'] = pd.to_timedelta(df_ura['smf30aic']) / np.timedelta64(1, 's')
        df_ura['smf30aid'] = pd.to_timedelta(df_ura['smf30aid']) / np.timedelta64(1, 's')
        df_ura['smf30aiw'] = pd.to_timedelta(df_ura['smf30aiw']) / np.timedelta64(1, 's')
        df_ura['smf30eic'] = pd.to_timedelta(df_ura['smf30eic']) / np.timedelta64(1, 's')
        df_ura['smf30eid'] = pd.to_timedelta(df_ura['smf30eid']) / np.timedelta64(1, 's')
        df_ura['smf30eiw'] = pd.to_timedelta(df_ura['smf30eiw']) / np.timedelta64(1, 's')

    else:
        df_ura = pd.DataFrame(columns=Smf30Ura.__table__.columns.keys()
                                ).set_index(['smf30syp', 'smf30syn', 'start_interval', 'wkl', 'smf30typ',
                                             'smf30jbn', 'smf30asi', 'smf30jnm', 'smf30stn', 'gid', 'suffix'])
    return df_ura


def build_cas(df_core_shape: tuple[int, int], df: pd.DataFrame, df_main: pd.DataFrame) -> pd.DataFrame:
    """Build the dataframe for Processor Accounting Section which will be uploaded to smf30_cas table.

    Args:
        df_core_shape: The df_core dataframe shape.
        df: The master dataframe which is created from the JSON file.
        df_main: The dataframe of the Subsystem Section and Identification Section.

    Returns:
        The dataframe for the smf30 Processor Accounting section.
    """
    hex_2_int = np.vectorize(hex2int)
    convert_to_datetime = np.vectorize(to_datetime)
    if df_core_shape[0] > 0:  #'smf30cas' in df.columns:
        df_cas = pd.json_normalize(df[df.index.get_level_values('no_smf30cas') == False]['smf30cas']).set_index(
            df_main.index)
        df_cas['datetime'] = df_main['datetime']
        df_cas['smf30tme'] = df_main['smf30tme']
        df_cas['smf30tfl'] = df_cas['smf30tfl'].apply(lambda x: int(str(x), 16))
        df_cas['smf30tf2'] = df_cas['smf30tf2'].apply(lambda x: int(str(x), 16))
        df_cas['smf30t32'] = df_cas['smf30t32'].apply(lambda x: int(str(x), 16))
        df_cas['smf30t33'] = df_cas['smf30t33'].apply(lambda x: int(str(x), 16))
        if 'smf30cas_flag' not in df_cas.columns:
            df_cas['smf30cas_flag'] = np.nan
            df_cas['smf30cas_oa54589'] = np.nan
        df_cas['smf30cas_flag'] = df_cas['smf30cas_flag'].apply(lambda x: int(str(x), 16) if not pd.isna(x) else x)
        df_cas['timer_used'] = df_cas['smf30tfl'].apply(lambda x: is_bit_set(x, 16, 0))
        df_cas['smf30cpt_inv'] = df_cas['smf30tfl'].apply(lambda x: is_bit_set(x, 16, 1))
        df_cas['smf30cps_inv'] = df_cas['smf30tfl'].apply(lambda x: is_bit_set(x, 16, 2))
        df_cas['smf30jvu_inv'] = df_cas['smf30tfl'].apply(lambda x: is_bit_set(x, 16, 3))
        df_cas['smf30jva_inv'] = df_cas['smf30tfl'].apply(lambda x: is_bit_set(x, 16, 4))
        df_cas['smf30isb_inv'] = df_cas['smf30tfl'].apply(lambda x: is_bit_set(x, 16, 5))
        df_cas['smf30icu_inv'] = df_cas['smf30tfl'].apply(lambda x: is_bit_set(x, 16, 6))
        df_cas['smf30ivu_inv'] = df_cas['smf30tfl'].apply(lambda x: is_bit_set(x, 16, 7))
        df_cas['smf30iva_inv'] = df_cas['smf30tfl'].apply(lambda x: is_bit_set(x, 16, 8))
        df_cas['smf30iip_inv'] = df_cas['smf30tfl'].apply(lambda x: is_bit_set(x, 16, 9))
        df_cas['smf30hpt_inv'] = df_cas['smf30tfl'].apply(lambda x: is_bit_set(x, 16, 10))
        df_cas['smf30rct_inv'] = df_cas['smf30tfl'].apply(lambda x: is_bit_set(x, 16, 11))
        df_cas['smf30asr_inv'] = df_cas['smf30tfl'].apply(lambda x: is_bit_set(x, 16, 12))
        df_cas['smf30enc_inv'] = df_cas['smf30tfl'].apply(lambda x: is_bit_set(x, 16, 13))
        df_cas['smf30det_inv'] = df_cas['smf30tfl'].apply(lambda x: is_bit_set(x, 16, 14))
        df_cas['smf30cep_inv'] = df_cas['smf30tfl'].apply(lambda x: is_bit_set(x, 16, 15))
        df_cas['smf30cpt'] = pd.to_timedelta(df_cas['smf30cpt']) / np.timedelta64(1, 's')
        df_cas['smf30cps'] = pd.to_timedelta(df_cas['smf30cps']) / np.timedelta64(1, 's')
        df_cas['smf30icu'] = pd.to_timedelta(df_cas['smf30icu']) / np.timedelta64(1, 's')
        df_cas['smf30isb'] = pd.to_timedelta(df_cas['smf30isb']) / np.timedelta64(1, 's')
        df_cas['smf30jvu'] = pd.to_timedelta(df_cas['smf30jvu']) / np.timedelta64(1, 's')
        df_cas['smf30ivu'] = pd.to_timedelta(df_cas['smf30ivu']) / np.timedelta64(1, 's')
        df_cas['smf30jva'] = pd.to_timedelta(df_cas['smf30jva']) / np.timedelta64(1, 's')
        df_cas['smf30iva'] = pd.to_timedelta(df_cas['smf30iva']) / np.timedelta64(1, 's')
        df_cas['smf30ist'] = convert_to_datetime(df_cas['smf30ist'])
        df_cas['smf30iip'] = pd.to_timedelta(df_cas['smf30iip']) / np.timedelta64(1, 's')
        df_cas['smf30rct'] = pd.to_timedelta(df_cas['smf30rct']) / np.timedelta64(1, 's')
        df_cas['smf30hpt'] = pd.to_timedelta(df_cas['smf30hpt']) / np.timedelta64(1, 's')
        df_cas['smf30asr'] = pd.to_timedelta(df_cas['smf30asr']) / np.timedelta64(1, 's')
        df_cas['smf30enc'] = pd.to_timedelta(df_cas['smf30enc']) / np.timedelta64(1, 's')
        df_cas['smf30det'] = pd.to_timedelta(df_cas['smf30det']) / np.timedelta64(1, 's')
        df_cas['smf30cep'] = pd.to_timedelta(df_cas['smf30cep']) / np.timedelta64(1, 's')
        df_cas['smf30_time_on_ifa_f'] = df_cas['smf30tf2'].apply(lambda x: is_bit_set(x, 8, 0))
        df_cas['smf30_enclave_time_on_ifa_f'] = df_cas['smf30tf2'].apply(lambda x: is_bit_set(x, 8, 1))
        df_cas['smf30_dep_enclave_time_on_ifa_f'] = df_cas['smf30tf2'].apply(lambda x: is_bit_set(x, 8, 2))
        df_cas['smf30_time_ifa_on_cp_f'] = df_cas['smf30tf2'].apply(lambda x: is_bit_set(x, 8, 3))
        df_cas['smf30_enclave_time_ifa_on_cp_f'] = df_cas['smf30tf2'].apply(lambda x: is_bit_set(x, 8, 4))
        df_cas['smf30_dep_enclave_time_ifa_on_cp_f'] = df_cas['smf30tf2'].apply(lambda x: is_bit_set(x, 8, 5))
        df_cas['smf30_cepi_failed'] = df_cas['smf30tf2'].apply(lambda x: is_bit_set(x, 8, 6))
        df_cas['smf30crp_failed'] = df_cas['smf30tf2'].apply(lambda x: is_bit_set(x, 8, 7))
        df_cas['smf30_time_on_ziip_f'] = df_cas['smf30t32'].apply(lambda x: is_bit_set(x, 8, 0))
        df_cas['smf30_enclave_time_on_ziip_f'] = df_cas['smf30t32'].apply(lambda x: is_bit_set(x, 8, 1))
        df_cas['smf30_dep_time_on_ziip_f'] = df_cas['smf30t32'].apply(lambda x: is_bit_set(x, 8, 2))
        df_cas['smf30_time_ziip_on_cp_f'] = df_cas['smf30t32'].apply(lambda x: is_bit_set(x, 8, 3))
        df_cas['smf30_enclave_time_ziip_on_cp_f'] = df_cas['smf30t32'].apply(lambda x: is_bit_set(x, 8, 4))
        df_cas['smf30_depenc_time_ziip_on_cp_f'] = df_cas['smf30t32'].apply(lambda x: is_bit_set(x, 8, 5))
        df_cas['smf30_time_java_on_ziip_f'] = df_cas['smf30t32'].apply(lambda x: is_bit_set(x, 8, 6))
        df_cas['smf30_encalve_time_java_on_ziip_f'] = df_cas['smf30t32'].apply(lambda x: is_bit_set(x, 8, 7))
        df_cas['enclave_time_ziip_qual_f'] = df_cas['smf30t33'].apply(lambda x: is_bit_set(x, 8, 6))
        df_cas['depenc_time_ziip_qual_f'] = df_cas['smf30t33'].apply(lambda x: is_bit_set(x, 8, 7))
        df_cas['smf30_boostinfo'] = df_cas['smf30_boostinfo'].apply(lambda x: int(str(x), 16))
        df_cas['ziipboost_active'] = df_cas['smf30_boostinfo'].apply(lambda x: is_bit_set(x, 8, 0))
        df_cas['speedboost_active'] = df_cas['smf30_boostinfo'].apply(lambda x: is_bit_set(x, 8, 1))
        df_cas['boostclass'] = df_cas['smf30_boostinfo'].apply(lambda x: extractKBits(x, 8, 2, 5))
        df_cas['smf30_time_on_ifa'] = pd.to_timedelta(df_cas['smf30_time_on_ifa']) / np.timedelta64(1, 's')
        df_cas['smf30_enclave_time_on_ifa'] = (pd.to_timedelta(df_cas['smf30_enclave_time_on_ifa'])
                                               / np.timedelta64(1, 's'))
        df_cas['smf30_dep_enclave_time_on_ifa'] = (pd.to_timedelta(df_cas['smf30_dep_enclave_time_on_ifa'])
                                                   / np.timedelta64(1, 's'))
        df_cas['smf30_time_ifa_on_cp'] = pd.to_timedelta(df_cas['smf30_time_ifa_on_cp']) / np.timedelta64(1, 's')
        df_cas['smf30_enclave_time_ifa_on_cp'] = (pd.to_timedelta(df_cas['smf30_enclave_time_ifa_on_cp'])
                                                  / np.timedelta64(1, 's'))
        df_cas['smf30_dep_enclave_time_ifa_on_cp'] = (pd.to_timedelta(df_cas['smf30_dep_enclave_time_ifa_on_cp'])
                                                      / np.timedelta64(1, 's'))
        df_cas['smf30cepi'] = pd.to_timedelta(df_cas['smf30cepi']) / np.timedelta64(1, 's')
        df_cas['smf30_time_on_ziip'] = pd.to_timedelta(df_cas['smf30_time_on_ziip']) / np.timedelta64(1, 's')
        df_cas['smf30_enclave_time_on_ziip'] = (pd.to_timedelta(df_cas['smf30_enclave_time_on_ziip'])
                                               / np.timedelta64(1, 's'))
        df_cas['smf30_depenc_time_on_ziip'] = (pd.to_timedelta(df_cas['smf30_depenc_time_on_ziip'])
                                              / np.timedelta64(1, 's'))
        df_cas['smf30_time_ziip_on_cp'] = pd.to_timedelta(df_cas['smf30_time_ziip_on_cp']) / np.timedelta64(1, 's')
        df_cas['smf30_enclave_time_ziip_on_cp'] = (pd.to_timedelta(df_cas['smf30_enclave_time_ziip_on_cp'])
                                                  / np.timedelta64(1, 's'))
        df_cas['smf30_depenc_time_ziip_on_cp'] = (pd.to_timedelta(df_cas['smf30_depenc_time_ziip_on_cp'])
                                                 / np.timedelta64(1, 's'))
        df_cas['smf30_enclave_time_ziip_qual'] = (pd.to_timedelta(df_cas['smf30_enclave_time_ziip_qual'])
                                                 / np.timedelta64(1, 's'))
        df_cas['smf30_depenc_time_ziip_qual'] = (pd.to_timedelta(df_cas['smf30_depenc_time_ziip_qual'])
                                                / np.timedelta64(1, 's'))
        if 'smf30_time_java_on_ziip' in df_cas.columns:
            df_cas['smf30_time_java_on_ziip'] = (pd.to_timedelta(df_cas['smf30_time_java_on_ziip'])
                                                 / np.timedelta64(1, 's'))
            df_cas['smf30_enclave_time_java_on_ziip'] = (pd.to_timedelta(df_cas['smf30_enclave_time_java_on_ziip'])
                                                         / np.timedelta64(1, 's'))
            df_cas['smf30_depenc_time_java_on_ziip'] = (pd.to_timedelta(df_cas['smf30_depenc_time_java_on_ziip'])
                                                        / np.timedelta64(1, 's'))
            df_cas['smf30_time_java_on_cp'] = (pd.to_timedelta(df_cas['smf30_time_java_on_cp'])
                                               / np.timedelta64(1, 's'))
            df_cas['smf30_enclave_time_java_on_cp'] = (pd.to_timedelta(df_cas['smf30_enclave_time_java_on_cp'])
                                                       / np.timedelta64(1, 's'))
            df_cas['smf30_depenc_time_java_on_cp'] = (pd.to_timedelta(df_cas['smf30_depenc_time_java_on_cp'])
                                                      / np.timedelta64(1, 's'))
        df_cas['smf30crp'] = pd.to_timedelta(df_cas['smf30crp']) / np.timedelta64(1, 's')
        df_cas['smf30icu_step_term'] = pd.to_timedelta(df_cas['smf30icu_step_term']) / np.timedelta64(1, 's')
        df_cas['smf30icu_step_init'] = pd.to_timedelta(df_cas['smf30icu_step_init']) / np.timedelta64(1, 's')
        df_cas['smf30isb_step_term'] = pd.to_timedelta(df_cas['smf30isb_step_term']) / np.timedelta64(1, 's')
        df_cas['smf30isb_step_init'] = pd.to_timedelta(df_cas['smf30isb_step_init']) / np.timedelta64(1, 's')
        df_cas['smf30_missed_smf30dct'] = pd.to_timedelta(df_cas['smf30_missed_smf30dct']) / np.timedelta64(1, 's')
        df_cas['smf30cas_inelighonorpriority'] = df_cas['smf30cas_flag'].apply(lambda x: is_bit_set(x, 8, 0))
        df_cas['smf30cas_oa54589'] = hex_2_int(df_cas['smf30cas_oa54589'])
        df_cas.drop(columns=['smf30_time_on_sup', 'smf30_enclave_time_on_sup', 'smf30_depenc_time_on_sup',
                             'smf30_time_sup_on_cp', 'smf30_enclave_time_sup_on_cp', 'smf30_depenc_time_sup_on_cp',
                             'smf30_enclave_time_sup_qual', 'smf30_depenc_time_sup_qual'], inplace=True)

    else:
        df_cas = pd.DataFrame(columns=Smf30Cas.__table__.columns.keys()).set_index(
            ['smf30syp', 'smf30syn', 'start_interval', 'wkl', 'smf30typ', 'smf30jbn', 'smf30asi', 'smf30jnm',
             'smf30stn', 'gid', 'suffix'])
    return df_cas


def build_prf(df_core_shape: tuple[int, int], df: pd.DataFrame, df_main: pd.DataFrame) -> pd.DataFrame:
    """Build the dataframe for Performance Section which will be uploaded to smf30_prf table.

    Args:
        df_core_shape: The df_core dataframe shape.
        df: The master dataframe which is created from the JSON file.
        df_main: The dataframe of the Subsystem Section and Identification Section.

    Returns:
        The dataframe for the smf30 Performance section.
    """
    hex_2_int = np.vectorize(hex2int)
    if df_core_shape[0] > 0:  #'smf30prf' in df.columns:
        df_prf = pd.json_normalize(df[df.index.get_level_values('no_smf30cas') == False]['smf30prf']).set_index(
            df_main.index)
        df_prf['datetime'] = df_main['datetime']
        df_prf['smf30tme'] = df_main['smf30tme']
        df_prf['smf30pf1'] = df_prf['smf30pf1'].apply(lambda x: int(str(x), 16))
        df_prf['smf30pf2'] = df_prf['smf30pf2'].apply(lambda x: int(str(x), 16))
        df_prf['smf30inv'] = df_prf['smf30inv'].apply(lambda x: int(str(x), 16))
        df_prf['smf30acb'] = df_prf['smf30acb'].apply(lambda x: int(str(x), 16))
        df_prf['smf30_capacity_flags'] = df_prf['smf30_capacity_flags'].apply(lambda x: int(str(x), 16))
        df_prf['smf30tat'] = pd.to_timedelta(df_prf['smf30tat']) / np.timedelta64(1, 's')
        df_prf['smf30res'] = pd.to_timedelta(df_prf['smf30res']) / np.timedelta64(1, 's')
        df_prf['smf30eta'] = pd.to_timedelta(df_prf['smf30eta']) / np.timedelta64(1, 's')
        df_prf['smf30jqt'] = pd.to_timedelta(df_prf['smf30jqt']) / np.timedelta64(1, 's')
        df_prf['smf30rqt'] = pd.to_timedelta(df_prf['smf30rqt']) / np.timedelta64(1, 's')
        df_prf['smf30hqt'] = pd.to_timedelta(df_prf['smf30hqt']) / np.timedelta64(1, 's')
        df_prf['smf30sqt'] = pd.to_timedelta(df_prf['smf30sqt']) / np.timedelta64(1, 's')
        df_prf['smf30_capacity_adjustment_ind'] = hex_2_int(df_prf['smf30_capacity_adjustment_ind'])
        df_prf['smf30pfj'] = df_prf['smf30pf1'].apply(lambda x: is_bit_set(x, 8, 0))
        df_prf['smf30pfr'] = df_prf['smf30pf1'].apply(lambda x: is_bit_set(x, 8, 1))
        df_prf['smf30pff'] = df_prf['smf30pf1'].apply(lambda x: is_bit_set(x, 8, 2))
        df_prf['smf30rtr'] = df_prf['smf30pf1'].apply(lambda x: is_bit_set(x, 8, 3))
        df_prf['smf30msi'] = df_prf['smf30pf1'].apply(lambda x: is_bit_set(x, 8, 4))
        df_prf['smf30wmi'] = df_prf['smf30pf1'].apply(lambda x: is_bit_set(x, 8, 5))
        df_prf['smf30ccp'] = df_prf['smf30pf1'].apply(lambda x: is_bit_set(x, 8, 6))
        df_prf['smf30csp'] = df_prf['smf30pf1'].apply(lambda x: is_bit_set(x, 8, 7))
        df_prf['smf30asp'] = df_prf['smf30pf2'].apply(lambda x: is_bit_set(x, 8, 0))
        df_prf['smf30sme'] = df_prf['smf30pf2'].apply(lambda x: is_bit_set(x, 8, 1))
        df_prf['smf30cpr'] = df_prf['smf30pf2'].apply(lambda x: is_bit_set(x, 8, 2))
        df_prf['smf30spr'] = df_prf['smf30pf2'].apply(lambda x: is_bit_set(x, 8, 3))
        df_prf['smf30pin'] = df_prf['smf30pf2'].apply(lambda x: is_bit_set(x, 8, 4))
        df_prf['smf30crm'] = df_prf['smf30pf2'].apply(lambda x: is_bit_set(x, 8, 5))
        df_prf['smf30srv_inv'] = df_prf['smf30inv'].apply(lambda x: is_bit_set(x, 8, 0))
        df_prf['smf30csu_inv'] = df_prf['smf30inv'].apply(lambda x: is_bit_set(x, 8, 1))
        df_prf['smf30srb_inv'] = df_prf['smf30inv'].apply(lambda x: is_bit_set(x, 8, 2))
        df_prf['smf30io_inv'] = df_prf['smf30inv'].apply(lambda x: is_bit_set(x, 8, 3))
        df_prf['smf30mso_inv'] = df_prf['smf30inv'].apply(lambda x: is_bit_set(x, 8, 4))
        df_prf['smf30esu_inv'] = df_prf['smf30inv'].apply(lambda x: is_bit_set(x, 8, 5))
        df_prf['smf30_event_driven_intvl_rec'] = df_prf['smf30_capacity_flags'].apply(lambda x: is_bit_set(x, 8, 0))
        df_prf['smf30_rqsvsus_err'] = df_prf['smf30_capacity_flags'].apply(lambda x: is_bit_set(x, 8, 1))
        df_prf['smf30_capacity_data_err'] = df_prf['smf30_capacity_flags'].apply(lambda x: is_bit_set(x, 8, 2))
        df_prf['smf30_pcd_rsvd_exists'] = df_prf['smf30_capacity_flags'].apply(lambda x: is_bit_set(x, 8, 3))

    else:
        df_prf = pd.DataFrame(columns=Smf30Prf.__table__.columns.keys()).set_index(
            ['smf30syp', 'smf30syn', 'start_interval', 'wkl', 'smf30typ', 'smf30jbn', 'smf30asi', 'smf30jnm',
             'smf30stn', 'gid', 'suffix'])
    return df_prf


def build_sap(df_core_shape: tuple[int, int], df: pd.DataFrame, df_main: pd.DataFrame) -> pd.DataFrame:
    """Build the dataframe for Storage and Paging Section which will be uploaded to smf30_sap table.

    Args:
        df_core_shape: The df_core dataframe shape.
        df: The master dataframe which is created from the JSON file.
        df_main: The dataframe of the Subsystem Section and Identification Section.

    Returns:
        The dataframe for the smf30 Storage and Paging section.
    """
    if df_core_shape[0] > 0:  #'smf30sap' in df.columns:
        df_sap = pd.json_normalize(df[df.index.get_level_values('no_smf30cas') == False]['smf30sap']).set_index(
            df_main.index)
        df_sap['datetime'] = df_main['datetime']
        df_sap['smf30tme'] = df_main['smf30tme']
        if 'sm30tiu' not in df_sap.columns:
            df_sap['smf30tiu'] = np.nan
        df_sap['smf30tiu'] = np.where(df_sap['smf30tiu'] >= 4294967256, np.nan, df_sap['smf30tiu'])
        df_sap['smf30mes'] = df_sap['smf30mes'].str[2:]
        df_sap['smf30sfl'] = df_sap['smf30sfl'].apply(lambda x: int(str(x), 16))
        df_sap['smf30slm'] = df_sap['smf30slm'].apply(lambda x: int(str(x), 16))
        df_sap['smf30_raxflags'] = df_sap['smf30_raxflags'].apply(lambda x: int(str(x), 16))
        df_sap['storage_vr_specified_flg'] = df_sap['smf30sfl'].apply(lambda x: is_bit_set(x, 8, 0))
        df_sap['storage_iefusi_changed_flg'] = df_sap['smf30sfl'].apply(lambda x: is_bit_set(x, 8, 1))
        df_sap['storage_memlimit_set_flg'] = df_sap['smf30sfl'].apply(lambda x: is_bit_set(x, 8, 2))
        df_sap['storage_incomp_flg'] = df_sap['smf30sfl'].apply(lambda x: is_bit_set(x, 8, 3))
        df_sap['nohonor_iefusi_set'] = df_sap['smf30sfl'].apply(lambda x: is_bit_set(x, 8, 4))
        df_sap['rsvdhbb77b0_exists'] = df_sap['smf30sfl'].apply(lambda x: is_bit_set(x, 8, 5))
        df_sap['smf30psc'] = pd.to_timedelta(df_sap['smf30psc']) / np.timedelta64(1, 's')
        df_sap['smf30psf'] = pd.to_timedelta(df_sap['smf30psf']) / np.timedelta64(1, 's')
        df_sap['smf30ers'] = pd.to_timedelta(df_sap['smf30ers']) / np.timedelta64(1, 's')
        df_sap['sl1'] = df_sap['smf30slm'].apply(lambda x: is_bit_set(x, 8, 0))
        df_sap['sl2'] = df_sap['smf30slm'].apply(lambda x: is_bit_set(x, 8, 1))
        df_sap['sl3'] = df_sap['smf30slm'].apply(lambda x: is_bit_set(x, 8, 2))
        df_sap['sl4'] = df_sap['smf30slm'].apply(lambda x: is_bit_set(x, 8, 3))
        df_sap['sl5'] = df_sap['smf30slm'].apply(lambda x: is_bit_set(x, 8, 4))
        df_sap['sl6'] = df_sap['smf30slm'].apply(lambda x: is_bit_set(x, 8, 5))
        df_sap['sl7'] = df_sap['smf30slm'].apply(lambda x: is_bit_set(x, 8, 6))
        df_sap['sl8'] = df_sap['smf30slm'].apply(lambda x: is_bit_set(x, 8, 7))
        df_sap['smf30_userkeycommonauditenabled'] = df_sap['smf30_raxflags'].apply(lambda x: is_bit_set(x, 8, 0))
        df_sap['smf30_userkeycsausage'] = df_sap['smf30_raxflags'].apply(lambda x: is_bit_set(x, 8, 1))
        df_sap['smf30_userkeycadsusage'] = df_sap['smf30_raxflags'].apply(lambda x: is_bit_set(x, 8, 2))
        df_sap['smf30_userkeychangkeyusage'] = df_sap['smf30_raxflags'].apply(lambda x: is_bit_set(x, 8, 3))
        df_sap['smf30_userkeyrucsausage'] = df_sap['smf30_raxflags'].apply(lambda x: is_bit_set(x, 8, 4))
        df_sap['smf30_rucsaearlyusage'] = df_sap['smf30_raxflags'].apply(lambda x: is_bit_set(x, 8, 5))
        df_sap.drop(columns=['smf30pia', 'smf30poa', 'smf30arb', 'smf30ear', 'smf30urb', 'smf30eur', 'smf30hvo'], inplace=True)

    else:
        df_sap = pd.DataFrame(columns=Smf30Sap.__table__.columns.keys()).set_index(
            ['smf30syp', 'smf30syn', 'start_interval', 'wkl', 'smf30typ', 'smf30jbn', 'smf30asi', 'smf30jnm',
             'smf30stn', 'gid', 'suffix'])
    return df_sap


def build_ops(df_core_shape: tuple[int, int], df: pd.DataFrame, df_main: pd.DataFrame) -> pd.DataFrame:
    """Build the dataframe for Operator Section which will be uploaded to smf30_ops table.

    Args:
        df_core_shape: The df_core dataframe shape.
        df: The master dataframe which is created from the JSON file.
        df_main: The dataframe of the Subsystem Section and Identification Section.

    Returns:
        The dataframe for the smf30 Operator section.
    """
    if df_core_shape[0] > 0:
        if 'smf30ops' in df.columns:
            df_ops = pd.json_normalize(
                df[df.index.get_level_values('no_smf30cas') == False]['smf30ops']).set_index(
                df_main.index)
            df_ops['datetime'] = df_main['datetime']
            df_ops['smf30tme'] = df_main['smf30tme']
        else:
            ops_cols_list = ['smf30tme', 'datetime', 'smf30pdm', 'smf30prd', 'smf30ptm', 'smf30tpr', 'smf30mtm',
                             'smf30msr']
            df_ops = pd.DataFrame(columns=ops_cols_list, index=df_main.index)
            df_ops['smf30tme'] = df_main['smf30tme']
            df_ops['datetime'] = df_main['datetime']
    else:
        df_ops = pd.DataFrame(columns=Smf30Ops.__table__.columns.keys()).set_index(
            ['smf30syp', 'smf30syn', 'start_interval', 'wkl', 'smf30typ', 'smf30jbn', 'smf30asi', 'smf30jnm',
             'smf30stn', 'gid', 'suffix'])
    return df_ops


def build_uss(df: pd.DataFrame, df_id_idx: pd.Index, df_main: pd.DataFrame) -> pd.DataFrame:
    """Build the dataframe for zEDC Usage Statistics Section which will be uploaded to smf30_uss table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_id_idx: The index of the dataframe of the Subsystem Section and Identification Section.
        df_main: The dataframe of the Subsystem Section and Identification Section.

    Returns:
        The dataframe for the smf30 zEDC Usage Statistics section.
    """
    if 'smf30uss' in df.columns:
        df_uss = pd.json_normalize(df['smf30uss']).set_index(df_id_idx)
        df_uss['datetime'] = df_main['datetime']
        df_uss['smf30tme'] = df_main['smf30tme']
        df_uss['smf30_us_queuetime'] = pd.to_timedelta(df_uss['smf30_us_queuetime']) / np.timedelta64(1, 's')
        df_uss['smf30_us_exectime'] = pd.to_timedelta(df_uss['smf30_us_exectime']) / np.timedelta64(1, 's')
        drop_columns = ['smf30_us_comprreq', 'smf30_us_comprreq_prob', 'smf30_us_queuetime', 'smf30_us_exectime',
                        'smf30_us_def_uncomprin', 'smf30_us_def_comprout', 'smf30_us_inf_comprin',
                        'smf30_us_inf_decomprout']
        df_uss.dropna(subset=[column for column in list(filter(None, df_uss.index.names + df_uss.columns.values.tolist())) if column in
                    drop_columns], how='all', inplace=True)
    else:
        df_uss = pd.DataFrame(columns=Smf30Uss.__table__.columns.keys()).set_index(
            ['smf30syp', 'smf30syn', 'start_interval', 'wkl', 'smf30typ', 'smf30jbn', 'smf30asi', 'smf30jnm',
             'smf30stn', 'gid', 'suffix'])
    return df_uss


def build_exp(df: pd.DataFrame, df_id_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for Execute Channel Program (EXCP) Section which will be uploaded to smf30_exp table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_id_idx: The index of the dataframe of the Subsystem Section and Identification Section.

    Returns:
        The dataframe for the smf30 Execute Channel Program (EXCP) section.
    """
    set_datetime = np.vectorize(setdatetime)
    convert_to_list = np.vectorize(converttolist)
    if 'smf30exp' in df.columns:
        z = df['smf30exp'].to_frame().set_index(df_id_idx) #new_df_all.index)
        z.dropna(how='all', inplace=True)
        z['smf30exp'] = convert_to_list(z['smf30exp'])
        x = z.explode('smf30exp')
        df_exp = pd.json_normalize(x['smf30exp']).set_index(x.index).reset_index()
        df_exp['smf30bsz'] = df_exp['smf30bsz'].apply(lambda x: int(str(x), 16))
        df_exp['cbs'] = df_exp['smf30bsz'].apply(lambda x: is_bit_set(x, 8, 0))
        df_exp['smf30cua'] = df_exp['smf30cua'].str[2:]
        df_exp['smf30dev'] = df_exp['smf30dev'].str[2:]
        df_exp['smf30utp'] = df_exp['smf30utp'].str[2:]
        df_exp['smf30dct'] = pd.to_timedelta(df_exp['smf30dct']) / np.timedelta64(1, 's')
        df_exp['datetime'] = set_datetime(df_exp['smf30tme'])
        df_exp['dd_idx'] = df_exp.groupby(['smf30syp', 'smf30syn', 'start_interval', 'wkl', 'smf30typ',
                                           'smf30jbn', 'smf30asi', 'smf30jnm', 'smf30stn', 'gid', 'suffix']).cumcount()
        df_exp['dd_idx'] = df_exp['dd_idx'] + df_exp['excp_num']
        df_exp.set_index(['smf30syp', 'smf30syn', 'start_interval', 'wkl', 'smf30typ', 'smf30jbn',
                          'smf30asi', 'smf30jnm', 'smf30stn', 'gid', 'suffix', 'smf30cua', 'smf30ddn', 'dd_idx'],
                         inplace=True)

        df_exp.drop(columns=['excp_num'], inplace=True)
    else:
        df_exp = pd.DataFrame(columns=Smf30Exp.__table__.columns.keys()).set_index(
            ['smf30syp', 'smf30syn', 'start_interval', 'wkl', 'smf30typ', 'smf30jbn', 'smf30asi', 'smf30jnm',
             'smf30stn', 'gid', 'suffix', 'smf30cua', 'smf30ddn', 'dd_idx'])
    return df_exp


def build_ud(df: pd.DataFrame, df_id_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for Usage Data Section which will be uploaded to smf30_exp table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_id_idx: The index of the dataframe of the Subsystem Section and Identification Section.

    Returns:
        The dataframe for the smf30 Usage Data section.
    """
    set_datetime = np.vectorize(setdatetime)
    convert_to_list = np.vectorize(converttolist)
    if 'smf30ud' in df.columns:
        z = df['smf30ud'].to_frame().set_index(df_id_idx) #new_df_all.index)
        z.dropna(how='all', inplace=True)
        z['smf30ud'] = convert_to_list(z['smf30ud'])
        x = z.explode('smf30ud')
        df_ud = pd.json_normalize(x['smf30ud']).set_index(x.index).reset_index()
        df_ud['smf30ufg'] = df_ud['smf30ufg'].apply(lambda x: int(str(x), 16))
        df_ud['unauth_register_requested'] = df_ud['smf30ufg'].apply(lambda x: is_bit_set(x, 8, 0))
        df_ud['smf30uct'] = pd.to_timedelta(df_ud['smf30uct']) / np.timedelta64(1, 's')
        df_ud['smf30ucs'] = pd.to_timedelta(df_ud['smf30ucs']) / np.timedelta64(1, 's')
        df_ud['datetime'] = set_datetime(df_ud['smf30tme'])
        df_ud['prod_idx'] = (df_ud.groupby(['smf30syp', 'smf30syn', 'start_interval', 'wkl', 'smf30typ',
                                           'smf30jbn', 'smf30asi', 'smf30jnm', 'smf30stn', 'gid', 'suffix'])
                             .cumcount() + df_ud['usage_data_num'])
        df_ud.set_index(['smf30syp', 'smf30syn', 'start_interval', 'wkl', 'smf30typ', 'smf30jbn',
                         'smf30asi', 'smf30jnm', 'smf30stn', 'gid', 'suffix', 'prod_idx'], inplace=True)

        df_ud.drop(columns=['usage_data_num'], inplace=True)
    else:
        df_ud = pd.DataFrame(columns=Smf30Ud.__table__.columns.keys()).set_index(
            ['smf30syp', 'smf30syn', 'start_interval', 'wkl', 'smf30typ', 'smf30jbn', 'smf30asi', 'smf30jnm',
             'smf30stn', 'gid', 'suffix', 'prod_idx'])
    return df_ud


def build_op(df: pd.DataFrame, df_id_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for z/OS UNIX PRocess Section which will be uploaded to smf30_exp table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_id_idx: The index of the dataframe of the Subsystem Section and Identification Section.

    Returns:
        The dataframe for the smf30 z/OS UNIX PRocess section.
    """
    set_datetime = np.vectorize(setdatetime)
    convert_to_list = np.vectorize(converttolist)
    if 'smf30op' in df.columns:
        z = df['smf30op'].to_frame().set_index(df_id_idx) #new_df_all.index)
        z.dropna(how='all', inplace=True)
        z['smf30op'] = convert_to_list(z['smf30op'])
        x = z.explode('smf30op')
        df_op = pd.json_normalize(x['smf30op']).set_index(x.index).reset_index()
        df_op['smf30ost'] = pd.to_timedelta(df_op['smf30ost']) / np.timedelta64(1, 's')
        df_op['datetime'] = set_datetime(df_op['smf30tme'])
        df_op['proc_idx'] = (df_op.groupby(['smf30syp', 'smf30syn', 'start_interval', 'wkl', 'smf30typ',
                                           'smf30jbn', 'smf30asi', 'smf30jnm', 'smf30stn', 'gid', 'suffix', 'smf30opi'])
                             .cumcount() + df_op['unix_process_num'])
        df_op.set_index(['smf30syp', 'smf30syn', 'start_interval', 'wkl', 'smf30typ', 'smf30jbn',
                         'smf30asi', 'smf30jnm', 'smf30stn', 'gid', 'suffix', 'smf30opi', 'proc_idx'], inplace=True)
        df_op.drop(columns=['smf30osr', 'smf30osw', 'smf30okr', 'smf30okw', 'smf30oms', 'smf30omr', 'unix_process_num'],
                   inplace=True)
    else:
        df_op = pd.DataFrame(columns=Smf30Op.__table__.columns.keys()).set_index(
            ['smf30syp', 'smf30syn', 'start_interval', 'wkl', 'smf30typ', 'smf30jbn', 'smf30asi', 'smf30jnm',
             'smf30stn', 'gid', 'suffix', 'smf30opi', 'proc_idx'])
    return df_op


def format_30df(df: pd.DataFrame, interval: int = 30) -> tuple:
    """Format smf30 JSON files to the dataframes.

    Args:
        df: JSON dataframe.
        interval (int, optional): Default STC interval.

    Returns:
        A dictionary of dataframes.
    """
    convert_to_datetime = np.vectorize(to_datetime)
    set_datetime = np.vectorize(setdatetime)
    jobclass = np.vectorize(getjobclass)
    ebcdic_2_ascii = np.vectorize(ebcdic2ascii)
    set_wkl = np.vectorize(setwkl)
    duration = np.vectorize(cal_duration)
    # inner functions
    def check_existence(i: int, colname: str) -> pd.Series:
        return pd.isnull(df.iloc[i][colname])

    def find_suffix(no_smf30cas: int, subtype: int, gid: int, suffix: int) -> int:
        if (subtype != 1) and no_smf30cas:
            parent_suffix = dfs_dict['id'][(dfs_dict['id'].index.get_level_values('gid') == gid) & (dfs_dict['id']['no_smf30cas'] == False)][
                'suffix'].values
            if len(parent_suffix) > 0:
                return parent_suffix[0]
            else:
                return 0
        else:
            return suffix

    def get_index_values(subtype: int, gid: int, suffix: int) -> tuple:
        if (subtype != 1) and (not df_main_copy.empty):
            i = df_main_copy[(df_main_copy.index.get_level_values('gid') == gid) & (
                    df_main_copy.index.get_level_values('suffix') == suffix) & (
                                     df_main_copy['no_smf30cas'] == False)].index
            if len(i) > 0:
                return (i.get_level_values('smf30syp').values[0],
                        i.get_level_values('smf30syn').values[0],
                        i.get_level_values('start_interval').values[0], i.get_level_values('wkl').values[0],
                        i.get_level_values('excp_num').values[0], i.get_level_values('unix_process_num')[0],
                        i.get_level_values('usage_data_num').values[0])
            else:
                print('Corresponding gid and suffix not found...', gid, suffix)
                return None, None, None, None, None, None, None
        elif (subtype == 1) and (not dfs_dict['core1'].empty):
            i = dfs_dict['core1'][(dfs_dict['core1'].index.get_level_values('gid') == gid) & (
                    dfs_dict['core1'].index.get_level_values('suffix') == suffix)].index
            if len(i) > 0:
                return (i.get_level_values('smf30syp').values[0],
                        i.get_level_values('smf30syn').values[0],
                        i.get_level_values('start_interval').values[0], i.get_level_values('wkl').values[0],
                        i.get_level_values('excp_num').values[0], i.get_level_values('unix_process_num')[0],
                        i.get_level_values('usage_data_num').values[0])
            else:
                print('Corresponding gid and suffix not found...', gid, suffix)
                return None, None, None, None, None, None, None
        elif subtype != 1:
            # print('No core records exist....')
            return None, None, None, None, None, None, None
        else:
            print('Something incorrect....')
            return None, None, None, None, None, None, None

    default_stc_interval = pd.Timedelta(interval, 'm')
    if 'smf30id' not in df.columns:
        dfs_dict = {'id': pd.DataFrame(), 'core': pd.DataFrame(), 'core1': pd.DataFrame()}
        return dfs_dict, default_stc_interval

    dfs_dict = {'id': pd.concat([df['header'].apply(pd.Series),
                                 df['smf30pss'].apply(pd.Series),
                                 df['smf30id'].apply(pd.Series)], axis=1),
                'core': pd.DataFrame(), 'core1': pd.DataFrame(), 'core6': pd.DataFrame(),}
    dfs_dict['id']['dateTime'] = pd.to_datetime(dfs_dict['id']['dateTime'])
    dfs_dict['id']['start_interval'] = dfs_dict['id']['dateTime'].dt.floor('5min')
    dfs_dict['id']['gid'] = (pd.util.hash_pandas_object(df['smf30id'].astype(str), index=False) % (10 ** 8)).astype(
        'int64')
    if 'smf30cas' in df.columns:
        dfs_dict['id']['no_smf30cas'] = np.vectorize(check_existence)(dfs_dict['id'].index, 'smf30cas')
    else:
        dfs_dict['id']['no_smf30cas'] = True
    dfs_dict['id']['suffix'] = dfs_dict['id'][(dfs_dict['id']['no_smf30cas'] == False) | (
            dfs_dict['id']['smf30typ'] == 1)].groupby('gid').cumcount()
    dfs_dict['id'].set_index(['gid'], inplace=True)
    dfs_dict['id']['suffix'] = np.vectorize(find_suffix)(
        dfs_dict['id']['no_smf30cas'], dfs_dict['id']['smf30typ'],
        dfs_dict['id'].index.get_level_values('gid').values, dfs_dict['id']['suffix'])
    dfs_dict['id'] = dfs_dict['id'].reset_index().rename(columns={'dateTime': 'smf30tme'})

    dfs_dict['id']['smf30jf1'] = dfs_dict['id']['smf30jf1'].apply(lambda x: int(str(x), 16))
    dfs_dict['id']['smf30pgn_inv'] = dfs_dict['id']['smf30jf1'].apply(lambda x: is_bit_set(x, 8, 0))
    dfs_dict['id']['excp_num'] = 0
    dfs_dict['id']['unix_process_num'] = 0
    dfs_dict['id']['usage_data_num'] = 0
    dfs_dict['id']['restart_mgmt_num'] = dfs_dict['id']['smf30rmn'] + dfs_dict['id']['smf30rms']
    dfs_dict['id']['msys_encl_rem_system_data_num'] = dfs_dict['id']['smf30mno'] + dfs_dict['id']['smf30mos']
    dfs_dict['id']['smf30ast'] = convert_to_datetime(dfs_dict['id']['smf30ast'])
    dfs_dict['id']['smf30pps'] = convert_to_datetime(dfs_dict['id']['smf30pps'])
    dfs_dict['id']['smf30sit'] = convert_to_datetime(dfs_dict['id']['smf30sit'])
    dfs_dict['id']['smf30rst'] = convert_to_datetime(dfs_dict['id']['smf30rst'])
    dfs_dict['id']['smf30ret'] = convert_to_datetime(dfs_dict['id']['smf30ret'])
    dfs_dict['id']['smf30iss'] = convert_to_datetime(dfs_dict['id']['smf30iss'])
    dfs_dict['id']['smf30iet'] = convert_to_datetime(dfs_dict['id']['smf30iet'])
    dfs_dict['id']['smf30asi'] = dfs_dict['id']['smf30asi'].str[2:]
    dfs_dict['id']['datetime'] = set_datetime(dfs_dict['id']['smf30tme'])
    dfs_dict['id']['smf30cls'] = jobclass(dfs_dict['id']['subSysId'], dfs_dict['id']['smf30cls'])
    dfs_dict['id']['smf30exn'] = ebcdic_2_ascii(dfs_dict['id']['smf30exn'])
    if 'smf30holduntil' in dfs_dict['id'].columns:
        dfs_dict['id']['smf30holduntil'] = convert_to_datetime(dfs_dict['id']['smf30holduntil'])
        dfs_dict['id']['smf30deadline'] = convert_to_datetime(dfs_dict['id']['smf30deadline'])
    dfs_dict['id'] = dfs_dict['id'].drop(
        columns=['recLen', 'sysInd', 'recType', 'sysId', 'subType', 'smf30son', 'smf30ion', 'smf30uon',
                 'smf30ton', 'smf30con', 'smf30aon', 'smf30ron', 'smf30pon', 'smf30oon', 'smf30eor', 'smf30eos',
                 'smf30drn', 'smf30eon', 'smf30opn', 'smf30arn', 'smf30opm', 'smf30uds', 'smf30rmn', 'smf30rms',
                 'smf30mno', 'smf30mos', 'smf30udn', 'smf30cdn', 'smf30usn']).set_index( #, 'smf30jf1']).set_index(
        ['gid', 'suffix', 'smf30typ', 'no_smf30cas'])
    df.set_index(dfs_dict['id'].index, inplace=True)

    dfs_dict['core'] = build_df_core(df, dfs_dict['id'])

    if 1 in dfs_dict['id'].index.get_level_values('smf30typ').unique():
        dfs_dict['core1'] = pd.DataFrame(
            columns=Smf30Id.__table__.columns.keys() + ['no_smf30cas', 'subSysId'])
        id_cols = list(filter(None, dfs_dict['id'].index.names + dfs_dict['id'].columns.values.tolist())) #dfs_dict['id'].reset_index().columns
        dfs_dict['core1'][id_cols] = dfs_dict['id'][dfs_dict['id'].index.get_level_values('smf30typ') == 1].reset_index()[id_cols]
        dfs_dict['core1']['wkl'] = set_wkl(dfs_dict['core1']['smf30typ'], dfs_dict['core1']['subSysId'], dfs_dict['core1']['smf30pgm'], '')
        dfs_dict['core1'].set_index(['gid', 'suffix', 'smf30typ', 'no_smf30cas'], inplace=True)
        dfs_dict['core1'].drop(columns=['subSysId'], inplace=True)
    else:
        dfs_dict['core1'] = pd.DataFrame(columns=Smf30Id.__table__.columns.keys())

    if dfs_dict['core'].shape[0] > 0:
        dfs_dict['core6'] = dfs_dict['core'][dfs_dict['core'].index.get_level_values('smf30typ') == 6].copy()

        if dfs_dict['core6'].shape[0] > 0:
            stc_interval = dfs_dict['core6'].reset_index().groupby(
                ['smf30syp', 'smf30syn', 'smf30jbn', 'smf30asi', 'smf30jnm',
                 'smf30stn', 'smf30typ']).apply(lambda x: x['start_interval'].diff(
            ).astype('timedelta64[s]').mean(), include_groups=False).min()
        else:
            stc_interval = default_stc_interval
    else:
        stc_interval = default_stc_interval
    if pd.isnull(stc_interval):
        stc_interval = default_stc_interval

    if dfs_dict['core1'].shape[0] > 0:
        dfs_dict['core1']['duration'] = duration(dfs_dict['core1'].index.get_level_values('smf30typ'),
                                        dfs_dict['core1']['smf30iet'],
                                        dfs_dict['core1']['smf30iss'], dfs_dict['core1']['smf30tme'],
                                        dfs_dict['core1']['smf30sit'],
                                        stc_interval)
    if dfs_dict['core'].shape[0] > 0:
        dfs_dict['core']['duration'] = duration(dfs_dict['core'].index.get_level_values('smf30typ'),
                                       dfs_dict['core']['smf30iet'], dfs_dict['core']['smf30iss'],
                                       dfs_dict['core']['smf30tme'], dfs_dict['core']['smf30sit'], stc_interval)

        dfs_dict['core'].drop(columns=['subSysId', 'smf30cpt', 'smf30cps', 'smf30hpt', 'smf30iip', 'smf30rct',
                              'smf30icu_step_term', 'smf30icu_step_init', 'smf30isb_step_term',
                              'smf30isb_step_init', 'smf30cpc', 'smf30csu_l', 'smf30sus', 'smf30src',
                              'smf30srb_l'], inplace=True)

    if dfs_dict['core'].shape[0] > 0:
        dfs_dict['main'] = pd.concat([dfs_dict['id'][(dfs_dict['id'].index.get_level_values('smf30typ') != 1) & (
                dfs_dict['id'].index.get_level_values('no_smf30cas') == False)],
                             df[(df.index.get_level_values('smf30typ') != 1) & (
                                     df.index.get_level_values('no_smf30cas') == False)][
                                 'smf30prf'].apply(pd.Series)[['smf30scn']]], axis=1).reset_index()
        dfs_dict['main']['wkl'] = set_wkl(dfs_dict['main']['smf30typ'], dfs_dict['main']['subSysId'],
                                          dfs_dict['main']['smf30pgm'], dfs_dict['main']['smf30scn'])
        dfs_dict['main'].set_index(
            ['smf30syp', 'smf30syn', 'start_interval', 'wkl', 'smf30typ', 'smf30jbn', 'smf30asi',
             'smf30jnm', 'smf30stn', 'gid', 'suffix'], inplace=True)

    else:  # subtype 1 only
        dfs_dict['main'] = pd.DataFrame(
            columns=['smf30syp', 'smf30syn', 'start_interval', 'wkl', 'smf30typ', 'smf30jbn', 'smf30asi',
                     'smf30jnm', 'smf30stn', 'gid', 'suffix', 'excp_num', 'unix_process_num', 'usage_data_num']
        ).set_index(
            ['smf30syp', 'smf30syn', 'start_interval', 'wkl', 'smf30typ', 'smf30jbn', 'smf30asi',
             'smf30jnm', 'smf30stn', 'gid', 'suffix'])
    df_main_copy = dfs_dict['main'].reset_index().set_index(
        ['smf30syp', 'smf30syn', 'start_interval', 'wkl', 'smf30typ', 'smf30jbn', 'smf30asi', 'smf30jnm',
         'smf30stn', 'gid', 'suffix', 'excp_num', 'unix_process_num', 'usage_data_num'])
    if dfs_dict['core1'].shape[0] > 0:
        dfs_dict['core1'] = dfs_dict['core1'].reset_index().set_index(
            ['smf30syp', 'smf30syn', 'start_interval', 'wkl', 'smf30typ', 'smf30jbn', 'smf30asi',
             'smf30jnm', 'smf30stn', 'gid', 'suffix', 'excp_num', 'unix_process_num', 'usage_data_num'])
    df_all = dfs_dict['id'].reset_index()
    df_all['smf30syp'], df_all['smf30syn'], df_all['start_interval'], df_all['wkl'], df_all[
        'excp_num'], df_all['unix_process_num'], df_all['usage_data_num'] = np.vectorize(
        get_index_values)(df_all['smf30typ'], df_all['gid'], df_all['suffix'])
    df_all.set_index(
        ['smf30syp', 'smf30syn', 'start_interval', 'wkl', 'smf30typ', 'smf30jbn', 'smf30asi',
         'smf30jnm', 'smf30stn', 'gid', 'suffix'], inplace=True)

    dfs_dict['ura'] = build_ura(dfs_dict['core'].shape, df, dfs_dict['main'])
    dfs_dict['cas'] = build_cas(dfs_dict['core'].shape, df, dfs_dict['main'])
    dfs_dict['prf'] = build_prf(dfs_dict['core'].shape, df, dfs_dict['main'])
    dfs_dict['sap'] = build_sap(dfs_dict['core'].shape, df, dfs_dict['main'])
    dfs_dict['ops'] = build_ops(dfs_dict['core'].shape, df, dfs_dict['main'])
    dfs_dict['uss'] = build_uss(df, df_all.index, dfs_dict['main'])
    dfs_dict['exp'] = build_exp(df,
                       df_all.reset_index().set_index(
                           ['smf30syp', 'smf30syn', 'start_interval', 'wkl', 'smf30typ', 'smf30jbn',
                            'smf30asi', 'smf30jnm', 'smf30stn', 'gid', 'suffix', 'excp_num', 'smf30tme']).index)
    dfs_dict['ud'] = build_ud(df,
                     df_all.reset_index().set_index(
                         ['smf30syp', 'smf30syn', 'start_interval', 'wkl', 'smf30typ', 'smf30jbn',
                          'smf30asi', 'smf30jnm', 'smf30stn', 'gid', 'suffix', 'usage_data_num',
                          'smf30tme']).index)
    dfs_dict['op'] = build_op(df,
                     df_all.reset_index().set_index(
                         ['smf30syp', 'smf30syn', 'start_interval', 'wkl', 'smf30typ', 'smf30jbn',
                          'smf30asi', 'smf30jnm', 'smf30stn', 'gid', 'suffix', 'unix_process_num',
                          'smf30tme']).index)

    return dfs_dict, stc_interval


def print_addr_space_activity_report(jsonfiles: tuple, start_time_str: str, end_time_str: str,
                                     interval: int = 30, subtype: Union[int, None] = None,
                                     jobname: Union[str, None] = None, exclude_job_starts: Union[str, None] = None) -> str:
    """Print smf30 Address Space Activity Report based on JSON files.

    Args:
        jsonfiles: JSON file or files.
        subtype: Target subtype to print.
        start_time_str: Start time string.
        end_time_str: End time string.
        interval: STC interval.
        jobname: Job name.
        exclude_job_starts: Exclude job names start with.

    Returns:
        Address Space activity report.
    """
    start_time = pd.to_datetime(start_time_str)
    end_time = pd.to_datetime(end_time_str)

    report = ''
    dict_typ = {1: 'STA (Subtype 1)', 2: 'INT (Subtype 2)', 3: 'STE (Subtype 3)', 4: 'STT (Subtype 4)',
                5: 'JOB (Subtype 5)', 6: 'SAS (Subtype 6)'}
    for jsonfile in jsonfiles:
        with open(jsonfile) as f:
            try:
                df = pd.read_json(f)
            except ValueError:
                click.echo(
                    f"\nInvalid JSON file {jsonfile}. This file will be skipped.")
                continue

            if 'header' not in df.columns or not isinstance(df.iloc[0]['header'], dict) \
                    or df.iloc[0]['header'].get('recType') is None or df.iloc[0]['header']['recType'] != 30:
                click.echo(
                    f"\nInvalid JSON file {jsonfile}. This file will be skipped.")
                continue

            try:
                df_dict, stc_interval = format_30df(df, interval=interval)
            except Exception as e:
                click.echo(f"\nUnsupported JSON file {jsonfile} with error: {str(e)}. This file will be skipped.")
                continue

            if df_dict['id'].empty:
                click.echo(
                    f"\nThis JSON file {jsonfile} is not for this smf type. This file will be skipped.")
                # Cannot continue processing
                continue

            smf30_id = df_dict['id'].query(
                "smf30tme > @start_time and smf30tme < @end_time").reset_index()

            if smf30_id.empty:
                continue

            is_single_unique = len(np.unique(smf30_id['smf30typ'])) == 1
            if subtype is None and is_single_unique:
                subtype = smf30_id['smf30typ'].iloc[0]

            if subtype is not None:
                if jobname is None:
                    if exclude_job_starts is not None:
                        smf30_tbl = df_dict['core'].query(
                            "smf30tme > @start_time and smf30tme < @end_time and smf30typ == @subtype and not smf30jbn.str.startswith(@exclude_job_starts)").reset_index()
                        smf30_1 = df_dict['core1'].query(
                            "smf30tme > @start_time and smf30tme < @end_time and smf30typ == @subtype and not smf30jbn.str.startswith(@exclude_job_starts)").reset_index()
                    else:
                        smf30_tbl = df_dict['core'].query(
                            "smf30tme > @start_time and smf30tme < @end_time and smf30typ == @subtype").reset_index()
                        smf30_1 = df_dict['core1'].query(
                            "smf30tme > @start_time and smf30tme < @end_time and smf30typ == @subtype").reset_index()
                else:
                    if exclude_job_starts is not None:
                        smf30_tbl = df_dict['core'].query(
                            "smf30tme > @start_time and smf30tme < @end_time and smf30typ == @subtype and smf30jbn == @jobname and not smf30jbn.str.startswith(@exclude_job_starts)").reset_index()
                        smf30_1 = df_dict['core1'].query(
                            "smf30tme > @start_time and smf30tme < @end_time and smf30typ == @subtype and smf30jbn == @jobname and not smf30jbn.str.startswith(@exclude_job_starts)").reset_index()
                    else:
                        smf30_tbl = df_dict['core'].query(
                            "smf30tme > @start_time and smf30tme < @end_time and smf30typ == @subtype and smf30jbn == @jobname").reset_index()
                        smf30_1 = df_dict['core1'].query(
                            "smf30tme > @start_time and smf30tme < @end_time and smf30typ == @subtype and smf30jbn == @jobname").reset_index()
            else:
                if jobname is None:
                    if exclude_job_starts is not None:
                        smf30_tbl = df_dict['core'].query(
                            "smf30tme > @start_time and smf30tme < @end_time and not smf30jbn.str.startswith(@exclude_job_starts)").reset_index()
                        smf30_1 = df_dict['core1'].query(
                            "smf30tme > @start_time and smf30tme < @end_time and not smf30jbn.str.startswith(@exclude_job_starts)").reset_index()
                    else:
                        smf30_tbl = df_dict['core'].query(
                            "smf30tme > @start_time and smf30tme < @end_time").reset_index()
                        smf30_1 = df_dict['core1'].query(
                            "smf30tme > @start_time and smf30tme < @end_time").reset_index()
                else:
                    if exclude_job_starts is not None:
                        smf30_tbl = df_dict['core'].query(
                            "smf30tme > @start_time and smf30tme < @end_time and smf30jbn == @jobname and not smf30jbn.str.startswith(@exclude_job_starts)").reset_index()
                        smf30_1 = df_dict['core1'].query(
                            "smf30tme > @start_time and smf30tme < @end_time and smf30jbn == @jobname and not smf30jbn.str.startswith(@exclude_job_starts)").reset_index()
                    else:
                        smf30_tbl = df_dict['core'].query(
                            "smf30tme > @start_time and smf30tme < @end_time and smf30jbn == @jobname").reset_index()
                        smf30_1 = df_dict['core1'].query(
                            "smf30tme > @start_time and smf30tme < @end_time and smf30jbn == @jobname").reset_index()
            if subtype != 1:
                if subtype is None:
                    if not smf30_1.empty:
                        smf30_tbl = pd.concat([smf30_tbl, smf30_1], axis=0).set_index(
                            ['smf30tme', 'smf30jbn', 'smf30typ']).sort_index()
                        smf30_tbl = smf30_tbl.reset_index()
                smf30_df = pd.concat([smf30_tbl['smf30tme'].dt.strftime('%Y-%m-%d %H:%M:%S').rename('\n\nStart Date/Time'),
                                      (smf30_tbl['duration'].replace([np.nan, 'nan'], None)
                                                                   ).rename('\nDuration\n(Sec)'),
                                      smf30_tbl[['smf30typ', 'smf30syn', 'smf30jbn', 'smf30stm']
                                      ].rename(columns={'smf30typ':'\n\nTyp', 'smf30syn':'\nSystem\nName',
                                                        'smf30jbn':'\n\nJobName',
                                                        'smf30stm':'\nStep\nname'}),
                                      smf30_tbl['smf30scc'].replace([np.nan, 'nan'], None).rename('\n\nComp'),
                                      smf30_tbl[['cpu_total', 'smf30_time_on_ziip', 'tcb_time', 'srb_time']
                                      ].replace(np.nan, None).rename(
                                          columns={'cpu_total': 'Total\nCPU\nUsage', 'smf30_time_on_ziip': '\nzIIP\nUsage',
                                                   'tcb_time': '\nCPU\nTCB', 'srb_time': '\nCPU\nSRB'}),
                                        ((smf30_tbl['tcb_time'] + smf30_tbl['srb_time'])*100/smf30_tbl['duration']
                                         ).replace([np.nan, np.inf], None).rename('\n\n%CPU'),
                                        (smf30_tbl['smf30tex']/smf30_tbl['duration']
                                         ).replace([np.nan, np.inf], None).rename('\nEXCPs\n/Sec'),
                                        (smf30_tbl['smf30arb'] + smf30_tbl['smf30urb']).apply(lambda x:convert_bi(
                                            x,5, unit='M') if not pd.isna(x) else None).rename('\nStor\n<16M'),
                                        (smf30_tbl['smf30ear'] + smf30_tbl['smf30eur']).apply(lambda x:convert_bi(
                                            x,5, unit='M') if not pd.isna(x) else None).rename('\nStor\n>16M'),
                                        smf30_tbl['smf30hvo'].apply(lambda x:convert_bi(
                                            x,5, unit='M') if not pd.isna(x) else None).rename('\nStor\n64bit'),
                                        (smf30_tbl['smf30pgi']/smf30_tbl['duration']
                                         ).replace([np.nan, np.inf], None).rename('Page\n/Sec\nIn'),
                                        (smf30_tbl['smf30pgo']/smf30_tbl['duration']
                                         ).replace([np.nan, np.inf], None).rename('Page\n/Sec\nOut'),
                                        (smf30_tbl['smf30nsw']/smf30_tbl['duration']
                                         ).replace([np.nan, np.inf], None).rename('Page\n/Sec\nSwap'),
                                        ], axis=1)
            elif not smf30_1.empty:
                smf30_df = pd.concat([smf30_1['smf30tme'].dt.strftime('%Y-%m-%d %H:%M:%S').rename('Start Date/Time'),
                                      (smf30_1['duration'].apply(lambda x: format_s2hr(x) if not pd.isna(x) else None
                                                                   )).rename('Duration'),
                                      smf30_1[['smf30typ', 'smf30jbn', 'smf30jnm', 'smf30stm', 'smf30pgm']
                                      ].rename(
                                          columns={'smf30typ': 'Typ', 'smf30jbn': 'JobName', 'smf30jnm': 'JES Job Id',
                                                   'smf30stm': 'Stepname', 'smf30pgm': 'Program Name'})
                                      ], axis=1)
            else:
                smf30_df = pd.DataFrame()
            if not smf30_df.empty:
                header1 = [
                    ["                                              S M F    3 0   -   A D D R E S S    S P A C E    A C T I V I T Y    R E P O R T"]]
                header2 = [
                    [f"                                                      Data from   {start_time: %Y/%m/%d %H:%M}    to   {end_time:%Y/%m/%d %H:%M}"]]
                report += tb.tabulate(header1, tablefmt="plain") + "\n" + tb.tabulate(header2, tablefmt="plain") + "\n"
                report += tb.tabulate(
                    smf30_df, headers='keys', tablefmt='psql', showindex=False,
                    floatfmt=('', '.6f', '', '', '', '', '', '.6f', '.6f', '.6f', '.6f', '.2f', '.0f', '', '', '',
                              '.0f', '.0f', '.0f'))
                report += '\n\n'
    if report == '':
        report = 'No data found.'
    return report

