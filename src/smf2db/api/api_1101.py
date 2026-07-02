from typing import Union

import click
import pandas as pd
import numpy as np
import tabulate as tb

from smf2db.db_models.smf1101_model import Smf1101
from smf2db.db_models.smf1101_rename import rename_110
from smf2db.api.util import to_localtime, col_to_frame, setdatetime

tb.PRESERVE_WHITESPACE = True


def format_1101df(df: pd.DataFrame) -> dict:
    """Format smf110 subtype 1 JSON files to the dataframes.

    Args:
        df: JSON dataframe.

    Returns:
        A dictionary of dataframes.
    """

    # inner function
    def check_existence(i: int, colname: str) -> bool:
        if isinstance(df.iloc[i][colname], list):
            return True
        elif not pd.isnull(df.iloc[i][colname]):
            return True
        else:
            return False

    check_col = np.vectorize(check_existence)
    convert_to_localtime = np.vectorize(to_localtime)
    set_datetime = np.vectorize(setdatetime)

    dfs_dict = {'dfhmntds': pd.DataFrame()}
    if 'dfhmntds' not in df.columns:
        return dfs_dict

    df_header = df['header'].apply(pd.Series)[
        ['recType', 'subType', 'sysId', 'smfmnrvn', 'smfmnprn', 'smfmnspn', 'smfmndto', 'smfmnjbn']].rename(
        columns={'sysId': 'smfmnsid'})
    df_header['has_dfhmntds'] = check_col(df_header.index, 'dfhmntds')
    df_header['smfmndto'] = pd.to_timedelta(df_header['smfmndto'])
    df_header['smfmnrvn'] = df_header['smfmnrvn'].str[2:]
    df_header.set_index(['smfmnsid', 'smfmnrvn', 'smfmnprn', 'smfmnspn', 'smfmndto', 'smfmnjbn', 'has_dfhmntds'],
                        inplace=True)
    index_110 = df_header.index[df_header.index.get_level_values('has_dfhmntds')]
    df.set_index(df_header.index, inplace=True)

    df_110 = col_to_frame(df[df.index.get_level_values('has_dfhmntds')], 'dfhmntds', index_110).rename(
        columns=rename_110)#.astype(dtype={"cics_phtranno": str, "cics_pttranno": str})
    astype_dict = {k: str for k in ['cics_phtranno', 'cics_pttranno'] if k in df_110.columns}
    df_110 = df_110.astype(dtype=astype_dict)

    if not df_110.empty:
        df_110['cics_rtype'] = df_110['cics_rtype'].str.lstrip()
        for column in [col for col in Smf1101.__table__.columns if
                       col.name in df_110.columns and
                       col not in [column for column in Smf1101.__table__.primary_key.columns.values()]]:
            first_col_value = df_110.iloc[0][column.name]
            if column.name in ['cics_phtranno', 'cics_pttranno']:
                df_110[column.name] = df_110[column.name].apply(lambda x: x.replace('.0', '') if not pd.isna(x) else x)
            if 'DATETIME' in str(column.type):
                if not pd.isna(first_col_value) and len(first_col_value) >= 22:
                    col_format = '%Y-%m-%d %H:%M:%S.%f'
                else:
                    col_format = '%Y-%m-%d %H:%M:%S'
                df_110[column.name] = pd.to_datetime(df_110[column.name], errors='coerce',
                                                           format=col_format)

            elif 'FLOAT' in str(column.type):
                if not df_110[column.name].str.contains(':').all():
                    df_110.update(
                        df_110[column.name].mask(df_110[column.name].str.contains("0x"), '00:00:00.000000'))

                df_110[column.name] = pd.to_timedelta(df_110[column.name]) / np.timedelta64(1, 's')
            elif 'INTEGER' in str(column.type) and df_110[column.name].dtype not in [np.int64,
                                                                                           np.float64] and '0x' in first_col_value:
                df_110[column.name] = df_110[column.name].apply(
                    lambda x: int(x, base=16) if pd.notnull(x) and x not in ['0xFFFFFFFF'] else np.nan)
                df_110[column.name] = df_110[column.name].apply(
                    lambda x: x if pd.notnull(x) and x != 4294967295 else np.nan)
            elif 'BIGINT' in str(column.type):
                df_110[column.name] = df_110[column.name].apply(
                    lambda x: x if pd.notnull(x) and x != 4294967295 else np.nan)
            elif 'INTEGER' in str(column.type):
                df_110[column.name] = df_110[column.name].apply(
                    lambda x: int(x, 16) if isinstance(x, str) and '0x' in x else x)
                df_110[column.name] = df_110[column.name].apply(
                    lambda x: x if pd.notnull(x) and x != 4294967295 else np.nan)
            elif 'VARCHAR(1)' in str(column.type):
                df_110[column.name] = df_110[column.name].apply(
                    lambda x: bytes.fromhex(x[2:]).decode('cp500') if '0x' in x and bytes.fromhex(x[2:]).decode('cp500').isprintable() else np.nan if len(x) > 1 else x)
        drop_columns = list(set(df_110.columns) - set(Smf1101.__table__.columns.keys()))
        df_110['cics_start'] = pd.to_datetime(df_110['cics_start']) + df_110['smfmndto']
        df_110['cics_stop'] = pd.to_datetime(df_110['cics_stop']) + df_110['smfmndto']
        df_110['cics_ostart'] = convert_to_localtime(df_110['cics_ostart'], df_110['smfmndto'])
        df_110['cics_phstart'] = convert_to_localtime(df_110['cics_phstart'], df_110['smfmndto'])
        dfs_dict['dfhmntds'] = df_110.copy().drop(columns=drop_columns)
        dfs_dict['dfhmntds']['elapsed'] = (dfs_dict['dfhmntds']['cics_stop'] - dfs_dict['dfhmntds']['cics_start']) / np.timedelta64(1, 's')
        dfs_dict['dfhmntds']['datetime_15m'] = dfs_dict['dfhmntds']['cics_stop'].dt.floor('15min')
        dfs_dict['dfhmntds']['datetime'] = set_datetime(dfs_dict['dfhmntds']['cics_stop'])
        dfs_dict['dfhmntds'] = dfs_dict['dfhmntds'].set_index(
            ['smfmnsid', 'smfmnprn', 'smfmnspn', 'task_tran', 'cics_start', 'task_trannum', 'elapsed'])

    return dfs_dict


def print_cics_performance_report(jsonfiles: tuple, start_time_str: str, end_time_str: str,
                                  specific_appl: Union[str, None] = None, exclude_trans_starts: Union[str, None] = None) -> str:
    """Print CICS Performance Report based on JSON files.

    Args:
        jsonfiles: JSON file or files.
        start_time_str: Start time string.
        end_time_str: End time string.
        specific_appl: Specific applid to include.
        exclude_trans_starts: Exclude transactions starting with.

    Returns:
        CICS Performance report.
    """
    start_time = pd.to_datetime(start_time_str)
    end_time = pd.to_datetime(end_time_str)

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
                    or df.iloc[0]['header'].get('recType') is None or df.iloc[0]['header']['recType'] != 110:
                click.echo(
                    f"\nInvalid JSON file {jsonfile}. This file will be skipped.")
                continue
            try:
                df_dict = format_1101df(df)
            except Exception as e:
                click.echo(f"\nUnsupported JSON file {jsonfile} with error: {str(e)}. This file will be skipped.")
                continue

            if df_dict['dfhmntds'].empty:
                click.echo(
                    f"\nThis JSON file {jsonfile} is not for this smf type. This file will be skipped.")
                # Cannot continue processing
                continue

            metrics_cols = ['smfmnprn', 'cics_start', 'cics_stop', 'task_tran', 'task_usrcput', 'elapsed', 'task_usrdispt',
                            'task_susptime', 'sync_synctime', 'task_rmitime', 'file_fciowtt', 'jour_jciowtt',
                            'task_dspdelay', 'task_dispwtt', 'file_fcamct', 'file_fctotct', 'term_iriowtt',
                            'stor_scusrhwm', 'stor_scusrhwm_a']
            if specific_appl is not None and exclude_trans_starts is not None:
                metrics_df = df_dict['dfhmntds'].reset_index().query(
                                "cics_start > @start_time and cics_start < @end_time and smfmnprn == @specific_appl and not task_tran.str.startswith(@exclude_trans_starts)"
                )[metrics_cols]
            elif specific_appl is not None:
                metrics_df = df_dict['dfhmntds'].reset_index().query(
                    "cics_start > @start_time and cics_start < @end_time and smfmnprn == @specific_appl"
                )[metrics_cols]
            elif exclude_trans_starts is not None:
                metrics_df = df_dict['dfhmntds'].reset_index().query(
                    "cics_start > @start_time and cics_start < @end_time and not task_tran.str.startswith(@exclude_trans_starts)"
                )[metrics_cols]
            else:
                metrics_df = df_dict['dfhmntds'].reset_index().query(
                    "cics_start > @start_time and cics_start < @end_time"
                )[metrics_cols]

            if metrics_df.empty:
                continue

            metrics_gp = metrics_df.groupby(['smfmnprn', 'task_tran']).agg({
                'cics_start': ['count'],
                'elapsed': ['mean', 'max'],
                'task_usrdispt': ['mean'],
                'task_usrcput': ['mean'],
                'task_susptime': ['mean', 'max'],
                'task_dispwtt': ['mean'],
                'file_fciowtt': ['mean'],
                'file_fcamct': ['mean'],
                'term_iriowtt': ['mean'],
                'stor_scusrhwm': ['mean'],
                'stor_scusrhwm_a': ['mean'],
            }).reset_index()
            for col_name in metrics_gp.columns:
                metrics_gp[col_name] = metrics_gp[col_name].replace(to_replace=[np.nan], value=None)
            metrics_gp.columns = ['Appl\nId', '\nTran',
                                  '\n#Tasks', 'Avg\nResponse', 'Max\nResponse', 'Avg\nDispatch', 'Avg\nUser CPU',
                                  'Avg\nSuspend', 'Max\nSuspend', 'Avg\nDispWait', 'Avg\nFC Wait', 'Avg\nFCAMRq',
                                  'Avg\nIR Wait', 'Avg\nSC24UHW', 'Avg\nSC31UHWM']
            if metrics_gp.shape[0] > 0:
                header1 = [["                                              C I C S    P E R F O R M A N C E    R E P O R T"]]
                header2 = [[f"                                          Data from   {start_time: %Y/%m/%d %H:%M}    to   {end_time:%Y/%m/%d %H:%M}"]]
                report += tb.tabulate(header1, tablefmt="plain") + "\n" + tb.tabulate(header2, tablefmt="plain") + "\n"
                report += tb.tabulate(
                    metrics_gp, headers='keys', tablefmt='psql', showindex=False,
                floatfmt=('','','.0f','.04f','.04f','.04f','.04f','.04f','.04f','.04f','.04f','.0f','.04f','.0f','.0f'),)

    return report

