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


class Base123(Base):
    __abstract__ = True
    metadata = sa.MetaData(schema='smf123', naming_convention=convention)


class Base12315m(Base):
    __abstract__ = True
    metadata = sa.MetaData(schema='smf123', naming_convention=convention)


class Base123Hr(Base):
    __abstract__ = True
    metadata = sa.MetaData(schema='smf123', naming_convention=convention)


class Base123Da(Base):
    __abstract__ = True
    metadata = sa.MetaData(schema='smf123', naming_convention=convention)


class DfhcbtsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhcbts - Performance data in group DFHCBTS."""

    cbts_prcsname: so.Mapped[Optional[str]] = so.mapped_column(sa.String(36),
                                                               doc="The name of the CICS business transaction service (BTS) process of which the user task formed part.")
    cbts_prcstype: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                               doc="The process-type of the CICS BTS process of which the user task formed part.")
    cbts_prcsid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(52),
                                                             doc="The CICS-assigned identifier of the CICS BTS root activity that the user task implemented.")
    cbts_actvtyid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(52),
                                                               doc="The CICS-assigned identifier of the CICS BTS activity that the user task implemented.")
    cbts_actvtynm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(16),
                                                               doc="The name of the CICS BTS activity that the user task implemented.")
    cbts_barsynct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of CICS BTS run process, or run activity, requests that the user task made in order to execute a process or activity synchronously.")
    cbts_barasyct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of CICS BTS run process, or run activity, requests that the user task made in order to execute a process or activity asynchronously.")
    cbts_balkpact: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of CICS BTS link process, or link activity, requests that the user task issued.")
    cbts_badproct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of CICS BTS define process requests issued by the user task.")
    cbts_badactct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of CICS BTS define activity requests issued by the user task.")
    cbts_barspact: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of CICS BTS reset process and reset activity requests issued by the user task.")
    cbts_basupact: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of CICS BTS suspend process, or suspend activity, requests issued by the user task.")
    cbts_barmpact: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of CICS BTS resume process, or resume activity, requests issued by the user task.")
    cbts_badcpact: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of CICS BTS delete activity, cancel process, or cancel activity, requests issued by the user task.")
    cbts_baacqpct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of CICS BTS acquire process, or acquire activity, requests issued by the user task.")
    cbts_batotpct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Total number of CICS BTS process and activity requests issued by the user task.")
    cbts_baprdcct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of CICS BTS delete, get, move, or put, container requests for process data containers issued by the user task.")
    cbts_baacdcct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of CICS BTS delete, get, move, or put, container requests for current activity data containers issued by the user task.")
    cbts_batotcct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Total number of CICS BTS delete, get, move, or put, process container and activity container requests issued by the user task.")
    cbts_baratect: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of CICS BTS retrieve-reattach event requests issued by the user task.")
    cbts_badfiect: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of CICS BTS define-input event requests issued by the user task.")
    cbts_batiaect: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of CICS BTS DEFINE TIMER EVENT, CHECK TIMER EVENT, DELETE TIMER EVENT, and FORCE TIMER EVENT requests issued by the user task.")
    cbts_batotect: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Total number of CICS BTS event-related requests issued by the user task.")


class DfhchnlBase(AbstractConcreteBase):
    """Abstract class for structure Dfhchnl - Performance data in group DFHCHNL."""

    chnl_pgtotcct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of CICS requests for channel containers issued by the user task.")
    chnl_pgbrwcct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of CICS browse requests for channel containers issued by the user task.")
    chnl_pggetcct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of GET CONTAINER and GET64 CONTAINER requests for channel containers issued by the user task.")
    chnl_pgputcct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of PUT CONTAINER and PUT64 CONTAINER requests for channel containers issued by the user task.")
    chnl_pgmovcct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of MOVE CONTAINER requests for channel containers issued by the user task.")
    chnl_pggetcdl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The total length, in bytes, of the data in the containers of all the GET CONTAINER CHANNEL and GET64 CONTAINER CHANNEL commands issued by the user task.")
    chnl_pgputcdl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The total length, in bytes, of the data in the containers of all the PUT CONTAINER CHANNEL and PUT64 CONTAINER CHANNEL commands issued by the user task.")
    chnl_pgcrecct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of containers created by MOVE, PUT CONTAINER, and PUT64 CONTAINER requests for channel containers issued by the user task.")
    chnl_pgcsthwm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Maximum amount (high-water mark), in bytes, of container storage allocated to the user task.")


class DfhcicsBase(AbstractConcreteBase):
    """Abstract class for structure Dfhcics - Performance data in group DFHCICS."""

    cics_cfcapict: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Number of CICS OO foundation class requests, including the Java API for CICS (JCICS) classes, issued by the user task.")
    cics_userid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                             doc="User identification at task creation. This identification can also be the remote user identifier for a task created as the result of receiving an ATTACH request across an MRO or APPC link with attach-time security enabled.")
    cics_exwttime: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="Accumulated data for exception conditions. The timer component of the clock contains the total elapsed time for which the user waited on exception conditions. The period count equals the number of exception conditions that have occurred for this task. For more information on exception conditions, see Exception class data: Listing of data fields . For more information on clocks, see Clocks and time stamps.")
    cics_rtype: so.Mapped[Optional[str]] = so.mapped_column(sa.String(1),
                                                            doc="Performance record type (low-order byte-3).")
    cics_rsysid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4),
                                                             doc="The name (SYSID) of the remote system to which this transaction was routed either statically or dynamically.")
    cics_perrecnt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of performance class records written by the CICS Monitoring Facility (CMF) for the user task.")
    cics_srvclsnm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                               doc="The z/OS Workload Manager (WLM) service class for this transaction. This field is null if no transaction classification rules are defined for CICS subsystems in the active z/OS Workload Manager (WLM) service policy, or if the transaction was WLM-classified in another CICS region.")
    cics_rptclsnm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                               doc="The z/OS Workload Manager (WLM) report class for this transaction. This field is null if no transaction classification rules are defined for CICS subsystems in the active z/OS Workload Manager (WLM) service policy, or if the transaction was WLM-classified in another CICS region.")
    cics_oadid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64),
                                                            doc="The adapter identifier added to the origin data by the adapter. This field is blank if the task was not started by using an adapter, or if it was and the adapter did not set this value.")
    cics_oadata2: so.Mapped[Optional[str]] = so.mapped_column(sa.String(130),
                                                              doc="The data added to the origin data by using the adapter. This field is blank if the task was not started by using an adapter, or if it was and the adapter did not set this value.")
    cics_oadata3: so.Mapped[Optional[str]] = so.mapped_column(sa.String(130),
                                                              doc="The data added to the origin data by the adapter. This field is blank if the task was not started by using an adapter, or if it was and the adapter did not set this value.")
    cics_onetwkid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                               doc="The network identifier from which this work request (transaction) originated.")
    cics_oapplid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                              doc="The APPLID of the CICS region in which this work request (transaction) originated; for example, the region in which the CWXN task ran.")
    cics_ostart: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                     doc="The time at which the originating task, for example the CWXN task, was started.")
    cics_otrannum: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                               doc="The number of the originating task; for example, the CWXN task.")
    cics_otran: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4),
                                                            doc="The transaction ID (TRANSID) of the originating task; for example, the CWXN task.")
    cics_ouserid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                              doc="The originating Userid-2 or Userid-1, for example from CWBA, depending on the originating task.")
    cics_ousercor: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64), doc="The originating user correlator.")
    cics_otcpsvce: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                               doc="The name of the originating TCPIPSERVICE.")
    cics_oportnum: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The port number used by the originating TCPIPSERVICE.")
    cics_ocliport: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The TCP/IP port number of the originating client or Telnet client.")
    cics_otranflg: so.Mapped[Optional[str]] = so.mapped_column(sa.String(18),
                                                               doc="Originating transaction flags, a string of 64 bits used for signaling transaction definition and status information:.")
    cics_ofctynme: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                               doc="The facility name of the originating transaction. If the originating transaction is not associated with a facility, this field is null. The transaction facility type, if any, can be identified using byte 0 of the originating transaction flags, OTRANFLG (370), field.")
    cics_oclipadr: so.Mapped[Optional[str]] = so.mapped_column(sa.String(40),
                                                               doc="The IP address of the originating client or Telnet client.")
    cics_phntwkid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                               doc="The network identifier of the CICS system of an immediately previous task in another CICS system with which this task is associated. See Previous hop data characteristics for more information about previous hop data.")
    cics_phapplid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                               doc="If the task was initiated by a task in another CICS region, PHAPPLID contains the APPLID of the other CICS region, which is obtained from previous hop data.")
    cics_phstart: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                      doc="The start time of the immediately previous task in another CICS system with which this task is associated. See Previous hop data characteristics for more information about previous hop data.")
    cics_phtranno: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                               doc="If the task was initiated by a task in another CICS region, PHTRANNO contains the task number of the immediately previous task in another CICS system with which this task is associated. This value is obtained from previous hop data.")
    cics_phtran: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4),
                                                             doc="The transaction ID (TRANSID) of the immediately previous task in another CICS system with which this task is associated. See Previous hop data characteristics for more information about previous hop data.")
    cics_phcount: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="If the task was initiated by a task in another CICS region, PHCOUNT contains the number of times there has been a request from one CICS system to another CICS system to initiate a task with which this task is associated. See Previous hop data characteristics for more information about previous hop data.")
    cics_eictotct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The total number of EXEC CICS commands issued by the user task.")
    cics_tiasktct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of EXEC CICS ASKTIME commands issued by the user task.")
    cics_titotct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="The total number of EXEC CICS ASKTIME , CONVERTTIME , and FORMATTIME commands issued by the user task.")
    cics_bfdgstct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The total number of EXEC CICS BIF DIGEST commands issued by the user task.")
    cics_bftotct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="The total number of EXEC CICS BIF DEEDIT and BIF DIGEST commands issued by the user task.")
    cics_ecsigect: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of EXEC CICS SIGNAL EVENT commands issued by the user task.")
    cics_ecefopct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of event filter operations performed by the user task.")
    cics_ecevntct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of events captured by the user task.")
    cics_ecsevcct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of synchronous emission events captured by the user task.")
    cics_mpprtxcd: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of policy task rule thresholds that this task has exceeded. This field is all nulls (0x00 bytes) if no thresholds have been exceeded or if the task has had no task rules applied to it.")
    cics_ncgetct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="The total number of requests to a named counter server to satisfy EXEC CICS GET COUNTER and EXEC CICS GET DCOUNTER commands issued by the user task.")
    cics_mpsrect: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="The number of times that policy system rules have been evaluated for the task.")
    cics_mpsract: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="The number of times that policy system rules that have been evaluated true and have triggered an action. This field is all nulls (0x00 bytes) if no system rules have been evaluated true.")
    cics_ptstart: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                      doc="The start time of the immediately previous or parent task in the same CICS system with which the task is associated. See Previous transaction data characteristics for more information about previous transaction data.")
    cics_pttranno: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                               doc="The task number of the immediately previous or parent task in the same CICS system with which the task is associated. See Previous transaction data characteristics for more information about previous transaction data.")
    cics_pttran: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4),
                                                             doc="The transaction ID (TRANSID) of the immediately previous or parent task in the same CICS system with which the task is associated. See Previous transaction data characteristics for more information about previous transaction data.")
    cics_ptcount: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="The number of times there has been a request from one task to initiate another task in the same CICS system with which this task is associated, such as by a RUN TRANSID or START command. This is effectively the task depth in the local region when using the RUN TRANSID command, or the START command when a new point of origin is not created. See Previous transaction data characteristics for more information about previous transaction data.")


class DfhdataBase(AbstractConcreteBase):
    """Abstract class for structure Dfhdata - Performance data in group DFHDATA."""

    data_imsreqct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of IMS (DBCTL) requests issued by the user task.")
    data_db2reqct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The total number of Db2 EXEC SQL and Instrumentation Facility Interface (IFI) requests issued by the user task.")
    data_imswait: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="The elapsed time during which the user task waited for DBCTL to service the IMS requests issued by the user task.")
    data_db2rdyqw: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="The elapsed time during which the user task waited for a Db2 thread to become available.")
    data_db2conwt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="The elapsed time during which the user task waited for a Db2 connection to become available for use with the user task's open TCB.")
    data_wmqreqct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The total number of IBM MQ requests issued by the user task.")
    data_wmqgetwt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="The elapsed time during which the user task waited for IBM MQ to service the user task's GETWAIT request.")
    data_wmqasrbt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="The IBM MQ SRB time this transaction spent processing IBM MQ API requests. Add this field to the transaction CPU time field (USRCPUT) when considering the measurement of the total processor time consumed by a transaction. This field is zero for point-to-point messaging activity, but it is nonzero where IBM MQ API requests result in publish and subscribe type messaging.")


class DfhdestBase(AbstractConcreteBase):
    """Abstract class for structure Dfhdest - Performance data in group DFHDEST."""

    dest_tdgetct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="Number of transient data GET requests issued by the user task.")
    dest_tdputct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="Number of transient data PUT requests issued by the user task.")
    dest_tdpurct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="Number of transient data PURGE requests issued by the user task.")
    dest_tdtotct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="Total number of transient data requests issued by the user task. This field is the sum of TDGETCT, TDPUTCT, and TDPURCT.")
    dest_tdiowtt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="Elapsed time in which the user waited for VSAM transient data I/O. For more information, see Clocks and time stamps and Transaction wait (suspend) times in Reference.")
    dest_tdilwtt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="The elapsed time for which the user task waited for an intrapartition transient data lock (TDIPLOCK). For more information, see Clocks and time stamps and Transaction wait (suspend) times in Reference. For more information about tasks suspended on resource type TDIPLOCK, see Resource type TDIPLOCK: waits for transient data intrapartition requests.")
    dest_tdelwtt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="The elapsed time for which the user task waited for an extrapartition transient data lock (TDEPLOCK). For more information, see Clocks and time stamps and Transaction wait (suspend) times in Reference.")


class DfhdochBase(AbstractConcreteBase):
    """Abstract class for structure Dfhdoch - Performance data in group DFHDOCH."""

    doch_dhdelct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="The number of document handler DELETE requests issued by the user task.")
    doch_dhcrect: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="The number of document handler CREATE requests issued by the user task.")
    doch_dhinsct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="The number of document handler INSERT requests issued by the user task.")
    doch_dhsetct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="The number of document handler SET requests issued by the user task.")
    doch_dhretct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="The number of document handler RETRIEVE requests issued by the user task.")
    doch_dhtotct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="The total number of document handler requests issued by the user task.")
    doch_dhtotdcl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The total length of all documents created by the user task.")


class DfhfepiBase(AbstractConcreteBase):
    """Abstract class for structure Dfhfepi - Performance data in group DFHFEPI."""

    fepi_szalloct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Number of conversations allocated by the user task. This number is incremented for each FEPI ALLOCATE POOL or FEPI CONVERSE POOL.")
    fepi_szrcvct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="Number of FEPI RECEIVE requests made by the user task. This number is also incremented for each FEPI CONVERSE request.")
    fepi_szsendct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Number of FEPI SEND requests made by the user task. This number is also incremented for each FEPI CONVERSE request.")
    fepi_szstrtct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Number of FEPI START requests made by the user task.")
    fepi_szchrout: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Number of characters sent through FEPI by the user task.")
    fepi_szchrin: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="Number of characters received through FEPI by the user task.")
    fepi_szwait: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                               doc="Elapsed time in which the user task waited for all FEPI services. For more information, see Clocks and time stamps, and Transaction wait (suspend) times in Reference.")
    fepi_szallcto: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Number of times the user task timed out while waiting to allocate a conversation.")
    fepi_szrcvto: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="Number of times the user task timed out while waiting to receive data.")
    fepi_sztotct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="Total number of all FEPI API and SPI requests made by the user task.")


class DfhfileBase(AbstractConcreteBase):
    """Abstract class for structure Dfhfile - Performance data in group DFHFILE."""

    file_fcgetct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="Number of file GET requests issued by the user task.")
    file_fcputct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="Number of file PUT requests issued by the user task.")
    file_fcbrwct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="Number of file browse requests issued by the user task. This number excludes the START and END browse requests.")
    file_fcaddct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="Number of file ADD requests issued by the user task.")
    file_fcdelct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="Number of file DELETE requests issued by the user task.")
    file_fciowtt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="Elapsed time in which the user task waited for file I/O. For more information, see Clocks and time stamps, and Transaction wait (suspend) times in Reference.")
    file_fcamct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                             doc="Number of times the user task invoked file access-method interfaces. This number excludes requests for OPEN and CLOSE.")
    file_fctotct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="Total number of file control requests issued by the user task. This number excludes any request for OPEN, CLOSE, ENABLE, or DISABLE of a file.")
    file_rlswait: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="Elapsed time in which the user task waited for RLS file I/O. For more information, see Clocks and time stamps and Transaction wait (suspend) times in Reference.")
    file_rlscput: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="For RLS requests issued from the QR TCB:.")
    file_cfdtwait: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="The elapsed time in which the user task waited for a data table access request to the Coupling Facility Data Table server to complete. For more information, see Clocks and time stamps, and Transaction wait (suspend) times in Reference.")
    file_fcxcwtt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="The elapsed time in which the user task waited for exclusive control of a VSAM control interval. This field counts time spent waiting on resource type FCXCSUSP, FCXDSUSP, FCXCPROT, or FCXDPROT. For more information, see Clocks and time stamps, and Transaction wait (suspend) times in Reference.")
    file_fcvswtt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="The elapsed time in which the user task waited for a VSAM string. This field counts time spent waiting on resource type FCPSSUSP or FCSRSUSP. For more information, see Clocks and time stamps and Transaction wait (suspend) times in Reference.")


class DfhjourBase(AbstractConcreteBase):
    """Abstract class for structure Dfhjour - Performance data in group DFHJOUR."""

    jour_jciowtt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="Elapsed time for which the user task waited for journal (logstream) I/O. For more information, see Clocks and time stamps, and Transaction wait (suspend) times in Reference.")
    jour_jnlwrtct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Number of journal write requests issued by the user task.")
    jour_logwrtct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Number of CICS log stream write requests issued by the user task.")


class DfhmappBase(AbstractConcreteBase):
    """Abstract class for structure Dfhmapp - Performance data in group DFHMAPP."""

    mapp_bmsmapct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Number of BMS MAP requests issued by the user task. This field corresponds to the number of RECEIVE MAP requests that did not incur a terminal I/O, and the number of RECEIVE MAP FROM requests.")
    mapp_bmsinct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="Number of BMS IN requests issued by the user task. This field corresponds to the number of RECEIVE MAP requests that incurred a terminal I/O.")
    mapp_bmsoutct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Number of BMS OUT requests issued by the user task. This field corresponds to the number of SEND MAP requests.")
    mapp_bmstotct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Total number of BMS requests issued by the user task. This field is the sum of BMS RECEIVE MAP, RECEIVE MAP FROM, SEND MAP, SEND TEXT, and SEND CONTROL requests issued by the user task.")


class DfhotelBase(AbstractConcreteBase):
    """Abstract class for structure Dfhotel - Performance data in group DFHOTEL."""

    otel_oteltid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(32),
                                                              doc="The OpenTelemetry (OTel) trace identifier. This field is null if there is no OTel data associated with the task.")
    otel_otelpid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(16),
                                                              doc="OTel parent span id. This field is null if there is no OTel data associated with the task.")
    otel_otelsid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(16),
                                                              doc="OTel span id. This field is null if there is no OTel data associated with the task.")
    otel_otelmisc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(18),
                                                               doc="OTel miscellaneous flags, a string of 64 bits.")


class DfhprogBase(AbstractConcreteBase):
    """Abstract class for structure Dfhprog - Performance data in group DFHPROG."""

    prog_pclinkct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Number of program LINK and INVOKE APPLICATION requests issued by the user task, including the link to the first program of the user task. This field does not include program LINK URM (userreplaceable module) requests.")
    prog_pcxctlct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Number of program XCTL requests issued by the user task.")
    prog_pcloadct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Number of program LOAD requests issued by the user task.")
    prog_pgmname: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                              doc="The name of the first program called at transaction attach-time.")
    prog_pclurmct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Number of program LINK URM (user-replaceable module) requests issued by, or on behalf of, the user task.")
    prog_pcdplct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="Number of distributed program link (DPL) requests issued by the user task.")
    prog_abcodeo: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="Original abend code.")
    prog_abcodec: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="Current abend code.")
    prog_pcloadtm: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="Elapsed time in which the user task waited for fetches from DFHRPL or dynamic LIBRARY concatenations. Only fetches for programs with installed program definitions or autoinstalled as a result of application requests are included in this figure. However, installed programs in the LPA are not included (because they do not incur a physical fetch from a library). For more information about program load time, see Clocks and time stamps, and Program load time.")
    prog_pcdlcsdl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The total length, in bytes, of the data in the containers of all the distributed program link (DPL) requests issued with the CHANNEL option by the user task. This total includes the length of any headers to the data.")
    prog_pcdlcrdl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The total length, in bytes, of the data in the containers of all DPL RETURN CHANNEL commands issued by the user task. This total includes the length of any headers to the data.")
    prog_pclnkcct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Number of local program LINK and INVOKE APPLICATION requests, with the CHANNEL option, issued by the user task.")
    prog_pcxclcct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Number of program XCTL requests issued with the CHANNEL option by the user task.")
    prog_pcdplcct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Number of program distributed program link (DPL) requests issued with the CHANNEL option by the user task.")
    prog_pcrtncct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Number of remote pseudoconversational RETURN requests, with the CHANNEL option, issued by the user task.")
    prog_pcrtncdl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The total length, in bytes, of the data in the containers of all the remote pseudoconversational RETURN CHANNEL commands issued by the user task. This total includes the length of any headers to the data.")


class DfhrmiBase(AbstractConcreteBase):
    """Abstract class for structure Dfhrmi - Performance data in group DFHRMI."""

    rmi_rmitotal: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="The total elapsed time spent in the CICS Resource Manager Interface (RMI).")
    rmi_rmiother: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="The total elapsed time spent in the CICS RMI for resource manager requests other than Db2, DBCTL, EXEC DLI, IBM MQ, CICSPlex SM, and CICS TCP/IP socket requests.")
    rmi_rmidb2: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="The total elapsed time spent in the CICS RMI for Db2 requests.")
    rmi_rmidbctl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="The total elapsed time spent in the CICS RMI for DBCTL requests.")
    rmi_rmiexdli: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="The total elapsed time spent in the CICS RMI for EXEC DLI requests.")
    rmi_rmimqm: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="The total elapsed time spent in the CICS RMI for IBM MQ requests.")
    rmi_rmicpsm: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                               doc="The total elapsed time spent in the CICS RMI for CICSPlex SM requests.")
    rmi_rmitcpip: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="The total elapsed time spent in the CICS RMI for CICS TCP/IP socket requests.")


class DfhsockBase(AbstractConcreteBase):
    """Abstract class for structure Dfhsock - Performance data in group DFHSOCK."""

    sock_soiowtt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="The elapsed time the user task spent waiting for any socket I/O to complete. This time includes time that the task the spent on send and receive calls. It applies to inbound and outbound sockets. For more information, see Clocks and time stamps and Transaction wait (suspend) times in Reference.")
    sock_sobyenct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of bytes encrypted by the secure sockets layer for the user task.")
    sock_sobydect: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of bytes decrypted by the secure sockets layer for the user task.")
    sock_tcpsrvce: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                               doc="The TCP/IP service name that attached the user task.")
    sock_portnum: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="The TCP/IP port number of the TCP/IP service that attached the user task.")
    sock_isalloct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of allocate session requests that are issued by the user task for sessions that use IPIC.")
    sock_soextrct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of EXTRACT TCPIP and EXTRACT CERTIFICATE requests issued by the user task.")
    sock_socnpsct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The total number of requests made by the user task to create an outbound socket.")
    sock_sonpshwm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The peak number of outbound sockets owned by the user task.")
    sock_sorcvct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="The total number of receive requests issued for outbound sockets (persistent and nonpersistent) by the user task.")
    sock_sochrin: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="The total number of bytes received on outbound sockets by the user task.")
    sock_sosendct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The total number of send requests issued for outbound sockets (persistent and nonpersistent) by the user task.")
    sock_sochrout: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The total number of bytes sent on outbound sockets by the user task.")
    sock_sototct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="The total number of socket requests issued by the user task.")
    sock_sooiowtt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="The elapsed time that the user task spent waiting for a socket to be created by the socket manager when CICS is at the MAXSOCKETS limit. This field is not used because no callers within CICS choose to wait for a socket to become available when CICS is at the MAXSOCKETS limit.")
    sock_isiowtt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="The elapsed time for which a user task waited for control at this end of an IPIC connection.")
    sock_somsgin1: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of inbound socket receive requests that are issued by the user task.")
    sock_sochrin1: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of characters that are received by inbound socket receive requests that are issued by the user task.")
    sock_somsgou1: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of inbound socket send requests issued by the user task.")
    sock_sochrou1: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of characters that are sent by inbound socket send requests that are issued by the user task.")
    sock_isipicnm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                               doc="The name of the IPIC connection for the TCP/IP service that attached the user task.")
    sock_clipaddr: so.Mapped[Optional[str]] = so.mapped_column(sa.String(40),
                                                               doc="The IP address of the client or Telnet client.")
    sock_isalwtt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="The elapsed time for which a user task waited for an allocate request for an IPIC session. For more information, see Clocks and time stamps and Transaction wait (suspend) times in Reference.")
    sock_socipher: so.Mapped[Optional[str]] = so.mapped_column(sa.String(10),
                                                               doc="Identifies the code for the cipher suite that was selected during the initial handshake for use on the inbound connection, for example X'0000002F'. For a list of the cipher suites that are supported by CICS and z/OS and their codes, see Cipher Suite Definitions in z/OS Cryptographic Services System SSL Programming.")
    sock_clipport: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The port number of the client or Telnet client.")
    sock_soconmsg: so.Mapped[Optional[str]] = so.mapped_column(sa.String(10),
                                                               doc="Indicates whether the task processed the first message for establishing a new connection for a client. This field helps you measure how often a new socket connection is created.")
    sock_sotlslvl: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                               doc="Identifies the TLS protocol that was selected during the initial handshake for use on the inbound connection.")
    sock_soflag: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                             doc="Socket flags, a string of 32 bits used for socket status information. Bit 0 and Bit 1 cannot both be set to the value 1 at the same time.")


class DfhstorBase(AbstractConcreteBase):
    """Abstract class for structure Dfhstor - Performance data in group DFHSTOR."""

    stor_scusrhwm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Maximum amount (high-water mark) of user storage allocated to the user task below the 16 MB line.")
    stor_scugetct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Number of user-storage GETMAIN requests issued by the user task for storage below the 16 MB line.")
    stor_scusrstg: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                               doc="Storage occupancy of the user task below the 16 MB line. This measures the area under the curve of storage in use against elapsed time. For more information about storage occupancy, see Storage occupancy counts.")
    stor_scugetct_a: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                 doc="Number of user-storage GETMAIN requests issued by the user task for storage above the 16 MB line.")
    stor_scusrhwm_a: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                 doc="Maximum amount (high-water mark) of user storage allocated to the user task above the 16 MB line.")
    stor_scusrstg_a: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="Storage occupancy of the user task above the 16 MB line. This measures the area under the curve of storage in use against elapsed time. For more information, see Storage occupancy counts.")
    stor_sc24chwm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Maximum amount (high-water mark) of user storage allocated to the user task below the 16 MB line.")
    stor_sccgetct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Number of user-storage GETMAIN requests issued by the user task for storage below the 16 MB line.")
    stor_sc24cocc: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                               doc="Storage occupancy of the user task below the 16 MB line. This measures the area under the curve of storage in use against elapsed time. For more information, see Storage occupancy counts.")
    stor_sc31chwm: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                               doc="Maximum amount (high-water mark) of user storage allocated to the user task above the 16 MB line.")
    stor_sccgetct_a: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="Number of user-storage GETMAIN requests issued by the user task for storage above the 16 MB line.")
    stor_sc31cocc: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                               doc="Storage occupancy of the user task above the 16 MB line. This measures the area under the curve of storage in use against elapsed time. For more information, see Storage occupancy counts.")
    stor_sc64cgct: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                               doc="Number of user-storage GETMAIN requests issued by the user task for storage above the bar.")
    stor_sc64chwm: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                               doc="Maximum amount (high-water mark) of user storage, rounded up to the next 4K, allocated to the user task above the bar.")
    stor_sc64ugct: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                               doc="Number of user-storage GETMAIN requests issued by the user task for storage above the bar.")
    stor_sc64uhwm: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                               doc="Maximum amount (high-water mark) of user storage, rounded up to the next 4K, allocated to the user task above the bar.")
    stor_sc24sgct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Number of storage GETMAIN requests issued by the user task for shared storage below the 16 MB line.")
    stor_sc24gshr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Number of bytes of shared storage obtained by the user task by using a GETMAIN request below the 16 MB line.")
    stor_sc24fshr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Number of bytes of shared storage released by the user task by using a FREEMAIN request below the 16 MB line.")
    stor_sc31sgct: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                               doc="Number of storage GETMAIN requests issued by the user task for shared storage above the 16 MB line.")
    stor_sc31gshr: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                               doc="Number of bytes of shared storage obtained by the user task by using a GETMAIN request above the 16 MB line.")
    stor_sc31fshr: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                               doc="Number of bytes of shared storage released by the user task by using a FREEMAIN request above the 16 MB line.")
    stor_sc64sgct: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                               doc="Number of storage GETMAIN requests issued by the user task for shared storage above the bar.")
    stor_sc64gshr: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                               doc="Amount of shared storage obtained by the user task by using a GETMAIN request above the bar. The total number of bytes obtained is rounded up to the next 4096 bytes, and the resulting number of 4K pages is displayed.")
    stor_sc64fshr: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                               doc="Amount of shared storage released by the user task by using a FREEMAIN request above the bar. The total number of bytes obtained is rounded up to the next 4096 bytes, and the resulting number of 4K pages is displayed.")
    stor_pcstghwm: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                               doc="Maximum amount (high-water mark) of program storage in use by the user task both above and below the 16 MB line.")
    stor_pc24bhwm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Maximum amount (high-water mark) of program storage in use by the user task below the 16 MB line. This field is a subset of PCSTGHWM (field id 087) that resides below the 16 MB line.")
    stor_pc31rhwm: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                               doc="Maximum amount (high-water mark) of program storage in use by the user task above the 16 MB line, in the extended read-only dynamic storage area (ERDSA). This field is a subset of PC31AHWM (field id 139) that resides in the ERDSA.")
    stor_pc31ahwm: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                               doc="Maximum amount (high-water mark) of program storage in use by the user task above the 16 MB line. This field is a subset of PCSTGHWM (field id 087) that resides above the 16 MB line.")
    stor_pc31chwm: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                               doc="Maximum amount (high-water mark) of program storage in use by the user task above the 16 MB line, in the extended CICS dynamic storage area (ECDSA). This field is a subset of PC31AHWM (139) that resides in the EPCDSA.")
    stor_pc24chwm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Maximum amount (high-water mark) of program storage in use by the user task below the 16 MB line, in the CICS dynamic storage area (CDSA). This field is a subset of PC24BHWM (108) that resides in the PCDSA.")
    stor_pc24shwm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Maximum amount (high-water mark) of program storage in use by the user task below the 16 MB line, in the shared dynamic storage area (SDSA). This field is a subset of PC24BHWM (108) that resides in the PUDSA.")
    stor_pc31shwm: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                               doc="Maximum amount (high-water mark) of program storage in use by the user task above the 16 MB line, in the extended shared dynamic storage area (ESDSA). This field is a subset of PC31AHWM (139) that resides in the EPUDSA.")
    stor_pc24rhwm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Maximum amount (high-water mark) of program storage in use by the user task below the 16 MB line, in the read-only dynamic storage area (RDSA). This field is a subset of PC24BHWM (108) that resides in the RDSA.")


class DfhsyncBase(AbstractConcreteBase):
    """Abstract class for structure Dfhsync - Performance data in group DFHSYNC."""

    sync_spsyncct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Number of SYNCPOINT requests issued during the user task.")
    sync_synctime: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="Total elapsed time for which the user task was dispatched and was processing syncpoint requests.")
    sync_srvsywtt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="Total elapsed time in which the user task waited for syncpoint or resynchronization processing using the Coupling Facility data tables server to complete.")
    sync_syncdly: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="The elapsed time in which the user task waited for a syncpoint request to be issued by its parent transaction. The user task was executing as a result of the parent task issuing a CICS BTS run-process or run-activity request to execute a process or activity synchronously. For more information, see Clocks and time stamps, and Transaction wait (suspend) times in Reference.")
    sync_otsindwt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="The elapsed time in which the user task was dispatched or suspended indoubt (or both) while processing a syncpoint for an Object Transaction Service (OTS) syncpoint request. For more information, see Clocks and time stamps, and Transaction wait (suspend) times in Reference.")


class DfhtaskBase(AbstractConcreteBase):
    """Abstract class for structure Dfhtask - Performance data in group DFHTASK."""

    task_ttype: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4),
                                                            doc="Transaction start type. The high-order bytes (0 and 1) are set as follows:.")
    task_usrdispt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="Total elapsed time during which the user task was dispatched on each CICS TCB under which the task ran. The TCB modes managed by the CICS dispatcher are: QR, RO, CO, FO, SZ ,RP, SL, SP, SO, EP, L8, L9, S8, TP, T8, X8, X9, and D2. Be aware that, for each CICS release, new TCB modes might be added to this list, or obsolete TCB modes might be removed. For more information about dispatch time and CPU time, see Transaction response time, dispatch time, and CPU time.")
    task_usrcput: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="Processor time for which the user task was dispatched on each CICS TCB under which the task ran. The TCB modes managed by the CICS dispatcher are: QR, RO, CO, FO, SZ, RP, SL, SP, SO, EP, L8, L9,.")
    task_susptime: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="Total elapsed wait time for which the user task was suspended by the dispatcher. This wait time includes these values:.")
    task_xsnlnact: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of QUERY SECURITY LOGMESSAGE(NOLOG) requests that succeeded but returned no authority on READ, UPDATE, CONTROL or ALTER.")
    task_xsnlnfct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of QUERY SECURITY LOGMESSAGE(NOLOG) requests that failed with response code 13 NOTFND and reason code 5 or 8.")
    task_icpuinct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Number of interval control START or INITIATE requests during the user task.")
    task_taskflag: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Task error flags, a string of 32 bits used for signaling unusual conditions occurring during the user task:.")
    task_icstacct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Total number of local interval control START requests, with the CHANNEL option, issued by the user task.")
    task_ictotct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="Total number of Interval Control Start, Cancel, Delay, and Retrieve requests issued by the user task.")
    task_trngrpid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(58),
                                                               doc="The transaction group ID is assigned at transaction attach time, and can be used to correlate the transactions that CICS runs for the same incoming work request; for example, the CWXN and CWBA transactions for Web requests. This transaction group ID relationship is useful when applied to the.")
    task_netuowpx: so.Mapped[Optional[str]] = so.mapped_column(sa.String(20),
                                                               doc="Fully qualified name by which the originating system is known to the z/OS Communications Server network. This name is assigned at attach time using either the netname derived from the TCT (when the task is attached to a local terminal) or the netname passed as part of an ISC APPC or IRC attach header. At least three padding bytes (X'00') are present at the end of the name.")
    task_netuowsx: so.Mapped[Optional[str]] = so.mapped_column(sa.String(18),
                                                               doc="Name by which the network unit of work ID is known in the originating system. This name is assigned at attach time using either an STCK-derived token (when the task is attached to a local terminal), or the network unit of work ID passed as part of an ISC (APPC) or IRC (MRO) attach header.")
    task_dispwtt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="Elapsed time for which the user task waited for redispatch. This time is the aggregate of the wait times between each event completion and user-task redispatch.")
    task_tranpri: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="Transaction priority when monitoring of the task was initialized (low-order byte-3).")
    task_gnqdelay: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="The elapsed time waiting for a CICS task control global enqueue. For more information, see Clocks and time stamps.")
    task_brdgtran: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4),
                                                               doc="Bridge listener transaction identifier. For CICS 3270 Bridge transactions, this field is the name of the Bridge listener transaction that attached the user task.")
    task_dspdelay: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="The elapsed time waiting for first dispatch.")
    task_tcldelay: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="The elapsed time waiting for first dispatch, which was delayed because of the limits set for the transaction class of this transaction, TCLSNAME (166), being reached. For more information, see Clocks and time stamps. This field is a component of the first dispatch delay, DSPDELAY (125), field.")
    task_mxtdelay: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="The elapsed time waiting for the first dispatch, which was delayed because of the limits set by the system parameter, MXT, being reached. The field is a component of the first dispatch delay, DSPDELAY (125), field.")
    task_lmdelay: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="The elapsed time that the user task waited to acquire a lock on a resource. A user task cannot explicitly acquire a lock on a resource, but many CICS modules lock resources on behalf of user tasks using the CICS lock manager (LM) domain.")
    task_enqdelay: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="The elapsed time waiting for a CICS task control local enqueue. For more information, see Clocks and time stamps. This field is a component of the task suspend time, SUSPTIME (014), field.")
    task_rmuowid: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                      doc="The identifier of the unit of work (unit of recovery) for this task. Unit of recovery values are used to synchronize recovery operations among CICS and other resource managers, such as IMS and Db2.")
    task_fctyname: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4),
                                                               doc="Transaction facility name. This field is null if the transaction is not associated with a facility. The transaction facility type (if any) can be identified using byte 0 of the transaction flags, TRANFLAG , (164) field.")
    task_tranflag: so.Mapped[Optional[str]] = so.mapped_column(sa.String(18),
                                                               doc="Transaction flags, a string of 64 bits used for signaling transaction definition and status information:.")
    task_tclsname: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                               doc="Transaction class name. This field is null if the transaction is not in a TRANCLASS.")
    task_rmitime: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="The total elapsed time spent in the CICS Resource Manager Interface (RMI). For more information, see Clocks and time stamps, Transaction wait (suspend) times in Reference, and RMI elapsed and suspend time.")
    task_rmisusp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="The total elapsed time that the task was suspended by the CICS dispatcher while in the CICS Resource Manager Interface (RMI). For more information, see Clocks and time stamps, Transaction wait (suspend) times in Reference, and RMI elapsed and suspend time. The field is a component of the task suspend time, SUSPTIME (014), field and also the RMITIME (170) field.")
    task_wtexwait: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="The elapsed time that the user task waited for one or more ECBs, passed to CICS by the user task using the EXEC CICS WAIT EXTERNAL ECBLIST command, to be posted by the MVS POST command. The user task can wait on one or more ECBs. If it waits on more than one, it is dispatchable as soon as one of the ECBs is posted. For more information, see Clocks and time stamps and Transaction wait (suspend) times in Reference. This field is a component of the task suspend time, SUSPTIME (014), field.")
    task_wtcewait: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="The elapsed time that the user task waited for one of these events:.")
    task_icdelay: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="The elapsed time that the user task waited as a result of issuing one of the following commands:.")
    task_gvupwait: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="The elapsed time that the user task waited as a result of giving up control to another task. A user task can give up control in many ways. Some examples are application programs that use one or more of the following EXEC CICS API or SPI commands:.")
    task_tclstsks: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Total number of active and queued tasks, including this task, in the associated TRANCLASS when the task was attached. This field does not apply if the transaction is not in a TRANCLASS.")
    task_rrmsurid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(16),
                                                               doc="RRMS/MVS unit-of-recovery ID (URID).")
    task_rrmswait: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="The elapsed time in which the user task waited indoubt using resource recovery services for EXCI.")
    task_rqrwait: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="The elapsed time during which the request receiver user task CIRR (or user specified transaction ID) waited for any outstanding replies to be satisfied.")
    task_rqpwait: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="The elapsed time during which the request processor user task CIRP waited for any outstanding replies to be satisfied. This field is a component of the task suspend time, SUSPTIME (014), field.")
    task_otstid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(128),
                                                             doc="This field is the first 128 bytes of the Object Transaction Service (OTS) Transaction ID (TID).")
    task_runtrwtt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="The elapsed time in which the user task waited for completion of a transaction that ran as a result of the user task issuing a CICS BTS run process request and a run activity request synchronously.")
    task_dschmdly: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="The elapsed time in which the user task waited for redispatch after a CICS Dispatcher change-TCB mode request was issued by or on behalf of the user task. For example, a change-TCB mode request from a CICS L8 or S8 mode TCB back to the CICS QR mode TCB might have to wait for the QR TCB because another task is currently dispatched on the QR TCB. The period count component of DSCHMDLY represents the number of change-TCB mode requests. This field is a component of the task suspend time, SUSPTIME (014), field. For more information, see Clocks and time stamps and Transaction wait (suspend) times in Reference.")
    task_qrmoddly: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="The elapsed time for which the user task waited for redispatch on the CICS QR mode TCB. This time is the aggregate of the wait times between each event completion and user-task redispatch. This field does not include the elapsed time spent waiting for the first dispatch. The QRMODDLY field is a component of the task suspend time, SUSPTIME (014), field, and also the redispatch wait, DISPWTT (102), field.")
    task_maxotdly: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="The elapsed time in which the user task waited to obtain a CICS L8 or L9 mode open TCB, because the region had reached the limit set by CICS for these TCBs. L8 and L9 mode open TCBs are used by OPENAPI application programs or by task-related user exit programs that have been enabled with the OPENAPI option, for example, the CICS-Db2 adapter, when CICS connects to Db2 Version 6 or later and the CICS-MQ adapter, when CICS connects to Websphere MQ Version 6 or later.")
    task_tcbattct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of CICS TCBs attached by or on behalf of the user task.")
    task_dstcbhwm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The peak number of CICS open TCBs (in TCB modes L8, L9, S8, T8, X8, and X9) that have been concurrently allocated to the user task.")
    task_jvmtime: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="The total elapsed time spent in the JVM by the user task. For more information, see JVM elapsed time, suspend time, and cleanup time.")
    task_jvmsusp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="The elapsed time for which the user task was suspended by the CICS dispatcher while running in the JVM. For more information, see JVM elapsed time, suspend time, and cleanup time. This field is a component of the task suspend time, SUSPTIME (014), field.")
    task_qrdispt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="The elapsed time for which the user task was dispatched on the CICS QR TCB. For more information, see Clocks and time stamps.")
    task_qrcput: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                               doc="The processor time for which the user task was dispatched on the CICS QR TCB. For more information, see Clocks and time stamps.")
    task_msdispt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="Elapsed time for which the user task was dispatched on each CICS TCB. The CICS TCB modes are used as follows:.")
    task_mscput: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                               doc="The processor time for which the user task was dispatched on each CICS TCB. The usage of each CICS TCB is shown in the description for field MSDISPT (field ID 257 in group DFHTASK). For more information, see Clocks and time stamps.")
    task_l8cput: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                               doc="The processor time during which the user task was dispatched by the CICS dispatcher domain on a CICS L8 mode TCB. When a transaction starts an OPENAPI application program defined with EXECKEY=CICS, or a task-related user exit program that has been enabled with the OPENAPI option, CICS allocates a CICS L8 mode TCB to the task. (An L8 mode TCB can also be allocated if the OPENAPI program is defined with EXECKEY=USER, but the storage protection facility is inactive.) After a task has been allocated an L8 mode TCB, that same TCB remains associated with the task until the transaction is detached. For more information on this field, see Clocks and time stamps.")
    task_s8cput: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                               doc="The processor time during which the user task was dispatched by the CICS dispatcher domain on a CICS S8 mode TCB. A transaction is allocated a CICS S8 mode TCB when it uses the secure sockets layer (SSL) during client certificate negotiation. The S8 mode TCB remains associated with the same task for the life of the SSL request. For more information, see Clocks and time stamps.")
    task_ky8dispt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="The total elapsed time during which the user task was dispatched by the CICS dispatcher on a CICS Key 8 mode TCB:.")
    task_ky8cput: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="The processor time during which the user task was dispatched by the CICS dispatcher on a CICS Key 8 mode TCB. The usage of the CICS Key 8 mode TCBs is shown in the description for field KY8DISPT (field ID 262 in group DFHTASK). This field is a component of the task CPU time field, USRCPUT (field ID 008 in group DFHTASK).")
    task_ky9dispt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="The total elapsed time during which the user task was dispatched by the CICS dispatcher on a CICS Key 9 mode TCB:.")
    task_ky9cput: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="The processor time during which the user task was dispatched by the CICS dispatcher on a CICS Key 9 mode TCB. The usage of the CICS Key 9 mode TCBs is shown in the description for field KY9DISPT (field ID 264 in group DFHTASK). This field is a component of the task CPU time field, USRCPUT (field ID 008 in group DFHTASK).")
    task_l9cput: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                               doc="The processor time during which the user task was dispatched by the CICS dispatcher domain on a CICS L9 mode TCB. When a transaction calls an OPENAPI application program that is defined with EXECKEY=USER it is allocated and uses a CICS L9 mode TCB. If the storage protection facility is.")
    task_dstcbmwt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="The elapsed time that the user task spent in TCB mismatch waits; that is, waiting because no available TCB matched the request, but at least one non matching TCB was free.")
    task_rodispt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="The elapsed time during which the user task was dispatched by the CICS dispatcher on the CICS RO mode TCB. The RO TCB is used for loading programs, unless the command to load the program (EXEC CICS LOAD, XCTL, or LINK) is issued by an application that is currently running on an open TCB. In that situation, the open TCB is used to load the program instead of the RO TCB. The CICS RO mode TCB is also used for opening and closing CICS data sets, issuing RACF calls, and similar tasks. This field is a component of the task dispatch time field, USRDISPT (group name: DFHTASK, field ID: 007) and the task miscellaneous TCB dispatch time field, MSDISPT (group name: DFHTASK, field ID: 257).")
    task_rocput: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                               doc="The processor time during which the user task was dispatched by the CICS dispatcher on the CICS RO mode TCB. The RO TCB is used for loading programs, unless the command to load the program (EXEC CICS LOAD, XCTL, or LINK) is issued by an application that is currently running on an open TCB. In that situation, the open TCB is used to load the program instead of the RO TCB. The CICS RO mode TCB is also used for opening and closing CICS data sets, issuing RACF calls, and similar tasks. This field is a component of the task CPU time field, USRCPUT (group name: DFHTASK, field ID: 008) and the task miscellaneous TCB CPU time field, MSCPUT (group name: DFHTASK, field ID: 258).")
    task_x8cput: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                               doc="The processor time during which the user task was dispatched by the CICS dispatcher domain on a CICS X8 mode TCB. When a transaction calls a C or C++ program that was compiled with the XPLINK option, and that is defined with EXECKEY=CICS, it is allocated and uses a CICS X8 mode TCB. An X8 mode TCB can also be allocated if the program is defined with EXECKEY=USER, but the storage protection facility is inactive. After a task has been allocated an X8 mode TCB, that same TCB remains associated with the task until the program completes. This field is a component of the total task CPU time field, USRCPUT (field ID 008 in group DFHTASK), and the task key 8 CPU time field, KY8CPUT (field ID 263 in group DFHTASK).")
    task_x9cput: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                               doc="The processor time during which the user task was dispatched by the CICS dispatcher domain on a CICS X9 mode TCB. When a transaction calls a C or C++ program that was compiled with the XPLINK option, and that is defined with EXECKEY=USER, it is allocated and uses a CICS X9 mode TCB. (If the storage protection facility is inactive, an X8 mode TCB is used instead of an X9 mode TCB.) After a task has been allocated an X9 mode TCB, that same TCB remains associated with the task until the program completes. This field is a component of the total task CPU time field, USRCPUT (field ID 008 in group DFHTASK), and the task key 9 CPU time field, KY9CPUT (field ID 265 in group DFHTASK).")
    task_jvmitime: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="The elapsed time spent initializing the JVM environment. For more information, see Clocks and time stamps.")
    task_smmvsswt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="The time that the user task waited because MVS user region or extended user region was short on storage. For more information, see Transaction wait (suspend) times in Reference. This field is a component of the task suspend time, SUSPTIME (014), field.")
    task_jvmrtime: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Reserved field, returns zero.")
    task_dsmmscwt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="The elapsed time that the user task spent waiting because no TCB was available and a TCB was not created because of MVS storage constraints. This field is not populated. The field is a component of the task suspend time, SUSPTIME (014), field.")
    task_maxstdly: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="The elapsed time for which the user task waited to obtain a CICS SSL TCB (S8 mode), because the CICS system reached the limit set by the system initialization parameter MAXSSLTCBS. The S8 mode open TCBs are used exclusively by secure sockets layer (SSL) pthread requests issued by or on behalf of a user task. For more information, see Transaction wait (suspend) times in Reference. This field is a component of the task suspend time, SUSPTIME (014), field.")
    task_maxxtdly: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="The elapsed time for which the user task waited to obtain a CICS XP TCB (X8 or X9 mode), because the CICS system reached the limit set by CICS for these types of TCB. The X8 and X9 mode open TCBs are used exclusively by C and C++ programs that were compiled with the XPLINK option. For more information, see Transaction wait (suspend) times in Reference. This field is a component of the task suspend time, SUSPTIME (014), field.")
    task_maxttdly: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="The elapsed time for which the user task waited to obtain a T8 TCB, because the CICS system reached the limit of available threads. The T8 mode open TCBs are used by a JVM server to perform multithreaded processing. Each T8 TCB runs under one thread. The thread limit is 2000 for each CICS region and each JVM server in a CICS region can have up to 256 threads. For more information, see Transaction wait (suspend) times in Reference. This field is a component of the task suspend time, SUSPTIME (014), field. This does not apply to Liberty JVM servers.")
    task_ptpwait: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="The elapsed time for which the user task waited for the 3270 bridge partner transaction to complete. For more information, see Transaction wait (suspend) times in Reference. This field is a component of the task suspend time, SUSPTIME (014), field.")
    task_icstacdl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Total length, in bytes, of the data in the containers of all the locally executed START CHANNEL requests issued by the user task. This total includes the length of any headers to the data.")
    task_icstrcct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Total number of interval control START CHANNEL requests, to be run on remote systems, issued by the user task.")
    task_icstrcdl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Total length, in bytes, of the data in the containers of all the remotely executed START CHANNEL requests issued by the user task. This total includes the length of any headers to the data.")
    task_romoddly: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="The elapsed time for which the user task waited for redispatch on the CICS RO TCB. This time is the aggregate of the wait times between each event completion and user-task redispatch. The ROMODDLY field is a component of the task suspend time, SUSPTIME (014), field, and also the redispatch wait, DISPWTT (102), field.")
    task_somoddly: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="The elapsed time for which the user task waited for redispatch on the CICS SO TCB. This time is the aggregate of the wait times between each event completion and user-task redispatch. The SOMODDLY field is a component of the task suspend time, SUSPTIME (014), field, and also the redispatch wait, DISPWTT (102), field.")
    task_t8cput: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                               doc="The processor time during which the user task was dispatched by the CICS dispatcher domain on a CICS T8 mode TCB. T8 mode TCBs are used by a JVM server to perform multithreaded processing. When a thread is allocated a T8 mode TCB, that same TCB remains associated with the thread until the processing completes. This field is a component of the total task CPU time field, USRCPUT (field ID 008 in group DFHTASK), and the task key 8 CPU time field, KY8CPUT (field ID 263 in group DFHTASK).")
    task_jvmthdwt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="The elapsed time that the user task waited to obtain a JVM server thread because the CICS system had reached the thread limit for a JVM server in the CICS region. This field is a component of the task suspend time, SUSPTIME (014), field. This does not apply to Liberty JVM servers.")
    task_dsapthwt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="The dispatcher allocated pthread wait time. This is the time that the transaction had to wait for a Liberty pthread to be allocated during links to Liberty programs. For more information, see Clocks and time stamps and Transaction wait (suspend) times in Reference. This field is a component of the task suspend time, SUSPTIME (014), field.")
    task_cecmchtp: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4),
                                                               doc="The CEC machine type, in EBCDIC, for the physical hardware environment where the CICS region is running. CEC (central electronics complex) is a commonly used synonym for CPC (central processing complex).")
    task_cecmdlid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(16),
                                                               doc="The CEC model number, in EBCDIC, for the physical hardware environment where the CICS region is running.")
    task_lparname: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                               doc="The name, in EBCDIC, of the logical partition (LPAR) on the processor where the CICS region is running.")
    task_maxtasks: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The MXT or MAXTASKS value, expressed as a number of tasks, for the CICS region at the time the user task was attached.")
    task_curtasks: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The current number of active user transactions in the system at the time the user task was attached.")
    task_xsvfypwd: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="The total elapsed time that the user task spent verifying passwords, password phrases, PassTickets, and MFA tokens.")
    task_cputoncp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="The total task processor time on a standard processor for which the user task was dispatched on each CICS TCB under which the task ran.")
    task_offlcput: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="The total task processor time that was spent on a standard processor but was eligible for offload to a specialty processor (zIIP or zAAP).")
    task_xsvfybas: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="The total elapsed time that the user task spent verifying basic authentication tokens (BASICAUTH).")
    task_xsvfyker: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="The total elapsed time that the user task spent verifying Kerberos tokens (KERBEROS).")
    task_xsvfyjwt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="The total elapsed time that the user task spent verifying JSON web tokens (JWT).")
    task_acapplnm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64),
                                                               doc="The 64-character name of the application in the application context data.")
    task_acplatnm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64),
                                                               doc="The 64-character name of the platform in the application context data.")
    task_acmajver: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The major version of the application in the application context data, expressed as a 4-byte binary value.")
    task_acminver: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The minor version of the application in the application context data, expressed as a 4-byte binary value.")
    task_acmicver: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The micro version of the application in the application context data, expressed as a 4-byte binary value.")
    task_acopernm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64),
                                                               doc="The 64-character name of the operation in the application context data.")
    task_astotct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="The total number of EXEC CICS asynchronous API commands that have been issued by the user task. Includes RUN TRANSID , FETCH CHILD , FETCH ANY , and FREE CHILD commands.")
    task_asrunct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="The number of EXEC CICS RUN TRANSID commands that have been issued by the user task.")
    task_asftchct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of EXEC CICS FETCH CHILD and EXEC CICS FETCH ANY commands that have been issued by the user task.")
    task_asfreect: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of EXEC CICS FREE CHILD commands that have been issued by the user task.")
    task_asftchwt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="The elapsed time that the user task waited for a child task as a result of issuing an EXEC CICS FETCH CHILD or EXEC CICS FETCH ANY command which was not completed.")
    task_asrnatwt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="The elapsed time that the user task was delayed as a result of asynchronous child task limits managed by the asynchronous services domain.")


class DfhtempBase(AbstractConcreteBase):
    """Abstract class for structure Dfhtemp - Performance data in group DFHTEMP."""

    temp_tsiowtt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="Elapsed time for which the user task waited for VSAM temporary storage I/O. For more information, see Clocks and time stamps, and Transaction wait (suspend) times in Reference.")
    temp_tsgetct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="Number of temporary storage GET requests to auxiliary or main temporary storage issued by the user task.")
    temp_tsputact: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Number of PUT requests to auxiliary temporary storage issued by the user task.")
    temp_tsputmct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Number of PUT requests to main temporary storage issued by the user task.")
    temp_tstotct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="Total number of temporary storage requests issued by the user task. This field is the sum of the temporary storage READQ (TSGETCT), READQ shared (TSGETSCT), WRITEQ AUX (TSPUTACT), WRITEQ MAIN (TSPUTMCT), WRITEQ shared (TSPUTSCT), and DELETEQ requests issued by the user task.")
    temp_tsshwait: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="Elapsed time that the user task waited for an asynchronous shared temporary storage request to a temporary storage data server to complete. For more information, see Clocks and time stamps, and Transaction wait (suspend) times in Reference.")
    temp_tsgetsct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Number of temporary storage GET requests from shared temporary storage issued by the user task.")
    temp_tsputsct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Number of temporary storage PUT requests to shared temporary storage issued by the user task.")


class DfhtermBase(AbstractConcreteBase):
    """Abstract class for structure Dfhterm - Performance data in group DFHTERM."""

    term_term: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4),
                                                           doc="Terminal or session identification. This field is null if the task is not associated with a terminal or session.")
    term_tciowtt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="Elapsed time for which the user task waited for input from the terminal operator after issuing a RECEIVE request. For more information, see Clocks and time stamps and Transaction wait (suspend) times in Reference.")
    term_tcmsgin1: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Number of messages received from the principal terminal facility of the task, including LUTYPE6.1 and LUTYPE6.2 (APPC) but not MRO (IRC).")
    term_tcmsgou1: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Number of messages sent to the principal terminal facility of the task, including LUTYPE6.1 and LUTYPE6.2 (APPC) but not MRO (IRC).")
    term_tcmsgin2: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Number of messages received from the LUTYPE6.1 alternate terminal facilities by the user task.")
    term_tcmsgou2: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Number of messages sent to the LUTYPE6.1 alternate terminal facilities by the user task.")
    term_tcalloct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Number of TCTTE ALLOCATE requests issued by the user task for LUTYPE6.2 (APPC), LUTYPE6.1, and IRC sessions.")
    term_tcchrin1: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Number of characters received from the principal terminal facility of the task, including LUTYPE6.1 and LUTYPE6.2 (APPC) but not MRO (IRC).")
    term_tcchrou1: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Number of characters sent to the principal terminal facility of the task, including LUTYPE6.1 and LUTYPE6.2 (APPC) but not MRO (IRC).")
    term_tcchrin2: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Number of characters received from the LUTYPE6.1 alternate terminal facilities by the user task. (Not applicable to ISC APPC.).")
    term_tcchrou2: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Number of characters sent to the LUTYPE6.1 alternate terminal facilities by the user task. (Not applicable to ISC APPC.).")
    term_iriowtt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="Elapsed time for which the user task waited for control at this end of an MRO link. For more information, see Clocks and time stamps and Transaction wait (suspend) times in Reference.")
    term_luname: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                             doc="The z/OS Communications Server SNA logical unit name (if available) of the terminal that is associated with this transaction. If the task is executing in an application-owning or file-owning region, the LUNAME is the generic applid of the originating connection for MRO, LUTYPE6.1, and LUTYPE6.2 (APPC). The LUNAME is blank if the originating connection is an external CICS interface (EXCI).")
    term_lu61wtt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="The elapsed time for which the user task waited for I/O on a LUTYPE6.1 connection or session. This time also includes the waits incurred for conversations across LUTYPE6.1 connections, but not the waits incurred because of LUTYPE6.1 syncpoint flows. For more information, see Clocks and time stamps and Transaction wait (suspend) times in Reference.")
    term_lu62wtt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="The elapsed time for which the user task waited for I/O on a LUTYPE6.2 (APPC) connection or session. This time also includes the waits incurred for conversations across LUTYPE6.2 (APPC) connections, but not the waits incurred because of LUTYPE6.2 (APPC) syncpoint flows. For more information, see Clocks and time stamps and Transaction wait (suspend) times in Reference.")
    term_tcm62in2: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Number of messages received from the alternate facility by the user task for LUTYPE6.2 (APPC) sessions.")
    term_tcm62ou2: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Number of messages sent to the alternate facility by the user task for LUTYPE6.2 (APPC) sessions.")
    term_tcc62in2: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Number of characters received from the alternate facility by the user task for LUTYPE6.2 (APPC) sessions.")
    term_tcc62ou2: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Number of characters sent to the alternate facility by the user task for LUTYPE6.2 (APPC) sessions.")
    term_terminfo: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Terminal or session information for the principal facility of this task, as identified in the 'TERM' field id 002. This field is null if the task is not associated with a terminal or session facility.")
    term_termcnnm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4),
                                                               doc="Terminal session connection name. If the terminal facility associated with this transaction is a session, this field is the name of the owning connection (sysid).")
    term_netid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                            doc="NETID if a network qualified name has been received from the Communications Server. If it is a resource and the network qualified name has not yet been received, NETID is 8 blanks. In all other cases, it is nulls.")
    term_rluname: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                              doc="Real network name if a network qualified name has been received from the Communications Server. In all other cases, this field is the same as LUNAME (field ID 111). For non-Communications Server resources, it is nulls.")
    term_tcalwtt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="The elapsed time for which a user task waited for an allocate request for an MRO (Inter-Region Communication), LU6.1, or LU6.2 session. For more information, see Clocks and time stamps and Transaction wait (suspend) times in Reference.")


class DfhwebbBase(AbstractConcreteBase):
    """Abstract class for structure Dfhwebb - Performance data in group DFHWEBB."""

    webb_wbreadct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of CICS web support READ HTTPHEADER, READ FORMFIELD, and READ QUERYPARM requests issued by the user task.")
    webb_wbwritct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of CICS web support WRITE HTTPHEADER requests issued by the user task.")
    webb_wbrcvct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="The number of CICS web support RECEIVE requests issued by the user task.")
    webb_wbchrin: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="The number of bytes received by the CICS web support RECEIVE requests issued by the user task.")
    webb_wbsendct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of CICS web support SEND requests issued by the user task.")
    webb_wbchrout: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of bytes sent by the CICS web support SEND requests issued by the user task.")
    webb_wbtotct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="The total number of CICS web support requests issued by the user task.")
    webb_wbreprct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of reads from the repository in temporary storage issued by the user task.")
    webb_wbrepwct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of writes to the repository in temporary storage issued by the user task.")
    webb_wbextrct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of CICS web support EXTRACT requests issued by the user task.")
    webb_wbbrwct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="The number of CICS web support browsing requests for HTTPHEADER, FORMFIELD, and QUERYPARM (STARTBROWSE, READNEXT, and ENDBROWSE) issued by the user task.")
    webb_wbredoct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of CICS web support READ HTTPHEADER requests issued by the user task when CICS is an HTTP client.")
    webb_wbwrtoct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of CICS web support WRITE HTTPHEADER requests issued by the user task when CICS is an HTTP client.")
    webb_wbrcvin1: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of CICS web support RECEIVE and CONVERSE requests issued by the user task when CICS is an HTTP client.")
    webb_wbchrin1: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of bytes received by the CICS web support RECEIVE and CONVERSE requests issued by the user task when CICS is an HTTP client. This number includes the HTTP headers for the response.")
    webb_wbsndou1: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of CICS web support SEND and CONVERSE requests issued by the user task when CICS is an HTTP client.")
    webb_wbchrou1: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of bytes sent by the CICS web support SEND and CONVERSE requests issued by the user task when CICS is an HTTP client. This number includes the HTTP headers for the request.")
    webb_wbparsct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of CICS web support PARSE URL requests issued by the user task.")
    webb_wbbrwoct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of CICS web support BROWSE HTTPHEADER requests (STARTBROWSE, READNEXT, and ENDBROWSE) issued by the user task when CICS is an HTTP client.")
    webb_wburiopn: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="The total elapsed time that the user task was processing WEB OPEN URIMAP requests that are issued by the user task. For more information, see Clocks and time stamps.")
    webb_wbiwbsct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of EXEC CICS INVOKE SERVICE and EXEC CICS INVOKE WEBSERVICE requests issued by the user task.")
    webb_wbreprdl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The total length, in bytes, of the data read from the repository in temporary storage by the user task.")
    webb_wbrepwdl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The total length, in bytes, of the data written to the repository in temporary storage by the user task.")
    webb_wburimnm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                               doc="For CICS web support, Atom feeds, and web service applications, the name of the URIMAP resource definition that was mapped to the URI of the inbound request that was processed by this task.")
    webb_wbpiplnm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                               doc="For web service applications, the name of the PIPELINE resource definition that was used to provide information about the message handlers that act on the service request processed by this task.")
    webb_wbatmsnm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                               doc="For Atom feeds, the name of the ATOMSERVICE resource definition that was used to process this task.")
    webb_wbsvcenm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(32),
                                                               doc="For web service applications, the name of the WEBSERVICE resource definition that was used to process this task.")
    webb_wbsvopnm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64),
                                                               doc="For web service applications, the first 64 bytes of the web service operation name.")
    webb_wbprognm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                               doc="For CICS web support, the name of the program from the URIMAP resource definition that was used to provide the application-generated response to the HTTP request processed by this task.")
    webb_wbsfcrct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of EXEC CICS SOAPFAULT CREATE commands issued by the user task.")
    webb_wbsftoct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The total number of EXEC CICS SOAPFAULT ADD , CREATE , and DELETE commands issued by the user task.")
    webb_wbissfct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The total number of SOAP faults received in response to the EXEC CICS INVOKE SERVICE and EXEC CICS INVOKE WEBSERVICE commands issued by the user task.")
    webb_wbsreqbl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="For web service applications, the SOAP request body length.")
    webb_wbsrspbl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="For web service applications, the SOAP response body length.")
    webb_wburircv: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="The total elapsed time that the user task was processing WEB RECEIVE requests and the receiving side of WEB CONVERSE requests that are issued by the user task. The sessions these requests target to are opened by the WEB OPEN URIMAP command. For more information, see Clocks and time stamps.")
    webb_wburisnd: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="The total elapsed time that the user task was processing WEB SEND requests and the sending side of WEB CONVERSE requests that are issued by the user task. The sessions these requests target to are opened by the WEB OPEN URIMAP command. For more information, see Clocks and time stamps.")
    webb_mlxsstdl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The total length of the documents that were parsed using the z/OS XML System Services parser.")
    webb_mlxmltct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of EXEC CICS TRANSFORM commands issued by the user task.")
    webb_njsappnm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(32),
                                                               doc="Node.js application name from which the task was started.")
    webb_wsacblct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of EXEC CICS WSACONTEXT BUILD commands issued by the user task.")
    webb_wsacgtct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of EXEC CICS WSACONTEXT GET commands issued by the user task.")
    webb_wsaepcct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The number of EXEC CICS WSAEPR CREATE commands issued by the user task.")
    webb_wsatotct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The total number of EXEC CICS WS-Addressing commands issued by the user task.")
    webb_wbjsnrql: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="For JSON web service applications, the JSON message request length.")
    webb_wbjsnrpl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="For JSON web service applications, the JSON message response length.")


class DfhwebcBase(AbstractConcreteBase):
    """Abstract class for structure Dfhwebc - Performance data in group DFHWEBC."""

    webc_wbsvinvk: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="The total elapsed time that the user task was processing INVOKE SERVICE requests for WEBSERVICEs. For more information, see Clocks and time stamps.")


class Smf123RequestSummaryBase(AbstractConcreteBase):
    """Abstract class for section Smf123RequestSummary."""

    tasks: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                       doc="Total number of transaction records within the duration.")
    elapsed: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="Total elapsed time of the transactions within the duration.")
    smfmnjbn: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Jobname.")
    smfmnrvn: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4),
                                                          doc="Record version (CICS), format 0VRM (V = version; R = release M = modification).")
    requests: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of requests made.")
    fail: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of failures made.")
    timed_out: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of timed-out requests made.")
    gets: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of GET requests made.")
    posts: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of POST requests made.")
    puts: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of PUT requests made.")
    deletes: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of DELETE requests made.")
    sor_sent_latency_avg: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                        doc="Average latency (in seconds) when z/OS Connect received the request to when sent the request to CICS.")
    sor_sent_latency_max: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                        doc="Maximum latency (in seconds) when z/OS Connect received the request to when sent the request to CICS.")
    sor_sent_latency_reqid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                        doc="The request Id when the maximum latency occurred.")
    sor_sent_latency_zc_entry: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                                   doc="The time the request was received by the z/OS Connect EE server when maximum latency occurred.")
    sor_response_avg: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="Average elapsed time (in seconds) when it took CICS to respond to the requests.")
    sor_response_max: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="Maximum elapsed time (in seconds) when it took CICS to respond to the requests.")
    sor_response_reqid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                    doc="The request Id when the maximum elapsed time occurred.")
    sor_response_zc_entry: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                               doc="The time the request was received by the z/OS Connect EE server when maximum elapsed time.")
    zc_exit_latency_avg: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                       doc="Average elapsed time it took z/OS Connect to respond to the client after it receive the response from CICS.")
    zc_exit_latency_max: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                       doc="Maximum elapsed time it took z/OS Connect to respond to the client.")
    zc_exit_latency_reqid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                       doc="The request Id when the maximum elapsed time respond to the client occurred.")
    zc_exit_latency_zc_entry: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                                  doc="The time the request was received by the z/OS Connect EE server when maximum elapsed time respond to the client occurred.")
    zc_response_avg: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                   doc="Average request elapsed time (in seconds) from z/OS Connect received the request to when sent the response to the client.")
    zc_response_max: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                   doc="Maximum request elapsed time (in seconds) from z/OS Connect recieved the request to when sent the response to the client.")
    zc_response_reqid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                   doc="The request Id when the maximum zc response time occurred.")
    zc_response_zc_entry: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                              doc="The time the request was received by the z/OS Connect EE server when maximum zc response time occurred.")
    zc_time_avg: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                               doc="Average elapsed time it took inside z/OS Connect.")
    zc_time_max: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                               doc="Maximum elapsed time it took inside z/OS Connect.")
    zc_time_reqid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="The request Id when the maximum zc time occurred.")
    zc_time_zc_entry: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="The time the request was received by the z/OS Connect EE server when maximum zc time occurred.")


class Smf123RequestDataBase(AbstractConcreteBase):
    """Abstract class for section Smf123RequestData."""

    smf123s1_req_data_ver: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                       doc="Version of request data record. Set to 1.")
    smf123s1_req_type: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                   doc="Request type: 0 = Unknown 1 = API 2 = Service 3 = Admin.")
    smf123s1_http_resp_code: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="HTTP response code.")
    smf123s1_resp_flags: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Response flags.")
    smf123s1_user_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64), doc="See Note 1.")
    smf123s1_user_name_mapped: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                                           doc="If a distributed ID was sent on the request and is mapped to a SAF username, then this value is the authenticated SAF username. Otherwise, this value is blank.")
    smf123s1_client_ip_addr: so.Mapped[Optional[str]] = so.mapped_column(sa.String(48), doc="Client IP address.")
    smf123s1_api_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64), doc="API name.")
    smf123s1_api_version: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="API version.")
    smf123s1_service_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64), doc="Service name.")
    smf123s1_service_version: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Service version.")
    smf123s1_req_method: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Method GET/POST/PUT/DELETE.")
    smf123s1_req_query_str: so.Mapped[Optional[str]] = so.mapped_column(sa.String(128), doc="Query string.")
    smf123s1_req_target_uri: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256), doc="Target URI.")
    smf123s1_req_payload_len: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                          doc="Request payload length in bytes.")
    smf123s1_resp_payload_len: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                           doc="Response payload length in bytes.")
    smf123s1_time_zc_entry: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                                doc="Time the request was received by the z/OS Connect server. See Note 4.")
    smf123s1_time_zc_exit: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                               doc="Time the response was ready to be sent to the HTTP client. See Note 4.")
    smf123s1_time_sor_sent: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                                doc="Time the request was sent to the system of record. For information about IMS, see Note 2. For more information about interpreting time data, see Note 4.")
    smf123s1_time_sor_recv: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                                doc="Time the response was received from the system of record. For information about IMS, see Note 2. For more information.")
    smf123s1_sp_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(16),
                                                                  doc="Service provider name. Value of com.ibm.zosconnect.spi.Data.SERVICE_PROVIDER_NAME.")
    smf123s1_sor_reference: so.Mapped[Optional[str]] = so.mapped_column(sa.String(32),
                                                                        doc="Reference to the element in server.xml that identifies the connection to the system of record. Value of com.ibm.zosconnect.spi.Data.SOR_REFERENCE. See Note 2.")
    smf123s1_sor_resource: so.Mapped[Optional[str]] = so.mapped_column(sa.String(128),
                                                                       doc="System of record resource. Value of com.ibm.zosconnect.spi.Data.SOR_RESOURCE. See Note 2.")
    smf123s1_tracking_token: so.Mapped[Optional[str]] = so.mapped_column(sa.String(130),
                                                                         doc="Tracking token that is padded with spaces (0x40) since 3.0.45 and nulls (0x00) previously. See Note 3.")
    smf123s1_req_hdr1: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64),
                                                                   doc="Request header. <header1name>:<header1value>.")
    smf123s1_req_hdr2: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64),
                                                                   doc="Request header. <header2name>:<header2value>.")
    smf123s1_req_hdr3: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64),
                                                                   doc="Request header. <header3name>:<header3value>.")
    smf123s1_req_hdr4: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64),
                                                                   doc="Request header. <header4name>:<header4value>.")
    smf123s1_resp_hdr1: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64),
                                                                    doc="Mapped response header. <header1name>:<header1value>.")
    smf123s1_resp_hdr2: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64),
                                                                    doc="Mapped response header. <header2name>:<header2value>.")
    smf123s1_resp_hdr3: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64),
                                                                    doc="Mapped response header. <header3name>:<header3value>.")
    smf123s1_resp_hdr4: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64),
                                                                    doc="Mapped response header. <header4name>:<header4value>.")
    timed_out: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of timed-out requests made.")
    zc_resp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="Request elapsed time from when z/OS Connect received the request to when it sent the response to the client, including CICS response time. It is derived by subtracting the z/OS connect entry time from the exit time.")
    sent_late: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                             doc="The elapsed time from when z/OS Connect received the request to when it sent the request to CICS. It is derived by subtracting the z/OS Connect entry time from the time it sent the request to CICS.")
    sor_resp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="The elapsed time it took CICS to respond to the request. It is derived by subtracting the time the request was sent to CICS from the time CICS responded.")
    exit_late: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                             doc="The elapsed time it took z/OS Connect to respond to the client after is received the response from CICS. It is derived by subtracting the CICS response time from the z/OS Connect exit time.")
    zc_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="The elapsed time it took inside z/OS Connect.")
    tasks: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                       doc="Total number of transaction records within the duration.")
    elapsed: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="Total elapsed time of the transactions within the duration.")


class Smf123ServerBase(AbstractConcreteBase):
    """Abstract class for section Smf123Server."""

    smf123_server_sect_version: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                            doc="Version of the server section. From 3.0.74.0, value is 2; prior to this value is 1.")
    smf123_server_feature_major: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                             doc="From 3.0.74.0, z/OS Connect feature major version. For SMF123_SERVER_SECT_VERSION=1, field is reserved. See Note.")
    smf123_server_feature_minor: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                             doc="From 3.0.74.0, z/OS Connect feature minor version. See Note For SMF123_SERVER_SECT_VERSION=1, field is reserved.")
    smf123_server_system: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="System name (CVTSNAME).")
    smf123_server_stoken: so.Mapped[Optional[str]] = so.mapped_column(sa.String(18),
                                                                      doc="SToken of the server (ASS-BSTKN).")
    smf123_server_config_dir: so.Mapped[Optional[str]] = so.mapped_column(sa.String(128),
                                                                          doc="The path to where the server.xml file for the server is located. This includes the server name.")
    smf123_server_version: so.Mapped[Optional[str]] = so.mapped_column(sa.String(16),
                                                                       doc="Version of the server in the form v.r.m.f.")
    smf123_ssi: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="Subsystem ID. Set to 'ZCON'.")
    smf123_subtype: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                doc="Record subtype (0x0001 for API provider and 0x0002 for API requester).")
    smf123_subtype_version: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                        doc="Record subtype version. Set to 2.")
    smf123_datetime_offset: so.Mapped[Optional[str]] = so.mapped_column(sa.String(30),
                                                                        doc="Local date and time offset (CVTLDTO).")
