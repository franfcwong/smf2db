import datetime as dt
from typing import Optional

import sqlalchemy as sa
import sqlalchemy.orm as so

from .smf1101_base import ReprMixin, Base110115m, DfhcbtsBase, DfhchnlBase, DfhcicsBase, DfhdataBase, DfhdestBase, \
    DfhdochBase, DfhfepiBase, DfhfileBase, DfhjourBase, DfhmappBase, DfhotelBase, DfhprogBase, DfhrmiBase, DfhsockBase, \
    DfhstorBase, DfhsyncBase, DfhtaskBase, DfhtempBase, DfhtermBase, DfhwebbBase, DfhwebcBase


class Smf110115m(ReprMixin, Base110115m, DfhcbtsBase, DfhchnlBase, DfhcicsBase, DfhdataBase, DfhdestBase, DfhdochBase,
                 DfhfepiBase, DfhfileBase, DfhjourBase, DfhmappBase, DfhotelBase, DfhprogBase, DfhrmiBase, DfhsockBase,
                 DfhstorBase, DfhsyncBase, DfhtaskBase, DfhtempBase, DfhtermBase, DfhwebbBase, DfhwebcBase):
    """The Smf110115m class stores the 15-minutes Smf1101 record in the smf110_1_15m table."""

    __tablename__ = "smf110_1_15m"
    datetime_15m: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="The 15-minute interval of the record.")
    datetime: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfmnjbn: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Jobname.")
    smfmnrvn: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4),
                                                          doc="Record version (CICS), format 0VRM (V = version; R = release M = modification).")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    tasks: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                       doc="Total number of transaction records within the duration.")
    elapsed: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="Total elapsed time of the transactions within the duration.")
    smfmnsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="System identification.")
    smfmnprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfmnspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    task_tran: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Transaction identification.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfmnsid, smfmnprn, smfmnspn, task_tran, datetime_15m),
    )
