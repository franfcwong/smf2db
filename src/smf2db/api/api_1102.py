import sys
from typing import Union

import click
import numpy as np
import pandas as pd
import sqlalchemy
import tabulate

from smf2db.api.util import setdatetime, converttolist, col_to_frame, cols_to_frame, x_divided_by_y
from smf2db.db_models.smf1102_model import *

tabulate.PRESERVE_WHITESPACE = True


def build_structure(target_structure: Union[str, list, tuple], df_whole: pd.DataFrame,
                    structure_class: sqlalchemy.orm.DeclarativeBase, extra_columns: list = None,
                    extra_index: pd.Index = None) -> pd.DataFrame:
    """Create the dataframe based on the target structure from the JSON dataframe.

    Args:
        target_structure (Union[str, list, tuple]): Target structure from the JSON dataframe.
        df_whole (pd.DataFrame): Whole dataframe from the JSON file.
        structure_class (sqlalchemy.orm.base): Structure class from the DB model.
        extra_columns (list): Extra columns to be added to the dataframe.
        extra_index (pd.DataFrame.index): Extra index to be included druing the generation of the dataframe.

    Returns:
        pd.DataFrame: Structure dataframe.
    """
    if isinstance(target_structure, str):
        if target_structure in df_whole.columns:
            structure_df = col_to_frame(df_whole, target_structure, df_whole.index)
            structure_df = structure_df[[col for col in structure_df.columns if col in
                                         structure_class.__table__.columns.keys()]].set_index(
                [col.name for col in structure_class.__table__.primary_key.columns.values()])
        else:
            structure_df = pd.DataFrame(columns=structure_class.__table__.columns.keys()).set_index(
                [col.name for col in structure_class.__table__.primary_key.columns.values()])
    elif isinstance(target_structure, tuple):  # multiple layers structure
        if len(target_structure) >= 2 and target_structure[0] in df_whole.columns:
            if extra_columns is None:
                new_df = df_whole[target_structure[0]].apply(pd.Series)
                structure_df = col_to_frame(new_df, target_structure[1], df_whole.index)
            else:
                new_index_columns = [col.name for col in
                                     structure_class.__table__.primary_key.columns.values()] + extra_columns
                new_df = df_whole[target_structure[0]].apply(pd.Series)
                structure_df = col_to_frame(new_df, target_structure[1],
                                            new_df.reset_index().set_index(new_index_columns).index)
            if extra_index is None:
                structure_df = structure_df[[col for col in structure_df.columns if col in
                                             structure_class.__table__.columns.keys()]].set_index(
                    [col.name for col in structure_class.__table__.primary_key.columns.values()])
            else:
                structure_df = structure_df.drop(
                    columns=list(set([col.name for col in structure_class.__table__.primary_key.columns.values() if
                                      col.name not in ['datetime']]) &
                                 set(df_whole.reset_index().columns))
                ).set_index(extra_index).reset_index().set_index(
                    [col.name for col in structure_class.__table__.primary_key.columns.values()])
        else:
            structure_df = pd.DataFrame(columns=structure_class.__table__.columns.keys()).set_index(
                [col.name for col in structure_class.__table__.primary_key.columns.values()])
    else:  # multiple structures
        if target_structure[0] in df_whole.columns:
            structure_df = cols_to_frame(df_whole, target_structure, df_whole.index)
            structure_df = structure_df[[col for col in structure_df.columns if col in
                                         structure_class.__table__.columns.keys()]].set_index(
                [col.name for col in structure_class.__table__.primary_key.columns.values()])
        else:
            structure_df = pd.DataFrame(columns=structure_class.__table__.columns.keys()).set_index(
                [col.name for col in structure_class.__table__.primary_key.columns.values()])
    if not structure_df.empty:
        for column in [col for col in structure_class.__table__.columns if
                       col.name in structure_df.columns and
                       col not in [column for column in structure_class.__table__.primary_key.columns.values()]]:
            first_col_value = structure_df.iloc[0][column.name]

            if 'DATETIME' in str(column.type):
                if not pd.isna(first_col_value) and len(first_col_value) >= 22:
                    col_format = '%Y-%m-%d %H:%M:%S.%f'
                else:
                    col_format = '%Y-%m-%d %H:%M:%S'
                structure_df[column.name] = pd.to_datetime(structure_df[column.name], errors='coerce',
                                                           format=col_format)

            elif 'FLOAT' in str(column.type):
                if not structure_df[column.name].str.contains(':').all():
                    structure_df.update(
                        structure_df[column.name].mask(structure_df[column.name].str.contains("0x"), '00:00:00.000000'))

                structure_df[column.name] = pd.to_timedelta(structure_df[column.name]) / np.timedelta64(1, 's')
            elif 'INTEGER' in str(column.type) and structure_df[column.name].dtype not in [np.int64,
                                                                                           np.float64] and '0x' in first_col_value:
                structure_df[column.name] = structure_df[column.name].apply(
                    lambda x: int(x, base=16) if pd.notnull(x) and x not in ['0xFFFFFFFF'] else np.nan)
                structure_df[column.name] = structure_df[column.name].apply(
                    lambda x: x if pd.notnull(x) and x != 4294967295 else np.nan)
            elif 'BIGINT' in str(column.type):
                structure_df[column.name] = structure_df[column.name].apply(
                    lambda x: x if pd.notnull(x) and x != 4294967295 else np.nan)
            elif 'INTEGER' in str(column.type):
                structure_df[column.name] = structure_df[column.name].apply(
                    lambda x: int(x, 16) if isinstance(x, str) and '0x' in x else x)
                structure_df[column.name] = structure_df[column.name].apply(
                    lambda x: x if pd.notnull(x) and x != 4294967295 else np.nan)
            elif 'VARCHAR(1)' in str(column.type):
                structure_df[column.name] = structure_df[column.name].apply(
                    lambda x: bytes.fromhex(x[2:]).decode('cp500') if '0x' in x and bytes.fromhex(x[2:]).decode('cp500').isprintable() else np.nan if len(x) > 1 else x)

    return structure_df


def col_to_frame_with_key(df_source: pd.DataFrame, primary_col: str, key_col: str,
                          df_index: pd.Index) -> pd.DataFrame:
    """Create a dataframe with a key column and a primary column from the source dataframe.

    Args:
        df_source (pd.DataFrame): The source dataframe.
        primary_col (str): The primary column name.
        key_col (str): The key column name.
        df_index (pd.DataFrame): The dataframe index.

    Returns:
        pd.DataFrame: A dataframe with a key column and a primary column from the source dataframe.
    """
    convert_to_list = np.vectorize(converttolist)
    z = df_source.reset_index()[[key_col, primary_col]].set_index(df_index)
    z.dropna(how='all', inplace=True)
    z = z.reset_index().set_index(['smfstsid', 'smfstprn', 'smfstspn', 'datetime', 'smfsttme', key_col])
    z[primary_col] = convert_to_list(z[primary_col])
    x = z.explode(primary_col)
    return pd.json_normalize(x[primary_col]).set_index(x.index).reset_index()


def build_singular_structure_with_key(df_source: pd.DataFrame, primary_col: str, secondary_col: str,
                                      primary_tbl, secondary_tbl) -> pd.DataFrame:
    convert_to_list = np.vectorize(converttolist)
    if primary_col in df_source.columns:
        d = col_to_frame(df_source, primary_col, df_source.index)
        z = d.reset_index()[[col.name for col in primary_tbl.__table__.primary_key.columns.values()] + [secondary_col]]
        z = z.reset_index().set_index([col.name for col in primary_tbl.__table__.primary_key.columns.values()])
        z[secondary_col] = convert_to_list(z[secondary_col])
        x = z.explode(secondary_col)
        result = pd.json_normalize(x[secondary_col]).set_index(x.index).reset_index()
        return result.set_index(
            [col.name for col in secondary_tbl.__table__.primary_key.columns.values()])
    else:
        return pd.DataFrame(columns=secondary_tbl.__table__.columns.keys()).set_index(
            [col.name for col in secondary_tbl.__table__.primary_key.columns.values()])


def build_bssds(df):
    if 'dfha08ds' in df.columns:
        d = df['dfha08ds'].apply(pd.Series)
        if 'a08bssds' in d.columns:
            df_bssds = col_to_frame_with_key(d, 'a08bssds', 'a08srpid', df.index)
            df_bssds['isIndxBuffer'] = 0
        elif 'a08bsds_data' in d.columns:
            df_bssds = col_to_frame_with_key(d, 'a08bssds_data', 'a08srpid', df.index)
            df_bssds['isIndxBuffer'] = 0
        else:
            df_bssds = pd.DataFrame(columns=A08bssds.__table__.columns.keys())

        if 'a08bsds_indx' in d.columns:
            df_bssds_indx = col_to_frame_with_key(d, 'a08bssds_indx', 'a08srpid', df.index)
            df_bssds_indx['isIndxBuffer'] = 1
        else:
            df_bssds_indx = pd.DataFrame(columns=A08bssds.__table__.columns.keys())

        if df_bssds_indx.shape[0] > 0:
            df_bssds = pd.concat([df_bssds, df_bssds_indx], axis=0)[A08bssds.__table__.columns.keys()].set_index(
                [col.name for col in A08bssds.__table__.primary_key.columns.values()])
        else:
            df_bssds = df_bssds[A08bssds.__table__.columns.keys()].set_index(
                [col.name for col in A08bssds.__table__.primary_key.columns.values()])
    else:
        df_bssds = pd.DataFrame(columns=A08bssds.__table__.columns.keys()).set_index(
            [col.name for col in A08bssds.__table__.primary_key.columns.values()])
    return df_bssds


tbs_list = ['dfha03ds', 'dfha04ds', 'dfha06ds', 'dfha09ds', 'dfha14ds', 'dfha16ds', 'a16stats', 'dfha17ds', 'dfha21ds',
            'dfhxmrds', 'dfhnqgds', 'nqgbody',  'dfhusgds', 'dfhlggds', 'dfhlgrds', 'dfhlgsds', 'dfhrmgds', 'dfhtsgds',
            'dfhsogds', 'dfhwbgds', 'dfhdhdds', 'dfhepgds', 'dfhstgds', 'dfhpgdds', 'dfhpgrds', 'dfhdsgds', 'dfhdstds',
            'dfhdsrds', 'dsgtcbm',  'dsgtcbp',  'dfhtqgds', 'dfhxmgds', 'smsglobal', 'smsbody', 'dfha08ds', 'a08bssds',
            'dfhxmcds', 'dfhd2gds', 'dfhd2rds', 'dfhsdgds', 'dfhtdgds', 'dfhsmdds', 'dfhsmtds', 'smtbody',  'dfhldrds',
            'ldgglobal','ldgdsastat','dfhldbds','ldb_dsnames','dfhtdrds','dfhsdrds','dfhmngds', 'dfhtqrds', 'dfhasgds',
            'dfhldyds','ldy_dsnames','dfhisrds','dfhmlrds', 'dfhmqrds', 'dfhmqgds', 'dfha24ds', 'dfha23ds', 'dfhwbrds',
            'dfhcfs6d', 'dfhcfs7d', 'dfha22ds', 'dfhpgeds', 'dfhw2rds', 'dfha20ds', 'dfhmprds', 'dfhpirds', 'dfheprds',
            'dfhsjsds', 'dfhpiwds', 'dfheccds', 'dfhrlrds', 'dfhxqs1d', 'dfhcfs8d', 'dfhsjnds', 'dfhpgpds', 'dfhsords',
            'dfhncs5d', 'dfhecgds', 'dfhecrds', 'dfhldpds', 'dfhxqs2d', 'dfhxqs3d', 'dfhpggds', 'dfhcfs9d', 'dfhncs4d']


def str_to_class(classname: str, extension: str = None):
    if '_' in classname:
        formatted_classname = classname.replace('_', ' ').title().replace(' ', '')
    else:
        formatted_classname = classname.capitalize()
    if extension is None:
        return getattr(sys.modules[__name__], formatted_classname)
    else:
        return getattr(sys.modules[__name__], formatted_classname + extension)


tbls = {}
for tb in tbs_list:
    tbls[tb] = str_to_class(tb)


def format_1102df(df: pd.DataFrame) -> dict:
    """Format smf110 subtype 2 JSON files to the dataframes.

    Args:
        df: JSON dataframe.

    Returns:
        A dictionary of dataframes.
    """
    set_datetime = np.vectorize(setdatetime)

    dfs_dict = {}

    if 'header' not in df.columns:
        for table in tbs_list:
            dfs_dict[table] = pd.DataFrame()
        return dfs_dict
    if not df.columns.str.startswith('dfh').any():
        for table in tbs_list:
            dfs_dict[table] = pd.DataFrame()
        return dfs_dict

    df_header = df['header'].apply(pd.Series)[
        ['recType', 'subType', 'sysId', 'dateTime', 'smfstprn', 'smfstspn']].rename(
        columns={'sysId': 'smfstsid', 'dateTime': 'smfsttme'})
    df_header['smfsttme'] = pd.to_datetime(df_header['smfsttme'])
    df_header['datetime'] = set_datetime(df_header['smfsttme'])
    df_header.set_index(['recType', 'subType', 'smfstsid', 'smfstprn', 'smfstspn', 'datetime', 'smfsttme'],
                        inplace=True)
    df.set_index(df_header.index, inplace=True)


    for table in tbs_list:
        if table.startswith('dfh'):
            dfs_dict[table] = build_structure(table, df, tbls[table])
        elif table == 'a08bssds':
            dfs_dict[table] = build_bssds(df)
        elif table == 'a16stats':
            dfs_dict[table] = build_structure(('dfha16ds', 'a16stats'), df, tbls[table])
        elif table == 'nqgbody':
            dfs_dict[table] = build_structure(('dfhnqgds', 'nqgbody'), df, tbls[table])
        elif table == 'dsgtcbm':
            dfs_dict[table] = build_structure(('dfhdsgds', 'dsgtcbm'), df, tbls[table])
        elif table == 'dsgtcbp':
            dfs_dict[table] = build_structure(('dfhdsgds', 'dsgtcbp'), df, tbls[table])
        elif table == 'smsglobal':
            dfs_dict[table] = build_structure(('dfhsmsds', 'smsglobal'), df, tbls[table],
                                              ['smslen', 'smsid', 'smsdvers'])
        elif table == 'smsbody':
            dfs_dict[table] = build_structure(('dfhsmsds', 'smsbody'), df, tbls[table],
                                              extra_index=dfs_dict['smsglobal'].reindex(
                                                  dfs_dict['smsglobal'].index.repeat(
                                                      dfs_dict['smsglobal'].smsnpagp)).reset_index().set_index(
                                                  ['smfstsid', 'smfstprn', 'smfstspn', 'smfsttme',
                                                   'smsdsalimit', 'smsedsalimit']).index)
        elif table == 'smtbody':
            dfs_dict[table] = build_structure(('dfhsmtds', 'smtbody'), df, tbls[table])
        elif table == 'ldgglobal':
            dfs_dict[table] = build_structure(('dfhldgds', 'ldgglobal'), df, tbls[table],
                                              ['ldglen', 'ldgid', 'ldgdvers'])
        elif table == 'ldgdsastat':
            dfs_dict[table] = build_structure(('dfhldgds', 'ldgdsastat'), df, tbls[table])
        elif table == 'ldb_dsnames':
            dfs_dict[table] = build_singular_structure_with_key(df, 'dfhldbds', 'ldb_dsnames',
                                                                Dfhldbds, tbls[table])
        elif table == 'ldy_dsnames':
            dfs_dict[table] = build_singular_structure_with_key(df, 'dfhldyds', 'ldy_dsnames',
                                                                Dfhldyds, tbls[table])
        else:
            print('Table {} not found.'.format(table))
    return dfs_dict


def print_cics_statistics_report(jsonfiles: tuple, start_time_str: str, end_time_str: str,
                                  specific_appl: Union[str, None] = None) -> str:
    """Print CICS Statistics Report based on JSON files.

    Args:
        jsonfiles: JSON file or files.
        start_time_str: Start time string.
        end_time_str: End time string.
        specific_appl: Specific applid to include.

    Returns:
        CICS Statistics report.
    """
    start_time = pd.to_datetime(start_time_str)
    end_time = pd.to_datetime(end_time_str)
    x_div_y = np.vectorize(x_divided_by_y)
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
                    or df.iloc[0]['header'].get('recType') is None or df.iloc[0]['header']['recType'] != 110:
                click.echo(
                    f"\nInvalid JSON file {jsonfile}. This file will be skipped.")
                continue
            try:
                df_dict = format_1102df(df)
            except Exception as e:
                click.echo(f"\nUnsupported JSON file {jsonfile} with error: {str(e)}. This file will be skipped.")
                continue

            if specific_appl is not None:
                query_stmt = "smfsttme > @start_time and smfsttme < @end_time and smfstprn == @specific_appl"
            else:
                query_stmt = "smfsttme > @start_time and smfsttme < @end_time"

            if not df_dict['dfhxmgds'].empty:
                trans_mgr = df_dict['dfhxmgds'].reset_index().query(query_stmt)[
                    ['smfstsid','smfstprn','smfsttme','xmgnum','xmgtat','xmgpat','xmgmxt']]

                trans_mgr.columns = ['Lpar','Applid','Time','System and User Transactions','User Transactions',
                                    'Peak User Transactions','Current MAXTASK']
            else:
                trans_mgr = pd.DataFrame()

            if not df_dict['nqgbody'].empty:
                enq_mgr = df_dict['nqgbody'].reset_index().query(query_stmt)[
                    ['smfstsid','smfstprn','smfsttme','nqgpool','nqgtnqsw','nqgtnqsi','nqgtnqsr','nqgtirjb','nqgtirjr']]
                enq_mgr.columns = ['Lpar','Applid','Time','Pool ID','ENQs Waited','ENQs Issued','Total ENQs Retained',
                                    'Total Rejected ENQBUSY','Total Rejected ENQ Retained']
            else:
                enq_mgr = pd.DataFrame()

            if not df_dict['dfhxmcds'].empty:
                trans_class = df_dict['dfhxmcds'].reset_index().query(query_stmt)[
                    ['smfstsid','smfstprn','smfsttme','xmctcl','xmctama','xmctapt']]
                trans_class.columns = ['Lpar','Applid','Time','TClass Name','Times at Maxactive','Times at Purge Threshold']
            else:
                trans_class = pd.DataFrame()

            if not df_dict['dfha14ds'].empty:
                isc_mro_connection = df_dict['dfha14ds'].reset_index().query(query_stmt)[
                    ['smfstsid','smfstprn','smfsttme','a14cntn','a14estaq','a14estaf','a14estao']]
                isc_mro_connection.columns = ['Lpar','Applid','Time','Connection Name','Queued Allocates',
                                    'Failed Link Allocates','Failed Allocates Other Reasons']
            else:
                isc_mro_connection = pd.DataFrame()

            if not df_dict['dfhtdgds'].empty:
                dumps_tdgds = df_dict['dfhtdgds'].reset_index().query(query_stmt)[
                    ['smfstsid','smfstprn','smfsttme','trans_dump_taken','trans_dump_supp']]
                dumps_tdgds.columns = ['Lpar','Applid','Time','Transaction Dumps Taken','Transaction Dumps Suppressed']
            else:
                dumps_tdgds = pd.DataFrame()

            if not df_dict['dfhsdgds'].empty:
                dumps_sdgds = df_dict['dfhsdgds'].reset_index().query(query_stmt)[
                    ['smfstsid','smfstprn','smfsttme','sys_dumps_taken','sys_dumps_suppr']]
                dumps_sdgds.columns = ['Lpar','Applid','Time','System Dumps Taken','System Dumps Suppressed']
            else:
                dumps_sdgds = pd.DataFrame()

            if not df_dict['dfhtsgds'].empty:
                tsgds_df = df_dict['dfhtsgds'].reset_index().query(query_stmt)[
                    ['smfstsid','smfstprn','smfsttme','tsgsta5f','tsgnmg','tsgsta7f','tsgnag']]
                tsgds_df.columns = ['Lpar','Applid','Time','PUT/PUTQ Main Storage Requests','GET/GETQ Main Storage Requests',
                                    'PUT/PUTQ Auxiliary Storage Requests','GET/GETQ Auxiliary Storage Requests']
            else:
                tsgds_df = pd.DataFrame()

            if not df_dict['dfhdstds'].empty:
                dsgds_df = pd.concat([df_dict['dfhdstds'][['dstds_cicstcb_cputime']],df_dict['dfhdsgds'][['dsgsrbt']]],
                                     axis=1).reset_index().query(query_stmt)[
                    ['smfstsid','smfstprn','smfsttme','dstds_cicstcb_cputime','dsgsrbt']]
                dsgds_df.columns = ['Lpar','Applid','Time','Address Space CPU Time', 'Address Space SRB Time']
            else:
                dsgds_df = pd.DataFrame()

            if not df_dict['dfhd2gds'].empty:
                d2gds_df = df_dict['dfhd2gds'].reset_index().query(query_stmt)[
                    ['smfstsid','smfstprn','smfsttme','d2g_tcb_hwm','d2g_tcb_limit']]
                d2gds_df.columns = ['Lpar','Applid','Time','Peak TCBs','TCB Limit']
            else:
                d2gds_df = pd.DataFrame()

            if not df_dict['dfhd2rds'].empty:
                d2rds_df = df_dict['dfhd2rds'].reset_index().query(query_stmt)[
                    ['smfstsid','smfstprn','smfsttme','d2r_thread_hwm']]
                d2rds_df.columns = ['Lpar','Applid','Time','Highest Peak Threads']
            else:
                d2rds_df = pd.DataFrame()

            if not df_dict['dfhlggds'].empty:
                lggds_df = df_dict['dfhlggds'].reset_index().query(query_stmt)[
                    ['smfstsid','smfstprn','smfsttme','lggakpstkn']]
                lggds_df.columns = ['Lpar','Applid','Time','Activity Keypoints Taken']
            else:
                lggds_df = pd.DataFrame()

            if not df_dict['dfhlgsds'].empty:
                lgsds_df = df_dict['dfhlgsds'].reset_index().query(query_stmt)[
                    ['smfstsid','smfstprn','smfsttme','lgsbytes','lgsstrnam']]
                lgsds_df.columns = ['Lpar','Applid','Time','Logstream Bytes Written', 'Logstream Name']
            else:
                lgsds_df = pd.DataFrame()

            if not df_dict['dsgtcbm'].empty:
                dsgtcbm_df = df_dict['dsgtcbm'].reset_index().query(query_stmt)[
                    ['smfstsid','smfstprn','smfsttme','dsgtcbnm','dsgtdt','dsgact']]
                if not dsgtcbm_df.empty:
                    dsgtcbm_df['TCB CPU Dispatch Ratio'] = x_div_y(dsgtcbm_df['dsgact'], dsgtcbm_df['dsgtdt']) * 100
                    dsgtcbm_df.columns = ['Lpar','Applid','Time','TCB Mode Name','Total TCB Dispatch Time',
                                          'Total TCB CPU Time','TCB CPU Dispatch Ratio']
            else:
                dsgtcbm_df = pd.DataFrame()

            if not df_dict['dfhtqgds'].empty:
                tqgds_df = df_dict['dfhtqgds'].reset_index().query(query_stmt)[
                    ['smfstsid','smfstprn','smfsttme','tqgactpt','tqgactgt']]
                tqgds_df.columns = ['Lpar','Applid','Time','Data Set Writes','Data Set Reads']
            else:
                tqgds_df = pd.DataFrame()

            dfs_list = []
            cols_list = ['\n\n\nLpar','\n\n\nApplid','\n\n\nTime']
            floatfmt_list = ['','','']
            if not trans_mgr.empty:
                trans_mgr = trans_mgr.assign(
                    maxtaskratio=lambda x: (x['Peak User Transactions'] / x['Current MAXTASK']) * 100
                    ).rename(columns={'maxtaskratio': '% of MAXTASK'})[
                    ['Lpar','Applid','Time','User Transactions','Peak User Transactions','% of MAXTASK']
                ].set_index(['Lpar','Applid','Time'])
                dfs_list.append(trans_mgr)
                cols_list = cols_list + ['\n\nUser\nXact', '\nPeak\nUser\nXact', '\n%\nof\nMAXTASK']
                floatfmt_list = floatfmt_list + ['.0f','.0f','.02f']

            if not enq_mgr.empty:
                enq_mgr_dfg = enq_mgr.groupby(['Lpar','Applid','Time']).agg({"ENQs Waited": "sum",
                                                                             "ENQs Issued": "sum",
                                                                             "Total ENQs Retained": "sum",
                                                                             "Total Rejected ENQBUSY": "sum",
                                                                             "Total Rejected ENQ Retained": "sum"
                                                                             })#.reset_index()
                enq_mgr_dfg = enq_mgr_dfg.assign(
                    successratio=lambda x: (1 - (x['ENQs Waited'] / x['ENQs Issued'])) * 100
                    ).rename(columns={'successratio': '% Immediate Success'})[
                    ['ENQs Issued','% Immediate Success']]
                dfs_list.append(enq_mgr_dfg)
                cols_list = cols_list + ['\n\nENQs\nIssued', 'ENQs\n%\nImmed\nSuccess']
                floatfmt_list = floatfmt_list + ['.0f', '.02f']

            if not trans_class.empty:
                trans_class_dfg = trans_class.groupby(['Lpar','Applid','Time']).agg(
                    {"Times at Maxactive": "sum",
                     "Times at Purge Threshold": "sum"
                     }).rename(columns={'Times at Maxactive': 'Times at Maxactive (TClass)',
                                        'Times at Purge Threshold': 'Times at Purge Threshold (TClass)'})
                dfs_list.append(trans_class_dfg)
                cols_list = cols_list + ['\nTimes at\nMaxactive\n(TClass)', 'Times at\nPurge\nThreshold\n(TClass)']
                floatfmt_list = floatfmt_list + ['.0f', '.0f']

            if not isc_mro_connection.empty:
                isc_mro_connect_dfg = isc_mro_connection.groupby(['Lpar','Applid','Time']).agg({
                    "Queued Allocates": "sum",
                    "Failed Link Allocates": "sum",
                    "Failed Allocates Other Reasons": "sum"
                    })
                isc_mro_connect_dfg = isc_mro_connect_dfg.assign(Failed=lambda x: x['Failed Link Allocates'] +
                                                                                  x['Failed Allocates Other Reasons']
                                                                 ).rename(columns={'Failed': 'Failed MRO Allocates',
                                                                                   'Queued Allocates': 'MRO Queued Allocates'}
                                                                          )[['MRO Queued Allocates','Failed MRO Allocates',]]
                dfs_list.append(isc_mro_connect_dfg)
                cols_list = cols_list + ['\nMRO\nQueued\nAlloc', '\nFailed\nMRO\nAlloc']
                floatfmt_list = floatfmt_list + ['.0f', '.0f']

            if not dumps_tdgds.empty and not dumps_sdgds.empty:
                dumps_df = pd.merge(dumps_tdgds, dumps_sdgds, how="outer", on=['Lpar','Applid','Time'])
                dumps_df = dumps_df.assign(Taken=lambda x: x['Transaction Dumps Taken'] + x['System Dumps Taken']
                                           ).rename(columns={'Taken': 'Dumps Taken'})
                dumps_df = dumps_df.assign(Suppressed=lambda x: x['Transaction Dumps Suppressed'] + x['System Dumps Suppressed']
                                           ).rename(columns={'Suppressed': 'Dumps Suppressed'}
                                                    ).set_index(['Lpar','Applid','Time'])[['Dumps Taken','Dumps Suppressed']]
                dfs_list.append(dumps_df)
                cols_list = cols_list + ['\n\nDumps\nTaken', '\n\nDumps\nSuppr']
                floatfmt_list = floatfmt_list + ['.0f', '.0f']

            if not tsgds_df.empty:
                tsgds_df = tsgds_df.assign(Main_Requests=lambda x: x['PUT/PUTQ Main Storage Requests'] +
                                                                   x['GET/GETQ Main Storage Requests']
                                             ).rename(columns={'Main_Requests': 'TS Main Storage Requests'})
                tsgds_df = tsgds_df.assign(Aux_Requests=lambda x: x['PUT/PUTQ Auxiliary Storage Requests'] +
                                                                  x['GET/GETQ Auxiliary Storage Requests']
                                             ).rename(columns={'Aux_Requests': 'TS Auxiliary Storage Requests'}
                                                      ).set_index(['Lpar','Applid','Time'])[
                    ['TS Main Storage Requests','TS Auxiliary Storage Requests']]
                dfs_list.append(tsgds_df)
                cols_list = cols_list + ['TS\nMain\nStorage\nReqs', 'TS\nAux\nStorage\nReqs']
                floatfmt_list = floatfmt_list + ['.0f', '.0f']

            if not dsgds_df.empty:
                dsgds_dfg = dsgds_df.set_index(['Lpar','Applid','Time'])
                dfs_list.append(dsgds_dfg)
                cols_list = cols_list + ['Address\nSpace\nCPU\nTime', 'Address\nSpace\nSRB\nTime']
                floatfmt_list = floatfmt_list + ['.2f', '.2f']

            if not d2gds_df.empty:
                d2gds_df = d2gds_df.assign(ratio=lambda x: (x['Peak TCBs'] / x['TCB Limit']) * 100
                                           ).rename(columns={'ratio': '% of TCB Limit'})
                d2gds_dfg = d2gds_df.set_index(['Lpar','Applid','Time'])[['Peak TCBs','% of TCB Limit']]
                dfs_list.append(d2gds_dfg)
                cols_list = cols_list + ['\n\nPeak\nTCBs', '%\nof\nTCB\nLimit']
                floatfmt_list = floatfmt_list + ['.0f','.02f']

            if not d2rds_df.empty:
                d2rds_dfg = d2rds_df.groupby(['Lpar','Applid','Time']).agg({"Highest Peak Threads": "max"}
                                                                           ).rename(
                    columns={'Highest Peak Threads': 'Highest Db2 Peak Threads'})
                dfs_list.append(d2rds_dfg)
                cols_list = cols_list + ['Highest\nDb2\nPeak\nThreads']
                floatfmt_list = floatfmt_list + ['.0f']
            if not lggds_df.empty:
                lggds_dfg = lggds_df.set_index(['Lpar','Applid','Time'])
                dfs_list.append(lggds_dfg)
                cols_list = cols_list + ['\nActivity\nKeypoints\nTaken']
                floatfmt_list = floatfmt_list + ['.0f']

            if not lgsds_df.empty:
                lgsds_dfg = lgsds_df.groupby(['Lpar','Applid','Time']).agg({"Logstream Bytes Written": "sum"})
                dfs_list.append(lgsds_dfg)
                cols_list = cols_list + ['\nLogstream\nBytes\nWritten']
                floatfmt_list = floatfmt_list + ['.0f']

            if not dsgtcbm_df.empty:
                dsgtcbm_df["Minimum CPU / Dispatch Ratio"] = np.where(dsgtcbm_df["Total TCB Dispatch Time"] > 0,
                                                                      dsgtcbm_df["Total TCB CPU Time"] * 100 /
                                                                      dsgtcbm_df["Total TCB Dispatch Time"],
                                                                      np.nan)
                dsgtcbm_df2 = pd.merge(dsgtcbm_df[dsgtcbm_df['TCB Mode Name'] == 'QR'][
                    ['Lpar', 'Applid', 'Time', 'Total TCB Dispatch Time',
                     'Total TCB CPU Time', 'Minimum CPU / Dispatch Ratio']].rename(
                    columns={"Total TCB Dispatch Time": "Total QR Dispatch Time",
                             "Total TCB CPU Time": "Total QR CPU Time",
                             "Minimum CPU / Dispatch Ratio": "Minimum QR CPU / Dispatch Ratio"}),
                    dsgtcbm_df[dsgtcbm_df['TCB Mode Name'] == 'L8'][
                        ['Lpar', 'Applid', 'Time', 'Total TCB Dispatch Time',
                         'Total TCB CPU Time', 'Minimum CPU / Dispatch Ratio']].rename(
                        columns={"Total TCB Dispatch Time": "Total L8 Dispatch Time",
                                 "Total TCB CPU Time": "Total L8 CPU Time",
                                 "Minimum CPU / Dispatch Ratio": "Minimum L8 CPU / Dispatch Ratio"}),
                    how="outer", on=['Lpar','Applid','Time'])
                dsgtcbm_df2 = dsgtcbm_df2.assign(TotalDispatch=lambda x: x['Total QR Dispatch Time'] +
                                                                         x['Total L8 Dispatch Time'])
                dsgtcbm_df2 = dsgtcbm_df2.assign(
                    QRratio=lambda x: (x['Total QR CPU Time'] / x['Total QR Dispatch Time']) * 100
                    ).rename(columns={"QRratio": "Avg QR CPU / Dispatch Ratio %"})
                dsgtcbm_df2 = dsgtcbm_df2.assign(
                    L8ratio=lambda x: (x['Total L8 CPU Time'] / x['Total L8 Dispatch Time']) * 100
                    ).rename(columns={"L8ratio": "Avg L8 CPU / Dispatch Ratio %"}).set_index(
                    ['Lpar','Applid','Time'])[
                    ['Minimum QR CPU / Dispatch Ratio', 'Minimum L8 CPU / Dispatch Ratio',
                     'Avg QR CPU / Dispatch Ratio %', 'Avg L8 CPU / Dispatch Ratio %']]
                dfs_list.append(dsgtcbm_df2)
                cols_list = cols_list + ['Minimum\nQR CPU /\nDispatch\nRatio', 'Minimum\nL8 CPU /\nDispatch\nRatio',
                                         'Avg\nQR CPU /\nDispatch\nRatio %', 'Avg\nL8 CPU /\nDispatch\nRatio %']
                floatfmt_list = floatfmt_list + ['.02f', '.02f', '.02f', '.02f']

            if not tqgds_df.empty:
                tqgds_df = tqgds_df.assign(TotalRequests=lambda x: x['Data Set Writes'] + x['Data Set Reads']
                                           ).rename(columns={"TotalRequests": "Total TD Queue Requests"})
                tqgds_dfg = tqgds_df.set_index(['Lpar','Applid','Time'])[['Total TD Queue Requests']]
                dfs_list.append(tqgds_dfg)
                cols_list = cols_list + ['Total\nTD\nQueue\nReqs']
                floatfmt_list = floatfmt_list + ['.0f']

            if len(dfs_list) > 0:
                system_overview = pd.concat(dfs_list, axis=1).reset_index()
                system_overview.columns = cols_list
                for col in system_overview.columns:
                    system_overview[col] = system_overview[col].replace(np.nan, None, regex=True)
                system_overview['\n\n\nTime'] = system_overview['\n\n\nTime'].dt.strftime("%m-%d %H:%M:%S")
                header1 = [
                    ["                                              C I C S    S T A T I S T I C S    R E P O R T"]]
                header2 = [
                    [f"                                          Data from   {start_time: %Y/%m/%d %H:%M}    to   {end_time:%Y/%m/%d %H:%M}"]]
                report += tabulate.tabulate(header1, tablefmt="plain") + "\n" + tabulate.tabulate(header2, tablefmt="plain") + "\n"
                report += tabulate.tabulate(system_overview, tablefmt='psql', showindex=False, headers='keys',
                                           floatfmt=(f'{x}' for x in floatfmt_list))
    return report

