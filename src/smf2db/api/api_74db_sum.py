import datetime as dt
import time

import numpy as np
import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from smf2db import SUCCESS
from smf2db.api.api_74 import (agg_r748adc, agg_r748aebc, agg_r748atyp)
from smf2db.api.util import (agg_next, agg_boost,
                             agg_hex_sum, UploadResult, create_int_dtypedict, df_upsert, sum_up_by_partition, is_bit_set)
from smf2db.db_models.smf74_da_model import (Smf74ProDa, Smf74DctlDa, Smf74DevDa, Smf74XctlDa, Smf74SysDa,
                                             Smf74PathDa, Smf74MbrDa, Smf74OmvsDa, Smf74CachsysDa, Smf74CdevDa,
                                             Smf74RaidDa, Smf74XpoolDa, Smf74RrankDa, Smf74HfsDa, Smf74GbufDa,
                                             Smf74FsysDa, Smf74FcdDa, Smf74SwitchDa, Smf74PortDa, Smf74ConnectorDa,
                                             Smf74CntlDa, Smf74LssDa, Smf74ExtpDa, Smf74RankDa, Smf74ArryDa,
                                             Smf74SiolDa, Smf74PcieDa, Smf74ScmDa, Smf74EadmDa, Smf74CfDa, Smf74LcfDa,
                                             Smf74SreqDa, Smf74ProcDa, Smf74CachDa, Smf74CfrfDa, Smf74SubchpaDa,
                                             Smf74MscmDa, Smf74StrDa, Smf74SrtdDa, Smf74AdupDa, Smf74DupchpaDa)
from smf2db.db_models.smf74_hr_model import (Smf74ProHr, Smf74DctlHr, Smf74DevHr, Smf74XctlHr, Smf74SysHr,
                                             Smf74PathHr, Smf74MbrHr, Smf74OmvsHr, Smf74CachsysHr, Smf74CdevHr,
                                             Smf74RaidHr, Smf74XpoolHr, Smf74RrankHr, Smf74HfsHr, Smf74GbufHr,
                                             Smf74FsysHr, Smf74FcdHr, Smf74SwitchHr, Smf74PortHr, Smf74ConnectorHr,
                                             Smf74CntlHr, Smf74LssHr, Smf74ExtpHr, Smf74RankHr, Smf74ArryHr,
                                             Smf74SiolHr, Smf74PcieHr, Smf74ScmHr, Smf74EadmHr, Smf74CfHr, Smf74LcfHr,
                                             Smf74SreqHr, Smf74ProcHr, Smf74CachHr, Smf74CfrfHr, Smf74SubchpaHr,
                                             Smf74MscmHr, Smf74StrHr, Smf74SrtdHr, Smf74AdupHr, Smf74DupchpaHr)
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
tbls_hr = {'pro': Smf74ProHr, 'dctl': Smf74DctlHr, 'dev': Smf74DevHr, 'xctl': Smf74XctlHr, 'sys': Smf74SysHr,
           'path': Smf74PathHr, 'mbr': Smf74MbrHr, 'omvs': Smf74OmvsHr, 'cf': Smf74CfHr, 'lcf': Smf74LcfHr,
           'sreq': Smf74SreqHr, 'proc': Smf74ProcHr, 'cach': Smf74CachHr, 'cfrf': Smf74CfrfHr,
           'subchpa': Smf74SubchpaHr, 'mscm': Smf74MscmHr, 'str': Smf74StrHr, 'adup': Smf74AdupHr,
           'dupchpa': Smf74DupchpaHr, 'cachsys': Smf74CachsysHr, 'cdev': Smf74CdevHr, 'raid': Smf74RaidHr,
           'extp': Smf74ExtpHr, 'xpool': Smf74XpoolHr, 'rrank': Smf74RrankHr, 'hfs': Smf74HfsHr, 'gbuf': Smf74GbufHr,
           'fsys': Smf74FsysHr, 'fcd': Smf74FcdHr, 'switch': Smf74SwitchHr, 'port': Smf74PortHr,
           'connector': Smf74ConnectorHr, 'cntl': Smf74CntlHr, 'lss': Smf74LssHr, 'rank': Smf74RankHr,
           'arry': Smf74ArryHr, 'siol': Smf74SiolHr, 'pcie': Smf74PcieHr, 'srtd': Smf74SrtdHr, 'scm': Smf74ScmHr,
           'eadm': Smf74EadmHr}
tbls_da = {'pro': Smf74ProDa, 'dctl': Smf74DctlDa, 'dev': Smf74DevDa, 'xctl': Smf74XctlDa, 'sys': Smf74SysDa,
           'path': Smf74PathDa, 'mbr': Smf74MbrDa, 'omvs': Smf74OmvsDa, 'cf': Smf74CfDa, 'lcf': Smf74LcfDa,
           'sreq': Smf74SreqDa, 'proc': Smf74ProcDa, 'cach': Smf74CachDa, 'cfrf': Smf74CfrfDa,
           'subchpa': Smf74SubchpaDa, 'mscm': Smf74MscmDa, 'str': Smf74StrDa, 'adup': Smf74AdupDa,
           'dupchpa': Smf74DupchpaDa, 'cachsys': Smf74CachsysDa, 'cdev': Smf74CdevDa, 'raid': Smf74RaidDa,
           'extp': Smf74ExtpDa, 'xpool': Smf74XpoolDa, 'rrank': Smf74RrankDa, 'rank': Smf74RankDa, 'hfs': Smf74HfsDa,
           'gbuf': Smf74GbufDa, 'fsys': Smf74FsysDa, 'fcd': Smf74FcdDa, 'switch': Smf74SwitchDa, 'port': Smf74PortDa,
           'connector': Smf74ConnectorDa, 'cntl': Smf74CntlDa, 'lss': Smf74LssDa, 'arry': Smf74ArryDa,
           'siol': Smf74SiolDa, 'pcie': Smf74PcieDa, 'srtd': Smf74SrtdDa, 'scm': Smf74ScmDa, 'eadm': Smf74EadmDa}
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
tblnames_hr = {'pro': 'smf74_pro_hr', 'dctl': 'smf74_dctl_hr', 'dev': 'smf74_dev_hr', 'xctl': 'smf74_xctl_hr',
               'sys': 'smf74_sys_hr', 'path': 'smf74_path_hr', 'mbr': 'smf74_mbr_hr', 'omvs': 'smf74_omvs_hr',
               'cf': 'smf74_cf_hr', 'lcf': 'smf74_lcf_hr', 'sreq': 'smf74_sreq_hr', 'proc': 'smf74_proc_hr',
               'cach': 'smf74_cach_hr', 'cfrf': 'smf74_cfrf_hr', 'subchpa': 'smf74_subchpa_hr', 'mscm': 'smf74_mscm_hr',
               'str': 'smf74_str_hr', 'adup': 'smf74_adup_hr', 'dupchpa': 'smf74_dupchpa_hr',
               'cachsys': 'smf74_cachsys_hr', 'cdev': 'smf74_cdev_hr', 'raid': 'smf74_raid_hr', 'extp': 'smf74_extp_hr',
               'xpool': 'smf74_xpool_hr', 'rrank': 'smf74_rrank_hr', 'rank': 'smf74_rank_hr', 'hfs': 'smf74_hfs_hr',
               'gbuf': 'smf74_gbuf_hr', 'fsys': 'smf74_fsys_hr', 'fcd': 'smf74_fcd_hr', 'switch': 'smf74_switch_hr',
               'port': 'smf74_port_hr', 'connector': 'smf74_connector_hr', 'cntl': 'smf74_cntl_hr',
               'lss': 'smf74_lss_hr', 'arry': 'smf74_arry_hr', 'siol': 'smf74_siol_hr', 'pcie': 'smf74_pcie_hr',
               'srtd': 'smf74_srtd_hr', 'scm': 'smf74_scm_hr', 'eadm': 'smf74_eadm_hr'}
tblnames_da = {'pro': 'smf74_pro_da', 'dctl': 'smf74_dctl_da', 'dev': 'smf74_dev_da', 'xctl': 'smf74_xctl_da',
               'sys': 'smf74_sys_da', 'path': 'smf74_path_da', 'mbr': 'smf74_mbr_da', 'omvs': 'smf74_omvs_da',
               'cf': 'smf74_cf_da', 'lcf': 'smf74_lcf_da', 'sreq': 'smf74_sreq_da', 'proc': 'smf74_proc_da',
               'cach': 'smf74_cach_da', 'cfrf': 'smf74_cfrf_da', 'subchpa': 'smf74_subchpa_da', 'mscm': 'smf74_mscm_da',
               'str': 'smf74_str_da', 'adup': 'smf74_adup_da', 'dupchpa': 'smf74_dupchpa_da',
               'cachsys': 'smf74_cachsys_da', 'cdev': 'smf74_cdev_da', 'raid': 'smf74_raid_da', 'extp': 'smf74_extp_da',
               'xpool': 'smf74_xpool_da', 'rrank': 'smf74_rrank_da', 'rank': 'smf74_rank_da', 'hfs': 'smf74_hfs_da',
               'gbuf': 'smf74_gbuf_da', 'fsys': 'smf74_fsys_da', 'fcd': 'smf74_fcd_da', 'switch': 'smf74_switch_da',
               'port': 'smf74_port_da', 'connector': 'smf74_connector_da', 'cntl': 'smf74_cntl_da',
               'lss': 'smf74_lss_da', 'arry': 'smf74_arry_da', 'siol': 'smf74_siol_da', 'pcie': 'smf74_pcie_da',
               'srtd': 'smf74_srtd_da', 'scm': 'smf74_scm_da', 'eadm': 'smf74_eadm_da'}

int_dtypedict = create_int_dtypedict(tbls)

agg_dict = {
    'pro': {'smf74flg': 'first',
            'smf74gie': 'last', 'smf74mfv': 'last', 'smf74int': 'sum', 'smf74sam': 'sum', 'smf74cyc': 'last',
            'smf74mvs': 'last', 'smf74iml': 'last', 'smf74ptn': 'last', 'smf74srl': 'last', 'smf74lgo': 'last',
            'smf74oil': 'last', 'smf74syn': 'last', 'smf74xnm': 'last', 'smf74snm': 'last',
            'speed_boost': agg_boost, 'ziip_boost': agg_boost,
            'smf74prd': 'last', 'smf74fla': 'last', 'smf74prf': 'last'},
    'dev': {'lcd': 'max', 'cmb': 'max', 'del_': 'max', 'par': 'max', 'vac': 'max', 'sta': 'last',
            'smf74ser': 'first', 'smf74typ': 'first', 'smf74nux': 'sum', 'smf74ssc': 'sum', 'smf74mec': 'sum',
            'smf74cnn': 'sum', 'smf74pen': 'sum', 'smf74atv': 'sum', 'smf74dis': 'sum', 'smf74que': 'sum',
            'smf74utl': 'sum', 'smf74rsv': 'sum', 'smf74alc': 'sum', 'smf74mtp': 'sum', 'smf74nrd': 'sum',
            'smf74cof': 'sum', 'smf74ict': 'sum', 'smf74dvb': 'sum', 'rnr': 'first', 'rsg': 'first', 'rcs': 'max',
            'mts': 'max', 'mte': 'max', 'ctw': 'max', 'smf74sgn': 'first', 'smf74nda': 'sum', 'smf74dev': 'first',
            'smf74cu': 'first', 'dyc': 'max', 'ddt': 'max', 'pav': 'max', 'nxc': 'max', 'ntf': 'last', 'cni': 'max',
            'hpv': 'last', 'cfc': 'last', 'hwr': 'max', 'xpv': 'last', 'sir': 'last', 'siw': 'last',
            'smf74mtc': 'sum', 'srd': 'max', 'snd': 'max', 'shv': 'max', 'shr': 'last', 'smf74dct': 'first',
            'smf74dct_hex2': 'last', 'smf74hpc': 'last', 'smf74nss': 'sum', 'smf74psm': 'sum', 'smf74pct': 'sum',
            'smf74cmr': 'sum', 'smf74cap': 'last', 'smf74idt': 'sum', 'smf74cuq': 'sum', 'smf74nm2': 'first',
            'smf74atd': 'sum', 'smf74agc': 'last', 'smf74ags': 'last', 'smf74sbr': 'sum', 'smf74sbw': 'sum',
            'smf74sqr': 'sum', 'smf74sqw': 'sum', 'smf74spr': 'sum', 'smf74spw': 'sum', 'smf74sftr': 'sum',
            'smf74sftw': 'sum', 'smf74slbr': 'sum', 'smf74slbw': 'sum', 'smf74scmr': 'sum', 'smf74snis': 'sum',
            'smf74stor': 'sum', 'smf74stow': 'sum', 'smf74sor': 'sum', 'smf74sow': 'sum', 'smf74ios': 'sum',
            'sync_device_read_activity_rate': 'mean', 'sync_device_write_activity_rate': 'mean',
            'sync_read_xfer_rate': 'mean', 'sync_write_xfer_rate': 'mean', 'sync_req_success': 'mean',
            'sync_link_busy': 'mean', 'sync_cache_miss': 'mean', 'sync_timeout': 'mean', 'sync_rej_read': 'mean',
            'sync_rej_write': 'mean', 'sync_total_req': 'sum', 'device_activity_rate': 'mean',
            'dev_conn_percent': 'mean', 'dev_util_percent': 'mean', 'dev_resv_percent': 'mean',
            'any_alloc_percent': 'mean', 'mt_pend_percent': 'mean', 'not_ready_percent': 'mean', 'num_of_mts': 'sum',
            'time_dev_alloc': 'sum', 'smf74sam': 'sum', 'smf74int': 'sum',
            'smf74cnf': 'last', 'smf74clf': 'last', 'smf74cnx': 'last', 'smf74cn2': 'last', 'smf74dts': 'last'},
    'dctl': {'smf74tot': 'last', 'smf74gen': 'last', 'nrf': 'last', 'sgf': 'last', '_429': 'max', 'sme': 'max',
             'ecm': 'last', 'sts': 'last', 'fcm': 'max', 'fid': 'max', 'smf74s15': 'last', 'smf74src': 'last',
             'smf74srs': 'last', 'smf74tsr': 'sum', 'config_changed': 'max', 'config_changed_since_ipl': 'max',
             'ipl_iodf': 'max', 'io_token_valid': 'max', 'smf74tnm': 'last', 'smf74tsf': 'last',
             'smf74dcf': 'last', 'smf74dms': 'last', 'smf74enf': 'last', 'smf74smf': 'last', 'smf74cfl': 'last',
             'smf74tdy': 'last', 'smf74tdt': 'last', 'smf74mct': 'max', 'smf_type': 'first', 'smf74sam': 'sum',
             'smf74int': 'sum'},
    'xctl': {'smf_type': 'first'},
    'sys': {'r742sact': 'first', 'r742siac': 'first', 'r742sres': 'first', 'r742spar': 'first', 'r742spth': 'first',
            'r742sbsy': 'sum', 'r742snop': 'sum', 'r742smxb': 'max', 'r742sbig': 'sum', 'r742sfit': 'sum',
            'r742ssml': 'sum', 'r742sovr': 'sum', 'r742stcl': 'first', 'r742sstf': 'first'},
    'path': {'r742pdev': 'first', 'r742pact': 'first', 'r742piac': 'first', 'r742pres': 'first', 'r742podv': 'first',
             'r742pst': 'first', 'r742prs': 'first', 'r742pwk': 'first', 'r742psp': 'first', 'r742plk': 'first',
             'r742pnp': 'first', 'r742psf': 'first', 'r742prb': 'first', 'r742pqg': 'first', 'r742pqd': 'first',
             'r742pret': 'first', 'r742prst': 'sum', 'r742pmxm': 'max', 'r742psig': 'sum', 'r742pqln': 'sum',
             'r742pibr': 'sum', 'r742psus': 'sum', 'r742papp': 'sum', 'r742piot': 'mean', 'r742prct': 'sum',
             'r742ppnd': 'first', 'r742puse': 'first', 'r742plin': 'first', 'r742pusg_timesum_1': 'sum',
             'r742pusg_timessq_1': 'sum', 'r742pusg_timenum_1': 'sum', 'r742pusg_sigcnt_1': 'sum',
             'r742pusg_percent_1': 'mean', 'r742pusg_timesum_2': 'sum', 'r742pusg_timessq_2': 'sum',
             'r742pusg_timenum_2': 'sum', 'r742pusg_sigcnt_2': 'sum', 'r742pusg_percent_2': 'mean',
             'r742pusg_timesum_3': 'sum', 'r742pusg_timessq_3': 'sum', 'r742pusg_timenum_3': 'sum',
             'r742pusg_sigcnt_3': 'sum', 'r742pusg_percent_3': 'mean', 'r742pusg_timesum_4': 'sum',
             'r742pusg_timessq_4': 'sum', 'r742pusg_timenum_4': 'sum', 'r742pusg_sigcnt_4': 'sum',
             'r742pusg_percent_4': 'mean', 'r742pnib_timesum': 'sum', 'r742pnib_timessq': 'sum',
             'r742pnib_timenum': 'sum', 'r742pstf': 'last', 'r742psta': 'last', 'r742pstm': 'last'},
    'mbr': {'r742mact': 'first', 'r742miac': 'first', 'r742mres': 'first', 'r742mpar': 'first', 'r742mnoq': 'first',
            'r742mst1': 'first', 'r742mssm': 'first', 'r742mtrm': 'first', 'r742mmsm': 'first', 'r742mmsd': 'first',
            'r742mrem': 'first', 'r742msnt': 'sum', 'r742mrcv': 'sum', 'r742mint': 'first', 'r742mjob': 'first',
            'r742mstf': 'first', 'r742mst2': 'first'},
    'omvs': {'r743cycu': 'sum', 'r743cyct': 'first', 'r743ter': 'first', 'r743chpr': 'first', 'r743chus': 'first',
             'r743chpu': 'first', 'r743chms': 'first', 'r743chse': 'first', 'r743chsh': 'first', 'r743chsp': 'first',
             'r743chma': 'first', 'r743chpa': 'first', 'r743chlr': 'first', 'r743cqsg': 'first', 'r743sysc': 'sum',
             'r743scmn': 'min', 'r743scmx': 'max', 'r743cpu': 'sum', 'r743ctmn': 'min', 'r743ctmx': 'max',
             'r743opr': 'sum', 'r743opmn': 'min', 'r743opmx': 'max', 'r743ous': 'sum', 'r743oumn': 'min',
             'r743oumx': 'max', 'r743opru': 'sum', 'r743ormn': 'min', 'r743ormx': 'max', 'r743maxp': 'max',
             'r743maxu': 'max', 'r743mxpu': 'max', 'r743curp': 'sum', 'r743cpmn': 'min', 'r743cpmx': 'max',
             'r743curu': 'sum', 'r743cumn': 'min', 'r743cumx': 'max', 'r743mmsg': 'max', 'r743msem': 'max',
             'r743mshm': 'max', 'r743mspg': 'max', 'r743cmsg': 'sum', 'r743cmmn': 'min', 'r743cmmx': 'max',
             'r743csem': 'sum', 'r743csmn': 'min', 'r743csmx': 'max', 'r743cshm': 'sum', 'r743chmn': 'min',
             'r743chmx': 'max', 'r743cspg': 'sum', 'r743cgmn': 'min', 'r743cgmx': 'max', 'r743omsg': 'sum',
             'r743ommn': 'min', 'r743ommx': 'max', 'r743osem': 'sum', 'r743osmn': 'min', 'r743osmx': 'max',
             'r743oshm': 'sum', 'r743ohmn': 'min', 'r743ohmx': 'max', 'r743ospg': 'sum', 'r743ogmn': 'min',
             'r743ogmx': 'max', 'r743mmap': 'max', 'r743cmap': 'sum', 'r743camn': 'min', 'r743camx': 'max',
             'r743omap': 'sum', 'r743oamn': 'min', 'r743oamx': 'max', 'r743mpag': 'max', 'r743cpag': 'sum',
             'r743cxmn': 'min', 'r743cxmx': 'max', 'r743opag': 'sum', 'r743oxmn': 'min', 'r743oxmx': 'max',
             'r743mslr': 'max', 'r743cslr': 'sum', 'r743clmn': 'min', 'r743clmx': 'max', 'r743oslr': 'sum',
             'r743olmn': 'min', 'r743olmx': 'max', 'r743mqds': 'max', 'r743oqds': 'sum', 'r743oqmn': 'min',
             'r743oqmx': 'max', 'smf_type': 'first', 'r743flg': 'first'},
    'proc': {'csc': 'first', 'r744fsys': 'first', 'r744pbsy': 'sum', 'r744pwai': 'sum', 'r744ptde': agg_next,
             'r744pwgt': agg_next, 'r744pbsg': agg_next, 'r744pcct': 'sum', 'r744ptle': agg_next,
             'r744ptyp': 'last'},
    'cach': {'r744crhc': 'sum', 'r744crmd': 'sum', 'r744crma': 'sum', 'r744crmn': 'sum', 'r744crmt': 'sum',
             'r744cwh0': 'sum', 'r744cwh1': 'sum', 'r744cwmn': 'sum', 'r744cwmi': 'sum', 'r744cwmt': 'sum',
             'r744cder': 'sum', 'r744cdtr': 'sum', 'r744cxdr': 'sum', 'r744cxfw': 'sum', 'r744cxni': 'sum',
             'r744cxci': 'sum', 'r744ccoc': 'sum', 'r744crsm': 'sum', 'r744ctsf': 'sum', 'r744cdec': 'last',
             'r744cdac': 'last', 'r744ctcc': 'sum', 'r744cdta': 'sum', 'r744crlc': 'sum', 'r744cprl': 'sum',
             'r744cxrl': 'sum', 'r744cwuc': 'sum', 'csc': 'first'},
    'sreq': {'csc': 'first', 'r744sver': 'first',
             'r744styp': agg_next, 'r744scei': 'last', 'r744sadi': 'last', 'r744scad': 'last', 'r744sdas': 'last',
             'r744spri': 'last', 'r744ssec': 'last', 'r744senc': 'last', 'r744slec': 'last', 'r744slel': 'max',
             'r744slem': 'last', 'r744sltl': 'last', 'r744sltm': 'last', 'r744ssta': 'sum', 'r744strc': 'sum',
             'r744stac': 'sum', 'r744sarc': 'sum', 'r744satm': 'sum', 'r744sasq': 'sum', 'r744ssrc': 'sum',
             'r744sstm': 'sum', 'r744sssq': 'sum', 'r744sqrc': 'sum', 'r744sqtm': 'sum', 'r744sqsq': 'sum',
             'r744sdrc': 'sum', 'r744sdtm': 'sum', 'r744sdsq': 'sum', 'r744sdmp': 'sum', 'r744shto': 'sum',
             'r744shmn': 'min', 'r744shmx': 'max', 'r744slto': 'sum', 'r744slmn': 'min', 'r744slmx': 'max',
             'r744sdto': 'sum', 'r744sdmn': 'min', 'r744sdmx': 'max', 'r744scn': 'sum', 'r744sfcn': 'sum',
             'r744ssiz': 'last', 'r744smas': 'max', 'r744smis': 'min', 'r744sdec': 'mean', 'r744sdel': 'mean',
             'r744snlh': 'sum', 'r744smae': 'max', 'r744scue': 'last', 'r744cdsi': 'last', 'r744cdne': 'last',
             'r744spln': 'sum', 'r744spes': 'sum', 'r744sptc': 'sum', 'r744spst': 'sum', 'r744spss': 'sum',
             'r744srtc': 'sum', 'r744srst': 'sum', 'r744srss': 'sum', 'r744sctc': 'sum', 'r744scst': 'sum',
             'r744scss': 'sum', 'r744slsv': 'last', 'r744setm': 'sum', 'r744sisc': 'last', 'r744snsc': 'last',
             'r744ssac': 'sum', 'r744sosa': 'sum', 'r744siad': 'last', 'r744sadn': 'last', 'r744sixc': 'sum',
             'r744sxsc': 'sum', 'r744sxst': 'sum', 'r744sxsq': 'sum', 'r744sado': 'sum', 'r744sadr': 'sum',
             'r744sqch': 'last', 'r744sxap': 'last', 'r744sxas': 'last', 'r744sxcm': 'last', 'r744sxmo': 'last',
             'r744swdr': 'sum', 'r744swac': 'sum', 'r744srdr': 'sum', 'r744srac': 'sum', 'r744swec': 'sum',
             'r744srec': 'sum', 'r744swed': 'sum', 'r744swes': 'sum', 'r744sred': 'sum', 'r744sres': 'sum',
             'r744smrc': 'sum', 'r744smtm': 'sum', 'r744smsq': 'sum', 'r744smto': 'sum', 'r744smht': 'sum',
             'r744smmn': 'min', 'r744smmx': 'max', 'r744smhn': 'min', 'r744smhx': 'max', 'r744crhc': 'sum',
             'r744crmd': 'sum', 'r744crma': 'sum', 'r744crmn': 'sum', 'r744crmt': 'sum', 'r744cwh0': 'sum',
             'r744cwh1': 'sum', 'r744cwmn': 'sum', 'r744cwmi': 'sum', 'r744cwmt': 'sum', 'r744cder': 'sum',
             'r744cdtr': 'sum', 'r744cxdr': 'sum', 'r744cxfw': 'sum', 'r744cxni': 'sum', 'r744cxci': 'sum',
             'r744ccoc': 'sum', 'r744crsm': 'sum', 'r744ctsf': 'sum', 'r744cdec': 'last', 'r744cdac': 'last',
             'r744ctcc': 'sum', 'r744cdta': 'sum', 'r744crlc': 'sum', 'r744cprl': 'sum', 'r744cxrl': 'sum',
             'r744cwuc': 'sum', 'r744sflg': 'last', 'r744sxfl': 'last'},
    'lcf': {'smf74sam': 'sum', 'r744fsys': 'last', 'r744fscg': 'max', 'r744fscu': 'max', 'r744fscl': 'max',
            'r744fscc': 'sum', 'r744ftim': 'sum', 'r744fsqu': 'sum', 'r744fctm': 'sum', 'r744fcsq': 'sum',
            'r744fpbc': 'sum', 'r744ftor': 'sum', 'r744fail': 'sum', 'r744ftap_1': 'last', 'r744ftap_2': 'last',
            'r744ftap_3': 'last', 'r744ftap_4': 'last', 'r744ftap_5': 'last', 'r744ftap_6': 'last',
            'r744ftap_7': 'last', 'r744ftap_8': 'last', 'r744fpas': 'last', 'r744fpis': 'last', 'r744fpcm': 'last',
            'r744fidp_1': 'last', 'r744fidp_2': 'last', 'r744fidp_3': 'last', 'r744fidp_4': 'last',
            'r744fidp_5': 'last', 'r744fidp_6': 'last', 'r744fidp_7': 'last', 'r744fidp_8': 'last',
            'r744ssta': 'sum', 'r744strc': 'sum', 'r744stac': 'sum', 'r744sarc': 'sum', 'r744satm': 'sum',
            'r744sasq': 'sum', 'r744ssrc': 'sum', 'r744sstm': 'sum', 'r744sssq': 'sum', 'r744sqrc': 'sum',
            'r744sqtm': 'sum', 'r744sqsq': 'sum', 'total_list_r744ssrc': 'sum', 'total_list_r744sarc': 'sum',
            'total_lock_r744ssrc': 'sum', 'total_lock_r744sarc': 'sum', 'total_cache_r744ssrc': 'sum',
            'total_cache_r744sarc': 'sum', 'total_list_delayed_reqs': 'sum', 'total_list_delay_time': 'sum',
            'total_list_delay_sq_time': 'sum', 'total_lock_delayed_reqs': 'sum', 'total_lock_delay_time': 'sum',
            'total_lock_delay_sq_time': 'sum', 'total_cache_delayed_reqs': 'sum', 'total_cache_delay_time': 'sum',
            'total_cache_delay_sq_time': 'sum', 'csc': 'first', 'smf_type': 'first',
            'r744fcpi': 'last', 'r744fcpn': 'last'},
    'cfrf': {'csc': 'first', 'r744rsys': 'first', 'ndepartition': 'first', 'r744rpgs': 'first',
             'ndeconfigcode': 'last', 'ndetype': 'last', 'ndemodel': 'last', 'ndemfg': 'last', 'ndeplant': 'last',
             'ndesequence': 'last', 'ndecpcid': 'last', 'r744rres': 'sum', 'r744rrcs': 'sum', 'r744rhes': 'sum',
             'r744rrss': 'sum', 'r744rrsa': 'sum', 'r744rsss': 'sum', 'r744rdsc': 'sum', 'r744rsdt': 'sum',
             'r744rssd': 'sum', 'r744rsrs': 'sum', 'r744rtap_1': 'last', 'r744rtap_2': 'last', 'r744rtap_3': 'last',
             'r744rtap_4': 'last', 'r744rtap_5': 'last', 'r744rtap_6': 'last', 'r744rtap_7': 'last',
             'r744rtap_8': 'last', 'r744rsse': 'sum', 'r744ridp_1': 'last', 'r744ridp_2': 'last',
             'r744ridp_3': 'last', 'r744ridp_4': 'last', 'r744ridp_5': 'last', 'r744ridp_6': 'last',
             'r744ridp_7': 'last', 'r744ridp_8': 'last', 'r744rsgs': 'last', 'r744rsap_1': 'last',
             'r744rsap_2': 'last', 'r744rsap_3': 'last', 'r744rsap_4': 'last', 'r744rsap_5': 'last',
             'r744rsap_6': 'last', 'r744rsap_7': 'last', 'r744rsap_8': 'last', 'r744rsid_1': 'last',
             'r744rsid_2': 'last', 'r744rsid_3': 'last', 'r744rsid_4': 'last', 'r744rsid_5': 'last',
             'r744rsid_6': 'last', 'r744rsid_7': 'last', 'r744rsid_8': 'last', 'r744rsc': 'last', 'r744ramc': 'sum',
             'r744ramst': 'sum', 'r744ramsq': 'sum', 'r744rampb': 'sum', 'r744ramns': 'sum',
             'r744rsst': 'last', 'r744rcpi': 'last', 'r744rcpn': 'last'},
    'cf': {'smf74mfv': 'last', 'smf74int': 'sum', 'smf74sam': 'sum', 'smf74cyc': 'last', 'smf74mvs': 'last',
          'r744fcei': 'last', 'r744fadi': 'last', 'r744fpec': 'last', 'r744fdyd': 'last', 'r744fthn': 'last',
           'r744fnohw': 'last', 'r744fcho': 'last', 'r744famv': 'last', 'r744fpam': 'last', 'r744fmod': 'last',
           'r744fver': 'last', 'r744fmpc': 'last', 'r744flpn': 'last', 'r744flvl': 'last', 'r744fseq': 'last',
           'r744fpsn': 'last', 'r744fpdn': 'last', 'r744gcsd': 'last', 'r744gcsf': 'last', 'r744gtsd': 'last',
           'r744gtsf': 'last', 'r744gdsa': 'last', 'r744gdsf': 'last', 'r744gdsr': 'max', 'r744gtsc': 'last',
           'r744gfsc': 'last', 'r744gisc': 'last', 'total_str_alloc': 'mean', 'total_augmented_alloc': 'sum',
           'total_max_scm': 'sum', 'total_processor_busy': 'mean', 'total_processor_wait': 'mean', 'r744pwgt': 'mean',
           'r744fscg': 'max', 'r744fscu': 'max', 'r744fscl': 'max', 'r744fscc': 'sum', 'r744ftim': 'sum',
           'r744fsqu': 'sum', 'r744fctm': 'sum', 'r744fcsq': 'sum', 'r744fpbc': 'sum', 'r744ftor': 'sum',
           'r744fail': 'sum', 'r744fflg': 'last', 'r744fflc': 'last'},
    'subchpa': {'r744htap': 'last', 'r744hhca': 'max', 'r744hmov': 'max', 'r744hlav': 'max', 'r744hdev': 'max',
                'r744hsav1': 'max', 'r744hsav2': 'max', 'r744hsav3': 'max', 'r744hsav4': 'max', 'r744hpcv': 'max',
                'r744hopm': 'last', 'r744hdeg': 'last', 'r744hlat': 'mean', 'r744hpcp': 'last', 'r744haid': 'last',
                'r744hapn': 'last', 'r744hsap_1': 'last', 'r744hsap_2': 'last', 'r744hsap_3': 'last',
                'r744hsap_4': 'last', 'csc': 'first'},
    'dupchpa': {'r744htap': 'last', 'r744hhca': 'max', 'r744hmov': 'max', 'r744hlav': 'max', 'r744hdev': 'max',
                'r744hsav1': 'max', 'r744hsav2': 'max', 'r744hsav3': 'max', 'r744hsav4': 'max', 'r744hpcv': 'max',
                'r744hopm': 'last', 'r744hdeg': 'last', 'r744hlat': 'mean', 'r744hpcp': 'last', 'r744haid': 'last',
                'r744hapn': 'last', 'r744hsap_1': 'last', 'r744hsap_2': 'last', 'r744hsap_3': 'last',
                'r744hsap_4': 'last', 'csc': 'first'},
    'mscm': {'r744msma': 'max', 'r744malg': 'last', 'r744mfau': 'last', 'r744miua': 'max', 'r744mius': 'max',
             'r744mema': 'max', 'r744meml': 'max', 'r744meme': 'max', 'r744menl': 'max', 'r744mene': 'max',
             'r744mslt': 'last', 'r744msut': 'last', 'r744mslr': 'last', 'r744msur': 'last', 'r744mswc': 'sum',
             'r744mrfc': 'sum', 'r744mrpc': 'sum', 'r744mrst': 'sum', 'r744mrsq': 'sum', 'r744mwst': 'sum',
             'r744mwsq': 'sum', 'r744mrbt': 'sum', 'r744mwbt': 'sum', 'r744maec': 'sum', 'r744msrl': 'sum',
             'r744msrr': 'sum', 'r744msrm': 'sum', 'r744mmbl': 'max', 'r744mmbe': 'max', 'r744mnel': 'min',
             'r744mnec': 'min', 'r744msrk': 'sum', 'csc': 'first'},
    'adup': {'r744afo': 'last', 'r744aheo': 'max', 'r744alaoh': 'max', 'r744alaosh': 'max', 'r744alcoh': 'max',
             'r744alcoph': 'max', 'r744alao': 'sum', 'r744alaos': 'sum', 'r744alco': 'sum', 'r744alcop': 'sum',
             'r744atpoct': 'sum', 'r744atpoc': 'sum', 'r744arcpot': 'sum', 'r744arcpo': 'sum',
             'r744acqsc': 'sum', 'r744apdt': 'sum', 'r744apdq': 'sum', 'r744amdt': 'sum', 'r744amdq': 'sum',
             'r744aqdt': 'sum', 'r744aqdq': 'sum', 'r744aqst': 'sum', 'r744aqsq': 'sum', 'r744acdt': 'sum',
             'r744acdq': 'sum', 'r744ardt': 'sum', 'r744ardq': 'sum', 'r744aott': 'sum', 'r744aotq': 'sum',
             'r744astt': 'sum', 'r744astq': 'sum', 'csc': 'first'},
    'str': {'r744qsiz': 'last', 'r744qver': 'last', 'r744qact': 'last', 'r744qrbn': 'last', 'r744qrbo': 'last',
            'r744qtra': 'last', 'r744qhol': 'last', 'r744qdpt': 'last', 'r744qrbp': 'last', 'r744qrbd': 'last',
            'r744qaad': 'last', 'r744styp': 'last', 'r744scei': 'last', 'r744sadi': 'last', 'r744scad': 'last',
            'r744sdas': 'last', 'r744spri': 'last', 'r744ssec': 'last', 'r744senc': 'last', 'r744slec': 'last',
            'r744slel': 'max', 'r744slem': 'last', 'r744sltl': 'last', 'r744sltm': 'last', 'r744ssta': 'sum',
            'r744strc': 'sum', 'r744stac': 'sum', 'r744sarc': 'sum', 'r744satm': 'sum', 'r744sasq': 'sum',
            'r744ssrc': 'sum', 'r744sstm': 'sum', 'r744sssq': 'sum', 'r744sqrc': 'sum', 'r744sqtm': 'sum',
            'r744sqsq': 'sum', 'r744sdrc': 'sum', 'r744sdtm': 'sum', 'r744sdsq': 'sum', 'r744sdmp': 'sum',
            'r744shto': 'sum', 'r744shmn': 'min', 'r744shmx': 'max', 'r744slto': 'sum', 'r744slmn': 'min',
            'r744slmx': 'max', 'r744sdto': 'sum', 'r744sdmn': 'min', 'r744sdmx': 'max', 'r744scn': 'sum',
            'r744sfcn': 'sum', 'r744ssiz': 'last', 'r744smas': 'max', 'r744smis': 'min', 'r744sdec': 'mean',
            'r744sdel': 'mean', 'r744snlh': 'sum', 'r744smae': 'max', 'r744scue': 'last', 'r744cdsi': 'last',
            'r744cdne': 'sum', 'r744spln': 'sum', 'r744spes': 'sum', 'r744sptc': 'sum', 'r744spst': 'sum',
            'r744spss': 'sum', 'r744srtc': 'sum', 'r744srst': 'sum', 'r744srss': 'sum', 'r744sctc': 'sum',
            'r744scst': 'sum', 'r744scss': 'sum', 'r744slsv': 'last', 'r744setm': 'sum', 'r744sisc': 'last',
            'r744snsc': 'sum', 'r744ssac': 'sum', 'r744sosa': 'sum', 'r744siad': 'last', 'r744sadn': 'sum',
            'r744sixc': 'sum', 'r744sxsc': 'sum', 'r744sxst': 'sum', 'r744sxsq': 'sum', 'r744sado': 'sum',
            'r744sadr': 'sum', 'r744sqch': 'last', 'r744sxap': 'last', 'r744sxas': 'last', 'r744sxcm': 'last',
            'r744sxmo': 'last', 'r744swdr': 'sum', 'r744swac': 'sum', 'r744srdr': 'sum', 'r744srac': 'sum',
            'r744swec': 'sum', 'r744srec': 'sum', 'r744swed': 'sum', 'r744swes': 'sum', 'r744sred': 'sum',
            'r744sres': 'sum', 'r744smrc': 'sum', 'r744smtm': 'sum', 'r744smsq': 'sum', 'r744smto': 'sum',
            'r744smht': 'sum', 'r744smmn': 'min', 'r744smmx': 'max', 'r744smhn': 'min', 'r744smhx': 'max',
            'r744crhc': 'sum', 'r744crmd': 'sum', 'r744crma': 'sum', 'r744crmn': 'sum', 'r744crmt': 'sum',
            'r744cwh0': 'sum', 'r744cwh1': 'sum', 'r744cwmn': 'sum', 'r744cwmi': 'sum', 'r744cwmt': 'sum',
            'r744cder': 'sum', 'r744cdtr': 'sum', 'r744cxdr': 'sum', 'r744cxfw': 'sum', 'r744cxni': 'sum',
            'r744cxci': 'sum', 'r744ccoc': 'sum', 'r744crsm': 'sum', 'r744ctsf': 'sum', 'r744cdec': 'last',
            'r744cdac': 'last', 'r744ctcc': 'sum', 'r744cdta': 'sum', 'r744crlc': 'sum', 'r744cprl': 'sum',
            'r744cxrl': 'sum', 'r744cwuc': 'sum', 'r744msma': 'max', 'r744malg': 'last', 'r744mfau': 'last',
            'r744miua': 'max', 'r744mius': 'max', 'r744mema': 'max', 'r744meml': 'max', 'r744meme': 'max',
            'r744menl': 'max', 'r744mene': 'max', 'r744mslt': 'last', 'r744msut': 'last', 'r744mslr': 'last',
            'r744msur': 'last', 'r744mswc': 'sum', 'r744mrfc': 'sum', 'r744mrpc': 'sum', 'r744mrst': 'sum',
            'r744mrsq': 'sum', 'r744mwst': 'sum', 'r744mwsq': 'sum', 'r744mrbt': 'sum', 'r744mwbt': 'sum',
            'r744maec': 'sum', 'r744msrl': 'sum', 'r744msrr': 'sum', 'r744msrm': 'sum', 'r744mmbl': 'max',
            'r744mmbe': 'max', 'r744mnel': 'min', 'r744mnec': 'min', 'r744msrk': 'sum', 'r744afo': 'last',
            'r744aheo': 'max', 'r744alaoh': 'max', 'r744alaosh': 'max', 'r744alcoh': 'max', 'r744alcoph': 'max',
            'r744alao': 'sum', 'r744alaos': 'sum', 'r744alco': 'sum', 'r744alcop': 'sum', 'r744atpoct': 'sum',
            'r744atpoc': 'sum', 'r744arcpot': 'sum', 'r744arcpo': 'sum', 'r744acqsc': 'sum', 'r744apdt': 'sum',
            'r744apdq': 'sum', 'r744amdt': 'sum', 'r744amdq': 'sum', 'r744aqdt': 'sum', 'r744aqdq': 'sum',
            'r744aqst': 'sum', 'r744aqsq': 'sum', 'r744acdt': 'sum', 'r744acdq': 'sum', 'r744ardt': 'sum',
            'r744ardq': 'sum', 'r744aott': 'sum', 'r744aotq': 'sum', 'r744astt': 'sum', 'r744astq': 'sum',
            'r744qflg': 'last', 'r744qfl1': 'last', 'r744sflg': 'last', 'r744sxfl': 'last'},
    'cdev': {'r745cint': 'sum', 'r745dcid': 'last', 'r745dev4': 'last', 'r745dscs': 'last', 'r745dccu': 'last',
             'r745dunt': 'last', 'r745dvol': 'last', 'r745dnav': 'last', 'r745dpdf': 'last', 'r745dfrm': 'last',
             'r745dvid': 'last', 'r745dsdv': 'last', 'r745dsfw': 'last', 'r745dspd': 'last', 'r745dssd': 'last',
             'r745dsdp': 'last', 'r745dvs2': 'last', 'r745dcol': 'last', 'r745defn': 'last', 'r745dbdp': 'last',
             'r745dpdt': 'last', 'r745incr': 'last', 'r7451unt': 'last', 'r745drcr': 'sum', 'r745dcrh': 'sum',
             'r745dwrc': 'sum', 'r745dwch': 'sum', 'r745drsr': 'sum', 'r745drsh': 'sum', 'r745dwsr': 'sum',
             'r745dwsh': 'sum', 'r745drnr': 'sum', 'r745dnrh': 'sum', 'r745dwnr': 'sum', 'r745dwnh': 'sum',
             'r745dicl': 'sum', 'r745dbcr': 'sum', 'r745dtc': 'sum', 'r745dntd': 'sum', 'r745dctd': 'sum',
             'r745dfwb': 'sum', 'r745dfwc': 'sum', 'r745dfws': 'sum', 'r745dcrm': 'sum', 'r745dcwp': 'sum',
             'r745dkdw': 'sum', 'r745dkdh': 'sum', 'r745dfwr': 'sum', 'r745bytr': 'sum', 'r745bytw': 'sum',
             'r745rtir': 'sum', 'r745rtiw': 'sum', 'total_io': 'sum', 'cache_io': 'sum', 'total_hits': 'sum',
             'total_reads': 'sum', 'read_hits': 'sum', 'total_writes': 'sum', 'fast_writes': 'sum',
             'write_hits': 'sum', 'dasd_io': 'sum',
             'r7452pro': 'sum', 'r7452pwo': 'sum', 'r7452pbr': 'sum', 'r7452pbw': 'sum', 'r7452prt': 'sum', 'r7452pwt': 'sum',
             'r7451rrq': 'sum', 'r7451wrq': 'sum', 'r7451sr': 'sum', 'r7451sw': 'sum', 'r7451rrt': 'sum', 'r7451wrt': 'sum',
             'r7451rmr': 'sum', 'r7451xsf': 'sum', 'r7451xcw': 'sum', 'r7451tsp': 'sum', 'r7451nvs': 'sum',
             'r7451ct1': 'sum', 'r7451ct2': 'sum', 'r7451ct3': 'sum', 'r7451ct4': 'sum', 'r7451ct5': 'sum',
             'r7451ct6': 'sum', 'r7451zhl': 'sum', 'r7451zhh': 'sum', 'r7451gsf': 'sum', 'r7451gss': 'sum',
             'r7451srr': 'sum', 'r7451srh': 'sum', 'r7451swr': 'sum', 'r7451swh': 'sum', 'r745dfl4': 'last',
             'r745dflg': 'last', 'r745dsg2': 'last', 'r745dvs1': 'last'},
    'raid': {'r7451sio': 'last', 'r7451hpf': 'last', 'r7451xfl': 'last', 'r7451scs': 'last', 'r7451rsv': 'sum',
             'r7451flg': 'last', 'r7451aid': 'last', 'r7451hdd': 'last', 'r7451rty': 'last', 'r7451hss': 'last',
             'r7451rrq': 'sum', 'r7451wrq': 'sum', 'r7451sr': 'sum', 'r7451sw': 'sum', 'r7451rrt': 'sum',
             'r7451wrt': 'sum', 'r7451unt': 'last', 'r7451rmr': 'sum', 'r7451xsf': 'sum', 'r7451xcw': 'sum',
             'r7451tsp': 'sum', 'r7451nvs': 'sum', 'r7451ct1': 'sum', 'r7451ct2': 'sum', 'r7451ct3': 'sum',
             'r7451ct4': 'sum', 'r7451ct5': 'sum', 'r7451ct6': 'sum', 'r7451zhl': 'sum', 'r7451zhh': 'sum',
             'r7451gsf': 'sum', 'r7451gss': 'sum', 'r7451srr': 'sum', 'r7451srh': 'sum', 'r7451swr': 'sum',
             'r7451swh': 'sum', 'r7451rid': 'last', 'r745dvol': 'last'},
    'rrank': {'r7451sio': 'last', 'r7451hpf': 'last', 'r7451xfl': 'last', 'r7451scs': 'last', 'r7451rsv': 'sum',
              'r7451flg': 'last', 'r7451aid': 'last', 'r7451hdd': 'last', 'r7451rty': 'last', 'r7451hss': 'last',
              'r7451rrq': 'sum', 'r7451wrq': 'sum', 'r7451sr': 'sum', 'r7451sw': 'sum', 'r7451rrt': 'sum',
              'r7451wrt': 'sum', 'r7451unt': 'last', 'r7451rmr': 'sum', 'r7451xsf': 'sum', 'r7451xcw': 'sum',
              'r7451tsp': 'sum', 'r7451nvs': 'sum', 'r7451ct1': 'sum', 'r7451ct2': 'sum', 'r7451ct3': 'sum',
              'r7451ct4': 'sum', 'r7451ct5': 'sum', 'r7451ct6': 'sum', 'r7451zhl': 'sum', 'r7451zhh': 'sum',
              'r7451gsf': 'sum', 'r7451gss': 'sum', 'r7451srr': 'sum', 'r7451srh': 'sum', 'r7451swr': 'sum',
              'r7451swh': 'sum', 'r745ssid': 'last'},
    'xpool': {'r745dvol': 'last', 'r7451sio': 'last', 'r7451hpf': 'last', 'r7451xfl': 'last', 'r7451scs': 'last',
              'r7451rsv': 'sum', 'r7451flg': 'last', 'r7452xty': 'last', 'r7452dxa': 'last', 'r7452dsh': 'last',
              'r7452mis': 'last', 'ccmt_seqn': 'last', 'r7451unt': 'last', 'r7451rmr': 'sum', 'r7451xsf': 'sum',
              'r7451xcw': 'sum', 'r7451tsp': 'sum', 'r7451nvs': 'sum', 'r7451ct1': 'sum', 'r7451ct2': 'sum',
              'r7451ct3': 'sum', 'r7451ct4': 'sum', 'r7451ct5': 'sum', 'r7451ct6': 'sum', 'r7451zhl': 'sum',
              'r7451zhh': 'sum', 'r7451gsf': 'sum', 'r7451gss': 'sum', 'r7451srr': 'sum', 'r7451srh': 'sum',
              'r7451swr': 'sum', 'r7451swh': 'sum', 'r748xpid': 'last'},
    'cachsys': {'smf_type': 'first', 'r745clvl': 'last', 'r745cmdl': 'last', 'r745cuid': 'last',
                'r745csc': 'last', 'r745cae': 'last', 'r745crtn': 'last', 'r745cioc': 'last', 'r745cint': 'sum',
                'r745cfdv': 'last', 'r745ccmt_typen': 'last', 'r745ccmt_modn': 'last', 'r745ccmt_manuf': 'last',
                'r745ccmt_pmanu': 'last', 'r745ccmt_seqn': 'last', 'r745ccmt_tag': 'last', 'r745svol': 'last',
                'r745sunt': 'last', 'r745sdev': 'last', 'r745sln': 'last', 'r745sft': 'last', 'r745sdid': 'last',
                'r745snad': 'last', 'r745snss': 'last', 'r745sos': 'last', 'r745snr': 'last', 'r745snht': 'last',
                'r745snis': 'last', 'r745dfwi': 'last', 'r745snds': 'last', 'r745snpe': 'last',
                'r745scln': 'last', 'r745scsf': 'last', 'r745scnf': 'last', 'r745savl': 'last',
                'r745spin': 'last', 'r745soff': 'last', 'r745sdcs': 'last', 'r745sdfw': 'last',
                'r745spdp': 'last', 'r745ssdp': 'last', 'r745sdps': 'last', 'r745sds2': 'last',
                'r745scnv': 'last', 'r745spnd': 'last', 'r745scol': 'last', 'r745sfvs': 'last',
                'r745sdbp': 'last', 'r745spda': 'last', 'r745sgl': 'last', 'ccmt_seqn': 'first',
                'r745drcr': 'sum', 'r745dcrh': 'sum', 'r745dwrc': 'sum', 'r745dwch': 'sum', 'r745drsr': 'sum',
                'r745drsh': 'sum', 'r745dwsr': 'sum', 'r745dwsh': 'sum', 'r745drnr': 'sum', 'r745dnrh': 'sum',
                'r745dwnr': 'sum', 'r745dwnh': 'sum', 'r745dicl': 'sum', 'r745dbcr': 'sum', 'r745dtc': 'sum',
                'r745dntd': 'sum', 'r745dctd': 'sum', 'r745dfwb': 'sum', 'r745dfwc': 'sum', 'r745dfws': 'sum',
                'r745dcrm': 'sum', 'r745dcwp': 'sum', 'r745dkdw': 'sum', 'r745dkdh': 'sum', 'r745dfwr': 'sum',
                'r745bytr': 'sum', 'r745bytw': 'sum', 'r745rtir': 'sum', 'r745rtiw': 'sum', 'total_io': 'sum',
                'cache_io': 'sum', 'total_hits': 'sum', 'total_reads': 'sum', 'read_hits': 'sum',
                'total_writes': 'sum', 'fast_writes': 'sum', 'write_hits': 'sum', 'dasd_io': 'sum',
                'r7451unt': 'last', 'r7452pro': 'sum', 'r7452pwo': 'sum', 'r7452pbr': 'sum', 'r7452pbw': 'sum',
                'r7451rmr': 'sum', 'r7451xsf': 'sum', 'r7451xcw': 'sum', 'r7451tsp': 'sum', 'r7451nvs': 'sum',
                'r7452prt': 'sum', 'r7452pwt': 'sum', 'r7451ct1': 'sum', 'r7451ct2': 'sum', 'r7451ct3': 'sum',
                'r7451ct4': 'sum', 'r7451ct5': 'sum', 'r7451ct6': 'sum', 'r7451zhl': 'sum', 'r7451zhh': 'sum',
                'r7451gsf': 'sum', 'r7451gss': 'sum', 'r7451srr': 'sum', 'r7451srh': 'sum', 'r7451swr': 'sum',
                'r7451swh': 'sum',
                'r745scs': 'last', 'r745svss': 'last', 'r745sds1': 'last', 'r745sg2': 'last'},
    'hfs': {'r746gmxv': 'max', 'r746gusv': 'max', 'r746gmnf': 'min', 'r746gusf': 'max', 'r746gmc': 'sum',
            'r746gmnc': 'sum', 'r746g1c': 'sum', 'r746g1nc': 'sum', 'r746glrs': 'last', 'r746glrc': 'last',
            'r746gsrc': 'last', 'r746gsrs': 'last', 'r746gonr': 'last', 'r746gnbl': 'last', 'r746gngd': 'last',
            'r746gpgd': 'last', 'smf_type': 'first', 'r746gsfl': 'last'},
    'gbuf': {'r746gsb': 'first', 'r746gnds': 'first', 'r746gsbp': 'first', 'r746gsbf': 'first', 'r746gbf': 'sum',
             'r746gbnf': 'sum'},
    'fsys': {'r746fsnl': 'first', 'r746fnhs': 'first', 'r746fmtc': 'first', 'r746ffsm': 'first', 'r746fmtm': 'max',
             'r746fsf': 'first', 'r746fpf': 'max', 'r746fpd': 'max', 'r746fpc': 'max', 'r746fsfi': 'sum',
             'r746frfi': 'sum', 'r746fmc': 'sum', 'r746fmnc': 'sum', 'r746f1c': 'sum', 'r746f1nc': 'sum',
             'r746fint': 'sum', 'r746fis': 'sum', 'r746fij': 'sum', 'r746firh': 'sum', 'r746firm': 'sum',
             'r746fiwh': 'sum', 'r746fiwm': 'sum', 'r746fsrc': 'last', 'r746fsrs': 'last', 'r746fsfl': 'last'},
    'port': {'smf74sid': 'last', 'r747ppir': 'last', 'r747pnti': 'last', 'r747plf': 'last', 'r747poff': 'last',
             'r747pscr': 'last', 'ndeconfigcode': 'last', 'ndetype': 'last', 'ndemodel': 'last', 'ndemfg': 'last',
             'ndeplant': 'last', 'ndesequence': 'last', 'ndecpcid': 'last', 'r747pfpt': 'sum', 'r747pnwr': 'sum',
             'r747pnwt': 'sum', 'r747pnfr': 'sum', 'r747pnft': 'sum', 'r747pner': 'sum'},
    'connector': {'r747cscu': 'last', 'r747cmcu': 'last', 'r747cchp': 'last', 'r747csw': 'last',
                  'r747ctnu': 'last', 'r747cinu': 'last', 'r747cosy': 'last', 'r747cins': 'last',
                  'r747cvar': 'last', 'r747crem': 'last', 'r747cact': 'last', 'r747cnmd': 'last',
                  'r747ccun': 'last', 'r747ctfl': 'last', 'r747csfl': 'last'},
    'switch': {'r747slsn': 'last', 'r747svar': 'last', 'r747snpc': 'last', 'r747soff': 'last', 'r747snol': 'last',
               'r747sfcs': 'last', 'ndeconfigcode': 'last', 'ndetype': 'last', 'ndemodel': 'last', 'ndemfg': 'last',
               'ndeplant': 'last', 'ndesequence': 'last', 'ndecpcid': 'last', 'r747snsp': 'last', 'r747snip': 'last',
               'r747pfpt': 'sum', 'r747pnwr': 'sum', 'r747pnwt': 'sum', 'r747pnfr': 'sum', r'r747pnft': 'sum',
               'r747pner': 'sum', 'r747spfl': 'last'},
    'fcd': {'smf_type': 'first', 'r747gdca': 'last', 'r747giac': 'last', 'r747giod': 'last', 'r747gicv': 'last',
            'r747gnfd': 'last', 'r747ginm': 'last', 'r747gisf': 'last', 'r747gict': 'last', 'r747pfpt': 'sum',
            'r747pnwr': 'sum', 'r747pnwt': 'sum', 'r747pnfr': 'sum', r'r747pnft': 'sum', 'r747pner': 'sum',
            'r747gcfl': 'last'},
    'cntl': {'r748clvl': 'last', 'r748ctyp': 'last', 'r748cmdl': 'last', 'r748cvsn': 'last', 'r748cae': 'last',
             'r748crtn': 'last', 'r748csc': 'last', 'r748cioc': 'last', 'r748cfdv': 'last', 'r748cvol': 'last',
             'r748cdev': 'last', 'r748cxvl': 'last', 'r748cscs': 'last', 'r748cint': 'sum', 'r748cftm': 'last',
             'r748cfdt': 'last', 'r748cfci': 'last', 'r748cfsc': 'last', 'smf_type': 'first', 'r748cflg': 'last', },
    'lss': {'r748ltyp': 'first', 'r748lbyt': 'first', 'r748ltim': 'first', 'r748lerb': 'sum', 'r748lewb': 'sum',
            'r748lero': 'sum', 'r748lewo': 'sum', 'r748lert': 'sum', 'r748lewt': 'sum', 'r748lpsb': 'sum',
            'r748lprb': 'sum', 'r748lpso': 'sum', 'r748lpro': 'sum', 'r748lpst': 'sum', 'r748lprt': 'sum',
            'r748lsrb': 'sum', 'r748lswb': 'sum', 'r748lsro': 'sum', 'r748lswo': 'sum', 'r748lsrt': 'sum',
            'r748lswt': 'sum', 'r748lflf': 'sum', 'r748lfly': 'sum', 'r748lfls': 'sum', 'r748lfpq': 'sum',
            'r748lfit': 'sum', 'r748lfcr': 'sum', 'r748lfr1': 'sum', 'r748lfr2': 'sum', 'r748lfif': 'sum',
            'r748lfod': 'sum', 'r748lfoa': 'sum', 'r748lfdf': 'sum', 'r748lfio': 'sum', 'r748lftc': 'sum',
            'r748lfbc': 'mean', 'r748lflg': 'last'},
    'arry': {'r748aebc': 'last', 'r748atyp': 'last', 'r748aasp': 'last', 'r748aawd': 'last', 'r748aacp': 'last',
             'r748adc': agg_r748adc, 'r748ard': 'last', 'r748adt': 'last', 'r748are': 'last', 'r748acmp': 'max',
             'rank_cap': 'last', 'r748aast': 'last'},
    'rank': {'r748rcnt': 'last', 'r748rbyr': 'sum', 'r748rbyw': 'sum', 'r748rrop': 'sum', 'r748rwop': 'sum',
             'r748rkrt': 'sum', 'r748rkwt': 'sum', 'data_encrypted_rank': 'first', 'compression_rank': 'last',
             'r748rai': 'first', 'r748rpnm': 'first',
             'rank_adapter_id_valid': 'first', 'r748aebc': 'last', 'r748atyp': 'last', 'r748aasp': 'min',
             'r748aawd': 'last',
             'r748aacp': 'last', 'r748adc': agg_r748adc, 'r748ard': 'max', 'r748adt': 'max', 'r748are': 'max',
             'r748acmp': 'max', 'rank_cap': 'last', 'r748rtq': 'last', 'r748aast': 'last'},
    'siol': {'r748styp': 'first', 'r748sspd': 'first', 'r748swdh': 'first', 'r748sste': 'first', 'r748sbyt': 'first',
             'r748stim': 'first', 'r748scbr': 'sum', 'r748scro': 'sum', 'r748scrs': 'sum', 'r748scrt': 'sum',
             'r748scbw': 'sum', 'r748scwo': 'sum', 'r748scws': 'sum', 'r748scwt': 'sum', 'r748snbw': 'sum',
             'r748snwo': 'sum', 'r748snws': 'sum', 'r748snwt': 'sum', 'r748sflg': 'first'},
    'extp': {'r748xplt': 'last', 'encrypted_extent_pool': 'last', 'compression_extent_pool': 'last',
             'extent_sizes_valid': 'last', 'r748xrcp': 'last', 'r748xrns': 'last', 'r748xrna': 'last',
             'r748xrsc': 'sum', 'r748xvcp': 'last', 'r748xvns': 'last', 'r748xvsc': 'sum', 'r748xsdy': 'sum',
             'r748xtdy': 'sum', 'r748xeps': 'last', 'r748xtpc': 'last', 'r748xupc': 'last', 'r748xtlc': 'last',
             'r748xulc': 'last', 'r748rcnt': 'last', 'r748rbyr': 'sum', 'r748rbyw': 'sum', 'r748rrop': 'sum',
             'r748rwop': 'sum', 'r748rkrt': 'sum', 'r748rkwt': 'sum', 'data_encrypted_rank': 'last',
             'compression_rank': 'last', 'rank_adapter_id_valid': 'last',
             'r748rai': 'last', 'r748aebc': agg_r748aebc, 'r748atyp': agg_r748atyp, 'r748aasp': 'min',
             'r748aawd': 'last', 'r748aacp': 'last', 'rank_cap': 'last', 'r748adc': agg_r748adc, 'r748ard': 'max',
             'r748adt': 'max', 'r748are': 'max', 'r748acmp': 'max',
             'r748xptq': 'last', 'r748rtq': 'last', 'r748aast': 'last'},
    'srtd': {'response_time_for_sync_io_read': 'last', 'r749rtsc': 'sum', 'r749rflg': 'last'},
    'pcie': {'smf74sid': 'last', 'csc': 'last', 'r749asid': 'last', 'r749jobn': 'last', 'r749pcid': 'last',
            'status': 'last', 'r749atst': 'last', 'physical_network': 'max', 'pcie_valid': 'max',
            'pci_oper_rates_invalid': 'max', 'global_performance': 'max', 'r749errt': 'sum', 'r749devt': 'last',
            'r749devn': 'last', 'r749allt': 'sum', 'r749scnt': 'last', 'r749loop': 'sum', 'r749stop': 'sum',
            'r749sbop': 'sum', 'r749rfop': 'sum', 'r749port': 'last', 'r749pft': 'last', 'r749net1': 'last',
            'r749net2': 'last', 'r749wwnn': 'last', 'r749lkid': 'last', 'r749dman': 'last', 'r749fpfn': 'last',
            'r749fp1n': 'last', 'r749sion': 'last', 'r749rtdn': 'last', 'r749sndt': 'last', 'r749sndm': 'last',
            'r749sndn': 'last', 'r749sndp': 'last', 'r749snds': 'last', 'r749dfmt': 'last', 'r749dmar': 'sum',
            'r749dmaw': 'sum', 'r749dbyr': 'sum', 'r749dbyt': 'sum', 'r749dpkr': 'sum', 'r749dpkt': 'sum',
            'r749dwup': 'sum', 'r749dwum': 'sum', 'r749dbyx': 'sum', 'r749srbf': 'sum', 'r749swbf': 'sum',
            'r749ssrf': 'sum', 'r749slrf': 'sum', 'r749srrf': 'sum', 'r749stpf': 'sum', 'r749srbc': 'sum',
            'r749swbc': 'sum', 'r749ssrc': 'sum', 'r749slrc': 'sum', 'r749srrc': 'sum', 'r749stpc': 'sum',
            'r749ftyp': 'last', 'r749fdsc': 'last', 'r749frqc': 'sum', 'r749frqe': 'sum', 'r749fqfl': 'sum',
            'r749ftet': 'sum', 'r749fsqe': agg_hex_sum, 'r749ftqt': 'sum', 'r749fsqq': agg_hex_sum,
            'r749fdrd': 'sum', 'r749fdwr': 'sum', 'stdd_ftet': 'mean', 'stdd_ftqt': 'mean', 'r7491dib': 'sum',
            'r7491dis': agg_hex_sum, 'r7491dob': 'sum', 'r7491dos': agg_hex_sum, 'r7491dct': 'sum',
            'r7491iib': 'sum', 'r7491iis': agg_hex_sum, 'r7491iob': 'sum', 'r7491ios': agg_hex_sum,
            'r7491ict': 'sum', 'r7491bps': 'last', 'r7491bpc': 'sum', 'stdd_1dib': 'mean', 'stdd_1dob': 'mean',
            'stdd_1iib': 'mean', 'stdd_1iob': 'mean', 'smf_type': 'first'},
    'scm': {'smf74int': 'sum', 'r7410cdus': 'last', 'r7410crqc': 'sum', 'r7410crq': 'sum', 'r7410cdwc': 'sum',
            'r7410cdw': 'sum', 'r7410cdrc': 'sum', 'r7410cdr': 'sum', 'r7410crtc': 'sum', 'r7410crt': 'sum',
            'r7410ciqc': 'sum', 'r7410cwuc': 'mean', 'r7410cwu': 'mean', 'r7410vfm': 'first',
            'r7410cdwc_bytes': 'sum', 'r7410cdw_bytes': 'sum', 'r7410cdrc_bytes': 'sum', 'r7410cdr_bytes': 'sum',
            'smf_type': 'first', 'r7410flg': 'last'},
    'eadm': {'smf74int': 'sum', 'r7410dsct': 'sum', 'r7410dnum': 'sum', 'r7410dfpt': 'sum', 'r7410diqt': 'sum',
             'r7410dcrt': 'sum', 'r7410ecpr': 'first', 'r7410docc': 'sum', 'r7410docd': 'sum', 'r7410disc': 'sum',
             'r7410dosc': 'sum', 'r7410disd': 'sum', 'r7410dosd': 'sum', 'smf_type': 'first', 'r7410dflg': 'last'}
}


def sum_74db(db_engines: dict, db_session: Session, summary_level: str, start_time_str: str, end_time_str: str,
             partitions_scheme: str, db_driver: str = 'postgresql+psycopg2') -> UploadResult:
    """Summarize smf74 interval database to the hourly or daily database.

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
    # inner functions
    def sum_up_dev():
        result = 0
        df_dev_list = []
        null_column_list = []
        dev_stmt = select(Smf74Dev).where(Smf74Dev.datetime.between(start, end))
        for part in partitions_range:
            df_dev = pd.read_sql(dev_stmt, db_engines[f'74.{part}'])
            if not df_dev.empty:
                df_dev['date'] = df_dev['datetime'].dt.date
                df_dev_list.append(df_dev)
                null_columns = df_dev.columns[df_dev.isna().all()].tolist()
                for col in null_columns:
                    if col not in null_column_list:
                        null_column_list.append(col)
        if len(df_dev_list) > 0:
            df_devs = pd.concat([df.dropna(axis=1, how='all') for df in df_dev_list])
            if len(null_column_list) > 0:
                new_cols = df_devs.columns.tolist()
                for col in null_column_list:
                    if col not in new_cols:
                        new_cols.append(col)
                df_devs = df_devs.reindex(columns=new_cols)
            df_dev_sum = df_devs.groupby(
                [col.name for col in summary_class[summary_level]['dev'].__table__.primary_key.columns.values()]).agg(
                agg_dict['dev']).copy().reset_index()
            if 'date' not in df_dev_sum.columns:
                df_dev_sum['date'] = df_dev_sum['datetime'].dt.date
            df_dev_sum['last_update_time'] = current_time
            df_dev_sum['sync_avg_read_resp_time'] = ((df_dev_sum['smf74spr'] / (df_dev_sum['smf74sqr'] * 2000))
                                                    .where(df_dev_sum['smf74sqr'] > 0, 0))
            df_dev_sum['sync_avg_write_resp_time'] = ((df_dev_sum['smf74spw'] / (df_dev_sum['smf74sqw'] * 2000))
                                                     .where(df_dev_sum['smf74sqw'] > 0, 0))
            df_dev_sum['device_active_time'] = df_dev_sum['smf74atv'] / df_dev_sum['smf74mec']
            df_dev_sum['IOSQ_time'] = np.where(df_dev_sum['smf74sub'] != '0080',
                                              (df_dev_sum['smf74que'] / df_dev_sum['smf74sam']) / (
                                                      df_dev_sum['smf74ssc'] / df_dev_sum['smf74int']),
                                              df_dev_sum['smf74ios'] / df_dev_sum['smf74ssc'])
            df_dev_sum['avg_resp_time'] = df_dev_sum['device_active_time'] + df_dev_sum['IOSQ_time']
            df_dev_sum['avg_iosq_time'] = (df_dev_sum['smf74ios'] / df_dev_sum['smf74ssc']).where(df_dev_sum['smf74ssc'] > 0, 0)
            df_dev_sum['avg_cmr_dly'] = (df_dev_sum['smf74cmr'] / df_dev_sum['smf74mec']).where(df_dev_sum['smf74mec'] > 0, 0)
            df_dev_sum['avg_db_dly'] = (df_dev_sum['smf74dvb'] / df_dev_sum['smf74mec']).where(df_dev_sum['smf74mec'] > 0, 0)
            df_dev_sum['avg_int_dly'] = (df_dev_sum['smf74idt'] / df_dev_sum['smf74mec']).where(df_dev_sum['smf74mec'] > 0, 0)
            df_dev_sum['avg_pend_time'] = (df_dev_sum['smf74pen'] / df_dev_sum['smf74mec']).where(df_dev_sum['smf74mec'] > 0, 0)
            df_dev_sum['avg_disc_time'] = (df_dev_sum['smf74dis'] / df_dev_sum['smf74mec']).where(df_dev_sum['smf74mec'] > 0, 0)
            df_dev_sum['avg_conn_time'] = (df_dev_sum['smf74cnn'] / df_dev_sum['smf74mec']).where(df_dev_sum['smf74mec'] > 0, 0)
            df_dev_sum['avg_numbr_alloc'] = df_dev_sum['smf74nda'] / df_dev_sum['smf74sam']
            df_dev_sum['avg_mt_time'] = (
                    df_dev_sum['smf74mtp'] * df_dev_sum['smf74int'] / df_dev_sum['smf74sam'] / df_dev_sum['smf74mtc']
            ).where(df_dev_sum['smf74mtc'] > 0, 0)
            result = df_upsert(db_driver, db_engines[summary_engine[summary_level]], db_session,
                               df_dev_sum[summary_class[summary_level]['dev'].__table__.columns.keys()],
                               summary_tblname[summary_level]['dev'], summary_class[summary_level]['dev'], 'smf74',
                               [col.name for col in summary_class[summary_level]['dev'].__table__.primary_key.columns.values()],
                               int_dtypedict['dev'], shard_id=summary_engine[summary_level]
                               )
        return result

    def sum_up_cf():
        result = 0
        df_cf_list = []
        null_column_list = []
        cf_stmt = select(Smf74Cf).where(Smf74Cf.datetime.between(start, end))
        for part in partitions_range:
            df_cf = pd.read_sql(cf_stmt, db_engines[f'74.{part}'])
            if not df_cf.empty:
                df_cf['date'] = df_cf['datetime'].dt.date
                df_cf_list.append(df_cf)
                null_columns = df_cf.columns[df_cf.isna().all()].tolist()
                for col in null_columns:
                    if col not in null_column_list:
                        null_column_list.append(col)
        if len(df_cf_list) > 0:
            df_cfs = pd.concat([df.dropna(axis=1, how='all') for df in df_cf_list])
            if len(null_column_list) > 0:
                new_cols = df_cfs.columns.tolist()
                for col in null_column_list:
                    if col not in new_cols:
                        new_cols.append(col)
                df_cfs = df_cfs.reindex(columns=new_cols)
            df_cf_sum = df_cfs.groupby(
                [col.name for col in summary_class[summary_level]['cf'].__table__.primary_key.columns.values()]).agg(
                agg_dict['cf']).copy().reset_index()
            if 'date' not in df_cf_sum.columns:
                df_cf_sum['date'] = df_cf_sum['datetime'].dt.date
            df_cf_sum['last_update_time'] = current_time
            df_cf_sum['avg_processor_weight'] = np.where(df_cf_sum['r744fpsn'] > 0,
                                                        df_cf_sum['r744pwgt'] / df_cf_sum['r744fpsn'],
                                                        0)
            result = df_upsert(db_driver, db_engines[summary_engine[summary_level]], db_session,
                               df_cf_sum[summary_class[summary_level]['cf'].__table__.columns.keys()],
                               summary_tblname[summary_level]['cf'], summary_class[summary_level]['cf'], 'smf74',
                               [col.name for col in summary_class[summary_level]['cf'].__table__.primary_key.columns.values()],
                               int_dtypedict['cf'], shard_id=summary_engine[summary_level]
                               )
        return result


    def sum_up_pcie():
        def find_match(row, response_time_for_sync_io_write, srtd_idx):  # , response_time_for_sync_io_write, srtd_idx):
            idx = row.name + (response_time_for_sync_io_write, srtd_idx,)
            try:
                return df_srtd_sum.loc[idx]['r749rtsc'].values[0]
            except KeyError:
                return np.nan
        result = 0
        srtd_stmt = select(Smf74Srtd).join_from(Smf74Pcie, Smf74Pcie.smf74_srtds).where(Smf74Srtd.datetime.between(start, end))
        pcie_stmt = select(Smf74Pcie).where(Smf74Pcie.datetime.between(start, end))
        df_srtd_list = []
        df_pcie_list = []
        null_column_list1 = []
        null_column_list2 = []
        for part in partitions_range:
            df_pcie = pd.read_sql(pcie_stmt, db_engines[f'74.{part}'])
            if not df_pcie.empty:
                df_pcie['date'] = df_pcie['datetime'].dt.date
                df_pcie_list.append(df_pcie)
                null_columns = df_pcie.columns[df_pcie.isna().all()].tolist()
                for col in null_columns:
                    if col not in null_column_list1:
                        null_column_list1.append(col)

                df_srtd = pd.read_sql(srtd_stmt, db_engines[f'74.{part}'])
                if not df_srtd.empty:
                    df_srtd['date'] = df_srtd['datetime'].dt.date
                    df_srtd_list.append(df_srtd)
                    null_columns = df_srtd.columns[df_srtd.isna().all()].tolist()
                    for col in null_columns:
                        if col not in null_column_list2:
                            null_column_list2.append(col)
        if len(df_srtd_list) > 0:
            df_srtds = pd.concat([df.dropna(axis=1, how='all') for df in df_srtd_list])
            if len(null_column_list2) > 0:
                new_cols = df_srtds.columns.tolist()
                for col in null_column_list2:
                    if col not in new_cols:
                        new_cols.append(col)
                df_srtds = df_srtds.reindex(columns=new_cols)
            df_srtd_sum = df_srtds.groupby(
                [col.name for col in summary_class[summary_level]['srtd'].__table__.primary_key.columns.values()]).agg(
                agg_dict['srtd']).copy().reset_index()
            if 'date' not in df_srtd_sum.columns:
                df_srtd_sum['date'] = df_srtd_sum['datetime'].dt.date
            df_srtd_sum.set_index(
                [col.name for col in summary_class[summary_level]['srtd'].__table__.primary_key.columns.values()],
                inplace=True)
        else:
            df_srtd_sum = pd.DataFrame()

        if len(df_pcie_list) > 0:
            df_pcies = pd.concat([df.dropna(axis=1, how='all') for df in df_pcie_list])
            if len(null_column_list1) > 0:
                new_cols = df_pcies.columns.tolist()
                for col in null_column_list1:
                    if col not in new_cols:
                        new_cols.append(col)
                df_pcies = df_pcies.reindex(columns=new_cols)
            df_pcie_sum = df_pcies.groupby(
                [col.name for col in summary_class[summary_level]['pcie'].__table__.primary_key.columns.values()]).agg(
                agg_dict['pcie']).copy().reset_index()
            if 'date' not in df_pcie_sum.columns:
                df_pcie_sum['date'] = df_pcie_sum['datetime'].dt.date
            df_pcie_sum['last_update_time'] = current_time
            df_pcie_sum['pciload'] = df_pcie_sum['r749loop'] / df_pcie_sum['r749allt']
            df_pcie_sum['pcistor'] = df_pcie_sum['r749stop'] / df_pcie_sum['r749allt']
            df_pcie_sum['pcistbl'] = df_pcie_sum['r749sbop'] / df_pcie_sum['r749allt']
            df_pcie_sum['pcirptr'] = df_pcie_sum['r749rfop'] / df_pcie_sum['r749allt']
            df_pcie_sum['fpgbusy'] = df_pcie_sum['r749ftet'] * 100 / df_pcie_sum['r749allt']
            df_pcie_sum['fpgrtim'] = df_pcie_sum['r749ftet'] * 1e6 / df_pcie_sum['r749frqc']
            df_pcie_sum['fpgqtim'] = df_pcie_sum['r749ftqt'] * 1e6 / df_pcie_sum['r749frqc']
            df_pcie_sum['fpgbyts'] = (df_pcie_sum['r749fdrd'] + df_pcie_sum['r749fdwr']) * 256 / (df_pcie_sum['r749allt'] * 1e6)
            df_pcie_sum['fpgbytr'] = (df_pcie_sum['r749fdrd'] + df_pcie_sum['r749fdwr']) * 256 / (
                        df_pcie_sum['r749frqc'] * 1000)
            df_pcie_sum['fpgcors'] = df_pcie_sum['r7491dct'] / df_pcie_sum['r749allt']
            df_pcie_sum['fpgcobs'] = df_pcie_sum['r7491dib'] / (df_pcie_sum['r749allt'] * 1e6)
            df_pcie_sum['fpgcort'] = df_pcie_sum['r7491dib'] / df_pcie_sum['r7491dob']
            df_pcie_sum['fpgdcrs'] = df_pcie_sum['r7491ict'] / df_pcie_sum['r749allt']
            df_pcie_sum['fpgdcbs'] = df_pcie_sum['r7491iib'] / (df_pcie_sum['r749allt'] * 1e6)
            df_pcie_sum['fpgdcrt'] = df_pcie_sum['r7491iib'] / df_pcie_sum['r7491iob']
            df_pcie_sum['fpgbprt'] = df_pcie_sum['r7491bpc'] / (
                    (df_pcie_sum['r7491dct'] + df_pcie_sum['r7491ict']) * df_pcie_sum['r7491bps'])
            if "0x00" in df_pcie_sum['r749dfmt'].values:
                df_pcie_sum['pcidmar'] = np.where(df_pcie_sum['r749dfmt'] == '0x00',
                                                 df_pcie_sum['r749dmar'] / (df_pcie_sum['r749allt'] * 1e6), np.nan)
                df_pcie_sum['pcidmaw'] = np.where(df_pcie_sum['r749dfmt'] == '0x00',
                                                 df_pcie_sum['r749dmaw'] / (df_pcie_sum['r749allt'] * 1e6), np.nan)
            if "0x01" in df_pcie_sum['r749dfmt'].values:
                df_pcie_sum['pcibytr'] = np.where(df_pcie_sum['r749dfmt'] == "0x01",
                                                 df_pcie_sum['r749dbyr'] / (df_pcie_sum['r749allt'] * 1e6), np.nan)
                df_pcie_sum['pcipakr'] = np.where(df_pcie_sum['r749dfmt'] == "0x01",
                                                 df_pcie_sum['r749dpkr'] / df_pcie_sum['r749allt'], np.nan)
                df_pcie_sum['pcipakt'] = np.where(df_pcie_sum['r749dfmt'] == "0x01",
                                                 df_pcie_sum['r749dpkt'] / df_pcie_sum['r749allt'], np.nan)
            if df_pcie_sum['r749dfmt'].isin(["0x01", "0x03"]).any():
                df_pcie_sum['pcibytt'] = np.where(df_pcie_sum['r749dfmt'] == "0x01",
                                                 df_pcie_sum['r749dbyt'] / (df_pcie_sum['r749allt'] * 1e6),
                                                 np.where(df_pcie_sum['r749dfmt'] == "0x03",
                                                          df_pcie_sum['r749dbyx'] / (df_pcie_sum['r749allt'] * 1e6), np.nan))
            if "0x02" in df_pcie_sum['r749dfmt'].values:
                df_pcie_sum['pciwup'] = np.where(df_pcie_sum['r749dfmt'] == "0x02",
                                                df_pcie_sum['r749dwup'] / df_pcie_sum['r749allt'], np.nan)
                df_pcie_sum['pciutil'] = np.where(df_pcie_sum['r749dfmt'] == "0x02",
                                                 df_pcie_sum['r749dwup'] * 100 / (
                                                         df_pcie_sum['r749allt'] * df_pcie_sum['r749dwum']), np.nan)
            if "0x04" in df_pcie_sum['r749dfmt'].values:
                df_pcie_sum['fpgbusy'] = np.where(df_pcie_sum['r749dfmt'] == "0x04",
                                                 df_pcie_sum['r749stpf'] * 100 / df_pcie_sum['r749allt'],
                                                 df_pcie_sum['fpgbusy'])
                df_pcie_sum['synctr'] = np.where(df_pcie_sum['r749dfmt'] == "0x04",
                                                (df_pcie_sum['r749ssrf'] + df_pcie_sum['r749slrf'] + df_pcie_sum['r749srrf']) /
                                                df_pcie_sum['r749allt'], np.nan)
                df_pcie_sum['syncsr'] = np.where(df_pcie_sum['r749dfmt'] == "0x04",
                                                df_pcie_sum['r749ssrf'] / df_pcie_sum['r749allt'], np.nan)
                df_pcie_sum['pcibytr'] = np.where(df_pcie_sum['r749dfmt'] == "0x04",
                                                 df_pcie_sum['r749srbf'] / (df_pcie_sum['r749allt'] * 1e6), np.nan)
                df_pcie_sum['pcibytt'] = np.where(df_pcie_sum['r749dfmt'] == "0x04",
                                                 df_pcie_sum['r749swbf'] / (df_pcie_sum['r749allt'] * 1e6), np.nan)
                df_pcie_sum['pcibytr_ratio'] = np.where(df_pcie_sum['r749dfmt'] == "0x04",
                                                       df_pcie_sum['r749srbf'] / (df_pcie_sum['r749ssrf'] * 1e6), np.nan)
                df_pcie_sum['pcibytt_ratio'] = np.where(df_pcie_sum['r749dfmt'] == "0x04",
                                                       df_pcie_sum['r749swbf'] / (df_pcie_sum['r749ssrf'] * 1e6), np.nan)

                df_pcie_sum['cpcfpgbusy'] = np.where(
                    (df_pcie_sum['global_performance'] == 1) & (df_pcie_sum['r749dfmt'] == "0x04"),
                    df_pcie_sum['r749stpc'] * 100 / df_pcie_sum['r749allt'], np.nan)
                df_pcie_sum['cpcsynctr'] = np.where(
                    (df_pcie_sum['global_performance'] == 1) & (df_pcie_sum['r749dfmt'] == "0x04"),
                    (df_pcie_sum['r749ssrc'] + df_pcie_sum['r749slrc'] + df_pcie_sum['r749srrc']) /
                    df_pcie_sum['r749allt'], np.nan)
                df_pcie_sum['cpcsyncsr'] = np.where(
                    (df_pcie_sum['global_performance'] == 1) & (df_pcie_sum['r749dfmt'] == "0x04"),
                    df_pcie_sum['r749ssrc'] / df_pcie_sum['r749allt'], np.nan)
                df_pcie_sum['cpcpcibytr'] = np.where(
                    (df_pcie_sum['global_performance'] == 1) & (df_pcie_sum['r749dfmt'] == "0x04"),
                    df_pcie_sum['r749srbc'] / (df_pcie_sum['r749allt'] * 1e6), np.nan)
                df_pcie_sum['cpcpcibytt'] = np.where(
                    (df_pcie_sum['global_performance'] == 1) & (df_pcie_sum['r749dfmt'] == "0x04"),
                    df_pcie_sum['r749swbc'] / (df_pcie_sum['r749allt'] * 1e6), np.nan)
                df_pcie_sum['cpcpcibytr_ratio'] = np.where(
                    (df_pcie_sum['global_performance'] == 1) & (df_pcie_sum['r749dfmt'] == "0x04"),
                    df_pcie_sum['r749srbc'] / (df_pcie_sum['r749ssrc'] * 1e6), np.nan)
                df_pcie_sum['cpcpcibytt_ratio'] = np.where(
                    (df_pcie_sum['global_performance'] == 1) & (df_pcie_sum['r749dfmt'] == "0x04"),
                    df_pcie_sum['r749swbc'] / (df_pcie_sum['r749ssrc'] * 1e6), np.nan)
            df_pcie_sum.set_index(
                [col.name for col in summary_class[summary_level]['pcie'].__table__.primary_key.columns.values()],
                inplace=True)
            if not df_srtd_sum.empty:
                df_pcie_sum['pcipcr1'] = df_pcie_sum.apply(find_match, args=[0, 0], axis=1)
                df_pcie_sum['pcipcr2'] = df_pcie_sum.apply(find_match, args=[0, 1], axis=1)
                df_pcie_sum['pcipcr3'] = df_pcie_sum.apply(find_match, args=[0, 2], axis=1)
                df_pcie_sum['pcipcr4'] = df_pcie_sum.apply(find_match, args=[0, 3], axis=1)
                df_pcie_sum['pcipcr5'] = df_pcie_sum.apply(find_match, args=[0, 4], axis=1)
                df_pcie_sum['pcipcr6'] = df_pcie_sum.apply(find_match, args=[0, 5], axis=1)
                df_pcie_sum['pcipcr7'] = df_pcie_sum.apply(find_match, args=[0, 6], axis=1)
                df_pcie_sum['pcipcr8'] = df_pcie_sum.apply(find_match, args=[0, 7], axis=1)
                df_pcie_sum['pcipcr9'] = df_pcie_sum.apply(find_match, args=[0, 8], axis=1)
                df_pcie_sum['pcipcr10'] = df_pcie_sum.apply(find_match, args=[0, 9], axis=1)
                df_pcie_sum['pcipcw1'] = df_pcie_sum.apply(find_match, args=[1, 0], axis=1)
                df_pcie_sum['pcipcw2'] = df_pcie_sum.apply(find_match, args=[1, 1], axis=1)
                df_pcie_sum['pcipcw3'] = df_pcie_sum.apply(find_match, args=[1, 2], axis=1)
                df_pcie_sum['pcipcw4'] = df_pcie_sum.apply(find_match, args=[1, 3], axis=1)
                df_pcie_sum['pcipcw5'] = df_pcie_sum.apply(find_match, args=[1, 4], axis=1)
                df_pcie_sum['pcipcw6'] = df_pcie_sum.apply(find_match, args=[1, 5], axis=1)
                df_pcie_sum['pcipcw7'] = df_pcie_sum.apply(find_match, args=[1, 6], axis=1)
                df_pcie_sum['pcipcw8'] = df_pcie_sum.apply(find_match, args=[1, 7], axis=1)
                df_pcie_sum['pcipcw9'] = df_pcie_sum.apply(find_match, args=[1, 8], axis=1)
                df_pcie_sum['pcipcw10'] = df_pcie_sum.apply(find_match, args=[1, 8], axis=1)
                df_pcie_sum['pcitosir'] = (
                        df_pcie_sum['pcipcr1'] + df_pcie_sum['pcipcr2'] + df_pcie_sum['pcipcr3'] + df_pcie_sum['pcipcr4'] +
                        df_pcie_sum['pcipcr5'] +
                        df_pcie_sum['pcipcr6'] + df_pcie_sum['pcipcr7'] + df_pcie_sum['pcipcr8'] + df_pcie_sum['pcipcr9'] +
                        df_pcie_sum['pcipcr10'])
                df_pcie_sum['pcitosiw'] = (
                        df_pcie_sum['pcipcw1'] + df_pcie_sum['pcipcw2'] + df_pcie_sum['pcipcw3'] + df_pcie_sum['pcipcw4'] +
                        df_pcie_sum['pcipcw5'] +
                        df_pcie_sum['pcipcw6'] + df_pcie_sum['pcipcw7'] + df_pcie_sum['pcipcw8'] + df_pcie_sum['pcipcw9'] +
                        df_pcie_sum['pcipcw10'])
                df_pcie_sum['pcipcr1'] = df_pcie_sum['pcipcr1'] * 100 / df_pcie_sum['pcitosir']
                df_pcie_sum['pcipcr2'] = df_pcie_sum['pcipcr2'] * 100 / df_pcie_sum['pcitosir']
                df_pcie_sum['pcipcr3'] = df_pcie_sum['pcipcr3'] * 100 / df_pcie_sum['pcitosir']
                df_pcie_sum['pcipcr4'] = df_pcie_sum['pcipcr4'] * 100 / df_pcie_sum['pcitosir']
                df_pcie_sum['pcipcr5'] = df_pcie_sum['pcipcr5'] * 100 / df_pcie_sum['pcitosir']
                df_pcie_sum['pcipcr6'] = df_pcie_sum['pcipcr6'] * 100 / df_pcie_sum['pcitosir']
                df_pcie_sum['pcipcr7'] = df_pcie_sum['pcipcr7'] * 100 / df_pcie_sum['pcitosir']
                df_pcie_sum['pcipcr8'] = df_pcie_sum['pcipcr8'] * 100 / df_pcie_sum['pcitosir']
                df_pcie_sum['pcipcr9'] = df_pcie_sum['pcipcr9'] * 100 / df_pcie_sum['pcitosir']
                df_pcie_sum['pcipcr10'] = df_pcie_sum['pcipcr10'] * 100 / df_pcie_sum['pcitosir']
                df_pcie_sum['pcipcw1'] = df_pcie_sum['pcipcw1'] * 100 / df_pcie_sum['pcitosiw']
                df_pcie_sum['pcipcw2'] = df_pcie_sum['pcipcw2'] * 100 / df_pcie_sum['pcitosiw']
                df_pcie_sum['pcipcw3'] = df_pcie_sum['pcipcw3'] * 100 / df_pcie_sum['pcitosiw']
                df_pcie_sum['pcipcw4'] = df_pcie_sum['pcipcw4'] * 100 / df_pcie_sum['pcitosiw']
                df_pcie_sum['pcipcw5'] = df_pcie_sum['pcipcw5'] * 100 / df_pcie_sum['pcitosiw']
                df_pcie_sum['pcipcw6'] = df_pcie_sum['pcipcw6'] * 100 / df_pcie_sum['pcitosiw']
                df_pcie_sum['pcipcw7'] = df_pcie_sum['pcipcw7'] * 100 / df_pcie_sum['pcitosiw']
                df_pcie_sum['pcipcw8'] = df_pcie_sum['pcipcw8'] * 100 / df_pcie_sum['pcitosiw']
                df_pcie_sum['pcipcw9'] = df_pcie_sum['pcipcw9'] * 100 / df_pcie_sum['pcitosiw']
                df_pcie_sum['pcipcw10'] = df_pcie_sum['pcipcw10'] * 100 / df_pcie_sum['pcitosiw']
            result = df_upsert(db_driver, db_engines[summary_engine[summary_level]], db_session,
                               df_pcie_sum.reset_index(),
                               summary_tblname[summary_level]['pcie'], summary_class[summary_level]['pcie'], 'smf74',
                               [col.name for col in summary_class[summary_level]['pcie'].__table__.primary_key.columns.values()],
                               int_dtypedict['pcie'], shard_id=summary_engine[summary_level]
                              )
        return result

    def sum_up_pro():
        result = 0
        df_pro_list = []
        pro_stmt = select(Smf74Pro).where(Smf74Pro.datetime.between(start, end))
        for part in partitions_range:
            df_pro = pd.read_sql(pro_stmt, db_engines[f'74.{part}'])
            if not df_pro.empty:
                df_pro['date'] = df_pro['datetime'].dt.date
                df_pro_list.append(df_pro)
        if len(df_pro_list) > 0:
            df_pros = pd.concat(df_pro_list)
            df_pros['speed_boost'] = df_pros['smf74fla'].apply(
                lambda x: is_bit_set(x, 16, 10) if pd.notna(x) else np.nan)
            df_pros['ziip_boost'] = df_pros['smf74fla'].apply(
                lambda x: is_bit_set(x, 16, 9) if pd.notna(x) else np.nan)
            df_pro_sum = df_pros.groupby(
                [col.name for col in
                 summary_class[summary_level]['pro'].__table__.primary_key.columns.values()]).agg(
                agg_dict['pro']).copy().reset_index()
            if 'date' not in df_pro_sum.columns:
                df_pro_sum['date'] = df_pro_sum['datetime'].dt.date
            df_pro_sum['last_update_time'] = current_time
            df_pro_sum[['speed_boost', 'speed_boost_change']] = pd.DataFrame(df_pro_sum['speed_boost'].tolist(),
                                                                             index=df_pro_sum.index)
            df_pro_sum[['ziip_boost', 'ziip_boost_change']] = pd.DataFrame(df_pro_sum['ziip_boost'].tolist(),
                                                                           index=df_pro_sum.index)
            result = df_upsert(db_driver, db_engines[summary_engine[summary_level]], db_session,
                               df_pro_sum[summary_class[summary_level]['pro'].__table__.columns.keys()],
                               summary_tblname[summary_level]['pro'],
                               summary_class[summary_level]['pro'], 'smf74',
                               [col.name for col in
                                summary_class[summary_level][
                                    'pro'].__table__.primary_key.columns.values()],
                               int_dtypedict['pro'], shard_id=summary_engine[summary_level]
                               )
        return result

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

    insert_dict = {'pro': 0, 'dctl': 0, 'dev': 0, 'xctl': 0, 'sys': 0, 'path': 0, 'mbr': 0, 'omvs': 0,
                   'cf': 0, 'proc': 0, 'str': 0, 'lcf': 0, 'sreq': 0, 'cach': 0, 'cfrf': 0, 'subchpa': 0, 'dupchpa': 0,
                   'mscm': 0, 'adup': 0, 'cachsys': 0, 'cdev': 0, 'raid': 0, 'rrank': 0, 'xpool': 0,
                   'hfs': 0, 'gbuf': 0, 'fsys': 0, 'fcd': 0, 'switch': 0, 'port': 0, 'connector': 0,
                   'cntl': 0, 'lss': 0, 'extp': 0, 'rank': 0, 'arry': 0, 'siol': 0,
                   'pcie': 0, 'srtd': 0, 'scm': 0, 'eadm': 0, }
    summary_class = {'hourly': tbls_hr, 'daily': tbls_da}
    summary_tblname = {'hourly': tblnames_hr, 'daily': tblnames_da}
    summary_engine = {'hourly': '74.hourly', 'daily': '74.daily'}

    result_list = []

    st = time.time()
    current_time = dt.datetime.now()

    # sum up hr and da tables
    tbls_list = insert_dict.copy().keys()
    for tbl in tbls_list:
        if tbl == 'pro':
            insert_dict['pro'] = sum_up_pro()
        elif tbl == 'dev':
            insert_dict['dev'] = sum_up_dev()
        elif tbl == 'cf':
            insert_dict['cf'] = sum_up_cf()
        elif tbl == 'pcie':
            insert_dict['pcie'] = sum_up_pcie()
        else:
            insert_dict[tbl] = sum_up_by_partition(tbls[tbl], summary_class[summary_level][tbl],
                                                   summary_tblname[summary_level][tbl],
                                                   start, end, current_time, agg_dict[tbl], int_dtypedict[tbl],
                                                   partitions_scheme, summary_engine[summary_level],
                                                   db_engines, '74', 'smf74', db_session, db_driver)

    result_list.append({summary_tblname[summary_level][k]:v for k,v in insert_dict.items() if k in summary_tblname[summary_level].keys()})

    et = time.time()  # get the end time
    # get the execution time
    elapsed_time = (et - st) / 60
    print(f'Execution time ({summary_level}):', elapsed_time, 'minutes')

    overall_et = time.time()
    overall_elapsed_time = (overall_et - overall_st) / 60
    return UploadResult(result_list, overall_elapsed_time, SUCCESS)

