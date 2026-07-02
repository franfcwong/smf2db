import datetime as dt
import time
from pathlib import Path
import warnings

import click
import pandas as pd
import sqlalchemy
from sqlalchemy import select, and_
from sqlalchemy.orm import Session

from smf2db import SUCCESS, JSON_ERROR
from smf2db.api.api_123 import format_123df
from smf2db.api.util import UploadResult, create_int_dtypedict, df_insert_by_partitions, df_upsert_by_partitions
from smf2db.db_models.smf1101_agg_dict import agg_110
from smf2db.db_models.smf1101_model import Smf1101
from smf2db.db_models.smf123_model import Smf123Server, Smf123RequestData, Smf110Smf123


def get_110_records(db_engine: sqlalchemy.Engine, start_time: dt.datetime, end_time: dt.datetime) -> pd.DataFrame:
    """Get Smf110 subtype-1 records related to z/OS Connect between the given time range.

    Args:
        db_engine (sqlalchemy.engine): The database engine.
        start_time (dt.datetime): The start time.
        end_time (dt.datetime): The end time.

    Returns:
        pd.DataFrame: A DataFrame containing Smf110 subtype 1 recrods.
    """
    stmt_110 = select(Smf1101).filter(and_(Smf1101.cics_start.between(start_time, end_time),
                                           Smf1101.cics_oadid.like('IBM_zOS_Connect_CICS_SP%'),
                                           Smf1101.cics_oadata1 != ""))
    df_110 = pd.read_sql(stmt_110, db_engine)
    return df_110


def agg_fail(series):
    s_bool = (series > 299)
    return s_bool.sum()


tbls = {'server': Smf123Server,
        'data': Smf123RequestData,
        '110': Smf110Smf123}
tblnames = {'server': 'smf123_server', 'data': 'smf123_request_data', '110': 'smf110_123'}
int_dtypedict = create_int_dtypedict(tbls)


def upload_123db(db_engines: dict, db_session: Session, jsonfiles: str, partitions_scheme: str,
                 db_driver: str = 'postgresql+psycopg2') -> UploadResult:
    """Upload smf123 JSON files to the database.

    Args:
        db_engines: A dictionary of all the db_engines in the database.
        db_session: SQLAlchemy session.
        jsonfiles: JSON file or files.
        partitions_scheme: Partitions scheme.
        db_driver: Db driver to connect to database.

    Returns:
        A NamedTuple including the insert dictionary, total elapsed time of the upload and the return code.
    """
    overall_st = time.time()

    if partitions_scheme == 'weekday':
        partitions_range = range(1, 8)
    elif partitions_scheme == 'day':
        partitions_range = range(1, 32)
    elif partitions_scheme == 'week':
        partitions_range = range(1, 53)
    else:
        partitions_range = range(1, 2) # single partition

    result_list = []

    update_agg_110 = agg_110.copy()
    update_agg_110.update({'smfmnsid': 'last', 'smfmnprn': 'last', 'smfmnspn': 'last', 'task_tran': 'last'})

    for jsonfile in jsonfiles:
        if not Path(jsonfile).is_file() or Path(jsonfile).suffix != '.json':
            continue
        st = time.time()
        # print(jsonfile)
        current_time = dt.datetime.now()
        insert_dict = {'server': 0, 'data': 0, '110': 0}
        with open(jsonfile) as f:
            # program logic start here
            try:
                df = pd.read_json(f)
            except ValueError:
                click.echo(
                    f"\nInvalid JSON file {jsonfile}. This file will be skipped.")
                continue

            if 'header' not in df.columns or not isinstance(df.iloc[0]['header'], dict) \
                    or df.iloc[0]['header'].get('smf123_rec_type') is None or df.iloc[0]['header']['smf123_rec_type'] != 123:
                click.echo(
                    f"\nThis JSON file {jsonfile} is not for this smf type. This file will be skipped.")
                continue
            elif 'reqDataSection' not in df.columns:
                click.echo(
                    f"\nThis JSON file {jsonfile} is not for this smf type. This file will be skipped.")
                continue
            try:
                df_dict = format_123df(df, current_time)
            except Exception as e:
                click.echo(f"\nUnsupported JSON file {jsonfile} with error: {str(e)}. This file will be skipped.")
                continue
            for key in df_dict.keys():
                insert_dict[key] = df_dict[key].shape[0]

            df_110_list = []
            null_column_list = []
            for part in partitions_range:
                try:
                    df_110 = get_110_records(db_engines[f'110_1.{part}'],
                                             df_dict['data']['smf123s1_time_sor_sent'].min(),
                                             df_dict['data']['smf123s1_time_zc_exit'].max())
                    if not df_110.empty:
                        df_110_list.append(df_110)
                        null_columns = df_110.columns[df_110.isna().all()].tolist()
                        for col in null_columns:
                            if col not in null_column_list:
                                null_column_list.append(col)
                except Exception as e:
                    click.echo("Smf110 Subtype 1 DB have not been initialized and therefore no Smf110 data if any will be linked up to Smf123 records.")
                    break

            if len(df_110_list) > 0:
                df_dict['110'] = pd.concat([df.dropna(axis=1, how='all') for df in df_110_list])
                if len(null_column_list) > 0:
                    new_cols = df_dict['110'].columns.tolist()
                    for col in null_column_list:
                        if col not in new_cols:
                            new_cols.append(col)
                    df_dict['110'] = df_dict['110'].reindex(columns=new_cols)

                df_dict['110'] = df_dict['110'].loc[df_dict['110']['cics_oadata1'].isin(df_dict['data']['smf123s1_tracking_token'].values)]
                insert_dict['110'] = df_dict['110'].shape[0]

            if insert_dict['110'] > 0:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", category=pd.errors.PerformanceWarning)
                    df_110g = df_dict['110'].groupby('cics_oadata1').agg(update_agg_110).reset_index().rename(
                        columns={'cics_start': 'tasks', 'cics_oadata1': 'smf123s1_tracking_token'}).set_index('smf123s1_tracking_token')
                    df_data = df_dict['data'].copy().reset_index().set_index('smf123s1_tracking_token')
                    df_dict['data'] = pd.concat([df_data, df_110g], axis=1).reset_index(
                        ).set_index([col.name for col in Smf123RequestData.__table__.primary_key.columns.values()])

            if insert_dict['server'] > 0:
                server_columns = [column for column in list(filter(None, df_dict['server'].index.names + df_dict['server'].columns.values.tolist()))
                                  if column in Smf123Server.__table__.columns.keys()]

                server_records = df_upsert_by_partitions(db_driver, db_engines, db_session,
                                                         df_dict['server'].reset_index()[server_columns].drop_duplicates(),
                                                        'smf123_server', Smf123Server, 'smf123',
                                                         [col.name for col in Smf123Server.__table__.primary_key.columns.values()],
                                                         '123', partitions_scheme, int_dtypedict['server']
                                                        )
                insert_dict['server'] = server_records
            if insert_dict['data'] > 0:
                data_columns = list(filter(None, df_dict['data'].index.names + df_dict['data'].columns.values.tolist()))
                drop_columns = list(
                    set(data_columns) - set(Smf123RequestData.__table__.columns.keys()))
                new_df_data = df_dict['data'].copy().reset_index().drop(columns=drop_columns)
                insert_dict['data'] = df_insert_by_partitions(db_driver, db_engines, db_session, new_df_data,
                                                              'smf123_request_data', Smf123RequestData, 'smf123',
                                                              int_dtypedict['data'], '123', partitions_scheme, True)

            if insert_dict['110'] > 0:
                insert_dict['110'] = df_insert_by_partitions(db_driver, db_engines, db_session, df_dict['110'],
                                                            'smf110_123', Smf110Smf123, 'smf123', int_dtypedict['110'],
                                                            '123', partitions_scheme,  True,)


            result_list.append({tblnames[k]:v for k,v in insert_dict.items() if k in tblnames.keys()})

        et = time.time()  # get the end time
        # get the execution time
        elapsed_time = (et - st) / 60
        print(f'Execution time ({jsonfile}):', elapsed_time, 'minutes')

    overall_et = time.time()
    overall_elapsed_time = (overall_et - overall_st) / 60
    return UploadResult(result_list, overall_elapsed_time, SUCCESS)

