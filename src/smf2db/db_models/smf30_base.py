from typing import Optional

import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.ext.declarative import AbstractConcreteBase
import datetime as dt


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


class Base30(Base):
    __abstract__ = True
    metadata = sa.MetaData(schema='smf30', naming_convention=convention)


class Base30Hr(Base):
    __abstract__ = True
    metadata = sa.MetaData(schema='smf30', naming_convention=convention)


class Base30Da(Base):
    __abstract__ = True
    metadata = sa.MetaData(schema='smf30', naming_convention=convention)


class Smf30pss(AbstractConcreteBase):
    """Abstract class for structure Smf30pss - Subsystem section."""

    smf30rs1: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Reserved.")
    smf30pflags: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                             doc="Product flags. Bit Meaning when set 0 Reserved. 1 (SMF30_CrypCtrs_Active) Indicates that crypto counter processing is active. 2 (SMF30_NNPICtrs_Active) Indicates that NNPI counter processing is active 3 - 7 Reserved.")
    smf30rvn: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                          doc="Record version number Value Meaning '05' MVS/SP Version 5 '04' MVS/SP Version 4 '03' MVS/SP Version 3 '02' MVS/SP Version 2 '01' VS2")
    smf30pnm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="Subsystem or product name, for example SMF.")
    smf30osl: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="Code string for the operating system level to represent the version, release, and modification level, as described for CVTPRODN. Guaranteed to be larger in each release.")


class Smf30cmp(AbstractConcreteBase):
    """Abstract class for structure Smf30cmp - Completion section."""

    smf30scc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4),
                                                          doc="Step completion code X'0 ccc ' Indicates system abnormal end (abend) of task in the job step, where ccc is the system abend code. (See z/OS MVS System Codes")
    smf30sti: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4),
                                                          doc="Step/Job termination indicator Bit Meaning when set 0 Reserved 1 Canceled by exit IEFUJV. 2 Canceled by exit IEFUJI. 3 Canceled by exit IEFUSI. 4 Canceled by exit IEFACTRT. 5 Step is to be restarted. 6 If zero, then normal completion. If 1, then abnormal end of task (abend). If step completion code equals 0322 or 0522, then IEFUTL caused the abend. If step completion code equals 0722, then IEFUSO caused the abend. 7 If zero, then normal completion. If 1, then step was flushed. 8 EXCP counts might be incorrect because the record did not include all the DD statements. 9 Previous interval record was not written because an error occurred. The cumulative count might be incorrect because the counters were cleared. 10 EXCP sections were not merged from the interval to the step record or from the step to the job record. 11 Step completed with a 'post execution' error. Post-execution errors include a failure that occurred because the ALLOCxx parmlib member specified CATLG_ERR FAILJOB(YES). 12 Step completed due to z/OS UNIX exec function request. 13 JOB abnormally ended because of COND= condition on the JOB card. This flag will be set on in the subtype 5 job termination record only. 14 Job was evicted via the $EJ nn ,STEP,HOLD or equivalent command. This bit is set for subtype 4 (step end) records only. 15")
    smf30arc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Abend reason code.")


class Smf30id(AbstractConcreteBase):
    """Abstract class for structure Smf30Id - identification section."""

    smf30pgm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="Program name (taken from PGM= parameter on EXEC card). If a backward reference was used, this field contains PGM=*.DD.")
    smf30stm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Step name (taken from name on EXEC card).")
    smf30uif: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="User-defined identification field (taken from common exit parameter area, not from USER=parameter on job statement).")
    smf30cls: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                          doc="Job class (blank for TSO/E session or started tasks).")
    smf30jf1: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Flag word Bit Meaning when set 0 Job/Session ID section flag. 1-7")
    smf30pgn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Beginning with z/OS V1R3, this field is always zero.")
    smf30jpt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="JES input priority. If no value is specified for the PRTY parameter (on the JOB card), this field contains: • For JES3, the default priority specified on the JES3 STANDARDS initialization card • For JES2, a zero. Note that JES2 does not use the priority value reported in the field. (The JES2 job selection priority is requested using the JES2")
    smf30ast: so.Mapped[Optional[str]] = so.mapped_column(sa.String(11),
                                                          doc="Device allocation start time, in hundredths of a second.")
    smf30pps: so.Mapped[Optional[str]] = so.mapped_column(sa.String(11),
                                                          doc="Problem program start time, in hundredths of a second.")
    smf30sit: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                  doc="Time since midnight, in hundredths of a second, that the initiator selected this step or job.")
    smf30rst: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                  doc="Time since midnight, in hundredths of a second, that the reader recognized the JOB card (for this job).")
    smf30ret: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                  doc="Time since midnight, in hundredths of a second, that the reader recognized the end of the JCL being read for the job or started task (reader stop time). For TSO/E this is the logon enqueue time.")
    smf30usr: so.Mapped[Optional[str]] = so.mapped_column(sa.String(20), doc="Programmer's name.")
    smf30grp: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="RACF group ID. 0 = RACF is not active.")
    smf30rud: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="RACF user ID. 0 = RACF is not active.")
    smf30tid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="RACF terminal ID. This field is zero if RACF is not active (or the user is not a terminal user).")
    smf30tsn: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Terminal symbolic name.")
    smf30psn: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="The name of the step that invoked the procedure. This field contains blanks if not part of a procedure.")
    smf30cl8: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="8-character job class (left justified, padded with blanks). For JES2, taken from the SMF30CLS field (if not specified), 'TSU' for TSO sessions, or 'STC' for started tasks. For JES3, taken from the CLASS parameter on the //* MAIN card (if valid), or the default (JS3BATCH).")
    smf30iss: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                  doc="Time and date that the interval started for subtype 2 and 3 records, in time-of-day (TOD) format, an unsigned 64-bit fixed-point number where bit 51 is equivalent to 1 microsecond. The representation of this value in local time is stored in SMF30IST and SMF30IDT. Variations in setting the local time can make the times appear to be out of synchronization.")
    smf30iet: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                  doc="Time and date that the interval ended for subtype 2 and 3 records, in time-of-day (TOD) format, an unsigned 64-bit fixed-point number where bit 51 is equivalent to 1 microsecond. If you requested synchronized interval recording, you can use this field to compare this record with other records generated at the end of the same interval. If the address space being reported was not swapped in when the interval ended, then the time contained in this field might be earlier than the time that the record was generated.")
    smf30ssn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Substep number. This field is set to zero for non-z/OS UNIX steps. When the z/OS UNIX exec function is requested, a new substep is begun and this value is incremented.")
    smf30exn: so.Mapped[Optional[str]] = so.mapped_column(sa.String(16),
                                                          doc="Program name. For a z/OS UNIX program, this contains the name, for up to 16 bytes, starting after the last slash in the file name, of the program that was run. The z/OS UNIX name ends with the null character X'00'. For an MVS program, it is an unqualified name of up to 8 characters of the program that was executed. The MVS program name is padded with blanks to a length of 16 characters. For example, for a z/OS UNIX name of /usr/joe/somepgm , the field in SMF record type 30 is somepgm ended by X'00' . For a z/OS UNIX name of /usr/joe/someverylongprogramname , the field is truncated to someverylongprog .")
    smf30cor: so.Mapped[Optional[str]] = so.mapped_column(sa.String(130), doc="JES job correlator.")
    smf30jclid1: so.Mapped[Optional[str]] = so.mapped_column(sa.String(10),
                                                             doc="JES-computed binary identifier for the job that was submitted (using method 1), if provided by the primary subsystem.")
    smf30jclid2: so.Mapped[Optional[str]] = so.mapped_column(sa.String(10),
                                                             doc="JES-computed binary identifier for the job that was submitted (using method 2) , if provided by the primary subsystem.")
    smf30jcltoken: so.Mapped[Optional[str]] = so.mapped_column(sa.String(18),
                                                               doc="Identifier for the job, if provided by the primary subsystem.")
    smf30holduntil: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                        doc="A UTC timestamp represented by the first 6 bytes (bits 0-47) of an ETOD value. This is the resolved HOLDUNTL value for the job (from JCL or JES2 symbol on the internal reader interface) , if provided by the primary subsystem.")
    smf30deadline: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                       doc="A UTC timestamp represented by the first 6 bytes (bits 0-47) of an ETOD value. This is the resolved DEADLINE value for the job (from JES2 symbol on the internal reader interface) , if provided by the")
    smf30_rctpcpua_actual: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                       doc="Physical CPU adjustment factor (this is the adjustment factor for converting CPU time to equivalent service, in basic-mode with all processors online). Based on model capacity rating.")
    smf30_rctpcpua_nominal: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                        doc="Physical CPU adjustment factor (this is the adjustment factor for converting CPU time to equivalent service in basic-mode with all processors online). Based on nominal model capacity rating.")
    smf30_rctpcpua_scaling_factor: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                               doc="Scaling factor for SMF30_RCTPCPUA_actual and SMF30_RCTPCPUA_nominal.")
    smf30_capacity_adjustment_ind: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                               doc="Field values and meanings are: Value Meaning 0 The indication is not reported. 1-99 Some amount of reduction is indicated. 100 The machine is operating in normal capacity. Primary CPUs and all secondary-type CPUs are similarly affected.")
    smf30_rmctadjn_nominal: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Nominal CPU rate adjustment.")
    smf30_time_on_ziip: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                      doc="(SMF30_TIME_ON_SUP) Accumulation of time spent on zIIP. Time is in hundredths of a second (includes enclave time).")
    smf30tex: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Total blocks transferred - accumulated EXCP counts. This field is the 8-byte equivalent of SMF30TEP, but this field remains valid after SMF30TEP is invalid.")
    smf30pgi: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="(SMF30PIA) Number of page-ins from auxiliary storage, regardless of the page size (4K or 1M).")
    smf30pgo: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="(SMF30POA) Number of page-outs to auxiliary storage, regardless of the page size (4K or 1M).")
    smf30nsw: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="As of z/OS 1.8, this field is no longer valid; the value is always zero. Prior to z/OS 1.8, this field contained: Number of address space swap sequences. (A swap sequence consists of an address space swap-out and swap-in. Logical swap-out and swap-in are not included.)")
    duration: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="the duration of the job.")
    tcb_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="the calculated TCB time based on the service units.")
    srb_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="the calculated SRB time base on the service units.")
    cpu_total: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="the total CPU time.")
    consumed_msu: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="the total MSU consumed.")
    smf30pgn_inv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="smf30jf1 (Bit 0) showing job/session ID section flag that smf30pgn is invalid.")
    excp_num: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="the number of Execute CHannel Program (EXCP) sections related to this record.")
    unix_process_num: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                  doc="number of z/OS UNIX PRocess sections related to this record.")
    usage_data_num: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                doc="number of Usage Data sections related to this record.")
    restart_mgmt_num: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                  doc="number of AUtomatic Restart Management section related to this record.")
    msys_encl_rem_system_data_num: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                               doc="number of Multisystem Enclave Remote System Data section related to this record.")


class Smf30ura(AbstractConcreteBase):
    """Abstract class for structure Smf30Ura - I/O activity section."""

    smf30inp: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Number of card-image records in DD DATA and DD* data sets read by the reader for the map. This field is not set for subtypes 2 or 3.")
    smf30tep: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Total blocks transferred (accumulated execute channel program (EXCP) counts - valid up to X'FFFFFFFE', zero and invalid when SMF30TEF is set)")
    smf30tpt: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Number of TPUTS (terminal writes) for a TSO/E session. If a batch job or a started task successfully processes TPUTs, this field might be non-zero for batch jobs or started tasks.")
    smf30tgt: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Number of TGETS (terminal reads) for a TSO/E session.")
    smf30tcn: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total device connect time (in 128 micro-second units) for this address space. For a DIV object, this field contains total device connect time for reads, writes, and re-reads.")
    smf30trr: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Total address space REREAD count.")
    smf30aic: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="DASD I/O connect time, in 128-microsecond units, for address space plus dependent enclaves. Note that the value of RqsvAIC for FICON ® channel utilization cannot be calculated. For more information, see the footnote.")
    smf30aid: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="DASD I/O disconnect time, in 128-microsecond units, for address space plus dependent enclaves.")
    smf30aiw: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="DASD I/O pending plus control unit queue time, in 128-microsecond units, for address space plus dependent enclaves.")
    smf30ais: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="DASD I/O start subchannel count for address space plus dependent enclaves.")
    smf30eic: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="DASD I/O connect time, in 128-microsecond units, for independent enclaves owned by the address space. Note that the value of RqsvEIC for FICON channel utilization cannot be calculated. For more information, see the footnote.")
    smf30eid: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="DASD I/O disconnect time, in 128-microsecond units, for independent enclaves owned by the address space.")
    smf30eiw: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="DASD I/O pending plus control unit queue time, in 128-microsecond units, for independent enclaves owned by the address space.")
    smf30eis: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="DASD I/O start subchannel count for independent enclaves.")
    smf30tex: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Total blocks transferred - accumulated EXCP counts. This field is the 8-byte equivalent of SMF30TEP, but this field remains valid after SMF30TEP is invalid.")
    smf30das: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of DDs that had their DD accounting information suppressed.")


class Smf30prf(AbstractConcreteBase):
    """Abstract class for structure Smf30Prf - Performance section."""

    smf30srv: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Total service units. This field grows to X'FFFFFFFF' and then wraps back to zero and continues growing. When wrapping occurs, SMF30SRV_INV is set to on. SMF30SRV_L is the 8-byte equivalent of this field.")
    smf30csu: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="CPU service units. This field grows to X'FFFFFFFF' and then wraps back to zero and continues growing. When wrapping occurs, SMF30CSU_INV is set to on. SMF30CSU_L is the 8-byte equivalent of this field.")
    smf30srb: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Service request block (SRB) service units. This field grows to X'FFFFFFFF' and then wraps back to zero and continues growing. When wrapping occurs, SMF30SRB_INV is set to on. SMF30SRB_L is the 8-byte equivalent of this field.")
    smf30io: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                         doc="I/O service units. This field grows to X'FFFFFFFF' and then wraps back to zero and continues growing. When wrapping occurs, SMF30IO_INV is set to on. SMF30IO_L is the 8-byte equivalent of this field.")
    smf30mso: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Main storage occupancy (MSO) service units. This field grows to X'FFFFFFFF' and then wraps back to zero and continues growing. When wrapping occurs, SMF30MSO_INV is set to on. SMF30MSO_L is the 8-byte equivalent of this field.")
    smf30tat: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="System resources manager (SRM) transaction active time, in 1024- microsecond units.")
    smf30sus: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Copy of RmctAdjC when this SMF record was produced, number of sixteenths of one CPU microsecond per CPU service unit.")
    smf30res: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="System resources manager (SRM) transaction residency time, in 1024-microsecond units. That is the amount of time the SRM transaction was in real storage.")
    smf30trs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of system resources manager (SRM) transactions.")
    smf30eta: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Independent enclave transaction active time in 1024-microsecond units.")
    smf30esu: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Independent enclave CPU service units. This field grows to X'FFFFFFFF' and then wraps back to zero and continues growing. When wrapping occurs, SMF30ESU_INV is set to on. SMF30ESU_L is the 8-byte equivalent of this field.")
    smf30etc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Independent enclave transaction count.")
    smf30jqt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Job preparation time. This is the elapsed time before the job was first queued for execution. It excludes time to read the job into the system. It includes delays incurred waiting for and during conversion, such as when eligible systems are not active to convert the job. If the JOB statement specified TYPRUN=JCLHOLD, this time is 0. The time is in 1024-microsecond units.")
    smf30rqt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Time following job preparation when the job was ineligible for execution due to either the job's eligible systems being inactive or the job's scheduling environment not being available. The time is in 1024-microsecond units.")
    smf30hqt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Time following job preparation when the job was ineligible for execution for reasons not included in SMF30RQT. This includes job hold, job class hold, job queue hold, duplicate job name serialization, and job class execution limits. If the JOB statement specified TYPRUN=HOLD, the time that the job is held for this reason is not included. The time is in 1024-microsecond units.")
    smf30sqt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Time the job was eligible for execution. This is the amount of time between the end of job conversion and Problem Program Start time (SMF30PPS). The time is in 1024-microsecond units. For JES3, this field includes time the job was ineligible for execution.")
    smf30msc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="MSO Service Definition Coefficient (SDC). Always zero.")
    smf30cpc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="CPU Service Definition Coefficient (SDC) scaled by 10.")
    smf30loc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="IOC Service Definition Coefficient (SDC). Always zero.")
    smf30src: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="SRB Service Definition Coefficient (SDC) scaled by 10.")
    smf30znf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Normalization factor for zAAP service time. Used to convert between real zAAP times and 'normalized' zAAP times, that is, the equivalent time on a standard CP. Multiply SMF30_TIME_ON_zAAP by this value and divide by 256 to calculate the normalized zAAP time.")
    smf30snf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Normalization factor for zIIP service time. Used to convert between real zIIP times and normalized zIIP times, that is, the equivalent time on a standard CP. Multiply SMF30_TIME_ON_zIIP by this value")
    smf30srv_l: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                            doc="Total service units. This is the 8-byte equivalent of SMF30SRV. The value of this field continues to grow after SMF30SRV_INV is set.")
    smf30csu_l: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                            doc="CPU service units. This is the 8-byte equivalent of SMF30CSU. The value of this field continues to grow after SMF30CSU_INV is set.")
    smf30srb_l: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                            doc="SRB service units. This is the 8-byte equivalent of SMF30SRB. The value of this field continues to grow after SMF30SRB_INV is set.")
    smf30io_l: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                           doc="I/O service units. This is the 8-byte equivalent of SMF30IO. The value of this field continues to grow after SMF30IO_INV is set.")
    smf30mso_l: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                            doc="MSO service units. This is the 8-byte equivalent of SMF30MSO. The value of this field continues to grow after SMF30MSO_INV is set.")
    smf30esu_l: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                            doc="ESU service units. This is the 8-byte equivalent of SMF30ESU. The value of this field continues to grow after SMF30ESU_INV is set.")
    smf30_capacity_change_cnt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                           doc="The number of processor capacity changes that occurred since the previous interval or event interval. This number will be greater than 1 when the number of processor capacity changes exceeded the number specified in the MAXEVENTINTRECS parmlib option.")
    smf30_rctpcpua_actual: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                       doc="Physical CPU adjustment factor (this is the adjustment factor for converting CPU time to equivalent service, in basic-mode with all processors online). Based on model capacity rating.")
    smf30_rctpcpua_nominal: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                        doc="Physical CPU adjustment factor (this is the adjustment factor for converting CPU time to equivalent service in basic-mode with all processors online). Based on nominal model capacity rating.")
    smf30_rctpcpua_scaling_factor: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                               doc="Scaling factor for SMF30_RCTPCPUA_actual and SMF30_RCTPCPUA_nominal.")
    smf30_capacity_adjustment_ind: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                               doc="Field values and meanings are: Value Meaning 0 The indication is not reported. 1-99 Some amount of reduction is indicated. 100 The machine is operating in normal capacity. Primary CPUs and all secondary-type CPUs are similarly affected.")
    smf30_rmctadjn_nominal: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Nominal CPU rate adjustment.")


class Smf30cas(AbstractConcreteBase):
    """Abstract class for structure Smf30Cas - Processor accounting section."""

    smf30cpt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="All standard CPU step time in hundredths of a second. Includes enclave time, preemptable class SRB time, client SRB time. Also includes time consumed by zAAP or zIIP eligible work running on a standard processor. This value includes the value in field SMF30OST.")
    smf30cps: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Step CPU time under the service request block (SRB), in hundredths of a second. You can calculate the SRB time in microseconds (1/100 of a second using the following formula: (SMF30SRB*10)/SMF30SRC * SMF30SUS/16 = SRB time in microseconds This value includes the value in field SMF30OST.")
    smf30icu: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Initiator CPU time under the task control block (TCB), in hundredths of a second. This field is set at step termination. SMF30ICU = SMF30ICU_STEP_INIT (for this step) + SMF30ICU_STEP_TERM (from the previous step)")
    smf30isb: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Initiator CPU time under the service request block (SRB), in hundredths of a second. This field is set at step termination. SMF30ISB = SMF30ISB_STEP_INIT (for this step) + SMF30ISB_STEP_TERM (from the previous step)")
    smf30jvu: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Step vector CPU time, in hundredths of a second.")
    smf30ivu: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Initiator vector CPU time, in hundredths of a second. This field is set at step termination. As of z/OS 1.11, this field is no longer valid; the value will always be zero.")
    smf30jva: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Step vector affinity time, in hundredths of a second. As of z/OS 1.11, this field is no longer valid; the value will always be zero.")
    smf30iva: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Initiator vector affinity time, in hundredths of a second. This field is set at step termination. As of z/OS 1.11, this field is no longer valid; the value will always be zero.")
    smf30iip: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Amount of CPU time used to process I/O interrupts, in hundredths of a second.")
    smf30rct: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Amount of CPU time used by the region control task (RCT), in hundredths of a second.")
    smf30hpt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="CPU time consumed for the step, in hundredths of a second, to support requests for data to be transferred between a hiperspace and an address space, when the hiperspace is backed by expanded storage. The CPU time may vary depending on the availability of expanded storage.")
    smf30csc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Integrated Cryptographic Service Facility/MVS (ICSF/MVS) service count. This is the number of cryptographic instructions executed on behalf of caller (within caller's address space).")
    smf30dmi: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="ADMF-Number of pages moved with ADMF WRITE operation.")
    smf30dmo: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="ADMF-Number of pages moved with ADMF READ operation.")
    smf30asr: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Additional CPU time accumulated by the preemptible SRBs and client SRBs for this job, in hundredths of a second. This value is also included in the value in SMF30CPT.")
    smf30enc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="CPU time, in hundredths of seconds, used by the independent enclave, but only when in the WLM enclave. Note that independent enclave time on an IFA is not included; see field SMF30_ENCLAVE_TIME_ON_IFA for that value. SMF30ENC is also part of the value in SMF30CPT.")
    smf30det: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="CPU time, in hundredths of seconds, used by the dependent enclave, but only when in the WLM enclave. Note that dependent enclave time on an IFA is not included; see field SMF30_DEP_ENCLAVE_TIME_ON_IFA for that value. SMF30DET is also part of the value in SMF30CPT.")
    smf30cep: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Cumulative CPU time consumed for an address space or job while enqueue promoted (in 1.024 millisecond units).")
    smf30_boostinfo: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                 doc="Boost Information Bit Meaning when set 0 zIIP boost was active at some point within the interval. An SMF30 step-end record will have the 'active' bit on if the bit was on in any interval record created for the step. An SMF30 job record will have the 'active' bit on if the bit was on in any interval record created for the job. 1 Speed boost was active at some point within the interval. An SMF30 step-end record will have the 'active' bit on if the bit was on in any interval record created for the step. An SMF30 job record will have the 'active' bit on if the bit was on in any interval record created for the job. 5 - 7 Boost class: 001 : IPL 010 : Shutdown 011 : Recovery process Note: The boost class value is valid only when one or more boosts is active; that is, a boost active bit is also")
    smf30_time_on_ifa: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                     doc="Accumulation of CPU time spent on zAAP. Time is in hundredths of a second (includes enclave time).")
    smf30_enclave_time_on_ifa: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                             doc="Accumulation of enclave time spent on zAAP. Time is in hundredths of a second.")
    smf30_dep_enclave_time_on_ifa: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                 doc="Accumulation of dependent enclave time spent on zAAP. Time is in hundredths of a second.")
    smf30_time_ifa_on_cp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                        doc="Accumulation of CPU time spent running zAAP eligible work on a standard CP. Time is in hundredths of a second (includes enclave time).")
    smf30_enclave_time_ifa_on_cp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                doc="Accumulation of zAAP enclave time spent on a standard CP. Time is in hundredths of a second.")
    smf30_dep_enclave_time_ifa_on_cp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                    doc="Accumulation of zAAP dependent enclave time spent on a standard CP. Time is in hundredths of a second.")
    smf30cepi: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                             doc="CPU time consumed for an address space or job while enqueue promoted (in 1.024 millisecond units). Contains only the time consumed during the interval (not cumulative).")
    smf30_time_on_ziip: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                      doc="(SMF30_TIME_ON_SUP) Accumulation of time spent on zIIP. Time is in hundredths of a second (includes enclave time).")
    smf30_enclave_time_on_ziip: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                              doc="(SMF30_ENCLAVE_TIME_ON_SUP) Accumulation of enclave time spent on zIIP. Time is in hundredths of a second.")
    smf30_depenc_time_on_ziip: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                             doc="(SMF30_DEPENC_TIME_ON_SUP) Accumulation of dependent enclave time spent on zIIP. Time is in hundredths of a second.")
    smf30_time_ziip_on_cp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                         doc="(SMF30_TIME_SUP_ON_CP) Accumulation of CPU time spent running zIIP eligible work on a standard CP. Time is in hundredths of a second (includes enclave time).")
    smf30_enclave_time_ziip_on_cp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                 doc="(SMF30_ENCLAVE_TIME_SUP_ON_CP) Accumulation of zIIP enclave time spent on a standard CP. Time is in hundredths of a second.")
    smf30_depenc_time_ziip_on_cp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                doc="(SMF30_DEPENC_TIME_SUP_ON_CP) Accumulation of zIIP dependent enclave time spent on a standard CP. Time is in hundredths of a second.")
    smf30_enclave_time_ziip_qual: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                doc="(SMF30_ENCLAVE_TIME_SUP_QUAL) Normalized enclave time qualified to be on zIIP in hundredths of a second. Note that qualified time is the SRB time for an enclave that a program (Db2, for example) has identified to Workload Management for zIIP eligibility. The program also indicates the portion of the SRB time intended for eligibility to the zIIP(s). The eligible time achieved is reported in xxx_TIME_ON_ZIIP and xxx_TIME_ZIIP_ON_CP fields.")
    smf30_depenc_time_ziip_qual: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                               doc="(SMF30_DEPENC_TIME_SUP_QUAL) Normalized dependent enclave time qualified to be on zIIP in hundredths of a second. Note that qualified time is the SRB time for an enclave that a program (Db2, for example) has identified to Workload Management for zIIP eligibility. The program also indicates the portion of the SRB time intended for eligibility to the zIIP(s). The eligible time achieved is reported in")
    smf30crp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="CPU time consumed for an address space or job while promoted because of chronic resource contention (in 1.024 millisecond units). For interval records, this field contains only the time consumed during the interval itself.")
    smf30icu_step_term: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                      doc="CPU TCB time, in hundredths of seconds, spent by the initiator during job step termination processing. This field is the step termination portion of SMF30ICU that is reported in the next step end record.")
    smf30icu_step_init: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                      doc="CPU TCB time, in hundredths of seconds, spent by the initiator during job step initialization processing. This field is the step initialization portion of SMF30ICU for this step end record.")
    smf30isb_step_term: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                      doc="CPU SRB time, in hundredths of seconds, spent by the initiator during job step termination processing. This field is the step termination portion of SMF30ISB that is reported in the next step end record.")
    smf30isb_step_init: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                      doc="CPU SRB time, in hundredths of seconds, spent by the initiator during job step initialization processing. This field is the step initialization portion of SMF30ISB for this step end record.")
    smf30_missed_smf30blk: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                       doc="Accumulated value of I/O block counts when serialization could not be obtained for accumulating the value to SMF30BLK. This value is maintained at the job step level as opposed to the DD level of its SMF30BLK counterpart.")
    smf30_missed_smf30dct: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                         doc="Accumulated value of device connect time, in 128- microsecond units, when serialization could not be obtained for accumulating the value to SMF30DCT. This value is maintained at the job step level as opposed to the DD level of its SMF30DCT counterpart. This field contains zero for started tasks.")
    smf30_highest_task_cpu_percent: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                                doc="For interval records, the largest percentage of CPU time used by any task in the address space, rounded to the nearest integer. The percentage value is calculated as: TCB time * 100 / interval time. For step-end and job-end records, the value is the largest reported interval value.")
    smf30_highest_task_cpu_program: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                                                doc="Name of the program loaded by the task that used the largest percentage of CPU time in this address space. This field corresponds to SMF30_Highest_Task_CPU_Percent. A value of blanks indicates that no task reported any CPU time in the address space, or that the CPU time could not be obtained. A value of ???????? indicates that the program name could not be obtained for the task that reported the highest percentage of CPU time.")
    smf30cas_flag: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="CPU accounting segment flags. Bit Meaning when set 0 SMF30CAS_InEligHonorPriority indicates eligible work in this address space is not offloaded to CPs for help processing. Once this bit is set on for a job interval or step-end record, this bit will also be set on for step-total and job-end records.")
    smf30_time_java_on_ziip: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                           doc="Time spent in Java work on zIIP in hundredths of a second including enclave time. Valid when SMF30_Time_Java_On_zIIP_F is 0 and SMF30CLN ≥ SMF30CAS_Len_V2.")
    smf30_enclave_time_java_on_ziip: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                   doc="Enclave time spent in Java work on zIIP in hundredths of a second. Valid when SMF30_ENCLAVE_Time_Java_On_zIIP_F is 0 and SMF30CLN ≥ SMF30CAS_Len_V2.")
    smf30_depenc_time_java_on_ziip: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                  doc="Dependent enclave time spent in Java work on zIIP in hundredths of a second. Valid when SMF30_DEPENC_Time_Java_On_zIIP_F is 0 and SMF30CLN ≥ SMF30CAS_Len_V2.")
    smf30_time_java_on_cp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                       doc="zIIP eligible time spent in Java work on CP in hundredths of a second including enclave time. Valid when SMF30_Time_Java_On_CP_F is 0 and SMF30CLN ≥ SMF30CAS_Len_V2.")
    smf30_enclave_time_java_on_cp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                 doc="zIIP eligible enclave time spent in Java work on CP in hundredths of a second. Valid when SMF30_ENCLAVE_Time_Java_On_CP_F is 0 and SMF30CLN ≥ SMF30CAS_Len_V2.")
    smf30_depenc_time_java_on_cp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                              doc="zIIP eligible dependent enclave time spent in Java work on CP in hundredths of a second. Valid when SMF30_DEPENC_Time_Java_On_CP_F is 0 and SMF30CLN ≥ SMF30CAS_Len_V2.")
    ziipboost_active: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                  doc="smf30_boostinfo (Bit 0) showing zIIP boost was active at some point within the interval. A smf30 step-end record will have the 'active' bit on if the bit was on in any interval record created for the step. A smf30 job record will have the 'active' bit on if the bit was on in any interval record created for the job.")
    speedboost_active: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                   doc="smf30_boostinfo (Bit 1) showing speed boost was active at some point witinin the interval. A smf30 step-end record will have the 'active' bit on if the bit was on in any interval record created for the step. A smf30 job record will have the 'active' bit on if the bit was on in any interval record created for the job.")
    boostclass: so.Mapped[Optional[str]] = so.mapped_column(sa.String(3),
                                                            doc="smf30_boostinfo (Bit 5-7) showing boost class (001: IPL; 010: Shutdown; 011: Recovery process).")


class Smf30exp(AbstractConcreteBase):
    """Abstract class for structure Smf30Exp - Data set access information of Execute Channel Program (EXCP) section."""

    smf30dev: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2), doc="Device class.")
    smf30utp: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="Unit type.")
    smf30blk: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of blocks issued for the device against the data set. This field has a maximum value of X'FFFFFFFF' = 4,294,967,295. If it exceeds that value it will wrap to zero and then continue to increase again for additional blocks transferred.")
    smf30bsz: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Largest blocksize of the data set Bit Meaning when set 0 Indicated changed blocksize for the data set. Post processors should use this field to avoid the possibility of negative numbers. 1-15 Largest blocksize of the data set.")
    smf30xbs: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Block size value.")
    cbs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                     doc="smf30bsz (Bit 0) indicated changed blocksize for the data set. Post processors should use this field to avoid the possiblity of negative number.")


class Smf30op(AbstractConcreteBase):
    """Abstract class for structure Smf30Op - z/OS Unix process section."""

    smf30osc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of z/OS UNIX services requested by the process. When the z/OS UNIX parmlib option SYSCALL_COUNTS is set to NO, there is no collection of data for the count of syscalls. When gathering syscall counts for a job, do not switch between SYSCALL_COUNTS=YES and SYSCALL_COUNTS=NO because doing so can lead to inaccurate values in the SMF30OSC field.")
    smf30ost: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total CPU time (in hundredths of a second) accumulated by z/OS UNIX services requested by the process. Note that the value in SMF30OST is already included in fields SMF30CPT or SMF30CPS. When the z/OS UNIX parmlib option SYSCALL_COUNTS is set to NO, there is no collection of data for CPU usage. When gathering CPU usage for a job, do not switch between SYSCALL_COUNTS=YES and SYSCALL_COUNTS=NO because doing so can lead to inaccurate values in the SMF30OST field.")
    smf30odr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of z/OS UNIX directory reads for the process.")
    smf30ofr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Read I/O block count for z/OS UNIX regular files.")
    smf30ofw: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Write I/O block count for z/OS UNIX regular files.")
    smf30opr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Read I/O block count for z/OS UNIX pipes and AF_UNIX sockets.")
    smf30opw: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Write I/O block count for z/OS UNIX pipes and AF_UNIX sockets.")
    smf30oll: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of pathname lookup calls to the logical file system.")
    smf30olp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of pathname lookup calls to the physical file system.")
    smf30ogl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of pathname generation calls to the logical file system.")
    smf30ogp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of pathname generation calls to the physical file system to determine a pathname.")
    smf30osy: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of times the sync() function was called.")


class Smf30ops(AbstractConcreteBase):
    """Abstract class for structure Smf30Ops - Operator section."""

    smf30pdm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of non-specific DASD mounts.")
    smf30prd: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of specific DASD mounts.")
    smf30ptm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of non-specific tape mounts.")
    smf30tpr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of specific tape mounts.")
    smf30mtm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of non-specific MSS mounts. As of MVS/SP4.1, this field is no longer valid, and contains zeroes.")
    smf30msr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of specific MSS mounts. As of MVS/SP4.1, this field is no longer valid, and contains zeroes.")


class Smf30ud(AbstractConcreteBase):
    """Abstract class for structure Smf30Ud - Usage data section."""

    smf30uct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Product TCB Time (in hundredths of a second).")
    smf30ucs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Product SRB Time (in hundredths of a second).")


class Smf30uss(AbstractConcreteBase):
    """Abstract class for structure Smf30Uss - Usage statistics section."""

    smf30_us_comprreq: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                   doc="Total number of compression and decompression requests (both supervisor-state and problem-state requests) 1")
    smf30_us_comprreq_prob: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                        doc="Total number of problem-state compression and decompression requests. 2")
    smf30_us_queuetime: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                      doc="Total queue time. The amount of time, in microseconds, from when the request was submitted until the adapter started executing the request. 2")
    smf30_us_exectime: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                     doc="Total execution time, in microseconds. 2")
    smf30_us_def_uncomprin: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                        doc="Total number, in bytes, of uncompressed data input. 1")
    smf30_us_def_comprout: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                       doc="Total number, in bytes, of compressed data output. 1")
    smf30_us_inf_comprin: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                      doc="Total number, in bytes, of compressed data input. 1")
    smf30_us_inf_decomprout: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                         doc="Total number, in bytes, of decompressed data output. 1")


class Smf30sap(AbstractConcreteBase):
    """Abstract class for structure Smf30Sap - Storage and paging section."""

    smf30pgi: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="(SMF30PIA) Number of page-ins from auxiliary storage, regardless of the page size (4K or 1M).")
    smf30pgo: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="(SMF30POA) Number of page-outs to auxiliary storage, regardless of the page size (4K or 1M).")
    smf30cpm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of attempts to read data from an ESO hiperspace that were not satisfied because the data has been deleted.")
    smf30nsw: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="As of z/OS 1.8, this field is no longer valid; the value is always zero. Prior to z/OS 1.8, this field contained: Number of address space swap sequences. (A swap sequence consists of an address space swap-out and swap-in. Logical swap-out and swap-in are not included.)")
    smf30psi: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="As of z/OS 1.8, this field is no longer valid; the value is always zero. Prior to z/OS 1.8, this field contained: Number of pages swapped in from auxiliary storage to central storage. This field includes: (local system queue area (LSQA), fixed pages, and pages that the real storage manager determined to be active when the address space was swapping in. It does not include page reclaims or pages found in storage during the swap-in process (such as pages brought in by the service request blocks (SRB), started after completion of swap-in Stage 1 processing).")
    smf30pso: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="As of z/OS 1.8, this field is no longer valid; the value is always zero. Prior to z/OS 1.8, this field contained: Number of pages swapped out from central storage to auxiliary storage. This field includes: local system queue area (LSQA), private area fixed pages, and private area non-fixed changed pages.")
    smf30vpi: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Number of VIO page-ins from auxiliary storage to central storage for this step. This field includes page-ins resulting from page faults or specific page requests on a VIO window. It does not include VIO swap-ins or page-ins for the common area.")
    smf30vpo: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Number of VIO page-outs from central storage to auxiliary storage for this step. This field includes page-outs resulting from specific page requests on a VIO window as well as those pages stolen by the paging supervisor through infrequent use. It does not include VIO swap-outs or page-outs for the common area.")
    smf30vpr: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Number of VIO reclaims.")
    smf30cpi: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Number of common area page-ins (LPA + CSA) from auxiliary storage to central storage.")
    smf30hpi: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Number of hiperspace page-ins from auxiliary to processor")
    smf30lpi: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Number of LPA page-ins from auxiliary storage to central storage.")
    smf30hpo: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Number of hiperspace page-outs from processor to auxiliary storage.")
    smf30pst: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="As of z/OS 1.8, this field is no longer valid; the value is always zero. Prior to z/OS 1.8, this field contained: Number of pages stolen from this address space.")
    smf30psc: so.Mapped[Optional[float]] = so.mapped_column(sa.Double,
                                                            doc="Number of CPU page milliseconds for this address space. A page millisecond unit equals 1.024 milliseconds * 1 page (4K). This value can be used to illustrate the duration of memory consumption where a small spike in memory demand may have less of an impact than a smaller amount of memory used over a longer period of time.")
    smf30pie: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="As of z/OS 1.6, this field is no longer valid; the value is always zero. Prior to z/OS 1.6, this field contained: Number of unblocked pages that were paged in from expanded storage.")
    smf30poe: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="As of z/OS 1.6, this field is no longer valid; the value is always zero. Prior to z/OS 1.6, this field contained: Number of unblocked pages that were paged out to expanded storage.")
    smf30bia: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Number of blocked pages that were paged in from auxiliary storage.")
    smf30boa: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Number of blocked pages that were paged out to auxiliary storage.")
    smf30bie: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="As of z/OS 1.6, this field is no longer valid; the value is always zero. Prior to z/OS 1.6, this field contained: Number of blocked pages that were paged in from expanded storage.")
    smf30boe: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="As of z/OS 1.6, this field is no longer valid; the value is always zero. Prior to z/OS 1.6, this field contained: Number of blocked pages that were paged out to expanded storage.")
    smf30kia: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Number of blocks that were paged in from auxiliary storage.")
    smf30koa: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Number of blocks that were paged out to auxiliary storage.")
    smf30kie: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="As of z/OS 1.6, this field is no longer valid; the value is always zero. Prior to z/OS 1.6, this field contained:")
    smf30koe: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="As of z/OS 1.6, this field is no longer valid; the value is always zero. Prior to z/OS 1.6, this field contained: Number of blocks that were paged out to expanded storage.")
    smf30psf: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Number of CPU page seconds for the IARVSERV shared central storage frames in use by this address space, in page milliseconds.")
    smf30pai: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Binary number of IARVSERV shared pages that were paged in from auxiliary storage when referenced by a unit of work whose home space was this address space.")
    smf30pei: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="As of z/OS 1.6, this field is no longer valid; the value is always zero. Prior to z/OS 1.6, this field contained: Number of IARVSERV shared pages that were paged in from expanded storage in this address space.")
    smf30ers: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="As of z/OS 1.6, this field is no longer valid; the value is always zero. Prior to z/OS 1.6, this field contained: Expanded storage page residency time in page-milliseconds.")
    smf30hvr: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="High water mark for the number of real storage frames that are used to back 64-bit private storage. The high water mark does not include 2G frames.")
    smf30hva: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="High water mark for the amount of auxiliary storage that is used to back 64-bit private storage. This value is a total of the number of paging data set slots and storage-class memory (SCM) blocks.")
    smf30tih: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="High water mark of TIOT space used for TIOT entries (in bytes).")
    smf30numberofdataspaceshwm: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                            doc="The high water mark for the number of in-use data spaces created by problem state user key invokers of DSPSERV during this job step.")
    smf30userdataspacecreatereqcount: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                                  doc="The total number of data spaces created by problem state user key callers during this job step.")
    smf30_dmemrequested2g: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                       doc="Requested dedicated memory, in 2G units, at start of job step.")
    smf30_dmemminrequested2g: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                          doc="Requested minimum amount of dedicated memory, in 2G units, at start of job step.")
    smf30_dmemassigned2g: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                      doc="Assigned dedicated memory, in 2G units, at start of job step.")
    smf30_dmemnuminuseas2g: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                        doc="Number of 2G dedicated memory frames in use.")
    smf30_dmemnuminuseasfixed1m: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                             doc="Number of fixed 1M dedicated memory frames in use.")
    smf30_dmemnuminuseaspageable1m: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                                doc="Number of pageable 1M dedicated memory frames in use.")
    smf30_dmemnuminuseas4k: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                        doc="Number of 4K dedicated memory frames in use.")
    smf30_dmemnuminuseasdattables: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                               doc="Number of 4K dedicated memory frames in use as DAT tables.")
    smf30_dmemnuminuseas4khwm: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                           doc="High-water mark for the number of dedicated real storage")
    smf30_dmemnuminuseaspageable1mhwm: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                                   doc="High-water mark of the number of dedicated real storage frames (1M units) that are used to back pageable 1M pages.")
    smf30_dmemnuminuseasfixed1mhwm: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                                doc="High-water mark of the number of dedicated real storage frames (1M units) that are used to back fixed 1M pages.")
    smf30_dmemnuminuseas2ghwm: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                           doc="High-water mark of the number of dedicated real storage frames (2G units) that are used to back 2G pages.")
    smf30_dmemnuminuseasdattableshwm: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                                  doc="High-water mark of the number of dedicated real storage frames (4K units) that are used to back DAT tables.")
    smf30_dmemnuminusehwm: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                       doc="High-water mark of the number of dedicated memory frames in use, in 4K units.")
    smf30_dmemnum2gfailed: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                       doc="Count of requested 2G frames that were eligible to be backed by dedicated memory frames but were not because not enough dedicated memory frames were available.")
    smf30_dmemnum1mfailed: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                       doc="Count of requested 1M frames that were eligible to be backed by dedicated memory frames but were not because not enough dedicated memory frames were available.")
    smf30_dmemnum4kfailed: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                       doc="Count of requested 4K frames that were eligible to be backed by dedicated memory frames but were not because not enough dedicated memory frames were available.")
    smf30_numinuseas2ghwm: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                       doc="High water mark for the number of 2G frames in use by the job step.")
    smf30_num2gfailed: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                   doc="Number of 2G frames that could not be obtained because none were available at the time of the IARV64 request.")
    smf30_obtainshomespace: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                        doc="Number of GETMAIN or STORAGE OBTAIN requests within the scope of the record, either for the current interval, job step, or job. Results are for the home address space at the time of the invocation.")
    smf30_iarv64obtainshomespace: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                              doc="Number of IARV64 GETSTOR or GETCOMMON requests within the scope of the record, either for the current interval, job step, or job. Results are for the home address space at the time of the invocation.")
    smf30_framesfirstreferencebacking: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                                   doc="Count of real storage frames (4K units) that are backing both 31-bit and 64-bit first-reference virtual storage within the scope of the record, either for the current interval, job step, or job. Count includes dedicated real storage frames.")
    smf30_sumreal1m: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                 doc="Sum of samples of the amount of real memory (includes dedicated memory) in 1M units used by the address space within the scope of the record, either for the current interval, job step, or job.")
    smf30_sumsquaresreal1m: so.Mapped[Optional[str]] = so.mapped_column(sa.String(34),
                                                                        doc="Sum of squared samples of the amount of real memory (includes dedicated memory) in 1M units used by the address space within the scope of the record, either for the current interval, job step, or job.")
    smf30_numsamples: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                  doc="Number of samples for both SMF30_SumReal1M and SMF30_SumSquaresReal1M within the scope of the record, either for the current interval, job step, or job.")
    smf30_hwmhvreal1m: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                   doc="High water mark for the number, in 1M units, of real frames (includes dedicated memory) that are backing 64-bit virtual private storage for all frame types (4K, 1M, and 2G) within the scope of the record, either for the current interval, job step, or job.")
