import datetime as dt
from typing import List, Optional

import sqlalchemy as sa
import sqlalchemy.orm as so

from .smf72_base import ReprMixin, Base72Da, Smf72pro, Smf72policy, Smf72wms, Smf72scs, Smf72rts, Smf72wrs, Smf72rgs, \
    Smf72data, Smf72cmss, Smf72lotd, Smf72clod, Smf72clrd, Smf72lasc, Smf72ense, Smf72qsad, Smf72sctl


class Smf72ProDa(ReprMixin, Base72Da, Smf72pro):
    """The Smf72ProDa class stores the daily Smf72Pro record in the smf72_pro_da table."""

    __tablename__ = "smf72_pro_da"
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    speed_boost: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                             doc="smf72fla (Bit 10) indcating speed boost was active during entire interval.")
    ziip_boost: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                            doc="smf72fla (Bit 9) indciating zIIP boost was active during entire interval.")
    smf_type: so.Mapped[str] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(date, smf_type, smf72xnm, smf72sid),
    )

    smf72_sctl_da: so.Mapped['Smf72SctlDa'] = so.relationship(back_populates='smf72_pro_da', viewonly=True)
    smf72_policy_da: so.Mapped['Smf72PolicyDa'] = so.relationship(back_populates='smf72_pro_das', viewonly=True,
                                                                  foreign_keys=[date, smf_type, smf72xnm],
                                                                  primaryjoin='and_(Smf72ProDa.date==Smf72PolicyDa.date, Smf72ProDa.smf_type==Smf72PolicyDa.smf_type, Smf72ProDa.smf72xnm==Smf72PolicyDa.smf72xnm)', )
    smf72_scs_das: so.Mapped[List['Smf72ScsDa']] = so.relationship(back_populates='smf72_pro_da', viewonly=True)
    smf72_data_das: so.Mapped[List['Smf72DataDa']] = so.relationship(back_populates='smf72_pro_da', viewonly=True)


class Smf72WrsDa(ReprMixin, Base72Da, Smf72wrs):
    """The Smf72WrsDa class stores the daily Smf72Wrs record in the smf72_wrs_da table."""

    __tablename__ = "smf72_wrs_da"
    r723rtyp: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="Subsystem type, as used in the classification rules specified in the WLM administrative application. The subsystem's documentation should explain the meaning that the product attributes to the various states.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    phase: so.Mapped[str] = so.mapped_column(sa.String(3),
                                             doc="states sampled in the begin_to_end phase of a transaction or in the execution phase of a transaction.")
    r723rexe: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r723rflg (Bit 1) representing states sampled in the execution phase of a transaction.")
    r723rdbe: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r723rflg (Bit 0) representing states sampled in the begin_to_end phase of a transaction.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    r723mnsp: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Policy name.")
    r723mwnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Workload name.")
    r723mcnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service/Report class name.")
    r723cper: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service or report class period number.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, date, r723mnsp, r723mwnm, r723mcnm, r723cper, smf72sid, r723rtyp, phase),

        sa.ForeignKeyConstraint(
            ['smf72xnm', 'date', 'r723mnsp', 'r723mwnm', 'r723mcnm', 'r723cper', 'smf72sid'],
            ['smf72_scs_da.smf72xnm', 'smf72_scs_da.date', 'smf72_scs_da.r723mnsp', 'smf72_scs_da.r723mwnm',
             'smf72_scs_da.r723mcnm', 'smf72_scs_da.r723cper', 'smf72_scs_da.smf72sid']),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'date', 'r723mnsp', 'r723mwnm', 'r723mcnm', 'r723cper', 'r723rtyp', 'phase'],
            ['smf72_wrsx_da.smf72xnm', 'smf72_wrsx_da.date', 'smf72_wrsx_da.r723mnsp', 'smf72_wrsx_da.r723mwnm',
             'smf72_wrsx_da.r723mcnm', 'smf72_wrsx_da.r723cper', 'smf72_wrsx_da.r723rtyp', 'smf72_wrsx_da.phase']),
    )

    smf72_scs_da: so.Mapped['Smf72ScsDa'] = so.relationship(back_populates='smf72_wrs_das', viewonly=True)
    smf72_wrsx_da: so.Mapped['Smf72WrsxDa'] = so.relationship(back_populates='smf72_wrs_das', viewonly=True)
    smf72_dns_das: so.Mapped[List['Smf72DnsDa']] = so.relationship(back_populates='smf72_wrs_da', viewonly=True)


class Smf72ScsDa(ReprMixin, Base72Da, Smf72scs, Smf72wrs):
    """The Smf72ScsDa class stores the daily Smf72Scs record in the smf72_scs_da table."""

    __tablename__ = "smf72_scs_da"
    r723cper: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service or report class period number.")
    r723cimp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Importance of the goal to be achieved for this period (1=highest, 5=lowest). The value is zero for a discretionary or system goal.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
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
    r723mnsp: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Policy name.")
    r723mwnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Workload name.")
    r723mcnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service/Report class name.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, date, r723mnsp, r723mwnm, r723mcnm, r723cper, smf72sid),

        sa.ForeignKeyConstraint(
            ['smf72xnm', 'date', 'r723mnsp', 'r723mwnm', 'r723mcnm', 'r723cper'],
            ['smf72_wms_da.smf72xnm', 'smf72_wms_da.date', 'smf72_wms_da.r723mnsp', 'smf72_wms_da.r723mwnm',
             'smf72_wms_da.r723mcnm', 'smf72_wms_da.r723cper']),
        sa.ForeignKeyConstraint(
            ['date', 'smf_type', 'smf72xnm', 'smf72sid'],
            ['smf72_pro_da.date', 'smf72_pro_da.smf_type', 'smf72_pro_da.smf72xnm', 'smf72_pro_da.smf72sid']),
    )

    smf72_rts_da: so.Mapped['Smf72RtsDa'] = so.relationship(back_populates='smf72_scs_da', viewonly=True)
    smf72_wms_da: so.Mapped['Smf72WmsDa'] = so.relationship(back_populates='smf72_scs_das', viewonly=True)
    smf72_pro_da: so.Mapped['Smf72ProDa'] = so.relationship(back_populates='smf72_scs_das', viewonly=True)
    smf72_wrs_das: so.Mapped[List['Smf72WrsDa']] = so.relationship(back_populates='smf72_scs_da', viewonly=True)


class Smf72PolicyDa(ReprMixin, Base72Da, Smf72policy):
    """The Smf72PolicyDa class stores the daily Smf72Policy record in the smf72_policy_da table."""

    __tablename__ = "smf72_policy_da"
    smf_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    interval_start_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                             doc="the start time of the interval")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    r723mnsp: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Policy name.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, date, r723mnsp),
    )

    smf72_workload_das: so.Mapped[List['Smf72WorkloadDa']] = so.relationship(back_populates='smf72_policy_da',
                                                                             viewonly=True)
    smf72_wms_das: so.Mapped[List['Smf72WmsDa']] = so.relationship(back_populates='smf72_policy_da', viewonly=True)
    smf72_rgs_das: so.Mapped[List['Smf72RgsDa']] = so.relationship(back_populates='smf72_policy_da', viewonly=True)
    smf72_pro_das: so.Mapped[List['Smf72ProDa']] = so.relationship(back_populates='smf72_policy_da', viewonly=True,
                                                                   foreign_keys='Smf72ProDa.date, Smf72ProDa.smf_type, Smf72ProDa.smf72xnm',
                                                                   primaryjoin='and_(Smf72PolicyDa.date==Smf72ProDa.date, Smf72PolicyDa.smf_type==Smf72ProDa.smf_type, Smf72PolicyDa.smf72xnm==Smf72ProDa.smf72xnm)', )


class Smf72WorkloadDa(ReprMixin, Base72Da):
    """The Smf72WorkloadDa class stores the daily Smf72Workload record in the smf72_workload_da table."""

    __tablename__ = "smf72_workload_da"
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    r723mwde: so.Mapped[Optional[str]] = so.mapped_column(sa.String(32), doc="Workload description.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    r723mnsp: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Policy name.")
    r723mwnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Workload name.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, date, r723mnsp, r723mwnm),

        sa.ForeignKeyConstraint(
            ['smf72xnm', 'date', 'r723mnsp'],
            ['smf72_policy_da.smf72xnm', 'smf72_policy_da.date', 'smf72_policy_da.r723mnsp']),
    )

    smf72_policy_da: so.Mapped['Smf72PolicyDa'] = so.relationship(back_populates='smf72_workload_das', viewonly=True)
    smf72_wms_das: so.Mapped[List['Smf72WmsDa']] = so.relationship(back_populates='smf72_workload_da', viewonly=True)


class Smf72RtsDa(ReprMixin, Base72Da, Smf72rts):
    """The Smf72RtsDa class stores the daily Smf72Rts record in the smf72_rts_da table."""

    __tablename__ = "smf72_rts_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    r723mnsp: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Policy name.")
    r723mwnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Workload name.")
    r723mcnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service/Report class name.")
    r723cper: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service or report class period number.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, date, r723mnsp, r723mwnm, r723mcnm, r723cper, smf72sid),

        sa.ForeignKeyConstraint(
            ['smf72xnm', 'date', 'r723mnsp', 'r723mwnm', 'r723mcnm', 'r723cper', 'smf72sid'],
            ['smf72_scs_da.smf72xnm', 'smf72_scs_da.date', 'smf72_scs_da.r723mnsp', 'smf72_scs_da.r723mwnm',
             'smf72_scs_da.r723mcnm', 'smf72_scs_da.r723cper', 'smf72_scs_da.smf72sid']),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'date', 'r723mnsp', 'r723mwnm', 'r723mcnm', 'r723cper'],
            ['smf72_wms_da.smf72xnm', 'smf72_wms_da.date', 'smf72_wms_da.r723mnsp', 'smf72_wms_da.r723mwnm',
             'smf72_wms_da.r723mcnm', 'smf72_wms_da.r723cper']),
    )

    smf72_scs_da: so.Mapped['Smf72ScsDa'] = so.relationship(back_populates='smf72_rts_da', viewonly=True)
    smf72_wms_da: so.Mapped['Smf72WmsDa'] = so.relationship(back_populates='smf72_rts_das', viewonly=True)


class Smf72SctlDa(ReprMixin, Base72Da, Smf72sctl):
    """The Smf72SctlDa class stores the daily Smf72Sctl record in the smf72_sctl_da table."""

    __tablename__ = "smf72_sctl_da"
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, smf72sid, date),

        sa.ForeignKeyConstraint(
            ['date', 'smf_type', 'smf72xnm', 'smf72sid'],
            ['smf72_pro_da.date', 'smf72_pro_da.smf_type', 'smf72_pro_da.smf72xnm', 'smf72_pro_da.smf72sid']),
    )

    smf72_pro_da: so.Mapped['Smf72ProDa'] = so.relationship(back_populates='smf72_sctl_da', viewonly=True)
    smf72_cmss_das: so.Mapped[List['Smf72CmssDa']] = so.relationship(back_populates='smf72_sctl_da', viewonly=True)
    smf72_ceds_das: so.Mapped[List['Smf72CedsDa']] = so.relationship(back_populates='smf72_sctl_da', viewonly=True)
    smf72_clas_das: so.Mapped[List['Smf72ClasDa']] = so.relationship(back_populates='smf72_sctl_da', viewonly=True)
    smf72_csms_das: so.Mapped[List['Smf72CsmsDa']] = so.relationship(back_populates='smf72_sctl_da', viewonly=True)
    smf72_lotd_das: so.Mapped[List['Smf72LotdDa']] = so.relationship(back_populates='smf72_sctl_da', viewonly=True)
    smf72_clod_das: so.Mapped[List['Smf72ClodDa']] = so.relationship(back_populates='smf72_sctl_da', viewonly=True)
    smf72_clrd_das: so.Mapped[List['Smf72ClrdDa']] = so.relationship(back_populates='smf72_sctl_da', viewonly=True)
    smf72_lasc_das: so.Mapped[List['Smf72LascDa']] = so.relationship(back_populates='smf72_sctl_da', viewonly=True)
    smf72_lare_das: so.Mapped[List['Smf72LareDa']] = so.relationship(back_populates='smf72_sctl_da', viewonly=True)
    smf72_ense_das: so.Mapped[List['Smf72EnseDa']] = so.relationship(back_populates='smf72_sctl_da', viewonly=True)
    smf72_ensy_das: so.Mapped[List['Smf72EnsyDa']] = so.relationship(back_populates='smf72_sctl_da', viewonly=True)
    smf72_enss_das: so.Mapped[List['Smf72EnssDa']] = so.relationship(back_populates='smf72_sctl_da', viewonly=True)
    smf72_qsad_das: so.Mapped[List['Smf72QsadDa']] = so.relationship(back_populates='smf72_sctl_da', viewonly=True)


class Smf72WmsDa(ReprMixin, Base72Da, Smf72wms, Smf72scs, Smf72rts, Smf72wrs):
    """The Smf72WmsDa class stores the daily Smf72Wms record in the smf72_wms_da table."""

    __tablename__ = "smf72_wms_da"
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
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    r723cper: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service or report class period number.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, date, r723mnsp, r723mwnm, r723mcnm, r723cper),

        sa.ForeignKeyConstraint(
            ['smf72xnm', 'date', 'r723mnsp'],
            ['smf72_policy_da.smf72xnm', 'smf72_policy_da.date', 'smf72_policy_da.r723mnsp']),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'date', 'r723mnsp', 'r723mwnm'],
            ['smf72_workload_da.smf72xnm', 'smf72_workload_da.date', 'smf72_workload_da.r723mnsp',
             'smf72_workload_da.r723mwnm']),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'date', 'r723mnsp', 'r723ggnm'],
            ['smf72_rgs_da.smf72xnm', 'smf72_rgs_da.date', 'smf72_rgs_da.r723mnsp', 'smf72_rgs_da.r723ggnm']),
    )

    smf72_policy_da: so.Mapped['Smf72PolicyDa'] = so.relationship(back_populates='smf72_wms_das', viewonly=True)
    smf72_workload_da: so.Mapped['Smf72WorkloadDa'] = so.relationship(back_populates='smf72_wms_das', viewonly=True)
    smf72_rgs_da: so.Mapped['Smf72RgsDa'] = so.relationship(back_populates='smf72_wms_das', viewonly=True)
    smf72_sss_das: so.Mapped[List['Smf72SssDa']] = so.relationship(back_populates='smf72_wms_da', viewonly=True)
    smf72_rts_das: so.Mapped[List['Smf72RtsDa']] = so.relationship(back_populates='smf72_wms_da', viewonly=True)
    smf72_scs_das: so.Mapped[List['Smf72ScsDa']] = so.relationship(back_populates='smf72_wms_da', viewonly=True)
    smf72_wrsx_das: so.Mapped[List['Smf72WrsxDa']] = so.relationship(back_populates='smf72_wms_da', viewonly=True)


class Smf72WrsxDa(ReprMixin, Base72Da, Smf72wrs):
    """The Smf72WrsxDa class stores the daily Smf72Wrsx record in the smf72_wrsx_da table."""

    __tablename__ = "smf72_wrsx_da"
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    r723rexe: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r723rflg (Bit 1) representing states sampled in the execution phase of a transaction.")
    r723rdbe: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r723rflg (Bit 0) representing states sampled in the begin_to_end phase of a transaction.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    phase: so.Mapped[str] = so.mapped_column(sa.String(3),
                                             doc="states sampled in the begin_to_end phase of a transaction or in the execution phase of a transaction.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    r723mnsp: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Policy name.")
    r723mwnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Workload name.")
    r723mcnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service/Report class name.")
    r723cper: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service or report class period number.")
    r723rtyp: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="Subsystem type, as used in the classification rules specified in the WLM administrative application. The subsystem's documentation should explain the meaning that the product attributes to the various states.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, date, r723mnsp, r723mwnm, r723mcnm, r723cper, r723rtyp, phase),

        sa.ForeignKeyConstraint(
            ['smf72xnm', 'date', 'r723mnsp', 'r723mwnm', 'r723mcnm', 'r723cper'],
            ['smf72_wms_da.smf72xnm', 'smf72_wms_da.date', 'smf72_wms_da.r723mnsp', 'smf72_wms_da.r723mwnm',
             'smf72_wms_da.r723mcnm', 'smf72_wms_da.r723cper']),
    )

    smf72_wms_da: so.Mapped['Smf72WmsDa'] = so.relationship(back_populates='smf72_wrsx_das', viewonly=True)
    smf72_dnsx_das: so.Mapped[List['Smf72DnsxDa']] = so.relationship(back_populates='smf72_wrsx_da', viewonly=True)
    smf72_wrs_das: so.Mapped[List['Smf72WrsDa']] = so.relationship(back_populates='smf72_wrsx_da', viewonly=True)


class Smf72DnsDa(ReprMixin, Base72Da):
    """The Smf72DnsDa class stores the daily Smf72Dns record in the smf72_dns_da table."""

    __tablename__ = "smf72_dns_da"
    r723dnst: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="Subsystem type as used in the classification rules specified in the WLM administrative application.")
    r723dnde: so.Mapped[str] = so.mapped_column(sa.String(16), doc="Resource delay description.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    r723rwnn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="number of the resource delay type. Values 1...15 are related to r723rw01...r723rw15 respectively.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
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
        sa.PrimaryKeyConstraint(smf72xnm, date, r723mnsp, r723mwnm, r723mcnm, r723cper, smf72sid, r723rtyp, phase,
                                r723dnst, r723dnde),

        sa.ForeignKeyConstraint(
            ['smf72xnm', 'date', 'r723mnsp', 'r723mwnm', 'r723mcnm', 'r723cper', 'smf72sid', 'r723rtyp', 'phase'],
            ['smf72_wrs_da.smf72xnm', 'smf72_wrs_da.date', 'smf72_wrs_da.r723mnsp', 'smf72_wrs_da.r723mwnm',
             'smf72_wrs_da.r723mcnm', 'smf72_wrs_da.r723cper', 'smf72_wrs_da.smf72sid', 'smf72_wrs_da.r723rtyp',
             'smf72_wrs_da.phase']),
        sa.ForeignKeyConstraint(
            ['smf72xnm', 'date', 'r723mnsp', 'r723mwnm', 'r723mcnm', 'r723cper', 'r723rtyp', 'phase', 'r723dnst',
             'r723dnde'],
            ['smf72_dnsx_da.smf72xnm', 'smf72_dnsx_da.date', 'smf72_dnsx_da.r723mnsp', 'smf72_dnsx_da.r723mwnm',
             'smf72_dnsx_da.r723mcnm', 'smf72_dnsx_da.r723cper', 'smf72_dnsx_da.r723rtyp', 'smf72_dnsx_da.phase',
             'smf72_dnsx_da.r723dnst', 'smf72_dnsx_da.r723dnde']),
    )

    smf72_wrs_da: so.Mapped['Smf72WrsDa'] = so.relationship(back_populates='smf72_dns_das', viewonly=True)
    smf72_dnsx_da: so.Mapped['Smf72DnsxDa'] = so.relationship(back_populates='smf72_dns_das', viewonly=True)


class Smf72DnsxDa(ReprMixin, Base72Da):
    """The Smf72DnsxDa class stores the daily Smf72Dnsx record in the smf72_dnsx_da table."""

    __tablename__ = "smf72_dnsx_da"
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    r723rwnn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="number of the resource delay type. Values 1...15 are related to r723rw01...r723rw15 respectively.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
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
        sa.PrimaryKeyConstraint(smf72xnm, date, r723mnsp, r723mwnm, r723mcnm, r723cper, r723rtyp, phase, r723dnst,
                                r723dnde),

        sa.ForeignKeyConstraint(
            ['smf72xnm', 'date', 'r723mnsp', 'r723mwnm', 'r723mcnm', 'r723cper', 'r723rtyp', 'phase'],
            ['smf72_wrsx_da.smf72xnm', 'smf72_wrsx_da.date', 'smf72_wrsx_da.r723mnsp', 'smf72_wrsx_da.r723mwnm',
             'smf72_wrsx_da.r723mcnm', 'smf72_wrsx_da.r723cper', 'smf72_wrsx_da.r723rtyp', 'smf72_wrsx_da.phase']),
    )

    smf72_wrsx_da: so.Mapped['Smf72WrsxDa'] = so.relationship(back_populates='smf72_dnsx_das', viewonly=True)
    smf72_dns_das: so.Mapped[List['Smf72DnsDa']] = so.relationship(back_populates='smf72_dnsx_da', viewonly=True)


class Smf72DataDa(ReprMixin, Base72Da, Smf72data):
    """The Smf72DataDa class stores the daily Smf72Data record in the smf72_data_da table."""

    __tablename__ = "smf72_data_da"
    r724pnam: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Name of active service policy.")
    r724ptm: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                 doc="Local time/date of policy activation (STCK format).")
    r724lcnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service class name.")
    r724per_: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service class period number.")
    smf_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, smf72sid, date, r724pnam, r724lcnm, r724per_),

        sa.ForeignKeyConstraint(
            ['date', 'smf_type', 'smf72xnm', 'smf72sid'],
            ['smf72_pro_da.date', 'smf72_pro_da.smf_type', 'smf72_pro_da.smf72xnm', 'smf72_pro_da.smf72sid']),
    )

    smf72_pro_da: so.Mapped['Smf72ProDa'] = so.relationship(back_populates='smf72_data_das', viewonly=True)


class Smf72RgsDa(ReprMixin, Base72Da, Smf72rgs):
    """The Smf72RgsDa class stores the daily Smf72Rgs record in the smf72_rgs_da table."""

    __tablename__ = "smf72_rgs_da"
    r723ggnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Resource group name.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    r723mnsp: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Policy name.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, date, r723mnsp, r723ggnm),

        sa.ForeignKeyConstraint(
            ['smf72xnm', 'date', 'r723mnsp'],
            ['smf72_policy_da.smf72xnm', 'smf72_policy_da.date', 'smf72_policy_da.r723mnsp']),
    )

    smf72_policy_da: so.Mapped['Smf72PolicyDa'] = so.relationship(back_populates='smf72_rgs_das', viewonly=True)
    smf72_wms_das: so.Mapped[List['Smf72WmsDa']] = so.relationship(back_populates='smf72_rgs_da', viewonly=True)


class Smf72SssDa(ReprMixin, Base72Da):
    """The Smf72SssDa class stores the daily Smf72Sss record in the smf72_sss_da table."""

    __tablename__ = "smf72_sss_da"
    r723scsn: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Name of service class being served (by one or more address spaces in service class R723MCNM).")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    r723scs_: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="number of times an address space running in service class r723mcnm was observed serving the served service class r723scsn.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    r723mnsp: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Policy name.")
    r723mwnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Workload name.")
    r723mcnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service/Report class name.")
    r723cper: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service or report class period number.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, date, r723mnsp, r723mwnm, r723mcnm, r723cper, r723scsn, smf72sid),

        sa.ForeignKeyConstraint(
            ['smf72xnm', 'date', 'r723mnsp', 'r723mwnm', 'r723mcnm', 'r723cper'],
            ['smf72_wms_da.smf72xnm', 'smf72_wms_da.date', 'smf72_wms_da.r723mnsp', 'smf72_wms_da.r723mwnm',
             'smf72_wms_da.r723mcnm', 'smf72_wms_da.r723cper']),
    )

    smf72_wms_da: so.Mapped['Smf72WmsDa'] = so.relationship(back_populates='smf72_sss_das', viewonly=True)


class Smf72CmssDa(ReprMixin, Base72Da, Smf72cmss):
    """The Smf72CmssDa class stores the daily Smf72Cmss record in the smf72_cmss_da table."""

    __tablename__ = "smf72_cmss_da"
    r725cmjn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Name of the job.")
    r725cmsp: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service class period.")
    r725cmst: so.Mapped[str] = so.mapped_column(sa.String(18), doc="Address space SToken.")
    r725cmsn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service class name.")
    r725cmty: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="Lock type: Value Meaning 1 CMS lock 2 CMS Enqueue/Dequeue lock 3 CMS Latch lock 4 CMS SMF lock")
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, smf72sid, date, r725cmst, r725cmjn, r725cmsn, r725cmsp, r725cmty),

        sa.ForeignKeyConstraint(
            ['smf72xnm', 'smf72sid', 'date'],
            ['smf72_sctl_da.smf72xnm', 'smf72_sctl_da.smf72sid', 'smf72_sctl_da.date']),
    )

    smf72_sctl_da: so.Mapped['Smf72SctlDa'] = so.relationship(back_populates='smf72_cmss_das', viewonly=True)


class Smf72LascDa(ReprMixin, Base72Da, Smf72lasc):
    """The Smf72LascDa class stores the daily Smf72Lasc record in the smf72_lasc_da table."""

    __tablename__ = "smf72_lasc_da"
    r725lajn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Name of the job.")
    r725lasp: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service class period.")
    r725last: so.Mapped[str] = so.mapped_column(sa.String(18), doc="Address space SToken.")
    r725lasn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service class name.")
    r725laty: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="Request type: Value Meaning 1 Latch obtain requests against a latch set created by this address space 2 Latch obtain requests from this address space")
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, smf72sid, date, r725last, r725lajn, r725lasn, r725lasp, r725laty),

        sa.ForeignKeyConstraint(
            ['smf72xnm', 'smf72sid', 'date'],
            ['smf72_sctl_da.smf72xnm', 'smf72_sctl_da.smf72sid', 'smf72_sctl_da.date']),
    )

    smf72_sctl_da: so.Mapped['Smf72SctlDa'] = so.relationship(back_populates='smf72_lasc_das', viewonly=True)


class Smf72ClodDa(ReprMixin, Base72Da, Smf72clod):
    """The Smf72ClodDa class stores the daily Smf72Clod record in the smf72_clod_da table."""

    __tablename__ = "smf72_clod_da"
    r725cojn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Name of the job.")
    r725cosp: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service class period.")
    r725cost: so.Mapped[str] = so.mapped_column(sa.String(18), doc="Address space SToken.")
    r725cosn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service class name.")
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, smf72sid, date, r725cost, r725cojn, r725cosn, r725cosp),

        sa.ForeignKeyConstraint(
            ['smf72xnm', 'smf72sid', 'date'],
            ['smf72_sctl_da.smf72xnm', 'smf72_sctl_da.smf72sid', 'smf72_sctl_da.date']),
    )

    smf72_sctl_da: so.Mapped['Smf72SctlDa'] = so.relationship(back_populates='smf72_clod_das', viewonly=True)


class Smf72ClrdDa(ReprMixin, Base72Da, Smf72clrd):
    """The Smf72ClrdDa class stores the daily Smf72Clrd record in the smf72_clrd_da table."""

    __tablename__ = "smf72_clrd_da"
    r725crjn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Name of the job.")
    r725crsp: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service class period.")
    r725crst: so.Mapped[str] = so.mapped_column(sa.String(18), doc="Address space SToken.")
    r725crsn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service class name.")
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, smf72sid, date, r725crst, r725crjn, r725crsn, r725crsp),

        sa.ForeignKeyConstraint(
            ['smf72xnm', 'smf72sid', 'date'],
            ['smf72_sctl_da.smf72xnm', 'smf72_sctl_da.smf72sid', 'smf72_sctl_da.date']),
    )

    smf72_sctl_da: so.Mapped['Smf72SctlDa'] = so.relationship(back_populates='smf72_clrd_das', viewonly=True)


class Smf72EnseDa(ReprMixin, Base72Da, Smf72ense):
    """The Smf72EnseDa class stores the daily Smf72Ense record in the smf72_ense_da table."""

    __tablename__ = "smf72_ense_da"
    r725enjn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Name of the job.")
    r725ensp: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service class period.")
    r725enst: so.Mapped[str] = so.mapped_column(sa.String(18), doc="Address space SToken.")
    r725ensn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service class name.")
    r725ensc: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="Enqueue scope type: Value Meaning 1 Scope = Step 2 Scope = System 3 Scope = Systems")
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    ense_index: so.Mapped[int] = so.mapped_column(sa.Integer, doc="The index of GRS Enqueue Step data")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, smf72sid, date, r725enst, r725enjn, r725ensn, r725ensp, r725ensc, ense_index),

        sa.ForeignKeyConstraint(
            ['smf72xnm', 'smf72sid', 'date'],
            ['smf72_sctl_da.smf72xnm', 'smf72_sctl_da.smf72sid', 'smf72_sctl_da.date']),
    )

    smf72_sctl_da: so.Mapped['Smf72SctlDa'] = so.relationship(back_populates='smf72_ense_das', viewonly=True)


class Smf72EnsyDa(ReprMixin, Base72Da, Smf72ense):
    """The Smf72EnsyDa class stores the daily Smf72Ensy record in the smf72_ensy_da table."""

    __tablename__ = "smf72_ensy_da"
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    ensy_index: so.Mapped[int] = so.mapped_column(sa.Integer, doc="The index of GRS Enqueue System data")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    r725enst: so.Mapped[str] = so.mapped_column(sa.String(18), doc="Address space SToken.")
    r725enjn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Name of the job.")
    r725ensn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service class name.")
    r725ensp: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service class period.")
    r725ensc: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="Enqueue scope type: Value Meaning 1 Scope = Step 2 Scope = System 3 Scope = Systems")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, smf72sid, date, r725enst, r725enjn, r725ensn, r725ensp, r725ensc, ensy_index),

        sa.ForeignKeyConstraint(
            ['smf72xnm', 'smf72sid', 'date'],
            ['smf72_sctl_da.smf72xnm', 'smf72_sctl_da.smf72sid', 'smf72_sctl_da.date']),
    )

    smf72_sctl_da: so.Mapped['Smf72SctlDa'] = so.relationship(back_populates='smf72_ensy_das', viewonly=True)


class Smf72LotdDa(ReprMixin, Base72Da, Smf72lotd):
    """The Smf72LotdDa class stores the daily Smf72Lotd record in the smf72_lotd_da table."""

    __tablename__ = "smf72_lotd_da"
    r725lojn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Name of the job.")
    r725losp: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service class period.")
    r725lost: so.Mapped[str] = so.mapped_column(sa.String(18), doc="Address space SToken.")
    r725losn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service class name.")
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, smf72sid, date, r725lost, r725lojn, r725losn, r725losp),

        sa.ForeignKeyConstraint(
            ['smf72xnm', 'smf72sid', 'date'],
            ['smf72_sctl_da.smf72xnm', 'smf72_sctl_da.smf72sid', 'smf72_sctl_da.date']),
    )

    smf72_sctl_da: so.Mapped['Smf72SctlDa'] = so.relationship(back_populates='smf72_lotd_das', viewonly=True)


class Smf72QsadDa(ReprMixin, Base72Da, Smf72qsad):
    """The Smf72QsadDa class stores the daily Smf72Qsad record in the smf72_qsad_da table."""

    __tablename__ = "smf72_qsad_da"
    r725qsjn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Name of the job.")
    r725qssp: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service class period.")
    r725qsst: so.Mapped[str] = so.mapped_column(sa.String(18), doc="Address space SToken.")
    r725qssn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service class name.")
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, smf72sid, date, r725qsst, r725qsjn, r725qssn, r725qssp),

        sa.ForeignKeyConstraint(
            ['smf72xnm', 'smf72sid', 'date'],
            ['smf72_sctl_da.smf72xnm', 'smf72_sctl_da.smf72sid', 'smf72_sctl_da.date']),
    )

    smf72_sctl_da: so.Mapped['Smf72SctlDa'] = so.relationship(back_populates='smf72_qsad_das', viewonly=True)


class Smf72EnssDa(ReprMixin, Base72Da, Smf72ense):
    """The Smf72EnssDa class stores the daily Smf72Enss record in the smf72_enss_da table."""

    __tablename__ = "smf72_enss_da"
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    r725enst: so.Mapped[str] = so.mapped_column(sa.String(18), doc="Address space SToken.")
    r725enjn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Name of the job.")
    r725ensn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service class name.")
    r725ensp: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service class period.")
    r725ensc: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="Enqueue scope type: Value Meaning 1 Scope = Step 2 Scope = System 3 Scope = Systems")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, smf72sid, date, r725enst, r725enjn, r725ensn, r725ensp, r725ensc),

        sa.ForeignKeyConstraint(
            ['smf72xnm', 'smf72sid', 'date'],
            ['smf72_sctl_da.smf72xnm', 'smf72_sctl_da.smf72sid', 'smf72_sctl_da.date']),
    )

    smf72_sctl_da: so.Mapped['Smf72SctlDa'] = so.relationship(back_populates='smf72_enss_das', viewonly=True)


class Smf72LareDa(ReprMixin, Base72Da, Smf72lasc):
    """The Smf72LareDa class stores the daily Smf72Lare record in the smf72_lare_da table."""

    __tablename__ = "smf72_lare_da"
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    r725last: so.Mapped[str] = so.mapped_column(sa.String(18), doc="Address space SToken.")
    r725lajn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Name of the job.")
    r725lasn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service class name.")
    r725lasp: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service class period.")
    r725laty: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="Request type: Value Meaning 1 Latch obtain requests against a latch set created by this address space 2 Latch obtain requests from this address space")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, smf72sid, date, r725last, r725lajn, r725lasn, r725lasp, r725laty),

        sa.ForeignKeyConstraint(
            ['smf72xnm', 'smf72sid', 'date'],
            ['smf72_sctl_da.smf72xnm', 'smf72_sctl_da.smf72sid', 'smf72_sctl_da.date']),
    )

    smf72_sctl_da: so.Mapped['Smf72SctlDa'] = so.relationship(back_populates='smf72_lare_das', viewonly=True)


class Smf72CsmsDa(ReprMixin, Base72Da, Smf72cmss):
    """The Smf72CsmsDa class stores the daily Smf72Csms record in the smf72_csms_da table."""

    __tablename__ = "smf72_csms_da"
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    r725cmst: so.Mapped[str] = so.mapped_column(sa.String(18), doc="Address space SToken.")
    r725cmjn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Name of the job.")
    r725cmsn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service class name.")
    r725cmsp: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service class period.")
    r725cmty: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="Lock type: Value Meaning 1 CMS lock 2 CMS Enqueue/Dequeue lock 3 CMS Latch lock 4 CMS SMF lock")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, smf72sid, date, r725cmst, r725cmjn, r725cmsn, r725cmsp, r725cmty),

        sa.ForeignKeyConstraint(
            ['smf72xnm', 'smf72sid', 'date'],
            ['smf72_sctl_da.smf72xnm', 'smf72_sctl_da.smf72sid', 'smf72_sctl_da.date']),
    )

    smf72_sctl_da: so.Mapped['Smf72SctlDa'] = so.relationship(back_populates='smf72_csms_das', viewonly=True)


class Smf72ClasDa(ReprMixin, Base72Da, Smf72cmss):
    """The Smf72ClasDa class stores the daily Smf72Clas record in the smf72_clas_da table."""

    __tablename__ = "smf72_clas_da"
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    r725cmst: so.Mapped[str] = so.mapped_column(sa.String(18), doc="Address space SToken.")
    r725cmjn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Name of the job.")
    r725cmsn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service class name.")
    r725cmsp: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service class period.")
    r725cmty: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="Lock type: Value Meaning 1 CMS lock 2 CMS Enqueue/Dequeue lock 3 CMS Latch lock 4 CMS SMF lock")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, smf72sid, date, r725cmst, r725cmjn, r725cmsn, r725cmsp, r725cmty),

        sa.ForeignKeyConstraint(
            ['smf72xnm', 'smf72sid', 'date'],
            ['smf72_sctl_da.smf72xnm', 'smf72_sctl_da.smf72sid', 'smf72_sctl_da.date']),
    )

    smf72_sctl_da: so.Mapped['Smf72SctlDa'] = so.relationship(back_populates='smf72_clas_das', viewonly=True)


class Smf72CedsDa(ReprMixin, Base72Da, Smf72cmss):
    """The Smf72CedsDa class stores the daily Smf72Ceds record in the smf72_ceds_da table."""

    __tablename__ = "smf72_ceds_da"
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smf72xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf72sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    r725cmst: so.Mapped[str] = so.mapped_column(sa.String(18), doc="Address space SToken.")
    r725cmjn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Name of the job.")
    r725cmsn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Service class name.")
    r725cmsp: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Service class period.")
    r725cmty: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="Lock type: Value Meaning 1 CMS lock 2 CMS Enqueue/Dequeue lock 3 CMS Latch lock 4 CMS SMF lock")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf72xnm, smf72sid, date, r725cmst, r725cmjn, r725cmsn, r725cmsp, r725cmty),

        sa.ForeignKeyConstraint(
            ['smf72xnm', 'smf72sid', 'date'],
            ['smf72_sctl_da.smf72xnm', 'smf72_sctl_da.smf72sid', 'smf72_sctl_da.date']),
    )

    smf72_sctl_da: so.Mapped['Smf72SctlDa'] = so.relationship(back_populates='smf72_ceds_das', viewonly=True)
