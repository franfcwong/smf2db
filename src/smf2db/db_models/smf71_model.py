import datetime as dt
from typing import Optional

import sqlalchemy as sa
import sqlalchemy.orm as so

from .smf71_base import ReprMixin, Base71, Smf71pro, Smf71pag


class Smf71Pro(ReprMixin, Base71, Smf71pro):
    """The Smf71Pro class stores the Smf71Pro section in the smf71_pro table."""

    __tablename__ = "smf71_pro"
    smf71ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf71iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval was synchronized with SMF).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf_type: so.Mapped[str] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf71sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(datetime, smf71ist, smf71iet, smf_type, csc, smf71sid),
        sa.ForeignKeyConstraint(
            ['csc', 'smf71sid', 'datetime', 'smf71ist', 'smf71iet'],
            ['smf71_pag.csc', 'smf71_pag.smf71sid', 'smf71_pag.datetime', 'smf71_pag.smf71ist', 'smf71_pag.smf71iet']),
    )

    smf71_pag: so.Mapped["Smf71Pag"] = so.relationship(back_populates="smf71_pro", viewonly=True)


class Smf71Pag(ReprMixin, Base71, Smf71pag):
    """The Smf71Pag class stores the Smf71Pag section in the smf71_pag table."""

    __tablename__ = "smf71_pag"
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf71sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf71ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf71iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval was synchronized with SMF).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf71sid, datetime, smf71ist, smf71iet),
    )

    smf71_pro: so.Mapped["Smf71Pro"] = so.relationship(back_populates="smf71_pag", viewonly=True)
