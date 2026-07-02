import datetime as dt
import time
from pathlib import Path

import click
import pandas as pd
from sqlalchemy.orm import Session

from smf2db import SUCCESS, JSON_ERROR
from smf2db.api.api_71 import format_71df
from smf2db.api.util import (get_csc_in_db, UploadResult, df_insert_by_partitions,
                             create_int_dtypedict)
from smf2db.db_models.smf71_model import Smf71Pag, Smf71Pro

tbls = {'pro': Smf71Pro,
        'pag': Smf71Pag}
tblnames = {'pro': 'smf71_pro',
            'pag': 'smf71_pag'}
int_dtypedict = create_int_dtypedict(tbls)

def upload_71db(db_engines: dict, db_session: Session, jsonfiles: list, partitions_scheme: str,
                db_driver: str = 'postgresql+psycopg2') -> UploadResult:
    """Upload smf71 JSON files to the database.

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

    result_list = []

    for jsonfile in jsonfiles:
        if not Path(jsonfile).is_file() or Path(jsonfile).suffix != '.json':
            continue

        st = time.time()
        # print(jsonfile)
        current_time = dt.datetime.now()
        insert_dict = {'pag': 0, 'pro': 0}
        with open(jsonfile) as f:
            # program logic start here
            try:
                df = pd.read_json(f)
            except ValueError:
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
            else:
                csc = get_csc_in_db(dfs_dict['pro']['smf71xnm'].unique()[0], dfs_dict['pro']['smf71snm'].unique()[0],
                                    pd.to_numeric(dfs_dict['pro']['smf71ptn'].unique()[0], downcast="integer"), db_session)
                if csc is None:
                    click.echo(
                        f"\nThe file {jsonfile} cannot be processed until the corresponding Smf70 Subtype 1 records have been processed. This file will be skipped.")
                    continue
                # Update csc value in dataframes
                dfs_dict['pro'] = dfs_dict['pro'].reset_index()
                dfs_dict['pro']['csc'] = csc
                dfs_dict['pro'].set_index([col.name for col in Smf71Pro.__table__.primary_key.columns.values()], inplace=True)
                dfs_dict['pag'] = dfs_dict['pag'].reset_index()
                dfs_dict['pag']['csc'] = csc
                dfs_dict['pag'].set_index([col.name for col in Smf71Pag.__table__.primary_key.columns.values()], inplace=True)

            for table in insert_dict.keys():
                if dfs_dict[table].shape[0] > 0:
                    # insert_dict[table] = dfs_dict[table].shape[0]
                    insert_dict[table] = df_insert_by_partitions(db_driver, db_engines, db_session,
                                                                 dfs_dict[table].reset_index(), tblnames[table],
                                                                 tbls[table],'smf71', int_dtypedict[table],
                                                                 '71', partitions_scheme, True)

            result_list.append({tblnames[k]:v for k,v in insert_dict.items() if k in tblnames.keys()})

        et = time.time()  # get the end time
        # get the execution time
        elapsed_time = (et - st) / 60
        print(f'Execution time ({jsonfile}):', elapsed_time, 'minutes')

    overall_et = time.time()
    overall_elapsed_time = (overall_et - overall_st) / 60
    return UploadResult(result_list, overall_elapsed_time, SUCCESS)

