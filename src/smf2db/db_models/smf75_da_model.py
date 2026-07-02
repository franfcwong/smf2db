import datetime as dt
from typing import List, Optional

import sqlalchemy as sa
import sqlalchemy.orm as so

from .smf75_base import ReprMixin, Base75Da, Smf75pro, Smf75psd


class Smf75ProDa(ReprMixin, Base75Da, Smf75pro):
    """The Smf75ProDa class stores the daily Smf75Pro record in the smf75_pro_da table."""

    __tablename__ = "smf75_pro_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    speed_boost: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                             doc="smf75fla (Bit 10) indcating speed boost was active during entire interval.")
    ziip_boost: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                            doc="smf75fla (Bit 9) indciating zIIP boost was active during entire interval.")
    smf_type: so.Mapped[str] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf75sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(date, smf_type, csc, smf75sid),
    )

    smf75_psd_das: so.Mapped[List['Smf75PsdDa']] = so.relationship(back_populates='smf75_pro_da', viewonly=True)


class Smf75PsdDa(ReprMixin, Base75Da, Smf75psd):
    """The Smf75PsdDa class stores the daily Smf75Psd record in the smf75_psd_da table."""

    __tablename__ = "smf75_psd_da"
    smf75dsn: so.Mapped[str] = so.mapped_column(sa.String(44),
                                                doc="Page data set name. Valid only when bit 4 of SMF75FL2 is not set.")
    smf_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf75sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf75sid, date, smf75dsn),

        sa.ForeignKeyConstraint(
            ['date', 'smf_type', 'csc', 'smf75sid'],
            ['smf75_pro_da.date', 'smf75_pro_da.smf_type', 'smf75_pro_da.csc', 'smf75_pro_da.smf75sid']),
    )

    smf75_pro_da: so.Mapped['Smf75ProDa'] = so.relationship(back_populates='smf75_psd_das', viewonly=True)
