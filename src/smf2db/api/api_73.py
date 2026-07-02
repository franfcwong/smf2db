from typing import Union

import click
import numpy as np
import pandas as pd

from smf2db.api.report_util import format_channel_activity_report, is_bit_set, extractKBits
from smf2db.api.util import setdatetime, to_int, ebcdic2ascii, col_to_frame
from smf2db.db_models.smf73_model import Smf73Ctl


def calspd(msc, spd):
    if msc > 0:
        return spd * (10 ** msc)
    else:
        return spd * 100 * 1e6


def build_pro(df: pd.DataFrame) -> Union[pd.DataFrame, None]:
    """Build the dataframe for RMF Product Section which will be uploaded to smf73_pro table.

    Args:
        df: The master dataframe which is created from the JSON file.

    Returns:
        The dataframe for the RMF product section or None if csc is not found in the database.
    """
    set_datetime = np.vectorize(setdatetime)

    df_pro = pd.concat([df['header'].apply(pd.Series),
                        df['smf73pro'].apply(pd.Series)],
                       axis=1).rename(
        columns={'sysId': 'smf73sid',
                 'sysInd': 'smf73flg', 'recType': 'smf_type'})

    df_pro['csc'] = np.nan
    df_pro['smf73sid'] = df_pro['smf73sid'].str.strip()
    df_pro['smf73ist'] = pd.to_datetime(df_pro['smf73ist'])
    df_pro['smf73gie'] = pd.to_datetime(df_pro['smf73gie'])
    df_pro['smf73int'] = pd.to_timedelta(df_pro['smf73int']) / np.timedelta64(1, 's')
    df_pro['smf73lgo'] = pd.to_timedelta(df_pro['smf73lgo']) / np.timedelta64(1, 'h')
    df_pro['datetime'] = set_datetime(df_pro['smf73ist'])
    df_pro['smf73flg'] = df_pro['smf73flg'].apply(lambda x: int(str(x), 16))
    df_pro['smf73fla'] = df_pro['smf73fla'].apply(lambda x: int(str(x), 16))
    df_pro['smf73prf'] = df_pro['smf73prf'].apply(lambda x: int(str(x), 16))
    df_pro['smf73srl'] = df_pro['smf73srl'].apply(lambda x: int(str(x), 16))
    df_pro['speed_boost'] = df_pro['smf73fla'].apply(lambda x: is_bit_set(x, 16, 10))
    df_pro['ziip_boost'] = df_pro['smf73fla'].apply(lambda x: is_bit_set(x, 16, 9))
    df_pro['smf_type'] = df_pro['smf_type'].astype(str) + '.' + df_pro['subType'].astype(str)
    df_pro = df_pro.set_index(
        ['datetime', 'smf73ist', 'smf73iet', 'smf_type', 'csc', 'smf73sid', 'smf73int'])
    return df_pro


def build_ctl(df: pd.DataFrame, df_pro_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for Channel Path Control Section which will be uploaded to smf73_ctl table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_pro_idx: The index of the RMF product section dataframe.

    Returns:
        The dataframe for the Channel Path Control section.
    """
    convert_2_int = np.vectorize(to_int)
    if 'smf73ctl' in df.columns:
        df_ctl = col_to_frame(df[df.index.get_level_values('smf_type') == '73.1'], 'smf73ctl', df_pro_idx
        ).reset_index().set_index(['csc', 'smf73sid', 'datetime', 'smf73ist', 'smf73iet'])
        df_ctl['smf73cfl'] = df_ctl['smf73cfl'].apply(lambda x: int(str(x), 16))
        df_ctl['smf73sfl'] = df_ctl['smf73sfl'].apply(lambda x: int(str(x), 16))
        df_ctl['config_changed'] = df_ctl['smf73cfl'].apply(lambda x: is_bit_set(x, 8, 0))
        df_ctl['config_changed_since_ipl'] = df_ctl['smf73cfl'].apply(lambda x: is_bit_set(x, 8, 1))
        df_ctl['ipl_iodf'] = df_ctl['smf73cfl'].apply(lambda x: is_bit_set(x, 8, 2))
        df_ctl['io_token_valid'] = df_ctl['smf73cfl'].apply(lambda x: is_bit_set(x, 8, 3))
        df_ctl['invalid_ds'] = df_ctl['smf73cfl'].apply(lambda x: is_bit_set(x, 8, 4))
        df_ctl['cpmf'] = df_ctl['smf73cfl'].apply(lambda x: is_bit_set(x, 8, 5))
        df_ctl['cpmf_changed'] = df_ctl['smf73cfl'].apply(lambda x: is_bit_set(x, 8, 7))
        df_ctl['dcm_supported'] = df_ctl['smf73sfl'].apply(lambda x: is_bit_set(x, 8, 0))
        df_ctl['dcm_ch'] = df_ctl['smf73sfl'].apply(lambda x: is_bit_set(x, 8, 1))
        df_ctl['mcs'] = df_ctl['smf73sfl'].apply(lambda x: is_bit_set(x, 8, 2))
        df_ctl['ench_ch_measurement'] = df_ctl['smf73sfl'].apply(lambda x: is_bit_set(x, 8, 3))
        df_ctl['smf73tdt'] = pd.to_datetime(df_ctl['smf73tdy'] + ' ' + df_ctl['smf73tok.smf73ttm'],
                                                 format='%m/%d/%Y %H.%M.%S',
                                                 errors='coerce')
        df_ctl['smf73tdy'] = pd.to_datetime(df_ctl['smf73tdy'], format='%m/%d/%Y', errors='coerce')
        df_ctl['smf73cmi'] = convert_2_int(df_ctl['smf73cmi'])
    else:
        df_ctl = pd.DataFrame(columns=Smf73Ctl.__table__.columns.keys()).set_index(
            ['csc', 'smf73sid', 'datetime', 'smf73ist', 'smf73iet'])
    return df_ctl


def build_cha(df: pd.DataFrame, df_pro_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for Channel Path Data Section which will be uploaded to either smf73_cha1, smf73_cha2 or smf73_cha3 table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_pro_idx: The index of the RMF product section dataframe.

    Returns:
        The dataframe for the Channel Path Data section.
    """
    cal_spd = np.vectorize(calspd)
    ebcdic_2_ascii = np.vectorize(ebcdic2ascii)
    if 'smf73cha' in df.columns:
        df_cha = col_to_frame(df[df.index.get_level_values('smf_type') == '73.1'], 'smf73cha', df_pro_idx).rename(
            columns={
                'smf73ccm.smf73tut': 'smf73tut', 'smf73ccm.smf73put': 'smf73put',
                'smf73ccm.smf73mbc': 'smf73mbc', 'smf73ccm.smf73mcu': 'smf73mcu', 'smf73ccm.smf73mwu': 'smf73mwu',
                'smf73ccm.smf73mru': 'smf73mru', 'smf73ccm.smf73us': 'smf73us',   'smf73ccm.smf73tbc': 'smf73tbc',
                'smf73ccm.smf73tuc': 'smf73tuc', 'smf73ccm.smf73puc': 'smf73puc', 'smf73ccm.smf73twu': 'smf73twu',
                'smf73ccm.smf73pwu': 'smf73pwu', 'smf73ccm.smf73tru': 'smf73tru', 'smf73ccm.smf73pru': 'smf73pru',
                'smf73ccm.smf73pdu': 'smf73pdu', 'smf73ccm.smf73tdu': 'smf73tdu', 'smf73ccm.smf73pum': 'smf73pum',
                'smf73ccm.smf73tum': 'smf73tum', 'smf73ccm.smf73pms': 'smf73pms', 'smf73ccm.smf73tms': 'smf73tms',
                'smf73ccm.smf73pus': 'smf73pus', 'smf73ccm.smf73pub': 'smf73pub', 'smf73ccm.smf73tub': 'smf73tub',
                'smf73ccm.smf73pds': 'smf73pds', 'smf73ccm.smf73tds': 'smf73tds',
                'smf73ccm.smf73g4mbc': 'smf73g4mbc','smf73ccm.smf73g4mcu': 'smf73g4mcu','smf73ccm.smf73g4mwu': 'smf73g4mwu',
                'smf73ccm.smf73g4mru': 'smf73g4mru','smf73ccm.smf73g4ioec': 'smf73g4ioec','smf73ccm.smf73g4us': 'smf73g4us',
                'smf73ccm.smf73g4tbc': 'smf73g4tbc','smf73ccm.smf73g4tuc': 'smf73g4tuc','smf73ccm.smf73g4puc': 'smf73g4puc',
                'smf73ccm.smf73g4twu': 'smf73g4twu','smf73ccm.smf73g4pwu': 'smf73g4pwu','smf73ccm.smf73g4tru': 'smf73g4tru',
                'smf73ccm.smf73g4pru': 'smf73g4pru',
                'smf73ccm.smf73g5mbc': 'smf73g5mbc','smf73ccm.smf73g5mcu': 'smf73g5mcu','smf73ccm.smf73g5mwu': 'smf73g5mwu',
                'smf73ccm.smf73g5mru': 'smf73g5mru','smf73ccm.smf73g5ioec': 'smf73g5ioec','smf73ccm.smf73g5us': 'smf73g5us',
                'smf73ccm.smf73g5tbc': 'smf73g5tbc','smf73ccm.smf73g5tuc': 'smf73g5tuc','smf73ccm.smf73g5puc': 'smf73g5puc',
                'smf73ccm.smf73g5twu': 'smf73g5twu','smf73ccm.smf73g5pwu': 'smf73g5pwu','smf73ccm.smf73g5tru': 'smf73g5tru',
                'smf73ccm.smf73g5pru': 'smf73g5pru',
            }).reset_index()
        df_cha['smf73pid'] = df_cha['smf73pid'].str[2:]
        df_cha['smf73fg2'] = df_cha['smf73fg2'].apply(lambda x: int(str(x), 16))
        df_cha['smf73fg3'] = df_cha['smf73fg3'].apply(lambda x: int(str(x), 16))
        df_cha['smf73fg4'] = df_cha['smf73fg4'].apply(lambda x: int(str(x), 16))
        df_cha['smf73fg5'] = df_cha['smf73fg5'].apply(lambda x: int(str(x), 16))
        df_cha['smf73msc'] = df_cha['smf73msc'].apply(lambda x: int(str(x), 16))
        df_cha['smf73cmg'] = df_cha['smf73cmg'].apply(lambda x: int(str(x), 16))
        df_cha['smf73nt1'] = np.where(df_cha['smf73nt1'] == '0x00', "", ebcdic_2_ascii(df_cha['smf73nt1']))
        df_cha['smf73nt2'] = np.where(df_cha['smf73nt2'] == '0x00', "", ebcdic_2_ascii(df_cha['smf73nt2']))
        df_cha['block_multiplexor'] = df_cha['smf73fg2'].apply(lambda x: is_bit_set(x, 8, 2))
        df_cha['byte_multiplexor'] = df_cha['smf73fg2'].apply(lambda x: is_bit_set(x, 8, 3))
        df_cha['partial_stat'] = df_cha['smf73fg2'].apply(lambda x: is_bit_set(x, 8, 5))
        df_cha['data_invalid'] = df_cha['smf73fg2'].apply(lambda x: is_bit_set(x, 8, 6))
        df_cha['ch_path_online'] = df_cha['smf73fg2'].apply(lambda x: is_bit_set(x, 8, 7))
        df_cha['es_connection_ch'] = df_cha['smf73fg3'].apply(lambda x: is_bit_set(x, 8, 0))
        df_cha['es_connection_dir'] = df_cha['smf73fg3'].apply(lambda x: is_bit_set(x, 8, 1))
        df_cha['es_conv_ch'] = df_cha['smf73fg3'].apply(lambda x: is_bit_set(x, 8, 2))
        df_cha['ch_path_modified'] = df_cha['smf73fg3'].apply(lambda x: is_bit_set(x, 8, 3))
        df_cha['ch_path_deleted'] = df_cha['smf73fg3'].apply(lambda x: is_bit_set(x, 8, 4))
        df_cha['ch_path_inserted'] = df_cha['smf73fg3'].apply(lambda x: is_bit_set(x, 8, 5))
        df_cha['valid_path'] = df_cha['smf73fg3'].apply(lambda x: is_bit_set(x, 8, 6))
        df_cha['ch_path_shared'] = df_cha['smf73fg3'].apply(lambda x: is_bit_set(x, 8, 7))
        df_cha['cpmb_invalid'] = df_cha['smf73fg4'].apply(lambda x: is_bit_set(x, 8, 0))
        df_cha['ctc_defined'] = df_cha['smf73fg4'].apply(lambda x: is_bit_set(x, 8, 1))
        df_cha['ch_conversion'] = df_cha['smf73fg4'].apply(lambda x: is_bit_set(x, 8, 2))
        df_cha['ch_path_dcm'] = df_cha['smf73fg4'].apply(lambda x: is_bit_set(x, 8, 4))
        df_cha['ch_charact_changed'] = df_cha['smf73fg4'].apply(lambda x: is_bit_set(x, 8, 5))
        df_cha['ch_path_extended'] = df_cha['smf73fg4'].apply(lambda x: is_bit_set(x, 8, 6))
        df_cha['physical_network'] = df_cha['smf73fg4'].apply(lambda x: is_bit_set(x, 8, 7))
        df_cha['cpmf_word1'] = df_cha['smf73fg5'].apply(lambda x: is_bit_set(x, 8, 0))
        df_cha['cpmf_word2'] = df_cha['smf73fg5'].apply(lambda x: is_bit_set(x, 8, 1))
        df_cha['cpmf_word3'] = df_cha['smf73fg5'].apply(lambda x: is_bit_set(x, 8, 2))
        df_cha['cpmf_word4'] = df_cha['smf73fg5'].apply(lambda x: is_bit_set(x, 8, 3))
        df_cha['cpmf_word5'] = df_cha['smf73fg5'].apply(lambda x: is_bit_set(x, 8, 4))
        df_cha['smf73msc'] = df_cha['smf73msc'].apply(lambda x: extractKBits(x, 8, 4)).astype(int)
        df_cha['smf73pby'] = pd.to_timedelta(df_cha['smf73pby']) / np.timedelta64(1, 's')
        df_cha['smf73pti'] = pd.to_timedelta(df_cha['smf73pti']) / np.timedelta64(1, 's')
        df_cha['smf73spd'] = cal_spd(df_cha['smf73msc'], df_cha['smf73spd'])
        df_cha = df_cha.set_index(['csc', 'smf73sid', 'datetime', 'smf73ist', 'smf73iet', 'smf73pid'])
    else:
        df_cha = pd.DataFrame()
    return df_cha


def build_ecd(df: pd.DataFrame, df_pro_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for Extended Channel Path Data Section.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_pro_idx: The index of the RMF product section dataframe.

    Returns:
        The dataframe for the Extended Channel Path Data section.
    """
    if 'smf73ecd' in df.columns:
        df_ecd = col_to_frame(df[df.index.get_level_values('smf_type') == '73.1'], 'smf73ecd', df_pro_idx).rename(
            columns={'smf73ecp': 'smf73pid'}).drop(columns=['smf_type', 'smf73int'])
        df_ecd['smf73pid'] = df_ecd['smf73pid'].str[2:]
        df_ecd = df_ecd.set_index(['csc', 'smf73sid', 'datetime', 'smf73ist', 'smf73iet', 'smf73pid'])
    else:
        df_ecd = pd.DataFrame()
    return df_ecd


def format_73df(df: pd.DataFrame) -> dict:
    """Format smf73 JSON files to the dataframes.

    Args:
        df: JSON dataframe.

    Returns:
        A dictionary of dataframes.
    """
    df_dict = {'ctl': pd.DataFrame(), 'cha1': pd.DataFrame(), 'cha2': pd.DataFrame(), 'cha3': pd.DataFrame(),
               'cha4': pd.DataFrame(), 'cha5': pd.DataFrame(), 'pro': pd.DataFrame()}

    if 'smf73pro' not in df.columns:
        return df_dict
    else:
        df_dict['pro'] = build_pro(df)

    if df_dict['pro'].empty:
        # Cannot continue processing
        return df_dict

    df.set_index(df_dict['pro'].index, inplace=True)

    if '73.1' in df_dict['pro'].index.get_level_values('smf_type'):  # Contains subtype 1 records

        df_dict['ctl'] = build_ctl(df, df_dict['pro'].index)

        # Channel Path Data Section
        df_cha = build_cha(df,
                           df_dict['ctl'].reset_index().set_index(
                               ['datetime', 'smf73ist', 'smf73iet', 'smf_type', 'csc', 'smf73sid', 'smf73int',
                                'smf73smp']).index)

        df_dict['cha1'] = df_cha[(df_cha['valid_path'] == 1) & (df_cha['smf73cmg'] == 1)].copy()
        df_dict['cha2'] = df_cha[(df_cha['valid_path'] == 1) & (df_cha['smf73cmg'] == 2)].copy()
        df_dict['cha3'] = df_cha[(df_cha['valid_path'] == 1) & (df_cha['smf73cmg'] == 3)].copy()
        df_dict['cha4'] = df_cha[(df_cha['valid_path'] == 1) & (df_cha['smf73cmg'] == 4)].copy()
        df_dict['cha5'] = df_cha[(df_cha['valid_path'] == 1) & (df_cha['smf73cmg'] == 5)].copy()
        if not df_dict['cha1'].empty:
            df_dict['cha1']['smf73tut'] = pd.to_timedelta(df_dict['cha1']['smf73tut']) / np.timedelta64(1, 's')
            df_dict['cha1']['smf73put'] = pd.to_timedelta(df_dict['cha1']['smf73put']) / np.timedelta64(1, 's')
            df_dict['cha1']['total_utilization_pct'] = df_dict['cha1']['smf73tut'] * 100 / df_dict['cha1']['smf73pti']
            df_dict['cha1']['part_utilization_pct'] = df_dict['cha1']['smf73put'] * 100 / df_dict['cha1']['smf73pti']
            df_dict['cha1']['bus_utilization_pct'] = df_dict['cha1']['smf73bsy'] * 100 / df_dict['cha1']['smf73smp']
        if not df_dict['cha2'].empty:
            df_dict['cha2']['total_utilization_pct'] = df_dict['cha2']['smf73tuc'] * 100 / (df_dict['cha2']['smf73mcu'] * df_dict['cha2']['smf73pti'])
            df_dict['cha2']['part_utilization_pct'] = df_dict['cha2']['smf73puc'] * 100 / (df_dict['cha2']['smf73mcu'] * df_dict['cha2']['smf73pti'])
            df_dict['cha2']['bus_utilization_pct'] = df_dict['cha2']['smf73tbc'] * 100 / (df_dict['cha2']['smf73mbc'] * df_dict['cha2']['smf73pti'])
            df_dict['cha2']['part_read_rate'] = df_dict['cha2']['smf73pru'] * df_dict['cha2']['smf73us'] / df_dict['cha2']['smf73pti'] / 1e6
            df_dict['cha2']['total_read_rate'] = df_dict['cha2']['smf73tru'] * df_dict['cha2']['smf73us'] / df_dict['cha2']['smf73pti'] / 1e6
            df_dict['cha2']['part_write_rate'] = df_dict['cha2']['smf73pwu'] * df_dict['cha2']['smf73us'] / df_dict['cha2']['smf73pti'] / 1e6
            df_dict['cha2']['total_write_rate'] = df_dict['cha2']['smf73twu'] * df_dict['cha2']['smf73us'] / df_dict['cha2']['smf73pti'] / 1e6
        if not df_dict['cha3'].empty:
            df_dict['cha3']['part_read_rate'] = df_dict['cha3']['smf73pru'] * df_dict['cha3']['smf73us'] / df_dict['cha3']['smf73pti'] / 1e6
            df_dict['cha3']['total_read_rate'] = df_dict['cha3']['smf73tru'] * df_dict['cha3']['smf73us'] / df_dict['cha3']['smf73pti'] / 1e6
            df_dict['cha3']['part_write_rate'] = df_dict['cha3']['smf73pds'] * df_dict['cha3']['smf73pdu'] / df_dict['cha3']['smf73pti'] / 1e6
            df_dict['cha3']['total_write_rate'] = df_dict['cha3']['smf73tds'] * df_dict['cha3']['smf73tdu'] / df_dict['cha3']['smf73pti'] / 1e6
            df_dict['cha3']['message_rate_part'] = df_dict['cha3']['smf73pms'] * df_dict['cha3']['smf73pum'] / df_dict['cha3']['smf73pti']
            df_dict['cha3']['message_rate_total'] = df_dict['cha3']['smf73tms'] * df_dict['cha3']['smf73tum'] / df_dict['cha3']['smf73pti']
            df_dict['cha3']['message_size_part'] = df_dict['cha3']['smf73pds'] * df_dict['cha3']['smf73pdu'] / (
                    df_dict['cha3']['smf73pms'] * df_dict['cha3']['smf73pum'])
            df_dict['cha3']['message_size_total'] = df_dict['cha3']['smf73tds'] * df_dict['cha3']['smf73tdu'] / (
                    df_dict['cha3']['smf73tms'] * df_dict['cha3']['smf73tum'])
            df_dict['cha3']['send_fail_part'] = df_dict['cha3']['smf73pus'] / df_dict['cha3']['smf73pti']
            df_dict['cha3']['receive_fail_part'] = df_dict['cha3']['smf73pub'] / df_dict['cha3']['smf73pti']
            df_dict['cha3']['receive_fail_total'] = df_dict['cha3']['smf73tub'] / df_dict['cha3']['smf73pti']
        if not df_dict['cha4'].empty:
            df_dict['cha4']['total_utilization_pct'] = df_dict['cha4']['smf73g4tuc'] * 100 / (
                        df_dict['cha4']['smf73g4mcu'] * df_dict['cha4']['smf73pti'])
            df_dict['cha4']['part_utilization_pct'] = df_dict['cha4']['smf73g4puc'] * 100 / (
                        df_dict['cha4']['smf73g4mcu'] * df_dict['cha4']['smf73pti'])
            df_dict['cha4']['bus_utilization_pct'] = df_dict['cha4']['smf73g4tbc'] * 100 / (
                        df_dict['cha4']['smf73g4mbc'] * df_dict['cha4']['smf73pti'])
            df_dict['cha4']['part_read_rate'] = df_dict['cha4']['smf73g4pru'] * df_dict['cha4']['smf73g4us'] / \
                                                df_dict['cha4']['smf73pti'] / 1e6
            df_dict['cha4']['total_read_rate'] = df_dict['cha4']['smf73g4tru'] * df_dict['cha4']['smf73g4us'] / \
                                                 df_dict['cha4']['smf73pti'] / 1e6
            df_dict['cha4']['part_write_rate'] = df_dict['cha4']['smf73g4pwu'] * df_dict['cha4']['smf73g4us'] / \
                                                 df_dict['cha4']['smf73pti'] / 1e6
            df_dict['cha4']['total_write_rate'] = df_dict['cha4']['smf73g4twu'] * df_dict['cha4']['smf73g4us'] / \
                                                  df_dict['cha4']['smf73pti'] / 1e6
        if not df_dict['cha5'].empty:
            df_dict['cha5']['total_utilization_pct'] = df_dict['cha5']['smf73g5tuc'] * 100 / (
                        df_dict['cha5']['smf73g5mcu'] * df_dict['cha5']['smf73pti'])
            df_dict['cha5']['part_utilization_pct'] = df_dict['cha5']['smf73g5puc'] * 100 / (
                        df_dict['cha5']['smf73g5mcu'] * df_dict['cha5']['smf73pti'])
            df_dict['cha5']['bus_utilization_pct'] = df_dict['cha5']['smf73g5tbc'] * 100 / (
                        df_dict['cha5']['smf73g5mbc'] * df_dict['cha5']['smf73pti'])
            df_dict['cha5']['part_read_rate'] = df_dict['cha5']['smf73g5pru'] * df_dict['cha5']['smf73g5us'] / \
                                                df_dict['cha5']['smf73pti'] / 1e6
            df_dict['cha5']['total_read_rate'] = df_dict['cha5']['smf73g5tru'] * df_dict['cha5']['smf73g5us'] / \
                                                 df_dict['cha5']['smf73pti'] / 1e6
            df_dict['cha5']['part_write_rate'] = df_dict['cha5']['smf73g5pwu'] * df_dict['cha5']['smf73g5us'] / \
                                                 df_dict['cha5']['smf73pti'] / 1e6
            df_dict['cha5']['total_write_rate'] = df_dict['cha5']['smf73g5twu'] * df_dict['cha5']['smf73g5us'] / \
                                                  df_dict['cha5']['smf73pti'] / 1e6

        df_ecd = build_ecd(df, df_dict['pro'].index)
        if not df_ecd.empty and not df_dict['cha2'].empty:
            df_dict['cha2'] = df_dict['cha2'].join(df_ecd[['smf73eoc','smf73eod','smf73eos','smf73etc','smf73etd','smf73ets']])
            df_dict['cha2']['ficon_operations_rate'] = df_dict['cha2']['smf73eoc'] / df_dict['cha2']['smf73pti']
            df_dict['cha2']['ficon_operations_active'] = df_dict['cha2']['smf73eos'] / df_dict['cha2']['smf73eoc']
            df_dict['cha2']['ficon_operations_defer'] = df_dict['cha2']['smf73eod'] / df_dict['cha2']['smf73pti']
            df_dict['cha2']['zhpf_operations_rate'] = df_dict['cha2']['smf73etc'] / df_dict['cha2']['smf73pti']
            df_dict['cha2']['zhpf_operations_active'] = df_dict['cha2']['smf73ets'] / df_dict['cha2']['smf73etc']
            df_dict['cha2']['zhpf_operations_defer'] = df_dict['cha2']['smf73etd'] / df_dict['cha2']['smf73pti']

        if not df_ecd.empty and not df_dict['cha4'].empty:
            df_dict['cha4'] = df_dict['cha4'].join(df_ecd[['smf73g4ecet','smf73g4eioet']])

        if not df_ecd.empty and not df_dict['cha5'].empty:
            df_dict['cha5'] = df_dict['cha5'].join(df_ecd[['smf73g5ecet','smf73g5eioet','smf73g5eoc','smf73g5eod',
                                                           'smf73g5eos','smf73g5etc','smf73g5etd','smf73g5ets']])
            df_dict['cha5']['ficon_operations_rate'] = df_dict['cha5']['smf73g5eoc'] / df_dict['cha5']['smf73pti']
            df_dict['cha5']['ficon_operations_active'] = df_dict['cha5']['smf73g5eos'] / df_dict['cha5']['smf73g5eoc']
            df_dict['cha5']['ficon_operations_defer'] = df_dict['cha5']['smf73g5eod'] / df_dict['cha5']['smf73pti']
            df_dict['cha5']['zhpf_operations_rate'] = df_dict['cha5']['smf73g5etc'] / df_dict['cha5']['smf73pti']
            df_dict['cha5']['zhpf_operations_active'] = df_dict['cha5']['smf73g5ets'] / df_dict['cha5']['smf73g5etc']
            df_dict['cha5']['zhpf_operations_defer'] = df_dict['cha5']['smf73g5etd'] / df_dict['cha5']['smf73pti']
    return df_dict

def print_channel_activity_report(jsonfiles: tuple, lpar: str, start_time_str: str, end_time_str: str) -> str:
    """Print smf73 Channel Activity Report based on JSON files.

    Args:
        jsonfiles: JSON file or files.
        lpar: Target LPAR to print.
        start_time_str: Start time string.
        end_time_str: End time string.

    Returns:
        Channel activity report.
    """
    start_time = pd.to_datetime(start_time_str)
    end_time = pd.to_datetime(end_time_str)
    sid = lpar

    report = ""
    for jsonfile in jsonfiles:
        with open(jsonfile) as f:
            try:
                df = pd.read_json(f)
            except ValueError:
                click.echo(
                    f"\nInvalid JSON file {jsonfile}. This file will be skipped.")
                continue

            if 'header' not in df.columns or not isinstance(df.iloc[0]['header'], dict) \
                    or df.iloc[0]['header'].get('recType') is None or df.iloc[0]['header']['recType'] != 73:
                click.echo(
                    f"\nInvalid JSON file {jsonfile}. This file will be skipped.")
                continue
            try:
                dfs_dict = format_73df(df)
            except Exception as e:
                click.echo(f"\nUnsupported JSON file {jsonfile} with error: {str(e)}. This file will be skipped.")
                continue

            if dfs_dict['pro'].empty:
                click.echo(
                    f"\nThis JSON file {jsonfile} is not for this smf type. This file will be skipped.")
                # Cannot continue processing
                continue
            page_detail = ''
            pro = dfs_dict['pro'].loc[~dfs_dict['pro'].index.duplicated(keep='first'), :].query(
                "smf73ist > @start_time and smf73ist < @end_time and smf73sid == @sid").copy().reset_index().set_index(
                [col.name for col in Smf73Ctl.__table__.primary_key.columns.values()])
            ctl = dfs_dict['ctl'].loc[~dfs_dict['ctl'].index.duplicated(keep='first'), :].query(
                "smf73ist > @start_time and smf73ist < @end_time and smf73sid == @sid").copy()
            cha1 = dfs_dict['cha1'].query(
                "smf73ist > @start_time and smf73ist < @end_time and smf73sid == @sid").copy().reset_index().set_index(
                [col.name for col in Smf73Ctl.__table__.primary_key.columns.values()])
            cha2 = dfs_dict['cha2'].query(
                "smf73ist > @start_time and smf73ist < @end_time and smf73sid == @sid").copy().reset_index().set_index(
                [col.name for col in Smf73Ctl.__table__.primary_key.columns.values()])
            cha3 = dfs_dict['cha3'].query(
                "smf73ist > @start_time and smf73ist < @end_time and smf73sid == @sid").copy().reset_index().set_index(
                [col.name for col in Smf73Ctl.__table__.primary_key.columns.values()])

            for index in ctl.index:
                pro_dict = pro.loc[[index]].reset_index().to_dict('records')[0]
                ctl_dict = ctl.loc[[index]].reset_index().to_dict('records')[0]
                if cha1.empty or index not in cha1.index:
                    cha1s_dict = []
                else:
                    for col_name in cha1.columns:
                        cha1[col_name].replace({np.nan: None}, inplace=True)
                    cha1s_dict = cha1.loc[[index]].reset_index().to_dict('records')
                if cha2.empty or index not in cha2.index:
                    cha2s_dict = []
                else:
                    for col_name in cha2.columns:
                        cha2[col_name] = cha2[col_name].replace({np.nan: None})

                    cha2s_dict = cha2.loc[[index]].reset_index().to_dict('records')
                if cha3.empty or index not in cha3.index:
                    cha3s_dict = []
                else:
                    for col_name in cha3.columns:
                        cha3[col_name] = cha3[col_name].replace({np.nan: None})

                    cha3s_dict = cha3.loc[[index]].reset_index().to_dict('records')

                page_detail += format_channel_activity_report(pro_dict, ctl_dict, cha1s_dict, cha2s_dict, cha3s_dict)
                page_detail += '\n\n'
            if page_detail != '':
                report += page_detail
    if report == '':
        report = 'No data found.'
    return report

