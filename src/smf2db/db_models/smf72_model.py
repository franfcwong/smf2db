import datetime as dt
from typing import List, Optional

import sqlalchemy as sa
import sqlalchemy.orm as so

from .smf72_base import ReprMixin, Base72, Smf72pro, Smf72policy, Smf72wms, Smf72scs, Smf72rts, Smf72wrs, Smf72rgs, \
    Smf72data, Smf72cmss, Smf72lotd, Smf72clod, Smf72clrd, Smf72lasc, Smf72ense, Smf72qsad, Smf72sctl


class Smf72Pro(ReprMixin, Base72, Smf72pro):
    """The Smf72Pro class stores the Smf72Pro section in the smf72_pro table."""

    __tablename__ = "smf72_pro"
    smf72ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf72iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf_type: so.Mapped[str] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(datetime, smf72ist, smf72iet, smf_type, smf72xnm, smf72sid),
    )

    smf72_sctl: so.Mapped["Smf72Sctl"] = so.relationship(back_populates="smf72_pro", viewonly=True)
    smf72_policy: so.Mapped['Smf72Policy'] = so.relationship(back_populates='smf72_pros', viewonly=True,
                                                             foreign_keys=[datetime, smf72ist, smf72iet, smf_type,
                                                                           smf72xnm],
                                                             primaryjoin='and_(Smf72Pro.datetime==Smf72Policy.datetime, Smf72Pro.smf72ist==Smf72Policy.smf72ist, Smf72Pro.smf72iet==Smf72Policy.smf72iet, Smf72Pro.smf_type==Smf72Policy.smf_type, Smf72Pro.smf72xnm==Smf72Policy.smf72xnm)', )
    smf72_scss: so.Mapped[List['Smf72Scs']] = so.relationship(back_populates='smf72_pro', viewonly=True)
    smf72_datas: so.Mapped[List['Smf72Data']] = so.relationship(back_populates='smf72_pro', viewonly=True)


class Smf72Wrs(ReprMixin, Base72, Smf72wrs):
    """The Smf72Wrs class stores the Smf72Wrs section in the smf72_wrs table."""

    __tablename__ = "smf72_wrs"
    r723rtyp: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="Subsystem type, as used in the classification rules specified in the WLM administrative application. The subsystem's documentation should explain the meaning that the product attributes to the various states.")
    r723rdnx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Index into resource delay type names table.")
    r723rdnn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of entries in resource delay type names table.")
    phase: so.Mapped[str] = so.mapped_column(sa.String(3),
                                             doc="states sampled in the begin_to_end phase of a transaction or in the execution phase of a transaction.")
    r723rexe: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r723rflg (Bit 1) representing states sampled in the execution phase of a transaction.")
    r723rdbe: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r723rflg (Bit 0) representing states sampled in the begin_to_end phase of a transaction.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf72ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf72iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")
    r723mnsp: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Policy name.")
    r723mwnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Workload name.")
    r723mcnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service/Report class name.")
    r723cper: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service or report class period number.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, datetime, smf72ist, smf72iet, r723mnsp, r723mwnm, r723mcnm, r723cper,
                                smf72sid, r723rtyp, phase),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'datetime', 'smf72ist', 'smf72iet', 'r723mnsp', 'r723mwnm', 'r723mcnm', 'r723cper',
             'smf72sid'],
            ['smf72_scs.smf72xnm', 'smf72_scs.datetime', 'smf72_scs.smf72ist', 'smf72_scs.smf72iet',
             'smf72_scs.r723mnsp', 'smf72_scs.r723mwnm', 'smf72_scs.r723mcnm', 'smf72_scs.r723cper',
             'smf72_scs.smf72sid']),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'datetime', 'smf72ist', 'smf72iet', 'r723mnsp', 'r723mwnm', 'r723mcnm', 'r723cper', 'r723rtyp',
             'phase'],
            ['smf72_wrsx.smf72xnm', 'smf72_wrsx.datetime', 'smf72_wrsx.smf72ist', 'smf72_wrsx.smf72iet',
             'smf72_wrsx.r723mnsp', 'smf72_wrsx.r723mwnm', 'smf72_wrsx.r723mcnm', 'smf72_wrsx.r723cper',
             'smf72_wrsx.r723rtyp', 'smf72_wrsx.phase']),
    )

    smf72_scs: so.Mapped['Smf72Scs'] = so.relationship(back_populates='smf72_wrss', viewonly=True)
    smf72_wrsx: so.Mapped['Smf72Wrsx'] = so.relationship(back_populates='smf72_wrss', viewonly=True)
    smf72_dnss: so.Mapped[List['Smf72Dns']] = so.relationship(back_populates='smf72_wrs', viewonly=True)


class Smf72Scs(ReprMixin, Base72, Smf72scs, Smf72wrs):
    """The Smf72Scs class stores the Smf72Scs section in the smf72_scs table."""

    __tablename__ = "smf72_scs"
    r723crtx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Index into the response time distribution count table in the Response Time Distribution data section. These buckets exist only for periods with a response time or execution velocity goal.")
    r723cwmx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Index into the work/resource manager states area.")
    r723cwmn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of entries in the work/resource manager states area associated with this period (R723CWMX points to the first entry).")
    r723cper: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service or report class period number.")
    r723cimp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Importance of the goal to be achieved for this period (1=highest, 5=lowest). The value is zero for a discretionary or system goal.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    r723rtyp: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4),
                                                          doc="Subsystem type, as used in the classification rules specified in the WLM administrative application. The subsystem's documentation should explain the meaning that the product attributes to the various states.")
    r723madj: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Adjustment factor for CPU rate.")
    r723nffi: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Normalization factor for zAAP. Multiply zAAP service times or service units with this value and divide by 256 to calculate the CP equivalent value.")
    r723nffs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Normalization factor for zIIP. Multiply zIIP service units with this value and divide by 256 to calculate the CP equivalent")
    r723mcpu: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="CPU service coefficient * 10,000.")
    r723msrb: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="SRB service coefficient * 10,000")
    r723cpa_scaling_factor: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                        doc="Scaling factor for R723CPA_actual.")
    r723cpa_actual: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                doc="Physical CPU adjustment factor based on Model Capacity Rating.")
    r723mcf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                         doc="Multithreading maximum capacity numerator for general purpose processors. Divide this value by 1024 to get the MT maximum capacity factor for all general purpose processors that were configured ONLINE for the complete interval.")
    r723mcfs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Multithreading maximum capacity numerator for zIIP. Divide this value by 1024 to get the multithreading maximum capacity factor for all zIIPs that were configured ONLINE for the complete interval. A zero value is reported if no zIIP is currently installed.")
    r723mcfi: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Multithreading maximum capacity numerator for zAAP. Divide this value by 1024 to get the multithreading maximum capacity factor for all zAAPs that were configured ONLINE for the complete interval. A zero value is reported if no zAAP is currently installed.")
    smf72int: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Duration of the RMF measurement interval, in the form mmsstttF where mm is the minutes, ss is the seconds, ttt is the milliseconds, and F is the sign. The end of the measurement interval is the sum of the recorded start time (and this field.)")
    smf_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    is_report_class: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                 doc="r723mscf (Bit 0) showing the indicator for a report class.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf72ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf72iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")
    r723mnsp: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Policy name.")
    r723mwnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Workload name.")
    r723mcnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service/Report class name.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, datetime, smf72ist, smf72iet, r723mnsp, r723mwnm, r723mcnm, r723cper,
                                smf72sid),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'datetime', 'smf72ist', 'smf72iet', 'r723mnsp', 'r723mwnm', 'r723mcnm', 'r723cper'],
            ['smf72_wms.smf72xnm', 'smf72_wms.datetime', 'smf72_wms.smf72ist', 'smf72_wms.smf72iet',
             'smf72_wms.r723mnsp', 'smf72_wms.r723mwnm', 'smf72_wms.r723mcnm', 'smf72_wms.r723cper']),
        sa.ForeignKeyConstraint(
            ['datetime', 'smf72ist', 'smf72iet', 'smf_type', 'smf72xnm', 'smf72sid'],
            ['smf72_pro.datetime', 'smf72_pro.smf72ist', 'smf72_pro.smf72iet', 'smf72_pro.smf_type',
             'smf72_pro.smf72xnm', 'smf72_pro.smf72sid']),
    )

    smf72_rts: so.Mapped["Smf72Rts"] = so.relationship(back_populates="smf72_scs", viewonly=True)
    smf72_wms: so.Mapped['Smf72Wms'] = so.relationship(back_populates='smf72_scss', viewonly=True)
    smf72_pro: so.Mapped['Smf72Pro'] = so.relationship(back_populates='smf72_scss', viewonly=True)
    smf72_wrss: so.Mapped[List['Smf72Wrs']] = so.relationship(back_populates='smf72_scs', viewonly=True)


class Smf72Policy(ReprMixin, Base72, Smf72policy):
    """The Smf72Policy class stores the Smf72Policy section in the smf72_policy table."""

    __tablename__ = "smf72_policy"
    smf_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf72ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf72iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")
    r723mnsp: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Policy name.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, datetime, smf72ist, smf72iet, r723mnsp),
    )

    smf72_workloads: so.Mapped[List['Smf72Workload']] = so.relationship(back_populates='smf72_policy', viewonly=True)
    smf72_wmss: so.Mapped[List['Smf72Wms']] = so.relationship(back_populates='smf72_policy', viewonly=True)
    smf72_rgss: so.Mapped[List['Smf72Rgs']] = so.relationship(back_populates='smf72_policy', viewonly=True)
    smf72_pros: so.Mapped[List['Smf72Pro']] = so.relationship(back_populates='smf72_policy', viewonly=True,
                                                              foreign_keys='Smf72Pro.datetime, Smf72Pro.smf72ist, Smf72Pro.smf72iet, Smf72Pro.smf_type, Smf72Pro.smf72xnm',
                                                              primaryjoin='and_(Smf72Policy.datetime==Smf72Pro.datetime, Smf72Policy.smf72ist==Smf72Pro.smf72ist, Smf72Policy.smf72iet==Smf72Pro.smf72iet, Smf72Policy.smf_type==Smf72Pro.smf_type, Smf72Policy.smf72xnm==Smf72Pro.smf72xnm)', )


class Smf72Workload(ReprMixin, Base72):
    """The Smf72Workload class stores the Smf72Workload section in the smf72_workload table."""

    __tablename__ = "smf72_workload"
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    r723mwde: so.Mapped[Optional[str]] = so.mapped_column(sa.String(32), doc="Workload description.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf72ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf72iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")
    r723mnsp: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Policy name.")
    r723mwnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Workload name.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, datetime, smf72ist, smf72iet, r723mnsp, r723mwnm),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'datetime', 'smf72ist', 'smf72iet', 'r723mnsp'],
            ['smf72_policy.smf72xnm', 'smf72_policy.datetime', 'smf72_policy.smf72ist', 'smf72_policy.smf72iet',
             'smf72_policy.r723mnsp']),
    )

    smf72_policy: so.Mapped['Smf72Policy'] = so.relationship(back_populates='smf72_workloads', viewonly=True)
    smf72_wmss: so.Mapped[List['Smf72Wms']] = so.relationship(back_populates='smf72_workload', viewonly=True)


class Smf72Rts(ReprMixin, Base72, Smf72rts):
    """The Smf72Rts class stores the Smf72Rts section in the smf72_rts table."""

    __tablename__ = "smf72_rts"
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf72ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf72iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")
    r723mnsp: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Policy name.")
    r723mwnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Workload name.")
    r723mcnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service/Report class name.")
    r723cper: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service or report class period number.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, datetime, smf72ist, smf72iet, r723mnsp, r723mwnm, r723mcnm, r723cper,
                                smf72sid),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'datetime', 'smf72ist', 'smf72iet', 'r723mnsp', 'r723mwnm', 'r723mcnm', 'r723cper',
             'smf72sid'],
            ['smf72_scs.smf72xnm', 'smf72_scs.datetime', 'smf72_scs.smf72ist', 'smf72_scs.smf72iet',
             'smf72_scs.r723mnsp', 'smf72_scs.r723mwnm', 'smf72_scs.r723mcnm', 'smf72_scs.r723cper',
             'smf72_scs.smf72sid']),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'datetime', 'smf72ist', 'smf72iet', 'r723mnsp', 'r723mwnm', 'r723mcnm', 'r723cper'],
            ['smf72_wms.smf72xnm', 'smf72_wms.datetime', 'smf72_wms.smf72ist', 'smf72_wms.smf72iet',
             'smf72_wms.r723mnsp', 'smf72_wms.r723mwnm', 'smf72_wms.r723mcnm', 'smf72_wms.r723cper']),
    )

    smf72_scs: so.Mapped["Smf72Scs"] = so.relationship(back_populates="smf72_rts", viewonly=True)
    smf72_wms: so.Mapped['Smf72Wms'] = so.relationship(back_populates='smf72_rtss', viewonly=True)


class Smf72Sctl(ReprMixin, Base72, Smf72sctl):
    """The Smf72Sctl class stores the Smf72Sctl section in the smf72_sctl table."""

    __tablename__ = "smf72_sctl"
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf72ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf72iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, smf72sid, datetime, smf72ist, smf72iet),
        sa.ForeignKeyConstraint(
            ['datetime', 'smf72ist', 'smf72iet', 'smf_type', 'smf72xnm', 'smf72sid'],
            ['smf72_pro.datetime', 'smf72_pro.smf72ist', 'smf72_pro.smf72iet', 'smf72_pro.smf_type',
             'smf72_pro.smf72xnm', 'smf72_pro.smf72sid']),
    )

    smf72_pro: so.Mapped["Smf72Pro"] = so.relationship(back_populates="smf72_sctl", viewonly=True)
    smf72_cmsss: so.Mapped[List['Smf72Cmss']] = so.relationship(back_populates='smf72_sctl', viewonly=True)
    smf72_cedss: so.Mapped[List['Smf72Ceds']] = so.relationship(back_populates='smf72_sctl', viewonly=True)
    smf72_class: so.Mapped[List['Smf72Clas']] = so.relationship(back_populates='smf72_sctl', viewonly=True)
    smf72_csmss: so.Mapped[List['Smf72Csms']] = so.relationship(back_populates='smf72_sctl', viewonly=True)
    smf72_lotds: so.Mapped[List['Smf72Lotd']] = so.relationship(back_populates='smf72_sctl', viewonly=True)
    smf72_clods: so.Mapped[List['Smf72Clod']] = so.relationship(back_populates='smf72_sctl', viewonly=True)
    smf72_clrds: so.Mapped[List['Smf72Clrd']] = so.relationship(back_populates='smf72_sctl', viewonly=True)
    smf72_lascs: so.Mapped[List['Smf72Lasc']] = so.relationship(back_populates='smf72_sctl', viewonly=True)
    smf72_lares: so.Mapped[List['Smf72Lare']] = so.relationship(back_populates='smf72_sctl', viewonly=True)
    smf72_enses: so.Mapped[List['Smf72Ense']] = so.relationship(back_populates='smf72_sctl', viewonly=True)
    smf72_ensys: so.Mapped[List['Smf72Ensy']] = so.relationship(back_populates='smf72_sctl', viewonly=True)
    smf72_ensss: so.Mapped[List['Smf72Enss']] = so.relationship(back_populates='smf72_sctl', viewonly=True)
    smf72_qsads: so.Mapped[List['Smf72Qsad']] = so.relationship(back_populates='smf72_sctl', viewonly=True)


class Smf72Wms(ReprMixin, Base72, Smf72wms, Smf72scs, Smf72rts, Smf72wrs):
    """The Smf72Wms class stores the Smf72Wms section in the smf72_wms table."""

    __tablename__ = "smf72_wms"
    r723mnsp: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Policy name.")
    r723mwnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Workload name.")
    r723mcnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service/Report class name.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    r723cimp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Importance of the goal to be achieved for this period (1=highest, 5=lowest). The value is zero for a discretionary or system goal.")
    r723ggnm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Resource group name.")
    r723rtyp: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4),
                                                          doc="Subsystem type, as used in the classification rules specified in the WLM administrative application. The subsystem's documentation should explain the meaning that the product attributes to the various states.")
    smf72int: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Duration of the RMF measurement interval, in the form mmsstttF where mm is the minutes, ss is the seconds, ttt is the milliseconds, and F is the sign. The end of the measurement interval is the sum of the recorded start time (and this field.)")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf72ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf72iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")
    r723cper: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service or report class period number.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, datetime, smf72ist, smf72iet, r723mnsp, r723mwnm, r723mcnm, r723cper),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'datetime', 'smf72ist', 'smf72iet', 'r723mnsp'],
            ['smf72_policy.smf72xnm', 'smf72_policy.datetime', 'smf72_policy.smf72ist', 'smf72_policy.smf72iet',
             'smf72_policy.r723mnsp']),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'datetime', 'smf72ist', 'smf72iet', 'r723mnsp', 'r723mwnm'],
            ['smf72_workload.smf72xnm', 'smf72_workload.datetime', 'smf72_workload.smf72ist', 'smf72_workload.smf72iet',
             'smf72_workload.r723mnsp', 'smf72_workload.r723mwnm']),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'datetime', 'smf72ist', 'smf72iet', 'r723mnsp', 'r723ggnm'],
            ['smf72_rgs.smf72xnm', 'smf72_rgs.datetime', 'smf72_rgs.smf72ist', 'smf72_rgs.smf72iet',
             'smf72_rgs.r723mnsp', 'smf72_rgs.r723ggnm']),
    )

    smf72_policy: so.Mapped['Smf72Policy'] = so.relationship(back_populates='smf72_wmss', viewonly=True)
    smf72_workload: so.Mapped['Smf72Workload'] = so.relationship(back_populates='smf72_wmss', viewonly=True)
    smf72_rgs: so.Mapped['Smf72Rgs'] = so.relationship(back_populates='smf72_wmss', viewonly=True)
    smf72_ssss: so.Mapped[List['Smf72Sss']] = so.relationship(back_populates='smf72_wms', viewonly=True)
    smf72_rtss: so.Mapped[List['Smf72Rts']] = so.relationship(back_populates='smf72_wms', viewonly=True)
    smf72_scss: so.Mapped[List['Smf72Scs']] = so.relationship(back_populates='smf72_wms', viewonly=True)
    smf72_wrsxs: so.Mapped[List['Smf72Wrsx']] = so.relationship(back_populates='smf72_wms', viewonly=True)


class Smf72Wrsx(ReprMixin, Base72, Smf72wrs):
    """The Smf72Wrsx class stores the Smf72Wrsx section in the smf72_wrsx table."""

    __tablename__ = "smf72_wrsx"
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    r723rexe: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r723rflg (Bit 1) representing states sampled in the execution phase of a transaction.")
    r723rdbe: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r723rflg (Bit 0) representing states sampled in the begin_to_end phase of a transaction.")
    phase: so.Mapped[str] = so.mapped_column(sa.String(3),
                                             doc="states sampled in the begin_to_end phase of a transaction or in the execution phase of a transaction.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf72ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf72iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")
    r723mnsp: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Policy name.")
    r723mwnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Workload name.")
    r723mcnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service/Report class name.")
    r723cper: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service or report class period number.")
    r723rtyp: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="Subsystem type, as used in the classification rules specified in the WLM administrative application. The subsystem's documentation should explain the meaning that the product attributes to the various states.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, datetime, smf72ist, smf72iet, r723mnsp, r723mwnm, r723mcnm, r723cper,
                                r723rtyp, phase),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'datetime', 'smf72ist', 'smf72iet', 'r723mnsp', 'r723mwnm', 'r723mcnm', 'r723cper'],
            ['smf72_wms.smf72xnm', 'smf72_wms.datetime', 'smf72_wms.smf72ist', 'smf72_wms.smf72iet',
             'smf72_wms.r723mnsp', 'smf72_wms.r723mwnm', 'smf72_wms.r723mcnm', 'smf72_wms.r723cper']),
    )

    smf72_wms: so.Mapped['Smf72Wms'] = so.relationship(back_populates='smf72_wrsxs', viewonly=True)
    smf72_dnsxs: so.Mapped[List['Smf72Dnsx']] = so.relationship(back_populates='smf72_wrsx', viewonly=True)
    smf72_wrss: so.Mapped[List['Smf72Wrs']] = so.relationship(back_populates='smf72_wrsx', viewonly=True)


class Smf72Dns(ReprMixin, Base72):
    """The Smf72Dns class stores the Smf72Dns section in the smf72_dns table."""

    __tablename__ = "smf72_dns"
    r723dnst: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="Subsystem type as used in the classification rules specified in the WLM administrative application.")
    r723dnde: so.Mapped[str] = so.mapped_column(sa.String(16), doc="Resource delay description.")
    r723rwnn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="number of the resource delay type. Values 1...15 are related to r723rw01...r723rw15 respectively.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf72ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf72iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")
    r723mnsp: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Policy name.")
    r723mwnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Workload name.")
    r723mcnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service/Report class name.")
    r723cper: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service or report class period number.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    r723rtyp: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="Subsystem type, as used in the classification rules specified in the WLM administrative application. The subsystem's documentation should explain the meaning that the product attributes to the various states.")
    phase: so.Mapped[str] = so.mapped_column(sa.String(3),
                                             doc="states sampled in the begin_to_end phase of a transaction or in the execution phase of a transaction.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, datetime, smf72ist, smf72iet, r723mnsp, r723mwnm, r723mcnm, r723cper,
                                smf72sid, r723rtyp, phase, r723dnst, r723dnde),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'datetime', 'smf72ist', 'smf72iet', 'r723mnsp', 'r723mwnm', 'r723mcnm', 'r723cper', 'smf72sid',
             'r723rtyp', 'phase'],
            ['smf72_wrs.smf72xnm', 'smf72_wrs.datetime', 'smf72_wrs.smf72ist', 'smf72_wrs.smf72iet',
             'smf72_wrs.r723mnsp', 'smf72_wrs.r723mwnm', 'smf72_wrs.r723mcnm', 'smf72_wrs.r723cper',
             'smf72_wrs.smf72sid', 'smf72_wrs.r723rtyp', 'smf72_wrs.phase']),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'datetime', 'smf72ist', 'smf72iet', 'r723mnsp', 'r723mwnm', 'r723mcnm', 'r723cper', 'r723rtyp',
             'phase', 'r723dnst', 'r723dnde'],
            ['smf72_dnsx.smf72xnm', 'smf72_dnsx.datetime', 'smf72_dnsx.smf72ist', 'smf72_dnsx.smf72iet',
             'smf72_dnsx.r723mnsp', 'smf72_dnsx.r723mwnm', 'smf72_dnsx.r723mcnm', 'smf72_dnsx.r723cper',
             'smf72_dnsx.r723rtyp', 'smf72_dnsx.phase', 'smf72_dnsx.r723dnst', 'smf72_dnsx.r723dnde']),
    )

    smf72_wrs: so.Mapped['Smf72Wrs'] = so.relationship(back_populates='smf72_dnss', viewonly=True)
    smf72_dnsx: so.Mapped['Smf72Dnsx'] = so.relationship(back_populates='smf72_dnss', viewonly=True)


class Smf72Dnsx(ReprMixin, Base72):
    """The Smf72Dnsx class stores the Smf72Dnsx section in the smf72_dnsx table."""

    __tablename__ = "smf72_dnsx"
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    r723rwnn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="number of the resource delay type. Values 1...15 are related to r723rw01...r723rw15 respectively.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf72ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf72iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")
    r723mnsp: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Policy name.")
    r723mwnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Workload name.")
    r723mcnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service/Report class name.")
    r723cper: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service or report class period number.")
    r723rtyp: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="Subsystem type, as used in the classification rules specified in the WLM administrative application. The subsystem's documentation should explain the meaning that the product attributes to the various states.")
    phase: so.Mapped[str] = so.mapped_column(sa.String(3),
                                             doc="states sampled in the begin_to_end phase of a transaction or in the execution phase of a transaction.")
    r723dnst: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="Subsystem type as used in the classification rules specified in the WLM administrative application.")
    r723dnde: so.Mapped[str] = so.mapped_column(sa.String(16), doc="Resource delay description.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, datetime, smf72ist, smf72iet, r723mnsp, r723mwnm, r723mcnm, r723cper,
                                r723rtyp, phase, r723dnst, r723dnde),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'datetime', 'smf72ist', 'smf72iet', 'r723mnsp', 'r723mwnm', 'r723mcnm', 'r723cper', 'r723rtyp',
             'phase'],
            ['smf72_wrsx.smf72xnm', 'smf72_wrsx.datetime', 'smf72_wrsx.smf72ist', 'smf72_wrsx.smf72iet',
             'smf72_wrsx.r723mnsp', 'smf72_wrsx.r723mwnm', 'smf72_wrsx.r723mcnm', 'smf72_wrsx.r723cper',
             'smf72_wrsx.r723rtyp', 'smf72_wrsx.phase']),
    )

    smf72_wrsx: so.Mapped['Smf72Wrsx'] = so.relationship(back_populates='smf72_dnsxs', viewonly=True)
    smf72_dnss: so.Mapped[List['Smf72Dns']] = so.relationship(back_populates='smf72_dnsx', viewonly=True)


class Smf72Data(ReprMixin, Base72, Smf72data):
    """The Smf72Data class stores the Smf72Data section in the smf72_data table."""

    __tablename__ = "smf72_data"
    r724pnam: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Name of active service policy.")
    r724ptm: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                 doc="Local time/date of policy activation (STCK format).")
    r724lcnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service class name.")
    r724per_: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service class period number.")
    smf_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf72ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf72iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, smf72sid, datetime, smf72ist, smf72iet, r724pnam, r724lcnm, r724per_),
        sa.ForeignKeyConstraint(
            ['datetime', 'smf72ist', 'smf72iet', 'smf_type', 'smf72xnm', 'smf72sid'],
            ['smf72_pro.datetime', 'smf72_pro.smf72ist', 'smf72_pro.smf72iet', 'smf72_pro.smf_type',
             'smf72_pro.smf72xnm', 'smf72_pro.smf72sid']),
    )

    smf72_pro: so.Mapped['Smf72Pro'] = so.relationship(back_populates='smf72_datas', viewonly=True)


class Smf72Rgs(ReprMixin, Base72, Smf72rgs):
    """The Smf72Rgs class stores the Smf72Rgs section in the smf72_rgs table."""

    __tablename__ = "smf72_rgs"
    r723ggnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Resource group name.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf72ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf72iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")
    r723mnsp: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Policy name.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, datetime, smf72ist, smf72iet, r723mnsp, r723ggnm),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'datetime', 'smf72ist', 'smf72iet', 'r723mnsp'],
            ['smf72_policy.smf72xnm', 'smf72_policy.datetime', 'smf72_policy.smf72ist', 'smf72_policy.smf72iet',
             'smf72_policy.r723mnsp']),
    )

    smf72_policy: so.Mapped['Smf72Policy'] = so.relationship(back_populates='smf72_rgss', viewonly=True)
    smf72_wmss: so.Mapped[List['Smf72Wms']] = so.relationship(back_populates='smf72_rgs', viewonly=True)


class Smf72Sss(ReprMixin, Base72):
    """The Smf72Sss class stores the Smf72Sss section in the smf72_sss table."""

    __tablename__ = "smf72_sss"
    r723scsn: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Name of service class being served (by one or more address spaces in service class R723MCNM).")
    r723scs_: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="number of times an address space running in service class r723mcnm was observed serving the served service class r723scsn.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf72ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf72iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")
    r723mnsp: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Policy name.")
    r723mwnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Workload name.")
    r723mcnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service/Report class name.")
    r723cper: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service or report class period number.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, datetime, smf72ist, smf72iet, r723mnsp, r723mwnm, r723mcnm, r723cper,
                                r723scsn, smf72sid),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'datetime', 'smf72ist', 'smf72iet', 'r723mnsp', 'r723mwnm', 'r723mcnm', 'r723cper'],
            ['smf72_wms.smf72xnm', 'smf72_wms.datetime', 'smf72_wms.smf72ist', 'smf72_wms.smf72iet',
             'smf72_wms.r723mnsp', 'smf72_wms.r723mwnm', 'smf72_wms.r723mcnm', 'smf72_wms.r723cper']),
    )

    smf72_wms: so.Mapped['Smf72Wms'] = so.relationship(back_populates='smf72_ssss', viewonly=True)


class Smf72Cmss(ReprMixin, Base72, Smf72cmss):
    """The Smf72Cmss class stores the Smf72Cmss section in the smf72_cmss table."""

    __tablename__ = "smf72_cmss"
    r725cmjn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Name of the job.")
    r725cmsp: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service class period.")
    r725cmst: so.Mapped[str] = so.mapped_column(sa.String(18), doc="Address space SToken.")
    r725cmsn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service class name.")
    r725cmty: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="Lock type: Value Meaning 1 CMS lock 2 CMS Enqueue/Dequeue lock 3 CMS Latch lock 4 CMS SMF lock")
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf72ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf72iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, smf72sid, datetime, smf72ist, smf72iet, r725cmst, r725cmjn, r725cmsn,
                                r725cmsp, r725cmty),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'smf72sid', 'datetime', 'smf72ist', 'smf72iet'],
            ['smf72_sctl.smf72xnm', 'smf72_sctl.smf72sid', 'smf72_sctl.datetime', 'smf72_sctl.smf72ist',
             'smf72_sctl.smf72iet']),
    )

    smf72_sctl: so.Mapped['Smf72Sctl'] = so.relationship(back_populates='smf72_cmsss', viewonly=True)


class Smf72Lasc(ReprMixin, Base72, Smf72lasc):
    """The Smf72Lasc class stores the Smf72Lasc section in the smf72_lasc table."""

    __tablename__ = "smf72_lasc"
    r725lajn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Name of the job.")
    r725lasp: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service class period.")
    r725last: so.Mapped[str] = so.mapped_column(sa.String(18), doc="Address space SToken.")
    r725lasn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service class name.")
    r725laty: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="Request type: Value Meaning 1 Latch obtain requests against a latch set created by this address space 2 Latch obtain requests from this address space")
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf72ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf72iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, smf72sid, datetime, smf72ist, smf72iet, r725last, r725lajn, r725lasn,
                                r725lasp, r725laty),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'smf72sid', 'datetime', 'smf72ist', 'smf72iet'],
            ['smf72_sctl.smf72xnm', 'smf72_sctl.smf72sid', 'smf72_sctl.datetime', 'smf72_sctl.smf72ist',
             'smf72_sctl.smf72iet']),
    )

    smf72_sctl: so.Mapped['Smf72Sctl'] = so.relationship(back_populates='smf72_lascs', viewonly=True)


class Smf72Clod(ReprMixin, Base72, Smf72clod):
    """The Smf72Clod class stores the Smf72Clod section in the smf72_clod table."""

    __tablename__ = "smf72_clod"
    r725cojn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Name of the job.")
    r725cosp: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service class period.")
    r725cost: so.Mapped[str] = so.mapped_column(sa.String(18), doc="Address space SToken.")
    r725cosn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service class name.")
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf72ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf72iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, smf72sid, datetime, smf72ist, smf72iet, r725cost, r725cojn, r725cosn,
                                r725cosp),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'smf72sid', 'datetime', 'smf72ist', 'smf72iet'],
            ['smf72_sctl.smf72xnm', 'smf72_sctl.smf72sid', 'smf72_sctl.datetime', 'smf72_sctl.smf72ist',
             'smf72_sctl.smf72iet']),
    )

    smf72_sctl: so.Mapped['Smf72Sctl'] = so.relationship(back_populates='smf72_clods', viewonly=True)


class Smf72Clrd(ReprMixin, Base72, Smf72clrd):
    """The Smf72Clrd class stores the Smf72Clrd section in the smf72_clrd table."""

    __tablename__ = "smf72_clrd"
    r725crjn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Name of the job.")
    r725crsp: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service class period.")
    r725crst: so.Mapped[str] = so.mapped_column(sa.String(18), doc="Address space SToken.")
    r725crsn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service class name.")
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf72ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf72iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, smf72sid, datetime, smf72ist, smf72iet, r725crst, r725crjn, r725crsn,
                                r725crsp),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'smf72sid', 'datetime', 'smf72ist', 'smf72iet'],
            ['smf72_sctl.smf72xnm', 'smf72_sctl.smf72sid', 'smf72_sctl.datetime', 'smf72_sctl.smf72ist',
             'smf72_sctl.smf72iet']),
    )

    smf72_sctl: so.Mapped['Smf72Sctl'] = so.relationship(back_populates='smf72_clrds', viewonly=True)


class Smf72Ense(ReprMixin, Base72, Smf72ense):
    """The Smf72Ense class stores the Smf72Ense section in the smf72_ense table."""

    __tablename__ = "smf72_ense"
    r725enjn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Name of the job.")
    r725ensp: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service class period.")
    r725enst: so.Mapped[str] = so.mapped_column(sa.String(18), doc="Address space SToken.")
    r725ensn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service class name.")
    r725ensc: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="Enqueue scope type: Value Meaning 1 Scope = Step 2 Scope = System 3 Scope = Systems")
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    ense_index: so.Mapped[int] = so.mapped_column(sa.Integer, doc="The index of GRS Enqueue Step data")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf72ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf72iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, smf72sid, datetime, smf72ist, smf72iet, r725enst, r725enjn, r725ensn,
                                r725ensp, r725ensc, ense_index),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'smf72sid', 'datetime', 'smf72ist', 'smf72iet'],
            ['smf72_sctl.smf72xnm', 'smf72_sctl.smf72sid', 'smf72_sctl.datetime', 'smf72_sctl.smf72ist',
             'smf72_sctl.smf72iet']),
    )

    smf72_sctl: so.Mapped['Smf72Sctl'] = so.relationship(back_populates='smf72_enses', viewonly=True)


class Smf72Ensy(ReprMixin, Base72, Smf72ense):
    """The Smf72Ensy class stores the Smf72Ensy section in the smf72_ensy table."""

    __tablename__ = "smf72_ensy"
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    ensy_index: so.Mapped[int] = so.mapped_column(sa.Integer, doc="The index of GRS Enqueue System data")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf72ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf72iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")
    r725enst: so.Mapped[str] = so.mapped_column(sa.String(18), doc="Address space SToken.")
    r725enjn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Name of the job.")
    r725ensn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service class name.")
    r725ensp: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service class period.")
    r725ensc: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="Enqueue scope type: Value Meaning 1 Scope = Step 2 Scope = System 3 Scope = Systems")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, smf72sid, datetime, smf72ist, smf72iet, r725enst, r725enjn, r725ensn,
                                r725ensp, r725ensc, ensy_index),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'smf72sid', 'datetime', 'smf72ist', 'smf72iet'],
            ['smf72_sctl.smf72xnm', 'smf72_sctl.smf72sid', 'smf72_sctl.datetime', 'smf72_sctl.smf72ist',
             'smf72_sctl.smf72iet']),
    )

    smf72_sctl: so.Mapped['Smf72Sctl'] = so.relationship(back_populates='smf72_ensys', viewonly=True)


class Smf72Lotd(ReprMixin, Base72, Smf72lotd):
    """The Smf72Lotd class stores the Smf72Lotd section in the smf72_lotd table."""

    __tablename__ = "smf72_lotd"
    r725lojn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Name of the job.")
    r725losp: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service class period.")
    r725lost: so.Mapped[str] = so.mapped_column(sa.String(18), doc="Address space SToken.")
    r725losn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service class name.")
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf72ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf72iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, smf72sid, datetime, smf72ist, smf72iet, r725lost, r725lojn, r725losn,
                                r725losp),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'smf72sid', 'datetime', 'smf72ist', 'smf72iet'],
            ['smf72_sctl.smf72xnm', 'smf72_sctl.smf72sid', 'smf72_sctl.datetime', 'smf72_sctl.smf72ist',
             'smf72_sctl.smf72iet']),
    )

    smf72_sctl: so.Mapped['Smf72Sctl'] = so.relationship(back_populates='smf72_lotds', viewonly=True)


class Smf72Qsad(ReprMixin, Base72, Smf72qsad):
    """The Smf72Qsad class stores the Smf72Qsad section in the smf72_qsad table."""

    __tablename__ = "smf72_qsad"
    r725qsjn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Name of the job.")
    r725qssp: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service class period.")
    r725qsst: so.Mapped[str] = so.mapped_column(sa.String(18), doc="Address space SToken.")
    r725qssn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service class name.")
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf72ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf72iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, smf72sid, datetime, smf72ist, smf72iet, r725qsst, r725qsjn, r725qssn,
                                r725qssp),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'smf72sid', 'datetime', 'smf72ist', 'smf72iet'],
            ['smf72_sctl.smf72xnm', 'smf72_sctl.smf72sid', 'smf72_sctl.datetime', 'smf72_sctl.smf72ist',
             'smf72_sctl.smf72iet']),
    )

    smf72_sctl: so.Mapped['Smf72Sctl'] = so.relationship(back_populates='smf72_qsads', viewonly=True)


class Smf72Enss(ReprMixin, Base72, Smf72ense):
    """The Smf72Enss class stores the Smf72Enss section in the smf72_enss table."""

    __tablename__ = "smf72_enss"
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf72ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf72iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")
    r725enst: so.Mapped[str] = so.mapped_column(sa.String(18), doc="Address space SToken.")
    r725enjn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Name of the job.")
    r725ensn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service class name.")
    r725ensp: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service class period.")
    r725ensc: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="Enqueue scope type: Value Meaning 1 Scope = Step 2 Scope = System 3 Scope = Systems")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, smf72sid, datetime, smf72ist, smf72iet, r725enst, r725enjn, r725ensn,
                                r725ensp, r725ensc),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'smf72sid', 'datetime', 'smf72ist', 'smf72iet'],
            ['smf72_sctl.smf72xnm', 'smf72_sctl.smf72sid', 'smf72_sctl.datetime', 'smf72_sctl.smf72ist',
             'smf72_sctl.smf72iet']),
    )

    smf72_sctl: so.Mapped['Smf72Sctl'] = so.relationship(back_populates='smf72_ensss', viewonly=True)


class Smf72Lare(ReprMixin, Base72, Smf72lasc):
    """The Smf72Lare class stores the Smf72Lare section in the smf72_lare table."""

    __tablename__ = "smf72_lare"
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf72ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf72iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")
    r725last: so.Mapped[str] = so.mapped_column(sa.String(18), doc="Address space SToken.")
    r725lajn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Name of the job.")
    r725lasn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service class name.")
    r725lasp: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service class period.")
    r725laty: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="Request type: Value Meaning 1 Latch obtain requests against a latch set created by this address space 2 Latch obtain requests from this address space")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, smf72sid, datetime, smf72ist, smf72iet, r725last, r725lajn, r725lasn,
                                r725lasp, r725laty),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'smf72sid', 'datetime', 'smf72ist', 'smf72iet'],
            ['smf72_sctl.smf72xnm', 'smf72_sctl.smf72sid', 'smf72_sctl.datetime', 'smf72_sctl.smf72ist',
             'smf72_sctl.smf72iet']),
    )

    smf72_sctl: so.Mapped['Smf72Sctl'] = so.relationship(back_populates='smf72_lares', viewonly=True)


class Smf72Csms(ReprMixin, Base72, Smf72cmss):
    """The Smf72Csms class stores the Smf72Csms section in the smf72_csms table."""

    __tablename__ = "smf72_csms"
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf72ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf72iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")
    r725cmst: so.Mapped[str] = so.mapped_column(sa.String(18), doc="Address space SToken.")
    r725cmjn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Name of the job.")
    r725cmsn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service class name.")
    r725cmsp: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service class period.")
    r725cmty: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="Lock type: Value Meaning 1 CMS lock 2 CMS Enqueue/Dequeue lock 3 CMS Latch lock 4 CMS SMF lock")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, smf72sid, datetime, smf72ist, smf72iet, r725cmst, r725cmjn, r725cmsn,
                                r725cmsp, r725cmty),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'smf72sid', 'datetime', 'smf72ist', 'smf72iet'],
            ['smf72_sctl.smf72xnm', 'smf72_sctl.smf72sid', 'smf72_sctl.datetime', 'smf72_sctl.smf72ist',
             'smf72_sctl.smf72iet']),
    )

    smf72_sctl: so.Mapped['Smf72Sctl'] = so.relationship(back_populates='smf72_csmss', viewonly=True)


class Smf72Clas(ReprMixin, Base72, Smf72cmss):
    """The Smf72Clas class stores the Smf72Clas section in the smf72_clas table."""

    __tablename__ = "smf72_clas"
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf72ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf72iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")
    r725cmst: so.Mapped[str] = so.mapped_column(sa.String(18), doc="Address space SToken.")
    r725cmjn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Name of the job.")
    r725cmsn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service class name.")
    r725cmsp: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service class period.")
    r725cmty: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="Lock type: Value Meaning 1 CMS lock 2 CMS Enqueue/Dequeue lock 3 CMS Latch lock 4 CMS SMF lock")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, smf72sid, datetime, smf72ist, smf72iet, r725cmst, r725cmjn, r725cmsn,
                                r725cmsp, r725cmty),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'smf72sid', 'datetime', 'smf72ist', 'smf72iet'],
            ['smf72_sctl.smf72xnm', 'smf72_sctl.smf72sid', 'smf72_sctl.datetime', 'smf72_sctl.smf72ist',
             'smf72_sctl.smf72iet']),
    )

    smf72_sctl: so.Mapped['Smf72Sctl'] = so.relationship(back_populates='smf72_class', viewonly=True)


class Smf72Ceds(ReprMixin, Base72, Smf72cmss):
    """The Smf72Ceds class stores the Smf72Ceds section in the smf72_ceds table."""

    __tablename__ = "smf72_ceds"
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf72ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf72iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")
    r725cmst: so.Mapped[str] = so.mapped_column(sa.String(18), doc="Address space SToken.")
    r725cmjn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Name of the job.")
    r725cmsn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service class name.")
    r725cmsp: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service class period.")
    r725cmty: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="Lock type: Value Meaning 1 CMS lock 2 CMS Enqueue/Dequeue lock 3 CMS Latch lock 4 CMS SMF lock")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, smf72sid, datetime, smf72ist, smf72iet, r725cmst, r725cmjn, r725cmsn,
                                r725cmsp, r725cmty),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'smf72sid', 'datetime', 'smf72ist', 'smf72iet'],
            ['smf72_sctl.smf72xnm', 'smf72_sctl.smf72sid', 'smf72_sctl.datetime', 'smf72_sctl.smf72ist',
             'smf72_sctl.smf72iet']),
    )

    smf72_sctl: so.Mapped['Smf72Sctl'] = so.relationship(back_populates='smf72_cedss', viewonly=True)
