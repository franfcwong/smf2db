from typing import List, Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
import datetime as dt
from .smf70_base import ReprMixin, Base70Hr, Smf70pro, Smf70ctl, Smf70aid, Smf70cpu, Smf70bct, Smf70bpd, Smf70trg, \
    Smf70ccf, Smf70typ3, Smf70typ4, Smf70typ5, Smf70wc


class Smf70ProHr(ReprMixin, Base70Hr, Smf70pro):
    """The Smf70ProHr class stores the hourly Smf70Pro record in the smf70_pro_hr table."""

    __tablename__ = "smf70_pro_hr"
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    speed_boost: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                             doc="smf70fla (Bit 10) indcating speed boost was active during entire interval.")
    ziip_boost: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                            doc="smf70fla (Bit 9) indciating zIIP boost was active during entire interval.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf_type: so.Mapped[str] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf70sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(datetime, smf_type, csc, smf70sid),
    )

    smf70_ctl_hr: so.Mapped['Smf70CtlHr'] = so.relationship(back_populates='smf70_pro_hr', viewonly=True)
    smf70_ccf_hr: so.Mapped['Smf70CcfHr'] = so.relationship(back_populates='smf70_pro_hr', viewonly=True)
    smf70_typ3_hrs: so.Mapped[List['Smf70Typ3Hr']] = so.relationship(back_populates='smf70_pro_hr', viewonly=True)
    smf70_typ4_hrs: so.Mapped[List['Smf70Typ4Hr']] = so.relationship(back_populates='smf70_pro_hr', viewonly=True)
    smf70_typ5_hrs: so.Mapped[List['Smf70Typ5Hr']] = so.relationship(back_populates='smf70_pro_hr', viewonly=True)


class Smf70CtlHr(ReprMixin, Base70Hr, Smf70ctl):
    """The Smf70CtlHr class stores the hourly Smf70Ctl record in the smf70_ctl_hr table."""

    __tablename__ = "smf70_ctl_hr"
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf70sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf70sid, datetime),
        sa.ForeignKeyConstraint(
            ['datetime', 'smf_type', 'csc', 'smf70sid'],
            ['smf70_pro_hr.datetime', 'smf70_pro_hr.smf_type', 'smf70_pro_hr.csc', 'smf70_pro_hr.smf70sid']),
    )

    smf70_pro_hr: so.Mapped['Smf70ProHr'] = so.relationship(back_populates='smf70_ctl_hr', viewonly=True)
    smf70_aid_hr: so.Mapped['Smf70AidHr'] = so.relationship(back_populates='smf70_ctl_hr', viewonly=True)
    smf70_cpu_hrs: so.Mapped[List['Smf70CpuHr']] = so.relationship(back_populates='smf70_ctl_hr', viewonly=True)
    smf70_bct_hrs: so.Mapped[List['Smf70BctHr']] = so.relationship(back_populates='smf70_ctl_hr', viewonly=True)
    smf70_trg_hrs: so.Mapped[List['Smf70TrgHr']] = so.relationship(back_populates='smf70_ctl_hr', viewonly=True)
    smf70_wc_hrs: so.Mapped[List['Smf70WcHr']] = so.relationship(back_populates='smf70_ctl_hr', viewonly=True)


class Smf70AidHr(ReprMixin, Base70Hr, Smf70aid):
    """The Smf70AidHr class stores the hourly Smf70Aid record in the smf70_aid_hr table."""

    __tablename__ = "smf70_aid_hr"
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf70sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf70sid, datetime),
        sa.ForeignKeyConstraint(
            ['csc', 'smf70sid', 'datetime'],
            ['smf70_ctl_hr.csc', 'smf70_ctl_hr.smf70sid', 'smf70_ctl_hr.datetime']),
    )

    smf70_ctl_hr: so.Mapped['Smf70CtlHr'] = so.relationship(back_populates='smf70_aid_hr', viewonly=True)


class Smf70CpuHr(ReprMixin, Base70Hr, Smf70cpu):
    """The Smf70CpuHr class stores the hourly Smf70Cpu record in the smf70_cpu_hr table."""

    __tablename__ = "smf70_cpu_hr"
    smf70cid: so.Mapped[int] = so.mapped_column(sa.Integer, doc="CPU identification")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf70sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf70sid, datetime, smf70cid),
        sa.ForeignKeyConstraint(
            ['csc', 'smf70sid', 'datetime'],
            ['smf70_ctl_hr.csc', 'smf70_ctl_hr.smf70sid', 'smf70_ctl_hr.datetime']),
    )

    smf70_ctl_hr: so.Mapped['Smf70CtlHr'] = so.relationship(back_populates='smf70_cpu_hrs', viewonly=True)


class Smf70Typ3Hr(ReprMixin, Base70Hr, Smf70typ3):
    """The Smf70Typ3Hr class stores the hourly Smf70Typ3 record in the smf70_typ3_hr table."""

    __tablename__ = "smf70_typ3_hr"
    r7023ax: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Crypto processor index.")
    r7023scope: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                  doc="Specifies the scope of the cryptographic CCA coprocessor data section. Value Meaning 0 Data with CPC scope 1 Data with System scope")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf70sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf70sid, datetime, r7023ax, r7023scope),
        sa.ForeignKeyConstraint(
            ['datetime', 'smf_type', 'csc', 'smf70sid'],
            ['smf70_pro_hr.datetime', 'smf70_pro_hr.smf_type', 'smf70_pro_hr.csc', 'smf70_pro_hr.smf70sid']),
    )

    smf70_pro_hr: so.Mapped['Smf70ProHr'] = so.relationship(back_populates='smf70_typ3_hrs', viewonly=True)


class Smf70Typ4Hr(ReprMixin, Base70Hr, Smf70typ4):
    """The Smf70Typ4Hr class stores the hourly Smf70Typ4 record in the smf70_typ4_hr table."""

    __tablename__ = "smf70_typ4_hr"
    r7024ax: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Crypto processor index.")
    r7024scope: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                  doc="Specifies the scope of the cryptographic accelerator data section. Value Meaning 0 Data with CPC scope 1")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf70sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf70sid, datetime, r7024ax, r7024scope),
        sa.ForeignKeyConstraint(
            ['datetime', 'smf_type', 'csc', 'smf70sid'],
            ['smf70_pro_hr.datetime', 'smf70_pro_hr.smf_type', 'smf70_pro_hr.csc', 'smf70_pro_hr.smf70sid']),
    )

    smf70_pro_hr: so.Mapped['Smf70ProHr'] = so.relationship(back_populates='smf70_typ4_hrs', viewonly=True)


class Smf70Typ5Hr(ReprMixin, Base70Hr, Smf70typ5):
    """The Smf70Typ5Hr class stores the hourly Smf70Typ5 record in the smf70_typ5_hr table."""

    __tablename__ = "smf70_typ5_hr"
    r7025ax: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Crypto processor index.")
    r7025scope: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                  doc="Specifies the scope of the cryptographic PKCS11 coprocessor data section. Value Meaning 0 Data with CPC scope 1 Data with System scope")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf70sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf70sid, datetime, r7025ax, r7025scope),
        sa.ForeignKeyConstraint(
            ['datetime', 'smf_type', 'csc', 'smf70sid'],
            ['smf70_pro_hr.datetime', 'smf70_pro_hr.smf_type', 'smf70_pro_hr.csc', 'smf70_pro_hr.smf70sid']),
    )

    smf70_pro_hr: so.Mapped['Smf70ProHr'] = so.relationship(back_populates='smf70_typ5_hrs', viewonly=True)


class Smf70CcfHr(ReprMixin, Base70Hr, Smf70ccf):
    """The Smf70CcfHr class stores the hourly Smf70Ccf record in the smf70_ccf_hr table."""

    __tablename__ = "smf70_ccf_hr"
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf70sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf70sid, datetime),
        sa.ForeignKeyConstraint(
            ['datetime', 'smf_type', 'csc', 'smf70sid'],
            ['smf70_pro_hr.datetime', 'smf70_pro_hr.smf_type', 'smf70_pro_hr.csc', 'smf70_pro_hr.smf70sid']),
    )

    smf70_pro_hr: so.Mapped['Smf70ProHr'] = so.relationship(back_populates='smf70_ccf_hr', viewonly=True)


class Smf70BpdHr(ReprMixin, Base70Hr, Smf70bpd):
    """The Smf70BpdHr class stores the hourly Smf70Bpd record in the smf70_bpd_hr table."""

    __tablename__ = "smf70_bpd_hr"
    smf70vpa: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Logical processor address.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
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
    smf70sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, lpar_system_name, lpar_number, datetime, smf70sid, smf70vpa),
        sa.ForeignKeyConstraint(
            ['csc', 'lpar_system_name', 'lpar_number', 'datetime', 'smf70sid', 'smf70cix'],
            ['smf70_bct_cpu_hr.csc', 'smf70_bct_cpu_hr.lpar_system_name', 'smf70_bct_cpu_hr.lpar_number',
             'smf70_bct_cpu_hr.datetime', 'smf70_bct_cpu_hr.smf70sid', 'smf70_bct_cpu_hr.smf70cix']),
    )

    smf70_bct_cpu_hr: so.Mapped['Smf70BctCpuHr'] = so.relationship(back_populates='smf70_bpd_hrs', viewonly=True)


class Smf70BctHr(ReprMixin, Base70Hr, Smf70bct):
    """The Smf70BctHr class stores the hourly Smf70Bct record in the smf70_bct_hr table."""

    __tablename__ = "smf70_bct_hr"
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    lpar_system_name: so.Mapped[str] = so.mapped_column(sa.String(17),
                                                        doc="combining lpar long name with lpar short name.")
    lpar_number: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                   doc="PR/SM partition number of the partition that wrote this record.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf70sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, lpar_system_name, lpar_number, datetime, smf70sid),
        sa.ForeignKeyConstraint(
            ['csc', 'smf70sid', 'datetime'],
            ['smf70_ctl_hr.csc', 'smf70_ctl_hr.smf70sid', 'smf70_ctl_hr.datetime']),
    )

    smf70_ctl_hr: so.Mapped['Smf70CtlHr'] = so.relationship(back_populates='smf70_bct_hrs', viewonly=True)
    smf70_bct_cpu_hrs: so.Mapped[List['Smf70BctCpuHr']] = so.relationship(back_populates='smf70_bct_hr', viewonly=True)


class Smf70TrgHr(ReprMixin, Base70Hr, Smf70trg):
    """The Smf70TrgHr class stores the hourly Smf70Trg record in the smf70_trg_hr table."""

    __tablename__ = "smf70_trg_hr"
    smf70_trg_name: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Tenant resource group name.")
    smf70_trg_tntid: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Tenant identifier.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf70sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf70sid, datetime, smf70_trg_name, smf70_trg_tntid),
        sa.ForeignKeyConstraint(
            ['csc', 'smf70sid', 'datetime'],
            ['smf70_ctl_hr.csc', 'smf70_ctl_hr.smf70sid', 'smf70_ctl_hr.datetime']),
    )

    smf70_ctl_hr: so.Mapped['Smf70CtlHr'] = so.relationship(back_populates='smf70_trg_hrs', viewonly=True)


class Smf70WcHr(ReprMixin, Base70Hr, Smf70wc):
    """The Smf70WcHr class stores the hourly Smf70Wc record in the smf70_wc_hr table."""

    __tablename__ = "smf70_wc_hr"
    smf70wc_cpu_type: so.Mapped[int] = so.mapped_column(sa.Integer, doc="CPU type as defined by SMF70TYP.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf70sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf70sid, datetime, smf70wc_cpu_type),
        sa.ForeignKeyConstraint(
            ['csc', 'smf70sid', 'datetime'],
            ['smf70_ctl_hr.csc', 'smf70_ctl_hr.smf70sid', 'smf70_ctl_hr.datetime']),
    )

    smf70_ctl_hr: so.Mapped['Smf70CtlHr'] = so.relationship(back_populates='smf70_wc_hrs', viewonly=True)


class Smf70BctCpuHr(ReprMixin, Base70Hr, Smf70bpd):
    """The Smf70BctCpuHr class stores the hourly Smf70BctCpu record in the smf70_bct_cpu_hr table."""

    __tablename__ = "smf70_bct_cpu_hr"
    smf70cix: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="EBCDIC name corresponding to the CPU type of the logical processor in CPU-identification name section.")
    wait_completion_status: so.Mapped[Optional[str]] = so.mapped_column(sa.String(3),
                                                                        doc="the wait completion is enabled of this processor.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
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
    smf70sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, lpar_system_name, lpar_number, datetime, smf70sid, smf70cix),
        sa.ForeignKeyConstraint(
            ['csc', 'lpar_system_name', 'lpar_number', 'datetime', 'smf70sid'],
            ['smf70_bct_hr.csc', 'smf70_bct_hr.lpar_system_name', 'smf70_bct_hr.lpar_number', 'smf70_bct_hr.datetime',
             'smf70_bct_hr.smf70sid']),
    )

    smf70_bct_hr: so.Mapped['Smf70BctHr'] = so.relationship(back_populates='smf70_bct_cpu_hrs', viewonly=True)
    smf70_bpd_hrs: so.Mapped[List['Smf70BpdHr']] = so.relationship(back_populates='smf70_bct_cpu_hr', viewonly=True)
