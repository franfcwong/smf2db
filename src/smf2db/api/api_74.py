import datetime as dt
from typing import Union, Tuple

import click
import numpy as np
import pandas as pd
import tabulate as tb

from smf2db.api.report_util import format_cachsys_status_and_overview, \
    format_cachsys_device_overview_and_raid_activity, \
    format_cache_device_status_and_activity, format_cachsys_summary, format_top20_report, \
    format_cf_activity_report, format_device_activity_report, format_link_statistics, format_sync_io_statistics, \
    format_extent_pool_statistics, format_rank_statistics, format_switch_activity, format_hfs_global_statistics, \
    format_hfs_file_system_statistics, format_omvs_activity_report, convert_si, format_xcf_activity_report, extractKBits
from smf2db.api.util import (calculate_std_dev, setdatetime, substr_x, converttolist,
                             to_int, col_to_frame, cols_to_frame, agg_next, is_bit_set)
from smf2db.db_models.smf74_model import (Smf74Pro, Smf74Dctl, Smf74Dev, Smf74Xctl, Smf74Sys, Smf74Path,
                                          Smf74Mbr, Smf74Omvs, Smf74Cachsys, Smf74Cdev, Smf74Raid, Smf74Xpool,
                                          Smf74Rrank, Smf74Hfs, Smf74Gbuf, Smf74Fsys, Smf74Fcd, Smf74Switch,
                                          Smf74Port, Smf74Connector, Smf74Cntl, Smf74Lss, Smf74Extp, Smf74Rank,
                                          Smf74Arry, Smf74Siol, Smf74Pcie, Smf74Scm, Smf74Eadm, Smf74Cf, Smf74Lcf,
                                          Smf74Sreq, Smf74Proc, Smf74Cach, Smf74Cfrf, Smf74Subchpa, Smf74Mscm,
                                          Smf74Str, Smf74Srtd, Smf74Adup, Smf74Dupchpa)

tb.PRESERVE_WHITESPACE = True


def build_pro(df: pd.DataFrame) -> Union[pd.DataFrame, None]:
    """Build the dataframe for RMF Product Section which will be uploaded to smf74_pro table.

    Args:
        df: The master dataframe which is created from the JSON file.

    Returns:
        The dataframe for the RMF product section or None if csc is not found in the database.
    """
    set_datetime = np.vectorize(setdatetime)
    df_pro = pd.concat([df['header'].apply(pd.Series),
                        df['smf74pro'].apply(pd.Series)],
                       axis=1).rename(
        columns={'sysId': 'smf74sid',
                 'sysInd': 'smf74flg', 'recType': 'smf_type'})
    df_pro['csc'] = np.nan
    df_pro['smf74sid'] = df_pro['smf74sid'].str.strip()
    df_pro['smf74ist'] = pd.to_datetime(df_pro['smf74ist'])
    df_pro['smf74gie'] = pd.to_datetime(df_pro['smf74gie'])
    df_pro['smf74int'] = pd.to_timedelta(df_pro['smf74int']) / np.timedelta64(1, 's')
    df_pro['smf74lgo'] = pd.to_timedelta(df_pro['smf74lgo']) / np.timedelta64(1, 'h')
    df_pro['datetime'] = set_datetime(df_pro['smf74ist'])
    df_pro['smf_type'] = df_pro['smf_type'].astype(str) + '.' + df_pro['subType'].astype(str)
    df_pro['smf74flg'] = df_pro['smf74flg'].apply(lambda x: int(str(x), 16))
    df_pro['smf74fla'] = df_pro['smf74fla'].apply(lambda x: int(str(x), 16))
    df_pro['smf74prf'] = df_pro['smf74prf'].apply(lambda x: int(str(x), 16))
    df_pro['smf74srl'] = df_pro['smf74srl'].apply(lambda x: int(str(x), 16))
    df_pro['speed_boost'] = df_pro['smf74fla'].apply(lambda x: is_bit_set(x, 16, 10))
    df_pro['ziip_boost'] = df_pro['smf74fla'].apply(lambda x: is_bit_set(x, 16, 9))
    df_pro = df_pro.set_index(
        ['datetime', 'smf74ist', 'smf74iet', 'smf_type', 'csc', 'smf74sid', 'smf74int'])
    return df_pro


def build_dctl(df: pd.DataFrame, df_pro_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for Device Control Data Section which will be uploaded to smf74_dctl table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_pro_idx: The index of the RMF product section dataframe.

    Returns:
        The dataframe for the Device Control Data section.
    """
    if 'smf74a' in df.columns:
        df_dctl = col_to_frame(df[df.index.get_level_values('smf_type') == '74.1'], 'smf74a', df_pro_idx)  # .rename(
        df_dctl['smf74sub'] = df_dctl['smf74sub'].str[2:]
        df_dctl['smf74dcf'] = df_dctl['smf74dcf'].apply(lambda x: int(str(x), 16))
        df_dctl['smf74dms'] = df_dctl['smf74dms'].apply(lambda x: int(str(x), 16))
        df_dctl['smf74enf'] = df_dctl['smf74enf'].apply(lambda x: int(str(x), 16))
        df_dctl['smf74cfl'] = df_dctl['smf74cfl'].apply(lambda x: int(str(x), 16))
        df_dctl['smf74smf'] = df_dctl['smf74smf'].apply(lambda x: int(str(x), 16))
        df_dctl['smf74s15'] = df_dctl['smf74s15'].apply(lambda x: int(str(x), 16))
        df_dctl['smf74src'] = df_dctl['smf74src'].apply(lambda x: int(str(x), 16))
        df_dctl['smf74srs'] = df_dctl['smf74srs'].apply(lambda x: int(str(x), 16))
        df_dctl['nrf'] = df_dctl['smf74dcf'].apply(lambda x: is_bit_set(x, 8, 0))
        df_dctl['sgf'] = df_dctl['smf74dcf'].apply(lambda x: is_bit_set(x, 8, 1))
        df_dctl['_429'] = df_dctl['smf74dms'].apply(lambda x: is_bit_set(x, 8, 0))
        df_dctl['sme'] = df_dctl['smf74dms'].apply(lambda x: is_bit_set(x, 8, 1))
        df_dctl['ecm'] = df_dctl['smf74enf'].apply(lambda x: is_bit_set(x, 8, 0))
        df_dctl['sts'] = df_dctl['smf74enf'].apply(lambda x: is_bit_set(x, 8, 1))
        df_dctl['fcm'] = df_dctl['smf74enf'].apply(lambda x: is_bit_set(x, 8, 2))
        df_dctl['fid'] = df_dctl['smf74enf'].apply(lambda x: is_bit_set(x, 8, 3))
        df_dctl['msm'] = df_dctl['smf74smf'].apply(lambda x: is_bit_set(x, 8, 0))
        df_dctl['config_changed'] = df_dctl['smf74cfl'].apply(lambda x: is_bit_set(x, 8, 0))
        df_dctl['config_changed_since_ipl'] = df_dctl['smf74cfl'].apply(lambda x: is_bit_set(x, 8, 1))
        df_dctl['ipl_iodf'] = df_dctl['smf74cfl'].apply(lambda x: is_bit_set(x, 8, 2))
        df_dctl['io_token_valid'] = df_dctl['smf74cfl'].apply(lambda x: is_bit_set(x, 8, 3))
        df_dctl['smf74tdt'] = pd.to_datetime(df_dctl['smf74tdy'] + ' ' + df_dctl['smf74tok.smf74ttm'],
                                             format='%m/%d/%Y %H.%M.%S',
                                             errors='coerce')
        df_dctl['smf74tdy'] = pd.to_datetime(df_dctl['smf74tdy']).dt.date
        df_dctl = df_dctl[Smf74Dctl.__table__.columns.keys()].set_index(
            ['csc', 'smf74sid', 'datetime', 'smf74ist', 'smf74iet', 'smf74sub'])
    else:
        df_dctl = pd.DataFrame(columns=Smf74Dctl.__table__.columns.keys()).set_index(
            ['csc', 'smf74sid', 'datetime', 'smf74ist', 'smf74iet', 'smf74sub'])
    return df_dctl


def build_dev(df: pd.DataFrame, df_dctl_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for Device Data Section which will be uploaded to either smf74_ddev table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_dctl_idx: The index of the Device COntrol Data section dataframe.

    Returns:
        The dataframe for the Device Data section.
    """

    if 'smf74b' in df.columns:
        df_dev = col_to_frame(df[df.index.get_level_values('smf_type') == '74.1'], 'smf74b', df_dctl_idx)
        df_dev['smf74cnf'] = df_dev['smf74cnf'].apply(lambda x: int(str(x), 16))
        df_dev['smf74clf'] = df_dev['smf74clf'].apply(lambda x: int(str(x), 16))
        df_dev['smf74cnx'] = df_dev['smf74cnx'].apply(lambda x: int(str(x), 16))
        df_dev['smf74cn2'] = df_dev['smf74cn2'].apply(lambda x: int(str(x), 16))
        df_dev['smf74dts'] = df_dev['smf74dts'].apply(lambda x: int(str(x), 16))
        df_dev['smf74lcu'] = df_dev['smf74lcu'].str[2:]
        df_dev['smf74num'] = df_dev['smf74num'].str[2:]
        df_dev['smf74typ'] = df_dev['smf74typ'].str[2:]
        df_dev['lcd'] = df_dev['smf74cnf'].apply(lambda x: is_bit_set(x, 8, 1))
        df_dev['cmb'] = df_dev['smf74cnf'].apply(lambda x: is_bit_set(x, 8, 2))
        df_dev['del_'] = df_dev['smf74cnf'].apply(lambda x: is_bit_set(x, 8, 3))
        df_dev['par'] = df_dev['smf74cnf'].apply(lambda x: is_bit_set(x, 8, 4))
        df_dev['vac'] = df_dev['smf74cnf'].apply(lambda x: is_bit_set(x, 8, 6))
        df_dev['sta'] = df_dev['smf74cnf'].apply(lambda x: is_bit_set(x, 8, 7))
        df_dev['smf74cnn'] = pd.to_timedelta(df_dev['smf74cnn']) / np.timedelta64(1, 's')
        df_dev['smf74pen'] = pd.to_timedelta(df_dev['smf74pen']) / np.timedelta64(1, 's')
        df_dev['smf74atv'] = pd.to_timedelta(df_dev['smf74atv']) / np.timedelta64(1, 's')
        df_dev['smf74dis'] = pd.to_timedelta(df_dev['smf74dis']) / np.timedelta64(1, 's')
        df_dev['smf74dvb'] = pd.to_timedelta(df_dev['smf74dvb']) / np.timedelta64(1, 's')
        df_dev['rnr'] = df_dev['smf74clf'].apply(lambda x: is_bit_set(x, 8, 0))
        df_dev['rsg'] = df_dev['smf74clf'].apply(lambda x: is_bit_set(x, 8, 1))
        df_dev['rcs'] = df_dev['smf74clf'].apply(lambda x: is_bit_set(x, 8, 2))
        df_dev['mts'] = df_dev['smf74clf'].apply(lambda x: is_bit_set(x, 8, 3))
        df_dev['mte'] = df_dev['smf74clf'].apply(lambda x: is_bit_set(x, 8, 4))
        df_dev['ctw'] = df_dev['smf74clf'].apply(lambda x: is_bit_set(x, 8, 6))
        df_dev['dyc'] = df_dev['smf74cnx'].apply(lambda x: is_bit_set(x, 8, 0))
        df_dev['ddt'] = df_dev['smf74cnx'].apply(lambda x: is_bit_set(x, 8, 1))
        df_dev['pav'] = df_dev['smf74cnx'].apply(lambda x: is_bit_set(x, 8, 2))
        df_dev['nxc'] = df_dev['smf74cnx'].apply(lambda x: is_bit_set(x, 8, 3))
        df_dev['ntf'] = df_dev['smf74cnx'].apply(lambda x: is_bit_set(x, 8, 4))
        df_dev['cni'] = df_dev['smf74cnx'].apply(lambda x: is_bit_set(x, 8, 5))
        df_dev['hpv'] = df_dev['smf74cnx'].apply(lambda x: is_bit_set(x, 8, 6))
        df_dev['cfc'] = df_dev['smf74cnx'].apply(lambda x: is_bit_set(x, 8, 7))
        df_dev['hwr'] = df_dev['smf74cn2'].apply(lambda x: is_bit_set(x, 8, 0))
        df_dev['xpv'] = df_dev['smf74cn2'].apply(lambda x: is_bit_set(x, 8, 1))
        df_dev['sir'] = df_dev['smf74cn2'].apply(lambda x: is_bit_set(x, 8, 2))
        df_dev['siw'] = df_dev['smf74cn2'].apply(lambda x: is_bit_set(x, 8, 3))
        df_dev['srd'] = df_dev['smf74dts'].apply(lambda x: is_bit_set(x, 8, 0))
        df_dev['snd'] = df_dev['smf74dts'].apply(lambda x: is_bit_set(x, 8, 1))
        df_dev['shv'] = df_dev['smf74dts'].apply(lambda x: is_bit_set(x, 8, 3))
        df_dev['shr'] = df_dev['smf74dts'].apply(lambda x: is_bit_set(x, 8, 4))
        df_dev['smf74dct_hex2'] = df_dev['smf74dct_hex2'].str[2:]
        df_dev['smf74cmr'] = pd.to_timedelta(df_dev['smf74cmr']) / np.timedelta64(1, 's')
        df_dev['smf74idt'] = pd.to_timedelta(df_dev['smf74idt']) / np.timedelta64(1, 's')
        df_dev['smf74cuq'] = pd.to_timedelta(df_dev['smf74cuq']) / np.timedelta64(1, 's')
        df_dev['smf74nm2'] = df_dev['smf74nm2'].str[2:]
        df_dev['smf74spr'] = pd.to_timedelta(df_dev['smf74spr']) / np.timedelta64(1, 's')
        df_dev['smf74spw'] = pd.to_timedelta(df_dev['smf74spw']) / np.timedelta64(1, 's')
        df_dev['smf74sftr'] = pd.to_timedelta(df_dev['smf74sftr']) / np.timedelta64(1, 's')
        df_dev['smf74sftw'] = pd.to_timedelta(df_dev['smf74sftw']) / np.timedelta64(1, 's')
        df_dev['smf74ios'] = pd.to_timedelta(df_dev['smf74ios']) / np.timedelta64(1, 's')
        df_dev['sync_device_read_activity_rate'] = df_dev['smf74sqr'] / df_dev['smf74int']
        df_dev['sync_device_write_activity_rate'] = df_dev['smf74sqw'] / df_dev['smf74int']
        df_dev['sync_avg_read_resp_time'] = ((df_dev['smf74spr'] / (df_dev['smf74sqr'] * 2000))
                                             .where(df_dev['smf74sqr'] > 0, 0))
        df_dev['sync_avg_write_resp_time'] = ((df_dev['smf74spw'] / (df_dev['smf74sqw'] * 2000))
                                              .where(df_dev['smf74sqw'] > 0, 0))
        df_dev['sync_read_xfer_rate'] = df_dev['smf74sbr'] / (df_dev['smf74int'] * 1000)
        df_dev['sync_write_xfer_rate'] = df_dev['smf74sbw'] / (df_dev['smf74int'] * 1000)
        df_dev['sync_req_success'] = df_dev['smf74sqr'] + df_dev['smf74sqw']
        df_dev['sync_link_busy'] = df_dev['smf74slbr'] + df_dev['smf74slbw']
        df_dev['sync_cache_miss'] = df_dev['smf74scmr'] + df_dev['smf74snis']
        df_dev['sync_timeout'] = df_dev['smf74stor'] + df_dev['smf74stow']
        df_dev['sync_rej_read'] = df_dev['smf74slbr'] + df_dev['smf74scmr'] + df_dev['smf74stor'] + df_dev['smf74sor']
        df_dev['sync_rej_write'] = df_dev['smf74slbw'] + df_dev['smf74snis'] + df_dev['smf74stow'] + df_dev['smf74sow']
        df_dev['sync_total_req'] = (df_dev['smf74sqr'] + df_dev['smf74sqw'] + df_dev['smf74slbr'] + df_dev['smf74slbw']
                                    + df_dev['smf74scmr'] + df_dev['smf74snis'] + df_dev['smf74stor']
                                    + df_dev['smf74stow'] + df_dev['smf74sor'] + df_dev['smf74sow'])
        df_dev['device_activity_rate'] = df_dev['smf74ssc'] / df_dev['smf74int']
        df_dev['IOSQ_time'] = np.where(df_dev['smf74sub'] != '0080',
                                       (df_dev['smf74que'] / df_dev['smf74sam']) / (
                                               df_dev['smf74ssc'] / df_dev['smf74int']),
                                       df_dev['smf74ios'] / df_dev['smf74ssc'])
        df_dev['avg_iosq_time'] = (df_dev['smf74ios'] / df_dev['smf74ssc']).where(df_dev['smf74ssc'] > 0, 0)  # * 1000
        df_dev['avg_cmr_dly'] = (df_dev['smf74cmr'] / df_dev['smf74mec']).where(df_dev['smf74mec'] > 0, 0)  # * 1000
        df_dev['avg_db_dly'] = (df_dev['smf74dvb'] / df_dev['smf74mec']).where(df_dev['smf74mec'] > 0, 0)  # * 1000
        df_dev['avg_int_dly'] = (df_dev['smf74idt'] / df_dev['smf74mec']).where(df_dev['smf74mec'] > 0, 0)  # * 1000
        df_dev['avg_pend_time'] = (df_dev['smf74pen'] / df_dev['smf74mec']).where(df_dev['smf74mec'] > 0, 0)  # * 1000
        df_dev['avg_disc_time'] = (df_dev['smf74dis'] / df_dev['smf74mec']).where(df_dev['smf74mec'] > 0, 0)  # * 1000
        df_dev['avg_conn_time'] = (df_dev['smf74cnn'] / df_dev['smf74mec']).where(df_dev['smf74mec'] > 0, 0)  # * 1000
        df_dev['device_active_time'] = df_dev['avg_pend_time'] + df_dev['avg_disc_time'] + df_dev['avg_conn_time']
        df_dev['avg_resp_time'] = df_dev['device_active_time'] + df_dev['IOSQ_time']
        df_dev['dev_conn_percent'] = df_dev['smf74cnn'] / df_dev['smf74int'] * 100
        df_dev['dev_util_percent'] = ((df_dev['smf74cnn'] + df_dev['smf74dis']) / df_dev['smf74int']
                                      + df_dev['smf74utl'] / df_dev['smf74sam']) * 100
        df_dev['dev_resv_percent'] = df_dev['smf74rsv'] / df_dev['smf74sam'] * 100
        df_dev['avg_numbr_alloc'] = df_dev['smf74nda'] / df_dev['smf74sam']
        df_dev['any_alloc_percent'] = df_dev['smf74alc'] / df_dev['smf74sam'] * 100
        df_dev['mt_pend_percent'] = df_dev['smf74mtp'] / df_dev['smf74sam'] * 100
        df_dev['not_ready_percent'] = df_dev['smf74nrd'] / df_dev['smf74sam'] * 100
        df_dev['num_of_mts'] = df_dev['smf74mtc']
        df_dev['avg_mt_time'] = (
                df_dev['smf74mtp'] * df_dev['smf74int'] / df_dev['smf74sam'] / df_dev['smf74mtc']).where(
            df_dev['smf74mtc'] > 0, 0)
        df_dev['time_dev_alloc'] = df_dev['smf74alc'] * df_dev['smf74int'] / df_dev['smf74sam']
        df_dev = df_dev[Smf74Dev.__table__.columns.keys()].set_index(
            [col.name for col in Smf74Dev.__table__.primary_key.columns.values()])

    else:
        df_dev = pd.DataFrame(columns=Smf74Dev.__table__.columns.keys()).set_index(
            [col.name for col in Smf74Dev.__table__.primary_key.columns.values()])
    return df_dev


def build_sys(df: pd.DataFrame, df_pro_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for XCF System Data Section which will be uploaded to smf74_sys table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_pro_idx: The index of the RMF product section dataframe.

    Returns:
        The dataframe for the XCF System Data section.
    """
    dir_type = {'0x80': 'IN', '0x40': 'OUT', '0x20': 'LCL'}
    if 'r742sys' in df.columns:
        df_sys = col_to_frame(df[df.index.get_level_values('smf_type') == '74.2'], 'r742sys', df_pro_idx)
        df_sys['r742sdir'] = df_sys['r742sdir'].map(dir_type)
        df_sys['r742sstf'] = df_sys['r742sstf'].apply(lambda x: int(str(x), 16))
        df_sys['r742sact'] = df_sys['r742sstf'].apply(lambda x: is_bit_set(x, 8, 0))
        df_sys['r742siac'] = df_sys['r742sstf'].apply(lambda x: is_bit_set(x, 8, 1))
        df_sys['r742sres'] = df_sys['r742sstf'].apply(lambda x: is_bit_set(x, 8, 2))
        df_sys['r742spar'] = df_sys['r742sstf'].apply(lambda x: is_bit_set(x, 8, 3))
        df_sys = df_sys[Smf74Sys.__table__.columns.keys()].set_index(
            [col.name for col in Smf74Sys.__table__.primary_key.columns.values()])
    else:
        df_sys = pd.DataFrame(columns=Smf74Sys.__table__.columns.keys()).set_index(
            [col.name for col in Smf74Sys.__table__.primary_key.columns.values()])
    return df_sys


def build_path(df: pd.DataFrame, df_pro_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for XCF Path Data Section which will be uploaded to smf74_path table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_pro_idx: The index of the RMF product section dataframe.

    Returns:
        The dataframe for the XCF Path Data section.
    """
    convert_2_int = np.vectorize(to_int)
    dir_type = {'0x80': 'IN', '0x40': 'OUT', '0x20': 'LCL'}
    if 'r742pth' in df.columns:
        df_path = col_to_frame(df[df.index.get_level_values('smf_type') == '74.2'], 'r742pth', df_pro_idx).rename(
            columns={'r742pnib_time_': 'r742pnib_timenum'})
        df_path['r742pdir'] = df_path['r742pdir'].map(dir_type)
        df_path['r742ptyp'] = convert_2_int(df_path['r742ptyp'])
        df_path['r742pstf'] = df_path['r742pstf'].apply(lambda x: int(str(x), 16))
        df_path['r742psta'] = df_path['r742psta'].apply(lambda x: int(str(x), 16))
        df_path['r742pstm'] = df_path['r742pstm'].apply(lambda x: int(str(x), 16))
        df_path['r742pact'] = df_path['r742pstf'].apply(lambda x: is_bit_set(x, 8, 0))
        df_path['r742piac'] = df_path['r742pstf'].apply(lambda x: is_bit_set(x, 8, 1))
        df_path['r742pres'] = df_path['r742pstf'].apply(lambda x: is_bit_set(x, 8, 2))
        df_path['r742pst'] = df_path['r742psta'].apply(lambda x: is_bit_set(x, 8, 0))
        df_path['r742prs'] = df_path['r742psta'].apply(lambda x: is_bit_set(x, 8, 1))
        df_path['r742pwk'] = df_path['r742psta'].apply(lambda x: is_bit_set(x, 8, 2))
        df_path['r742psp'] = df_path['r742psta'].apply(lambda x: is_bit_set(x, 8, 3))
        df_path['r742plk'] = df_path['r742psta'].apply(lambda x: is_bit_set(x, 8, 4))
        df_path['r742pnp'] = df_path['r742psta'].apply(lambda x: is_bit_set(x, 8, 5))
        df_path['r742psf'] = df_path['r742psta'].apply(lambda x: is_bit_set(x, 8, 6))
        df_path['r742prb'] = df_path['r742psta'].apply(lambda x: is_bit_set(x, 8, 7))
        df_path['r742pqg'] = df_path['r742pstm'].apply(lambda x: is_bit_set(x, 8, 0))
        df_path['r742pqd'] = df_path['r742pstm'].apply(lambda x: is_bit_set(x, 8, 1))
        df_path['r742piot'] = pd.to_timedelta(df_path['r742piot']) / np.timedelta64(1, 's')
        df_path['r742pnib_timesum'] = pd.to_timedelta(df_path['r742pnib_timesum']) / np.timedelta64(1, 's')
        df_path['r742pnib_timessq'] = pd.to_timedelta(df_path['r742pnib_timessq']) / np.timedelta64(1, 's')
        df_path[['stat1', 'stat2', 'stat3', 'stat4']] = pd.DataFrame(df_path['r742pusg_stats'].tolist(),
                                                                     index=df_path.index)
        df_path = pd.concat([df_path,
                             pd.json_normalize(df_path['stat1']).rename(
                                 columns={'r742pusg_timesum': 'r742pusg_timesum_1',
                                          'r742pusg_timessq': 'r742pusg_timessq_1',
                                          'r742pusg_time_': 'r742pusg_timenum_1',
                                          'r742pusg_sigcnt': 'r742pusg_sigcnt_1',
                                          'r742pusg_percent': 'r742pusg_percent_1'}),
                             pd.json_normalize(df_path['stat2']).rename(
                                 columns={'r742pusg_timesum': 'r742pusg_timesum_2',
                                          'r742pusg_timessq': 'r742pusg_timessq_2',
                                          'r742pusg_time_': 'r742pusg_timenum_2',
                                          'r742pusg_sigcnt': 'r742pusg_sigcnt_2',
                                          'r742pusg_percent': 'r742pusg_percent_2'}),
                             pd.json_normalize(df_path['stat3']).rename(
                                 columns={'r742pusg_timesum': 'r742pusg_timesum_3',
                                          'r742pusg_timessq': 'r742pusg_timessq_3',
                                          'r742pusg_time_': 'r742pusg_timenum_3',
                                          'r742pusg_sigcnt': 'r742pusg_sigcnt_3',
                                          'r742pusg_percent': 'r742pusg_percent_3'}),
                             pd.json_normalize(df_path['stat4']).rename(
                                 columns={'r742pusg_timesum': 'r742pusg_timesum_4',
                                          'r742pusg_timessq': 'r742pusg_timessq_4',
                                          'r742pusg_time_': 'r742pusg_timenum_4',
                                          'r742pusg_sigcnt': 'r742pusg_sigcnt_4',
                                          'r742pusg_percent': 'r742pusg_percent_4'})],
                            axis=1).drop(columns=['stat1', 'stat2', 'stat3', 'stat4'])
        df_path['r742pusg_timesum_1'] = pd.to_timedelta(df_path['r742pusg_timesum_1']) / np.timedelta64(1, 's')
        df_path['r742pusg_timessq_1'] = pd.to_timedelta(df_path['r742pusg_timessq_1']) / np.timedelta64(1, 's')
        df_path['r742pusg_timesum_2'] = pd.to_timedelta(df_path['r742pusg_timesum_2']) / np.timedelta64(1, 's')
        df_path['r742pusg_timessq_2'] = pd.to_timedelta(df_path['r742pusg_timessq_2']) / np.timedelta64(1, 's')
        df_path['r742pusg_timesum_3'] = pd.to_timedelta(df_path['r742pusg_timesum_3']) / np.timedelta64(1, 's')
        df_path['r742pusg_timessq_3'] = pd.to_timedelta(df_path['r742pusg_timessq_3']) / np.timedelta64(1, 's')
        df_path['r742pusg_timesum_4'] = pd.to_timedelta(df_path['r742pusg_timesum_4']) / np.timedelta64(1, 's')
        df_path['r742pusg_timessq_4'] = pd.to_timedelta(df_path['r742pusg_timessq_4']) / np.timedelta64(1, 's')
        df_path = df_path[Smf74Path.__table__.columns.keys()].set_index(
            [col.name for col in Smf74Path.__table__.primary_key.columns.values()])
    else:
        df_path = pd.DataFrame(columns=Smf74Path.__table__.columns.keys()).set_index(
            [col.name for col in Smf74Path.__table__.primary_key.columns.values()])
    return df_path


def build_mbr(df: pd.DataFrame, df_pro_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for XCF Member Data Section which will be uploaded to smf74_mbr table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_pro_idx: The index of the RMF product section dataframe.

    Returns:
        The dataframe for the XCF Member Data section.
    """
    if 'r742mbr' in df.columns:
        df_mbr = col_to_frame(df[df.index.get_level_values('smf_type') == '74.2'], 'r742mbr', df_pro_idx)
        df_mbr['r742mstf'] = df_mbr['r742mstf'].apply(lambda x: int(str(x), 16))
        df_mbr['r742mst1'] = df_mbr['r742mst1'].apply(lambda x: int(str(x), 16))
        df_mbr['r742mst2'] = df_mbr['r742mst2'].apply(lambda x: int(str(x), 16))
        df_mbr['r742mact'] = df_mbr['r742mstf'].apply(lambda x: is_bit_set(x, 8, 0))
        df_mbr['r742miac'] = df_mbr['r742mstf'].apply(lambda x: is_bit_set(x, 8, 1))
        df_mbr['r742mres'] = df_mbr['r742mstf'].apply(lambda x: is_bit_set(x, 8, 2))
        df_mbr['r742mpar'] = df_mbr['r742mstf'].apply(lambda x: is_bit_set(x, 8, 3))
        df_mbr['r742mnoq'] = df_mbr['r742mstf'].apply(lambda x: is_bit_set(x, 8, 4))
        df_mbr['r742mst1'] = df_mbr['r742mst1'].apply(lambda x: is_bit_set(x, 8, 0))
        df_mbr['r742mssm'] = df_mbr['r742mst2'].apply(lambda x: is_bit_set(x, 8, 0))
        df_mbr['r742mtrm'] = df_mbr['r742mst2'].apply(lambda x: is_bit_set(x, 8, 1))
        df_mbr['r742mmsm'] = df_mbr['r742mst2'].apply(lambda x: is_bit_set(x, 8, 3))
        df_mbr['r742mmsd'] = df_mbr['r742mst2'].apply(lambda x: is_bit_set(x, 8, 4))
        df_mbr['r742mrem'] = df_mbr['r742mst2'].apply(lambda x: is_bit_set(x, 8, 6))
        df_mbr = df_mbr[Smf74Mbr.__table__.columns.keys()].set_index(
            [col.name for col in Smf74Mbr.__table__.primary_key.columns.values()])
    else:
        df_mbr = pd.DataFrame(columns=Smf74Mbr.__table__.columns.keys()).set_index(
            [col.name for col in Smf74Mbr.__table__.primary_key.columns.values()])
    return df_mbr


def build_omvs(df: pd.DataFrame, df_pro_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for OMVS Kernel Control Data Section which will be uploaded to smf74_omvs table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_pro_idx: The index of the RMF product section dataframe.

    Returns:
        The dataframe for the OMVS Kernel Control Data section.
    """
    if 'r743data' in df.columns:
        df_omvs = col_to_frame(df[df.index.get_level_values('smf_type') == '74.3'], 'r743data', df_pro_idx)
        df_omvs['r743flg'] = df_omvs['r743flg'].apply(lambda x: int(str(x), 16))
        df_omvs['r743ter'] = df_omvs['r743flg'].apply(lambda x: is_bit_set(x, 32, 0))
        df_omvs['r743chpr'] = df_omvs['r743flg'].apply(lambda x: is_bit_set(x, 32, 1))
        df_omvs['r743chus'] = df_omvs['r743flg'].apply(lambda x: is_bit_set(x, 32, 2))
        df_omvs['r743chpu'] = df_omvs['r743flg'].apply(lambda x: is_bit_set(x, 32, 3))
        df_omvs['r743chms'] = df_omvs['r743flg'].apply(lambda x: is_bit_set(x, 32, 4))
        df_omvs['r743chse'] = df_omvs['r743flg'].apply(lambda x: is_bit_set(x, 32, 5))
        df_omvs['r743chsh'] = df_omvs['r743flg'].apply(lambda x: is_bit_set(x, 32, 6))
        df_omvs['r743chsp'] = df_omvs['r743flg'].apply(lambda x: is_bit_set(x, 32, 7))
        df_omvs['r743chma'] = df_omvs['r743flg'].apply(lambda x: is_bit_set(x, 32, 8))
        df_omvs['r743chpa'] = df_omvs['r743flg'].apply(lambda x: is_bit_set(x, 32, 9))
        df_omvs['r743chlr'] = df_omvs['r743flg'].apply(lambda x: is_bit_set(x, 32, 10))
        df_omvs['r743cqsg'] = df_omvs['r743flg'].apply(lambda x: is_bit_set(x, 32, 11))
        df_omvs['r743cpu'] = pd.to_timedelta(df_omvs['r743cpu']) / np.timedelta64(1, 's')
        df_omvs['r743ctmn'] = pd.to_timedelta(df_omvs['r743ctmn']) / np.timedelta64(1, 's')
        df_omvs['r743ctmx'] = pd.to_timedelta(df_omvs['r743ctmx']) / np.timedelta64(1, 's')
        df_omvs = df_omvs[Smf74Omvs.__table__.columns.keys()].set_index(
            [col.name for col in Smf74Omvs.__table__.primary_key.columns.values()])
    else:
        df_omvs = pd.DataFrame(columns=Smf74Omvs.__table__.columns.keys()).set_index(
            [col.name for col in Smf74Omvs.__table__.primary_key.columns.values()])
    return df_omvs


def build_cf(df: pd.DataFrame, df_pro_idx: pd.Index, current_time: dt.datetime) -> pd.DataFrame:
    """Build the dataframe for Coupling Facility which will be uploaded to smf74_cf table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_pro_idx: The index of the RMF product section dataframe.
        current_time: The last update dattime.

    Returns:
        The dataframe for the Coupling Facility.
    """
    convert_2_int = np.vectorize(to_int)
    if 'r744flcf' in df.columns:
        if 'r744gsrg' in df.columns:
            df_cf = cols_to_frame(df[df.index.get_level_values('smf_type') == '74.4'], ['r744flcf', 'r744gsrg'],
                                  df_pro_idx)
        else:
            df_cf = col_to_frame(df[df.index.get_level_values('smf_type') == '74.4'], 'r744flcf', df_pro_idx)
        df_cf['r744fflg'] = df_cf['r744fflg'].apply(lambda x: int(str(x), 16))
        df_cf['r744fflc'] = df_cf['r744fflc'].apply(lambda x: int(str(x), 16))
        df_cf['r744fcei'] = df_cf['r744fflg'].apply(lambda x: is_bit_set(x, 8, 0))
        df_cf['r744fadi'] = df_cf['r744fflg'].apply(lambda x: is_bit_set(x, 8, 1))
        df_cf['r744fpec'] = df_cf['r744fflg'].apply(lambda x: is_bit_set(x, 8, 2))
        df_cf['r744fdyd'] = df_cf['r744fflg'].apply(lambda x: is_bit_set(x, 8, 3))
        df_cf['r744fthn'] = df_cf['r744fflg'].apply(lambda x: is_bit_set(x, 8, 4))
        df_cf['r744fnohw'] = df_cf['r744fflg'].apply(lambda x: is_bit_set(x, 8, 5))
        df_cf['r744fcho'] = df_cf['r744fflc'].apply(lambda x: is_bit_set(x, 8, 0))
        df_cf['r744fmod'] = df_cf['r744fmod'].str.strip(' ')
        df_cf['r744flvl'] = convert_2_int(df_cf['r744flvl'])
        df_cf['last_update_time'] = current_time
        cf_cols = ['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'r744fnam', 'smf74mfv', 'smf74int', 'smf74sam',
                   'smf74cyc', 'smf74mvs', 'r744fadi', 'r744fcei', 'r744fpec', 'r744fdyd', 'r744fthn', 'r744fnohw',
                   'r744fcho', 'r744famv', 'r744fpam', 'r744fmod', 'r744fver', 'r744fmpc', 'r744flpn', 'r744flvl',
                   'r744fseq', 'r744fpsn', 'r744fpdn', 'last_update_time', 'r744fflg', 'r744fflc']
        if 'r744gsrg' in df.columns:
            gsrg_cols = ['r744gcsd', 'r744gcsf', 'r744gtsd', 'r744gtsf', 'r744gdsa', 'r744gdsf', 'r744gdsr', 'r744gtsc',
                         'r744gfsc', 'r744gisc']
            agg_gsrg = {'r744gcsd': 'first', 'r744gcsf': 'first', 'r744gtsd': 'first', 'r744gtsf': 'first',
                        'r744gdsa': 'first', 'r744gdsf': 'first', 'r744gdsr': 'first', 'r744gtsc': 'first',
                        'r744gfsc': 'first', 'r744gisc': 'first'}
            all_cols = cf_cols + gsrg_cols
            df_cf = df_cf[all_cols].groupby(cf_cols).agg(agg_gsrg).reset_index().set_index(
                [col.name for col in Smf74Cf.__table__.primary_key.columns.values()])
        else:
            df_cf = df_cf[cf_cols].drop_duplicates().set_index(
                [col.name for col in Smf74Cf.__table__.primary_key.columns.values()])
    else:
        df_cf = pd.DataFrame(columns=Smf74Cf.__table__.columns.keys()).set_index(
            [col.name for col in Smf74Cf.__table__.primary_key.columns.values()])
    return df_cf


def build_lcf(df: pd.DataFrame, df_pro_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for Local Coupling Facility Data Section which will be uploaded to smf74_lcf table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_pro_idx: The index of the RMF product section dataframe.

    Returns:
        The dataframe for the Local Coupling Facility Data section.
    """
    if 'r744flcf' in df.columns:
        df_lcf = col_to_frame(df[df.index.get_level_values('smf_type') == '74.4'], 'r744flcf', df_pro_idx)
        df_lcf['r744ftim'] = pd.to_timedelta(df_lcf['r744ftim']) / np.timedelta64(1, 's')
        df_lcf['r744fsqu'] = pd.to_timedelta(df_lcf['r744fsqu']) / np.timedelta64(1, 's')
        df_lcf['r744fctm'] = pd.to_timedelta(df_lcf['r744fctm']) / np.timedelta64(1, 's')
        df_lcf['r744fcsq'] = pd.to_timedelta(df_lcf['r744fcsq']) / np.timedelta64(1, 's')
        df_lcf[['r744ftap_1', 'r744ftap_2', 'r744ftap_3', 'r744ftap_4',
                'r744ftap_5', 'r744ftap_6', 'r744ftap_7', 'r744ftap_8']] = pd.DataFrame(df_lcf['r744ftap'].tolist(),
                                                                                        index=df_lcf.index)
        df_lcf[['r744fidp_1', 'r744fidp_2', 'r744fidp_3', 'r744fidp_4',
                'r744fidp_5', 'r744fidp_6', 'r744fidp_7', 'r744fidp_8']] = pd.DataFrame(df_lcf['r744fidp'].tolist(),
                                                                                        index=df_lcf.index)
        df_lcf['r744fidp_1'] = df_lcf['r744fidp_1'].str[2:]
        df_lcf['r744fidp_2'] = df_lcf['r744fidp_2'].str[2:]
        df_lcf['r744fidp_3'] = df_lcf['r744fidp_3'].str[2:]
        df_lcf['r744fidp_4'] = df_lcf['r744fidp_4'].str[2:]
        df_lcf['r744fidp_5'] = df_lcf['r744fidp_5'].str[2:]
        df_lcf['r744fidp_6'] = df_lcf['r744fidp_6'].str[2:]
        df_lcf['r744fidp_7'] = df_lcf['r744fidp_7'].str[2:]
        df_lcf['r744fidp_8'] = df_lcf['r744fidp_8'].str[2:]
        df_lcf = df_lcf.set_index(
            [col.name for col in Smf74Lcf.__table__.primary_key.columns.values()])
    else:
        df_lcf = pd.DataFrame(columns=Smf74Lcf.__table__.columns.keys()).set_index(
            [col.name for col in Smf74Lcf.__table__.primary_key.columns.values()])
    return df_lcf


def build_str(df: pd.DataFrame, df_lcf_idx: pd.Index, current_time: dt.datetime) -> pd.DataFrame:
    """Build the dataframe for Coupling Facility Structure Data Section which will be uploaded to smf74_str table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_lcf_idx: The index of the Local Coupling Facility Data section dataframe.
        current_time: The last update dattime.

    Returns:
        The dataframe for the Coupling Facility Structure Data Section.
    """
    if 'r744qsds' in df.columns:  # Structure Data Section
        df_str = col_to_frame(df[df.index.get_level_values('smf_type') == '74.4'], 'r744qsds', df_lcf_idx)
        df_str['r744qflg'] = df_str['r744qflg'].apply(lambda x: int(str(x), 16))
        df_str['r744qfl1'] = df_str['r744qfl1'].apply(lambda x: int(str(x), 16))
        df_str['r744qver'] = pd.to_datetime(df_str['r744qver'])
        df_str['r744qact'] = df_str['r744qflg'].apply(lambda x: is_bit_set(x, 8, 0))
        df_str['r744qrbn'] = df_str['r744qflg'].apply(lambda x: is_bit_set(x, 8, 1))
        df_str['r744qrbo'] = df_str['r744qflg'].apply(lambda x: is_bit_set(x, 8, 2))
        df_str['r744qtra'] = df_str['r744qflg'].apply(lambda x: is_bit_set(x, 8, 3))
        df_str['r744qhol'] = df_str['r744qflg'].apply(lambda x: is_bit_set(x, 8, 4))
        df_str['r744qdpt'] = df_str['r744qflg'].apply(lambda x: is_bit_set(x, 8, 5))
        df_str['r744qrbp'] = df_str['r744qflg'].apply(lambda x: is_bit_set(x, 8, 6))
        df_str['r744qrbd'] = df_str['r744qflg'].apply(lambda x: is_bit_set(x, 8, 7))
        df_str['r744qaad'] = df_str['r744qfl1'].apply(lambda x: is_bit_set(x, 8, 0))
        df_str['last_update_time'] = current_time
        str_cols = ['smf74xnm', 'smf74iet', 'smf74ist', 'datetime', 'r744fnam', 'r744qstr', 'last_update_time',
                    'r744qsiz', 'r744qver', 'r744qact', 'r744qrbn', 'r744qrbo', 'r744qtra', 'r744qhol', 'r744qdpt',
                    'r744qrbp', 'r744qrbd', 'r744qaad', 'r744qflg', 'r744qfl1']
        df_str = df_str[str_cols].drop_duplicates().set_index(
            [col.name for col in Smf74Str.__table__.primary_key.columns.values()])
    else:
        df_str = pd.DataFrame(columns=Smf74Str.__table__.columns.keys()).set_index(
            [col.name for col in Smf74Str.__table__.primary_key.columns.values()])
    return df_str


def build_sreq(df: pd.DataFrame, df_lcf_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for Coupling Facility Request Data Section which will be uploaded to smf74_sreq table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_lcf_idx: The index of the Local Coupling Facility Data section dataframe.

    Returns:
        The dataframe for the Coupling Facility Request Data Section.
    """
    convert_2_int = np.vectorize(to_int)
    if 'r744sreq' in df.columns:  # Request data section for each structure
        df_sreq = col_to_frame(df[df.index.get_level_values('smf_type') == '74.4'], 'r744sreq', df_lcf_idx)
        df_sreq['r744sver'] = pd.to_datetime(df_sreq['r744sver'])
        df_sreq['r744styp'] = convert_2_int(df_sreq['r744styp'])
        df_sreq['r744slec'] = convert_2_int(df_sreq['r744slec'])
        df_sreq['r744sflg'] = df_sreq['r744sflg'].apply(lambda x: int(str(x), 16))
        df_sreq['r744sxfl'] = df_sreq['r744sxfl'].apply(lambda x: int(str(x), 16))
        df_sreq['r744scei'] = df_sreq['r744sflg'].apply(lambda x: is_bit_set(x, 8, 0))
        df_sreq['r744sadi'] = df_sreq['r744sflg'].apply(lambda x: is_bit_set(x, 8, 1))
        df_sreq['r744scad'] = df_sreq['r744sflg'].apply(lambda x: is_bit_set(x, 8, 2))
        df_sreq['r744sdas'] = df_sreq['r744sflg'].apply(lambda x: is_bit_set(x, 8, 3))
        df_sreq['r744spri'] = df_sreq['r744sflg'].apply(lambda x: is_bit_set(x, 8, 4))
        df_sreq['r744ssec'] = df_sreq['r744sflg'].apply(lambda x: is_bit_set(x, 8, 5))
        df_sreq['r744senc'] = df_sreq['r744sflg'].apply(lambda x: is_bit_set(x, 8, 6))
        df_sreq['r744satm'] = pd.to_timedelta(df_sreq['r744satm']) / np.timedelta64(1, 's')
        df_sreq['r744sstm'] = pd.to_timedelta(df_sreq['r744sstm']) / np.timedelta64(1, 's')
        df_sreq['r744sqtm'] = pd.to_timedelta(df_sreq['r744sqtm']) / np.timedelta64(1, 's')
        df_sreq['r744sdtm'] = pd.to_timedelta(df_sreq['r744sdtm']) / np.timedelta64(1, 's')
        df_sreq['r744spst'] = pd.to_timedelta(df_sreq['r744spst']) / np.timedelta64(1, 's')
        df_sreq['r744srst'] = pd.to_timedelta(df_sreq['r744srst']) / np.timedelta64(1, 's')
        df_sreq['r744scst'] = pd.to_timedelta(df_sreq['r744scst']) / np.timedelta64(1, 's')
        df_sreq['r744slsv'] = pd.to_datetime(df_sreq['r744slsv'], format="%Y-%m-%d %H:%M:%S.%f", errors='coerce')
        df_sreq['r744setm'] = pd.to_timedelta(df_sreq['r744setm']) / np.timedelta64(1, 's')
        df_sreq['r744sxst'] = pd.to_timedelta(df_sreq['r744sxst']) / np.timedelta64(1, 's')
        df_sreq['r744sxap'] = df_sreq['r744sxfl'].apply(lambda x: is_bit_set(x, 8, 0))
        df_sreq['r744sxas'] = df_sreq['r744sxfl'].apply(lambda x: is_bit_set(x, 8, 1))
        df_sreq['r744sxcm'] = df_sreq['r744sxfl'].apply(lambda x: is_bit_set(x, 8, 2))
        df_sreq['r744sxmo'] = df_sreq['r744sxfl'].apply(lambda x: is_bit_set(x, 8, 3))
        df_sreq['r744smtm'] = pd.to_timedelta(df_sreq['r744smtm']) / np.timedelta64(1, 's')
        df_sreq = df_sreq.set_index(
            [col.name for col in Smf74Sreq.__table__.primary_key.columns.values()])
    else:
        df_sreq = pd.DataFrame(columns=Smf74Sreq.__table__.columns.keys()).set_index(
            [col.name for col in Smf74Sreq.__table__.primary_key.columns.values()])
    return df_sreq


def build_cach(df: pd.DataFrame, df_pro_idx: pd.Index, df_sreq: pd.DataFrame) -> pd.DataFrame:
    """Build the dataframe for Local Coupling Facility Cache Data Section which will be uploaded to smf74_cach table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_pro_idx: The index of the RMF product section dataframe.
        df_sreq: The dataframe of Coupling Facility Request Data section.

    Returns:
        The dataframe for the Local Coupling Facility Cache Data section.
    """
    convert_to_list = np.vectorize(converttolist)
    if 'r744cach' in df.columns:  # Cache Data Section
        z = df[(df.index.get_level_values('smf_type') == '74.4')].reset_index()['r744cach'].to_frame().set_index(
            df_pro_idx)
        z.dropna(how='all', inplace=True)
        z['r744cach'] = convert_to_list(z['r744cach'])
        x = z.explode('r744cach').reset_index()
        x['cach_idx'] = x.groupby(['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'smf74sid', 'index']).cumcount() + 1
        x.set_index(['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'smf74sid', 'index', 'cach_idx'], inplace=True)
        df_x = pd.json_normalize(x['r744cach']).set_index(x.index)
        df_cach = df_sreq[df_sreq['r744cdne'] > 0].reset_index().set_index(
            ['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'r744fnam', 'r744snam', 'smf74sid', 'index'])[
            ['r744cdsi', 'r744cdne']]
        df_cach = df_cach.reindex(df_cach.index.repeat(df_cach.r744cdne))
        df_cach['cach_idx'] = df_cach.groupby(
            ['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'r744fnam', 'r744snam', 'smf74sid', 'index']
        ).cumcount() + df_cach['r744cdsi']
        df_cach = df_cach.reset_index().set_index(['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'smf74sid', 'index',
                                                   'cach_idx'])
        df_cach = df_cach.join(df_x)
        df_cach['csc'] = np.nan
        df_cach = df_cach.reset_index()[Smf74Cach.__table__.columns.keys()].set_index(
            [col.name for col in Smf74Cach.__table__.primary_key.columns.values()])
    else:
        df_cach = pd.DataFrame(columns=Smf74Cach.__table__.columns.keys()).set_index(
            [col.name for col in Smf74Cach.__table__.primary_key.columns.values()])
    return df_cach


def build_chpa(df: pd.DataFrame, df_pro_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for Local Coupling Facility Channel Path Data Section which will be uploaded to smf74_chpa table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_pro_idx: The index of the RMF product section dataframe.

    Returns:
        The dataframe for the Local Coupling Facility Channel Path Data section if Channel Path Data section exist, otherwise an empty dataframe.
    """
    substr = np.vectorize(substr_x)
    convert_to_list = np.vectorize(converttolist)
    if 'r744chpa' in df.columns:  # Channel path data section
        z = df[(df.index.get_level_values('smf_type') == '74.4')].reset_index()['r744chpa'].to_frame().set_index(
            df_pro_idx)
        z.dropna(how='all', inplace=True)
        z['r744chpa'] = convert_to_list(z['r744chpa'])
        x = z.explode('r744chpa').reset_index()
        x['chpa_idx'] = x.groupby(['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'smf74sid', 'index']).cumcount() + 1
        x.set_index(['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'smf74sid', 'index', 'chpa_idx'], inplace=True)
        df_chpa = pd.json_normalize(x['r744chpa']).set_index(x.index)
        df_chpa['r744hcpi'] = df_chpa['r744hcpi'].str[2:]
        df_chpa['r744hfl1'] = df_chpa['r744hfl1'].apply(lambda x: int(str(x), 16))
        df_chpa['r744hfl2'] = df_chpa['r744hfl2'].apply(lambda x: int(str(x), 16))
        df_chpa['r744hchf'] = df_chpa['r744hchf'].apply(lambda x: int(str(x), 16))
        df_chpa['r744hhca'] = df_chpa['r744hfl1'].apply(lambda x: is_bit_set(x, 8, 0))
        df_chpa['r744hmov'] = df_chpa['r744hfl1'].apply(lambda x: is_bit_set(x, 8, 1))
        df_chpa['r744hlav'] = df_chpa['r744hfl1'].apply(lambda x: is_bit_set(x, 8, 2))
        df_chpa['r744hdev'] = df_chpa['r744hfl1'].apply(lambda x: is_bit_set(x, 8, 3))
        df_chpa['r744hsav1'] = df_chpa['r744hfl1'].apply(lambda x: is_bit_set(x, 8, 4))
        df_chpa['r744hsav2'] = df_chpa['r744hfl1'].apply(lambda x: is_bit_set(x, 8, 5))
        df_chpa['r744hsav3'] = df_chpa['r744hfl1'].apply(lambda x: is_bit_set(x, 8, 6))
        df_chpa['r744hsav4'] = df_chpa['r744hfl1'].apply(lambda x: is_bit_set(x, 8, 7))
        df_chpa['r744hpcv'] = df_chpa['r744hfl2'].apply(lambda x: is_bit_set(x, 8, 0))
        df_chpa['r744hdeg'] = df_chpa['r744hchf'].apply(lambda x: is_bit_set(x, 8, 0))
        df_chpa['r744hsnd'] = df_chpa['r744hchf'].apply(lambda x: is_bit_set(x, 8, 1))
        df_chpa['r744hlat'] = pd.to_timedelta(df_chpa['r744hlat']) / np.timedelta64(1, 's')
        df_chpa['r744hpcp'] = df_chpa['r744hpcp'].str[2:]
        df_chpa['r744haid'] = df_chpa['r744haid'].str[2:]
        df_chpa['r744hapn'] = df_chpa['r744hapn'].str[2:]
        df_chpa[['r744hsap_1', 'r744hsap_2', 'r744hsap_3', 'r744hsap_4']] = pd.DataFrame(df_chpa['r744hsap'].tolist(),
                                                                                         index=df_chpa.index)
        df_chpa['r744hsap_1'] = substr(df_chpa['r744hsap_1'], 2)
        df_chpa['r744hsap_2'] = substr(df_chpa['r744hsap_2'], 2)
        df_chpa['r744hsap_3'] = substr(df_chpa['r744hsap_3'], 2)
        df_chpa['r744hsap_4'] = substr(df_chpa['r744hsap_4'], 2)
        return df_chpa
    else:
        return pd.DataFrame()


def build_subchpa(df_lcf: pd.DataFrame, df_chpa_: pd.DataFrame) -> pd.DataFrame:
    """Build the dataframe for the possible channel paths from the Lcoal Coupling Facility Data Section and the data will be uploaded to smf74_subchpa table.

    Args:
        df_lcf: The dataframe of the Local Coupling Facility Data Section.
        df_chpa_: The dataframe of the Channel Path Data Section.

    Returns:
        The dataframe of the possible channel paths from the Local Coupling Facility Data Section if there is possible channel paths exist, otherwise an empty dataframe.
    """
    if not df_chpa_.empty:  # Channel path data section
        df_subchpa = df_lcf[df_lcf['r744fcpn'] > 0].reset_index().set_index(
            ['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'r744fnam', 'smf74sid', 'index'])[['r744fcpi', 'r744fcpn']]
        df_subchpa = df_subchpa.reindex(df_subchpa.index.repeat(df_subchpa.r744fcpn))
        df_subchpa['chpa_idx'] = df_subchpa.groupby(
            ['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'r744fnam', 'smf74sid', 'index']
        ).cumcount() + df_subchpa['r744fcpi']
        df_subchpa = df_subchpa.reset_index().set_index(
            ['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'smf74sid', 'index', 'chpa_idx'])
        df_subchpa = df_subchpa.join(df_chpa_)
        df_subchpa['csc'] = np.nan
        df_subchpa = df_subchpa.reset_index()[Smf74Subchpa.__table__.columns.keys()].set_index(
            [col.name for col in Smf74Subchpa.__table__.primary_key.columns.values()])
    else:
        df_subchpa = pd.DataFrame(columns=Smf74Subchpa.__table__.columns.keys()).set_index(
            [col.name for col in Smf74Subchpa.__table__.primary_key.columns.values()])
    return df_subchpa


def build_mscm(df: pd.DataFrame, df_pro_idx: pd.Index, df_sreq: pd.DataFrame) -> pd.DataFrame:
    """Build the dataframe for Coupling Facility Storage Class Memory Data Section which will be uploaded to smf74_mscm table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_pro_idx: The index of the RMF product section dataframe.
        df_sreq: The dataframe of Coupling Facility Request Data section.

    Returns:
        The dataframe for the Coupling Facility Storage Class Memory Data section if there is any, otherwise an empty dataframe.
    """
    convert_to_list = np.vectorize(converttolist)
    if 'r744mscm' in df.columns:  # Storage Class Memory Data Section
        z = df[(df.index.get_level_values('smf_type') == '74.4')].reset_index()['r744mscm'].to_frame().set_index(
            df_pro_idx)
        z.dropna(how='all', inplace=True)
        z['r744mscm'] = convert_to_list(z['r744mscm'])
        x = z.explode('r744mscm').reset_index()
        x['mscm_idx'] = x.groupby(['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'smf74sid', 'index']).cumcount() + 1
        x.set_index(['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'smf74sid', 'index', 'mscm_idx'], inplace=True)
        df_x = pd.json_normalize(x['r744mscm']).set_index(x.index).reset_index()
        df_x['mscm_idx'] = df_x.groupby(['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'smf74sid', 'index']).cumcount() + 1
        df_x['r744mrst'] = pd.to_timedelta(df_x['r744mrst']) / np.timedelta64(1, 's')
        df_x['r744mwst'] = pd.to_timedelta(df_x['r744mwst']) / np.timedelta64(1, 's')
        df_x.set_index(['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'smf74sid', 'index', 'mscm_idx'], inplace=True)
        df_mscm = df_sreq[df_sreq['r744snsc'] > 0].reset_index().set_index(
            ['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'r744fnam', 'r744snam', 'smf74sid', 'index'])[
            ['r744snsc', 'r744sisc']]
        df_mscm = df_mscm.reindex(df_mscm.index.repeat(df_mscm.r744snsc))
        df_mscm['mscm_idx'] = df_mscm.groupby(
            ['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'r744fnam', 'r744snam', 'smf74sid', 'index']
        ).cumcount() + df_mscm['r744sisc']
        df_mscm = df_mscm.reset_index().set_index(['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'smf74sid', 'index',
                                                   'mscm_idx'])
        df_mscm = df_mscm.join(df_x)
        df_mscm['csc'] = np.nan
        df_mscm = df_mscm.reset_index()[Smf74Mscm.__table__.columns.keys()].set_index(
            [col.name for col in Smf74Mscm.__table__.primary_key.columns.values()])
    else:
        df_mscm = pd.DataFrame(columns=Smf74Mscm.__table__.columns.keys()).set_index(
            [col.name for col in Smf74Mscm.__table__.primary_key.columns.values()])
    return df_mscm


def build_adup(df: pd.DataFrame, df_pro_idx: pd.Index, df_sreq: pd.DataFrame) -> pd.DataFrame:
    """Build the dataframe for Coupling Facility Asynchronous CF Duplexing Data Section which will be uploaded to smf74_adup table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_pro_idx: The index of the RMF product section dataframe.
        df_sreq: The dataframe of Coupling Facility Request Data section.

    Returns:
        The dataframe for the Coupling Facility Asynchronous CF Duplexing Data section if there is any, otherwise, an empty dataframe.
    """
    convert_to_list = np.vectorize(converttolist)
    if 'r744adup' in df.columns:  # Asynchronous CF Duplexing Data Section
        z = df[(df.index.get_level_values('smf_type') == '74.4')].reset_index()['r744adup'].to_frame().set_index(
            df_pro_idx)
        z.dropna(how='all', inplace=True)
        z['r744adup'] = convert_to_list(z['r744adup'])
        x = z.explode('r744adup').reset_index()
        x['adup_idx'] = x.groupby(['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'smf74sid', 'index']).cumcount() + 1
        x.set_index(['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'smf74sid', 'index', 'adup_idx'], inplace=True)
        df_x = pd.json_normalize(x['r744adup']).set_index(x.index).reset_index()
        df_x['adup_idx'] = df_x.groupby(['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'smf74sid', 'index']).cumcount() + 1
        df_x['r744apdt'] = pd.to_timedelta(df_x['r744apdt']) / np.timedelta64(1, 's')
        df_x['r744amdt'] = pd.to_timedelta(df_x['r744amdt']) / np.timedelta64(1, 's')
        df_x['r744aqdt'] = pd.to_timedelta(df_x['r744aqdt']) / np.timedelta64(1, 's')
        df_x['r744aqst'] = pd.to_timedelta(df_x['r744aqst']) / np.timedelta64(1, 's')
        df_x['r744acdt'] = pd.to_timedelta(df_x['r744acdt']) / np.timedelta64(1, 's')
        df_x['r744ardt'] = pd.to_timedelta(df_x['r744ardt']) / np.timedelta64(1, 's')
        df_x['r744aott'] = pd.to_timedelta(df_x['r744aott']) / np.timedelta64(1, 's')
        df_x['r744astt'] = pd.to_timedelta(df_x['r744astt']) / np.timedelta64(1, 's')
        df_x.set_index(['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'smf74sid', 'index', 'adup_idx'], inplace=True)
        df_adup = df_sreq[df_sreq['r744sadn'] > 0].reset_index().set_index(
            ['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'r744fnam', 'r744snam', 'smf74sid', 'index'])[
            ['r744sadn', 'r744siad']]
        df_adup = df_adup.reindex(df_adup.index.repeat(df_adup.r744sadn))
        df_adup['adup_idx'] = df_adup.groupby(
            ['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'r744fnam', 'r744snam', 'smf74sid', 'index']
        ).cumcount() + df_adup['r744siad']
        df_adup = df_adup.reset_index().set_index(['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'smf74sid', 'index',
                                                   'adup_idx'])
        df_adup = df_adup.join(df_x)
        df_adup['csc'] = np.nan
        df_adup = df_adup.reset_index()[Smf74Adup.__table__.columns.keys()].set_index(
            [col.name for col in Smf74Adup.__table__.primary_key.columns.values()])
    else:
        df_adup = pd.DataFrame(columns=Smf74Adup.__table__.columns.keys()).set_index(
            [col.name for col in Smf74Adup.__table__.primary_key.columns.values()])
    return df_adup


def build_proc(df: pd.DataFrame, df_lcf_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for Coupling Facility Processor Utilization Data Section which will be uploaded to smf74_proc table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_lcf_idx: The index of the Local Coupling Facility Data section dataframe.

    Returns:
        The dataframe for the Coupling Facility Processor Utilization Data Section.
    """
    if 'r744proc' in df.columns:  # Processor Utilization Data Section
        df_proc = col_to_frame(df[df.index.get_level_values('smf_type') == '74.4'], 'r744proc', df_lcf_idx)
        df_proc['r744ptyp'] = df_proc['r744ptyp'].apply(lambda x: int(str(x), 16))
        df_proc['r744pbsy'] = pd.to_timedelta(df_proc['r744pbsy']) / np.timedelta64(1, 's')
        df_proc['r744pwai'] = pd.to_timedelta(df_proc['r744pwai']) / np.timedelta64(1, 's')
        df_proc['r744ptde'] = df_proc['r744ptyp'].apply(lambda x: is_bit_set(x, 8, 0))
        if 'r744pbsg' not in df_proc.columns:
            df_proc['r744pbsg'], df_proc['r744pcct'], df_proc['r744ptle'] = np.nan, np.nan, np.nan
        df_proc = df_proc[Smf74Proc.__table__.columns.keys()].set_index(
            [col.name for col in Smf74Proc.__table__.primary_key.columns.values()])
    else:
        df_proc = pd.DataFrame(columns=Smf74Proc.__table__.columns.keys()).set_index(
            [col.name for col in Smf74Proc.__table__.primary_key.columns.values()])
    return df_proc


def build_cfrf(df: pd.DataFrame, df_lcf_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for Coupling Facility Remote Facility Data Section which will be uploaded to smf74_cfrf table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_lcf_idx: The index of the Local Coupling Facility Data section dataframe.

    Returns:
        The dataframe for the Coupling Facility Remote Facility Data Section.
    """
    substr = np.vectorize(substr_x)
    if 'r744cfrf' in df.columns:  # Remote facility Data Section (duplexing coupling facility)
        df_cfrf = col_to_frame(df[df.index.get_level_values('smf_type') == '74.4'], 'r744cfrf', df_lcf_idx).rename(
            columns={'r744rnde.ndepartition': 'ndepartition', 'r744rnde.ndetype': 'ndetype',
                     'r744rnde.ndemodel': 'ndemodel', 'r744rnde.ndemfg': 'ndemfg', 'r744rnde.ndeplant': 'ndeplant',
                     'r744rnde.ndesequence': 'ndesequence', 'r744rnde.ndecpcid': 'ndecpcid',
                     'r744rnde.ndebyte1': 'ndeconfigcode'})
        df_cfrf['r744rflg'] = df_cfrf['r744rflg'].apply(lambda x: int(str(x), 16))
        df_cfrf['ndeconfigcode'] = df_cfrf['ndeconfigcode'].apply(lambda x: int(str(x), 16))
        df_cfrf['ndeconfigcode'] = df_cfrf['ndeconfigcode'].apply(lambda x: extractKBits(x, 8, 0, 7))
        df_cfrf['r744rsdt'] = pd.to_timedelta(df_cfrf['r744rsdt']) / np.timedelta64(1, 's')
        df_cfrf['r744rsse'] = pd.to_timedelta(df_cfrf['r744rsse']) / np.timedelta64(1, 's')
        df_cfrf['r744ramst'] = pd.to_timedelta(df_cfrf['r744ramst']) / np.timedelta64(1, 's')
        df_cfrf['r744ramsq'] = pd.to_timedelta(df_cfrf['r744ramsq']) / np.timedelta64(1, 's')
        df_cfrf[['r744rtap_1', 'r744rtap_2', 'r744rtap_3', 'r744rtap_4',
                 'r744rtap_5', 'r744rtap_6', 'r744rtap_7', 'r744rtap_8']] = pd.DataFrame(df_cfrf['r744rtap'].tolist(),
                                                                                         index=df_cfrf.index)
        df_cfrf[['r744ridp_1', 'r744ridp_2', 'r744ridp_3', 'r744ridp_4',
                 'r744ridp_5', 'r744ridp_6', 'r744ridp_7', 'r744ridp_8']] = pd.DataFrame(df_cfrf['r744ridp'].tolist(),
                                                                                         index=df_cfrf.index)
        df_cfrf[['r744rsap_1', 'r744rsap_2', 'r744rsap_3', 'r744rsap_4',
                 'r744rsap_5', 'r744rsap_6', 'r744rsap_7', 'r744rsap_8']] = pd.DataFrame(df_cfrf['r744rsap'].tolist(),
                                                                                         index=df_cfrf.index)
        df_cfrf[['r744rsid_1', 'r744rsid_2', 'r744rsid_3', 'r744rsid_4',
                 'r744rsid_5', 'r744rsid_6', 'r744rsid_7', 'r744rsid_8']] = pd.DataFrame(df_cfrf['r744rsid'].tolist(),
                                                                                         index=df_cfrf.index)
        df_cfrf['r744ridp_1'] = substr(df_cfrf['r744ridp_1'], 2)
        df_cfrf['r744ridp_2'] = substr(df_cfrf['r744ridp_2'], 2)
        df_cfrf['r744ridp_3'] = substr(df_cfrf['r744ridp_3'], 2)
        df_cfrf['r744ridp_4'] = substr(df_cfrf['r744ridp_4'], 2)
        df_cfrf['r744ridp_5'] = substr(df_cfrf['r744ridp_5'], 2)
        df_cfrf['r744ridp_6'] = substr(df_cfrf['r744ridp_6'], 2)
        df_cfrf['r744ridp_7'] = substr(df_cfrf['r744ridp_7'], 2)
        df_cfrf['r744ridp_8'] = substr(df_cfrf['r744ridp_8'], 2)
        df_cfrf['r744rsid_1'] = substr(df_cfrf['r744rsid_1'], 2)
        df_cfrf['r744rsid_2'] = substr(df_cfrf['r744rsid_2'], 2)
        df_cfrf['r744rsid_3'] = substr(df_cfrf['r744rsid_3'], 2)
        df_cfrf['r744rsid_4'] = substr(df_cfrf['r744rsid_4'], 2)
        df_cfrf['r744rsid_5'] = substr(df_cfrf['r744rsid_5'], 2)
        df_cfrf['r744rsid_6'] = substr(df_cfrf['r744rsid_6'], 2)
        df_cfrf['r744rsid_7'] = substr(df_cfrf['r744rsid_7'], 2)
        df_cfrf['r744rsid_8'] = substr(df_cfrf['r744rsid_8'], 2)
        cfrf_cols = Smf74Cfrf.__table__.columns.keys() + ['index']

        df_cfrf = df_cfrf[cfrf_cols].set_index(
            [col.name for col in Smf74Cfrf.__table__.primary_key.columns.values()])
    else:
        df_cfrf = pd.DataFrame(columns=Smf74Cfrf.__table__.columns.keys()).set_index(
            [col.name for col in Smf74Cfrf.__table__.primary_key.columns.values()])
    return df_cfrf


def build_dupchpa(df_cfrf: pd.DataFrame, df_chpa: pd.DataFrame) -> pd.DataFrame:
    """Build the dataframe for the possible channel paths from the Lcoal Coupling Facility Data Section and the data will be uploaded to smf74_dupchpa table.

    Args:
        df_cfrf: The dataframe of the Remote Facility Data Section.
        df_chpa: The dataframe of the Channel Path Data Section.

    Returns:
        The dataframe of the possible channel paths from the Remote Facility Data Section if there is possible channel paths exist, otherwise an empty dataframe.
    """
    if not df_cfrf.empty:
        df_dupchpa = df_cfrf[df_cfrf['r744rcpn'] > 0].reset_index().set_index(
            ['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'r744fnam', 'r744rnam', 'smf74sid', 'index'])[
            ['r744rcpi', 'r744rcpn']]
        df_dupchpa = df_dupchpa.reindex(df_dupchpa.index.repeat(df_dupchpa.r744rcpn))
        df_dupchpa['chpa_idx'] = df_dupchpa.groupby(
            ['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'r744fnam', 'r744rnam', 'smf74sid', 'index']
        ).cumcount() + df_dupchpa['r744rcpi']
        df_dupchpa = df_dupchpa.reset_index().set_index(
            ['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'smf74sid', 'index', 'chpa_idx'])
        df_dupchpa = df_dupchpa.join(df_chpa)
        df_dupchpa['csc'] = np.nan
        df_dupchpa = df_dupchpa.reset_index()[Smf74Dupchpa.__table__.columns.keys()].set_index(
            [col.name for col in Smf74Dupchpa.__table__.primary_key.columns.values()])
    else:
        df_dupchpa = pd.DataFrame(columns=Smf74Dupchpa.__table__.columns.keys()).set_index(
            [col.name for col in Smf74Dupchpa.__table__.primary_key.columns.values()])
    return df_dupchpa


def build_cachsys(df: pd.DataFrame, df_pro_idx: pd.Index, current_time: dt.datetime) -> pd.DataFrame:
    """Build the dataframe for Cache Subsystem which will be uploaded to smf74_cachsys table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_pro_idx: The index of the RMF product section dataframe.
        current_time: The last update time.

    Returns:
        The dataframe for the Cache Subsystem.
    """
    convert_2_int = np.vectorize(to_int)
    if 'r745stat' in df.columns:
        df_cachsys = cols_to_frame(df[df.index.get_level_values('smf_type') == '74.5'], ['r745cntl', 'r745stat'],
                                   df_pro_idx)
        df_cachsys['r745ssid'] = df_cachsys['r745ssid'].str[2:]
        df_cachsys['r748cser'] = df_cachsys['r745ccmt_seqn'].str[2:]
        df_cachsys['r745sft'] = convert_2_int(df_cachsys['r745sft'])
        df_cachsys['r745scs'] = df_cachsys['r745scs'].apply(lambda x: int(str(x), 16))
        df_cachsys['r745svss'] = df_cachsys['r745svss'].apply(lambda x: int(str(x), 16))
        df_cachsys['r745sds1'] = df_cachsys['r745sds1'].apply(lambda x: int(str(x), 16))
        df_cachsys['r745sg2'] = df_cachsys['r745sg2'].apply(lambda x: int(str(x), 16))
        df_cachsys['r745clvl'] = convert_2_int(df_cachsys['r745clvl'])
        df_cachsys['r745cmdl'] = df_cachsys['r745cmdl'].str[2:]
        df_cachsys['r745csc'] = convert_2_int(df_cachsys['r745csc'])
        df_cachsys['r745sos'] = df_cachsys['r745scs'].apply(lambda x: extractKBits(x, 8, 0, 3))
        df_cachsys['r745snr'] = df_cachsys['r745scs'].apply(lambda x: is_bit_set(x, 8, 7))
        df_cachsys['r745snht'] = df_cachsys['r745svss'].apply(lambda x: is_bit_set(x, 8, 0))
        df_cachsys['r745snis'] = df_cachsys['r745svss'].apply(lambda x: is_bit_set(x, 8, 1))
        df_cachsys['r745dfwi'] = df_cachsys['r745svss'].apply(lambda x: is_bit_set(x, 8, 2))
        df_cachsys['r745snds'] = df_cachsys['r745svss'].apply(lambda x: is_bit_set(x, 8, 3))
        df_cachsys['r745snpe'] = df_cachsys['r745svss'].apply(lambda x: is_bit_set(x, 8, 4))
        df_cachsys['r745sdcs'] = df_cachsys['r745sds1'].apply(lambda x: extractKBits(x, 8, 0, 2))
        df_cachsys['r745sdfw'] = df_cachsys['r745sds1'].apply(lambda x: extractKBits(x, 8, 2, 4))
        df_cachsys['r745spdp'] = df_cachsys['r745sds1'].apply(lambda x: is_bit_set(x, 8, 4))
        df_cachsys['r745ssdp'] = df_cachsys['r745sds1'].apply(lambda x: is_bit_set(x, 8, 5))
        df_cachsys['r745sdps'] = df_cachsys['r745sds1'].apply(lambda x: extractKBits(x, 8, 6))
        df_cachsys['r745sds2'] = df_cachsys['r745sds2'].apply(lambda x: int(str(x), 16))
        df_cachsys['r745scol'] = df_cachsys['r745sg2'].apply(lambda x: extractKBits(x, 8, 0, 2))
        df_cachsys['r745sfvs'] = df_cachsys['r745sg2'].apply(lambda x: is_bit_set(x, 8, 2))
        df_cachsys['r745sdbp'] = df_cachsys['r745sg2'].apply(lambda x: is_bit_set(x, 8, 3))
        df_cachsys['r745spda'] = df_cachsys['r745sg2'].apply(lambda x: extractKBits(x, 8, 6))
        df_cachsys['ccmt_seqn'] = df_cachsys['r745ccmt_seqn'].str[2:]
        df_cachsys['last_update_time'] = current_time
        cachsys_cols = ['smf_type', 'r745ccnt', 'last_update_time', 'ccmt_seqn', 'r745clvl', 'r745cmdl', 'r745cuid',
                        'r745csc', 'r745cae', 'r745crtn', 'r745cioc', 'r745cint', 'r745cfdv', 'r745ccmt_typen',
                        'r745ccmt_modn', 'r745ccmt_manuf', 'r745ccmt_pmanu', 'r745ccmt_seqn', 'r745ccmt_tag',
                        'r745svol', 'r745sunt', 'r745sdev', 'r745sln', 'r745sft', 'r745sdid', 'r745snad', 'r745snss',
                        'r745sos', 'r745snr', 'r745snht', 'r745snis', 'r745dfwi', 'r745snds', 'r745snpe', 'r745scln',
                        'r745scsf', 'r745scnf', 'r745savl', 'r745spin', 'r745soff', 'r745sdcs', 'r745sdfw', 'r745spdp',
                        'r745ssdp', 'r745sdps', 'r745sds2', 'r745scnv', 'r745spnd', 'r745scol', 'r745sfvs', 'r745sdbp',
                        'r745spda', 'r745sgl', 'r745scs', 'r745svss', 'r745sds1', 'r745sg2'] + \
                       [col.name for col in Smf74Cachsys.__table__.primary_key.columns.values()]
        df_cachsys = df_cachsys[cachsys_cols].set_index(
            [col.name for col in Smf74Cachsys.__table__.primary_key.columns.values()])
    else:
        df_cachsys = pd.DataFrame(columns=Smf74Cachsys.__table__.columns.keys()).set_index(
            [col.name for col in Smf74Cachsys.__table__.primary_key.columns.values()])
    return df_cachsys


def build_cdev(df: pd.DataFrame, df_cachsys_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for Cache Device Data Section which will be uploaded to smf74_cdev table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_cachsys_idx: The index of the Cache Subsystem dataframe.

    Returns:
        The dataframe for the Cache Device Data Section.
    """
    if 'r745dev' in df.columns:  # Cache Device Data Section
        df_cdev = cols_to_frame(df[df.index.get_level_values('smf_type') == '74.5'], ['r745dev', 'r7451dev'],
                                df_cachsys_idx)
        df_cdev['r745devn'] = df_cdev['r745devn'].str[2:]
        df_cdev['r745dsid'] = df_cdev['r745dsid'].str[2:]
        df_cdev['r745dfl4'] = df_cdev['r745dfl4'].apply(lambda x: int(str(x), 16))
        df_cdev['r745dflg'] = df_cdev['r745dflg'].apply(lambda x: int(str(x), 16))
        df_cdev['r745dvs1'] = df_cdev['r745dvs1'].apply(lambda x: int(str(x), 16))
        df_cdev['r745dsg2'] = df_cdev['r745dsg2'].apply(lambda x: int(str(x), 16))
        df_cdev['r745dev4'] = df_cdev['r745dfl4'].apply(lambda x: is_bit_set(x, 8, 0))
        df_cdev['r745dscs'] = df_cdev['r745dfl4'].apply(lambda x: extractKBits(x, 8, 1, 3))
        df_cdev['r745dnav'] = df_cdev['r745dflg'].apply(lambda x: is_bit_set(x, 8, 0))
        df_cdev['r745dpdf'] = df_cdev['r745dflg'].apply(lambda x: extractKBits(x, 8, 1, 4))
        df_cdev['r745dfrm'] = df_cdev['r745dflg'].apply(lambda x: extractKBits(x, 8, 4))
        df_cdev['r745dsdv'] = df_cdev['r745dvs1'].apply(lambda x: extractKBits(x, 8, 0, 2))
        df_cdev['r745dsfw'] = df_cdev['r745dvs1'].apply(lambda x: extractKBits(x, 8, 2, 4))
        df_cdev['r745dspd'] = df_cdev['r745dvs1'].apply(lambda x: is_bit_set(x, 8, 4))
        df_cdev['r745dssd'] = df_cdev['r745dvs1'].apply(lambda x: is_bit_set(x, 8, 5))
        df_cdev['r745dsdp'] = df_cdev['r745dvs1'].apply(lambda x: extractKBits(x, 8, 6))
        df_cdev['r745dvs2'] = df_cdev['r745dvs2'].apply(lambda x: int(str(x), 16))
        df_cdev['r745dcol'] = df_cdev['r745dsg2'].apply(lambda x: extractKBits(x, 8, 0, 2))
        df_cdev['r745defn'] = df_cdev['r745dsg2'].apply(lambda x: is_bit_set(x, 8, 2))
        df_cdev['r745dbdp'] = df_cdev['r745dsg2'].apply(lambda x: is_bit_set(x, 8, 3))
        df_cdev['r745dpdt'] = np.where(df_cdev['r745sft'] == 0,
                                       df_cdev['r745dsg2'].apply(lambda x: extractKBits(x, 8, 2, 2)),
                                       df_cdev['r745dsg2'].apply(lambda x: extractKBits(x, 8, 6)))
        df_cdev['r745rtir'] = pd.to_timedelta(df_cdev['r745rtir']) / np.timedelta64(1, 's')
        df_cdev['r745rtiw'] = pd.to_timedelta(df_cdev['r745rtiw']) / np.timedelta64(1, 's')
        df_cdev['total_io'] = (df_cdev['r745drcr'] + df_cdev['r745drsr'] + df_cdev['r745drnr'] + df_cdev['r745dwrc']
                               + df_cdev['r745dwsr'] + df_cdev['r745dwnr'] + df_cdev['r745dicl'] + df_cdev['r745dbcr'])
        df_cdev['cache_io'] = (df_cdev['r745drcr'] + df_cdev['r745drsr'] + df_cdev['r745drnr'] + df_cdev['r745dwrc']
                               + df_cdev['r745dwsr'] + df_cdev['r745dwnr'])
        df_cdev['total_hits'] = (df_cdev['r745dcrh'] + df_cdev['r745drsh'] + df_cdev['r745dnrh'] + df_cdev['r745dwch']
                                 + df_cdev['r745dwsh'] + df_cdev['r745dwnh'])
        df_cdev['total_reads'] = df_cdev['r745drcr'] + df_cdev['r745drsr'] + df_cdev['r745drnr']
        df_cdev['read_hits'] = df_cdev['r745dcrh'] + df_cdev['r745drsh'] + df_cdev['r745dnrh']
        df_cdev['total_writes'] = df_cdev['r745dwrc'] + df_cdev['r745dwsr'] + df_cdev['r745dwnr']
        df_cdev['fast_writes'] = df_cdev['r745dfwc'] + df_cdev['r745dfws'] + df_cdev['r745dwnr']
        df_cdev['write_hits'] = df_cdev['r745dwch'] + df_cdev['r745dwsh'] + df_cdev['r745dwnh']
        df_cdev['dasd_io'] = df_cdev['total_reads'] + df_cdev['total_writes'] - df_cdev['total_hits']

        df_cdev['r7451dvn'] = df_cdev['r7451dvn'].str[2:]
        if 'r7451rid' in df_cdev.columns:
            df_cdev['r7451rid'] = df_cdev['r7451rid'].str[2:]
            df_cdev['r7451rrt'] = pd.to_timedelta(df_cdev['r7451rrt']) / np.timedelta64(1, 's')
            df_cdev['r7451wrt'] = pd.to_timedelta(df_cdev['r7451wrt']) / np.timedelta64(1, 's')
        else:
            df_cdev[['r7451rid', 'r7451rrt', 'r7451wrt', 'r7451rrq', 'r7451wrq', 'r7451sr', 'r7451sw']] = np.nan
        if 'r7451xid' in df_cdev.columns:
            df_cdev['r7452prt'] = pd.to_timedelta(df_cdev['r7452prt']) / np.timedelta64(1, 's')
            df_cdev['r7452pwt'] = pd.to_timedelta(df_cdev['r7452pwt']) / np.timedelta64(1, 's')
            df_cdev['r7451xid'] = df_cdev['r7451xid'].str[2:]
        else:
            df_cdev[['r7451xid', 'r7452prt', 'r7452pwt', 'r7452pro', 'r7452pwo', 'r7452pbr', 'r7452pbw']] = np.nan
        df_cdev['r7451inc'] = df_cdev['r7451inc'].apply(lambda x: int(str(x), 16))
        df_cdev['r7451sio'] = df_cdev['r7451inc'].apply(lambda x: is_bit_set(x, 8, 3))
        df_cdev['r7451hpf'] = df_cdev['r7451inc'].apply(lambda x: is_bit_set(x, 8, 4))
        df_cdev['r7451unt'] = df_cdev['r7451inc'].apply(lambda x: extractKBits(x, 8, 5, 7))
        df_cdev['r7451rsv'] = pd.to_timedelta(df_cdev['r7451rsv']) / np.timedelta64(1, 's')
        df_cdev['r7451ct3'] = pd.to_timedelta(df_cdev['r7451ct3']) / np.timedelta64(1, 's')
        df_cdev['r7451ct4'] = pd.to_timedelta(df_cdev['r7451ct4']) / np.timedelta64(1, 's')

    else:
        df_cdev = pd.DataFrame(columns=Smf74Cdev.__table__.columns.keys()).set_index(
            [col.name for col in Smf74Cdev.__table__.primary_key.columns.values()])
    return df_cdev


def build_cntl(df: pd.DataFrame, df_pro_idx: pd.Index,
               df_xpool: pd.DataFrame = pd.DataFrame()) -> pd.DataFrame:
    """Build the dataframe for Enterprise Disk System Control Data Section which will be uploaded to smf74_cntl table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_pro_idx: The index of the RMF product section dataframe.
        df_xpool: The dataframe of Cache Subsystem Extent Pool Statistics section from Subtype 5 and default is an empty dataframe.

    Returns:
        The dataframe for the Enterprise Disk System Control Data Section.
    """
    convert_2_int = np.vectorize(to_int)
    if 'r748cntl' in df.columns:
        df_cntl = col_to_frame(df[df.index.get_level_values('smf_type') == '74.8'], 'r748cntl', df_pro_idx)
        df_cntl['r748cflg'] = df_cntl['r748cflg'].apply(lambda x: int(str(x), 16))
        df_cntl['r748cxvl'] = df_cntl['r748cflg'].apply(lambda x: is_bit_set(x, 8, 0))
        df_cntl['r748clvl'] = convert_2_int(df_cntl['r748clvl'])
        df_cntl['r748csc'] = df_cntl['r748csc'].str[2:]
        df_cntl['r748cscs'] = df_cntl['r748cscs'].str[2:]
        df_cntl['r748cfsc'] = df_cntl['r748cfsc'].str[2:]
        df_cntl['r748cfci'] = pd.to_timedelta(df_cntl['r748cfci']) / np.timedelta64(1, 's')
        df_cntl = df_cntl[Smf74Cntl.__table__.columns.keys()].set_index(
            [col.name for col in Smf74Cntl.__table__.primary_key.columns.values()])

    elif df_xpool.shape[0] > 0:
        df_cntl = df_xpool.reset_index().rename(columns={'ccmt_seqn': 'r748cser'})[
            [col.name for col in Smf74Cntl.__table__.primary_key.columns.values()]].copy().drop_duplicates().set_index(
            [col.name for col in Smf74Cntl.__table__.primary_key.columns.values()])
    else:
        df_cntl = pd.DataFrame(columns=Smf74Cntl.__table__.columns.keys()).set_index(
            [col.name for col in Smf74Cntl.__table__.primary_key.columns.values()])
    return df_cntl


def build_lss(df: pd.DataFrame, df_cntl_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for Enterprise Disk System Link Statistics Section which will be uploaded to smf74_lss table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_cntl_idx: The index of the Control Data section dataframe.

    Returns:
        The dataframe for the Enterprise Disk System Link Statistics Section.
    """
    if 'r748lss' in df.columns:
        df_lss = col_to_frame(df[df.index.get_level_values('smf_type') == '74.8'], 'r748lss', df_cntl_idx)
        df_lss['r748laid'] = df_lss['r748laid'].str[2:]
        df_lss['r748lflg'] = df_lss['r748lflg'].apply(lambda x: int(str(x), 16))
        df_lss['r748lbyt'] = df_lss['r748lflg'].apply(lambda x: is_bit_set(x, 8, 0))
        df_lss['r748ltim'] = df_lss['r748lflg'].apply(lambda x: is_bit_set(x, 8, 1))
        df_lss['r748lert'] = pd.to_timedelta(df_lss['r748lert']) / np.timedelta64(1, 's')
        df_lss['r748lewt'] = pd.to_timedelta(df_lss['r748lewt']) / np.timedelta64(1, 's')
        df_lss['r748lpst'] = pd.to_timedelta(df_lss['r748lpst']) / np.timedelta64(1, 's')
        df_lss['r748lprt'] = pd.to_timedelta(df_lss['r748lprt']) / np.timedelta64(1, 's')
        df_lss['r748lsrt'] = pd.to_timedelta(df_lss['r748lsrt']) / np.timedelta64(1, 's')
        df_lss['r748lswt'] = pd.to_timedelta(df_lss['r748lswt']) / np.timedelta64(1, 's')
        df_lss = df_lss[Smf74Lss.__table__.columns.keys()].set_index(
            [col.name for col in Smf74Lss.__table__.primary_key.columns.values()])
    else:
        df_lss = pd.DataFrame(columns=Smf74Lss.__table__.columns.keys()).set_index(
            [col.name for col in Smf74Lss.__table__.primary_key.columns.values()])
    return df_lss


def build_arry(df: pd.DataFrame, df_cntl_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for Enterprise Disk System Rank Array Data Section which will be uploaded to smf74_arry table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_cntl_idx: The index of the Control Data section dataframe.

    Returns:
        The dataframe for the Enterprise Disk System Rank Array Data Section.
    """
    if 'r748arry' in df.columns:
        df_arry = col_to_frame(df[df.index.get_level_values('smf_type') == '74.8'], 'r748arry', df_cntl_idx)
        df_arry['r748aast'] = df_arry['r748aast'].apply(lambda x: int(str(x), 16))
        df_arry['r748arid'] = df_arry['r748arid'].str[2:]
        df_arry['r748aaid'] = df_arry['r748aaid'].str[2:]
        df_arry['r748adc'] = df_arry['r748aast'].apply(lambda x: extractKBits(x, 8, 0, 2))
        df_arry['r748ard'] = df_arry['r748aast'].apply(lambda x: is_bit_set(x, 8, 2))
        df_arry['r748adt'] = df_arry['r748aast'].apply(lambda x: is_bit_set(x, 8, 3))
        df_arry['r748are'] = df_arry['r748aast'].apply(lambda x: is_bit_set(x, 8, 4))
        df_arry['r748acmp'] = df_arry['r748aast'].apply(lambda x: is_bit_set(x, 8, 6))
        df_arry['rank_cap'] = df_arry['r748aawd'] * df_arry['r748aacp']
        df_arry = df_arry[Smf74Arry.__table__.columns.keys()].set_index(
            [col.name for col in Smf74Arry.__table__.primary_key.columns.values()])
    else:
        df_arry = pd.DataFrame(columns=Smf74Arry.__table__.columns.keys()).set_index(
            [col.name for col in Smf74Arry.__table__.primary_key.columns.values()])
    return df_arry


def agg_r748adc(series):
    if '11' in series.tolist():
        return '11'
    else:
        return '  '


def agg_r748aebc(series):
    if len(set(series)) == 1:
        return series.iloc[0]
    else:
        return 'MIXED'


def agg_r748atyp(series):
    if len(set(series)) == 1:
        return series.iloc[0]
    else:
        return 0


def build_rank(df: pd.DataFrame, df_cntl_idx: pd.Index, df_arry: pd.DataFrame,
               current_time: dt.datetime) -> pd.DataFrame:
    """Build the dataframe for Enterprise Disk System Rank Statistics Section which will be uploaded to smf74_rank table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_cntl_idx: The index of the Control Data section dataframe.
        df_arry: The dataframe of Rank Array Data Section.
        current_time: the last update time.

    Returns:
        The dataframe for the Enterprise Disk System Rank Statistics Section.
    """
    if 'r748rank' in df.columns:
        agg_arry = {'r748aebc': 'last', 'r748atyp': 'last', 'r748aasp': 'min', 'r748aawd': 'sum', 'r748aacp': 'sum',
                    'r748aast': 'last', 'r748adc': agg_r748adc, 'r748ard': 'max', 'r748acmp': 'max',
                    'r748adt': 'max', 'r748are': 'max', 'rank_cap': 'sum'}
        df_rank = col_to_frame(df[df.index.get_level_values('smf_type') == '74.8'], 'r748rank', df_cntl_idx)
        df_rank['r748rtq'] = df_rank['r748rtq'].apply(lambda x: int(str(x), 16))
        df_rank['r748rrid'] = df_rank['r748rrid'].str[2:]
        df_rank['r748rpnm'] = df_rank['r748rpnm'].str[2:]
        df_rank['r748rkrt'] = pd.to_timedelta(df_rank['r748rkrt']) / np.timedelta64(1, 's')
        df_rank['r748rkwt'] = pd.to_timedelta(df_rank['r748rkwt']) / np.timedelta64(1, 's')
        df_rank['data_encrypted_rank'] = df_rank['r748rtq'].apply(lambda x: is_bit_set(x, 8, 0))
        df_rank['compression_rank'] = df_rank['r748rtq'].apply(lambda x: is_bit_set(x, 8, 1))
        df_rank['rank_adapter_id_valid'] = df_rank['r748rtq'].apply(lambda x: is_bit_set(x, 8, 7))
        df_rank['r748rai'] = df_rank['r748rai'].str[2:]
        df_rank['last_update_time'] = current_time
        df_rank.set_index([col.name for col in Smf74Rank.__table__.primary_key.columns.values()], inplace=True)
        if df_arry.shape[0] > 0:
            df_arry_gp = df_arry.reset_index().rename(columns={'r748arid': 'r748rrid'}).groupby(
                [col.name for col in Smf74Rank.__table__.primary_key.columns.values()]).agg(agg_arry)
            df_rank = pd.concat([df_rank, df_arry_gp], axis=1)
            df_rank = df_rank.reset_index()[Smf74Rank.__table__.columns.keys()].set_index(
                [col.name for col in Smf74Rank.__table__.primary_key.columns.values()])
        else:
            # df_rank = df_rank.reset_index().drop(columns=['r748rtq']).set_index(
            df_rank = df_rank.reset_index().set_index(
                [col.name for col in Smf74Rank.__table__.primary_key.columns.values()])
    else:
        df_rank = pd.DataFrame(columns=Smf74Rank.__table__.columns.keys()).set_index(
            [col.name for col in Smf74Rank.__table__.primary_key.columns.values()])
    return df_rank


def build_siol(df: pd.DataFrame, df_cntl_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for Enterprise Disk System Synchronous I/O Link Statistics Section which will be uploaded to smf74_siol table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_cntl_idx: The index of the Control Data section dataframe.

    Returns:
        The dataframe for the Enterprise Disk System Synchronous I/O Link Statistics Section.
    """
    if 'r748siol' in df.columns:
        df_siol = col_to_frame(df[df.index.get_level_values('smf_type') == '74.8'], 'r748siol', df_cntl_idx)
        df_siol['r748sflg'] = df_siol['r748sflg'].apply(lambda x: int(str(x), 16))
        df_siol['r748siid'] = df_siol['r748siid'].str[2:]
        df_siol['r748styp'] = df_siol['r748styp'].str[2:]
        df_siol['r748sspd'] = df_siol['r748sspd'].str[2:]
        df_siol['r748sste'] = df_siol['r748sste'].str[2:]
        df_siol['r748sbyt'] = df_siol['r748sflg'].apply(lambda x: is_bit_set(x, 8, 0))
        df_siol['r748stim'] = df_siol['r748sflg'].apply(lambda x: is_bit_set(x, 8, 1))
        df_siol['r748scrt'] = pd.to_timedelta(df_siol['r748scrt']) / np.timedelta64(1, 's')
        df_siol['r748scwt'] = pd.to_timedelta(df_siol['r748scwt']) / np.timedelta64(1, 's')
        df_siol['r748snwt'] = pd.to_timedelta(df_siol['r748snwt']) / np.timedelta64(1, 's')
        df_siol = df_siol[Smf74Siol.__table__.columns.keys()].set_index(
            [col.name for col in Smf74Siol.__table__.primary_key.columns.values()])
    else:
        df_siol = pd.DataFrame(columns=Smf74Siol.__table__.columns.keys()).set_index(
            [col.name for col in Smf74Siol.__table__.primary_key.columns.values()])
    return df_siol


def build_hfs(df: pd.DataFrame, df_pro_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for Hierarchical File System HFS Global Data Section which will be uploaded to smf74_hfs table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_pro_idx: The index of the RMF product section dataframe.

    Returns:
        The dataframe for the Hierarchical File System HFS Global Data Section.
    """
    if 'r746gdat' in df.columns:
        df_hfs = col_to_frame(df[df.index.get_level_values('smf_type') == '74.6'], 'r746gdat', df_pro_idx)
        df_hfs['r746gsfl'] = df_hfs['r746gsfl'].apply(lambda x: int(str(x), 16))
        df_hfs['r746glrc'] = df_hfs['r746glrc'].str[2:]
        df_hfs['r746glrs'] = df_hfs['r746glrs'].str[2:]
        df_hfs['r746gsrc'] = df_hfs['r746gsrc'].str[2:]
        df_hfs['r746gsrs'] = df_hfs['r746gsrs'].str[2:]
        df_hfs['r746gonr'] = df_hfs['r746gsfl'].apply(lambda x: is_bit_set(x, 8, 0))
        df_hfs['r746gnbl'] = df_hfs['r746gsfl'].apply(lambda x: is_bit_set(x, 8, 1))
        df_hfs['r746gngd'] = df_hfs['r746gsfl'].apply(lambda x: is_bit_set(x, 8, 2))
        df_hfs['r746gpgd'] = df_hfs['r746gsfl'].apply(lambda x: is_bit_set(x, 8, 3))
        df_hfs = df_hfs[Smf74Hfs.__table__.columns.keys()].set_index(
            [col.name for col in Smf74Hfs.__table__.primary_key.columns.values()])
    else:
        df_hfs = pd.DataFrame(columns=Smf74Hfs.__table__.columns.keys()).set_index(
            [col.name for col in Smf74Hfs.__table__.primary_key.columns.values()])
    return df_hfs


def build_gbuf(df: pd.DataFrame, df_pro_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for Hierarchical File System HFS Global Buffer Section which will be uploaded to smf74_gbuf table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_pro_idx: The index of the RMF product section dataframe.

    Returns:
        The dataframe for the Hierarchical File System HFS Global Buffer Section.
    """
    convert_to_list = np.vectorize(converttolist)
    if 'r746gbuf' in df.columns:  # HFS Global Buffer section
        z = df[(df.index.get_level_values('smf_type') == '74.6')].reset_index()['r746gbuf'].to_frame().set_index(
            df_pro_idx)
        z.dropna(how='all', inplace=True)
        z['r746gbuf'] = convert_to_list(z['r746gbuf'])
        x = z.explode('r746gbuf').reset_index()
        x['pool_number'] = x.groupby(['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'smf74sid']).cumcount() + 1
        x.set_index(['csc', 'smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'smf74sid', 'pool_number'], inplace=True)
        df_gbuf = pd.json_normalize(x['r746gbuf']).set_index(x.index).reset_index()
        df_gbuf = df_gbuf[Smf74Gbuf.__table__.columns.keys()].set_index(
            [col.name for col in Smf74Gbuf.__table__.primary_key.columns.values()])
    else:
        df_gbuf = pd.DataFrame(columns=Smf74Gbuf.__table__.columns.keys()).set_index(
            [col.name for col in Smf74Gbuf.__table__.primary_key.columns.values()])
    return df_gbuf


def build_fsys(df: pd.DataFrame, df_pro_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for Hierarchical File System HFS File System Section which will be uploaded to smf74_fsys table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_pro_idx: The index of the RMF product section dataframe.

    Returns:
        The dataframe for the Hierarchical File System HFS File System Section.
    """
    if 'r746fsys' in df.columns:
        df_fsys = col_to_frame(df[df.index.get_level_values('smf_type') == '74.6'], 'r746fsys', df_pro_idx)
        df_fsys['r746fsfl'] = df_fsys['r746fsfl'].apply(lambda x: int(str(x), 16))
        df_fsys['r746fnhs'] = df_fsys['r746fsfl'].apply(lambda x: is_bit_set(x, 8, 0))
        df_fsys['r746fmtc'] = df_fsys['r746fsfl'].apply(lambda x: is_bit_set(x, 8, 1))
        df_fsys['r746ffsm'] = df_fsys['r746fsfl'].apply(lambda x: is_bit_set(x, 8, 2))
        df_fsys['r746fmtm'] = pd.to_datetime(df_fsys['r746fmtm'])
        df_fsys['r746fctm'] = pd.to_datetime(df_fsys['r746fctm'])
        df_fsys['r746fsrc'] = df_fsys['r746fsrc'].str[2:]
        df_fsys['r746fsrs'] = df_fsys['r746fsrs'].str[2:]
        df_fsys = df_fsys[Smf74Fsys.__table__.columns.keys()].set_index(
            [col.name for col in Smf74Fsys.__table__.primary_key.columns.values()])
    else:
        df_fsys = pd.DataFrame(columns=Smf74Fsys.__table__.columns.keys()).set_index(
            [col.name for col in Smf74Fsys.__table__.primary_key.columns.values()])
    return df_fsys


def build_fcd(df: pd.DataFrame, df_pro_idx: pd.Index, current_time: dt.datetime) -> pd.DataFrame:
    """Build the dataframe for FICON Director FCD Global Data Section which will be uploaded to smf74_fcd table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_pro_idx: The index of the RMF product section dataframe.
        current_time: The last update time.

    Returns:
        The dataframe for the FICON Director FCD Global Data Section.
    """
    if 'r747gdat' in df.columns:
        df_fcd = col_to_frame(df[df.index.get_level_values('smf_type') == '74.7'], 'r747gdat', df_pro_idx)
        df_fcd['r747gcfl'] = df_fcd['r747gcfl'].apply(lambda x: int(str(x), 16))
        df_fcd['r747gdca'] = df_fcd['r747gcfl'].apply(lambda x: is_bit_set(x, 8, 0))
        df_fcd['r747giac'] = df_fcd['r747gcfl'].apply(lambda x: is_bit_set(x, 8, 1))
        df_fcd['r747giod'] = df_fcd['r747gcfl'].apply(lambda x: is_bit_set(x, 8, 2))
        df_fcd['r747gicv'] = df_fcd['r747gcfl'].apply(lambda x: is_bit_set(x, 8, 3))
        df_fcd['r747gict'] = pd.to_datetime(df_fcd['r747gicd'] + ' ' +
                                            df_fcd['r747gict'],
                                            format='%m/%d/%Y %H.%M.%S', errors='coerce')
        df_fcd['last_update_time'] = current_time
        df_fcd = df_fcd.drop_duplicates(
            subset=[col.name for col in Smf74Fcd.__table__.primary_key.columns.values()]).drop(
            columns=['csc', 'smf74int', 'r747gicd', 'smf74sid']).set_index(
            [col.name for col in Smf74Fcd.__table__.primary_key.columns.values()])
    else:
        df_fcd = pd.DataFrame(columns=Smf74Fcd.__table__.columns.keys()).set_index(
            [col.name for col in Smf74Fcd.__table__.primary_key.columns.values()])
    return df_fcd


def build_switch(df: pd.DataFrame, df_pro_idx: pd.Index, current_time: dt.datetime) -> pd.DataFrame:
    """Build the dataframe for FICON Director FCD Switch Data Section which will be uploaded to smf74_switch table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_pro_idx: The index of the RMF product section dataframe.
        current_time: The last update time.

    Returns:
        The dataframe for the FICON Director FCD Switch Data Section.
    """
    if 'r747sdat' in df.columns:
        df_switch = col_to_frame(df[df.index.get_level_values('smf_type') == '74.7'], 'r747sdat', df_pro_idx).rename(
            columns={'r747snd.ndetype': 'ndetype', 'r747snd.ndemodel': 'ndemodel', 'r747snd.ndemfg': 'ndemfg',
                     'r747snd.ndeplant': 'ndeplant', 'r747snd.ndecpcid': 'ndecpcid',
                     'r747snd.ndesequence': 'ndesequence', 'r747snd.ndebyte1': 'ndeconfigcode'})
        df_switch['r747sdev'] = df_switch['r747sdev'].str[2:]
        df_switch['r747spfl'] = df_switch['r747spfl'].apply(lambda x: int(str(x), 16))
        df_switch['r747slsn'] = df_switch['r747slsn'].str[2:]
        df_switch['r747svar'] = df_switch['r747spfl'].apply(lambda x: is_bit_set(x, 8, 0))
        df_switch['r747snpc'] = df_switch['r747spfl'].apply(lambda x: is_bit_set(x, 8, 1))
        df_switch['r747soff'] = df_switch['r747spfl'].apply(lambda x: is_bit_set(x, 8, 2))
        df_switch['r747snol'] = df_switch['r747spfl'].apply(lambda x: is_bit_set(x, 8, 3))
        df_switch['r747sfcs'] = df_switch['r747spfl'].apply(lambda x: is_bit_set(x, 8, 4))
        df_switch['ndeconfigcode'] = df_switch['ndeconfigcode'].apply(lambda x: int(str(x), 16))
        df_switch['ndeconfigcode'] = df_switch['ndeconfigcode'].apply(lambda x: extractKBits(x, 8, 0, 7))
        df_switch['last_update_time'] = current_time
        df_switch = df_switch.drop(
            columns=['r747snd.ndepartition', 'csc', 'smf74int', 'smf_type']).set_index(
            [col.name for col in Smf74Switch.__table__.primary_key.columns.values()])
    else:
        df_switch = pd.DataFrame(columns=Smf74Switch.__table__.columns.keys()).set_index(
            [col.name for col in Smf74Switch.__table__.primary_key.columns.values()])
    return df_switch


def build_port(df: pd.DataFrame, df_switch_idx: pd.Index) -> Tuple:
    """Build the dataframe for FICON Director FCD Port Data Section which will be uploaded to smf74_port table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_switch_idx: The index of the FICON Switch Data section dataframe.

    Returns:
        The dataframe for the FICON Director FCD Port Data Section.
        The dataframe for the FICON Connector Data.
    """
    if 'r747pdat' in df.columns:
        df_port = col_to_frame(df[df.index.get_level_values('smf_type') == '74.7'], 'r747pdat', df_switch_idx).rename(
            columns={'r747pand.ndetype': 'ndetype', 'r747pand.ndemodel': 'ndemodel', 'r747pand.ndemfg': 'ndemfg',
                     'r747pand.ndeplant': 'ndeplant', 'r747pand.ndecpcid': 'ndecpcid',
                     'r747pand.ndesequence': 'ndesequence', 'r747pand.ndebyte1': 'ndeconfigcode'})
        df_port['r747padr'] = df_port['r747padr'].str[2:]
        df_port['r747pnum'] = df_port['r747pnum'].str[2:]
        df_port['r747ptfl'] = df_port['r747ptfl'].apply(lambda x: int(str(x), 16))
        df_port['r747psfl'] = df_port['r747psfl'].apply(lambda x: int(str(x), 16))
        df_port['r747ppfl'] = df_port['r747ppfl'].apply(lambda x: int(str(x), 16))
        df_port['r747posy'] = df_port['r747psfl'].apply(lambda x: is_bit_set(x, 8, 2))
        df_port['r747ppir'] = df_port['r747ppfl'].apply(lambda x: is_bit_set(x, 8, 0))
        df_port['r747pnti'] = df_port['r747ppfl'].apply(lambda x: is_bit_set(x, 8, 1))
        df_port['r747plf'] = df_port['r747ppfl'].apply(lambda x: is_bit_set(x, 8, 2))
        df_port['r747poff'] = df_port['r747ppfl'].apply(lambda x: is_bit_set(x, 8, 3))
        df_port['r747pscr'] = df_port['r747ppfl'].apply(lambda x: is_bit_set(x, 8, 4))
        df_port['r747pfpt'] = pd.to_timedelta(df_port['r747pfpt']) / np.timedelta64(1, 's')
        df_port['ndeconfigcode'] = df_port['ndeconfigcode'].apply(lambda x: int(str(x), 16))
        df_port['ndeconfigcode'] = df_port['ndeconfigcode'].apply(lambda x: extractKBits(x, 8, 0, 7))
        df_port['smf74sid'] = np.where(df_port['r747posy'] == 1, df_port['smf74sid'], np.nan)
        df_port = df_port[Smf74Port.__table__.columns.keys()].set_index(
            [col.name for col in Smf74Port.__table__.primary_key.columns.values()])

        df_connector = col_to_frame(df[df.index.get_level_values('smf_type') == '74.7'], 'r747pdat',
                                    df_switch_idx).rename(
            columns={'r747padr': 'r747cadr', 'r747pnum': 'r747cnum', 'r747ptfl': 'r747ctfl', 'r747psfl': 'r747csfl',
                     'r747pcu': 'r747ccu', 'r747pcun': 'r747ccun'})
        df_connector['r747cadr'] = df_connector['r747cadr'].str[2:]
        df_connector['r747ccu'] = df_connector['r747ccu'].str[2:]
        df_connector['r747cnum'] = df_connector['r747cnum'].str[2:]
        df_connector['r747ctfl'] = df_connector['r747ctfl'].apply(lambda x: int(str(x), 16))
        df_connector['r747csfl'] = df_connector['r747csfl'].apply(lambda x: int(str(x), 16))
        df_connector['r747cscu'] = df_connector['r747ctfl'].apply(lambda x: is_bit_set(x, 8, 0))
        df_connector['r747cmcu'] = df_connector['r747ctfl'].apply(lambda x: is_bit_set(x, 8, 1))
        df_connector['r747cchp'] = df_connector['r747ctfl'].apply(lambda x: is_bit_set(x, 8, 2))
        df_connector['r747csw'] = df_connector['r747ctfl'].apply(lambda x: is_bit_set(x, 8, 3))
        df_connector['r747ctnu'] = df_connector['r747csfl'].apply(lambda x: is_bit_set(x, 8, 0))
        df_connector['r747cinu'] = df_connector['r747csfl'].apply(lambda x: is_bit_set(x, 8, 1))
        df_connector['r747cosy'] = df_connector['r747csfl'].apply(lambda x: is_bit_set(x, 8, 2))
        df_connector['r747cins'] = df_connector['r747csfl'].apply(lambda x: is_bit_set(x, 8, 3))
        df_connector['r747cvar'] = df_connector['r747csfl'].apply(lambda x: is_bit_set(x, 8, 4))
        df_connector['r747crem'] = df_connector['r747csfl'].apply(lambda x: is_bit_set(x, 8, 5))
        df_connector['r747cact'] = df_connector['r747csfl'].apply(lambda x: is_bit_set(x, 8, 6))
        df_connector['r747cnmd'] = df_connector['r747csfl'].apply(lambda x: is_bit_set(x, 8, 7))
        df_connector = df_connector[Smf74Connector.__table__.columns.keys()].set_index(
            [col.name for col in Smf74Connector.__table__.primary_key.columns.values()])
    else:
        df_port = pd.DataFrame(columns=Smf74Port.__table__.columns.keys()).set_index(
            [col.name for col in Smf74Port.__table__.primary_key.columns.values()])
        df_connector = pd.DataFrame(columns=Smf74Connector.__table__.columns.keys()).set_index(
            [col.name for col in Smf74Connector.__table__.primary_key.columns.values()])
    return df_port, df_connector


def build_connector(df: pd.DataFrame, df_switch_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for FICON Director FCD Connector Data Section which will be uploaded to smf74_connector table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_switch_idx: The index of the FICON Switch Data section dataframe.

    Returns:
        The dataframe for the FICON Connector Data Section.
    """
    convert_to_list = np.vectorize(converttolist)
    if 'r747cdat' in df.columns:
        z = df[(df.index.get_level_values('smf_type') == '74.7')].reset_index()['r747cdat'].to_frame().set_index(
            df_switch_idx)
        z.dropna(how='all', inplace=True)
        z = z.reset_index().reset_index().set_index(['datetime', 'smf74ist', 'smf74iet', 'r747sdev'])
        z['r747cdat'] = convert_to_list(z['r747cdat'])
        x = z.explode('r747cdat').reset_index()
        x['cdat_idx'] = x.groupby(['datetime', 'smf74ist', 'smf74iet', 'r747sdev']).cumcount() + 1
        x.set_index(['datetime', 'smf74ist', 'smf74iet', 'r747sdev', 'cdat_idx'], inplace=True)
        df_cdat = pd.json_normalize(x['r747cdat']).set_index(x.index).reset_index()
        df_cdat['r747cadr'] = df_cdat['r747cadr'].str[2:]
        df_cdat['r747cnum'] = df_cdat['r747cnum'].str[2:]
        df_cdat['r747ccu'] = df_cdat['r747ccu'].str[2:]
        df_cdat['r747ctfl'] = df_cdat['r747ctfl'].apply(lambda x: int(str(x), 16))
        df_cdat['r747csfl'] = df_cdat['r747csfl'].apply(lambda x: int(str(x), 16))
        df_cdat['r747cscu'] = df_cdat['r747ctfl'].apply(lambda x: is_bit_set(x, 8, 0))
        df_cdat['r747cmcu'] = df_cdat['r747ctfl'].apply(lambda x: is_bit_set(x, 8, 1))
        df_cdat['r747cchp'] = df_cdat['r747ctfl'].apply(lambda x: is_bit_set(x, 8, 2))
        df_cdat['r747csw'] = df_cdat['r747ctfl'].apply(lambda x: is_bit_set(x, 8, 3))
        df_cdat['r747ctnu'] = df_cdat['r747csfl'].apply(lambda x: is_bit_set(x, 8, 0))
        df_cdat['r747cinu'] = df_cdat['r747csfl'].apply(lambda x: is_bit_set(x, 8, 1))
        df_cdat['r747cosy'] = df_cdat['r747csfl'].apply(lambda x: is_bit_set(x, 8, 2))
        df_cdat['r747cins'] = df_cdat['r747csfl'].apply(lambda x: is_bit_set(x, 8, 3))
        df_cdat['r747cvar'] = df_cdat['r747csfl'].apply(lambda x: is_bit_set(x, 8, 4))
        df_cdat['r747crem'] = df_cdat['r747csfl'].apply(lambda x: is_bit_set(x, 8, 5))
        df_cdat['r747cact'] = df_cdat['r747csfl'].apply(lambda x: is_bit_set(x, 8, 6))
        df_cdat['r747cnmd'] = df_cdat['r747csfl'].apply(lambda x: is_bit_set(x, 8, 7))
        df_cdat = df_cdat.set_index(
            ['datetime', 'smf74ist', 'smf74iet', 'r747sdev', 'r747cadr', 'r747cnum', 'cdat_idx'])
    else:
        df_cdat = pd.DataFrame(columns=Smf74Connector.__table__.columns.keys()).set_index(
            [col.name for col in Smf74Connector.__table__.primary_key.columns.values()])
    return df_cdat


def build_pcie(df: pd.DataFrame, df_pro_idx1: pd.Index, df_pro_idx2: pd.Index,
               current_time: dt.datetime) -> pd.DataFrame:
    """Build PCI Express Based Function PCIE Function Data Section which will be uplodaed to smf74_pcie table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_pro_idx1: The index of the RMF product section dataframe with csc, sid and smf_type in the index.
        df_pro_idx2: The index of the RMF product section dataframe without csc, sid and smf_type in the index.
        current_time: The last update time.

    Returns:
        The dataframe for the PCIE Function Data Section.
    """
    convert_to_list = np.vectorize(converttolist)
    cal_std_dev = np.vectorize(calculate_std_dev)
    if 'r749pf' in df.columns:
        df_pcie = col_to_frame(df[df.index.get_level_values('smf_type') == '74.9'], 'r749pf', df_pro_idx1)  # .rename(
        df_pcie['r749pfid'] = df_pcie['r749pfid'].str[-4:]
        df_pcie['r749asid'] = df_pcie['r749asid'].str[2:]
        df_pcie['r749pcid'] = df_pcie['r749pcid'].str[2:]
        df_pcie['r749pffl'] = df_pcie['r749pffl'].apply(lambda x: int(str(x), 16))
        df_pcie['r749pff1'] = df_pcie['r749pff1'].apply(lambda x: int(str(x), 16))
        df_pcie['r749flag'] = df_pcie['r749flag'].apply(lambda x: int(str(x), 16))
        df_pcie['r749atst'] = pd.to_datetime(df_pcie['r749atst'])
        df_pcie['physical_network'] = df_pcie['r749flag'].apply(lambda x: is_bit_set(x, 8, 0))
        df_pcie['pcie_valid'] = df_pcie['r749flag'].apply(lambda x: is_bit_set(x, 8, 1))
        df_pcie['pci_oper_rates_invalid'] = df_pcie['r749flag'].apply(lambda x: is_bit_set(x, 8, 2))
        df_pcie['global_performance'] = df_pcie['r749flag'].apply(lambda x: is_bit_set(x, 8, 3))
        df_pcie['r749errt'] = pd.to_timedelta(df_pcie['r749errt']) / np.timedelta64(1, 's')
        df_pcie['r749allt'] = pd.to_timedelta(df_pcie['r749allt']) / np.timedelta64(1, 's')
        df_pcie['r749lkid'] = df_pcie['r749lkid'].str[2:]
        df_pcie['last_update_time'] = current_time
        df_pcie['status'] = np.where(df_pcie['r749pffl'].apply(lambda x: is_bit_set(x, 8, 0)) == 1, 'Allocated',
                                     np.where(df_pcie['r749pff1'].apply(lambda x: is_bit_set(x, 8, 0)) == 1,
                                              'De-Allocate-Pending',
                                              np.where(df_pcie['r749pff1'].apply(lambda x: is_bit_set(x, 8, 2)) == 1,
                                                       'Error',
                                                       np.where(df_pcie['r749pffl'].apply(
                                                           lambda x: is_bit_set(x, 8, 1)) == 1, 'De-allocated',
                                                                np.where(df_pcie['r749pff1'].apply(
                                                                    lambda x: is_bit_set(x, 8, 1)) == 1,
                                                                         'Re-allocated', 'Unknown')))))
        df_pcie['pciload'] = df_pcie['r749loop'] / df_pcie['r749allt']
        df_pcie['pcistor'] = df_pcie['r749stop'] / df_pcie['r749allt']
        df_pcie['pcistbl'] = df_pcie['r749sbop'] / df_pcie['r749allt']
        df_pcie['pcirptr'] = df_pcie['r749rfop'] / df_pcie['r749allt']

        df_pcie = df_pcie.set_index(
            [col.name for col in Smf74Pcie.__table__.primary_key.columns.values()])

        if 'r749sync' in df.columns:
            sync_z = df[(df.index.get_level_values('smf_type') == '74.9')].reset_index()[
                'r749sync'].to_frame().set_index(df_pro_idx2)
            sync_z.dropna(how='all', inplace=True)
            sync_z['r749sync'] = convert_to_list(sync_z['r749sync'])
            sync_x = sync_z.explode('r749sync').reset_index()
            sync_x['r749sioo'] = sync_x.groupby(['datetime', 'smf74ist', 'smf74iet', 'index']).cumcount()
            sync_x.set_index(['datetime', 'smf74ist', 'smf74iet', 'index', 'r749sioo'], inplace=True)
            df_sync = pd.json_normalize(sync_x['r749sync']).set_index(sync_x.index)
            df_pcie = df_pcie.reset_index().set_index(['datetime', 'smf74ist', 'smf74iet', 'index', 'r749sioo'])
            df_pcie_1 = df_pcie[df_pcie['r749sion'] > 0].join(df_sync)
            df_pcie = pd.concat([df_pcie_1, df_pcie[df_pcie['r749sion'] == 0]], axis=0)
            df_pcie = df_pcie.reset_index().set_index(
                [col.name for col in Smf74Pcie.__table__.primary_key.columns.values()])
        if 'r749dma' in df.columns:
            dma_z = df[(df.index.get_level_values('smf_type') == '74.9')].reset_index()['r749dma'].to_frame().set_index(
                df_pro_idx2)
            dma_z.dropna(how='all', inplace=True)
            dma_z['r749dma'] = convert_to_list(dma_z['r749dma'])
            dma_x = dma_z.explode('r749dma').reset_index()
            dma_x['r749dmao'] = dma_x.groupby(['datetime', 'smf74iet', 'smf74iet', 'index']).cumcount()
            dma_x.set_index(['datetime', 'smf74ist', 'smf74iet', 'index', 'r749dmao'], inplace=True)
            df_dma = pd.json_normalize(dma_x['r749dma']).set_index(dma_x.index)
            if "0x04" in df_dma['r749dfmt'].values:  # any(df_dma['r749dfmt'] == "0x04"):
                df_dma['r749stpf'] = pd.to_timedelta(df_dma['r749stpf']) / np.timedelta64(1, 's')
                df_dma['r749stpc'] = pd.to_timedelta(df_dma['r749stpc']) / np.timedelta64(1, 's')
            df_pcie = df_pcie.reset_index().set_index(['datetime', 'smf74ist', 'smf74iet', 'index', 'r749dmao'])
            df_pcie_1 = df_pcie[df_pcie['r749dman'] > 0].join(df_dma)
            df_pcie = pd.concat([df_pcie_1, df_pcie[df_pcie['r749dman'] == 0]], axis=0)
            if "0x00" in df_pcie['r749dfmt'].values:  # any(df_pcie['r749dfmt'] == "0x00"):
                df_pcie['pcidmar'] = np.where(df_pcie['r749dfmt'] == '0x00',
                                              df_pcie['r749dmar'] / (df_pcie['r749allt'] * 1e6), np.nan)
                df_pcie['pcidmaw'] = np.where(df_pcie['r749dfmt'] == '0x00',
                                              df_pcie['r749dmaw'] / (df_pcie['r749allt'] * 1e6), np.nan)
            if "0x01" in df_pcie['r749dfmt'].values:  # any(df_pcie['r749dfmt'] == "0x01"):
                df_pcie['pcibytr'] = np.where(df_pcie['r749dfmt'] == "0x01",
                                              df_pcie['r749dbyr'] / (df_pcie['r749allt'] * 1e6), np.nan)
                df_pcie['pcipakr'] = np.where(df_pcie['r749dfmt'] == "0x01",
                                              df_pcie['r749dpkr'] / df_pcie['r749allt'], np.nan)
                df_pcie['pcipakt'] = np.where(df_pcie['r749dfmt'] == "0x01",
                                              df_pcie['r749dpkt'] / df_pcie['r749allt'], np.nan)
            if df_pcie['r749dfmt'].isin(["0x01", "0x03"]).any():
                df_pcie['pcibytt'] = np.where(df_pcie['r749dfmt'] == "0x01",
                                              df_pcie['r749dbyt'] / (df_pcie['r749allt'] * 1e6),
                                              np.where(df_pcie['r749dfmt'] == "0x03",
                                                       df_pcie['r749dbyx'] / (df_pcie['r749allt'] * 1e6), np.nan))
            if "0x02" in df_pcie['r749dfmt'].values:  # any(df_pcie['r749dfmt'] == "0x02"):
                df_pcie['pciwup'] = np.where(df_pcie['r749dfmt'] == "0x02",
                                             df_pcie['r749dwup'] / df_pcie['r749allt'], np.nan)
                df_pcie['pciutil'] = np.where(df_pcie['r749dfmt'] == "0x02",
                                              df_pcie['r749dwup'] * 100 / (df_pcie['r749allt'] * df_pcie['r749dwum']),
                                              np.nan)
            if "0x04" in df_pcie['r749dfmt'].values:  # any(df_pcie['r749dfmt'] == "0x04"):
                if 'fpgbusy' in df_pcie.columns:
                    df_pcie['fpgbusy'] = np.where((df_pcie['r749sion'] > 0) & (df_pcie['r749dfmt'] == "0x04"),
                                                  df_pcie['r749stpf'] * 100 / df_pcie['r749allt'], df_pcie['fpgbusy'])
                else:
                    df_pcie['fpgbusy'] = np.where((df_pcie['r749sion'] > 0) & (df_pcie['r749dfmt'] == "0x04"),
                                                  df_pcie['r749stpf'] * 100 / df_pcie['r749allt'], np.nan)
                df_pcie['synctr'] = np.where((df_pcie['r749sion'] > 0) & (df_pcie['r749dfmt'] == "0x04"),
                                             (df_pcie['r749ssrf'] + df_pcie['r749slrf'] + df_pcie['r749srrf']) /
                                             df_pcie['r749allt'], np.nan)
                df_pcie['syncsr'] = np.where((df_pcie['r749sion'] > 0) & (df_pcie['r749dfmt'] == "0x04"),
                                             df_pcie['r749ssrf'] / df_pcie['r749allt'], np.nan)
                df_pcie['pcibytr'] = np.where((df_pcie['r749sion'] > 0) & (df_pcie['r749dfmt'] == "0x04"),
                                              df_pcie['r749srbf'] / (df_pcie['r749allt'] * 1e6), np.nan)
                df_pcie['pcibytt'] = np.where((df_pcie['r749sion'] > 0) & (df_pcie['r749dfmt'] == "0x04"),
                                              df_pcie['r749swbf'] / (df_pcie['r749allt'] * 1e6), np.nan)
                df_pcie['pcibytr_ratio'] = np.where((df_pcie['r749sion'] > 0) & (df_pcie['r749dfmt'] == "0x04"),
                                                    df_pcie['r749srbf'] / (df_pcie['r749ssrf'] * 1e6), np.nan)
                df_pcie['pcibytt_ratio'] = np.where((df_pcie['r749sion'] > 0) & (df_pcie['r749dfmt'] == "0x04"),
                                                    df_pcie['r749swbf'] / (df_pcie['r749ssrf'] * 1e6), np.nan)

                df_pcie['cpcfpgbusy'] = np.where(
                    (df_pcie['r749sion'] > 0) & (df_pcie['global_performance'] == 1) & (df_pcie['r749dfmt'] == "0x04"),
                    df_pcie['r749stpc'] * 100 / df_pcie['r749allt'], np.nan)
                df_pcie['cpcsynctr'] = np.where(
                    (df_pcie['r749sion'] > 0) & (df_pcie['global_performance'] == 1) & (df_pcie['r749dfmt'] == "0x04"),
                    (df_pcie['r749ssrc'] + df_pcie['r749slrc'] + df_pcie['r749srrc']) / df_pcie['r749allt'], np.nan)
                df_pcie['cpcsyncsr'] = np.where(
                    (df_pcie['r749sion'] > 0) & (df_pcie['global_performance'] == 1) & (df_pcie['r749dfmt'] == "0x04"),
                    df_pcie['r749ssrc'] / df_pcie['r749allt'], np.nan)
                df_pcie['cpcpcibytr'] = np.where(
                    (df_pcie['r749sion'] > 0) & (df_pcie['global_performance'] == 1) & (df_pcie['r749dfmt'] == "0x04"),
                    df_pcie['r749srbc'] / (df_pcie['r749allt'] * 1e6), np.nan)
                df_pcie['cpcpcibytt'] = np.where(
                    (df_pcie['r749sion'] > 0) & (df_pcie['global_performance'] == 1) & (df_pcie['r749dfmt'] == "0x04"),
                    df_pcie['r749swbc'] / (df_pcie['r749allt'] * 1e6), np.nan)
                df_pcie['cpcpcibytr_ratio'] = np.where(
                    (df_pcie['r749sion'] > 0) & (df_pcie['global_performance'] == 1) & (df_pcie['r749dfmt'] == "0x04"),
                    df_pcie['r749srbc'] / (df_pcie['r749ssrc'] * 1e6), np.nan)
                df_pcie['cpcpcibytt_ratio'] = np.where(
                    (df_pcie['r749sion'] > 0) & (df_pcie['global_performance'] == 1) & (df_pcie['r749dfmt'] == "0x04"),
                    df_pcie['r749swbc'] / (df_pcie['r749ssrc'] * 1e6), np.nan)
            df_pcie = df_pcie.reset_index().set_index(
                [col.name for col in Smf74Pcie.__table__.primary_key.columns.values()])
        if 'r749hwa' in df.columns:
            hwa_z = df[(df.index.get_level_values('smf_type') == '74.9')].reset_index()['r749hwa'].to_frame().set_index(
                df_pro_idx2)
            hwa_z.dropna(how='all', inplace=True)
            hwa_z['r749hwa'] = convert_to_list(hwa_z['r749hwa'])
            hwa_x = hwa_z.explode('r749hwa').reset_index()
            hwa_x['r749fpfo'] = hwa_x.groupby(['datetime', 'smf74ist', 'smf74iet', 'index']).cumcount()
            hwa_x.set_index(['datetime', 'smf74ist', 'smf74iet', 'index', 'r749fpfo'], inplace=True)
            df_hwa = pd.json_normalize(hwa_x['r749hwa']).set_index(hwa_x.index)
            df_hwa['r749ftet'] = pd.to_timedelta(df_hwa['r749ftet']) / np.timedelta64(1, 's')
            df_hwa['r749ftqt'] = pd.to_timedelta(df_hwa['r749ftqt']) / np.timedelta64(1, 's')
            df_pcie = df_pcie.reset_index().set_index(['datetime', 'smf74ist', 'smf74iet', 'index', 'r749fpfo'])
            df_pcie_1 = df_pcie[df_pcie['r749fpfn'] > 0].join(df_hwa)
            df_pcie = pd.concat([df_pcie_1, df_pcie[df_pcie['r749fpfn'] == 0]], axis=0)
            df_pcie['fpgbusy'] = df_pcie['r749ftet'] * 100 / df_pcie['r749allt']
            df_pcie['fpgrtim'] = df_pcie['r749ftet'] * 1e6 / df_pcie['r749frqc']
            df_pcie['fpgqtim'] = df_pcie['r749ftqt'] * 1e6 / df_pcie['r749frqc']
            df_pcie['fpgbyts'] = (df_pcie['r749fdrd'] + df_pcie['r749fdwr']) * 256 / (df_pcie['r749allt'] * 1e6)
            df_pcie['fpgbytr'] = (df_pcie['r749fdrd'] + df_pcie['r749fdwr']) * 256 / (df_pcie['r749frqc'] * 1000)
            df_pcie['stdd_ftet'] = cal_std_dev(df_pcie['r749frqc'] + df_pcie['r749frqe'], df_pcie['r749fsqe'],
                                               df_pcie['r749ftet'] * 1e6)
            df_pcie['stdd_ftqt'] = cal_std_dev(df_pcie['r749frqc'] + df_pcie['r749frqe'], df_pcie['r749fsqq'],
                                               df_pcie['r749ftqt'] * 1e6)
            df_pcie = df_pcie.reset_index().set_index(
                [col.name for col in Smf74Pcie.__table__.primary_key.columns.values()])
        if 'r749hwa1' in df.columns:
            hwa1_z = df[(df.index.get_level_values('smf_type') == '74.9')].reset_index()[
                'r749hwa1'].to_frame().set_index(df_pro_idx2)
            hwa1_z.dropna(how='all', inplace=True)
            hwa1_z['r749hwa1'] = convert_to_list(hwa1_z['r749hwa1'])
            hwa1_x = hwa1_z.explode('r749hwa1').reset_index()
            hwa1_x['r749fp1o'] = hwa1_x.groupby(['datetime', 'smf74ist', 'smf74iet', 'index']).cumcount()
            hwa1_x.set_index(['datetime', 'smf74ist', 'smf74iet', 'index', 'r749fp1o'], inplace=True)
            df_hwa1 = pd.json_normalize(hwa1_x['r749hwa1']).set_index(hwa1_x.index)
            df_pcie = df_pcie.reset_index().set_index(['datetime', 'smf74ist', 'smf74iet', 'index', 'r749fp1o'])
            df_pcie_1 = df_pcie[df_pcie['r749fp1n'] > 0].join(df_hwa1)
            df_pcie = pd.concat([df_pcie_1, df_pcie[df_pcie['r749fp1n'] == 0]], axis=0)
            df_pcie['fpgcors'] = df_pcie['r7491dct'] / df_pcie['r749allt']
            df_pcie['fpgcobs'] = df_pcie['r7491dib'] / (df_pcie['r749allt'] * 1e6)
            df_pcie['fpgcort'] = df_pcie['r7491dib'] / df_pcie['r7491dob']
            df_pcie['fpgdcrs'] = df_pcie['r7491ict'] / df_pcie['r749allt']
            df_pcie['fpgdcbs'] = df_pcie['r7491iib'] / (df_pcie['r749allt'] * 1e6)
            df_pcie['fpgdcrt'] = df_pcie['r7491iib'] / df_pcie['r7491iob']
            df_pcie['fpgbprt'] = df_pcie['r7491bpc'] / (
                    (df_pcie['r7491dct'] + df_pcie['r7491ict']) * df_pcie['r7491bps'])
            df_pcie['stdd_1dib'] = cal_std_dev(df_pcie['r7491dct'], df_pcie['r7491dis'], df_pcie['r7491dib'])
            df_pcie['stdd_1dob'] = cal_std_dev(df_pcie['r7491dct'], df_pcie['r7491dos'], df_pcie['r7491dob'])
            df_pcie['stdd_1iib'] = cal_std_dev(df_pcie['r7491ict'], df_pcie['r7491iis'], df_pcie['r7491iib'])
            df_pcie['stdd_1iob'] = cal_std_dev(df_pcie['r7491ict'], df_pcie['r7491ios'], df_pcie['r7491iob'])
            df_pcie = df_pcie.reset_index().set_index(
                [col.name for col in Smf74Pcie.__table__.primary_key.columns.values()])
    else:
        df_pcie = pd.DataFrame(columns=Smf74Pcie.__table__.columns.keys()).set_index(
            [col.name for col in Smf74Pcie.__table__.primary_key.columns.values()])
    return df_pcie


def build_srtd(df: pd.DataFrame, df_pro_idx: pd.Index, df_pcie: pd.DataFrame) -> pd.DataFrame:
    """Build PCI Express Based Function Synchronous I/O Response Time Distribution Data Section which will be uplodaed to smf74_srtd table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_pro_idx: The index of the RMF product section dataframe.
        df_pcie: The dataframe of PCIE Function Data Section.

    Returns:
        The dataframe for the Synchronouse I/O Response Time Distribution Data Section.
    """
    convert_to_list = np.vectorize(converttolist)
    if 'r749srtd' in df.columns:
        srtd_z = df[(df.index.get_level_values('smf_type') == '74.9')].reset_index()['r749srtd'].to_frame().set_index(
            df_pro_idx)
        srtd_z.dropna(how='all', inplace=True)
        srtd_z['r749srtd'] = convert_to_list(srtd_z['r749srtd'])
        srtd_x = srtd_z.explode('r749srtd').reset_index()
        srtd_x['r749rtdo_idx'] = srtd_x.groupby(['datetime', 'smf74ist', 'smf74iet', 'index']).cumcount()
        srtd_x.set_index(['datetime', 'smf74ist', 'smf74iet', 'index', 'r749rtdo_idx'], inplace=True)
        srtd_df = pd.json_normalize(srtd_x['r749srtd']).set_index(srtd_x.index)
        srtd_df['r749rflg'] = srtd_df['r749rflg'].apply(lambda x: int(str(x), 16))
        srtd_df['response_time_for_sync_io_read'] = srtd_df['r749rflg'].apply(lambda x: is_bit_set(x, 8, 0))
        srtd_df['response_time_for_sync_io_write'] = srtd_df['r749rflg'].apply(lambda x: is_bit_set(x, 8, 1))
        srtd_df['r749rtrv'] = pd.to_timedelta(srtd_df['r749rtrv']) / np.timedelta64(1, 's')
        df_srtd = df_pcie[df_pcie['r749rtdn'] > 0].reset_index().set_index(
            ['datetime', 'smf74ist', 'smf74iet', 'r749pfid', 'index'])[['r749rtdo', 'r749rtdn']]
        df_srtd = df_srtd.reindex(df_srtd.index.repeat(df_srtd.r749rtdn))
        df_srtd['r749rtdo_idx'] = df_srtd.groupby(['datetime', 'smf74ist', 'smf74iet', 'r749pfid', 'index']
                                                  ).cumcount() + df_srtd['r749rtdo']
        df_srtd = df_srtd.reset_index().set_index(['datetime', 'smf74ist', 'smf74iet', 'index', 'r749rtdo_idx'])
        df_srtd = df_srtd.join(srtd_df)
        df_srtd['srtd_idx'] = df_srtd.groupby(
            ['datetime', 'smf74ist', 'smf74iet', 'r749pfid', 'response_time_for_sync_io_write']).cumcount()
        df_srtd = df_srtd.reset_index()[Smf74Srtd.__table__.columns.keys()].set_index(
            ['datetime', 'smf74ist', 'smf74iet', 'r749pfid', 'response_time_for_sync_io_write', 'srtd_idx'])
    else:
        df_srtd = pd.DataFrame(columns=Smf74Srtd.__table__.columns.keys()).set_index(
            [col.name for col in Smf74Srtd.__table__.primary_key.columns.values()])
    return df_srtd


def build_scm(df: pd.DataFrame, df_pro_idx: pd.Index) -> pd.DataFrame:
    """Build Extended Asynchronous Data Mover (EADM) Storage Class Memory (SCM) Configuration Measurement Section which will be uplodaed to smf74_scm table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_pro_idx: The index of the RMF product section dataframe.

    Returns:
        The dataframe for the Storage Class Memory (SCM) Configuration Measurement Section.
    """
    if 'r7410cm' in df.columns:
        df_scm = col_to_frame(df[df.index.get_level_values('smf_type') == '74.10'], 'r7410cm', df_pro_idx)
        df_scm['r7410crid'] = df_scm['r7410crid'].str[2:]
        df_scm['r7410cpid'] = df_scm['r7410cpid'].str[2:]
        df_scm['r7410flg'] = df_scm['r7410flg'].apply(lambda x: int(str(x), 16))
        df_scm['r7410crtc'] = pd.to_timedelta(df_scm['r7410crtc']) / np.timedelta64(1, 's')
        df_scm['r7410crt'] = pd.to_timedelta(df_scm['r7410crt']) / np.timedelta64(1, 's')
        df_scm['r7410ciqc'] = pd.to_timedelta(df_scm['r7410ciqc']) / np.timedelta64(1, 's')
        df_scm['r7410vfm'] = df_scm['r7410flg'].apply(lambda x: is_bit_set(x, 8, 0))

        df_scm['r7410cdwc_bytes'] = df_scm['r7410cdwc'] * df_scm['r7410cdus']
        df_scm['r7410cdw_bytes'] = df_scm['r7410cdw'] * df_scm['r7410cdus']
        df_scm['r7410cdrc_bytes'] = df_scm['r7410cdrc'] * df_scm['r7410cdus']
        df_scm['r7410cdr_bytes'] = df_scm['r7410cdr'] * df_scm['r7410cdus']
        df_scm = df_scm[Smf74Scm.__table__.columns.keys()].set_index(
            [col.name for col in Smf74Scm.__table__.primary_key.columns.values()])
    else:
        df_scm = pd.DataFrame(columns=Smf74Scm.__table__.columns.keys()).set_index(
            [col.name for col in Smf74Scm.__table__.primary_key.columns.values()])
    return df_scm


def build_eadm(df: pd.DataFrame, df_pro_idx: pd.Index) -> pd.DataFrame:
    """Build Extended Asynchronous Data Mover (EADM) Device (Subchannel) Information Section which will be uplodaed to smf74_eadm table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_pro_idx: The index of the RMF product section dataframe.

    Returns:
        The dataframe for the Extended Asynchronous Data Mover (EADM) device (Subchannel) Information Section.
    """
    if 'r7410di' in df.columns:
        df_eadm = col_to_frame(df[df.index.get_level_values('smf_type') == '74.10'], 'r7410di', df_pro_idx)
        df_eadm['r7410dflg'] = df_eadm['r7410dflg'].apply(lambda x: int(str(x), 16))
        df_eadm['r7410dfpt'] = pd.to_timedelta(df_eadm['r7410dfpt']) / np.timedelta64(1, 's')
        df_eadm['r7410diqt'] = pd.to_timedelta(df_eadm['r7410diqt']) / np.timedelta64(1, 's')
        df_eadm['r7410dcrt'] = pd.to_timedelta(df_eadm['r7410dcrt']) / np.timedelta64(1, 's')
        df_eadm['r7410ecpr'] = df_eadm['r7410dflg'].apply(lambda x: is_bit_set(x, 8, 0))
        df_eadm = df_eadm[Smf74Eadm.__table__.columns.keys()].set_index(
            [col.name for col in Smf74Eadm.__table__.primary_key.columns.values()])
    else:
        df_eadm = pd.DataFrame(columns=Smf74Eadm.__table__.columns.keys()).set_index(
            [col.name for col in Smf74Eadm.__table__.primary_key.columns.values()])
    return df_eadm


def format_74df(df: pd.DataFrame, current_time: dt.datetime) -> dict:
    """Format smf72 JSON files to the dataframes.

    Args:
        df: JSON dataframe.
        current_time: current time in datetime format.

    Returns:
        A dictionary of dataframes.
    """
    dfs_dict = {'dctl': pd.DataFrame(), 'dev': pd.DataFrame(), 'xctl': pd.DataFrame(), 'sys': pd.DataFrame(),
                'path': pd.DataFrame(), 'mbr': pd.DataFrame(), 'omvs': pd.DataFrame(), 'cf': pd.DataFrame(),
                'proc': pd.DataFrame(), 'str': pd.DataFrame(), 'lcf': pd.DataFrame(), 'sreq': pd.DataFrame(),
                'cach': pd.DataFrame(), 'cfrf': pd.DataFrame(), 'subchpa': pd.DataFrame(), 'dupchpa': pd.DataFrame(),
                'mscm': pd.DataFrame(), 'adup': pd.DataFrame(), 'cachsys': pd.DataFrame(), 'rrank': pd.DataFrame(),
                'cntl': pd.DataFrame(), 'lss': pd.DataFrame(), 'rank': pd.DataFrame(), 'arry': pd.DataFrame(),
                'extp': pd.DataFrame(), 'siol': pd.DataFrame(), 'cdev': pd.DataFrame(), 'raid': pd.DataFrame(),
                'xpool': pd.DataFrame(), 'hfs': pd.DataFrame(), 'gbuf': pd.DataFrame(), 'fsys': pd.DataFrame(),
                'fcd': pd.DataFrame(), 'switch': pd.DataFrame(),
                'port': pd.DataFrame(), 'connector': pd.DataFrame(), 'pcie': pd.DataFrame(), 'srtd': pd.DataFrame(),
                'scm': pd.DataFrame(), 'eadm': pd.DataFrame(), 'pro': pd.DataFrame()
                }

    if 'smf74pro' not in df.columns:
        return dfs_dict
    else:
        dfs_dict['pro'] = build_pro(df)

    if dfs_dict['pro'].empty:
        # Cannot continue processing
        return dfs_dict

    df.set_index(dfs_dict['pro'].index, inplace=True)
    if '74.1' in dfs_dict['pro'].index.get_level_values('smf_type'):  # Contains subtype 1 records
        dfs_dict['dctl'] = build_dctl(df, dfs_dict['pro'][
            dfs_dict['pro'].index.get_level_values('smf_type') == '74.1'].reset_index().set_index(
            ['datetime', 'smf74ist', 'smf74iet', 'smf_type', 'csc', 'smf74sid', 'smf74int', 'smf74sam']).index)

        dfs_dict['dev'] = build_dev(df, dfs_dict['dctl'].reset_index().set_index(
            ['csc', 'smf74sid', 'datetime', 'smf74ist', 'smf74iet', 'smf74sub', 'smf74int', 'smf74sam']).index)

    if '74.2' in dfs_dict['pro'].index.get_level_values('smf_type'):  # Contains subtype 2 records
        if 'r742cntl' in df.columns:
            dfs_dict['xctl'] = col_to_frame(df[df.index.get_level_values('smf_type') == '74.2'], 'r742cntl',
                                            dfs_dict['pro'][
                                                dfs_dict['pro'].index.get_level_values('smf_type') == '74.2'].index
                                            )[Smf74Xctl.__table__.columns.keys()].set_index(
                [col.name for col in Smf74Xctl.__table__.primary_key.columns.values()])
        else:
            dfs_dict['xctl'] = pd.DataFrame(
                columns=Smf74Xctl.__table__.columns.keys()).set_index(
                [col.name for col in Smf74Xctl.__table__.primary_key.columns.values()])
        dfs_dict['sys'] = build_sys(df,
                                    dfs_dict['pro'][dfs_dict['pro'].index.get_level_values('smf_type') == '74.2'].index)

        dfs_dict['path'] = build_path(df, dfs_dict['pro'][
            dfs_dict['pro'].index.get_level_values('smf_type') == '74.2'].index)

        dfs_dict['mbr'] = build_mbr(df,
                                    dfs_dict['pro'][dfs_dict['pro'].index.get_level_values('smf_type') == '74.2'].index)

    if '74.3' in dfs_dict['pro'].index.get_level_values('smf_type'):  # Contains subtype 3 records
        dfs_dict['omvs'] = build_omvs(df, dfs_dict['pro'][
            dfs_dict['pro'].index.get_level_values('smf_type') == '74.3'].index)

    if '74.4' in dfs_dict['pro'].index.get_level_values('smf_type'):  # Contains subtype 4 records
        dfs_dict['cf'] = build_cf(df, dfs_dict['pro'][
            dfs_dict['pro'].index.get_level_values('smf_type') == '74.4'].reset_index().set_index(
            ['datetime', 'smf74ist', 'smf74iet', 'smf_type', 'smf74int', 'smf74xnm', 'smf74mfv', 'smf74sam',
             'smf74mvs', 'smf74cyc']).index, current_time)

        dfs_dict['lcf'] = build_lcf(df, dfs_dict['pro'][
            dfs_dict['pro'].index.get_level_values('smf_type') == '74.4'].reset_index().reset_index().set_index(
            ['csc', 'datetime', 'smf74ist', 'smf74iet', 'smf_type', 'smf74sid', 'smf74int', 'smf74sam', 'smf74xnm',
             'index']).index)

        dfs_dict['str'] = build_str(df, dfs_dict['lcf'].reset_index().set_index(
            ['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'r744fnam']).index, current_time)

        dfs_dict['sreq'] = build_sreq(df, dfs_dict['lcf'].reset_index().set_index(
            ['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'r744fnam', 'smf74sid', 'csc', 'index']).index)

        if dfs_dict['sreq'].shape[0] > 0 and dfs_dict['str'].shape[0] == 0:
            dfs_dict['str'] = dfs_dict['sreq'].reset_index().rename(columns={'r744snam': 'r744qstr'})[
                [col.name for col in
                 Smf74Str.__table__.primary_key.columns.values()]].drop_duplicates().set_index(
                [col.name for col in Smf74Str.__table__.primary_key.columns.values()])
            dfs_dict['str']['last_update_time'] = current_time

        if dfs_dict['lcf'].shape[0] > 0:
            agg_lcf_styp = {'r744sqrc': 'sum', 'r744sptc': 'sum', 'r744sctc': 'sum', 'r744sdto': 'sum',
                            'r744smrc': 'sum', 'r744sqtm': 'sum', 'r744spst': 'sum', 'r744scst': 'sum',
                            'r744sdtm': 'sum', 'r744smtm': 'sum', 'r744sqsq': 'sum', 'r744spss': 'sum',
                            'r744scss': 'sum', 'r744sdsq': 'sum', 'r744smsq': 'sum', 'r744ssrc': 'sum',
                            'r744sarc': 'sum'}
            agg_lcf_sreq = {'r744ssta': 'sum', 'r744strc': 'sum', 'r744stac': 'sum', 'r744sarc': 'sum',
                            'r744satm': 'sum', 'r744sasq': 'sum', 'r744ssrc': 'sum', 'r744sstm': 'sum',
                            'r744sssq': 'sum', 'r744sqrc': 'sum', 'r744sqtm': 'sum', 'r744sqsq': 'sum'}
            df_sreq_gp0 = dfs_dict['sreq'].groupby(
                ['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'r744fnam', 'smf74sid']
                ).agg(agg_lcf_sreq)
            df_sreq_gp1 = dfs_dict['sreq'][dfs_dict['sreq']['r744styp'].isin([1, 2])].groupby(
                ['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'r744fnam', 'smf74sid']).agg(agg_lcf_styp).rename(
                columns={'r744ssrc': 'total_list_r744ssrc', 'r744sarc': 'total_list_r744sarc'})
            df_sreq_gp1['total_list_delayed_reqs'] = df_sreq_gp1['r744sqrc'] + df_sreq_gp1['r744sptc'] + \
                                                     df_sreq_gp1['r744sctc'] + df_sreq_gp1['r744sdto'] + \
                                                     df_sreq_gp1['r744smrc']
            df_sreq_gp1['total_list_delay_time'] = df_sreq_gp1['r744sqtm'] + df_sreq_gp1['r744spst'] + \
                                                   df_sreq_gp1['r744scst'] + df_sreq_gp1['r744sdtm'] + \
                                                   df_sreq_gp1['r744smtm']
            df_sreq_gp1['total_list_delay_sq_time'] = df_sreq_gp1['r744sqsq'] + df_sreq_gp1['r744spss'] + \
                                                      df_sreq_gp1['r744scss'] + df_sreq_gp1['r744sdsq'] + \
                                                      df_sreq_gp1['r744smsq']
            df_sreq_gp2 = dfs_dict['sreq'][dfs_dict['sreq']['r744styp'] == 3].groupby(
                ['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'r744fnam', 'smf74sid']).agg(agg_lcf_styp).rename(
                columns={'r744ssrc': 'total_lock_r744ssrc', 'r744sarc': 'total_lock_r744sarc'})
            df_sreq_gp2['total_lock_delayed_reqs'] = df_sreq_gp2['r744sqrc'] + df_sreq_gp2['r744sptc'] + \
                                                     df_sreq_gp2['r744sctc'] + df_sreq_gp2['r744sdto'] + \
                                                     df_sreq_gp2['r744smrc']
            df_sreq_gp2['total_lock_delay_time'] = df_sreq_gp2['r744sqtm'] + df_sreq_gp2['r744spst'] + \
                                                   df_sreq_gp2['r744scst'] + df_sreq_gp2['r744sdtm'] + \
                                                   df_sreq_gp2['r744smtm']
            df_sreq_gp2['total_lock_delay_sq_time'] = df_sreq_gp2['r744sqsq'] + df_sreq_gp2['r744spss'] + \
                                                      df_sreq_gp2['r744scss'] + df_sreq_gp2['r744sdsq'] + \
                                                      df_sreq_gp2['r744smsq']
            df_sreq_gp3 = dfs_dict['sreq'][dfs_dict['sreq']['r744styp'] == 4].groupby(
                ['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'r744fnam', 'smf74sid']).agg(agg_lcf_styp).rename(
                columns={'r744ssrc': 'total_cache_r744ssrc', 'r744sarc': 'total_cache_r744sarc'})
            df_sreq_gp3['total_cache_delayed_reqs'] = df_sreq_gp3['r744sqrc'] + df_sreq_gp3['r744sptc'] + \
                                                      df_sreq_gp3['r744sctc'] + df_sreq_gp3['r744sdto'] + \
                                                      df_sreq_gp3['r744smrc']
            df_sreq_gp3['total_cache_delay_time'] = df_sreq_gp3['r744sqtm'] + df_sreq_gp3['r744spst'] + \
                                                    df_sreq_gp3['r744scst'] + df_sreq_gp3['r744sdtm'] + \
                                                    df_sreq_gp3['r744smtm']
            df_sreq_gp3['total_cache_delay_sq_time'] = df_sreq_gp3['r744sqsq'] + df_sreq_gp3['r744spss'] + \
                                                       df_sreq_gp3['r744scss'] + df_sreq_gp3['r744sdsq'] + \
                                                       df_sreq_gp3['r744smsq']

            dfs_dict['lcf'] = pd.concat([dfs_dict['lcf'],
                                         df_sreq_gp0,
                                         df_sreq_gp1[['total_list_delayed_reqs', 'total_list_delay_time',
                                                      'total_list_delay_sq_time', 'total_list_r744ssrc',
                                                      'total_list_r744sarc']],
                                         df_sreq_gp2[['total_lock_delayed_reqs', 'total_lock_delay_time',
                                                      'total_lock_delay_sq_time', 'total_lock_r744ssrc',
                                                      'total_lock_r744sarc']],
                                         df_sreq_gp3[['total_cache_delayed_reqs', 'total_cache_delay_time',
                                                      'total_cache_delay_sq_time', 'total_cache_r744ssrc',
                                                      'total_cache_r744sarc']]],
                                        axis=1)
        dfs_dict['cach'] = build_cach(df, dfs_dict['pro'][
            dfs_dict['pro'].index.get_level_values('smf_type') == '74.4'].reset_index().reset_index().set_index(
            ['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'smf74sid', 'index']).index, dfs_dict['sreq'])

        if dfs_dict['cach'].shape[0] > 0:
            agg_sreq_cach = {'r744crhc': 'max', 'r744crmd': 'max', 'r744crma': 'max', 'r744crmn': 'max',
                             'r744crmt': 'max', 'r744cwh0': 'max', 'r744cwh1': 'max', 'r744cwmn': 'max',
                             'r744cwmi': 'max', 'r744cwmt': 'max', 'r744cder': 'max', 'r744cdtr': 'max',
                             'r744cxdr': 'max', 'r744cxfw': 'max', 'r744cxni': 'max', 'r744cxci': 'max',
                             'r744ccoc': 'max', 'r744crsm': 'max', 'r744ctsf': 'max', 'r744cdec': 'max',
                             'r744cdac': 'max', 'r744ctcc': 'max', 'r744cdta': 'max', 'r744crlc': 'max',
                             'r744cprl': 'max', 'r744cxrl': 'max', 'r744cwuc': 'max'}
            df_cach_gp = dfs_dict['cach'].groupby(
                [col.name for col in Smf74Sreq.__table__.primary_key.columns.values()]).agg(agg_sreq_cach)
            dfs_dict['sreq'] = pd.concat([dfs_dict['sreq'], df_cach_gp], axis=1)

        df_chpa = build_chpa(df, dfs_dict['pro'][
            dfs_dict['pro'].index.get_level_values('smf_type') == '74.4'].reset_index().reset_index().set_index(
            ['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'smf74sid', 'index']).index)
        dfs_dict['subchpa'] = build_subchpa(dfs_dict['lcf'], df_chpa)

        dfs_dict['mscm'] = build_mscm(df, dfs_dict['pro'][
            dfs_dict['pro'].index.get_level_values('smf_type') == '74.4'].reset_index().reset_index().set_index(
            ['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'smf74sid', 'index']).index, dfs_dict['sreq'])

        dfs_dict['adup'] = build_adup(df, dfs_dict['pro'][
            dfs_dict['pro'].index.get_level_values('smf_type') == '74.4'].reset_index().reset_index().set_index(
            ['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'smf74sid', 'index']).index, dfs_dict['sreq'])

        dfs_dict['proc'] = build_proc(df, dfs_dict['lcf'].reset_index().set_index(
            ['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'r744fnam', 'r744fsys', 'smf74sid', 'csc']).index)

        dfs_dict['cfrf'] = build_cfrf(df, dfs_dict['lcf'].reset_index().set_index(
            ['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'r744fnam', 'smf74sid', 'csc', 'index']).index)

        if dfs_dict['cfrf'].shape[0] > 0:
            dfs_dict['dupchpa'] = build_dupchpa(dfs_dict['cfrf'], df_chpa)

    if '74.5' in dfs_dict['pro'].index.get_level_values('smf_type'):  # Contains subtype 5 records
        dfs_dict['cachsys'] = build_cachsys(df, dfs_dict['pro'][
            dfs_dict['pro'].index.get_level_values('smf_type') == '74.5'].index,
                                            current_time)
        dfs_dict['cdev'] = build_cdev(df, dfs_dict['cachsys'].reset_index().set_index(
            ['datetime', 'smf74ist', 'smf74iet', 'r745ssid', 'r745sft', 'r745cint', 'ccmt_seqn']).index)
        if dfs_dict['cdev'].shape[0] > 0:
            dfs_dict['raid'] = dfs_dict['cdev'][dfs_dict['cdev']['r7451flg'] == 1].copy()
            dfs_dict['xpool'] = dfs_dict['cdev'][dfs_dict['cdev']['r7451flg'] == 2].copy()
            # dfs_dict['cdev'] = dfs_dict['cdev'][[column for column in dfs_dict['cdev'].columns if column in
            #                Smf74Cdev.__table__.columns.keys()]].set_index(
            #     [col.name for col in Smf74Cdev.__table__.primary_key.columns.values()])
            dfs_dict['cdev'] = dfs_dict['cdev'][Smf74Cdev.__table__.columns.keys()].set_index(
                [col.name for col in Smf74Cdev.__table__.primary_key.columns.values()])

            agg_cdev = {'r745drcr': 'sum', 'r745dcrh': 'sum', 'r745dwrc': 'sum', 'r745dwch': 'sum',
                        'r745drsr': 'sum', 'r745drsh': 'sum', 'r745dwsr': 'sum',
                        'r745dwsh': 'sum', 'r745drnr': 'sum', 'r745dnrh': 'sum', 'r745dwnr': 'sum',
                        'r745dwnh': 'sum', 'r745dicl': 'sum', 'r745dbcr': 'sum',
                        'r745dtc': 'sum', 'r745dntd': 'sum', 'r745dctd': 'sum', 'r745dfwb': 'sum',
                        'r745dfwc': 'sum', 'r745dfws': 'sum', 'r745dcrm': 'sum',
                        'r745dcwp': 'sum', 'r745dkdw': 'sum', 'r745dkdh': 'sum', 'r745dfwr': 'sum',
                        'r745bytr': 'sum', 'r745bytw': 'sum', 'r745rtir': 'sum',
                        'r745rtiw': 'sum', 'total_io': 'sum', 'cache_io': 'sum', 'total_hits': 'sum',
                        'total_reads': 'sum', 'read_hits': 'sum', 'total_writes': 'sum',
                        'fast_writes': 'sum', 'write_hits': 'sum', 'dasd_io': 'sum', 'r7451unt': 'last',
                        'r7452pro': 'sum', 'r7452pwo': 'sum', 'r7452pbr': 'sum', 'r7452pbw': 'sum', 'r7452prt': 'sum',
                        'r7452pwt': 'sum',# for Extend pool
                        'r7451rrq': 'sum', 'r7451wrq': 'sum', 'r7451sr': 'sum', 'r7451sw': 'sum', 'r7451rrt': 'sum',
                        'r7451wrt': 'sum', # for Raid
                        'r7451rmr': 'sum', 'r7451xsf': 'sum', 'r7451xcw': 'sum', 'r7451tsp': 'sum', 'r7451nvs': 'sum',
                         'r7451ct1': 'sum', 'r7451ct2': 'sum', 'r7451ct3': 'sum',
                        'r7451ct4': 'sum', 'r7451ct5': 'sum', 'r7451ct6': 'sum',
                        'r7451zhl': 'sum', 'r7451zhh': 'sum', 'r7451gsf': 'sum', 'r7451gss': 'sum',
                        'r7451srr': 'sum', 'r7451srh': 'sum', 'r7451swr': 'sum',
                        'r7451swh': 'sum'}
            df_cdev_gp = dfs_dict['cdev'].reset_index().rename(columns={'r745dsid': 'r745ssid'}).groupby(
                [col.name for col in Smf74Cachsys.__table__.primary_key.columns.values()]).agg(agg_cdev)
            dfs_dict['cachsys'] = pd.concat([dfs_dict['cachsys'], df_cdev_gp], axis=1)

            if dfs_dict['raid'].shape[0] > 0:
                dfs_dict['raid']['r7451inc'] = dfs_dict['raid']['r7451inc'].apply(lambda x: int(str(x), 16))
                dfs_dict['raid']['r7451scs'] = dfs_dict['raid']['r7451scs'].str[2:]
                dfs_dict['raid']['r7451sio'] = dfs_dict['raid']['r7451inc'].apply(lambda x: is_bit_set(x, 8, 3))
                dfs_dict['raid']['r7451hpf'] = dfs_dict['raid']['r7451inc'].apply(lambda x: is_bit_set(x, 8, 4))
                dfs_dict['raid']['r7451xfl'] = dfs_dict['raid']['r7451inc'].apply(lambda x: is_bit_set(x, 8, 7))
                dfs_dict['raid']['r7451unt'] = dfs_dict['raid']['r7451inc'].apply(lambda x: extractKBits(x, 8, 5, 7))

                dfs_dict['rrank'] = dfs_dict['raid'][
                    ['datetime', 'smf74ist', 'smf74iet', 'r745ssid', 'r7451rid']].copy().drop_duplicates(
                    subset=[col.name for col in
                            Smf74Rrank.__table__.primary_key.columns.values()]).set_index(
                    [col.name for col in Smf74Rrank.__table__.primary_key.columns.values()])
                # formatting rrank
                agg_raid = {'r7451sio': agg_next, 'r7451hpf': agg_next, 'r7451xfl': agg_next, 'r7451scs': agg_next,
                            'r7451rsv': 'sum', 'r7451flg': agg_next, 'r7451aid': agg_next, 'r7451hdd': agg_next,
                            'r7451rty': agg_next, 'r7451hss': agg_next, 'r7451rrq': 'sum', 'r7451wrq': 'sum',
                            'r7451sr': 'sum', 'r7451sw': 'sum', 'r7451rrt': 'sum', 'r7451wrt': 'sum',
                            'r7451unt': agg_next, 'r7451rmr': 'sum', 'r7451xsf': 'sum', 'r7451xcw': 'sum',
                            'r7451tsp': 'sum', 'r7451nvs': 'sum', 'r7451ct1': 'sum', 'r7451ct2': 'sum',
                            'r7451ct3': 'sum', 'r7451ct4': 'sum', 'r7451ct5': 'sum', 'r7451ct6': 'sum',
                            'r7451zhl': 'sum', 'r7451zhh': 'sum', 'r7451gsf': 'sum', 'r7451gss': 'sum',
                            'r7451srr': 'sum', 'r7451srh': 'sum', 'r7451swr': 'sum', 'r7451swh': 'sum'}
                df_raid_gp = dfs_dict['raid'].groupby(
                    [col.name for col in Smf74Rrank.__table__.primary_key.columns.values()]).agg(agg_raid)
                dfs_dict['rrank'] = pd.concat([dfs_dict['rrank'], df_raid_gp], axis=1)
                dfs_dict['rrank']['last_update_time'] = current_time
                dfs_dict['raid'] = dfs_dict['raid'][Smf74Raid.__table__.columns.keys()].set_index(
                    [col.name for col in Smf74Raid.__table__.primary_key.columns.values()])

            if dfs_dict['xpool'].shape[0] > 0:
                dfs_dict['xpool']['r7451inc'] = dfs_dict['xpool']['r7451inc'].apply(lambda x: int(str(x), 16))
                dfs_dict['xpool']['r7452xfl'] = dfs_dict['xpool']['r7452xfl'].apply(lambda x: int(str(x), 16))
                dfs_dict['xpool']['r7451scs'] = dfs_dict['xpool']['r7451scs'].str[2:]
                dfs_dict['xpool']['r7451sio'] = dfs_dict['xpool']['r7451inc'].apply(lambda x: is_bit_set(x, 8, 3))
                dfs_dict['xpool']['r7451hpf'] = dfs_dict['xpool']['r7451inc'].apply(lambda x: is_bit_set(x, 8, 4))
                dfs_dict['xpool']['r7451xfl'] = dfs_dict['xpool']['r7451inc'].apply(lambda x: is_bit_set(x, 8, 7))
                dfs_dict['xpool']['r748xpid'] = dfs_dict['xpool']['r7451xid'].str[2:].map('{:0>4}'.format)
                dfs_dict['xpool']['r7452dxa'] = dfs_dict['xpool']['r7452xfl'].apply(lambda x: is_bit_set(x, 8, 0))
                dfs_dict['xpool']['r7452dsh'] = dfs_dict['xpool']['r7452xfl'].apply(lambda x: is_bit_set(x, 8, 1))
                dfs_dict['xpool']['r7452mis'] = dfs_dict['xpool']['r7452xfl'].apply(lambda x: is_bit_set(x, 8, 2))
                dfs_dict['xpool']['r7451unt'] = dfs_dict['xpool']['r7451inc'].apply(lambda x: extractKBits(x, 8, 5, 7))
                dfs_dict['xpool'] = dfs_dict['xpool'][Smf74Xpool.__table__.columns.keys()].set_index(
                    [col.name for col in Smf74Xpool.__table__.primary_key.columns.values()])

    if '74.6' in dfs_dict['pro'].index.get_level_values('smf_type'):  # Contains subtype 6 records
        dfs_dict['hfs'] = build_hfs(df,
                                    dfs_dict['pro'][dfs_dict['pro'].index.get_level_values('smf_type') == '74.6'].index)

        dfs_dict['gbuf'] = build_gbuf(df, dfs_dict['pro'][
            dfs_dict['pro'].index.get_level_values('smf_type') == '74.6'].reset_index().set_index(
            ['csc', 'datetime', 'smf74ist', 'smf74iet', 'smf74sid', 'smf74xnm']).index)

        dfs_dict['fsys'] = build_fsys(df, dfs_dict['pro'][
            dfs_dict['pro'].index.get_level_values('smf_type') == '74.6'].index)

    if '74.7' in dfs_dict['pro'].index.get_level_values('smf_type'):  # Contains subtype 7 records
        dfs_dict['fcd'] = build_fcd(df,
                                    dfs_dict['pro'][dfs_dict['pro'].index.get_level_values('smf_type') == '74.7'].index,
                                    current_time)

        dfs_dict['switch'] = build_switch(df, dfs_dict['pro'][
            dfs_dict['pro'].index.get_level_values('smf_type') == '74.7'].index,
                                          current_time)

        dfs_dict['port'], dfs_dict['connector'] = build_port(df, dfs_dict['switch'].reset_index().set_index(
            ['datetime', 'smf74ist', 'smf74iet', 'r747sdev', 'smf74sid']).index)

        if 'r747cdat' in df.columns:
            df_cdat = build_connector(df, dfs_dict['switch'].reset_index().set_index(
                ['datetime', 'smf74ist', 'smf74iet', 'r747sdev', 'smf74sid']).index)
            df_connector2 = dfs_dict['port'][dfs_dict['port']['r747pnpc'] > 0][
                ['r747pxpc', 'r747pnpc']].reset_index().rename(
                columns={'r747padr': 'r747cadr', 'r747pnum': 'r747cnum'}).set_index(
                ['datetime', 'smf74ist', 'smf74iet', 'r747sdev', 'r747cadr', 'r747cnum'])
            df_connector2 = df_connector2.reindex(df_connector2.index.repeat(df_connector2.r747pnpc))
            df_connector2['cdat_idx'] = df_connector2.groupby(
                ['datetime', 'smf74ist', 'smf74iet', 'r747sdev', 'r747cadr', 'r747cnum',
                 'r747pxpc']).cumcount() + df_connector2['r747pxpc']
            df_connector2 = df_connector2.reset_index().set_index(
                ['datetime', 'smf74ist', 'smf74iet', 'r747sdev', 'r747cadr', 'r747cnum', 'cdat_idx'])
            df_connector2 = df_connector2.join(df_cdat)
            dfs_dict['connector'] = pd.concat([dfs_dict['connector'], df_connector2.reset_index().set_index(
                [col.name for col in Smf74Connector.__table__.primary_key.columns.values()])])
            dfs_dict['connector'] = dfs_dict['connector'].reset_index()[
                Smf74Connector.__table__.columns.keys()].set_index(
                [col.name for col in Smf74Connector.__table__.primary_key.columns.values()])

    if '74.8' in dfs_dict['pro'].index.get_level_values('smf_type'):  # Contains subtype 8 records
        dfs_dict['cntl'] = build_cntl(df, dfs_dict['pro'][
            dfs_dict['pro'].index.get_level_values('smf_type') == '74.8'].index)

        dfs_dict['lss'] = build_lss(df, dfs_dict['cntl'].index)

        dfs_dict['arry'] = build_arry(df, dfs_dict['cntl'].index)

        dfs_dict['rank'] = build_rank(df, dfs_dict['cntl'].index, dfs_dict['arry'], current_time)

        dfs_dict['siol'] = build_siol(df, dfs_dict['cntl'].index)

    if 'r748extp' in df.columns:
        dfs_dict['extp'] = col_to_frame(df[df.index.get_level_values('smf_type') == '74.8'], 'r748extp',
                                        dfs_dict['cntl'].index)  # .rename(columns={'r748xpid': 'xpid'})
        dfs_dict['extp']['r748xpid'] = dfs_dict['extp']['r748xpid'].str[2:]
        dfs_dict['extp']['last_update_time'] = current_time
        dfs_dict['extp']['r748xptq'] = dfs_dict['extp']['r748xptq'].apply(lambda x: int(str(x), 16))
        dfs_dict['extp']['encrypted_extent_pool'] = dfs_dict['extp']['r748xptq'].apply(lambda x: is_bit_set(x, 8, 0))
        dfs_dict['extp']['compression_extent_pool'] = dfs_dict['extp']['r748xptq'].apply(lambda x: is_bit_set(x, 8, 1))
        dfs_dict['extp']['extent_sizes_valid'] = dfs_dict['extp']['r748xptq'].apply(lambda x: is_bit_set(x, 8, 7))
        if 'r748xeps' not in df.columns:
            dfs_dict['extp']['r748xeps'], dfs_dict['extp']['r748xtpc'], dfs_dict['extp']['r748xupc'], dfs_dict['extp'][
                'r748xtlc'], \
                dfs_dict['extp']['r748xulc'] = np.nan, np.nan, np.nan, np.nan, np.nan
        dfs_dict['extp'] = dfs_dict['extp'].set_index(
            [col.name for col in Smf74Extp.__table__.primary_key.columns.values()])

    if dfs_dict['rank'].shape[0] > 0:
        agg_rank = {'r748rcnt': 'sum', 'r748rbyr': 'sum', 'r748rbyw': 'sum', 'r748rrop': 'sum',
                    'r748rwop': 'sum', 'r748rkrt': 'sum', 'r748rkwt': 'sum', 'data_encrypted_rank': 'last',
                    'compression_rank': 'last', 'rank_adapter_id_valid': 'last', 'r748rai': 'last',
                    'r748aebc': agg_r748aebc, 'r748atyp': agg_r748atyp, 'r748aasp': 'min',
                    'r748aawd': 'sum', 'r748aacp': 'sum', 'rank_cap': 'sum', 'r748adc': agg_r748adc,
                    'r748ard': 'max', 'r748adt': 'max', 'r748are': 'max', 'r748acmp': 'max',
                    'r748rtq': 'last', 'r748aast': 'last'}
        df_rank_gp = dfs_dict['rank'].reset_index().rename(columns={'r748rpnm': 'r748xpid'}).groupby(
            [col.name for col in Smf74Extp.__table__.primary_key.columns.values()]).agg(agg_rank)
        dfs_dict['extp'] = pd.concat([dfs_dict['extp'], df_rank_gp], axis=1)
    if '74.9' in dfs_dict['pro'].index.get_level_values('smf_type'):  # Contains subtype 9 records
        def _srtd_r749rtsc(pcie_idx, response_time_for_sync_io_write, srtd_idx):
            try:
                idx = pcie_idx + (response_time_for_sync_io_write, srtd_idx)
                return dfs_dict['srtd'].loc[idx]['r749rtsc']
            except KeyError:
                return np.nan

        get_srtd_r749rtsc = np.vectorize(_srtd_r749rtsc)

        dfs_dict['pcie'] = build_pcie(df,
                                      dfs_dict['pro'][dfs_dict['pro'].index.get_level_values(
                                          'smf_type') == '74.9'].reset_index().reset_index().set_index(
                                          ['datetime', 'smf74ist', 'smf74iet', 'csc', 'smf74sid', 'smf_type',
                                           'index']).index,
                                      dfs_dict['pro'][dfs_dict['pro'].index.get_level_values(
                                          'smf_type') == '74.9'].reset_index().reset_index().set_index(
                                          ['datetime', 'smf74ist', 'smf74iet', 'index']).index, current_time)

        dfs_dict['srtd'] = build_srtd(df, dfs_dict['pro'][
            dfs_dict['pro'].index.get_level_values('smf_type') == '74.9'].reset_index().reset_index().set_index(
            ['datetime', 'smf74ist', 'smf74iet', 'index']).index, dfs_dict['pcie'])

        if dfs_dict['pcie'].shape[0] > 0:
            if dfs_dict['srtd'].shape[0] > 0:
                dfs_dict['pcie'] = dfs_dict['pcie'].copy() # reload the dataframe to avoid defragmentation
                dfs_dict['pcie']['pcipcr1'] = get_srtd_r749rtsc(dfs_dict['pcie'].index, 0, 0)
                dfs_dict['pcie']['pcipcr2'] = get_srtd_r749rtsc(dfs_dict['pcie'].index, 0, 1)
                dfs_dict['pcie']['pcipcr3'] = get_srtd_r749rtsc(dfs_dict['pcie'].index, 0, 2)
                dfs_dict['pcie']['pcipcr4'] = get_srtd_r749rtsc(dfs_dict['pcie'].index, 0, 3)
                dfs_dict['pcie']['pcipcr5'] = get_srtd_r749rtsc(dfs_dict['pcie'].index, 0, 4)
                dfs_dict['pcie']['pcipcr6'] = get_srtd_r749rtsc(dfs_dict['pcie'].index, 0, 5)
                dfs_dict['pcie']['pcipcr7'] = get_srtd_r749rtsc(dfs_dict['pcie'].index, 0, 6)
                dfs_dict['pcie']['pcipcr8'] = get_srtd_r749rtsc(dfs_dict['pcie'].index, 0, 7)
                dfs_dict['pcie']['pcipcr9'] = get_srtd_r749rtsc(dfs_dict['pcie'].index, 0, 8)
                dfs_dict['pcie']['pcipcr10'] = get_srtd_r749rtsc(dfs_dict['pcie'].index, 0, 9)
                dfs_dict['pcie']['pcipcw1'] = get_srtd_r749rtsc(dfs_dict['pcie'].index, 1, 0)
                dfs_dict['pcie']['pcipcw2'] = get_srtd_r749rtsc(dfs_dict['pcie'].index, 1, 1)
                dfs_dict['pcie']['pcipcw3'] = get_srtd_r749rtsc(dfs_dict['pcie'].index, 1, 2)
                dfs_dict['pcie']['pcipcw4'] = get_srtd_r749rtsc(dfs_dict['pcie'].index, 1, 3)
                dfs_dict['pcie']['pcipcw5'] = get_srtd_r749rtsc(dfs_dict['pcie'].index, 1, 4)
                dfs_dict['pcie']['pcipcw6'] = get_srtd_r749rtsc(dfs_dict['pcie'].index, 1, 5)
                dfs_dict['pcie']['pcipcw7'] = get_srtd_r749rtsc(dfs_dict['pcie'].index, 1, 6)
                dfs_dict['pcie']['pcipcw8'] = get_srtd_r749rtsc(dfs_dict['pcie'].index, 1, 7)
                dfs_dict['pcie']['pcipcw9'] = get_srtd_r749rtsc(dfs_dict['pcie'].index, 1, 8)
                dfs_dict['pcie']['pcipcw10'] = get_srtd_r749rtsc(dfs_dict['pcie'].index, 1, 9)
                dfs_dict['pcie']['pcitosir'] = (
                        dfs_dict['pcie']['pcipcr1'] + dfs_dict['pcie']['pcipcr2'] + dfs_dict['pcie']['pcipcr3'] +
                        dfs_dict['pcie'][
                            'pcipcr4'] + dfs_dict['pcie']['pcipcr5'] +
                        dfs_dict['pcie']['pcipcr6'] + dfs_dict['pcie']['pcipcr7'] + dfs_dict['pcie']['pcipcr8'] +
                        dfs_dict['pcie'][
                            'pcipcr9'] + dfs_dict['pcie']['pcipcr10'])
                dfs_dict['pcie']['pcitosiw'] = (
                        dfs_dict['pcie']['pcipcw1'] + dfs_dict['pcie']['pcipcw2'] + dfs_dict['pcie']['pcipcw3'] +
                        dfs_dict['pcie'][
                            'pcipcw4'] + dfs_dict['pcie']['pcipcw5'] +
                        dfs_dict['pcie']['pcipcw6'] + dfs_dict['pcie']['pcipcw7'] + dfs_dict['pcie']['pcipcw8'] +
                        dfs_dict['pcie'][
                            'pcipcw9'] + dfs_dict['pcie']['pcipcw10'])
                dfs_dict['pcie']['pcipcr1'] = dfs_dict['pcie']['pcipcr1'] * 100 / dfs_dict['pcie']['pcitosir']
                dfs_dict['pcie']['pcipcr2'] = dfs_dict['pcie']['pcipcr2'] * 100 / dfs_dict['pcie']['pcitosir']
                dfs_dict['pcie']['pcipcr3'] = dfs_dict['pcie']['pcipcr3'] * 100 / dfs_dict['pcie']['pcitosir']
                dfs_dict['pcie']['pcipcr4'] = dfs_dict['pcie']['pcipcr4'] * 100 / dfs_dict['pcie']['pcitosir']
                dfs_dict['pcie']['pcipcr5'] = dfs_dict['pcie']['pcipcr5'] * 100 / dfs_dict['pcie']['pcitosir']
                dfs_dict['pcie']['pcipcr6'] = dfs_dict['pcie']['pcipcr6'] * 100 / dfs_dict['pcie']['pcitosir']
                dfs_dict['pcie']['pcipcr7'] = dfs_dict['pcie']['pcipcr7'] * 100 / dfs_dict['pcie']['pcitosir']
                dfs_dict['pcie']['pcipcr8'] = dfs_dict['pcie']['pcipcr8'] * 100 / dfs_dict['pcie']['pcitosir']
                dfs_dict['pcie']['pcipcr9'] = dfs_dict['pcie']['pcipcr9'] * 100 / dfs_dict['pcie']['pcitosir']
                dfs_dict['pcie']['pcipcr10'] = dfs_dict['pcie']['pcipcr10'] * 100 / dfs_dict['pcie']['pcitosir']
                dfs_dict['pcie']['pcipcw1'] = dfs_dict['pcie']['pcipcw1'] * 100 / dfs_dict['pcie']['pcitosiw']
                dfs_dict['pcie']['pcipcw2'] = dfs_dict['pcie']['pcipcw2'] * 100 / dfs_dict['pcie']['pcitosiw']
                dfs_dict['pcie']['pcipcw3'] = dfs_dict['pcie']['pcipcw3'] * 100 / dfs_dict['pcie']['pcitosiw']
                dfs_dict['pcie']['pcipcw4'] = dfs_dict['pcie']['pcipcw4'] * 100 / dfs_dict['pcie']['pcitosiw']
                dfs_dict['pcie']['pcipcw5'] = dfs_dict['pcie']['pcipcw5'] * 100 / dfs_dict['pcie']['pcitosiw']
                dfs_dict['pcie']['pcipcw6'] = dfs_dict['pcie']['pcipcw6'] * 100 / dfs_dict['pcie']['pcitosiw']
                dfs_dict['pcie']['pcipcw7'] = dfs_dict['pcie']['pcipcw7'] * 100 / dfs_dict['pcie']['pcitosiw']
                dfs_dict['pcie']['pcipcw8'] = dfs_dict['pcie']['pcipcw8'] * 100 / dfs_dict['pcie']['pcitosiw']
                dfs_dict['pcie']['pcipcw9'] = dfs_dict['pcie']['pcipcw9'] * 100 / dfs_dict['pcie']['pcitosiw']
                dfs_dict['pcie']['pcipcw10'] = dfs_dict['pcie']['pcipcw10'] * 100 / dfs_dict['pcie']['pcitosiw']

    if '74.10' in dfs_dict['pro'].index.get_level_values('smf_type'):  # Contains subtype 10 records
        dfs_dict['scm'] = build_scm(df, dfs_dict['pro'][
            dfs_dict['pro'].index.get_level_values('smf_type') == '74.10'].index)

        dfs_dict['eadm'] = build_eadm(df, dfs_dict['pro'][
            dfs_dict['pro'].index.get_level_values('smf_type') == '74.10'].index)
    return dfs_dict


def print_omvs_activity(jsonfiles: tuple, lpar: str, start_time_str: str, end_time_str: str) -> str:
    """Print smf74 OMVS Activity Report based on JSON files.

    Args:
        jsonfiles: JSON file or files.
        lpar: Target LPAR to print.
        start_time_str: Start time string.
        end_time_str: End time string.

    Returns:
        OMVS Activity report.
    """
    start_time = pd.to_datetime(start_time_str)
    end_time = pd.to_datetime(end_time_str)
    sid = lpar
    current_time = dt.datetime.now()

    report = ''
    for jsonfile in jsonfiles:
        with (open(jsonfile) as f):
            try:
                df = pd.read_json(f)
            except ValueError:
                click.echo(
                    f"\nInvalid JSON file {jsonfile}. This file will be skipped.")
                continue

            if 'header' not in df.columns or not isinstance(df.iloc[0]['header'], dict) \
                    or df.iloc[0]['header'].get('recType') is None or df.iloc[0]['header']['recType'] != 74:
                click.echo(
                    f"\nInvalid JSON file {jsonfile}. This file will be skipped.")
                continue
            try:
                df_dict = format_74df(df, current_time)
            except Exception as e:
                click.echo(f"\nUnsupported JSON file {jsonfile} with error: {str(e)}. This file will be skipped.")
                continue

            if df_dict['pro'].empty:
                click.echo(
                    f"\nThis JSON file {jsonfile} is not for this smf type. This file will be skipped.")
                # Cannot continue processing
                continue

            if not df_dict['omvs'].empty:
                start_tbls = df_dict['omvs'].reset_index().query(
                    "smf74ist >= @start_time and smf74ist <= @end_time and smf74sid == @lpar"
                ).drop_duplicates()
            else:
                continue

            if start_tbls.empty:
                continue
            for omvs in start_tbls.to_dict('records'):
                pro = df_dict['pro'].reset_index().query(
                    "smf74iet == @omvs['smf74iet'] and smf74sid == @omvs['smf74sid'] and smf_type == '74.3'"
                ).drop_duplicates()
                page_detail = format_omvs_activity_report("RMF Interval", omvs, pro.to_dict('records')[0])
                if page_detail is not None:
                    if report != '':
                        report += '\n\n'
                    report += page_detail
    if report == '':
        report = 'No data found.'
    return report


def print_cache_subsystem_activity(jsonfiles: tuple, lpar: str, start_time_str: str, end_time_str: str,
                                   report_type: str, target_ssid: str = None) -> str:
    """Print smf74 Cache Subsystem Activity Report based on JSON files.

    Args:
        jsonfiles: JSON file or files.
        lpar: Target LPAR to print.
        start_time_str: Start time string.
        end_time_str: End time string.
        report_type: Type of report.
        target_ssid: Target cachsys name.

    Returns:
        Serialization Delay report.
    """

    def print_one_cache_subsystem_activity(cachsys: dict, report_type: str):
        pro = df_dict['pro'].query(
            "smf74iet == @cachsys['smf74iet'] and smf_type == '74.5'").reset_index().groupby(
            [col.name for col in
             Smf74Pro.__table__.primary_key.columns.values() if col.name != 'csc']).first().reset_index()
        if report_type == "Cache Subsystem Status and Overview":
            page = format_cachsys_status_and_overview("RMF Interval", cachsys, pro.to_dict('records')[0])

            # format "Cache Subsystem Device Overview and RAID Rank Activity"
            cdevs_raid = []
            rranks_raid = []
            cdevs_xpool = []
            cdevs = df_dict['cdev'].query(
                "smf74iet == @cachsys['smf74iet'] and r745dsid == @cachsys['r745ssid']").reset_index().groupby(
                [col.name for col in Smf74Cdev.__table__.primary_key.columns.values()]).first().reset_index()
            if not df_dict['rrank'].empty:
                rranks = df_dict['rrank'].query(
                    "smf74iet == @cachsys['smf74iet'] and r745ssid == @cachsys['r745ssid']").reset_index().groupby(
                    [col.name for col in
                     Smf74Rrank.__table__.primary_key.columns.values()]).first().reset_index().to_dict('records')
                for rrank in rranks:
                    rranks_raid.append(df_dict['raid'].query(
                        "smf74iet == @rrank['smf74iet'] and r7451rid == @rrank['r7451rid']"
                    ).reset_index().groupby([col.name for col in Smf74Raid.__table__.primary_key.columns.values()]
                                            ).first().reset_index().to_dict('records'))
            else:
                rranks = []
                rranks_raid = None
            for cdev in cdevs.to_dict('records'):
                cdev_raid = df_dict['raid'].query(
                    "smf74iet == @cdev['smf74iet'] and r745ssid == @cdev['r745dsid'] and r7451dvn == @cdev['r745devn']"
                ).reset_index().groupby([col.name for col in Smf74Raid.__table__.primary_key.columns.values()]
                                        ).first().reset_index()
                if not cdev_raid.empty:
                    cdevs_raid.append(cdev_raid.to_dict('records')[0])
                else:
                    cdevs_raid.append(None)
                cdev_xpool = df_dict['xpool'].query(
                    "smf74iet == @cdev['smf74iet'] and r745ssid == @cdev['r745dsid'] and r7451dvn == @cdev['r745devn']"
                ).reset_index().groupby([col.name for col in Smf74Xpool.__table__.primary_key.columns.values()]
                                        ).first().reset_index()
                if not cdev_xpool.empty:
                    cdevs_xpool.append(cdev_xpool.to_dict('records')[0])
                else:
                    cdevs_xpool.append(None)

            sub_page = format_cachsys_device_overview_and_raid_activity(
                "RMF Interval", cachsys, pro.to_dict('records')[0], cdevs.to_dict('records'), rranks,
                rranks_raid, cdevs_raid, cdevs_xpool)
            if sub_page is not None:
                page += '\n\n'
                page += sub_page

        else:
            cdevs = df_dict['cdev'].query(
                "smf74iet == @cachsys['smf74iet'] and r745dsid == @cachsys['r745ssid']"
            ).reset_index().groupby(
                [col.name for col in Smf74Cdev.__table__.primary_key.columns.values()]).first().reset_index()
            page = ''
            for cdev in cdevs.to_dict('records'):
                if not df_dict['raid'].empty:
                    raid = df_dict['raid'].query(
                        "smf74iet == @cdev['smf74iet'] and r745ssid == @cdev['r745dsid'] and r7451dvn == @cdev['r745devn']"
                    ).reset_index().groupby([col.name for col in Smf74Raid.__table__.primary_key.columns.values()]
                                            ).first().reset_index().to_dict('records')[0]
                else:
                    raid = None
                if not df_dict['xpool'].empty:
                    xpool = df_dict['xpool'].query(
                        "smf74iet == @cdev['smf74iet'] and r745ssid == @cdev['r745dsid'] and r7451dvn == @cdev['r745devn']"
                    ).reset_index().groupby([col.name for col in Smf74Xpool.__table__.primary_key.columns.values()]
                                            ).first().reset_index().to_dict('records')[0]
                else:
                    xpool = None

                sub_page = format_cache_device_status_and_activity(
                    "RMF Interval", cdev, cachsys, raid, xpool, pro.to_dict('records')[0])
                if sub_page is not None:
                    page += '\n\n'
                    page += sub_page
        return page

    start_time = pd.to_datetime(start_time_str)
    end_time = pd.to_datetime(end_time_str)
    sid = lpar
    current_time = dt.datetime.now()

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
                    or df.iloc[0]['header'].get('recType') is None or df.iloc[0]['header']['recType'] != 74:
                click.echo(
                    f"\nInvalid JSON file {jsonfile}. This file will be skipped.")
                continue
            try:
                df_dict = format_74df(df, current_time)
            except Exception as e:
                click.echo(f"\nUnsupported JSON file {jsonfile} with error: {str(e)}. This file will be skipped.")
                continue

            if df_dict['pro'].empty:
                click.echo(
                    f"\nThis JSON file {jsonfile} is not for this smf type. This file will be skipped.")
                # Cannot continue processing
                continue

            page_detail = ''
            cachsys_grp = []
            starting = 'cachsys'

            if not df_dict[starting].empty:
                if report_type != "Cache Subsystem Summary" and target_ssid is not None:
                    start_tbls = df_dict[starting].reset_index().query(
                        "smf74ist >= @start_time and smf74ist <= @end_time and r745ssid == @target_ssid"
                    ).drop_duplicates().copy().set_index(
                        [col.name for col in Smf74Cachsys.__table__.primary_key.columns.values()])
                    if start_tbls.empty:
                        continue
                else:
                    start_tbls = df_dict[starting].reset_index().query(
                        "smf74ist >= @start_time and smf74ist <= @end_time"
                    ).drop_duplicates().copy().set_index(
                        [col.name for col in Smf74Cachsys.__table__.primary_key.columns.values()])
                    if start_tbls.empty:
                        continue
                    cachsys_grp = start_tbls.reset_index().groupby('smf74iet')
            else:
                continue

            if start_tbls.empty:
                continue

            if report_type != "Cache Subsystem Summary" and target_ssid is not None:
                for cachsys in start_tbls.reset_index().to_dict('records'):
                    page_sub_detail = print_one_cache_subsystem_activity(cachsys, report_type)
                    if page_sub_detail != '':
                        if page_detail != '':
                            page_detail += '\n\n'
                        page_detail += page_sub_detail
            elif report_type != "Cache Subsystem Summary":  # target_ssid is None
                for report_iet, cachsys_df in cachsys_grp:
                    for cachsys in cachsys_df.to_dict('records'):
                        page_sub_detail = print_one_cache_subsystem_activity(cachsys, report_type)
                        if page_sub_detail != '':
                            if page_detail != '':
                                page_detail += '\n\n'
                            page_detail += page_sub_detail
            else:  # report_type == "Cache Subsystem Summary":
                for report_iet, cachsys_df in cachsys_grp:
                    pro = df_dict['pro'].query(
                        "smf74iet == @report_iet and smf_type == '74.5'").reset_index().groupby(
                        [col.name for col in
                         Smf74Pro.__table__.primary_key.columns.values() if col.name != 'csc']).first().reset_index()
                    page_sub_detail = format_cachsys_summary(
                        "RMF Interval", cachsys_df.to_dict('records'), pro.to_dict('records')[0])

                    # format top 20 device lists
                    query_tbl = 'cdev'
                    cdevs_total = df_dict[query_tbl].reset_index().query(
                        "smf74iet == @report_iet").reset_index().groupby(
                        [col.name for col in Smf74Cdev.__table__.primary_key.columns.values()]
                    ).first().reset_index().sort_values(by=['total_io'], ascending=False).head(20).to_dict('records')
                    cdevs_dasd = df_dict[query_tbl].reset_index().query(
                        "smf74iet == @report_iet").reset_index().groupby(
                        [col.name for col in Smf74Cdev.__table__.primary_key.columns.values()]
                    ).first().reset_index().sort_values(by=['dasd_io'], ascending=False).head(20).to_dict('records')
                    pro = df_dict['pro'].reset_index().query(
                        "smf74iet == @report_iet and smf_type == '74.5'").reset_index().groupby(
                        [col.name for col in
                         Smf74Pro.__table__.primary_key.columns.values() if col.name != 'csc']).first().reset_index()
                    top20_detail = format_top20_report(
                        "RMF Interval", cachsys_df.to_dict('records')[0], cdevs_total, cdevs_dasd,
                        pro.to_dict('records')[0])

                    if top20_detail is not None:
                        page_sub_detail += '\n\n'
                        page_sub_detail += top20_detail
                    if page_sub_detail is not None:
                        if page_detail != '':
                            page_detail += '\n\n'
                        page_detail += page_sub_detail

            report += page_detail
    if report == '':
        report = 'No data found.'
    return report


def print_device_activity(jsonfiles: tuple, lpar: str, start_time_str: str, end_time_str: str,
                          target_device_type: str) -> str:
    """Print smf74 Coupling Facility Activity Report based on JSON files.

    Args:
        jsonfiles: JSON file or files.
        lpar: Target LPAR to print.
        start_time_str: Start time string.
        end_time_str: End time string.
        target_device_type: Target device type.

    Returns:
        Coupling Facility Activity report.
    """
    start_time = pd.to_datetime(start_time_str)
    end_time = pd.to_datetime(end_time_str)
    sid = lpar
    current_time = dt.datetime.now()

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
                    or df.iloc[0]['header'].get('recType') is None or df.iloc[0]['header']['recType'] != 74:
                click.echo(
                    f"\nInvalid JSON file {jsonfile}. This file will be skipped.")
                continue
            try:
                df_dict = format_74df(df, current_time)
            except Exception as e:
                click.echo(f"\nUnsupported JSON file {jsonfile} with error: {str(e)}. This file will be skipped.")
                continue

            if df_dict['pro'].empty:
                click.echo(
                    f"\nThis JSON file {jsonfile} is not for this smf type. This file will be skipped.")
                # Cannot continue processing
                continue
            device_dict = {'DASD': '0020', 'Tape': '0080', 'Communication Device': '0040', 'Graphic Device': '0010'}
            starting = 'dctl'
            device_type = device_dict[target_device_type]

            if not df_dict[starting].empty:
                start_tbls = df_dict[starting].loc[
                    ~df_dict[starting].index.duplicated(keep='first'), :].reset_index().query(
                    "smf74ist >= @start_time and smf74ist <= @end_time and smf74sid == @lpar and smf74sub == @device_type"
                ).copy()
            else:
                continue

            if start_tbls.empty:
                continue
            for dctl in start_tbls.to_dict('records'):
                devs = df_dict['dev'].reset_index().query(
                    "smf74iet == @dctl['smf74iet'] and smf74sid == @dctl['smf74sid'] and smf74sub == @dctl['smf74sub']"
                ).copy()
                pro = df_dict['pro'].reset_index().query(
                    "smf74iet == @dctl['smf74iet'] and smf74sid == @dctl['smf74sid'] and smf_type == '74.1'"
                ).copy()
                device_gp_list = devs.groupby('smf74lcu')
                device_list = []
                for smf74lcu, device_df in device_gp_list:
                    device_list.append(device_df.to_dict('records'))
                page_detail = format_device_activity_report("RMF Interval", dctl, devs.to_dict('records'),
                                                            pro.to_dict('records')[0], device_list)
                if page_detail is not None:
                    if report != '':
                        report += '\n\n'
                    report += page_detail
    if report == '':
        report = 'No data found.'
    return report


def print_cf_activity(jsonfiles: tuple, lpar: str, start_time_str: str, end_time_str: str,
                      target_cf: Union[str, None] = None, report_type: Union[str, None] = None,
                      include_cache: bool = True, include_lock: bool = True, include_serialized_list: bool = True,
                      include_unserialized_list: bool = True) -> str:
    """Print smf74 Coupling Facility Activity Report based on JSON files.

    Args:
        jsonfiles: JSON file or files.
        lpar: Target LPAR to print.
        start_time_str: Start time string.
        end_time_str: End time string.
        report_type: Type of report.
        target_cf: Target CF to print.
        include_cache: Include cache if true.
        include_lock: Include lock if true.
        include_serialized_list: Include serialized list if true.
        include_unserialized_list: Include unserialized list if true.

    Returns:
        Coupling Facility Activity report.
    """
    agg_str = {'r744styp': agg_next, 'r744scei': agg_next, 'r744sadi': agg_next, 'r744scad': agg_next,
               'r744sdas': agg_next, 'r744spri': agg_next, 'r744ssec': agg_next, 'r744senc': agg_next,
               'r744slec': agg_next, 'r744slel': 'max', 'r744slem': 'last', 'r744sltl': agg_next,
               'r744sltm': agg_next, 'r744ssta': 'sum', 'r744strc': 'sum', 'r744stac': 'sum', 'r744sarc': 'sum',
               'r744satm': 'sum', 'r744sasq': 'sum', 'r744ssrc': 'sum', 'r744sstm': 'sum', 'r744sssq': 'sum',
               'r744sqrc': 'sum', 'r744sqtm': 'sum', 'r744sqsq': 'sum', 'r744sdrc': 'sum', 'r744sdtm': 'sum',
               'r744sdsq': 'sum', 'r744sdmp': 'sum', 'r744shto': 'sum', 'r744shmn': 'min', 'r744shmx': 'max',
               'r744slto': 'sum', 'r744slmn': 'min', 'r744slmx': 'max', 'r744sdto': 'sum', 'r744sdmn': 'min',
               'r744sdmx': 'max', 'r744scn': 'sum', 'r744sfcn': 'sum', 'r744ssiz': agg_next, 'r744smas': 'max',
               'r744smis': 'min', 'r744sdec': 'mean', 'r744sdel': 'mean', 'r744snlh': 'sum', 'r744smae': 'max',
               'r744scue': agg_next, 'r744cdsi': agg_next, 'r744cdne': 'sum', 'r744spln': 'sum', 'r744spes': 'sum',
               'r744sptc': 'sum', 'r744spst': 'sum', 'r744spss': 'sum', 'r744srtc': 'sum', 'r744srst': 'sum',
               'r744srss': 'sum', 'r744sctc': 'sum', 'r744scst': 'sum', 'r744scss': 'sum', 'r744slsv': agg_next,
               'r744setm': 'sum', 'r744sisc': agg_next, 'r744snsc': 'sum', 'r744ssac': 'sum', 'r744sosa': 'sum',
               'r744siad': agg_next, 'r744sadn': 'sum', 'r744sixc': 'sum', 'r744sxsc': 'sum', 'r744sxst': 'sum',
               'r744sxsq': 'sum', 'r744sado': 'sum', 'r744sadr': 'sum', 'r744sqch': agg_next, 'r744sxap': agg_next,
               'r744sxas': agg_next, 'r744sxcm': agg_next, 'r744sxmo': agg_next, 'r744swdr': 'sum', 'r744swac': 'sum',
               'r744srdr': 'sum', 'r744srac': 'sum', 'r744swec': 'sum', 'r744srec': 'sum', 'r744swed': 'sum',
               'r744swes': 'sum', 'r744sred': 'sum', 'r744sres': 'sum', 'r744smrc': 'sum', 'r744smtm': 'sum',
               'r744smsq': 'sum', 'r744smto': 'sum', 'r744smht': 'sum', 'r744smmn': 'min', 'r744smmx': 'max',
               'r744smhn': 'min', 'r744smhx': 'max', 'r744crhc': 'max', 'r744crmd': 'max', 'r744crma': 'max',
               'r744crmn': 'max', 'r744crmt': 'max', 'r744cwh0': 'max', 'r744cwh1': 'max', 'r744cwmn': 'max',
               'r744cwmi': 'max', 'r744cwmt': 'max', 'r744cder': 'max', 'r744cdtr': 'max', 'r744cxdr': 'max',
               'r744cxfw': 'max', 'r744cxni': 'max', 'r744cxci': 'max', 'r744ccoc': 'max', 'r744crsm': 'max',
               'r744ctsf': 'max', 'r744cdec': 'last', 'r744cdac': 'last', 'r744ctcc': 'max', 'r744cdta': 'max',
               'r744crlc': 'max', 'r744cprl': 'max', 'r744cxrl': 'max', 'r744cwuc': 'max'}
    agg_mscm = {'r744msma': 'max', 'r744malg': agg_next, 'r744mfau': agg_next, 'r744miua': 'max', 'r744mius': 'max',
                'r744mema': 'max', 'r744meml': 'max', 'r744meme': 'max', 'r744menl': 'max', 'r744mene': 'max',
                'r744mslt': agg_next, 'r744msut': agg_next, 'r744mslr': agg_next, 'r744msur': agg_next,
                'r744mswc': 'sum', 'r744mrfc': 'sum', 'r744mrpc': 'sum', 'r744mrst': 'sum', 'r744mrsq': 'sum',
                'r744mwst': 'sum', 'r744mwsq': 'sum', 'r744mrbt': 'sum', 'r744mwbt': 'sum', 'r744maec': 'sum',
                'r744msrl': 'sum', 'r744msrr': 'sum', 'r744msrm': 'sum', 'r744mmbl': 'max', 'r744mmbe': 'max',
                'r744mnel': 'min', 'r744mnec': 'min', 'r744msrk': 'sum'}
    agg_adup = {'r744afo': agg_next, 'r744aheo': 'max', 'r744alaoh': 'max', 'r744alaosh': 'max', 'r744alcoh': 'max',
                'r744alcoph': 'max', 'r744alao': 'sum', 'r744alaos': 'sum', 'r744alco': 'sum', 'r744alcop': 'sum',
                'r744atpoct': 'sum', 'r744atpoc': 'sum', 'r744arcpot': 'sum', 'r744arcpo': 'sum', 'r744acqsc': 'sum',
                'r744apdt': 'sum', 'r744apdq': 'sum', 'r744amdt': 'sum', 'r744amdq': 'sum', 'r744aqdt': 'sum',
                'r744aqdq': 'sum', 'r744aqst': 'sum', 'r744aqsq': 'sum', 'r744acdt': 'sum', 'r744acdq': 'sum',
                'r744ardt': 'sum', 'r744ardq': 'sum', 'r744aott': 'sum', 'r744aotq': 'sum', 'r744astt': 'sum',
                'r744astq': 'sum'}

    start_time = pd.to_datetime(start_time_str)
    end_time = pd.to_datetime(end_time_str)
    sid = lpar
    current_time = dt.datetime.now()

    report = ''
    for jsonfile in jsonfiles:
        page_detail = ''
        with open(jsonfile) as f:
            try:
                df = pd.read_json(f)
            except ValueError:
                click.echo(
                    f"\nInvalid JSON file {jsonfile}. This file will be skipped.")
                continue

            if 'header' not in df.columns or not isinstance(df.iloc[0]['header'], dict) \
                    or df.iloc[0]['header'].get('recType') is None or df.iloc[0]['header']['recType'] != 74:
                click.echo(
                    f"\nInvalid JSON file {jsonfile}. This file will be skipped.")
                continue
            try:
                df_dict = format_74df(df, current_time)
            except Exception as e:
                click.echo(f"\nUnsupported JSON file {jsonfile} with error: {str(e)}. This file will be skipped.")
                continue

            if df_dict['pro'].empty:
                click.echo(
                    f"\nThis JSON file {jsonfile} is not for this smf type. This file will be skipped.")
                # Cannot continue processing
                continue

            if df_dict['str'].shape[0] > 0:
                str_df1 = df_dict['sreq'].copy().reset_index().rename(columns={'r744snam': 'r744qstr'}).groupby(
                    [col.name for col in Smf74Str.__table__.primary_key.columns.values()]).agg(agg_str)
                str_df2 = df_dict['mscm'].copy().reset_index().rename(columns={'r744snam': 'r744qstr'}).groupby(
                    [col.name for col in Smf74Str.__table__.primary_key.columns.values()]).agg(agg_mscm)
                str_df3 = df_dict['adup'].copy().reset_index().rename(columns={'r744snam': 'r744qstr'}).groupby(
                    [col.name for col in Smf74Str.__table__.primary_key.columns.values()]).agg(agg_adup)
                df_dict['str'] = pd.concat([df_dict['str'], str_df1, str_df2, str_df3], axis=1)

            if df_dict['cf'].shape[0] > 0:
                agg_cf_str = {'r744ssiz': 'sum'}
                agg_cf_mscm = {'r744mfau': 'sum', 'r744msma': 'sum'}
                agg_cf_proc_sum = {'r744pbsy': 'sum', 'r744pwai': 'sum', 'r744pwgt': 'sum'}
                agg_cf_proc_mean = {'r744pbsy': 'mean', 'r744pwai': 'mean', 'r744pwgt': 'mean'}
                agg_cf_lcf = {'r744fscg': 'max', 'r744fscu': 'max', 'r744fscl': 'max', 'r744fscc': 'sum',
                              'r744ftim': 'sum', 'r744fsqu': 'sum', 'r744fctm': 'sum', 'r744fcsq': 'sum',
                              'r744fpbc': 'sum', 'r744ftor': 'sum', 'r744fail': 'sum'}
                cf_df1 = df_dict['str'].copy().reset_index().groupby(
                    [col.name for col in Smf74Cf.__table__.primary_key.columns.values()]).agg(agg_cf_str).rename(
                    columns={'r744ssiz': 'total_str_alloc'})
                cf_df2 = df_dict['mscm'].copy().reset_index().groupby(
                    [col.name for col in Smf74Cf.__table__.primary_key.columns.values()]).agg(agg_cf_mscm).rename(
                    columns={'r744mfau': 'total_augmented_alloc', 'r744msma': 'total_max_scm'})
                cf_df3a = df_dict['proc'].copy().reset_index().groupby(
                    ['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'r744fnam', 'r744pnum']).agg(agg_cf_proc_mean)
                cf_df3 = cf_df3a.copy().reset_index().groupby(
                    [col.name for col in Smf74Cf.__table__.primary_key.columns.values()]).agg(
                    agg_cf_proc_sum).rename(
                    columns={'r744pbsy': 'total_processor_busy', 'r744pwai': 'total_processor_wait'})

                cf_df4 = df_dict['lcf'].copy().reset_index().groupby(
                    [col.name for col in Smf74Cf.__table__.primary_key.columns.values()]).agg(agg_cf_lcf)

                df_dict['cf'] = pd.concat([df_dict['cf'], cf_df1, cf_df2, cf_df3, cf_df4], axis=1)
                df_dict['cf']['avg_processor_weight'] = np.where(df_dict['cf']['r744fpsn'] > 0,
                                                                 df_dict['cf']['r744pwgt'] / df_dict['cf']['r744fpsn'],
                                                                 0)
            starting = 'cf'
            if df_dict[starting].empty:
                continue
            if target_cf is not None:
                start_tbls = df_dict[starting].loc[~df_dict[starting].index.duplicated(keep='first'), :].query(
                    "smf74ist >= @start_time and smf74ist <= @end_time and r744fnam == @target_cf").copy()
            else:
                start_tbls = df_dict[starting].loc[~df_dict[starting].index.duplicated(keep='first'), :].query(
                    "smf74ist >= @start_time and smf74ist <= @end_time").copy()
            if start_tbls.empty:
                continue
            start_tbls_gp = start_tbls.reset_index().groupby('smf74iet')
            str_type_list = []
            if include_cache:
                str_type_list.append(4)
            if include_lock:
                str_type_list.append(3)
            if include_serialized_list:
                str_type_list.append(2)
            if include_unserialized_list:
                str_type_list.append(1)
            for report_iet, start_tbls_df in start_tbls_gp:
                for cf in start_tbls_df.to_dict('records'):
                    lcfs = df_dict['lcf'].copy().reset_index().query(
                        "smf74iet == @cf['smf74iet'] and r744fnam == @cf['r744fnam']"
                    )
                    strs = df_dict['str'].copy().reset_index().query(
                        "smf74iet == @cf['smf74iet'] and r744fnam == @cf['r744fnam']"
                    ).drop_duplicates()
                    cfrfs = df_dict['cfrf'].copy().reset_index().query(
                        "smf74iet == @cf['smf74iet'] and r744fnam == @cf['r744fnam']"
                    ).drop_duplicates()
                    procs = df_dict['proc'].copy().reset_index().query(
                        "smf74iet == @cf['smf74iet'] and r744fnam == @cf['r744fnam']"
                    ).drop_duplicates()
                    chpas = df_dict['subchpa'].copy().reset_index().query(
                        "smf74iet == @cf['smf74iet'] and r744fnam == @cf['r744fnam']"
                    ).drop_duplicates()
                    str_styp_group = strs.groupby('r744styp')
                    mscms_list = []
                    adups_list = []
                    sreqs_list = []
                    str_group_list = []
                    for styp, strs_df in str_styp_group:
                        mscms_list_styp = []
                        adups_list_styp = []
                        sreqs_list_styp = []
                        str_list = strs_df.to_dict('records')
                        for structure in str_list:
                            mscms_str_df = df_dict['mscm'].copy().reset_index().query(
                                "smf74iet == @structure['smf74iet'] and r744fnam == @structure['r744fnam'] and r744snam == @structure['r744qstr']"
                            ).drop_duplicates()
                            if not mscms_str_df.empty:
                                mscms_list_styp.append(mscms_str_df.to_dict('records'))
                            else:
                                mscms_list_styp.append([])
                            adups_str_df = df_dict['adup'].copy().reset_index().query(
                                "smf74iet == @structure['smf74iet'] and r744fnam == @structure['r744fnam'] and r744snam == @structure['r744qstr']"
                            ).drop_duplicates()
                            if not adups_str_df.empty:
                                adups_list_styp.append(adups_str_df.to_dict('records'))
                            else:
                                adups_list_styp.append([])
                            sreqs_df = df_dict['sreq'].copy().reset_index().query(
                                "smf74iet == @structure['smf74iet'] and r744fnam == @structure['r744fnam'] and r744snam == @structure['r744qstr']"
                            ).drop_duplicates()
                            sreqs_list_styp.append(sreqs_df.to_dict('records'))
                        mscms_list.append(mscms_list_styp)
                        adups_list.append(adups_list_styp)
                        str_group_list.append(str_list)
                        sreqs_list.append(sreqs_list_styp)
                    page_detail = ''
                    if report_type == 'CF Usage Summary' or report_type is None:
                        page_detail += format_cf_activity_report("RMF Interval", cf,
                                                                 strs.reset_index().to_dict('records'),
                                                                 'CF Usage Summary',
                                                                 lcfs.copy().reset_index().to_dict('records'),
                                                                 procs.copy().reset_index().to_dict('records'),
                                                                 cfrfs.copy().reset_index().to_dict('records'),
                                                                 str_group_list, chpas.copy().reset_index().to_dict('records'),
                                                                 sreqs=None, peer_cfs=None, dupchpas=None,
                                                                 mscms_list=mscms_list, adups_list=adups_list,
                                                                 str_type_list=str_type_list)
                    if report_type == "CF Structure Activity" or report_type is None:
                        if report_type is None:
                            page_detail += '\n\n'
                        page_detail += format_cf_activity_report("RMF Interval", cf,
                                                                 strs.copy().reset_index().to_dict('records'),
                                                                 'CF Structure Activity',
                                                                 lcfs.copy().reset_index().to_dict('records'),
                                                                 procs.copy().reset_index().to_dict('records'),
                                                                 cfrfs.copy().reset_index().to_dict('records'),
                                                                 str_group_list, chpas.copy().reset_index().to_dict('records'),
                                                                 sreqs_list, peer_cfs=None, dupchpas=None,
                                                                 mscms_list=mscms_list, adups_list=adups_list,
                                                                 str_type_list=str_type_list)
                    if report_type == "Subchannel Activity" or report_type is None:
                        page_detail += format_cf_activity_report("RMF Interval", cf,
                                                                 strs.copy().reset_index().to_dict('records'),
                                                                 'Subchannel Activity',
                                                                 lcfs.copy().reset_index().to_dict('records'),
                                                                 procs.copy().reset_index().to_dict('records'),
                                                                 cfrfs.copy().reset_index().to_dict('records'),
                                                                 str_group_list, chpas.copy().reset_index().to_dict('records'),
                                                                 sreqs_list, peer_cfs=None, dupchpas=None,
                                                                 mscms_list=mscms_list, adups_list=adups_list,
                                                                 str_type_list=str_type_list)
                    if report_type == "CF to CF Activity" or report_type is None:
                        if report_type is None:
                            page_detail += '\n\n'
                        peer_cfs_group = cfrfs.copy().reset_index().groupby('r744rnam')
                        peer_group_list = []
                        dupchpas_list = []
                        for r744rnam, cfrf_df in peer_cfs_group:
                            cfrf_records_list = cfrf_df.to_dict('records')
                            dupchpa_records_list = []
                            for cfrf in cfrf_records_list:
                                dupchpas_df = df_dict['dupchpa'].copy().reset_index().query(
                                    "smf74iet == @cfrf['smf74iet'] and r744fnam == @cfrf['r744fnam'] and r744rnam == @cfrf['r744rnam']"
                                ).drop_duplicates()
                                dupchpa_records_list.append(dupchpas_df.to_dict('records'))

                            peer_group_list.append(cfrf_records_list)
                            dupchpas_list.append(dupchpa_records_list)
                        page_detail += format_cf_activity_report("RMF Interval", cf,
                                                                 strs.copy().reset_index().to_dict('records'),
                                                                 'CF to CF Activity',
                                                                 lcfs.copy().reset_index().to_dict('records'),
                                                                 procs.copy().reset_index().to_dict('records'),
                                                                 cfrfs.copy().reset_index().to_dict('records'),
                                                                 str_group_list, chpas.copy().reset_index().to_dict('records'),
                                                                 sreqs=None, peer_cfs=peer_group_list,
                                                                 dupchpas=dupchpas_list,
                                                                 mscms_list=mscms_list, adups_list=adups_list,
                                                                 str_type_list=str_type_list)

                    if page_detail is not None:
                        if report != '':
                            report += '\n\n'
                        report += page_detail
    if report == '':
        report = 'No data found.'
    return report


def print_hfs_statistics(jsonfiles: tuple, lpar: str, start_time_str: str, end_time_str: str,
                         report_type: Union[str, None] = None) -> str:
    """Print smf74 HFS Statistics Report based on JSON files.

    Args:
        jsonfiles: JSON file or files.
        lpar: Target LPAR to print.
        start_time_str: Start time string.
        end_time_str: End time string.
        report_type: Type of report.

    Returns:
        HFS Statistics report.
    """
    start_time = pd.to_datetime(start_time_str)
    end_time = pd.to_datetime(end_time_str)
    sid = lpar
    current_time = dt.datetime.now()

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
                    or df.iloc[0]['header'].get('recType') is None or df.iloc[0]['header']['recType'] != 74:
                click.echo(
                    f"\nInvalid JSON file {jsonfile}. This file will be skipped.")
                continue
            try:
                df_dict = format_74df(df, current_time)
            except Exception as e:
                click.echo(f"\nUnsupported JSON file {jsonfile} with error: {str(e)}. This file will be skipped.")
                continue

            if df_dict['pro'].empty:
                click.echo(
                    f"\nThis JSON file {jsonfile} is not for this smf type. This file will be skipped.")
                # Cannot continue processing
                continue

            if not df_dict['hfs'].empty:
                start_tbls = df_dict['hfs'].query(
                    "smf74ist >= @start_time and smf74ist <= @end_time and smf74sid == @lpar")
            else:
                continue

            if start_tbls.empty:
                continue

            for hfs in start_tbls.reset_index().to_dict('records'):
                gbufs = df_dict['gbuf'].reset_index().query(
                    "smf74iet == @hfs['smf74iet'] and smf74sid == @hfs['smf74sid']"
                ).drop_duplicates()
                pro = df_dict['pro'].reset_index().query(
                    "smf74iet == @hfs['smf74iet'] and smf74sid == @hfs['smf74sid'] and smf_type == '74.6'"
                ).drop_duplicates()
                if not df_dict['fsys'].empty:
                    fsyss = df_dict['fsys'].reset_index().query(
                        "smf74iet == @hfs['smf74iet'] and smf74sid == @hfs['smf74sid']")
                else:
                    fsyss = pd.DataFrame()
                if report_type == 'HFS Global Statistics' or report_type is None:
                    stat_page = format_hfs_global_statistics("RMF Interval", hfs, pro.to_dict('records')[0],
                                                             gbufs.to_dict('records'))
                    if stat_page is not None:
                        if page_detail != '':
                            page_detail += '\n\n'
                        page_detail += stat_page
                if not fsyss.empty and (report_type == 'HFS File System Statistics' or report_type is None):
                    stat_page = format_hfs_file_system_statistics("RMF Interval", hfs, pro.to_dict('records')[0],
                                                                  fsyss.to_dict('records'))
                    if stat_page is not None:
                        if page_detail != '':
                            page_detail += '\n\n'
                        page_detail += stat_page
            if page_detail != '':
                report += page_detail
    if report == '':
        report = 'No data found.'
    return report


def print_fcd_activity(jsonfiles: tuple, start_time_str: str, end_time_str: str,
                       target_switch: Union[str, None] = None) -> str:
    """Print smf74 FCD Activity Report based on JSON files.

    Args:
        jsonfiles: JSON file or files.
        start_time_str: Start time string.
        end_time_str: End time string.
        target_switch: Target switch.

    Returns:
        FCD Activity report.
    """
    start_time = pd.to_datetime(start_time_str)
    end_time = pd.to_datetime(end_time_str)
    current_time = dt.datetime.now()

    report = ''
    for jsonfile in jsonfiles:
        page_detail = ''
        with open(jsonfile) as f:
            try:
                df = pd.read_json(f)
            except ValueError:
                click.echo(
                    f"\nInvalid JSON file {jsonfile}. This file will be skipped.")
                continue

            if 'header' not in df.columns or not isinstance(df.iloc[0]['header'], dict) \
                    or df.iloc[0]['header'].get('recType') is None or df.iloc[0]['header']['recType'] != 74:
                click.echo(
                    f"\nInvalid JSON file {jsonfile}. This file will be skipped.")
                continue
            try:
                df_dict = format_74df(df, current_time)
            except Exception as e:
                click.echo(f"\nUnsupported JSON file {jsonfile} with error: {str(e)}. This file will be skipped.")
                continue

            if df_dict['pro'].empty:
                click.echo(
                    f"\nThis JSON file {jsonfile} is not for this smf type. This file will be skipped.")
                # Cannot continue processing
                continue

            if df_dict['switch'].empty:
                click.echo(
                    f"\nThis JSON file {jsonfile} is not for this smf type. This file will be skipped.")
                # Cannot continue processing
                continue

            if target_switch is not None:
                start_tbls = df_dict['switch'].loc[
                    ~df_dict['switch'].index.duplicated(keep='first'), :].reset_index().query(
                    "smf74ist >= @start_time and smf74ist <= @end_time and r747sdev == @target_switch")
            else:
                start_tbls = df_dict['switch'].loc[
                    ~df_dict['switch'].index.duplicated(keep='first'), :].reset_index().query(
                    "smf74ist >= @start_time and smf74ist <= @end_time")

            if start_tbls.empty:
                continue

            start_tbls_gp = start_tbls.groupby('smf74iet')
            for report_iet, switch_df in start_tbls_gp:
                for switch in switch_df.to_dict('records'):
                    ports = df_dict['port'].reset_index().query(
                        "smf74iet == @switch['smf74iet'] and r747sdev == @switch['r747sdev']"
                    ).drop_duplicates()
                    fcd = df_dict['fcd'].reset_index().query(
                        "smf74iet == @switch['smf74iet']"
                    ).drop_duplicates()
                    pros = df_dict['pro'].reset_index().query(
                        "smf74iet == @switch['smf74iet'] and smf_type == '74.7'"
                    ).drop_duplicates()
                    connectors_list = []
                    for port in ports.to_dict('records'):
                        connectors = df_dict['connector'].reset_index().query(
                            "smf74iet == @switch['smf74iet'] and r747sdev == @port['r747sdev'] and r747cadr == @port['r747padr'] and r747cnum == @port['r747pnum']"
                        ).drop_duplicates()
                        connectors_list.append(connectors.to_dict('records'))
                    page_sub_detail = format_switch_activity("RMF Interval", switch, ports.to_dict('records'),
                                                             fcd.to_dict('records')[0], pros.to_dict('records'),
                                                             connectors_list)
                    if page_sub_detail is not None:
                        if page_detail != '':
                            page_detail += '\n\n'
                        page_detail += page_sub_detail
            if report != '':
                report += '\n\n'
            report += page_detail
    if report == '':
        report = 'No data found.'
    return report


def print_ess_activity(jsonfiles: tuple, start_time_str: str, end_time_str: str,
                       target_cu: Union[str, None] = None, report_type: Union[str, None] = None) -> str:
    """Print smf74 Enterprise Disk Systems Report based on JSON files.

    Args:
        jsonfiles: JSON file or files.
        start_time_str: Start time string.
        end_time_str: End time string.
        target_cu: Target CU.
        report_type: Type of report.

    Returns:
        ESS - Enterprise Disk Systems report.
    """

    def print_one_ess_activity(cntl: dict, report_category: Union[str, None]):
        pros = df_dict['pro'].reset_index().query(
            "smf74iet == @cntl['smf74iet'] and smf_type == '74.8'"
        ).drop_duplicates()
        lsss = df_dict['lss'].reset_index().query(
            "smf74iet == @cntl['smf74iet'] and r748cser == @cntl['r748cser']"
        ).drop_duplicates()
        siols = df_dict['siol'].reset_index().query(
            "smf74iet == @cntl['smf74iet'] and r748cser == @cntl['r748cser']"
        ).drop_duplicates()
        extps = df_dict['extp'].reset_index().query(
            "smf74iet == @cntl['smf74iet'] and r748cser == @cntl['r748cser']"
        ).drop_duplicates()
        report_detail = ''
        if report_category == "Link Statistics" or report_category is None:
            link_stats = format_link_statistics("RMF Interval", cntl, lsss.to_dict('records'),
                                                pros.to_dict('records'))
            if link_stats is not None:
                report_detail = link_stats
        if report_category == "Synchronous I/O Link Statistics" or report_category is None:
            sync_io_stats = format_sync_io_statistics("RMF Interval", cntl,
                                                      siols.to_dict('records'),
                                                      pros.to_dict('records'))
            if sync_io_stats is not None:
                if report_category is None:
                    report_detail += '\n\n'
                report_detail += sync_io_stats
        if report_category == "Extent Pool Statistics" or report_category is None:
            ext_pool_stat = format_extent_pool_statistics("RMF Interval", cntl,
                                                          extps.to_dict('records'),
                                                          pros.to_dict('records'))
            if ext_pool_stat is not None:
                if report_category is None:
                    report_detail += '\n\n'
                report_detail += ext_pool_stat
        if report_category == "Rank Statistics" or report_category is None:
            ranks_list = []
            ranks_arrys_list = []
            for extp in extps.to_dict('records'):
                ranks = df_dict['rank'].reset_index().query(
                    "smf74iet == @extp['smf74iet'] and r748cser == @extp['r748cser'] and r748rpnm == @extp['r748xpid']"
                ).drop_duplicates()
                arrys_list = []
                for rank in ranks.to_dict('records'):
                    arrys = df_dict['arry'].reset_index().query(
                        "smf74iet == @rank['smf74iet'] and r748cser == @rank['r748cser'] and r748arid == @rank['r748rrid']"
                    ).drop_duplicates()
                    arrys_list.append(arrys.to_dict('records'))
                ranks_list.append(ranks.to_dict('records'))
                ranks_arrys_list.append(arrys_list)
            rank_stats = format_rank_statistics("RMF Interval", cntl,
                                                extps.to_dict('records'),
                                                ranks_list, ranks_arrys_list,
                                                pros.to_dict('records'))
            if rank_stats is not None:
                if report_category is None:
                    report_detail += '\n\n'
                report_detail += rank_stats
        return report_detail

    start_time = pd.to_datetime(start_time_str)
    end_time = pd.to_datetime(end_time_str)
    current_time = dt.datetime.now()

    report = ''
    for jsonfile in jsonfiles:
        page_detail = ''
        with open(jsonfile) as f:
            try:
                df = pd.read_json(f)
            except ValueError:
                click.echo(
                    f"\nInvalid JSON file {jsonfile}. This file will be skipped.")
                continue

            if 'header' not in df.columns or not isinstance(df.iloc[0]['header'], dict) \
                    or df.iloc[0]['header'].get('recType') is None or df.iloc[0]['header']['recType'] != 74:
                click.echo(
                    f"\nInvalid JSON file {jsonfile}. This file will be skipped.")
                continue
            try:
                df_dict = format_74df(df, current_time)
            except Exception as e:
                click.echo(f"\nUnsupported JSON file {jsonfile} with error: {str(e)}. This file will be skipped.")
                continue

            if df_dict['pro'].empty:
                click.echo(
                    f"\nThis JSON file {jsonfile} is not for this smf type. This file will be skipped.")
                # Cannot continue processing
                continue
            if df_dict['cntl'].empty:
                click.echo(
                    f"\nThis JSON file {jsonfile} is not for this smf type. This file will be skipped.")
                # Cannot continue processing
                continue
            if target_cu is not None:
                start_tbls = df_dict['cntl'].loc[
                    ~df_dict['cntl'].index.duplicated(keep='first'), :].reset_index().query(
                    "smf74ist >= @start_time and smf74ist <= @end_time and r748cser == @target_cu")
            else:
                start_tbls = df_dict['cntl'].loc[
                    ~df_dict['cntl'].index.duplicated(keep='first'), :].reset_index().query(
                    "smf74ist >= @start_time and smf74ist <= @end_time")

            if start_tbls.empty:
                continue
            start_tbls_gp = start_tbls.reset_index().groupby('smf74iet')
            for report_iet, cntl_df in start_tbls_gp:
                for cntl in cntl_df.to_dict('records'):
                    page_sub_detail = print_one_ess_activity(cntl, report_type)

                    if page_sub_detail != '':
                        if page_detail != '':
                            page_detail += '\n\n'
                        page_detail += page_sub_detail

            if report != '':
                report += '\n\n'
            report += page_detail
    if report == '':
        report = 'No data found.'
    return report


def print_eadm_activity(jsonfiles: tuple, lpar: str, start_time_str: str, end_time_str: str) -> str:
    """Print smf74 EADM Activity Report based on JSON files.

    Args:
        jsonfiles: JSON file or files.
        lpar: Target LPAR to print.
        start_time_str: Start time string.
        end_time_str: End time string.

    Returns:
        EADM Activity report.
    """
    start_time = pd.to_datetime(start_time_str)
    end_time = pd.to_datetime(end_time_str)
    sid = lpar
    current_time = dt.datetime.now()

    report = ''
    for jsonfile in jsonfiles:
        page_detail = ''
        with open(jsonfile) as f:
            try:
                df = pd.read_json(f)
            except ValueError:
                click.echo(
                    f"\nInvalid JSON file {jsonfile}. This file will be skipped.")
                continue

            if 'header' not in df.columns or not isinstance(df.iloc[0]['header'], dict) \
                    or df.iloc[0]['header'].get('recType') is None or df.iloc[0]['header']['recType'] != 74:
                click.echo(
                    f"\nInvalid JSON file {jsonfile}. This file will be skipped.")
                continue
            try:
                df_dict = format_74df(df, current_time)
            except Exception as e:
                click.echo(f"\nUnsupported JSON file {jsonfile} with error: {str(e)}. This file will be skipped.")
                continue

            if df_dict['pro'].empty:
                click.echo(
                    f"\nThis JSON file {jsonfile} is not for this smf type. This file will be skipped.")
                # Cannot continue processing
                continue
            starting = 'eadm'
            starting2 = 'scm'
            if not df_dict[starting].empty:
                df1 = df_dict[starting].reset_index().query(
                    "smf74ist >= @start_time and smf74ist <= @end_time and smf74sid == @lpar"
                ).drop_duplicates()[['smf74ist', 'r7410dsct', 'r7410dfpt', 'r7410diqt', 'r7410dcrt', 'smf74int']]
                if not df1.empty:
                    df1['Date'] = df1['smf74ist'].dt.date
                    df1['Time'] = df1['smf74ist'].dt.strftime('%H:%M')
                    df1['Total\nNumber\nof\nSSCH'] = df1['r7410dsct']
                    df1['SSCH\nRate'] = df1['r7410dsct'] / df1['smf74int']
                    df1['Avg\nFunction\nPending\nTime'] = df1['r7410dfpt'] * 1000 / df1['r7410dsct']
                    df1['Avg\nIOP\nQueue\nTime'] = df1['r7410diqt'] * 1000 / df1['r7410dsct']
                    df1['Avg\nInitial\nCmd\nResponse\nTime'] = df1['r7410dcrt'] * 1000 / df1['r7410dsct']
                    df1.drop(columns=['smf74ist', 'r7410dsct', 'r7410dfpt', 'r7410diqt', 'r7410dcrt', 'smf74int'],
                             inplace=True)

                df2 = df_dict[starting].reset_index().query(
                    "smf74ist >= @start_time and smf74ist <= @end_time and smf74sid == @lpar"
                ).drop_duplicates()[['smf74ist', 'r7410dosc', 'r7410dosd', 'r7410docc', 'r7410disc', 'r7410docd',
                                     'r7410disd', 'smf74int']]
                if not df2.empty:
                    df2['Date'] = df2['smf74ist'].dt.date
                    df2['Time'] = df2['smf74ist'].dt.strftime('%H:%M')
                    df2['Compression\nRequest\nRate'] = df2['r7410docc'] / df2['smf74int']
                    df2['Compression\nThroughput'] = df2['r7410disc'] / df2['smf74int'] * 1024 * 1024
                    df2['Compression\nRatio'] = df2['r7410disc'] / df2['r7410dosc']
                    df2['Decompression\nRequest\nRate'] = df2['r7410docd'] / df2['smf74int']
                    df2['Decompression\nThroughput'] = df2['r7410disd'] / df2['smf74int'] * 1024 * 1024
                    df2['Decompression\nRatio'] = df2['r7410disd'] / df2['r7410dosd']
                    df2.drop(columns=['smf74ist', 'r7410dosc', 'r7410dosd', 'r7410docc', 'r7410disc', 'r7410docd',
                                      'r7410disd', 'smf74int'], inplace=True)
            else:
                df1 = pd.DataFrame()
                df2 = pd.DataFrame()
            if not df_dict[starting2].empty:
                df3 = df_dict[starting2].reset_index().query(
                    "smf74ist >= @start_time and smf74ist <= @end_time and smf74sid == @lpar and r7410vfm == 0"
                ).drop_duplicates()[['smf74ist', 'r7410crid', 'r7410cpid', 'r7410cwu', 'r7410cwuc', 'r7410cdr_bytes',
                                     'r7410cdrc_bytes', 'r7410cdw_bytes', 'r7410cdwc_bytes', 'r7410crq', 'r7410crqc',
                                     'r7410crt', 'r7410crtc', 'r7410ciqc', 'smf74int']]
                if not df3.empty:
                    df3['Date'] = df3['smf74ist'].dt.date
                    df3['Time'] = df3['smf74ist'].dt.strftime('%H:%M')
                    df3['Card\nID'] = df3['r7410cpid'] + '-' + df3['r7410crid']
                    df3['Util%\n(LPAR)'] = df3['r7410cwu'] / df3['smf74int']
                    df3['Util%\n(Total)'] = df3['r7410cwuc'] / df3['smf74int']
                    df3['Read\nB/Sec\n(LPAR)'] = df3['r7410cdr_bytes'] / df3['smf74int']
                    df3['Read\nB/Sec\n(Total)'] = df3['r7410cdrc_bytes'] / df3['smf74int']
                    df3['Write\nB/Sec\n(LPAR)'] = df3['r7410cdw_bytes'] / df3['smf74int']
                    df3['Write\nB/Sec\n(Total)'] = df3['r7410cdwc_bytes'] / df3['smf74int']
                    df3['Request\nRate\n(LPAR)'] = df3['r7410crq'] / df3['smf74int']
                    df3['Request\nRate\n(Total)'] = df3['r7410crqc'] / df3['smf74int']
                    df3['Avg\nResponse\nTime\n(LPAR)'] = df3['r7410crt'] * 1000 / df3['r7410crq']
                    df3['Avg\nResponse\nTime\n(Total)'] = df3['r7410crtc'] * 1000 / df3['r7410crqc']
                    df3['Avg\nIOP\nQueue\nTime\n(Total)'] = df3['r7410ciqc'] * 1000 / df3['r7410crqc']
                    df3['Requests\n(LPAR)'] = df3['r7410crq']
                    df3['Requests\n(Total)'] = df3['r7410crqc']
                    df3['Util%\n(LPAR)'] = df3['Util%\n(LPAR)'].where(df3['Util%\n(LPAR)'] < 100, 100)
                    df3['Util%\n(Total)'] = df3['Util%\n(Total)'].where(df3['Util%\n(Total)'] < 100, 100)
                    df3.drop(columns=['smf74ist', 'r7410crid', 'r7410cpid', 'r7410cwu', 'r7410cwuc', 'r7410cdr_bytes',
                                      'r7410cdrc_bytes', 'r7410cdw_bytes', 'r7410cdwc_bytes', 'r7410crq', 'r7410crqc',
                                      'r7410crt', 'r7410crtc', 'r7410ciqc', 'smf74int'], inplace=True)

                df4 = df_dict[starting2].reset_index().query(
                    "smf74ist >= @start_time and smf74ist <= @end_time and smf74sid == @lpar and r7410vfm == 1"
                ).drop_duplicates()[['smf74ist', 'r7410cwu', 'r7410cwuc', 'r7410cdr_bytes',
                                     'r7410cdrc_bytes', 'r7410cdw_bytes', 'r7410cdwc_bytes', 'r7410crq', 'r7410crqc',
                                     'r7410crt', 'r7410crtc', 'r7410ciqc', 'smf74int']]
                if not df4.empty:
                    df4['Date'] = df4['smf74ist'].dt.date
                    df4['Time'] = df4['smf74ist'].dt.strftime('%H:%M')
                    df4['Card\nID'] = 'VFM'
                    df4['Util%\n(LPAR)'] = df4['r7410cwu'] / df4['smf74int']
                    df4['Util%\n(Total)'] = df4['r7410cwuc'] / df4['smf74int']
                    df4['Read\nB/Sec\n(LPAR)'] = df4['r7410cdr_bytes'] / df4['smf74int']
                    df4['Read\nB/Sec\n(Total)'] = df4['r7410cdrc_bytes'] / df4['smf74int']
                    df4['Write\nB/Sec\n(LPAR)'] = df4['r7410cdw_bytes'] / df4['smf74int']
                    df4['Write\nB/Sec\n(Total)'] = df4['r7410cdwc_bytes'] / df4['smf74int']
                    df4['Request\nRate\n(LPAR)'] = df4['r7410crq'] / df4['smf74int']
                    df4['Request\nRate\n(Total)'] = df4['r7410crqc'] / df4['smf74int']
                    df4['Avg\nResponse\nTime\n(LPAR)'] = df4['r7410crt'] * 1000 / df4['r7410crq']
                    df4['Avg\nResponse\nTime\n(Total)'] = df4['r7410crtc'] * 1000 / df4['r7410crqc']
                    df4['Avg\nIOP\nQueue\nTime\n(Total)'] = df4['r7410ciqc'] * 1000 / df4['r7410crqc']
                    df4['Requests\n(LPAR)'] = df4['r7410crq']
                    df4['Requests\n(Total)'] = df4['r7410crqc']
                    df4['Util%\n(LPAR)'] = df4['Util%\n(LPAR)'].where(df4['Util%\n(LPAR)'] < 100, 100)
                    df4['Util%\n(Total)'] = df4['Util%\n(Total)'].where(df4['Util%\n(Total)'] < 100, 100)
                    df4.drop(columns=['smf74ist', 'r7410cwu', 'r7410cwuc', 'r7410cdr_bytes',
                                      'r7410cdrc_bytes', 'r7410cdw_bytes', 'r7410cdwc_bytes', 'r7410crq', 'r7410crqc',
                                      'r7410crt', 'r7410crtc', 'r7410ciqc', 'smf74int'], inplace=True)
            else:
                df3 = pd.DataFrame()
                df4 = pd.DataFrame()

            if not df1.empty:
                page_detail += '\nDevice/Subchannel Summary\n'
                for col_name in df1.columns:
                    df1[col_name] = df1[col_name].replace(to_replace=[np.nan], value=None)
                page_detail += tb.tabulate(
                    df1, headers='keys', tablefmt='psql', showindex=False, floatfmt='.2f')

            if not df2.empty:
                page_detail += '\nCompression Activity\n'
                for col_name in df2.columns:
                    df2[col_name] = df2[col_name].replace(to_replace=[np.nan], value=None)
                page_detail += tb.tabulate(
                    df2, headers='keys', tablefmt='psql', showindex=False, floatfmt='.2f')

            if not df3.empty:
                page_detail += '\nStorage Class Memory Activity\n'
                for col_name in df3.columns:
                    if df3[col_name].isnull().all():
                        df3 = df3.astype({col_name: str})
                        df3[col_name] = None
                    df3[col_name] = df3[col_name].replace(to_replace=[np.nan], value=None)
                page_detail += tb.tabulate(
                    df3, headers='keys', tablefmt='psql', showindex=False, floatfmt='.2f')

            if not df4.empty:
                page_detail += '\nStorage Class Memory Activity\n'
                for col_name in df4.columns:
                    if df4[col_name].isnull().all():
                        df4 = df4.astype({col_name: str})
                        df4[col_name] = None
                    df4[col_name] = df4[col_name].replace(to_replace=[np.nan], value=None)
                page_detail += tb.tabulate(
                    df4, headers='keys', tablefmt='psql', showindex=False, floatfmt='.2f')
            if report != '':
                report += '\n\n'
            report += page_detail
    if report == '':
        report = 'No data found.'
    return report


def print_pcie_activity(jsonfiles: tuple, start_time_str: str, end_time_str: str) -> str:
    """Print smf74 PCIE Activity Report based on JSON files.

    Args:
        jsonfiles: JSON file or files.
        start_time_str: Start time string.
        end_time_str: End time string.

    Returns:
        PCIE Activity report.
    """
    start_time = pd.to_datetime(start_time_str)
    end_time = pd.to_datetime(end_time_str)
    current_time = dt.datetime.now()

    report = ''
    for jsonfile in jsonfiles:
        page_detail = ''
        with open(jsonfile) as f:
            try:
                df = pd.read_json(f)
            except ValueError:
                click.echo(
                    f"\nInvalid JSON file {jsonfile}. This file will be skipped.")
                continue

            if 'header' not in df.columns or not isinstance(df.iloc[0]['header'], dict) \
                    or df.iloc[0]['header'].get('recType') is None or df.iloc[0]['header']['recType'] != 74:
                click.echo(
                    f"\nInvalid JSON file {jsonfile}. This file will be skipped.")
                continue
            try:
                df_dict = format_74df(df, current_time)
            except Exception as e:
                click.echo(f"\nUnsupported JSON file {jsonfile} with error: {str(e)}. This file will be skipped.")
                continue

            if df_dict['pro'].empty:
                click.echo(
                    f"\nThis JSON file {jsonfile} is not for this smf type. This file will be skipped.")
                # Cannot continue processing
                continue
            if df_dict['pcie'].empty:
                click.echo(
                    f"\nThis JSON file {jsonfile} is not for this smf type. This file will be skipped.")
                # Cannot continue processing
                continue

            general_df = df_dict['pcie'].reset_index().query(
                "smf74ist >= @start_time and smf74ist <= @end_time"
            ).drop_duplicates()[['smf74ist', 'r749pfid', 'r749pcid', 'r749devn', 'status', 'r749jobn', 'r749asid',
                                 'r749allt', 'pciload', 'pcistor', 'pcistbl', 'pcirptr', 'pcibytr', 'pcibytt']]

            ha_df = df_dict['pcie'].reset_index().query(
                "smf74ist >= @start_time and smf74ist <= @end_time and r749fpfn > 0"
            ).drop_duplicates()[
                ['smf74ist', 'r749pfid', 'fpgbusy', 'pciutil', 'pciwup', 'fpgrtim', 'stdd_ftet', 'fpgqtim',
                 'stdd_ftqt', 'fpgbytr', 'fpgbyts']]

            ha_compress_df = df_dict['pcie'].reset_index().query(
                "smf74ist >= @start_time and smf74ist <= @end_time and r749fp1n > 0"
            ).drop_duplicates()[
                ['smf74ist', 'r749pfid', 'fpgcors', 'fpgcobs', 'fpgcort', 'fpgdcrs', 'fpgdcbs', 'fpgdcrt',
                 'r7491bps', 'fpgbprt']]

            roce_df = df_dict['pcie'].reset_index().query(
                "smf74ist >= @start_time and smf74ist <= @end_time and physical_network == 1 and r749net2 != ''"
            ).drop_duplicates()[
                ['smf74ist', 'r749pfid', 'r749net1', 'r749net2', 'pcibytr', 'pcibytt', 'pcipakr', 'pcipakt']]

            ism_df = df_dict['pcie'].reset_index().query(
                "smf74ist >= @start_time and smf74ist <= @end_time and r749net1 != '' and r749net2 == ''"
            ).drop_duplicates()[['smf74ist', 'r749pfid', 'r749net1', 'pcibytt']]

            syncio_df = df_dict['pcie'].reset_index().query(
                "smf74ist >= @start_time and smf74ist <= @end_time and r749sion > 0"
            ).drop_duplicates()[['smf74ist', 'r749pfid', 'r749pcid', 'r749port', 'r749snds', 'r749sndt',
                                 'synctr', 'cpcsynctr', 'syncsr', 'cpcsyncsr', 'pcibytr', 'cpcpcibytr', 'pcibytr_ratio',
                                 'cpcpcibytr_ratio', 'pcibytt', 'cpcpcibytt', 'pcibytt_ratio', 'cpcpcibytt_ratio',
                                 'fpgbusy', 'cpcfpgbusy', 'r749sndm']]

            synciortd_df = df_dict['pcie'].reset_index().query(
                "smf74ist >= @start_time and smf74ist <= @end_time and r749rtdn > 0"
            ).drop_duplicates()[
                ['smf74ist', 'r749pfid', 'pcipcr1', 'pcipcr2', 'pcipcr3', 'pcipcr4', 'pcipcr5', 'pcipcr6',
                 'pcipcr7', 'pcipcr8', 'pcipcr9', 'pcipcr10', 'pcipcw1', 'pcipcw2', 'pcipcw3', 'pcipcw4',
                 'pcipcw5', 'pcipcw6', 'pcipcw7', 'pcipcw8', 'pcipcw9', 'pcipcw10']]

        if not general_df.empty:
            general_df['pcibytr'] = general_df['pcibytr'] + general_df['pcibytt']
            general_df.drop(['pcibytt'], inplace=True, axis=1)
            general_df.columns = ['DTime', 'Function\nID', 'Function\nCHID', 'Function Name', 'Function\nStatus',
                                  'Owner\nJob\nName', 'Owner\nAddress\nSpace\nID', 'Function\nAllocation\nTime',
                                  'PCI Load\nOperations\nRate', 'PCI Store\nOperations\nRate',
                                  'PCI Store\nBlock\nOperations\nRate', 'Refresh PCI\nTranslations\nOperations\nRate',
                                  'Data\nTransfer\nRate']
            general_df['Date'] = general_df['DTime'].dt.date
            general_df['Time'] = general_df['DTime'].dt.strftime('%H:%M')
            general_df = general_df[
                ['Date'] + ['Time'] + general_df.columns.drop(['Date', 'Time', 'DTime']).tolist()].copy()
            page_detail += '\nGeneral PCIE Activity\n'
            for col_name in general_df.columns:
                general_df[col_name] = general_df[col_name].replace(to_replace=[np.nan], value=None)
            page_detail += tb.tabulate(general_df, headers='keys', tablefmt='psql', showindex=False,
                                       floatfmt='.3f')  # , missingval='-')
            page_detail += '\n'

        if not ha_df.empty:
            ha_df['fpgbytr'] = ha_df['fpgbytr'] + ha_df['fpgbyts']
            ha_df.drop(['fpgbyts'], inplace=True, axis=1)
            ha_df.columns = ['DTime', 'Function\nID', 'Time\nBusy %', 'Adapter\nUtilization', 'pciutil',
                             'Request\nExecution Time',
                             'Std Dev for Request\nExecution Time', 'Request\nQueue Time',
                             'Std Dev for\nRequest Queue Time', 'Request\nSize']
            ha_df['Date'] = ha_df['DTime'].dt.date
            ha_df['Time'] = ha_df['DTime'].dt.strftime('%H:%M')
            ha_df['Work Units\nProcessed Rate'] = ha_df['pciutil'].map(lambda x: convert_si(x, 8, 0),
                                                                       na_action='ignore')
            ha_df = ha_df[['Date', 'Time', 'Function\nID', 'Time\nBusy %', 'Adapter\nUtilization',
                           'Work Units\nProcessed Rate', 'Request\nExecution Time',
                           'Std Dev for Request\nExecution Time', 'Request\nQueue Time',
                           'Std Dev for\nRequest Queue Time', 'Request\nSize']]
            page_detail += '\nHardware Accelerator Activity\n'
            page_detail += tb.tabulate(ha_df, headers='keys', tablefmt='psql', showindex=False, floatfmt='.1f',
                                       stralign='right')
            page_detail += '\n'

        if not ha_compress_df.empty:
            ha_compress_df.columns = ['DTime', 'Function\nID', 'Compression\nRequest Rate', 'Compression\nThroughput',
                                      'Compression\nRatio', 'Decompression\nRequest Rate', 'Decompression\nThroughput',
                                      'Decompression\nRatio', 'Buffer\nPool\nSize', 'Buffer Pool\nUtilization']
            ha_compress_df['Date'] = ha_compress_df['DTime'].dt.date
            ha_compress_df['Time'] = ha_compress_df['DTime'].dt.strftime('%H:%M')
            ha_compress_df = ha_compress_df[
                ['Date'] + ['Time'] + ha_compress_df.columns.drop(['Date', 'Time', 'DTime']).tolist()].copy()
            page_detail += '\nHardware Accelerator Compression Activity\n'
            page_detail += tb.tabulate(ha_compress_df, headers='keys', tablefmt='psql', showindex=False, floatfmt='.3f')
            page_detail += '\n'

        if not roce_df.empty:
            roce_df.columns = ['DTime', 'Function\nID', 'Physical Network ID\nPort 1', 'Physical Network ID\nPort 2',
                               'Read Transfer\nRate', 'Write Transfer\nRate', 'Packets Received\nRate',
                               'Packets Transmitted\nRate']
            roce_df['Date'] = roce_df['DTime'].dt.date
            roce_df['Time'] = roce_df['DTime'].dt.strftime('%H:%M')
            roce_df = roce_df[['Date'] + ['Time'] + roce_df.columns.drop(['Date', 'Time', 'DTime']).tolist()].copy()
            page_detail += '\nRoCE Activity\n'
            for col_name in roce_df.columns:
                roce_df[col_name] = roce_df[col_name].replace(to_replace=[np.nan], value=None)
            page_detail += tb.tabulate(roce_df, headers='keys', tablefmt='psql', showindex=False, floatfmt='.0f')
            page_detail += '\n'

        if not ism_df.empty:
            ism_df.columns = ['DTime', 'Function ID', 'Physical Network ID', 'Write Transfer Rate']
            ism_df['Date'] = ism_df['DTime'].dt.date
            ism_df['Time'] = ism_df['DTime'].dt.strftime('%H:%M')
            ism_df = ism_df[['Date'] + ['Time'] + ism_df.columns.drop(['Date', 'Time', 'DTime']).tolist()].copy()
            page_detail += '\nInternal Shared Memory Activity\n'
            for col_name in ism_df.columns:
                ism_df[col_name] = ism_df[col_name].replace(to_replace=[np.nan], value=None)
            page_detail += tb.tabulate(ism_df, headers='keys', tablefmt='psql', showindex=False, floatfmt='.0f')
            page_detail += '\n'

        if not syncio_df.empty:
            syncio_df['r749sndt'] = syncio_df['r749sndt'] + '-' + syncio_df['r749sndm']
            syncio_df.drop(['r749sndm'], inplace=True, axis=1)
            syncio_df.columns = ['DTime', 'Function\nID', 'Function\nCHID', 'Port\nID', 'Serial\nNumber', 'Type-Model',
                                 'Total\nRequest\nRate', 'Total\nRequest\nRate\n(CPC)', 'Successful\nRequest %',
                                 'Successful\nRequest %\n(CPC)', 'Read\nTransfer\nRate', 'Read\nTransfer\nRate\n(CPC)',
                                 'Read\nTransfer\nRatio', 'Read\nTransfer\nRatio\n(CPC)', 'Write\nTransfer\nRate',
                                 'Write\nTransfer\nRate\n(CPC)', 'Write\nTransfer\nRatio',
                                 'Write\nTransfer\nRatio\n(CPC)',
                                 'Time\nBusy\n%', 'Time\nBusy\n%\n(CPC)']
            syncio_df['Date'] = syncio_df['DTime'].dt.date
            syncio_df['Time'] = syncio_df['DTime'].dt.strftime('%H:%M')
            syncio_df = syncio_df[
                ['Date'] + ['Time'] + syncio_df.columns.drop(['Date', 'Time', 'DTime']).tolist()].copy()
            page_detail += '\nSynchronous I/O Link Activity\n'
            for col_name in syncio_df.columns:
                syncio_df[col_name] = syncio_df[col_name].replace(to_replace=[np.nan], value=None)
            page_detail += tb.tabulate(syncio_df, headers='keys', tablefmt='psql', showindex=False, floatfmt='.3f')
            page_detail += '\n'

        if not synciortd_df.empty:
            synciortd_df.columns = ['DTime', 'Function\nID', '%\nRead <\n20μsec', '%\nRead <\n30μsec',
                                    '%\nRead <\n40μsec', '%\nRead <\n50μsec', '%\nRead <\n60μsec', '%\nRead <\n70μsec',
                                    '%\nRead <\n80μsec', '%\nRead <\n90μsec', '% Read <\n100μsec', '% Read\n>= 100μsec',
                                    '%\nWrite <\n20μsec', '%\nWrite <\n30μsec', '%\nWrite <\n40μsec',
                                    '%\nWrite <\n50μsec', '%\nWrite <\n60μsec', '%\nWrite <\n70μsec',
                                    '%\nWrite <\n80μsec', '%\nWrite <\n90μsec', '% Write <\n100μsec',
                                    '% Write\n>= 100μsec']
            synciortd_df['Date'] = synciortd_df['DTime'].dt.date
            synciortd_df['Time'] = synciortd_df['DTime'].dt.strftime('%H:%M')
            synciortd_df = synciortd_df[
                ['Date'] + ['Time'] + synciortd_df.columns.drop(['Date', 'Time', 'DTime']).tolist()]
            page_detail += '\nSynchronous I/O Response Time Distribution\n'
            page_detail += tb.tabulate(synciortd_df, headers='keys', tablefmt='psql', showindex=False, floatfmt='.3f')
            page_detail += '\n'
        if report != '':
            report += '\n\n'
        report += page_detail
    if report == '':
        report = 'No data found.'
    return report


def print_xcf_activity(jsonfiles: tuple, lpar: str, start_time_str: str, end_time_str: str) -> str:
    """Print smf74 XCF Activity Report based on JSON files.

    Args:
        jsonfiles: JSON file or files.
        lpar: Target LPAR to print.
        start_time_str: Start time string.
        end_time_str: End time string.

    Returns:
        XCF Activity report.
    """
    start_time = pd.to_datetime(start_time_str)
    end_time = pd.to_datetime(end_time_str)
    sid = lpar
    current_time = dt.datetime.now()

    report = ''
    for jsonfile in jsonfiles:
        page_detail = ''
        with open(jsonfile) as f:
            try:
                df = pd.read_json(f)
            except ValueError:
                click.echo(
                    f"\nInvalid JSON file {jsonfile}. This file will be skipped.")
                continue

            if 'header' not in df.columns or not isinstance(df.iloc[0]['header'], dict) \
                    or df.iloc[0]['header'].get('recType') is None or df.iloc[0]['header']['recType'] != 74:
                click.echo(
                    f"\nInvalid JSON file {jsonfile}. This file will be skipped.")
                continue
            try:
                df_dict = format_74df(df, current_time)
            except Exception as e:
                click.echo(f"\nUnsupported JSON file {jsonfile} with error: {str(e)}. This file will be skipped.")
                continue

            if df_dict['pro'].empty:
                click.echo(
                    f"\nThis JSON file {jsonfile} is not for this smf type. This file will be skipped.")
                # Cannot continue processing
                continue
            if not df_dict['xctl'].empty:
                start_tbls = df_dict['xctl'].query(
                    "smf74ist >= @start_time and smf74ist <= @end_time and smf74sid == @lpar")
            else:
                continue

            if start_tbls.empty:
                continue

            for ctl in start_tbls.loc[~start_tbls.index.duplicated(keep='first'), :].reset_index().to_dict('records'):
                pro = df_dict['pro'].loc[~df_dict['pro'].index.duplicated(keep='first'), :].reset_index().query(
                    "smf74iet == @ctl['smf74iet'] and smf74sid == @ctl['smf74sid'] and smf_type == '74.2'"
                ).drop_duplicates()
                syss = df_dict['sys'].reset_index().query(
                    "smf74iet == @ctl['smf74iet'] and smf74sid == @ctl['smf74sid']"
                ).drop_duplicates()
                mbrs = df_dict['mbr'].reset_index().query(
                    "smf74iet == @ctl['smf74iet'] and smf74sid == @ctl['smf74sid']"
                ).drop_duplicates()
                paths = df_dict['path'].reset_index().query(
                    "smf74iet == @ctl['smf74iet'] and smf74sid == @ctl['smf74sid']"
                ).drop_duplicates()
                mbrs_list = []
                for sys in syss.to_dict('records'):
                    sys_mbrs_list = []
                    if sys['r742sdir'] == 'IN':
                        mbr_tbls = df_dict['mbr'].reset_index().query(
                            "smf74iet == @sys['smf74iet'] and smf74sid == @sys['smf74sid'] and r742msys == @sys['r742snme']"
                        ).drop_duplicates()
                        mbrs_list.append(mbr_tbls.to_dict('records'))
                    else:
                        mbrs_list.append(sys_mbrs_list)
                mbrs_group = mbrs.groupby('r742mgrp')
                mbr_group_list = []
                for gp, mbrs_df in mbrs_group:
                    mbr_group_list.append(mbrs_df.to_dict('records'))
                paths_group = paths.groupby('r742pdir')
                paths_group_list = []
                for gp, paths_df in paths_group:
                    paths_group_list.append(paths_df.to_dict('records'))
                xcf_detail_object_list, page_sub_detail = format_xcf_activity_report("RMF Interval", ctl,
                                                                                     pro.to_dict('records')[0],
                                                                                     syss.to_dict('records'),
                                                                                     mbrs.to_dict('records'),
                                                                                     paths.to_dict('records'),
                                                                                     mbrs_list, mbr_group_list,
                                                                                     paths_group_list)
                if page_sub_detail is not None:
                    if page_detail != '':
                        page_detail += '\n\n'
                    page_detail += page_sub_detail

            if report != '':
                report += '\n\n'
            report += page_detail
    if report == '':
        report = 'No data found.'
    return report

