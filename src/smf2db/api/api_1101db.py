import datetime as dt
import time
from pathlib import Path

import click
import pandas as pd
from sqlalchemy.orm import Session

from smf2db import JSON_ERROR, SUCCESS
from smf2db.api.api_1101 import format_1101df
from smf2db.api.util import UploadResult, create_int_dtypedict, df_insert_by_partitions
from smf2db.db_models.smf1101_model import Smf1101

tbls = {'detail': Smf1101}

int_dtypedict = create_int_dtypedict(tbls)


def upload_1101db(db_engines: dict, db_session: Session, jsonfiles: str, partitions_scheme: str,
                  db_driver: str = 'postgresql+psycopg2') -> UploadResult:
    """Upload smf110 Subtype 1 JSON files to the database.

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
        duplicate_dict = {'dfhmntds': 0}
        insert_dict = {'dfhmntds': 0}
        with open(jsonfile) as f:
            # program logic start here
            try:
                df = pd.read_json(f)
            except ValueError:
                click.echo(
                    f"\nInvalid JSON file {jsonfile}. This file will be skipped.")
                continue
            try:
                df_dict = format_1101df(df)
            except Exception as e:
                click.echo(f"\nUnsupported JSON file {jsonfile} with error: {str(e)}. This file will be skipped.")
                continue

            if df_dict['dfhmntds'].shape[0] > 0:
                insert_dict['dfhmntds'] = df_insert_by_partitions(db_driver, db_engines, db_session, df_dict['dfhmntds'].reset_index(),
                                                        'smf110_1', Smf1101, 'smf110', int_dtypedict['detail'],
                                                        '110_1', partitions_scheme, True)


                result_list.append({'smf110_1': insert_dict['dfhmntds']})
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

