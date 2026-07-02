import datetime as dt
import time
from pathlib import Path

import click
import numpy as np
import pandas as pd
from sqlalchemy import select, and_, func
from sqlalchemy.ext.horizontal_shard import set_shard_id
from sqlalchemy.orm import Session

from smf2db import SUCCESS, UPLOAD_ERROR, JSON_ERROR
from smf2db.api.api_30 import format_30df
from smf2db.api.util import (cal_tcb_time, cal_srb_time, cal_msu,
                             UploadResult, df_insert_by_partitions, create_int_dtypedict)
from smf2db.db_models.smf30_model import (Smf30Id, Smf30Ura, Smf30Prf, Smf30Cas, Smf30Sap, Smf30Ops, Smf30Exp, Smf30Op,
                                          Smf30Ud, Smf30Uss, Smf306)
from smf2db.db_models.smf7x_model import SmfLpar

col_dict = {'ura': ['smf30inp', 'smf30tep', 'smf30tpt', 'smf30tgt', 'smf30tcn', 'smf30trr', 'smf30aic', 'smf30aid',
                    'smf30aiw', 'smf30ais', 'smf30eic', 'smf30eid', 'smf30eiw', 'smf30eis', 'smf30tex', 'smf30das'],
            'prf': ['smf30srv', 'smf30csu', 'smf30srb', 'smf30io', 'smf30mso', 'smf30eta', 'smf30esu', 'smf30etc',
                    'smf30jqt', 'smf30rqt', 'smf30hqt', 'smf30sqt', 'smf30srv_l', 'smf30csu_l', 'smf30srb_l',
                    'smf30io_l', 'smf30mso_l', 'smf30esu_l', 'smf30_capacity_change_cnt'],
            'cas': ['smf30cpt', 'smf30cps', 'smf30icu', 'smf30isb', 'smf30jvu', 'smf30ivu', 'smf30jva', 'smf30iva',
                    'smf30iip', 'smf30rct', 'smf30hpt', 'smf30csc', 'smf30dmi', 'smf30dmo', 'smf30asr', 'smf30enc',
                    'smf30det', 'smf30cep', 'smf30_time_on_ifa', 'smf30_enclave_time_on_ifa',
                    'smf30_dep_enclave_time_on_ifa', 'smf30_time_ifa_on_cp', 'smf30_enclave_time_ifa_on_cp',
                    'smf30_dep_enclave_time_ifa_on_cp', 'smf30cepi', 'smf30_time_on_ziip', 'smf30_enclave_time_on_ziip',
                    'smf30_depenc_time_on_ziip', 'smf30_time_ziip_on_cp', 'smf30_enclave_time_ziip_on_cp',
                    'smf30_depenc_time_ziip_on_cp', 'smf30_enclave_time_ziip_qual', 'smf30_depenc_time_ziip_qual',
                    'smf30crp', 'smf30_time_java_on_ziip', 'smf30_enclave_time_java_on_ziip',
                    'smf30_depenc_time_java_on_ziip', 'smf30_time_java_on_cp', 'smf30_enclave_time_java_on_cp',
                    'smf30_depenc_time_java_on_cp', 'smf30icu_step_term', 'smf30icu_step_init', 'smf30isb_step_term',
                    'smf30isb_step_init', 'smf30_missed_smf30blk', 'smf30_missed_smf30dct'],
            'sap': ['smf30pgi', 'smf30pgo', 'smf30cpm', 'smf30nsw', 'smf30psi', 'smf30pso', 'smf30vpi', 'smf30vpo',
                    'smf30vpr', 'smf30cpi', 'smf30hpi', 'smf30lpi', 'smf30hpo', 'smf30pst', 'smf30psc', 'smf30pie',
                    'smf30poe', 'smf30bia', 'smf30boa', 'smf30bie', 'smf30boe', 'smf30kia', 'smf30koa', 'smf30kie',
                    'smf30koe', 'smf30psf', 'smf30pai', 'smf30pei', 'smf30ers', 'smf30tih',
                    'smf30userdataspacecreatereqcount'],
            'ops': ['smf30pdm', 'smf30prd', 'smf30ptm', 'smf30tpr', 'smf30mtm', 'smf30msr']}
cur_dict = {'ops': [],
            'ura': [],
            'sap': ['smf30hvr', 'smf30hva', 'smf30numberofdataspaceshwm'],
            'cas': ['ziipboost_active', 'speedboost_active', 'boostclass', 'smf30_highest_task_cpu_percent',
                    'smf30_highest_task_cpu_program'],
            'prf': ['smf30tat', 'smf30res', 'smf30trs', 'smf30msc', 'smf30loc', 'smf30znf', 'smf30snf']}

tbls = {'smf30_id': Smf30Id,
        'smf30_6': Smf306,
        'smf30_ura': Smf30Ura,
        'smf30_prf': Smf30Prf,
        'smf30_cas': Smf30Cas,
        'smf30_sap': Smf30Sap,
        'smf30_ops': Smf30Ops,
        'smf30_exp': Smf30Exp,
        'smf30_op': Smf30Op,
        'smf30_ud': Smf30Ud,
        'smf30_uss': Smf30Uss}
tblnames = {'smf30_id': 'smf30_id',
            'smf30_6': 'smf30_6',
            'smf30_ura': 'smf30_ura',
            'smf30_prf': 'smf30_prf',
            'smf30_cas': 'smf30_cas',
            'smf30_sap': 'smf30_sap',
            'smf30_ops': 'smf30_ops',
            'smf30_exp': 'smf30_exp',
            'smf30_op': 'smf30_op',
            'smf30_ud': 'smf30_ud',
            'smf30_uss': 'smf30_uss'}
tbldict = {'core': 'smf30_id',
           'core6': 'smf30_6',
           'ura': 'smf30_ura',
           'prf': 'smf30_prf',
           'cas': 'smf30_cas',
           'sap': 'smf30_sap',
           'ops': 'smf30_ops',
           'exp': 'smf30_exp',
           'op': 'smf30_op',
           'ud': 'smf30_ud',
           'uss': 'smf30_uss'}


int_dtypedict = create_int_dtypedict(tbls)

def upload_30db(db_engines: dict, db_session: Session, jsonfiles: str, partitions_scheme: str,
                db_driver: str = 'sqlite', interval: int=30) -> UploadResult:
    """Upload smf30 JSON files to the database.

    Args:
        db_engines: A dictionary of all the db_engines in the database.
        db_session: SQLAlchemy session.
        jsonfiles: JSON file or files.
        partitions_scheme: Partitions scheme (weekday, day, week).
        db_driver: Db driver is used to connect to the database.
        interval: A integer indicating time interval in minutes generating smf records.

    Returns:
        A NamedTuple including the insert dictionary, total elapsed time of the upload and the return code.
    """
    smf306_columns = Smf306.__table__.columns.keys()
    tcb_time = np.vectorize(cal_tcb_time)
    srb_time = np.vectorize(cal_srb_time)
    consumed_msu = np.vectorize(cal_msu)
    overall_st = time.time()


    result_list = []

    for jsonfile in jsonfiles:
        if not Path(jsonfile).is_file() or Path(jsonfile).suffix != '.json':
            continue
        st = time.time()
        # session start
        current_time = dt.datetime.now()

        insert_dict = {'core': 0, 'core6': 0, 'ura': 0, 'prf': 0, 'cas': 0, 'uss': 0, 'exp': 0, 'sap': 0, 'op': 0,
                       'ops': 0, 'ud': 0}
        with open(jsonfile) as f:
            try:
                df = pd.read_json(f)
            except ValueError:
                click.echo(
                    f"\nInvalid JSON file {jsonfile}. This file will be skipped.")
                continue

            try:
                df_dict, stc_interval = format_30df(df, interval)
            except Exception as e:
                click.echo(f"\nUnsupported JSON file {jsonfile} with error: {str(e)}. This file will be skipped.")
                continue

            if df_dict['id'].empty:
                click.echo(
                    f"\nThis JSON file {jsonfile} is not for this smf type. This file will be skipped.")
                # Cannot continue processing
                continue

            csc_list = []
            if df_dict['core'].shape[0] > 0:
                stmt = select(SmfLpar.csc).filter(
                    and_(SmfLpar.sysplex_name == df_dict['core']['smf30syp'].unique()[0],
                         SmfLpar.system_name == df_dict['core']['smf30syn'].unique()[0])).order_by(
                    SmfLpar.last_update_time.desc()).options(set_shard_id('smf.0'))
                try:
                    csc_list = db_session.execute(stmt).first()
                except Exception as e:
                    click.secho(
                        f"\nThis smf type cannot be processed until Smf70 have been initialized and the corresponding Smf70 Subtype 1 records have been processed.",
                        err=True,
                        fg="red"
                    )
                    raise SystemExit(1)
            elif df_dict['id'].shape[0] > 0:
                stmt = select(SmfLpar.csc).filter(
                    and_(SmfLpar.sysplex_name == df_dict['id']['smf30syp'].unique()[0],
                         SmfLpar.system_name == df_dict['id']['smf30syn'].unique()[0])).order_by(
                    SmfLpar.last_update_time.desc()).options(set_shard_id('smf.0'))
                try:
                    csc_list = db_session.execute(stmt).first()
                except Exception as e:
                    click.secho(
                        f"\nThis smf type cannot be processed until Smf70 have been initialized and the corresponding Smf70 Subtype 1 records have been processed.",
                        err=True,
                        fg="red"
                    )
                    raise SystemExit(1)

            if csc_list is None and df_dict['id'].shape[0] > 0:
                click.echo(
                    f"\nThe file {jsonfile} cannot be processed until the corresponding Smf70 Subtype 1 records have been processed. This file will be skipped.")
                continue

            elif len(csc_list) > 0:
                csc = csc_list[0]

            if df_dict['core1'].shape[0] > 0:
                df_dict['core1']['csc'] = csc
            if df_dict['core'].shape[0] > 0:
                df_dict['core']['csc'] = csc
            if df_dict['main'].shape[0] > 0:
                df_dict['main']['csc'] = csc
            if df_dict['ura'].shape[0] > 0:
                df_dict['ura']['csc'] = csc
            if df_dict['prf'].shape[0] > 0:
                df_dict['prf']['csc'] = csc
            if df_dict['cas'].shape[0] > 0:
                df_dict['cas']['csc'] = csc
            if df_dict['sap'].shape[0] > 0:
                df_dict['sap']['csc'] = csc
            if df_dict['op'].shape[0] > 0:
                df_dict['op']['csc'] = csc
            if df_dict['ops'].shape[0] > 0:
                df_dict['ops']['csc'] = csc
            if df_dict['ud'].shape[0] > 0:
                df_dict['ud']['csc'] = csc
            if df_dict['uss'].shape[0] > 0:
                df_dict['uss']['csc'] = csc
            if df_dict['exp'].shape[0] > 0:
                df_dict['exp']['csc'] = csc

            if df_dict['core'].shape[0] > 0:
                df_dict['main'] = df_dict['main'].reset_index().set_index(
                    ['csc', 'smf30syp', 'smf30syn', 'start_interval', 'wkl', 'smf30typ', 'smf30jbn', 'smf30asi',
                     'smf30jnm', 'smf30stn', 'gid', 'suffix'])
            else:  # subtype 1 only
                df_dict['main'] = pd.DataFrame(
                    columns=['csc', 'smf30syp', 'smf30syn', 'start_interval', 'wkl', 'smf30typ', 'smf30jbn', 'smf30asi',
                             'smf30jnm', 'smf30stn', 'gid', 'suffix', 'excp_num', 'unix_process_num', 'usage_data_num']
                ).set_index(
                    ['csc', 'smf30syp', 'smf30syn', 'start_interval', 'wkl', 'smf30typ', 'smf30jbn', 'smf30asi',
                     'smf30jnm', 'smf30stn', 'gid', 'suffix'])
            if df_dict['core1'].shape[0] > 0:
                df_dict['core1'] = df_dict['core1'].reset_index().set_index(
                    ['csc', 'smf30syp', 'smf30syn', 'start_interval', 'wkl', 'smf30typ', 'smf30jbn', 'smf30asi',
                     'smf30jnm', 'smf30stn', 'gid', 'suffix', 'excp_num', 'unix_process_num', 'usage_data_num'])

            df_dict['core'] = df_dict['core'].reset_index().set_index(
                ['csc', 'smf30syp', 'smf30syn', 'start_interval', 'wkl', 'smf30typ', 'smf30jbn',
                 'smf30asi', 'smf30jnm', 'smf30stn', 'gid', 'suffix'])
            if not df_dict['exp'].empty:
                grp_df_exp = df_dict['exp'].reset_index().groupby(
                    ['csc', 'smf30syp', 'smf30syn', 'start_interval', 'wkl', 'smf30typ', 'smf30jbn', 'smf30asi',
                     'smf30jnm', 'smf30stn', 'gid', 'suffix']
                ).agg({'dd_idx': 'max'}).astype({'dd_idx': 'int32'}).reset_index().set_index(
                    ['csc', 'smf30syp', 'smf30syn', 'start_interval', 'wkl', 'smf30typ', 'smf30jbn', 'smf30asi',
                     'smf30jnm', 'smf30stn', 'gid', 'suffix'])

                if df_dict['core'].shape[0] > 0:
                    indexes = df_dict['core'].loc[df_dict['core'].index.isin(grp_df_exp.index)].index
                    df_dict['core'].loc[indexes, 'excp_num'] = grp_df_exp.loc[indexes, 'dd_idx']
                    df_dict['core'].loc[indexes, 'excp_num'] = df_dict['core'].loc[indexes, 'excp_num'] + 1

            if not df_dict['ud'].empty:
                grp_df_ud = df_dict['ud'].reset_index().groupby(
                    ['csc', 'smf30syp', 'smf30syn', 'start_interval', 'wkl', 'smf30typ', 'smf30jbn', 'smf30asi',
                     'smf30jnm', 'smf30stn', 'gid', 'suffix']).agg({
                    'prod_idx': 'max'}).astype({'prod_idx': 'int32'}).reset_index().set_index(
                    ['csc', 'smf30syp', 'smf30syn', 'start_interval', 'wkl', 'smf30typ', 'smf30jbn', 'smf30asi',
                     'smf30jnm', 'smf30stn', 'gid', 'suffix'])

                if df_dict['core'].shape[0] > 0:
                    indexes = df_dict['core'].loc[df_dict['core'].index.isin(grp_df_ud.index)].index
                    df_dict['core'].loc[indexes, 'usage_data_num'] = grp_df_ud.loc[indexes, 'prod_idx']
                    df_dict['core'].loc[indexes, 'usage_data_num'] = df_dict['core'].loc[indexes, 'usage_data_num'] + 1

            if not df_dict['op'].empty:
                grp_df_op = df_dict['op'].reset_index().groupby(
                    ['csc', 'smf30syp', 'smf30syn', 'start_interval', 'wkl', 'smf30typ', 'smf30jbn', 'smf30asi',
                     'smf30jnm', 'smf30stn', 'gid', 'suffix']).agg({
                    'proc_idx': 'max'}).astype({'proc_idx': 'int32'}).reset_index().set_index(
                    ['csc', 'smf30syp', 'smf30syn', 'start_interval', 'wkl', 'smf30typ', 'smf30jbn', 'smf30asi',
                     'smf30jnm', 'smf30stn', 'gid', 'suffix'])

                if df_dict['core'].shape[0] > 0:
                    indexes = df_dict['core'].loc[df_dict['core'].index.isin(grp_df_op.index)].index
                    df_dict['core'].loc[indexes, 'unix_process_num'] = grp_df_op.loc[indexes, 'proc_idx']
                    df_dict['core'].loc[indexes, 'unix_process_num'] = df_dict['core'].loc[indexes, 'unix_process_num'] + 1

            # insert into detail tables
            if df_dict['core1'].shape[0] > 0:
                insert_dict['core'] = df_insert_by_partitions(db_driver, db_engines, db_session,
                                                            df_dict['core1'].reset_index()[Smf30Id.__table__.columns.keys()],
                                                            tblnames['smf30_id'], tbls['smf30_id'], 'smf30', int_dtypedict['smf30_id'],
                                                            '30', partitions_scheme, True)
            if df_dict['core'].shape[0] > 0:
                add_core_recs = df_insert_by_partitions(db_driver, db_engines, db_session,
                                                        df_dict['core'].reset_index()[
                                                            [column for column in list(
                                                                filter(None, df_dict['core'].index.names + df_dict['core'].columns.values.tolist())
                                                            ) if column in Smf30Id.__table__.columns.keys()]],
                                                        tblnames['smf30_id'], tbls['smf30_id'], 'smf30', int_dtypedict['smf30_id'],
                                                        '30', partitions_scheme, True)
                insert_dict['core'] += add_core_recs
            if df_dict['cas'].shape[0] > 0:
                insert_dict['cas'] = df_insert_by_partitions(db_driver, db_engines, db_session,
                                                            df_dict['cas'].reset_index()[
                                                                [column for column in list(
                                                                    filter(None, df_dict['cas'].index.names + df_dict['cas'].columns.values.tolist())
                                                                ) if column in Smf30Cas.__table__.columns.keys()]],
                                                            tblnames['smf30_cas'], tbls['smf30_cas'], 'smf30', int_dtypedict['smf30_cas'],
                                                            '30', partitions_scheme, True)
            if df_dict['prf'].shape[0] > 0:
                insert_dict['prf'] = df_insert_by_partitions(db_driver, db_engines, db_session,
                                                            df_dict['prf'].reset_index()[Smf30Prf.__table__.columns.keys()],
                                                            tblnames['smf30_prf'], tbls['smf30_prf'], 'smf30', int_dtypedict['smf30_prf'],
                                                            '30', partitions_scheme, True)
            if df_dict['ura'].shape[0] > 0:
                insert_dict['ura'] = df_insert_by_partitions(db_driver, db_engines, db_session,
                                                            df_dict['ura'].reset_index()[Smf30Ura.__table__.columns.keys()],
                                                            tblnames['smf30_ura'], tbls['smf30_ura'], 'smf30', int_dtypedict['smf30_ura'],
                                                            '30', partitions_scheme, True)
            if df_dict['sap'].shape[0] > 0:
                insert_dict['sap'] = df_insert_by_partitions(db_driver, db_engines, db_session,
                                                            df_dict['sap'].reset_index()[
                                                                [column for column in list(
                                                                    filter(None, df_dict['sap'].index.names + df_dict['sap'].columns.values.tolist())
                                                                ) if column in Smf30Sap.__table__.columns.keys()]],
                                                            tblnames['smf30_sap'], tbls['smf30_sap'], 'smf30', int_dtypedict['smf30_sap'],
                                                            '30', partitions_scheme, True)
            if df_dict['ops'].shape[0] > 0:
                insert_dict['ops'] = df_insert_by_partitions(db_driver, db_engines, db_session,
                                                            df_dict['ops'].reset_index()[Smf30Ops.__table__.columns.keys()],
                                                            tblnames['smf30_ops'], tbls['smf30_ops'], 'smf30', int_dtypedict['smf30_ops'],
                                                            '30', partitions_scheme, True)
            if df_dict['exp'].shape[0] > 0:
                insert_dict['exp'] = df_insert_by_partitions(db_driver, db_engines, db_session,
                                                            df_dict['exp'].reset_index()[Smf30Exp.__table__.columns.keys()],
                                                            tblnames['smf30_exp'], tbls['smf30_exp'], 'smf30', int_dtypedict['smf30_exp'],
                                                            '30', partitions_scheme, True)
            if df_dict['op'].shape[0] > 0:
                insert_dict['op'] = df_insert_by_partitions(db_driver, db_engines, db_session,
                                                            df_dict['op'].reset_index()[Smf30Op.__table__.columns.keys()],
                                                            tblnames['smf30_op'], tbls['smf30_op'], 'smf30', int_dtypedict['smf30_op'],
                                                            '30', partitions_scheme, True)
            if df_dict['ud'].shape[0] > 0:
                insert_dict['ud'] = df_insert_by_partitions(db_driver, db_engines, db_session,
                                                            df_dict['ud'].reset_index()[Smf30Ud.__table__.columns.keys()],
                                                            tblnames['smf30_ud'], tbls['smf30_ud'], 'smf30', int_dtypedict['smf30_ud'],
                                                            '30', partitions_scheme, True)
            if df_dict['uss'].shape[0] > 0:
                insert_dict['uss'] = df_insert_by_partitions(db_driver, db_engines, db_session,
                                                            df_dict['uss'].reset_index()[
                                                                [column for column in list(
                                                                    filter(None, df_dict['uss'].index.names + df_dict['uss'].columns.values.tolist())
                                                                ) if column in Smf30Uss.__table__.columns.keys()]],
                                                            tblnames['smf30_uss'], tbls['smf30_uss'], 'smf30', int_dtypedict['smf30_uss'],
                                                            '30', partitions_scheme, True)

            # Start process subtype 6
            if df_dict['core'].shape[0] > 0:
                updated_col_list = smf306_columns.copy()
                updated_col_list.remove('prev_start_interval')
                start = df_dict['core'].index.get_level_values('start_interval').min() - stc_interval
                end = df_dict['core'].index.get_level_values('start_interval').max() + stc_interval
                span = end - start

                for i in range(span.days + 1):
                    day = start + dt.timedelta(days=i)
                    if partitions_scheme == 'weekday':
                        engine = f'30.{day.isoweekday()}'
                    elif partitions_scheme == 'day':
                        engine = f'30.{day.day}'
                    elif partitions_scheme == 'week':
                        engine = f'30.{day.isocalendar().week}'
                    else:
                        engine = '30.1'
                    subquery = db_session.query(Smf306.gid)
                    cur6_df = pd.read_sql_query(
                        sql=db_session.query(Smf30Id,
                                             Smf30Ura,
                                             Smf30Cas,
                                             Smf30Prf,
                                             Smf30Sap,
                                             Smf30Ops).join(
                            Smf30Id.smf30_ura).join(Smf30Id.smf30_cas).join(Smf30Id.smf30_prf).join(Smf30Id.smf30_sap).join(
                            Smf30Id.smf30_ops).filter(
                            and_((Smf30Id.smf30typ == 6),
                                 (func.date(Smf30Id.start_interval) == day.date()),
                                 (~Smf30Id.gid.in_(subquery)))
                        ).statement,
                        con=db_engines[engine])[updated_col_list].set_index(
                        ['csc', 'smf30syp', 'smf30syn', 'start_interval', 'wkl', 'smf30jbn', 'smf30asi', 'smf30jnm',
                         'smf30stn', 'smf30typ']).sort_index()
                    cur6_df = cur6_df.copy() # reload the dataframe to avoid defragmentation
                    cur6_df['prev_start_interval'] = cur6_df.index.get_level_values('start_interval') - stc_interval
                    prev6_index = pd.MultiIndex.from_frame(
                        pd.DataFrame(cur6_df.copy().reset_index()[['csc', 'smf30syp', 'smf30syn', 'prev_start_interval', 'wkl',
                                                            'smf30jbn', 'smf30asi', 'smf30jnm', 'smf30stn', 'smf30typ']]))
                    prev6_df = cur6_df.loc[cur6_df.index.isin(prev6_index)]

                    if prev6_df.shape[0] > 0:
                        cur6_prev6_df = cur6_df.reset_index().rename(
                            columns={'start_interval': 'next_start_interval'}).rename(
                            columns={'prev_start_interval': 'start_interval'}).set_index(
                            ['csc', 'smf30syp', 'smf30syn', 'start_interval', 'wkl', 'smf30jbn', 'smf30asi', 'smf30jnm',
                             'smf30stn', 'smf30typ'])
                        new_df = cur6_prev6_df.loc[prev6_df.index].drop(columns=['next_start_interval'])
                        orig_df = cur6_prev6_df.loc[prev6_df.index].reset_index().rename(
                            columns={'start_interval': 'prev_start_interval', 'next_start_interval': 'start_interval'}
                        ).set_index(['csc', 'smf30syp', 'smf30syn', 'start_interval', 'wkl', 'smf30jbn', 'smf30asi',
                                     'smf30jnm', 'smf30stn', 'smf30typ'])
                        df6 = pd.concat([new_df[col_dict['cas']] - prev6_df[col_dict['cas']],
                                         new_df[col_dict['prf']] - prev6_df[col_dict['prf']],
                                         new_df[col_dict['ura']] - prev6_df[col_dict['ura']],
                                         new_df[col_dict['sap']] - prev6_df[col_dict['sap']],
                                         new_df[col_dict['ops']] - prev6_df[col_dict['ops']],
                                         new_df[cur_dict['cas'] + cur_dict['prf'] + cur_dict['ura'] + cur_dict['sap'] +
                                                cur_dict['ops']]
                                         ], axis=1).reset_index(drop=True).set_index(orig_df.index)
                        remain_cols = list(set([col for col in orig_df.reset_index().columns]) - set(
                            [col for col in df6.reset_index().columns]))
                        df6 = pd.concat([orig_df.reset_index()[remain_cols], df6.reset_index()], axis=1).set_index(
                            ['csc', 'smf30syp', 'smf30syn', 'start_interval', 'wkl', 'smf30jbn', 'smf30asi',
                             'smf30jnm', 'smf30stn', 'smf30typ'])
                        df6['tcb_time'] = tcb_time(df6['smf30cpt'], df6['smf30cpc'], df6['smf30csu_l'],
                                                   df6['smf30sus'])
                        df6['srb_time'] = srb_time(df6['smf30cps'], df6['smf30src'], df6['smf30srb_l'],
                                                   df6['smf30sus'])

                        df6['cpu_total'] = (df6['smf30cpt'] + df6['smf30cps'] +
                                            df6['smf30hpt'] + df6['smf30iip'] +
                                            df6['smf30rct'] + df6['smf30icu_step_term'] +
                                            df6['smf30icu_step_init'] + df6['smf30isb_step_term'] + df6['smf30isb_step_init'])
                        df6['consumed_msu'] = consumed_msu(df6['smf30_rctpcpua_actual'], df6['cpu_total'],
                                                           df6['smf30_rctpcpua_scaling_factor'])

                        if df6.shape[0] > 0:
                            insert_dict['core6'] = df_insert_by_partitions(db_driver, db_engines, db_session,
                                                                            df6.reset_index()[Smf306.__table__.columns.keys()],
                                                                            tblnames['smf30_6'], tbls['smf30_6'], 'smf30', int_dtypedict['smf30_6'],
                                                                            '30', partitions_scheme, True)

            result_list.append({tbldict[k]:v for k,v in insert_dict.items() if k in tbldict.keys()})

        et = time.time()  # get the end time
        # get the execution time
        elapsed_time = (et - st) / 60
        print(f'Execution time ({jsonfile}):', elapsed_time, 'minutes.')

    overall_et = time.time()
    overall_elapsed_time = (overall_et - overall_st) / 60
    return UploadResult(result_list, overall_elapsed_time, SUCCESS)
