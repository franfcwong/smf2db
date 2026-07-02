import datetime as dt
from typing import List, Optional

import sqlalchemy as sa
import sqlalchemy.orm as so

from .smf123_base import ReprMixin, Base123, DfhcbtsBase, DfhchnlBase, DfhcicsBase, DfhdataBase, DfhdestBase, \
    DfhdochBase, DfhfepiBase, DfhfileBase, DfhjourBase, DfhmappBase, DfhotelBase, DfhprogBase, DfhrmiBase, DfhsockBase, \
    DfhstorBase, DfhsyncBase, DfhtaskBase, DfhtempBase, DfhtermBase, DfhwebbBase, DfhwebcBase, Smf123RequestDataBase, \
    Smf123ServerBase


class Smf110Smf123(ReprMixin, Base123, DfhcbtsBase, DfhchnlBase, DfhcicsBase, DfhdataBase, DfhdestBase, DfhdochBase,
                   DfhfepiBase, DfhfileBase, DfhjourBase, DfhmappBase, DfhotelBase, DfhprogBase, DfhrmiBase,
                   DfhsockBase, DfhstorBase, DfhsyncBase, DfhtaskBase, DfhtempBase, DfhtermBase, DfhwebbBase,
                   DfhwebcBase):
    """The Smf110Smf123 class stores the Smf110Smf123 section in the smf110_123 table."""

    __tablename__ = "smf110_123"
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
        sa.Index("ix__smf110_123__cics_oadata1", "cics_oadata1"),
    )


class Smf123RequestData(ReprMixin, Base123, Smf123RequestDataBase, DfhcbtsBase, DfhchnlBase, DfhcicsBase, DfhdataBase,
                        DfhdestBase, DfhdochBase, DfhfepiBase, DfhfileBase, DfhjourBase, DfhmappBase, DfhotelBase,
                        DfhprogBase, DfhrmiBase, DfhsockBase, DfhstorBase, DfhsyncBase, DfhtaskBase, DfhtempBase,
                        DfhtermBase, DfhwebbBase, DfhwebcBase):
    """The Smf123RequestData class stores the Smf123RequestData section in the smf123_request_data table."""

    __tablename__ = "smf123_request_data"
    smf123s1_sor_identifier: so.Mapped[str] = so.mapped_column(sa.String(64),
                                                               doc="System of record identifier. Value of com.ibm.zosconnect.spi.Data.SOR_IDENTIFIER. See Note 2.")
    smf123s1_req_id: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                       doc="Request identifier that is unique within a z/OS Connect server instance.")
    datetime_15m: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                      doc="The 15-minute interval of the record.")
    datetime: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfmnsid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="System identification.")
    smfmnprn: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfmnspn: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    smfmnjbn: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Jobname.")
    smfmnrvn: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4),
                                                          doc="Record version (CICS), format 0VRM (V = version; R = release M = modification).")
    task_tran: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="Transaction identification.")
    smf123_server_sysplex: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name (ECVTSPLX).")
    smf123_sid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="System ID from the SID parameter.")
    smf123_server_jobname: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Job name of the server (JSABJBNM).")
    smf123_server_jobid: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Job ID of the server (JSABJBID).")
    smf123_timestamp: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                                doc="Time when record was moved into the SMF buffer, in hundredths of a second since midnight.'")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf123_server_sysplex, smf123_sid, smf123_server_jobname, smf123_server_jobid,
                                smf123_timestamp, smf123s1_sor_identifier, smf123s1_req_id),
        sa.ForeignKeyConstraint(
            ['smf123_server_sysplex', 'smf123_sid', 'smf123_server_jobname', 'smf123_server_jobid', 'smf123_timestamp'],
            ['smf123_server.smf123_server_sysplex', 'smf123_server.smf123_sid', 'smf123_server.smf123_server_jobname',
             'smf123_server.smf123_server_jobid', 'smf123_server.smf123_timestamp']),
    )

    smf123_server: so.Mapped['Smf123Server'] = so.relationship(back_populates='smf123_request_datas', viewonly=True)


class Smf123Server(ReprMixin, Base123, Smf123ServerBase):
    """The Smf123Server class stores the Smf123Server section in the smf123_server table."""

    __tablename__ = "smf123_server"
    smf123_server_sysplex: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name (ECVTSPLX).")
    smf123_server_jobid: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Job ID of the server (JSABJBID).")
    smf123_server_jobname: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Job name of the server (JSABJBNM).")
    datetime_15m: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                      doc="The 15-minute interval of the record.")
    datetime: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smf123_sid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="System ID from the SID parameter.")
    smf123_timestamp: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                                doc="Time when record was moved into the SMF buffer, in hundredths of a second since midnight.'")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf123_server_sysplex, smf123_sid, smf123_server_jobname, smf123_server_jobid,
                                smf123_timestamp),
    )

    smf123_request_datas: so.Mapped[List['Smf123RequestData']] = so.relationship(back_populates='smf123_server',
                                                                                 viewonly=True)
