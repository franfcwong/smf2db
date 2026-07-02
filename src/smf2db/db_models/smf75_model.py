import datetime as dt
from typing import List, Optional

import sqlalchemy as sa
import sqlalchemy.orm as so

from .smf75_base import ReprMixin, Base75, Smf75pro, Smf75psd


class Smf75Pro(ReprMixin, Base75, Smf75pro):
    """The Smf75Pro class stores the Smf75Pro section in the smf75_pro table."""

    __tablename__ = "smf75_pro"
    smf75ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf75iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval was synchronized with SMF).")
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
        sa.PrimaryKeyConstraint(datetime, smf75ist, smf75iet, smf_type, csc, smf75sid),
    )

    smf75_psds: so.Mapped[List['Smf75Psd']] = so.relationship(back_populates='smf75_pro', viewonly=True)


class Smf75Psd(ReprMixin, Base75, Smf75psd):
    """The Smf75Psd class stores the Smf75Psd section in the smf75_psd table."""

    __tablename__ = "smf75_psd"
    smf75dsn: so.Mapped[str] = so.mapped_column(sa.String(44),
                                                doc="Page data set name. Valid only when bit 4 of SMF75FL2 is not set.")
    smf_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf75sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf75ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf75iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval was synchronized with SMF).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf75sid, datetime, smf75ist, smf75iet, smf75dsn),
        sa.ForeignKeyConstraint(
            ['datetime', 'smf75ist', 'smf75iet', 'smf_type', 'csc', 'smf75sid'],
            ['smf75_pro.datetime', 'smf75_pro.smf75ist', 'smf75_pro.smf75iet', 'smf75_pro.smf_type', 'smf75_pro.csc',
             'smf75_pro.smf75sid']),
    )

    smf75_pro: so.Mapped['Smf75Pro'] = so.relationship(back_populates='smf75_psds', viewonly=True)
