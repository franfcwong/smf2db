import datetime as dt
from typing import List, Optional

import sqlalchemy as sa
import sqlalchemy.orm as so

from .smf78_base import ReprMixin, Base78Da, Smf78gd, Smf78ds, Smf78hpav, Smf78iqd, Smf78cpd, Smf78pro, Smf78comn, \
    Smf78pvsp, Smf78pvt, Smf78amg


class Smf78ProDa(ReprMixin, Base78Da, Smf78pro):
    """The Smf78ProDa class stores the daily Smf78Pro record in the smf78_pro_da table."""

    __tablename__ = "smf78_pro_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    speed_boost: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                             doc="smf78fla (Bit 10) indcating speed boost was active during entire interval.")
    ziip_boost: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                            doc="smf78fla (Bit 9) indciating zIIP boost was active during entire interval.")
    smf_type: so.Mapped[str] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf78sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(date, smf_type, csc, smf78sid),
    )

    smf78_comn_das: so.Mapped[List['Smf78ComnDa']] = so.relationship(back_populates='smf78_pro_da', viewonly=True)
    smf78_pvt_das: so.Mapped[List['Smf78PvtDa']] = so.relationship(back_populates='smf78_pro_da', viewonly=True)
    smf78_ioq_das: so.Mapped[List['Smf78IoqDa']] = so.relationship(back_populates='smf78_pro_da', viewonly=True)


class Smf78ComnDa(ReprMixin, Base78Da, Smf78comn):
    """The Smf78ComnDa class stores the daily Smf78Comn record in the smf78_comn_da table."""

    __tablename__ = "smf78_comn_da"
    smf_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf78sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf78sid, date),

        sa.ForeignKeyConstraint(
            ['date', 'smf_type', 'csc', 'smf78sid'],
            ['smf78_pro_da.date', 'smf78_pro_da.smf_type', 'smf78_pro_da.csc', 'smf78_pro_da.smf78sid']),
    )

    smf78_pro_da: so.Mapped['Smf78ProDa'] = so.relationship(back_populates='smf78_comn_das', viewonly=True)


class Smf78PvspDa(ReprMixin, Base78Da, Smf78pvsp):
    """The Smf78PvspDa class stores the daily Smf78Pvsp record in the smf78_pvsp_da table."""

    __tablename__ = "smf78_pvsp_da"
    r782spn: so.Mapped[int] = so.mapped_column(sa.Integer,
                                               doc="Subpool number. Each Private Area data section occurs one after the other. All Private Area Subpool sections follow all Private Area data sections. To relate a subpool to a job, see the R782SUBN fields in the Private Area data section.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf78sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    r782jobn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Name of job being monitored.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf78sid, date, r782jobn, r782spn),

        sa.ForeignKeyConstraint(
            ['csc', 'smf78sid', 'date', 'r782jobn'],
            ['smf78_pvt_da.csc', 'smf78_pvt_da.smf78sid', 'smf78_pvt_da.date', 'smf78_pvt_da.r782jobn']),
    )

    smf78_pvt_da: so.Mapped['Smf78PvtDa'] = so.relationship(back_populates='smf78_pvsp_das', viewonly=True)


class Smf78PvtDa(ReprMixin, Base78Da, Smf78pvt):
    """The Smf78PvtDa class stores the daily Smf78Pvt record in the smf78_pvt_da table."""

    __tablename__ = "smf78_pvt_da"
    r782jobn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Name of job being monitored.")
    smf_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf78sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf78sid, date, r782jobn),

        sa.ForeignKeyConstraint(
            ['date', 'smf_type', 'csc', 'smf78sid'],
            ['smf78_pro_da.date', 'smf78_pro_da.smf_type', 'smf78_pro_da.csc', 'smf78_pro_da.smf78sid']),
    )

    smf78_pro_da: so.Mapped['Smf78ProDa'] = so.relationship(back_populates='smf78_pvt_das', viewonly=True)
    smf78_pvsp_das: so.Mapped[List['Smf78PvspDa']] = so.relationship(back_populates='smf78_pvt_da', viewonly=True)


class Smf78IoqDa(ReprMixin, Base78Da, Smf78gd, Smf78iqd):
    """The Smf78IoqDa class stores the daily Smf78Ioq record in the smf78_ioq_da table."""

    __tablename__ = "smf78_ioq_da"
    smf_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf78sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf78sid, date),

        sa.ForeignKeyConstraint(
            ['date', 'smf_type', 'csc', 'smf78sid'],
            ['smf78_pro_da.date', 'smf78_pro_da.smf_type', 'smf78_pro_da.csc', 'smf78_pro_da.smf78sid']),
    )

    smf78_pro_da: so.Mapped['Smf78ProDa'] = so.relationship(back_populates='smf78_ioq_das', viewonly=True)
    smf78_iop_das: so.Mapped[List['Smf78IopDa']] = so.relationship(back_populates='smf78_ioq_da', viewonly=True)
    smf78_amg_das: so.Mapped[List['Smf78AmgDa']] = so.relationship(back_populates='smf78_ioq_da', viewonly=True)
    smf78_lcu_das: so.Mapped[List['Smf78LcuDa']] = so.relationship(back_populates='smf78_ioq_da', viewonly=True)


class Smf78IopDa(ReprMixin, Base78Da, Smf78iqd):
    """The Smf78IopDa class stores the daily Smf78Iop record in the smf78_iop_da table."""

    __tablename__ = "smf78_iop_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf78sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    r783iqid: so.Mapped[str] = so.mapped_column(sa.String(6),
                                                doc="Input output processor (IOP) initiative queue identifier.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf78sid, date, r783iqid),

        sa.ForeignKeyConstraint(
            ['csc', 'smf78sid', 'date'],
            ['smf78_ioq_da.csc', 'smf78_ioq_da.smf78sid', 'smf78_ioq_da.date']),
    )

    smf78_ioq_da: so.Mapped['Smf78IoqDa'] = so.relationship(back_populates='smf78_iop_das', viewonly=True)


class Smf78AmgDa(ReprMixin, Base78Da, Smf78amg):
    """The Smf78AmgDa class stores the daily Smf78Amg record in the smf78_amg_da table."""

    __tablename__ = "smf78_amg_da"
    r783amgs: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="The alias management group number assigned by z/OS for this LCU on this system. This number is valid, if the LCU is assigned to a DASD subsystem that supports alias management groups and bit 7 of R783DST is set.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf78sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf78sid, date, r783amgs),

        sa.ForeignKeyConstraint(
            ['csc', 'smf78sid', 'date'],
            ['smf78_ioq_da.csc', 'smf78_ioq_da.smf78sid', 'smf78_ioq_da.date']),
    )

    smf78_ioq_da: so.Mapped['Smf78IoqDa'] = so.relationship(back_populates='smf78_amg_das', viewonly=True)
    smf78_cha_das: so.Mapped[List['Smf78ChaDa']] = so.relationship(back_populates='smf78_amg_da', viewonly=True,
                                                                   foreign_keys=[csc, smf78sid, date, r783amgs],
                                                                   primaryjoin='and_(Smf78AmgDa.csc==Smf78ChaDa.csc, Smf78AmgDa.smf78sid==Smf78ChaDa.smf78sid, Smf78AmgDa.date==Smf78ChaDa.date, Smf78AmgDa.r783amgs==Smf78ChaDa.r783amgs)', )
    smf78_lcu_das: so.Mapped[List['Smf78LcuDa']] = so.relationship(back_populates='smf78_amg_da', viewonly=True,
                                                                   foreign_keys=[csc, smf78sid, date, r783amgs],
                                                                   primaryjoin='and_(Smf78AmgDa.csc==Smf78LcuDa.csc, Smf78AmgDa.smf78sid==Smf78LcuDa.smf78sid, Smf78AmgDa.date==Smf78LcuDa.date, Smf78AmgDa.r783amgs==Smf78LcuDa.r783amgs)', )
    smf78_chap_das: so.Mapped[List['Smf78ChapDa']] = so.relationship(back_populates='smf78_amg_da', viewonly=True)


class Smf78LcuDa(ReprMixin, Base78Da, Smf78ds, Smf78hpav):
    """The Smf78LcuDa class stores the daily Smf78Lcu record in the smf78_lcu_da table."""

    __tablename__ = "smf78_lcu_da"
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
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf78sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    r783id2: so.Mapped[str] = so.mapped_column(sa.String(6), doc="Logical control unit identifier.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf78sid, date, r783id2),

        sa.ForeignKeyConstraint(
            ['csc', 'smf78sid', 'date'],
            ['smf78_ioq_da.csc', 'smf78_ioq_da.smf78sid', 'smf78_ioq_da.date']),
    )

    smf78_ioq_da: so.Mapped['Smf78IoqDa'] = so.relationship(back_populates='smf78_lcu_das', viewonly=True)
    smf78_amg_da: so.Mapped['Smf78AmgDa'] = so.relationship(back_populates='smf78_lcu_das', viewonly=True,
                                                            foreign_keys='Smf78AmgDa.csc, Smf78AmgDa.smf78sid, Smf78AmgDa.date, Smf78AmgDa.r783amgs',
                                                            primaryjoin='and_(Smf78LcuDa.csc==Smf78AmgDa.csc, Smf78LcuDa.smf78sid==Smf78AmgDa.smf78sid, Smf78LcuDa.date==Smf78AmgDa.date, Smf78LcuDa.r783amgs==Smf78AmgDa.r783amgs)', )
    smf78_cha_das: so.Mapped[List['Smf78ChaDa']] = so.relationship(back_populates='smf78_lcu_da', viewonly=True)


class Smf78ChapDa(ReprMixin, Base78Da, Smf78cpd):
    """The Smf78ChapDa class stores the daily Smf78Chap record in the smf78_chap_da table."""

    __tablename__ = "smf78_chap_da"
    r783mcmn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Minimum number of DCM managed channels used.")
    r783mcmx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Maximum number of DCM managed channels used.")
    r783mcdf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Defined number of DCM managed channels.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf78sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    r783amgs: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="The alias management group number assigned by z/OS for this LCU on this system. This number is valid, if the LCU is assigned to a DASD subsystem that supports alias management groups and bit 7 of R783DST is set.")
    r783cpid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Channel path identifier.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf78sid, date, r783amgs, r783cpid),

        sa.ForeignKeyConstraint(
            ['csc', 'smf78sid', 'date', 'r783amgs'],
            ['smf78_amg_da.csc', 'smf78_amg_da.smf78sid', 'smf78_amg_da.date', 'smf78_amg_da.r783amgs']),
    )

    smf78_amg_da: so.Mapped['Smf78AmgDa'] = so.relationship(back_populates='smf78_chap_das', viewonly=True)
    smf78_cha_das: so.Mapped[List['Smf78ChaDa']] = so.relationship(back_populates='smf78_chap_da', viewonly=True,
                                                                   foreign_keys=[csc, smf78sid, date, r783amgs,
                                                                                 r783cpid],
                                                                   primaryjoin='and_(Smf78ChapDa.csc==Smf78ChaDa.csc, Smf78ChapDa.smf78sid==Smf78ChaDa.smf78sid, Smf78ChapDa.date==Smf78ChaDa.date, Smf78ChapDa.r783amgs==Smf78ChaDa.r783amgs, Smf78ChapDa.r783cpid==Smf78ChaDa.r783cpid)', )


class Smf78ChaDa(ReprMixin, Base78Da, Smf78cpd):
    """The Smf78ChaDa class stores the daily Smf78Cha record in the smf78_cha_da table."""

    __tablename__ = "smf78_cha_da"
    r783amgs: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="The alias management group number assigned by z/OS for this LCU on this system. This number is valid, if the LCU is assigned to a DASD subsystem that supports alias management groups and bit 7 of R783DST is set.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf78sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    r783id1: so.Mapped[str] = so.mapped_column(sa.String(6), doc="Logical control unit identifier.")
    r783cpid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Channel path identifier.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf78sid, date, r783id1, r783cpid),
        sa.ForeignKeyConstraint(
            ['csc', 'smf78sid', 'date', 'r783id1'],
            ['smf78_lcu_da.csc', 'smf78_lcu_da.smf78sid', 'smf78_lcu_da.date', 'smf78_lcu_da.r783id2']),
    )

    smf78_amg_da: so.Mapped['Smf78AmgDa'] = so.relationship(back_populates='smf78_cha_das', viewonly=True,
                                                            foreign_keys='Smf78AmgDa.csc, Smf78AmgDa.smf78sid, Smf78AmgDa.date, Smf78AmgDa.r783amgs',
                                                            primaryjoin='and_(Smf78ChaDa.csc==Smf78AmgDa.csc, Smf78ChaDa.smf78sid==Smf78AmgDa.smf78sid, Smf78ChaDa.date==Smf78AmgDa.date, Smf78ChaDa.r783amgs==Smf78AmgDa.r783amgs)', )
    smf78_lcu_da: so.Mapped['Smf78LcuDa'] = so.relationship(back_populates='smf78_cha_das', viewonly=True)
    smf78_chap_da: so.Mapped['Smf78ChapDa'] = so.relationship(back_populates='smf78_cha_das', viewonly=True,
                                                              foreign_keys='Smf78ChapDa.csc, Smf78ChapDa.smf78sid, Smf78ChapDa.date, Smf78ChapDa.r783amgs, Smf78ChapDa.r783cpid',
                                                              primaryjoin='and_(Smf78ChaDa.csc==Smf78ChapDa.csc, Smf78ChaDa.smf78sid==Smf78ChapDa.smf78sid, Smf78ChaDa.date==Smf78ChapDa.date, Smf78ChaDa.r783amgs==Smf78ChapDa.r783amgs, Smf78ChaDa.r783cpid==Smf78ChapDa.r783cpid)', )
