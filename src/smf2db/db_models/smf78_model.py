import datetime as dt
from typing import List, Optional

import sqlalchemy as sa
import sqlalchemy.orm as so

from .smf78_base import ReprMixin, Base78, Smf78gd, Smf78ds, Smf78hpav, Smf78iqd, Smf78cpd, Smf78pro, Smf78comn, \
    Smf78pvsp, Smf78pvt, Smf78amg


class Smf78Pro(ReprMixin, Base78, Smf78pro):
    """The Smf78Pro class stores the Smf78Pro section in the smf78_pro table."""

    __tablename__ = "smf78_pro"
    smf78ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF Monitor I measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf78iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval was synchronized with SMF).")
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
        sa.PrimaryKeyConstraint(datetime, smf78ist, smf78iet, smf_type, csc, smf78sid),
    )

    smf78_comns: so.Mapped[List['Smf78Comn']] = so.relationship(back_populates='smf78_pro', viewonly=True)
    smf78_pvts: so.Mapped[List['Smf78Pvt']] = so.relationship(back_populates='smf78_pro', viewonly=True)
    smf78_ioqs: so.Mapped[List['Smf78Ioq']] = so.relationship(back_populates='smf78_pro', viewonly=True)


class Smf78Comn(ReprMixin, Base78, Smf78comn):
    """The Smf78Comn class stores the Smf78Comn section in the smf78_comn table."""

    __tablename__ = "smf78_comn"
    smf_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf78sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf78ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF Monitor I measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf78iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval was synchronized with SMF).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf78sid, datetime, smf78ist, smf78iet),
        sa.ForeignKeyConstraint(
            ['datetime', 'smf78ist', 'smf78iet', 'smf_type', 'csc', 'smf78sid'],
            ['smf78_pro.datetime', 'smf78_pro.smf78ist', 'smf78_pro.smf78iet', 'smf78_pro.smf_type', 'smf78_pro.csc',
             'smf78_pro.smf78sid']),
    )

    smf78_pro: so.Mapped['Smf78Pro'] = so.relationship(back_populates='smf78_comns', viewonly=True)


class Smf78Pvsp(ReprMixin, Base78, Smf78pvsp):
    """The Smf78Pvsp class stores the Smf78Pvsp section in the smf78_pvsp table."""

    __tablename__ = "smf78_pvsp"
    r782spn: so.Mapped[int] = so.mapped_column(sa.Integer,
                                               doc="Subpool number. Each Private Area data section occurs one after the other. All Private Area Subpool sections follow all Private Area data sections. To relate a subpool to a job, see the R782SUBN fields in the Private Area data section.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf78sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf78ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF Monitor I measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf78iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval was synchronized with SMF).")
    r782jobn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Name of job being monitored.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf78sid, datetime, smf78ist, smf78iet, r782jobn, r782spn),
        sa.ForeignKeyConstraint(
            ['csc', 'smf78sid', 'datetime', 'smf78ist', 'smf78iet', 'r782jobn'],
            ['smf78_pvt.csc', 'smf78_pvt.smf78sid', 'smf78_pvt.datetime', 'smf78_pvt.smf78ist', 'smf78_pvt.smf78iet',
             'smf78_pvt.r782jobn']),
    )

    smf78_pvt: so.Mapped['Smf78Pvt'] = so.relationship(back_populates='smf78_pvsps', viewonly=True)


class Smf78Pvt(ReprMixin, Base78, Smf78pvt):
    """The Smf78Pvt class stores the Smf78Pvt section in the smf78_pvt table."""

    __tablename__ = "smf78_pvt"
    r782jobn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Name of job being monitored.")
    r782subi: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Index of first subpool entry in the Private Area Subpool section for this job. This field provides the first array element for this job's Private Area Subpool sections.")
    r782subn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Index of last subpool entry for this job. This field provides the last array element for this job's private area subpools.")
    smf_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf78sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf78ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF Monitor I measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf78iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval was synchronized with SMF).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf78sid, datetime, smf78ist, smf78iet, r782jobn),
        sa.ForeignKeyConstraint(
            ['datetime', 'smf78ist', 'smf78iet', 'smf_type', 'csc', 'smf78sid'],
            ['smf78_pro.datetime', 'smf78_pro.smf78ist', 'smf78_pro.smf78iet', 'smf78_pro.smf_type', 'smf78_pro.csc',
             'smf78_pro.smf78sid']),
    )

    smf78_pro: so.Mapped['Smf78Pro'] = so.relationship(back_populates='smf78_pvts', viewonly=True)
    smf78_pvsps: so.Mapped[List['Smf78Pvsp']] = so.relationship(back_populates='smf78_pvt', viewonly=True)


class Smf78Ioq(ReprMixin, Base78, Smf78gd, Smf78iqd):
    """The Smf78Ioq class stores the Smf78Ioq section in the smf78_ioq table."""

    __tablename__ = "smf78_ioq"
    smf_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf78sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf78ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF Monitor I measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf78iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval was synchronized with SMF).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf78sid, datetime, smf78ist, smf78iet),
        sa.ForeignKeyConstraint(
            ['datetime', 'smf78ist', 'smf78iet', 'smf_type', 'csc', 'smf78sid'],
            ['smf78_pro.datetime', 'smf78_pro.smf78ist', 'smf78_pro.smf78iet', 'smf78_pro.smf_type', 'smf78_pro.csc',
             'smf78_pro.smf78sid']),
    )

    smf78_pro: so.Mapped['Smf78Pro'] = so.relationship(back_populates='smf78_ioqs', viewonly=True)
    smf78_iops: so.Mapped[List['Smf78Iop']] = so.relationship(back_populates='smf78_ioq', viewonly=True)
    smf78_amgs: so.Mapped[List['Smf78Amg']] = so.relationship(back_populates='smf78_ioq', viewonly=True)
    smf78_lcus: so.Mapped[List['Smf78Lcu']] = so.relationship(back_populates='smf78_ioq', viewonly=True)


class Smf78Iop(ReprMixin, Base78, Smf78iqd):
    """The Smf78Iop class stores the Smf78Iop section in the smf78_iop table."""

    __tablename__ = "smf78_iop"
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf78sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf78ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF Monitor I measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf78iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval was synchronized with SMF).")
    r783iqid: so.Mapped[str] = so.mapped_column(sa.String(6),
                                                doc="Input output processor (IOP) initiative queue identifier.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf78sid, datetime, smf78ist, smf78iet, r783iqid),
        sa.ForeignKeyConstraint(
            ['csc', 'smf78sid', 'datetime', 'smf78ist', 'smf78iet'],
            ['smf78_ioq.csc', 'smf78_ioq.smf78sid', 'smf78_ioq.datetime', 'smf78_ioq.smf78ist', 'smf78_ioq.smf78iet']),
    )

    smf78_ioq: so.Mapped['Smf78Ioq'] = so.relationship(back_populates='smf78_iops', viewonly=True)


class Smf78Amg(ReprMixin, Base78, Smf78amg):
    """The Smf78Amg class stores the Smf78Amg section in the smf78_amg table."""

    __tablename__ = "smf78_amg"
    r783amgs: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="The alias management group number assigned by z/OS for this LCU on this system. This number is valid, if the LCU is assigned to a DASD subsystem that supports alias management groups and bit 7 of R783DST is set.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf78sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf78ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF Monitor I measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf78iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval was synchronized with SMF).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf78sid, datetime, smf78ist, smf78iet, r783amgs),
        sa.ForeignKeyConstraint(
            ['csc', 'smf78sid', 'datetime', 'smf78ist', 'smf78iet'],
            ['smf78_ioq.csc', 'smf78_ioq.smf78sid', 'smf78_ioq.datetime', 'smf78_ioq.smf78ist', 'smf78_ioq.smf78iet']),
    )

    smf78_ioq: so.Mapped['Smf78Ioq'] = so.relationship(back_populates='smf78_amgs', viewonly=True)
    smf78_chas: so.Mapped[List['Smf78Cha']] = so.relationship(back_populates='smf78_amg', viewonly=True,
                                                              foreign_keys=[csc, smf78sid, datetime, smf78ist, smf78iet,
                                                                            r783amgs],
                                                              primaryjoin='and_(Smf78Amg.csc==Smf78Cha.csc, Smf78Amg.smf78sid==Smf78Cha.smf78sid, Smf78Amg.datetime==Smf78Cha.datetime, Smf78Amg.smf78ist==Smf78Cha.smf78ist, Smf78Amg.smf78iet==Smf78Cha.smf78iet, Smf78Amg.r783amgs==Smf78Cha.r783amgs)', )
    smf78_lcus: so.Mapped[List['Smf78Lcu']] = so.relationship(back_populates='smf78_amg', viewonly=True,
                                                              foreign_keys=[csc, smf78sid, datetime, smf78ist, smf78iet,
                                                                            r783amgs],
                                                              primaryjoin='and_(Smf78Amg.csc==Smf78Lcu.csc, Smf78Amg.smf78sid==Smf78Lcu.smf78sid, Smf78Amg.datetime==Smf78Lcu.datetime, Smf78Amg.smf78ist==Smf78Lcu.smf78ist, Smf78Amg.smf78iet==Smf78Lcu.smf78iet, Smf78Amg.r783amgs==Smf78Lcu.r783amgs)', )
    smf78_chaps: so.Mapped[List['Smf78Chap']] = so.relationship(back_populates='smf78_amg', viewonly=True)


class Smf78Lcu(ReprMixin, Base78, Smf78ds, Smf78hpav):
    """The Smf78Lcu class stores the Smf78Lcu section in the smf78_lcu table."""

    __tablename__ = "smf78_lcu"
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
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf78sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf78ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF Monitor I measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf78iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval was synchronized with SMF).")
    r783id2: so.Mapped[str] = so.mapped_column(sa.String(6), doc="Logical control unit identifier.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf78sid, datetime, smf78ist, smf78iet, r783id2),
        sa.ForeignKeyConstraint(
            ['csc', 'smf78sid', 'datetime', 'smf78ist', 'smf78iet'],
            ['smf78_ioq.csc', 'smf78_ioq.smf78sid', 'smf78_ioq.datetime', 'smf78_ioq.smf78ist', 'smf78_ioq.smf78iet']),
    )

    smf78_ioq: so.Mapped['Smf78Ioq'] = so.relationship(back_populates='smf78_lcus', viewonly=True)
    smf78_amg: so.Mapped['Smf78Amg'] = so.relationship(back_populates='smf78_lcus', viewonly=True,
                                                       foreign_keys='Smf78Amg.csc, Smf78Amg.smf78sid, Smf78Amg.datetime, Smf78Amg.smf78ist, Smf78Amg.smf78iet, Smf78Amg.r783amgs',
                                                       primaryjoin='and_(Smf78Lcu.csc==Smf78Amg.csc, Smf78Lcu.smf78sid==Smf78Amg.smf78sid, Smf78Lcu.datetime==Smf78Amg.datetime, Smf78Lcu.smf78ist==Smf78Amg.smf78ist, Smf78Lcu.smf78iet==Smf78Amg.smf78iet, Smf78Lcu.r783amgs==Smf78Amg.r783amgs)', )
    smf78_chas: so.Mapped[List['Smf78Cha']] = so.relationship(back_populates='smf78_lcu', viewonly=True)


class Smf78Chap(ReprMixin, Base78, Smf78cpd):
    """The Smf78Chap class stores the Smf78Chap section in the smf78_chap table."""

    __tablename__ = "smf78_chap"
    r783mcmn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Minimum number of DCM managed channels used.")
    r783mcmx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Maximum number of DCM managed channels used.")
    r783mcdf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Defined number of DCM managed channels.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf78sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf78ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF Monitor I measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf78iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval was synchronized with SMF).")
    r783amgs: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="The alias management group number assigned by z/OS for this LCU on this system. This number is valid, if the LCU is assigned to a DASD subsystem that supports alias management groups and bit 7 of R783DST is set.")
    r783cpid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Channel path identifier.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf78sid, datetime, smf78ist, smf78iet, r783amgs, r783cpid),
        sa.ForeignKeyConstraint(
            ['csc', 'smf78sid', 'datetime', 'smf78ist', 'smf78iet', 'r783amgs'],
            ['smf78_amg.csc', 'smf78_amg.smf78sid', 'smf78_amg.datetime', 'smf78_amg.smf78ist', 'smf78_amg.smf78iet',
             'smf78_amg.r783amgs']),
    )

    smf78_amg: so.Mapped['Smf78Amg'] = so.relationship(back_populates='smf78_chaps', viewonly=True)
    smf78_chas: so.Mapped[List['Smf78Cha']] = so.relationship(back_populates='smf78_chap', viewonly=True,
                                                              foreign_keys=[csc, smf78sid, datetime, smf78ist, smf78iet,
                                                                            r783amgs, r783cpid],
                                                              primaryjoin='and_(Smf78Chap.csc==Smf78Cha.csc, Smf78Chap.smf78sid==Smf78Cha.smf78sid, Smf78Chap.datetime==Smf78Cha.datetime, Smf78Chap.smf78ist==Smf78Cha.smf78ist, Smf78Chap.smf78iet==Smf78Cha.smf78iet, Smf78Chap.r783amgs==Smf78Cha.r783amgs, Smf78Chap.r783cpid==Smf78Cha.r783cpid)', )


class Smf78Cha(ReprMixin, Base78, Smf78cpd):
    """The Smf78Cha class stores the Smf78Cha section in the smf78_cha table."""

    __tablename__ = "smf78_cha"
    r783amgs: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="The alias management group number assigned by z/OS for this LCU on this system. This number is valid, if the LCU is assigned to a DASD subsystem that supports alias management groups and bit 7 of R783DST is set.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf78sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf78ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF Monitor I measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf78iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval was synchronized with SMF).")
    r783id1: so.Mapped[str] = so.mapped_column(sa.String(6), doc="Logical control unit identifier.")
    r783cpid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Channel path identifier.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf78sid, datetime, smf78ist, smf78iet, r783id1, r783cpid),
        sa.ForeignKeyConstraint(
            ['csc', 'smf78sid', 'datetime', 'smf78ist', 'smf78iet', 'r783id1'],
            ['smf78_lcu.csc', 'smf78_lcu.smf78sid', 'smf78_lcu.datetime', 'smf78_lcu.smf78ist', 'smf78_lcu.smf78iet',
             'smf78_lcu.r783id2']),
    )

    smf78_amg: so.Mapped['Smf78Amg'] = so.relationship(back_populates='smf78_chas', viewonly=True,
                                                       foreign_keys='Smf78Amg.csc, Smf78Amg.smf78sid, Smf78Amg.datetime, Smf78Amg.smf78ist, Smf78Amg.smf78iet, Smf78Amg.r783amgs',
                                                       primaryjoin='and_(Smf78Cha.csc==Smf78Amg.csc, Smf78Cha.smf78sid==Smf78Amg.smf78sid, Smf78Cha.datetime==Smf78Amg.datetime, Smf78Cha.smf78ist==Smf78Amg.smf78ist, Smf78Cha.smf78iet==Smf78Amg.smf78iet, Smf78Cha.r783amgs==Smf78Amg.r783amgs)', )
    smf78_lcu: so.Mapped['Smf78Lcu'] = so.relationship(back_populates='smf78_chas', viewonly=True)
    smf78_chap: so.Mapped['Smf78Chap'] = so.relationship(back_populates='smf78_chas', viewonly=True,
                                                         foreign_keys='Smf78Chap.csc, Smf78Chap.smf78sid, Smf78Chap.datetime, Smf78Chap.smf78ist, Smf78Chap.smf78iet, Smf78Chap.r783amgs, Smf78Chap.r783cpid',
                                                         primaryjoin='and_(Smf78Cha.csc==Smf78Chap.csc, Smf78Cha.smf78sid==Smf78Chap.smf78sid, Smf78Cha.datetime==Smf78Chap.datetime, Smf78Cha.smf78ist==Smf78Chap.smf78ist, Smf78Cha.smf78iet==Smf78Chap.smf78iet, Smf78Cha.r783amgs==Smf78Chap.r783amgs, Smf78Cha.r783cpid==Smf78Chap.r783cpid)', )
