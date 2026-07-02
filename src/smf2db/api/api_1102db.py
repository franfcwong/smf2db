import time
from pathlib import Path

import click
import pandas as pd
from sqlalchemy.orm import Session

from smf2db import SUCCESS, JSON_ERROR
from smf2db.api.api_1102 import format_1102df, tbs_list, str_to_class
from smf2db.api.util import UploadResult, create_int_dtypedict, df_insert_by_partitions
from smf2db.db_models.smf1102_model import *

tbls = {}
tblnames = {}
for tb in tbs_list:
    tbls[tb] = str_to_class(tb)
    tblnames[tb] = tb

int_dtypedict = create_int_dtypedict(tbls)


def upload_1102db(db_engines: dict, db_session: Session, jsonfiles: str, partitions_scheme: str,
                  db_driver: str = 'postgresql+psycopg2') -> UploadResult:
    """Upload smf110 Subtype 2 JSON files to the database.

    Args:
        db_engines: A dictionary of all the db_engines in the database.
        db_session: SQLAlchemy session.
        jsonfiles: JSON file or files.
        partitions_scheme: Partitions scheme.
        db_driver: Db driver to connect to the database.

    Returns:
        A NamedTuple including the insert dictionary, total elapsed time of the upload and the return code.
    """
    overall_st = time.time()

    result_list = []

    for jsonfile in jsonfiles:
        if not Path(jsonfile).is_file() or Path(jsonfile).suffix != '.json':
            continue
        st = time.time()
        # print(jsonfile)
        current_time = dt.datetime.now()
        insert_dict = {}
        for table in tbs_list:
            insert_dict[table] = 0

        with open(jsonfile) as f:
            # program logic start here
            try:
                df = pd.read_json(f)
            except ValueError:
                click.echo(
                    f"\nInvalid JSON file {jsonfile}. This file will be skipped.")
                continue
            try:
                dfs_dict = format_1102df(df)
            except Exception as e:
                click.echo(f"\nUnsupported JSON file {jsonfile} with error: {str(e)}. This file will be skipped.")
                continue
            contains_data = False
            for table in insert_dict.keys():
                if dfs_dict[table].shape[0] > 0:
                    contains_data = True
                    insert_dict[table] = df_insert_by_partitions(db_driver, db_engines, db_session,
                                                                dfs_dict[table].reset_index()[
                                                                    [column for column in dfs_dict[table].reset_index().columns if
                                                                     column in tbls[table].__table__.columns.keys()]],
                                                                tblnames[table], tbls[table], 'smf110', int_dtypedict[table],
                                                                '110_2', partitions_scheme, True)
            if contains_data:
                result_list.append({tblnames[k]:v for k,v in insert_dict.items() if k in tblnames.keys()})
            else:
                click.echo(
                    f"\nThis JSON file {jsonfile} is not for this smf type. This file will be skipped.")
                # Cannot continue processing
                continue

        et = time.time()  # get the end time
        # get the execution time
        elapsed_time = (et - st) / 60
        print(f'Execution time ({jsonfile}):', elapsed_time, 'minutes')

    overall_et = time.time()
    overall_elapsed_time = (overall_et - overall_st) / 60
    return UploadResult(result_list, overall_elapsed_time, SUCCESS)

