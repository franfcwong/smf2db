import datetime as dt
from typing import List, Optional

import sqlalchemy as sa
import sqlalchemy.orm as so

from .smf70_base import ReprMixin, Base70, Smf70pro, Smf70ctl, Smf70aid, Smf70cpu, Smf70bct, Smf70bpd, Smf70trg, \
    Smf70ccf, Smf70typ3, Smf70typ4, Smf70typ5, Smf70wc


class Smf70Pro(ReprMixin, Base70, Smf70pro):
    """The Smf70Pro class stores the Smf70Pro section in the smf70_pro table."""

    __tablename__ = "smf70_pro"
    smf70ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf70iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval was synchronized with SMF).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf_type: so.Mapped[str] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf70sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(datetime, smf70ist, smf70iet, smf_type, csc, smf70sid),
    )

    smf70_ctl: so.Mapped["Smf70Ctl"] = so.relationship(back_populates="smf70_pro", viewonly=True)
    smf70_ccf: so.Mapped["Smf70Ccf"] = so.relationship(back_populates="smf70_pro", viewonly=True)
    smf70_typ3s: so.Mapped[List['Smf70Typ3']] = so.relationship(back_populates='smf70_pro', viewonly=True)
    smf70_typ4s: so.Mapped[List['Smf70Typ4']] = so.relationship(back_populates='smf70_pro', viewonly=True)
    smf70_typ5s: so.Mapped[List['Smf70Typ5']] = so.relationship(back_populates='smf70_pro', viewonly=True)


class Smf70Ctl(ReprMixin, Base70, Smf70ctl):
    """The Smf70Ctl class stores the Smf70Ctl section in the smf70_ctl table."""

    __tablename__ = "smf70_ctl"
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf70sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf70ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf70iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval was synchronized with SMF).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf70sid, datetime, smf70ist, smf70iet),
        sa.ForeignKeyConstraint(
            ['datetime', 'smf70ist', 'smf70iet', 'smf_type', 'csc', 'smf70sid'],
            ['smf70_pro.datetime', 'smf70_pro.smf70ist', 'smf70_pro.smf70iet', 'smf70_pro.smf_type', 'smf70_pro.csc',
             'smf70_pro.smf70sid']),
    )

    smf70_pro: so.Mapped["Smf70Pro"] = so.relationship(back_populates="smf70_ctl", viewonly=True)
    smf70_aid: so.Mapped["Smf70Aid"] = so.relationship(back_populates="smf70_ctl", viewonly=True)
    smf70_cpus: so.Mapped[List['Smf70Cpu']] = so.relationship(back_populates='smf70_ctl', viewonly=True)
    smf70_bcts: so.Mapped[List['Smf70Bct']] = so.relationship(back_populates='smf70_ctl', viewonly=True)
    smf70_trgs: so.Mapped[List['Smf70Trg']] = so.relationship(back_populates='smf70_ctl', viewonly=True)
    smf70_wcs: so.Mapped[List['Smf70Wc']] = so.relationship(back_populates='smf70_ctl', viewonly=True)


class Smf70Aid(ReprMixin, Base70, Smf70aid):
    """The Smf70Aid class stores the Smf70Aid section in the smf70_aid table."""

    __tablename__ = "smf70_aid"
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf70sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf70ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf70iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval was synchronized with SMF).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf70sid, datetime, smf70ist, smf70iet),
        sa.ForeignKeyConstraint(
            ['csc', 'smf70sid', 'datetime', 'smf70ist', 'smf70iet'],
            ['smf70_ctl.csc', 'smf70_ctl.smf70sid', 'smf70_ctl.datetime', 'smf70_ctl.smf70ist', 'smf70_ctl.smf70iet']),
    )

    smf70_ctl: so.Mapped["Smf70Ctl"] = so.relationship(back_populates="smf70_aid", viewonly=True)


class Smf70Cpu(ReprMixin, Base70, Smf70cpu):
    """The Smf70Cpu class stores the Smf70Cpu section in the smf70_cpu table."""

    __tablename__ = "smf70_cpu"
    smf70cid: so.Mapped[int] = so.mapped_column(sa.Integer, doc="CPU identification")
    smf70_cpu_skip: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                doc="The CPU data sections for this core are grouped together in the record. To get to the first CPU data section associated with this logical core, skip over the number of CPU data sections specified by this field, starting at the first CPU data section in the record.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf70sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf70ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf70iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval was synchronized with SMF).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf70sid, datetime, smf70ist, smf70iet, smf70cid),
        sa.ForeignKeyConstraint(
            ['csc', 'smf70sid', 'datetime', 'smf70ist', 'smf70iet'],
            ['smf70_ctl.csc', 'smf70_ctl.smf70sid', 'smf70_ctl.datetime', 'smf70_ctl.smf70ist', 'smf70_ctl.smf70iet']),
    )

    smf70_ctl: so.Mapped['Smf70Ctl'] = so.relationship(back_populates='smf70_cpus', viewonly=True)


class Smf70Typ3(ReprMixin, Base70, Smf70typ3):
    """The Smf70Typ3 class stores the Smf70Typ3 section in the smf70_typ3 table."""

    __tablename__ = "smf70_typ3"
    r7023ax: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Crypto processor index.")
    r7023scope: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                  doc="Specifies the scope of the cryptographic CCA coprocessor data section. Value Meaning 0 Data with CPC scope 1 Data with System scope")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf70sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf70ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf70iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval was synchronized with SMF).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf70sid, datetime, smf70ist, smf70iet, r7023ax, r7023scope),
        sa.ForeignKeyConstraint(
            ['datetime', 'smf70ist', 'smf70iet', 'smf_type', 'csc', 'smf70sid'],
            ['smf70_pro.datetime', 'smf70_pro.smf70ist', 'smf70_pro.smf70iet', 'smf70_pro.smf_type', 'smf70_pro.csc',
             'smf70_pro.smf70sid']),
    )

    smf70_pro: so.Mapped['Smf70Pro'] = so.relationship(back_populates='smf70_typ3s', viewonly=True)


class Smf70Typ4(ReprMixin, Base70, Smf70typ4):
    """The Smf70Typ4 class stores the Smf70Typ4 section in the smf70_typ4 table."""

    __tablename__ = "smf70_typ4"
    r7024ax: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Crypto processor index.")
    r7024scope: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                  doc="Specifies the scope of the cryptographic accelerator data section. Value Meaning 0 Data with CPC scope 1")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf70sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf70ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf70iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval was synchronized with SMF).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf70sid, datetime, smf70ist, smf70iet, r7024ax, r7024scope),
        sa.ForeignKeyConstraint(
            ['datetime', 'smf70ist', 'smf70iet', 'smf_type', 'csc', 'smf70sid'],
            ['smf70_pro.datetime', 'smf70_pro.smf70ist', 'smf70_pro.smf70iet', 'smf70_pro.smf_type', 'smf70_pro.csc',
             'smf70_pro.smf70sid']),
    )

    smf70_pro: so.Mapped['Smf70Pro'] = so.relationship(back_populates='smf70_typ4s', viewonly=True)


class Smf70Typ5(ReprMixin, Base70, Smf70typ5):
    """The Smf70Typ5 class stores the Smf70Typ5 section in the smf70_typ5 table."""

    __tablename__ = "smf70_typ5"
    r7025ax: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Crypto processor index.")
    r7025scope: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                  doc="Specifies the scope of the cryptographic PKCS11 coprocessor data section. Value Meaning 0 Data with CPC scope 1 Data with System scope")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf70sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf70ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf70iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval was synchronized with SMF).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf70sid, datetime, smf70ist, smf70iet, r7025ax, r7025scope),
        sa.ForeignKeyConstraint(
            ['datetime', 'smf70ist', 'smf70iet', 'smf_type', 'csc', 'smf70sid'],
            ['smf70_pro.datetime', 'smf70_pro.smf70ist', 'smf70_pro.smf70iet', 'smf70_pro.smf_type', 'smf70_pro.csc',
             'smf70_pro.smf70sid']),
    )

    smf70_pro: so.Mapped['Smf70Pro'] = so.relationship(back_populates='smf70_typ5s', viewonly=True)


class Smf70Ccf(ReprMixin, Base70, Smf70ccf):
    """The Smf70Ccf class stores the Smf70Ccf section in the smf70_ccf table."""

    __tablename__ = "smf70_ccf"
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf70sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf70ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf70iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval was synchronized with SMF).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf70sid, datetime, smf70ist, smf70iet),
        sa.ForeignKeyConstraint(
            ['datetime', 'smf70ist', 'smf70iet', 'smf_type', 'csc', 'smf70sid'],
            ['smf70_pro.datetime', 'smf70_pro.smf70ist', 'smf70_pro.smf70iet', 'smf70_pro.smf_type', 'smf70_pro.csc',
             'smf70_pro.smf70sid']),
    )

    smf70_pro: so.Mapped["Smf70Pro"] = so.relationship(back_populates="smf70_ccf", viewonly=True)


class Smf70Bpd(ReprMixin, Base70, Smf70bpd):
    """The Smf70Bpd class stores the Smf70Bpd section in the smf70_bpd table."""

    __tablename__ = "smf70_bpd"
    smf70vpa: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Logical processor address.")
    sysplex_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                              doc="the sysplex name which this partition belongs to.")
    system_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="the partition system name.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    lpar_system_name: so.Mapped[str] = so.mapped_column(sa.String(17),
                                                        doc="combining lpar long name with lpar short name.")
    lpar_number: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                   doc="PR/SM partition number of the partition that wrote this record.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf70ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf70iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval was synchronized with SMF).")
    smf70sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, lpar_system_name, lpar_number, datetime, smf70ist, smf70iet, smf70sid, smf70vpa),
        sa.ForeignKeyConstraint(
            ['csc', 'lpar_system_name', 'lpar_number', 'datetime', 'smf70ist', 'smf70iet', 'smf70sid', 'smf70cix'],
            ['smf70_bct_cpu.csc', 'smf70_bct_cpu.lpar_system_name', 'smf70_bct_cpu.lpar_number',
             'smf70_bct_cpu.datetime', 'smf70_bct_cpu.smf70ist', 'smf70_bct_cpu.smf70iet', 'smf70_bct_cpu.smf70sid',
             'smf70_bct_cpu.smf70cix']),
    )

    smf70_bct_cpu: so.Mapped['Smf70BctCpu'] = so.relationship(back_populates='smf70_bpds', viewonly=True)


class Smf70Bct(ReprMixin, Base70, Smf70bct):
    """The Smf70Bct class stores the Smf70Bct section in the smf70_bct table."""

    __tablename__ = "smf70_bct"
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    lpar_system_name: so.Mapped[str] = so.mapped_column(sa.String(17),
                                                        doc="combining lpar long name with lpar short name.")
    lpar_number: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                   doc="PR/SM partition number of the partition that wrote this record.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf70ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf70iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval was synchronized with SMF).")
    smf70sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, lpar_system_name, lpar_number, datetime, smf70ist, smf70iet, smf70sid),
        sa.ForeignKeyConstraint(
            ['csc', 'smf70sid', 'datetime', 'smf70ist', 'smf70iet'],
            ['smf70_ctl.csc', 'smf70_ctl.smf70sid', 'smf70_ctl.datetime', 'smf70_ctl.smf70ist', 'smf70_ctl.smf70iet']),
    )

    smf70_ctl: so.Mapped['Smf70Ctl'] = so.relationship(back_populates='smf70_bcts', viewonly=True)
    smf70_bct_cpus: so.Mapped[List['Smf70BctCpu']] = so.relationship(back_populates='smf70_bct', viewonly=True)


class Smf70Trg(ReprMixin, Base70, Smf70trg):
    """The Smf70Trg class stores the Smf70Trg section in the smf70_trg table."""

    __tablename__ = "smf70_trg"
    smf70_trg_name: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Tenant resource group name.")
    smf70_trg_tntid: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Tenant identifier.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf70sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf70ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf70iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval was synchronized with SMF).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf70sid, datetime, smf70ist, smf70iet, smf70_trg_name, smf70_trg_tntid),
        sa.ForeignKeyConstraint(
            ['csc', 'smf70sid', 'datetime', 'smf70ist', 'smf70iet'],
            ['smf70_ctl.csc', 'smf70_ctl.smf70sid', 'smf70_ctl.datetime', 'smf70_ctl.smf70ist', 'smf70_ctl.smf70iet']),
    )

    smf70_ctl: so.Mapped['Smf70Ctl'] = so.relationship(back_populates='smf70_trgs', viewonly=True)


class Smf70Wc(ReprMixin, Base70, Smf70wc):
    """The Smf70Wc class stores the Smf70Wc section in the smf70_wc table."""

    __tablename__ = "smf70_wc"
    smf70wc_cpu_type: so.Mapped[int] = so.mapped_column(sa.Integer, doc="CPU type as defined by SMF70TYP.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf70sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf70ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf70iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval was synchronized with SMF).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf70sid, datetime, smf70ist, smf70iet, smf70wc_cpu_type),
        sa.ForeignKeyConstraint(
            ['csc', 'smf70sid', 'datetime', 'smf70ist', 'smf70iet'],
            ['smf70_ctl.csc', 'smf70_ctl.smf70sid', 'smf70_ctl.datetime', 'smf70_ctl.smf70ist', 'smf70_ctl.smf70iet']),
    )

    smf70_ctl: so.Mapped['Smf70Ctl'] = so.relationship(back_populates='smf70_wcs', viewonly=True)


class Smf70BctCpu(ReprMixin, Base70, Smf70bpd):
    """The Smf70BctCpu class stores the Smf70BctCpu section in the smf70_bct_cpu table."""

    __tablename__ = "smf70_bct_cpu"
    smf70cix: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="EBCDIC name corresponding to the CPU type of the logical processor in CPU-identification name section.")
    wait_completion_status: so.Mapped[Optional[str]] = so.mapped_column(sa.String(3),
                                                                        doc="the wait completion is enabled of this processor.")
    wgt: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5),
                                                     doc="the processor weight of this kind of processor.")
    initial_cap_indicator: so.Mapped[Optional[str]] = so.mapped_column(sa.String(1),
                                                                       doc="the initial cap indicator of this processor.")
    cap_absolute_indicator: so.Mapped[Optional[str]] = so.mapped_column(sa.String(1),
                                                                        doc="the cap absolute indicator of this processor.")
    cap_absolute_group_indicator: so.Mapped[Optional[str]] = so.mapped_column(sa.String(1),
                                                                              doc="the cap absolute group indicator of this processor.")
    logical_processor_effective: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                               doc="the effective logical processor effective time of this processor.")
    logical_processor_total: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                           doc="the total logical processor time of this processor.")
    physical_processor_effective: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                doc="the effective physical processor effective time of this processor.")
    physical_processor_total: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                            doc="the total physical processor time of this processor.")
    actual_consumed_msu: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                       doc="the actual consumed MSU of this processor.")
    effective_consumed_msu: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                          doc="the effective consumed MSU of this processor.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    lpar_system_name: so.Mapped[str] = so.mapped_column(sa.String(17),
                                                        doc="combining lpar long name with lpar short name.")
    lpar_number: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                   doc="PR/SM partition number of the partition that wrote this record.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf70ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf70iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval was synchronized with SMF).")
    smf70sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, lpar_system_name, lpar_number, datetime, smf70ist, smf70iet, smf70sid, smf70cix),
        sa.ForeignKeyConstraint(
            ['csc', 'lpar_system_name', 'lpar_number', 'datetime', 'smf70ist', 'smf70iet', 'smf70sid'],
            ['smf70_bct.csc', 'smf70_bct.lpar_system_name', 'smf70_bct.lpar_number', 'smf70_bct.datetime',
             'smf70_bct.smf70ist', 'smf70_bct.smf70iet', 'smf70_bct.smf70sid']),
    )

    smf70_bct: so.Mapped['Smf70Bct'] = so.relationship(back_populates='smf70_bct_cpus', viewonly=True)
    smf70_bpds: so.Mapped[List['Smf70Bpd']] = so.relationship(back_populates='smf70_bct_cpu', viewonly=True)
