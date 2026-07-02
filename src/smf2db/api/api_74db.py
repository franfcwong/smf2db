import datetime as dt
import time
from pathlib import Path

import click
import numpy as np
import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from smf2db import SUCCESS, JSON_ERROR
from smf2db.api.api_74 import format_74df
from smf2db.api.util import get_csc_in_db, agg_next, UploadResult, create_int_dtypedict, df_insert_by_partitions, \
    df_upsert_by_partitions
from smf2db.db_models.smf74_model import (Smf74Pro, Smf74Dctl, Smf74Dev, Smf74Xctl, Smf74Sys, Smf74Path,
                                          Smf74Mbr, Smf74Omvs, Smf74Cachsys, Smf74Cdev, Smf74Raid, Smf74Xpool,
                                          Smf74Rrank, Smf74Hfs, Smf74Gbuf, Smf74Fsys, Smf74Fcd, Smf74Switch,
                                          Smf74Port, Smf74Connector, Smf74Cntl, Smf74Lss, Smf74Extp, Smf74Rank,
                                          Smf74Arry, Smf74Siol, Smf74Pcie, Smf74Scm, Smf74Eadm, Smf74Cf, Smf74Lcf,
                                          Smf74Sreq, Smf74Proc, Smf74Cach, Smf74Cfrf, Smf74Subchpa, Smf74Mscm,
                                          Smf74Str, Smf74Srtd, Smf74Adup, Smf74Dupchpa)

tbls = {'pro': Smf74Pro, 'dctl': Smf74Dctl, 'dev': Smf74Dev, 'xctl': Smf74Xctl, 'sys': Smf74Sys, 'path': Smf74Path,
        'mbr': Smf74Mbr, 'omvs': Smf74Omvs, 'cf': Smf74Cf, 'lcf': Smf74Lcf, 'sreq': Smf74Sreq, 'proc': Smf74Proc,
        'cach': Smf74Cach, 'cfrf': Smf74Cfrf, 'subchpa': Smf74Subchpa, 'mscm': Smf74Mscm, 'str': Smf74Str,
        'adup': Smf74Adup, 'dupchpa': Smf74Dupchpa, 'cachsys': Smf74Cachsys, 'cdev': Smf74Cdev, 'raid': Smf74Raid,
        'extp': Smf74Extp, 'xpool': Smf74Xpool, 'rrank': Smf74Rrank, 'hfs': Smf74Hfs, 'gbuf': Smf74Gbuf,
        'fsys': Smf74Fsys, 'fcd': Smf74Fcd, 'switch': Smf74Switch, 'port': Smf74Port, 'connector': Smf74Connector,
        'cntl': Smf74Cntl, 'lss': Smf74Lss, 'rank': Smf74Rank, 'arry': Smf74Arry, 'siol': Smf74Siol, 'pcie': Smf74Pcie,
        'srtd': Smf74Srtd, 'scm': Smf74Scm, 'eadm': Smf74Eadm}

tblnames = {'pro': 'smf74_pro', 'dctl': 'smf74_dctl', 'dev': 'smf74_dev', 'xctl': 'smf74_xctl',
            'sys': 'smf74_sys', 'path': 'smf74_path', 'mbr': 'smf74_mbr', 'omvs': 'smf74_omvs',
            'cf': 'smf74_cf', 'lcf': 'smf74_lcf', 'sreq': 'smf74_sreq', 'proc': 'smf74_proc',
            'cach': 'smf74_cach', 'cfrf': 'smf74_cfrf', 'subchpa': 'smf74_subchpa', 'mscm': 'smf74_mscm',
            'str': 'smf74_str', 'adup': 'smf74_adup', 'dupchpa': 'smf74_dupchpa',
            'cachsys': 'smf74_cachsys', 'cdev': 'smf74_cdev', 'raid': 'smf74_raid', 'extp': 'smf74_extp',
            'xpool': 'smf74_xpool', 'rrank': 'smf74_rrank', 'rank': 'smf74_rank', 'hfs': 'smf74_hfs',
            'gbuf': 'smf74_gbuf', 'fsys': 'smf74_fsys', 'fcd': 'smf74_fcd', 'switch': 'smf74_switch',
            'port': 'smf74_port', 'connector': 'smf74_connector', 'cntl': 'smf74_cntl',
            'lss': 'smf74_lss', 'arry': 'smf74_arry', 'siol': 'smf74_siol', 'pcie': 'smf74_pcie',
            'srtd': 'smf74_srtd', 'scm': 'smf74_scm', 'eadm': 'smf74_eadm'}

agg_str = {'r744styp': agg_next, 'r744scei': agg_next, 'r744sadi': agg_next, 'r744scad': agg_next,
           'r744sdas': agg_next, 'r744spri': agg_next, 'r744ssec': agg_next, 'r744senc': agg_next,
           'r744slec': agg_next, 'r744slel': 'max', 'r744slem': 'last', 'r744sltl': agg_next,
           'r744sltm': agg_next, 'r744ssta': 'sum', 'r744strc': 'sum', 'r744stac': 'sum', 'r744sarc': 'sum',
           'r744satm': 'sum', 'r744sasq': 'sum', 'r744ssrc': 'sum', 'r744sstm': 'sum', 'r744sssq': 'sum',
           'r744sqrc': 'sum', 'r744sqtm': 'sum', 'r744sqsq': 'sum', 'r744sdrc': 'sum', 'r744sdtm': 'sum',
           'r744sdsq': 'sum', 'r744sdmp': 'sum', 'r744shto': 'sum', 'r744shmn': 'min', 'r744shmx': 'max',
           'r744slto': 'sum', 'r744slmn': 'min', 'r744slmx': 'max', 'r744sdto': 'sum', 'r744sdmn': 'min',
           'r744sdmx': 'max', 'r744scn': 'sum', 'r744sfcn': 'sum', 'r744ssiz': agg_next, 'r744smas': 'max',
           'r744smis': 'min', 'r744sdec': 'mean', 'r744sdel': 'mean', 'r744snlh': 'sum', 'r744smae': 'max',
           'r744scue': agg_next, 'r744cdsi': agg_next, 'r744cdne': 'sum', 'r744spln': 'sum', 'r744spes': 'sum',
           'r744sptc': 'sum', 'r744spst': 'sum', 'r744spss': 'sum', 'r744srtc': 'sum', 'r744srst': 'sum',
           'r744srss': 'sum', 'r744sctc': 'sum', 'r744scst': 'sum', 'r744scss': 'sum', 'r744slsv': agg_next,
           'r744setm': 'sum', 'r744sisc': agg_next, 'r744snsc': 'sum', 'r744ssac': 'sum', 'r744sosa': 'sum',
           'r744siad': agg_next, 'r744sadn': 'sum', 'r744sixc': 'sum', 'r744sxsc': 'sum', 'r744sxst': 'sum',
           'r744sxsq': 'sum', 'r744sado': 'sum', 'r744sadr': 'sum', 'r744sqch': agg_next, 'r744sxap': agg_next,
           'r744sxas': agg_next, 'r744sxcm': agg_next, 'r744sxmo': agg_next, 'r744swdr': 'sum', 'r744swac': 'sum',
           'r744srdr': 'sum', 'r744srac': 'sum', 'r744swec': 'sum', 'r744srec': 'sum', 'r744swed': 'sum',
           'r744swes': 'sum', 'r744sred': 'sum', 'r744sres': 'sum', 'r744smrc': 'sum', 'r744smtm': 'sum',
           'r744smsq': 'sum', 'r744smto': 'sum', 'r744smht': 'sum', 'r744smmn': 'min', 'r744smmx': 'max',
           'r744smhn': 'min', 'r744smhx': 'max', 'r744crhc': 'max', 'r744crmd': 'max', 'r744crma': 'max',
           'r744crmn': 'max', 'r744crmt': 'max', 'r744cwh0': 'max', 'r744cwh1': 'max', 'r744cwmn': 'max',
           'r744cwmi': 'max', 'r744cwmt': 'max', 'r744cder': 'max', 'r744cdtr': 'max', 'r744cxdr': 'max',
           'r744cxfw': 'max', 'r744cxni': 'max', 'r744cxci': 'max', 'r744ccoc': 'max', 'r744crsm': 'max',
           'r744ctsf': 'max', 'r744cdec': 'last', 'r744cdac': 'last', 'r744ctcc': 'max', 'r744cdta': 'max',
           'r744crlc': 'max', 'r744cprl': 'max', 'r744cxrl': 'max', 'r744cwuc': 'max', 'r744sflg': agg_next,
           'r744sxfl': agg_next}
agg_mscm = {'r744msma': 'max', 'r744malg': agg_next, 'r744mfau': agg_next, 'r744miua': 'max', 'r744mius': 'max',
            'r744mema': 'max', 'r744meml': 'max', 'r744meme': 'max', 'r744menl': 'max', 'r744mene': 'max',
            'r744mslt': agg_next, 'r744msut': agg_next, 'r744mslr': agg_next, 'r744msur': agg_next,
            'r744mswc': 'sum', 'r744mrfc': 'sum', 'r744mrpc': 'sum', 'r744mrst': 'sum', 'r744mrsq': 'sum',
            'r744mwst': 'sum', 'r744mwsq': 'sum', 'r744mrbt': 'sum', 'r744mwbt': 'sum', 'r744maec': 'sum',
            'r744msrl': 'sum', 'r744msrr': 'sum', 'r744msrm': 'sum', 'r744mmbl': 'max', 'r744mmbe': 'max',
            'r744mnel': 'min', 'r744mnec': 'min', 'r744msrk': 'sum'}
agg_adup = {'r744afo': agg_next, 'r744aheo': 'max', 'r744alaoh': 'max', 'r744alaosh': 'max', 'r744alcoh': 'max',
            'r744alcoph': 'max', 'r744alao': 'sum', 'r744alaos': 'sum', 'r744alco': 'sum', 'r744alcop': 'sum',
            'r744atpoct': 'sum', 'r744atpoc': 'sum', 'r744arcpot': 'sum', 'r744arcpo': 'sum', 'r744acqsc': 'sum',
            'r744apdt': 'sum', 'r744apdq': 'sum', 'r744amdt': 'sum', 'r744amdq': 'sum', 'r744aqdt': 'sum',
            'r744aqdq': 'sum', 'r744aqst': 'sum', 'r744aqsq': 'sum', 'r744acdt': 'sum', 'r744acdq': 'sum',
            'r744ardt': 'sum', 'r744ardq': 'sum', 'r744aott': 'sum', 'r744aotq': 'sum', 'r744astt': 'sum',
            'r744astq': 'sum'}

int_dtypedict = create_int_dtypedict(tbls)


def upload_74db(db_engines: dict, db_session: Session, jsonfiles: str, partitions_scheme: str,
                db_driver: str = 'postgresql+psycopg2') -> UploadResult:
    """Upload smf74 JSON files to the database.

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
        partitions_range = range(1, 2)  # single partition


    result_list = []

    for jsonfile in jsonfiles:
        if not Path(jsonfile).is_file() or Path(jsonfile).suffix != '.json':
            continue
        st = time.time()
        # print(jsonfile)
        current_time = dt.datetime.now()
        insert_dict = {'pro': 0, 'dctl': 0, 'dev': 0, 'xctl': 0, 'sys': 0, 'path': 0, 'mbr': 0, 'omvs': 0,
                       'cf': 0, 'proc': 0, 'str': 0, 'lcf': 0, 'sreq': 0, 'cach': 0, 'subchpa': 0, 'cfrf': 0,
                       'dupchpa': 0, 'mscm': 0, 'adup': 0, 'cntl': 0, 'lss': 0, 'extp': 0, 'rank': 0,
                       'arry': 0, 'siol': 0, 'cachsys': 0, 'rrank': 0, 'cdev': 0, 'raid': 0, 'xpool': 0,
                       'hfs': 0, 'gbuf': 0, 'fsys': 0, 'fcd': 0, 'switch': 0, 'port': 0, 'connector': 0,
                       'pcie': 0, 'srtd': 0, 'scm': 0, 'eadm': 0, }

        with open(jsonfile) as f:
            # program logic start here
            try:
                df = pd.read_json(f)
            except ValueError:
                click.echo(
                    f"\nInvalid JSON file {jsonfile}. This file will be skipped.")
                continue
            try:
                dfs_dict = format_74df(df, current_time)
            except Exception as e:
                click.echo(f"\nUnsupported JSON file {jsonfile} with error: {str(e)}. This file will be skipped.")
                continue

            if dfs_dict['pro'].empty:
                click.echo(
                    f"\nThis JSON file {jsonfile} is not for this smf type. This file will be skipped.")
                # Cannot continue processing
                continue
            else:
                csc = get_csc_in_db(dfs_dict['pro']['smf74xnm'].unique()[0], dfs_dict['pro']['smf74snm'].unique()[0],
                                    pd.to_numeric(dfs_dict['pro']['smf74ptn'].unique()[0], downcast="integer"),
                                    db_session)
                if csc is None:
                    click.echo(
                        f"\nThe file {jsonfile} cannot be processed until the corresponding Smf70 Subtype 1 records have been processed. This file will be skipped.")
                    continue
            # Update csc value in dataframes
            for table in dfs_dict.keys():
                if dfs_dict[table].shape[0] > 0:
                    if 'csc' in tbls[table].__table__.columns.keys():
                        dfs_dict[table] = dfs_dict[table].copy().reset_index()
                        dfs_dict[table]['csc'] = csc
                        dfs_dict[table].set_index(
                            [col.name for col in tbls[table].__table__.primary_key.columns.values()],
                            inplace=True)

            # insert the detail tbls
            for table in insert_dict.keys():
                if dfs_dict[table].shape[0] > 0:
                    insert_dict[table] = df_insert_by_partitions(db_driver, db_engines, db_session,
                                                                 dfs_dict[table].copy().reset_index(), tblnames[table],
                                                                 tbls[table],'smf74', int_dtypedict[table],
                                                                 '74', partitions_scheme, True)

            if insert_dict['str'] > 0:
                str_stmt1 = select(Smf74Sreq).join_from(Smf74Str, Smf74Str.smf74_sreqs).filter(
                    Smf74Str.last_update_time.__eq__(current_time))
                str_stmt2 = select(Smf74Mscm).join_from(Smf74Str, Smf74Str.smf74_mscms).filter(
                    Smf74Str.last_update_time.__eq__(current_time))
                str_stmt3 = select(Smf74Adup).join_from(Smf74Str, Smf74Str.smf74_adups).filter(
                    Smf74Str.last_update_time.__eq__(current_time))

                df_sreqs_list = []
                df_mscms_list = []
                df_adups_list = []
                for part in partitions_range:
                    df_sreq = pd.read_sql(str_stmt1, db_engines[f'74.{part}']).rename(columns={'r744snam': 'r744qstr'})
                    if not df_sreq.empty:
                        df_sreqs_list.append(df_sreq)

                    df_mscm = pd.read_sql(str_stmt2, db_engines[f'74.{part}']).rename(
                        columns={'r744snam': 'r744qstr'})
                    if not df_mscm.empty:
                        df_mscms_list.append(df_mscm)

                    df_adup = pd.read_sql(str_stmt3, db_engines[f'74.{part}']).rename(
                        columns={'r744snam': 'r744qstr'})
                    if not df_adup.empty:
                        df_adups_list.append(df_adup)

                if len(df_sreqs_list) > 0:
                    df_sreqs = pd.concat(df_sreqs_list)
                else:
                    df_sreqs = pd.DataFrame()
                if len(df_mscms_list) > 0:
                    df_mscms = pd.concat(df_mscms_list)
                else:
                    df_mscms = pd.DataFrame()
                if len(df_adups_list) > 0:
                    df_adups = pd.concat(df_adups_list)
                else:
                    df_adups = pd.DataFrame()
                if not df_sreqs.empty:
                    str_df1 = df_sreqs.groupby(
                        [col.name for col in Smf74Str.__table__.primary_key.columns.values()]).agg(agg_str)

                    if not df_mscms.empty:
                        str_df2 = df_mscms.groupby(
                            [col.name for col in Smf74Str.__table__.primary_key.columns.values()]).agg(agg_mscm)
                    else:
                        str_df2 = pd.DataFrame()

                    if not df_adups.empty:
                        str_df3 = df_adups.groupby(
                            [col.name for col in Smf74Str.__table__.primary_key.columns.values()]).agg(agg_adup)
                    else:
                        str_df3 = pd.DataFrame()

                    dfs_dict['str'] = pd.concat([dfs_dict['str'], str_df1, str_df2, str_df3], axis=1)
                    str_result = df_upsert_by_partitions(db_driver, db_engines, db_session,
                                                          dfs_dict['str'].copy().reset_index().drop_duplicates(),
                                                          'smf74_str', Smf74Str, 'smf74',
                                                          [col.name for col in Smf74Str.__table__.primary_key.columns.values()],
                                                          '74', partitions_scheme, int_dtypedict['str']
                                                          )
                    insert_dict['str'] = str_result
            #
            if insert_dict['cf'] > 0:
                agg_cf_str = {'r744ssiz': 'sum'}
                agg_cf_mscm = {'r744mfau': 'sum', 'r744msma': 'sum'}
                agg_cf_proc_sum = {'r744pbsy': 'sum', 'r744pwai': 'sum', 'r744pwgt': 'sum'}
                agg_cf_proc_mean = {'r744pbsy': 'mean', 'r744pwai': 'mean', 'r744pwgt': 'mean'}
                agg_cf_lcf = {'r744fscg': 'max', 'r744fscu': 'max', 'r744fscl': 'max', 'r744fscc': 'sum',
                              'r744ftim': 'sum',
                              'r744fsqu': 'sum', 'r744fctm': 'sum', 'r744fcsq': 'sum', 'r744fpbc': 'sum',
                              'r744ftor': 'sum',
                              'r744fail': 'sum'}
                cf_stmt1 = select(Smf74Str).join_from(Smf74Cf, Smf74Cf.smf74_strs).filter(
                    Smf74Cf.last_update_time.__eq__(current_time))
                cf_stmt2 = select(Smf74Mscm).join_from(Smf74Cf, Smf74Cf.smf74_mscms).filter(
                    Smf74Cf.last_update_time.__eq__(current_time))
                cf_stmt3 = select(Smf74Proc).join_from(Smf74Cf, Smf74Cf.smf74_procs).filter(
                    Smf74Cf.last_update_time.__eq__(current_time))
                cf_stmt4 = select(Smf74Lcf).join_from(Smf74Cf, Smf74Cf.smf74_lcfs).filter(
                    Smf74Cf.last_update_time.__eq__(current_time))

                df_strs_list = []
                df_mscm_list = []
                df_procs_list = []
                df_lcfs_list = []
                for part in partitions_range:
                    df_str = pd.read_sql(cf_stmt1, db_engines[f'74.{part}'])
                    if not df_str.empty:
                        df_strs_list.append(df_str)
                    df_mscm = pd.read_sql(cf_stmt2, db_engines[f'74.{part}'])
                    if not df_mscm.empty:
                        df_mscm_list.append(df_mscm)
                    df_proc = pd.read_sql(cf_stmt3, db_engines[f'74.{part}'])
                    if not df_proc.empty:
                        df_procs_list.append(df_proc)
                    df_lcf = pd.read_sql(cf_stmt4, db_engines[f'74.{part}'])
                    if not df_lcf.empty:
                        df_lcfs_list.append(df_lcf)
                if len(df_strs_list) > 0:
                    df_strs = pd.concat(df_strs_list)
                else:
                    df_strs = pd.DataFrame()
                if len(df_mscm_list) > 0:
                    df_mscms = pd.concat(df_mscm_list)
                else:
                    df_mscms = pd.DataFrame()
                if len(df_procs_list) > 0:
                    df_procs = pd.concat(df_procs_list)
                else:
                    df_procs = pd.DataFrame()
                if len(df_lcfs_list) > 0:
                    df_lcfs = pd.concat(df_lcfs_list)
                else:
                    df_lcfs = pd.DataFrame()

                if not df_strs.empty:
                    cf_df1 = df_strs.groupby(['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'r744fnam']).agg(
                        agg_cf_str).rename(columns={'r744ssiz': 'total_str_alloc'})


                    if not df_mscms.empty:
                        cf_df2 = df_mscms.groupby(['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'r744fnam']).agg(
                            agg_cf_mscm).rename(
                            columns={'r744mfau': 'total_augmented_alloc', 'r744msma': 'total_max_scm'})
                    else:
                        cf_df2 = pd.DataFrame()


                    if not df_procs.empty:
                        cf_df3a = df_procs.groupby(
                            ['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'r744fnam', 'r744pnum']).agg(
                            agg_cf_proc_mean)
                        cf_df3 = cf_df3a.groupby(['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'r744fnam']).agg(
                            agg_cf_proc_sum).rename(
                            columns={'r744pbsy': 'total_processor_busy', 'r744pwai': 'total_processor_wait'})
                    else:
                        cf_df3 = pd.DataFrame()


                    if not df_lcfs.empty:
                        cf_df4 = df_lcfs.groupby(['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'r744fnam']).agg(
                            agg_cf_lcf)
                    else:
                        cf_df4 = pd.DataFrame()
                    dfs_dict['cf'] = pd.concat([dfs_dict['cf'], cf_df1, cf_df2, cf_df3, cf_df4], axis=1)
                    dfs_dict['cf']['avg_processor_weight'] = np.where(dfs_dict['cf']['r744fpsn'] > 0,
                                                                      dfs_dict['cf']['r744pwgt'] / dfs_dict['cf']['r744fpsn'],
                                                                      0)
                    cf_result = df_upsert_by_partitions(db_driver, db_engines, db_session,
                                                        dfs_dict['cf'].reset_index()[Smf74Cf.__table__.columns.keys()].drop_duplicates(),
                                                        'smf74_cf', Smf74Cf, 'smf74',
                                                        [col.name for col in Smf74Cf.__table__.primary_key.columns.values()],
                                                        '74', partitions_scheme, int_dtypedict['cf'],
                                                       )
                    insert_dict['cf'] = cf_result

            if insert_dict['switch'] > 0:
                agg_port = {'r747pfpt': 'sum', 'r747pnwr': 'sum', 'r747pnwt': 'sum', 'r747pnfr': 'sum',
                            'r747pnft': 'sum', 'r747pner': 'sum'}
                switch_stmt1 = select(Smf74Port).join_from(Smf74Switch, Smf74Switch.smf74_ports).filter(
                    Smf74Switch.last_update_time.__eq__(current_time))
                df_port_list = []
                for part in partitions_range:
                    df_port = pd.read_sql(switch_stmt1, db_engines[f'74.{part}'])
                    if not df_port.empty:
                        df_port_list.append(df_port)
                if len(df_port_list) > 0:
                    df_ports = pd.concat(df_port_list)
                else:
                    df_ports = pd.DataFrame()
                if not df_ports.empty:
                    df_ports_gp = df_ports.reset_index().groupby(
                        [col.name for col in Smf74Switch.__table__.primary_key.columns.values()]).agg(agg_port)
                    dfs_dict['switch'] = pd.concat([dfs_dict['switch'], df_ports_gp], axis=1)
                    switch_result = df_upsert_by_partitions(db_driver, db_engines, db_session,
                                                            dfs_dict['switch'].reset_index()[Smf74Switch.__table__.columns.keys()].drop_duplicates(),
                                                            'smf74_switch', Smf74Switch, 'smf74',
                                                            [col.name for col in Smf74Switch.__table__.primary_key.columns.values()],
                                                            '74', partitions_scheme, int_dtypedict['switch']
                                                           )
                    insert_dict['switch'] = switch_result
            if insert_dict['fcd'] > 0:
                agg_port = {'r747pfpt': 'sum', 'r747pnwr': 'sum', 'r747pnwt': 'sum', 'r747pnfr': 'sum',
                            r'r747pnft': 'sum',
                            'r747pner': 'sum'}
                fcd_stmt1 = select(Smf74Switch).join_from(Smf74Fcd, Smf74Fcd.smf74_switchs).filter(
                    Smf74Fcd.last_update_time.__eq__(current_time))
                df_switch_list = []
                for part in partitions_range:
                    df_switch = pd.read_sql(fcd_stmt1, db_engines[f'74.{part}'])
                    if not df_switch.empty:
                        df_switch_list.append(df_switch)
                if len(df_switch_list) > 0:
                    df_switches = pd.concat(df_switch_list)
                else:
                    df_switches = pd.DataFrame()
                if not df_switches.empty:
                    df_switchs_gp = df_switches.reset_index().groupby(
                        [col.name for col in Smf74Fcd.__table__.primary_key.columns.values()]).agg(agg_port)
                    dfs_dict['fcd'] = pd.concat([dfs_dict['fcd'], df_switchs_gp], axis=1)
                    fcd_result = df_upsert_by_partitions(db_driver, db_engines, db_session,
                                                         dfs_dict['fcd'].reset_index()[Smf74Fcd.__table__.columns.keys()].drop_duplicates(),
                                                         'smf74_fcd', Smf74Fcd, 'smf74',
                                                         [col.name for col in Smf74Fcd.__table__.primary_key.columns.values()],
                                                         '74', partitions_scheme, int_dtypedict['fcd']
                                                         )
                    insert_dict['fcd'] = fcd_result
            if insert_dict['rrank'] > 0:
                agg_raid = {'r7451sio': agg_next, 'r7451hpf': agg_next, 'r7451xfl': agg_next, 'r7451scs': agg_next,
                            'r7451rsv': 'sum', 'r7451flg': agg_next, 'r7451aid': agg_next, 'r7451hdd': agg_next,
                            'r7451rty': agg_next, 'r7451hss': agg_next, 'r7451rrq': 'sum', 'r7451wrq': 'sum',
                            'r7451sr': 'sum', 'r7451sw': 'sum', 'r7451rrt': 'sum', 'r7451wrt': 'sum',
                            'r7451unt': agg_next, 'r7451rmr': 'sum', 'r7451xsf': 'sum', 'r7451xcw': 'sum',
                            'r7451tsp': 'sum', 'r7451nvs': 'sum', 'r7451ct1': 'sum', 'r7451ct2': 'sum',
                            'r7451ct3': 'sum', 'r7451ct4': 'sum', 'r7451ct5': 'sum', 'r7451ct6': 'sum',
                            'r7451zhl': 'sum', 'r7451zhh': 'sum', 'r7451gsf': 'sum', 'r7451gss': 'sum',
                            'r7451srr': 'sum', 'r7451srh': 'sum', 'r7451swr': 'sum', 'r7451swh': 'sum'}
                rrank_stmt1 = select(Smf74Raid).join_from(Smf74Rrank, Smf74Rrank.smf74_raids).filter(
                    Smf74Rrank.last_update_time.__eq__(current_time))
                dfs_dict['rrank'] = dfs_dict['rrank'].reset_index()[
                    ['datetime', 'smf74ist', 'smf74iet', 'r745ssid', 'r7451rid', 'last_update_time']].set_index(
                    [col.name for col in Smf74Rrank.__table__.primary_key.columns.values()])
                df_raid_list = []
                for part in partitions_range:
                    df_raid = pd.read_sql(rrank_stmt1, db_engines[f'74.{part}'])
                    if not df_raid.empty:
                        df_raid_list.append(df_raid)
                if len(df_raid_list) > 0:
                    df_raids = pd.concat(df_raid_list)
                else:
                    df_raids = pd.DataFrame()
                if not df_raids.empty:
                    df_raid_gp = df_raids.groupby(
                        [col.name for col in Smf74Rrank.__table__.primary_key.columns.values()]).agg(agg_raid)
                    dfs_dict['rrank'] = pd.concat([dfs_dict['rrank'], df_raid_gp], axis=1)
                    rrank_result = df_upsert_by_partitions(db_driver, db_engines, db_session,
                                                         dfs_dict['rrank'].reset_index()[Smf74Rrank.__table__.columns.keys()],
                                                         'smf74_rrank', Smf74Rrank, 'smf74',
                                                         [col.name for col in Smf74Rrank.__table__.primary_key.columns.values()],
                                                         '74', partitions_scheme, int_dtypedict['rrank'],
                                                        )
                    insert_dict['rrank'] = rrank_result

        result_list.append({tblnames[k]:v for k,v in insert_dict.items() if k in tblnames.keys()})

        et = time.time()  # get the end time
        # get the execution time
        elapsed_time = (et - st) / 60
        print(f'Execution time ({jsonfile}):', elapsed_time, 'minutes')
    # result_list.append(total_insert_dict)
    overall_et = time.time()
    overall_elapsed_time = (overall_et - overall_st) / 60
    return UploadResult(result_list, overall_elapsed_time, SUCCESS)

