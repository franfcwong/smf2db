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


class Base75(Base):
    __abstract__ = True
    metadata = sa.MetaData(schema='smf75', naming_convention=convention)


class Base75Hr(Base):
    __abstract__ = True
    metadata = sa.MetaData(schema='smf75', naming_convention=convention)


class Base75Da(Base):
    __abstract__ = True
    metadata = sa.MetaData(schema='smf75', naming_convention=convention)


class Smf75pro(AbstractConcreteBase):
    """Abstract class for structure Smf75Pro - RMF product section."""

    smf75mfv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="RMF version number.")
    smf75prd: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Product name ('RMF').")
    smf75int: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Duration of the RMF measurement interval, in the form mmsstttF where mm is the minutes, ss is the seconds, ttt is the milliseconds, and F is the sign. The end of the measurement interval is the sum of the recorded start time (and this field.)")
    smf75sam: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of RMF samples.")
    smf75fla: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Flags Bit Meaning when set 0 Reserved 1 Samples have been skipped 2 Record was written by RMF Monitor III 3 Interval was synchronized with SMF 4 SMF record converted to lower service level. 5 SMF record converted to higher release or service level. 6 Running under an alternate virtual machine. 7 - 15 Reserved.")
    smf75cyc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Sampling cycle length, in the form 000 ttttF , where tttt is the milliseconds and F is the sign (taken from CYCLE option). The range of values is 0.050 to 9.999 seconds.")
    smf75mvs: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="z/OS software level (consists of an acronym and the version, release, and modification level - ZV vvrrmm ).")
    smf75iml: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Indicates the type of processor complex on which data measurements were taken. Value Meaning 3 9672, zSeries")
    smf75prf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Processor flags. Bit Meaning when set 0 The system has expanded storage 1 The processor is enabled for ES connection architecture (ESCA) 2 There is an ES connection director in the configuration 3 System is running in z/Architecture mode 4 At least one zAAP is currently installed 5 At least one zIIP is currently installed 6 Enhanced DAT facility 1 available")
    smf75ptn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="PR/SM partition number of the partition that wrote this record.")
    smf75srl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="SMF record level change number (X'8E' for z/OS V2R4 RMF with RMF Data Gatherer APAR OA59330). This field enables processing of SMF record level changes in an existing release.")
    smf75lgo: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Offset GMT to local time (STCK format).")
    smf75oil: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Original interval length as defined in the session or by SMF (in seconds).")
    smf75syn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="SYNC value in seconds.")
    smf75gie: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                  doc="Projected gathering interval end (STCK format) GMT time.")
    smf75xnm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf75snm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="System name for current system as defined in parmlib member IEASYSxx SYSNAME parameter.")
    smf75flg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="System indicator Bit Meaning when set 0 New record format 1 Subtypes used 2 Reserved. 3-6 Version indicators (See 'Standard and extended SMF record headers' on page 164 for details.) 7 System is running in PR/SM mode.")


class Smf75psd(AbstractConcreteBase):
    """Abstract class for structure Smf75Psd - Page data set data section."""

    smf75pst: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Page space type: Bit Meaning when set 0 PLPA 1 COMMON 2 Reserved. 3 LOCAL 4 Reserved. 5 Data set unusable. 6 Data set brought online during interval. 7 Data set taken offline during interval.")
    smf75fl2: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Bit Meaning when set 0 Data set accepts VIO pages. 1 Reserved. 2 Data set is on a device with an alternate control unit. 3 SMF75DEV contains a valid device name. 4 Page space type is SCM.")
    smf75typ: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="Device type. Valid only when bit 4 of SMF75FL2 is not set.")
    smf75cha: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6),
                                                          doc="Device number in the form hhhh (hex digits). Valid only when bit 4 of SMF75FL2 is not set.")
    smf75vol: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6),
                                                          doc="Volume serial number. Valid only when bit 4 of SMF75FL2 is not set.")
    smf75scs: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4),
                                                          doc="Subchannel set ID. Valid only when bit 4 of SMF75FL2 is not set.")
    smf75sla: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of slots contained within the page data set.")
    smf75mxu: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Maximum number of slots used.")
    smf75mnu: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Minimum number of slots used.")
    smf75avu: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Average number of slots used.")
    smf75bds: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of unusable slots.")
    smf75use: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of samples indicating data set was being used by ASM.")
    smf75req: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="The value is the same as SMF75USE.")
    smf75sio: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of I/O requests for the data set.")
    smf75pgx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of pages transferred to or from page data set.")
    smf75dev: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="Device name (blank if device name cannot be determined). Valid only when bit 4 of SMF75FL2 is not set.")
    smf75cu: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                         doc="Control unit name (blank if control unit name cannot be determined). Valid only when bit 4 of SMF75FL2 is not set.")
    smf75lvu: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Average number of slots used (same as SMF75AVU).")
    smf75int: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Duration of the RMF measurement interval, in the form mmsstttF where mm is the minutes, ss is the seconds, ttt is the milliseconds, and F is the sign. The end of the measurement interval is the sum of the recorded start time (and this field.)")
    smf75sam: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of RMF samples.")
    lpa: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                     doc="smf75pst (Bit 0) showing page space type is PLPA.")
    com: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                     doc="smf75pst (Bit 1) showing page space type is COMMON.")
    loc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                     doc="smf75pst (Bit 3) showing page space type is LOCAL.")
    dsb: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="smf75pst (Bit 5) showing data set unusable.")
    onl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                     doc="smf75pst (Bit 6) showing data set brought online during interval.")
    ofl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                     doc="smf75pst (Bit 7) showing data set taken offline during interval.")
    ds_accepts_vio: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                doc="smf75fl2 (Bit 0) showing data set accepts VIO pages.")
    ds_on_alt_control_unit: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                        doc="smf75fl2 (Bit 2) showing data set is on a device with an alternate control unit.")
    device_name_valid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                   doc="smf75fl2 (Bit 3) showing smf75dev contains a valid device name.")
    page_space_scm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                doc="smf75fl2 (Bit 4) showing page space type is SCM.")
    psbsy: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                         doc="percentage of time during the reporting interval when the data set was considered busy by the Auxiliary Storage Manager (ASM). At each cycle, RMF tests each data set, and at the end of the interval, the percentage is calculated.")
    psptt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                         doc="average number of seconds required to complete a page transfer.")
    pspt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                        doc="number of pages that were transferred to or from the page data set or SCM in units of 4K pages.")
    psart: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                         doc="total number of I/O requests for the data set made during the interval.")
