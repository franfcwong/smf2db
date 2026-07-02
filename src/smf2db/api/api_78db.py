import datetime as dt
import time
from pathlib import Path

import click
import pandas as pd
from sqlalchemy.orm import Session

from smf2db import SUCCESS, JSON_ERROR
from smf2db.api.api_77db import int_dtypedict
from smf2db.api.api_78 import format_78df
from smf2db.api.util import (get_csc_in_db, UploadResult, create_int_dtypedict, df_insert_by_partitions)
from smf2db.db_models.smf78_model import (Smf78Pro, Smf78Comn, Smf78Ioq, Smf78Iop, Smf78Amg, Smf78Cha, Smf78Lcu,
                                          Smf78Chap, Smf78Pvt, Smf78Pvsp)

tbls = {'pro': Smf78Pro,
        'comn': Smf78Comn,
        'pvt': Smf78Pvt,
        'pvsp': Smf78Pvsp,
        'ioq': Smf78Ioq,
        'amg': Smf78Amg,
        'cha': Smf78Cha,
        'iop': Smf78Iop,
        'lcu': Smf78Lcu,
        'chap': Smf78Chap}
tblnames = {'pro': 'smf78_pro',
            'comn': 'smf78_comn',
            'pvt': 'smf78_pvt',
            'pvsp': 'smf78_pvsp',
            'ioq': 'smf78_ioq',
            'amg': 'smf78_amg',
            'cha': 'smf78_cha',
            'iop': 'smf78_iop',
            'lcu': 'smf78_lcu',
            'chap': 'smf78_chap'}

int_dtypedict = create_int_dtypedict(tbls)


def upload_78db(db_engines: dict, db_session: Session, jsonfiles: str, partitions_scheme: str,
                db_driver: str = 'postgresql+psycopg2') -> UploadResult:
    """Upload smf78 JSON files to the database.

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
        insert_dict = {'pro': 0, 'comn': 0, 'pvt': 0, 'pvsp': 0,
                       'ioq': 0, 'iop': 0, 'amg': 0, 'lcu': 0, 'cha': 0, 'chap': 0}
        with open(jsonfile) as f:
            # program logic start here
            try:
                df = pd.read_json(f)
            except ValueError:
                click.echo(
                    f"\nInvalid JSON file {jsonfile}. This file will be skipped.")
                continue

            dfs_dict = format_78df(df)

            if dfs_dict['pro'].empty:
                click.echo(
                    f"\nThis JSON file {jsonfile} is not for this smf type. This file will be skipped.")
                # Cannot continue processing
                continue
            else:
                csc = get_csc_in_db(dfs_dict['pro']['smf78xnm'].unique()[0], dfs_dict['pro']['smf78snm'].unique()[0],
                                    pd.to_numeric(dfs_dict['pro']['smf78ptn'].unique()[0], downcast="integer"),
                                    db_session)
                if csc is None:
                    click.echo(
                        f"\nThe file {jsonfile} cannot be processed until the corresponding Smf70 Subtype 1 records have been processed. This file will be skipped.")
                    continue

            # Update csc value in dataframes
            for table in dfs_dict.keys():
                if dfs_dict[table].shape[0] > 0:
                    dfs_dict[table] = dfs_dict[table].copy().reset_index()
                    dfs_dict[table]['csc'] = csc
                    dfs_dict[table].set_index([col.name for col in tbls[table].__table__.primary_key.columns.values()],
                                              inplace=True)
            # insert the detail tbls
            for table in insert_dict.keys():
                if dfs_dict[table].shape[0] > 0:
                    table_columns = [column for column in list(filter(None, dfs_dict[table].index.names + dfs_dict[table].columns.values.tolist()))
                                     if column in tbls[table].__table__.columns.keys()]
                    insert_dict[table] = df_insert_by_partitions(db_driver, db_engines, db_session,
                                                                 dfs_dict[table].copy().reset_index()[table_columns],
                                                                 tblnames[table], tbls[table],'smf78', int_dtypedict[table],
                                                                '78', partitions_scheme, True)

            result_list.append({tblnames[k]:v for k,v in insert_dict.items() if k in tblnames.keys()})

        et = time.time()  # get the end time
        # get the execution time
        elapsed_time = (et - st) / 60
        print(f'Execution time ({jsonfile}):', elapsed_time, 'minutes')

    overall_et = time.time()
    overall_elapsed_time = (overall_et - overall_st) / 60
    return UploadResult(result_list, overall_elapsed_time, SUCCESS)

