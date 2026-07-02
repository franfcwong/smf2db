import datetime as dt
from typing import Optional

import sqlalchemy as sa
import sqlalchemy.orm as so

from .smf1101_base import ReprMixin, Base1101, DfhcbtsBase, DfhchnlBase, DfhcicsBase, DfhdataBase, DfhdestBase, \
    DfhdochBase, DfhfepiBase, DfhfileBase, DfhjourBase, DfhmappBase, DfhotelBase, DfhprogBase, DfhrmiBase, DfhsockBase, \
    DfhstorBase, DfhsyncBase, DfhtaskBase, DfhtempBase, DfhtermBase, DfhwebbBase, DfhwebcBase


class Smf1101(ReprMixin, Base1101, DfhcbtsBase, DfhchnlBase, DfhcicsBase, DfhdataBase, DfhdestBase, DfhdochBase,
              DfhfepiBase, DfhfileBase, DfhjourBase, DfhmappBase, DfhotelBase, DfhprogBase, DfhrmiBase, DfhsockBase,
              DfhstorBase, DfhsyncBase, DfhtaskBase, DfhtempBase, DfhtermBase, DfhwebbBase, DfhwebcBase):
    """The Smf1101 class stores the Smf1101 section in the smf110_1 table."""

    __tablename__ = "smf110_1"
    datetime_15m: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                      doc="The 15-minute interval of the record.")
    datetime: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfmnjbn: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Jobname.")
    smfmnrvn: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4),
                                                          doc="Record version (CICS), format 0VRM (V = version; R = release M = modification).")
    cics_stop: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                   doc="Finish time of measurement interval, which is one of the following times:.")
    cics_oadata1: so.Mapped[Optional[str]] = so.mapped_column(sa.String(130),
                                                              doc="The data added to the origin data by the adapter. This field is blank if the task was not started by using an adapter, or if it was and the adapter did not set this value.")
    elapsed: so.Mapped[float] = so.mapped_column(sa.Float,
                                                 doc="Total elapsed time of the transactions within the duration.")
    smfmnsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="System identification.")
    smfmnprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfmnspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    task_tran: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Transaction identification.")
    cics_start: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                          doc="Start time of measurement interval, which is one of the following times:.")
    task_trannum: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                    doc="Transaction identification number. The transaction number field is normally a 4-byte packed decimal number. However, some CICS system tasks are identified by transaction numbers that comprise special characters, as follows:.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfmnsid, smfmnprn, smfmnspn, task_tran, cics_start, task_trannum, elapsed),
        sa.Index("ix__smf110_1__cics_oadata1", "cics_oadata1"),
    )
