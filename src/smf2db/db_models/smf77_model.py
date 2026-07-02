import datetime as dt
from typing import List, Optional

import sqlalchemy as sa
import sqlalchemy.orm as so

from .smf77_base import ReprMixin, Base77, Smf77pro, Smf77ctl, Smf77enq


class Smf77Pro(ReprMixin, Base77, Smf77pro):
    """The Smf77Pro class stores the Smf77Pro section in the smf77_pro table."""

    __tablename__ = "smf77_pro"
    smf77ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time since midnight that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf77iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval was synchronized with SMF).")
    speed_boost: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                             doc="smf77fla (Bit 10) indcating speed boost was active during entire interval.")
    ziip_boost: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                            doc="smf77fla (Bit 9) indciating zIIP boost was active during entire interval.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf_type: so.Mapped[str] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf77sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(datetime, smf77ist, smf77iet, smf_type, csc, smf77sid),
        sa.ForeignKeyConstraint(
            ['csc', 'smf77sid', 'datetime', 'smf77ist', 'smf77iet'],
            ['smf77_ctl.csc', 'smf77_ctl.smf77sid', 'smf77_ctl.datetime', 'smf77_ctl.smf77ist', 'smf77_ctl.smf77iet']),
    )

    smf77_ctls: so.Mapped[List['Smf77Ctl']] = so.relationship(back_populates='smf77_pro', viewonly=True)


class Smf77Ctl(ReprMixin, Base77, Smf77ctl):
    """The Smf77Ctl class stores the Smf77Ctl section in the smf77_ctl table."""

    __tablename__ = "smf77_ctl"
    smf_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf77sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf77ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time since midnight that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf77iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval was synchronized with SMF).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf77sid, datetime, smf77ist, smf77iet),
    )

    smf77_pro: so.Mapped['Smf77Pro'] = so.relationship(back_populates='smf77_ctls', viewonly=True)
    smf77_enqs: so.Mapped[List['Smf77Enq']] = so.relationship(back_populates='smf77_ctl', viewonly=True)


class Smf77Enq(ReprMixin, Base77, Smf77enq):
    """The Smf77Enq class stores the Smf77Enq section in the smf77_enq table."""

    __tablename__ = "smf77_enq"
    smf77qnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Major name of resource.")
    smf77rnm: so.Mapped[str] = so.mapped_column(sa.String(44), doc="Minor name of resource.")
    smf77rln: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Minor name length.")
    smf77dfg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Current resource detail indicator Bit Meaning 0 Resource still in contention 1 On - Scope of systems Off - Scope of system 2 On - Owner has exclusive control of the resource Off - Owner shares the resource 3 On - First job is waiting for exclusive use Off - First job is waiting for shared use 4 On - Second job is waiting for exclusive use Off - Second job is waiting for shared use 5 On - Resource is global Off - Resource is local")
    smf77do1: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="Job name 1 of resource owner during period of maximum contention.")
    smf77do2: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="Job name 2 of resource owner during period of maximum contention.")
    smf77dw1: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="Job name 1 waiting for the resource owner during period of maximum contention.")
    smf77dw2: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="Job name 2 waiting for the resource owner during period of maximum contention.")
    smf77sy1: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="System identifier of job name 1 (resource owner at maximum contention).")
    smf77sy2: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="System identifier of job name 2 (resource owner at maximum contention).")
    smf77sy3: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="System identifier of job name 1 (waiting for the resource at maximum contention).")
    smf77sy4: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="System identifier of job name 2 (waiting for the resource at maximum contention).")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    idx: so.Mapped[int] = so.mapped_column(sa.Integer, doc=" the index of the entries in the section.")
    system_scope: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc=" smf77dfg (Bit 1) showing scope of systems if ON, otherwise, scope of system.")
    resource_contention: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                     doc=" smf77dfg (Bit 0) showing resource still in contention.")
    exclusive_owner: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                 doc=" smf77dfg (Bit 2) showing owner has exclusive control of the resource if ON, otherwise owner shares the resource.")
    job_wait_for_exc_usage: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                        doc=" smf77dfg (Bit 3) showing first job is waiting for exclusive use if ON, otherwise first job is waiting for shared use.")
    job_wait_for_2exc_usage: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                         doc=" smf77dfg (Bit 4) showing second job is waiting for exclusive use if ON, otherwise second job is waiting for shared use.")
    global_resource: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                 doc=" smf77dfg (Bit 5) showing resource is global.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf77sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf77ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time since midnight that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf77iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval was synchronized with SMF).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf77sid, datetime, smf77ist, smf77iet, smf77qnm, smf77rnm, idx),
        sa.ForeignKeyConstraint(
            ['csc', 'smf77sid', 'datetime', 'smf77ist', 'smf77iet'],
            ['smf77_ctl.csc', 'smf77_ctl.smf77sid', 'smf77_ctl.datetime', 'smf77_ctl.smf77ist', 'smf77_ctl.smf77iet']),
    )

    smf77_ctl: so.Mapped['Smf77Ctl'] = so.relationship(back_populates='smf77_enqs', viewonly=True)
