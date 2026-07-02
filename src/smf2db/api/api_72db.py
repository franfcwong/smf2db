import datetime as dt
import time
from pathlib import Path

import click
import numpy as np
import pandas as pd
from sqlalchemy import select, and_
from sqlalchemy.ext.horizontal_shard import set_shard_id
from sqlalchemy.orm import Session

from smf2db import SUCCESS, JSON_ERROR
from smf2db.api.api_72 import (cal_performance_index, format_72df, agg_scs_group_by, agg_rts)
from smf2db.api.util import (get_lpar_info_in_db, UploadResult,
                             create_int_dtypedict, df_insert_by_partitions, df_upsert_by_partitions)
from smf2db.db_models.smf70_model import Smf70Ctl
from smf2db.db_models.smf72_model import (Smf72Pro, Smf72Policy, Smf72Dnsx, Smf72Workload, Smf72Wrsx, Smf72Scs,
                                          Smf72Data, Smf72Sctl, Smf72Wms, Smf72Sss, Smf72Rgs, Smf72Rts, Smf72Wrs,
                                          Smf72Dns, Smf72Cmss, Smf72Ceds, Smf72Clod, Smf72Clrd, Smf72Lotd, Smf72Lasc,
                                          Smf72Lare, Smf72Ense, Smf72Ensy, Smf72Enss, Smf72Qsad, Smf72Clas, Smf72Csms)

tbls = {'pro': Smf72Pro,
        'policy': Smf72Policy,
        'workload': Smf72Workload,
        'wms': Smf72Wms,
        'sss': Smf72Sss,
        'rgs': Smf72Rgs,
        'rts': Smf72Rts,
        'wrs': Smf72Wrs,
        'wrsx': Smf72Wrsx,
        'dns': Smf72Dns,
        'dnsx': Smf72Dnsx,
        'cmss': Smf72Cmss,
        'ceds': Smf72Ceds,
        'clas': Smf72Clas,
        'csms': Smf72Csms,
        'clod': Smf72Clod,
        'clrd': Smf72Clrd,
        'lotd': Smf72Lotd,
        'lare': Smf72Lare,
        'lasc': Smf72Lasc,
        'ense': Smf72Ense,
        'enss': Smf72Enss,
        'ensy': Smf72Ensy,
        'qsad': Smf72Qsad,
        'scs': Smf72Scs,
        'data': Smf72Data,
        'sctl': Smf72Sctl}
tblnames = {'pro': 'smf72_pro',
            'policy': 'smf72_policy',
            'workload': 'smf72_workload',
            'wms': 'smf72_wms',
            'sss': 'smf72_sss',
            'rgs': 'smf72_rgs',
            'rts': 'smf72_rts',
            'wrs': 'smf72_wrs',
            'wrsx': 'smf72_wrsx',
            'dns': 'smf72_dns',
            'dnsx': 'smf72_dnsx',
            'cmss': 'smf72_cmss',
            'ceds': 'smf72_ceds',
            'clas': 'smf72_clas',
            'csms': 'smf72_csms',
            'clod': 'smf72_clod',
            'clrd': 'smf72_clrd',
            'lotd': 'smf72_lotd',
            'lare': 'smf72_lare',
            'lasc': 'smf72_lasc',
            'ense': 'smf72_ense',
            'enss': 'smf72_enss',
            'ensy': 'smf72_ensy',
            'qsad': 'smf72_qsad',
            'scs': 'smf72_scs',
            'data': 'smf72_data',
            'sctl': 'smf72_sctl'}

int_dtypedict = create_int_dtypedict(tbls)

agg_wms = {'r723ggnm': 'last', 'r723mcde': 'first', 'r723mscf': 'last', 'r723mflg': 'last', 'r723mfl2': 'last',
           'stor_protection': 'first', 'cpu_protection': 'first',
           'velocity_io_delays': 'first', 'svpol_unaval': 'first', 'rcaa_unaval': 'first',
           'tenant_report_class': 'first', 'honor_prio': 'max', 'hismt_failure': 'max', 'ziip_honor_prio': 'max',
           'zaap_honor_prio': 'max', 'zaap_crossover': 'max',
           'r723mtvl': 'first', 'r723mtv_': 'sum',
           'r723mcpg': 'first', 'r723msub': 'first', 'r723clsc': 'first', 'smf72int': 'sum',
           'appl_percentage_cp_time': 'mean', 'appl_percentage_iipcp_time': 'mean', 'appl_percentage_iip_time': 'mean',
           'appl_percentage_aapcp_time': 'mean', 'appl_percentage_aap_time': 'mean',
           'transaction_total_percentage_cp_time': 'mean', 'transaction_total_percentage_sp_on_cp_time': 'mean',
           'transaction_total_percentage_sp_time': 'mean', 'transaction_mobile_percentage_cp_time': 'mean',
           'transaction_mobile_percentage_sp_on_cp_time': 'mean', 'transaction_mobile_percentage_sp_time': 'mean',
           'transaction_cata_percentage_cp_time': 'mean', 'transaction_cata_percentage_sp_on_cp_time': 'mean',
           'transaction_cata_percentage_sp_time': 'mean', 'transaction_catb_percentage_cp_time': 'mean',
           'transaction_catb_percentage_sp_on_cp_time': 'mean', 'transaction_catb_percentage_sp_time': 'mean'}
agg_scs = {'smf_type': 'first', 'r723cimp': 'first', 'r723crs1': 'last', 'r723cadf': 'last', 'r723crtf': 'last',
           'r723crgf': 'last',
           'is_heterogeneous': 'first', 'r723ceda': 'first',
           'r723crta': 'first', 'r723crca': 'first', 'response_time_hours': 'first', 'response_time_minutes': 'first',
           'response_time_seconds': 'first', 'response_time_millisec': 'first', 'r723cstm': 'first',
           'r723cdsc': 'first', 'r723cvel': 'first', 'r723cavg': 'first', 'r723cprc': 'first',
           'class_goal_type': 'first', 'r723cval': 'first', 'r723cpct': 'first', 'r723cdur': 'first',
           'r723rtdm': 'last', 'r723csrv': 'sum', 'r723ccpu': 'sum', 'r723cioc': 'sum', 'r723cmso': 'sum',
           'r723csrb': 'sum', 'r723cpir': 'sum', 'r723chpi': 'sum', 'r723cbpi': 'sum', 'r723cpie': 'sum',
           'r723cbpe': 'sum', 'r723cbka': 'sum', 'r723cbke': 'sum', 'r723cprs': 'sum', 'r723cers': 'sum',
           'r723ctrr': 'sum', 'r723ctat': 'sum', 'r723crct': 'sum', 'r723ciit': 'sum', 'r723chst': 'sum',
           'r723cswc': 'sum', 'r723ccrm': 'sum', 'r723crcp': 'sum', 'r723carc': 'sum', 'r723cncp': 'sum',
           'r723canc': 'sum', 'r723ctet': 'sum', 'r723ctetx': 'sum', 'transaction_execution_time': 'sum',
           'r723cxetx': 'sum', 'r723cets': 'sum', 'r723cetsx': 'sum', 'r723ccus': 'sum', 'r723ctot': 'sum',
           'r723ccde': 'sum', 'r723ccca': 'sum', 'r723cswi': 'sum', 'r723cmpl': 'sum', 'r723capr': 'sum',
           'r723caco': 'sum', 'r723caxm': 'sum', 'r723cvio': 'sum', 'r723chsp': 'sum', 'r723cchs': 'sum',
           'sample_storage_delay': 'sum', 'r723cunk': 'sum', 'r723cidl': 'sum', 'r723cpde': 'sum', 'r723cpqu': 'sum',
           'r723csac': 'sum', 'r723csrs': 'sum', 'r723cspa': 'sum', 'r723cspe': 'sum', 'r723cict': 'sum',
           'r723ciwt': 'sum', 'r723cidt': 'sum', 'r723circ': 'sum', 'r723ctou': 'sum', 'r723ciou': 'sum',
           'r723ciod': 'sum', 'r723cq': 'sum', 'r723cspv': 'sum', 'r723csvi': 'sum', 'r723cshs': 'sum',
           'r723csmp': 'sum', 'r723cssw': 'sum', 'sample_server_delay': 'sum', 'r723cndi': 'sum', 'r723ctdq': 'sum',
           'r723ctsa': 'sum', 'r723ciot': 'sum', 'transaction_queue_delay_time': 'sum',
           'transaction_aff_delay_time': 'sum', 'transaction_jcl_time': 'sum', 'transaction_inel_delay_time': 'sum',
           'r723ciea': 'sum', 'r723cxea': 'sum', 'r723cfea': 'sum', 'r723apu': 'sum', 'r723apd': 'sum',
           'r723fqd': 'sum', 'sample_crypto_using': 'sum', 'sample_crypto_delay': 'sum', 'r723plsc': 'last',
           'r723rcod': 'sum', 'r723rcou': 'sum', 'r723ectc': 'sum', 'r723ifau': 'sum', 'r723ifcu': 'sum',
           'r723cifa': 'sum', 'r723cifc': 'sum', 'r723ifad': 'sum', 'r723supu': 'sum', 'r723sucu': 'sum',
           'r723supd': 'sum', 'r723csup': 'sum', 'r723csuc': 'sum', 'r723tpdp': 'sum', 'r723cpdp': 'sum',
           'r723lpdp': 'sum', 'r723spdp': 'sum', 'r723rtdc': 'sum', 'r723rtdt': 'last', 'r723tsucp': 'sum',
           'r723tsusp': 'sum', 'r723tsuocp': 'sum', 'r723msucp': 'sum', 'r723msusp': 'sum', 'r723msuocp': 'sum',
           'r723asucp': 'sum', 'r723asusp': 'sum', 'r723asuocp': 'sum', 'r723bsucp': 'sum', 'r723bsusp': 'sum',
           'r723bsuocp': 'sum', 'r723cqdtx': 'sum', 'r723cadtx': 'sum', 'r723ccvtx': 'sum', 'r723ciqtx': 'sum',
           'r723rtyp': 'first',
           'r723ress': 'sum', 'r723ract': 'sum', 'r723rrdy': 'sum', 'r723ridl': 'sum',
           'r723rwlo': 'sum', 'r723rwio': 'sum', 'r723rwco': 'sum', 'r723rwds': 'sum', 'r723rwsl': 'sum',
           'r723rwsn': 'sum', 'r723rwss': 'sum', 'r723rwtm': 'sum', 'r723rwo': 'sum', 'r723rwms': 'sum',
           'r723rssl': 'sum', 'r723rsss': 'sum', 'r723rssn': 'sum', 'r723rwst': 'sum', 'r723rwrt': 'sum',
           'r723rwwr': 'sum', 'r723rapp': 'sum', 'r723rwnl': 'sum', 'r723rbpm': 'sum', 'r723rw01': 'sum',
           'r723rw02': 'sum', 'r723rw03': 'sum', 'r723rw04': 'sum', 'r723rw05': 'sum', 'r723rw06': 'sum',
           'r723rw07': 'sum', 'r723rw08': 'sum', 'r723rw09': 'sum', 'r723rw10': 'sum', 'r723rw11': 'sum',
           'r723rw12': 'sum', 'r723rw13': 'sum', 'r723rw14': 'sum', 'r723rw15': 'sum', 'is_report_class': 'first',
           'sample_rate': 'first', 'r723madj': 'first', 'r723nffs': 'first', 'r723nffi': 'first', 'r723mcpu': 'first',
           'r723msrb': 'first', 'r723cpa_scaling_factor': 'first', 'r723cpa_actual': 'first', 'r723mcf': 'first',
           'r723mcfs': 'first', 'r723mcfi': 'first', 'r723mtv_': 'sum',
           'r723cxet': 'sum', 'r723cqdt': 'sum', 'r723cadt': 'sum', 'r723ccvt': 'sum', 'r723ciqt': 'sum',
           'r723enctrxnum': 'sum', 'r723enctrxcalls': 'sum', 'r723enctrxet': 'sum', 'r723enctrxets': 'sum'}

def get_cai_in_db(csc, sid, ctl_date, db_session, partitions_scheme):
    if partitions_scheme == 'weekday':
        partitions_range = range(1, 8)
    elif partitions_scheme == 'day':
        partitions_range = range(1, 32)
    elif partitions_scheme == 'week':
        partitions_range = range(1, 53)
    else:
        partitions_range = range(1, 2)
    try:
        for part in partitions_range:
            cai = db_session.execute(select(Smf70Ctl.smf70cai).filter(
                and_(Smf70Ctl.csc == csc, Smf70Ctl.smf70sid == sid)).options(set_shard_id(f'70.{part}'))).scalar()
            if cai is not None:
                return cai
    except Exception as e:
        click.secho(
            f"\nThis smf type cannot be processed until Smf70 have been initialized and the corresponding Smf70 Subtype 1records have been processed.",
            err=True,
            fg="red"
        )
        raise SystemExit(1)
    return None


def upload_72db(db_engines: dict, db_session: Session, jsonfiles: str, partitions_scheme: str,
                db_driver: str = 'postgresql+psycopg2') -> UploadResult:
    """Upload smf72 JSON files to the database.

    Args:
        db_engines: A dictionary of all the db_engines in the database.
        db_session: SQLAlchemy session.
        jsonfiles: JSON file or files.
        partitions_scheme: Partitions scheme.
        db_driver: Db driver to connect to database.

    Returns:
        A NamedTuple including the insert dictionary, total elapsed time of the upload and the return code.
    """

    # inner functions

    get_performance_index = np.vectorize(cal_performance_index)

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

    for jsonfile in jsonfiles:
        if not Path(jsonfile).is_file() or Path(jsonfile).suffix != '.json':
            continue
        st = time.time()
        # print(jsonfile)
        current_time = dt.datetime.now()
        insert_dict = {'pro': 0, 'policy': 0, 'workload': 0, 'rgs': 0, 'wms': 0, 'scs': 0, 'data': 0, 'sctl': 0,
                       'sss': 0, 'rts': 0, 'wrsx': 0, 'wrs': 0, 'dnsx': 0, 'dns': 0,
                       'cmss': 0, 'ceds': 0, 'clas': 0, 'csms': 0, 'lotd': 0, 'clod': 0, 'clrd': 0,
                       'lasc': 0, 'lare': 0, 'ense': 0, 'ensy': 0, 'enss': 0, 'qsad': 0}
        with open(jsonfile) as f:
            # program logic start here
            try:
                df = pd.read_json(f)
            except ValueError:
                click.echo(
                    f"\nInvalid JSON file {jsonfile}. This file will be skipped.")
                continue
            try:
                dfs_dict = format_72df(df, current_time)
            except Exception as e:
                click.echo(f"\nUnsupported JSON file {jsonfile} with error: {str(e)}. This file will be skipped.")
                continue

            if dfs_dict['pro'].empty:
                click.echo(
                    f"\nThis JSON file {jsonfile} is not for this smf type. This file will be skipped.")
                # Cannot continue processing
                continue
            else:
                csc, r723cpa_actual, r723cpa_scaling_factor = get_lpar_info_in_db(
                    dfs_dict['pro']['smf72xnm'].unique()[0],
                    dfs_dict['pro']['smf72snm'].unique()[0],
                    pd.to_numeric(
                        dfs_dict['pro']['smf72ptn'].unique()[0],
                        downcast="integer"),
                    db_session)
                if pd.isna(csc):
                    click.echo(
                        f"\nThe file {jsonfile} cannot be processed until the corresponding Smf70 Subtype 1 records have been processed. This file will be skipped.")
                    continue

                dfs_dict['pro']['r723cpa_actual'] = r723cpa_actual
                dfs_dict['pro']['r723cpa_scaling_factor'] = r723cpa_scaling_factor
                if dfs_dict['policy'].shape[0] > 0 and dfs_dict['policy']['r723cpa_actual'].isnull().all():
                    dfs_dict['policy']['r723cpa_actual'] = r723cpa_actual
                    dfs_dict['policy']['r723cpa_scaling_factor'] = r723cpa_scaling_factor
                if dfs_dict['scs'].shape[0] > 0 and dfs_dict['scs']['r723cpa_actual'].isnull().all():
                    dfs_dict['scs']['r723cpa_actual'] = r723cpa_actual
                    dfs_dict['scs']['r723cpa_scaling_factor'] = r723cpa_scaling_factor
                    dfs_dict['scs']['msu_physical'] = np.where(
                        dfs_dict['scs']['r723cpa_scaling_factor'] is not None,
                        dfs_dict['scs']['cpu_time'] * 16 * dfs_dict['scs']['r723cpa_scaling_factor']
                        / dfs_dict['scs']['r723cpa_actual'] * 3600 / dfs_dict['scs']['smf72int'], np.nan)

                cai_date = dfs_dict['policy'].index.get_level_values('datetime').unique()[0]
                cai = get_cai_in_db(csc, dfs_dict['policy']['smf72snm'].unique()[0], cai_date, db_session, partitions_scheme)
                if cai is None:
                    click.echo(
                        f"\nThe file {jsonfile} cannot be processed until the corresponding Smf70 Subtype 1 records have been processed. This file will be skipped.")
                    continue
                dfs_dict['policy']['smf70cai'] = cai

            # Update csc value in dataframes
            for table in dfs_dict.keys():
                if dfs_dict[table].shape[0] > 0:
                    dfs_dict[table] = dfs_dict[table].copy().reset_index()
                    dfs_dict[table]['csc'] = csc
                    dfs_dict[table].set_index([col.name for col in tbls[table].__table__.primary_key.columns.values()],
                                              inplace=True)

            for table in insert_dict.keys():
                if dfs_dict[table].shape[0] > 0: # and table not in ['dnsx', 'wrsx', 'wms']:
                    insert_dict[table] = df_insert_by_partitions(db_driver, db_engines, db_session,
                                                                 dfs_dict[table].reset_index(), tblnames[table],
                                                                 tbls[table],'smf72', int_dtypedict[table],
                                                        '72', partitions_scheme, True)

            if insert_dict['dnsx'] > 0:
                agg_dnsx = {'r723rwnn': 'sum'}
                dnsx_stmt = select(Smf72Dns).join_from(Smf72Dnsx, Smf72Dnsx.smf72_dnss).filter(
                    Smf72Dnsx.last_update_time.__eq__(current_time))
                df_dnss_list = []
                for part in partitions_range:
                    df_dns = pd.read_sql(dnsx_stmt, db_engines[f'72.{part}'])
                    if not df_dns.empty:
                        df_dnss_list.append(df_dns)
                if len(df_dnss_list) > 0:
                    df_dnss = pd.concat(df_dnss_list)
                    df_dnsx_ = df_dnss.groupby(
                        [col.name for col in Smf72Dnsx.__table__.primary_key.columns.values()]).agg(
                        agg_dnsx).reset_index()
                    df_dnsx_['last_update_time'] = current_time
                    dnsx_result = df_upsert_by_partitions(
                        db_driver, db_engines, db_session,
                        df_dnsx_[Smf72Dnsx.__table__.columns.keys()],
                        'smf72_dnsx', Smf72Dnsx, 'smf72',
                        [col.name for col in Smf72Dnsx.__table__.primary_key.columns.values()],
                        '72', partitions_scheme, int_dtypedict['dnsx']
                    )
                    insert_dict['dnsx'] = dnsx_result

            if insert_dict['wrsx'] > 0:
                agg_wrsx = {'r723rexe': 'max', 'r723rdbe': 'max', 'r723ress': 'sum', 'r723ract': 'sum',
                            'r723rrdy': 'sum', 'r723ridl': 'sum', 'r723rwlo': 'sum',
                            'r723rwio': 'sum', 'r723rwco': 'sum', 'r723rwds': 'sum', 'r723rwsl': 'sum',
                            'r723rwsn': 'sum', 'r723rwss': 'sum', 'r723rwtm': 'sum',
                            'r723rwo': 'sum', 'r723rwms': 'sum', 'r723rssl': 'sum', 'r723rsss': 'sum',
                            'r723rssn': 'sum', 'r723rwst': 'sum', 'r723rwrt': 'sum',
                            'r723rwwr': 'sum', 'r723rapp': 'sum', 'r723rwnl': 'sum', 'r723rbpm': 'sum',
                            'r723rw01': 'sum', 'r723rw02': 'sum', 'r723rw03': 'sum',
                            'r723rw04': 'sum', 'r723rw05': 'sum', 'r723rw06': 'sum', 'r723rw07': 'sum',
                            'r723rw08': 'sum', 'r723rw09': 'sum', 'r723rw10': 'sum',
                            'r723rw11': 'sum', 'r723rw12': 'sum', 'r723rw13': 'sum', 'r723rw14': 'sum',
                            'r723rw15': 'sum'}
                wrsx_stmt = select(Smf72Wrs).join_from(Smf72Wrsx, Smf72Wrsx.smf72_wrss).filter(
                    Smf72Wrsx.last_update_time.__eq__(current_time))
                df_wrss_list = []
                for part in partitions_range:
                    df_wrs = pd.read_sql(wrsx_stmt, db_engines[f'72.{part}'])
                    if not df_wrs.empty:
                        df_wrss_list.append(df_wrs)
                if len(df_wrss_list) > 0:
                    df_wrss = pd.concat(df_wrss_list)
                    df_wrsx_ = df_wrss.groupby(
                        [col.name for col in Smf72Wrsx.__table__.primary_key.columns.values()]).agg(
                        agg_wrsx).reset_index()
                    df_wrsx_['last_update_time'] = current_time
                    wrsx_result = df_upsert_by_partitions(
                        db_driver, db_engines, db_session,
                        df_wrsx_[Smf72Wrsx.__table__.columns.keys()],
                        'smf72_wrsx', Smf72Wrsx, 'smf72',
                        [col.name for col in Smf72Wrsx.__table__.primary_key.columns.values()],
                        '72', partitions_scheme, int_dtypedict['wrsx'],
                        )
                    insert_dict['wrsx'] = wrsx_result

            if insert_dict['wms'] > 0:
                wms_stmt1 = select(Smf72Scs).join_from(Smf72Wms, Smf72Wms.smf72_scss).filter(
                    Smf72Wms.last_update_time.__eq__(current_time))
                wms_stmt2 = select(Smf72Rts).join_from(Smf72Wms, Smf72Wms.smf72_rtss).filter(
                    Smf72Wms.last_update_time.__eq__(current_time))
                # total_wms = 0
                df_scss_list = []
                df_rtss_list = []
                df_rtss = pd.DataFrame()
                for part in partitions_range:
                    df_scs = pd.read_sql(wms_stmt1, db_engines[f'72.{part}'])
                    if not df_scs.empty:
                        df_scss_list.append(df_scs)
                        df_rts = pd.read_sql(wms_stmt2, db_engines[f'72.{part}'])
                        if not df_rts.empty:
                            df_rtss_list.append(df_rts)
                if len(df_scss_list) > 0:
                    df_scss = pd.concat(df_scss_list)
                    if len(df_rtss_list) > 0:
                        df_rtss = pd.concat(df_rtss_list)

                    if not df_scss.empty:
                        df_wms_1 = agg_scs_group_by(df_scss,
                                                    [col.name for col in Smf72Wms.__table__.primary_key.columns.values()],
                                                    'first',
                                                    'r723ctetx' in dfs_dict['scs'].columns)
                        if not df_rtss.empty:
                            df_wms_2 = df_rtss.groupby(
                                [col.name for col in Smf72Wms.__table__.primary_key.columns.values()]).agg(agg_rts)
                        else:
                            df_wms_2 = pd.DataFrame()
                        dfs_dict['wms'] = dfs_dict['wms'][
                            ['r723cimp', 'r723ggnm', 'r723mcde', 'r723mscf', 'r723mflg', 'is_report_class',
                             'r723mfl2', 'stor_protection', 'cpu_protection', 'velocity_io_delays',
                             'svpol_unaval', 'rcaa_unaval', 'tenant_report_class', 'honor_prio',
                             'hismt_failure', 'ziip_honor_prio', 'zaap_honor_prio', 'zaap_crossover',
                             'r723mtvl', 'r723mtv_', 'r723mcpg', 'r723msub', 'r723clsc', 'smf72int']].copy()
                        df_wms_x = pd.concat([dfs_dict['wms'],
                                              df_wms_1.drop(columns=['r723cimp', 'is_report_class', 'r723mtv_', 'smf72int']),
                                              df_wms_2], axis=1)
                        df_wms_x['performance_index'] = get_performance_index(df_wms_x['class_goal_type'],
                                                                              df_wms_x['execution_velocity'],
                                                                              df_wms_x['r723cval'],
                                                                              df_wms_x['r723cpct'],
                                                                              df_wms_x['class_rt_bucket_1'],
                                                                              df_wms_x['class_rt_bucket_2'],
                                                                              df_wms_x['class_rt_bucket_3'],
                                                                              df_wms_x['class_rt_bucket_4'],
                                                                              df_wms_x['class_rt_bucket_5'],
                                                                              df_wms_x['class_rt_bucket_6'],
                                                                              df_wms_x['class_rt_bucket_7'],
                                                                              df_wms_x['class_rt_bucket_8'],
                                                                              df_wms_x['class_rt_bucket_9'],
                                                                              df_wms_x['class_rt_bucket_10'],
                                                                              df_wms_x['class_rt_bucket_11'],
                                                                              df_wms_x['class_rt_bucket_12'],
                                                                              df_wms_x['class_rt_bucket_13'],
                                                                              df_wms_x['class_rt_bucket_14'])
                        df_wms_x['last_update_time'] = current_time

                        wms_result = df_upsert_by_partitions(
                            db_driver, db_engines, db_session,
                            df_wms_x.copy().reset_index()[Smf72Wms.__table__.columns.keys()],
                           'smf72_wms', Smf72Wms, 'smf72',
                            [col.name for col in Smf72Wms.__table__.primary_key.columns.values()],
                            '72', partitions_scheme,
                            int_dtypedict['wms']
                        )
                        insert_dict['wms'] = wms_result
            result_list.append({tblnames[k]:v for k,v in insert_dict.items() if k in tblnames.keys()})

        et = time.time()  # get the end time
        # get the execution time
        elapsed_time = (et - st) / 60
        print(f'Execution time ({jsonfile}):', elapsed_time, 'minutes')

    overall_et = time.time()
    overall_elapsed_time = (overall_et - overall_st) / 60
    return UploadResult(result_list, overall_elapsed_time, SUCCESS)

