import datetime as dt
from typing import Optional

import sqlalchemy as sa
import sqlalchemy.orm as so

from .smf71_base import ReprMixin, Base71Hr, Smf71pro, Smf71pag


class Smf71ProHr(ReprMixin, Base71Hr, Smf71pro):
    """The Smf71ProHr class stores the hourly Smf71Pro record in the smf71_pro_hr table."""

    __tablename__ = "smf71_pro_hr"
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    speed_boost: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                             doc="smf71fla (Bit 10) indcating speed boost was active during entire interval.")
    ziip_boost: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                            doc="smf71fla (Bit 9) indciating zIIP boost was active during entire interval.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf_type: so.Mapped[str] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf71sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(datetime, smf_type, csc, smf71sid),
        sa.ForeignKeyConstraint(
            ['csc', 'smf71sid', 'datetime'],
            ['smf71_pag_hr.csc', 'smf71_pag_hr.smf71sid', 'smf71_pag_hr.datetime']),
    )

    smf71_pag_hr: so.Mapped['Smf71PagHr'] = so.relationship(back_populates='smf71_pro_hr', viewonly=True)


class Smf71PagHr(ReprMixin, Base71Hr, Smf71pag):
    """The Smf71PagHr class stores the hourly Smf71Pag record in the smf71_pag_hr table."""

    __tablename__ = "smf71_pag_hr"
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf71sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf71sid, datetime),
    )

    smf71_pro_hr: so.Mapped['Smf71ProHr'] = so.relationship(back_populates='smf71_pag_hr', viewonly=True)
