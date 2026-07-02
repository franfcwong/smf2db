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


class Base77(Base):
    __abstract__ = True
    metadata = sa.MetaData(schema='smf77', naming_convention=convention)


class Base77Hr(Base):
    __abstract__ = True
    metadata = sa.MetaData(schema='smf77', naming_convention=convention)


class Base77Da(Base):
    __abstract__ = True
    metadata = sa.MetaData(schema='smf77', naming_convention=convention)


class Smf77pro(AbstractConcreteBase):
    """Abstract class for structure Smf77Pro - RMF product section."""

    smf77mfv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="RMF version number.")
    smf77prd: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Product name ('RMF').")
    smf77int: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Duration of RMF measurement interval, in the form mmsstttF where mm is the minutes, ss is the seconds, ttt is the milliseconds, and F is the sign. (The end of the measurement interval is the sum of the recorded start time and this field.)")
    smf77sam: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of RMF samples.")
    smf77fla: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Flags Bit Meaning when set 0 Reserved 1 Samples have been skipped 2 Record was written by RMF Monitor III 3 Interval was synchronized with SMF 4 SMF record converted to lower service level. 5 SMF record converted to higher release or service level. 6 Running under an alternate virtual machine. 7 - 15 Reserved.")
    smf77cyc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Sampling cycle length, in the form 000 ttttF , where tttt is the milliseconds and F is the sign (taken from CYCLE option). The")
    smf77mvs: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="z/OS software level (consists of an acronym and the version,")
    smf77iml: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Indicates the type of processor complex on which data measurements were taken. Value Meaning 3 9672, zSeries")
    smf77prf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Processor flags. Bit Meaning when set 0 The system has expanded storage 1 The processor is enabled for ES connection architecture (ESCA) 2 There is an ES connection director in the configuration 3 System is running in z/Architecture mode 4 At least one zAAP is currently installed 5 At least one zIIP is currently installed 6 Enhanced DAT facility 1 available 7 Enhanced DAT facility 2 available")
    smf77ptn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="PR/SM partition number of the partition that wrote this record.")
    smf77srl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="SMF record level change number (X'8E' for z/OS V2R4 RMF with RMF Data Gatherer APAR OA59330). This field enables processing of SMF record level changes in an existing release.")
    smf77lgo: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Offset GMT to local time (STCK format).")
    smf77oil: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Original interval length as defined in the session or by SMF (in seconds).")
    smf77syn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="SYNC value in seconds.")
    smf77gie: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                  doc="Projected gathering interval end (STCK format) GMT time.")
    smf77xnm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf77snm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="System name for current system as defined in parmlib member IEASYSxx SYSNAME parameter.")
    smf77flg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="System indicator Bit Meaning when set 0 New record format 1 Subtypes used 2 Reserved. 3-6 Version indicators* 7 System is running in PR/SM mode. *See 'Standard and extended SMF record headers' on page 164 for a detailed description.")


class Smf77ctl(AbstractConcreteBase):
    """Abstract class for structure Smf77Ctl - Enqueue control section."""

    smf77fg1: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Enqueue status indicator Bit Meaning 0 Enqueue summary table full 1 Specified resource had no contention 2 Enqueue had bad CPU clock 3 Enqueue event processing abend 4 On - detail data requested   Off - summary data requested 5 On - GRS=NONE (local sysplex) 6 Off - GRS=RING, if bit 5 = '0' 7 On - bits 5 and 6 are valid")
    smf77rf2: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Second status indicator Bit Meaning 0 GRS system problems 1 RMF/GRS interface problems 2-7 Reserved.")
    resource_no_contention: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                        doc="smf77fg1 (Bit 1) showing specified resource had no contention.")
    enqueue_bad_cpu_clock: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                       doc="smf77fg1 (Bit 2) showing enqueue had bad CPU clock.")
    enqueue_processing_abend: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                          doc="smf77fg1 (Bit 3) showing enqueue event processing abend.")
    detail_data_req: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                 doc="smf77fg1 (Bit 4) showing detail data requested if ON, otherwise summary data requested.")
    grs_none: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="smf77fg1 (Bit 5) showing GRS=NONE (local sysplex).")
    grs_ring: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="smf77fg1 (Bit 6) showing GRS=RING, if bit 5 = '0'.")
    grs_mode: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="smf77fg1 (Bit 7) showing bits 5 and 6 are valid.")
    grs_sys_problem: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                 doc="smf77rf2 (Bit 0) showing GRS system problems.")
    grs_interface_problem: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                       doc="smf77rf2 (Bit 1) showing RMF/GRS interface problems.")


class Smf77enq(AbstractConcreteBase):
    """Abstract class for structure Smf77Enq - Enqueue data section."""

    smf77wtm: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Minimum resource contention time during the measurement interval, in 1024-microsecond units. After an internal RMF restart (for example, due to a change of gatherer options) the contention time can be larger than the measurement interval.")
    smf77wtx: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Maximum resource contention time during the measurement interval, in 1024-microsecond units. After an internal RMF restart (for example, due to a change of gatherer options) the contention time can be larger than the measurement interval.")
    smf77wtt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total resource contention time during the measurement interval, in 1024-microsecond units. After an internal RMF restart (for example, due to a change of gatherer options) the contention time can be larger than the measurement interval.")
    smf77ql1: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Counter for queue length of 1.")
    smf77ql2: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Counter for queue length of 2.")
    smf77ql3: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Counter for queue length of 3.")
    smf77ql4: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Counter for queue length of 4 or more.")
    smf77exm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Minimum number of exclusive requests waiting.")
    smf77exx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Maximum number of exclusive requests waiting.")
    smf77shm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Minimum number of share requests waiting.")
    smf77shx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Maximum number of share requests waiting.")
    smf77evt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of contention events that occurred during the measurement interval. A contention event is the period starting from the time when the resource has contention until the resource no longer has contention.")
    smf77dow: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of owners using the resource at maximum contention.")
    smf77dwr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of jobs waiting for the resource at maximum contention.")
    smf77aql: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of waiting requests during the measurement interval.")
    smf77csc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of contention status change events that occurred during the measurement interval.")
    smf77nod: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of contention status change events accumulated during the measurement interval which did not provide separate contention detail data.")
