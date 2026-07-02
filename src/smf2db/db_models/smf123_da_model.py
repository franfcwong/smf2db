import datetime as dt
from typing import List, Optional

import sqlalchemy as sa
import sqlalchemy.orm as so

from .smf123_base import ReprMixin, Base123Da, DfhcbtsBase, DfhchnlBase, DfhcicsBase, DfhdataBase, DfhdestBase, \
    DfhdochBase, DfhfepiBase, DfhfileBase, DfhjourBase, DfhmappBase, DfhotelBase, DfhprogBase, DfhrmiBase, DfhsockBase, \
    DfhstorBase, DfhsyncBase, DfhtaskBase, DfhtempBase, DfhtermBase, DfhwebbBase, DfhwebcBase, Smf123RequestSummaryBase, \
    Smf123ServerBase


class Smf110Smf123Da(ReprMixin, Base123Da, DfhcbtsBase, DfhchnlBase, DfhcicsBase, DfhdataBase, DfhdestBase, DfhdochBase,
                     DfhfepiBase, DfhfileBase, DfhjourBase, DfhmappBase, DfhotelBase, DfhprogBase, DfhrmiBase,
                     DfhsockBase, DfhstorBase, DfhsyncBase, DfhtaskBase, DfhtempBase, DfhtermBase, DfhwebbBase,
                     DfhwebcBase):
    """The Smf110Smf123Da class stores the daily Smf110Smf123 record in the smf110_123_da table."""

    __tablename__ = "smf110_123_da"
    smfmnjbn: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Jobname.")
    smfmnrvn: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4),
                                                          doc="Record version (CICS), format 0VRM (V = version; R = release M = modification).")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    tasks: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                       doc="Total number of transaction records within the duration.")
    elapsed: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="Total elapsed time of the transactions within the duration.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    smfmnsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="System identification.")
    smfmnprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfmnspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    task_tran: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Transaction identification.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfmnsid, smfmnprn, smfmnspn, task_tran, date),
    )


class Smf123RequestDataDa(ReprMixin, Base123Da, Smf123RequestSummaryBase, DfhcbtsBase, DfhchnlBase, DfhcicsBase,
                          DfhdataBase, DfhdestBase, DfhdochBase, DfhfepiBase, DfhfileBase, DfhjourBase, DfhmappBase,
                          DfhotelBase, DfhprogBase, DfhrmiBase, DfhsockBase, DfhstorBase, DfhsyncBase, DfhtaskBase,
                          DfhtempBase, DfhtermBase, DfhwebbBase, DfhwebcBase):
    """The Smf123RequestDataDa class stores the daily Smf123RequestData record in the smf123_request_data_da table."""

    __tablename__ = "smf123_request_data_da"
    smf123s1_sor_identifier: so.Mapped[str] = so.mapped_column(sa.String(64),
                                                               doc="System of record identifier. Value of com.ibm.zosconnect.spi.Data.SOR_IDENTIFIER. See Note 2.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    smf123_server_sysplex: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name (ECVTSPLX).")
    smf123_sid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="System ID from the SID parameter.")
    smf123_server_jobname: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Job name of the server (JSABJBNM).")
    smf123_server_jobid: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Job ID of the server (JSABJBID).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf123_server_sysplex, smf123_sid, smf123_server_jobname, smf123_server_jobid, date,
                                smf123s1_sor_identifier),

        sa.ForeignKeyConstraint(
            ['smf123_server_sysplex', 'smf123_sid', 'smf123_server_jobname', 'smf123_server_jobid', 'date'],
            ['smf123_server_da.smf123_server_sysplex', 'smf123_server_da.smf123_sid',
             'smf123_server_da.smf123_server_jobname', 'smf123_server_da.smf123_server_jobid',
             'smf123_server_da.date']),
    )

    smf123_server_da: so.Mapped['Smf123ServerDa'] = so.relationship(back_populates='smf123_request_data_das',
                                                                    viewonly=True)


class Smf123ServerDa(ReprMixin, Base123Da, Smf123ServerBase):
    """The Smf123ServerDa class stores the daily Smf123Server record in the smf123_server_da table."""

    __tablename__ = "smf123_server_da"
    smf123_server_sysplex: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name (ECVTSPLX).")
    smf123_server_jobid: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Job ID of the server (JSABJBID).")
    smf123_server_jobname: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Job name of the server (JSABJBNM).")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    smf123_sid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="System ID from the SID parameter.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf123_server_sysplex, smf123_sid, smf123_server_jobname, smf123_server_jobid, date),
    )

    smf123_request_data_das: so.Mapped[List['Smf123RequestDataDa']] = so.relationship(back_populates='smf123_server_da',
                                                                                      viewonly=True)
