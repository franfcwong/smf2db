import click
import pandas as pd
import numpy as np
import datetime as dt
import tabulate as tb
from smf2db.db_models.smf123_model import Smf123Server,  Smf123RequestData
from smf2db.api.util import time_diff, col_to_frame, is_bit_set, setdatetime

tb.PRESERVE_WHITESPACE = True

def to_localtime(t: str, o: str):
    """Convert the time to local time.

    Args:
        t (str): The time to convert.
        o (str): The time offset.

    Returns:
        str: The converted time.
    """
    if not pd.isnull(t):
        return pd.to_datetime(t, format='%Y-%m-%d %H:%M:%S.%f', errors='coerce') + pd.to_timedelta(o)
    else:
        return pd.NaT


def format_123df(df: pd.DataFrame, current_time: dt.datetime) -> dict:
    """Format smf123 JSON files to the dataframes.

    Args:
        df: JSON dataframe.
        current_time: Current datetime object.

    Returns:
        A dictionary of dataframes.
    """
    convert_to_localtime = np.vectorize(to_localtime, otypes=['object'])
    get_time_diff = np.vectorize(time_diff)
    set_datetime = np.vectorize(setdatetime)

    dfs_dict = {'server': pd.DataFrame(), 'data': pd.DataFrame()}
    if 'serverSection' not in df.columns:
        return dfs_dict

    dfs_dict['server'] = pd.concat([df['header'].apply(pd.Series),
                                    df['serverSection'].apply(pd.Series)], axis=1
                                   ).rename(columns={'smf123_datetime': 'smf123_timestamp'})

    dfs_dict['server']['smf123_timestamp'] = pd.to_datetime(dfs_dict['server']['smf123_timestamp'])
    dfs_dict['server']['datetime_15m'] = dfs_dict['server']['smf123_timestamp'].dt.floor('15min')
    dfs_dict['server']['datetime'] = set_datetime(dfs_dict['server']['smf123_timestamp'])
    dfs_dict['server']['last_update_time'] = current_time
    index_column = [col.name for col in Smf123Server.__table__.primary_key.columns.values()] + [
        'smf123_datetime_offset']
    index_123 = dfs_dict['server'][(dfs_dict['server']['smf123_subtype'] == 1) & (dfs_dict['server']['smf123_subtype_version'] == 2)
                          ].set_index(index_column).index
    dfs_dict['server'].set_index([col.name for col in Smf123Server.__table__.primary_key.columns.values()
                         ] + ['smf123_datetime_offset', 'smf123_subtype', 'smf123_subtype_version'],
                        inplace=True)

    df.set_index(dfs_dict['server'].index, inplace=True)

    dfs_dict['data'] = col_to_frame(df[(df.index.get_level_values('smf123_subtype') == 1) & (
            df.index.get_level_values('smf123_subtype_version') == 2)], 'reqDataSection', index_123)
    dfs_dict['data']['datetime_15m'] = dfs_dict['data']['smf123_timestamp'].dt.floor('15min')
    dfs_dict['data']['datetime'] = set_datetime(dfs_dict['data']['smf123_timestamp'])
    dfs_dict['data']['smf123s1_time_zc_entry'] = convert_to_localtime(dfs_dict['data']['smf123s1_time_zc_entry'],
                                                             dfs_dict['data']['smf123_datetime_offset'])
    dfs_dict['data']['smf123s1_time_zc_exit'] = convert_to_localtime(dfs_dict['data']['smf123s1_time_zc_exit'],
                                                            dfs_dict['data']['smf123_datetime_offset'])
    dfs_dict['data']['smf123s1_time_sor_sent'] = convert_to_localtime(dfs_dict['data']['smf123s1_time_sor_sent'],
                                                             dfs_dict['data']['smf123_datetime_offset'])
    dfs_dict['data']['smf123s1_time_sor_recv'] = convert_to_localtime(dfs_dict['data']['smf123s1_time_sor_recv'],
                                                             dfs_dict['data']['smf123_datetime_offset'])
    dfs_dict['data']['sent_late'] = get_time_diff(dfs_dict['data']['smf123s1_time_sor_sent'], dfs_dict['data']['smf123s1_time_zc_entry'])
    dfs_dict['data']['exit_late'] = get_time_diff(dfs_dict['data']['smf123s1_time_zc_exit'], dfs_dict['data']['smf123s1_time_sor_recv'])
    dfs_dict['data']['sor_resp'] = get_time_diff(dfs_dict['data']['smf123s1_time_sor_recv'], dfs_dict['data']['smf123s1_time_sor_sent'])
    dfs_dict['data']['zc_resp'] = get_time_diff(dfs_dict['data']['smf123s1_time_zc_exit'], dfs_dict['data']['smf123s1_time_zc_entry'])
    dfs_dict['data']['zc_time'] = dfs_dict['data']['zc_resp'] - dfs_dict['data']['sor_resp']
    dfs_dict['data']['smf123s1_resp_flags'] = dfs_dict['data']['smf123s1_resp_flags'].apply(lambda x: int(str(x), 16))
    dfs_dict['data']['timed_out'] = dfs_dict['data']['smf123s1_resp_flags'].apply(lambda x: is_bit_set(x, 8, 0))
    dfs_dict['data'].set_index([col.name for col in Smf123RequestData.__table__.primary_key.columns.values()],
                      inplace=True)
    # print(dfs_dict['data'].reset_index().to_string())
    return dfs_dict

def print_zcee_request_report(jsonfiles: tuple, start_time_str: str, end_time_str: str) -> str:
    """Print smf123 Request Activity Report based on JSON files.

    Args:
        jsonfiles: JSON file or files.
        start_time_str: Start time string.
        end_time_str: End time string.

    Returns:
        Address Space activity report.
    """
    start_time = pd.to_datetime(start_time_str)
    end_time = pd.to_datetime(end_time_str)
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
                    or df.iloc[0]['header'].get('smf123_rec_type') is None or df.iloc[0]['header']['smf123_rec_type'] != 123:
                click.echo(
                    f"\nInvalid JSON file {jsonfile}. This file will be skipped.")
                continue
            elif 'reqDataSection' not in df.columns:
                click.echo(
                    f"\nInvalid JSON file {jsonfile}. This file will be skipped.")
                continue
            try:
                df_dict = format_123df(df, current_time)
            except Exception as e:
                click.echo(f"\nUnsupported JSON file {jsonfile} with error: {str(e)}. This file will be skipped.")
                continue

            if df_dict['data'].empty:
                click.echo(
                    f"\nThis JSON file {jsonfile} is not for this smf type. This file will be skipped.")
                # Cannot continue processing
                continue

            data_tbl = df_dict['data'].query(
                "smf123_timestamp >= @start_time and smf123_timestamp <= @end_time").reset_index()
            if data_tbl.empty:
                continue

            data_df = pd.concat([data_tbl[['smf123_server_jobname', 'smf123_sid', #'smf123_ssi',
                                           'smf123s1_req_id']].rename(
                                    columns={'smf123_server_jobname':'\nJobname',
                                             'smf123_sid':'\nSID', 'smf123s1_req_id':'Req\nId'}),
                                 data_tbl['smf123s1_api_name'].str[:40].rename('\nAPI Name'),
                                 data_tbl[['smf123s1_api_version', 'smf123s1_req_method','smf123s1_http_resp_code',
                                           'smf123s1_sor_identifier']].rename(
                                     columns={'smf123s1_api_version':'API\nVRM', 'smf123s1_req_method':'Req\nMethod',
                                              'smf123s1_http_resp_code':'Resp\nCode',
                                              'smf123s1_sor_identifier':'\nSOR Id'}),
                                 data_tbl['smf123s1_time_zc_entry'].dt.strftime('%Y-%m-%d %H:%M:%S.%f').rename('\nZC Entry'),
                                 data_tbl[['zc_resp', 'sent_late', 'sor_resp', 'exit_late', 'zc_time']
                                 ].replace([np.nan, np.inf], None).rename(
                                     columns={'zc_resp':'\nZC Resp', 'sent_late':'\nSent Late', 'sor_resp':'\nSOR Resp',
                                              'exit_late':'\nSOR Late', 'zc_time':'\nZC Time'})
                ], axis=1)
            if not data_df.empty:
                header1 = [
                    ["                                              Z / O S    C O N N E C T    E E    P E R F O R M A N C E    R E P O R T"]]
                header2 = [
                    [f"                                                   Data from   {start_time: %Y/%m/%d %H:%M}    to   {end_time:%Y/%m/%d %H:%M}"]]
                report += tb.tabulate(header1, tablefmt="plain") + "\n" + tb.tabulate(header2, tablefmt="plain") + "\n"
                report += tb.tabulate(
                    data_df, headers='keys', tablefmt='psql', showindex=False,
                    floatfmt=('','','','','','','','','','','','.6f','.6f','.6f','.6f','.6f'))
                report += "\n"

    if report == '':
        report = 'No data found.'
    return report

