from typing import Union

import click
import numpy as np
import pandas as pd

from smf2db.api.report_util import format_enq_activity
from smf2db.api.util import setdatetime, col_to_frame, is_bit_set
from smf2db.db_models.smf77_model import Smf77Enq, Smf77Ctl


def build_pro(df: pd.DataFrame) -> Union[pd.DataFrame, None]:
    """Build the dataframe for RMF Product Section which will be uploaded to smf77_pro table.

    Args:
        df: The master dataframe which is created from the JSON file.

    Returns:
        The dataframe for the RMF product section or None if csc is not found in the database.
    """
    set_datetime = np.vectorize(setdatetime)
    df_pro = pd.concat([df['header'].apply(pd.Series),
                        df['smf77pro'].apply(pd.Series)],
                       axis=1).rename(
        columns={'sysId': 'smf77sid',
                 'sysInd': 'smf77flg', 'recType': 'smf_type'})

    df_pro['csc'] = np.nan
    df_pro['smf77sid'] = df_pro['smf77sid'].str.strip()
    df_pro['smf77ist'] = pd.to_datetime(df_pro['smf77ist'])
    df_pro['smf77gie'] = pd.to_datetime(df_pro['smf77gie'])
    df_pro['smf77int'] = pd.to_timedelta(df_pro['smf77int']) / np.timedelta64(1, 's')
    df_pro['smf77lgo'] = pd.to_timedelta(df_pro['smf77lgo']) / np.timedelta64(1, 'h')
    df_pro['datetime'] = set_datetime(df_pro['smf77ist'])
    df_pro['smf77flg'] = df_pro['smf77flg'].apply(lambda x: int(str(x), 16))
    df_pro['smf77fla'] = df_pro['smf77fla'].apply(lambda x: int(str(x), 16))
    df_pro['smf77prf'] = df_pro['smf77prf'].apply(lambda x: int(str(x), 16))
    df_pro['smf77srl'] = df_pro['smf77srl'].apply(lambda x: int(str(x), 16))
    df_pro['speed_boost'] = df_pro['smf77fla'].apply(lambda x: is_bit_set(x, 16, 10))
    df_pro['ziip_boost'] = df_pro['smf77fla'].apply(lambda x: is_bit_set(x, 16, 9))
    df_pro['smf_type'] = df_pro['smf_type'].astype(str) + '.' + df_pro['subType'].astype(str)
    df_pro = df_pro.set_index(
        ['datetime', 'smf77ist', 'smf77iet', 'smf_type', 'csc', 'smf77sid', 'smf77int', 'smf77sam'])
    return df_pro


def build_ctl(df: pd.DataFrame, df_pro_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for Enqueue Control Section which will be uploaded to smf77_ctl table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_pro_idx: The index of the RMF product section dataframe.

    Returns:
        The dataframe for the Enqueue Control section.
    """
    if 'smf77ctl' in df.columns:
        df_ctl = col_to_frame(df[df.index.get_level_values('smf_type') == '77.1'], 'smf77ctl', df_pro_idx)
        df_ctl['smf77fg1'] = df_ctl['smf77fg1'].apply(lambda x: int(str(x), 16))
        df_ctl['smf77rf2'] = df_ctl['smf77rf2'].apply(lambda x: int(str(x), 16))
        df_ctl['resource_no_contention'] = df_ctl['smf77fg1'].apply(lambda x: is_bit_set(x, 8, 1))
        df_ctl['enqueue_bad_cpu_clock'] = df_ctl['smf77fg1'].apply(lambda x: is_bit_set(x, 8, 2))
        df_ctl['enqueue_processing_abend'] = df_ctl['smf77fg1'].apply(lambda x: is_bit_set(x, 8, 3))
        df_ctl['detail_data_req'] = df_ctl['smf77fg1'].apply(lambda x: is_bit_set(x, 8, 4))
        df_ctl['grs_none'] = df_ctl['smf77fg1'].apply(lambda x: is_bit_set(x, 8, 5))
        df_ctl['grs_ring'] = df_ctl['smf77fg1'].apply(lambda x: is_bit_set(x, 8, 6))
        df_ctl['grs_mode'] = df_ctl['smf77fg1'].apply(lambda x: is_bit_set(x, 8, 7))
        df_ctl['grs_sys_problem'] = df_ctl['smf77rf2'].apply(lambda x: is_bit_set(x, 8, 0))
        df_ctl['grs_interface_problem'] = df_ctl['smf77rf2'].apply(lambda x: is_bit_set(x, 8, 1))
        df_ctl = df_ctl.reset_index()[Smf77Ctl.__table__.columns.keys()].set_index(
            [col.name for col in Smf77Ctl.__table__.primary_key.columns.values()])
    else:
        df_ctl = pd.DataFrame(columns=Smf77Ctl.__table__.columns.keys()).set_index(
            [col.name for col in Smf77Ctl.__table__.primary_key.columns.values()])
    return df_ctl


def build_enq(df: pd.DataFrame, df_pro_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for Enqueue Data Section which will be uploaded to smf77_enq table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_pro_idx: The index of the RMF product section dataframe.

    Returns:
        The dataframe for the Enqueue Data section.
    """
    if 'smf77enq' in df.columns:
        df_enq = col_to_frame(df[df.index.get_level_values('smf_type') == '77.1'], 'smf77enq', df_pro_idx)
        df_enq['date'] = df_enq['datetime'].dt.date
        df_enq['smf77rnm'] = df_enq['smf77rnm'].str[2:]
        df_enq['smf77dfg'] = df_enq['smf77dfg'].apply(lambda x: int(str(x), 16))
        df_enq['system_scope'] = df_enq['smf77dfg'].apply(lambda x: is_bit_set(x, 8, 1))
        df_enq['smf77wtm'] = pd.to_timedelta(df_enq['smf77wtm']) / np.timedelta64(1, 's')
        df_enq['smf77wtx'] = pd.to_timedelta(df_enq['smf77wtx']) / np.timedelta64(1, 's')
        df_enq['smf77wtt'] = pd.to_timedelta(df_enq['smf77wtt']) / np.timedelta64(1, 's')
        df_enq['resource_contention'] = df_enq['smf77dfg'].apply(lambda x: is_bit_set(x, 8, 0))
        df_enq['exclusive_owner'] = df_enq['smf77dfg'].apply(lambda x: is_bit_set(x, 8, 2))
        df_enq['job_wait_for_exc_usage'] = df_enq['smf77dfg'].apply(lambda x: is_bit_set(x, 8, 3))
        df_enq['job_wait_for_2exc_usage'] = df_enq['smf77dfg'].apply(lambda x: is_bit_set(x, 8, 4))
        df_enq['global_resource'] = df_enq['smf77dfg'].apply(lambda x: is_bit_set(x, 8, 5))
        df_enq['idx'] = df_enq.groupby(['smf77sid', 'datetime', 'smf77ist', 'smf77iet', 'smf77qnm', 'smf77rnm']).cumcount()
        df_enq = df_enq.reset_index()[Smf77Enq.__table__.columns.keys()].set_index(
            [col.name for col in Smf77Enq.__table__.primary_key.columns.values()])
    else:
        df_enq = pd.DataFrame(columns=Smf77Enq.__table__.columns.keys()).set_index(
            [col.name for col in Smf77Enq.__table__.primary_key.columns.values()])
    return df_enq


def format_77df(df: pd.DataFrame) -> dict:
    """Format smf77 JSON files to the dataframes.

    Args:
        df: JSON dataframe.

    Returns:
        A dictionary of dataframes.
    """
    dfs_dict = {'ctl': pd.DataFrame(), 'enq': pd.DataFrame(), 'pro': pd.DataFrame()}

    if 'smf77pro' not in df.columns:
        return dfs_dict
    else:
        dfs_dict['pro'] = build_pro(df)

    if dfs_dict['pro'].empty:
        # Cannot continue processing
        return dfs_dict

    df.set_index(dfs_dict['pro'].index, inplace=True)

    dfs_dict['ctl'] = build_ctl(df, dfs_dict['pro'][dfs_dict['pro'].index.get_level_values('smf_type') == '77.1'].index)

    dfs_dict['enq'] = build_enq(df, dfs_dict['pro'][dfs_dict['pro'].index.get_level_values('smf_type') == '77.1'].index)

    return dfs_dict


def print_enq_activity_report(jsonfiles: tuple, lpar: str, start_time_str: str, end_time_str: str) -> str:
    """Print smf77 Page Data Set Activity Report based on JSON files.

    Args:
        jsonfiles: JSON file or files.
        lpar: Target LPAR to print.
        start_time_str: Start time string.
        end_time_str: End time string.

    Returns:
        Enqueue activity report.
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
                    or df.iloc[0]['header'].get('recType') is None or df.iloc[0]['header']['recType'] != 77:
                click.echo(
                    f"\nInvalid JSON file {jsonfile}. This file will be skipped.")
                continue
            try:
                dfs_dict = format_77df(df)
            except Exception as e:
                click.echo(f"\nUnsupported JSON file {jsonfile} with error: {str(e)}. This file will be skipped.")
                continue

            page_detail = ''
            if dfs_dict['pro'].empty:
                click.echo(
                    f"\nThis JSON file {jsonfile} is not for this smf type. This file will be skipped.")
                # Cannot continue processing
                continue

            pro = dfs_dict['pro'].query("smf77ist > @start_time and smf77ist < @end_time and smf77sid == @sid"
                                       ).drop_duplicates().copy().reset_index().set_index(
                [col.name for col in Smf77Ctl.__table__.primary_key.columns.values()])
            ctl = dfs_dict['ctl'].query("smf77ist > @start_time and smf77ist < @end_time and smf77sid == @sid"
                                        ).drop_duplicates().copy().reset_index().set_index(
                [col.name for col in Smf77Ctl.__table__.primary_key.columns.values()])
            enq = dfs_dict['enq'].query("smf77ist > @start_time and smf77ist < @end_time and smf77sid == @sid"
                                        ).drop_duplicates().copy().reset_index().set_index(
                [col.name for col in Smf77Ctl.__table__.primary_key.columns.values()])

            if ctl.empty:
                continue

            for index in ctl.index:
                pro_dict = pro.loc[[index]].reset_index().to_dict('records')[0]
                ctl_dict = ctl.loc[[index]].reset_index().to_dict('records')[0]
                if enq.empty or index not in enq.index:
                    enqs_dict = []
                else:
                    enqs_dict = enq.loc[[index]].reset_index().to_dict('records')
                if len(enqs_dict) > 0:
                    page_detail += format_enq_activity(pro_dict, ctl_dict, enqs_dict)
                    page_detail += '\n\n'
            if page_detail != '':
                report += page_detail
    if report == '':
        report = 'No data found.'
    return report
