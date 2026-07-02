import datetime as dt
from typing import Union

import click
import numpy as np
import pandas as pd

from smf2db.api.report_util import format_policy_page, format_workload_header, format_transaction_detail, \
    format_state_samples_breakdown, format_goal_and_response_lpar, format_response_time_distribution, \
    format_goal_and_response_sysplex, format_delay_summary, format_cms_lock_detail, format_cml_lock_detail, \
    format_grs_latch_detail, format_grs_enq_detail, format_sdelay_header, is_bit_set
from smf2db.api.util import (setdatetime, to_int, col_to_frame, is_list_of_list,
                             calculate_std_dev, cols_to_frame)
from smf2db.db_models.smf72_model import (Smf72Pro, Smf72Policy, Smf72Dnsx, Smf72Workload, Smf72Wrsx, Smf72Scs,
                                          Smf72Data, Smf72Sctl, Smf72Wms, Smf72Sss, Smf72Rgs, Smf72Rts, Smf72Wrs,
                                          Smf72Dns, Smf72Cmss, Smf72Ceds, Smf72Clod, Smf72Clrd, Smf72Lotd, Smf72Lasc,
                                          Smf72Lare, Smf72Ense, Smf72Ensy, Smf72Enss, Smf72Qsad, Smf72Clas, Smf72Csms)


def build_pro(df: pd.DataFrame) -> Union[pd.DataFrame, None]:
    """Build the dataframe for RMF Product Section which will be uploaded to smf72_pro table.

    Args:
        df: The master dataframe which is created from the JSON file.

    Returns:
        The dataframe for the RMF product section or None if csc is not found in the database.
    """
    set_datetime = np.vectorize(setdatetime)
    df_pro = pd.concat([df['header'].apply(pd.Series),
                        df['smf72pro'].apply(pd.Series)],
                       axis=1).rename(
        columns={'sysId': 'smf72sid', 'sysInd': 'smf72flg', 'recType': 'smf_type'})
    df_pro['csc'] = np.nan
    df_pro['smf72sid'] = df_pro['smf72sid'].str.strip()
    df_pro['smf72ist'] = pd.to_datetime(df_pro['smf72ist'])
    df_pro['smf72gie'] = pd.to_datetime(df_pro['smf72gie'])
    df_pro['smf72int'] = pd.to_timedelta(df_pro['smf72int']) / np.timedelta64(1, 's')
    df_pro['smf72lgo'] = pd.to_timedelta(df_pro['smf72lgo']) / np.timedelta64(1, 'h')
    df_pro['datetime'] = set_datetime(df_pro['smf72ist'])
    df_pro['smf72flg'] = df_pro['smf72flg'].apply(lambda x: int(str(x), 16))
    df_pro['smf72fla'] = df_pro['smf72fla'].apply(lambda x: int(str(x), 16))
    df_pro['smf72prf'] = df_pro['smf72prf'].apply(lambda x: int(str(x), 16))
    df_pro['smf72srl'] = df_pro['smf72srl'].apply(lambda x: int(str(x), 16))
    df_pro['speed_boost'] = df_pro['smf72fla'].apply(lambda x: is_bit_set(x, 16, 10))
    df_pro['ziip_boost'] = df_pro['smf72fla'].apply(lambda x: is_bit_set(x, 16, 9))
    df_pro['smf_type'] = df_pro['smf_type'].astype(str) + '.' + df_pro['subType'].astype(str)
    df_pro = df_pro.set_index(
        ['datetime', 'smf72ist', 'smf72iet', 'smf_type', 'csc', 'smf72sid', 'smf72int'])
    return df_pro


def build_policy(df: pd.DataFrame) -> Union[pd.DataFrame, None]:
    """Build the dataframe for Policy class which will be uploaded to smf72_policy table.

    Args:
        df: The master dataframe which is created from the JSON file.

    Returns:
        The dataframe for the Policy class or None if csc is not found in the database.
    """
    if 'r723wms' in df.columns:
        if 'r723rgs' in df.columns:
            df_policy = pd.concat([df[df.index.get_level_values('smf_type') == '72.3']['smf72pro'].apply(pd.Series)[
                                       ['smf72ptn', 'smf72snm', 'smf72xnm', 'smf72mvs', 'smf72mfv', 'smf72prf']],
                                   df[df.index.get_level_values('smf_type') == '72.3']['r723wms'].apply(pd.Series),
                                   df[df.index.get_level_values('smf_type') == '72.3']['r723rgs'].apply(pd.Series)[
                                       ['r723ggnm']]],
                                  axis=1).reset_index().set_index(
                ['smf72xnm', 'datetime', 'smf72ist', 'smf72iet', 'r723mnsp', 'smf72sid'])
        else:
            df_policy = pd.concat([df[df.index.get_level_values('smf_type') == '72.3']['smf72pro'].apply(pd.Series)[
                                       ['smf72ptn', 'smf72snm', 'smf72xnm', 'smf72mvs', 'smf72mfv', 'smf72prf']],
                                   df[df.index.get_level_values('smf_type') == '72.3']['r723wms'].apply(pd.Series),
                                   ], axis=1).reset_index().set_index(
                ['smf72xnm', 'datetime', 'smf72ist', 'smf72iet', 'r723mnsp', 'smf72sid'])
        if 'r723cpa_actual' not in df_policy.columns:
            df_policy['r723cpa_scaling_factor'] = np.nan
            df_policy['r723cpa_actual'] = np.nan
        df_policy['smf72prf'] = df_policy['smf72prf'].apply(lambda x: int(str(x), 16))
        df_policy['r723mscf'] = df_policy['r723mscf'].apply(lambda x: int(str(x), 16))
        df_policy['r723mflg'] = df_policy['r723mflg'].apply(lambda x: int(str(x), 16))
        df_policy['r723mfl2'] = df_policy['r723mfl2'].apply(lambda x: int(str(x), 16))
        df_policy['r723mtpa'] = pd.to_datetime(df_policy['r723mtpa'], errors='coerce')
        df_policy['r723mtvl'] = pd.to_timedelta(df_policy['r723mtvl']) / np.timedelta64(1, 's')
        df_policy['r723mtdi'] = pd.to_datetime(df_policy['r723mtdi'], errors='coerce')
        df_policy['io_high'] = df_policy['r723mscf'].apply(lambda x: is_bit_set(x, 8, 7))
        df_policy['velocity_io_delays'] = df_policy['r723mscf'].apply(lambda x: is_bit_set(x, 8, 3))
        df_policy['dynamic_alias'] = df_policy['r723mscf'].apply(lambda x: is_bit_set(x, 8, 6))
        df_policy['r723mdis'] = df_policy['r723mscf'].apply(lambda x: is_bit_set(x, 8, 6))
        df_policy['r723mtpa'] = pd.to_datetime(df_policy['r723mtpa'], errors='coerce')
        df_policy['r723mcpu'] = df_policy['r723mcpu'] / 10000
        df_policy['r723mioc'] = df_policy['r723mioc'] / 10000
        df_policy['r723mmso'] = df_policy['r723mmso'] / 10000
        df_policy['r723msrb'] = df_policy['r723msrb'] / 10000
        df_policy['r723mtdi'] = pd.to_datetime(df_policy['r723mtdi'], errors='coerce')
        df_policy['ziip_inst'] = df_policy['smf72prf'].apply(lambda x: is_bit_set(x, 8, 5))
        df_policy['zaap_inst'] = df_policy['smf72prf'].apply(lambda x: is_bit_set(x, 8, 4))

        if 'r723ggnm' not in df_policy.columns:
            df_policy['r723ggnm'] = np.nan
        df_policy['cpu_service_coefficient_adjusted'] = df_policy['r723mcpu'] * 16e6 / df_policy['r723madj']
        df_policy['srb_service_coefficient_adjusted'] = df_policy['r723msrb'] * 16e6 / df_policy['r723madj']
    else:
        df_policy = pd.DataFrame(columns=Smf72Policy.__table__.columns.keys()).set_index(
            [col.name for col in Smf72Policy.__table__.primary_key.columns.values()])
    return df_policy


def build_sss(df: pd.DataFrame) -> pd.DataFrame:
    """Build the dataframe for Service Class Served Data Section which will be loaded to smf72_sss table.

    Args:
        df: The master dataframe which is created from the JSON file.

    Returns:
        The dataframe for the Service Class Served class.
    """
    if 'r723sss' in df.columns:  # Service Class being served
        x = pd.concat([df[df.index.get_level_values('smf_type') == '72.3']['smf72pro'].apply(pd.Series)[
                           ['smf72ptn', 'smf72snm', 'smf72xnm', 'smf72mvs', 'smf72mfv']],
                       df[df.index.get_level_values('smf_type') == '72.3']['r723wms'].apply(pd.Series)[
                           ['r723mnsp', 'r723mwnm', 'r723mcnm']],
                       df[df.index.get_level_values('smf_type') == '72.3']['r723scs'].apply(pd.Series)[['r723cper']],
                       df[df.index.get_level_values('smf_type') == '72.3'][['r723sss']]], axis=1
                      ).reset_index().set_index(
            ['smf72xnm', 'datetime', 'smf72ist', 'smf72iet', 'r723mnsp', 'r723mwnm', 'r723mcnm', 'r723cper',
             'smf72sid'])
        df_sss = col_to_frame(x, 'r723sss', x.index
                              ).astype({'r723cper': int}).set_index(
            [col.name for col in Smf72Sss.__table__.primary_key.columns.values()])
    else:
        df_sss = pd.DataFrame(columns=Smf72Sss.__table__.columns.keys()).set_index(
            [col.name for col in Smf72Sss.__table__.primary_key.columns.values()])
    return df_sss


def build_workload(df: pd.DataFrame, df_policy: pd.DataFrame, current_time: dt.datetime) -> pd.DataFrame:
    """Build the dataframe for Workload class which will be uploaded to smf72_workload table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_policy: The policy dataframe.
        current_time: The time to update the last update time.

    Returns:
        The dataframe for the Workload class.
    """
    if 'r723wms' in df.columns:
        df_workload = df_policy.reset_index()[
            ['smf72xnm', 'datetime', 'smf72ist', 'smf72iet', 'r723mnsp', 'r723mwnm', 'r723mwde']].copy().set_index(
            [col.name for col in Smf72Workload.__table__.primary_key.columns.values()])
        df_workload['last_update_time'] = current_time
    else:
        df_workload = pd.DataFrame(columns=Smf72Workload.__table__.columns.keys()).set_index(
            [col.name for col in Smf72Workload.__table__.primary_key.columns.values()])
    return df_workload


def build_wms(df: pd.DataFrame, df_policy_idx: pd.Index, current_time: dt.datetime) -> pd.DataFrame:
    """Build the dataframe for Workload Management Service class which will be uploaded to smf72_wms table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_policy_idx: The index of th policy dataframe.
        current_time: The time to update the last update time.

    Returns:
        The dataframe for the Workload Management Service class.
    """
    if 'r723scs' in df.columns:
        df_wms = col_to_frame(df[df.index.get_level_values('smf_type') == '72.3'], 'r723scs', df_policy_idx
                              ).set_index([col.name for col in Smf72Wms.__table__.primary_key.columns.values()])
        df_wms['r723cadf'] = df_wms['r723cadf'].apply(lambda x: int(str(x), 16))
        df_wms['r723crtf'] = df_wms['r723crtf'].apply(lambda x: int(str(x), 16))
        df_wms['r723crgf'] = df_wms['r723crgf'].apply(lambda x: int(str(x), 16))
        df_wms['r723crs1'] = df_wms['r723crs1'].apply(lambda x: int(str(x), 16))
        df_wms['stor_protection'] = df_wms['r723mscf'].apply(lambda x: is_bit_set(x, 8, 5))
        df_wms['cpu_protection'] = df_wms['r723mscf'].apply(lambda x: is_bit_set(x, 8, 4))
        df_wms['velocity_io_delays'] = df_wms['r723mscf'].apply(lambda x: is_bit_set(x, 8, 3))
        df_wms['svpol_unaval'] = df_wms['r723mscf'].apply(lambda x: is_bit_set(x, 8, 2))
        df_wms['rcaa_unaval'] = df_wms['r723mscf'].apply(lambda x: is_bit_set(x, 8, 1))
        df_wms['is_report_class'] = df_wms['r723mscf'].apply(lambda x: is_bit_set(x, 8, 0))
        df_wms['zaap_crossover'] = df_wms['r723mflg'].apply(lambda x: is_bit_set(x, 8, 0))
        df_wms['zaap_honor_prio'] = df_wms['r723mflg'].apply(lambda x: is_bit_set(x, 8, 1))
        df_wms['ziip_honor_prio'] = df_wms['r723mflg'].apply(lambda x: is_bit_set(x, 8, 2))
        df_wms['hismt_failure'] = df_wms['r723mflg'].apply(lambda x: is_bit_set(x, 8, 3))
        df_wms['honor_prio'] = df_wms['r723mflg'].apply(lambda x: is_bit_set(x, 8, 4))
        df_wms['tenant_report_class'] = df_wms['r723mflg'].apply(lambda x: is_bit_set(x, 8, 5))
        df_wms['r723rtdt'] = pd.to_datetime(df_wms['r723rtdt'], format='%Y-%m-%d %H:%M:%S.%f', errors='coerce')
        df_wms['last_update_time'] = current_time
    else:
        df_wms = pd.DataFrame(columns=Smf72Wms.__table__.columns.keys()).set_index(
            [col.name for col in Smf72Wms.__table__.primary_key.columns.values()])
    return df_wms


def build_rgs(df: pd.DataFrame, df_policy_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for Resource Group Data Section which will be uploaded to smf72_rgs table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_policy_idx: The index of th policy dataframe.

    Returns:
        The dataframe for the Resource Group Data Section.
    """
    if 'r723rgs' in df.columns:  # r723rgs exists (only one can exist)
        df_rgs = col_to_frame(df[df.index.get_level_values('smf_type') == '72.3'], 'r723rgs', df_policy_idx
                              ).set_index([col.name for col in Smf72Rgs.__table__.primary_key.columns.values()])
        df_rgs['r723gglt'] = df_rgs['r723gglt'].apply(lambda x: int(str(x), 16))
        df_rgs['r723ggtf'] = df_rgs['r723ggtf'].apply(lambda x: int(str(x), 16))
        df_rgs['has_max_capacity'] = df_rgs['r723gglt'].apply(lambda x: is_bit_set(x, 8, 0))
        df_rgs['has_min_capacity'] = df_rgs['r723gglt'].apply(lambda x: is_bit_set(x, 8, 1))
        df_rgs['r723ggpv'] = df_rgs['r723gglt'].apply(lambda x: is_bit_set(x, 8, 2))
        df_rgs['r723ggpc'] = df_rgs['r723gglt'].apply(lambda x: is_bit_set(x, 8, 3))
        df_rgs['has_memory_limit'] = df_rgs['r723gglt'].apply(lambda x: is_bit_set(x, 8, 4))
        df_rgs['r723ggms'] = df_rgs['r723gglt'].apply(lambda x: is_bit_set(x, 8, 5))
        df_rgs['r723gisp'] = df_rgs['r723gglt'].apply(lambda x: is_bit_set(x, 8, 6))
        df_rgs['is_tenant'] = df_rgs['r723ggtf'].apply(lambda x: is_bit_set(x, 8, 0))

        df_rgs['r723ggmx'] = np.where(df_rgs['r723ggpc'] | df_rgs['r723ggpv'], df_rgs['r723ggmx'] / 100,
                                      df_rgs['r723ggmx'])
        df_rgs['r723ggmn'] = np.where(df_rgs['r723ggpc'] | df_rgs['r723ggpv'], df_rgs['r723ggmn'] / 100,
                                      df_rgs['r723ggmn'])

        if 'r723ggky' not in df_rgs.columns:
            df_rgs['r723ggky'] = np.nan
            df_rgs['r723ggtn'] = np.nan
            df_rgs['r723ggml'] = np.nan
            df_rgs['r723ggti'] = np.nan

    else:
        df_rgs = pd.DataFrame(columns=Smf72Rgs.__table__.columns.keys()).set_index(
            [col.name for col in Smf72Rgs.__table__.primary_key.columns.values()])
    return df_rgs


def build_rts(df: pd.DataFrame, df_wms_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for Response Time Distribution data section which will be uploaded to smf72_rts table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_wms_idx: The index of th Wms dataframe.

    Returns:
        The dataframe for the Response Time Distribution data section.
    """
    check_list_of_list = np.vectorize(is_list_of_list)
    if 'r723rts' in df.columns:
        z = df[(df.index.get_level_values('smf_type') == '72.3')].reset_index()['r723rts'].to_frame()
        z.dropna(how='all', inplace=True)
        z['res'] = check_list_of_list(z['r723rts'])
        x = pd.DataFrame(z[z['res']]['r723rts'].to_list()).drop(columns=[0]).set_index(
            z[z['res']].index).stack().reset_index(name='r723rts').dropna()
        df_rts = pd.DataFrame(x['r723rts'].to_list(),
                              columns=['class_rt_bucket_1', 'class_rt_bucket_2', 'class_rt_bucket_3',
                                       'class_rt_bucket_4', 'class_rt_bucket_5', 'class_rt_bucket_6',
                                       'class_rt_bucket_7', 'class_rt_bucket_8', 'class_rt_bucket_9',
                                       'class_rt_bucket_10', 'class_rt_bucket_11', 'class_rt_bucket_12',
                                       'class_rt_bucket_13', 'class_rt_bucket_14']).set_index(df_wms_idx)
    else:
        df_rts = pd.DataFrame(columns=Smf72Rts.__table__.columns.keys()).set_index(
            [col.name for col in Smf72Rts.__table__.primary_key.columns.values()])
    return df_rts


def build_scs(df: pd.DataFrame, df_policy_idx: pd.Index, df_wms_idx: pd.Index,
              df_rts: pd.DataFrame) -> pd.DataFrame:
    """Build the dataframe for Service/report class period data section which will be uploaded to smf72_scs table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_policy_idx: The index of the policy dataframe.
        df_wms_idx: The index of th Wms dataframe.
        df_rts: The dataframe of response time distribution.

    Returns:
        The dataframe for the Service/report class period data section.
    """

    # inner function
    def min_performance_index(rts_idx, class_goal_type, execution_velocity, class_goal_value,
                              class_goal_percentile):
        try:
            rts = df_rts.loc[rts_idx]
            performance_index = cal_performance_index(class_goal_type, execution_velocity, class_goal_value,
                                                      class_goal_percentile, rts.class_rt_bucket_1,
                                                      rts.class_rt_bucket_2,
                                                      rts.class_rt_bucket_3, rts.class_rt_bucket_4,
                                                      rts.class_rt_bucket_5,
                                                      rts.class_rt_bucket_6, rts.class_rt_bucket_7,
                                                      rts.class_rt_bucket_8,
                                                      rts.class_rt_bucket_9, rts.class_rt_bucket_10,
                                                      rts.class_rt_bucket_11, rts.class_rt_bucket_12,
                                                      rts.class_rt_bucket_13, rts.class_rt_bucket_14)
        except KeyError:
            performance_index = cal_performance_index(class_goal_type, execution_velocity, class_goal_value,
                                                      class_goal_percentile, np.nan, np.nan, np.nan, np.nan, np.nan,
                                                      np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
                                                      np.nan)

        return performance_index

    cal_std_dev = np.vectorize(calculate_std_dev)
    cal_min_performance_index = np.vectorize(min_performance_index, otypes=[float])

    class_goal_dict = {'0x08': 'System Specified', '0x10': 'Discretionary',
                       '0x20': 'Execution Velocity', '0x40': 'Average Resp. Time',
                       '0x80': 'Percentile Resp. Time', '0x00': 'None'}
    if 'r723scs' in df.columns:
        df_scs = col_to_frame(df[df.index.get_level_values('smf_type') == '72.3'], 'r723scs', df_policy_idx).drop(
            columns=['smf72xnm', 'datetime', 'smf72ist', 'smf72iet', 'r723mnsp', 'r723cper', 'smf72sid']
        ).set_index(df_wms_idx).reset_index().set_index(
            [col.name for col in Smf72Scs.__table__.primary_key.columns.values()])
        df_scs2 = pd.DataFrame(index=df_scs.index)
        df_scs['date'] = df_scs.index.get_level_values('datetime')
        df_scs['date'] = df_scs['date'].dt.date
        df_scs['class_goal_type'] = df_scs['r723crgf'].map(class_goal_dict)
        df_scs['r723cadf'] = df_scs['r723cadf'].apply(lambda x: int(str(x), 16))
        df_scs['r723crtf'] = df_scs['r723crtf'].apply(lambda x: int(str(x), 16))
        df_scs['r723crgf'] = df_scs['r723crgf'].apply(lambda x: int(str(x), 16))
        df_scs['r723crs1'] = df_scs['r723crs1'].apply(lambda x: int(str(x), 16))
        df_scs['is_heterogeneous'] = df_scs['r723crs1'].apply(lambda x: is_bit_set(x, 8, 0))
        df_scs['r723ceda'] = df_scs['r723cadf'].apply(lambda x: is_bit_set(x, 8, 2))
        df_scs['r723crta'] = df_scs['r723cadf'].apply(lambda x: is_bit_set(x, 8, 1))
        df_scs['r723crca'] = df_scs['r723cadf'].apply(lambda x: is_bit_set(x, 8, 0))
        df_scs['response_time_millisec'] = df_scs['r723crtf'].apply(lambda x: is_bit_set(x, 8, 0))
        df_scs['response_time_seconds'] = df_scs['r723crtf'].apply(lambda x: is_bit_set(x, 8, 1))
        df_scs['response_time_minutes'] = df_scs['r723crtf'].apply(lambda x: is_bit_set(x, 8, 2))
        df_scs['response_time_hours'] = df_scs['r723crtf'].apply(lambda x: is_bit_set(x, 8, 3))
        df_scs['r723cstm'] = df_scs['r723crgf'].apply(lambda x: is_bit_set(x, 8, 4))
        df_scs['r723cdsc'] = df_scs['r723crgf'].apply(lambda x: is_bit_set(x, 8, 3))
        df_scs['r723cvel'] = df_scs['r723crgf'].apply(lambda x: is_bit_set(x, 8, 2))
        df_scs['r723cavg'] = df_scs['r723crgf'].apply(lambda x: is_bit_set(x, 8, 1))
        df_scs['r723cprc'] = df_scs['r723crgf'].apply(lambda x: is_bit_set(x, 8, 0))
        df_scs['sample_crypto_using'] = df_scs['r723apu']
        df_scs2['sample_rate'] = 1 / df_scs['r723mtvl']
        df_scs2['tcbtime_insec'] = df_scs['r723ccpu'] * df_scs['r723madj'] / (
                16e6 * df_scs['r723mcpu'])
        df_scs2['srbtime_insec'] = df_scs['r723csrb'] * df_scs['r723madj'] / (
                16e6 * df_scs['r723msrb'])
        df_scs['r723cprs'] = df_scs['r723cprs'] * 1024 / 1e6
        df_scs['storage_total_swapped_in'] = df_scs['r723cprs'] / df_scs['smf72int']
        df_scs['r723cers'] = df_scs['r723cers'] * 1024 / 1e6
        df_scs['r723ctrr'] = df_scs['r723ctrr'] * 1024 / 1e6
        df_scs['r723ctat'] = df_scs['r723ctat'] * 1024 / 1e6
        df_scs['transaction_average_active'] = df_scs['r723ctat'] / df_scs['smf72int']
        df_scs['r723crct'] = df_scs['r723crct'] / 1e6
        df_scs['r723ciit'] = df_scs['r723ciit'] / 1e6
        df_scs['r723chst'] = df_scs['r723chst'] / 1e6
        df_scs['utilization_total'] = (df_scs2['tcbtime_insec'] + df_scs2['srbtime_insec'] + df_scs['r723crct'] +
                                       df_scs['r723ciit'] + df_scs['r723chst']) / df_scs['smf72int']
        df_scs['transaction_total_per_second'] = df_scs['r723crcp'] / df_scs['smf72int']
        df_scs['transaction_executed_per_second'] = df_scs['r723cncp'] / df_scs['smf72int']
        df_scs['r723ctet'] = df_scs['r723ctet'] * 1024 / 1e6
        df_scs['r723cets'] = df_scs['r723cets'] * 1024
        df_scs['sample_storage_delay'] = (df_scs['r723capr'] + df_scs['r723caco'] +
                                          df_scs['r723caxm'] + df_scs['r723cvio'] +
                                          df_scs['r723chsp'] + df_scs['r723cchs'])
        df_scs['transaction_address_space_percentage'] = df_scs['r723csac'] / df_scs[
            'r723mtv_']
        df_scs['r723csrs'] = df_scs['r723csrs'] * 1024 / 1e6
        df_scs['r723cict'] = df_scs['r723cict'] * 128 / 1e6
        df_scs['r723ciwt'] = df_scs['r723ciwt'] * 128 / 1e6
        df_scs['r723cidt'] = df_scs['r723cidt'] * 128 / 1e6
        df_scs['sample_server_delay'] = (
                df_scs['r723cspv'] + df_scs['r723csvi'] +
                df_scs['r723cshs'] + df_scs['r723csmp'] +
                df_scs['r723cssw'])
        df_scs['r723ciot'] = df_scs['r723ciot'] * 128 / 1e6
        df_scs['r723ciea'] = df_scs['r723ciea'] * 1024 / 1e6
        df_scs['transaction_enclave_average'] = df_scs['r723ciea'] / df_scs['smf72int']
        df_scs['r723cxea'] = df_scs['r723cxea'] * 1024 / 1e6
        df_scs['r723cfea'] = df_scs['r723cfea'] * 1024 / 1e6
        df_scs2['foreign_enclave_average'] = df_scs['r723cfea'] / df_scs['smf72int']
        df_scs2['export_enclave_average'] = df_scs['r723cxea'] / df_scs['smf72int']
        df_scs2['sample_crypto_delay'] = df_scs['r723fqd'] + df_scs['r723apd']
        df_scs['r723ectc'] = df_scs['r723ectc'] * 1024 / 1e6
        df_scs2['utilization_zaap'] = df_scs['r723cifa'] * df_scs['r723nffi'] / 256 / \
                                      df_scs['smf72int']
        df_scs2['utilization_zaap_on_cp'] = df_scs['r723cifc'] / df_scs['smf72int']
        df_scs2['utilization_ziip'] = df_scs['r723csup'] * df_scs['r723nffs'] / 256 / \
                                      df_scs['smf72int']
        df_scs2['utilization_ziip_on_cp'] = df_scs['r723csuc'] / df_scs['smf72int']
        df_scs['r723tpdp'] = df_scs['r723tpdp'] * 1024 / 1e6
        df_scs['r723cpdp'] = df_scs['r723cpdp'] * 1024 / 1e6
        df_scs['r723lpdp'] = df_scs['r723lpdp'] * 1024 / 1e6
        df_scs['r723spdp'] = df_scs['r723spdp'] * 1024 / 1e6
        df_scs2['performance_index'] = 0.0
        df_scs2['aaptime_insec'] = df_scs['r723cifa'] * df_scs['r723madj'] / (16e6 * df_scs['r723mcpu'])
        df_scs2['iiptime_insec'] = df_scs['r723csup'] * df_scs['r723madj'] / (16e6 * df_scs['r723mcpu'])
        df_scs2['su_sec'] = ((df_scs['r723ccpu'] - df_scs['r723csup'] - df_scs['r723cifa']
                              ) / df_scs['r723mcpu'] + (df_scs['r723csrb'] / df_scs['r723msrb'])
                             ) / df_scs['smf72int']
        df_scs2['cpu_time'] = ((df_scs['r723ccpu'] - df_scs['r723csup'] - df_scs['r723cifa'])
                               / df_scs['cpu_service_coefficient_adjusted'] + (df_scs['r723csrb']
                                                                               / df_scs[
                                                                                   'srb_service_coefficient_adjusted']))
        df_scs2['msu_physical'] = np.where(df_scs['r723cpa_scaling_factor'] is not None,
                                           df_scs2['cpu_time'] * 16 * df_scs['r723cpa_scaling_factor'] / df_scs[
                                               'r723cpa_actual'] * 3600 / df_scs['smf72int'],
                                           np.nan)
        df_scs2['num_of_cps'] = df_scs2['cpu_time'] / df_scs['smf72int']
        df_scs2['memory_usage'] = df_scs['r723cprs'] * 4096 / df_scs['smf72int']
        df_scs2['absorption_rate'] = np.where(df_scs['r723ctrr'] > 0,
                                              df_scs['r723csrv'] / df_scs['r723ctrr'], 0)
        df_scs['r723rtdt'] = pd.to_datetime(df_scs['r723rtdt'], format='%Y-%m-%d %H:%M:%S.%f', errors='coerce')
        df_scs2['single_page_in_rate'] = np.where((df_scs['r723ctrr'] - df_scs['r723ciea']) > 0,
                                                  df_scs['r723cpir'] / (df_scs['r723ctrr'] - df_scs[
                                                      'r723ciea']), 0)
        df_scs2['block_page_in_rate'] = np.where((df_scs['r723ctrr'] - df_scs['r723ciea']) > 0,
                                                 df_scs['r723cbpi'] / (df_scs['r723ctrr'] - df_scs[
                                                     'r723ciea']), 0)
        df_scs2['shared_page_in_rate'] = np.where((df_scs['r723ctrr'] - df_scs['r723ciea']) > 0,
                                                  df_scs['r723cspa'] / (df_scs['r723ctrr'] - df_scs[
                                                      'r723ciea']), 0)
        df_scs2['hsp_page_in_rate'] = np.where((df_scs['r723ctrr'] - df_scs['r723ciea']) > 0,
                                               df_scs['r723chpi'] / (df_scs['r723ctrr'] - df_scs[
                                                   'r723ciea']), 0)
        df_scs2['transaction_service_rate'] = np.where(df_scs['r723ctat'] > 0,
                                                       df_scs['r723csrv'] / df_scs['r723ctat'],
                                                       0)
        df_scs2['appl_percentage_cp_time'] = (df_scs2['tcbtime_insec'] + df_scs2['srbtime_insec'] + df_scs['r723crct'] +
                                              df_scs['r723ciit'] + df_scs['r723chst'] -
                                              (df_scs2['aaptime_insec'] * df_scs['r723nffi'] / 256) -
                                              (df_scs2['iiptime_insec'] * df_scs[
                                                  'r723nffs'] / 256)) / (
                                                     df_scs['smf72int'] * (df_scs['r723mcf'] / 1024)) * 100
        df_scs2['appl_percentage_iipcp_time'] = ((df_scs['r723csuc'] * df_scs['r723madj']) / (
                16e6 * df_scs['r723mcpu'])) / (
                                                        df_scs['smf72int'] * (df_scs['r723mcf'] / 1024)) * 100
        df_scs2['appl_percentage_iip_time'] = df_scs2['iiptime_insec'] / (
                df_scs['smf72int'] * (df_scs['r723mcfs'] / 1024)) * 100
        df_scs2['appl_percentage_aapcp_time'] = ((df_scs['r723cifc'] * df_scs['r723madj']) / (
                16e6 * df_scs['r723mcpu'])) / (
                                                        df_scs['smf72int'] * (df_scs['r723mcf'] / 1024)) * 100
        df_scs2['appl_percentage_aap_time'] = np.where(df_scs['r723mcfi'] > 0,
                                                       df_scs2['aaptime_insec'] / (df_scs['smf72int'] * (
                                                               df_scs['r723mcfi'] / 1024)) * 100, 0)
        df_scs2['start_subchannel_rate'] = df_scs['r723circ'] / df_scs['smf72int']
        df_scs2['avg_dasd_response_time'] = np.where(df_scs['r723circ'] > 0,
                                                     (df_scs['r723cict'] + df_scs['r723ciwt'] + df_scs['r723cidt'] +
                                                      df_scs['r723ciot']
                                                      ) / df_scs['r723circ'], 0)
        df_scs2['avg_dasd_connect_time'] = np.where(df_scs['r723circ'] > 0,
                                                    df_scs['r723cict'] / df_scs['r723circ'], 0)
        df_scs2['avg_dasd_disconnect_time'] = np.where(df_scs['r723circ'] > 0,
                                                       df_scs['r723cidt'] / df_scs['r723circ'], 0)
        df_scs2['avg_dasd_pending_time'] = np.where(df_scs['r723circ'] > 0,
                                                    df_scs['r723ciwt'] / df_scs['r723circ'], 0)
        df_scs2['avg_dasd_ios_queue_time'] = np.where(df_scs['r723circ'] > 0,
                                                      df_scs['r723ciot'] / df_scs['r723circ'], 0)
        if 'r723ctetx' in df_scs.columns:
            df_scs['r723ctetx'] = df_scs['r723ctetx']
            df_scs['r723cxetx'] = df_scs['r723cxetx'] / 1e6
            df_scs['r723cqdtx'] = df_scs['r723cqdtx'] / 1e6
            df_scs['r723cadtx'] = df_scs['r723cadtx'] / 1e6
            df_scs['r723ccvtx '] = df_scs['r723ccvtx'] / 1e6
            df_scs['r723ciqtx'] = df_scs['r723ciqtx'] / 1e6
            df_scs['r723ctet'] = df_scs['r723ctetx'] / 1e6
            df_scs['r723cets'] = df_scs['r723cetsx']

        df_scs2['transaction_average_swapped_in'] = df_scs['r723ctrr'] / df_scs['smf72int']

        df_scs2['transaction_total_percentage_cp_time'] = ((df_scs['r723tsucp'] * df_scs['r723madj']) / (
                16e6 * df_scs['r723mcpu'])) / (df_scs['smf72int'] * (df_scs['r723mcf'] / 1024)) * 100
        df_scs2['transaction_total_percentage_sp_time'] = ((df_scs['r723tsusp'] * df_scs['r723madj']) / (
                16e6 * df_scs['r723mcpu'])) / (df_scs['smf72int'] * (df_scs['r723mcfs'] / 1024)) * 100
        df_scs2['transaction_total_percentage_sp_on_cp_time'] = ((df_scs['r723tsuocp'] * df_scs['r723madj']) / (
                16e6 * df_scs['r723mcpu'])) / (df_scs['smf72int'] * (df_scs['r723mcf'] / 1024)) * 100
        df_scs2['transaction_mobile_percentage_cp_time'] = ((df_scs['r723msucp'] * df_scs['r723madj']) / (
                16e6 * df_scs['r723mcpu'])) / (df_scs['smf72int'] * (df_scs['r723mcf'] / 1024)) * 100
        df_scs2['transaction_mobile_percentage_sp_time'] = ((df_scs['r723msusp'] * df_scs['r723madj']) / (
                16e6 * df_scs['r723mcpu'])) / (df_scs['smf72int'] * (df_scs['r723mcfs'] / 1024)) * 100
        df_scs2['transaction_mobile_percentage_sp_on_cp_time'] = ((df_scs['r723msuocp'] * df_scs['r723madj']) / (
                16e6 * df_scs['r723mcpu'])) / (df_scs['smf72int'] * (df_scs['r723mcf'] / 1024)) * 100
        df_scs2['transaction_cata_percentage_cp_time'] = ((df_scs['r723asucp'] * df_scs['r723madj']) / (
                16e6 * df_scs['r723mcpu'])) / (df_scs['smf72int'] * (df_scs['r723mcf'] / 1024)) * 100
        df_scs2['transaction_cata_percentage_sp_time'] = ((df_scs['r723asusp'] * df_scs['r723madj']) / (
                16e6 * df_scs['r723mcpu'])) / (df_scs['smf72int'] * (df_scs['r723mcfs'] / 1024)) * 100
        df_scs2['transaction_cata_percentage_sp_on_cp_time'] = ((df_scs['r723asuocp'] * df_scs['r723madj']) / (
                16e6 * df_scs['r723mcpu'])) / (df_scs['smf72int'] * (df_scs['r723mcf'] / 1024)) * 100
        df_scs2['transaction_catb_percentage_cp_time'] = ((df_scs['r723bsucp'] * df_scs['r723madj']) / (
                16e6 * df_scs['r723mcpu'])) / (df_scs['smf72int'] * (df_scs['r723mcf'] / 1024)) * 100
        df_scs2['transaction_catb_percentage_sp_time'] = ((df_scs['r723bsusp'] * df_scs['r723madj']) / (
                16e6 * df_scs['r723mcpu'])) / (df_scs['smf72int'] * (df_scs['r723mcfs'] / 1024)) * 100
        df_scs2['transaction_catb_percentage_sp_on_cp_time'] = ((df_scs['r723bsuocp'] * df_scs['r723madj']) / (
                16e6 * df_scs['r723mcpu'])) / (df_scs['smf72int'] * (df_scs['r723mcf'] / 1024)) * 100
        if 'r723ctetx' in df_scs.columns:
            df_scs2['transaction_execution_time'] = df_scs['r723cxetx']
            df_scs2['transaction_queue_delay_time'] = df_scs['r723cqdtx']
            df_scs2['transaction_aff_delay_time'] = df_scs['r723cadtx']
            df_scs2['transaction_inel_delay_time'] = df_scs['r723ciqtx']
            df_scs2['transaction_jcl_time'] = df_scs['r723ccvtx']
        else:
            df_scs2['transaction_execution_time'] = df_scs['r723cxet'] * 1024 / 1e6
            df_scs2['transaction_queue_delay_time'] = df_scs['r723cqdt'] * 1024 / 1e6
            df_scs2['transaction_aff_delay_time'] = df_scs['r723cadt'] * 1024 / 1e6
            df_scs2['transaction_inel_delay_time'] = df_scs['r723ciqt'] * 1024
            df_scs2['transaction_jcl_time'] = df_scs['r723ccvt'] * 1024 / 1e6

        df_scs2['swaps_per_transaction'] = np.where(df_scs['r723crcp'] > 0,
                                                    df_scs['r723cswc'] / df_scs['r723crcp'], 0)
        df_scs2['transaction_response_time_mean'] = np.where(df_scs['r723crcp'] > 0,
                                                             df_scs['r723ctet'] / df_scs[
                                                                 'r723crcp'], 0)
        df_scs2['transaction_execution_time_mean'] = np.where(df_scs['r723crcp'] > 0,
                                                              df_scs2['transaction_execution_time'] / df_scs[
                                                                  'r723crcp'], 0)
        df_scs2['transaction_queue_delay_time_mean'] = np.where(df_scs['r723crcp'] > 0,
                                                                df_scs2['transaction_queue_delay_time'] / df_scs[
                                                                    'r723crcp'], 0)
        df_scs2['transaction_aff_delay_time_mean'] = np.where(df_scs['r723crcp'] > 0,
                                                              df_scs2['transaction_aff_delay_time'] / df_scs[
                                                                  'r723crcp'], 0)
        df_scs2['transaction_jcl_time_mean'] = np.where(df_scs['r723crcp'] > 0,
                                                        df_scs2['transaction_jcl_time'] / df_scs[
                                                            'r723crcp'], 0)
        df_scs2['transaction_inel_delay_time_mean'] = np.where(df_scs['r723crcp'] > 0,
                                                               df_scs2['transaction_inel_delay_time'] / df_scs[
                                                                   'r723crcp'], 0)
        df_scs2['transaction_execution_time'] = np.where(df_scs['r723crcp'] > 0,
                                                         df_scs2['transaction_execution_time'], 0)
        df_scs2['transaction_queue_delay_time'] = np.where(df_scs['r723crcp'] > 0,
                                                           df_scs2['transaction_queue_delay_time'], 0)
        df_scs2['transaction_aff_delay_time'] = np.where(df_scs['r723crcp'] > 0,
                                                         df_scs2['transaction_aff_delay_time'], 0)
        df_scs2['transaction_inel_delay_time'] = np.where(df_scs['r723crcp'] > 0,
                                                          df_scs2['transaction_inel_delay_time'], 0)
        df_scs2['transaction_jcl_time'] = np.where(df_scs['r723crcp'] > 0,
                                                   df_scs2['transaction_jcl_time'], 0)
        df_scs2['swaps_per_transaction'] = np.where(df_scs['r723crcp'] > 0,
                                                    df_scs2['swaps_per_transaction'], 0)
        df_scs2['execution_velocity'] = np.where((df_scs['r723ctou'] + df_scs['r723ctot']) > 0,
                                                 df_scs['r723ctou'] * 100 / (df_scs['r723ctou'] + df_scs['r723ctot']),
                                                 0)
        df_scs['utilization_cp'] = df_scs['utilization_total'] - df_scs2['utilization_ziip'] - df_scs2[
            'utilization_zaap']
        if 'r723ctetx' in df_scs.columns:
            df_scs2['transaction_average_elapsed_time_std_dev'] = cal_std_dev(df_scs['r723crcp'],
                                                                              df_scs['r723cetsx'], df_scs['r723ctetx'],
                                                                              1e6)
        else:
            df_scs2['transaction_average_elapsed_time_std_dev'] = cal_std_dev(df_scs['r723crcp'],
                                                                              df_scs['r723cets'],
                                                                              df_scs['r723ctet'],
                                                                              1e6)

        df_scs = pd.concat([df_scs, df_scs2], axis=1)
        df_scs['performance_index'] = cal_min_performance_index(df_scs.index,
                                                                df_scs['class_goal_type'], df_scs['execution_velocity'],
                                                                df_scs['r723cval'], df_scs['r723cpct'])
    else:
        df_scs = pd.DataFrame(columns=Smf72Scs.__table__.columns.keys()).set_index(
            [col.name for col in Smf72Scs.__table__.primary_key.columns.values()])

    return df_scs


def build_dns(df: pd.DataFrame, df_policy_idx: pd.Index, df_wrs: pd.DataFrame) -> pd.DataFrame:
    """Build the dataframe for the Resource Delay Type Names section which will be uploaded to smf72_dns table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_policy_idx: The index of the policy dataframe.
        df_wrs: The dataframe of work manager/resource manager state section.

    Returns:
        The dataframe for the Service/report class period data section.
    """

    def _wrs_rwxx(wrs_idx, rw_col):
        try:
            wrs = df_wrs.loc[wrs_idx]
            return int(wrs[rw_col])
        except KeyError:
            return np.nan

    get_wrs_rwxx = np.vectorize(_wrs_rwxx, otypes=[object])
    if 'r723dns' in df.columns:
        z = df[(df.index.get_level_values('smf_type') == '72.3')].reset_index()['r723dns'].to_frame().set_index(
            df_policy_idx)
        z.dropna(how='all', inplace=True)
        x = z.explode('r723dns').reset_index()
        x['dns_idx'] = x.groupby(['smf72xnm', 'datetime', 'smf72ist', 'smf72iet', 'r723mnsp', 'r723mwnm', 'r723mcnm', 'smf72sid']).cumcount() + 1
        x.set_index(
            ['smf72xnm', 'datetime', 'smf72ist', 'smf72iet', 'r723mnsp', 'r723mwnm', 'r723mcnm', 'smf72sid', 'dns_idx'],
            inplace=True)
        df_x = pd.json_normalize(x['r723dns']).set_index(x.index)  # .reset_index()
        df_dns = df_wrs[df_wrs['r723rdnn'] > 0].reset_index().set_index(
            ['smf72xnm', 'datetime', 'smf72ist', 'smf72iet', 'r723mnsp', 'r723mwnm', 'r723mcnm', 'r723cper', 'smf72sid',
             'r723rtyp', 'phase'])[['r723rdnx', 'r723rdnn']]
        df_dns = df_dns.reindex(df_dns.index.repeat(df_dns.r723rdnn))
        df_dns['dns_idx'] = df_dns.groupby(
            ['smf72xnm', 'datetime', 'smf72ist', 'smf72iet', 'r723mnsp', 'r723mwnm', 'r723mcnm', 'r723cper',
             'smf72sid', 'r723rtyp', 'phase']).cumcount() + df_dns['r723rdnx']
        df_dns = df_dns.reset_index().set_index(
            ['smf72xnm', 'datetime', 'smf72ist', 'smf72iet', 'r723mnsp', 'r723mwnm', 'r723mcnm', 'smf72sid', 'dns_idx'])
        df_dns = df_dns.join(df_x)
        df_dns['r723dnuu'] = df_dns['r723dnnu'].astype('str')
        df_dns['r723rwnn'] = 'r723rw' + df_dns['r723dnuu'].str.zfill(2)
        df_dns = df_dns.reset_index().set_index(
            ['smf72xnm', 'datetime', 'smf72ist', 'smf72iet', 'r723mnsp', 'r723mwnm', 'r723mcnm', 'r723cper',
             'smf72sid', 'r723rtyp', 'phase'])
        df_dns['r723rwnn'] = get_wrs_rwxx(df_dns.index, df_dns['r723dnuu'])
        df_dns = df_dns.drop(columns=['dns_idx', 'r723rdnx', 'r723rdnn', 'r723dnuu']).reset_index().set_index(
            [col.name for col in Smf72Dns.__table__.primary_key.columns.values()])
    else:
        df_dns = pd.DataFrame(columns=Smf72Dns.__table__.columns.keys()).set_index(
            [col.name for col in Smf72Dns.__table__.primary_key.columns.values()])
    return df_dns


def build_dnsx(df: pd.DataFrame, df_dns: pd.DataFrame, current_time: dt.datetime) -> pd.DataFrame:
    """Build the dataframe for the Resource Delay Type Names section for sysplex level which will be uploaded to smf72_dnsx table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_dns: The dataframe of Resource Delay Type Names section.
        current_time: The current timestamp.

    Returns:
        The dataframe for the Resource Delay Type Names section for sysplex level.
    """
    if 'r723dns' in df.columns:
        df_dnsx = df_dns.reset_index().set_index(
            [col.name for col in Smf72Dnsx.__table__.primary_key.columns.values()])
        df_dnsx['last_update_time'] = current_time
    else:
        df_dnsx = pd.DataFrame(columns=Smf72Dnsx.__table__.columns.keys()).set_index(
            [col.name for col in Smf72Dnsx.__table__.primary_key.columns.values()])
    return df_dnsx


def build_wrs(df: pd.DataFrame, df_policy_idx: pd.Index, df_scs_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for the Work Manager/Resource Manager State section which will be uploaded to smf72_wrs table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_policy_idx: The index of the policy dataframe.
        df_scs_idx: The index of the Service/report class period data section dataframe.

    Returns:
        The dataframe for the Work Manager/Resource Manager State section.
    """
    if 'r723wrs' in df.columns:
        df_wrs = col_to_frame(df[df.index.get_level_values('smf_type') == '72.3'], 'r723wrs', df_policy_idx).drop(
            columns=['smf72xnm', 'datetime', 'smf72ist', 'smf72iet', 'r723mnsp', 'smf72sid']).set_index(df_scs_idx)
        df_wrs['r723rflg'] = df_wrs['r723rflg'].apply(lambda x: int(str(x), 16))
        df_wrs['r723rexe'] = df_wrs['r723rflg'].apply(lambda x: is_bit_set(x, 8, 1))
        df_wrs['r723rdbe'] = df_wrs['r723rflg'].apply(lambda x: is_bit_set(x, 8, 0))
        df_wrs['phase'] = np.where(df_wrs['r723rdbe'], 'BTE',
                                   np.where(df_wrs['r723rdbe'], 'EXE', '???'))

        df_wrs = df_wrs.reset_index().set_index(
            [col.name for col in Smf72Wrs.__table__.primary_key.columns.values()])
    else:
        df_wrs = pd.DataFrame(columns=Smf72Wrs.__table__.columns.keys()).set_index(
            [col.name for col in Smf72Wrs.__table__.primary_key.columns.values()])

    return df_wrs


def build_wrsx(df: pd.DataFrame, df_wrs: pd.DataFrame, current_time: dt.datetime) -> pd.DataFrame:
    """Build the dataframe for the Work Manager/Resource Manager State section for sysplex level which will be uploaded to smf72_wrsx table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_wrs: The dataaframe for the Work Manager/Resource Manager State Section.
        current_time: The current timestamp.

    Returns:
        The dataframe for the Work Manager/Resource Manager State section for sysplex level.
    """
    if 'r723wrs' in df.columns:
        df_wrsx = df_wrs.reset_index().set_index(
            [col.name for col in Smf72Wrsx.__table__.primary_key.columns.values()])
        df_wrsx['last_update_time'] = current_time
    else:
        df_wrsx = pd.DataFrame(columns=Smf72Wrsx.__table__.columns.keys()).set_index(
            [col.name for col in Smf72Wrsx.__table__.primary_key.columns.values()])
    return df_wrsx


def build_data(df: pd.DataFrame, df_pro_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for the Service Class Period Data section which will be uploaded to smf72_data table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_pro_idx: The index of the RMF product section dataframe.

    Returns:
        The dataframe for the Service Class Period Data section.
    """
    if 'r724data' in df.columns:
        df_data = cols_to_frame(df[df.index.get_level_values('smf_type') == '72.4'], ['r724data', 'r724swre'],
                                df_pro_idx
                                ).set_index([col.name for col in Smf72Data.__table__.primary_key.columns.values()])
        df_data['r724ptm'] = pd.to_datetime(df_data['r724ptm'], errors='coerce')
        if 'r724etx' not in df_data.columns:
            df_data['r724etx'] = np.nan
            df_data['r724qtx'] = np.nan
            df_data['r724or7a'] = np.nan
    else:
        df_data = pd.DataFrame(columns=Smf72Data.__table__.columns.keys()).set_index(
            [col.name for col in Smf72Data.__table__.primary_key.columns.values()])
    return df_data


def build_sctl(df: pd.DataFrame, df_pro_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for the Serialization Control section which will be uploaded to smf72_sctl table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_pro_idx: The index of the RMF product section dataframe.

    Returns:
        The dataframe for the Serialization Control section.
    """
    convert_2_int = np.vectorize(to_int)
    if 'r725sctl' in df.columns:
        df_sctl = col_to_frame(df[df.index.get_level_values('smf_type') == '72.5'], 'r725sctl', df_pro_idx).set_index(
            [col.name for col in Smf72Sctl.__table__.primary_key.columns.values()])
        df_sctl['r725sgmo'] = convert_2_int(df_sctl['r725sgmo'])
        df_sctl['r725scmt'] = pd.to_timedelta(df_sctl['r725scmt']) / np.timedelta64(1, 's')
        df_sctl['r725sedt'] = pd.to_timedelta(df_sctl['r725sedt']) / np.timedelta64(1, 's')
        df_sctl['r725slat'] = pd.to_timedelta(df_sctl['r725slat']) / np.timedelta64(1, 's')
        df_sctl['r725ssmt'] = pd.to_timedelta(df_sctl['r725ssmt']) / np.timedelta64(1, 's')
        df_sctl['r725slot'] = pd.to_timedelta(df_sctl['r725slot']) / np.timedelta64(1, 's')
        df_sctl['r725sclt'] = pd.to_timedelta(df_sctl['r725sclt']) / np.timedelta64(1, 's')
        df_sctl['r725slrt'] = pd.to_timedelta(df_sctl['r725slrt']) / np.timedelta64(1, 's')
        df_sctl['r725slrq'] = convert_2_int(df_sctl['r725slrq']) / 1000000
        df_sctl['r725sstt'] = pd.to_timedelta(df_sctl['r725sstt']) / np.timedelta64(1, 's')
        df_sctl['r725sstq'] = convert_2_int(df_sctl['r725sstq']) / 1000000
        df_sctl['r725ssyt'] = pd.to_timedelta(df_sctl['r725ssyt']) / np.timedelta64(1, 's')
        df_sctl['r725ssyq'] = convert_2_int(df_sctl['r725ssyq']) / 1000000
        df_sctl['r725ssst'] = pd.to_timedelta(df_sctl['r725ssst']) / np.timedelta64(1, 's')
        df_sctl['r725sssq'] = convert_2_int(df_sctl['r725sssq']) / 1000000

    else:
        df_sctl = pd.DataFrame(columns=Smf72Sctl.__table__.columns.keys()).set_index(
            [col.name for col in Smf72Sctl.__table__.primary_key.columns.values()])
    return df_sctl


def build_cmss(df: pd.DataFrame, df_pro_idx: pd.Index):
    """Build the dataframe for the CMS Lock Data section which will be uploaded to smf72_cmss table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_pro_idx: The index of the RMF product section dataframe.

    Returns:
        The dataframe for the CMS Lock Data section.
    """
    if 'r725cmss' in df.columns:
        df_cmss = col_to_frame(df[df.index.get_level_values('smf_type') == '72.5'], 'r725cmss', df_pro_idx)
        df_cmss['r725cmas'] = df_cmss['r725cmas'].str[2:]
        df_cmss['r725cmti'] = pd.to_timedelta(df_cmss['r725cmti']) / np.timedelta64(1, 's')
        df_cmss.set_index([col.name for col in Smf72Cmss.__table__.primary_key.columns.values()], inplace=True)
    else:
        df_cmss = pd.DataFrame(columns=Smf72Cmss.__table__.columns.keys()).set_index(
            [col.name for col in Smf72Cmss.__table__.primary_key.columns.values()])
    return df_cmss


def build_ceds(df: pd.DataFrame, df_pro_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for the CMS Enqueue/Dequeue Lock Data section which will be uploaded to smf72_ceds table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_pro_idx: The index of the RMF product section dataframe.

    Returns:
        The dataframe for the CMS Enqueue/Dequeue Lock Data section.
    """
    if 'r725ceds' in df.columns:
        df_ceds = col_to_frame(df[df.index.get_level_values('smf_type') == '72.5'], 'r725ceds', df_pro_idx)
        df_ceds['r725cmas'] = df_ceds['r725cmas'].str[2:]
        df_ceds['r725cmti'] = pd.to_timedelta(df_ceds['r725cmti']) / np.timedelta64(1, 's')
        df_ceds.set_index([col.name for col in Smf72Ceds.__table__.primary_key.columns.values()], inplace=True)
    else:
        df_ceds = pd.DataFrame(columns=Smf72Ceds.__table__.columns.keys()).set_index(
            [col.name for col in Smf72Ceds.__table__.primary_key.columns.values()])
    return df_ceds


def build_clas(df: pd.DataFrame, df_pro_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for the CMS Latch Lock Data section which will be uploaded to smf72_clas table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_pro_idx: The index of the RMF product section dataframe.

    Returns:
        The dataframe for the CMS Latch Lock Data section.
    """
    if 'r725clas' in df.columns:
        df_clas = col_to_frame(df[df.index.get_level_values('smf_type') == '72.5'], 'r725clas', df_pro_idx)
        df_clas['r725cmas'] = df_clas['r725cmas'].str[2:]
        df_clas['r725cmti'] = pd.to_timedelta(df_clas['r725cmti']) / np.timedelta64(1, 's')
        df_clas.set_index([col.name for col in Smf72Clas.__table__.primary_key.columns.values()], inplace=True)
    else:
        df_clas = pd.DataFrame(columns=Smf72Clas.__table__.columns.keys()).set_index(
            [col.name for col in Smf72Clas.__table__.primary_key.columns.values()])
    return df_clas


def build_csms(df: pd.DataFrame, df_pro_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for the CMS SMF Lock Data section which will be uploaded to smf72_csms table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_pro_idx: The index of the RMF product section dataframe.

    Returns:
        The dataframe for the CMS SMF Lock Data section.
    """
    if 'r725csms' in df.columns:
        df_csms = col_to_frame(df[df.index.get_level_values('smf_type') == '72.5'], 'r725csms', df_pro_idx)
        df_csms['r725cmas'] = df_csms['r725cmas'].str[2:]
        df_csms['r725cmti'] = pd.to_timedelta(df_csms['r725cmti']) / np.timedelta64(1, 's')
        df_csms.set_index([col.name for col in Smf72Csms.__table__.primary_key.columns.values()], inplace=True)
    else:
        df_csms = pd.DataFrame(columns=Smf72Csms.__table__.columns.keys()).set_index(
            [col.name for col in Smf72Csms.__table__.primary_key.columns.values()])
    return df_csms


def build_lotd(df: pd.DataFrame, df_pro_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for the Local Lock Data section which will be uploaded to smf72_lotd table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_pro_idx: The index of the RMF product section dataframe.

    Returns:
        The dataframe for the Local Lock Data section.
    """
    if 'r725lotd' in df.columns:
        df_lotd = col_to_frame(df[df.index.get_level_values('smf_type') == '72.5'], 'r725lotd', df_pro_idx)
        df_lotd['r725loas'] = df_lotd['r725loas'].str[2:]
        df_lotd['r725loti'] = pd.to_timedelta(df_lotd['r725loti']) / np.timedelta64(1, 's')
        df_lotd['r725lcti'] = pd.to_timedelta(df_lotd['r725lcti']) / np.timedelta64(1, 's')
        df_lotd.set_index([col.name for col in Smf72Lotd.__table__.primary_key.columns.values()], inplace=True)
    else:
        df_lotd = pd.DataFrame(columns=Smf72Lotd.__table__.columns.keys()).set_index(
            [col.name for col in Smf72Lotd.__table__.primary_key.columns.values()])
    return df_lotd


def build_clod(df: pd.DataFrame, df_pro_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for the CML Lock Owner Data section which will be uploaded to smf72_clod table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_pro_idx: The index of the RMF product section dataframe.

    Returns:
        The dataframe for the CML Lock Owner Data section.
    """
    if 'r725clod' in df.columns:
        df_clod = col_to_frame(df[df.index.get_level_values('smf_type') == '72.5'], 'r725clod', df_pro_idx)
        df_clod['r725coas'] = df_clod['r725coas'].str[2:]
        df_clod['r725coti'] = pd.to_timedelta(df_clod['r725coti']) / np.timedelta64(1, 's')
        df_clod['r725clti'] = pd.to_timedelta(df_clod['r725clti']) / np.timedelta64(1, 's')
        df_clod.set_index([col.name for col in Smf72Clod.__table__.primary_key.columns.values()], inplace=True)
    else:
        df_clod = pd.DataFrame(columns=Smf72Clod.__table__.columns.keys()).set_index(
            [col.name for col in Smf72Clod.__table__.primary_key.columns.values()])
    return df_clod


def build_clrd(df: pd.DataFrame, df_pro_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for the CML Lock Requestor Data section which will be uploaded to smf72_clrd table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_pro_idx: The index of the RMF product section dataframe.

    Returns:
        The dataframe for the CML Lock Requestor Data section.
    """
    if 'r725clrd' in df.columns:
        df_clrd = col_to_frame(df[df.index.get_level_values('smf_type') == '72.5'], 'r725clrd', df_pro_idx)
        df_clrd['r725cras'] = df_clrd['r725cras'].str[2:]
        df_clrd['r725crti'] = pd.to_timedelta(df_clrd['r725crti']) / np.timedelta64(1, 's')
        df_clrd.set_index([col.name for col in Smf72Clrd.__table__.primary_key.columns.values()], inplace=True)
    else:
        df_clrd = pd.DataFrame(columns=Smf72Clrd.__table__.columns.keys()).set_index(
            [col.name for col in Smf72Clrd.__table__.primary_key.columns.values()])
    return df_clrd


def build_lasc(df: pd.DataFrame, df_pro_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for the GRS Latch Set Creator Data Section which will be uploaded to smf72_lasc table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_pro_idx: The index of the RMF product section dataframe.

    Returns:
        The dataframe for the GRS Latch Set Creator Data section.
    """
    convert_2_int = np.vectorize(to_int)
    if 'r725lasc' in df.columns:
        df_lasc = col_to_frame(df[df.index.get_level_values('smf_type') == '72.5'], 'r725lasc', df_pro_idx)
        df_lasc['r725laas'] = df_lasc['r725laas'].str[2:]
        df_lasc['r725lati'] = pd.to_timedelta(df_lasc['r725lati']) / np.timedelta64(1, 's')
        df_lasc['r725lasq'] = convert_2_int(df_lasc['r725lasq']) / 1000000
        df_lasc.set_index([col.name for col in Smf72Lasc.__table__.primary_key.columns.values()], inplace=True)
    else:
        df_lasc = pd.DataFrame(columns=Smf72Lasc.__table__.columns.keys()).set_index(
            [col.name for col in Smf72Lasc.__table__.primary_key.columns.values()])
    return df_lasc


def build_lare(df: pd.DataFrame, df_pro_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for the GRS Latch Requestor Data Section which will be uploaded to smf72_lare table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_pro_idx: The index of the RMF product section dataframe.

    Returns:
        The dataframe for the GRS Latch Requestor Data section.
    """
    convert_2_int = np.vectorize(to_int)
    if 'r725lare' in df.columns:
        df_lare = col_to_frame(df[df.index.get_level_values('smf_type') == '72.5'], 'r725lare', df_pro_idx)
        df_lare['r725laas'] = df_lare['r725laas'].str[2:]
        df_lare['r725lati'] = pd.to_timedelta(df_lare['r725lati']) / np.timedelta64(1, 's')
        df_lare['r725lasq'] = convert_2_int(df_lare['r725lasq']) / 1000000
        df_lare.set_index([col.name for col in Smf72Lare.__table__.primary_key.columns.values()], inplace=True)
    else:
        df_lare = pd.DataFrame(columns=Smf72Lare.__table__.columns.keys()).set_index(
            [col.name for col in Smf72Lare.__table__.primary_key.columns.values()])
    return df_lare


def build_ense(df: pd.DataFrame, df_pro_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for the GRS Enqueue Step Data Section which will be uploaded to smf72_ense table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_pro_idx: The index of the RMF product section dataframe.

    Returns:
        The dataframe for the GRS Enqueue Step Data section.
    """
    convert_2_int = np.vectorize(to_int)
    if 'r725ense' in df.columns:
        df_ense = col_to_frame(df[df.index.get_level_values('smf_type') == '72.5'], 'r725ense', df_pro_idx)
        df_ense['r725enas'] = df_ense['r725enas'].str[2:]
        df_ense['r725enti'] = pd.to_timedelta(df_ense['r725enti']) / np.timedelta64(1, 's')
        df_ense['r725ensq'] = convert_2_int(df_ense['r725ensq']) / 1000000
        df_ense['ense_index'] = df_ense.groupby(
            ['smf72xnm', 'smf72sid', 'datetime', 'smf72ist', 'smf72iet', 'r725enst', 'r725enjn', 'r725ensn',
             'r725ensp', 'r725ensc']).cumcount()
        df_ense.set_index([col.name for col in Smf72Ense.__table__.primary_key.columns.values()], inplace=True)
    else:
        df_ense = pd.DataFrame(columns=Smf72Ense.__table__.columns.keys()).set_index(
            [col.name for col in Smf72Ense.__table__.primary_key.columns.values()])
    return df_ense


def build_ensy(df: pd.DataFrame, df_pro_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for the GRS Enqueue System Data Section which will be uploaded to smf72_ensy table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_pro_idx: The index of the RMF product section dataframe.

    Returns:
        The dataframe for the GRS Enqueue System Data section.
    """
    convert_2_int = np.vectorize(to_int)
    if 'r725ensy' in df.columns:
        df_ensy = col_to_frame(df[df.index.get_level_values('smf_type') == '72.5'], 'r725ensy', df_pro_idx)
        df_ensy['r725enas'] = df_ensy['r725enas'].str[2:]
        df_ensy['r725enti'] = pd.to_timedelta(df_ensy['r725enti']) / np.timedelta64(1, 's')
        df_ensy['r725ensq'] = convert_2_int(df_ensy['r725ensq']) / 1000000
        df_ensy['ensy_index'] = df_ensy.groupby(
            ['smf72xnm', 'smf72sid', 'datetime', 'smf72ist', 'smf72iet', 'r725enst', 'r725enjn', 'r725ensn',
             'r725ensp', 'r725ensc']).cumcount()
        df_ensy.set_index([col.name for col in Smf72Ensy.__table__.primary_key.columns.values()], inplace=True)
    else:
        df_ensy = pd.DataFrame(columns=Smf72Ensy.__table__.columns.keys()).set_index(
            [col.name for col in Smf72Ensy.__table__.primary_key.columns.values()])
    return df_ensy


def build_enss(df: pd.DataFrame, df_pro_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for the GRS Enqueue Systems Data Section which will be uploaded to smf72_enss table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_pro_idx: The index of the RMF product section dataframe.

    Returns:
        The dataframe for the GRS Enqueue Systems Data section.
    """
    convert_2_int = np.vectorize(to_int)
    if 'r725enss' in df.columns:
        df_enss = col_to_frame(df[df.index.get_level_values('smf_type') == '72.5'], 'r725enss', df_pro_idx)
        df_enss['r725enas'] = df_enss['r725enas'].str[2:]
        df_enss['r725enti'] = pd.to_timedelta(df_enss['r725enti']) / np.timedelta64(1, 's')
        df_enss['r725ensq'] = convert_2_int(df_enss['r725ensq']) / 1000000
        df_enss.set_index([col.name for col in Smf72Enss.__table__.primary_key.columns.values()], inplace=True)
    else:
        df_enss = pd.DataFrame(columns=Smf72Enss.__table__.columns.keys()).set_index(
            [col.name for col in Smf72Enss.__table__.primary_key.columns.values()])
    return df_enss


def build_qsad(df: pd.DataFrame, df_pro_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for the GRS QScan Statistics Data Section which will be uploaded to smf72_qsad table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_pro_idx: The index of the RMF product section dataframe.

    Returns:
        The dataframe for the GRS QScan Statistics Data section.
    """
    convert_2_int = np.vectorize(to_int)
    if 'r725qsad' in df.columns:
        df_qsad = col_to_frame(df[df.index.get_level_values('smf_type') == '72.5'], 'r725qsad', df_pro_idx)
        df_qsad['r725qsas'] = df_qsad['r725qsas'].str[2:]
        df_qsad['r725qsti'] = pd.to_timedelta(df_qsad['r725qsti']) / np.timedelta64(1, 's')
        df_qsad['r725qsrq'] = convert_2_int(df_qsad['r725qsrq']) / 1000000
        df_qsad['r725qstq'] = convert_2_int(df_qsad['r725qstq']) / 1000000
        df_qsad.set_index([col.name for col in Smf72Qsad.__table__.primary_key.columns.values()], inplace=True)
    else:
        df_qsad = pd.DataFrame(columns=Smf72Qsad.__table__.columns.keys()).set_index(
            [col.name for col in Smf72Qsad.__table__.primary_key.columns.values()])
    return df_qsad


def cal_performance_index(class_goal_type: str, execution_velocity: float, class_goal_value: int,
                          class_goal_percentile: int,
                          class_rt_bucket_1: Union[int, float], class_rt_bucket_2: Union[int, float],
                          class_rt_bucket_3: Union[int, float], class_rt_bucket_4: Union[int, float],
                          class_rt_bucket_5: Union[int, float], class_rt_bucket_6: Union[int, float],
                          class_rt_bucket_7: Union[int, float], class_rt_bucket_8: Union[int, float],
                          class_rt_bucket_9: Union[int, float], class_rt_bucket_10: Union[int, float],
                          class_rt_bucket_11: Union[int, float], class_rt_bucket_12: Union[int, float],
                          class_rt_bucket_13: Union[int, float], class_rt_bucket_14: Union[int, float]):
    """Calculate performance index.

    Args:
        class_goal_type: A string of response time goal type.
        execution_velocity: A float showing the execution velocity.
        class_goal_value: A integer indicating response time or execution velocity goal, or zero if discretionary or system goal. Units are defined in r723crtf.
        class_goal_percentile: A integer indicating goal percentile value (in percentage).
        class_rt_bucket_1: A integer of count of completed transactions with response time <= 50% of the goal.
        class_rt_bucket_2: A integer of count of completed transactions with response time > 50% of the goal and <= 60% of the goal.
        class_rt_bucket_3: A integer of count of completed transactions with response time > 60% of the goal and <= 70% of the goal.
        class_rt_bucket_4: A integer of count of completed transactions with response time > 70% of the goal and <= 80% of the goal.
        class_rt_bucket_5: A integer of count of completed transactions with response time > 80% of the goal and <= 90% of the goal.
        class_rt_bucket_6: A integer of count of completed transactions with response time > 90% of the goal and <= 100% of the goal.
        class_rt_bucket_7: A integer of count of completed transactions with response time > 100% of the goal and <= 110% of the goal.
        class_rt_bucket_8: A integer of count of completed transactions with response time > 110% of the goal and <= 120% of the goal.
        class_rt_bucket_9: A integer of count of completed transactions with response time > 120% of the goal and <= 130% of the goal.
        class_rt_bucket_10: A integer of count of completed transactions with response time > 130% of the goal and <= 140% of the goal.
        class_rt_bucket_11: A integer of count of completed transactions with response time > 140% of the goal and <= 150% of the goal.
        class_rt_bucket_12: A integer of count of completed transactions with response time > 150% of the goal and <= 200% of the goal.
        class_rt_bucket_13: A integer of count of completed transactions with response time > 200% of the goal and <= 400% of the goal.
        class_rt_bucket_14: A integer of count of completed transactions with response time > 400% of the goal.

    Returns:
        performance index.
    """
    performance_index = 0.0
    if class_goal_type in ('Percentile Resp. Time', 'Average Resp. Time'):
        if not pd.isna(class_rt_bucket_1):
            bucket_sum = class_rt_bucket_1 + class_rt_bucket_2 + class_rt_bucket_3 \
                         + class_rt_bucket_4 + class_rt_bucket_5 + class_rt_bucket_6 \
                         + class_rt_bucket_7 + class_rt_bucket_8 + class_rt_bucket_9 \
                         + class_rt_bucket_10 + class_rt_bucket_11 + class_rt_bucket_12 \
                         + class_rt_bucket_13 + class_rt_bucket_14
            if bucket_sum != 0:
                weighted_bucket_sum = 50 * class_rt_bucket_1 + 60 * class_rt_bucket_2 + \
                                      70 * class_rt_bucket_3 + 80 * class_rt_bucket_4 + 90 * class_rt_bucket_5 + \
                                      100 * class_rt_bucket_6 + 110 * class_rt_bucket_7 + 120 * class_rt_bucket_8 + \
                                      130 * class_rt_bucket_9 + 140 * class_rt_bucket_10 + 150 * class_rt_bucket_11 + \
                                      200 * class_rt_bucket_12 + 400 * class_rt_bucket_13 + 550 * class_rt_bucket_14
                bucket1 = (class_rt_bucket_1 / bucket_sum * 100) >= class_goal_percentile
                bucket2 = ((class_rt_bucket_2 + class_rt_bucket_1) / bucket_sum * 100
                           ) >= class_goal_percentile
                bucket3 = ((class_rt_bucket_3 + class_rt_bucket_2 + class_rt_bucket_1
                            ) / bucket_sum * 100) >= class_goal_percentile
                bucket4 = ((class_rt_bucket_4 + class_rt_bucket_3 + class_rt_bucket_2 +
                            class_rt_bucket_1) / bucket_sum * 100) >= class_goal_percentile
                bucket5 = ((class_rt_bucket_5 + class_rt_bucket_4 + class_rt_bucket_3 +
                            class_rt_bucket_2 + class_rt_bucket_1) / bucket_sum * 100
                           ) >= class_goal_percentile
                bucket6 = ((class_rt_bucket_6 + class_rt_bucket_5 + class_rt_bucket_4 +
                            class_rt_bucket_3 + class_rt_bucket_2 + class_rt_bucket_1
                            ) / bucket_sum * 100) >= class_goal_percentile
                bucket7 = ((class_rt_bucket_7 + class_rt_bucket_6 + class_rt_bucket_5 +
                            class_rt_bucket_4 + class_rt_bucket_3 + class_rt_bucket_2 +
                            class_rt_bucket_1) / bucket_sum * 100) >= class_goal_percentile
                bucket8 = ((class_rt_bucket_8 + class_rt_bucket_7 + class_rt_bucket_6 +
                            class_rt_bucket_5 + class_rt_bucket_4 + class_rt_bucket_3 +
                            class_rt_bucket_2 + class_rt_bucket_1) / bucket_sum * 100
                           ) >= class_goal_percentile
                bucket9 = ((class_rt_bucket_9 + class_rt_bucket_8 + class_rt_bucket_7 +
                            class_rt_bucket_6 + class_rt_bucket_5 + class_rt_bucket_4 +
                            class_rt_bucket_3 + class_rt_bucket_2 + class_rt_bucket_1
                            ) / bucket_sum * 100) >= class_goal_percentile
                bucket10 = ((class_rt_bucket_10 + class_rt_bucket_9 + class_rt_bucket_8 +
                             class_rt_bucket_7 + class_rt_bucket_6 + class_rt_bucket_5 +
                             class_rt_bucket_4 + class_rt_bucket_3 + class_rt_bucket_2 +
                             class_rt_bucket_1) / bucket_sum * 100) >= class_goal_percentile
                bucket11 = ((class_rt_bucket_11 + class_rt_bucket_10 + class_rt_bucket_9 +
                             class_rt_bucket_8 + class_rt_bucket_7 + class_rt_bucket_6 +
                             class_rt_bucket_5 + class_rt_bucket_4 + class_rt_bucket_3 +
                             class_rt_bucket_2 + class_rt_bucket_1) / bucket_sum * 100
                            ) >= class_goal_percentile
                bucket12 = ((class_rt_bucket_12 + class_rt_bucket_11 + class_rt_bucket_10 +
                             class_rt_bucket_9 + class_rt_bucket_8 + class_rt_bucket_7 +
                             class_rt_bucket_6 + class_rt_bucket_5 + class_rt_bucket_4 +
                             class_rt_bucket_3 + class_rt_bucket_2 + class_rt_bucket_1
                             ) / bucket_sum * 100) >= class_goal_percentile
                bucket13 = ((class_rt_bucket_13 + class_rt_bucket_12 + class_rt_bucket_11 +
                             class_rt_bucket_10 + class_rt_bucket_9 + class_rt_bucket_8 +
                             class_rt_bucket_7 + class_rt_bucket_6 + class_rt_bucket_5 +
                             class_rt_bucket_4 + class_rt_bucket_3 + class_rt_bucket_2 +
                             class_rt_bucket_1) / bucket_sum * 100) >= class_goal_percentile
                if class_goal_type == 'Percentile Resp. Time':
                    maxindex = pd.Series([13])
                    for bucket in [bucket1, bucket2, bucket3, bucket4, bucket5, bucket6, bucket7,
                                   bucket8, bucket9, bucket10, bucket11, bucket12, bucket13]:
                        maxindex = maxindex.subtract(int(bucket))
                    performance_index = (50 + maxindex.iloc[0] * 10 + ((maxindex.iloc[0] == 11) * 40
                                                                       ) + ((maxindex.iloc[0] == 12) * 230) + (
                                                 (maxindex.iloc[0] == 13) * 370)) / 100
                else:  # Average Resp. Time
                    performance_index = weighted_bucket_sum / bucket_sum
    if (class_goal_type == 'Execution Velocity') and (execution_velocity > 0):
        performance_index = class_goal_value / execution_velocity
    return performance_index


def agg_scs_group_by(df_scss: pd.DataFrame, group_by: list, interval_agg: str, r723ctetx_exist: bool) -> pd.DataFrame:
    cal_std_dev = np.vectorize(calculate_std_dev)
    if isinstance(interval_agg, str) and interval_agg == 'sum':
        agg_scs_x = agg_scs | {'smf72int': interval_agg}
        df_scs_gp = df_scss.groupby(group_by).agg(agg_scs_x)
        df_scs_gp = df_scs_gp.copy()
        df_scs_gp['tcbtime_insec'] = df_scs_gp['r723ccpu'] * df_scs_gp['r723madj'] / (16e6 * df_scs_gp['r723mcpu'])
        df_scs_gp['srbtime_insec'] = df_scs_gp['r723csrb'] * df_scs_gp['r723madj'] / (16e6 * df_scs_gp['r723msrb'])
        df_scs_gp['aaptime_insec'] = df_scs_gp['r723cifa'] * df_scs_gp['r723madj'] / (16e6 * df_scs_gp['r723mcpu'])
        df_scs_gp['iiptime_insec'] = df_scs_gp['r723csup'] * df_scs_gp['r723madj'] / (16e6 * df_scs_gp['r723mcpu'])
        df_scs_gp['appl_percentage_cp_time'] = (df_scs_gp['tcbtime_insec'] + df_scs_gp['srbtime_insec'] +
                                                df_scs_gp['r723crct'] + df_scs_gp['r723ciit'] + df_scs_gp['r723chst'] -
                                                (df_scs_gp['aaptime_insec'] * df_scs_gp['r723nffi'] / 256) -
                                                (df_scs_gp['iiptime_insec'] * df_scs_gp['r723nffs'] / 256)) / (
                                                       df_scs_gp['smf72int'] * (df_scs_gp['r723mcf'] / 1024)) * 100
        df_scs_gp['appl_percentage_iipcp_time'] = ((df_scs_gp['r723csuc'] * df_scs_gp['r723madj']) / (
                16e6 * df_scs_gp['r723mcpu'])) / (df_scs_gp['smf72int'] * (df_scs_gp['r723mcf'] / 1024)) * 100
        df_scs_gp['appl_percentage_iip_time'] = df_scs_gp['iiptime_insec'] / (
                df_scs_gp['smf72int'] * (df_scs_gp['r723mcfs'] / 1024)) * 100
        df_scs_gp['appl_percentage_aapcp_time'] = ((df_scs_gp['r723cifc'] * df_scs_gp['r723madj']) / (
                16e6 * df_scs_gp['r723mcpu'])) / (df_scs_gp['smf72int'] * (df_scs_gp['r723mcf'] / 1024)) * 100
        df_scs_gp['appl_percentage_aap_time'] = np.where(df_scs_gp['r723mcfi'] > 0,
                                                         df_scs_gp['aaptime_insec'] / (df_scs_gp['smf72int'] * (
                                                                 df_scs_gp['r723mcfi'] / 1024)) * 100, 0)
        df_scs_gp['transaction_total_percentage_cp_time'] = ((df_scs_gp['r723tsucp'] * df_scs_gp['r723madj']) / (
                16e6 * df_scs_gp['r723mcpu'])) / (df_scs_gp['smf72int'] * (df_scs_gp['r723mcf'] / 1024)) * 100
        df_scs_gp['transaction_total_percentage_sp_time'] = ((df_scs_gp['r723tsusp'] * df_scs_gp['r723madj']) / (
                16e6 * df_scs_gp['r723mcpu'])) / (df_scs_gp['smf72int'] * (df_scs_gp['r723mcfs'] / 1024)) * 100
        df_scs_gp['transaction_total_percentage_sp_on_cp_time'] = ((df_scs_gp['r723tsuocp'] * df_scs_gp['r723madj']) / (
                16e6 * df_scs_gp['r723mcpu'])) / (df_scs_gp['smf72int'] * (df_scs_gp['r723mcf'] / 1024)) * 100
        df_scs_gp['transaction_mobile_percentage_cp_time'] = ((df_scs_gp['r723msucp'] * df_scs_gp['r723madj']) / (
                16e6 * df_scs_gp['r723mcpu'])) / (df_scs_gp['smf72int'] * (df_scs_gp['r723mcf'] / 1024)) * 100
        df_scs_gp['transaction_mobile_percentage_sp_time'] = ((df_scs_gp['r723msusp'] * df_scs_gp['r723madj']) / (
                16e6 * df_scs_gp['r723mcpu'])) / (df_scs_gp['smf72int'] * (df_scs_gp['r723mcfs'] / 1024)) * 100
        df_scs_gp['transaction_mobile_percentage_sp_on_cp_time'] = ((df_scs_gp['r723msuocp'] * df_scs_gp[
            'r723madj']) / (
                                                                            16e6 * df_scs_gp['r723mcpu'])) / (
                                                                           df_scs_gp['smf72int'] * (
                                                                           df_scs_gp['r723mcf'] / 1024)) * 100
        df_scs_gp['transaction_cata_percentage_cp_time'] = ((df_scs_gp['r723asucp'] * df_scs_gp['r723madj']) / (
                16e6 * df_scs_gp['r723mcpu'])) / (df_scs_gp['smf72int'] * (df_scs_gp['r723mcf'] / 1024)) * 100
        df_scs_gp['transaction_cata_percentage_sp_time'] = ((df_scs_gp['r723asusp'] * df_scs_gp['r723madj']) / (
                16e6 * df_scs_gp['r723mcpu'])) / (df_scs_gp['smf72int'] * (df_scs_gp['r723mcfs'] / 1024)) * 100
        df_scs_gp['transaction_cata_percentage_sp_on_cp_time'] = ((df_scs_gp['r723asuocp'] * df_scs_gp['r723madj']) / (
                16e6 * df_scs_gp['r723mcpu'])) / (df_scs_gp['smf72int'] * (df_scs_gp['r723mcf'] / 1024)) * 100
        df_scs_gp['transaction_catb_percentage_cp_time'] = ((df_scs_gp['r723bsucp'] * df_scs_gp['r723madj']) / (
                16e6 * df_scs_gp['r723mcpu'])) / (df_scs_gp['smf72int'] * (df_scs_gp['r723mcf'] / 1024)) * 100
        df_scs_gp['transaction_catb_percentage_sp_time'] = ((df_scs_gp['r723bsusp'] * df_scs_gp['r723madj']) / (
                16e6 * df_scs_gp['r723mcpu'])) / (df_scs_gp['smf72int'] * (df_scs_gp['r723mcfs'] / 1024)) * 100
        df_scs_gp['transaction_catb_percentage_sp_on_cp_time'] = ((df_scs_gp['r723bsuocp'] * df_scs_gp['r723madj']) / (
                16e6 * df_scs_gp['r723mcpu'])) / (df_scs_gp['smf72int'] * (df_scs_gp['r723mcf'] / 1024)) * 100
    elif isinstance(interval_agg, str) and interval_agg == 'first':
        agg_scs_x = agg_scs | {'smf72int': 'first', 'tcbtime_insec': 'sum', 'srbtime_insec': 'sum',
                               'aaptime_insec': 'sum', 'iiptime_insec': 'sum',
                               'appl_percentage_cp_time': 'sum', 'appl_percentage_iipcp_time': 'sum',
                               'appl_percentage_iip_time': 'sum',
                               'appl_percentage_aapcp_time': 'sum', 'appl_percentage_aap_time': 'sum',
                               'transaction_total_percentage_cp_time': 'sum',
                               'transaction_total_percentage_sp_on_cp_time': 'sum',
                               'transaction_total_percentage_sp_time': 'sum',
                               'transaction_mobile_percentage_cp_time': 'sum',
                               'transaction_mobile_percentage_sp_on_cp_time': 'sum',
                               'transaction_mobile_percentage_sp_time': 'sum',
                               'transaction_cata_percentage_cp_time': 'sum',
                               'transaction_cata_percentage_sp_on_cp_time': 'sum',
                               'transaction_cata_percentage_sp_time': 'sum',
                               'transaction_catb_percentage_cp_time': 'sum',
                               'transaction_catb_percentage_sp_on_cp_time': 'sum',
                               'transaction_catb_percentage_sp_time': 'sum'}
        for key, value in agg_scs_x.items():
            if key not in df_scss.columns:
                df_scss[key] = np.nan
        df_scs_gp = df_scss.groupby(group_by).agg(agg_scs_x)
        df_scs_gp = df_scs_gp.copy()  # reload the dataframe to avoid performance warning
    else:
        agg_scs_x = agg_scs | {'tcbtime_insec': 'sum', 'srbtime_insec': 'sum', 'aaptime_insec': 'sum',
                               'iiptime_insec': 'sum'}
        df_scs_gp = df_scss.groupby(group_by).agg(agg_scs_x)
        df_scs_gp = df_scs_gp.copy()  # reload the dataframe to avoid performance warning
        df_scs_gp['smf72int'] = interval_agg
    df_scs_gp['cpu_service_coefficient_adjusted'] = df_scs_gp['r723mcpu'] * 16e6 / df_scs_gp['r723madj']
    df_scs_gp['srb_service_coefficient_adjusted'] = df_scs_gp['r723msrb'] * 16e6 / df_scs_gp['r723madj']
    df_scs_gp['storage_total_swapped_in'] = df_scs_gp['r723cprs'] / df_scs_gp['smf72int']
    df_scs_gp['transaction_average_active'] = df_scs_gp['r723ctat'] / df_scs_gp['smf72int']
    df_scs_gp['utilization_total'] = (df_scs_gp['tcbtime_insec'] + df_scs_gp['srbtime_insec'] + df_scs_gp['r723crct'] +
                                      df_scs_gp['r723ciit'] + df_scs_gp['r723chst']) / df_scs_gp['smf72int']
    df_scs_gp['transaction_total_per_second'] = df_scs_gp['r723crcp'] / df_scs_gp['smf72int']
    df_scs_gp['transaction_executed_per_second'] = df_scs_gp['r723cncp'] / df_scs_gp['smf72int']
    df_scs_gp['transaction_address_space_percentage'] = df_scs_gp['r723csac'] / df_scs_gp['r723mtv_']
    df_scs_gp['transaction_enclave_average'] = df_scs_gp['r723ciea'] / df_scs_gp['smf72int']
    df_scs_gp['foreign_enclave_average'] = df_scs_gp['r723cfea'] / df_scs_gp['smf72int']
    df_scs_gp['export_enclave_average'] = df_scs_gp['r723cxea'] / df_scs_gp['smf72int']
    df_scs_gp['utilization_zaap'] = df_scs_gp['r723cifa'] * df_scs_gp['r723nffi'] / 256 / df_scs_gp['smf72int']
    df_scs_gp['utilization_zaap_on_cp'] = df_scs_gp['r723cifc'] / df_scs_gp['smf72int']
    df_scs_gp['utilization_ziip'] = df_scs_gp['r723csup'] * df_scs_gp['r723nffs'] / 256 / df_scs_gp['smf72int']
    df_scs_gp['utilization_ziip_on_cp'] = df_scs_gp['r723csuc'] / df_scs_gp['smf72int']
    df_scs_gp['performance_index'] = 0.0
    df_scs_gp['su_sec'] = ((df_scs_gp['r723ccpu'] - df_scs_gp['r723csup'] - df_scs_gp['r723cifa']
                            ) / df_scs_gp['r723mcpu'] + (df_scs_gp['r723csrb'] / df_scs_gp['r723msrb'])
                           ) / df_scs_gp['smf72int']
    df_scs_gp['cpu_time'] = ((df_scs_gp['r723ccpu'] - df_scs_gp['r723csup'] - df_scs_gp['r723cifa'])
                             / df_scs_gp['cpu_service_coefficient_adjusted']
                             + (df_scs_gp['r723csrb'] / df_scs_gp['srb_service_coefficient_adjusted']))
    df_scs_gp['msu_physical'] = np.where(df_scs_gp['r723cpa_scaling_factor'] is not None,
                                         df_scs_gp['cpu_time'] * 16 * df_scs_gp['r723cpa_scaling_factor'] / df_scs_gp[
                                             'r723cpa_actual'] * 3600 / df_scs_gp['smf72int'],
                                         np.nan)
    df_scs_gp['num_of_cps'] = df_scs_gp['cpu_time'] / df_scs_gp['smf72int']
    df_scs_gp['memory_usage'] = df_scs_gp['r723cprs'] * 4096 / df_scs_gp['smf72int']
    df_scs_gp['absorption_rate'] = np.where(df_scs_gp['r723ctrr'] > 0,
                                            df_scs_gp['r723csrv'] / df_scs_gp['r723ctrr'], 0)
    df_scs_gp['single_page_in_rate'] = np.where(
        (df_scs_gp['r723ctrr'] - df_scs_gp['r723ciea']) > 0,
        df_scs_gp['r723cpir'] / (df_scs_gp['r723ctrr'] - df_scs_gp['r723ciea']), 0)
    df_scs_gp['block_page_in_rate'] = np.where((df_scs_gp['r723ctrr'] - df_scs_gp['r723ciea']) > 0,
                                               df_scs_gp['r723cbpi'] / (df_scs_gp['r723ctrr'] - df_scs_gp['r723ciea']),
                                               0)
    df_scs_gp['shared_page_in_rate'] = np.where(
        (df_scs_gp['r723ctrr'] - df_scs_gp['r723ciea']) > 0,
        df_scs_gp['r723cspa'] / (df_scs_gp['r723ctrr'] - df_scs_gp['r723ciea']), 0)
    df_scs_gp['hsp_page_in_rate'] = np.where((df_scs_gp['r723ctrr'] - df_scs_gp['r723ciea']) > 0,
                                             df_scs_gp['r723chpi'] / (df_scs_gp['r723ctrr'] - df_scs_gp['r723ciea']), 0)
    df_scs_gp['transaction_service_rate'] = np.where(df_scs_gp['r723ctat'] > 0,
                                                     df_scs_gp['r723csrv'] / df_scs_gp['r723ctat'], 0)

    df_scs_gp['start_subchannel_rate'] = df_scs_gp['r723circ'] / df_scs_gp['smf72int']
    df_scs_gp['avg_dasd_response_time'] = np.where(df_scs_gp['r723circ'] > 0,
                                                   (df_scs_gp['r723cict'] + df_scs_gp['r723ciwt']
                                                    + df_scs_gp['r723cidt'] + df_scs_gp['r723ciot']
                                                    ) / df_scs_gp['r723circ'], 0)
    df_scs_gp['avg_dasd_connect_time'] = np.where(df_scs_gp['r723circ'] > 0,
                                                  df_scs_gp['r723cict'] / df_scs_gp['r723circ'], 0)
    df_scs_gp['avg_dasd_disconnect_time'] = np.where(df_scs_gp['r723circ'] > 0,
                                                     df_scs_gp['r723cidt'] / df_scs_gp['r723circ'], 0)
    df_scs_gp['avg_dasd_pending_time'] = np.where(df_scs_gp['r723circ'] > 0,
                                                  df_scs_gp['r723ciwt'] / df_scs_gp['r723circ'], 0)
    df_scs_gp['avg_dasd_ios_queue_time'] = np.where(df_scs_gp['r723circ'] > 0,
                                                    df_scs_gp['r723ciot'] / df_scs_gp['r723circ'], 0)
    df_scs_gp['transaction_average_swapped_in'] = df_scs_gp['r723ctrr'] / df_scs_gp['smf72int']

    df_scs_gp['swaps_per_transaction'] = np.where(df_scs_gp['r723crcp'] > 0,
                                                  df_scs_gp['r723cswc'] / df_scs_gp['r723crcp'], 0)
    df_scs_gp['transaction_response_time_mean'] = np.where(df_scs_gp['r723crcp'] > 0,
                                                           df_scs_gp['r723ctet'] / df_scs_gp['r723crcp'], 0)
    df_scs_gp['transaction_execution_time_mean'] = np.where(df_scs_gp['r723crcp'] > 0,
                                                            df_scs_gp['transaction_execution_time'] / df_scs_gp[
                                                                'r723crcp'], 0)
    df_scs_gp['transaction_queue_delay_time_mean'] = np.where(df_scs_gp['r723crcp'] > 0,
                                                              df_scs_gp['transaction_queue_delay_time'] / df_scs_gp[
                                                                  'r723crcp'], 0)
    df_scs_gp['transaction_aff_delay_time_mean'] = np.where(df_scs_gp['r723crcp'] > 0,
                                                            df_scs_gp['transaction_aff_delay_time'] / df_scs_gp[
                                                                'r723crcp'], 0)
    df_scs_gp['transaction_jcl_time_mean'] = np.where(df_scs_gp['r723crcp'] > 0,
                                                      df_scs_gp['transaction_jcl_time'] / df_scs_gp['r723crcp'], 0)
    df_scs_gp['transaction_inel_delay_time_mean'] = np.where(df_scs_gp['r723crcp'] > 0,
                                                             df_scs_gp['transaction_inel_delay_time'] / df_scs_gp[
                                                                 'r723crcp'], 0)
    df_scs_gp['execution_velocity'] = np.where((df_scs_gp['r723ctou'] + df_scs_gp['r723ctot']) > 0,
                                               df_scs_gp['r723ctou'] * 100 / (df_scs_gp['r723ctou'] + df_scs_gp[
                                                   'r723ctot']), 0)
    df_scs_gp['utilization_cp'] = df_scs_gp['utilization_total'] - df_scs_gp['utilization_ziip'] - df_scs_gp[
        'utilization_zaap']
    if r723ctetx_exist:
        df_scs_gp['transaction_average_elapsed_time_std_dev'] = cal_std_dev(df_scs_gp['r723crcp'],
                                                                            df_scs_gp['r723cetsx'],
                                                                            df_scs_gp['r723ctetx'], 1e6)
    else:
        df_scs_gp['transaction_average_elapsed_time_std_dev'] = cal_std_dev(df_scs_gp['r723crcp'],
                                                                            df_scs_gp['r723cets'],
                                                                            df_scs_gp['r723ctet'], 1e6)
    return df_scs_gp


agg_wms = {'r723ggnm': 'last', 'r723mcde': 'first', 'r723mflg': 'last', 'r723mfl2': 'last',
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
           'r723crgf': 'last', 'is_heterogeneous': 'first', 'r723ceda': 'first',
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
agg_rts = {'class_rt_bucket_1': 'sum', 'class_rt_bucket_2': 'sum', 'class_rt_bucket_3': 'sum',
           'class_rt_bucket_4': 'sum', 'class_rt_bucket_5': 'sum', 'class_rt_bucket_6': 'sum',
           'class_rt_bucket_7': 'sum', 'class_rt_bucket_8': 'sum', 'class_rt_bucket_9': 'sum',
           'class_rt_bucket_10': 'sum', 'class_rt_bucket_11': 'sum', 'class_rt_bucket_12': 'sum',
           'class_rt_bucket_13': 'sum', 'class_rt_bucket_14': 'sum'}


def format_72df(df: pd.DataFrame, current_time: dt.datetime) -> dict:
    """Format smf72 JSON files to the dataframes.

    Args:
        df: JSON dataframe.
        current_time: current time in datetime format.

    Returns:
        A dictionary of dataframes.
    """
    dfs_dict = {'pro': pd.DataFrame(), 'policy': pd.DataFrame(), 'workload': pd.DataFrame(), 'rgs': pd.DataFrame(),
                'wms': pd.DataFrame(), 'scs': pd.DataFrame(), 'data': pd.DataFrame(), 'sctl': pd.DataFrame(),
                'sss': pd.DataFrame(), 'rts': pd.DataFrame(), 'wrsx': pd.DataFrame(), 'wrs': pd.DataFrame(),
                'dnsx': pd.DataFrame(), 'dns': pd.DataFrame(), 'cmss': pd.DataFrame(), 'ceds': pd.DataFrame(),
                'clas': pd.DataFrame(), 'csms': pd.DataFrame(), 'lotd': pd.DataFrame(), 'clod': pd.DataFrame(),
                'clrd': pd.DataFrame(), 'lasc': pd.DataFrame(), 'lare': pd.DataFrame(), 'ense': pd.DataFrame(),
                'ensy': pd.DataFrame(), 'enss': pd.DataFrame(), 'qsad': pd.DataFrame()}

    if 'smf72pro' not in df.columns:
        return dfs_dict
    else:
        dfs_dict['pro'] = build_pro(df)

    if dfs_dict['pro'].empty:
        # Cannot continue processing
        return dfs_dict

    df.set_index(dfs_dict['pro'].index, inplace=True)

    if '72.3' in dfs_dict['pro'].index.get_level_values('smf_type'):  # Contains subtype 3 records
        dfs_dict['policy'] = build_policy(df)
        if dfs_dict['policy'].empty:
            # Cannot continue processing
            return dfs_dict
        dfs_dict['rgs'] = build_rgs(df, dfs_dict['policy'].index)
        dfs_dict['sss'] = build_sss(df)
        dfs_dict['workload'] = build_workload(df, dfs_dict['policy'], current_time)
        dfs_dict['wms'] = build_wms(df,
                                    dfs_dict['policy'].reset_index().set_index(
                                        ['smf72xnm', 'datetime', 'smf72ist', 'smf72iet', 'r723mnsp', 'r723mwnm',
                                         'r723mcnm', 'smf72sid', 'r723mscf', 'r723mflg', 'r723mfl2',
                                         'r723mtvl', 'r723mtv_',
                                         'r723mcde', 'r723mcpg', 'r723msub', 'r723clsc', 'r723madj', 'r723mcpu',
                                         'r723mcf', 'r723mcfs', 'cpu_service_coefficient_adjusted',
                                         'srb_service_coefficient_adjusted', 'r723cpa_scaling_factor',
                                         'r723cpa_actual', 'r723mcfi', 'r723msrb', 'r723nffi', 'r723nffs', 'smf72int',
                                         'r723ggnm']).index,
                                    current_time)

        dfs_dict['rts'] = build_rts(df,
                                    dfs_dict['wms'][dfs_dict['wms']['r723crtx'] > 0].reset_index().set_index(
                                        ['smf72xnm', 'datetime', 'smf72ist', 'smf72iet', 'r723mnsp', 'r723mwnm',
                                         'r723mcnm', 'r723cper',
                                         'smf72sid']).index)
        dfs_dict['scs'] = build_scs(df,
                                    dfs_dict['policy'].reset_index().set_index(
                                        ['smf72xnm', 'datetime', 'smf72ist', 'smf72iet', 'r723mnsp', 'smf72sid',
                                         'smf_type']).index,
                                    dfs_dict['wms'].reset_index().set_index(
                                        ['smf72xnm', 'datetime', 'smf72ist', 'smf72iet', 'r723mnsp', 'r723mwnm',
                                         'r723mcnm', 'r723cper', 'smf72sid', 'is_report_class', 'r723mtvl', 'r723mtv_',
                                         'r723madj', 'r723mcpu', 'r723mcf', 'r723mcfs',
                                         'cpu_service_coefficient_adjusted', 'srb_service_coefficient_adjusted',
                                         'r723cpa_scaling_factor', 'r723cpa_actual', 'r723mcfi', 'r723msrb', 'r723nffi',
                                         'r723nffs', 'smf72int']).index,
                                    dfs_dict['rts'])
        df_scs_idx = dfs_dict['scs'][dfs_dict['scs']['r723cwmn'] > 0].copy().reset_index().set_index(
            ['smf72xnm', 'datetime', 'smf72ist', 'smf72iet', 'r723mnsp', 'r723mwnm', 'r723mcnm', 'r723cper',
             'smf72sid'])
        df_scs_idx = df_scs_idx.reindex(df_scs_idx.index.repeat(df_scs_idx.r723cwmn)).index
        dfs_dict['wrs'] = build_wrs(df, dfs_dict['policy'].index, df_scs_idx)
        if dfs_dict['wrs'].shape[0] > 0:
            agg_f = dict.fromkeys(dfs_dict['wrs'], 'sum')
            agg_f.pop('r723rflg', None)
            agg_f.pop('r723rexe', None)
            agg_f.pop('r723rdbe', None)
            agg_f.pop('r723rdnx', None)
            agg_f.pop('r723rdnn', None)
            agg_f['r723rtyp'] = 'first'
            df_wrs_gp = dfs_dict['wrs'].reset_index().groupby(
                [col.name for col in Smf72Scs.__table__.primary_key.columns.values()]).agg(agg_f)

            dfs_dict['scs'] = dfs_dict['scs'].join(df_wrs_gp)

        dfs_dict['wrsx'] = build_wrsx(df, dfs_dict['wrs'], current_time)
        dfs_dict['dns'] = build_dns(df,
                                    dfs_dict['policy'].reset_index()[
                                        ['smf72xnm', 'datetime', 'smf72ist', 'smf72iet', 'r723mnsp', 'r723mwnm',
                                         'r723mcnm', 'smf72sid']
                                    ].set_index(['smf72xnm', 'datetime', 'smf72ist', 'smf72iet', 'r723mnsp', 'r723mwnm',
                                                 'r723mcnm', 'smf72sid']).index,
                                    dfs_dict['wrs'])
        dfs_dict['dnsx'] = build_dnsx(df, dfs_dict['dns'], current_time)

    if '72.4' in dfs_dict['pro'].index.get_level_values('smf_type'):  # Contains subtype 4 records
        dfs_dict['data'] = build_data(df,
                                      dfs_dict['pro'][dfs_dict['pro'].index.get_level_values(
                                          'smf_type') == '72.4'].reset_index().set_index(
                                          ['csc', 'smf72xnm', 'smf72sid', 'datetime', 'smf72ist', 'smf72iet',
                                           'smf_type',
                                           'smf72int']).index)
    if '72.5' in dfs_dict['pro'].index.get_level_values('smf_type'):  # Contains subtype 5 records
        df_pro_idx = dfs_dict['pro'][dfs_dict['pro'].index.get_level_values('smf_type') == '72.5'].reset_index(
        ).set_index(['csc', 'smf72xnm', 'smf72sid', 'datetime', 'smf72ist', 'smf72iet', 'smf_type', 'smf72int']).index
        dfs_dict['sctl'] = build_sctl(df, df_pro_idx)
        dfs_dict['cmss'] = build_cmss(df, df_pro_idx)
        dfs_dict['ceds'] = build_ceds(df, df_pro_idx)
        dfs_dict['clas'] = build_clas(df, df_pro_idx)
        dfs_dict['csms'] = build_csms(df, df_pro_idx)
        dfs_dict['lotd'] = build_lotd(df, df_pro_idx)
        dfs_dict['clod'] = build_clod(df, df_pro_idx)
        dfs_dict['clrd'] = build_clrd(df, df_pro_idx)
        dfs_dict['lasc'] = build_lasc(df, df_pro_idx)
        dfs_dict['lare'] = build_lare(df, df_pro_idx)
        dfs_dict['ense'] = build_ense(df, df_pro_idx)
        dfs_dict['ensy'] = build_ensy(df, df_pro_idx)
        dfs_dict['enss'] = build_enss(df, df_pro_idx)
        dfs_dict['qsad'] = build_qsad(df, df_pro_idx)
    return dfs_dict


def print_serialization_delay(jsonfiles: tuple, lpar: str, start_time_str: str, end_time_str: str) -> str:
    """Print smf72 Serialization Delay Report based on JSON files.

    Args:
        jsonfiles: JSON file or files.
        lpar: Target LPAR to print.
        start_time_str: Start time string.
        end_time_str: End time string.

    Returns:
        Serialization Delay report.
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
                    or df.iloc[0]['header'].get('recType') is None or df.iloc[0]['header']['recType'] != 72:
                click.echo(
                    f"\nInvalid JSON file {jsonfile}. This file will be skipped.")
                continue

            try:
                df_dict = format_72df(df, current_time)
            except Exception as e:
                click.echo(f"\nUnsupported JSON file {jsonfile} with error: {str(e)}. This file will be skipped.")
                continue

            if df_dict['pro'].empty:
                click.echo(
                    f"\nThis JSON file {jsonfile} is not for this smf type. This file will be skipped.")
                # Cannot continue processing
                continue

            if df_dict['sctl'].empty:
                click.echo(
                    f"\nThis JSON file {jsonfile} is not for this smf type. This file will be skipped.")
                # Cannot continue processing
                continue
            start_tbls = df_dict['sctl'].loc[~df_dict['sctl'].index.duplicated(keep='first'), :].query(
                "smf72ist >= @start_time and smf72ist <= @end_time and smf72sid == @lpar").copy()
            if start_tbls.empty:
                continue
            for sctl in start_tbls.reset_index().to_dict('records'):
                cmsss = df_dict['cmss'].query(
                    "smf72iet == @sctl['smf72iet']").reset_index().groupby(
                    [col.name for col in
                     Smf72Cmss.__table__.primary_key.columns.values()]).first().reset_index()
                cedss = df_dict['ceds'].query(
                    "smf72iet == @sctl['smf72iet']").reset_index().groupby(
                    [col.name for col in
                     Smf72Ceds.__table__.primary_key.columns.values()]).first().reset_index()
                class_ = df_dict['clas'].query(
                    "smf72iet == @sctl['smf72iet']").reset_index().groupby(
                    [col.name for col in
                     Smf72Clas.__table__.primary_key.columns.values()]).first().reset_index()
                csmss = df_dict['csms'].query(
                    "smf72iet == @sctl['smf72iet']").reset_index().groupby(
                    [col.name for col in
                     Smf72Csms.__table__.primary_key.columns.values()]).first().reset_index()
                lotds = df_dict['lotd'].query(
                    "smf72iet == @sctl['smf72iet']").reset_index().groupby(
                    [col.name for col in
                     Smf72Lotd.__table__.primary_key.columns.values()]).first().reset_index()
                clods = df_dict['clod'].query(
                    "smf72iet == @sctl['smf72iet']").reset_index().groupby(
                    [col.name for col in
                     Smf72Clod.__table__.primary_key.columns.values()]).first().reset_index()
                clrds = df_dict['clrd'].query(
                    "smf72iet == @sctl['smf72iet']").reset_index().groupby(
                    [col.name for col in
                     Smf72Clrd.__table__.primary_key.columns.values()]).first().reset_index()
                lascs = df_dict['lasc'].query(
                    "smf72iet == @sctl['smf72iet']").reset_index().groupby(
                    [col.name for col in
                     Smf72Lasc.__table__.primary_key.columns.values()]).first().reset_index()
                lares = df_dict['lare'].query(
                    "smf72iet == @sctl['smf72iet']").reset_index().groupby(
                    [col.name for col in
                     Smf72Lare.__table__.primary_key.columns.values()]).first().reset_index()
                enses = df_dict['ense'].query(
                    "smf72iet == @sctl['smf72iet']").reset_index().groupby(
                    [col.name for col in
                     Smf72Ense.__table__.primary_key.columns.values()]).first().reset_index()
                ensys = df_dict['ensy'].query(
                    "smf72iet == @sctl['smf72iet']").reset_index().groupby(
                    [col.name for col in
                     Smf72Ensy.__table__.primary_key.columns.values()]).first().reset_index()
                ensss = df_dict['enss'].query(
                    "smf72iet == @sctl['smf72iet']").reset_index().groupby(
                    [col.name for col in
                     Smf72Enss.__table__.primary_key.columns.values()]).first().reset_index()
                pro = df_dict['pro'].query(
                    "smf72iet == @sctl['smf72iet'] and smf_type == '72.5'").reset_index().groupby(
                    [col.name for col in
                     Smf72Pro.__table__.primary_key.columns.values()]).first().reset_index()

                grs_mode, system_lock_summary, latch_summary, grs_summary = format_delay_summary(sctl)
                cms_lock_detail = format_cms_lock_detail(cmsss.to_dict('records'),
                                                         cedss.to_dict('records'),
                                                         class_.to_dict('records'),
                                                         csmss.to_dict('records'))
                cml_lock_detail = format_cml_lock_detail(lotds.to_dict('records'),
                                                         clods.to_dict('records'),
                                                         clrds.to_dict('records'))
                grs_latch_detail = format_grs_latch_detail(lascs.to_dict('records'),
                                                           lares.to_dict('records'))
                grs_enq_detail = format_grs_enq_detail(enses.to_dict('records'),
                                                       ensys.to_dict('records'),
                                                       ensss.to_dict('records'))
                if cms_lock_detail is not None or cml_lock_detail is not None or grs_latch_detail is not None or grs_enq_detail is not None:
                    page_sub_detail = format_sdelay_header('RMF Interval', sctl, pro.to_dict('records')[0])
                    page_sub_detail += '\nSystem Locks\n'
                    page_sub_detail += system_lock_summary
                    page_sub_detail += '\nGRS Latch Set Creator\n'
                    page_sub_detail += latch_summary
                    page_sub_detail += '\nGRS Enqueue\n'
                    page_sub_detail += grs_summary

                    if cms_lock_detail is not None:
                        page_sub_detail += '\nCMS Lock Details\n'
                        page_sub_detail += cms_lock_detail
                    if cml_lock_detail is not None:
                        page_sub_detail += '\nCML and Local Lock Details\n'
                        page_sub_detail += cml_lock_detail
                    if grs_latch_detail is not None:
                        page_sub_detail += '\nGRS Latch Details\n'
                        page_sub_detail += grs_latch_detail
                    if grs_enq_detail is not None:
                        page_sub_detail += '\nGRS Enqueue Details\n'
                        page_sub_detail += grs_enq_detail
                    if page_detail != '':
                        page_detail += '\n\n'
                    page_detail += page_sub_detail
            if page_detail != '':
                if report != '':
                    report += '\n\n'
                report += page_detail
    if report == '':
        report = 'No data found.'
    return report


def print_workload_activity_report(jsonfiles: tuple, lpar: str, start_time_str: str, end_time_str: str,
                                   category_selected: str, lpar_sysplex: str,
                                   lpar_sysplex_selected: str, wlm_selected: str = None, cpa_actual: int = None) -> str:
    """Print smf72 Workload Activity Report based on JSON files.

    Args:
        jsonfiles: JSON file or files.
        lpar: Target LPAR to print.
        start_time_str: Start time string.
        end_time_str: End time string.
        category_selected: Category selected.
        lpar_sysplex: Lpar or Sysplex.
        lpar_sysplex_selected: Lpar or Sysplex selected.
        wlm_selected: WLM selected.
        cpa_actual: Physical CPU adjustment factor based on Model Capacity Rating.

    Returns:
        Workload activity report.
    """

    # inner functions
    def format_policy_code(iet):
        policy = df_dict['policy'].query(
            "smf72iet == @iet").reset_index().groupby(
            [col.name for col in Smf72Policy.__table__.primary_key.columns.values()]).first().reset_index()
        policy_name = policy['r723mnsp'].values[0]
        pro = df_dict['pro'].query(
            "smf72iet == @iet and smf_type == '72.3'").reset_index().groupby(
            [col.name for col in Smf72Pro.__table__.primary_key.columns.values()]).first().reset_index()
        sid_list = pro[['smf72sid', 'smf72int', 'speed_boost', 'ziip_boost']].values.tolist()
        rgss = df_dict['rgs'].query("smf72iet == @iet and r723mnsp == @policy_name")
        r723ggnm_list = rgss.reset_index()['r723ggnm'].to_list()
        rgss_wmss = []
        rgss_wmss_scss = []
        for ggnm in r723ggnm_list:
            rgss_wms = df_dict['wms'].query(
                "smf72iet == @iet and r723mnsp == @policy_name and r723ggnm == @ggnm and r723cper == 1")
            rgss_ggnm_wms = []
            for index in rgss_wms.index:
                rgss_ggnm_wms_scss = df_dict['scs'][df_dict['scs'].reset_index().set_index(
                    [col.name for col in Smf72Wms.__table__.primary_key.columns.values()]).index == index]
                rgss_ggnm_wms.append(rgss_ggnm_wms_scss.reset_index().to_dict('records'))
            rgss_wmss.append(rgss_wms.reset_index().to_dict('records'))
            rgss_wmss_scss.append(rgss_ggnm_wms)

        policy_code = format_policy_page("Interval", policy.to_dict('records')[0],
                                         sid_list, rgss.reset_index().to_dict('records'),
                                         rgss_wmss, rgss_wmss_scss)
        header_code = format_workload_header("Interval", policy.to_dict('records')[0])
        return policy_code, header_code

    def print_one_workload(target_df, header_code, target_type):
        page_content = ''
        for row in target_df.reset_index().to_dict('records'):
            page_sub_content = ""
            # if row['r723crcp'] == 0 and row['r723csrv'] == 0:
            #     continue
            policy = df_dict['policy'].query(
                "smf72iet == @row['smf72iet']").reset_index().groupby(
                [col.name for col in
                 Smf72Policy.__table__.primary_key.columns.values()]).first().reset_index()
            if target_type == 'scs':
                wms = df_dict['wms'].query(
                    "smf72iet == @row['smf72iet'] and r723mnsp == @row['r723mnsp'] and r723mwnm == @row['r723mwnm'] and r723mcnm == @row['r723mcnm'] and r723cper == @row['r723cper']"
                ).reset_index().groupby(
                    [col.name for col in Smf72Wms.__table__.primary_key.columns.values()]).first().reset_index()
                rts = df_dict['rts'].query(
                    "smf72iet == @row['smf72iet'] and r723mnsp == @row['r723mnsp'] and r723mwnm == @row['r723mwnm'] and r723mcnm == @row['r723mcnm'] and r723cper == @row['r723cper']"
                ).reset_index().groupby(
                    [col.name for col in Smf72Rts.__table__.primary_key.columns.values()]).first().reset_index()
            else:
                scss = df_dict['scs'].query(
                    "smf72iet == @row['smf72iet'] and r723mnsp == @row['r723mnsp'] and r723mwnm == @row['r723mwnm'] and r723mcnm == @row['r723mcnm'] and r723cper == @row['r723cper']"
                ).reset_index().groupby(
                    [col.name for col in Smf72Scs.__table__.primary_key.columns.values()]).first().reset_index()
            ssss = df_dict['sss'].query(
                "smf72iet == @row['smf72iet'] and r723mnsp == @row['r723mnsp'] and r723mwnm == @row['r723mwnm'] and r723mcnm == @row['r723mcnm'] and r723cper == @row['r723cper']"
            ).reset_index().groupby(
                [col.name for col in
                 Smf72Sss.__table__.primary_key.columns.values()]).first().reset_index()
            wrss = df_dict['wrs'].query(
                "smf72iet == @row['smf72iet'] and r723mnsp == @row['r723mnsp'] and r723mwnm == @row['r723mwnm'] and r723mcnm == @row['r723mcnm'] and r723cper == @row['r723cper']"
            ).reset_index().groupby(
                [col.name for col in
                 Smf72Wrs.__table__.primary_key.columns.values()]).first().reset_index()
            pro = df_dict['pro'].query(
                "smf72iet == @row['smf72iet'] and smf_type == '72.3'").reset_index().groupby(
                [col.name for col in
                 Smf72Pro.__table__.primary_key.columns.values()]).first().reset_index()
            if target_type == 'scs':
                transaction_detail = format_transaction_detail(row,
                                                               wms.to_dict('records')[0],
                                                               policy.to_dict('records')[0],
                                                               ssss.reset_index().to_dict('records'))
            else:
                transaction_detail = format_transaction_detail(row, row,
                                                               policy.to_dict('records')[0],
                                                               ssss.reset_index().to_dict('records'))
            state_detail = format_state_samples_breakdown(row,
                                                          wrss.to_dict('records'))
            page_sub_content += header_code
            page_sub_content += transaction_detail

            if state_detail is not None:
                page_sub_content += state_detail
            if target_type == 'scs':
                if not rts.empty:
                    goal_response = format_goal_and_response_lpar(row, pro.to_dict('records')[0],
                                                                  rts.to_dict('records')[0])
                    response_time_distribution = format_response_time_distribution(
                        row, rts.to_dict('records')[0], policy.to_dict('records')[0]['smf72int'])
                else:
                    goal_response = format_goal_and_response_lpar(row, pro.to_dict('records')[0], None)
                    response_time_distribution = format_response_time_distribution(
                        row, None, policy.to_dict('records')[0]['smf72int'])
            else:
                goal_response = format_goal_and_response_sysplex(row, scss.reset_index().to_dict('records'),
                                                                 pro.to_dict('records')[0])
                response_time_distribution = format_response_time_distribution(
                    row, row, policy.to_dict('records')[0]['smf72int'], scss.reset_index().to_dict('records'))
            if goal_response is not None and '- All Data Zero -' not in page_sub_content:
                page_sub_content += goal_response

            if response_time_distribution is not None:
                page_sub_content += response_time_distribution

            page_content += '\n\n'
            page_content += page_sub_content

        return page_content

    if category_selected not in ['Workload Group', 'Service Class', 'Report Class'] or \
            lpar_sysplex not in ['Lpar', 'Sysplex']:
        return 'Invalid report type.'

    get_performance_index = np.vectorize(cal_performance_index)
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
                    or df.iloc[0]['header'].get('recType') is None or df.iloc[0]['header']['recType'] != 72:
                click.echo(
                    f"\nInvalid JSON file {jsonfile}. This file will be skipped.")
                continue
            try:
                df_dict = format_72df(df, current_time)
            except Exception as e:
                click.echo(f"\nUnsupported JSON file {jsonfile} with error: {str(e)}. This file will be skipped.")
                continue

            if df_dict['pro'].empty:
                click.echo(
                    f"\nThis JSON file {jsonfile} is not for this smf type. This file will be skipped.")
                # Cannot continue processing
                continue
            if df_dict['policy'].empty:
                click.echo(
                    f"\nThis JSON file {jsonfile} is not for this smf type. This file will be skipped.")
                # Cannot continue processing
                continue

            if cpa_actual is not None:
                df_dict['pro']['r723cpa_actual'] = cpa_actual
                df_dict['pro']['r723cpa_scaling_factor'] = 64
                if df_dict['policy'].shape[0] > 0 and df_dict['policy']['r723cpa_actual'].isnull().all():
                    df_dict['policy']['r723cpa_actual'] = cpa_actual
                    df_dict['policy']['r723cpa_scaling_factor'] = 64
                if df_dict['scs'].shape[0] > 0 and df_dict['scs']['r723cpa_actual'].isnull().all():
                    df_dict['scs']['r723cpa_actual'] = cpa_actual
                    df_dict['scs']['r723cpa_scaling_factor'] = 64
                    df_dict['scs']['msu_physical'] = np.where(
                        df_dict['scs']['r723cpa_scaling_factor'] is not None,
                        df_dict['scs']['cpu_time'] * 16 * df_dict['scs']['r723cpa_scaling_factor']
                        / df_dict['scs']['r723cpa_actual'] * 3600 / df_dict['scs']['smf72int'], np.nan)

            if not df_dict['policy'].empty:
                df_dict['policy']['smf70cai'] = 100  # "N/A"
            if 'r723ctetx' not in df_dict['scs'].columns:
                r723ctetx_exist = False
            else:
                r723ctetx_exist = True
            df_dict['scs'] = df_dict['scs'].copy() # reload the dataframe to avoid defragmentation
            for column in ['r723cadtx', 'r723ccvtx', 'r723cetsx', 'r723ciqtx', 'r723cqdtx', 'r723ctetx',
                           'r723cxetx', 'r723enctrxcalls', 'r723enctrxet', 'r723enctrxets', 'r723enctrxnum']:
                if column not in df_dict['scs'].columns:
                    df_dict['scs'][column] = np.nan
            df_wms_1 = agg_scs_group_by(df_dict['scs'],
                                        [col.name for col in Smf72Wms.__table__.primary_key.columns.values()],
                                        'first',
                                        r723ctetx_exist)

            df_wms_2 = df_dict['rts'].groupby(
                [col.name for col in Smf72Wms.__table__.primary_key.columns.values()]).agg(agg_rts)
            df_dict['wms'] = df_dict['wms'][
                ['r723cimp', 'r723ggnm', 'r723mcde', 'is_report_class', 'r723mflg', 'r723mfl2', 'r723mscf',
                 'stor_protection', 'cpu_protection', 'velocity_io_delays',
                 'svpol_unaval', 'rcaa_unaval', 'tenant_report_class', 'honor_prio',
                 'hismt_failure', 'ziip_honor_prio', 'zaap_honor_prio', 'zaap_crossover',
                 'r723mtvl', 'r723mtv_', 'r723mcpg', 'r723msub', 'r723clsc', 'smf72int']].copy()
            df_dict['wms'] = pd.concat([df_dict['wms'],
                                        df_wms_1.drop(columns=['r723cimp', 'is_report_class', 'r723mtv_', 'smf72int']),
                                        df_wms_2], axis=1)
            df_dict['wms']['performance_index'] = get_performance_index(df_dict['wms']['class_goal_type'],
                                                                        df_dict['wms']['execution_velocity'],
                                                                        df_dict['wms']['r723cval'],
                                                                        df_dict['wms']['r723cpct'],
                                                                        df_dict['wms']['class_rt_bucket_1'],
                                                                        df_dict['wms']['class_rt_bucket_2'],
                                                                        df_dict['wms']['class_rt_bucket_3'],
                                                                        df_dict['wms']['class_rt_bucket_4'],
                                                                        df_dict['wms']['class_rt_bucket_5'],
                                                                        df_dict['wms']['class_rt_bucket_6'],
                                                                        df_dict['wms']['class_rt_bucket_7'],
                                                                        df_dict['wms']['class_rt_bucket_8'],
                                                                        df_dict['wms']['class_rt_bucket_9'],
                                                                        df_dict['wms']['class_rt_bucket_10'],
                                                                        df_dict['wms']['class_rt_bucket_11'],
                                                                        df_dict['wms']['class_rt_bucket_12'],
                                                                        df_dict['wms']['class_rt_bucket_13'],
                                                                        df_dict['wms']['class_rt_bucket_14'])
            df_dict['wms']['last_update_time'] = current_time
            if df_dict['dnsx'].shape[0] > 0:
                agg_dnsx = {'r723rwnn': 'sum'}
                df_dict['dnsx'] = df_dict['dns'].groupby(
                    [col.name for col in Smf72Dnsx.__table__.primary_key.columns.values()]).agg(
                    agg_dnsx).reset_index()
                df_dict['dnsx']['last_update_time'] = current_time

            if df_dict['wrsx'].shape[0] > 0:
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
                df_dict['wrsx'] = df_dict['wrs'].groupby(
                    [col.name for col in Smf72Wrsx.__table__.primary_key.columns.values()]).agg(
                    agg_wrsx).reset_index()
                df_dict['wrsx']['last_update_time'] = current_time

            if category_selected == 'Workload Group':
                starting = 'workload'
                starting_tbl = Smf72Workload
            else:  # 'Service Class' or 'Report Class'
                if lpar_sysplex == 'Lpar':
                    starting = 'scs'
                    starting_tbl = Smf72Scs
                else:
                    starting = 'wms'
                    starting_tbl = Smf72Wms
            if category_selected != 'Workload Group' and lpar_sysplex == 'Lpar':
                start_tbls = df_dict[starting].copy().reset_index().query(
                    "smf72ist >= @start_time and smf72ist <= @end_time and smf72sid == @lpar_sysplex_selected"
                ).drop_duplicates().set_index(
                    [col.name for col in starting_tbl.__table__.primary_key.columns.values()])

            elif lpar_sysplex == 'Sysplex':
                if wlm_selected is not None:
                    if category_selected in ('Service Class', 'Report Class'):
                        start_tbls = df_dict[starting].copy().reset_index().query(
                            "smf72ist >= @start_time and smf72ist <= @end_time and smf72xnm == @lpar_sysplex_selected and r723mcnm == @wlm_selected"
                        ).drop_duplicates().reset_index().set_index(
                            [col.name for col in starting_tbl.__table__.primary_key.columns.values()])
                    else:
                        start_tbls = df_dict[starting].copy().reset_index().query(
                            "smf72ist >= @start_time and smf72ist <= @end_time and smf72xnm == @lpar_sysplex_selected and r723mwnm == @wlm_selected"
                        ).drop_duplicates().reset_index().set_index(
                            [col.name for col in starting_tbl.__table__.primary_key.columns.values()])
                else:
                    if category_selected in ('Service Class', 'Report Class'):
                        start_tbls = df_dict[starting].copy().reset_index().query(
                            "smf72ist >= @start_time and smf72ist <= @end_time and smf72xnm == @lpar_sysplex_selected"
                        ).drop_duplicates().reset_index().set_index(
                            [col.name for col in starting_tbl.__table__.primary_key.columns.values()])
                    else:
                        start_tbls = df_dict[starting].copy().reset_index().query(
                            "smf72ist >= @start_time and smf72ist <= @end_time and smf72xnm == @lpar_sysplex_selected"
                        ).drop_duplicates().reset_index().set_index(
                            [col.name for col in starting_tbl.__table__.primary_key.columns.values()])
            else:  # 'Workload Group' and 'Lpar'
                if wlm_selected is not None:
                    start_tbls = df_dict[starting].copy().reset_index().query(
                        "smf72ist >= @start_time and smf72ist <= @end_time and r723mwnm == @wlm_selected"
                    ).drop_duplicates().reset_index().set_index(
                        [col.name for col in starting_tbl.__table__.primary_key.columns.values()])
                else:
                    start_tbls = df_dict[starting].copy().reset_index().query(
                        "smf72ist >= @start_time and smf72ist <= @end_time"
                    ).drop_duplicates().reset_index().set_index(
                        [col.name for col in starting_tbl.__table__.primary_key.columns.values()])

            if start_tbls.empty:
                continue

            workload_object_list = []
            header_code = None
            policy_code = None
            policy = None
            if category_selected in ('Service Class', 'Report Class'):
                if lpar_sysplex == 'Lpar':
                    if wlm_selected is not None:
                        scss_grp = start_tbls.query('r723mcnm == @wlm_selected').copy().reset_index().groupby('smf72iet')
                    else:
                        scss_grp = start_tbls.copy().reset_index().groupby('smf72iet')
                    for report_iet, scss_df in scss_grp:
                        policy_code, header_code = format_policy_code(report_iet)
                        report_detail = print_one_workload(scss_df, header_code, 'scs')
                        report_detail += '\n\n'
                        report_detail += header_code
                        report_detail += policy_code
                        if page_detail != '':
                            page_detail += '\n\n'
                        page_detail += report_detail

                else:  # lpar_sysplex == 'Sysplex'
                    if wlm_selected is not None:
                        wms_grp = start_tbls.query('r723mcnm == @wlm_selected').copy().reset_index().groupby('smf72iet')
                    else:
                        wms_grp = start_tbls.copy().reset_index().groupby('smf72iet')
                    for report_iet, wms_df in wms_grp:
                        policy_code, header_code = format_policy_code(report_iet)
                        report_detail = print_one_workload(wms_df, header_code, 'wms')
                        report_detail += '\n\n'
                        report_detail += header_code
                        report_detail += policy_code
                        if page_detail != '':
                            page_detail += '\n\n'
                        page_detail += report_detail

            else:  # 'Workload Group'
                workload_grp = start_tbls.copy().reset_index().groupby('smf72iet')
                for report_iet, workload_df in workload_grp:
                    policy_code, header_code = format_policy_code(report_iet)
                    page_sub_detail = ''
                    for workload in workload_df.copy().reset_index().to_dict('records'):
                        wmss = df_dict['wms'].query(
                            "smf72iet == @report_iet and r723mnsp == @workload['r723mnsp'] and r723mwnm == @workload['r723mwnm']"
                        ).reset_index().groupby(
                            [col.name for col in Smf72Wms.__table__.primary_key.columns.values()]).first().reset_index()
                        if lpar_sysplex == 'Lpar':
                            for wms in wmss.to_dict('records'):
                                scss = df_dict['scs'].query(
                                    "smf72iet == @wms['smf72iet'] and r723mnsp == @wms['r723mnsp'] and r723mwnm == @wms['r723mwnm'] and r723mcnm == @wms['r723mcnm'] and r723cper == @wms['r723cper']"
                                ).reset_index().groupby(
                                    [col.name for col in
                                     Smf72Scs.__table__.primary_key.columns.values()]).first().reset_index()
                                page_sub_detail += print_one_workload(scss, header_code, 'scs')
                        else:
                            page_sub_detail += print_one_workload(wmss, header_code, 'wms')

                    page_detail += page_sub_detail
                    page_detail += '\n'
                    page_detail += header_code
                    page_detail += policy_code

            if page_detail != '':
                if report != '':
                    report += '\n\n'
                report += page_detail
    if report == '':
        report = 'No data found.'

    return report

