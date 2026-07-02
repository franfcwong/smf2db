import datetime as dt
from typing import List, Optional

import sqlalchemy as sa
import sqlalchemy.orm as so

from .smf77_base import ReprMixin, Base77Da, Smf77pro, Smf77ctl, Smf77enq


class Smf77ProDa(ReprMixin, Base77Da, Smf77pro):
    """The Smf77ProDa class stores the daily Smf77Pro record in the smf77_pro_da table."""

    __tablename__ = "smf77_pro_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    speed_boost: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                             doc="smf77fla (Bit 10) indcating speed boost was active during entire interval.")
    ziip_boost: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                            doc="smf77fla (Bit 9) indciating zIIP boost was active during entire interval.")
    smf_type: so.Mapped[str] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf77sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(date, smf_type, csc, smf77sid),

        sa.ForeignKeyConstraint(
            ['csc', 'smf77sid', 'date'],
            ['smf77_ctl_da.csc', 'smf77_ctl_da.smf77sid', 'smf77_ctl_da.date']),
    )

    smf77_ctl_das: so.Mapped[List['Smf77CtlDa']] = so.relationship(back_populates='smf77_pro_da', viewonly=True)


class Smf77CtlDa(ReprMixin, Base77Da, Smf77ctl):
    """The Smf77CtlDa class stores the daily Smf77Ctl record in the smf77_ctl_da table."""

    __tablename__ = "smf77_ctl_da"
    smf_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf77sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf77sid, date),
    )

    smf77_pro_da: so.Mapped['Smf77ProDa'] = so.relationship(back_populates='smf77_ctl_das', viewonly=True)
    smf77_enq_das: so.Mapped[List['Smf77EnqDa']] = so.relationship(back_populates='smf77_ctl_da', viewonly=True)


class Smf77EnqDa(ReprMixin, Base77Da, Smf77enq):
    """The Smf77EnqDa class stores the daily Smf77Enq record in the smf77_enq_da table."""

    __tablename__ = "smf77_enq_da"
    smf77qnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Major name of resource.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf77sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf77sid, date, smf77qnm),

        sa.ForeignKeyConstraint(
            ['csc', 'smf77sid', 'date'],
            ['smf77_ctl_da.csc', 'smf77_ctl_da.smf77sid', 'smf77_ctl_da.date']),
    )

    smf77_ctl_da: so.Mapped['Smf77CtlDa'] = so.relationship(back_populates='smf77_enq_das', viewonly=True)
