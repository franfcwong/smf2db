from typing import List, Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
import datetime as dt
from .smf30_base import ReprMixin, Base30Hr, Smf30id, Smf30pss, Smf30cmp, Smf30ura, Smf30prf, Smf30cas, Smf30sap, \
    Smf30ops, Smf30exp, Smf30op, Smf30ud, Smf30uss


class Smf30IdHr(ReprMixin, Base30Hr):
    """The Smf30IdHr class stores the hourly Smf30Id record in the smf30_id_hr table."""

    __tablename__ = "smf30_id_hr"
    smf30_rctpcpua_actual: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                       doc="Physical CPU adjustment factor (this is the adjustment factor for converting CPU time to equivalent service, in basic-mode with all processors online). Based on model capacity rating.")
    smf30_rctpcpua_nominal: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                        doc="Physical CPU adjustment factor (this is the adjustment factor for converting CPU time to equivalent service in basic-mode with all processors online). Based on nominal model capacity rating.")
    smf30_rctpcpua_scaling_factor: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                               doc="Scaling factor for SMF30_RCTPCPUA_actual and SMF30_RCTPCPUA_nominal.")
    smf30_capacity_adjustment_ind: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                               doc="Field values and meanings are: Value Meaning 0 The indication is not reported. 1-99 Some amount of reduction is indicated. 100 The machine is operating in normal capacity. Primary CPUs and all secondary-type CPUs are similarly affected.")
    smf30_rmctadjn_nominal: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Nominal CPU rate adjustment.")
    smf30_time_on_ziip: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                      doc="(SMF30_TIME_ON_SUP) Accumulation of time spent on zIIP. Time is in hundredths of a second (includes enclave time).")
    smf30tex: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Total blocks transferred - accumulated EXCP counts. This field is the 8-byte equivalent of SMF30TEP, but this field remains valid after SMF30TEP is invalid.")
    smf30pgi: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="(SMF30PIA) Number of page-ins from auxiliary storage, regardless of the page size (4K or 1M).")
    smf30pgo: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="(SMF30POA) Number of page-outs to auxiliary storage, regardless of the page size (4K or 1M).")
    smf30nsw: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="As of z/OS 1.8, this field is no longer valid; the value is always zero. Prior to z/OS 1.8, this field contained: Number of address space swap sequences. (A swap sequence consists of an address space swap-out and swap-in. Logical swap-out and swap-in are not included.)")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    duration: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="the duration of the job.")
    tcb_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="the calculated TCB time based on the service units.")
    srb_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="the calculated SRB time base on the service units.")
    cpu_total: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="the total CPU time.")
    consumed_msu: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="the total MSU consumed.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf30syp: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Sysplex name (from the SYSPLEX parameter in the COUPLExx parmlib member).")
    smf30syn: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="System name (from the SYSNAME parameter in the IEASYSxx parmlib member).")
    wkl: so.Mapped[str] = so.mapped_column(sa.String(7), doc="the workload group based on the problem program run.")
    smf30typ: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="Subtype identification Value Meaning 1 Job start or start of other work unit. 2 Activity since previous interval ended. Produced only when interval recording is active. 3 Activity for the last interval before step termination. Produced only when interval recording is active. 4 Step total 5 Job termination or termination of other work unit. 6")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf30syp, smf30syn, datetime, wkl, smf30typ),
    )

    smf30_ura_hr: so.Mapped['Smf30UraHr'] = so.relationship(back_populates='smf30_id_hr', viewonly=True)
    smf30_prf_hr: so.Mapped['Smf30PrfHr'] = so.relationship(back_populates='smf30_id_hr', viewonly=True)
    smf30_cas_hr: so.Mapped['Smf30CasHr'] = so.relationship(back_populates='smf30_id_hr', viewonly=True)
    smf30_sap_hr: so.Mapped['Smf30SapHr'] = so.relationship(back_populates='smf30_id_hr', viewonly=True)
    smf30_ops_hr: so.Mapped['Smf30OpsHr'] = so.relationship(back_populates='smf30_id_hr', viewonly=True)
    smf30_exp_hrs: so.Mapped[List['Smf30ExpHr']] = so.relationship(back_populates='smf30_id_hr', viewonly=True)
    smf30_op_hrs: so.Mapped[List['Smf30OpHr']] = so.relationship(back_populates='smf30_id_hr', viewonly=True)
    smf30_ud_hrs: so.Mapped[List['Smf30UdHr']] = so.relationship(back_populates='smf30_id_hr', viewonly=True)
    smf30_uss_hrs: so.Mapped[List['Smf30UssHr']] = so.relationship(back_populates='smf30_id_hr', viewonly=True)


class Smf30UraHr(ReprMixin, Base30Hr, Smf30ura):
    """The Smf30UraHr class stores the hourly Smf30Ura record in the smf30_ura_hr table."""

    __tablename__ = "smf30_ura_hr"
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf30syp: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Sysplex name (from the SYSPLEX parameter in the COUPLExx parmlib member).")
    smf30syn: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="System name (from the SYSNAME parameter in the IEASYSxx parmlib member).")
    wkl: so.Mapped[str] = so.mapped_column(sa.String(7), doc="the workload group based on the problem program run.")
    smf30typ: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="Subtype identification Value Meaning 1 Job start or start of other work unit. 2 Activity since previous interval ended. Produced only when interval recording is active. 3 Activity for the last interval before step termination. Produced only when interval recording is active. 4 Step total 5 Job termination or termination of other work unit. 6")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf30syp, smf30syn, datetime, wkl, smf30typ),
        sa.ForeignKeyConstraint(
            ['csc', 'smf30syp', 'smf30syn', 'datetime', 'wkl', 'smf30typ'],
            ['smf30_id_hr.csc', 'smf30_id_hr.smf30syp', 'smf30_id_hr.smf30syn', 'smf30_id_hr.datetime',
             'smf30_id_hr.wkl', 'smf30_id_hr.smf30typ']),
    )

    smf30_id_hr: so.Mapped['Smf30IdHr'] = so.relationship(back_populates='smf30_ura_hr', viewonly=True)


class Smf30PrfHr(ReprMixin, Base30Hr, Smf30prf):
    """The Smf30PrfHr class stores the hourly Smf30Prf record in the smf30_prf_hr table."""

    __tablename__ = "smf30_prf_hr"
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf30syp: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Sysplex name (from the SYSPLEX parameter in the COUPLExx parmlib member).")
    smf30syn: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="System name (from the SYSNAME parameter in the IEASYSxx parmlib member).")
    wkl: so.Mapped[str] = so.mapped_column(sa.String(7), doc="the workload group based on the problem program run.")
    smf30typ: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="Subtype identification Value Meaning 1 Job start or start of other work unit. 2 Activity since previous interval ended. Produced only when interval recording is active. 3 Activity for the last interval before step termination. Produced only when interval recording is active. 4 Step total 5 Job termination or termination of other work unit. 6")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf30syp, smf30syn, datetime, wkl, smf30typ),
        sa.ForeignKeyConstraint(
            ['csc', 'smf30syp', 'smf30syn', 'datetime', 'wkl', 'smf30typ'],
            ['smf30_id_hr.csc', 'smf30_id_hr.smf30syp', 'smf30_id_hr.smf30syn', 'smf30_id_hr.datetime',
             'smf30_id_hr.wkl', 'smf30_id_hr.smf30typ']),
    )

    smf30_id_hr: so.Mapped['Smf30IdHr'] = so.relationship(back_populates='smf30_prf_hr', viewonly=True)


class Smf30CasHr(ReprMixin, Base30Hr, Smf30cas):
    """The Smf30CasHr class stores the hourly Smf30Cas record in the smf30_cas_hr table."""

    __tablename__ = "smf30_cas_hr"
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf30syp: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Sysplex name (from the SYSPLEX parameter in the COUPLExx parmlib member).")
    smf30syn: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="System name (from the SYSNAME parameter in the IEASYSxx parmlib member).")
    wkl: so.Mapped[str] = so.mapped_column(sa.String(7), doc="the workload group based on the problem program run.")
    smf30typ: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="Subtype identification Value Meaning 1 Job start or start of other work unit. 2 Activity since previous interval ended. Produced only when interval recording is active. 3 Activity for the last interval before step termination. Produced only when interval recording is active. 4 Step total 5 Job termination or termination of other work unit. 6")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf30syp, smf30syn, datetime, wkl, smf30typ),
        sa.ForeignKeyConstraint(
            ['csc', 'smf30syp', 'smf30syn', 'datetime', 'wkl', 'smf30typ'],
            ['smf30_id_hr.csc', 'smf30_id_hr.smf30syp', 'smf30_id_hr.smf30syn', 'smf30_id_hr.datetime',
             'smf30_id_hr.wkl', 'smf30_id_hr.smf30typ']),
    )

    smf30_id_hr: so.Mapped['Smf30IdHr'] = so.relationship(back_populates='smf30_cas_hr', viewonly=True)


class Smf30ExpHr(ReprMixin, Base30Hr):
    """The Smf30ExpHr class stores the hourly Smf30Exp record in the smf30_exp_hr table."""

    __tablename__ = "smf30_exp_hr"
    smf30dct: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Device connect time for this data set (in 128 micro-second units). For DIV object, device connect time is not collected by SMF; however, this field may not always be zero. For example, if a user is using a DIV data set and calls a VSAM utility to process it using the same DD statement, this will result in device connect time being charged by VSAM to the DIV object.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf30syp: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Sysplex name (from the SYSPLEX parameter in the COUPLExx parmlib member).")
    smf30syn: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="System name (from the SYSNAME parameter in the IEASYSxx parmlib member).")
    wkl: so.Mapped[str] = so.mapped_column(sa.String(7), doc="the workload group based on the problem program run.")
    smf30typ: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="Subtype identification Value Meaning 1 Job start or start of other work unit. 2 Activity since previous interval ended. Produced only when interval recording is active. 3 Activity for the last interval before step termination. Produced only when interval recording is active. 4 Step total 5 Job termination or termination of other work unit. 6")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf30syp, smf30syn, datetime, wkl, smf30typ),
        sa.ForeignKeyConstraint(
            ['csc', 'smf30syp', 'smf30syn', 'datetime', 'wkl', 'smf30typ'],
            ['smf30_id_hr.csc', 'smf30_id_hr.smf30syp', 'smf30_id_hr.smf30syn', 'smf30_id_hr.datetime',
             'smf30_id_hr.wkl', 'smf30_id_hr.smf30typ']),
    )

    smf30_id_hr: so.Mapped['Smf30IdHr'] = so.relationship(back_populates='smf30_exp_hrs', viewonly=True)


class Smf30OpHr(ReprMixin, Base30Hr, Smf30op):
    """The Smf30OpHr class stores the hourly Smf30Op record in the smf30_op_hr table."""

    __tablename__ = "smf30_op_hr"
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf30syp: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Sysplex name (from the SYSPLEX parameter in the COUPLExx parmlib member).")
    smf30syn: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="System name (from the SYSNAME parameter in the IEASYSxx parmlib member).")
    wkl: so.Mapped[str] = so.mapped_column(sa.String(7), doc="the workload group based on the problem program run.")
    smf30typ: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="Subtype identification Value Meaning 1 Job start or start of other work unit. 2 Activity since previous interval ended. Produced only when interval recording is active. 3 Activity for the last interval before step termination. Produced only when interval recording is active. 4 Step total 5 Job termination or termination of other work unit. 6")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf30syp, smf30syn, datetime, wkl, smf30typ),
        sa.ForeignKeyConstraint(
            ['csc', 'smf30syp', 'smf30syn', 'datetime', 'wkl', 'smf30typ'],
            ['smf30_id_hr.csc', 'smf30_id_hr.smf30syp', 'smf30_id_hr.smf30syn', 'smf30_id_hr.datetime',
             'smf30_id_hr.wkl', 'smf30_id_hr.smf30typ']),
    )

    smf30_id_hr: so.Mapped['Smf30IdHr'] = so.relationship(back_populates='smf30_op_hrs', viewonly=True)


class Smf30OpsHr(ReprMixin, Base30Hr, Smf30ops):
    """The Smf30OpsHr class stores the hourly Smf30Ops record in the smf30_ops_hr table."""

    __tablename__ = "smf30_ops_hr"
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf30syp: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Sysplex name (from the SYSPLEX parameter in the COUPLExx parmlib member).")
    smf30syn: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="System name (from the SYSNAME parameter in the IEASYSxx parmlib member).")
    wkl: so.Mapped[str] = so.mapped_column(sa.String(7), doc="the workload group based on the problem program run.")
    smf30typ: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="Subtype identification Value Meaning 1 Job start or start of other work unit. 2 Activity since previous interval ended. Produced only when interval recording is active. 3 Activity for the last interval before step termination. Produced only when interval recording is active. 4 Step total 5 Job termination or termination of other work unit. 6")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf30syp, smf30syn, datetime, wkl, smf30typ),
        sa.ForeignKeyConstraint(
            ['csc', 'smf30syp', 'smf30syn', 'datetime', 'wkl', 'smf30typ'],
            ['smf30_id_hr.csc', 'smf30_id_hr.smf30syp', 'smf30_id_hr.smf30syn', 'smf30_id_hr.datetime',
             'smf30_id_hr.wkl', 'smf30_id_hr.smf30typ']),
    )

    smf30_id_hr: so.Mapped['Smf30IdHr'] = so.relationship(back_populates='smf30_ops_hr', viewonly=True)


class Smf30UdHr(ReprMixin, Base30Hr, Smf30ud):
    """The Smf30UdHr class stores the hourly Smf30Ud record in the smf30_ud_hr table."""

    __tablename__ = "smf30_ud_hr"
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf30syp: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Sysplex name (from the SYSPLEX parameter in the COUPLExx parmlib member).")
    smf30syn: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="System name (from the SYSNAME parameter in the IEASYSxx parmlib member).")
    wkl: so.Mapped[str] = so.mapped_column(sa.String(7), doc="the workload group based on the problem program run.")
    smf30typ: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="Subtype identification Value Meaning 1 Job start or start of other work unit. 2 Activity since previous interval ended. Produced only when interval recording is active. 3 Activity for the last interval before step termination. Produced only when interval recording is active. 4 Step total 5 Job termination or termination of other work unit. 6")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf30syp, smf30syn, datetime, wkl, smf30typ),
        sa.ForeignKeyConstraint(
            ['csc', 'smf30syp', 'smf30syn', 'datetime', 'wkl', 'smf30typ'],
            ['smf30_id_hr.csc', 'smf30_id_hr.smf30syp', 'smf30_id_hr.smf30syn', 'smf30_id_hr.datetime',
             'smf30_id_hr.wkl', 'smf30_id_hr.smf30typ']),
    )

    smf30_id_hr: so.Mapped['Smf30IdHr'] = so.relationship(back_populates='smf30_ud_hrs', viewonly=True)


class Smf30UssHr(ReprMixin, Base30Hr, Smf30uss):
    """The Smf30UssHr class stores the hourly Smf30Uss record in the smf30_uss_hr table."""

    __tablename__ = "smf30_uss_hr"
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf30syp: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Sysplex name (from the SYSPLEX parameter in the COUPLExx parmlib member).")
    smf30syn: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="System name (from the SYSNAME parameter in the IEASYSxx parmlib member).")
    wkl: so.Mapped[str] = so.mapped_column(sa.String(7), doc="the workload group based on the problem program run.")
    smf30typ: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="Subtype identification Value Meaning 1 Job start or start of other work unit. 2 Activity since previous interval ended. Produced only when interval recording is active. 3 Activity for the last interval before step termination. Produced only when interval recording is active. 4 Step total 5 Job termination or termination of other work unit. 6")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf30syp, smf30syn, datetime, wkl, smf30typ),
        sa.ForeignKeyConstraint(
            ['csc', 'smf30syp', 'smf30syn', 'datetime', 'wkl', 'smf30typ'],
            ['smf30_id_hr.csc', 'smf30_id_hr.smf30syp', 'smf30_id_hr.smf30syn', 'smf30_id_hr.datetime',
             'smf30_id_hr.wkl', 'smf30_id_hr.smf30typ']),
    )

    smf30_id_hr: so.Mapped['Smf30IdHr'] = so.relationship(back_populates='smf30_uss_hrs', viewonly=True)


class Smf30SapHr(ReprMixin, Base30Hr, Smf30sap):
    """The Smf30SapHr class stores the hourly Smf30Sap record in the smf30_sap_hr table."""

    __tablename__ = "smf30_sap_hr"
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf30syp: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Sysplex name (from the SYSPLEX parameter in the COUPLExx parmlib member).")
    smf30syn: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="System name (from the SYSNAME parameter in the IEASYSxx parmlib member).")
    wkl: so.Mapped[str] = so.mapped_column(sa.String(7), doc="the workload group based on the problem program run.")
    smf30typ: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="Subtype identification Value Meaning 1 Job start or start of other work unit. 2 Activity since previous interval ended. Produced only when interval recording is active. 3 Activity for the last interval before step termination. Produced only when interval recording is active. 4 Step total 5 Job termination or termination of other work unit. 6")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf30syp, smf30syn, datetime, wkl, smf30typ),
        sa.ForeignKeyConstraint(
            ['csc', 'smf30syp', 'smf30syn', 'datetime', 'wkl', 'smf30typ'],
            ['smf30_id_hr.csc', 'smf30_id_hr.smf30syp', 'smf30_id_hr.smf30syn', 'smf30_id_hr.datetime',
             'smf30_id_hr.wkl', 'smf30_id_hr.smf30typ']),
    )

    smf30_id_hr: so.Mapped['Smf30IdHr'] = so.relationship(back_populates='smf30_sap_hr', viewonly=True)


class Smf306Hr(ReprMixin, Base30Hr, Smf30ura, Smf30prf, Smf30cas, Smf30sap, Smf30ops):
    """The Smf306Hr class stores the hourly Smf306 record in the smf30_6_hr table."""

    __tablename__ = "smf30_6_hr"
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf30arb: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Maximum virtual storage, in bytes, allocated from the local system queue area (LSQA) and the SWA subpools (less than 16 MB).")
    smf30ear: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Maximum virtual storage in bytes allocated from the local system queue area (LSQA) and the SWA subpools (greater than 16 MB).")
    smf30urb: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Maximum virtual storage in bytes allocated from the user subpools (less than 16 MB).")
    smf30eur: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Maximum virtual storage in bytes allocated from the user subpools (greater than 16 MB).")
    smf30hvo: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Amount of 64-bit private storage in bytes that is obtained by this step or job. This includes guarded virtual storage. The SMF30HVO field contains a snapshot value of high virtual private storage allocation. As the memory objects owned by the executed program have already been detached at the time the step or job goes through termination, SMF30HVO contains the memory object size still allocated to the initiator address space, but no longer reflects the memory objects that may have been allocated by the program executed in the job step. In contrast to SMF30HVO, the SMF30HVH field is maintained as a high water mark. Its content reflects the high virtual memory object size that was once allocated by the job step being executed under the initiator address space.")
    smf30rvn: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                          doc="Record version number Value Meaning '05' MVS/SP Version 5 '04' MVS/SP Version 4 '03' MVS/SP Version 3 '02' MVS/SP Version 2 '01' VS2")
    smf30pnm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="Subsystem or product name, for example SMF.")
    smf30osl: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="Code string for the operating system level to represent the version, release, and modification level, as described for CVTPRODN. Guaranteed to be larger in each release.")
    smf30cls: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                          doc="Job class (blank for TSO/E session or started tasks).")
    smf30jpt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="JES input priority. If no value is specified for the PRTY parameter (on the JOB card), this field contains: • For JES3, the default priority specified on the JES3 STANDARDS initialization card • For JES2, a zero. Note that JES2 does not use the priority value reported in the field. (The JES2 job selection priority is requested using the JES2")
    duration: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="the duration of the job.")
    tcb_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="the calculated TCB time based on the service units.")
    srb_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="the calculated SRB time base on the service units.")
    cpu_total: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="the total CPU time.")
    consumed_msu: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="the total MSU consumed.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smf30stn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Step number (first step = 1, and so on).")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf30syp: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Sysplex name (from the SYSPLEX parameter in the COUPLExx parmlib member).")
    smf30syn: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="System name (from the SYSNAME parameter in the IEASYSxx parmlib member).")
    wkl: so.Mapped[str] = so.mapped_column(sa.String(7), doc="the workload group based on the problem program run.")
    smf30typ: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="Subtype identification Value Meaning 1 Job start or start of other work unit. 2 Activity since previous interval ended. Produced only when interval recording is active. 3 Activity for the last interval before step termination. Produced only when interval recording is active. 4 Step total 5 Job termination or termination of other work unit. 6")
    smf30jbn: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Job or session name. The job name, time, and date that the reader recognized the JOB card (for this job) constitute the job log identification.")
    smf30asi: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Address space identifier.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf30syp, smf30syn, datetime, wkl, smf30jbn, smf30asi, smf30typ),
    )
