from typing import Union

import click
import pandas as pd
import numpy as np

from smf2db.api.report_util import format_psd_activity
from smf2db.db_models.smf75_model import Smf75Pro, Smf75Psd
from smf2db.api.util import setdatetime, col_to_frame, is_bit_set


def build_pro(df: pd.DataFrame) -> Union[pd.DataFrame, None]:
    """Build the dataframe for RMF Product Section which will be uploaded to smf75_pro table.

    Args:
        df: The master dataframe which is created from the JSON file.

    Returns:
        The dataframe for the RMF product section or None if csc is not found in the database.
    """
    set_datetime = np.vectorize(setdatetime)
    df_pro = pd.concat([df['header'].apply(pd.Series),
                        df['smf75pro'].apply(pd.Series)],
                       axis=1).rename(
        columns={'sysId': 'smf75sid',
                 'sysInd': 'smf75flg', 'recType': 'smf_type'})

    df_pro['csc'] = np.nan
    df_pro['smf75sid'] = df_pro['smf75sid'].str.strip()
    df_pro['smf75ist'] = pd.to_datetime(df_pro['smf75ist'])
    df_pro['smf75gie'] = pd.to_datetime(df_pro['smf75gie'])
    df_pro['smf75int'] = pd.to_timedelta(df_pro['smf75int']) / np.timedelta64(1, 's')
    df_pro['smf75lgo'] = pd.to_timedelta(df_pro['smf75lgo']) / np.timedelta64(1, 'h')
    df_pro['datetime'] = set_datetime(df_pro['smf75ist'])
    df_pro['smf75flg'] = df_pro['smf75flg'].apply(lambda x: int(str(x), 16))
    df_pro['smf75fla'] = df_pro['smf75fla'].apply(lambda x: int(str(x), 16))
    df_pro['smf75prf'] = df_pro['smf75prf'].apply(lambda x: int(str(x), 16))
    df_pro['smf75srl'] = df_pro['smf75srl'].apply(lambda x: int(str(x), 16))
    df_pro['speed_boost'] = df_pro['smf75fla'].apply(lambda x: is_bit_set(x, 16, 10))
    df_pro['ziip_boost'] = df_pro['smf75fla'].apply(lambda x: is_bit_set(x, 16, 9))
    df_pro['smf_type'] = df_pro['smf_type'].astype(str) + '.' + df_pro['subType'].astype(str)
    df_pro = df_pro.set_index(
        ['datetime', 'smf75ist', 'smf75iet', 'smf_type', 'csc', 'smf75sid', 'smf75int', 'smf75sam'])
    return df_pro


def build_psd(df: pd.DataFrame, df_pro_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for Page Data Set Data Section which will be uploaded to smf75_psd table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_pro_idx: The index of the RMF product section dataframe.

    Returns:
        The dataframe for the Page Data Set Data section.
    """
    if 'smf75psd' in df.columns:
        df_psd = col_to_frame(df[df.index.get_level_values('smf_type') == '75.1'], 'smf75psd', df_pro_idx#
        ).reset_index().set_index(['csc', 'smf75sid', 'datetime', 'smf75ist', 'smf75iet'])
        df_psd['smf75pst'] = df_psd['smf75pst'].apply(lambda x: int(str(x), 16))
        df_psd['smf75fl2'] = df_psd['smf75fl2'].apply(lambda x: int(str(x), 16))
        df_psd['lpa'] = df_psd['smf75pst'].apply(lambda x: is_bit_set(x, 8, 0))
        df_psd['com'] = df_psd['smf75pst'].apply(lambda x: is_bit_set(x, 8, 1))
        df_psd['loc'] = df_psd['smf75pst'].apply(lambda x: is_bit_set(x, 8, 3))
        df_psd['dsb'] = df_psd['smf75pst'].apply(lambda x: is_bit_set(x, 8, 5))
        df_psd['onl'] = df_psd['smf75pst'].apply(lambda x: is_bit_set(x, 8, 6))
        df_psd['ofl'] = df_psd['smf75pst'].apply(lambda x: is_bit_set(x, 8, 7))
        df_psd['ds_accepts_vio'] = df_psd['smf75fl2'].apply(lambda x: is_bit_set(x, 8, 0))
        df_psd['ds_on_alt_control_unit'] = df_psd['smf75fl2'].apply(lambda x: is_bit_set(x, 8, 2))
        df_psd['device_name_valid'] = df_psd['smf75fl2'].apply(lambda x: is_bit_set(x, 8, 3))
        df_psd['page_space_scm'] = df_psd['smf75fl2'].apply(lambda x: is_bit_set(x, 8, 4))
        df_psd['smf75typ'] = df_psd['smf75typ'].str[2:]
        df_psd['smf75cha'] = df_psd['smf75cha'].str[2:]
        df_psd['psbsy'] = df_psd['smf75use'] * 100 / df_psd['smf75sam']
        df_psd['psptt'] = ((df_psd['smf75req'] * df_psd['smf75int']) / df_psd['smf75sam']) / df_psd['smf75pgx']
        df_psd['pspt'] = df_psd['smf75pgx'] / df_psd['smf75int']
        df_psd['psart'] = df_psd['smf75sio'] / df_psd['smf75int']
        if 'smf75lvu' not in df_psd.columns:
            df_psd['smf75lvu'] = np.nan
        df_psd = df_psd.reset_index()[Smf75Psd.__table__.columns.keys()].set_index(
            [col.name for col in Smf75Psd.__table__.primary_key.columns.values()])
    else:
        df_psd = pd.DataFrame(columns=Smf75Psd.__table__.columns.keys()).set_index(
            [col.name for col in Smf75Psd.__table__.primary_key.columns.values()])
    return df_psd


def format_75df(df: pd.DataFrame) -> dict:
    """Format smf75 JSON files to the dataframes.

    Args:
        df: JSON dataframe.

    Returns:
        A dictionary of dataframes.
    """
    dfs_dict = {'psd': pd.DataFrame(), 'pro': pd.DataFrame()}

    if 'smf75pro' not in df.columns:
        return dfs_dict
    else:
        dfs_dict['pro'] = build_pro(df)

    if dfs_dict['pro'].empty:
        # Cannot continue processing
        return dfs_dict

    df.set_index(dfs_dict['pro'].index, inplace=True)

    dfs_dict['psd'] = build_psd(df, dfs_dict['pro'].index)

    return dfs_dict


def print_psd_activity_report(jsonfiles: tuple, lpar: str, start_time_str: str, end_time_str: str) -> str:
    """Print smf75 Page Data Set Activity Report based on JSON files.

    Args:
        jsonfiles: JSON file or files.
        lpar: Target LPAR to print.
        start_time_str: Start time string.
        end_time_str: End time string.

    Returns:
        Page Data Set activity report.
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
                    or df.iloc[0]['header'].get('recType') is None or df.iloc[0]['header']['recType'] != 75:
                click.echo(
                    f"\nInvalid JSON file {jsonfile}. This file will be skipped.")
                continue
            try:
                dfs_dict = format_75df(df)
            except Exception as e:
                click.echo(f"\nUnsupported JSON file {jsonfile} with error: {str(e)}. This file will be skipped.")
                continue

            if dfs_dict['pro'].empty:
                click.echo(
                    f"\nThis JSON file {jsonfile} is not for this smf type. This file will be skipped.")
                # Cannot continue processing
                continue
            page_detail = ''
            pro = dfs_dict['pro'].query("smf75ist > @start_time and smf75ist < @end_time and smf75sid == @sid"
                                       ).drop_duplicates().copy().reset_index().set_index(
                [col.name for col in Smf75Pro.__table__.primary_key.columns.values()])
            psd = dfs_dict['psd'].query("smf75ist > @start_time and smf75ist < @end_time and smf75sid == @sid"
                                        ).drop_duplicates().copy().reset_index().set_index(
                [col.name for col in Smf75Pro.__table__.primary_key.columns.values()])

            if pro.empty:
                continue

            for index in pro.index:
                pro_dict = pro.loc[[index]].reset_index().to_dict('records')[0]
                if psd.empty or index not in psd.index:
                    psds_dict = []
                else:
                    psds_dict = psd.loc[[index]].reset_index().to_dict('records')

                if len(psds_dict) > 0:
                    page_detail += format_psd_activity(pro_dict, psds_dict)
                    page_detail += '\n\n'
            if page_detail != '':
                report += page_detail
    if report == '':
        return "No data found."
    return report

