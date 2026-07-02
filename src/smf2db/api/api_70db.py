import datetime as dt
import time
from pathlib import Path

import click
import pandas as pd
from sqlalchemy import INTEGER
from sqlalchemy.orm import Session

from smf2db import JSON_ERROR, SUCCESS
from smf2db.api.api_70 import format_70df
from smf2db.api.util import (UploadResult, get_csc, get_csc_in_db, get_lpar_in_db, get_lpar,
                             df_insert_by_partitions, create_int_dtypedict)
from smf2db.db_models.smf70_model import (Smf70Pro, Smf70Ctl, Smf70Aid,
                                          Smf70Cpu, Smf70Bct, Smf70BctCpu, Smf70Bpd,
                                          Smf70Trg, Smf70Ccf, Smf70Typ3, Smf70Typ4, Smf70Typ5, )

smf70typ_cpu_type = {0: 'CP', 1: 'IFA', 2: 'IIP'}

tbls = {'pro': Smf70Pro,
        'ctl': Smf70Ctl,
        'cpu': Smf70Cpu,
        'bct': Smf70Bct,
        'bpd': Smf70Bpd,
        'bct_cpu': Smf70BctCpu,
        'aid': Smf70Aid,
        'trg': Smf70Trg,
        'typ3': Smf70Typ3,
        'typ4': Smf70Typ4,
        'typ5': Smf70Typ5,
        'ccf': Smf70Ccf}
tblnames = {'pro': 'smf70_pro',
            'ctl': 'smf70_ctl',
            'cpu': 'smf70_cpu',
            'bct': 'smf70_bct',
            'bpd': 'smf70_bpd',
            'bct_cpu': 'smf70_bct_cpu',
            'aid': 'smf70_aid',
            'trg': 'smf70_trg',
            'typ3': 'smf70_typ3',
            'typ4': 'smf70_typ4',
            'typ5': 'smf70_typ5',
            'ccf': 'smf70_ccf'}


int_dtypedict = create_int_dtypedict(tbls)

def upload_70db(db_engines: dict, db_session: Session, jsonfiles: str, partitions_scheme: str,
                db_driver: str = 'postgresql+psycopg2') -> UploadResult:
    """Upload smf70 JSON files to the database.

    Args:
        db_engines: A dictionary of all the db_engines in the database.
        db_session: SQLAlchemy session.
        jsonfiles: JSON file or files.
        partitions_scheme: Partitions scheme (weekday, day, week).
        db_driver: 'psycopg2' or 'sqlite'.

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
        insert_dict = {'pro': 0, 'ctl': 0, 'cpu': 0, 'aid': 0, 'bct': 0, 'bct_cpu': 0, 'bpd': 0, 'trg': 0,
                       'ccf': 0, 'typ3': 0, 'typ4': 0, 'typ5': 0, 'wc': 0}

        with open(jsonfile) as f:
            # program logic start here
            try:
                df = pd.read_json(f)
            except ValueError:
                click.echo(
                    f"\nInvalid JSON file {jsonfile}. This file will be skipped.")
                continue
            try:
                df_dict = format_70df(df)
            except Exception as e:
                click.echo(f"\nUnsupported JSON file {jsonfile} with error: {str(e)}. This file will be skipped.")
                continue

            if df_dict['pro'].empty:
                click.echo(
                    f"\nThis JSON file {jsonfile} is not for this smf type. This file will be skipped.")
                # Cannot continue processing
                continue
            else:
                if 'smf70ctl' in df.columns:
                    # insert the record to SmfLpar
                    target = get_csc(df_dict['pro'].reset_index()['csc'].unique()[0], db_session)
                else:
                    csc = get_csc_in_db(df_dict['pro']['smf70xnm'].unique()[0], df_dict['pro']['smf70snm'].unique()[0],
                                        pd.to_numeric(df_dict['pro']['smf70ptn'].unique()[0], downcast="integer"), db_session)
                    if csc is None:
                        click.echo(
                            f"\nThe file {jsonfile} cannot be processed until the corresponding Smf70 Subtype 1 records have been processed. This file will be skipped.")
                        continue

                    df_dict['pro']['csc'] = csc

            if df_dict['bct'].shape[0] > 0:
                for row in df_dict['bct'].reset_index()[
                    ['csc', 'smf70lpm', 'system_name', 'lpar_number', 'sysplex_name',
                     'is_CF']].drop_duplicates().itertuples():
                    lpar_obj = get_lpar_in_db(getattr(row, 'csc'),
                                              getattr(row, 'smf70lpm'),
                                              getattr(row, 'system_name'),
                                              getattr(row, 'lpar_number'),
                                              getattr(row, 'sysplex_name'),
                                              current_time, db_session,
                                              getattr(row, 'is_CF'))
                db_session.commit()

            if df_dict['ctl'].shape[0] > 0:
                current_lpar = get_lpar(df_dict['ctl'].index.get_level_values('csc').unique()[0],
                                        df_dict['ctl']['smf70ptn'].unique()[0], db_session)
                if current_lpar is not None:
                    if current_lpar.smf70cpa_scaling_factor is None:
                        current_lpar.smf70cpa_scaling_factor = df_dict['ctl']['smf70cpa_scaling_factor'].unique()[0].astype(
                            INTEGER)
                        current_lpar.smf70cpa_actual = \
                            df_dict['ctl']['smf70cpa_actual'].unique()[0].astype(INTEGER)
                    if current_lpar.sysplex_name != df_dict['ctl']['smf70xnm'].unique()[0]:
                        current_lpar.sysplex_name = df_dict['ctl']['smf70xnm'].unique()[0]
                    if current_lpar.smf70lpm != df_dict['ctl']['smf70lpm'].unique()[0]:
                        print(
                            'Current lpar system name is different to the one in the database with the same lpar number')
                        current_lpar.smf70lpm = df_dict['ctl']['smf70lpm'].unique()[0]
                        current_lpar.last_update_time = current_time
                    db_session.commit()

            for table in insert_dict.keys():
                if df_dict[table].shape[0] > 0 and table in tbls.keys():
                    insert_dict[table] = df_dict[table].shape[0]
                    if table in ['ctl', 'cpu']:
                        df_dict[table]['date'] = df_dict[table].index.get_level_values('datetime').date
                        if table == 'ctl':
                            df_dict[table] = df_dict['ctl'][df_dict['ctl']['isFirst']]
                    df_table = df_dict[table].reset_index()

                    if table == 'bct_cpu':
                        insert_dict[table] = df_insert_by_partitions(db_driver, db_engines, db_session, df_table, tblnames[table], tbls[table],
                                  'smf70', int_dtypedict[table], '70', partitions_scheme, False)
                    else:
                        insert_dict[table] = df_insert_by_partitions(db_driver, db_engines, db_session, df_table, tblnames[table], tbls[table],
                                  'smf70', int_dtypedict[table], '70', partitions_scheme, True)

            result_list.append({tblnames[k]:v for k,v in insert_dict.items() if k in tblnames.keys()})

        et = time.time()  # get the end time
        # get the execution time
        elapsed_time = (et - st) / 60
        print(f'Execution time ({jsonfile}):', elapsed_time, 'minutes')

    overall_et = time.time()
    overall_elapsed_time = (overall_et - overall_st) / 60
    return UploadResult(result_list, overall_elapsed_time, SUCCESS)

