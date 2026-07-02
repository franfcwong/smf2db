import datetime as dt
from typing import List, Optional

import sqlalchemy as sa
import sqlalchemy.orm as so

from .smf72_base import ReprMixin, Base72Hr, Smf72pro, Smf72policy, Smf72wms, Smf72scs, Smf72rts, Smf72wrs, Smf72rgs, \
    Smf72data, Smf72cmss, Smf72lotd, Smf72clod, Smf72clrd, Smf72lasc, Smf72ense, Smf72qsad, Smf72sctl


class Smf72ProHr(ReprMixin, Base72Hr, Smf72pro):
    """The Smf72ProHr class stores the hourly Smf72Pro record in the smf72_pro_hr table."""

    __tablename__ = "smf72_pro_hr"
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    speed_boost: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                             doc="smf72fla (Bit 10) indcating speed boost was active during entire interval.")
    ziip_boost: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                            doc="smf72fla (Bit 9) indciating zIIP boost was active during entire interval.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf_type: so.Mapped[str] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(datetime, smf_type, smf72xnm, smf72sid),
    )

    smf72_sctl_hr: so.Mapped['Smf72SctlHr'] = so.relationship(back_populates='smf72_pro_hr', viewonly=True)
    smf72_policy_hr: so.Mapped['Smf72PolicyHr'] = so.relationship(back_populates='smf72_pro_hrs', viewonly=True,
                                                                  foreign_keys=[datetime, smf_type, smf72xnm],
                                                                  primaryjoin='and_(Smf72ProHr.datetime==Smf72PolicyHr.datetime, Smf72ProHr.smf_type==Smf72PolicyHr.smf_type, Smf72ProHr.smf72xnm==Smf72PolicyHr.smf72xnm)', )
    smf72_scs_hrs: so.Mapped[List['Smf72ScsHr']] = so.relationship(back_populates='smf72_pro_hr', viewonly=True)
    smf72_data_hrs: so.Mapped[List['Smf72DataHr']] = so.relationship(back_populates='smf72_pro_hr', viewonly=True)


class Smf72WrsHr(ReprMixin, Base72Hr, Smf72wrs):
    """The Smf72WrsHr class stores the hourly Smf72Wrs record in the smf72_wrs_hr table."""

    __tablename__ = "smf72_wrs_hr"
    r723rtyp: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="Subsystem type, as used in the classification rules specified in the WLM administrative application. The subsystem's documentation should explain the meaning that the product attributes to the various states.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    phase: so.Mapped[str] = so.mapped_column(sa.String(3),
                                             doc="states sampled in the begin_to_end phase of a transaction or in the execution phase of a transaction.")
    r723rexe: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r723rflg (Bit 1) representing states sampled in the execution phase of a transaction.")
    r723rdbe: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r723rflg (Bit 0) representing states sampled in the begin_to_end phase of a transaction.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    r723mnsp: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Policy name.")
    r723mwnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Workload name.")
    r723mcnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service/Report class name.")
    r723cper: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service or report class period number.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, datetime, r723mnsp, r723mwnm, r723mcnm, r723cper, smf72sid, r723rtyp, phase),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'datetime', 'r723mnsp', 'r723mwnm', 'r723mcnm', 'r723cper', 'smf72sid'],
            ['smf72_scs_hr.smf72xnm', 'smf72_scs_hr.datetime', 'smf72_scs_hr.r723mnsp', 'smf72_scs_hr.r723mwnm',
             'smf72_scs_hr.r723mcnm', 'smf72_scs_hr.r723cper', 'smf72_scs_hr.smf72sid']),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'datetime', 'r723mnsp', 'r723mwnm', 'r723mcnm', 'r723cper', 'r723rtyp', 'phase'],
            ['smf72_wrsx_hr.smf72xnm', 'smf72_wrsx_hr.datetime', 'smf72_wrsx_hr.r723mnsp', 'smf72_wrsx_hr.r723mwnm',
             'smf72_wrsx_hr.r723mcnm', 'smf72_wrsx_hr.r723cper', 'smf72_wrsx_hr.r723rtyp', 'smf72_wrsx_hr.phase']),
    )

    smf72_scs_hr: so.Mapped['Smf72ScsHr'] = so.relationship(back_populates='smf72_wrs_hrs', viewonly=True)
    smf72_wrsx_hr: so.Mapped['Smf72WrsxHr'] = so.relationship(back_populates='smf72_wrs_hrs', viewonly=True)
    smf72_dns_hrs: so.Mapped[List['Smf72DnsHr']] = so.relationship(back_populates='smf72_wrs_hr', viewonly=True)


class Smf72ScsHr(ReprMixin, Base72Hr, Smf72scs, Smf72wrs):
    """The Smf72ScsHr class stores the hourly Smf72Scs record in the smf72_scs_hr table."""

    __tablename__ = "smf72_scs_hr"
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
    r723mnsp: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Policy name.")
    r723mwnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Workload name.")
    r723mcnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service/Report class name.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, datetime, r723mnsp, r723mwnm, r723mcnm, r723cper, smf72sid),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'datetime', 'r723mnsp', 'r723mwnm', 'r723mcnm', 'r723cper'],
            ['smf72_wms_hr.smf72xnm', 'smf72_wms_hr.datetime', 'smf72_wms_hr.r723mnsp', 'smf72_wms_hr.r723mwnm',
             'smf72_wms_hr.r723mcnm', 'smf72_wms_hr.r723cper']),
        sa.ForeignKeyConstraint(
            ['datetime', 'smf_type', 'smf72xnm', 'smf72sid'],
            ['smf72_pro_hr.datetime', 'smf72_pro_hr.smf_type', 'smf72_pro_hr.smf72xnm', 'smf72_pro_hr.smf72sid']),
    )

    smf72_rts_hr: so.Mapped['Smf72RtsHr'] = so.relationship(back_populates='smf72_scs_hr', viewonly=True)
    smf72_wms_hr: so.Mapped['Smf72WmsHr'] = so.relationship(back_populates='smf72_scs_hrs', viewonly=True)
    smf72_pro_hr: so.Mapped['Smf72ProHr'] = so.relationship(back_populates='smf72_scs_hrs', viewonly=True)
    smf72_wrs_hrs: so.Mapped[List['Smf72WrsHr']] = so.relationship(back_populates='smf72_scs_hr', viewonly=True)


class Smf72PolicyHr(ReprMixin, Base72Hr, Smf72policy):
    """The Smf72PolicyHr class stores the hourly Smf72Policy record in the smf72_policy_hr table."""

    __tablename__ = "smf72_policy_hr"
    smf_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    interval_start_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                             doc="the start time of the interval")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    r723mnsp: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Policy name.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, datetime, r723mnsp),
    )

    smf72_workload_hrs: so.Mapped[List['Smf72WorkloadHr']] = so.relationship(back_populates='smf72_policy_hr',
                                                                             viewonly=True)
    smf72_wms_hrs: so.Mapped[List['Smf72WmsHr']] = so.relationship(back_populates='smf72_policy_hr', viewonly=True)
    smf72_rgs_hrs: so.Mapped[List['Smf72RgsHr']] = so.relationship(back_populates='smf72_policy_hr', viewonly=True)
    smf72_pro_hrs: so.Mapped[List['Smf72ProHr']] = so.relationship(back_populates='smf72_policy_hr', viewonly=True,
                                                                   foreign_keys='Smf72ProHr.datetime, Smf72ProHr.smf_type, Smf72ProHr.smf72xnm',
                                                                   primaryjoin='and_(Smf72PolicyHr.datetime==Smf72ProHr.datetime, Smf72PolicyHr.smf_type==Smf72ProHr.smf_type, Smf72PolicyHr.smf72xnm==Smf72ProHr.smf72xnm)', )


class Smf72WorkloadHr(ReprMixin, Base72Hr):
    """The Smf72WorkloadHr class stores the hourly Smf72Workload record in the smf72_workload_hr table."""

    __tablename__ = "smf72_workload_hr"
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    r723mwde: so.Mapped[Optional[str]] = so.mapped_column(sa.String(32), doc="Workload description.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    r723mnsp: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Policy name.")
    r723mwnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Workload name.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, datetime, r723mnsp, r723mwnm),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'datetime', 'r723mnsp'],
            ['smf72_policy_hr.smf72xnm', 'smf72_policy_hr.datetime', 'smf72_policy_hr.r723mnsp']),
    )

    smf72_policy_hr: so.Mapped['Smf72PolicyHr'] = so.relationship(back_populates='smf72_workload_hrs', viewonly=True)
    smf72_wms_hrs: so.Mapped[List['Smf72WmsHr']] = so.relationship(back_populates='smf72_workload_hr', viewonly=True)


class Smf72RtsHr(ReprMixin, Base72Hr, Smf72rts):
    """The Smf72RtsHr class stores the hourly Smf72Rts record in the smf72_rts_hr table."""

    __tablename__ = "smf72_rts_hr"
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    r723mnsp: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Policy name.")
    r723mwnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Workload name.")
    r723mcnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service/Report class name.")
    r723cper: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service or report class period number.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, datetime, r723mnsp, r723mwnm, r723mcnm, r723cper, smf72sid),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'datetime', 'r723mnsp', 'r723mwnm', 'r723mcnm', 'r723cper', 'smf72sid'],
            ['smf72_scs_hr.smf72xnm', 'smf72_scs_hr.datetime', 'smf72_scs_hr.r723mnsp', 'smf72_scs_hr.r723mwnm',
             'smf72_scs_hr.r723mcnm', 'smf72_scs_hr.r723cper', 'smf72_scs_hr.smf72sid']),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'datetime', 'r723mnsp', 'r723mwnm', 'r723mcnm', 'r723cper'],
            ['smf72_wms_hr.smf72xnm', 'smf72_wms_hr.datetime', 'smf72_wms_hr.r723mnsp', 'smf72_wms_hr.r723mwnm',
             'smf72_wms_hr.r723mcnm', 'smf72_wms_hr.r723cper']),
    )

    smf72_scs_hr: so.Mapped['Smf72ScsHr'] = so.relationship(back_populates='smf72_rts_hr', viewonly=True)
    smf72_wms_hr: so.Mapped['Smf72WmsHr'] = so.relationship(back_populates='smf72_rts_hrs', viewonly=True)


class Smf72SctlHr(ReprMixin, Base72Hr, Smf72sctl):
    """The Smf72SctlHr class stores the hourly Smf72Sctl record in the smf72_sctl_hr table."""

    __tablename__ = "smf72_sctl_hr"
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, smf72sid, datetime),
        sa.ForeignKeyConstraint(
            ['datetime', 'smf_type', 'smf72xnm', 'smf72sid'],
            ['smf72_pro_hr.datetime', 'smf72_pro_hr.smf_type', 'smf72_pro_hr.smf72xnm', 'smf72_pro_hr.smf72sid']),
    )

    smf72_pro_hr: so.Mapped['Smf72ProHr'] = so.relationship(back_populates='smf72_sctl_hr', viewonly=True)
    smf72_cmss_hrs: so.Mapped[List['Smf72CmssHr']] = so.relationship(back_populates='smf72_sctl_hr', viewonly=True)
    smf72_ceds_hrs: so.Mapped[List['Smf72CedsHr']] = so.relationship(back_populates='smf72_sctl_hr', viewonly=True)
    smf72_clas_hrs: so.Mapped[List['Smf72ClasHr']] = so.relationship(back_populates='smf72_sctl_hr', viewonly=True)
    smf72_csms_hrs: so.Mapped[List['Smf72CsmsHr']] = so.relationship(back_populates='smf72_sctl_hr', viewonly=True)
    smf72_lotd_hrs: so.Mapped[List['Smf72LotdHr']] = so.relationship(back_populates='smf72_sctl_hr', viewonly=True)
    smf72_clod_hrs: so.Mapped[List['Smf72ClodHr']] = so.relationship(back_populates='smf72_sctl_hr', viewonly=True)
    smf72_clrd_hrs: so.Mapped[List['Smf72ClrdHr']] = so.relationship(back_populates='smf72_sctl_hr', viewonly=True)
    smf72_lasc_hrs: so.Mapped[List['Smf72LascHr']] = so.relationship(back_populates='smf72_sctl_hr', viewonly=True)
    smf72_lare_hrs: so.Mapped[List['Smf72LareHr']] = so.relationship(back_populates='smf72_sctl_hr', viewonly=True)
    smf72_ense_hrs: so.Mapped[List['Smf72EnseHr']] = so.relationship(back_populates='smf72_sctl_hr', viewonly=True)
    smf72_ensy_hrs: so.Mapped[List['Smf72EnsyHr']] = so.relationship(back_populates='smf72_sctl_hr', viewonly=True)
    smf72_enss_hrs: so.Mapped[List['Smf72EnssHr']] = so.relationship(back_populates='smf72_sctl_hr', viewonly=True)
    smf72_qsad_hrs: so.Mapped[List['Smf72QsadHr']] = so.relationship(back_populates='smf72_sctl_hr', viewonly=True)


class Smf72WmsHr(ReprMixin, Base72Hr, Smf72wms, Smf72scs, Smf72rts, Smf72wrs):
    """The Smf72WmsHr class stores the hourly Smf72Wms record in the smf72_wms_hr table."""

    __tablename__ = "smf72_wms_hr"
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
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    r723cper: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service or report class period number.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, datetime, r723mnsp, r723mwnm, r723mcnm, r723cper),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'datetime', 'r723mnsp'],
            ['smf72_policy_hr.smf72xnm', 'smf72_policy_hr.datetime', 'smf72_policy_hr.r723mnsp']),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'datetime', 'r723mnsp', 'r723mwnm'],
            ['smf72_workload_hr.smf72xnm', 'smf72_workload_hr.datetime', 'smf72_workload_hr.r723mnsp',
             'smf72_workload_hr.r723mwnm']),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'datetime', 'r723mnsp', 'r723ggnm'],
            ['smf72_rgs_hr.smf72xnm', 'smf72_rgs_hr.datetime', 'smf72_rgs_hr.r723mnsp', 'smf72_rgs_hr.r723ggnm']),
    )

    smf72_policy_hr: so.Mapped['Smf72PolicyHr'] = so.relationship(back_populates='smf72_wms_hrs', viewonly=True)
    smf72_workload_hr: so.Mapped['Smf72WorkloadHr'] = so.relationship(back_populates='smf72_wms_hrs', viewonly=True)
    smf72_rgs_hr: so.Mapped['Smf72RgsHr'] = so.relationship(back_populates='smf72_wms_hrs', viewonly=True)
    smf72_sss_hrs: so.Mapped[List['Smf72SssHr']] = so.relationship(back_populates='smf72_wms_hr', viewonly=True)
    smf72_rts_hrs: so.Mapped[List['Smf72RtsHr']] = so.relationship(back_populates='smf72_wms_hr', viewonly=True)
    smf72_scs_hrs: so.Mapped[List['Smf72ScsHr']] = so.relationship(back_populates='smf72_wms_hr', viewonly=True)
    smf72_wrsx_hrs: so.Mapped[List['Smf72WrsxHr']] = so.relationship(back_populates='smf72_wms_hr', viewonly=True)


class Smf72WrsxHr(ReprMixin, Base72Hr, Smf72wrs):
    """The Smf72WrsxHr class stores the hourly Smf72Wrsx record in the smf72_wrsx_hr table."""

    __tablename__ = "smf72_wrsx_hr"
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    r723rexe: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r723rflg (Bit 1) representing states sampled in the execution phase of a transaction.")
    r723rdbe: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r723rflg (Bit 0) representing states sampled in the begin_to_end phase of a transaction.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    phase: so.Mapped[str] = so.mapped_column(sa.String(3),
                                             doc="states sampled in the begin_to_end phase of a transaction or in the execution phase of a transaction.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    r723mnsp: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Policy name.")
    r723mwnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Workload name.")
    r723mcnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service/Report class name.")
    r723cper: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service or report class period number.")
    r723rtyp: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="Subsystem type, as used in the classification rules specified in the WLM administrative application. The subsystem's documentation should explain the meaning that the product attributes to the various states.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, datetime, r723mnsp, r723mwnm, r723mcnm, r723cper, r723rtyp, phase),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'datetime', 'r723mnsp', 'r723mwnm', 'r723mcnm', 'r723cper'],
            ['smf72_wms_hr.smf72xnm', 'smf72_wms_hr.datetime', 'smf72_wms_hr.r723mnsp', 'smf72_wms_hr.r723mwnm',
             'smf72_wms_hr.r723mcnm', 'smf72_wms_hr.r723cper']),
    )

    smf72_wms_hr: so.Mapped['Smf72WmsHr'] = so.relationship(back_populates='smf72_wrsx_hrs', viewonly=True)
    smf72_dnsx_hrs: so.Mapped[List['Smf72DnsxHr']] = so.relationship(back_populates='smf72_wrsx_hr', viewonly=True)
    smf72_wrs_hrs: so.Mapped[List['Smf72WrsHr']] = so.relationship(back_populates='smf72_wrsx_hr', viewonly=True)


class Smf72DnsHr(ReprMixin, Base72Hr):
    """The Smf72DnsHr class stores the hourly Smf72Dns record in the smf72_dns_hr table."""

    __tablename__ = "smf72_dns_hr"
    r723dnst: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="Subsystem type as used in the classification rules specified in the WLM administrative application.")
    r723dnde: so.Mapped[str] = so.mapped_column(sa.String(16), doc="Resource delay description.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    r723rwnn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="number of the resource delay type. Values 1...15 are related to r723rw01...r723rw15 respectively.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
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
        sa.PrimaryKeyConstraint(smf72xnm, datetime, r723mnsp, r723mwnm, r723mcnm, r723cper, smf72sid, r723rtyp, phase,
                                r723dnst, r723dnde),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'datetime', 'r723mnsp', 'r723mwnm', 'r723mcnm', 'r723cper', 'smf72sid', 'r723rtyp', 'phase'],
            ['smf72_wrs_hr.smf72xnm', 'smf72_wrs_hr.datetime', 'smf72_wrs_hr.r723mnsp', 'smf72_wrs_hr.r723mwnm',
             'smf72_wrs_hr.r723mcnm', 'smf72_wrs_hr.r723cper', 'smf72_wrs_hr.smf72sid', 'smf72_wrs_hr.r723rtyp',
             'smf72_wrs_hr.phase']),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'datetime', 'r723mnsp', 'r723mwnm', 'r723mcnm', 'r723cper', 'r723rtyp', 'phase', 'r723dnst',
             'r723dnde'],
            ['smf72_dnsx_hr.smf72xnm', 'smf72_dnsx_hr.datetime', 'smf72_dnsx_hr.r723mnsp', 'smf72_dnsx_hr.r723mwnm',
             'smf72_dnsx_hr.r723mcnm', 'smf72_dnsx_hr.r723cper', 'smf72_dnsx_hr.r723rtyp', 'smf72_dnsx_hr.phase',
             'smf72_dnsx_hr.r723dnst', 'smf72_dnsx_hr.r723dnde']),
    )

    smf72_wrs_hr: so.Mapped['Smf72WrsHr'] = so.relationship(back_populates='smf72_dns_hrs', viewonly=True)
    smf72_dnsx_hr: so.Mapped['Smf72DnsxHr'] = so.relationship(back_populates='smf72_dns_hrs', viewonly=True)


class Smf72DnsxHr(ReprMixin, Base72Hr):
    """The Smf72DnsxHr class stores the hourly Smf72Dnsx record in the smf72_dnsx_hr table."""

    __tablename__ = "smf72_dnsx_hr"
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    r723rwnn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="number of the resource delay type. Values 1...15 are related to r723rw01...r723rw15 respectively.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
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
        sa.PrimaryKeyConstraint(smf72xnm, datetime, r723mnsp, r723mwnm, r723mcnm, r723cper, r723rtyp, phase, r723dnst,
                                r723dnde),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'datetime', 'r723mnsp', 'r723mwnm', 'r723mcnm', 'r723cper', 'r723rtyp', 'phase'],
            ['smf72_wrsx_hr.smf72xnm', 'smf72_wrsx_hr.datetime', 'smf72_wrsx_hr.r723mnsp', 'smf72_wrsx_hr.r723mwnm',
             'smf72_wrsx_hr.r723mcnm', 'smf72_wrsx_hr.r723cper', 'smf72_wrsx_hr.r723rtyp', 'smf72_wrsx_hr.phase']),
    )

    smf72_wrsx_hr: so.Mapped['Smf72WrsxHr'] = so.relationship(back_populates='smf72_dnsx_hrs', viewonly=True)
    smf72_dns_hrs: so.Mapped[List['Smf72DnsHr']] = so.relationship(back_populates='smf72_dnsx_hr', viewonly=True)


class Smf72DataHr(ReprMixin, Base72Hr, Smf72data):
    """The Smf72DataHr class stores the hourly Smf72Data record in the smf72_data_hr table."""

    __tablename__ = "smf72_data_hr"
    r724pnam: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Name of active service policy.")
    r724ptm: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                 doc="Local time/date of policy activation (STCK format).")
    r724lcnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service class name.")
    r724per_: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service class period number.")
    smf_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, smf72sid, datetime, r724pnam, r724lcnm, r724per_),
        sa.ForeignKeyConstraint(
            ['datetime', 'smf_type', 'smf72xnm', 'smf72sid'],
            ['smf72_pro_hr.datetime', 'smf72_pro_hr.smf_type', 'smf72_pro_hr.smf72xnm', 'smf72_pro_hr.smf72sid']),
    )

    smf72_pro_hr: so.Mapped['Smf72ProHr'] = so.relationship(back_populates='smf72_data_hrs', viewonly=True)


class Smf72RgsHr(ReprMixin, Base72Hr, Smf72rgs):
    """The Smf72RgsHr class stores the hourly Smf72Rgs record in the smf72_rgs_hr table."""

    __tablename__ = "smf72_rgs_hr"
    r723ggnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Resource group name.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    r723mnsp: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Policy name.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, datetime, r723mnsp, r723ggnm),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'datetime', 'r723mnsp'],
            ['smf72_policy_hr.smf72xnm', 'smf72_policy_hr.datetime', 'smf72_policy_hr.r723mnsp']),
    )

    smf72_policy_hr: so.Mapped['Smf72PolicyHr'] = so.relationship(back_populates='smf72_rgs_hrs', viewonly=True)
    smf72_wms_hrs: so.Mapped[List['Smf72WmsHr']] = so.relationship(back_populates='smf72_rgs_hr', viewonly=True)


class Smf72SssHr(ReprMixin, Base72Hr):
    """The Smf72SssHr class stores the hourly Smf72Sss record in the smf72_sss_hr table."""

    __tablename__ = "smf72_sss_hr"
    r723scsn: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Name of service class being served (by one or more address spaces in service class R723MCNM).")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    r723scs_: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="number of times an address space running in service class r723mcnm was observed serving the served service class r723scsn.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    r723mnsp: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Policy name.")
    r723mwnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Workload name.")
    r723mcnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service/Report class name.")
    r723cper: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service or report class period number.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, datetime, r723mnsp, r723mwnm, r723mcnm, r723cper, r723scsn, smf72sid),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'datetime', 'r723mnsp', 'r723mwnm', 'r723mcnm', 'r723cper'],
            ['smf72_wms_hr.smf72xnm', 'smf72_wms_hr.datetime', 'smf72_wms_hr.r723mnsp', 'smf72_wms_hr.r723mwnm',
             'smf72_wms_hr.r723mcnm', 'smf72_wms_hr.r723cper']),
    )

    smf72_wms_hr: so.Mapped['Smf72WmsHr'] = so.relationship(back_populates='smf72_sss_hrs', viewonly=True)


class Smf72CmssHr(ReprMixin, Base72Hr, Smf72cmss):
    """The Smf72CmssHr class stores the hourly Smf72Cmss record in the smf72_cmss_hr table."""

    __tablename__ = "smf72_cmss_hr"
    r725cmjn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Name of the job.")
    r725cmsp: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service class period.")
    r725cmst: so.Mapped[str] = so.mapped_column(sa.String(18), doc="Address space SToken.")
    r725cmsn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service class name.")
    r725cmty: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="Lock type: Value Meaning 1 CMS lock 2 CMS Enqueue/Dequeue lock 3 CMS Latch lock 4 CMS SMF lock")
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, smf72sid, datetime, r725cmst, r725cmjn, r725cmsn, r725cmsp, r725cmty),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'smf72sid', 'datetime'],
            ['smf72_sctl_hr.smf72xnm', 'smf72_sctl_hr.smf72sid', 'smf72_sctl_hr.datetime']),
    )

    smf72_sctl_hr: so.Mapped['Smf72SctlHr'] = so.relationship(back_populates='smf72_cmss_hrs', viewonly=True)


class Smf72LascHr(ReprMixin, Base72Hr, Smf72lasc):
    """The Smf72LascHr class stores the hourly Smf72Lasc record in the smf72_lasc_hr table."""

    __tablename__ = "smf72_lasc_hr"
    r725lajn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Name of the job.")
    r725lasp: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service class period.")
    r725last: so.Mapped[str] = so.mapped_column(sa.String(18), doc="Address space SToken.")
    r725lasn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service class name.")
    r725laty: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="Request type: Value Meaning 1 Latch obtain requests against a latch set created by this address space 2 Latch obtain requests from this address space")
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, smf72sid, datetime, r725last, r725lajn, r725lasn, r725lasp, r725laty),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'smf72sid', 'datetime'],
            ['smf72_sctl_hr.smf72xnm', 'smf72_sctl_hr.smf72sid', 'smf72_sctl_hr.datetime']),
    )

    smf72_sctl_hr: so.Mapped['Smf72SctlHr'] = so.relationship(back_populates='smf72_lasc_hrs', viewonly=True)


class Smf72ClodHr(ReprMixin, Base72Hr, Smf72clod):
    """The Smf72ClodHr class stores the hourly Smf72Clod record in the smf72_clod_hr table."""

    __tablename__ = "smf72_clod_hr"
    r725cojn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Name of the job.")
    r725cosp: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service class period.")
    r725cost: so.Mapped[str] = so.mapped_column(sa.String(18), doc="Address space SToken.")
    r725cosn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service class name.")
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, smf72sid, datetime, r725cost, r725cojn, r725cosn, r725cosp),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'smf72sid', 'datetime'],
            ['smf72_sctl_hr.smf72xnm', 'smf72_sctl_hr.smf72sid', 'smf72_sctl_hr.datetime']),
    )

    smf72_sctl_hr: so.Mapped['Smf72SctlHr'] = so.relationship(back_populates='smf72_clod_hrs', viewonly=True)


class Smf72ClrdHr(ReprMixin, Base72Hr, Smf72clrd):
    """The Smf72ClrdHr class stores the hourly Smf72Clrd record in the smf72_clrd_hr table."""

    __tablename__ = "smf72_clrd_hr"
    r725crjn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Name of the job.")
    r725crsp: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service class period.")
    r725crst: so.Mapped[str] = so.mapped_column(sa.String(18), doc="Address space SToken.")
    r725crsn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service class name.")
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, smf72sid, datetime, r725crst, r725crjn, r725crsn, r725crsp),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'smf72sid', 'datetime'],
            ['smf72_sctl_hr.smf72xnm', 'smf72_sctl_hr.smf72sid', 'smf72_sctl_hr.datetime']),
    )

    smf72_sctl_hr: so.Mapped['Smf72SctlHr'] = so.relationship(back_populates='smf72_clrd_hrs', viewonly=True)


class Smf72EnseHr(ReprMixin, Base72Hr, Smf72ense):
    """The Smf72EnseHr class stores the hourly Smf72Ense record in the smf72_ense_hr table."""

    __tablename__ = "smf72_ense_hr"
    r725enjn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Name of the job.")
    r725ensp: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service class period.")
    r725enst: so.Mapped[str] = so.mapped_column(sa.String(18), doc="Address space SToken.")
    r725ensn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service class name.")
    r725ensc: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="Enqueue scope type: Value Meaning 1 Scope = Step 2 Scope = System 3 Scope = Systems")
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    ense_index: so.Mapped[int] = so.mapped_column(sa.Integer, doc="The index of GRS Enqueue Step data")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, smf72sid, datetime, r725enst, r725enjn, r725ensn, r725ensp, r725ensc,
                                ense_index),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'smf72sid', 'datetime'],
            ['smf72_sctl_hr.smf72xnm', 'smf72_sctl_hr.smf72sid', 'smf72_sctl_hr.datetime']),
    )

    smf72_sctl_hr: so.Mapped['Smf72SctlHr'] = so.relationship(back_populates='smf72_ense_hrs', viewonly=True)


class Smf72EnsyHr(ReprMixin, Base72Hr, Smf72ense):
    """The Smf72EnsyHr class stores the hourly Smf72Ensy record in the smf72_ensy_hr table."""

    __tablename__ = "smf72_ensy_hr"
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    ensy_index: so.Mapped[int] = so.mapped_column(sa.Integer, doc="The index of GRS Enqueue System data")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    r725enst: so.Mapped[str] = so.mapped_column(sa.String(18), doc="Address space SToken.")
    r725enjn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Name of the job.")
    r725ensn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service class name.")
    r725ensp: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service class period.")
    r725ensc: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="Enqueue scope type: Value Meaning 1 Scope = Step 2 Scope = System 3 Scope = Systems")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, smf72sid, datetime, r725enst, r725enjn, r725ensn, r725ensp, r725ensc,
                                ensy_index),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'smf72sid', 'datetime'],
            ['smf72_sctl_hr.smf72xnm', 'smf72_sctl_hr.smf72sid', 'smf72_sctl_hr.datetime']),
    )

    smf72_sctl_hr: so.Mapped['Smf72SctlHr'] = so.relationship(back_populates='smf72_ensy_hrs', viewonly=True)


class Smf72LotdHr(ReprMixin, Base72Hr, Smf72lotd):
    """The Smf72LotdHr class stores the hourly Smf72Lotd record in the smf72_lotd_hr table."""

    __tablename__ = "smf72_lotd_hr"
    r725lojn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Name of the job.")
    r725losp: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service class period.")
    r725lost: so.Mapped[str] = so.mapped_column(sa.String(18), doc="Address space SToken.")
    r725losn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service class name.")
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, smf72sid, datetime, r725lost, r725lojn, r725losn, r725losp),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'smf72sid', 'datetime'],
            ['smf72_sctl_hr.smf72xnm', 'smf72_sctl_hr.smf72sid', 'smf72_sctl_hr.datetime']),
    )

    smf72_sctl_hr: so.Mapped['Smf72SctlHr'] = so.relationship(back_populates='smf72_lotd_hrs', viewonly=True)


class Smf72QsadHr(ReprMixin, Base72Hr, Smf72qsad):
    """The Smf72QsadHr class stores the hourly Smf72Qsad record in the smf72_qsad_hr table."""

    __tablename__ = "smf72_qsad_hr"
    r725qsjn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Name of the job.")
    r725qssp: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service class period.")
    r725qsst: so.Mapped[str] = so.mapped_column(sa.String(18), doc="Address space SToken.")
    r725qssn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service class name.")
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, smf72sid, datetime, r725qsst, r725qsjn, r725qssn, r725qssp),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'smf72sid', 'datetime'],
            ['smf72_sctl_hr.smf72xnm', 'smf72_sctl_hr.smf72sid', 'smf72_sctl_hr.datetime']),
    )

    smf72_sctl_hr: so.Mapped['Smf72SctlHr'] = so.relationship(back_populates='smf72_qsad_hrs', viewonly=True)


class Smf72EnssHr(ReprMixin, Base72Hr, Smf72ense):
    """The Smf72EnssHr class stores the hourly Smf72Enss record in the smf72_enss_hr table."""

    __tablename__ = "smf72_enss_hr"
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    r725enst: so.Mapped[str] = so.mapped_column(sa.String(18), doc="Address space SToken.")
    r725enjn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Name of the job.")
    r725ensn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service class name.")
    r725ensp: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service class period.")
    r725ensc: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="Enqueue scope type: Value Meaning 1 Scope = Step 2 Scope = System 3 Scope = Systems")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, smf72sid, datetime, r725enst, r725enjn, r725ensn, r725ensp, r725ensc),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'smf72sid', 'datetime'],
            ['smf72_sctl_hr.smf72xnm', 'smf72_sctl_hr.smf72sid', 'smf72_sctl_hr.datetime']),
    )

    smf72_sctl_hr: so.Mapped['Smf72SctlHr'] = so.relationship(back_populates='smf72_enss_hrs', viewonly=True)


class Smf72LareHr(ReprMixin, Base72Hr, Smf72lasc):
    """The Smf72LareHr class stores the hourly Smf72Lare record in the smf72_lare_hr table."""

    __tablename__ = "smf72_lare_hr"
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    r725last: so.Mapped[str] = so.mapped_column(sa.String(18), doc="Address space SToken.")
    r725lajn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Name of the job.")
    r725lasn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service class name.")
    r725lasp: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service class period.")
    r725laty: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="Request type: Value Meaning 1 Latch obtain requests against a latch set created by this address space 2 Latch obtain requests from this address space")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, smf72sid, datetime, r725last, r725lajn, r725lasn, r725lasp, r725laty),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'smf72sid', 'datetime'],
            ['smf72_sctl_hr.smf72xnm', 'smf72_sctl_hr.smf72sid', 'smf72_sctl_hr.datetime']),
    )

    smf72_sctl_hr: so.Mapped['Smf72SctlHr'] = so.relationship(back_populates='smf72_lare_hrs', viewonly=True)


class Smf72CsmsHr(ReprMixin, Base72Hr, Smf72cmss):
    """The Smf72CsmsHr class stores the hourly Smf72Csms record in the smf72_csms_hr table."""

    __tablename__ = "smf72_csms_hr"
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    r725cmst: so.Mapped[str] = so.mapped_column(sa.String(18), doc="Address space SToken.")
    r725cmjn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Name of the job.")
    r725cmsn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service class name.")
    r725cmsp: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service class period.")
    r725cmty: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="Lock type: Value Meaning 1 CMS lock 2 CMS Enqueue/Dequeue lock 3 CMS Latch lock 4 CMS SMF lock")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, smf72sid, datetime, r725cmst, r725cmjn, r725cmsn, r725cmsp, r725cmty),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'smf72sid', 'datetime'],
            ['smf72_sctl_hr.smf72xnm', 'smf72_sctl_hr.smf72sid', 'smf72_sctl_hr.datetime']),
    )

    smf72_sctl_hr: so.Mapped['Smf72SctlHr'] = so.relationship(back_populates='smf72_csms_hrs', viewonly=True)


class Smf72ClasHr(ReprMixin, Base72Hr, Smf72cmss):
    """The Smf72ClasHr class stores the hourly Smf72Clas record in the smf72_clas_hr table."""

    __tablename__ = "smf72_clas_hr"
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    r725cmst: so.Mapped[str] = so.mapped_column(sa.String(18), doc="Address space SToken.")
    r725cmjn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Name of the job.")
    r725cmsn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service class name.")
    r725cmsp: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service class period.")
    r725cmty: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="Lock type: Value Meaning 1 CMS lock 2 CMS Enqueue/Dequeue lock 3 CMS Latch lock 4 CMS SMF lock")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, smf72sid, datetime, r725cmst, r725cmjn, r725cmsn, r725cmsp, r725cmty),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'smf72sid', 'datetime'],
            ['smf72_sctl_hr.smf72xnm', 'smf72_sctl_hr.smf72sid', 'smf72_sctl_hr.datetime']),
    )

    smf72_sctl_hr: so.Mapped['Smf72SctlHr'] = so.relationship(back_populates='smf72_clas_hrs', viewonly=True)


class Smf72CedsHr(ReprMixin, Base72Hr, Smf72cmss):
    """The Smf72CedsHr class stores the hourly Smf72Ceds record in the smf72_ceds_hr table."""

    __tablename__ = "smf72_ceds_hr"
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    r725cmst: so.Mapped[str] = so.mapped_column(sa.String(18), doc="Address space SToken.")
    r725cmjn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Name of the job.")
    r725cmsn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service class name.")
    r725cmsp: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service class period.")
    r725cmty: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="Lock type: Value Meaning 1 CMS lock 2 CMS Enqueue/Dequeue lock 3 CMS Latch lock 4 CMS SMF lock")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, smf72sid, datetime, r725cmst, r725cmjn, r725cmsn, r725cmsp, r725cmty),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'smf72sid', 'datetime'],
            ['smf72_sctl_hr.smf72xnm', 'smf72_sctl_hr.smf72sid', 'smf72_sctl_hr.datetime']),
    )

    smf72_sctl_hr: so.Mapped['Smf72SctlHr'] = so.relationship(back_populates='smf72_ceds_hrs', viewonly=True)
