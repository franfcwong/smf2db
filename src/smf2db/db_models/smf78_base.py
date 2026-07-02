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


class Base78(Base):
    __abstract__ = True
    metadata = sa.MetaData(schema='smf78', naming_convention=convention)


class Base78Hr(Base):
    __abstract__ = True
    metadata = sa.MetaData(schema='smf78', naming_convention=convention)


class Base78Da(Base):
    __abstract__ = True
    metadata = sa.MetaData(schema='smf78', naming_convention=convention)


class Smf78pro(AbstractConcreteBase):
    """Abstract class for structure Smf78Pro - RMF product section."""

    smf78mfv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="RMF version number.")
    smf78prd: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Product name ('RMF').")
    smf78int: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Duration of the RMF Monitor I measurement interval, in the form mmsstttF where mm is the minutes, ss is the seconds, ttt is the milliseconds, and F is the sign, (The end of the measurement interval is the sum of the recorded start time and this field.)")
    smf78sam: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of RMF samples.")
    smf78fla: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Flags Bit Meaning when set 0 Reserved 1 Samples have been skipped 2 Record was written by RMF Monitor III 3 Interval was synchronized with SMF 4 SMF record converted to lower service level. 5 SMF record converted to higher release or service level. 6 Running under an alternate virtual machine. 7 - 15")
    smf78cyc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Sampling cycle length, in the form 000 ttttF , where tttt is the milliseconds and F is the sign (taken from CYCLE option). The range")
    smf78mvs: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="z/OS software level (consists of an acronym and the version, release, and modification level - ZV vvrrmm ).")
    smf78iml: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Indicates the type of processor complex on which data measurements were taken. Value Meaning 3 9672, zSeries")
    smf78prf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Processor flags. Bit Meaning when set 0 The system has expanded storage 1 The processor is enabled for ES connection architecture (ESCA) 2 There is an ES connection director in the configuration 3 System is running in z/Architecture mode 4 At least one zAAP is currently installed 5 At least one zIIP is currently installed 6 Enhanced DAT facility 1 available 7 Enhanced DAT facility 2 available")
    smf78ptn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="PR/SM partition number of the partition that wrote this record.")
    smf78srl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="SMF record level change number (X'8E' for z/OS V2R4 RMF with RMF Data Gatherer APAR OA59330). This field enables processing of SMF record level changes in an existing release.")
    smf78lgo: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Offset GMT to local time (STCK format).")
    smf78oil: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Original interval length as defined in the session or by SMF (in seconds).")
    smf78syn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="SYNC value in seconds.")
    smf78gie: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                  doc="Projected gathering interval end (STCK format) GMT time.")
    smf78xnm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf78snm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="System name for current system as defined in parmlib member IEASYSxx SYSNAME parameter.")
    smf78flg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="System indicator Bit Meaning when set 0 New record format 1 Subtypes used 2 Reserved. 3-6 Version indicators* 7 System is running in PR/SM mode.")


class Smf78gd(AbstractConcreteBase):
    """Abstract class for structure Smf78gd - I/O queuing global section."""

    r783gflg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="IOQ global flags Bit Meaning when set 0 Incorrect data because channel measurement facility failed 1 DIAGNOSE interface failed 2 Store Primary Queue Data not supported 3 DCM supported by hardware 4 Configuration contains DCM managed channels 5 IOP utilization data supported 6 Initial command response time measurements supported 7 First-transfer-ready-disabled data available")
    r783gflx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="IOQ global flags extended Bit Meaning when set 0 Alias management groups available. 1 EADM compression facility available. 2 Storage-class memory measurement facility available. 3 - 7 Reserved.")
    r783gntr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of descriptor triplets following.")
    r783tsr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                         doc="Total number of small records written during interval.")
    r783tot: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                         doc="Total number of data sections recorded during the interval.")
    r783cfl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="Configuration change flags Bit Meaning when set 0 Configuration changed. Used to decide whether to provide the text 'POR' or 'ACTIVATE' on reports. Also used to check whether data can be combined in a duration report. 1 Configuration change since power on reset (POR). 2 POR using IOC data set that contains a token. 3 I/O token is valid. 4 Hardware allows multiple channel subsystems. 5-7 Reserved.")
    r783css: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4),
                                                         doc="Channel Subsystem ID. Only valid if bit 4 of R783CFL is set.")
    r783tnm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(44), doc="IODF name.")
    r783tsf: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2), doc="IODF name suffix.")
    r783tdt: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="IODF creation date, in the form mm/dd/yy .")
    r783ttm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="IODF creation time, in the form hh.mm.ss .")
    r783tdy: so.Mapped[Optional[str]] = so.mapped_column(sa.String(10),
                                                         doc="IODF creation date, in the form mm/dd/yyyy")
    data_invalid_ch_failure: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                         doc="r783gflg (Bit 0) showing incorrect data because channel measurement facility failed.")
    diagnose_failed: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                 doc="r783gflg (Bit 1) showing DIAGNOSE interface failed.")
    store_primary_not_supported: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                             doc="r783gflg (Bit 2) showing Store Primary Queue Data not supported.")
    dcm_hw_supported: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                  doc="r783gflg (Bit 3) showing DCM supported by hardware.")
    dcm_managed_ch: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                doc="r783gflg (Bit 4) showing configuration contains DCM amanged channels.")
    iop_util_data_supported: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                         doc="r783gflg (Bit 5) showing IOP utilization data supported.")
    command_response_time_supported: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                                 doc="r783gflg (Bit 6) showing initial command response time measurements supported.")
    transfer_ready_disabled_aval: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                              doc="r783gflg (Bit 7) showing first-transfer-ready-disabled data available.")
    alias_management_aval: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                       doc="r783gflx (Bit 0) showing alias management groups available.")
    eadm_compression_aval: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                       doc="r783gflx (Bit 1) showing EADM compression facility available.")
    scm_aval: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r783gflx (Bit 2) showing storage-class memory measurement facility available.")
    config_changed: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                doc="r783cfl (Bit 0) showing configuration changed. Used to decide whether to provide the text 'POR' or 'ACTIVATE' on reports. Also used to check whether data can be combined in a duration report.")
    config_changed_since_ipl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                          doc="r783cfl (Bit 1) showing configuration change since power on reset (POR).")
    ipl_iodf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r783cfl (Bit 2) showing POR using IOC data set that contains a token.")
    io_config_token_valid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                       doc="r783cfl (Bit 3) showing I/O token is valid.")
    multi_ch_subsys_allowed: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                         doc="r783cfl (Bit 4) showing hardware allows multiple channel subsystems.")


class Smf78iqd(AbstractConcreteBase):
    """Abstract class for structure Smf78iqd - IOP initiative queue and utilization data section."""

    r783iflg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Input output processor (IOP) Flags Bit Meaning when set 0 Input output processor (IOP) is installed. 1-7")
    r783iqsm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Accumulator is incremented by the current queue length in the Input output processor (IOP) whenever a request is enqueued.")
    r783iqct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of elements enqueued on the Input output processor (IOP) initiative queue.")
    r783iipb: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Number of times the I/O processor was busy.")
    r783iipi: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Number of times the I/O processor was idle.")
    r783iifs: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Number of I/O functions initially started.")
    r783ipii: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Number of processed I/O interrupts.")
    r783icpb: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of times an I/O was retried due to channel path busy.")
    r783idpb: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of times an I/O was retried due to director port busy.")
    r783icub: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of times an I/O was retried due to control unit busy.")
    r783idvb: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of times an I/O was retried due to device busy.")
    r783iscb: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of times the I/O processor was busy with SCM operations.")
    r783iecb: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of times the I/O processor was busy with compression or decompression.")
    smf78int: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Duration of the RMF Monitor I measurement interval, in the form mmsstttF where mm is the minutes, ss is the seconds, ttt is the milliseconds, and F is the sign, (The end of the measurement interval is the sum of the recorded start time and this field.)")
    iop_installed: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="r783iflg (Bit 0) showing Input Output Processor (IOP) is installed.")
    iopac: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="I/O processor (IOP) queue activity rate.")
    iopql: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                         doc="I/O processor (IOP) initiative queue average queue length.")
    iopipb: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="percent I/O processor busy.")
    iopecb: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                          doc="percent I/O processor busy with EADM compression/decompression.")
    iopscb: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="percent I/O processor busy with SCM.")
    iopipi: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="percent I/O processor idle.")
    iorifs: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="rate I/O functions started.")
    iorpii: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="rate processed I/O interrrupts.")
    iopalb: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="percent of I/O retries.")
    iopchb: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="percent of I/O retries due to channel busy.")
    iopdpb: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                          doc="percent of I/O retries due to director port busy.")
    iopcub: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                          doc="percent of I/O retries due to control unit busy.")
    iopdvb: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="percent of I/O retries due to device busy.")
    ionalb: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="percent of I/O retries per SSCH.")
    ionchb: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                          doc="number of I/O retries per SSCH due to channel busy.")
    iondpb: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                          doc="number of I/O retries per SSCH due to director port busy.")
    ioncub: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                          doc="number of I/O retries per SSCH due to control unit busy.")
    iondvb: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                          doc="number of I/O retries per SSCH due to device busy.")


class Smf78cpd(AbstractConcreteBase):
    """Abstract class for structure Smf78cpd - I/O queuing configuration data section."""

    r783cpst: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Channel path status Bit Meaning when set 0 Channel path installed 1 Channel path online 2 Channel path varied 3 Channel path offline to all devices of the LCU 4 Channel path connection to all devices of the LCU altered by VARY PATH command during interval 5 Measured channel path data incorrect 6 Channel path is DCM managed 7 CHPID manipulated, requiring data reset")
    r783cun: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of control units attached.")
    r783cu1: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="First control unit attached.")
    r783cu2: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Second control unit attached.")
    r783cu3: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Third control unit attached.")
    r783cu4: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Fourth control unit attached.")
    r783cub: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of times control unit was busy.")
    r783pt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of times channel path was taken.")
    r783dpb: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                         doc="Number of times that the Director Port was busy.")
    r783cbt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                         doc="Delay time of an I/O request because the control unit was busy.")
    r783cmr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                         doc="Initial command response time until the first command is indicated as accepted by the device.")
    r783sbs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                         doc="Switch busy count summation: contains the switch busy counts received for all partitions.")
    r783cpxf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Channel path extended flags Bit Meaning when set 0 Extended I/O measurement-block format-1 data available 1 Extended I/O measurement-block format-2 data available 2 First-transfer-ready-disabled supported")
    r783cpat: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Path attributes Value Meaning 0 Not specified for this path. 1 Preferred path. 2 Non-preferred path.")
    r783ctmw: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Transport mode write count")
    r783ctrd: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="First-transfer-ready-disabled write count")
    smf78int: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Duration of the RMF Monitor I measurement interval, in the form mmsstttF where mm is the minutes, ss is the seconds, ttt is the milliseconds, and F is the sign, (The end of the measurement interval is the sum of the recorded start time and this field.)")
    ioart: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="channel path taken rate.")
    iocub: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                         doc="percentage of requests caused by control unit busy.")
    iodpb: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                         doc="percentage of requests caused by director port busy.")
    iocbt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="average control unit busy delay time.")
    iocmr: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="average initial command reponse time.")
    ch_path_installed: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                   doc="r783cpst (Bit 0) showing channel path installed.")
    ch_path_online: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                doc="r783cpst (Bit 1) showing channel path online.")
    ch_path_varied: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                doc="r783cpst (Bit 2) showing channel path varied.")
    ch_path_offline: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                 doc="r783cpst (Bit 3) showing channel path offline to all devices of the LCU.")
    vary_path_action: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                  doc="r783cpst (Bit 4) showing channel path connection to all devices of the LCU altered by VARY PATH command during interval.")
    ch_path_data_invalid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                      doc="r783cpst (Bit 5) showing measured channel path data incorrect.")
    ch_path_dcm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                             doc="r783cpst (Bit 6) showing channel path is DCM managed.")
    chpid_manipulated: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                   doc="r783cpst (Bit 7) showing CHPID manipulated, requiring data reset.")
    extended_io_measurement1: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                          doc="r783cpxf (Bit 0) showing extended I/O measurement-block format-1 data available.")
    extended_io_measurement2: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                          doc="r783cpxf (Bit 1) showing extended I/O measurement-block format-2 data available.")
    first_transfer_ready_disabled: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                               doc="r783cpxf (Bit 2) showing first-transfer-ready-disabled supported.")


class Smf78ds(AbstractConcreteBase):
    """Abstract class for structure Smf78ds - I/O queuing data section."""

    r783dst: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                         doc="Data Status Bit Meaning when set 0 No hardware measurements available 1 Dynamically changed 2 Dynamically added 3 Configuration change attempted 4 LCU contains DCM managed channels 5 Path attributes are valid. 6 LCU has HyperPAV devices. 7 LCU has SuperPAV devices.")
    r783dstx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Data status extension. Bit Meaning when set 0 LCU contains at least one FICON channel. 1 Connect time of at least one device is invalid. 2 Disconnect time of at least one device is invalid. 3-7 Reserved.")
    r783qsm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Sum of total length of the CU-HDR queue.")
    r783qct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of entries on the CU-HDR queue.")
    r783mcmn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Minimum number of DCM managed channels used.")
    r783mcmx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Maximum number of DCM managed channels used.")
    r783mcdf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Defined number of DCM managed channels.")
    r783ptm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                         doc="Accumulated path taken count for DCM managed channels.")
    r783dpbm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Accumulated director port busy count for DCM managed channels.")
    r783cubm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Accumulated control unit busy count for DCM managed channels.")
    r783cbtm: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Accumulated delay time for DCM-managed channels because of a busy control unit.")
    r783cmrm: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Accumulated initial command response time for DCM- managed channels.")
    r783sbsm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Switch busy count summation for DCM-managed channels.")
    r783dctm: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Accumulated device connect time in units of 128 microseconds.")
    r783ddtm: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Accumulated device disconnect time in units of 128 microseconds.")
    r783csst: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Channel subsystem wait time in units of 128 microseconds.")
    r783tmwm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Accumulated transport mode write count for DCM managed channels.")
    r783trdm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Accumulated first-transfer-ready-disabled write count for DCM managed channels.")
    smf78int: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Duration of the RMF Monitor I measurement interval, in the form mmsstttF where mm is the minutes, ss is the seconds, ttt is the milliseconds, and F is the sign, (The end of the measurement interval is the sum of the recorded start time and this field.)")
    ioctr: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="contention rate.")
    iodlq: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="average queue length of delayed I/O requests.")
    iocss: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="average channel subsystem delay time.")
    iohwait: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="HyperPAV wait ratio.")
    iohmax: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="maximum number of in-use HyperPAV aliases.")
    iohdmax: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="maximum number of in-use HyperPAV aliaes for one device.")
    iohioqc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="the high watermark of queued I/O requests.")
    no_hw_measurement: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                   doc="r783dst (Bit 0) showing no hardware measurements available.")
    dynamically_changed: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                     doc="r783dst (Bit 1) showing dynamically changed.")
    dynamically_added: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                   doc="r783dst (Bit 2) showing dynamically added.")
    config_change_attempt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                       doc="r783dst (Bit 3) showing configuration change attempted.")
    lcu_has_dcm_ch: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                doc="r783dst (Bit 4) showing LCU contains DCM managed channels.")
    path_attr_valid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                 doc="r783dst (Bit 5) showing path attributes are valid.")
    lcu_has_hyperpav: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                  doc="r783dst (Bit 6) showing LCU has HyperPAV devices.")
    lcu_has_superpav: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                  doc="r783dst (Bit 7) showing LCU has SuperPAV devices.")
    lcu_has_ficon: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="r783dstx (Bit 0) showing LCU contains at least one FICON channel.")
    connect_time_invalid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                      doc="r783dstx (Bit 1) showing connect time of at least one device is invalid.")
    disconnect_time_invalid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                         doc="r783dstx (Bit 2) showing disconnect time of at least one device is invalid.")


class Smf78hpav(AbstractConcreteBase):
    """Abstract class for structure Smf78hpav - HyperPAV/SuperPAV data section."""

    r783hcu: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="HyperPAV control unit identifier.")
    r783hnai: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="The number of times an I/O could not start because no HyperPAV- aliases were available.")
    r783htio: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="The total number of HyperPAV I/O requests for the LSS.")
    r783haiu: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="The high water mark of the number of in-use HyperPAV-alias devices for the LSS (does not include borrowed alias devices).")
    r783hcad: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="The high water mark of the number of aliases concurrently in use by one of the HyperPAV-base devices of the LSS (including loaned alias devices).")
    r783hioq: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="The high water mark of queued I/O requests.")
    r783xanc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="The number of times an alias was needed to start an I/O.")
    r783xauc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="The number of times an alias was needed to start an I/O and one was used.")
    r783xnhc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="The number of times an alias was needed to start an I/O, but none was available in the home LCU. Valid only if bit 7 of R783DST is set.")
    r783xabc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="The number of times an alias was borrowed from a peer LCU. Valid only if bit 7 of R783DST is set.")
    r783xcbc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="The number of aliases concurrently borrowed from peer LCUs. Valid only if bit 7 of R783DST is set.")
    r783xhbc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="The high water mark of concurrently borrowed aliases from peer LCUs. Valid only if bit 7 of R783DST is set.")
    r783xalc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="The number of times an alias was loaned to a peer LCU. Valid only if bit 7 of R783DST is set.")
    r783xclc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="The number of aliases concurrently loaned to peer LCUs. Valid only if bit 7 of R783DST is set.")
    r783xhlc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="The high water mark of concurrently loaned aliases to peer LCUs. Valid only if bit 7 of R783DST is set.")
    r783xnag: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="The number of attempts that were made to borrow an alias from peer LCUs, but none were available. Valid only if bit 7 of R783DST is set.")
    r783xcqd: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="The cumulative number of I/Os queued at the subsystem level when aliases were needed.")
    r783xciu: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="The cumulative number of aliases defined to this subsystem that were in use when aliases were needed.")


class Smf78comn(AbstractConcreteBase):
    """Abstract class for structure Smf78Comn - Virtual storage common storage data section."""

    r782pa: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Private area address below 16 megabytes.")
    r782ps: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                        doc="Private area size (in bytes) below 16 megabytes.")
    r782epa: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Private area address above 16 megabytes.")
    r782eps: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                         doc="Private area size (in bytes) above 16 megabytes.")
    r782ca: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="CSA address below 16 megabytes.")
    r782cs: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="CSA size (in bytes) below 16 megabytes.")
    r782eca: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="CSA address above 16 megabytes.")
    r782ecs: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="CSA size (in bytes) above 16 megabytes.")
    r782flg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                         doc="Flags: Bit Meaning when set 0 Restricted use common service area (RUCSA) is defined.")
    r782mla: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                         doc="Modified link pack area (MLPA) address below 16 megabytes.")
    r782mls: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                         doc="Modified link pack area (MLPA) size (in bytes) below 16 megabytes.")
    r782emla: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="Modified link pack area (MLPA) address above 16 megabytes.")
    r782emls: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Modified link pack area (MLPA) size (in bytes) above 16 megabytes.")
    r782fla: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                         doc="Fixed link pack area (FLPA) address below 16 megabytes.")
    r782fls: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                         doc="Fixed link pack area (FLPA) size (in bytes) below 16 megabytes.")
    r782efla: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="Fixed link pack area (FLPA) address above 16 megabytes.")
    r782efls: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Fixed link pack area (FLPA) size (in bytes) above 16 megabytes.")
    r782pla: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                         doc="Pageable link pack area (PLPA) address below 16 megabytes.")
    r782pls: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                         doc="Pageable link pack area (PLPA) size (in bytes) below 16 megabytes.")
    r782elpa: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="Pageable link pack area (PLPA) address above 16 megabytes.")
    r782elps: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Pageable link pack area (PLPA) size (in bytes) above 16 megabytes.")
    r782sa: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                        doc="System queue area (SQA) address below 16 megabytes.")
    r782ss: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                        doc="System queue area (SQA) size (in bytes) below 16 megabytes.")
    r782esa: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                         doc="System queue area (SQA) address above 16 megabytes.")
    r782ess: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                         doc="System queue area (SQA) size (in bytes) above 16 megabytes.")
    r782na: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Nucleus address below 16 megabytes.")
    r782ns: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                        doc="Nucleus size (in bytes) below 16 megabytes.")
    r782ena: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Nucleus address above 16 megabytes.")
    r782ens: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                         doc="Nucleus size (in bytes) above 16 megabytes.")
    r782nl: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                        doc="Pageable link pack area (PLPA) space redundant with MLPA/FLPA below 16 megabytes.")
    r782enl: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                         doc="Pageable link pack area (PLPA) space redundant with MLPA/FLPA above 16 megabytes.")
    r782lpai: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Intermodule space in Pageable link pack area (PLPA) below 16 megabytes.")
    r782elpi: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Intermodule space in Pageable link pack area (PLPA) above 16 megabytes.")
    r782mr: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                        doc="Maximum possible user region below 16 megabytes.")
    r782emr: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                         doc="Maximum possible user region above 16 megabytes.")
    sqau_vsdbmin: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="System queue area (SQA) usage both above and below 16 megabytes. The description of the format of all fields being marked as 'Mixed(1)' can be found in Table 16 on page 745 and Table 17 on page 746. - Minimum value for below 16 megabytes.")
    sqau_vsdbntme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="System queue area (SQA) usage both above and below 16 megabytes. The description of the format of all fields being marked as 'Mixed(1)' can be found in Table 16 on page 745 and Table 17 on page 746. - Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    sqau_vsdbmax: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="System queue area (SQA) usage both above and below 16 megabytes. The description of the format of all fields being marked as 'Mixed(1)' can be found in Table 16 on page 745 and Table 17 on page 746. - Maximum value for below 16 megabytes.")
    sqau_vsdbxtme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="System queue area (SQA) usage both above and below 16 megabytes. The description of the format of all fields being marked as 'Mixed(1)' can be found in Table 16 on page 745 and Table 17 on page 746. - Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    sqau_vsdbtotl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="System queue area (SQA) usage both above and below 16 megabytes. The description of the format of all fields being marked as 'Mixed(1)' can be found in Table 16 on page 745 and Table 17 on page 746. - Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    sqau_vsdamin: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="System queue area (SQA) usage both above and below 16 megabytes. The description of the format of all fields being marked as 'Mixed(1)' can be found in Table 16 on page 745 and Table 17 on page 746. - Minimum value for above 16 megabytes.")
    sqau_vsdantme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="System queue area (SQA) usage both above and below 16 megabytes. The description of the format of all fields being marked as 'Mixed(1)' can be found in Table 16 on page 745 and Table 17 on page 746. - Time stamp for minimum. Format is high-order bytes of time-of- day (TOD) clock.")
    sqau_vsdamax: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="System queue area (SQA) usage both above and below 16 megabytes. The description of the format of all fields being marked as 'Mixed(1)' can be found in Table 16 on page 745 and Table 17 on page 746. - Maximum value for above 16 megabytes.")
    sqau_vsdaxtme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="System queue area (SQA) usage both above and below 16 megabytes. The description of the format of all fields being marked as 'Mixed(1)' can be found in Table 16 on page 745 and Table 17 on page 746. - Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    sqau_vsdatotl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="System queue area (SQA) usage both above and below 16 megabytes. The description of the format of all fields being marked as 'Mixed(1)' can be found in Table 16 on page 745 and Table 17 on page 746. - Total for all samples above 16 megabytes (used to calculate average).")
    csau_vsdbmin: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="CSA usage both above and below 16 megabytes, including RUCSA. - Minimum value for below 16 megabytes.")
    csau_vsdbntme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="CSA usage both above and below 16 megabytes, including RUCSA. - Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    csau_vsdbmax: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="CSA usage both above and below 16 megabytes, including RUCSA. - Maximum value for below 16 megabytes.")
    csau_vsdbxtme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="CSA usage both above and below 16 megabytes, including RUCSA. - Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    csau_vsdbtotl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="CSA usage both above and below 16 megabytes, including RUCSA. - Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    csau_vsdamin: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="CSA usage both above and below 16 megabytes, including RUCSA. - Minimum value for above 16 megabytes.")
    csau_vsdantme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="CSA usage both above and below 16 megabytes, including RUCSA. - Time stamp for minimum. Format is high-order bytes of time-of- day (TOD) clock.")
    csau_vsdamax: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="CSA usage both above and below 16 megabytes, including RUCSA. - Maximum value for above 16 megabytes.")
    csau_vsdaxtme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="CSA usage both above and below 16 megabytes, including RUCSA. - Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    csau_vsdatotl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="CSA usage both above and below 16 megabytes, including RUCSA. - Total for all samples above 16 megabytes (used to calculate average).")
    csak_vsdbmin_0: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 0) Minimum value for below 16 megabytes.")
    csak_vsdbntme_0: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                         doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 0) Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    csak_vsdbmax_0: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 0) Maximum value for below 16 megabytes.")
    csak_vsdbxtme_0: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                         doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 0) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    csak_vsdbtotl_0: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                   doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 0) Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    csak_vsdamin_0: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 0) Minimum value for above 16 megabytes.")
    csak_vsdantme_0: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                         doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 0) Time stamp for minimum. Format is high-order bytes of time-of- day (TOD) clock.")
    csak_vsdamax_0: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 0) Maximum value for above 16 megabytes.")
    csak_vsdaxtme_0: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                         doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 0) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    csak_vsdatotl_0: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                   doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 0) Total for all samples above 16 megabytes (used to calculate average).")
    csak_vsdbmin_1: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 1) Minimum value for below 16 megabytes.")
    csak_vsdbntme_1: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                         doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 1) Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    csak_vsdbmax_1: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 1) Maximum value for below 16 megabytes.")
    csak_vsdbxtme_1: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                         doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 1) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    csak_vsdbtotl_1: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                   doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 1) Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    csak_vsdamin_1: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 1) Minimum value for above 16 megabytes.")
    csak_vsdantme_1: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                         doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 1) Time stamp for minimum. Format is high-order bytes of time-of- day (TOD) clock.")
    csak_vsdamax_1: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 1) Maximum value for above 16 megabytes.")
    csak_vsdaxtme_1: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                         doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 1) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    csak_vsdatotl_1: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                   doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 1) Total for all samples above 16 megabytes (used to calculate average).")
    csak_vsdbmin_2: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 2) Minimum value for below 16 megabytes.")
    csak_vsdbntme_2: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                         doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 2) Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    csak_vsdbmax_2: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 2) Maximum value for below 16 megabytes.")
    csak_vsdbxtme_2: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                         doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 2) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    csak_vsdbtotl_2: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                   doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 2) Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    csak_vsdamin_2: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 2) Minimum value for above 16 megabytes.")
    csak_vsdantme_2: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                         doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 2) Time stamp for minimum. Format is high-order bytes of time-of- day (TOD) clock.")
    csak_vsdamax_2: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 2) Maximum value for above 16 megabytes.")
    csak_vsdaxtme_2: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                         doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 2) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    csak_vsdatotl_2: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                   doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 2) Total for all samples above 16 megabytes (used to calculate average).")
    csak_vsdbmin_3: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 3) Minimum value for below 16 megabytes.")
    csak_vsdbntme_3: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                         doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 3) Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    csak_vsdbmax_3: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 3) Maximum value for below 16 megabytes.")
    csak_vsdbxtme_3: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                         doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 3) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    csak_vsdbtotl_3: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                   doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 3) Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    csak_vsdamin_3: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 3) Minimum value for above 16 megabytes.")
    csak_vsdantme_3: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                         doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 3) Time stamp for minimum. Format is high-order bytes of time-of- day (TOD) clock.")
    csak_vsdamax_3: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 3) Maximum value for above 16 megabytes.")
    csak_vsdaxtme_3: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                         doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 3) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    csak_vsdatotl_3: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                   doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 3) Total for all samples above 16 megabytes (used to calculate average).")
    csak_vsdbmin_4: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 4) Minimum value for below 16 megabytes.")
    csak_vsdbntme_4: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                         doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 4) Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    csak_vsdbmax_4: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 4) Maximum value for below 16 megabytes.")
    csak_vsdbxtme_4: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                         doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 4) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    csak_vsdbtotl_4: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                   doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 4) Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    csak_vsdamin_4: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 4) Minimum value for above 16 megabytes.")
    csak_vsdantme_4: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                         doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 4) Time stamp for minimum. Format is high-order bytes of time-of- day (TOD) clock.")
    csak_vsdamax_4: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 4) Maximum value for above 16 megabytes.")
    csak_vsdaxtme_4: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                         doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 4) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    csak_vsdatotl_4: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                   doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 4) Total for all samples above 16 megabytes (used to calculate average).")
    csak_vsdbmin_5: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 5) Minimum value for below 16 megabytes.")
    csak_vsdbntme_5: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                         doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 5) Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    csak_vsdbmax_5: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 5) Maximum value for below 16 megabytes.")
    csak_vsdbxtme_5: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                         doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 5) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    csak_vsdbtotl_5: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                   doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 5) Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    csak_vsdamin_5: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 5) Minimum value for above 16 megabytes.")
    csak_vsdantme_5: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                         doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 5) Time stamp for minimum. Format is high-order bytes of time-of- day (TOD) clock.")
    csak_vsdamax_5: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 5) Maximum value for above 16 megabytes.")
    csak_vsdaxtme_5: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                         doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 5) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    csak_vsdatotl_5: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                   doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 5) Total for all samples above 16 megabytes (used to calculate average).")
    csak_vsdbmin_6: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 6) Minimum value for below 16 megabytes.")
    csak_vsdbntme_6: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                         doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 6) Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    csak_vsdbmax_6: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 6) Maximum value for below 16 megabytes.")
    csak_vsdbxtme_6: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                         doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 6) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    csak_vsdbtotl_6: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                   doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 6) Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    csak_vsdamin_6: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 6) Minimum value for above 16 megabytes.")
    csak_vsdantme_6: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                         doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 6) Time stamp for minimum. Format is high-order bytes of time-of- day (TOD) clock.")
    csak_vsdamax_6: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 6) Maximum value for above 16 megabytes.")
    csak_vsdaxtme_6: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                         doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 6) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    csak_vsdatotl_6: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                   doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 6) Total for all samples above 16 megabytes (used to calculate average).")
    csak_vsdbmin_7: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 7) Minimum value for below 16 megabytes.")
    csak_vsdbntme_7: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                         doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 7) Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    csak_vsdbmax_7: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 7) Maximum value for below 16 megabytes.")
    csak_vsdbxtme_7: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                         doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 7) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    csak_vsdbtotl_7: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                   doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 7) Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    csak_vsdamin_7: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 7) Minimum value for above 16 megabytes.")
    csak_vsdantme_7: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                         doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 7) Time stamp for minimum. Format is high-order bytes of time-of- day (TOD) clock.")
    csak_vsdamax_7: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 7) Maximum value for above 16 megabytes.")
    csak_vsdaxtme_7: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                         doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 7) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    csak_vsdatotl_7: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                   doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 7) Total for all samples above 16 megabytes (used to calculate average).")
    csak_vsdbmin_8: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 8) Minimum value for below 16 megabytes.")
    csak_vsdbntme_8: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                         doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 8) Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    csak_vsdbmax_8: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 8) Maximum value for below 16 megabytes.")
    csak_vsdbxtme_8: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                         doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 8) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    csak_vsdbtotl_8: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                   doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 8) Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    csak_vsdamin_8: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 8) Minimum value for above 16 megabytes.")
    csak_vsdantme_8: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                         doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 8) Time stamp for minimum. Format is high-order bytes of time-of- day (TOD) clock.")
    csak_vsdamax_8: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 8) Maximum value for above 16 megabytes.")
    csak_vsdaxtme_8: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                         doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 8) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    csak_vsdatotl_8: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                   doc="CSA used both above and below 16 megabytes by subpool key. 40 bytes for each of 9 keys. - (Key 8) Total for all samples above 16 megabytes (used to calculate average).")
    csaf_vsdbmin: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="Free CSA both above and below 16 megabytes, including RUCSA. - Minimum value for below 16 megabytes.")
    csaf_vsdbntme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="Free CSA both above and below 16 megabytes, including RUCSA. - Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    csaf_vsdbmax: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="Free CSA both above and below 16 megabytes, including RUCSA. - Maximum value for below 16 megabytes.")
    csaf_vsdbxtme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="Free CSA both above and below 16 megabytes, including RUCSA. - Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    csaf_vsdbtotl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="Free CSA both above and below 16 megabytes, including RUCSA. - Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    csaf_vsdamin: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="Free CSA both above and below 16 megabytes, including RUCSA. - Minimum value for above 16 megabytes.")
    csaf_vsdantme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="Free CSA both above and below 16 megabytes, including RUCSA. - Time stamp for minimum. Format is high-order bytes of time-of- day (TOD) clock.")
    csaf_vsdamax: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="Free CSA both above and below 16 megabytes, including RUCSA. - Maximum value for above 16 megabytes.")
    csaf_vsdaxtme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="Free CSA both above and below 16 megabytes, including RUCSA. - Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    csaf_vsdatotl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="Free CSA both above and below 16 megabytes, including RUCSA. - Total for all samples above 16 megabytes (used to calculate average).")
    cslf_vsdbmin: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="Largest free block of CSA both above and below 16 megabytes; can either be CSA or RUCSA. - Minimum value for below 16 megabytes.")
    cslf_vsdbntme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="Largest free block of CSA both above and below 16 megabytes; can either be CSA or RUCSA. - Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    cslf_vsdbmax: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="Largest free block of CSA both above and below 16 megabytes; can either be CSA or RUCSA. - Maximum value for below 16 megabytes.")
    cslf_vsdbxtme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="Largest free block of CSA both above and below 16 megabytes; can either be CSA or RUCSA. - Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    cslf_vsdbtotl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="Largest free block of CSA both above and below 16 megabytes; can either be CSA or RUCSA. - Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    cslf_vsdamin: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="Largest free block of CSA both above and below 16 megabytes; can either be CSA or RUCSA. - Minimum value for above 16 megabytes.")
    cslf_vsdantme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="Largest free block of CSA both above and below 16 megabytes; can either be CSA or RUCSA. - Time stamp for minimum. Format is high-order bytes of time-of- day (TOD) clock.")
    cslf_vsdamax: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="Largest free block of CSA both above and below 16 megabytes; can either be CSA or RUCSA. - Maximum value for above 16 megabytes.")
    cslf_vsdaxtme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="Largest free block of CSA both above and below 16 megabytes; can either be CSA or RUCSA. - Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    cslf_vsdatotl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="Largest free block of CSA both above and below 16 megabytes; can either be CSA or RUCSA. - Total for all samples above 16 megabytes (used to calculate average).")
    csal_vsdbmin: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="CSA allocated area size (in bytes) both above and below 16 megabytes, including RUCSA. - Minimum value for below 16 megabytes.")
    csal_vsdbntme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="CSA allocated area size (in bytes) both above and below 16 megabytes, including RUCSA. - Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    csal_vsdbmax: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="CSA allocated area size (in bytes) both above and below 16 megabytes, including RUCSA. - Maximum value for below 16 megabytes.")
    csal_vsdbxtme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="CSA allocated area size (in bytes) both above and below 16 megabytes, including RUCSA. - Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    csal_vsdbtotl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="CSA allocated area size (in bytes) both above and below 16 megabytes, including RUCSA. - Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    csal_vsdamin: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="CSA allocated area size (in bytes) both above and below 16 megabytes, including RUCSA. - Minimum value for above 16 megabytes.")
    csal_vsdantme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="CSA allocated area size (in bytes) both above and below 16 megabytes, including RUCSA. - Time stamp for minimum. Format is high-order bytes of time-of- day (TOD) clock.")
    csal_vsdamax: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="CSA allocated area size (in bytes) both above and below 16 megabytes, including RUCSA. - Maximum value for above 16 megabytes.")
    csal_vsdaxtme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="CSA allocated area size (in bytes) both above and below 16 megabytes, including RUCSA. - Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    csal_vsdatotl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="CSA allocated area size (in bytes) both above and below 16 megabytes, including RUCSA. - Total for all samples above 16 megabytes (used to calculate average).")
    sqaf_vsdbmin: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="Free system queue area (SQA) both above and below 16 megabytes. - Minimum value for below 16 megabytes.")
    sqaf_vsdbntme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="Free system queue area (SQA) both above and below 16 megabytes. - Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    sqaf_vsdbmax: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="Free system queue area (SQA) both above and below 16 megabytes. - Maximum value for below 16 megabytes.")
    sqaf_vsdbxtme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="Free system queue area (SQA) both above and below 16 megabytes. - Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    sqaf_vsdbtotl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="Free system queue area (SQA) both above and below 16 megabytes. - Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    sqaf_vsdamin: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="Free system queue area (SQA) both above and below 16 megabytes. - Minimum value for above 16 megabytes.")
    sqaf_vsdantme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="Free system queue area (SQA) both above and below 16 megabytes. - Time stamp for minimum. Format is high-order bytes of time-of- day (TOD) clock.")
    sqaf_vsdamax: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="Free system queue area (SQA) both above and below 16 megabytes. - Maximum value for above 16 megabytes.")
    sqaf_vsdaxtme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="Free system queue area (SQA) both above and below 16 megabytes. - Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    sqaf_vsdatotl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="Free system queue area (SQA) both above and below 16 megabytes. - Total for all samples above 16 megabytes (used to calculate average).")
    sqlf_vsdbmin: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="Largest free block of system queue area (SQA) both above and below 16 megabytes. - Minimum value for below 16 megabytes.")
    sqlf_vsdbntme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="Largest free block of system queue area (SQA) both above and below 16 megabytes. - Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    sqlf_vsdbmax: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="Largest free block of system queue area (SQA) both above and below 16 megabytes. - Maximum value for below 16 megabytes.")
    sqlf_vsdbxtme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="Largest free block of system queue area (SQA) both above and below 16 megabytes. - Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    sqlf_vsdbtotl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="Largest free block of system queue area (SQA) both above and below 16 megabytes. - Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    sqlf_vsdamin: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="Largest free block of system queue area (SQA) both above and below 16 megabytes. - Minimum value for above 16 megabytes.")
    sqlf_vsdantme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="Largest free block of system queue area (SQA) both above and below 16 megabytes. - Time stamp for minimum. Format is high-order bytes of time-of- day (TOD) clock.")
    sqlf_vsdamax: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="Largest free block of system queue area (SQA) both above and below 16 megabytes. - Maximum value for above 16 megabytes.")
    sqlf_vsdaxtme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="Largest free block of system queue area (SQA) both above and below 16 megabytes. - Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    sqlf_vsdatotl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="Largest free block of system queue area (SQA) both above and below 16 megabytes. - Total for all samples above 16 megabytes (used to calculate average).")
    sqal_vsdbmin: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="System queue area (SQA) allocated area size (in bytes) both above and below 16 megabytes. - Minimum value for below 16 megabytes.")
    sqal_vsdbntme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="System queue area (SQA) allocated area size (in bytes) both above and below 16 megabytes. - Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    sqal_vsdbmax: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="System queue area (SQA) allocated area size (in bytes) both above and below 16 megabytes. - Maximum value for below 16 megabytes.")
    sqal_vsdbxtme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="System queue area (SQA) allocated area size (in bytes) both above and below 16 megabytes. - Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    sqal_vsdbtotl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="System queue area (SQA) allocated area size (in bytes) both above and below 16 megabytes. - Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    sqal_vsdamin: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="System queue area (SQA) allocated area size (in bytes) both above and below 16 megabytes. - Minimum value for above 16 megabytes.")
    sqal_vsdantme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="System queue area (SQA) allocated area size (in bytes) both above and below 16 megabytes. - Time stamp for minimum. Format is high-order bytes of time-of- day (TOD) clock.")
    sqal_vsdamax: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="System queue area (SQA) allocated area size (in bytes) both above and below 16 megabytes. - Maximum value for above 16 megabytes.")
    sqal_vsdaxtme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="System queue area (SQA) allocated area size (in bytes) both above and below 16 megabytes. - Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    sqal_vsdatotl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="System queue area (SQA) allocated area size (in bytes) both above and below 16 megabytes. - Total for all samples above 16 megabytes (used to calculate average).")
    sqex_vsdbmin: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="System queue area (SQA) expansion into CSA both above and below 16 megabytes. - Minimum value for below 16 megabytes.")
    sqex_vsdbntme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="System queue area (SQA) expansion into CSA both above and below 16 megabytes. - Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    sqex_vsdbmax: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="System queue area (SQA) expansion into CSA both above and below 16 megabytes. - Maximum value for below 16 megabytes.")
    sqex_vsdbxtme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="System queue area (SQA) expansion into CSA both above and below 16 megabytes. - Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    sqex_vsdbtotl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="System queue area (SQA) expansion into CSA both above and below 16 megabytes. - Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    sqex_vsdamin: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="System queue area (SQA) expansion into CSA both above and below 16 megabytes. - Minimum value for above 16 megabytes.")
    sqex_vsdantme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="System queue area (SQA) expansion into CSA both above and below 16 megabytes. - Time stamp for minimum. Format is high-order bytes of time-of- day (TOD) clock.")
    sqex_vsdamax: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="System queue area (SQA) expansion into CSA both above and below 16 megabytes. - Maximum value for above 16 megabytes.")
    sqex_vsdaxtme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="System queue area (SQA) expansion into CSA both above and below 16 megabytes. - Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    sqex_vsdatotl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="System queue area (SQA) expansion into CSA both above and below 16 megabytes. - Total for all samples above 16 megabytes (used to calculate average).")
    s227k_vsdbmin_0: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 227 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 0) Minimum value for below 16 megabytes.")
    s227k_vsdbntme_0: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 227 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 0) Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    s227k_vsdbmax_0: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 227 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 0) Maximum value for below 16 megabytes.")
    s227k_vsdbxtme_0: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 227 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 0) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    s227k_vsdbtotl_0: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="CSA subpool 227 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 0) Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    s227k_vsdbmin_1: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 227 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 1) Minimum value for below 16 megabytes.")
    s227k_vsdbntme_1: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 227 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 1) Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    s227k_vsdbmax_1: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 227 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 1) Maximum value for below 16 megabytes.")
    s227k_vsdbxtme_1: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 227 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 1) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    s227k_vsdbtotl_1: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="CSA subpool 227 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 1) Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    s227k_vsdbmin_2: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 227 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 2) Minimum value for below 16 megabytes.")
    s227k_vsdbntme_2: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 227 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 2) Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    s227k_vsdbmax_2: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 227 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 2) Maximum value for below 16 megabytes.")
    s227k_vsdbxtme_2: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 227 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 2) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    s227k_vsdbtotl_2: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="CSA subpool 227 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 2) Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    s227k_vsdbmin_3: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 227 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 3) Minimum value for below 16 megabytes.")
    s227k_vsdbntme_3: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 227 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 3) Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    s227k_vsdbmax_3: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 227 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 3) Maximum value for below 16 megabytes.")
    s227k_vsdbxtme_3: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 227 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 3) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    s227k_vsdbtotl_3: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="CSA subpool 227 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 3) Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    s227k_vsdbmin_4: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 227 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 4) Minimum value for below 16 megabytes.")
    s227k_vsdbntme_4: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 227 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 4) Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    s227k_vsdbmax_4: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 227 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 4) Maximum value for below 16 megabytes.")
    s227k_vsdbxtme_4: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 227 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 4) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    s227k_vsdbtotl_4: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="CSA subpool 227 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 4) Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    s227k_vsdbmin_5: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 227 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 5) Minimum value for below 16 megabytes.")
    s227k_vsdbntme_5: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 227 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 5) Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    s227k_vsdbmax_5: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 227 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 5) Maximum value for below 16 megabytes.")
    s227k_vsdbxtme_5: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 227 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 5) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    s227k_vsdbtotl_5: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="CSA subpool 227 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 5) Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    s227k_vsdbmin_6: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 227 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 6) Minimum value for below 16 megabytes.")
    s227k_vsdbntme_6: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 227 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 6) Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    s227k_vsdbmax_6: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 227 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 6) Maximum value for below 16 megabytes.")
    s227k_vsdbxtme_6: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 227 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 6) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    s227k_vsdbtotl_6: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="CSA subpool 227 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 6) Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    s227k_vsdbmin_7: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 227 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 7) Minimum value for below 16 megabytes.")
    s227k_vsdbntme_7: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 227 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 7) Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    s227k_vsdbmax_7: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 227 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 7) Maximum value for below 16 megabytes.")
    s227k_vsdbxtme_7: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 227 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 7) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    s227k_vsdbtotl_7: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="CSA subpool 227 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 7) Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    s227k_vsdbmin_8: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 227 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 8) Minimum value for below 16 megabytes.")
    s227k_vsdbntme_8: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 227 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 8) Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    s227k_vsdbmax_8: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 227 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 8) Maximum value for below 16 megabytes.")
    s227k_vsdbxtme_8: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 227 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 8) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    s227k_vsdbtotl_8: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="CSA subpool 227 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 8) Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    s227k_vsdbmin_all: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                   doc="CSA subpool 227 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key all) Minimum value for below 16 megabytes.")
    s227k_vsdbntme_all: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                            doc="CSA subpool 227 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key all) Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    s227k_vsdbmax_all: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                   doc="CSA subpool 227 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key all) Maximum value for below 16 megabytes.")
    s227k_vsdbxtme_all: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                            doc="CSA subpool 227 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key all) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    s227k_vsdbtotl_all: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                      doc="CSA subpool 227 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key all) Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    s228k_vsdbmin_0: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 228 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 0) Minimum value for below 16 megabytes.")
    s228k_vsdbntme_0: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 228 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 0) Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    s228k_vsdbmax_0: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 228 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 0) Maximum value for below 16 megabytes.")
    s228k_vsdbxtme_0: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 228 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 0) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    s228k_vsdbtotl_0: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="CSA subpool 228 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 0) Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    s228k_vsdbmin_1: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 228 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 1) Minimum value for below 16 megabytes.")
    s228k_vsdbntme_1: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 228 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 1) Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    s228k_vsdbmax_1: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 228 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 1) Maximum value for below 16 megabytes.")
    s228k_vsdbxtme_1: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 228 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 1) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    s228k_vsdbtotl_1: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="CSA subpool 228 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 1) Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    s228k_vsdbmin_2: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 228 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 2) Minimum value for below 16 megabytes.")
    s228k_vsdbntme_2: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 228 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 2) Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    s228k_vsdbmax_2: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 228 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 2) Maximum value for below 16 megabytes.")
    s228k_vsdbxtme_2: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 228 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 2) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    s228k_vsdbtotl_2: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="CSA subpool 228 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 2) Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    s228k_vsdbmin_3: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 228 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 3) Minimum value for below 16 megabytes.")
    s228k_vsdbntme_3: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 228 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 3) Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    s228k_vsdbmax_3: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 228 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 3) Maximum value for below 16 megabytes.")
    s228k_vsdbxtme_3: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 228 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 3) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    s228k_vsdbtotl_3: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="CSA subpool 228 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 3) Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    s228k_vsdbmin_4: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 228 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 4) Minimum value for below 16 megabytes.")
    s228k_vsdbntme_4: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 228 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 4) Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    s228k_vsdbmax_4: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 228 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 4) Maximum value for below 16 megabytes.")
    s228k_vsdbxtme_4: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 228 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 4) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    s228k_vsdbtotl_4: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="CSA subpool 228 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 4) Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    s228k_vsdbmin_5: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 228 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 5) Minimum value for below 16 megabytes.")
    s228k_vsdbntme_5: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 228 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 5) Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    s228k_vsdbmax_5: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 228 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 5) Maximum value for below 16 megabytes.")
    s228k_vsdbxtme_5: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 228 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 5) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    s228k_vsdbtotl_5: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="CSA subpool 228 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 5) Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    s228k_vsdbmin_6: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 228 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 6) Minimum value for below 16 megabytes.")
    s228k_vsdbntme_6: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 228 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 6) Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    s228k_vsdbmax_6: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 228 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 6) Maximum value for below 16 megabytes.")
    s228k_vsdbxtme_6: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 228 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 6) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    s228k_vsdbtotl_6: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="CSA subpool 228 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 6) Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    s228k_vsdbmin_7: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 228 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 7) Minimum value for below 16 megabytes.")
    s228k_vsdbntme_7: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 228 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 7) Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    s228k_vsdbmax_7: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 228 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 7) Maximum value for below 16 megabytes.")
    s228k_vsdbxtme_7: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 228 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 7) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    s228k_vsdbtotl_7: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="CSA subpool 228 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 7) Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    s228k_vsdbmin_8: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 228 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 8) Minimum value for below 16 megabytes.")
    s228k_vsdbntme_8: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 228 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 8) Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    s228k_vsdbmax_8: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 228 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 8) Maximum value for below 16 megabytes.")
    s228k_vsdbxtme_8: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 228 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 8) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    s228k_vsdbtotl_8: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="CSA subpool 228 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 8) Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    s228k_vsdbmin_all: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                   doc="CSA subpool 228 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key all) Minimum value for below 16 megabytes.")
    s228k_vsdbntme_all: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                            doc="CSA subpool 228 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key all) Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    s228k_vsdbmax_all: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                   doc="CSA subpool 228 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key all) Maximum value for below 16 megabytes.")
    s228k_vsdbxtme_all: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                            doc="CSA subpool 228 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key all) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    s228k_vsdbtotl_all: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                      doc="CSA subpool 228 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key all) Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    s231k_vsdbmin_0: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 231 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 0) Minimum value for below 16 megabytes.")
    s231k_vsdbntme_0: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 231 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 0) Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    s231k_vsdbmax_0: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 231 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 0) Maximum value for below 16 megabytes.")
    s231k_vsdbxtme_0: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 231 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 0) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    s231k_vsdbtotl_0: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="CSA subpool 231 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 0) Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    s231k_vsdbmin_1: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 231 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 1) Minimum value for below 16 megabytes.")
    s231k_vsdbntme_1: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 231 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 1) Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    s231k_vsdbmax_1: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 231 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 1) Maximum value for below 16 megabytes.")
    s231k_vsdbxtme_1: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 231 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 1) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    s231k_vsdbtotl_1: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="CSA subpool 231 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 1) Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    s231k_vsdbmin_2: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 231 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 2) Minimum value for below 16 megabytes.")
    s231k_vsdbntme_2: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 231 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 2) Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    s231k_vsdbmax_2: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 231 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 2) Maximum value for below 16 megabytes.")
    s231k_vsdbxtme_2: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 231 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 2) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    s231k_vsdbtotl_2: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="CSA subpool 231 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 2) Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    s231k_vsdbmin_3: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 231 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 3) Minimum value for below 16 megabytes.")
    s231k_vsdbntme_3: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 231 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 3) Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    s231k_vsdbmax_3: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 231 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 3) Maximum value for below 16 megabytes.")
    s231k_vsdbxtme_3: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 231 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 3) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    s231k_vsdbtotl_3: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="CSA subpool 231 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 3) Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    s231k_vsdbmin_4: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 231 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 4) Minimum value for below 16 megabytes.")
    s231k_vsdbntme_4: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 231 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 4) Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    s231k_vsdbmax_4: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 231 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 4) Maximum value for below 16 megabytes.")
    s231k_vsdbxtme_4: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 231 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 4) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    s231k_vsdbtotl_4: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="CSA subpool 231 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 4) Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    s231k_vsdbmin_5: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 231 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 5) Minimum value for below 16 megabytes.")
    s231k_vsdbntme_5: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 231 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 5) Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    s231k_vsdbmax_5: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 231 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 5) Maximum value for below 16 megabytes.")
    s231k_vsdbxtme_5: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 231 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 5) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    s231k_vsdbtotl_5: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="CSA subpool 231 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 5) Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    s231k_vsdbmin_6: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 231 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 6) Minimum value for below 16 megabytes.")
    s231k_vsdbntme_6: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 231 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 6) Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    s231k_vsdbmax_6: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 231 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 6) Maximum value for below 16 megabytes.")
    s231k_vsdbxtme_6: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 231 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 6) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    s231k_vsdbtotl_6: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="CSA subpool 231 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 6) Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    s231k_vsdbmin_7: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 231 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 7) Minimum value for below 16 megabytes.")
    s231k_vsdbntme_7: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 231 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 7) Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    s231k_vsdbmax_7: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 231 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 7) Maximum value for below 16 megabytes.")
    s231k_vsdbxtme_7: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 231 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 7) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    s231k_vsdbtotl_7: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="CSA subpool 231 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 7) Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    s231k_vsdbmin_8: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 231 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 8) Minimum value for below 16 megabytes.")
    s231k_vsdbntme_8: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 231 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 8) Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    s231k_vsdbmax_8: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 231 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 8) Maximum value for below 16 megabytes.")
    s231k_vsdbxtme_8: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 231 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 8) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    s231k_vsdbtotl_8: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="CSA subpool 231 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 8) Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    s231k_vsdbmin_all: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                   doc="CSA subpool 231 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key all) Minimum value for below 16 megabytes.")
    s231k_vsdbntme_all: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                            doc="CSA subpool 231 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key all) Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    s231k_vsdbmax_all: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                   doc="CSA subpool 231 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key all) Maximum value for below 16 megabytes.")
    s231k_vsdbxtme_all: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                            doc="CSA subpool 231 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key all) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    s231k_vsdbtotl_all: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                      doc="CSA subpool 231 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key all) Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    s241k_vsdbmin_0: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 241 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 0) Minimum value for below 16 megabytes.")
    s241k_vsdbntme_0: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 241 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 0) Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    s241k_vsdbmax_0: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 241 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 0) Maximum value for below 16 megabytes.")
    s241k_vsdbxtme_0: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 241 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 0) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    s241k_vsdbtotl_0: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="CSA subpool 241 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 0) Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    s241k_vsdbmin_1: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 241 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 1) Minimum value for below 16 megabytes.")
    s241k_vsdbntme_1: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 241 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 1) Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    s241k_vsdbmax_1: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 241 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 1) Maximum value for below 16 megabytes.")
    s241k_vsdbxtme_1: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 241 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 1) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    s241k_vsdbtotl_1: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="CSA subpool 241 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 1) Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    s241k_vsdbmin_2: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 241 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 2) Minimum value for below 16 megabytes.")
    s241k_vsdbntme_2: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 241 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 2) Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    s241k_vsdbmax_2: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 241 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 2) Maximum value for below 16 megabytes.")
    s241k_vsdbxtme_2: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 241 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 2) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    s241k_vsdbtotl_2: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="CSA subpool 241 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 2) Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    s241k_vsdbmin_3: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 241 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 3) Minimum value for below 16 megabytes.")
    s241k_vsdbntme_3: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 241 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 3) Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    s241k_vsdbmax_3: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 241 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 3) Maximum value for below 16 megabytes.")
    s241k_vsdbxtme_3: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 241 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 3) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    s241k_vsdbtotl_3: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="CSA subpool 241 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 3) Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    s241k_vsdbmin_4: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 241 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 4) Minimum value for below 16 megabytes.")
    s241k_vsdbntme_4: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 241 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 4) Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    s241k_vsdbmax_4: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 241 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 4) Maximum value for below 16 megabytes.")
    s241k_vsdbxtme_4: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 241 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 4) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    s241k_vsdbtotl_4: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="CSA subpool 241 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 4) Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    s241k_vsdbmin_5: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 241 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 5) Minimum value for below 16 megabytes.")
    s241k_vsdbntme_5: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 241 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 5) Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    s241k_vsdbmax_5: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 241 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 5) Maximum value for below 16 megabytes.")
    s241k_vsdbxtme_5: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 241 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 5) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    s241k_vsdbtotl_5: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="CSA subpool 241 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 5) Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    s241k_vsdbmin_6: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 241 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 6) Minimum value for below 16 megabytes.")
    s241k_vsdbntme_6: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 241 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 6) Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    s241k_vsdbmax_6: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 241 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 6) Maximum value for below 16 megabytes.")
    s241k_vsdbxtme_6: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 241 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 6) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    s241k_vsdbtotl_6: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="CSA subpool 241 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 6) Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    s241k_vsdbmin_7: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 241 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 7) Minimum value for below 16 megabytes.")
    s241k_vsdbntme_7: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 241 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 7) Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    s241k_vsdbmax_7: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 241 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 7) Maximum value for below 16 megabytes.")
    s241k_vsdbxtme_7: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 241 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 7) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    s241k_vsdbtotl_7: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="CSA subpool 241 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 7) Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    s241k_vsdbmin_8: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 241 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 8) Minimum value for below 16 megabytes.")
    s241k_vsdbntme_8: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 241 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 8) Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    s241k_vsdbmax_8: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="CSA subpool 241 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 8) Maximum value for below 16 megabytes.")
    s241k_vsdbxtme_8: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="CSA subpool 241 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 8) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    s241k_vsdbtotl_8: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="CSA subpool 241 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key 8) Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    s241k_vsdbmin_all: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                   doc="CSA subpool 241 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key all) Minimum value for below 16 megabytes.")
    s241k_vsdbntme_all: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                            doc="CSA subpool 241 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key all) Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    s241k_vsdbmax_all: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                   doc="CSA subpool 241 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key all) Maximum value for below 16 megabytes.")
    s241k_vsdbxtme_all: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                            doc="CSA subpool 241 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key all) Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    s241k_vsdbtotl_all: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                      doc="CSA subpool 241 (below 16 megabytes) by key. The key data appears in the following order: 0, 1, 2, 3, 4, 5, 6, 7, 8-F, ALL. 20 bytes for each of 10 keys. - (Key all) Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    s226_vsdbmin: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="System queue area (SQA) subpool 226 (below 16 megabytes). - Minimum value for below 16 megabytes.")
    s226_vsdbntme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="System queue area (SQA) subpool 226 (below 16 megabytes). - Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    s226_vsdbmax: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="System queue area (SQA) subpool 226 (below 16 megabytes). - Maximum value for below 16 megabytes.")
    s226_vsdbxtme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="System queue area (SQA) subpool 226 (below 16 megabytes). - Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    s226_vsdbtotl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="System queue area (SQA) subpool 226 (below 16 megabytes). - Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    s239_vsdbmin: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="System queue area (SQA) subpool 239 (below 16 megabytes). - Minimum value for below 16 megabytes.")
    s239_vsdbntme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="System queue area (SQA) subpool 239 (below 16 megabytes). - Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    s239_vsdbmax: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="System queue area (SQA) subpool 239 (below 16 megabytes). - Maximum value for below 16 megabytes.")
    s239_vsdbxtme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="System queue area (SQA) subpool 239 (below 16 megabytes). - Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    s239_vsdbtotl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="System queue area (SQA) subpool 239 (below 16 megabytes). - Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    s245_vsdbmin: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="System queue area (SQA) subpool 245 (below 16 megabytes). - Minimum value for below 16 megabytes.")
    s245_vsdbntme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="System queue area (SQA) subpool 245 (below 16 megabytes). - Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    s245_vsdbmax: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="System queue area (SQA) subpool 245 (below 16 megabytes). - Maximum value for below 16 megabytes.")
    s245_vsdbxtme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="System queue area (SQA) subpool 245 (below 16 megabytes). - Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    s245_vsdbtotl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="System queue area (SQA) subpool 245 (below 16 megabytes). - Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    r782ruca: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="RUCSA address below 16 megabytes.")
    r782rucs: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="RUCSA size (in bytes) below 16 megabytes. Zero when RUCSA is not defined.")
    r782eruca: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                           doc="RUCSA address above 16 megabytes. Equal to R782EPA when extended RUCSA (ERUCSA) is not defined.")
    r782erucs: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                           doc="RUCSA size (in bytes) above 16 megabytes. Zero when ERUCSA is not defined.")
    r782rucd: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r782flg (Bit 0) showing restricted use common service area (RUCSA) is defined.")


class Smf78pvsp(AbstractConcreteBase):
    """Abstract class for structure Smf78Pvsp - Virtual storage private area subpool section."""

    spd_vsdbmin: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                             doc="Subpool data. - Minimum value for below 16 megabytes.")
    spd_vsdbntme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                      doc="Subpool data. - Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    spd_vsdbmax: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                             doc="Subpool data. - Maximum value for below 16 megabytes.")
    spd_vsdbxtme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                      doc="Subpool data. - Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    spd_vsdbtotl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="Subpool data. - Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")


class Smf78pvt(AbstractConcreteBase):
    """Abstract class for structure Smf78Pvt - Virtual storage private area data section."""

    r782rdtm: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Reader start time.")
    r782step: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="Name of step active when monitoring began.")
    r782pgmn: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="Program name (taken from PGM= parameter on EXEC card) of job being monitored.")
    r782flgs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Bit Meaning when set 0 Job active at start of interval. 1 Job terminated during interval. 2 GETMAIN limit changed during interval. 3 Data incorrect because RMF terminated abnormally while sampling. 4 Shared values above 2G available (z/OS V1R5 or later).")
    r782samp: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Number of samples. This field is used to calculate the averages in the private area data and Private Area Subpool sections.")
    r782regr: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Region requested by JCL (in bytes).")
    r782rgab: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Region below 16 megabytes assigned by exits (in bytes).")
    r782rgaa: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Region above 16 megabytes assigned by exits (in bytes).")
    r782gmlb: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="GETMAIN limit below 16 megabytes (in bytes).")
    r782gmla: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="GETMAIN limit above 16 megabytes (in bytes).")
    r782urab: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="User region address below 16 megabytes.")
    r782uraa: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="User region address above 16 megabytes.")
    lsfp_vsdbmin: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="LSQA/SWA/229/230/249 free pages both above and below 16 megabytes. - Minimum value for below 16 megabytes.")
    lsfp_vsdbntme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="LSQA/SWA/229/230/249 free pages both above and below 16 megabytes. - Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    lsfp_vsdbmax: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="LSQA/SWA/229/230/249 free pages both above and below 16 megabytes. - Maximum value for below 16 megabytes.")
    lsfp_vsdbxtme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="LSQA/SWA/229/230/249 free pages both above and below 16 megabytes. - Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    lsfp_vsdbtotl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="LSQA/SWA/229/230/249 free pages both above and below 16 megabytes. - Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    lsfp_vsdamin: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="LSQA/SWA/229/230/249 free pages both above and below 16 megabytes. - Minimum value for above 16 megabytes.")
    lsfp_vsdantme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="LSQA/SWA/229/230/249 free pages both above and below 16 megabytes. - Time stamp for minimum. Format is high-order bytes of time-of- day (TOD) clock.")
    lsfp_vsdamax: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="LSQA/SWA/229/230/249 free pages both above and below 16 megabytes. - Maximum value for above 16 megabytes.")
    lsfp_vsdaxtme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="LSQA/SWA/229/230/249 free pages both above and below 16 megabytes. - Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    lsfp_vsdatotl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="LSQA/SWA/229/230/249 free pages both above and below 16 megabytes. - Total for all samples above 16 megabytes (used to calculate average).")
    lsfb_vsdbmin: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="LSQA/SWA/229/230/249 largest free block both above and below 16 megabytes. - Minimum value for below 16 megabytes.")
    lsfb_vsdbntme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="LSQA/SWA/229/230/249 largest free block both above and below 16 megabytes. - Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    lsfb_vsdbmax: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="LSQA/SWA/229/230/249 largest free block both above and below 16 megabytes. - Maximum value for below 16 megabytes.")
    lsfb_vsdbxtme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="LSQA/SWA/229/230/249 largest free block both above and below 16 megabytes. - Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    lsfb_vsdbtotl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="LSQA/SWA/229/230/249 largest free block both above and below 16 megabytes. - Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    lsfb_vsdamin: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="LSQA/SWA/229/230/249 largest free block both above and below 16 megabytes. - Minimum value for above 16 megabytes.")
    lsfb_vsdantme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="LSQA/SWA/229/230/249 largest free block both above and below 16 megabytes. - Time stamp for minimum. Format is high-order bytes of time-of- day (TOD) clock.")
    lsfb_vsdamax: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="LSQA/SWA/229/230/249 largest free block both above and below 16 megabytes. - Maximum value for above 16 megabytes.")
    lsfb_vsdaxtme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="LSQA/SWA/229/230/249 largest free block both above and below 16 megabytes. - Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    lsfb_vsdatotl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="LSQA/SWA/229/230/249 largest free block both above and below 16 megabytes. - Total for all samples above 16 megabytes (used to calculate average).")
    lsal_vsdbmin: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="LSQA/SWA/229/230/249 allocated area size (in bytes) both above and below 16 megabytes. - Minimum value for below 16 megabytes.")
    lsal_vsdbntme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="LSQA/SWA/229/230/249 allocated area size (in bytes) both above and below 16 megabytes. - Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    lsal_vsdbmax: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="LSQA/SWA/229/230/249 allocated area size (in bytes) both above and below 16 megabytes. - Maximum value for below 16 megabytes.")
    lsal_vsdbxtme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="LSQA/SWA/229/230/249 allocated area size (in bytes) both above and below 16 megabytes. - Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    lsal_vsdbtotl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="LSQA/SWA/229/230/249 allocated area size (in bytes) both above and below 16 megabytes. - Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    lsal_vsdamin: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="LSQA/SWA/229/230/249 allocated area size (in bytes) both above and below 16 megabytes. - Minimum value for above 16 megabytes.")
    lsal_vsdantme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="LSQA/SWA/229/230/249 allocated area size (in bytes) both above and below 16 megabytes. - Time stamp for minimum. Format is high-order bytes of time-of- day (TOD) clock.")
    lsal_vsdamax: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="LSQA/SWA/229/230/249 allocated area size (in bytes) both above and below 16 megabytes. - Maximum value for above 16 megabytes.")
    lsal_vsdaxtme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="LSQA/SWA/229/230/249 allocated area size (in bytes) both above and below 16 megabytes. - Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    lsal_vsdatotl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="LSQA/SWA/229/230/249 allocated area size (in bytes) both above and below 16 megabytes. - Total for all samples above 16 megabytes (used to calculate average).")
    lspa_vsdbmin: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="LSQA/SWA/229/230/249 allocated pages both above and below 16 megabytes. - Minimum value for below 16 megabytes.")
    lspa_vsdbntme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="LSQA/SWA/229/230/249 allocated pages both above and below 16 megabytes. - Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    lspa_vsdbmax: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="LSQA/SWA/229/230/249 allocated pages both above and below 16 megabytes. - Maximum value for below 16 megabytes.")
    lspa_vsdbxtme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="LSQA/SWA/229/230/249 allocated pages both above and below 16 megabytes. - Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    lspa_vsdbtotl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="LSQA/SWA/229/230/249 allocated pages both above and below 16 megabytes. - Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    lspa_vsdamin: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="LSQA/SWA/229/230/249 allocated pages both above and below 16 megabytes. - Minimum value for above 16 megabytes.")
    lspa_vsdantme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="LSQA/SWA/229/230/249 allocated pages both above and below 16 megabytes. - Time stamp for minimum. Format is high-order bytes of time-of- day (TOD) clock.")
    lspa_vsdamax: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="LSQA/SWA/229/230/249 allocated pages both above and below 16 megabytes. - Maximum value for above 16 megabytes.")
    lspa_vsdaxtme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="LSQA/SWA/229/230/249 allocated pages both above and below 16 megabytes. - Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    lspa_vsdatotl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="LSQA/SWA/229/230/249 allocated pages both above and below 16 megabytes. - Total for all samples above 16 megabytes (used to calculate average).")
    usfp_vsdbmin: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="User region free pages both above and below 16 megabytes. - Minimum value for below 16 megabytes.")
    usfp_vsdbntme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="User region free pages both above and below 16 megabytes. - Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    usfp_vsdbmax: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="User region free pages both above and below 16 megabytes. - Maximum value for below 16 megabytes.")
    usfp_vsdbxtme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="User region free pages both above and below 16 megabytes. - Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    usfp_vsdbtotl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="User region free pages both above and below 16 megabytes. - Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    usfp_vsdamin: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="User region free pages both above and below 16 megabytes. - Minimum value for above 16 megabytes.")
    usfp_vsdantme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="User region free pages both above and below 16 megabytes. - Time stamp for minimum. Format is high-order bytes of time-of- day (TOD) clock.")
    usfp_vsdamax: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="User region free pages both above and below 16 megabytes. - Maximum value for above 16 megabytes.")
    usfp_vsdaxtme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="User region free pages both above and below 16 megabytes. - Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    usfp_vsdatotl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="User region free pages both above and below 16 megabytes. - Total for all samples above 16 megabytes (used to calculate average).")
    usfb_vsdbmin: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="User region largest free block both above and below 16 megabytes. - Minimum value for below 16 megabytes.")
    usfb_vsdbntme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="User region largest free block both above and below 16 megabytes. - Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    usfb_vsdbmax: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="User region largest free block both above and below 16 megabytes. - Maximum value for below 16 megabytes.")
    usfb_vsdbxtme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="User region largest free block both above and below 16 megabytes. - Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    usfb_vsdbtotl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="User region largest free block both above and below 16 megabytes. - Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    usfb_vsdamin: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="User region largest free block both above and below 16 megabytes. - Minimum value for above 16 megabytes.")
    usfb_vsdantme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="User region largest free block both above and below 16 megabytes. - Time stamp for minimum. Format is high-order bytes of time-of- day (TOD) clock.")
    usfb_vsdamax: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="User region largest free block both above and below 16 megabytes. - Maximum value for above 16 megabytes.")
    usfb_vsdaxtme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="User region largest free block both above and below 16 megabytes. - Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    usfb_vsdatotl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="User region largest free block both above and below 16 megabytes. - Total for all samples above 16 megabytes (used to calculate average).")
    usal_vsdbmin: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="User region allocated area size (in bytes) above 16 megabytes. - Minimum value for below 16 megabytes.")
    usal_vsdbntme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="User region allocated area size (in bytes) above 16 megabytes. - Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    usal_vsdbmax: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="User region allocated area size (in bytes) above 16 megabytes. - Maximum value for below 16 megabytes.")
    usal_vsdbxtme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="User region allocated area size (in bytes) above 16 megabytes. - Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    usal_vsdbtotl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="User region allocated area size (in bytes) above 16 megabytes. - Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    usal_vsdamin: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="User region allocated area size (in bytes) above 16 megabytes. - Minimum value for above 16 megabytes.")
    usal_vsdantme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="User region allocated area size (in bytes) above 16 megabytes. - Time stamp for minimum. Format is high-order bytes of time-of- day (TOD) clock.")
    usal_vsdamax: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="User region allocated area size (in bytes) above 16 megabytes. - Maximum value for above 16 megabytes.")
    usal_vsdaxtme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="User region allocated area size (in bytes) above 16 megabytes. - Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    usal_vsdatotl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="User region allocated area size (in bytes) above 16 megabytes. - Total for all samples above 16 megabytes (used to calculate average).")
    uspa_vsdbmin: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="User region pages allocated both below and above 16 megabytes. - Minimum value for below 16 megabytes.")
    uspa_vsdbntme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="User region pages allocated both below and above 16 megabytes. - Time stamp for minimum. Format is high-order bytes of time-of-day (TOD) clock.")
    uspa_vsdbmax: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="User region pages allocated both below and above 16 megabytes. - Maximum value for below 16 megabytes.")
    uspa_vsdbxtme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="User region pages allocated both below and above 16 megabytes. - Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    uspa_vsdbtotl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="User region pages allocated both below and above 16 megabytes. - Total for all samples below 16 megabytes (used to calculate average). See SMF78SAM to calculate averages for Common Storage data section fields, and R782SAMP to calculate averages for private area data and Private Subpool section fields.")
    uspa_vsdamin: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="User region pages allocated both below and above 16 megabytes. - Minimum value for above 16 megabytes.")
    uspa_vsdantme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="User region pages allocated both below and above 16 megabytes. - Time stamp for minimum. Format is high-order bytes of time-of- day (TOD) clock.")
    uspa_vsdamax: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                              doc="User region pages allocated both below and above 16 megabytes. - Maximum value for above 16 megabytes.")
    uspa_vsdaxtme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="User region pages allocated both below and above 16 megabytes. - Time stamp for maximum. Format is high-order bytes of time-of- day (TOD) clock.")
    uspa_vsdatotl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="User region pages allocated both below and above 16 megabytes. - Total for all samples above 16 megabytes (used to calculate average).")
    toby_vsdgmin: so.Mapped[Optional[float]] = so.mapped_column(sa.Double,
                                                                doc="Number of bytes allocated in storage above the 2-GB-line. - Minimum number of bytes allocated above 2GB.")
    toby_vsdgntme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="Number of bytes allocated in storage above the 2-GB-line. - Time stamp for minimum value.")
    toby_vsdgmax: so.Mapped[Optional[float]] = so.mapped_column(sa.Double,
                                                                doc="Number of bytes allocated in storage above the 2-GB-line. - Maximum number of bytes allocated above 2GB.")
    toby_vsdgxtme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="Number of bytes allocated in storage above the 2-GB-line. - Time stamp for maximum value.")
    toby_vsdgtotl: so.Mapped[Optional[float]] = so.mapped_column(sa.Double,
                                                                 doc="Number of bytes allocated in storage above the 2-GB-line. - Total for all samples above 2GB (used to calculate the average).")
    toby_vsdghwm: so.Mapped[Optional[float]] = so.mapped_column(sa.Double,
                                                                doc="Number of bytes allocated in storage above the 2-GB-line. - Peak number of bytes allocated in storage above 2GB.")
    shby_vsdgmin: so.Mapped[Optional[float]] = so.mapped_column(sa.Double,
                                                                doc="Number of bytes allocated in shared memory objects. - Minimum number of bytes allocated above 2GB.")
    shby_vsdgntme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="Number of bytes allocated in shared memory objects. - Time stamp for minimum value.")
    shby_vsdgmax: so.Mapped[Optional[float]] = so.mapped_column(sa.Double,
                                                                doc="Number of bytes allocated in shared memory objects. - Maximum number of bytes allocated above 2GB.")
    shby_vsdgxtme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="Number of bytes allocated in shared memory objects. - Time stamp for maximum value.")
    shby_vsdgtotl: so.Mapped[Optional[float]] = so.mapped_column(sa.Double,
                                                                 doc="Number of bytes allocated in shared memory objects. - Total for all samples above 2GB (used to calculate the average).")
    shby_vsdghwm: so.Mapped[Optional[float]] = so.mapped_column(sa.Double,
                                                                doc="Number of bytes allocated in shared memory objects. - Peak number of bytes allocated in storage above 2GB.")
    coby_vsdgmin: so.Mapped[Optional[float]] = so.mapped_column(sa.Double,
                                                                doc="Number of high virtual common bytes allocated. - Minimum number of bytes allocated above 2GB.")
    coby_vsdgntme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="Number of high virtual common bytes allocated. - Time stamp for minimum value.")
    coby_vsdgmax: so.Mapped[Optional[float]] = so.mapped_column(sa.Double,
                                                                doc="Number of high virtual common bytes allocated. - Maximum number of bytes allocated above 2GB.")
    coby_vsdgxtme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="Number of high virtual common bytes allocated. - Time stamp for maximum value.")
    coby_vsdgtotl: so.Mapped[Optional[float]] = so.mapped_column(sa.Double,
                                                                 doc="Number of high virtual common bytes allocated. - Total for all samples above 2GB (used to calculate the average).")
    coby_vsdghwm: so.Mapped[Optional[float]] = so.mapped_column(sa.Double,
                                                                doc="Number of high virtual common bytes allocated. - Peak number of bytes allocated in storage above 2GB.")
    tomo_vsdcmin: so.Mapped[Optional[float]] = so.mapped_column(sa.Double,
                                                                doc="Total number of memory objects allocated in high virtual storage. - Minimum number high virtual memory objects / frames")
    tomo_vsdcntme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="Total number of memory objects allocated in high virtual storage. - Time stamp for minimum value.")
    tomo_vsdcmax: so.Mapped[Optional[float]] = so.mapped_column(sa.Double,
                                                                doc="Total number of memory objects allocated in high virtual storage. - Maximum number of high virtual memory objects / frames")
    tomo_vsdcxtme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="Total number of memory objects allocated in high virtual storage. - Time stamp for maximum value.")
    tomo_vsdctotl: so.Mapped[Optional[float]] = so.mapped_column(sa.Double,
                                                                 doc="Total number of memory objects allocated in high virtual storage. - Total for all samples (used to calculate the average).")
    shmo_vsdcmin: so.Mapped[Optional[float]] = so.mapped_column(sa.Double,
                                                                doc="Number of memory objects allocated in high virtual shared storage. - Minimum number high virtual memory objects / frames")
    shmo_vsdcntme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="Number of memory objects allocated in high virtual shared storage. - Time stamp for minimum value.")
    shmo_vsdcmax: so.Mapped[Optional[float]] = so.mapped_column(sa.Double,
                                                                doc="Number of memory objects allocated in high virtual shared storage. - Maximum number of high virtual memory objects / frames")
    shmo_vsdcxtme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="Number of memory objects allocated in high virtual shared storage. - Time stamp for maximum value.")
    shmo_vsdctotl: so.Mapped[Optional[float]] = so.mapped_column(sa.Double,
                                                                 doc="Number of memory objects allocated in high virtual shared storage. - Total for all samples (used to calculate the average).")
    como_vsdcmin: so.Mapped[Optional[float]] = so.mapped_column(sa.Double,
                                                                doc="Number of memory objects allocated in high virtual common storage. - Minimum number high virtual memory objects / frames")
    como_vsdcntme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="Number of memory objects allocated in high virtual common storage. - Time stamp for minimum value.")
    como_vsdcmax: so.Mapped[Optional[float]] = so.mapped_column(sa.Double,
                                                                doc="Number of memory objects allocated in high virtual common storage. - Maximum number of high virtual memory objects / frames")
    como_vsdcxtme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="Number of memory objects allocated in high virtual common storage. - Time stamp for maximum value.")
    como_vsdctotl: so.Mapped[Optional[float]] = so.mapped_column(sa.Double,
                                                                 doc="Number of memory objects allocated in high virtual common storage. - Total for all samples (used to calculate the average).")
    lgmo_vsdcmin: so.Mapped[Optional[float]] = so.mapped_column(sa.Double,
                                                                doc="Number of fixed memory objects that can be backed in 1 MB frames. - Minimum number high virtual memory objects / frames")
    lgmo_vsdcntme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="Number of fixed memory objects that can be backed in 1 MB frames. - Time stamp for minimum value.")
    lgmo_vsdcmax: so.Mapped[Optional[float]] = so.mapped_column(sa.Double,
                                                                doc="Number of fixed memory objects that can be backed in 1 MB frames. - Maximum number of high virtual memory objects / frames")
    lgmo_vsdcxtme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="Number of fixed memory objects that can be backed in 1 MB frames. - Time stamp for maximum value.")
    lgmo_vsdctotl: so.Mapped[Optional[float]] = so.mapped_column(sa.Double,
                                                                 doc="Number of fixed memory objects that can be backed in 1 MB frames. - Total for all samples (used to calculate the average).")
    tofr_vsdcmin: so.Mapped[Optional[float]] = so.mapped_column(sa.Double,
                                                                doc="Number of 1 MB frames that are fixed in central storage. - Minimum number high virtual memory objects / frames")
    tofr_vsdcntme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="Number of 1 MB frames that are fixed in central storage. - Time stamp for minimum value.")
    tofr_vsdcmax: so.Mapped[Optional[float]] = so.mapped_column(sa.Double,
                                                                doc="Number of 1 MB frames that are fixed in central storage. - Maximum number of high virtual memory objects / frames")
    tofr_vsdcxtme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="Number of 1 MB frames that are fixed in central storage. - Time stamp for maximum value.")
    tofr_vsdctotl: so.Mapped[Optional[float]] = so.mapped_column(sa.Double,
                                                                 doc="Number of 1 MB frames that are fixed in central storage. - Total for all samples (used to calculate the average).")
    r782meml: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Address space memory limit in MB.")
    fifr_vsdcmin: so.Mapped[Optional[float]] = so.mapped_column(sa.Double,
                                                                doc="Number of 1 MB frames that can be used by fixed memory objects. - Minimum number high virtual memory objects / frames")
    fifr_vsdcntme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="Number of 1 MB frames that can be used by fixed memory objects. - Time stamp for minimum value.")
    fifr_vsdcmax: so.Mapped[Optional[float]] = so.mapped_column(sa.Double,
                                                                doc="Number of 1 MB frames that can be used by fixed memory objects. - Maximum number of high virtual memory objects / frames")
    fifr_vsdcxtme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="Number of 1 MB frames that can be used by fixed memory objects. - Time stamp for maximum value.")
    fifr_vsdctotl: so.Mapped[Optional[float]] = so.mapped_column(sa.Double,
                                                                 doc="Number of 1 MB frames that can be used by fixed memory objects. - Total for all samples (used to calculate the average).")
    pafr_vsdcmin: so.Mapped[Optional[float]] = so.mapped_column(sa.Double,
                                                                doc="Number of 1 MB frames that are used by pageable/DREF memory objects. - Minimum number high virtual memory objects / frames")
    pafr_vsdcntme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="Number of 1 MB frames that are used by pageable/DREF memory objects. - Time stamp for minimum value.")
    pafr_vsdcmax: so.Mapped[Optional[float]] = so.mapped_column(sa.Double,
                                                                doc="Number of 1 MB frames that are used by pageable/DREF memory objects. - Maximum number of high virtual memory objects / frames")
    pafr_vsdcxtme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="Number of 1 MB frames that are used by pageable/DREF memory objects. - Time stamp for maximum value.")
    pafr_vsdctotl: so.Mapped[Optional[float]] = so.mapped_column(sa.Double,
                                                                 doc="Number of 1 MB frames that are used by pageable/DREF memory objects. - Total for all samples (used to calculate the average).")
    lsmo_vsdcmin: so.Mapped[Optional[float]] = so.mapped_column(sa.Double,
                                                                doc="Number of shared memory objects that can be backed in 1 MB frames. - Minimum number high virtual memory objects / frames")
    lsmo_vsdcntme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="Number of shared memory objects that can be backed in 1 MB frames. - Time stamp for minimum value.")
    lsmo_vsdcmax: so.Mapped[Optional[float]] = so.mapped_column(sa.Double,
                                                                doc="Number of shared memory objects that can be backed in 1 MB frames. - Maximum number of high virtual memory objects / frames")
    lsmo_vsdcxtme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="Number of shared memory objects that can be backed in 1 MB frames. - Time stamp for maximum value.")
    lsmo_vsdctotl: so.Mapped[Optional[float]] = so.mapped_column(sa.Double,
                                                                 doc="Number of shared memory objects that can be backed in 1 MB frames. - Total for all samples (used to calculate the average).")
    gfmo_vsdcmin: so.Mapped[Optional[float]] = so.mapped_column(sa.Double,
                                                                doc="Number of fixed memory objects that are backed in 2 GB frames. - Minimum number high virtual memory objects / frames")
    gfmo_vsdcntme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="Number of fixed memory objects that are backed in 2 GB frames. - Time stamp for minimum value.")
    gfmo_vsdcmax: so.Mapped[Optional[float]] = so.mapped_column(sa.Double,
                                                                doc="Number of fixed memory objects that are backed in 2 GB frames. - Maximum number of high virtual memory objects / frames")
    gfmo_vsdcxtme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="Number of fixed memory objects that are backed in 2 GB frames. - Time stamp for maximum value.")
    gfmo_vsdctotl: so.Mapped[Optional[float]] = so.mapped_column(sa.Double,
                                                                 doc="Number of fixed memory objects that are backed in 2 GB frames. - Total for all samples (used to calculate the average).")
    gffr_vsdcmin: so.Mapped[Optional[float]] = so.mapped_column(sa.Double,
                                                                doc="Number of 2 GB pages that are fixed in central storage. - Minimum number high virtual memory objects / frames")
    gffr_vsdcntme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="Number of 2 GB pages that are fixed in central storage. - Time stamp for minimum value.")
    gffr_vsdcmax: so.Mapped[Optional[float]] = so.mapped_column(sa.Double,
                                                                doc="Number of 2 GB pages that are fixed in central storage. - Maximum number of high virtual memory objects / frames")
    gffr_vsdcxtme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="Number of 2 GB pages that are fixed in central storage. - Time stamp for maximum value.")
    gffr_vsdctotl: so.Mapped[Optional[float]] = so.mapped_column(sa.Double,
                                                                 doc="Number of 2 GB pages that are fixed in central storage. - Total for all samples (used to calculate the average).")
    r782actv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r782flgs (Bit 0) showing job active at start of interval.")
    r782term: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r782flgs (Bit 1) showing job terminated during interval.")
    r782glch: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r782flgs (Bit 2) showing GETMAIN limit changed during interval.")
    r782invl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r782flgs (Bit 3) showing data incorrect because RMF terminated abnormally while sampling.")
    r782shra: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r782flgs (Bit 4) showing shared values above 2G available (z/OS V1R5 or later).")


class Smf78amg(AbstractConcreteBase):
    """Abstract class for structure Smf78Amg - Alias Management Group data."""

    r783amgc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                          doc="The alias management group number defined on the physical controller for this LCU. This number is valid, if the LCU is assigned to a DASD subsystem that supports alias management groups and bit 7 of R783DST is set.")
    smf78int: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Duration of the RMF Monitor I measurement interval, in the form mmsstttF where mm is the minutes, ss is the seconds, ttt is the milliseconds, and F is the sign, (The end of the measurement interval is the sum of the recorded start time and this field.)")
    ioctr: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="contention rate.")
    iodlq: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="average queue length of delayed I/O requests.")
    ioart: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="channel path taken rate.")
    iocub: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                         doc="percentage of requests caused by control unit busy.")
    iodpb: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                         doc="percentage of requests caused by director port busy.")
    iocbt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="average control unit busy delay time.")
    iocmr: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="average initial command reponse time.")
    iocss: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="average channel subsystem delay time.")
    iohwait: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="HyperPAV wait ratio.")
    iohmax: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="maximum number of in-use HyperPAV aliases.")
    iohdmax: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="maximum number of in-use HyperPAV aliaes for one device.")
    iohioqc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="the high watermark of queued I/O requests.")
    ioxsareq: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="ratio of successful alias requests.")
    ioxuahrq: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="ratio of unsuccessful alias requests in home LCU.")
    ioxabc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="rate of aliases borrowed from peer LCUs.")
    ioxhcba: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                         doc="high watermark of concurrently borrowed aliases.")
    ioxalc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="rate of aliass laned to a peer LCU.")
    ioxhcla: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                         doc="high watermark of concurrently loaned aliases to a peer LCU.")
    ioxcqd: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                          doc="average queue length when an alias was needed.")
    ioxiuac: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="average number of in-use aliases when an alias was needed.")
