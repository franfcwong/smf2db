from typing import List, Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
import datetime as dt
from .smf70_base import ReprMixin, Base70Da, Smf70pro, Smf70ctl, Smf70aid, Smf70cpu, Smf70bct, Smf70bpd, Smf70trg, \
    Smf70ccf, Smf70typ3, Smf70typ4, Smf70typ5, Smf70wc


class Smf70ProDa(ReprMixin, Base70Da, Smf70pro):
    """The Smf70ProDa class stores the daily Smf70Pro record in the smf70_pro_da table."""

    __tablename__ = "smf70_pro_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    speed_boost: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                             doc="smf70fla (Bit 10) indcating speed boost was active during entire interval.")
    ziip_boost: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                            doc="smf70fla (Bit 9) indciating zIIP boost was active during entire interval.")
    smf_type: so.Mapped[str] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf70sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(date, smf_type, csc, smf70sid),
    )

    smf70_ctl_da: so.Mapped['Smf70CtlDa'] = so.relationship(back_populates='smf70_pro_da', viewonly=True)
    smf70_ccf_da: so.Mapped['Smf70CcfDa'] = so.relationship(back_populates='smf70_pro_da', viewonly=True)
    smf70_typ3_das: so.Mapped[List['Smf70Typ3Da']] = so.relationship(back_populates='smf70_pro_da', viewonly=True)
    smf70_typ4_das: so.Mapped[List['Smf70Typ4Da']] = so.relationship(back_populates='smf70_pro_da', viewonly=True)
    smf70_typ5_das: so.Mapped[List['Smf70Typ5Da']] = so.relationship(back_populates='smf70_pro_da', viewonly=True)


class Smf70CtlDa(ReprMixin, Base70Da, Smf70ctl):
    """The Smf70CtlDa class stores the daily Smf70Ctl record in the smf70_ctl_da table."""

    __tablename__ = "smf70_ctl_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf70sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf70sid, date),

        sa.ForeignKeyConstraint(
            ['date', 'smf_type', 'csc', 'smf70sid'],
            ['smf70_pro_da.date', 'smf70_pro_da.smf_type', 'smf70_pro_da.csc', 'smf70_pro_da.smf70sid']),
    )

    smf70_pro_da: so.Mapped['Smf70ProDa'] = so.relationship(back_populates='smf70_ctl_da', viewonly=True)
    smf70_aid_da: so.Mapped['Smf70AidDa'] = so.relationship(back_populates='smf70_ctl_da', viewonly=True)
    smf70_cpu_das: so.Mapped[List['Smf70CpuDa']] = so.relationship(back_populates='smf70_ctl_da', viewonly=True)
    smf70_bct_das: so.Mapped[List['Smf70BctDa']] = so.relationship(back_populates='smf70_ctl_da', viewonly=True)
    smf70_trg_das: so.Mapped[List['Smf70TrgDa']] = so.relationship(back_populates='smf70_ctl_da', viewonly=True)
    smf70_wc_das: so.Mapped[List['Smf70WcDa']] = so.relationship(back_populates='smf70_ctl_da', viewonly=True)


class Smf70AidDa(ReprMixin, Base70Da, Smf70aid):
    """The Smf70AidDa class stores the daily Smf70Aid record in the smf70_aid_da table."""

    __tablename__ = "smf70_aid_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf70sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf70sid, date),

        sa.ForeignKeyConstraint(
            ['csc', 'smf70sid', 'date'],
            ['smf70_ctl_da.csc', 'smf70_ctl_da.smf70sid', 'smf70_ctl_da.date']),
    )

    smf70_ctl_da: so.Mapped['Smf70CtlDa'] = so.relationship(back_populates='smf70_aid_da', viewonly=True)


class Smf70CpuDa(ReprMixin, Base70Da, Smf70cpu):
    """The Smf70CpuDa class stores the daily Smf70Cpu record in the smf70_cpu_da table."""

    __tablename__ = "smf70_cpu_da"
    smf70cid: so.Mapped[int] = so.mapped_column(sa.Integer, doc="CPU identification")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf70sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf70sid, date, smf70cid),

        sa.ForeignKeyConstraint(
            ['csc', 'smf70sid', 'date'],
            ['smf70_ctl_da.csc', 'smf70_ctl_da.smf70sid', 'smf70_ctl_da.date']),
    )

    smf70_ctl_da: so.Mapped['Smf70CtlDa'] = so.relationship(back_populates='smf70_cpu_das', viewonly=True)


class Smf70Typ3Da(ReprMixin, Base70Da, Smf70typ3):
    """The Smf70Typ3Da class stores the daily Smf70Typ3 record in the smf70_typ3_da table."""

    __tablename__ = "smf70_typ3_da"
    r7023ax: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Crypto processor index.")
    r7023scope: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                  doc="Specifies the scope of the cryptographic CCA coprocessor data section. Value Meaning 0 Data with CPC scope 1 Data with System scope")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf70sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf70sid, date, r7023ax, r7023scope),

        sa.ForeignKeyConstraint(
            ['date', 'smf_type', 'csc', 'smf70sid'],
            ['smf70_pro_da.date', 'smf70_pro_da.smf_type', 'smf70_pro_da.csc', 'smf70_pro_da.smf70sid']),
    )

    smf70_pro_da: so.Mapped['Smf70ProDa'] = so.relationship(back_populates='smf70_typ3_das', viewonly=True)


class Smf70Typ4Da(ReprMixin, Base70Da, Smf70typ4):
    """The Smf70Typ4Da class stores the daily Smf70Typ4 record in the smf70_typ4_da table."""

    __tablename__ = "smf70_typ4_da"
    r7024ax: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Crypto processor index.")
    r7024scope: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                  doc="Specifies the scope of the cryptographic accelerator data section. Value Meaning 0 Data with CPC scope 1")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf70sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf70sid, date, r7024ax, r7024scope),

        sa.ForeignKeyConstraint(
            ['date', 'smf_type', 'csc', 'smf70sid'],
            ['smf70_pro_da.date', 'smf70_pro_da.smf_type', 'smf70_pro_da.csc', 'smf70_pro_da.smf70sid']),
    )

    smf70_pro_da: so.Mapped['Smf70ProDa'] = so.relationship(back_populates='smf70_typ4_das', viewonly=True)


class Smf70Typ5Da(ReprMixin, Base70Da, Smf70typ5):
    """The Smf70Typ5Da class stores the daily Smf70Typ5 record in the smf70_typ5_da table."""

    __tablename__ = "smf70_typ5_da"
    r7025ax: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Crypto processor index.")
    r7025scope: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                  doc="Specifies the scope of the cryptographic PKCS11 coprocessor data section. Value Meaning 0 Data with CPC scope 1 Data with System scope")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf70sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf70sid, date, r7025ax, r7025scope),

        sa.ForeignKeyConstraint(
            ['date', 'smf_type', 'csc', 'smf70sid'],
            ['smf70_pro_da.date', 'smf70_pro_da.smf_type', 'smf70_pro_da.csc', 'smf70_pro_da.smf70sid']),
    )

    smf70_pro_da: so.Mapped['Smf70ProDa'] = so.relationship(back_populates='smf70_typ5_das', viewonly=True)


class Smf70CcfDa(ReprMixin, Base70Da, Smf70ccf):
    """The Smf70CcfDa class stores the daily Smf70Ccf record in the smf70_ccf_da table."""

    __tablename__ = "smf70_ccf_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf70sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf70sid, date),

        sa.ForeignKeyConstraint(
            ['date', 'smf_type', 'csc', 'smf70sid'],
            ['smf70_pro_da.date', 'smf70_pro_da.smf_type', 'smf70_pro_da.csc', 'smf70_pro_da.smf70sid']),
    )

    smf70_pro_da: so.Mapped['Smf70ProDa'] = so.relationship(back_populates='smf70_ccf_da', viewonly=True)


class Smf70BpdDa(ReprMixin, Base70Da, Smf70bpd):
    """The Smf70BpdDa class stores the daily Smf70Bpd record in the smf70_bpd_da table."""

    __tablename__ = "smf70_bpd_da"
    smf70vpa: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Logical processor address.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
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
    smf70sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, lpar_system_name, lpar_number, date, smf70sid, smf70vpa),

        sa.ForeignKeyConstraint(
            ['csc', 'lpar_system_name', 'lpar_number', 'date', 'smf70sid', 'smf70cix'],
            ['smf70_bct_cpu_da.csc', 'smf70_bct_cpu_da.lpar_system_name', 'smf70_bct_cpu_da.lpar_number',
             'smf70_bct_cpu_da.date', 'smf70_bct_cpu_da.smf70sid', 'smf70_bct_cpu_da.smf70cix']),
    )

    smf70_bct_cpu_da: so.Mapped['Smf70BctCpuDa'] = so.relationship(back_populates='smf70_bpd_das', viewonly=True)


class Smf70BctDa(ReprMixin, Base70Da, Smf70bct):
    """The Smf70BctDa class stores the daily Smf70Bct record in the smf70_bct_da table."""

    __tablename__ = "smf70_bct_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    lpar_system_name: so.Mapped[str] = so.mapped_column(sa.String(17),
                                                        doc="combining lpar long name with lpar short name.")
    lpar_number: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                   doc="PR/SM partition number of the partition that wrote this record.")
    smf70sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, lpar_system_name, lpar_number, date, smf70sid),

        sa.ForeignKeyConstraint(
            ['csc', 'smf70sid', 'date'],
            ['smf70_ctl_da.csc', 'smf70_ctl_da.smf70sid', 'smf70_ctl_da.date']),
    )

    smf70_ctl_da: so.Mapped['Smf70CtlDa'] = so.relationship(back_populates='smf70_bct_das', viewonly=True)
    smf70_bct_cpu_das: so.Mapped[List['Smf70BctCpuDa']] = so.relationship(back_populates='smf70_bct_da', viewonly=True)


class Smf70TrgDa(ReprMixin, Base70Da, Smf70trg):
    """The Smf70TrgDa class stores the daily Smf70Trg record in the smf70_trg_da table."""

    __tablename__ = "smf70_trg_da"
    smf70_trg_name: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Tenant resource group name.")
    smf70_trg_tntid: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Tenant identifier.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf70sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf70sid, date, smf70_trg_name, smf70_trg_tntid),

        sa.ForeignKeyConstraint(
            ['csc', 'smf70sid', 'date'],
            ['smf70_ctl_da.csc', 'smf70_ctl_da.smf70sid', 'smf70_ctl_da.date']),
    )

    smf70_ctl_da: so.Mapped['Smf70CtlDa'] = so.relationship(back_populates='smf70_trg_das', viewonly=True)


class Smf70WcDa(ReprMixin, Base70Da, Smf70wc):
    """The Smf70WcDa class stores the daily Smf70Wc record in the smf70_wc_da table."""

    __tablename__ = "smf70_wc_da"
    smf70wc_cpu_type: so.Mapped[int] = so.mapped_column(sa.Integer, doc="CPU type as defined by SMF70TYP.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf70sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf70sid, date, smf70wc_cpu_type),

        sa.ForeignKeyConstraint(
            ['csc', 'smf70sid', 'date'],
            ['smf70_ctl_da.csc', 'smf70_ctl_da.smf70sid', 'smf70_ctl_da.date']),
    )

    smf70_ctl_da: so.Mapped['Smf70CtlDa'] = so.relationship(back_populates='smf70_wc_das', viewonly=True)


class Smf70BctCpuDa(ReprMixin, Base70Da, Smf70bpd):
    """The Smf70BctCpuDa class stores the daily Smf70BctCpu record in the smf70_bct_cpu_da table."""

    __tablename__ = "smf70_bct_cpu_da"
    smf70cix: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="EBCDIC name corresponding to the CPU type of the logical processor in CPU-identification name section.")
    wait_completion_status: so.Mapped[Optional[str]] = so.mapped_column(sa.String(3),
                                                                        doc="the wait completion is enabled of this processor.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
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
    smf70sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, lpar_system_name, lpar_number, date, smf70sid, smf70cix),

        sa.ForeignKeyConstraint(
            ['csc', 'lpar_system_name', 'lpar_number', 'date', 'smf70sid'],
            ['smf70_bct_da.csc', 'smf70_bct_da.lpar_system_name', 'smf70_bct_da.lpar_number', 'smf70_bct_da.date',
             'smf70_bct_da.smf70sid']),
    )

    smf70_bct_da: so.Mapped['Smf70BctDa'] = so.relationship(back_populates='smf70_bct_cpu_das', viewonly=True)
    smf70_bpd_das: so.Mapped[List['Smf70BpdDa']] = so.relationship(back_populates='smf70_bct_cpu_da', viewonly=True)
