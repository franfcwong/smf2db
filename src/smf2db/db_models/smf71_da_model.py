import datetime as dt
from typing import Optional

import sqlalchemy as sa
import sqlalchemy.orm as so

from .smf71_base import ReprMixin, Base71Da, Smf71pro, Smf71pag


class Smf71ProDa(ReprMixin, Base71Da, Smf71pro):
    """The Smf71ProDa class stores the daily Smf71Pro record in the smf71_pro_da table."""

    __tablename__ = "smf71_pro_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    speed_boost: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                             doc="smf71fla (Bit 10) indcating speed boost was active during entire interval.")
    ziip_boost: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                            doc="smf71fla (Bit 9) indciating zIIP boost was active during entire interval.")
    smf_type: so.Mapped[str] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf71sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(date, smf_type, csc, smf71sid),

        sa.ForeignKeyConstraint(
            ['csc', 'smf71sid', 'date'],
            ['smf71_pag_da.csc', 'smf71_pag_da.smf71sid', 'smf71_pag_da.date']),
    )

    smf71_pag_da: so.Mapped['Smf71PagDa'] = so.relationship(back_populates='smf71_pro_da', viewonly=True)


class Smf71PagDa(ReprMixin, Base71Da, Smf71pag):
    """The Smf71PagDa class stores the daily Smf71Pag record in the smf71_pag_da table."""

    __tablename__ = "smf71_pag_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf71sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf71sid, date),
    )

    smf71_pro_da: so.Mapped['Smf71ProDa'] = so.relationship(back_populates='smf71_pag_da', viewonly=True)
