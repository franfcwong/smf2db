import datetime as dt
from typing import Optional

import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.ext.declarative import AbstractConcreteBase


class ReprMixin(object):
    """A mixin to implement a generic __repr__ method"""

    def as_dict(self):
        """return instance as a dictionary"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return '<%s(%s)>' % (self.__class__.__name__,
                             ', '.join([f'{c.name} = {getattr(self, c.name)}' for c in self.__table__.primary_key]))


convention = {
    'all_column_names': lambda constraint, table: '_'.join(
        [column.name for column in constraint.columns.values()]
    ),
    'ix': 'ix__%(table_name)s__%(all_column_names)s',
    'uq': 'uq__%(table_name)s__%(all_column_names)s',
    'ck': 'ck__%(table_name)s__%(constraint_name)s',
    'fk': 'fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s',
    'pk': 'pk__%(table_name)s',
}


class Base(so.DeclarativeBase):
    pass


class Base1102(Base):
    __abstract__ = True
    metadata = sa.MetaData(schema='smf110', naming_convention=convention)


class Base1102Hr(Base):
    __abstract__ = True
    metadata = sa.MetaData(schema='smf110', naming_convention=convention)


class Base1102Da(Base):
    __abstract__ = True
    metadata = sa.MetaData(schema='smf110', naming_convention=convention)


class DfhwbgdsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhwbgds - Web Urimap Global stats record."""

    wbgds_len: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Web Urimap stats record length.")
    wbgds_id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Web Urimap stats id.")
    wbgds_vers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Web Urimap stats version.")
    wbg_urimap_reference_count: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Urimap reference count.")
    wbg_urimap_match_disabled: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                           doc="Urimap host/path match disabled.")
    wbg_urimap_no_match_count: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Urimap host/path no match.")
    wbg_urimap_match_count: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Urimap host/path match.")
    wbg_urimap_match_redirect: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                           doc="Urimap host/path match redirect.")
    wbg_urimap_match_analyzer: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                           doc="Urimap host/path match analyzer.")
    wbg_urimap_static_content: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Urimap static content.")
    wbg_urimap_dynamic_content: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Urimap dynamic content.")
    wbg_urimap_pipeline_reqs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Urimap pipeline requests.")
    wbg_urimap_scheme_http: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Urimap scheme(http) requests.")
    wbg_urimap_scheme_https: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                         doc="Urimap scheme(https) requests.")
    wbg_host_disabled_count: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Host disabled count.")
    wbg_urimap_atomserv_reqs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                          doc="Urimap atomservice requests.")
    wbg_urimap_jvmserver_reqs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Urimap JVMServer requests.")
    wbg_urimap_entrypoint_ref: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                           doc="Urimap entrypoint ref count.")
    wbg_urimap_direct_attach: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                          doc="Urimap direct user tran att.")
    wbg_urimap_scheme_jms: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Urimap scheme(jms) request.")
    wbg_urimap_scheme_iiop: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Urimap scheme(iiop) request.")


class DfhisrdsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhisrds - IPCONN Resid stats record."""

    isrds_len: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="IPCONN stats record length.")
    isrds_id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="IPCONN stats id.")
    isrds_vers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="IPCONN stats version.")
    isr_applid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="IPCONN applid.")
    isr_network_id: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="IPCONN network id.")
    isr_host_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(116), doc="IPCONN Host name.")
    isr_port_number: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="IPCONN port number.")
    isr_ssl_support: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="IPCONN SSL Support.")
    isr_userauth: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="IPCONN Userauth.")
    isr_linkauth: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="IPCONN Linkauth.")
    isr_mirrorlife: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="IPCONN Mirrorlife.")
    isr_tcpip_service: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="IPCONN Tcpip service.")
    isr_fs_ts_requests: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="FS Temporary Storage (TS) reqs.")
    isr_fs_ts_bytes_sent: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="FS TS reqs bytes sent.")
    isr_fs_ts_bytes_received: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                          doc="FS TS reqs bytes received.")
    isr_ipconn_gmt_create_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                                    doc="AI IPCONN create time - GMT.")
    isr_ipconn_create_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                                doc="AI IPCONN create time - Local.")
    isr_ipconn_gmt_delete_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                                    doc="AI IPCONN delete time - GMT.")
    isr_ipconn_delete_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                                doc="AI IPCONN delete time - Local.")
    isr_send_sessions: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Send sessions.")
    isr_current_send_sessions: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current send sessions.")
    isr_peak_send_sessions: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak send sessions.")
    isr_receive_sessions: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Receive sessions.")
    isr_current_receive_sessions: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                              doc="Current receive sessions.")
    isr_peak_receive_sessions: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak receive sessions.")
    isr_tr_requests: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Transaction Routing (TR) reqs.")
    isr_tr_bytes_sent: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="TR reqs bytes sent.")
    isr_tr_bytes_received: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="TR reqs bytes received.")
    isr_total_allocates: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="IPCONN total allocates.")
    isr_current_queued_allocates: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                              doc="Current queueed allocates.")
    isr_peak_queued_allocates: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak queued allocates.")
    isr_allocates_failed_link: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Failed allocates - Link.")
    isr_allocates_failed_other: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Failed allocates - Other.")
    isr_fs_td_requests: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="FS Transient Data (TD) reqs.")
    isr_fs_td_bytes_sent: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="FS TD reqs bytes sent.")
    isr_fs_td_bytes_received: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                          doc="FS TD reqs bytes received.")
    isr_allocate_queue_limit: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Allocate queuelimit.")
    isr_qlimit_alloc_rejects: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                          doc="Queuelimit allocate rejects.")
    isr_max_queue_time: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Max queue time.")
    isr_maxqtime_alloc_qpurges: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                            doc="Maxqtime allocate qpurges.")
    isr_maxqtime_allocs_purged: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                            doc="Maxqtime allocates purged.")
    isr_xisque_alloc_rejects: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Xisque allocate rejects.")
    isr_xisque_alloc_qpurges: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Xisque allocate qpurges.")
    isr_xisque_allocs_purged: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Xisque allocates purged.")
    isr_trans_attached: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. transactions attached.")
    isr_remote_term_starts: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Remote terminal starts.")
    isr_unsupported_requests: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Unsupported requests.")
    isr_fs_pg_requests: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Function Shipped Program reqs.")
    isr_fs_pg_bytes_sent: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="FS Program reqs bytes sent.")
    isr_fs_pg_bytes_received: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                          doc="FS Program reqs bytes received.")
    isr_fs_ic_requests: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="FS Interval Control (IC) reqs.")
    isr_fs_ic_bytes_sent: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="FS IC reqs bytes sent.")
    isr_fs_ic_bytes_received: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                          doc="FS IC reqs bytes received.")
    isr_ipconn_ip_address: so.Mapped[Optional[str]] = so.mapped_column(sa.String(39), doc="IP Resolved Address.")
    isr_ipconn_ip_family: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="IP Family.")
    isr_ipconn_define_source: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Group installed from.")
    isr_ipconn_change_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Change/create time.")
    isr_ipconn_change_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Change userid.")
    isr_ipconn_change_agent: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Change agent.")
    isr_ipconn_install_agent: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Install agent.")
    isr_ipconn_install_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                                 doc="Install/Create time.")
    isr_ipconn_install_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Install userid.")
    isr_fs_fc_requests: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="FS File Control (FC) reqs.")
    isr_fs_fc_bytes_sent: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="FS FC reqs bytes sent.")
    isr_fs_fc_bytes_received: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                          doc="FS FC reqs bytes received.")


class DfhxmrdsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhxmrds - Transaction Manager Domain Transaction Statistics DSECT."""

    xmrlen: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length of data area.")
    xmrid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Transaction Statistics id.")
    xmrdvers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Stats version number.")
    xmrpn: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Program name.")
    xmrtcl: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Tclass name.")
    xmrrnam: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Remote transid.")
    xmrrsys: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="Remote sysid.")
    xmrprty: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Transaction priority.")
    xmrdyn: so.Mapped[Optional[str]] = so.mapped_column(sa.String(1), doc="Dynamic indicator.")
    xmr_otel_prop_status: so.Mapped[Optional[str]] = so.mapped_column(sa.String(1), doc="OTEL prop init indicator.")
    xmrac: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Attach count.")
    xmrrc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Restart count.")
    xmrdlc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                        doc="Dynamic local count (the number of times the transaction routing exit decided to run this transaction locally).")
    xmrdrc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                        doc="Dynamic remote count (the number of times the transaction routing exit decided to run this transaction remotely).")
    xmrrsc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Remote start count.")
    xmrsvc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Storage Violation Count.")
    xmritov: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Indoubt timeout value (in minutes).")
    xmriwtop: so.Mapped[Optional[str]] = so.mapped_column(sa.String(1), doc="IndoubtWait option.")
    xmriactn: so.Mapped[Optional[str]] = so.mapped_column(sa.String(1), doc="Indoubt action (commit or backout).")
    xmr_tran_entrypoint: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Application Entry Point.")
    xmr_otel_emit_status: so.Mapped[Optional[str]] = so.mapped_column(sa.String(1), doc="OTEL emit indicator.")
    xmriwait: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of indoubt waits.")
    xmrfatxn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Forced action due to trandef.")
    xmrfait: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Forced action due to indoubt timeout.")
    xmrfanw: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Forced action due to no wait ability.")
    xmrfaop: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Forced action due to operator.")
    xmrfaot: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Forced action due to other.")
    xmramism: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of Action mismatches.")
    xmraendc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Abend count.")
    xmr_purged_trncls_threshold: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                             doc="Purge at threshold count.")
    xmr_otel_prop_count: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Propagated OTELs.")
    xmr_tran_define_source: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Group installed from.")
    xmr_tran_change_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Change/create time.")
    xmr_tran_change_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Change userid.")
    xmr_tran_change_agent: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Change agent.")
    xmr_tran_install_agent: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Install agent.")
    xmr_tran_install_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Install/Create time.")
    xmr_tran_install_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Install userid.")


class DfhmlrdsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhmlrds - Xmltransform Resid stats record."""

    mlrds_len: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Xmltransform stats record length.")
    mlrds_id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Xmltransform stats id.")
    mlrds_vers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Xmltransform stats version.")
    mlr_msg_validation: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Xmltransform msg validation.")
    mlr_xsdbind_file: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), doc="XML binding file.")
    mlr_xmlschema_file: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), doc="XML schema file.")
    mlr_xmltrnfm_use_count: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Xmltransform use count.")
    mlr_xmltrnfm_define_source: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Group installed from.")
    mlr_xmltrnfm_change_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                                  doc="Change/create time.")
    mlr_xmltrnfm_change_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Change userid.")
    mlr_xmltrnfm_change_agent: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Change agent.")
    mlr_xmltrnfm_install_agent: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Install agent.")
    mlr_xmltrnfm_install_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                                   doc="Install/Create time.")
    mlr_xmltrnfm_install_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Install userid.")


class DfhmqrdsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhmqrds - MQMONITOR statistics."""

    mqrlen: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length of record.")
    mqrid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Record id field.")
    mqrdvers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Version number.")
    mqr_tranid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="Monitor tranid.")
    mqr_tasknum: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Monitor task number.")
    mqr_monuserid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Monitor userid.")
    mqr_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Userid.")
    mqr_monstatus: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Monitor status.")
    mqr_topen: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of OPEN.")
    mqr_tclose: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of CLOSE.")
    mqr_tget: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of GET.")
    mqr_tgetwait: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of GETWAIT.")
    mqr_tput: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of PUT.")
    mqr_tput1: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of PUT1.")
    mqr_tinq: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of INQ.")
    mqr_tinql: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of INQL.")
    mqr_tset: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of SET.")
    mqr_tcommuow: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of Committed UOWs.")
    mqr_tbackuow: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of Backout UOWs.")
    mqr_tother: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of other calls.")
    mqr_start_time_gmt: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="start time (GMT).")
    mqr_start_time_local: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="start time (local).")
    mqr_stop_time_gmt: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="stop time (GMT).")
    mqr_stop_time_local: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="stop time (local).")
    mqr_mqmon_define_source: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Group installed from.")
    mqr_mqmon_change_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Change/create time.")
    mqr_mqmon_change_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Change userid.")
    mqr_mqmon_change_agent: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Change agent.")
    mqr_mqmon_install_agent: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Install agent.")
    mqr_mqmon_install_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Install/Create time.")
    mqr_mqmon_install_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Install userid.")


class DfhmqgdsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhmqgds - MQCONN statistics."""

    mqglen: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length of record.")
    mqgid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Record id field.")
    mqgdvers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Version number.")
    mqg_mq_release: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="Release of MQ vvrr.")
    mqg_connection_status: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Connection status.")
    mqg_resyncmember: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Resyncmember setting.")
    mqg_initiation_queue: so.Mapped[Optional[str]] = so.mapped_column(sa.String(48), doc="Initiation queue name.")
    mqg_ttasks: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of current tasks.")
    mqg_tfutileatt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of futile attempts.")
    mqg_tapi: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of calls.")
    mqg_tapiok: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of calls comp ok.")
    mqg_tcall: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of flows.")
    mqg_tcallsynccomp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of calls comp sync.")
    mqg_tcallio: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of calls need I/O.")
    mqg_twaitmsg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of real GETWAIT.")
    mqg_tsubtasked: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of calls switched.")
    mqg_topen: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of OPEN.")
    mqg_tclose: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of CLOSE.")
    mqg_tget: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of GET.")
    mqg_tgetwait: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of GETWAIT.")
    mqg_tput: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of PUT.")
    mqg_tput1: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of PUT1.")
    mqg_tinq: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of INQ.")
    mqg_tset: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of SET.")
    mqg_indoubtuow: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of indoubt units of work.")
    mqg_unresolveduow: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of unresolved units of work.")
    mqg_resolvecomm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of resolved committed UOWs.")
    mqg_resolveback: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of resolved backout UOWs.")
    mqg_tbackuow: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of Backout UOWs.")
    mqg_tcommuow: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of Committed UOWs.")
    mqg_ttaskend: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of tasks.")
    mqg_tspcomm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of Single Phase Comms.")
    mqg_t2pcomm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of 2 Phase Comms.")
    mqg_tcb: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of CB.")
    mqg_tconsume: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of msgs consumed.")
    mqg_tctl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of CTL.")
    mqg_tsub: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of SUB.")
    mqg_tsubrq: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of SUBRQ.")
    mqg_tstat: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of STAT.")
    mqg_tcrtmh: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of CRTMH.")
    mqg_tdltmh: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of DLTMH.")
    mqg_tsetmp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of SETMP.")
    mqg_tinqmp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of INQMP.")
    mqg_tdltmp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of DLTMP.")
    mqg_tmhbuf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of MHBUF.")
    mqg_tbufmh: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of BUFMH.")
    mqg_mqconn_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="name of the MQCONN.")
    mqg_mqname: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="MQNAME from the MQCONN.")
    mqg_connect_time_gmt: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="connect time (GMT).")
    mqg_connect_time_local: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                                doc="connect time (local).")
    mqg_disconnect_time_gmt: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                                 doc="disconnect time (GMT).")
    mqg_disconnect_time_local: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                                   doc="discconnect time (local).")
    mqg_mqconn_define_source: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Group installed from.")
    mqg_mqconn_change_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Change/create time.")
    mqg_mqconn_change_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Change userid.")
    mqg_mqconn_change_agent: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Change agent.")
    mqg_mqconn_install_agent: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Install agent.")
    mqg_mqconn_install_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                                 doc="Install/Create time.")
    mqg_mqconn_install_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Install userid.")


class DfhpgrdsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhpgrds - Jvmprogram Resid stats record."""

    pgrds_len: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Jvmprogram stats record length.")
    pgrds_id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Jvmprogram stats id.")
    pgrds_vers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Jvmprogram stats version.")
    pgr_jvmprogram_entrypoint: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Application Entry Point.")
    pgr_jvmprogram_usecount: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Jvmprogram Use count.")
    pgr_jvmprogram_exec_key: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Jvmprogram CICS/USER key.")
    pgr_jvmprogram_jvmclass: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255),
                                                                         doc="Jvmprogram Jvmclass name.")
    pgr_jvmprogram_server: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Jvmserver Name.")


class Dfha16dsBase(AbstractConcreteBase):
    """Abstract class for structure Dfha16ds - Table manager statistics (GLOBAL)."""

    a16len: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length of data area.")
    a16id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Table manager id.")
    a16dvers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Statistics version number.")


class DfhldbdsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhldbds - Loader Library Resid stats record."""

    ldbds_len: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Loader Library stats record length.")
    ldbds_id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Loader Library stats id.")
    ldbds_vers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Loader Library stats version.")
    ldb_library_search_pos: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Library search position.")
    ldb_library_ranking: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Library ranking.")
    ldb_library_critical: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Library critical.")
    ldb_library_enable_status: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Library enable status.")
    ldb_library_prog_loads: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Library program loads.")
    ldb_library_define_source: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Group installed from.")
    ldb_library_change_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Change/create time.")
    ldb_library_change_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Change userid.")
    ldb_library_change_agent: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Change agent.")
    ldb_library_install_agent: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Install agent.")
    ldb_library_install_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                                  doc="Install/Create time.")
    ldb_library_install_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Install userid.")
    ldb_library_numdsnames: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Library number dsnames.")


class DsgtcbpBase(AbstractConcreteBase):
    """Abstract class for structure Dsgtcbp - TCB Pool Stats."""

    dsgmxtcb: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Max number of TCBs.")
    dsgcnuat: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current TCBs attached.")
    dsgpnuat: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak TCBs attached.")
    dsgcnuus: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current TCBs in use.")
    dsgpnuus: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak TCBs in use.")
    dsgntcbl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. times at TCB Pool Limit.")
    dsgtotwl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Total Wait Time at TCB limit.")
    dsgcurwt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Current waiting time.")
    dsgtotnw: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of waits.")
    dsgcurnw: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current No. of tasks waiting for a TCB.")
    dsgpeanw: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak No. of tasks waiting for a TCB.")
    dsgmmwts: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total No. of TCB Mismatch waits.")
    dsgmmwtm: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Total TCB Mismatch wait time.")
    dsgcmmws: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current TCB Mismatch waits.")
    dsgpmmws: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak TCB Mismatch waits.")
    dsgcmmwt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Current TCB Mismatch Waiting time.")
    dsggtcbl: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Time (GMT) pool limit reached.")
    dsgltcbl: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Time (local) pool limit reached.")


class SmsbodyBase(AbstractConcreteBase):
    """Abstract class for structure Smsbody - Storage statistics body."""

    smslocn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Location (below/above/ abovebar).")
    smsaccess: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Access.")
    smsdsaindex: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="DSA index.")
    smsdsasz: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current size of DSA.")
    smshwmdsasz: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="HWM Size of DSA.")
    smscsize: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current cushion size.")
    smsgmreq: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of Getmain reqs.")
    smsfmreq: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of Freemain reqs.")
    smsasr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of Add-subpool reqs.")
    smsdsr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of Del-subpool reqs.")
    smscriss: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Cond reqs returning insufficient stg.")
    smsucss: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Uncond reqs suspended.")
    smscss: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Curr reqs susp for storage.")
    smshwmss: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="HWM reqs susp for storage.")
    smspwws: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of tasks purged, waiting storage.")
    smscrel: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of cushion releases.")
    smssos: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Times SOS occurred.")
    smstsos: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Total time SOS.")
    smscsubp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current Number of subpools.")
    smsfstg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Free storage (inc cushion).")
    smshwmfstg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="HWM free storage (inc cushion).")
    smslwmfstg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="LWM free storage (inc cushion).")
    smslfa: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Largest free area in DSA.")
    smssv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of of storage violations.")
    smsexts: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current number of extents.")
    smsextsa: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of extents added.")
    smsextsr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of extents released.")


class Dfha24dsBase(AbstractConcreteBase):
    """Abstract class for structure Dfha24ds - FEPI target statistics."""

    a24len: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length of data area.")
    a24id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="FEPI target id.")
    a24dvers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Target statistics version number.")
    a24pool: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Pool name.")
    a24appl: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Applid.")
    a24ndct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="# nodes.")
    a24alloc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="# conversation allocates.")
    a24totwt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total # allocates waited.")
    a24wait: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current # allocates waiting.")
    a24pkwt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak # allocates waiting.")
    a24tiout: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="# allocates that timed out.")


class Dfha23dsBase(AbstractConcreteBase):
    """Abstract class for structure Dfha23ds - FEPI connection statistics."""

    a23len: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length of data area.")
    a23id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="FEPI connection id.")
    a23dvers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Connection statistics version number.")
    a23targ: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Target name.")
    a23node: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Node name.")
    a23acq: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="# acquires for connection.")
    a23cnv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="# conversations.")
    a23usi: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="# unsolicited inputs received.")
    a23chout: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="# characters sent on connection.")
    a23chin: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="# characters received on connection.")
    a23rtout: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="# receive timeouts.")
    a23error: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="# error conditions.")


class DfhtqgdsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhtqgds - Transient data statistics (GLOBAL)."""

    tqglen: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length of data area.")
    tqgid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Transient data id.")
    tqgdvers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Statistics version number.")
    tqganbfa: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of Buffers.")
    tqgamxiu: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak containing valid data.")
    tqgatnal: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Times buffer accessed.")
    tqgamxal: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak concurrent access.")
    tqgatnwt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Times buffer wait occured.")
    tqgamxwt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak buffer waits.")
    tqgacisz: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Control interval size.")
    tqgancis: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. of control intervals.")
    tqgamxci: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak No. Control intervals used.")
    tqganosp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Times NOSPACE occurred.")
    tqgactpt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. of writes to dataset.")
    tqgactgt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. of reads from dataset.")
    tqgactft: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. formatting writes.")
    tqgactio: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. of I/O errors.")
    tqgsnsta: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of strings.")
    tqgstnal: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Times string accessed.")
    tqgsmxal: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak concurrent accesses.")
    tqgstnwt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Times string wait occurred.")
    tqgsmxwt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak string waits.")
    tqgacnal: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current concurrent buffer access.")
    tqgacnwt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current buffer waits.")
    tqgacniu: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current buffers containing valid data.")
    tqgscnal: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current concurrent string access.")
    tqgscnwt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current string waits.")
    tqgactci: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. of Control intervals in use.")


class DfhwbrdsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhwbrds - Web Urimap Resid stats record."""

    wbrds_len: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Web Urimap stats record length.")
    wbrds_id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Web Urimap stats id.")
    wbrds_vers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Web Urimap stats version.")
    wbr_urimap_usage: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Urimap usage.")
    wbr_urimap_scheme: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Urimap scheme.")
    wbr_urimap_analyzer_use: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Urimap analyzer program use.")
    wbr_urimap_redirect_type: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Urimap redirection type.")
    wbr_urimap_authenticate: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Urimap authenticate.")
    wbr_urimap_attls: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Urimap attls.")
    wbr_urimap_entrypoint: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Urimap app entry point.")
    wbr_urimap_hostname: so.Mapped[Optional[str]] = so.mapped_column(sa.String(116), doc="Urimap hostname.")
    wbr_urimap_port: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Urimap port.")
    wbr_urimap_path: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), doc="Urimap path.")
    wbr_urimap_templatename: so.Mapped[Optional[str]] = so.mapped_column(sa.String(48), doc="Urimap templatename.")
    wbr_urimap_hfsfile: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), doc="Urimap hfsfile.")
    wbr_urimap_location: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), doc="Urimap location.")
    wbr_urimap_trans_id: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="Urimap transaction id.")
    wbr_urimap_tcpipservice: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Urimap tcpipservice name.")
    wbr_urimap_converter: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Urimap converter name.")
    wbr_urimap_program_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Urimap program name.")
    wbr_urimap_webservice: so.Mapped[Optional[str]] = so.mapped_column(sa.String(32), doc="Urimap webservice name.")
    wbr_urimap_pipeline: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Urimap pipeline name.")
    wbr_urimap_atomservice: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Urimap atomservice name.")
    wbr_urimap_reference_count: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Urimap reference count.")
    wbr_urimap_match_disabled: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                           doc="Urimap host/path match disabled.")
    wbr_urimap_match_redirect: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                           doc="Urimap host/path match redirect.")
    wbr_urimap_socketclose: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Timeout value.")
    wbr_urimap_sockpoolsize: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Curr no. in pool.")
    wbr_urimap_sockpoolsize_peak: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak in pool.")
    wbr_urimap_sockets_reclaimed: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                              doc="Reclaimed from the pool.")
    wbr_urimap_sockets_timedout: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Timedout while in pool.")
    wbr_urimap_ip_address: so.Mapped[Optional[str]] = so.mapped_column(sa.String(39), doc="Urimap IP Address.")
    wbr_urimap_ip_family: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Urimap IP Family.")
    wbr_urimap_define_source: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Group installed from.")
    wbr_urimap_change_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Change/create time.")
    wbr_urimap_change_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Change userid.")
    wbr_urimap_change_agent: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Change agent.")
    wbr_urimap_install_agent: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Install agent.")
    wbr_urimap_install_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                                 doc="Install/Create time.")
    wbr_urimap_install_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Install userid.")


class Dfhcfs6dBase(AbstractConcreteBase):
    """Abstract class for structure Dfhcfs6d - , CF list structure statistics record."""

    s6len: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length of data area.")
    s6id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="List structure stats id.")
    s6dvers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="List structure stats version number.")
    s6pref: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="First part of structure name.")
    s6cnpref: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Prefix for connection name.")
    s6cnsysn: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Own MVS system name from CVTSNAME.")
    s6size: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Structure size in 4K pages.")
    s6sizemx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Maximum size in 4K pages.")
    s6hdrs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Maximum number of list headers.")
    s6hdrsct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Headers used for control lists.")
    s6hdrstd: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Headers available for table data.")
    s6elemln: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Data element size as a fullword.")
    s6elempw: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Data element size as power of 2.")
    s6elempe: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Max elements per entry (for 32K).")
    s6elemrt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Element side of entry:element ratio.")
    s6entrrt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Entry side of entry:element ratio.")
    s6entrct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current number of entries in use.")
    s6entrhi: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Highest number of entries in use.")
    s6entrlo: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Lowest number of free entries.")
    s6entrmx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Max entries returned by IXLCONN.")
    s6elemct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current number of elements in use.")
    s6elemhi: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Highest number of elements in use.")
    s6elemlo: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Lowest number of free elements.")
    s6elemmx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Max elements returned by IXLCONN.")
    s6usedct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of entries on used list.")
    s6usedhi: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Highest entries on used list.")
    s6freect: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of entries on free list.")
    s6freehi: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Highest entries on free list.")
    s6indxct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of entries in table index.")
    s6indxhi: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Highest entries in table index.")
    s6applct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of entries in APPLID list.")
    s6applhi: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Highest entries in APPLID list.")
    s6uowlct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of entries in UOW list.")
    s6uowlhi: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Highest entries in UOW list.")
    s6rdict: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Read table index entry.")
    s6wrict: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Write table index entry.")
    s6rwict: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Rewrite table index entry.")
    s6dlict: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Delete table index entry.")
    s6crlct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Create list.")
    s6mdlct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Modify list.")
    s6dllct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Delete list (1 per overall delete).")
    s6rddct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Read data item.")
    s6wrdct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Write data item.")
    s6rwdct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Rewrite data item.")
    s6dldct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Delete data item.")
    s6inlct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Inquire on data list.")
    s6rdmct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Read message queue.")
    s6wrmct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Write to message queue.")
    s6rduct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Read UOW entry.")
    s6wruct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Write UOW entry.")
    s6rwuct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Rewrite UOW entry.")
    s6dluct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Delete UOW entry.")
    s6rdact: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Read APPLID entry.")
    s6wract: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Write APPLID entry.")
    s6rwact: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Rewrite APPLID entry.")
    s6dlact: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Delete APPLID entry.")
    s6rrlct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Reread entry for full data length.")
    s6asyct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of asynchronous requests.")
    s6rsp1ct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Normal response, everything OK.")
    s6rsp2ct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Buffer length was too short for the data, needs full length reread.")
    s6rsp3ct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="No matching entry was found, indicates table not found in index or record not found in table.")
    s6rsp4ct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Entry version did not match, indicates entry updated by another system or duplicate entry exists when attempting to create entry.")
    s6rsp5ct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="List authority comparison mismatch, caused by table status update.")
    s6rsp6ct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Maximum list key reached, indicates max table size or max tables reached depending on list.")
    s6rsp7ct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="The list structure is out of space.")
    s6rsp8ct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="An IXLLIST return code occurred other than those described above.")
    s6rsp9ct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Structure temporarily unavailable, for example during rebuild.")


class Dfhcfs7dBase(AbstractConcreteBase):
    """Abstract class for structure Dfhcfs7d - , CF table access statistics record."""

    s7len: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length of data area.")
    s7id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Table access stats id.")
    s7dvers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Table access stats version number.")
    s7ocopen: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Open table.")
    s7occlos: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Close table.")
    s7ocset: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Set table attributes.")
    s7ocdele: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Delete table.")
    s7ocstat: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Extract table statistics.")
    s7rqpoin: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Point.")
    s7rqhigh: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Return highest key.")
    s7rqread: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Read (including read for update).")
    s7rqrddl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Read and delete.")
    s7rqunlk: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Unlock.")
    s7rqload: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Load.")
    s7rqwrit: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Write (new record).")
    s7rqrewr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Rewrite.")
    s7rqdele: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Delete.")
    s7rqdelm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Delete multiple.")


class Dfha22dsBase(AbstractConcreteBase):
    """Abstract class for structure Dfha22ds - FEPI pool statistics."""

    a22len: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length of data area.")
    a22id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="FEPI pool id.")
    a22dvers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Pool statistics version number.")
    a22trgct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="# targets.")
    a22ndct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="# nodes.")
    a22conct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="# connections.")
    a22conpk: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak # connections.")
    a22alloc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="# conversation allocates.")
    a22pkall: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak # concurrent allocates.")
    a22wait: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current # allocates waiting.")
    a22totwt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total # allocates waited.")
    a22pkwt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak # allocates waiting.")
    a22tiout: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="# allocates that timed out.")


class ldgglobal(AbstractConcreteBase):
    """Abstract class for structure Ldgglobal - Global statistics DSECT."""

    ldgllr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of LIBRARY load requests.")
    ldgllt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total time for all loads.")
    ldgpuses: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of program uses.")
    ldgwlr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of loader reqs waiting.")
    ldgwlrhw: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="HWM waiting loader reqs.")
    ldghwmt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Times at HWM.")
    ldgttw: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total time waiting.")
    ldgdrebs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of LIBRARY DEB rebuilds.")
    ldgwtdlr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of loader reqs that waited.")
    ldgllrro: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of LIBRARY load requests on the RO TCB.")
    ldglltro: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total time for loads on the RO TCB.")
    ldglwsou: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Load waits due to search order update.")
    ldglsort: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="LIBRARY search order update time.")
    ldglbsou: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="LIBRARY search order updates.")


class DfhpgedsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhpgeds - Programdef Resid stats record."""

    pgeds_len: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Programdef stats record length.")
    pgeds_id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Programdef stats id.")
    pgeds_vers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Programdef stats version.")
    pge_program_platform_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64), doc="Platform name.")
    pge_program_application_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64), doc="Application name.")
    pge_program_appl_major_ver: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                            doc="Application major version.")
    pge_program_appl_minor_ver: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                            doc="Application minor version.")
    pge_program_appl_micro_ver: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                            doc="Application micro version.")
    pge_program_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Program Name.")
    pge_program_type: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Program Type.")
    pge_program_exec_key: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Program CICS/USER key.")
    pge_program_data_loc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Program Data Location.")
    pge_program_execution_set: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Program Execution Set.")
    pge_program_lang_deduced: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Program Language Deduced.")
    pge_program_language: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Program Language.")
    pge_program_runtime_env: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Program Runtime Environment.")
    pge_program_concurrency: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Program Concurrency.")
    pge_program_api: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Program API.")
    pge_program_remote: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Program Remote.")
    pge_program_dynamic: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Program Dynamic.")
    pge_program_jvm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Program JVM.")
    pge_program_entrypoint: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Application Entry Point.")
    pge_program_remote_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Remote Program name.")
    pge_program_tran_id: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="Remote Transaction ID.")
    pge_program_remote_sysid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="Remote System name.")
    pge_program_jvmserver: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Program JVM server Name.")
    pge_program_define_source: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Group installed from.")
    pge_program_change_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Change/create time.")
    pge_program_change_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Change userid.")
    pge_program_change_agent: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Change agent.")
    pge_program_install_agent: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Install agent.")
    pge_program_install_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                                  doc="Install/Create time.")
    pge_program_install_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Install userid.")
    pge_program_operation_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64), doc="Operation name.")


class DfhxmgdsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhxmgds - Transaction Manager Domain Global Statistics DSECT."""

    xmglen: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length of data area.")
    xmgid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Transaction Manager domain id.")
    xmgdvers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Stats version number.")
    xmgnum: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                        doc="Number of transactions (user + system) attached.")
    xmgmxt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current MAXTASK value.")
    xmgcat: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current active user transactions.")
    xmgcqt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current queued user transactions.")
    xmgtamxt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Times at MAXTASK.")
    xmgpat: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak active user transactions.")
    xmgpqt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak queued user transactions.")
    xmgtat: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total active user transactions.")
    xmgtdt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                        doc="Total delayed user transactions note that this does not include those transactions currently queuing.")
    xmgtqtme: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total time spent waiting by transactions that had to queue for MXT but not including transactions currently queued.")
    xmgcqtme: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total time spent by transactions currently queued for MXT.")
    xmgtnum: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                         doc="Total number of transactions at the time of the last reset.")
    xmggtat: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="time last txn attached (GMT).")
    xmgltat: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="time last txn attached(local).")
    xmggsmxt: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="time MXT set (GMT).")
    xmglsmxt: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="time MXT set (local).")
    xmggamxt: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="time MXT reached (GMT).")
    xmglamxt: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="time MXT reached (local).")
    xmgatmxt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="at MXT indicator.")
    xmgotel: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="OTEL indicator.")


class DfhsmtdsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhsmtds - Task subpool statistics header."""

    smtlen: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length of data area.")
    smtid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Task subpool stats id.")
    smtdvers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Statistics version number.")
    smtntask: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. of task subpools.")


class DfhldrdsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhldrds - Loader statistics (RESID)."""

    ldrlen: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length of data area.")
    ldrid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Loader domain stats id.")
    ldrdvers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Domain data format version number.")
    ldrtu: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Times used since last reset.")
    ldrfc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Fetch count.")
    ldrft: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total time taken for all fetchs.")
    ldrtn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Times NEWCOPYed.")
    ldrpsize: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Program size.")
    ldrrpc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Times removed by program compression.")
    ldrlocn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Location of current copy.")
    ldrlbnm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Program library name.")
    ldrlbdnm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(44), doc="Program library dsname.")


class DfhtqrdsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhtqrds - Transient Data Queue statistics."""

    tqrlen: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length of data area.")
    tqrid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="TD Queue resid statistics id.")
    tqrdvers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Stats version number.")
    tqrqtype: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="TD Queue destination type.")
    tqrwrite: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total writes to queue.")
    tqrread: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total reads from queue.")
    tqrdelet: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total deletes of queue.")
    tqrtrigl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="ATI tranid trigger level.")
    tqrrtype: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Recovery type.")
    tqrftype: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="ATI facility type.")
    tqrfname: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="ATI facility name.")
    tqrwait: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Indoubt waiting supported.")
    tqrwaita: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Indoubt action (reject/ queue).")
    tqratran: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="ATI tranid.")
    tqrtrign: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of triglev triggers.")
    tqrccius: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current CI's in use by this queue.")
    tqrpcius: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak CI's in use by this queue.")
    tqrcnitm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current number of items in queue.")
    tqrrsys: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="Remote sysid.")
    tqrrqid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="Remote Queue identifier.")
    tqriqid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="Indirect Queue identifier.")
    tqriotyp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="I/O Type (input/output/ readback).")
    tqrddnm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="DD name of Extrapartition queue.")
    tqrdsnnm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(44), doc="Dataset name of Extrapartition Queue.")
    tqrpdsmn: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="PDS member name.")
    tqr_define_source: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Group installed from.")
    tqr_change_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Change/create time.")
    tqr_change_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Change userid.")
    tqr_change_agent: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Change agent.")
    tqr_install_agent: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Install agent.")
    tqr_install_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Install/Create time.")
    tqr_install_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Install userid.")
    tqrpnitm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak no. of items in queue.")


class Dfha17dsBase(AbstractConcreteBase):
    """Abstract class for structure Dfha17ds - File control statistics."""

    a17len: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length of data area.")
    a17id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="File control id.")
    a17dvers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="File stats version number.")
    a17floc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(1), doc="Set to 'R' if remote.")
    a17dt: so.Mapped[Optional[str]] = so.mapped_column(sa.String(1),
                                                       doc="Set to 'R', 'S', 'T', 'L', 'K' or 'X' if data table fields present.")
    a17dsrls: so.Mapped[Optional[str]] = so.mapped_column(sa.String(1),
                                                          doc="RLS/Non-RLS Indicator 'R' = RLS mode blank = non- RLS mode.")
    a17dsnam: so.Mapped[Optional[str]] = so.mapped_column(sa.String(44), doc="Dataset name.")
    a17dsrd: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="GET requests.")
    a17dsgu: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="GET update requests.")
    a17dsbr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="BROWSE requests.")
    a17dswra: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="ADD requests.")
    a17dswru: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="UPDATE requests.")
    a17dsdel: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="DELETE requests.")
    a17dsxcp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="VSAM EXCP requests - data.")
    a17dsixp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="VSAM EXCP requests - index.")
    a17dstsw: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Wait on string total.")
    a17dshsw: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Wait on string highest.")
    a17dttyp: so.Mapped[Optional[str]] = so.mapped_column(sa.String(1),
                                                          doc="Set to 'C', 'S', 'U', 'X', 'L' or 'K' for close.")
    a17dtrds: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Read/browse requests.")
    a17dtrnf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Source reads issued.")
    a17dtavr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="ADDs resulting from READs.")
    a17dtads: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="ADD requests.")
    a17dtarj: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="ADDs rejected by exit.")
    a17dtatf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="ADDs when table full.")
    a17dtrws: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="REWRITE requests.")
    a17dtdls: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="DELETE requests.")
    a17dtshi: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Highest table record count.")
    a17dtsiz: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current table record count.")
    a17dtalt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Storage allocated - total (KB).")
    a17dtust: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Storage in-use - total (KB).")
    a17dtale: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Storage allocated - entries (KB).")
    a17dtuse: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Storage in-use - entries (KB).")
    a17dtali: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Storage allocated - index (KB).")
    a17dtusi: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Storage in-use - index (KB).")
    a17dtald: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Storage allocated - data (KB).")
    a17dtusd: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Storage in-use - data (KB).")
    a17dtrrs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Read Retries for a SDT.")
    a17dsdnb: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No Buffers - Data.")
    a17dsinb: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No Buffers - Index.")
    a17pool: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="LSRPOOL Id.")
    a17strno: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No Strings.")
    a17rname: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Remote Name.")
    a17rsys: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="Remote Sysid.")
    a17dstyp: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="Dataset Type.")
    a17bdsnm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(44), doc="Base Dataset Name.")
    a17dsasc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No Active Strings.")
    a17dsasw: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No String Waits.")
    a17lopnt: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="File open time (Local STCK).")
    a17lclst: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="File close time (Local STCK).")
    a17gopnt: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="File open time (GMT STCK).")
    a17gclst: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="File close time (GMT STCK).")
    a17dsbru: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Browse for update count.")
    a17rlswt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="RLS request wait timeouts.")
    a17dtcon: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of CHANGED responses for a CFDT using contention, number of lock waits for a CFDT using locking.")
    a17dtcfp: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Coupling Facility Data Table Pool Name.")
    a17dtlds: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of LOADING responses.")
    a17fcxcc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No Exclusive Control Conflicts.")
    a17_file_define_source: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Group installed from.")
    a17_file_change_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Change/create time.")
    a17_file_change_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Change userid.")
    a17_file_change_agent: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Change agent.")
    a17_file_install_agent: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Install agent.")
    a17_file_install_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Install/Create time.")
    a17_file_install_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Install userid.")


class Dfha09dsBase(AbstractConcreteBase):
    """Abstract class for structure Dfha09ds - LSRPOOL statistics (File specifics)."""

    a09len: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length of data area.")
    a09id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="LSR pool id.")
    a09dvers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Statistics version number.")
    a09srpid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="LSR pool number.")
    a09dbn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Data buffer size.")
    a09ibn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Index buffer size.")
    a09tbw: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total buffer waits.")
    a09hbw: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Highest buffer waits.")


class DfhdsrdsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhdsrds - Dispatcher Domain MVSTCB statistics."""

    dsrds_len: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="MVSTCB resource stats record length.")
    dsrds_id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Statistics record id.")
    dsrds_vers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="MVSTCB resource stats version.")
    dsrds_tcb_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Initial prog or QR, RO etc.")
    dsrds_tcb_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(1), doc="'C' for CICS, 'N' for non- CICS.")
    dsrds_tcb_cics_task: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="CICS task number or 0.")
    dsrds_tcb_mother: so.Mapped[Optional[str]] = so.mapped_column(sa.String(10), doc="Address of mother TCB.")
    dsrds_tcb_sister: so.Mapped[Optional[str]] = so.mapped_column(sa.String(10), doc="Address of sister TCB.")
    dsrds_tcb_daughter: so.Mapped[Optional[str]] = so.mapped_column(sa.String(10), doc="Address of daughter TCB.")
    dsrds_tcb_cputime: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Total CPU time so far.")
    dsrds_tcb_stg_below: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Private storage below 16M.")
    dsrds_tcb_stg_above: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Private storage above 16M.")
    dsrds_tcb_stg_below_inuse: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Below 16M in use.")
    dsrds_tcb_stg_above_inuse: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Above 16M in use.")


class DfhsdgdsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhsdgds - System Dump Global statistics."""

    sdglen: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length of data area.")
    sdgid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="System dump global stats id.")
    sdgdvers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Dump domain global stats version.")
    sys_dumps_taken: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of system dumps taken.")
    sys_dumps_suppr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of system dumps suppressed.")


class DfhdstdsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhdstds - Dispatcher Domain MVSTCB statistics."""

    dstds_len: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="MVSTCB global stats record length.")
    dstds_id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Statistics record id.")
    dstds_vers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="MVSTCB global stats version.")
    dstds_cicstcb_count: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current number of CICS TCBs.")
    dstds_cicstcb_cputime: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="So far for currently attached.")
    dstds_cicstcb_stg_below: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Private stg below 16M.")
    dstds_cicstcb_stg_above: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Private stg above 16M.")
    dstds_noncicstcb_count: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                        doc="Current number of non- CICS TCBs.")
    dstds_noncicstcb_cputime: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                            doc="So far for currently attached.")
    dstds_noncicstcb_stg_below: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Private stg below 16M.")
    dstds_noncicstcb_stg_above: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Private stg above 16M.")
    dstds_cicstcb_stg_below_inuse: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="<16M in use.")
    dstds_cicstcb_stg_above_inuse: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc=">16M in use.")
    dstds_noncicstcb_stg_below_inuse: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="<16M in use.")
    dstds_noncicstcb_stg_above_inuse: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc=">16M in use.")


class Dfha06dsBase(AbstractConcreteBase):
    """Abstract class for structure Dfha06ds - Terminal Stats DSECT (RESID & TOTAL)."""

    a06len: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length of data area.")
    a06id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Terminal stats id.")
    a06dvers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Terminal statistics version number.")
    a06tett: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="Terminal type (cf TCTTTET).")
    a06eamib: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="Access method (cf TCTEAMIB).")
    a06lenp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of polls.")
    a06teni: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Input messages.")
    a06teno: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Output messages.")
    a06teot: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of transactions.")
    a06csvc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Storage violations.")
    a06tete: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Transmission errors.")
    a06teoe: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Transaction errors.")
    a06tcnt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Pipeline messages (Total).")
    a06scnt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Pipeline messages (Groups).")
    a06mcnt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Pipeline messages (Max consec).")
    a06lunam: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="LU Name.")
    a06prty: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Terminal Priority.")
    a06stg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="TIOA Storage.")
    a06sysid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="Owning SYSID of terminal/ session.")
    a06ontm: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Autoinstall logon time (Local).")
    a06offtm: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Autoinstall logoff time (Local).")
    a06gontm: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Autoinstall logon time (GMT).")
    a06goftm: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Autoinstall logoff time (GMT).")


class Dfhw2rdsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhw2rds - Web 2.0 Domain Resid stats record."""

    w2rds_len: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Web 2.0 Domain stats record len.")
    w2rds_id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Web 2.0 Domain stats id.")
    w2rds_vers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Web 2.0 Domain stats version.")
    w2r_atomserv_type: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Atomservice type.")
    w2r_atomserv_binding_file: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255),
                                                                           doc="Atomservice binding file.")
    w2r_atomserv_config_file: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255),
                                                                          doc="Atomservice configuration file.")
    w2r_atomserv_restype: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Atomservice resource type.")
    w2r_atomserv_resname: so.Mapped[Optional[str]] = so.mapped_column(sa.String(16), doc="Atomservice resource name.")
    w2r_atomserv_ref_count: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Reference count.")
    w2r_atomserv_ref_disabled: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Reference disabled.")
    w2r_atomserv_post_feed_cnt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="POST issued for feed.")
    w2r_atomserv_get_feed_cnt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="GET issued for feed.")
    w2r_atomserv_get_entry_cnt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="GET issued for entry.")
    w2r_atomserv_put_entry_cnt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="PUT issued for entry.")
    w2r_atomserv_del_entry_cnt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="DELETE issued for entry.")
    w2r_atomserv_define_source: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Group installed from.")
    w2r_atomserv_change_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                                  doc="Change/create time.")
    w2r_atomserv_change_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Change userid.")
    w2r_atomserv_change_agent: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Change agent.")
    w2r_atomserv_install_agent: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Install agent.")
    w2r_atomserv_install_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                                   doc="Install/Create time.")
    w2r_atomserv_install_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Install userid.")
    w2r_atomserv_urimap: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="URIMAP.")
    w2r_atomserv_xmltransform: so.Mapped[Optional[str]] = so.mapped_column(sa.String(32), doc="XMLTRANSFORM.")


class NqgbodyBase(AbstractConcreteBase):
    """Abstract class for structure Nqgbody - Individual ENQ pool statistics."""

    nqgtnqsi: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total enqueues issued.")
    nqgtnqsw: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total enqueues waited.")
    nqgtnqwt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Time enqueues had waited (STCK).")
    nqgcnqsw: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current enqueues waiting.")
    nqgcnqwt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Current enqueues waiting time (STCK).")
    nqggnqsw: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total sysplex ENQs waited.")
    nqggnqwt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Time sysplex ENQs had waited (STCK).")
    nqgsnqsw: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current sysplex ENQs waiting.")
    nqgsnqwt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Current sysplex ENQs wait time (STCK).")
    nqgtnqsr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total enqueues that were retained.")
    nqgtnqrt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Time enqueues were retained (STCK).")
    nqgcnqsr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current enqueues retained.")
    nqgcnqrt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Current enqueues retained time (STCK).")
    nqgtirjb: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total immed. rejected ENQBUSY.")
    nqgtirjr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total immed. rejected ENQ retained.")
    nqgtwrjr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total waiting ENQs rejected retained.")
    nqgtwpop: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total waiting ENQs purged by operator.")
    nqgtwpto: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total waiting ENQs purged by timeout.")


class DfhsmsdsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhsmsds - Storage statistics header."""

    smslen: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length of data area.")
    smsid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="DSA storage stats id.")
    smsdvers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Statistics version number.")


class SmsglobalBase(AbstractConcreteBase):
    """Abstract class for structure Smsglobal - Storage Mgr Global Stats."""

    smsgbllen: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                           doc="Global stats length (includes the length of the standard stats header which is 8 bytes).")
    smsnpagp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of Pagepools.")
    smsstgprot: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="State of STGPROT.")
    smsrentpgm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="State of RENTPGM.")
    smstraniso: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="State of TRANISO.")
    smsmemlimitsrc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="MEMLIMIT Source.")
    smsusscur: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current number of unique subspace users.")
    smsusscum: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                           doc="Cumulative number of unique subspace users.")
    smsusshwm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="HWM of unqiue subspace users.")
    smscsscur: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current number of common subspace users.")
    smscsscum: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                           doc="Cumulative number of common subspace users.")
    smscsshwm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="HWM of common subspace users.")
    smsdsalimit: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current DSA limit.")
    smsedsalimit: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current EDSA limit.")
    smsdsatotal: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current DSA total.")
    smsedsatotal: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current EDSA total.")
    smshwmdsatotal: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="HWM DSA total.")
    smshwmedsatotal: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="HWM EDSA total.")
    smstimewaitmvs: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="total time waiting for MVS storage.")
    smsmvsstgreqwaits: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                   doc="number of requests for MVS storage causing wait.")
    smsmemlimit: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="MEMLIMIT Size.")
    smsgetstorsize: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="GETSTOR request size.")
    smsasactive: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Current Address Space addres'ble.")
    smshwmasactive: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="HWM Address Space addressable.")
    smsgdsaactive: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Current GDSA active.")
    smshwmgdsaactive: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="HWM GDSA active.")
    smsgdsaalloc: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Current GDSA allocated.")
    smshwmgdsaalloc: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="HWM GDSA allocated.")
    smslvabytes: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                             doc="Bytes Allocated to Private Memory Objects.")
    smslvhbytes: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                             doc="Bytes Hidden within Private Memory Objects.")
    smslvgbytes: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                             doc="HWM Bytes Usable within Private Memory Objects.")
    smslvnmemobj: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Number of Private Memory Objects.")
    smsfromguardfail: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Number of FROMGUARD Failures.")
    smsfromguardfailsize: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="FROMGUARD Failure Size.")
    smslvshrbytes: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                               doc="Shared Bytes from Large Memory Objects.")
    smslvshrgbytes: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                doc="HWM Shared Bytes within Large Memory Objects.")
    smslvshrnmemobj: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Number of Shared Memory Objects.")
    smshvauxslots: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                               doc="Auxiliary slots to back 64- bit Private Memory Objects.")
    smshvgauxslots: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                doc="HWM Auxiliary slots to back 64-bit Private Memory Objects.")
    smshvpagesinreal: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                  doc="Real Frames to back 64-bit Private Memory Objects.")
    smshvgpagesinreal: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                   doc="HWM Real Frames to back 64-bit Private Memory Objects.")
    smslargememobj: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Number of Large Memory Objects.")
    smslargepagesinreal: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                     doc="Number of Large Pages Backed in Real Storage.")


class DfhsdrdsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhsdrds - Dump domain system dump stats."""

    sdrlen: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length of data area.")
    sdrid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Dump domain system stats id.")
    sdrdvers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Domain data format version number.")
    sdrstkn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of system dumps taken.")
    sdrssupr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of system dumps suppressed.")
    sdrttkn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of tran dumps taken (unused).")
    sdrtsupr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of tran dumps suppressed.")


class DfhpgddsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhpgdds - Programdef Resid stats record."""

    pgdds_len: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Programdef stats record length.")
    pgdds_id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Programdef stats id.")
    pgdds_vers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Programdef stats version.")
    pgd_program_type: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Program Type.")
    pgd_program_exec_key: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Program CICS/USER key.")
    pgd_program_data_loc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Program Data Location.")
    pgd_program_execution_set: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Program Execution Set.")
    pgd_program_lang_deduced: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Program Language Deduced.")
    pgd_program_language: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Program Language.")
    pgd_program_runtime_env: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Program Runtime Environment.")
    pgd_program_concurrency: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Program Concurrency.")
    pgd_program_api: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Program API.")
    pgd_program_remote: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Program Remote.")
    pgd_program_dynamic: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Program Dynamic.")
    pgd_program_jvm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Program JVM.")
    pgd_program_entrypoint: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Application Entry Point.")
    pgd_program_remote_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Remote Program name.")
    pgd_program_tran_id: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="Remote Transaction ID.")
    pgd_program_remote_sysid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="Remote System name.")
    pgd_program_jvmserver: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Program JVM server Name.")
    pgd_program_define_source: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Group installed from.")
    pgd_program_change_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Change/create time.")
    pgd_program_change_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Change userid.")
    pgd_program_change_agent: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Change agent.")
    pgd_program_install_agent: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Install agent.")
    pgd_program_install_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                                  doc="Install/Create time.")
    pgd_program_install_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Install userid.")


class Dfha14dsBase(AbstractConcreteBase):
    """Abstract class for structure Dfha14ds - ISC/IRC statistics."""

    a14len: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length of data area.")
    a14id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="ISC/IRC id.")
    a14dvers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="ISC/IRC stats version number.")
    a14esall: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Generic AIDS in chain.")
    a14ebid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current bids.")
    a14estam: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Max outstanding allocates.")
    a14e2hwm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Max secondaries.")
    a14ebhwm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Max bids.")
    a14es1: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="ATIs satisfied by primaries.")
    a14es2: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="ATIs satisfied by secondaries.")
    a14esbid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Bids sent.")
    a14estas: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total allocates.")
    a14estaq: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Queued allocates.")
    a14estaf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Failed link allocates.")
    a14estao: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Failed - other reasons.")
    a14estfc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="File control function shipping reqs.")
    a14estic: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Intv control function shipping reqs.")
    a14esttd: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="TD function shipping reqs.")
    a14estts: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="TS function shipping reqs.")
    a14estdl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="DL/I function shipping reqs.")
    a14esttc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Terminal sharing reqs.")
    a14e1hwm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Max primaries.")
    a14eqpct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="MAXQTIME purge count.")
    a14ealrj: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Allocates rejected (QLIMIT).")
    a14emxqt: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Max queue time.")
    a14ealim: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Allocate queue limit.")
    a14ezqrj: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="XZIQUE rejects.")
    a14ezqpu: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="XZIQUE purge count.")
    a14ezqpc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="XZIQUE allocates purged.")
    a14emqpc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="MAXQTIME allocates purged.")
    a14eall: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Aids in chain.")
    a14gact: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="AI GMT conn create time.")
    a14aict: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="AI conn create time.")
    a14gadt: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="AI GMT conn delete time.")
    a14aidt: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="AI conn delete time.")
    a14eahwm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Max AIDs.")
    a14esid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Connection netname.")
    a14accm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Access method.")
    a14eflgs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Protocol.")
    a14esecn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Send session count.")
    a14eprmn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Receive session count.")
    a14e1ry: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Primaries currently used.")
    a14e2ry: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Secondaries currently used.")
    a14estpc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Program Control funct ship reqs.")
    a14estpc_channel: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Program Control FS Channel reqs.")
    a14estpc_channel_sent: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                       doc="Bytes sent PC FS Channel reqs.")
    a14estpc_channel_rcvd: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                       doc="Bytes received PC FS Channel reqs.")
    a14esttc_channel: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Terminal Sharing Channel reqs.")
    a14esttc_channel_sent: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                       doc="Bytes sent Term Sharing Channel.")
    a14esttc_channel_rcvd: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                       doc="Bytes received Term Sharing Channel.")
    a14estic_channel: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Interval Control FS Channel reqs.")
    a14estic_channel_sent: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                       doc="Bytes sent IC FS Channel reqs.")
    a14estic_channel_rcvd: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                       doc="Bytes received IC FS Channel reqs.")
    a14_define_source: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Group installed from.")
    a14_change_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Change/create time.")
    a14_change_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Change userid.")
    a14_change_agent: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Change agent.")
    a14_install_agent: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Install agent.")
    a14_install_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Install/Create time.")
    a14_install_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Install userid.")


class Dfha20dsBase(AbstractConcreteBase):
    """Abstract class for structure Dfha20ds - ISC/IRC mode entry statistics."""

    a20len: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length of data area.")
    a20id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="ISC/IRC mode entry id.")
    a20dvers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="ISC/IRC mode entry stats vers No.")
    a20estam: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Max outstanding allocates.")
    a20e2hwm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Max secondaries.")
    a20ebhwm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Max bids.")
    a20e1hwm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak contention losers.")
    a20es1: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="ATIs satisfied by primaries.")
    a20es2: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="ATIs satisfied by secondaries.")
    a20esbid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Bids sent.")
    a20estas: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total allocates.")
    a20estaq: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Queued allocates.")
    a20estaf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Failed link allocates.")
    a20estao: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Failed - other reasons.")
    a20estag: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Generic allocates.")
    a20estap: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Specific allocates.")
    a20ebid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current bids.")
    a20eqpct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="XZIQUE purge count.")
    a20ezqpc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="XZIQUE allocates purged.")
    a20elmax: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Max session count.")
    a20emcon: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Max contention winners acceptable.")
    a20emaxs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current Max session count.")
    a20econw: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current CNOS contention winners.")
    a20econl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current CNOS contention losers.")
    a20e1ry: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Primaries currently used.")
    a20e2ry: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Secondaries currently used.")


class DfhmprdsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhmprds - POLICY statistics."""

    mprlen: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length of record.")
    mprid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Record id field.")
    mprdvers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Version number.")
    mpr_policy_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64), doc="Policy resource name.")
    mpr_rule_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64), doc="Policy Rule name.")
    mpr_policy_usertag: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Policy usertag.")
    mpr_bundle_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Policy bundle name.")
    mpr_bundle_dir: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), doc="Policy bundle dir.")
    mpr_rule_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(16), doc="Rule type.")
    mpr_rule_subtype: so.Mapped[Optional[str]] = so.mapped_column(sa.String(16), doc="Rule sub type.")
    mpr_action_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(16), doc="Action type.")
    mpr_action_count: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Rule action count.")
    mpr_action_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Rule last action time.")


class A08bssdsBase(AbstractConcreteBase):
    """Abstract class for structure A08bssds - Statistics by buffer size."""

    a08bkbfn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. of buffers.")
    a08bkhbn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. of hiperspace buffers.")
    a08bkbff: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. successful look asides.")
    a08bkfrd: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. buffer reads.")
    a08bkuiw: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. user initiated buffer writes.")
    a08bknuw: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. non-user initiated buffer writes.")
    a08bkcrs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. successful CREAD.")
    a08bkcws: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. successful CWRITE.")
    a08bkcrf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. failing CREAD.")
    a08bkcwf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. failing CWRITE.")


class Dfha08dsBase(AbstractConcreteBase):
    """Abstract class for structure Dfha08ds - LSRPOOL statistics (RESID & TOTALS)."""

    a08len: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length of data area.")
    a08id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="LSR pool id.")
    a08dvers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Statistics version number.")
    a08flags: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Flags.")
    a08lbkcd: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Time pool created (Local STCK).")
    a08lbkdd: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Time pool deleted (Local STCK).")
    a08gbkcd: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Time pool created (GMT STCK).")
    a08gbkdd: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Time pool deleted (GMT STCK).")
    a08bkkyl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Max key length.")
    a08bkstn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. of strings.")
    a08bkhsw: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak reqs waiting on string.")
    a08bktsw: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total No. reqs waiting on string.")
    a08bkhas: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak No. conc active FC strings.")
    a08tobfn_data: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total no. of data buffers.")
    a08tohbn_data: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total data hiperspace buffs.")
    a08tobff_data: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total no. successful look asides.")
    a08tofrd_data: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total no. buffer reads.")
    a08touiw_data: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total no. user initiated writes.")
    a08tonuw_data: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total no. non-user initiated writes.")
    a08tocrs_data: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total no. successful CREAD.")
    a08tocws_data: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total no. successful CWRITE.")
    a08tocrf_data: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total no. failing CREAD.")
    a08tocwf_data: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total no. failing CWRITE.")
    a08tobfn_indx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total no. of index buffers.")
    a08tohbn_indx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total indx hiperspace buffs.")
    a08tobff_indx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total no. successful look asides.")
    a08tofrd_indx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total no. buffer reads.")
    a08touiw_indx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total no. user initiated writes.")
    a08tonuw_indx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total no. non-user initiated writes.")
    a08tocrs_indx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total no. successful CREAD.")
    a08tocws_indx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total no. successful CWRITE.")
    a08tocrf_indx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total no. failing CREAD.")
    a08tocwf_indx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total no. failing CWRITE.")


class DfhpirdsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhpirds - Pipeline Resid stats record."""

    pirds_len: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Pipeline stats record length.")
    pirds_id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Pipeline stats id.")
    pirds_vers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Pipeline stats version.")
    pir_pipeline_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Pipeline name.")
    pir_pipeline_mode: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Pipeline mode.")
    pir_configuration_file: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255),
                                                                        doc="Pipeline configuration file.")
    pir_shelf_directory: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), doc="Pipeline shelf directory.")
    pir_wsdir_directory: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255),
                                                                     doc="Pipeline WSDIR pickup directory.")
    pir_pipeline_use_count: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Pipeline use count.")
    pir_json_java_parser: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Pipeline JSON parser.")
    pir_pipeline_define_source: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Group installed from.")
    pir_pipeline_change_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                                  doc="Change/create time.")
    pir_pipeline_change_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Change userid.")
    pir_pipeline_change_agent: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Change agent.")
    pir_pipeline_install_agent: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Install agent.")
    pir_pipeline_install_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                                   doc="Install/Create time.")
    pir_pipeline_install_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Install userid.")
    pir_pipeline_msgformat: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Message format.")


class A16statsBase(AbstractConcreteBase):
    """Abstract class for structure A16stats - Stats for each table."""

    a16tsize: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Table size.")


class DfhtdgdsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhtdgds - Transaction Dump Global Stats."""

    tdglen: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length of data area.")
    tdgid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Dump Domain global stats id.")
    tdgdvers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Dump domain global stats version.")
    trans_dump_taken: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. of transaction dumps taken.")
    trans_dump_supp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. of transaction dumps supprsd.")


class DfhepgdsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhepgds - EP Domain Global stats record."""

    epgds_len: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="EP Domain stats record length.")
    epgds_id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="EP Domain stats id.")
    epgds_vers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="EP Domain stats version.")
    epg_put_events: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Put Events.")
    epg_commit_forward_events: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                           doc="Commit forward async events.")
    epg_commit_backward_events: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                            doc="Commit backward async events.")
    epg_current_evc_queue: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current event capture queue.")
    epg_peak_evc_queue: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak event capture queue.")
    epg_current_trans_queue: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current transactional queue.")
    epg_peak_trans_queue: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak transactional queue.")
    epg_async_normal_events: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Async normal events.")
    epg_async_priority_events: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Async priority events.")
    epg_trans_events: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Transactional events.")
    epg_trans_events_discarded: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                            doc="Transactional events disc.")
    epg_sync_events: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Synchronous events.")
    epg_sync_events_failed: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Synchronous events failed.")
    epg_dispatchers_attached: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                          doc="Number of dispatcher attaches.")
    epg_current_dispatchers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current dispatcher tasks.")
    epg_peak_dispatchers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak dispatcher tasks.")
    epg_custom_adapter_events: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                           doc="Events to Custom EP adapter.")
    epg_wmq_adapter_events: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Events to WMQ EP adapter.")
    epg_trans_adapter_events: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Events to Trans EP adapter.")
    epg_tsqueue_adapter_events: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                            doc="Events to Tsqueue adapter.")
    epg_http_adapter_events: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Events to HTTP adapter.")
    epg_tdqueue_adapter_events: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Events to Tdqueue adapt.")
    epg_dispatch_failure_config: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Events lost - config.")
    epg_dispatch_failure_other: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Events lost - other.")
    epg_adapter_failure_config: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Events lost - config.")
    epg_adapter_failure_other: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Events lost - other.")
    epg_events_adapter_unavail: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Events lost - no adapter.")


class DfheprdsBase(AbstractConcreteBase):
    """Abstract class for structure Dfheprds - EP resource stats record."""

    eprds_len: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="EP resource stats record length.")
    eprds_id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="EP resource stats id.")
    eprds_vers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="EP resource stats version.")
    epr_adapter_type: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="EP adapter type.")
    epr_emission_mode: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Events are sync or async.")
    epr_put_events: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="put_events for this adapter.")
    epr_ada_define_source: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Group installed from.")
    epr_ada_change_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Change/create time.")
    epr_ada_change_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Change userid.")
    epr_ada_change_agent: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Change agent.")
    epr_ada_install_agent: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Install agent.")
    epr_ada_install_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Install/Create time.")
    epr_ada_install_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Install userid.")


class DfhasgdsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhasgds - AS Domain Global stats record."""

    asgds_len: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="AS Domain stats record length.")
    asgds_id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="AS Domain stats id.")
    asgds_vers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="AS Domain stats version.")
    asg_run_count: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Run API count.")
    asg_fetch_count: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Fetch APIs count.")
    asg_free_count: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Free APIs count.")
    asg_run_delay_count: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of Run API being delayed.")
    asg_parents_delayed_cur: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                         doc="Count of parents being delayed.")
    asg_parents_delayed_peak: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak parents being delayed.")
    asg_children_cur: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of running children.")
    asg_children_peak: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak running children.")


class DfhdhddsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhdhdds - Doctemplate Resid stats record."""

    dhdds_len: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Doctemplate stats record length.")
    dhdds_id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Doctemplate stats id.")
    dhdds_vers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Doctemplate stats version.")
    dhd_template_type: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Doctemplate type.")
    dhd_append_crlf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Doctemplate append crlf.")
    dhd_template_contents: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Doctemplate contents.")
    dhd_template_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(48), doc="Doctemplate template name.")
    dhd_template_exit_program: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                                           doc="Template exit program name.")
    dhd_template_file_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Template file name.")
    dhd_template_program_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Template program name.")
    dhd_template_pds_member: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Template PDS member.")
    dhd_template_pds_ddname: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Template PDS ddname.")
    dhd_template_pds_dsname: so.Mapped[Optional[str]] = so.mapped_column(sa.String(44), doc="Template PDS dsname.")
    dhd_template_tdqueue_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="Template tdqueue name.")
    dhd_template_tsqueue_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(16), doc="Template tsqueue name.")
    dhd_template_hfsfile_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), doc="Template hfsfile name.")
    dhd_template_cache_size: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Template cache size.")
    dhd_template_use_count: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Template use count.")
    dhd_template_newcopies: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Template newcopy count.")
    dhd_template_read_count: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Template read count.")
    dhd_template_cache_used: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Template cache copy used.")
    dhd_template_cache_deleted: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Template cache deleted.")
    dhd_template_define_source: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Group installed from.")
    dhd_template_change_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                                  doc="Change/create time.")
    dhd_template_change_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Change userid.")
    dhd_template_change_agent: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Change agent.")
    dhd_template_install_agent: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Install agent.")
    dhd_template_install_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                                   doc="Install/Create time.")
    dhd_template_install_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Install userid.")


class Dfha03dsBase(AbstractConcreteBase):
    """Abstract class for structure Dfha03ds - VTAM statistics (Global)."""

    a03len: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length of data area.")
    a03id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="VTAM global storage id.")
    a03dvers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="VTAM stats version number.")
    a03rplxt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Times at RPL max.")
    a03rplx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Max RPLs posted.")
    a03vtsos: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="VTAM SOS.")
    a03doc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Dynamic open count.")
    a03lunum: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current LUs in session.")
    a03luhwm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="HWM LUs in session.")
    a03psic: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="PRSS inquire count.")
    a03psnc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="PRSS nib count.")
    a03psoc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="PRSS opndst count.")
    a03psuc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="PRSS unbind count.")
    a03psec: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="PRSS error count.")
    a03pstyp: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="SNPS/MNPS/NOPS - Persistency.")
    a03psdin: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="PSDINT - Format 0hhmmss.")
    a03bmvl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="BMS 3270 Validation On/Off.")
    a03bmig: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="BMS 3270 ignored count.")
    a03bmlg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="BMS 3270 logged count.")
    a03bmab: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="BMS 3270 abended count.")


class DfhsjsdsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhsjsds - JVMSERVER Resid stats record."""

    sjsds_len: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="JVMSERVER stats record length.")
    sjsds_id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="JVMSERVER stats id.")
    sjsds_vers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="JVMSERVER stats version.")
    sjs_jvmserver_jvmprofile: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="JVMSERVER JVMPROFILE.")
    sjs_jvmserver_le_runopts: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="JVMSERVER LE RUNOPTS.")
    sjs_jvmserver_use_count: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="JVMSERVER use count.")
    sjs_jvmserver_state: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="JVMSERVER state.")
    sjs_jvmserver_thread_limit: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Max no. threads.")
    sjs_jvmserver_thread_current: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current threads.")
    sjs_jvmserver_thread_hwm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak threads.")
    sjs_jvmserver_thread_waits: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. thread waits.")
    sjs_jvmserver_thread_wait_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                  doc="Total thread wait time.")
    sjs_jvmserver_thread_wait_cur: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                               doc="Current waiting threads.")
    sjs_jvmserver_thread_wait_hwm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak waiting threads.")
    sjs_jvmserver_thread_wlp_actv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                               doc="Liberty active threads.")
    sjs_jvmserver_define_source: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Group installed from.")
    sjs_jvmserver_change_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                                   doc="Change/create time.")
    sjs_jvmserver_change_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Change userid.")
    sjs_jvmserver_change_agent: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Change agent.")
    sjs_jvmserver_install_agent: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Install agent.")
    sjs_jvmserver_install_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                                    doc="Install/Create time.")
    sjs_jvmserver_install_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Install userid.")
    sjs_jvmserver_sys_use_count: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="System thread use-count.")
    sjs_jvmserver_sys_waited: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. waited on sys thrd.")
    sjs_jvmserver_sys_waited_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Total time waited.")
    sjs_jvmserver_sys_wait_cur: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. waiting on sys thrd.")
    sjs_jvmserver_sys_wait_hwm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak waiting on sys thrd.")
    sjs_jvmserver_jvm_creation_gmt: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                                        doc="JVM creation time GMT.")
    sjs_jvmserver_jvm_creation_lcl: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                                        doc="JVM creation LOCAL.")
    sjs_jvmserver_current_heap: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Current heap.")
    sjs_jvmserver_initial_heap: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Initial heap.")
    sjs_jvmserver_max_heap: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Max heap.")
    sjs_jvmserver_peak_heap: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Peak heap.")
    sjs_jvmserver_occupancy: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Heap Occupancy.")
    sjs_jvmserver_gc_policy: so.Mapped[Optional[str]] = so.mapped_column(sa.String(32), doc="GC Policy.")
    sjs_jvmserver_mjr_gc_events: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                             doc="No. major GC collections.")
    sjs_jvmserver_mjr_gc_cpu: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Elapsed time in major GC.")
    sjs_jvmserver_mjr_heap_freed: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Storage freed by GC.")
    sjs_jvmserver_mnr_gc_events: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. minor collections.")
    sjs_jvmserver_mnr_gc_cpu: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Elapsed time in minor GC.")
    sjs_jvmserver_mnr_heap_freed: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Storage freed by GC.")
    sjs_jvmserver_code_cache_used: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Code cache used.")
    sjs_jvmserver_code_cache_alloc: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                                doc="Code cache allocated.")
    sjs_jvmserver_data_cache_used: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Data cache used.")
    sjs_jvmserver_data_cache_alloc: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                                doc="Data cache allocated.")
    sjs_jvmserver_class_strg_used: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Class storage used.")
    sjs_jvmserver_class_strg_alloc: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                                doc="Class strg. allocated.")
    sjs_jvmserver_classcache_size: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Classcache size.")
    sjs_jvmserver_classcache_free: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Classcache free.")


class DfhpiwdsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhpiwds - Webservice Resid stats record."""

    piwds_len: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Webservice stats record length.")
    piwds_id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Webservice stats id.")
    piwds_vers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Webservice stats version.")
    piw_program_interface: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Webservice program interface.")
    piw_msg_validation: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Webservice msg validation.")
    piw_pipeline_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Webservice pipeline name.")
    piw_urimap_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Webservice urimap name.")
    piw_wsbind_file: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), doc="Webservice WSBind file.")
    piw_wsdl_file: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), doc="Webservice WSDL file.")
    piw_wsdl_binding: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), doc="Webservice WSDL binding.")
    piw_endpoint_uri: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), doc="Webservice ENDPOINT URI.")
    piw_webservice_program: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Webservice program name.")
    piw_container_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(16), doc="Webservice container name.")
    piw_webservice_use_count: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Webservice use count.")
    piw_archive_file: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), doc="Webservice archive file.")
    piw_webservice_define_source: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Group installed from.")
    piw_webservice_change_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                                    doc="Change/create time.")
    piw_webservice_change_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Change userid.")
    piw_webservice_change_agent: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Change agent.")
    piw_webservice_install_agent: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Install agent.")
    piw_webservice_install_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                                     doc="Install/Create time.")
    piw_webservice_install_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Install userid.")


class Dfha21dsBase(AbstractConcreteBase):
    """Abstract class for structure Dfha21ds - ISC Statistics."""

    a21_stats_length: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length of data area.")
    a21_stats_id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Statistics id.")
    a21_stats_version: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Stats version number.")
    a21_sit_luit_time: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Delay time for LUIT table.")
    a21_luit_total_reuses: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                       doc="Total number of entries * * reused in LUIT table.")
    a21_luit_total_timeouts: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                         doc="Total number of entries * * timed out in LUIT table.")
    a21_luit_av_reuse_time: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                        doc="Average reuse time between * * entries in the LUIT table.")


class DfhxmcdsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhxmcds - Transaction Manager Domain Tclass Statistics DSECT."""

    xmclen: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length of data area.")
    xmcid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Tclass Statistics id.")
    xmcdvers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Stats version number.")
    xmctat: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                        doc="Total attach requests for trans- actions in this tclass.")
    xmcpi: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                       doc="Transactions purged immediately because threshold reached.")
    xmctq: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                       doc="Transactions that had to queue but are no longer queued.")
    xmcai: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Transactions accepted immediately.")
    xmcaaq: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Transactions accepted after queuing.")
    xmcpwq: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Transactions purged while queuing.")
    xmcmxt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Max. number of transactions allowed.")
    xmcth: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Purge threshold.")
    xmcitd: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                        doc="Installed transaction definitions in this tclass.")
    xmcpat: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak active user transactions.")
    xmcpqt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak queued user transactions.")
    xmctama: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Times at max. active.")
    xmctapt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Times at purge threshold.")
    xmccat: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current active user transactions.")
    xmccqt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current queued user transactions.")
    xmctqtme: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total queuing time of those trans- actions that are no longer queuing.")
    xmccqtme: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total queuing time of those trans- actions that are still queuing.")
    xmcgama: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Last time at max active.")
    xmcpua: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Tclass purge action.")
    xmc_tclass_define_source: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Group installed from.")
    xmc_tclass_change_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Change/create time.")
    xmc_tclass_change_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Change userid.")
    xmc_tclass_change_agent: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Change agent.")
    xmc_tclass_install_agent: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Install agent.")
    xmc_tclass_install_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                                 doc="Install/Create time.")
    xmc_tclass_install_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Install userid.")


class DfhtsgdsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhtsgds - Temp storage statistics."""

    tsglen: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length of data area.")
    tsgid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="TS stats id.")
    tsgdvers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="TS stats version number.")
    tsgsta5f: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="PUT/PUTQ main storage requests.")
    tsgnmg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="GET/GETQ main storage requests.")
    tsgsta7f: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="PUT/PUTQ aux storage requests.")
    tsgnag: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="GET/GETQ aux storage requests.")
    tsgqnumh: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak TS names in use.")
    tsgqinh: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Entries in longest Queue.")
    tsgsta3f: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Times queue created.")
    tsgcsz: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Control interval size.")
    tsgstabf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Writes more than control interval.")
    tsgnci: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="CIs in TS dataset.")
    tsgnciah: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak CIs used.")
    tsgsta8f: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Times aux store exhausted.")
    tsgnbca: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. TS Buffers.")
    tsgbwtn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. Buffer waits.")
    tsgbuwth: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak users waiting on buffer.")
    tsgtwtn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Buffer writes.")
    tsgtwtnr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Writes force for recovery.")
    tsgtrdn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Buffer reads.")
    tsgtwtnf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Format writes.")
    tsgnvca: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. TS strings.")
    tsgnvcah: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak strings in use.")
    tsgvwtn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Times string wait occurred.")
    tsgvuwth: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak users waiting on string.")
    tsgstaaf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="I/O errors on TS dataset.")
    tsgsta9f: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. TS compressions.")
    tsgncia: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current CIs in use.")
    tsgvuwt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Users waiting on string.")
    tsgbuwt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Users waiting on buffer.")
    tsgqnum: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="TS names in use.")
    tsglar: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Longest Auxiliary record length.")
    tsgnavb: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. available bytes per CI.")
    tsgspci: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Segments per CI.")
    tsgbpseg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Bytes per segment.")
    tsgshpdf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Shared pools defined.")
    tsgshpcn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Shared pools connected to.")
    tsgshrds: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Shared read requests.")
    tsgshwts: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Shared write requests.")
    tsgtslht: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times TSMAINLIMIT hit.")
    tsgtsmlm: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="TSMAINLIMIT setting.")
    tsgtsmus: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Current utilisation of TSMAIN.")
    tsgtsmax: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Maximum use of TS storage.")
    tsgtsqdl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of queues auto deleted.")
    tsgtsctr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of cleanup task runs.")
    tsgasu: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current Aux usage percent.")
    tsgasupk: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak Aux usage percent.")


class Dfha04dsBase(AbstractConcreteBase):
    """Abstract class for structure Dfha04ds - Autoinstall statistics (Global)."""

    a04len: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length of data area.")
    a04id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Autoinstall global storage id.")
    a04dvers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="stats version number.")
    a04vadat: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total attempts.")
    a04vadsh: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Times setlogon hold issued.")
    a04vadrj: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total rejected.")
    a04vadlo: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total deleted.")
    a04vadpk: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak concurrent attempts.")
    a04vadpx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Times peak reached.")
    a04vadqt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. queued logons.")
    a04vadqk: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak of Q'd logons.")
    a04vadqx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. times peak is reached.")
    a04rdint: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Shipped delete interval.")
    a04rdidl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Shipped delete idle time.")
    a04skblt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Remote terminals built.")
    a04skins: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Remote terminals installed.")
    a04skdel: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Remote terminals deleted.")
    a04tiexp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Times interval expired.")
    a04rdrec: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="# remdels received.")
    a04rdiss: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="# remdels issued.")
    a04rddel: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="# remdel deletes.")
    a04cidct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current idle count.")
    a04cidle: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Current idle time.")
    a04cmaxi: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Current maximum idle time.")
    a04tidct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total idle count.")
    a04tidle: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Total idle time.")
    a04tmaxi: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Maximum idle time.")


class DfheccdsBase(AbstractConcreteBase):
    """Abstract class for structure Dfheccds - Capturespec Resource stats record."""

    eccds_len: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Capturespec stats record length.")
    eccds_id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Capturespec stats id.")
    eccds_vers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Capturespec stats version.")
    ecc_capturespec_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(32), doc="Capturespec name.")
    ecc_capture_point_type: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Capturespec point type.")
    ecc_capture_point: so.Mapped[Optional[str]] = so.mapped_column(sa.String(25), doc="Capturespec capture point.")
    ecc_event_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(32), doc="Event name.")
    ecc_events_captured: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total events captured.")
    ecc_capture_failures: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of capture failures.")


class DfhrlrdsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhrlrds - ResLife Bundle Resid stats record."""

    rlrds_len: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="ResLife Bundle stats record length.")
    rlrds_id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="ResLife Bundle stats id.")
    rlrds_vers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="ResLife Bundle stats version.")
    rlr_bundle_directory: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), doc="Bundle directory.")
    rlr_bundle_basescope: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), doc="Bundle basescope.")
    rlr_bundle_define_source: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Group installed from.")
    rlr_bundle_change_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Change/create time.")
    rlr_bundle_change_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Change userid.")
    rlr_bundle_change_agent: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Change agent.")
    rlr_bundle_install_agent: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Install agent.")
    rlr_bundle_install_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                                 doc="Install/Create time.")
    rlr_bundle_install_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Install userid.")


class SmtbodyBase(AbstractConcreteBase):
    """Abstract class for structure Smtbody - Task subpool statistics body."""

    smtlocn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Location - Above/below the line.")
    smtaccess: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Access - CICS/USER.")
    smtdsaindex: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="DSA index.")
    smtgmreq: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. Getmain reqs.")
    smtfmreq: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. Freemain reqs.")
    smtces: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Sum of all element lengths.")
    smtcps: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current page storage.")
    smtcne: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current No. elements.")
    smthwmps: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="High Water Mark Page storage.")


class DfhnqgdsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhnqgds - Enqueue Manager Global statistics."""

    nqglen: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length of data area.")
    nqgid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Enqueue Manager statistics id.")
    nqgdvers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Stats version number.")
    nqgnpool: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of ENQ pools following.")


class DfhdsgdsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhdsgds - Dispatcher Domain DSECT."""

    dsglen: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length of data area.")
    dsgid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Dispatcher domain id.")
    dsgdvers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Stats version number.")
    dsgglen: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Global stats length.")
    dsgasize: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. of DSGTCBM dsects supplied.")
    dsgpsize: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. of DSGTCBP dsects supplied.")
    dsgicvt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current ICV time.")
    dsgicvrt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current ICVR Time.")
    dsgicvsd: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current ICVTSD time.")
    dsgpriag: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Priority aging.")
    dsgstsks: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Subtasks value.")
    dsgmbtch: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="QR Batching (MRO) value.")
    dsgcnt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current number of tasks.")
    dsgpnt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak number of tasks.")
    dsgstart: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="GMT STCK Sub-Disp start time.")
    dsglstrt: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Local STCK Sub-Disp start time.")
    dsgejst: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Accumulated TCB time.")
    dsgsrbt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Accumulated SRB time.")
    dsgxscns: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. of excess TCB scans.")
    dsgxscnn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. of scans - no TCB detached.")
    dsgxtcbd: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total no. excess TCBs detached.")
    dsggxscn: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                  doc="Time of last excess TCB scan (GMT).")
    dsglxscn: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                  doc="Time of last excess TCB scan (local).")
    dsggxsnd: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                  doc="Time of last excess TCB scan (GMT) - no TCB detached.")
    dsglxsnd: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                  doc="Time of last excess TCB scan (local) - no TCB detected.")


class Dfhxqs1dBase(AbstractConcreteBase):
    """Abstract class for structure Dfhxqs1d - , XQ list structure statistics record."""

    s1len: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length of data area.")
    s1id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="List structure stats id.")
    s1dvers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="List structure stats version number.")
    s1pref: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="First part of structure name.")
    s1cnpref: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Prefix for connection name.")
    s1cnsysn: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Own MVS system name from CVTSNAME.")
    s1size: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Structure size in 4K pages.")
    s1sizemx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Maximum size in 4K pages.")
    s1hdrs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Maximum number of list headers.")
    s1hdrsct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Headers used for control lists.")
    s1hdrsqd: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Headers available for queue data.")
    s1elemln: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Data element size as a fullword.")
    s1elempw: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Data element size as power of 2.")
    s1elempe: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Max elements per entry (for 32K).")
    s1elemrt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Element size of entry:element ratio.")
    s1entrrt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Entry size of entry:element ratio.")
    s1entrct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current number of entries in use.")
    s1entrhi: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Highest number of entries in use.")
    s1entrlo: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Lowest number of free entries.")
    s1entrmx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Max entries returned by IXLCONN.")
    s1elemct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current number of elements in use.")
    s1elemhi: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Highest number of elements in use.")
    s1elemlo: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Lowest number of free elements.")
    s1elemmx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Max elements returned by IXLCONN.")
    s1usedct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of entries on used list.")
    s1usedhi: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Highest entries on used list.")
    s1freect: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of entries on free list.")
    s1freehi: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Highest entries on free list.")
    s1indxct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of entries in queue index.")
    s1indxhi: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Highest entries in queue index.")
    s1rdqct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Read queue index entry.")
    s1wrqct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Write queue index entry.")
    s1dlqct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Delete queue index entry.")
    s1crlct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Create list for a big queue.")
    s1dllct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Delete list (1 per overall delete).")
    s1rdlct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Read list entry.")
    s1wrlct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Write list entry.")
    s1rwlct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Rewrite list entry.")
    s1inqct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Read queue index status only.")
    s1inlct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Inquire on list entry.")
    s1wract: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Write queue index adjunct area only.")
    s1rrqct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Reread index data for full length.")
    s1rrlct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Reread list data for full length.")
    s1asyct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of asynchronous requests.")
    s1rsp1ct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Normal response, everything OK.")
    s1rsp2ct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Buffer length was too short for the data, needs full length reread.")
    s1rsp3ct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="No matching entry was found, indicates queue not found in index or end of queue for list.")
    s1rsp4ct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Entry version did not match, indicates queue updated by another system or duplicate queue exists when attempting to create queue.")
    s1rsp5ct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="List authority comparison mismatch, indicates big queue was deleted.")
    s1rsp6ct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Maximum list key reached, indicates max queue size or max queues reached depending on list.")
    s1rsp7ct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="The list structure is out of space.")
    s1rsp8ct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="An IXLLIST return code occurred other than those described above.")
    s1rsp9ct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Structure temporarily unavailable, for example during rebuild.")


class Dfhcfs8dBase(AbstractConcreteBase):
    """Abstract class for structure Dfhcfs8d - , CFDT request statistics record."""

    s8len: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length of data area.")
    s8id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Server request stats id.")
    s8dvers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Server request stats version number.")
    s8ocopen: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Open table.")
    s8occlos: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Close table.")
    s8ocset: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Set table attributes.")
    s8ocdele: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Delete table.")
    s8ocstat: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Extract table statistics.")
    s8rqpoin: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Point to record.")
    s8rqhigh: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Return highest key.")
    s8rqread: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Read record (includes for update).")
    s8rqrddl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Read and delete record.")
    s8rqunlk: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Unlock record.")
    s8rqload: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Load record at initial load time.")
    s8rqwrit: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Write new record.")
    s8rqrewr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Rewrite existing record.")
    s8rqdele: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Delete record.")
    s8rqdelm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Delete multiple records.")
    s8iqinqu: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Inquire table.")
    s8spprep: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Prepare to commit unit of work.")
    s8spreta: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Retain locks for unit of work.")
    s8spcomm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Commit unit of work.")
    s8spback: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Back out unit of work.")
    s8spinqu: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Inquire about unit of work.")
    s8sprest: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Restart recoverable connection.")


class DfhtdrdsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhtdrds - Dump domain transaction dump stats."""

    tdrlen: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length of data area.")
    tdrid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="transaction dump stats id.")
    tdrdvers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Domain data format version number.")
    tdrstkn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="# of system dumps taken.")
    tdrssupr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="# of system dumps suppressed.")
    tdrttkn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="# of transaction dumps taken.")
    tdrtsupr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="# of transaction dumps suppressed.")


class DfhsjndsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhsjnds - NODEJSAPP Resid stats record."""

    sjnds_len: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="NODEJSAPP stats record length.")
    sjnds_id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="NODEJSAPP stats id.")
    sjnds_vers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="NODEJSAPP stats version.")
    sjn_nodejsapp_le_runopts: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="NODEJSAPP LE RUNOPTS.")
    sjn_nodejsapp_state: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="NODEJSAPP state.")
    sjn_nodejsapp_define_source: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Group installed from.")
    sjn_nodejsapp_change_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                                   doc="Change/create time.")
    sjn_nodejsapp_change_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Change userid.")
    sjn_nodejsapp_change_agent: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Change agent.")
    sjn_nodejsapp_install_agent: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Install agent.")
    sjn_nodejsapp_install_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                                    doc="Install/Create time.")
    sjn_nodejsapp_install_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Install userid.")
    sjn_nodejsapp_creation_lcl: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                                    doc="Creation time local.")
    sjn_nodejsapp_pid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="NODEJSAPP PID.")
    sjn_nodejsapp_bundle_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Bundle name.")
    sjn_nodejsapp_cpu: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Total CPU time.")
    sjn_nodejsapp_heap_current: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Allocated heap.")
    sjn_nodejsapp_heap_runtime: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Heap used by runtime.")
    sjn_nodejsapp_heap_app_data: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Heap used for data.")
    sjn_nodejsapp_heap_max: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Max possible heap.")
    sjn_nodejsapp_invk: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Completed invokes.")
    sjn_nodejsapp_invk_err: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Completed invokes in error.")
    sjn_nodejsapp_invk_cur: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current invokes in progress.")
    sjn_nodejsapp_invk_peak: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak invokes in progress.")
    sjn_nodejsapp_nodehome: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), doc="Nodehome profile entry.")
    sjn_nodejsapp_profile: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), doc="Profile.")
    sjn_nodejsapp_startscrit: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), doc="Entry JavaScript.")
    sjn_nodejsapp_stderr: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), doc="stderr file.")
    sjn_nodejsapp_stdout: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), doc="stdout file.")
    sjn_nodejsapp_trace: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), doc="trace file.")
    sjn_nodejsapp_log: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), doc="log file.")


class DfhlgsdsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhlgsds - Log Mgr Resid stats record."""

    lgslen: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Record length.")
    lgsid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Log Manager logstream stats id.")
    lgsdvers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Log Manager stats version.")
    lgswrites: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No of log writes.")
    lgsbytes: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Total No of bytes written.")
    lgscufwtrs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current number of force waiters.")
    lgspkfwtrs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak number of force waiters.")
    lgstfcwait: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of force waits.")
    lgsbufwait: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No of waits due to buffer full.")
    lgsbrwstrt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No of log browse starts.")
    lgsbrwread: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No of log browse reads.")
    lgsdeletes: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No of log deletes.")
    lgsrtyerrs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No of retryable errors.")
    lgsbufapp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No of buffer append reqs.")
    lgssyslg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="System log flag.")
    lgsdonly: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="DASD only flag.")
    lgsstruc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(16), doc="CF structure name.")
    lgsmaxbl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Max block length.")
    lgsretpd: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Data retention period.")
    lgsautod: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Data auto delete flag.")
    lgsqueries: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No of log queries.")


class DfhsmddsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhsmdds - Domain subpool statistics."""

    smdlen: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length of data area.")
    smdid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Domain subpool stats id.")
    smddvers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Statistics version number.")
    smddsaname: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="DSA name.")
    smdetype: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Element type (fixed/ variable?).")
    smdflen: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length (if fixed ).")
    smdelchn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Element chaining (yes/no?).")
    smdbndry: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Boundary.")
    smdlocn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Above/below 16 meg line.")
    smdaccess: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Access.")
    smddsaindex: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="DSA index.")
    smdifree: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Initial free value.")
    smdgmreq: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of Getmain reqs.")
    smdfmreq: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of Freemain reqs.")
    smdces: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Sum of all element lengths.")
    smdcps: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current page storage.")
    smdcelem: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current number of elements.")
    smdhwmps: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="High Water Mark Page Storage.")


class DfhldydsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhldyds - Loader Private Library Resid stats record."""

    ldyds_len: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Loader Library stats record length.")
    ldyds_id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Loader Library stats id.")
    ldyds_vers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Loader Library stats version.")
    ldy_library_appl_major_ver: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                            doc="Application major version.")
    ldy_library_appl_minor_ver: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                            doc="Application minor version.")
    ldy_library_appl_micro_ver: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                            doc="Application micro version.")
    ldy_library_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Library name.")
    ldy_library_search_pos: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Library search position.")
    ldy_library_ranking: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Library ranking.")
    ldy_library_critical: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Library critical.")
    ldy_library_enable_status: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Library enable status.")
    ldy_library_prog_loads: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Library program loads.")
    ldy_library_define_source: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Group installed from.")
    ldy_library_change_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Change/create time.")
    ldy_library_change_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Change userid.")
    ldy_library_change_agent: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Change agent.")
    ldy_library_install_agent: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Install agent.")
    ldy_library_install_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                                  doc="Install/Create time.")
    ldy_library_install_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Install userid.")
    ldy_library_numdsnames: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Library number dsnames.")


class LdgdsastatBase(AbstractConcreteBase):
    """Abstract class for structure Ldgdsastat - Program stats on a DSA basis."""

    ldgstgniu: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                           doc="Amount of storage occupied by NIU programs.")
    ldgprogniu: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of programs on NIU queue.")
    ldgrecniu: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                           doc="Number of programs reclaimed from NIU queue.")
    ldgdpscr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of programs removed by DPSC.")
    ldgdpsct: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Total time on NIU queue.")


class DfhpgpdsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhpgpds - Jvmprogram Resid stats record."""

    pgpds_len: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Jvmprogram stats record length.")
    pgpds_id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Jvmprogram stats id.")
    pgpds_vers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Jvmprogram stats version.")
    pgp_jvmprogram_appl_major_ver: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                               doc="Application major version.")
    pgp_jvmprogram_appl_minor_ver: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                               doc="Application minor version.")
    pgp_jvmprogram_appl_micro_ver: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                               doc="Application micro version.")
    pgp_jvmprogram_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Jvmprogram Name.")
    pgp_jvmprogram_entrypoint: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Application Entry Point.")
    pgp_jvmprogram_usecount: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Jvmprogram Use count.")
    pgp_jvmprogram_exec_key: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Jvmprogram CICS/USER key.")
    pgp_jvmprogram_jvmclass: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255),
                                                                         doc="Jvmprogram Jvmclass name.")
    pgp_jvmprogram_server: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Jvmserver Name.")
    pgp_jvmprogram_operation_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64), doc="Operation name.")


class DfhsordsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhsords - TCP/IP Service Resid stats record."""

    sords_len: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="TCP/IP Service stats record length.")
    sords_id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="TCP/IP service stats id.")
    sords_vers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="TCP/IP Service stats version.")
    sor_trans_attached: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. of Transactions Attached.")
    sor_current_conns: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current number of Connections.")
    sor_peak_conns: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak number of Connections.")
    sor_open_gmt: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Service Open Time (GMT).")
    sor_open_local: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Service Open Time (Local).")
    sor_close_gmt: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Service Close Time (GMT).")
    sor_close_local: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Service Close Time (Local).")
    sor_port_number: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="TCP/IP Service Port Number.")
    sor_ssl_support: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="TCP/IP Service SSL Support.")
    sor_backlog: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="TCP/IP Service Backlog setting.")
    sor_sends: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. of Sends (all sockets).")
    sor_bytes_sent: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="No. of Bytes Sent (all sockets).")
    sor_receives: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. of Receives (all sockets).")
    sor_bytes_received: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                    doc="No. of Bytes Received (all sockets).")
    sor_wlm_group: so.Mapped[Optional[str]] = so.mapped_column(sa.String(18), doc="TCP/IP Service Reserved.")
    sor_protocol: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="TCP/IP Service Protocol.")
    sor_authenticate: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="TCP/IP Service Authenticate.")
    sor_privacy: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="TCP/IP Service Privacy.")
    sor_attachsec: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="TCP/IP Service Attachsec.")
    sor_maxdata_length: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="TCP/IP Service Maxdata length.")
    sor_tcpips_tranid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="TCP/IP service Transaction ID.")
    sor_tcpips_urm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="TCP/IP service URM.")
    sor_tcpips_max_persist: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                        doc="Maximum Persistent Connections.")
    sor_tcpips_non_persist: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                        doc="No. Non-Persistent Connections.")
    sor_ip_address: so.Mapped[Optional[str]] = so.mapped_column(sa.String(39), doc="IP Address of TCP/IP Service.")
    sor_ip_family: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="IP family.")
    sor_hostname: so.Mapped[Optional[str]] = so.mapped_column(sa.String(116), doc="Hostname.")
    sor_define_source: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Group installed from.")
    sor_change_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Change/create time.")
    sor_change_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Change userid.")
    sor_change_agent: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Change agent.")
    sor_install_agent: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Install agent.")
    sor_install_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Install/Create time.")
    sor_install_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Install userid.")
    sor_total_conns: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total no. connections.")
    sor_nonp_at_maxpersist: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                        doc="No. made non-persistent because MAXPERSIST was reached.")
    sor_nonp_at_task_limit: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                        doc="No. new connections made non-pers when task limit exceeded.")
    sor_disc_at_task_limit: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                        doc="No. existing conns disconnected when task limit exceeded.")
    sor_disc_at_max_uses: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                      doc="No. connections disconnected when its no. uses exceeded limit.")
    sor_curr_backlog: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current backlog q depth.")
    sor_conns_dropped: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. connections dropped.")
    sor_conn_last_dropped: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                               doc="Date/time conn last dropped.")
    sor_curr_max_backlog: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Backlog currently in use.")
    sor_requests: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. requests processed.")
    sor_tcpips_optionspgm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="OPTIONS handler name.")


class Dfhncs5dBase(AbstractConcreteBase):
    """Abstract class for structure Dfhncs5d - , NC server main storage statistics."""

    s5len: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length of data area.")
    s5id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="NC server main storage stats id.")
    s5dvers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="NC server main storage stats version.")
    s5anynam: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Pool name AXMPGANY.")
    s5anysiz: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Size of storage pool area.")
    s5anyptr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Address of storage pool area.")
    s5anymx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total pages in the storage pool.")
    s5anyus: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of used pages in the pool.")
    s5anyfr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of free pages in the pool.")
    s5anylo: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Lowest free pages (since reset).")
    s5anyrqg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Storage GET requests.")
    s5anyrqf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Storage FREE requests.")
    s5anyrqs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="GETs which failed to get storage.")
    s5anyrqc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Compress (defragmentation) attempts.")
    s5lownam: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Pool name AXMPGLOW.")
    s5lowsiz: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Size of storage pool area.")
    s5lowptr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Address of storage pool area.")
    s5lowmx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total pages in the storage pool.")
    s5lowus: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of used pages in the pool.")
    s5lowfr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of free pages in the pool.")
    s5lowlo: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Lowest free pages (since reset).")
    s5lowrqg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Storage GET requests.")
    s5lowrqf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Storage FREE requests.")
    s5lowrqs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="GETs which failed to get storage.")
    s5lowrqc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Compress (defragmentation) attempts.")


class DfhlgrdsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhlgrds - Log Mgr Resid stats record."""

    lgrlen: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Record length.")
    lgrid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Log Manager stats id.")
    lgrdvers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Log Manager stats version.")
    lgrjtype: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Journal type (MVS, SMF, Dummy).")
    lgrstream: so.Mapped[Optional[str]] = so.mapped_column(sa.String(26), doc="Log stream name.")
    lgrwrites: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No of journal writes.")
    lgrbytes: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Total No of bytes written.")
    lgrbuflsh: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No of buffer flush requests.")


class DfhecgdsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhecgds - Eventbinding Global stats record."""

    ecgds_len: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Eventbinding stats record length.")
    ecgds_id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Eventbinding stats id.")
    ecgds_vers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Eventbinding stats version.")
    ecg_eb_event_filter_ops: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                         doc="Total event filtering operations.")
    ecg_eb_events_captured: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Total events captured.")
    ecg_eb_events_disabled: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                        doc="Events with disabled eventbinding.")
    ecg_sys_events_captured: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                         doc="Total system events captured.")
    ecg_filter_ops_failed: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. filter operations failed.")
    ecg_capture_ops_failed: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                        doc="No. capture operations failed.")


class DfhecrdsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhecrds - Eventbinding Resource stats record."""

    ecrds_len: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Eventbinding stats record length.")
    ecrds_id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Eventbinding stats id.")
    ecrds_vers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Eventbinding stats version.")
    ecr_epadapter_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(32), doc="EP adapter name.")
    ecr_eb_define_source: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Group installed from.")
    ecr_eb_change_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Change/create time.")
    ecr_eb_change_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Change userid.")
    ecr_eb_change_agent: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Change agent.")
    ecr_eb_install_agent: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Install agent.")
    ecr_eb_install_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Install/Create time.")
    ecr_eb_install_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Install userid.")


class DfhlggdsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhlggds - Log Mgr Global stats record."""

    lgglen: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Record length.")
    lggid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Log Manager logstream stats id.")
    lggdvers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Log Manager stats version.")
    lggakpfreq: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Keypoint Frequency.")
    lgglgdefer: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Logdefer Interval.")
    lggakpstkn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of Keypoints Taken.")


class DfhmngdsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhmngds - Monitoring Domain Stats."""

    mnglen: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length of data.")
    mngid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Monitoring domain id.")
    mngdvers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="DSECT version number.")
    mnger: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. Exception records.")
    mngers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. Exception records supp. by exit.")
    mngpr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. Performance records.")
    mngprs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. Performance records supp. by exit.")
    mngsmfr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. SMF records.")
    mngsmfe: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. SMF Errors.")
    mngsmfnc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. SMF records not compressed.")
    mngsmfcm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. SMF records compressed.")
    mngrr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. Resource records.")
    mngrrs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. Resource records supp. by exit.")
    mngir: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. Identity records.")
    mngirs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. Identity records supp. by exit.")
    mngfrl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="File Resource Limit.")
    mngtrl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Tsqueue Resource Limit.")
    mngdplrl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="DPL Resource Limit.")
    mngurirl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="URIMAP Resource Limit.")
    mngwebrl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="WEBSVC Resource Limit.")
    mngrmi: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="RMI option.")
    mngappns: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="APPLNAME option.")
    mngmrcmp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Data Compression Option.")
    mngavurl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Avg Uncompressed record length.")
    mngavcrl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Avg Compressed record length.")
    mngwlmmd: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Workload Management Mode.")
    mngwlmst: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="WLM Address Space Server status.")
    mngwlmsc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="WLM Service Class name - if any.")
    mngwlmwn: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="WLM Owning Workload Name.")
    mngwlmrg: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="WLM Resource Group name - if any.")
    mngwlmrc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="WLM Report Class name - if any.")
    mngwlmgt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="WLM Goal type.")
    mngwlmcc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="WLM CPU Critical.")
    mngwlmsk: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="WLM Storage Critical.")
    mngwlmgm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="WLM Address Space Goal Mgmt.")
    mngwlmgv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="WLM goal value Value of velocity goal 0 if type not velocity.")
    mngwlmgi: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="WLM goal importance.")
    mngcectp: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="CEC Machine Type.")
    mngcecid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(16), doc="CEC Model Number.")
    mngmctnm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="MCT program name.")
    mngutnum: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="User transactions ended.")
    mngstnum: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="System transactions ended.")
    mnggutcl: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Time last trans ended (GMT).")
    mnglutcl: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Time last trans ended (Local).")
    mnggutat: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Time last trans attach (GMT).")
    mnglutat: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Time last trans attch (Local).")
    mngmxuta: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="MXT at last trans attach.")
    mngcauta: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current tasks at last attach.")
    mngfreq: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="FREQUENCY HHMMSS.")
    mngautrt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Avg user trans resp time.")
    mngputrt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Peak user trans resp time.")
    mnggutrt: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Time peak resp time (GMT).")
    mnglutrt: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Time peak resp time (Local).")
    mngcput: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Total CPU time.")
    mngtoncp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Total CPU time on CP.")
    mngoflcp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Total CPU time offload on CP.")


class Dfhd2gdsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhd2gds - CICS/DB2 Global statistics."""

    d2glen: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length of data area.")
    d2gid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="CICS/DB2 global stats id.")
    d2gdvers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Stats version number.")
    d2g_db2conn_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="name of the DB2CONN.")
    d2g_db2_id: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="DB2 sysid.")
    d2g_db2_release: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="release of DB2.")
    d2g_connect_time_gmt: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="connect time (GMT).")
    d2g_connect_time_local: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                                doc="connect time (local).")
    d2g_disconnect_time_gmt: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                                 doc="disconnect time (GMT).")
    d2g_disconnect_time_local: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                                   doc="discconnect time (local).")
    d2g_tcb_limit: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="max number of TCBs.")
    d2g_tcb_current: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="current number of TCBs.")
    d2g_tcb_hwm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="HWM of TCBs.")
    d2g_tcb_free: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="current number of free TCBs.")
    d2g_tcb_readyq_current: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                        doc="number of tasks on TCB readyq.")
    d2g_tcb_readyq_hwm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                    doc="peak number of tasks on TCB readyq.")
    d2g_db2_group_id: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="DB2 group id.")
    d2g_resyncmember: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="resync uow's.")
    d2g_reuselimit: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Thread reuse limit.")
    d2g_tcb_protected_current: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                           doc="TCBs for protected threads.")
    d2g_pool_plan_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="static plan name if any.")
    d2g_pool_planexit_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="planexit name if any.")
    d2g_pool_authid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="static authid if any.")
    d2g_pool_authtype: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="authtype if any.")
    d2g_pool_accountrec: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Accountrec setting.")
    d2g_pool_threadwait: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Threadwait setting.")
    d2g_pool_priority: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="thread priority.")
    d2g_pool_calls: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="number of calls using pool.")
    d2g_pool_signons: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="number of signons.")
    d2g_pool_commits: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="number of commits.")
    d2g_pool_aborts: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="number of aborts.")
    d2g_pool_single_phase: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                       doc="number of single phase commits.")
    d2g_pool_thread_reuse: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="number of thread reuses.")
    d2g_pool_thread_term: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="number of thread terminates.")
    d2g_pool_thread_waits: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="number of thread waits.")
    d2g_pool_thread_limit: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="maximum number of threads.")
    d2g_pool_thread_current: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="current number of threads.")
    d2g_pool_thread_hwm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="peak number of threads.")
    d2g_pool_task_current: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="current number of tasks.")
    d2g_pool_task_hwm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="peak number of tasks.")
    d2g_pool_task_total: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="total number of tasks.")
    d2g_pool_readyq_current: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                         doc="number of tasks on ready queue.")
    d2g_pool_readyq_hwm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                     doc="peak number of tasks on ready queue.")
    d2g_pool_partial_signons: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="number of partial signons.")
    d2g_pool_thread_create: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="number of thread creates.")
    d2g_pool_reuselimit_count: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                           doc="number of times hit reuselimit.")
    d2g_comd_authid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="static authid if any.")
    d2g_comd_authtype: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="authtype if any.")
    d2g_comd_calls: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="number of dsnc comd calls.")
    d2g_comd_signons: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="number of signons.")
    d2g_comd_thread_term: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="number of thread terminates.")
    d2g_comd_thread_overf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="number of overflows to pool.")
    d2g_comd_thread_limit: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="maximum number of threads.")
    d2g_comd_thread_current: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="current number of threads.")
    d2g_comd_thread_hwm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="peak number of threads.")
    d2g_comd_thread_create: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="number of thread creates.")
    d2g_db2conn_define_source: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Group installed from.")
    d2g_db2conn_change_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Change/create time.")
    d2g_db2conn_change_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Change userid.")
    d2g_db2conn_change_agent: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Change agent.")
    d2g_db2conn_install_agent: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Install agent.")
    d2g_db2conn_install_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                                  doc="Install/Create time.")
    d2g_db2conn_install_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Install userid.")


class DfhldpdsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhldpds - Loader statistics (RESID)."""

    ldplen: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length of data area.")
    ldpid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Loader domain stats id.")
    ldpdvers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Domain data format version number.")
    ldp_appl_major_ver: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Application major version.")
    ldp_appl_minor_ver: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Application minor version.")
    ldp_appl_micro_ver: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Application micro version.")
    ldppname: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Program name.")
    ldptu: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Times used since last reset.")
    ldpfc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Fetch count.")
    ldpft: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Total time taken for all fetchs.")
    ldptn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Times NEWCOPYed.")
    ldppsize: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Program size.")
    ldprpc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Times removed by program compression.")
    ldplocn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Location of current copy.")
    ldplbnm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Program library name.")
    ldplbdnm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(44), doc="Program library dsname.")
    ldp_operation_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64), doc="Operation name.")


class Dfhxqs3dBase(AbstractConcreteBase):
    """Abstract class for structure Dfhxqs3d - , XQ main storage statistics record."""

    s3len: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length of data area.")
    s3id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="XQ main storage stats id.")
    s3dvers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="XQ main storage stats version.")
    s3anynam: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Pool name AXMPGANY.")
    s3anysiz: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Size of storage pool area.")
    s3anyptr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Address of storage pool area.")
    s3anymx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total pages in the storage pool.")
    s3anyus: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of used pages in the pool.")
    s3anyfr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of free pages in the pool.")
    s3anylo: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Lowest free pages (since reset).")
    s3anyrqg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Storage GET requests.")
    s3anyrqf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Storage FREE requests.")
    s3anyrqs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="GETs which failed to get storage.")
    s3anyrqc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Compress (defragmentation) attempts.")
    s3lownam: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Pool name AXMPGLOW.")
    s3lowsiz: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Size of storage pool area.")
    s3lowptr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Address of storage pool area.")
    s3lowmx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total pages in the storage pool.")
    s3lowus: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of used pages in the pool.")
    s3lowfr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of free pages in the pool.")
    s3lowlo: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Lowest free pages (since reset).")
    s3lowrqg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Storage GET requests.")
    s3lowrqf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Storage FREE requests.")
    s3lowrqs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="GETs which failed to get storage.")
    s3lowrqc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Compress (defragmentation) attempts.")


class Dfhd2rdsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhd2rds - CICS/DB2 Resource statistics."""

    d2rlen: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length of data area.")
    d2rid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="CICS/DB2 resource stats id.")
    d2rdvers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Stats version number.")
    d2r_plan_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="static plan name if any.")
    d2r_planexit_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="planexit name if any.")
    d2r_authid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="static authid if any.")
    d2r_authtype: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="authtype if any.")
    d2r_accountrec: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Accountrec setting.")
    d2r_threadwait: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Threadwait setting.")
    d2r_priority: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="thread priority.")
    d2r_calls: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="number of calls using db2entry.")
    d2r_signons: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="number of signons.")
    d2r_commits: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="number of commits.")
    d2r_aborts: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="number of aborts.")
    d2r_single_phase: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="number of single phase commits.")
    d2r_thread_reuse: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="number of thread reuses.")
    d2r_thread_term: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="number of thread terminates.")
    d2r_thread_wait_or_overfl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                           doc="number of thread waits or overflows.")
    d2r_thread_limit: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="maximum number of threads.")
    d2r_thread_current: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="current number of threads.")
    d2r_thread_hwm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="peak number of threads.")
    d2r_pthread_limit: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                   doc="maximum number of protected threads.")
    d2r_pthread_current: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                     doc="current number of protected threads.")
    d2r_pthread_hwm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="peak number of protected threads.")
    d2r_task_current: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="current number of tasks.")
    d2r_task_hwm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="peak number of tasks.")
    d2r_task_total: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="total number of tasks.")
    d2r_readyq_current: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="number of tasks on ready queue.")
    d2r_readyq_hwm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="peak number of tasks on ready queue.")
    d2r_partial_signons: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="number of partial signons.")
    d2r_thread_create: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of thread creates.")
    d2r_reuselimit_count: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                      doc="Number times reuselimit reached.")
    d2r_sharelocks: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="SHARELOCKS setting.")
    d2r_define_source: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Group installed from.")
    d2r_change_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Change/create time.")
    d2r_change_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Change userid.")
    d2r_change_agent: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Change agent.")
    d2r_install_agent: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Install agent.")
    d2r_install_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Install/Create time.")
    d2r_install_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Install userid.")


class DfhstgdsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhstgds - Statistics domain statistics."""

    stglen: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length of data.")
    stgid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Stats domain id.")
    stgdvers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Stats version number.")
    stgnc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of Interval Collections.")
    stgsmfw: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of SMF Writes.")
    stgldw: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length of Statistics Data Written.")
    stgsmfs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of SMF Writes Suppressed.")
    stgsmfe: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. SMF errors.")
    stgintr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. INT statistics records.")
    stgeodr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. EOD statistics records.")
    stgussr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. USS statistics records.")
    stgreqr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. REQ statistics records.")
    stgrrtr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. RRT statistics records.")
    stgcstrt: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Statistics CICS Start Time.")
    stglrt: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Statistics Last Reset Time.")
    stgintvl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Statistics Collection Interval.")
    stgeodt: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Statistics End-of-Day Time.")
    stgstrcd: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="STATRCD setting.")


class DfhsogdsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhsogds - Sockets Global stats record."""

    sogds_len: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Sockets Global stats record length.")
    sogds_id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Sockets Global stats id.")
    sogds_vers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Sockets Global stats version.")
    sog_maxsockets_limit: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Maxsockets limit.")
    sog_curr_inbound_sockets: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current Inbound sockets.")
    sog_peak_inbound_sockets: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak Outbound sockets.")
    sog_curr_outb_sockets: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current Outbound sockets.")
    sog_peak_outb_sockets: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak Outbound sockets.")
    sog_inb_sockets_created: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                         doc="Number Inbound sockets created.")
    sog_outb_sockets_created: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                          doc="Number Outbound sockets created.")
    sog_outb_sockets_closed: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                         doc="Number of Outb sockets closed.")
    sog_times_at_max_sockets: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                          doc="Number of times at maxsockets.")
    sog_delayed_at_max_sockets: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                            doc="Total delayed at maxsockets.")
    sog_qtime_at_max_sockets: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                            doc="Total delay time at maxsockets.")
    sog_timedout_at_max_sockets: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                             doc="Timeouts whilst at maxsockets.")
    sog_curr_delayed_at_max: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                         doc="Current delayed at maxsockets.")
    sog_peak_delayed_at_max: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak delayed at maxsockets.")
    sog_current_qtime_at_max: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                            doc="Current delay time at maxsockets.")
    sog_sslcache: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="SSLCACHE setting.")
    sog_sotuning: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Whether SOTUNING set.")
    sog_pausing_http_listening: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                            doc="Whether pausing HTTP listening.")
    sog_stopping_persistence: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                          doc="Whether stopping persistence.")
    sog_times_at_accept_limit: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Times noticed at limit.")
    sog_time_last_paused_http_listening: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                                             doc="Last time paused HTTP listening at accept limit.")
    sog_times_stopped_persistent: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                              doc="Times stopped persistenc.")
    sog_time_last_stopped_persistent: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                                          doc="Time last stopped pers.")
    sog_times_made_non_persistent: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                               doc="Times conn made non-pers.")
    sog_times_conn_disconnected_at_max: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Times disc conn.")
    sog_peak_pers_inb_sockets: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak persistent inbound.")
    sog_peak_npers_inb_sockets: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak non-pers inbound.")
    sog_curr_npers_inb_sockets: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current non-pers inbnd.")
    sog_npers_inb_sockets_created: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                               doc="Total non-pers inbound.")
    sog_times_outb_reused: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Times outbound reused.")
    sog_s8tlshs_requests_max: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Max TLS handshakes.")
    sog_s8tlshs_requests_cur: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current handshakes.")
    sog_s8tlshs_requests_peak: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak handshakes.")
    sog_s8tlshs_waiters_max: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Max handshake waiters.")
    sog_s8tlshs_waiters_cur: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current waiters.")
    sog_s8tlshs_waiters_peak: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak waiters.")
    sog_times_cicstls12_inb_used: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Inb CICS TLS12 used.")
    sog_times_cicstls13_inb_used: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Inb CICS TLS13 used.")
    sog_times_cicstlsall_inb_used: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Inb all CICS TLS used.")
    sog_times_cicstls12_outb_used: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Outb CICS TLS12 used.")
    sog_times_cicstls13_outb_used: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Outb CICS TLS13 used.")
    sog_times_cicstlsall_outb_used: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                                doc="Outb all CICS TLS used.")
    sog_times_atssl3_inb_used: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Inbound AT-SSL3 used.")
    sog_times_attls10_inb_used: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Inbound AT-TLS10 used.")
    sog_times_attls11_inb_used: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Inbound AT-TLS11 used.")
    sog_times_attls12_inb_used: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Inbound AT-TLS12 used.")
    sog_times_attls13_inb_used: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Inbound AT-TLS13 used.")
    sog_times_atssl3_outb_used: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Outbound AT-SSL3 used.")
    sog_times_attls10_outb_used: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Outbound AT-TLS10 used.")
    sog_times_attls11_outb_used: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Outbound AT-TLS11 used.")
    sog_times_attls12_outb_used: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Outbound AT-TLS12 used.")
    sog_times_attls13_outb_used: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Outbound AT-TLS13 used.")
    sog_handshakes_full_inb: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Inbound full HS count.")
    sog_handshakes_abbrev_inb: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Inbound abbr HS count.")
    sog_handshakes_full_outb: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Outbound full HS count.")
    sog_handshakes_abbrev_outb: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Outbound abbr HS count.")


class Dfhxqs2dBase(AbstractConcreteBase):
    """Abstract class for structure Dfhxqs2d - , XQ buffer pool statistics record."""

    s2len: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length of data area.")
    s2id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="XQ buffer pool stats id.")
    s2dvers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="XQ buffer pool version number.")
    s2bfqty: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total buffers defined.")
    s2bfenth: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of buffers used so far.")
    s2bfacts: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Active buffers owned by tasks.")
    s2bflrus: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Valid buffers on LRU chain.")
    s2bfemps: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Empty buffers on free chain.")
    s2bfpwts: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Waits on buffer pool lock.")
    s2bfgets: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="GET requests.")
    s2bfhits: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="GET which found a valid buffer.")
    s2bfgfrs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="GETs which used a free buffer.")
    s2bfgnws: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="GETs which used a new buffer.")
    s2bfglrs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="GETs which used the LRU buffer.")
    s2bflwts: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="GET waits on buffer lock.")
    s2bfgnbs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="GETs which returned no buffer.")
    s2bfputs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="PUTs (put back buffer as valid).")
    s2bfkeps: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="KEEPs (put back buffer as modified).")
    s2bffres: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="FREEs (put back buffer as empty).")
    s2bffnos: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="FREE errors, buffer not owned.")
    s2bfpurs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="PURGEs (mark buffer invalid).")
    s2bfpnfs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="PURGE with no matching buffer found.")
    s2bfpnos: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="PURGE errors, buffer not owned.")


class DfhpggdsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhpggds - pg global stats."""

    pgg_stats_length: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="length of record.")
    pgg_stats_id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="pg global stats id, should contain pgg_dcl_id.")
    pgg_stats_version: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="pg global stats version.")
    pgg_auto_attempts: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="number of autoinstalls attempted.")
    pgg_auto_rejects: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="number of autoinstalls rejected.")
    pgg_auto_failures: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="number of autoinstalls failed.")


class Dfhcfs9dBase(AbstractConcreteBase):
    """Abstract class for structure Dfhcfs9d - , CF main storage statistics record."""

    s9len: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length of data area.")
    s9id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="CF DT main storage stats id.")
    s9dvers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="CF DT main storage stats version.")
    s9anynam: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Pool name AXMPGANY.")
    s9anysiz: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Size of storage pool area.")
    s9anyptr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Address of storage pool area.")
    s9anymx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total pages in the storage pool.")
    s9anyus: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of used pages in the pool.")
    s9anyfr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of free pages in the pool.")
    s9anylo: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Lowest free pages (since reset).")
    s9anyrqg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Storage GET requests.")
    s9anyrqf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Storage FREE requests.")
    s9anyrqs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="GETs which failed to get storage.")
    s9anyrqc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Compress (defragmentation) attempts.")
    s9lownam: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Pool name AXMPGLOW.")
    s9lowsiz: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Size of storage pool area.")
    s9lowptr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Address of storage pool area.")
    s9lowmx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total pages in the storage pool.")
    s9lowus: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of used pages in the pool.")
    s9lowfr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of free pages in the pool.")
    s9lowlo: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Lowest free pages (since reset).")
    s9lowrqg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Storage GET requests.")
    s9lowrqf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Storage FREE requests.")
    s9lowrqs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="GETs which failed to get storage.")
    s9lowrqc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Compress (defragmentation) attempts.")


class DsgtcbmBase(AbstractConcreteBase):
    """Abstract class for structure Dsgtcbm - TCB Mode Stats."""

    dsgtcbmd: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="TCB Mode.")
    dsgtcbmp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="TCB Mode Pool number.")
    dsgntcba: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. of TCB attaches.")
    dsgtcbaf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. of TCB attach failures.")
    dsgtcbca: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current No. of TCBs attached.")
    dsgtcbpa: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak No. of TCBs attached.")
    dsgtcbcu: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current No. TCBs used by mode.")
    dsgtcbpu: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak No. TCBs used by mode.")
    dsgtcbal: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. TCB Allocates to task.")
    dsgtcbdu: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. of TCB detaches - unclean.")
    dsgtcbds: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. of TCB detaches - stolen.")
    dsgtcbdx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. of TCB detaches - excess.")
    dsgtcbdo: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. of TCB detaches - other.")
    dsgtcbst: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. of TCB steals.")
    dsgtcbmm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. of TCB mismatches.")
    dsgsysw: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No. of partition exits.")
    dsgtmcdq: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current tasks on dispatchable queue.")
    dsgtmpdq: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak tasks on dispatchable queue.")
    dsgtmadq: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Average tasks on dispatchable queue (2 decimal places).")
    dsgtwt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Cum real time CICS in OS wait.")
    dsgtdt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Cum real time TCB disp by MVS.")
    dsgtct: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Cum CPU time for DS task.")
    dsgact: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Cum CPU time for TCB.")


class Dfhncs4dBase(AbstractConcreteBase):
    """Abstract class for structure Dfhncs4d - , NC list structure statistics record."""

    s4len: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length of data area.")
    s4id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="List structure stats id.")
    s4dvers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="List structure stats version number.")
    s4pref: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="First part of structure name.")
    s4cnpref: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Prefix for connection name.")
    s4cnsysn: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Own MVS system name from CVTSNAME.")
    s4size: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Structure size in 4K pages.")
    s4sizemx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Maximum size in 4K pages.")
    s4entrct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current number of entries in use.")
    s4entrhi: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Highest number of entries in use.")
    s4entrlo: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Lowest number of free entries.")
    s4entrmx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Max entries returned by IXLCONN.")
    s4crect: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Create counter.")
    s4getct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Get and increment counter.")
    s4setct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Set counter.")
    s4delct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Delete counter.")
    s4keqct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Inquire KEQ.")
    s4kgect: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Inquire KGE.")
    s4asyct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of asynchronous requests.")
    s4rsp1ct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Normal response, everything OK.")
    s4rsp2ct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No matching entry was found.")
    s4rsp3ct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Entry version did not match.")
    s4rsp4ct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="List authority comparison mismatch.")
    s4rsp5ct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="The list structure is out of space.")
    s4rsp6ct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="An IXLLIST return code occurred other than those described above.")
    s4rsp7ct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Structure temporarily unavailable, during system- managed rebuild.")


class DfhrmgdsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhrmgds - Recovery Manager Global statistics."""

    rmglen: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length of data area.")
    rmgid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Recovery Manager statistics id.")
    rmgdvers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Stats version number.")
    rmgsyfwd: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total syncpoints forward.")
    rmgsybwd: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total syncpoints backward.")
    rmgresyn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total resynchronisations.")
    rmgtshin: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total shunted uows for indoubt.")
    rmgtshti: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Total time shunted for indoubt (STCK).")
    rmgcshin: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current uows shunted for indoubt.")
    rmgcshti: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Current time shunted indoubt (STCK).")
    rmgtshro: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total ouws shunted for RO commit fail.")
    rmgtshtr: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Total time shunted for RO fail (STCK).")
    rmgcshro: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current ouws shunts RO commit fail.")
    rmgcshtr: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Current time shunted RO fail (STCK).")
    rmgiaftr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total forced Indoubt Actions-trandef.")
    rmgiafti: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total forced Indoubt Actions-timeout.")
    rmgiafnw: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total forced Indoubt Actions-nowait.")
    rmgiafop: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total forced Indoubt Actions-operator.")
    rmgiafot: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total forced Indoubt Actions-other.")
    rmgiamis: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total Indoubt Action mismatches.")
    rmgnwtd: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total forced for no waiting in TD.")
    rmgnw61: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total forced for no waiting in LU61.")
    rmgnwmro: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total forced for no waiting in MRO.")
    rmgnwrmi: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total forced for no waiting in RMI.")
    rmgnwoth: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total forced for no waiting in other.")


class DfhusgdsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhusgds - User Domain Stats."""

    usglen: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length of data.")
    usgid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="User domain id.")
    usgdvers: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="DSECT version number.")
    usgtomrt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Timeout Mean Reuse Time.")
    usgtorc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Timeout Reuse count.")
    usgtoec: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Timeout Expiry count.")
    usgdrrc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Directory Reuse count.")
    usgdrnfc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Directory not found count.")
    usgdesof: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Deleted for sign-off.")
    usgdeenf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Deleted for ENF.")
    usgdrcur: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current in directory.")
    usgdrpk: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak in directory.")
    usgtocur: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current in Timeout queue.")
    usgtopk: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Peak in Timeout queue.")
    usgenfk: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="ENF events matched.")
    usgenfun: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="ENF events not matched.")
