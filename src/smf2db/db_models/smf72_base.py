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
    'fk': 'fk__%(table_name)s__%(referred_table_name)s',
    'pk': 'pk__%(table_name)s',
}


class Base(so.DeclarativeBase):
    pass


class Base72(Base):
    __abstract__ = True
    metadata = sa.MetaData(schema='smf72', naming_convention=convention)


class Base72Hr(Base):
    __abstract__ = True
    metadata = sa.MetaData(schema='smf72', naming_convention=convention)


class Base72Da(Base):
    __abstract__ = True
    metadata = sa.MetaData(schema='smf72', naming_convention=convention)


class Smf72pro(AbstractConcreteBase):
    """Abstract class for structure Smf72Pro - RMF product section."""

    smf72mfv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="RMF version number.")
    smf72prd: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Product name ('RMF').")
    smf72int: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Duration of the RMF measurement interval, in the form mmsstttF where mm is the minutes, ss is the seconds, ttt is the milliseconds, and F is the sign. The end of the measurement interval is the sum of the recorded start time (and this field.)")
    smf72sam: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of RMF samples.")
    smf72fla: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Reserved. Flags Bit Meaning when set 0 Reserved. 1 Samples have been skipped. 2 Record was written by RMF Monitor III. 3 Interval was synchronized with SMF. 4 SMF record converted to lower service level. 5 SMF record converted to higher release or service level. 6 Running under an alternate virtual machine. 7 - 8 Reserved. 9 zIIP boost was active during entire interval. 10 Speed boost was active during entire interval. 11 - 12 Reserved. 13 - 15 Boost class: 001 : IPL 010 : Shutdown 011 : Recovery process Note: The boost class value is valid only when one or more boosts is active; that is, a boost active bit is also on.")
    smf72cyc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Sampling cycle length, in the form 000 ttttF , where tttt is the milliseconds and F is the sign (taken from CYCLE option). The range of values is 0.050 to 9.999 seconds.")
    smf72mvs: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="z/OS software level (consists of an acronym and the version, release, and modification level - ZV vvrrmm ).")
    smf72iml: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Indicates the type of processor complex on which data measurements were taken. Value Meaning 3")
    smf72prf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Processor flags. Bit Meaning when set 0 The system has expanded storage 1 The processor is enabled for ES connection architecture (ESCA) 2 There is an ES connection director in the configuration 3 System is running in z/Architecture mode 4 At least one zAAP is currently installed 5 At least one zIIP is currently installed 6 Enhanced DAT facility 1 available")
    smf72ptn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="PR/SM partition number of the partition that wrote this record.")
    smf72srl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="SMF record level change number. This field enables processing of SMF record level changes in an existing release. SMF type 72 record levels for the current z/OS release: Subtypes Record level 3 X'8F' (APAR OA62502) 4 - 5 X'8E'")
    smf72lgo: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Offset GMT to local time (STCK format).")
    smf72oil: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Original interval length as defined in the session or by SMF (in seconds).")
    smf72syn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="SYNC value in seconds.")
    smf72gie: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                  doc="Projected gathering interval end (STCK format) GMT time.")
    smf72snm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="System name for current system as defined in parmlib member IEASYSxx SYSNAME parameter.")
    smf72flg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="System indicator: Bit Meaning when set 0 New SMF record format 1 Subtypes used 2 Reserved 3-6 Version indicators* 7 System is running in PR/SM mode")
    speed_boost: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                             doc="smf72fla (Bit 10) indcating speed boost was active during entire interval.")
    ziip_boost: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                            doc="smf72fla (Bit 9) indciating zIIP boost was active during entire interval.")


class Smf72wrs(AbstractConcreteBase):
    """Abstract class for structure Smf72Wrs - Work Manager/Resource Manager State section."""

    r723ress: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of transaction states sampled in the phase specified by R723RFLG.")
    r723ract: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of active state samples. Active indicates that there is a program executing on behalf of the work request, from the perspective of the work manager. This does not mean that the program is active from the base control program's perspective.")
    r723rrdy: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of ready state samples. Ready indicates that there is a program ready to execute on behalf of the work request described by the monitoring environment, but the work manager has given priority to another work request.")
    r723ridl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of idle state samples. Idle indicates that no work request is available to the work manager that is allowed to run.")
    r723rwlo: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of waiting for lock state samples.")
    r723rwio: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of waiting for I/O state samples. Waiting for I/O indicates that the work manager is waiting for an activity related to an I/O request. This may be an actual I/O operation or some other function associated with the I/O request.")
    r723rwco: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of waiting for conversation state samples. Waiting for conversation may have been used in conjunction with the WLM service IWMMSWCH to identify where the recipient of the conversation is located. In this case, only the switched state will be recorded.")
    r723rwds: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of waiting for distributed request state samples. Waiting for distributed request indicates a high level that some function or data must be routed prior to resumption of the work request. This is to be contrasted with waiting for conversation, which is a low level view of the precise resource that is needed. A distributed request could involve waiting on a conversation as part")
    r723rwsl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of waiting for a session to be established locally samples. Waiting for a session to be established locally, i.e. on the current MVS image.")
    r723rwsn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of waiting for a session to be established somewhere in the network samples.")
    r723rwss: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of waiting for a session to be established somewhere in the sysplex samples.")
    r723rwtm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of waiting for a timer samples.")
    r723rwo: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                         doc="Total number of waiting for another product samples.")
    r723rwms: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of waiting for unidentified resource samples. Waiting for unidentified resource, possibly among another more specific category, but which may not be readily determined.")
    r723rssl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of states representing transactions for which there are logical continuations on this MVS image. Subsystem work managers might set this state when they function ship a transaction to another component within the same MVS image.")
    r723rsss: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of states representing transactions for which there are logical continuations on another MVS image in the sysplex. Subsystem work managers might set this state when they function ship a transaction to another component on another MVS image within the sysplex.")
    r723rssn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of states representing transactions for which there are logical continuations somewhere within the network. Subsystem work managers might set this state when they function ship a transaction to another component within the network.")
    r723rwst: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of waiting for SSL thread samples.")
    r723rwrt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of waiting for regular thread samples.")
    r723rwwr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of waiting for work table registration samples.")
    r723rapp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of active application state samples.")
    r723rwnl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of state samples reflecting waiting for new latch.")
    r723rw01: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of samples waiting for resource type 1.")
    r723rw02: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of samples waiting for resource type 2.")
    r723rw03: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of samples waiting for resource type 3.")
    r723rw04: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of samples waiting for resource type 4.")
    r723rw05: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of samples waiting for resource type 5.")
    r723rw06: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of samples waiting for resource type 6.")
    r723rw07: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of samples waiting for resource type 7.")
    r723rw08: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of samples waiting for resource type 8.")
    r723rw09: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of samples waiting for resource type 9.")
    r723rw10: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of samples waiting for resource type 10.")
    r723rw11: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of samples waiting for resource type 11.")
    r723rw12: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of samples waiting for resource type 12.")
    r723rw13: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of samples waiting for resource type 13.")
    r723rw14: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of samples waiting for resource type 14.")
    r723rw15: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of samples waiting for resource type 15.")
    r723rbpm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of state samples representing buffer pool misses that resulted in I/O.")


class Smf72scs(AbstractConcreteBase):
    """Abstract class for structure Smf72Scs - Service/report class period data section."""

    r723crs1: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Service and Report class period flags. Bit Meaning when set 0 This report class period is heterogeneous. 1 Service class period is implicitly designated CPU critical. 2-7 Reserved.")
    r723cadf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="one of the subsections being a part of this section. Bit Meaning when set 0 Resource consumption data available 1 Response time data available 2 General execution delay data available 3-7 Reserved.")
    r723crtf: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Response time flags (indicates units for R723CVAL). Bit Meaning when set 0 Response time specified in milliseconds. 1 Response time specified in seconds. 2 Response time specified in minutes. 3 Response time specified in hours. 4-7 Reserved.")
    r723crgf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Response time goal flags. Bit Meaning when set 0 Percentile response time goal. 1 Average response time goal. 2 Execution velocity goal. 3 Discretionary goal. 4 System specified goal. 5-7 Reserved.")
    r723cval: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Response time or execution velocity goal, or zero if discretionary or system goal. Units are defined in R723CRTF.")
    r723cpct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Goal percentile value (in percentage).")
    r723cdur: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Period duration in weighted service units, or zero for the last period.")
    r723csrv: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Total service units.")
    r723ccpu: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total TCB service units. This value includes SUs on general purpose CPs and normalized SUs on zIIPs and zAAPs.")
    r723cioc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Total IOC service units. Always zero.")
    r723cmso: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total central storage service units. Always zero.")
    r723csrb: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total SRB service units. This value includes SUs on general purpose CPs and normalized SUs on zIIPs and zAAPs.")
    r723cpir: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Total page-in count.")
    r723chpi: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total hiperspace page-in count. This value includes only those hiperspace pages that were moved by the Real Storage Manager and not by the MVPG instruction.")
    r723cbpi: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Total block page-in from auxiliary count.")
    r723cpie: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Total page-in from expanded count.")
    r723cbpe: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Total block page-in from expanded count.")
    r723cbka: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Total auxiliary blocks paged in.")
    r723cbke: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Total expanded blocks paged in.")
    r723cprs: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total page residency time (1024-microsecond units).")
    r723cers: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total expanded page residency time (1024-microsecond units).")
    r723ctrr: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total in storage residency time (1024-microsecond units).")
    r723ctat: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total transaction active time (1024-microsecond units).")
    r723crct: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Total RCT time (microseconds).")
    r723ciit: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Total I/O interrupt time (microseconds).")
    r723chst: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total hiperspace service time (microseconds).")
    r723cswc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total swap count.")
    r723ccrm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total hiperspace ESO read miss count.")
    r723crcp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of transaction completions for this period. This field includes transaction completions reported by subsystem work managers by way of the IWMRPT service.")
    r723carc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of transactions that completed abnormally as reported by subsystem work manager. This value is not part of R723CRCP and should not be used for response time calculations.")
    r723cncp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of transactions that completed their execution phase as reported by subsystem work managers by way of the IWMNTFY service.")
    r723canc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of transactions that completed their execution phase abnormally as reported by subsystem work Manager. This value is not part of R723CNCP and should not be used for execution response time calculations.")
    r723ctet: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total transaction elapsed time (1024-microsecond units).")
    r723cxet: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total transaction execution time (1024-microsecond units).")
    r723cets: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Sum of transaction elapsed times squared (1024-microsecond units).")
    r723ccus: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="CPU using samples. These are included in R723CTOU.")
    r723ctot: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total general execution delay samples used in WLM's execution velocity calculation. For the velocity formula, see z/OS MVS Planning: Workload Management .")
    r723ccde: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="CPU delay. A TCB or SRB is waiting to be dispatched or a TCB is waiting for local lock.")
    r723ccca: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="CPU capping delay. A TCB or SRB is marked non-dispatchable because a resource group maximum is being enforced. Note that R723CCCA is NOT a subset of R723CCDE.")
    r723cswi: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Swap-in delay. Swap-in has started, but not completed.")
    r723cmpl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="MPL delay. Ready but swap-in has not started.")
    r723capr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Auxiliary page from private.")
    r723caco: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Auxiliary page from common.")
    r723caxm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Auxiliary page from cross memory.")
    r723cvio: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Auxiliary page from VIO.")
    r723chsp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Auxiliary page from standard hiperspaces.")
    r723cchs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Auxiliary page from ESO hiperspaces.")
    r723cunk: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Unknown. Address space or enclave is waiting, but none of the general execution delays (listed earlier) apply.")
    r723cidl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Idle. Address space or enclave is in STIMER wait, TSO terminal wait, APPC wait, or an initiator waiting for work.")
    r723cpde: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Resource group capping count. Group maximum is being enforced for work in this class.")
    r723cpqu: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Quiesce count. Some work in this service class has been reset by way of the RESET xxx, QUIESCE command.")
    r723csac: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Sampled address space count. Number of address spaces that contributed delay and using samples to this class.")
    r723csrs: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total shared page residency time in 1024-microsecond units.")
    r723cspa: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total shared page-ins from auxiliary storage.")
    r723cspe: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total shared page-ins from expanded storage.")
    r723cict: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total non-paging DASD connect time in 128-microsecond units.")
    r723ciwt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total non-paging DASD wait time (queue time + pending time) in 128-microsecond units.")
    r723cidt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total non-paging DASD disconnect time in 128-microsecond units. This does not include IOS queue time.")
    r723circ: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total non-paging DASD I/O start subchannel count. This can be used with fields R723CICT, R723CIWT, and R723CIDT to determine the average DASD response time for the period.")
    r723ctou: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total using samples. For the velocity formula, see z/OS MVS Planning: Workload Management .")
    r723ciou: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="DASD using samples. Only non-paging DASD I/O can contribute to I/O using samples.")
    r723ciod: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="DASD delay samples.")
    r723cq: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                        doc="Queue delay samples, work is waiting for a server.")
    r723cspv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Server private area paging delay samples.")
    r723csvi: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Server space VIO paging delay samples.")
    r723cshs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Server hiperspace paging delay samples.")
    r723csmp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Server MPL delay samples.")
    r723cssw: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Server swap-in delay samples.")
    r723cndi: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Non-DASD I/O using or delay samples.")
    r723ctdq: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total delay samples always including batch queue delay. For service classes that contain batch jobs that were not run in WLM managed initiators the batch queue delay samples are derived from the measured batch queue delay time. For service classes that contain jobs that ran in WLM managed initiators this value is the same as R723CTOT. R723CTDQ can be used as a migration aid to determine what a batch service class")
    r723ctsa: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total execution samples. It is the sum of R723CTOU, R723CTOT, R723CUNK, R723CIDL.")
    r723ciot: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total DASD IOS queue time in 128-microsecond units.")
    r723cqdt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total queue delay time in 1024-microsecond units. For batch jobs, this is the time jobs spent on the job queue while eligible to run on some system. It represents the time the jobs spent waiting for an initiator. For TSO users, this time can be a portion of the LOGON process. For APPC, this is the time an APPC request spent on an APPC queue.")
    r723cadt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total time (in 1024-microsecond units) batch jobs were ineligible to run because a resource that the job had affinity to was unavailable.")
    r723ccvt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total time (in 1024-microsecond units) batch jobs spent in JCL conversion.")
    r723ciqt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total time (in 1024-microsecond units) batch jobs spent on job queue (after JCL conversion) while ineligible to run on any system for reasons other than resource affinities.")
    r723ciea: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Independent enclave total transaction active time (in 1024- microsecond units) for enclaves that originated on this system.")
    r723cxea: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Exported enclave total transaction active time (in 1024- microsecond units).")
    r723cfea: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Foreign enclave total transaction active time (in 1024-microsecond units).")
    r723apu: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                         doc="AP crypto using samples: a TCB was found executing on a cryptographic assist processor.")
    r723apd: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                         doc="AP crypto delay samples: a TCB was found waiting for a cryptographic assist processor.")
    r723fqd: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                         doc="Feature queue delay samples: a TCB was found waiting on a processor feature queue associated with a CPU. This is a subset of R723CCDE.")
    r723plsc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="Service class that last contributed to this report class period during this interval. Blank if this is a service class period.")
    r723rcod: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Contention delay sample count. One sample is accumulated for each held resource which is reported to WLM by the resource manager by way of IWMCNTN.")
    r723rcou: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Contention using sample count. One sample is accumulated for each resource in use which is reported to WLM by the resource manager by way of IWMCNTN.")
    r723ectc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="CPU time consumed while dispatching priority was temporarily raised by enqueue management because the work unit held a resource that other work needed (in 1024 microsecond units).")
    r723ifau: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="zAAP using samples.")
    r723ifcu: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="zAAP on CP using samples. These samples are included in R723CCUS.")
    r723ifad: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="zAAP delay samples.")
    r723supu: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="zIIP using samples.")
    r723sucu: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="zIIP on CP using samples.")
    r723supd: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="zIIP delay samples.")
    r723csup: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total service units on zIIPs. Multiply with R723NFFS and divide by 256 to calculate the CP equivalent value.")
    r723csuc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total service units on CPs spent by zIIP eligible work.")
    r723cifa: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total service units on zAAPs. Multiply with R723NFFI and divide by 256 to calculate the CP equivalent value.")
    r723cifc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total service units on CPs spent by zAAP eligible work.")
    r723tpdp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="CPU time consumed while dispatching priority of work with low importance was temporarily raised to help blocked workloads (in 1024 microsecond units).")
    r723cpdp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="CPU time consumed while dispatching priority was temporarily raised by chronic resource contention management because the work unit held a resource that other work needed (in 1024 microsecond units).")
    r723lpdp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="CPU time consumed while dispatching priority was temporarily raised to shorten the lock hold time of a local suspend lock held by the work unit (in 1024 microsecond units). Only valid if HiperDispatch is active.")
    r723spdp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="CPU time consumed while dispatching priority for a work unit was temporarily raised by the z/OS supervisor to a higher dispatching priority than assigned by WLM (in 1024-microsecond units).")
    r723rtdm: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Midpoint of all response times that were collected in the response time distribution buckets in milliseconds. For response time goals, the midpoint is always the response time goal. For execution velocity goals, it is the average of all response times that were collected in the response time distribution buckets.")
    r723rtdc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of midpoint changes that occurred during the interval. Number equals zero for response time goals.")
    r723rtdt: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                  doc="Timestamp in STCK format, showing the latest point in time when a midpoint change occurred in R723RTDM.")
    r723tsucp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                             doc="Total service units consumed by transactions, executed on general purpose processors.")
    r723tsusp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                             doc="Total normalized service units consumed by transactions, executed on specialty processors.")
    r723tsuocp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="Total service units consumed by transactions, eligible to run on specialty processors, but executed on general purpose processors.")
    r723msucp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                             doc="Service units consumed by transactions, classified with reporting attribute MOBILE, executed on general purpose processors.")
    r723msusp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                             doc="Normalized service units consumed by transactions, classified with reporting attribute MOBILE, executed on specialty processors.")
    r723msuocp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="Service units consumed by transactions, classified with reporting attribute MOBILE, eligible to run on specialty processors, but executed on general purpose processors.")
    r723asucp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                             doc="Service units consumed by transactions, classified with reporting attribute CATEGORYA, executed on general purpose processors.")
    r723asusp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                             doc="Normalized service units consumed by transactions, classified with reporting attribute CATEGORYA, executed on specialty processors.")
    r723asuocp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="Service units consumed by transactions, classified with reporting attribute CATEGORYA, eligible to run on specialty processors, but")
    r723bsucp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                             doc="Service units consumed by transactions, classified with reporting attribute CATEGORYB, executed on general purpose processors.")
    r723bsusp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                             doc="Normalized service units consumed by transactions, classified with reporting attribute CATEGORYB, executed on specialty processors.")
    r723bsuocp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="Service units consumed by transactions, classified with reporting attribute CATEGORYB, eligible to run on specialty processors, but executed on general purpose processors.")
    r723ctetx: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                             doc="Total transaction elapsed time. Same as R723CTET, but in microseconds.")
    r723cxetx: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                             doc="Total transaction execution time. Same as R723CXET, but in microseconds.")
    r723cetsx: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                             doc="Sum of transaction elapsed times squared. Same as R723CETS, but in microseconds.")
    r723cqdtx: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                             doc="Total queue delay time. Same as R723CQDT, but in microseconds.")
    r723cadtx: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                             doc="Total time batch jobs were ineligible to run because a resource that the job had affinity to was unavailable. Same as R723CADT, but in microseconds.")
    r723ccvtx: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                             doc="Total time batch jobs spent in JCL conversion. Same as R723CCVT, but in microseconds.")
    r723ciqtx: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                             doc="Total time batch jobs spent on job queue (after JCL conversion) while ineligible to run on any system for reasons other than resource affinities. Same as R723CIQT, but in microseconds.")
    r723enctrxnum: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Number of subsystem transactions processed within enclaves.")
    r723enctrxcalls: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                 doc="Number of times transaction data has been reported by subsystem work managers when deleting an enclave. When zero, no transaction data for enclaves has been provided by the subsystem work manager.")
    r723enctrxet: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="Total execution time, in microseconds, for all subsystem transactions reported in R723ENCTRXNUM.")
    r723enctrxets: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="Sum of squared execution times, in microseconds, for all subsystem transactions reported in R723ENCTRXNUM.")
    r723mtv_: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of times when WLM sampling code ran.")
    is_heterogeneous: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                  doc="r723crs1 (Bit 0) indicating this report class period is heterogeneous.")
    r723ceda: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r723cadf (Bit 2) indicating general execution delay data available.")
    r723crta: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r723cadf (Bit 1) indicating response time data availabe.")
    r723crca: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r723cadf (Bit 0) indicating resource consumption data available.")
    response_time_hours: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                     doc="r723crtf (Bit 3) indicating response time specified in hours.")
    response_time_minutes: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                       doc="r723crtf (Bit 2) indicating response time specified in minutes.")
    response_time_seconds: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                       doc="r723crtf (Bit 1) indicating response time specified in seconds.")
    response_time_millisec: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                          doc="r723crtf (Bit 0) indicating response time specified in milliseconds.")
    r723cstm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r723crgf (Bit 4) indicating system specified goal.")
    r723cdsc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r723crfg (Bit 3) indicating discretionary goal.")
    r723cvel: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r723crfg (Bit 2) indicating execution velocity goal.")
    r723cavg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r723crfg (Bit 1) indicating average response time goal.")
    r723cprc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r723crfg (Bit 0) indicating percentile response time goal.")
    class_goal_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(21), doc="The goal type.")
    utilization_total: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="The total utilization.")
    utilization_cp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="The CP processor utilization.")
    storage_total_swapped_in: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                            doc="The total frames of all swapped-in transactions.")
    transaction_average_active: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                              doc="The average number of active transactions.")
    transaction_total_per_second: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                doc="The total ended transactions per second.")
    transaction_executed_per_second: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                   doc="The total executed transactions per second.")
    transaction_response_time_mean: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                  doc="The average transaction response time.")
    sample_rate: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="The number of samples per second.")
    transaction_execution_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                              doc="The transaction execution time.")
    transaction_execution_time_mean: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                   doc="The average transaction execution time.")
    execution_velocity: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                      doc="The execution velocity measures the portion of the acceptable processor and storage delays relative to the total execution time.")
    performance_index: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                     doc="The performance index for a period represents how close a period came to reaching the goal (PI is 1.0 if goal is reached), and how much this period suffered versus its goal.")
    sample_storage_delay: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                        doc="The number of samples in storage delay state.")
    transaction_address_space_percentage: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                        doc="The percentage of transaction address space count.")
    sample_server_delay: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                     doc="The sample delay for a server address space.")
    transaction_queue_delay_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                doc="The transaction queue delay time.")
    transaction_queue_delay_time_mean: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                     doc="The average transaction queue delay time.")
    transaction_aff_delay_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                              doc="The transaction affinity delay time.")
    transaction_aff_delay_time_mean: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                   doc="The average transaction affinity delay time.")
    transaction_jcl_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                        doc="The transaction JCL conversion time.")
    transaction_jcl_time_mean: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                             doc="The average transaction JCL conversion time.")
    transaction_inel_delay_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                               doc="The transaction ineligible queue time.")
    transaction_inel_delay_time_mean: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                    doc="The average transaction ineligible queue time.")
    transaction_enclave_average: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                               doc="The average number of independent enclaves during the interval. From a sysplex scope, this is the sum of active time for enclaves that originated on the respective system either for the single period or for all summarized periods divided by the RMF interval time.")
    foreign_enclave_average: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                           doc="The average number of foreign enclaves during the interval. From a sysplex scope, this is the sum of active time for enclaves that originated on a remote system in the sysplex, but are executing on the respective system either for the single period or for all summarized periods divided by the RMF interval time.")
    export_enclave_average: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                          doc="The average number of multi-system enclaves during the interval. From a sysplex scope, this is the sum of active time for enclaves that originated on the respective system and are executing on one or more remote systems in the sysplex in parallel either for the single period or for all summarized periods divided by the RMF interval time.")
    sample_crypto_using: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                     doc="The number of samples found in crypto using state - a TCB or SRB was found to be using an adjunct processor (AP).")
    sample_crypto_delay: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                     doc="The number of samples found in crypto delay state - a TCB or SRB was found to be waiting for an AP or a processor feature queue.")
    utilization_zaap: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="The zAAP service time in seconds.")
    utilization_zaap_on_cp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                          doc="The zAAP on CP service time in seconds.")
    utilization_ziip: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="The zIIP service time in seconds.")
    utilization_ziip_on_cp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                          doc="The zIIP on CP service time in seconds.")
    transaction_average_swapped_in: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                  doc="The average number of transactions swapped-in.")
    swaps_per_transaction: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                         doc="The number of swaps per transaction.")
    transaction_average_elapsed_time_std_dev: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                            doc="The average transaction elapsed time standard deviation.")
    transaction_total_percentage_cp_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                        doc="Total percentage of general purpose processor time used by transactions.")
    transaction_total_percentage_sp_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                        doc="Total percentage of specialty processor time used by transactions.")
    transaction_total_percentage_sp_on_cp_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                              doc="Total percentage of general purpose processor time used by transactions, eligible to run on specialty processors.")
    transaction_mobile_percentage_cp_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                         doc="Percentage of general purpose processors used by transactions classified with reporting attribute MOBILE.")
    transaction_mobile_percentage_sp_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                         doc="Percentage of specialty processor time used by transactions classified with reporting attribute MOBILE.")
    transaction_mobile_percentage_sp_on_cp_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                               doc="Percentage of general purpose processor time used by transactions classified with reporting attribute MOBILE, eligible to run on specialty processors.")
    transaction_cata_percentage_cp_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                       doc="Percentage of general purpose processors used by transactions classified with reporting attribute CATEGORYA.")
    transaction_cata_percentage_sp_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                       doc="Percentage of specialty processor time used by transactions classified with reporting attribute CATEGORYA.")
    transaction_cata_percentage_sp_on_cp_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                             doc="Percentage of general purpose processor time used by transactions classified with reporting attribute CATEGORYA eligible to run on specialty processors.")
    transaction_catb_percentage_cp_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                       doc="Percentage of general purpose processors used by transactions classified with reporting attribute CATEGORYB.")
    transaction_catb_percentage_sp_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                       doc="Percentage of specialty processor time used by transactions classified with reporting attribute CATEGORYB.")
    transaction_catb_percentage_sp_on_cp_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                             doc="Percentage of general purpose processor time used by transactions classified with reporting attribute CATEGORYB eligible to run on specialty processors.")
    absorption_rate: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                   doc="Absorption rate at which service is used while transactions are resident in main storage. This is the total service divided by the transaction residency time.")
    transaction_service_rate: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                            doc="Rate at which service is used by transactions that are active, but not necessarily in storage. This is the total service divided by the transaction active time.")
    tcbtime_insec: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="Task and preemptible-class SRB (enclave) time in seconds consumed on general purpose and special purpose processors.")
    srbtime_insec: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Service request block time in seconds.")
    iiptime_insec: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="zIIP service time in seconds.")
    aaptime_insec: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="zAAP service time in seconds.")
    appl_percentage_cp_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                           doc="Percentage of the processor time used by transactions running on general purpose processors in the service or report class period. The calculation of the processor time is based on the time values displayed under field heading SERVICE TIME.")
    appl_percentage_iipcp_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                              doc="Percentage of the processor time used by zIIP eligible transactions running on general purpose processors. This is a subset of APPL% CP.")
    appl_percentage_iip_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                            doc="Percentage of the processor time used by transactions executed on zIIPs in the service or report class period.")
    appl_percentage_aapcp_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                              doc="Percentage of the processor time used by zAAP eligible transactions running on general purpose processors. This is a subset of APPL% CP.")
    appl_percentage_aap_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                            doc="Percentage of the processor time used by transactions executed on zAAPs in the service or report class period.")
    start_subchannel_rate: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                         doc="Number of start subchannels SSCH per second in the reported interval.")
    avg_dasd_response_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                          doc="Average DASD response time (in milliseconds) of the transactions in this group. This is the sum of the average connect time (CONN), the average disconnect time (DISC), the average wait time (Q+PEND), and the IOS queue time (IOSQ).")
    avg_dasd_connect_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                         doc="Average DASD connection time of the transactions in this group, as reported by the channel measurement subsystem.")
    avg_dasd_disconnect_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                            doc="Average DASD disconnect time of the transactions in this group, as reported by the channel measurement subsystem.")
    avg_dasd_pending_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                         doc="Average DASD wait time (queue time + pending time) of the transactions in this group. This does not include IOSQ time, as reported by the channel measurement subsystem.")
    avg_dasd_ios_queue_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                           doc="Average time the transactions in this group spent on the IOS queue, based on sampled delays.")
    single_page_in_rate: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                       doc="The average rate at which pages are read into central storage while transactions are resident in central storage. On a single period level this is the total number of page-ins during the period, divided by transaction residency time. For all other levels it is the sum of the total number of page-ins for all periods summarized, divided by the sum of the transaction residency time for all periods being summarized.")
    block_page_in_rate: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                      doc="Rate of demand page-ins from DASD for blocked pages, expressed in pages per seconds.")
    shared_page_in_rate: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Rate of shared storage page-ins")
    hsp_page_in_rate: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="Rate of standard hiperspace pages read into central storage from auxiliary storage.")
    su_sec: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="The service units in seconds.")
    cpu_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="The calculated CPU time.")
    msu_physical: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="The physical MSU consumed.")
    num_of_cps: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="The number of general processors.")
    memory_usage: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="Amount of memory used by this resource group on a particular system.")


class Smf72policy(AbstractConcreteBase):
    """Abstract class for section Smf72Policy."""

    r723mdsp: so.Mapped[Optional[str]] = so.mapped_column(sa.String(32), doc="Policy description.")
    r723mtpa: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                  doc="Local time/date of policy activation (STCK format).")
    r723mcpu: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="CPU service coefficient * 10,000.")
    r723mioc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="I/O service coefficient. Always zero.")
    r723mmso: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Storage service coefficient. Always zero.")
    r723msrb: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="SRB service coefficient * 10,000")
    r723mopt: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2), doc="Suffix of the IEAOPTxx parmlib member.")
    r723merf: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Enqueue residency CPU service factor.")
    r723madj: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Adjustment factor for CPU rate.")
    r723midn: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Service definition name.")
    r723mtdi: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                  doc="Local time/date the service definition was installed (STCK format).")
    r723midu: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="Userid that installed the service definition.")
    r723midd: so.Mapped[Optional[str]] = so.mapped_column(sa.String(32), doc="Service definition description.")
    r723nffi: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Normalization factor for zAAP. Multiply zAAP service times or service units with this value and divide by 256 to calculate the CP equivalent value.")
    r723nffs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Normalization factor for zIIP. Multiply zIIP service units with this value and divide by 256 to calculate the CP equivalent")
    r723nadj: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Nominal adjustment factor for CPU rate.")
    r723ceca: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="CEC adjustment factor.")
    r723mcf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                         doc="Multithreading maximum capacity numerator for general purpose processors. Divide this value by 1024 to get the MT maximum capacity factor for all general purpose processors that were configured ONLINE for the complete interval.")
    r723mcfs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Multithreading maximum capacity numerator for zIIP. Divide this value by 1024 to get the multithreading maximum capacity factor for all zIIPs that were configured ONLINE for the complete interval. A zero value is reported if no zIIP is currently installed.")
    r723mcfi: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Multithreading maximum capacity numerator for zAAP. Divide this value by 1024 to get the multithreading maximum capacity factor for all zAAPs that were configured ONLINE for the complete interval. A zero value is reported if no zAAP is currently installed.")
    r723cpa_actual: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                doc="Physical CPU adjustment factor based on Model Capacity Rating.")
    r723cpa_scaling_factor: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                        doc="Scaling factor for R723CPA_actual.")
    smf72mvs: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="z/OS software level (consists of an acronym and the version, release, and modification level - ZV vvrrmm ).")
    smf72mfv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="RMF version number.")
    smf72prf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Processor flags. Bit Meaning when set 0 The system has expanded storage 1 The processor is enabled for ES connection architecture (ESCA) 2 There is an ES connection director in the configuration 3 System is running in z/Architecture mode 4 At least one zAAP is currently installed 5 At least one zIIP is currently installed 6 Enhanced DAT facility 1 available")
    smf72int: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Duration of the RMF measurement interval, in the form mmsstttF where mm is the minutes, ss is the seconds, ttt is the milliseconds, and F is the sign. The end of the measurement interval is the sum of the recorded start time (and this field.)")
    smf70cai: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Capacity-adjustment indication. When zero, the indication is not reported. When in the range from 1 to 99, some amount of reduction is indicated. When 100, the machine is operating at its normal capacity. Temporary capacity changes that affect machine performance (for example, CBU or OOCoD) are not included.")
    cpu_service_coefficient_adjusted: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                    doc="CPU service coefficient adjusted with r723madj.")
    srb_service_coefficient_adjusted: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                    doc="SRB service coefficient adjusted with r723madj.")
    io_high: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                         doc="r723mscf (Bit 7) of indicator I/O priority group HIGH.")
    velocity_io_delays: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                    doc="r723mscf (Bit 3) indicating execution velocity includes I/O delays.")
    dynamic_alias: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="r723mscf (Bit 6) of indicator for dynamic alias tuning.")
    r723mdis: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r723mflg (Bit 6) indicating service class and tenant report class periods that are assocaited with a resource group and have assigned a discretionary goal are excluded from workload management.")
    ziip_inst: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                           doc="smf72prf (Bit 5) in RMF product section indicating at least one zIIP is currently installed.")
    zaap_inst: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                           doc="smf72prf (Bit 4) in RMF product section indicating at lease one zAAP is currently installed.")
    interval_start_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                             doc="the start time of the interval")


class Smf72rts(AbstractConcreteBase):
    """Abstract class for structure Smf72Rts - Response Time Distribution Data section."""

    class_rt_bucket_1: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                   doc="Count of completed transactions with: Response time ≤ 50% of the goal.")
    class_rt_bucket_2: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                   doc="Count of completed transactions with: Response time > 50% of the goal. Response time ≤ 60% of the goal.")
    class_rt_bucket_3: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                   doc="Count of completed transactions with: Response time > 60% of the goal. Response time ≤ 70% of the goal.")
    class_rt_bucket_4: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                   doc="Count of completed transactions with: Response time > 70% of the goal. Response time ≤ 80% of the goal.")
    class_rt_bucket_5: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                   doc="Count of completed transactions with: Response time > 80% of the goal. Response time ≤ 90% of the goal.")
    class_rt_bucket_6: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                   doc="Count of completed transactions with: Response time > 90% of the goal. Response time ≤ 100% of the goal.")
    class_rt_bucket_7: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                   doc="Count of completed transactions with: Response time > 100% of the goal. Response time ≤ 110% of the goal.")
    class_rt_bucket_8: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                   doc="Count of completed transactions with: Response time > 110% of the goal. Response time ≤ 120% of the goal.")
    class_rt_bucket_9: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                   doc="Count of completed transactions with: Response time > 120% of the goal. Response time ≤ 130% of the goal.")
    class_rt_bucket_10: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                    doc="Count of completed transactions with: Response time > 130% of the goal. Response time ≤ 140% of the goal.")
    class_rt_bucket_11: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                    doc="Count of completed transactions with: Response time > 140% of the goal. Response time ≤ 150% of the goal.")
    class_rt_bucket_12: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                    doc="Count of completed transactions with: Response time > 150% of the goal. Response time ≤ 200% of the goal.")
    class_rt_bucket_13: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                    doc="Count of completed transactions with: Response time > 200% of the goal. Response time ≤ 400% of the goal.")
    class_rt_bucket_14: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                    doc="Count of completed transactions with: Response time > 400% of the goal.")


class Smf72sctl(AbstractConcreteBase):
    """Abstract class for structure Smf72Sctl - Serialization control section."""

    r725sgmo: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="GRS mode. Value Meaning 0 None 1 Ring 2")
    r725scms: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of times that a unit of work was suspended on a CMS lock.")
    r725scma: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of times that a unit of work was suspended on a CMS lock when there was already at least one other unit of work suspended for the lock.")
    r725scmt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total amount of time in milliseconds that a unit of work was suspended on a CMS lock.")
    r725seds: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of times that a unit of work was suspended on a CMS Enqueue/Dequeue lock.")
    r725seda: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of times that a unit of work was suspended on a CMS Enqueue/Dequeue lock when there was already at least one other unit of work suspended for the lock.")
    r725sedt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total amount of time in milliseconds that a unit of work was suspended on a CMS Enqueue/Dequeue lock.")
    r725slas: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of times that a unit of work was suspended on a CMS Latch lock.")
    r725slaa: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of times that a unit of work was suspended on a CMS Latch lock when there was already at least one other unit of work suspended for the lock.")
    r725slat: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total amount of time in milliseconds that a unit of work was suspended on a CMS Latch lock.")
    r725ssms: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of times that a unit of work was suspended on a CMS SMF lock.")
    r725ssma: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of times that a unit of work was suspended on a CMS SMF lock when there was already at least one other unit of work suspended for the lock.")
    r725ssmt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total amount of time in milliseconds that a unit of work was suspended on a CMS SMF lock.")
    r725slos: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of times that a unit of work was suspended on a local")
    r725sloa: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of times that a unit of work was suspended on a local lock when there was already at least one other unit of work suspended for the lock.")
    r725slot: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total amount of time in milliseconds that a unit of work was suspended on a local lock.")
    r725scls: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of times that a unit of work from another address space was suspended when requesting the local lock of an address space.")
    r725scla: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of times that a unit of work from another address space was suspended when requesting the local lock of an address space and there was already at least one other unit of")
    r725sclt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total amount of time in milliseconds that a unit of work from another address space was suspended when requesting the local lock of an address space.")
    r725slrs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of suspended latch obtain requests.")
    r725slrt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total amount of time in milliseconds that latch obtain requests were suspended.")
    r725slrq: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total sum of squares of time in milliseconds that latch obtain requests were suspended.")
    r725sstr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of ENQ SCOPE=STEP requests.")
    r725ssts: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of ENQ SCOPE=STEP requests that were suspended.")
    r725sstt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total amount of contention time in milliseconds caused by ENQ SCOPE=STEP requests.")
    r725sstq: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total sum of squares of contention time in milliseconds caused by ENQ SCOPE=STEP requests.")
    r725ssyr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of ENQ SCOPE=SYSTEM requests.")
    r725ssys: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of ENQ SCOPE=SYSTEM requests that were suspended.")
    r725ssyt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total amount of contention time in milliseconds caused by ENQ SCOPE=SYSTEM requests.")
    r725ssyq: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total sum of squares of contention time in milliseconds caused by ENQ SCOPE=SYSTEM requests.")
    r725sssr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of ENQ SCOPE= SYSTEMS requests.")
    r725ssss: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of ENQ SCOPE= SYSTEMS requests that were suspended.")
    r725ssst: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total amount of contention time in milliseconds caused by ENQ SCOPE= SYSTEMS requests.")
    r725sssq: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total sum of squares of contention time in milliseconds caused by ENQ SCOPE=SYSTEMS requests.")


class Smf72wms(AbstractConcreteBase):
    """Abstract class for structure Smf72Wms - Workload Manager control section."""

    r723mscf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Service/Report class flags. Bit Meaning when set 0 Indicator for a report class 1 Workload activity data not available 2 Policy data not available 3 Execution velocity includes I/O delays 4 Indicator for CPU protection 5 Indicator for storage protection 6 Indicator for dynamic alias tuning 7 Indicator for I/O priority group HIGH")
    r723mflg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Flags. Bit Meaning when set 0 Indicator for zAAP crossover. 1 Indicator for zAAP honor priority. 2 Indicator for zIIP honor priority. 3 Failure returned by HISMT service. Multithreading maximum capacity numerator values are invalid. 4 Indicator that service class is not eligible for honor priority processing. When on, specialty engine eligible work in this service class will not be offloaded to CPs for help processing. 5 Indicator for a tenant report class 6 Service class and tenant report class periods that are associated with a resource group and have assigned a discretionary goal are excluded from workload management. 7 WLM batch initiator management is AI-infused.")
    r723mfl2: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Additional flags: Bit Meaning when set 0 At least one zAAP is online in the sysplex (or local system when not joined to a sysplex). 1-7 Reserved.")
    r723mtvl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="WLM sample interval (in milliseconds).")
    r723mtv_: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of times when WLM sampling code ran.")
    r723mcde: so.Mapped[Optional[str]] = so.mapped_column(sa.String(32), doc="Service/Report class description.")
    r723mcpg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of periods belonging to this service or report class.")
    r723msub: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of entries in the work/resource manager state section belonging to a subsystem.")
    r723clsc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="Service class that last contributed to this report class. Blank if this is a service class.")
    is_report_class: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                 doc="r723mscf (Bit 0) representing an indicator for a report class.")
    stor_protection: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                 doc="r723mscf (Bit 5) representing an indicator for storage protection.")
    cpu_protection: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                doc="r723mscf (Bit 4) representing an indciator for CPU protection.")
    velocity_io_delays: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                    doc="r723mscf (Bit 3) indicating exection velocity includes I/O delays.")
    svpol_unaval: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="r723mscf (Bit 2) indicating policy data not available.")
    rcaa_unaval: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                             doc="r723mscf (Bit 1) indicating workload activity data not available.")
    tenant_report_class: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                     doc="r723mflg (Bit 5) representing an indicator for a tenant report class.")
    honor_prio: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                            doc="r723mflg (Bit 4) representing an indicator that service class is not eligible for honor priority processing. When on, speciality engine eligible work in this service class will not be offloaded to CPs for help processing.")
    hismt_failure: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="r723mflg (Bit 3) indicating failure returned by HISMT service. Multithreading maximum capacity numerator values are invalid.")
    ziip_honor_prio: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                 doc="r723mflg (Bit 2) representing an indicator for zIIP honor priority.")
    zaap_honor_prio: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                 doc="r723mflg (Bit 1) representing an indicator for zAAP honor priority.")
    zaap_crossover: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                doc="r723mflg (Bit 0) representing an indicator for zAAP crossover.")


class Smf72data(AbstractConcreteBase):
    """Abstract class for structure Smf72Data - Service Class Period Data section."""

    r724user: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of users found.")
    r724actv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of active users found.")
    r724acts: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of active samples (except OUTR).")
    r724idls: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of idle samples.")
    r724page: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of users delayed for paging at all samples.")
    r724swap: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of users delayed for swapping at all samples.")
    r724outr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of out and ready users at all samples.")
    r724pgin: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of page-ins.")
    r724divs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of DIV samples.")
    r724lssa: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total logically swapped samples for the group.")
    r724pssa: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total swapped samples for the group (except logical).")
    r724upro: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total processor using samples for the group.")
    r724udev: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total device using samples for the group.")
    r724dpro: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total processor delay samples for the group.")
    r724ddev: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total device delay samples for the group.")
    r724dsto: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total storage delay samples for the group.")
    r724djes: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total JES delay samples for the group.")
    r724dhsm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total HSM delay samples for the group.")
    r724dxcf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total XCF delay samples for the group.")
    r724denq: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total ENQ delay samples for the group.")
    r724dmnt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total mount delay samples for the group.")
    r724dmsg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total message delay samples for the group.")
    r724unkn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total unknown state samples for the group.")
    r724vald: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total valid samples for the group (single state sum of all using, delay, idle, and unknown).")
    r724lsct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of 'long' logical swaps for the group.")
    r724esct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of 'long' swaps to expanded storage for the group.")
    r724psct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of 'long' physical swaps for the group.")
    r724actf: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Number of active frames.")
    r724idle: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Number of idle frames.")
    r724slot: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Number of slots used.")
    r724div: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Number of DIV frames.")
    r724fix: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Number of fixed frames.")
    r724lscf: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of central frames for all logically swapped users at all samples.")
    r724lsef: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of expanded frames for all logically swapped users at all samples.")
    r724psef: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of expanded frames for all swapped users (except logical) at all samples.")
    r724vect: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total vector utilization time for the group (microseconds).")
    r724et: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                          doc="Total executiuon time for all transactions that ended in the group (1024-microsecond units). Does not include queued time.")
    r724qt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                          doc="Total time spent on JES or APPC queues by all transactions that ended in the group (1024-microsecond units).")
    r724end: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="Number of transactions that ended in the group .")
    r724tsv: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Sum of shared page views.")
    r724vin: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="Sum of shared pages in central storage that are valid.")
    r724vlc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Sum of shared page validations.")
    r724gpi: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="Sum of shared page-ins from auxiliary storage.")
    r724etx: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="Total execution time for all transactions that ended in the group. Same as R724ET, but in microseconds.")
    r724qtx: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="Total time spent on JES or APPC queues by all transactions that ended in the group. Same as R724QT, but in microseconds.")
    r724or1: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                         doc="STOR/OUTR delay samples for swap reason 1: Terminal output wait.")
    r724or2: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                         doc="STOR/OUTR delay samples for swap reason 2: Terminal input wait.")
    r724or3: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                         doc="STOR/OUTR delay samples for swap reason 3: Long wait.")
    r724or4: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                         doc="STOR/OUTR delay samples for swap reason 4: Auxiliary storage shortage.")
    r724or5: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                         doc="STOR/OUTR delay samples for swap reason 5: Real storage shortage.")
    r724or6: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                         doc="STOR/OUTR delay samples for swap reason 6: Detected long wait.")
    r724or7: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                         doc="STOR/OUTR delay samples for swap reason 7: Requested swap. No longer used - refer to R724OR7A.")
    r724or8: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                         doc="STOR/OUTR delay samples for swap reason 8: Enqueue exchange swap.")
    r724or9: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                         doc="STOR/OUTR delay samples for swap reason 9: Exchange swap.")
    r724or10: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="STOR/OUTR delay samples for swap reason 10: Unilateral swap.")
    r724or11: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="STOR/OUTR delay samples for swap reason 11: Transition swap.")
    r724or12: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="STOR/OUTR delay samples for swap reason 12: Improve central storage usage.")
    r724or13: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="STOR/OUTR delay samples for swap reason 13: Improve system paging rate.")
    r724or14: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="STOR/OUTR delay samples for swap reason 14: Make room for an out too long user.")
    r724or15: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="STOR/OUTR delay samples for swap reason 15: APPC wait.")
    r724or16: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="STOR/OUTR delay samples for swap reason 16: OMVS input wait.")
    r724or17: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="STOR/OUTR delay samples for swap reason 17: OMVS output wait.")
    r724or18: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="STOR/OUTR delay samples for swap reason 18: In-real swap.")
    r724or7a: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="STOR/OUTR delay samples for swap reason 7: Memory pool shortage")


class Smf72rgs(AbstractConcreteBase):
    """Abstract class for structure Smf72Rgs - Resource Group Data section."""

    r723ggde: so.Mapped[Optional[str]] = so.mapped_column(sa.String(32), doc="Resource group description.")
    r723gglt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Resource group flags. Bit Meaning when set 0 Maximum capacity was specified 1 Minimum capacity was specified 2 Specification of R723GGMN and R723GGMX is in percentage of the LPAR share rather than in service units. In addition, the scope of the resource group is system-wide rather than sysplex-wide. 3 Specification of R723GGMN and R723GGMX is in percentage of a single processor capacity rather than in service units. In addition, the scope of the resource group is system-wide rather than sysplex-wide. 4 Memory limit was specified. 5 Specification of R723GGMN and R723GGMX is in MSU/h rather than in service units. 6 Specialty processor consumption is included into the WLM capping algorithms, i.e. R723GGMN and R723GGMX limit the combined general purpose and specialty processor consumption. 7 Reserved.")
    r723ggtf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Tenant Resource Group Flags. Bit Meaning when set 0 Indicator for a tenant resource group 1-7 Reserved.")
    r723ggmn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="If bit 1 of R723GGLT is ON, minimum capacity of the resource group. If bit 2, bit 3, and bit 5 of R723GGLT are OFF, this value is in unweighted CPU service units per second. In addition, the scope of the resource group is sysplex-wide. If bit 2, bit 3, or bit 5 of R723GGLT is ON, see the description of R723GGLT.")
    r723ggmx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="If bit 0 of R723GGLT is ON, maximum capacity of the resource group. If bit 2, bit 3, and bit 5 of R723GGLT are OFF, this value is in unweighted CPU service units per second. In addition, the scope of the resource group is sysplex-wide. If bit 2, bit 3, or bit 5 of R723GGLT is ON, see the description of R723GGLT.")
    r723ggml: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="If bit 4 of R723GGLT is ON, memory limit (in GB) of the resource group. The scope of the resource group is system-wide.")
    r723ggti: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="Tenant identifier. Only valid if bit 0 of R723GGTF is ON.")
    r723ggtn: so.Mapped[Optional[str]] = so.mapped_column(sa.String(32),
                                                          doc="Tenant name. Only valid if bit 0 of R723GGTF is ON.")
    r723ggky: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64),
                                                          doc="Solution ID. Only valid if bit 0 of R723GGTF is ON.")
    r723gisp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r723gglt (Bit 6) showing specialty processor consumption is included into the WLM capping alogirthms, i.e. r723ggmn and r723ggmx limit the combined general purpose and specialty processor consumption.")
    r723ggms: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r723gglt (Bit 5) showing specificationof r723ggmn and r723ggmx is in MSU/h rather than in service units.")
    has_memory_limit: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                  doc="r723gglt (Bit 4) showing memory limit was specified.")
    r723ggpc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r723gglt (Bit 3) showing specification of r723ggmn and r723ggmx is in percentage of a single processor capacity rather than in service units. In addition, the scope of the resource group is system-wide rather than sysplex-wide.")
    r723ggpv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r723gglt (Bit 2) showing specification of r723ggmn and r723ggmx is in percentage of the LPAR share rather than in service units. In addition, the scope of the resource group is system-wide rather than sysplex-wide.")
    has_min_capacity: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                  doc="r723gglt (Bit 1) showing minimum capacity was specified.")
    has_max_capacity: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                  doc="r723gglt (Bit 0) showing maximum capacity was specified.")
    is_tenant: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                           doc="r723ggtf (Bit 0) showing an indicator for a tenant resource group.")


class Smf72cmss(AbstractConcreteBase):
    """Abstract class for structure Smf72Cmss - CMS lock type data."""

    r725cmas: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="Address space ID.")
    r725cmsu: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of times that a unit of work of this address space was suspended on the CMS lock type as specified in R725CMTY.")
    r725cmal: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of times that a unit of work of this address space was suspended on the CMS lock type as specified in R725CMTY when there was already at least one other unit of work suspended for this lock.")
    r725cmti: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total amount of time in milliseconds that a unit of work of this address space was suspended on the CMS lock type as specified in R725CMTY.")


class Smf72lasc(AbstractConcreteBase):
    """Abstract class for structure Smf72Lasc - GRS latch type data."""

    r725laas: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="Address space ID.")
    r725lasu: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of times a latch obtain request was suspended for the request type as specified in R725LATY.")
    r725lati: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total amount of suspend time in milliseconds that was caused by latch obtain requests for the request type as specified in R725LATY.")
    r725lasq: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Sum of squares of the individual suspend times in milliseconds that was caused by latch obtain requests for the request type as specified in R725LATY.")


class Smf72clod(AbstractConcreteBase):
    """Abstract class for structure Smf72Clod - CML lock owner data section."""

    r725coas: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="Address space ID.")
    r725cosu: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of times that a unit of work from another address space was suspended when requesting the local lock of this address space.")
    r725coal: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of times that a unit of work from another address space was suspended when requesting the local lock of this address space and there was already at least one other unit of work waiting for that lock.")
    r725coti: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total amount of time in milliseconds that a unit of work was suspended when requesting the local lock of this address space.")
    r725clsu: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of times that a unit of work of this address space was suspended on a local lock.")
    r725clal: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of times that a unit of work of this address space was suspended on a local lock when there was already at least one other unit of work suspended.")
    r725clti: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total amount of time in milliseconds that a unit of work of this address space was suspended on a local lock.")


class Smf72clrd(AbstractConcreteBase):
    """Abstract class for structure Smf72Clrd - CML lock requestor data section."""

    r725cras: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="Address space ID.")
    r725crsu: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of times that a unit of work from this address space was suspended when requesting the local lock of another address space.")
    r725cral: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of times that a unit of work from this address space was suspended when requesting the local lock of another address space and there was already at least one other unit of work waiting for that lock.")
    r725crti: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total amount of time in milliseconds that a unit of work was suspended when requesting the local lock of another address space.")


class Smf72ense(AbstractConcreteBase):
    """Abstract class for structure Smf72Ense - GRS enqueue data."""

    r725enas: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="Address space ID.")
    r725enrc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of GRS ENQ requests with the scope as specified in R725ENSC for this address space.")
    r725ensu: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of GRS ENQ requests with the scope as specified in R725ENSC that were suspended for this address space.")
    r725enti: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total amount of suspend time in milliseconds that was caused by GRS ENQ requests with the scope as specified in R725ENSC for this address space.")
    r725ensq: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Sum of squares of the individual suspend times in milliseconds.")


class Smf72lotd(AbstractConcreteBase):
    """Abstract class for structure Smf72Lotd - Local lock data section."""

    r725loas: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="Address space ID.")
    r725losu: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of times that a unit of work of this address space was suspended on a local lock.")
    r725loal: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of times that a unit of work of this address space was suspended on a local lock when there was already at least one other unit of work suspended.")
    r725loti: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total amount of time in milliseconds that a unit of work of this address space was suspended on a local lock.")
    r725lcsu: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of times that a unit of work from another address space was suspended when requesting the local lock of this address space.")
    r725lcal: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of times that a unit of work from another address space was suspended when requesting the local lock of this address space and there was already at least one other unit of work waiting for that lock.")
    r725lcti: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total amount of time in milliseconds that a unit of work was suspended when requesting the local lock of this address space.")


class Smf72qsad(AbstractConcreteBase):
    """Abstract class for structure Smf72Qsad - GRS QScan statistics data section."""

    r725qsas: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="Address space ID.")
    r725qsrc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of requests including START and RESUME requests, but not QUIT requests.")
    r725qssc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of specific requests that are either GQSCAN requests specified by QNAME and RNAME, or ISGQUERY requests specifying a search by ENQTOKEN.")
    r725qsrr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of resources returned for these requests.")
    r725qsrq: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Sum of squares of number of resources returned for these requests.")
    r725qsti: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total amount of execution times within GRS for these requests in microseconds.")
    r725qstq: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Sum of squares of individual request execution times in microseconds.")
