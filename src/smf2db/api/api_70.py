from typing import Union

import click
import tabulate as tb
import pandas as pd
import numpy as np

from smf2db.api.report_util import format_cpu_activity, format_aid_analysis, format_partition_report, \
    format_lpar_cluster_report, format_group_capacity_report, format_cca_coprocessor_detail, \
    format_pkcs11_coprocessor_detail, format_accelerator_detail, format_ccf_detail, format_crypto_header
from smf2db.db_models.smf70_model import (Smf70Pro, Smf70Ctl, Smf70Aid,
                                          Smf70Cpu, Smf70Bct, Smf70BctCpu, Smf70Bpd,
                                          Smf70Trg, Smf70Ccf, Smf70Typ3, Smf70Typ4, Smf70Typ5,)
from smf2db.api.util import (setdatetime, converttolist, is_bit_set,
                   col_to_frame, to_int, calrate, str2dict, getcputype, cputypedict,
                   agg_wait_completion_status, agg_tolist, max_processor_weight, any_1, any_gt_0,
                   agg_sum_processor_weight)


tb.PRESERVE_WHITESPACE = True
smf70typ_cpu_type = {0: 'CP', 1: 'IFA', 2: 'IIP'}


def get_ctn_can(dict_list: dict, cpu_type: str) -> tuple:
    """Get the number of physical CPUs and accumulated number of physical CPUs of this cpu type from the dictionary geneated from CPU Identification section.

    Args:
        dict_list: A dictionary generated from CPU identificaiton section with key is the cpu type.
        cpu_type: A string indciating the cpu type.

    Returns:
        the number of physical CPUs and accumulated number of physical CPUs of this cpu type.
    """
    for _dict in dict_list:
        if _dict['smf70cin'] == cpu_type:
            return _dict['smf70ctn'], _dict['smf70can']
    return None, None


def cis2dict(cislist: list) -> str:
    """From list to string of dictionary.

    Args:
        cislist: A JSON list of CPU Identification section.

    Returns:
        A string of dictionary of all CPU-identificaiton name.
    """
    newdict = {}
    for idx, item in enumerate(cislist):
        newdict[idx] = item['smf70cin']
    return str(newdict)


def getsysname(sysplex_name: str, system_name: str, smf70ptn: int, ptn: int, xnm: str, snm: str) -> tuple:
    """Get system name and sysplex name from RMF product section if they cannot be determined or are not provided.

    Args:
        sysplex_name: A sysplex name.
        system_name: A system name.
        smf70ptn: The value of smf70ptn in RMF product section.
        ptn: A partition number.
        xnm: The value of smf70xnm in RMF product section.
        snm: The value of smf70snm in RMF product section.

    Returns:
        system name and sysplex name.
    """
    if (sysplex_name == "") and (ptn == smf70ptn):
        sysplex_name = xnm
    if (system_name == "") and (ptn == smf70ptn):
        system_name = snm
    return system_name, sysplex_name


def setprocessor_weight(processor_weight_list: list) -> Union[str, float, None]:
    """Based on the list of processor weights to determine the overall processor weight.

        Args:
            processor_weight_list: A list of processor weights.

        Returns:
            Overall processor weight.
    """
    if isinstance(processor_weight_list, list):
        if len(processor_weight_list) > 0:
            if len(set(processor_weight_list)) == 1:
                if processor_weight_list[0] != 65535:
                    return str(processor_weight_list[0])
                else:
                    return 'DED'
            elif any(processor_weight_list) == 65535:
                return 'DMX'
            else:
                return 'WMX'
    return np.nan


def build_pro(df: pd.DataFrame) -> Union[pd.DataFrame, None]:
    """Build the dataframe for RMF Product Section which will be uploaded to smf70_pro table.

    Args:
        df: The master dataframe which is created from the JSON file.

    Returns:
        The dataframe for the RMF product section or None if csc is not found in the database, and it is smf70 subtype 2 record.
    """

    set_datetime = np.vectorize(setdatetime)
    if 'smf70ctl' in df.columns:
        df_pro = pd.concat([df['header'].apply(pd.Series),
                            df['smf70pro'].apply(pd.Series),
                            df['smf70bct'].apply(pd.Series)[0].str.get('smf70lpn'),
                            df['smf70ctl'].apply(pd.Series)[['smf70csc']]],
                           axis=1).rename(
            columns={'sysId': 'smf70sid',
                     'sysInd': 'smf70flg', 'recType': 'smf_type', 0: 'smf70lpn'})
        df['isFirst'] = df_pro['smf70lpn'] == df_pro['smf70ptn'].astype(float)
        df_pro['csc'] = df_pro['smf70csc'].str.lstrip('0').ffill()
    else:
        df_pro = pd.concat([df['header'].apply(pd.Series),
                            df['smf70pro'].apply(pd.Series)],
                           axis=1).rename(
            columns={'sysId': 'smf70sid',
                     'sysInd': 'smf70flg', 'recType': 'smf_type',
                    })
        df_pro['csc'] = np.nan
    df_pro['smf70sid'] = df_pro['smf70sid'].str.strip()
    df_pro['smf70ist'] = pd.to_datetime(df_pro['smf70ist'])
    df_pro['smf70gie'] = pd.to_datetime(df_pro['smf70gie'])
    df_pro['smf70int'] = pd.to_timedelta(df_pro['smf70int']) / np.timedelta64(1, 's')
    df_pro['smf70lgo'] = pd.to_timedelta(df_pro['smf70lgo']) / np.timedelta64(1, 'h')
    df_pro['datetime'] = set_datetime(df_pro['smf70ist'])
    df_pro['smf_type'] = df_pro['smf_type'].astype(str) + '.' + df_pro['subType'].astype(str)
    df_pro['smf70flg'] = df_pro['smf70flg'].apply(lambda x: int(str(x), 16))
    df_pro['smf70fla'] = df_pro['smf70fla'].apply(lambda x: int(str(x), 16))
    df_pro['smf70prf'] = df_pro['smf70prf'].apply(lambda x: int(str(x), 16))
    df_pro['smf70srl'] = df_pro['smf70srl'].apply(lambda x: int(str(x), 16))
    df_pro['speed_boost'] = df_pro['smf70fla'].apply(lambda x: is_bit_set(x, 16, 10))
    df_pro['ziip_boost'] = df_pro['smf70fla'].apply(lambda x: is_bit_set(x, 16, 9))
    df_pro = df_pro[Smf70Pro.__table__.columns.keys()].set_index(
        ['datetime', 'smf70ist', 'smf70iet', 'smf_type', 'csc', 'smf70sid', 'smf70int'])
    return df_pro


def build_ctl(df: pd.DataFrame) -> pd.DataFrame:
    """Build the dataframe for CPU Control Section which will be uploaded to smf70_ctl table.

    Args:
        df: The master dataframe which is created from the JSON file.

    Returns:
        The dataframe for the CPU Control section.
    """

    get_cis_value = np.vectorize(get_ctn_can)
    cis_2_dict = np.vectorize(cis2dict)
    if 'smf70ctl' in df.columns:
        df_ctl = pd.concat([df[df.index.get_level_values('smf_type') == '70.1']['smf70pro'].apply(pd.Series)[
                                ['smf70ptn', 'smf70snm', 'smf70xnm']],
                            df[df.index.get_level_values('smf_type') == '70.1']['smf70ctl'].apply(pd.Series),
                            df[df.index.get_level_values('smf_type') == '70.1']['isFirst'],
                            df[df.index.get_level_values('smf_type') == '70.1']['smf70cis']],
                           axis=1).rename(
            columns={'smf70cis': 'cisdict', 0: 'smf70lpn'})
        if 'smf70adj' in df_ctl.columns:
            df_ctl['smf70_ipl_time'] = pd.to_datetime(df_ctl['smf70_ipl_time'])
        else:
            df_ctl['smf70adj'] = np.nan
            df_ctl['smf70laccr'] = np.nan
            df_ctl['smf70maxpu'] = np.nan
            df_ctl['smf70os_prtct'] = np.nan
            df_ctl['smf70_ipl_time'] = pd.NaT
            df_ctl['smf70_trg_m_cnt'] = np.nan
            df_ctl['smf70cpc_type'] = np.nan
        df_ctl['smf70mod'] = df_ctl['smf70mod'].str[2:]
        df_ctl['smf70gts'] = pd.to_timedelta(df_ctl['smf70gts']) / np.timedelta64(1, 's')
        df_ctl['smf70hof'] = pd.to_timedelta(df_ctl['smf70hof']) / np.timedelta64(1, 's')
        df_ctl['smf70gjt'] = pd.to_datetime(df_ctl['smf70gjt'])
        df_ctl['smf70inb'] = df_ctl['smf70inb'].apply(lambda x: int(x, 16))
        df_ctl['smf70stf'] = df_ctl['smf70stf'].apply(lambda x: int(x, 16))
        df_ctl['smf70hhf'] = df_ctl['smf70hhf'].apply(lambda x: int(x, 16))
        df_ctl['smf70pmt'] = pd.to_timedelta(df_ctl['smf70pmt']) / np.timedelta64(1, 's')
        df_ctl['smf70mcf'] = df_ctl['smf70mcf'] / 1024
        df_ctl['smf70mcfs'] = df_ctl['smf70mcfs'] / 1024
        df_ctl['smf70mcfi'] = df_ctl['smf70mcfi'] / 1024
        df_ctl['smf70cf'] = df_ctl['smf70cf'] / 1024
        df_ctl['smf70cfs'] = df_ctl['smf70cfs'] / 1024
        df_ctl['smf70cfi'] = df_ctl['smf70cfi'] / 1024
        df_ctl['cpa_scaling_factor_effective'] = np.where(df_ctl['smf70cpa_actual'] != 0,
                                                          df_ctl['smf70cpa_scaling_factor'], 1)
        df_ctl['cpu_adjustment_factor_effective'] = np.where(df_ctl['smf70cpa_actual'] != 0,
                                                             df_ctl['smf70cpa_actual'],
                                                             df_ctl['smf70cpa'])
        df_cis = df[df.index.get_level_values('smf_type') == '70.1'][['smf70cis']]  #.apply(pd.Series)
        df_ctl['cpu_count_CP'], df_ctl['cpu_count_accumulated_CP'] = get_cis_value(df_cis['smf70cis'], 'CP')
        df_ctl['cpu_count_IFL'], df_ctl['cpu_count_accumulated_IFL'] = get_cis_value(df_cis['smf70cis'], 'IFL')
        df_ctl['cpu_count_ICF'], df_ctl['cpu_count_accumulated_ICF'] = get_cis_value(df_cis['smf70cis'], 'ICF')
        df_ctl['cpu_count_IIP'], df_ctl['cpu_count_accumulated_IIP'] = get_cis_value(df_cis['smf70cis'], 'IIP')
        df_ctl['cpu_count_CBP'], df_ctl['cpu_count_accumulated_CBP'] = get_cis_value(df_cis['smf70cis'], 'CBP')
        df_ctl['cpu_count_IFA'], df_ctl['cpu_count_accumulated_IFA'] = get_cis_value(df_cis['smf70cis'], 'IFA')
        df_ctl['cisdict'] = cis_2_dict(df_ctl['cisdict'])
        if 'smf70mdl_var' in df_ctl.columns:
            df_ctl['smf70mdl_var'] = df_ctl['smf70mdl_var'].apply(lambda x: bytearray.fromhex(x[2:]).decode('cp500').rstrip())
        df_ctl = df_ctl.reset_index().set_index(['csc', 'smf70sid', 'datetime', 'smf70ist', 'smf70iet'])
    else:
        df_ctl = pd.DataFrame(columns=Smf70Ctl.__table__.columns.keys()).set_index(
            ['csc', 'smf70sid', 'datetime', 'smf70ist', 'smf70iet'])
    return df_ctl


def build_bct(df: pd.DataFrame, ctl_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for PR/SM Partition Data Section which will be uploaded to smf70_bct table.

    Args:
        df: The master dataframe which is created from the JSON file.
        ctl_idx: The index of the dataframe for CPU Control section.

    Returns:
        The dataframe for the PR/SM Partition Data section.
    """

    convert_to_list = np.vectorize(converttolist)
    get_sys_name = np.vectorize(getsysname)
    if 'smf70bct' in df.columns:
        z = df[(df.index.get_level_values('smf_type') == '70.1')].reset_index()['smf70bct'].to_frame().set_index(
            ctl_idx)
        z.dropna(how='all', inplace=True)
        z['smf70bct'] = convert_to_list(z['smf70bct'])
        z = z.reset_index().reset_index().set_index(
            ['csc', 'smf70sid', 'datetime', 'smf70ist', 'smf70iet', 'smf70int', 'smf70dsa',
             'smf70cpa_actual', 'smf70cpa_scaling_factor', 'smf70ptn', 'smf70xnm', 'smf70snm',
             'cpa_scaling_factor_effective', 'cpu_adjustment_factor_effective',
             'cpu_count_CP', 'cpu_count_IFL', 'cpu_count_ICF', 'cpu_count_IIP', 'cpu_count_CBP',
             'cpu_count_IFA', 'cisdict', 'index'])
        x = z.explode('smf70bct').reset_index()
        x['bct_idx'] = x.groupby(['smf70sid', 'datetime', 'smf70ist', 'smf70iet', 'smf70int', 'smf70dsa',
                     'smf70cpa_actual', 'smf70cpa_scaling_factor', 'smf70ptn', 'smf70xnm', 'smf70snm',
                     'cpa_scaling_factor_effective', 'cpu_adjustment_factor_effective',
                     'cpu_count_CP', 'cpu_count_IFL', 'cpu_count_ICF', 'cpu_count_IIP', 'cpu_count_CBP',
                     'cpu_count_IFA', 'cisdict', 'index']).cumcount()
        x.set_index(['csc', 'smf70sid', 'datetime', 'smf70ist', 'smf70iet', 'smf70int', 'smf70dsa',
                     'smf70cpa_actual', 'smf70cpa_scaling_factor', 'smf70ptn', 'smf70xnm', 'smf70snm',
                     'cpa_scaling_factor_effective', 'cpu_adjustment_factor_effective',
                     'cpu_count_CP', 'cpu_count_IFL', 'cpu_count_ICF', 'cpu_count_IIP', 'cpu_count_CBP',
                     'cpu_count_IFA', 'cisdict', 'index', 'bct_idx'], inplace=True)
        df_bct = pd.json_normalize(x['smf70bct']).set_index(x.index).reset_index()
        df_bct['bct_idx'] = df_bct.groupby(['csc', 'smf70sid', 'datetime', 'smf70ist', 'smf70iet']).cumcount()
        df_bct['smf70csf'] = df_bct['smf70csf'].apply(lambda x: int(x[:-2]))
        df_bct['smf70esf'] = df_bct['smf70esf'].apply(lambda x: int(x[:-2]))
        df_bct['sysplex_name'] = df_bct['smf70spn']
        df_bct['system_name'], df_bct['sysplex_name'] = get_sys_name(df_bct['sysplex_name'], df_bct['smf70stn'],
                                                                     df_bct['smf70lpn'], df_bct['smf70ptn'],
                                                                     df_bct['smf70xnm'], df_bct['smf70snm'])
        df_bct['lpar_system_name'] = df_bct['smf70lpm'] + '-' + df_bct['system_name']
        df_bct['lpar_number'] = df_bct['smf70lpn']

        if 'smf70_boostinfo' in df_bct.columns:
            df_bct['smf70_boostinfo'] = df_bct['smf70_boostinfo'].apply(lambda x: int(x, 16))
        else:
            df_bct['smf70_boostinfo'] = np.nan

        df_bct['smf70pfl'] = df_bct['smf70pfl'].apply(lambda x: int(x, 16))
        df_bct['smf70pfg'] = df_bct['smf70pfg'].apply(lambda x: int(x, 16))
        df_bct.set_index(
            [col.name for col in Smf70Bct.__table__.primary_key.columns.values()], inplace=True)
    else:
        df_bct = pd.DataFrame(columns=Smf70Bct.__table__.columns.keys()).set_index(
            [col.name for col in Smf70Bct.__table__.primary_key.columns.values()])
    return df_bct


def build_aid(df: pd.DataFrame, ctl_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for ASID Data Area Section which will be uploaded to smf70_aid table.

    Args:
        df: The master dataframe which is created from the JSON file.
        ctl_idx: The index of the dataframe for CPU Control section.

    Returns:
        The dataframe for the ASID Data Area section.
    """
    if 'smf70aid' in df.columns:
        df_aid = pd.json_normalize(df[(df.index.get_level_values('smf_type') == '70.1') & (df['isFirst'])]['smf70aid']
                                   ).set_index(ctl_idx).reset_index()[Smf70Aid.__table__.columns.keys()
        ].set_index([col.name for col in Smf70Aid.__table__.primary_key.columns.values()])
    else:
        df_aid = pd.DataFrame(columns=Smf70Aid.__table__.columns.keys()).set_index(
            [col.name for col in Smf70Aid.__table__.primary_key.columns.values()])
    return df_aid


def build_trg(df: pd.DataFrame, ctl_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for Tenant Resource Group Data Section which will be uploaded to smf70_trg table.

    Args:
        df: The master dataframe which is created from the JSON file.
        ctl_idx: The index of the dataframe for CPU Control section.

    Returns:
        The dataframe for the Tenant Resource Group Data section.
    """
    if 'smf70tnt' in df.columns:
        df_trg = col_to_frame(df[(df.index.get_level_values('smf_type') == '70.1') & (df['isFirst'])], 'smf70tnt',
                              ctl_idx)[Smf70Trg.__table__.columns.keys()].drop_duplicates().set_index(
            [col.name for col in Smf70Trg.__table__.primary_key.columns.values()])
    else:
        df_trg = pd.DataFrame(columns=Smf70Trg.__table__.columns.keys()
                              ).set_index([col.name for col in Smf70Trg.__table__.primary_key.columns.values()])
    return df_trg


def build_bpd(df: pd.DataFrame, pro_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for PR/SM Logical Processor Data Section which will be uploaded to smf70_bpd table.

    Args:
        df: The master dataframe which is created from the JSON file.
        pro_idx: The index of the dataframe for RMF Product section.

    Returns:
        The dataframe for the PR/SM Logical Processor Data section.
    """

    convert_to_list = np.vectorize(converttolist)
    convert_2_int = np.vectorize(to_int)

    if 'smf70bpd' in df.columns:
        z = df[(df.index.get_level_values('smf_type') == '70.1')].reset_index()['smf70bpd'].to_frame().set_index(
            pro_idx)
        z.dropna(how='all', inplace=True)
        z['smf70bpd'] = convert_to_list(z['smf70bpd'])
        z = z.reset_index().reset_index().set_index(['csc', 'smf70sid', 'datetime', 'smf70ist', 'smf70iet', 'index'])
        x = z.explode('smf70bpd').reset_index()
        x['bpd_idx'] = x.groupby(['datetime', 'smf70ist', 'smf70iet', 'smf70sid', 'index']).cumcount()
        x.set_index(['csc', 'datetime', 'smf70ist', 'smf70iet', 'smf70sid', 'index', 'bpd_idx'], inplace=True)
        df_bpd = pd.json_normalize(x['smf70bpd']).set_index(x.index)
        df_bpd['smf70vpa'] = df_bpd['smf70vpa'].apply(int, base=16)
        df_bpd['smf70pdt'] = pd.to_timedelta(df_bpd['smf70pdt']) / np.timedelta64(1, 's')
        df_bpd['smf70edt'] = pd.to_timedelta(df_bpd['smf70edt']) / np.timedelta64(1, 's')
        df_bpd['smf70ont'] = pd.to_timedelta(
            df_bpd['smf70ont']) / np.timedelta64(1, 's')
        df_bpd['smf70wst'] = pd.to_timedelta(df_bpd['smf70wst']) / np.timedelta64(1, 's')
        df_bpd['smf70mtit'] = pd.to_timedelta(df_bpd['smf70mtit']) / np.timedelta64(1, 's')
        df_bpd['smf70bps'] = convert_2_int(df_bpd['smf70bps'])
        df_bpd['smf70mis'] = convert_2_int(df_bpd['smf70mis'])
        df_bpd['smf70mas'] = convert_2_int(df_bpd['smf70mas'])
        df_bpd['smf70vpf'] = df_bpd['smf70vpf'].apply(lambda k: int(k, 16))
        df_bpd['smf70pof'] = df_bpd['smf70pof'].apply(lambda k: int(k, 16))
        if 'smf70lpf' in df_bpd.columns:
            df_bpd['smf70lpf'] = df_bpd['smf70lpf'].apply(lambda x: int(x, 16))

    else:
        df_bpd = pd.DataFrame(columns=Smf70Bpd.__table__.columns.keys()).set_index(
            [col.name for col in Smf70Bpd.__table__.primary_key.columns.values()])
    return df_bpd


def build_cpu(df: pd.DataFrame, df_ctl: pd.DataFrame) -> pd.DataFrame:
    """Build the dataframe for CPU Data Section which will be uploaded to smf70_cpu table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_ctl: The dataframe for CPU Control section.

    Returns:
        The dataframe for the CPU Data section.
    """

    convert_to_list = np.vectorize(converttolist)
    cpu_type_dict = np.vectorize(cputypedict)
    if 'smf70cpu' in df.columns:
        ctl_columns = ['csc', 'datetime', 'smf70ist', 'smf70iet', 'smf70sid', 'smf70int',
                       'lpar_system_name', 'smf70ptn', 'smf70hhf']
        z_idx_columns = ctl_columns + ['index']
        x_idx_columns = z_idx_columns + ['cpu_idx']
        d = df_ctl.reset_index().reset_index().set_index(ctl_columns)
        z = df[(df.index.get_level_values('smf_type') == '70.1') & (df['isFirst'])].reset_index()[
            'smf70cpu'].to_frame().set_index(
            d[d['isFirst']].reset_index().set_index(z_idx_columns).index)
        z.dropna(how='all', inplace=True)
        z['smf70cpu'] = convert_to_list(z['smf70cpu'])
        x = z.explode('smf70cpu').reset_index()
        x['cpu_idx'] = x.groupby(z_idx_columns).cumcount()
        x.set_index(x_idx_columns, inplace=True)
        if 'smf70lcs' in df.columns:  # multithreading
            df_cpu = pd.json_normalize(x['smf70cpu']).set_index(x.index)
            df_cpu['multithreading'] = 1
        else:  # non-multhreading
            df_cpu = pd.json_normalize(x['smf70cpu']).set_index(x.index)
            df_cpu['smf70_core_id'] = np.nan
            df_cpu['smf70_cpu_skip'] = np.nan
            df_cpu['smf70_cpu_num'] = np.nan
            df_cpu['smf70_prod'] = np.nan
            df_cpu['lpb_valid'] = np.nan
            df_cpu['smf70_lpar_busy'] = np.nan
            df_cpu['multithreading'] = 0
        df_cpu = df_cpu.reset_index().set_index(['csc', 'datetime', 'smf70ist', 'smf70iet', 'smf70sid', 'index', 'cpu_idx'])
        df_cpu['smf70typ'] = cpu_type_dict(df_cpu['smf70typ'])
        df_cpu['smf70ser'] = df_cpu['smf70ser'].str[2:]
        df_cpu['smf70wat'] = pd.to_timedelta(df_cpu['smf70wat']) / np.timedelta64(1, 's')
        df_cpu['smf70pat'] = pd.to_timedelta(df_cpu['smf70pat']) / np.timedelta64(1, 's')
        df_cpu['smf70wti'] = pd.to_timedelta(df_cpu['smf70wti']) / np.timedelta64(1, 's')
        df_cpu['rate_io_interrupt'] = ((df_cpu['smf70slh'] + df_cpu['smf70tpi']) / df_cpu['smf70int']).where(
            df_cpu['smf70typ'] == 'CP', np.nan)
        df_cpu['rate_tcb'] = df_cpu['smf70tcb'] / df_cpu['smf70int']
        df_cpu['rate_srb'] = df_cpu['smf70srb'] / df_cpu['smf70int']
        df_cpu['rate_io'] = df_cpu['smf70nio'] / df_cpu['smf70int']
        df_cpu['rate_io_interrupt_by_tpi'] = (
                    100 * df_cpu['smf70tpi'] / (df_cpu['smf70slh'] + df_cpu['smf70tpi'])).where(
            (df_cpu['smf70typ'] == 'CP') & ((df_cpu['smf70slh'] + df_cpu['smf70tpi']) > 0), np.nan)
        df_cpu['smf70cnf'] = df_cpu['smf70cnf'].apply(lambda x: int(x, 16))
        df_cpu['smf70v'] = df_cpu['smf70v'].apply(lambda x: int(x, 16))
    else:
        df_cpu = pd.DataFrame(columns=Smf70Cpu.__table__.columns.keys()).set_index(
            [col.name for col in Smf70Cpu.__table__.primary_key.columns.values()])
    return df_cpu


def countpolarization(series: list, value: Union[str, int, float]) -> int:
    """Count the occurrence of the value in the series.

    Args:
        series: The list to count the value.
        value: The target value to be counted.

    Returns:
        The number of obervations in the list.
    """
    return series.count(value)


def extract_cpu_polarization(num):
    if not pd.isna(num):
        num = int(num)
        flags_polarization = "{0:0{l}b}".format(num, l=8)
        if flags_polarization[0:2] == '00':
            cpu_polarization = 'N/A'
        elif flags_polarization[0:2] == '01':
            cpu_polarization = 'LOW'
        elif flags_polarization[0:2] == '10':
            cpu_polarization = 'MED'
        elif flags_polarization[0:2] == '11':
            cpu_polarization = 'HIGH'
        else:
            cpu_polarization = 'UNKN'
    else:
        cpu_polarization = 'UNKN'
    return cpu_polarization


def build_bct_cpu(df_bpd: pd.DataFrame) -> pd.DataFrame:
    """Build the dataframe for PR/SM Logical Processor Data Section for the corresponding partition by CPU type which will be uploaded to smf70_bct_cpu table.

    Args:
        df_bpd: The dataframe of the PR/SM Logical Processor Data Section.

    Returns:
        The dataframe for the PR/SM Logical Processor Data section of the correspondign partition by CPU type.
    """
    count_polarization = np.frompyfunc(countpolarization, 2, 1)
    set_processor_weight = np.vectorize(setprocessor_weight, otypes=[object])
    set_cpu_polarization = np.vectorize(extract_cpu_polarization)
    new_df_bpd = df_bpd.copy()
    new_df_bpd['poc'] = new_df_bpd['smf70pof'].apply(lambda x: is_bit_set(x, 8, 2))
    new_df_bpd['cap_limit_chng'] = new_df_bpd['smf70vpf'].apply(lambda x: is_bit_set(x, 8, 7))
    new_df_bpd['hw_cap_limit_chng'] = new_df_bpd['smf70vpf'].apply(lambda x: is_bit_set(x, 8, 6))
    new_df_bpd['logical_vary_online'] = new_df_bpd['smf70vpf'].apply(lambda x: is_bit_set(x, 8, 5))
    new_df_bpd['initial_cap_chng'] = new_df_bpd['smf70vpf'].apply(lambda x: is_bit_set(x, 8, 4))
    new_df_bpd['initial_cap_no'] = new_df_bpd['smf70vpf'].apply(lambda x: is_bit_set(x, 8, 3))
    new_df_bpd['relative_share_chng'] = new_df_bpd['smf70vpf'].apply(lambda x: is_bit_set(x, 8, 2))
    new_df_bpd['wait_completion_status_chng'] = new_df_bpd['smf70vpf'].apply(lambda x: is_bit_set(x, 8, 1))
    new_df_bpd['wait_completion_status'] = new_df_bpd['smf70vpf'].apply(lambda x: is_bit_set(x, 8, 0))
    new_df_bpd['cpu_polarization'] = set_cpu_polarization(new_df_bpd['smf70pof'])
    if 'smf70lpf' not in new_df_bpd.columns:
        new_df_bpd['smf70lpf'] = np.nan
        new_df_bpd['smf70maxnl'] = np.nan
        new_df_bpd['smf70cordl1'] = np.nan
        new_df_bpd['smf70cordl2'] = np.nan
        new_df_bpd['smf70cordl3'] = np.nan
        new_df_bpd['smf70cordl4'] = np.nan
        new_df_bpd['smf70cordl5'] = np.nan
        new_df_bpd['smf70cordl6'] = np.nan
    df_bct_cpu = new_df_bpd.reset_index().groupby(
        ['csc', 'lpar_system_name', 'lpar_number', 'datetime', 'smf70ist', 'smf70iet', 'smf70sid', 'smf70cix']).agg(
        smf70stn=('smf70stn', 'first'),
        smf70lpn=('smf70lpn', 'first'),
        smf70lpm=('smf70lpm', 'first'),
        defined_cpu_count=('bpd_idx', 'count'),
        cpu_count=('cpu_count', 'first'),
        physical_cpu_count=('physical_cpu_count', 'first'),
        wait_completion_status=('wait_completion_status', agg_wait_completion_status),
        msu_physical=('msu_physical', 'mean'),
        wgt=('smf70bps', agg_tolist),
        smf70bps=('smf70bps', max_processor_weight),
        processor_weight_online=('processor_weight_online', 'max'),
        msu_effective=('msu_effective', 'mean'),
        smf70acs=('smf70acs', 'mean'),
        total_smf70acs=('smf70acs', 'sum'),
        share_current=('share_current', 'mean'),
        logical_processor_is_online=('logical_processor_is_online', 'sum'),
        utilization_per_cpu_physical=('utilization_per_cpu_physical', 'mean'),
        lpar_management_per_cpu=('lpar_management_per_cpu', 'sum'),
        smf70mis=('smf70mis', 'min'),
        smf70mas=('smf70mas', 'max'),
        smf70nsi=('smf70nsi', 'mean'),
        smf70nsa=('smf70nsa', 'mean'),
        smf70ont=('smf70ont', 'sum'),
        smf70edt=('smf70edt', 'sum'),
        smf70pdt=('smf70pdt', 'sum'),
        smf70wst=('smf70wst', 'sum'),
        smf70pma=('smf70pma', 'first'),
        smf70nsw=('smf70nsw', 'first'),
        smf70pow=('smf70pow', 'first'),
        smf70nca=('smf70nca', 'first'),
        smf70mtit=('smf70mtit', 'sum'),
        smf70hw_cap_limit=('smf70hw_cap_limit', 'max'),
        smf70hwgr_cap_limit=('smf70hwgr_cap_limit', 'max'),
        initial_cap_indicator=('initial_cap_no', any_1),
        cap_absolute_indicator=('smf70hw_cap_limit', any_gt_0),
        cap_absolute_group_indicator=('smf70hwgr_cap_limit', any_gt_0),
        smf70int=('smf70int', 'first'),
        smf70cpa_scaling_factor=('smf70cpa_scaling_factor', 'first'),
        smf70cpa_actual=('smf70cpa_actual', 'first'),
        cpu_polarization=('cpu_polarization', agg_tolist),
        smf70vpf=('smf70vpf', 'last'),
        smf70pof=('smf70pof', 'last'),
        smf70lpf=('smf70lpf', 'last'),
        smf70maxnl=('smf70maxnl', 'last'),
        smf70cordl1=('smf70cordl1', 'last'),
        smf70cordl2=('smf70cordl2', 'last'),
        smf70cordl3=('smf70cordl3', 'last'),
        smf70cordl4=('smf70cordl4', 'last'),
        smf70cordl5=('smf70cordl5', 'last'),
        smf70cordl6=('smf70cordl6', 'last'),
    ).reset_index().set_index(
        ['csc', 'lpar_system_name', 'lpar_number', 'smf70lpm', 'datetime', 'smf70ist', 'smf70iet', 'smf70sid', 'smf70cix'])
    df_bct_cpu['wgt'] = set_processor_weight(df_bct_cpu['wgt'])
    df_bct_cpu['logical_processor_effective'] = (
                df_bct_cpu['smf70edt'] * 100 / df_bct_cpu['smf70ont']
                ).where(df_bct_cpu['smf70ont'] > 0)
    df_bct_cpu['logical_processor_total'] = (
                df_bct_cpu['smf70pdt'] * 100 / df_bct_cpu['smf70ont']
                ).where(df_bct_cpu['smf70ont'] > 0)
    df_bct_cpu['physical_processor_effective'] = (
                df_bct_cpu['smf70edt'] * 100 / df_bct_cpu['physical_cpu_count'].astype('float') /
                df_bct_cpu['smf70int']
                ).where(df_bct_cpu['physical_cpu_count'] > 0, 0.0)
    df_bct_cpu['physical_processor_total'] = (
            df_bct_cpu['smf70pdt'] * 100 / df_bct_cpu['physical_cpu_count'].astype('float') / df_bct_cpu[
        'smf70int']).where(
        df_bct_cpu['physical_cpu_count'] > 0, 0)
    df_bct_cpu['actual_consumed_msu'] = df_bct_cpu['smf70pdt'] * 3600 * 16 * df_bct_cpu[
        'smf70cpa_scaling_factor'] / (
                                                df_bct_cpu['smf70cpa_actual'] * df_bct_cpu['smf70int'])
    df_bct_cpu['effective_consumed_msu'] = df_bct_cpu['smf70edt'] * 3600 * 16 * df_bct_cpu[
        'smf70cpa_scaling_factor'] / (
                                                   df_bct_cpu['smf70cpa_actual'] * df_bct_cpu['smf70int'])
    df_bct_cpu['high_polarization'] = count_polarization(df_bct_cpu['cpu_polarization'], 'HIGH')
    df_bct_cpu['med_polarization'] = count_polarization(df_bct_cpu['cpu_polarization'], 'MED')
    return df_bct_cpu


def build_typ3(df: pd.DataFrame, pro_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for Cryptographic CCA Coprocessor Data Section which will be uploaded to smf70_typ3 table.

    Args:
        df: The master dataframe which is created from the JSON file.
        pro_idx: The index of the dataframe for RMF Product section.

    Returns:
        The dataframe for the Cryptographic CCA Coprocessor Data section.
    """

    if 'r702typ3' in df.columns:
        typ3_type = {7: 'CEX2C', 9: 'CEX3C', 10: 'CEX4C', 11: 'CEX5C', 12: 'CEX6C', 13: 'CEX7C', 14: 'CEX8C'}
        df_typ3 = col_to_frame(df, 'r702typ3', pro_idx) #.drop(columns=['r7023mt'])
        if 'r7023scope' not in df_typ3.columns: # Version 2.2 or before
            df_typ3['r7023scope'] = 1
        df_typ3.set_index([col.name for col in Smf70Typ3.__table__.primary_key.columns.values()], inplace=True)
        df_typ3['r7023msk'] = df_typ3['r7023msk'].apply(lambda x: int(x, 16))
        df_typ3['r7023ct'] = df_typ3['r7023ct'].map(typ3_type)
    else:
        df_typ3 = pd.DataFrame(columns=Smf70Typ3.__table__.columns.keys()).set_index(
            [col.name for col in Smf70Typ3.__table__.primary_key.columns.values()])
    return df_typ3


def rename_tc_columns(column_list: list, suffix: str) -> dict:
    """Build a dictionary to add suffix to all the columns in the column list.

    Args:
        column_list: The column list.
        suffix: The suffix to be appended in the column name.

    Returns:
        A dictionary of original columns' name and new columns' name.

    """
    return dict(zip(column_list, [sub + suffix for sub in column_list]))


def build_typ4(df: pd.DataFrame, pro_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for Cryptographic Accelerataor Data Section which will be uploaded to smf70_typ4 table.

    Args:
        df: The master dataframe which is created from the JSON file.
        pro_idx: The index of the dataframe for RMF Product section.

    Returns:
        The dataframe for the Cryptographic Accelerator Data section.
    """

    def convert_col_list_2_columns(frame, target_col, len_of_list):
        dx = pd.DataFrame(df_typ4['r7024tc'].to_list(), columns=list(range(1, len_of_list + 1)))
        dx_list = []
        for i in range(1, len_of_list + 1):
            dx_list.append(pd.json_normalize(dx[i]).rename(
                columns=rename_tc_columns(
                    ['r7021met', 'r7021mec', 'r7022met', 'r7022mec', 'r7021crt', 'r7021crc', 'r7022crt', 'r7022crc'],
                    f'_{i}')))
        return pd.concat(dx_list, axis=1).set_index(frame.index)

    if 'r702typ4' in df.columns:
        typ4_type = {6: 'CEX2A', 8: 'CEX3A', 10: 'CEX4A', 11: 'CEX5A', 12: 'CEX6A', 13: 'CEX7A', 14: 'CEX8A'}
        df_typ4 = col_to_frame(df, 'r702typ4', pro_idx)
        if 'r7024scope' not in df_typ4.columns: # Version 2.2 or before
            df_typ4['r7024scope'] = 1
        df_typ4.set_index([col.name for col in Smf70Typ4.__table__.primary_key.columns.values()], inplace=True)
        df_typ4['r7024msk'] = df_typ4['r7024msk'].apply(lambda x: int(x, 16))
        df_typ4['r7024ct'] = df_typ4['r7024ct'].map(typ4_type)
        typ4_ext = convert_col_list_2_columns(df_typ4['r7024tc'].to_frame(), 'r7024tc', 5)
        df_typ4 = pd.concat([df_typ4, typ4_ext], axis=1).drop(columns=['r7024tc'])
    else:
        df_typ4 = pd.DataFrame(columns=Smf70Typ4.__table__.columns.keys()).set_index(
            [col.name for col in Smf70Typ4.__table__.primary_key.columns.values()])
    return df_typ4


def build_typ5(df: pd.DataFrame, pro_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for Cryptographic PKCS11 Coprocessor Data Section which will be uploaded to smf70_typ5 table.

    Args:
        df: The master dataframe which is created from the JSON file.
        pro_idx: The index of the dataframe for RMF Product section.

    Returns:
        The dataframe for the Cryptographic PKCS11 Coprocessor Data section.
    """

    if 'r702typ5' in df.columns:
        typ5_type = {10: 'CEX4P', 11: 'CEX5P', 12: 'CEX6P', 13: 'CEX7P', 14: 'CEX8P'}
        df_typ5 = col_to_frame(df, 'r702typ5', pro_idx)
        if 'r7025scope' not in df_typ5.columns: # Version 2.2 or before
            df_typ5['r7025scope'] = 1
        df_typ5.set_index([col.name for col in Smf70Typ5.__table__.primary_key.columns.values()], inplace=True)
        df_typ5['r7025msk'] = df_typ5['r7025msk'].apply(lambda x: int(x, 16))
        df_typ5['r7025ct'] = df_typ5['r7025ct'].map(typ5_type)
    else:
        df_typ5 = pd.DataFrame(columns=Smf70Typ5.__table__.columns.keys()).set_index(
            [col.name for col in Smf70Typ5.__table__.primary_key.columns.values()])
    return df_typ5


def build_ccf(df: pd.DataFrame, pro_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for ICSF Services Data Section which will be uploaded to smf70_ccf table.

    Args:
        df: The master dataframe which is created from the JSON file.
        pro_idx: The index of the dataframe for RMF Product section.

    Returns:
        The dataframe for the ICSF ServicesData section.
    """
    if 'r702ccf' in df.columns:
        df_ccf = col_to_frame(df, 'r702ccf', pro_idx).set_index(
            [col.name for col in Smf70Ccf.__table__.primary_key.columns.values()])
        df_ccf['r702aesc'] = np.where(df_ccf['r702cdlv'] > 11, df_ccf['r702aesc'], np.nan)
        df_ccf['r702aesb'] = np.where(df_ccf['r702cdlv'] > 11, df_ccf['r702aesb'], np.nan)
        df_ccf['r702aesi'] = np.where(df_ccf['r702cdlv'] > 11, df_ccf['r702aesi'], np.nan)
        df_ccf['r702asdc'] = np.where(df_ccf['r702cdlv'] > 11, df_ccf['r702asdc'], np.nan)
        df_ccf['r702asdb'] = np.where(df_ccf['r702cdlv'] > 11, df_ccf['r702asdb'], np.nan)
        df_ccf['r702asdi'] = np.where(df_ccf['r702cdlv'] > 11, df_ccf['r702asdi'], np.nan)
        df_ccf['r702drgc'] = np.where(df_ccf['r702cdlv'] > 13, df_ccf['r702drgc'], np.nan)
        df_ccf['r702drvc'] = np.where(df_ccf['r702cdlv'] > 13, df_ccf['r702drvc'], np.nan)
        df_ccf['r702degc'] = np.where(df_ccf['r702cdlv'] > 13, df_ccf['r702degc'], np.nan)
        df_ccf['r702devc'] = np.where(df_ccf['r702cdlv'] > 13, df_ccf['r702devc'], np.nan)
        df_ccf['r702amgc'] = np.where(df_ccf['r702cdlv'] > 17, df_ccf['r702amgc'], np.nan)
        df_ccf['r702amgb'] = np.where(df_ccf['r702cdlv'] > 17, df_ccf['r702amgb'], np.nan)
        df_ccf['r702amgi'] = np.where(df_ccf['r702cdlv'] > 17, df_ccf['r702amgi'], np.nan)
        df_ccf['r702amvc'] = np.where(df_ccf['r702cdlv'] > 17, df_ccf['r702amvc'], np.nan)
        df_ccf['r702amvb'] = np.where(df_ccf['r702cdlv'] > 17, df_ccf['r702amvb'], np.nan)
        df_ccf['r702amvi'] = np.where(df_ccf['r702cdlv'] > 17, df_ccf['r702amvi'], np.nan)
        df_ccf['r702fpec'] = np.where(df_ccf['r702cdlv'] > 19, df_ccf['r702fpec'], np.nan)
        df_ccf['r702fpeb'] = np.where(df_ccf['r702cdlv'] > 19, df_ccf['r702fpeb'], np.nan)
        df_ccf['r702fpei'] = np.where(df_ccf['r702cdlv'] > 19, df_ccf['r702fpei'], np.nan)
        df_ccf['r702fpdc'] = np.where(df_ccf['r702cdlv'] > 19, df_ccf['r702fpdc'], np.nan)
        df_ccf['r702fpdb'] = np.where(df_ccf['r702cdlv'] > 19, df_ccf['r702fpdb'], np.nan)
        df_ccf['r702fpdi'] = np.where(df_ccf['r702cdlv'] > 19, df_ccf['r702fpdi'], np.nan)
        df_ccf['r702fptc'] = np.where(df_ccf['r702cdlv'] > 19, df_ccf['r702fptc'], np.nan)
        df_ccf['r702fptb'] = np.where(df_ccf['r702cdlv'] > 19, df_ccf['r702fptb'], np.nan)
        df_ccf['r702fpti'] = np.where(df_ccf['r702cdlv'] > 19, df_ccf['r702fpti'], np.nan)
        if 'r702fxec' in df_ccf.columns:
            df_ccf['r702fxec'] = np.where(df_ccf['r702cdlv'] > 22, df_ccf['r702fxec'], np.nan)
            df_ccf['r702fxeb'] = np.where(df_ccf['r702cdlv'] > 22, df_ccf['r702fxeb'], np.nan)
            df_ccf['r702fxei'] = np.where(df_ccf['r702cdlv'] > 22, df_ccf['r702fxei'], np.nan)
            df_ccf['r702fxdc'] = np.where(df_ccf['r702cdlv'] > 22, df_ccf['r702fxdc'], np.nan)
            df_ccf['r702fxdb'] = np.where(df_ccf['r702cdlv'] > 22, df_ccf['r702fxdb'], np.nan)
            df_ccf['r702fxdi'] = np.where(df_ccf['r702cdlv'] > 22, df_ccf['r702fxdi'], np.nan)
            df_ccf['r702fxtc'] = np.where(df_ccf['r702cdlv'] > 22, df_ccf['r702fxtc'], np.nan)
            df_ccf['r702fxtb'] = np.where(df_ccf['r702cdlv'] > 22, df_ccf['r702fxtb'], np.nan)
            df_ccf['r702fxti'] = np.where(df_ccf['r702cdlv'] > 22, df_ccf['r702fxti'], np.nan)
            df_ccf['r702dqgc'] = np.where(df_ccf['r702cdlv'] > 22, df_ccf['r702dqgc'], np.nan)
            df_ccf['r702dqvc'] = np.where(df_ccf['r702cdlv'] > 22, df_ccf['r702dqvc'], np.nan)
    else:
        df_ccf = pd.DataFrame(columns=Smf70Ccf.__table__.columns.keys()).set_index(
            [col.name for col in Smf70Ccf.__table__.primary_key.columns.values()])
    return df_ccf


def calculate_total_log_proc_share_pct(wgt, weight_total, physical_cpu_count):
    if not pd.isna(wgt) and not pd.isna(weight_total) and weight_total > 0 and wgt not in (65535, 'DED', 'DMX', 'WMX'):
        return int(wgt) / weight_total * physical_cpu_count * 100
    else:
        return np.nan


def min_entitlement(init_weight, msu, gmu, bps, sum_bps, acs, sum_acs):
    if init_weight == 1:
        if sum_bps is not None and sum_bps > 0:
            return min(msu, gmu * bps / sum_bps)
        else:
            return msu
    else:
        if not pd.isna(sum_acs) and sum_acs > 0:
            return min(msu, gmu * acs / sum_acs)
        else:
            return msu


def max_entitlement(gmu, msu):
    return min(gmu, msu)


def format_70df(df: pd.DataFrame) -> dict:
    """Format smf70 JSON files to the dataframes.

    Args:
        df: JSON dataframe.

    Returns:
        A dictionary of dataframes.
    """
    str_2_dict = np.vectorize(str2dict)
    get_cpu_type = np.vectorize(getcputype)
    cal_rate = np.vectorize(calrate, otypes=[float])
    cal_total_log_proc_share_pct = np.frompyfunc(calculate_total_log_proc_share_pct, 3, 1)
    get_min_entitlement = np.frompyfunc(min_entitlement, 7, 1)
    get_max_entitlement = np.frompyfunc(max_entitlement, 2, 1)
    convert_to_list = np.vectorize(converttolist)

    dfs_dict = {'pro': pd.DataFrame(), 'ctl': pd.DataFrame(), 'cpu': pd.DataFrame(), 'aid': pd.DataFrame(),
                'bct': pd.DataFrame(), 'bpd': pd.DataFrame(), 'trg': pd.DataFrame(), 'ccf': pd.DataFrame(),
                'typ3': pd.DataFrame(), 'typ4': pd.DataFrame(), 'typ5': pd.DataFrame(), 'wc': pd.DataFrame()}

    if 'smf70cis' not in df.columns:
        return dfs_dict

    df['isFirst'] = True
    dfs_dict['pro'] = build_pro(df)

    if dfs_dict['pro'] is None:
        # Cannot continue processing
        return dfs_dict

    df.set_index(dfs_dict['pro'].index, inplace=True)

    if '70.1' in dfs_dict['pro'].index.get_level_values('smf_type'):  # Contains subtype 1 records
        dfs_dict['ctl'] = build_ctl(df)

        dfs_dict['aid'] = build_aid(df, dfs_dict['ctl'][dfs_dict['ctl']['isFirst']].index)

        dfs_dict['trg'] = build_trg(df, dfs_dict['ctl'][dfs_dict['ctl']['isFirst']].index)

        ctl_idx = dfs_dict['ctl'].reset_index().set_index(
            ['csc', 'smf70sid', 'datetime', 'smf70ist', 'smf70iet', 'smf70int', 'smf70dsa',
             'smf70cpa_actual', 'smf70cpa_scaling_factor', 'smf70ptn', 'smf70xnm', 'smf70snm',
             'cpa_scaling_factor_effective', 'cpu_adjustment_factor_effective',
             'cpu_count_CP', 'cpu_count_IFL', 'cpu_count_ICF', 'cpu_count_IIP', 'cpu_count_CBP',
             'cpu_count_IFA', 'cisdict']).index
        dfs_dict['bct'] = build_bct(df, ctl_idx)

        dfs_dict['bpd'] = build_bpd(df, dfs_dict['pro'][
            dfs_dict['pro'].index.get_level_values('smf_type') == '70.1'].reset_index().set_index(
            ['csc', 'datetime', 'smf70ist', 'smf70iet', 'smf70sid', 'smf70xnm']).index)

        if dfs_dict['bct'].shape[0] > 0:
            dfs_dict['bctbpd'] = dfs_dict['bct'][dfs_dict['bct']['smf70bdn'] > 0].reset_index().set_index(
                ['csc', 'datetime', 'smf70ist', 'smf70iet', 'smf70sid', 'index', 'bct_idx'])[
                ['lpar_system_name', 'lpar_number', 'sysplex_name', 'system_name', 'smf70lpm',
                 'smf70dsa', 'cisdict', 'cpa_scaling_factor_effective',
                 'cpu_adjustment_factor_effective', 'smf70cpa_scaling_factor', 'smf70cpa_actual',
                 'cpu_count_CP', 'cpu_count_IFL', 'cpu_count_ICF', 'cpu_count_IIP', 'cpu_count_CBP',
                 'cpu_count_IFA',
                 'smf70int', 'smf70bds', 'smf70bdn', 'smf70stn', 'smf70lpn']]
            dfs_dict['bctbpd'] = dfs_dict['bctbpd'].reindex(dfs_dict['bctbpd'].index.repeat(dfs_dict['bctbpd'].smf70bdn))
            dfs_dict['bctbpd']['bpd_idx'] = dfs_dict['bctbpd'].groupby(
                ['csc', 'smf70sid', 'datetime', 'smf70ist', 'smf70iet', 'index', 'bct_idx']
            ).cumcount() + dfs_dict['bctbpd']['smf70bds']
            dfs_dict['bctbpd'] = dfs_dict['bctbpd'].reset_index().set_index(
                ['csc', 'smf70sid', 'datetime', 'smf70ist', 'smf70iet', 'index', 'bpd_idx'])

            dfs_dict['bpd'] = dfs_dict['bctbpd'].join(dfs_dict['bpd'])
            dfs_dict['bpd']['smf70ont'] = np.where(
                (dfs_dict['bpd']['smf70ont'] == 0) & (dfs_dict['bpd']['smf70pdt'] > 0),
                dfs_dict['bpd']['smf70int'], dfs_dict['bpd']['smf70ont'])
            dfs_dict['bpd']['cisdict'] = str_2_dict(dfs_dict['bpd']['cisdict'])
            dfs_dict['bpd']['smf70cix'] = get_cpu_type(dfs_dict['bpd']['smf70cix'], dfs_dict['bpd']['cisdict'])
            dfs_dict['bpd']['share_current'] = cal_rate(dfs_dict['bpd']['smf70acs'] * 1e2, dfs_dict['bpd']['smf70dsa'])
            dfs_dict['bpd']['cpu_count'] = dfs_dict['bpd'][dfs_dict['bpd']['smf70ont'] > 0].groupby(
                ['csc', 'lpar_system_name', 'datetime', 'smf70ist', 'smf70iet', 'smf70sid',
                 'smf70cix']).cumcount()
            dfs_dict['bpd']['cpu_count'] = dfs_dict['bpd'][dfs_dict['bpd']['smf70ont'] > 0].groupby(
                ['csc', 'lpar_system_name', 'datetime', 'smf70ist', 'smf70iet', 'smf70sid', 'smf70cix'])[
                                      'cpu_count'].transform('max') + 1
            dfs_dict['bpd']['physical_cpu_count'] = np.where(dfs_dict['bpd']['smf70cix'] == 'CP', dfs_dict['bpd']['cpu_count_CP'],
                                                             np.where(dfs_dict['bpd']['smf70cix'] == 'IIP',
                                                                      dfs_dict['bpd']['cpu_count_IIP'],
                                                                      np.where(dfs_dict['bpd']['smf70cix'] == 'ICF',
                                                                               dfs_dict['bpd']['cpu_count_ICF'],
                                                                               np.where(
                                                                                   dfs_dict['bpd']['smf70cix'] == 'IFL',
                                                                          dfs_dict['bpd']['cpu_count_IFL'],
                                                                          np.where(dfs_dict['bpd'][
                                                                                       'smf70cix'] == 'CBP',
                                                                                   dfs_dict['bpd']['cpu_count_CBP'],
                                                                                   np.where(dfs_dict['bpd'][
                                                                                                'smf70cix'] == 'IFA',
                                                                                            dfs_dict['bpd'][
                                                                                                'cpu_count_IFA'],
                                                                                            np.nan))))))
            dfs_dict['bpd']['logical_processor_is_online'] = (dfs_dict['bpd']['smf70ont'] > 0).astype(
                int)
            dfs_dict['bpd']['msu_physical'] = dfs_dict['bpd']['smf70pdt'] * 16 * dfs_dict['bpd'][
                'cpa_scaling_factor_effective'] / dfs_dict['bpd']['cpu_adjustment_factor_effective'] \
                                              * 3.6 / dfs_dict['bpd']['smf70int']
            dfs_dict['bpd']['msu_effective'] = dfs_dict['bpd']['smf70edt'] * 16 * dfs_dict['bpd'][
                'cpa_scaling_factor_effective'] / dfs_dict['bpd']['cpu_adjustment_factor_effective'] \
                                               * 3.6 / dfs_dict['bpd']['smf70int']
            dfs_dict['bpd']['lpar_management_per_cpu'] = (100 * (
                    dfs_dict['bpd']['smf70pdt'] - dfs_dict['bpd']['smf70edt']) / dfs_dict['bpd'][
                                                     'smf70int']
                                                          ) / dfs_dict['bpd']['physical_cpu_count'].where(
                dfs_dict['bpd']['physical_cpu_count'] > 0, np.nan)
            dfs_dict['bpd']['lpar_management_per_cpu'] = np.where(
                (dfs_dict['bpd']['lpar_management_per_cpu'].isnull()) & (dfs_dict['bpd']['smf70pdt'] > 0),
                0, dfs_dict['bpd']['lpar_management_per_cpu'])
            dfs_dict['bpd']['processor_weight_online'] = np.where(
                (dfs_dict['bpd']['smf70ont'] > 0) & (dfs_dict['bpd']['physical_cpu_count'] > 0),
                dfs_dict['bpd']['smf70bps'], 0)
            dfs_dict['bpd']['utilization_per_cpu_physical'] = (100 * dfs_dict['bpd']['smf70pdt'] / dfs_dict['bpd'][
                'smf70ont']
                                                               ) / dfs_dict['bpd']['physical_cpu_count'].where(
                (dfs_dict['bpd']['physical_cpu_count'] > 0) & (dfs_dict['bpd']['smf70ont'] > 0), np.nan)
            dfs_dict['bpd'].drop(columns=['cisdict'], inplace=True)

            dfs_dict['bct_cpu'] = build_bct_cpu(dfs_dict['bpd'])

            piv_columns = ['wgt', 'smf70bps', 'high_polarization', 'med_polarization',
                           'smf70edt_total', 'smf70pdt',
                           'lpar_management_total', 'physical_processor_effective_total',
                           'physical_processor_total_total', 'cpu_count',
                           'defined_cpu_count', 'smf70acs', 'total_smf70acs']
            bct_cpu_piv = dfs_dict['bct_cpu'].rename(
                columns={'smf70edt': 'smf70edt_total',
                         'lpar_management_per_cpu': 'lpar_management_total',
                         'physical_processor_effective': 'physical_processor_effective_total',
                         'physical_processor_total': 'physical_processor_total_total'}
            ).reset_index().pivot(
                index=['csc', 'lpar_system_name', 'lpar_number', 'smf70lpm', 'datetime', 'smf70ist',
                       'smf70iet', 'smf70sid'],  # 'mtid',
                columns='smf70cix', values=piv_columns).reset_index().set_index(
                ['csc', 'lpar_system_name', 'lpar_number', 'smf70lpm', 'datetime', 'smf70ist', 'smf70iet',
                 'smf70sid'])  # 'mtid',

            bct_cpu_piv.columns = ['_'.join(str(s.lower()).strip() for s in col if s) for col in
                                   bct_cpu_piv.columns]
            bct_cpu_piv_wgt_cols = [col for col in bct_cpu_piv if col.startswith('wgt_')]
            bct_cpu_piv = bct_cpu_piv.reset_index().set_index(
                ['csc', 'datetime', 'smf70ist', 'smf70iet', 'smf70sid']).join(
                bct_cpu_piv.groupby(
                    ['csc', 'datetime', 'smf70ist', 'smf70iet', 'smf70sid'])[bct_cpu_piv_wgt_cols].agg(
                    agg_sum_processor_weight).rename(
                    columns={'wgt_cp': 'total_weight_cp', 'wgt_icf': 'total_weight_icf',
                             'wgt_iip': 'total_weight_iip', 'wgt_aap': 'total_weight_aap',
                             'wgt_ifl': 'total_weight_ifl'})
            ).reset_index().set_index(
                ['csc', 'lpar_system_name', 'lpar_number', 'smf70lpm', 'datetime', 'smf70ist', 'smf70iet',
                 'smf70sid'])

            dfs_dict['bct'] = dfs_dict['bct'].join(bct_cpu_piv.reset_index().drop(columns=['smf70lpm']).set_index(  # ,'mtid'
                [col.name for col in Smf70Bct.__table__.primary_key.columns.values()]))
            bct_wgt_cols = [col[4:] for col in dfs_dict['bct'] if col.startswith('wgt_')]
            for cpu_type in bct_wgt_cols:
                dfs_dict['bct'][f'med_polarization_{cpu_type}'] = dfs_dict['bct'][f'med_polarization_{cpu_type}'].astype(
                    'float')
                dfs_dict['bct'][f'high_polarization_{cpu_type}'] = dfs_dict['bct'][f'high_polarization_{cpu_type}'].astype(
                    'float')

                dfs_dict['bct'][f'total_log_proc_share_{cpu_type}'] = cal_total_log_proc_share_pct(
                    dfs_dict['bct'][f'smf70bps_{cpu_type}'],
                    dfs_dict['bct'][f'total_weight_{cpu_type}'],
                    dfs_dict['bct'][f'cpu_count_{cpu_type.upper()}'])
                dfs_dict['bct'][f'total_log_proc_share_{cpu_type}'] = dfs_dict['bct'][
                    f'total_log_proc_share_{cpu_type}'].astype('float')
                dfs_dict['bct'][f'med_log_proc_share_{cpu_type}'] = ((dfs_dict['bct'][f'total_log_proc_share_{cpu_type}'] -
                                                                      dfs_dict['bct'][f'high_polarization_{cpu_type}'] * 100)
                                                                     / dfs_dict['bct'][f'med_polarization_{cpu_type}']).where(
                    (dfs_dict['bct'][f'total_log_proc_share_{cpu_type}'].notnull()) & (
                        dfs_dict['bct'][f'med_polarization_{cpu_type}'].notnull()
                    ) & (dfs_dict['bct'][f'high_polarization_{cpu_type}'].notnull()
                         ) & (dfs_dict['bct'][f'med_polarization_{cpu_type}'] > 0), 0)
            dfs_dict['bct']['init_weight'] = dfs_dict['bct']['smf70pfl'].apply(lambda x: is_bit_set(x, 8, 3))
            dfs_dict['bct']['min_entitlement'] = get_min_entitlement(dfs_dict['bct']['init_weight'], dfs_dict['bct']['smf70msu'],
                                                                     dfs_dict['bct']['smf70gmu'],
                                                                     dfs_dict['bct']['smf70bps_cp'],
                                                                     dfs_dict['bct']['total_weight_cp'],
                                                                     dfs_dict['bct']['smf70acs_cp'],
                                                                     dfs_dict['bct']['total_smf70acs_cp'])
            dfs_dict['bct']['max_entitlement'] = get_max_entitlement(dfs_dict['bct']['smf70gmu'], dfs_dict['bct']['smf70msu'])
            if 'wgt_icf' in dfs_dict['bct'].columns:
                dfs_dict['bct']['is_CF'] = np.where(
                    (dfs_dict['bct']['wgt_icf'].notnull()) & (dfs_dict['bct']['smf70lpm'] != 'PHYSICAL'), 1, 0)
            else:
                dfs_dict['bct']['is_CF'] = 0

            wgt_columns = ['lpar_system_name', 'lpar_number', 'smf70lpm', 'smf70mtid',
                           'wgt_cp', 'wgt_ifl', 'wgt_iip', 'wgt_icf', 'wgt_aap',
                           'smf70bps_cp', 'smf70bps_ifl', 'smf70bps_iip', 'smf70bps_icf', 'smf70bps_aap',
                           'total_weight_cp', 'total_weight_ifl', 'total_weight_iip', 'total_weight_icf',
                           'total_weight_aap',
                           'total_log_proc_share_cp', 'total_log_proc_share_ifl', 'total_log_proc_share_iip',
                           'total_log_proc_share_icf', 'total_log_proc_share_aap',
                           'med_log_proc_share_cp', 'med_log_proc_share_ifl', 'med_log_proc_share_iip',
                           'med_log_proc_share_icf', 'med_log_proc_share_aap', ]
            dfs_dict['ctl'] = dfs_dict['ctl'].join(
                dfs_dict['bct'][dfs_dict['bct'].index.get_level_values('lpar_number') == dfs_dict['ctl']['smf70ptn'].unique()[0]
                                ].reset_index().set_index(
                    [col.name for col in Smf70Ctl.__table__.primary_key.columns.values()])[
                    [col for col in wgt_columns if col in dfs_dict['bct'].reset_index().columns]])

            sum_columns = ['smf70edt_total_cp', 'smf70edt_total_ifl', 'smf70edt_total_iip',
                           'smf70edt_total_icf', 'smf70edt_total_aap',
                           'smf70pdt_cp', 'smf70pdt_ifl', 'smf70pdt_iip', 'smf70pdt_icf', 'smf70pdt_aap',
                           'lpar_management_total_cp', 'lpar_management_total_ifl', 'lpar_management_total_iip',
                           'lpar_management_total_icf', 'lpar_management_total_aap',
                           'physical_processor_effective_total_cp', 'physical_processor_effective_total_ifl',
                           'physical_processor_effective_total_iip', 'physical_processor_effective_total_icf',
                           'physical_processor_effective_total_aap',
                           'physical_processor_total_total_cp', 'physical_processor_total_total_ifl',
                           'physical_processor_total_total_iip',
                           'physical_processor_total_total_icf', 'physical_processor_total_total_aap']
            agg_sum_columns = dict([(k, 'sum') for k in [
                col for col in sum_columns if col in dfs_dict['bct'].reset_index().columns]])
            df_bct_gp = dfs_dict['bct'][dfs_dict['bct']['smf70bdn'] > 0][
                [col for col in sum_columns if col in dfs_dict['bct'].reset_index().columns]].reset_index().groupby(
                [col.name for col in Smf70Ctl.__table__.primary_key.columns.values()]).agg(agg_sum_columns)
            dfs_dict['ctl'] = dfs_dict['ctl'].join(df_bct_gp)

        dfs_dict['cpu'] = build_cpu(df, dfs_dict['ctl'])
        set_cpu_polarization = np.vectorize(extract_cpu_polarization)

        if dfs_dict['cpu'].shape[0] > 0:
            if 'smf70lcs' in df.columns:
                ctl_columns = ['csc', 'datetime', 'smf70ist', 'smf70iet', 'smf70sid', 'smf70xnm', 'lpar_system_name',
                               'smf70ptn']
                z_idx_columns = ctl_columns + ['index']
                d = dfs_dict['ctl'].reset_index().reset_index().set_index(ctl_columns)
                z = df[(df.index.get_level_values('smf_type') == '70.1') & (df['isFirst'])].reset_index()[
                    'smf70lcs'].to_frame().set_index(
                    d[d['isFirst']].reset_index().set_index(z_idx_columns).index)
                z.dropna(how='all', inplace=True)
                z['smf70lcs'] = convert_to_list(z['smf70lcs'])
                z = z.reset_index().set_index(
                    ['csc', 'smf70sid', 'datetime', 'smf70ist', 'lpar_system_name', 'smf70ptn', 'smf70iet', 'index'])
                x = z.explode('smf70lcs').reset_index()
                x['lcs_idx'] = x.groupby(
                    ['datetime', 'smf70ist', 'smf70iet', 'smf70sid', 'lpar_system_name', 'smf70ptn',
                     'index']).cumcount()
                x.set_index(
                    ['csc', 'datetime', 'smf70ist', 'smf70iet', 'smf70sid', 'lpar_system_name', 'smf70ptn', 'index',
                     'lcs_idx'], inplace=True)
                df_lcs = pd.json_normalize(x['smf70lcs']).set_index(x.index)
                df_lcs['smf70_core_flg'] = df_lcs['smf70_core_flg'].apply(lambda x: int(x, 16))
                df_lcs['lpb_valid'] = df_lcs['smf70_core_flg'].apply(lambda x: is_bit_set(x, 8, 0))
                df_lcs['smf70_lpar_busy'] = pd.to_timedelta(df_lcs['smf70_lpar_busy']) / np.timedelta64(1, 's')
                df_lcs = df_lcs.reset_index().set_index(
                    ['csc', 'smf70sid', 'datetime', 'smf70ist', 'smf70iet', 'index', 'smf70_core_id'])
                df_lcs = df_lcs.reindex(df_lcs.index.repeat(df_lcs.smf70_cpu_num))
                df_lcs['sub_core_idx'] = df_lcs.groupby(
                    ['csc', 'smf70sid', 'datetime', 'smf70ist', 'smf70iet', 'index', 'smf70_core_id']).cumcount()
                df_lcs = pd.concat([df_lcs[df_lcs['sub_core_idx'] == 0].join(
                    dfs_dict['bpd'][dfs_dict['bpd']['lpar_number'] == df_lcs['smf70ptn'].unique()[0]].reset_index().rename(
                        columns={'bpd_idx': 'smf70_core_id'}).set_index(
                        ['csc', 'smf70sid', 'datetime', 'smf70ist', 'smf70iet', 'index', 'smf70_core_id']).drop(
                        columns=['lpar_system_name', 'smf70int'])),
                    df_lcs[df_lcs['sub_core_idx'] != 0]]).sort_index()
                df_lcs['cpu_idx'] = df_lcs.groupby(
                    ['csc', 'lpar_system_name', 'smf70ptn', 'datetime', 'smf70ist', 'smf70iet',
                     'smf70sid']).cumcount()
                df_lcs = df_lcs.reset_index().set_index(
                    ['csc', 'smf70sid', 'datetime', 'smf70ist', 'smf70iet', 'index', 'cpu_idx'])

                dfs_dict['cpu'] = df_lcs.join(dfs_dict['cpu'].drop(columns=['lpar_system_name', 'smf70ptn']))
            else:
                dfs_dict['cpu']['sub_core_idx'] = 0
                dfs_dict['cpu'] = dfs_dict['cpu'].join(
                    dfs_dict['bpd'][dfs_dict['bpd']['lpar_number'] == dfs_dict['cpu']['smf70ptn'].unique()[0]].reset_index().rename(
                        columns={'bpd_idx': 'cpu_idx'}).set_index(
                        ['csc', 'smf70sid', 'datetime', 'smf70ist', 'smf70iet', 'index', 'cpu_idx']).drop(
                        columns=['lpar_system_name', 'smf70int']))
            dfs_dict['cpu']['smf70ont'] = np.where(dfs_dict['cpu']['smf70ont'] > 0,
                                                   dfs_dict['cpu']['smf70ont'],
                                                   np.where(dfs_dict['cpu']['smf70pdt'] > 0,
                                                            dfs_dict['cpu']['smf70int'], 0))
            dfs_dict['cpu']['hd_active'] = dfs_dict['cpu']['smf70hhf'].apply(lambda x: is_bit_set(x, 8, 1))
            dfs_dict['cpu']['wait_completion_status'] = dfs_dict['cpu']['smf70vpf'].apply(lambda x: is_bit_set(int(x), 8, 0) if not pd.isna(x) else np.nan)
            dfs_dict['cpu']['cpu_polarization'] = set_cpu_polarization(dfs_dict['cpu']['smf70pof'])
            dfs_dict['cpu']['cpu_is_online'] = dfs_dict['cpu']['smf70cnf'].apply(lambda x: is_bit_set(x, 8, 7))

            dfs_dict['cpu']['cpu_time'] = np.where(
                (dfs_dict['cpu']['smf70bps'] == 'DED') & (dfs_dict['cpu']['smf70hhf'] & 1 != 1),
                dfs_dict['cpu']['smf70int'] - dfs_dict['cpu']['smf70wat'],
                np.where(dfs_dict['cpu']['wait_completion_status'].notnull() & (dfs_dict['cpu']['hd_active'] != 1) & (
                        dfs_dict['cpu']['wait_completion_status'] == 1),
                         dfs_dict['cpu']['smf70pdt'] - dfs_dict['cpu']['smf70wat'],
                         np.where(dfs_dict['cpu']['wait_completion_status'].notnull() & (
                                 dfs_dict['cpu']['wait_completion_status'] != 1),
                                  dfs_dict['cpu']['smf70pdt'],
                                  dfs_dict['cpu']['smf70_lpar_busy'])))
            dfs_dict['cpu']['lpar_busy_percentage'] = np.where(dfs_dict['cpu']['cpu_time'].notnull(),
                                                               dfs_dict['cpu']['cpu_time'] / dfs_dict['cpu']['smf70int'] * 100, np.nan)
            dfs_dict['cpu']['mt_util'] = ((dfs_dict['cpu']['smf70_prod'] / 1024) * dfs_dict['cpu']['lpar_busy_percentage']).where(
                (dfs_dict['cpu']['cpu_is_online'] == 1) & (dfs_dict['cpu']['multithreading'] == 1), np.nan)
            dfs_dict['cpu']['mt_prod'] = ((dfs_dict['cpu']['smf70_prod'] / 1024) * 100).where(dfs_dict['cpu']['cpu_is_online'] == 1,
                                                                                              np.nan)
            dfs_dict['cpu']['cpu_unparked_time'] = (dfs_dict['cpu']['smf70int'] - dfs_dict['cpu']['smf70pat']).clip(lower=0)
            dfs_dict['cpu']['cpu_busy_time'] = (
                    dfs_dict['cpu']['smf70int'] - dfs_dict['cpu']['smf70wat'] - dfs_dict['cpu']['smf70pat']).clip(
                lower=0)
            dfs_dict['cpu']['cpu_parked_percentage'] = (dfs_dict['cpu']['smf70pat'] / dfs_dict['cpu']['smf70int'] * 100).clip(
                upper=100)
            dfs_dict['cpu']['cpu_unparked_percentage'] = (
                    dfs_dict['cpu']['cpu_unparked_time'] / dfs_dict['cpu']['smf70int'] * 100).clip(upper=100)
            dfs_dict['cpu']['time_range'] = np.where(dfs_dict['cpu']['hd_active'] == 1,
                                                     dfs_dict['cpu']['smf70int'] - dfs_dict['cpu']['smf70pat'],
                                                     dfs_dict['cpu']['smf70int'])
            dfs_dict['cpu']['time_range'] = dfs_dict['cpu']['time_range'].clip(lower=0)
            dfs_dict['cpu']['mvs_busy_percentage'] = np.where(dfs_dict['cpu']['cpu_unparked_percentage'] > 0.1,
                                                              (dfs_dict['cpu']['time_range'] - dfs_dict['cpu']['smf70wat']) /
                                                              dfs_dict['cpu']['time_range'] * 100, np.nan)
            dfs_dict['cpu']['cpu_busy_percentage'] = (
                    dfs_dict['cpu']['cpu_busy_time'] * dfs_dict['cpu']['cpu_unparked_percentage'] / dfs_dict['cpu'][
                'cpu_unparked_time'] * 100).where(
                dfs_dict['cpu']['cpu_unparked_time'] > 0, 0)

            dfs_dict['cpu']['mvs_busy_unpark_total'] = (dfs_dict['cpu']['cpu_unparked_percentage'] / 100).where(
                dfs_dict['cpu']['cpu_is_online'] == 1, np.nan)
            dfs_dict['cpu']['mvs_busy_total'] = (
                    dfs_dict['cpu']['mvs_busy_percentage'] * dfs_dict['cpu']['cpu_unparked_percentage'] / 100).where(
                dfs_dict['cpu']['cpu_is_online'] == 1,
                np.nan)

            cpu_group_columns = [col.name for col in Smf70Ctl.__table__.primary_key.columns.values()] + [
                'smf70typ']
            df_cpu_gp = dfs_dict['cpu'].groupby(cpu_group_columns).agg(
                multithreading=('multithreading', 'first'),
                mvs_busy_unpark_total=('cpu_unparked_percentage', 'sum'),
                mvs_busy_total=('mvs_busy_total', 'sum'))
            df_cpu_gp['mvs_busy_unpark_total'] = df_cpu_gp['mvs_busy_unpark_total'] / 100
            df_cpu_gp['mvs_busy_total'] = df_cpu_gp['mvs_busy_total'] / df_cpu_gp['mvs_busy_unpark_total']
            df_cpu_gp['mt_prod_total'] = dfs_dict['cpu'][dfs_dict['cpu']['sub_core_idx'] == 0].groupby(cpu_group_columns)[
                'mt_prod'].mean()
            df_cpu_gp['mt_util_total'] = dfs_dict['cpu'][dfs_dict['cpu']['sub_core_idx'] == 0].groupby(cpu_group_columns)[
                'mt_util'].mean()
            df_cpu_gp['lpar_busy_total'] = dfs_dict['cpu'][dfs_dict['cpu']['sub_core_idx'] == 0].groupby(cpu_group_columns)[
                'lpar_busy_percentage'].mean()
            df_cpu_gp['rate_io_interrupt_total'] = \
                dfs_dict['cpu'][dfs_dict['cpu']['sub_core_idx'] == 0].groupby(cpu_group_columns)['rate_io_interrupt'].sum()
            df_cpu_gp['rate_io_interrupt_by_tpi_total'] = \
                dfs_dict['cpu'][dfs_dict['cpu']['sub_core_idx'] == 0].groupby(cpu_group_columns)['rate_io_interrupt_by_tpi'].sum()

            cpu_piv_columns = ['multithreading', 'mt_util_total', 'mt_prod_total', 'lpar_busy_total',
                               'mvs_busy_unpark_total', 'mvs_busy_total', 'rate_io_interrupt_total',
                               'rate_io_interrupt_by_tpi_total']
            cpu_gp_piv = df_cpu_gp.reset_index().pivot(
                index=[col.name for col in Smf70Ctl.__table__.primary_key.columns.values()],
                columns='smf70typ', values=cpu_piv_columns).reset_index().set_index(
                [col.name for col in Smf70Ctl.__table__.primary_key.columns.values()])
            cpu_gp_piv.columns = ['_'.join(str(s.lower()).strip() for s in col if s) for col in
                                  cpu_gp_piv.columns]

            dfs_dict['ctl'] = dfs_dict['ctl'].join(cpu_gp_piv.rename(
                columns={'multithreading_cp': 'multithreading',
                         'rate_io_interrupt_total_cp': 'rate_io_interrupt_total',
                         'rate_io_interrupt_by_tpi_total_cp': 'rate_io_interrupt_by_tpi_total'}))
            if 'mvs_busy_unpark_total_iip' in dfs_dict['ctl'].columns:
                dfs_dict['ctl']['numproc'] = dfs_dict['ctl']['mvs_busy_unpark_total_cp'] + dfs_dict['ctl']['mvs_busy_unpark_total_iip']
                dfs_dict['ctl'].drop(columns=['multithreading_iip', 'rate_io_interrupt_total_iip',
                                     'rate_io_interrupt_by_tpi_total_iip'], inplace=True)
            else:
                dfs_dict['ctl']['numproc'] = dfs_dict['ctl']['mvs_busy_unpark_total_cp']

    # subtype = 2
    if '70.2' in dfs_dict['pro'].index.get_level_values('smf_type'):  # Contains subtype 2 records
        dfs_dict['typ3'] = build_typ3(df,
                                      dfs_dict['pro'].reset_index().set_index(
                                 ['csc', 'smf70sid', 'datetime', 'smf70ist', 'smf70iet', 'smf_type', 'smf70ptn',
                                  'smf70int']).index)
        dfs_dict['typ4'] = build_typ4(df,
                                      dfs_dict['pro'].reset_index().set_index(
                                 ['csc', 'smf70sid', 'datetime', 'smf70ist', 'smf70iet', 'smf_type', 'smf70ptn',
                                  'smf70int']).index)
        dfs_dict['typ5'] = build_typ5(df,
                                      dfs_dict['pro'].reset_index().set_index(
                                 ['csc', 'smf70sid', 'datetime', 'smf70ist', 'smf70iet', 'smf_type', 'smf70ptn',
                                  'smf70int']).index)
        dfs_dict['ccf'] = build_ccf(df,
                                    dfs_dict['pro'].reset_index().set_index(
                               ['csc', 'smf70sid', 'datetime', 'smf70ist', 'smf70iet', 'smf_type',
                                'smf70ptn']).index)
    return dfs_dict

def print_crypto_activity_report(jsonfiles: tuple, lpar: str, start_time_str: str, end_time_str: str) -> str:
    """Print smf70 Crypto Activity Report based on JSON files.

    Args:
        jsonfiles: JSON file or files.
        lpar: Target LPAR to print.
        start_time_str: Start time string.
        end_time_str: End time string.

    Returns:
        CPU activity report.
    """
    start_time = pd.to_datetime(start_time_str)
    end_time = pd.to_datetime(end_time_str)
    sid = lpar

    report = ''
    for jsonfile in jsonfiles:
        page_detail = ''
        with (open(jsonfile) as f):
            try:
                df = pd.read_json(f)
            except ValueError:
                click.echo(
                    f"\nInvalid JSON file {jsonfile}. This file will be skipped.")
                continue

            if 'header' not in df.columns or not isinstance(df.iloc[0]['header'], dict) \
                    or df.iloc[0]['header'].get('recType') is None or df.iloc[0]['header']['recType'] != 70:
                click.echo(
                    f"\nInvalid JSON file {jsonfile}. This file will be skipped.")
                continue

            try:
                df_dict = format_70df(df)
            except Exception as e:
                click.echo(f"\nUnsupported JSON file {jsonfile} with error: {str(e)}. This file will be skipped.")
                continue

            if df_dict['pro'].empty:
                click.echo(
                    f"\nThis JSON file {jsonfile} is not for this smf type. This file will be skipped.")
                # Cannot continue processing
                continue

            pro = df_dict['pro'].query(
                "smf70ist > @start_time and smf70ist < @end_time and smf70sid == @sid and smf_type == '70.2'"
            ).copy().reset_index().set_index(
                [col.name for col in Smf70Pro.__table__.primary_key.columns.values()])

            if pro.empty:
                continue

            pro = pro.loc[~pro.index.duplicated(keep='first'), :]

            typ3 = df_dict['typ3'].query("smf70ist > @start_time and smf70ist < @end_time and smf70sid == @sid"
                                         ).copy().reset_index().set_index(
                [col.name for col in Smf70Pro.__table__.primary_key.columns.values()])
            typ4 = df_dict['typ4'].query("smf70ist > @start_time and smf70ist < @end_time and smf70sid == @sid"
                                         ).copy().reset_index().set_index(
                [col.name for col in Smf70Pro.__table__.primary_key.columns.values()])
            typ5 = df_dict['typ5'].query("smf70ist > @start_time and smf70ist < @end_time and smf70sid == @sid"
                                         ).copy().reset_index().set_index(
                [col.name for col in Smf70Pro.__table__.primary_key.columns.values()])
            ccf = df_dict['ccf'].query("smf70ist > @start_time and smf70ist < @end_time and smf70sid == @sid"
                                       ).copy().reset_index().set_index(
                [col.name for col in Smf70Pro.__table__.primary_key.columns.values()])

            if 'r702dqgc' not in ccf.columns:
                ccf['r702dqgc'], ccf['r702dqvc'], ccf['r702fxec'], ccf['r702fxdc'], ccf['r702fxtc'] = np.nan, np.nan, np.nan, np.nan, np.nan
            for index in pro.index:
                if typ3.empty:
                    typ3_dict = []
                elif index not in typ3.index:
                    typ3_dict = []
                else:
                    typ3_dict = typ3.loc[[index]].to_dict('records')
                if typ4.empty:
                    typ4_dict = []
                elif index not in typ4.index:
                    typ4_dict = []
                else:
                    typ4_dict = typ4.loc[[index]].to_dict('records')
                if typ5.empty:
                    typ5_dict = []
                elif index not in typ5.index:
                    typ5_dict = []
                else:
                    typ5_dict = typ5.loc[[index]].to_dict('records')
                if ccf.empty:
                    ccf_dict = None
                elif index not in ccf.index:
                    ccf_dict = None
                else:
                    ccf_dict = ccf.loc[[index]].to_dict('records')[0]

                pro_dict = pro.loc[[index]].reset_index().to_dict('records')[0]
                report_cca = format_cca_coprocessor_detail(typ3_dict)
                report_pkcs11 = format_pkcs11_coprocessor_detail(typ5_dict)
                report_accelerator = format_accelerator_detail(typ4_dict)
                ccf_detail = format_ccf_detail(pro_dict, ccf_dict)
                page_sub_detail = None
                if report_cca is not None or report_cca is not None or report_pkcs11 is not None or \
                        report_accelerator is not None or ccf_detail is not None:
                    page_sub_detail = format_crypto_header(pro_dict)

                if report_cca is not None:
                    page_sub_detail += report_cca
                if report_pkcs11 is not None:
                    page_sub_detail += report_pkcs11
                if report_accelerator is not None:
                    page_sub_detail += report_accelerator
                if ccf_detail is not None:
                    page_sub_detail += ccf_detail

                if page_sub_detail is not None:
                    if page_detail != '':
                        page_detail += '\n\n'
                    page_detail += page_sub_detail
            if page_detail is not None:
                if report != '':
                    report += '\n\n'
                report += page_detail

    if report == '':
        report = 'No data found.'
    return report

def print_cpu_activity_report(jsonfiles: tuple, lpar: str, start_time_str: str, end_time_str: str) -> str:
    """Print smf70 CPU Activity Report based on JSON files.

    Args:
        jsonfiles: JSON file or files.
        lpar: Target LPAR to print.
        start_time_str: Start time string.
        end_time_str: End time string.

    Returns:
        CPU activity report.
    """
    start_time = pd.to_datetime(start_time_str)
    end_time = pd.to_datetime(end_time_str)
    sid = lpar

    report = ''
    for jsonfile in jsonfiles:
        with open(jsonfile) as f:
            try:
                df = pd.read_json(f)
            except ValueError:
                click.echo(
                    f"\nInvalid JSON file {jsonfile}. This file will be skipped.")
                continue

            if 'header' not in df.columns or not isinstance(df.iloc[0]['header'], dict) \
                    or df.iloc[0]['header'].get('recType') is None or df.iloc[0]['header']['recType'] != 70:
                click.echo(
                    f"\nInvalid JSON file {jsonfile}. This file will be skipped.")
                continue

            try:
                df_dict = format_70df(df)
            except Exception as e:
                click.echo(f"\nUnsupported JSON file {jsonfile} with error: {str(e)}. This file will be skipped.")
                continue

            if df_dict['pro'].empty:
                click.echo(
                    f"\nThis JSON file {jsonfile} is not for this smf type. This file will be skipped.")
                # Cannot continue processing
                continue

            if df_dict['ctl'].empty:
                click.echo(
                    f"\nThis JSON file {jsonfile} is not for this smf type. This file will be skipped.")
                # Cannot continue processing
                continue

            ctl = df_dict['ctl'].query("smf70ist > @start_time and smf70ist < @end_time and smf70sid == @sid").copy()
            if ctl.empty:
                continue
            ctl = ctl.loc[~ctl.index.duplicated(keep='first'), :]
            pro = df_dict['pro'].query(
                "smf70ist > @start_time and smf70ist < @end_time and smf70sid == @sid and smf_type == '70.1'"
            ).drop_duplicates().copy().reset_index().set_index(
                [col.name for col in Smf70Ctl.__table__.primary_key.columns.values()])
            cpu = df_dict['cpu'].query("smf70ist > @start_time and smf70ist < @end_time and smf70sid == @sid"
                                       ).drop_duplicates().copy().reset_index().set_index(
                [col.name for col in Smf70Ctl.__table__.primary_key.columns.values()])
            bct = df_dict['bct'].query(
                "smf70ist > @start_time and smf70ist < @end_time and smf70sid == @sid").drop_duplicates().copy()
            bct_cpu_gp = df_dict['bct_cpu'].query("smf70ist > @start_time and smf70ist < @end_time and smf70sid == @sid"
                                                  ).reset_index().groupby(
                [col.name for col in Smf70Bct.__table__.primary_key.columns.values()])

            bct_cpus_list = []
            for index in bct.index:
                if index in bct_cpu_gp.groups:
                    bct_cpus_list.append(bct_cpu_gp.get_group(index).to_dict('records'))
                else:
                    bct_cpus_list.append([])

            bct['bct_cpus'] = bct_cpus_list

            bct = bct.reset_index().set_index(
                [col.name for col in Smf70Ctl.__table__.primary_key.columns.values()])

            aid = df_dict['aid'].query("smf70ist > @start_time and smf70ist < @end_time and smf70sid == @sid"
                                       ).drop_duplicates().copy().reset_index().set_index(
                [col.name for col in Smf70Ctl.__table__.primary_key.columns.values()])
            bct['wlm_active'] = bct['smf70pfg'].apply(lambda x: is_bit_set(x, 8, 4))
            bct['capacity_group_member'] = bct['smf70pfl'].apply(lambda x: is_bit_set(x, 8, 1))

            wlm_active_bct = bct.query("wlm_active == 1")
            capacity_group_bct = bct.query("capacity_group_member == 1")

            page_detail = ''
            for index in ctl.index:
                ctl_dict = ctl.loc[[index]].reset_index().to_dict('records')[0]

                pro_dict = pro.loc[[index]].reset_index().to_dict('records')[0]
                aid_dict = aid.loc[[index]].to_dict('records')[0]
                cpus_dict = cpu.loc[[index]].to_dict('records')
                bcts_dict = bct.loc[[index]].to_dict('records')
                if wlm_active_bct.shape[0] <= 1:
                    wlm_active_bct_dict = wlm_active_bct.reset_index().to_dict('records')
                else:
                    wlm_active_bct_dict = wlm_active_bct.loc[[index]].reset_index().to_dict('records')
                if capacity_group_bct.shape[0] <= 1:
                    capacity_group_bct_dict = capacity_group_bct.reset_index().to_dict('records')
                else:
                    capacity_group_bct_dict = capacity_group_bct.loc[[index]].reset_index().to_dict('records')

                page_detail += format_cpu_activity(ctl_dict,
                                                  pro_dict,
                                                  cpus_dict)  # .replace('nan', '---')
                page_detail += '\n\n'
                page_detail += format_aid_analysis(ctl_dict,
                                                   pro_dict,
                                                   aid_dict)
                page_detail += '\n\n'
                page_detail += format_partition_report(ctl_dict,
                                                       pro_dict,
                                                       bcts_dict)
                page_detail += '\n\n'
                page_detail += format_lpar_cluster_report(ctl_dict,
                                                          pro_dict,
                                                          wlm_active_bct_dict)
                page_detail += '\n\n'
                page_detail += format_group_capacity_report(ctl_dict,
                                                            pro_dict,
                                                            capacity_group_bct_dict)
            if page_detail != '':
                if report != '':
                    report += '\n\n'
                report += page_detail
    if report == '':
        report = 'No data found.'
    return report

