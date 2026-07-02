import datetime as dt
from typing import List, Optional

import sqlalchemy as sa
import sqlalchemy.orm as so

from .smf78_base import ReprMixin, Base78Hr, Smf78gd, Smf78ds, Smf78hpav, Smf78iqd, Smf78cpd, Smf78pro, Smf78comn, \
    Smf78pvsp, Smf78pvt, Smf78amg


class Smf78ProHr(ReprMixin, Base78Hr, Smf78pro):
    """The Smf78ProHr class stores the hourly Smf78Pro record in the smf78_pro_hr table."""

    __tablename__ = "smf78_pro_hr"
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    speed_boost: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                             doc="smf78fla (Bit 10) indcating speed boost was active during entire interval.")
    ziip_boost: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                            doc="smf78fla (Bit 9) indciating zIIP boost was active during entire interval.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf_type: so.Mapped[str] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf78sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(datetime, smf_type, csc, smf78sid),
    )

    smf78_comn_hrs: so.Mapped[List['Smf78ComnHr']] = so.relationship(back_populates='smf78_pro_hr', viewonly=True)
    smf78_pvt_hrs: so.Mapped[List['Smf78PvtHr']] = so.relationship(back_populates='smf78_pro_hr', viewonly=True)
    smf78_ioq_hrs: so.Mapped[List['Smf78IoqHr']] = so.relationship(back_populates='smf78_pro_hr', viewonly=True)


class Smf78ComnHr(ReprMixin, Base78Hr, Smf78comn):
    """The Smf78ComnHr class stores the hourly Smf78Comn record in the smf78_comn_hr table."""

    __tablename__ = "smf78_comn_hr"
    smf_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf78sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf78sid, datetime),
        sa.ForeignKeyConstraint(
            ['datetime', 'smf_type', 'csc', 'smf78sid'],
            ['smf78_pro_hr.datetime', 'smf78_pro_hr.smf_type', 'smf78_pro_hr.csc', 'smf78_pro_hr.smf78sid']),
    )

    smf78_pro_hr: so.Mapped['Smf78ProHr'] = so.relationship(back_populates='smf78_comn_hrs', viewonly=True)


class Smf78PvspHr(ReprMixin, Base78Hr, Smf78pvsp):
    """The Smf78PvspHr class stores the hourly Smf78Pvsp record in the smf78_pvsp_hr table."""

    __tablename__ = "smf78_pvsp_hr"
    r782spn: so.Mapped[int] = so.mapped_column(sa.Integer,
                                               doc="Subpool number. Each Private Area data section occurs one after the other. All Private Area Subpool sections follow all Private Area data sections. To relate a subpool to a job, see the R782SUBN fields in the Private Area data section.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf78sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    r782jobn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Name of job being monitored.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf78sid, datetime, r782jobn, r782spn),
        sa.ForeignKeyConstraint(
            ['csc', 'smf78sid', 'datetime', 'r782jobn'],
            ['smf78_pvt_hr.csc', 'smf78_pvt_hr.smf78sid', 'smf78_pvt_hr.datetime', 'smf78_pvt_hr.r782jobn']),
    )

    smf78_pvt_hr: so.Mapped['Smf78PvtHr'] = so.relationship(back_populates='smf78_pvsp_hrs', viewonly=True)


class Smf78PvtHr(ReprMixin, Base78Hr, Smf78pvt):
    """The Smf78PvtHr class stores the hourly Smf78Pvt record in the smf78_pvt_hr table."""

    __tablename__ = "smf78_pvt_hr"
    r782jobn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Name of job being monitored.")
    smf_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf78sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf78sid, datetime, r782jobn),
        sa.ForeignKeyConstraint(
            ['datetime', 'smf_type', 'csc', 'smf78sid'],
            ['smf78_pro_hr.datetime', 'smf78_pro_hr.smf_type', 'smf78_pro_hr.csc', 'smf78_pro_hr.smf78sid']),
    )

    smf78_pro_hr: so.Mapped['Smf78ProHr'] = so.relationship(back_populates='smf78_pvt_hrs', viewonly=True)
    smf78_pvsp_hrs: so.Mapped[List['Smf78PvspHr']] = so.relationship(back_populates='smf78_pvt_hr', viewonly=True)


class Smf78IoqHr(ReprMixin, Base78Hr, Smf78gd, Smf78iqd):
    """The Smf78IoqHr class stores the hourly Smf78Ioq record in the smf78_ioq_hr table."""

    __tablename__ = "smf78_ioq_hr"
    smf_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf78sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf78sid, datetime),
        sa.ForeignKeyConstraint(
            ['datetime', 'smf_type', 'csc', 'smf78sid'],
            ['smf78_pro_hr.datetime', 'smf78_pro_hr.smf_type', 'smf78_pro_hr.csc', 'smf78_pro_hr.smf78sid']),
    )

    smf78_pro_hr: so.Mapped['Smf78ProHr'] = so.relationship(back_populates='smf78_ioq_hrs', viewonly=True)
    smf78_iop_hrs: so.Mapped[List['Smf78IopHr']] = so.relationship(back_populates='smf78_ioq_hr', viewonly=True)
    smf78_amg_hrs: so.Mapped[List['Smf78AmgHr']] = so.relationship(back_populates='smf78_ioq_hr', viewonly=True)
    smf78_lcu_hrs: so.Mapped[List['Smf78LcuHr']] = so.relationship(back_populates='smf78_ioq_hr', viewonly=True)


class Smf78IopHr(ReprMixin, Base78Hr, Smf78iqd):
    """The Smf78IopHr class stores the hourly Smf78Iop record in the smf78_iop_hr table."""

    __tablename__ = "smf78_iop_hr"
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf78sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    r783iqid: so.Mapped[str] = so.mapped_column(sa.String(6),
                                                doc="Input output processor (IOP) initiative queue identifier.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf78sid, datetime, r783iqid),
        sa.ForeignKeyConstraint(
            ['csc', 'smf78sid', 'datetime'],
            ['smf78_ioq_hr.csc', 'smf78_ioq_hr.smf78sid', 'smf78_ioq_hr.datetime']),
    )

    smf78_ioq_hr: so.Mapped['Smf78IoqHr'] = so.relationship(back_populates='smf78_iop_hrs', viewonly=True)


class Smf78AmgHr(ReprMixin, Base78Hr, Smf78amg):
    """The Smf78AmgHr class stores the hourly Smf78Amg record in the smf78_amg_hr table."""

    __tablename__ = "smf78_amg_hr"
    r783amgs: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="The alias management group number assigned by z/OS for this LCU on this system. This number is valid, if the LCU is assigned to a DASD subsystem that supports alias management groups and bit 7 of R783DST is set.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf78sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf78sid, datetime, r783amgs),
        sa.ForeignKeyConstraint(
            ['csc', 'smf78sid', 'datetime'],
            ['smf78_ioq_hr.csc', 'smf78_ioq_hr.smf78sid', 'smf78_ioq_hr.datetime']),
    )

    smf78_ioq_hr: so.Mapped['Smf78IoqHr'] = so.relationship(back_populates='smf78_amg_hrs', viewonly=True)
    smf78_cha_hrs: so.Mapped[List['Smf78ChaHr']] = so.relationship(back_populates='smf78_amg_hr', viewonly=True,
                                                                   foreign_keys=[csc, smf78sid, datetime, r783amgs],
                                                                   primaryjoin='and_(Smf78AmgHr.csc==Smf78ChaHr.csc, Smf78AmgHr.smf78sid==Smf78ChaHr.smf78sid, Smf78AmgHr.datetime==Smf78ChaHr.datetime, Smf78AmgHr.r783amgs==Smf78ChaHr.r783amgs)', )
    smf78_lcu_hrs: so.Mapped[List['Smf78LcuHr']] = so.relationship(back_populates='smf78_amg_hr', viewonly=True,
                                                                   foreign_keys=[csc, smf78sid, datetime, r783amgs],
                                                                   primaryjoin='and_(Smf78AmgHr.csc==Smf78LcuHr.csc, Smf78AmgHr.smf78sid==Smf78LcuHr.smf78sid, Smf78AmgHr.datetime==Smf78LcuHr.datetime, Smf78AmgHr.r783amgs==Smf78LcuHr.r783amgs)', )
    smf78_chap_hrs: so.Mapped[List['Smf78ChapHr']] = so.relationship(back_populates='smf78_amg_hr', viewonly=True)


class Smf78LcuHr(ReprMixin, Base78Hr, Smf78ds, Smf78hpav):
    """The Smf78LcuHr class stores the hourly Smf78Lcu record in the smf78_lcu_hr table."""

    __tablename__ = "smf78_lcu_hr"
    r783amgs: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="The alias management group number assigned by z/OS for this LCU on this system. This number is valid, if the LCU is assigned to a DASD subsystem that supports alias management groups and bit 7 of R783DST is set.")
    r783cun: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of control units attached.")
    r783cu1: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="First control unit attached.")
    r783cu2: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Second control unit attached.")
    r783cu3: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Third control unit attached.")
    r783cu4: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Fourth control unit attached.")
    ioart: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="channel path taken rate.")
    iocub: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                         doc="percentage of requests caused by control unit busy.")
    iodpb: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                         doc="percentage of requests caused by director port busy.")
    iocbt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="average control unit busy delay time.")
    iocmr: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="average initial command reponse time.")
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
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf78sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    r783id2: so.Mapped[str] = so.mapped_column(sa.String(6), doc="Logical control unit identifier.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf78sid, datetime, r783id2),
        sa.ForeignKeyConstraint(
            ['csc', 'smf78sid', 'datetime'],
            ['smf78_ioq_hr.csc', 'smf78_ioq_hr.smf78sid', 'smf78_ioq_hr.datetime']),
    )

    smf78_ioq_hr: so.Mapped['Smf78IoqHr'] = so.relationship(back_populates='smf78_lcu_hrs', viewonly=True)
    smf78_amg_hr: so.Mapped['Smf78AmgHr'] = so.relationship(back_populates='smf78_lcu_hrs', viewonly=True,
                                                            foreign_keys='Smf78AmgHr.csc, Smf78AmgHr.smf78sid, Smf78AmgHr.datetime, Smf78AmgHr.r783amgs',
                                                            primaryjoin='and_(Smf78LcuHr.csc==Smf78AmgHr.csc, Smf78LcuHr.smf78sid==Smf78AmgHr.smf78sid, Smf78LcuHr.datetime==Smf78AmgHr.datetime, Smf78LcuHr.r783amgs==Smf78AmgHr.r783amgs)', )
    smf78_cha_hrs: so.Mapped[List['Smf78ChaHr']] = so.relationship(back_populates='smf78_lcu_hr', viewonly=True)


class Smf78ChapHr(ReprMixin, Base78Hr, Smf78cpd):
    """The Smf78ChapHr class stores the hourly Smf78Chap record in the smf78_chap_hr table."""

    __tablename__ = "smf78_chap_hr"
    r783mcmn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Minimum number of DCM managed channels used.")
    r783mcmx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Maximum number of DCM managed channels used.")
    r783mcdf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Defined number of DCM managed channels.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf78sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    r783amgs: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="The alias management group number assigned by z/OS for this LCU on this system. This number is valid, if the LCU is assigned to a DASD subsystem that supports alias management groups and bit 7 of R783DST is set.")
    r783cpid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Channel path identifier.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf78sid, datetime, r783amgs, r783cpid),
        sa.ForeignKeyConstraint(
            ['csc', 'smf78sid', 'datetime', 'r783amgs'],
            ['smf78_amg_hr.csc', 'smf78_amg_hr.smf78sid', 'smf78_amg_hr.datetime', 'smf78_amg_hr.r783amgs']),
    )

    smf78_amg_hr: so.Mapped['Smf78AmgHr'] = so.relationship(back_populates='smf78_chap_hrs', viewonly=True)
    smf78_cha_hrs: so.Mapped[List['Smf78ChaHr']] = so.relationship(back_populates='smf78_chap_hr', viewonly=True,
                                                                   foreign_keys=[csc, smf78sid, datetime, r783amgs,
                                                                                 r783cpid],
                                                                   primaryjoin='and_(Smf78ChapHr.csc==Smf78ChaHr.csc, Smf78ChapHr.smf78sid==Smf78ChaHr.smf78sid, Smf78ChapHr.datetime==Smf78ChaHr.datetime, Smf78ChapHr.r783amgs==Smf78ChaHr.r783amgs, Smf78ChapHr.r783cpid==Smf78ChaHr.r783cpid)', )


class Smf78ChaHr(ReprMixin, Base78Hr, Smf78cpd):
    """The Smf78ChaHr class stores the hourly Smf78Cha record in the smf78_cha_hr table."""

    __tablename__ = "smf78_cha_hr"
    r783amgs: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="The alias management group number assigned by z/OS for this LCU on this system. This number is valid, if the LCU is assigned to a DASD subsystem that supports alias management groups and bit 7 of R783DST is set.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf78sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    r783id1: so.Mapped[str] = so.mapped_column(sa.String(6), doc="Logical control unit identifier.")
    r783cpid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Channel path identifier.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf78sid, datetime, r783id1, r783cpid),
        sa.ForeignKeyConstraint(
            ['csc', 'smf78sid', 'datetime', 'r783id1'],
            ['smf78_lcu_hr.csc', 'smf78_lcu_hr.smf78sid', 'smf78_lcu_hr.datetime', 'smf78_lcu_hr.r783id2']),
    )

    smf78_amg_hr: so.Mapped['Smf78AmgHr'] = so.relationship(back_populates='smf78_cha_hrs', viewonly=True,
                                                            foreign_keys='Smf78AmgHr.csc, Smf78AmgHr.smf78sid, Smf78AmgHr.datetime, Smf78AmgHr.r783amgs',
                                                            primaryjoin='and_(Smf78ChaHr.csc==Smf78AmgHr.csc, Smf78ChaHr.smf78sid==Smf78AmgHr.smf78sid, Smf78ChaHr.datetime==Smf78AmgHr.datetime, Smf78ChaHr.r783amgs==Smf78AmgHr.r783amgs)', )
    smf78_lcu_hr: so.Mapped['Smf78LcuHr'] = so.relationship(back_populates='smf78_cha_hrs', viewonly=True)
    smf78_chap_hr: so.Mapped['Smf78ChapHr'] = so.relationship(back_populates='smf78_cha_hrs', viewonly=True,
                                                              foreign_keys='Smf78ChapHr.csc, Smf78ChapHr.smf78sid, Smf78ChapHr.datetime, Smf78ChapHr.r783amgs, Smf78ChapHr.r783cpid',
                                                              primaryjoin='and_(Smf78ChaHr.csc==Smf78ChapHr.csc, Smf78ChaHr.smf78sid==Smf78ChapHr.smf78sid, Smf78ChaHr.datetime==Smf78ChapHr.datetime, Smf78ChaHr.r783amgs==Smf78ChapHr.r783amgs, Smf78ChaHr.r783cpid==Smf78ChapHr.r783cpid)', )
