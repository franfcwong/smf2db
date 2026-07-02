import datetime as dt
from typing import List, Optional

import sqlalchemy as sa
import sqlalchemy.orm as so

from .smf75_base import ReprMixin, Base75Hr, Smf75pro, Smf75psd


class Smf75ProHr(ReprMixin, Base75Hr, Smf75pro):
    """The Smf75ProHr class stores the hourly Smf75Pro record in the smf75_pro_hr table."""

    __tablename__ = "smf75_pro_hr"
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    speed_boost: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                             doc="smf75fla (Bit 10) indcating speed boost was active during entire interval.")
    ziip_boost: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                            doc="smf75fla (Bit 9) indciating zIIP boost was active during entire interval.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf_type: so.Mapped[str] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf75sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(datetime, smf_type, csc, smf75sid),
    )

    smf75_psd_hrs: so.Mapped[List['Smf75PsdHr']] = so.relationship(back_populates='smf75_pro_hr', viewonly=True)


class Smf75PsdHr(ReprMixin, Base75Hr, Smf75psd):
    """The Smf75PsdHr class stores the hourly Smf75Psd record in the smf75_psd_hr table."""

    __tablename__ = "smf75_psd_hr"
    smf75dsn: so.Mapped[str] = so.mapped_column(sa.String(44),
                                                doc="Page data set name. Valid only when bit 4 of SMF75FL2 is not set.")
    smf_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf75sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf75sid, datetime, smf75dsn),
        sa.ForeignKeyConstraint(
            ['datetime', 'smf_type', 'csc', 'smf75sid'],
            ['smf75_pro_hr.datetime', 'smf75_pro_hr.smf_type', 'smf75_pro_hr.csc', 'smf75_pro_hr.smf75sid']),
    )

    smf75_pro_hr: so.Mapped['Smf75ProHr'] = so.relationship(back_populates='smf75_psd_hrs', viewonly=True)
