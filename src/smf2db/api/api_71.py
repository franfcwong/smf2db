from typing import Union

import click
import numpy as np
import pandas as pd

from smf2db.api.report_util import format_central_storage_paging_rates, format_central_storage_movement_req_rates, \
    format_frame_slot_counts, format_memory_obj
from smf2db.api.util import (setdatetime, is_bit_set)
from smf2db.db_models.smf71_model import Smf71Pag, Smf71Pro


def build_pro(df: pd.DataFrame) -> Union[pd.DataFrame, None]:
    """Build the dataframe for RMF Product Section which will be uploaded to smf71_pro table.

    Args:
        df: The master dataframe which is created from the JSON file.

    Returns:
        The dataframe for the RMF product section or None if csc is not found in the database.
    """
    set_datetime = np.vectorize(setdatetime)
    df_pro = pd.concat([df['header'].apply(pd.Series),
                        df['smf71pro'].apply(pd.Series)],
                       axis=1).rename(
        columns={'sysId': 'smf71sid',
                 'sysInd': 'smf71flg', 'recType': 'smf_type'})
    df_pro['csc'] = np.nan
    df_pro['smf71sid'] = df_pro['smf71sid'].str.strip()
    df_pro['smf71ist'] = pd.to_datetime(df_pro['smf71ist'])
    df_pro['smf71gie'] = pd.to_datetime(df_pro['smf71gie'])
    df_pro['smf71int'] = pd.to_timedelta(df_pro['smf71int']) / np.timedelta64(1, 's')
    df_pro['smf71lgo'] = pd.to_timedelta(df_pro['smf71lgo']) / np.timedelta64(1, 'h')
    df_pro['datetime'] = set_datetime(df_pro['smf71ist'])
    df_pro['smf_type'] = df_pro['smf_type'].astype(str) + '.' + df_pro['subType'].astype(str)
    df_pro['smf71flg'] = df_pro['smf71flg'].apply(lambda x: int(str(x), 16))
    df_pro['smf71fla'] = df_pro['smf71fla'].apply(lambda x: int(str(x), 16))
    df_pro['smf71prf'] = df_pro['smf71prf'].apply(lambda x: int(str(x), 16))
    df_pro['smf71srl'] = df_pro['smf71srl'].apply(lambda x: int(str(x), 16))
    df_pro['speed_boost'] = df_pro['smf71fla'].apply(lambda x: is_bit_set(x, 16, 10))
    df_pro['ziip_boost'] = df_pro['smf71fla'].apply(lambda x: is_bit_set(x, 16, 9))
    df_pro = df_pro[Smf71Pro.__table__.columns.keys()].set_index(
        ['datetime', 'smf71ist', 'smf71iet', 'smf_type', 'csc', 'smf71sid', 'smf71int'])
    return df_pro


def build_pag(df: pd.DataFrame) -> pd.DataFrame:
    """Build the dataframe for Paging Data Section which will be uploaded to smf71_pag table.

    Args:
        df: The master dataframe which is created from the JSON file.

    Returns:
        The dataframe for the Paging Data section.
    """
    if 'smf71pag' in df.columns:
        df_pag = pd.concat([df[df.index.get_level_values('smf_type') == '71.1']['smf71pro'].apply(pd.Series)[
                                ['smf71ptn', 'smf71snm', 'smf71xnm']],
                            df[df.index.get_level_values('smf_type') == '71.1']['smf71pag'].apply(pd.Series)],axis=1
                           ).reset_index().set_index(['csc', 'smf71sid', 'datetime', 'smf71ist', 'smf71iet'])
        df_pag['smf71rfl'] = df_pag['smf71rfl'].apply(lambda x: int(str(x), 16))
        df_pag['total_nvio_pgin_nswap_blk'] = df_pag['smf71blk'] + df_pag['smf71sbi']
        df_pag['total_sum_pgin_nswap_blk'] = df_pag['smf71blk'] + df_pag['smf71hin'] + \
                                             df_pag['smf71vin']
        df_pag['smf71pmt'] = pd.to_timedelta(df_pag['smf71pmt']) / np.timedelta64(1, 's')
        df_pag['pg_mv_within_cs'] = df_pag['smf71pmv']
        df_pag['pg_mv_rate'] = df_pag['smf71pmv'] / df_pag['smf71int']
        df_pag['pg_mv_time_percentage'] = df_pag['smf71pmt'] / df_pag['smf71int']  # pmt / int
        df_pag['avg_pg_per_blk'] = df_pag['smf71blk'] / df_pag['smf71int']  # blk / int
        df_pag['blk_per_seconds'] = df_pag['smf71blk'] / df_pag['smf71int']
        df_pag['pg_fault_rate'] = df_pag['smf71pin'] / df_pag['smf71int']  # pin / int
        df_pag['total_hspace_pgout_nswap'] = df_pag['smf71hot']  # hot
        df_pag['total_hspace_pgin_nswap_blk'] = df_pag['smf71hin']  # hin
        df_pag['total_vio_pgin_nswap_blk'] = df_pag['smf71vin']  # vin
        df_pag['total_nvio_pgin_swap'] = df_pag['smf71sin']  # sin
        df_pag['total_nvio_pgout_swap'] = df_pag['smf71sot']  # sot
        df_pag['total_sum_pgin_swap'] = df_pag['smf71sin']  # sin
        df_pag['total_sum_pgout_swap'] = df_pag['smf71sot']
        df_pag['total_vio_pgout_nswap'] = df_pag['smf71vot']
        df_pag['sys_csa_pgin_nswap_blk'] = df_pag['smf71sbi'] - df_pag['smf71lbi']  # sbi - lbi
        df_pag['sys_csa_pgin_nswap_nblk'] = df_pag['smf71sni'] - df_pag['smf71lni']  # sni - lni
        df_pag['as_nvio_pgin_nswap_nblk'] = df_pag['smf71pin'] - df_pag['smf71sni'] - df_pag['smf71blk']  # pin-sni-blk
        df_pag['as_sum_pgout_nswap'] = df_pag['total_hspace_pgout_nswap'] + df_pag['total_vio_pgout_nswap'] + df_pag[
            'smf71pot']
        df_pag['as_sum_pgin_nswap_blk'] = df_pag['total_hspace_pgin_nswap_blk'] + df_pag['total_vio_pgin_nswap_blk'] + \
                                          df_pag['smf71blp']
        df_pag['as_sum_pgin_nswap_nblk'] = df_pag['smf71pin'] - df_pag['smf71sni']  # pin - sni
        df_pag['total_sum_pgout_nswap'] = df_pag['total_hspace_pgout_nswap'] + df_pag['total_vio_pgout_nswap'] + df_pag[
            'smf71pot']
        df_pag['total_sum_pgin_nswap_nblk'] = df_pag['smf71pin'] - df_pag['smf71sbi']
        df_pag['as_sum_pgout_swap'] = df_pag['smf71sot']  # sot
        df_pag['as_sum_pgin_swap'] = df_pag['smf71sin']
        df_pag['sys_sum_pgout_nswap'] = df_pag['smf71sno']
        df_pag['total_nvio_pgout_nswap'] = df_pag['smf71pot']
    else:
        df_pag = pd.DataFrame(columns=Smf71Pag.__table__.columns.keys()).set_index(
            ['csc', 'smf71sid', 'datetime', 'smf71ist', 'smf71iet'])
    return df_pag


def format_71df(df: pd.DataFrame) -> dict:
    """Format smf71 JSON files to the dataframes.

    Args:
        df: JSON dataframe.

    Returns:
        A dictionary of dataframes.
    """
    dfs_dict = {'pag': pd.DataFrame(), 'pro': pd.DataFrame()}

    if 'smf71pro' not in df.columns:
        return dfs_dict

    dfs_dict['pro'] = build_pro(df)

    if dfs_dict['pro'].empty:
        # Cannot continue processing
        return dfs_dict

    df.set_index(dfs_dict['pro'].index, inplace=True)

    dfs_dict['pag'] = build_pag(df)
    if 'smf71lvv' not in dfs_dict['pag'].columns:
        return {'pag': pd.DataFrame(), 'pro': pd.DataFrame()}

    return dfs_dict


def print_paging_activity_report(jsonfiles: tuple, lpar: str, start_time_str: str, end_time_str: str) -> str:
    """Print smf71 Paging Activity Report based on JSON files.

    Args:
        jsonfiles: JSON file or files.
        lpar: Target LPAR to print.
        start_time_str: Start time string.
        end_time_str: End time string.

    Returns:
        Paging activity report.
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
                    or df.iloc[0]['header'].get('recType') is None or df.iloc[0]['header']['recType'] != 71:
                click.echo(
                    f"\nInvalid JSON file {jsonfile}. This file will be skipped.")
                continue
            try:
                dfs_dict = format_71df(df)
            except Exception as e:
                click.echo(f"\nUnsupported JSON file {jsonfile} with error: {str(e)}. This file will be skipped.")
                continue

            if dfs_dict['pro'].empty:
                click.echo(
                    f"\nThis JSON file {jsonfile} is not for this smf type. This file will be skipped.")
                # Cannot continue processing
                continue

            page_detail = ''
            pro = dfs_dict['pro'].query("smf71ist > @start_time and smf71ist < @end_time and smf71sid == @sid"
                                       ).drop_duplicates().copy().reset_index().set_index(
                [col.name for col in Smf71Pro.__table__.primary_key.columns.values()])
            pag = dfs_dict['pag'].loc[~dfs_dict['pag'].index.duplicated(keep='first'), :].query(
                "smf71ist > @start_time and smf71ist < @end_time and smf71sid == @sid").copy().reset_index().set_index(
                [col.name for col in Smf71Pro.__table__.primary_key.columns.values()])
            for index in pag.index:
                pro_dict = pro.loc[[index]].reset_index().to_dict('records')[0]
                pag_dict = pag.loc[[index]].reset_index().to_dict('records')[0]

                page_sub_detail = format_central_storage_paging_rates(pro_dict, pag_dict)
                page_sub_detail += '\n\n'

                page_sub_detail += format_central_storage_movement_req_rates(pro_dict, pag_dict)
                page_sub_detail += '\n\n'

                page_sub_detail += format_frame_slot_counts(pro_dict, pag_dict)
                page_sub_detail += '\n\n'

                page_sub_detail += format_memory_obj(pro_dict, pag_dict)
                page_sub_detail += '\n\n'

                page_detail += page_sub_detail
            if page_detail != '':
                report += page_detail
    if report == '':
        return "No data found."
    return report

