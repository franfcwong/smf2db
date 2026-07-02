import sys
import time

import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from smf2db import SUCCESS
from smf2db.api.api_1102 import tbs_list
from smf2db.api.util import UploadResult, create_int_dtypedict, df_upsert
from smf2db.db_models.smf1102_agg_dict import agg_dict
from smf2db.db_models.smf1102_model import *
from smf2db.db_models.smf1102_hr_model import *
from smf2db.db_models.smf1102_da_model import *


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
tbls_hr = {}
tbls_da = {}
tblnames = {}
tblnames_da = {}
tblnames_hr = {}
for tb in tbs_list:
    tbls[tb] = str_to_class(tb)
    tbls_hr[tb] = str_to_class(tb, 'Hr')
    tbls_da[tb] = str_to_class(tb, 'Da')
    tblnames[tb] = tb
    tblnames_da[tb] = tb + '_da'
    tblnames_hr[tb] = tb + '_hr'

int_dtypedict = create_int_dtypedict(tbls)


def sum_1102db(db_engines: dict, db_session: Session, summary_level: str, start_time_str: str, end_time_str: str,
             partitions_scheme: str, db_driver: str = 'postgresql+psycopg2') -> UploadResult:
    """Summarize smf110 Subtype 2 interval database to the hourly or daily database.

    Args:
        db_engines: A dictionary of all the db_engines in the database.
        db_session: SQLAlchemy session.
        summary_level: Summary level of data (hourly, daily).
        start_time_str: Start time of summary.
        end_time_str: End time of summary.
        partitions_scheme: Partitions scheme.
        db_driver: Db driver to connect to database.

    Returns:
        A NamedTuple including the insert dictionary, total elapsed time of the upload and the return code.
    """
    overall_st = time.time()
    start = pd.to_datetime(start_time_str)
    end = pd.to_datetime(end_time_str)

    if partitions_scheme == 'weekday':
        partitions_range = range(1, 8)
    elif partitions_scheme == 'day':
        partitions_range = range(1, 32)
    elif partitions_scheme == 'week':
        partitions_range = range(1, 53)
    else:
        partitions_range = range(1, 2)

    insert_dict = {}
    for table in tbs_list:
        insert_dict[table] = 0
    summary_class = {'hourly': tbls_hr, 'daily': tbls_da}
    summary_tblname = {'hourly': tblnames_hr, 'daily': tblnames_da}
    summary_engine = {'hourly': '110_2.hourly', 'daily': '110_2.daily'}

    result_list = []

    st = time.time()
    current_time = dt.datetime.now()

    for table in insert_dict.keys():
        if len(agg_dict[table]) > 0:
            df_table_list = []
            null_column_list = []
            stmt = select(tbls[table]).where(tbls[table].datetime.between(start, end))
            for part in partitions_range:
                df_table = pd.read_sql(stmt, db_engines[f'110_2.{part}'])
                if not df_table.empty:
                    df_table['date'] = df_table['datetime'].dt.date
                    df_table_list.append(df_table)
                    null_columns = df_table.columns[df_table.isna().all()].tolist()
                    for col in null_columns:
                        if col not in null_column_list:
                            null_column_list.append(col)
            if len(df_table_list) > 0:
                df_tables = pd.concat([df.dropna(axis=1, how='all') for df in df_table_list])
                if len(null_column_list) > 0:
                    new_cols = df_tables.columns.tolist()
                    for col in null_column_list:
                        if col not in new_cols:
                            new_cols.append(col)
                    df_tables = df_tables.reindex(columns=new_cols)
                df_table_sum = df_tables.groupby(
                    [col.name for col in summary_class[summary_level][table].__table__.primary_key.columns.values()]).agg(
                    agg_dict[table]).reset_index()
                if 'date' not in df_table_sum.columns:
                    df_table_sum['date'] = df_table_sum['datetime'].dt.date
                df_table_sum['last_update_time'] = current_time
                insert_dict[table] = df_upsert(db_driver, db_engines[summary_engine[summary_level]], db_session,
                                                df_table_sum[summary_class[summary_level][table].__table__.columns.keys()],
                                                summary_tblname[summary_level][table],
                                                summary_class[summary_level][table],'smf110',
                                                [col.name for col in
                                                 summary_class[summary_level][table].__table__.primary_key.columns.values()],
                                                int_dtypedict[table], shard_id=summary_engine[summary_level]
                                                )

    result_list.append({summary_tblname[summary_level][k]:v for k,v in insert_dict.items() if k in summary_tblname[summary_level].keys()})

    et = time.time()  # get the end time
    # get the execution time
    elapsed_time = (et - st) / 60
    print(f'Execution time ({summary_level}):', elapsed_time, 'minutes')

    overall_et = time.time()
    overall_elapsed_time = (overall_et - overall_st) / 60
    return UploadResult(result_list, overall_elapsed_time, SUCCESS)

