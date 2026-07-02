import datetime as dt
from typing import List, Optional

import sqlalchemy as sa
import sqlalchemy.orm as so

from .smf77_base import ReprMixin, Base77Hr, Smf77pro, Smf77ctl, Smf77enq


class Smf77ProHr(ReprMixin, Base77Hr, Smf77pro):
    """The Smf77ProHr class stores the hourly Smf77Pro record in the smf77_pro_hr table."""

    __tablename__ = "smf77_pro_hr"
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
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
        sa.PrimaryKeyConstraint(datetime, smf_type, csc, smf77sid),
        sa.ForeignKeyConstraint(
            ['csc', 'smf77sid', 'datetime'],
            ['smf77_ctl_hr.csc', 'smf77_ctl_hr.smf77sid', 'smf77_ctl_hr.datetime']),
    )

    smf77_ctl_hrs: so.Mapped[List['Smf77CtlHr']] = so.relationship(back_populates='smf77_pro_hr', viewonly=True)


class Smf77CtlHr(ReprMixin, Base77Hr, Smf77ctl):
    """The Smf77CtlHr class stores the hourly Smf77Ctl record in the smf77_ctl_hr table."""

    __tablename__ = "smf77_ctl_hr"
    smf_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf77sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf77sid, datetime),
    )

    smf77_pro_hr: so.Mapped['Smf77ProHr'] = so.relationship(back_populates='smf77_ctl_hrs', viewonly=True)
    smf77_enq_hrs: so.Mapped[List['Smf77EnqHr']] = so.relationship(back_populates='smf77_ctl_hr', viewonly=True)


class Smf77EnqHr(ReprMixin, Base77Hr, Smf77enq):
    """The Smf77EnqHr class stores the hourly Smf77Enq record in the smf77_enq_hr table."""

    __tablename__ = "smf77_enq_hr"
    smf77qnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Major name of resource.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf77sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf77sid, datetime, smf77qnm),
        sa.ForeignKeyConstraint(
            ['csc', 'smf77sid', 'datetime'],
            ['smf77_ctl_hr.csc', 'smf77_ctl_hr.smf77sid', 'smf77_ctl_hr.datetime']),
    )

    smf77_ctl_hr: so.Mapped['Smf77CtlHr'] = so.relationship(back_populates='smf77_enq_hrs', viewonly=True)
