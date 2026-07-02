import datetime as dt
from typing import List, Optional

import sqlalchemy as sa
import sqlalchemy.orm as so

from .smf1102_base import ReprMixin, Base1102Hr, DfhwbgdsBase, DfhisrdsBase, DfhxmrdsBase, DfhmlrdsBase, DfhmqrdsBase, \
    DfhmqgdsBase, DfhpgrdsBase, Dfha16dsBase, DfhldbdsBase, DsgtcbpBase, SmsbodyBase, Dfha24dsBase, Dfha23dsBase, \
    DfhtqgdsBase, DfhwbrdsBase, Dfhcfs6dBase, Dfhcfs7dBase, Dfha22dsBase, ldgglobal, DfhpgedsBase, DfhxmgdsBase, \
    DfhsmtdsBase, DfhldrdsBase, DfhtqrdsBase, Dfha17dsBase, Dfha09dsBase, DfhdsrdsBase, DfhsdgdsBase, DfhdstdsBase, \
    Dfha06dsBase, Dfhw2rdsBase, NqgbodyBase, DfhsmsdsBase, SmsglobalBase, DfhsdrdsBase, DfhpgddsBase, Dfha14dsBase, \
    Dfha20dsBase, DfhmprdsBase, A08bssdsBase, Dfha08dsBase, DfhpirdsBase, A16statsBase, DfhtdgdsBase, DfhepgdsBase, \
    DfheprdsBase, DfhasgdsBase, DfhdhddsBase, Dfha03dsBase, DfhsjsdsBase, DfhpiwdsBase, Dfha21dsBase, DfhxmcdsBase, \
    DfhtsgdsBase, Dfha04dsBase, DfheccdsBase, DfhrlrdsBase, SmtbodyBase, DfhnqgdsBase, DfhdsgdsBase, Dfhxqs1dBase, \
    Dfhcfs8dBase, DfhtdrdsBase, DfhsjndsBase, DfhlgsdsBase, DfhsmddsBase, DfhldydsBase, LdgdsastatBase, DfhpgpdsBase, \
    DfhsordsBase, Dfhncs5dBase, DfhlgrdsBase, DfhecgdsBase, DfhecrdsBase, DfhlggdsBase, DfhmngdsBase, Dfhd2gdsBase, \
    DfhldpdsBase, Dfhxqs3dBase, Dfhd2rdsBase, DfhstgdsBase, DfhsogdsBase, Dfhxqs2dBase, DfhpggdsBase, Dfhcfs9dBase, \
    DsgtcbmBase, Dfhncs4dBase, DfhrmgdsBase, DfhusgdsBase


class DfhwbgdsHr(ReprMixin, Base1102Hr, DfhwbgdsBase):
    """The DfhwbgdsHr class stores the hourly Dfhwbgds record in the dfhwbgds_hr table."""

    __tablename__ = "dfhwbgds_hr"
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime),
    )


class DfhisrdsHr(ReprMixin, Base1102Hr, DfhisrdsBase):
    """The DfhisrdsHr class stores the hourly Dfhisrds record in the dfhisrds_hr table."""

    __tablename__ = "dfhisrds_hr"
    isr_ipconn_name: so.Mapped[str] = so.mapped_column(sa.String(8), doc="IPCONN name.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, isr_ipconn_name),
    )


class DfhxmrdsHr(ReprMixin, Base1102Hr, DfhxmrdsBase):
    """The DfhxmrdsHr class stores the hourly Dfhxmrds record in the dfhxmrds_hr table."""

    __tablename__ = "dfhxmrds_hr"
    xmrti: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Transaction ID.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, xmrti),
    )


class DfhmlrdsHr(ReprMixin, Base1102Hr, DfhmlrdsBase):
    """The DfhmlrdsHr class stores the hourly Dfhmlrds record in the dfhmlrds_hr table."""

    __tablename__ = "dfhmlrds_hr"
    mlr_xmltransform_name: so.Mapped[str] = so.mapped_column(sa.String(32), doc="Xmltransform name.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, mlr_xmltransform_name),
    )


class DfhmqrdsHr(ReprMixin, Base1102Hr, DfhmqrdsBase):
    """The DfhmqrdsHr class stores the hourly Dfhmqrds record in the dfhmqrds_hr table."""

    __tablename__ = "dfhmqrds_hr"
    mqr_name: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Resource name.")
    mqr_qname: so.Mapped[str] = so.mapped_column(sa.String(48), doc="MQ Queue name.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, mqr_name, mqr_qname),
    )


class DfhmqgdsHr(ReprMixin, Base1102Hr, DfhmqgdsBase):
    """The DfhmqgdsHr class stores the hourly Dfhmqgds record in the dfhmqgds_hr table."""

    __tablename__ = "dfhmqgds_hr"
    mqg_qmgr_name: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Queue manager name.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, mqg_qmgr_name),
    )


class DfhpgrdsHr(ReprMixin, Base1102Hr, DfhpgrdsBase):
    """The DfhpgrdsHr class stores the hourly Dfhpgrds record in the dfhpgrds_hr table."""

    __tablename__ = "dfhpgrds_hr"
    pgr_jvmprogram_name: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Jvmprogram Name.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, pgr_jvmprogram_name),
    )


class Dfha16dsHr(ReprMixin, Base1102Hr, Dfha16dsBase):
    """The Dfha16dsHr class stores the hourly Dfha16ds record in the dfha16ds_hr table."""

    __tablename__ = "dfha16ds_hr"
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime),
    )

    a16stats_hrs: so.Mapped[List['A16statsHr']] = so.relationship(back_populates='dfha16ds_hr', viewonly=True)


class DfhldbdsHr(ReprMixin, Base1102Hr, DfhldbdsBase):
    """The DfhldbdsHr class stores the hourly Dfhldbds record in the dfhldbds_hr table."""

    __tablename__ = "dfhldbds_hr"
    ldb_library_name: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Library name.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, ldb_library_name),
    )

    ldb_dsnames_hrs: so.Mapped[List['LdbDsnamesHr']] = so.relationship(back_populates='dfhldbds_hr', viewonly=True)


class DsgtcbpHr(ReprMixin, Base1102Hr, DsgtcbpBase):
    """The DsgtcbpHr class stores the hourly Dsgtcbp record in the dsgtcbp_hr table."""

    __tablename__ = "dsgtcbp_hr"
    dsgtcbpn: so.Mapped[int] = so.mapped_column(sa.Integer, doc="TCB Pool Number.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, dsgtcbpn),
        sa.ForeignKeyConstraint(
            ['smfstsid', 'smfstprn', 'smfstspn', 'datetime'],
            ['dfhdsgds_hr.smfstsid', 'dfhdsgds_hr.smfstprn', 'dfhdsgds_hr.smfstspn', 'dfhdsgds_hr.datetime']),
    )

    dfhdsgds_hr: so.Mapped['DfhdsgdsHr'] = so.relationship(back_populates='dsgtcbp_hrs', viewonly=True)


class SmsbodyHr(ReprMixin, Base1102Hr, SmsbodyBase):
    """The SmsbodyHr class stores the hourly Smsbody record in the smsbody_hr table."""

    __tablename__ = "smsbody_hr"
    smsdsaname: so.Mapped[str] = so.mapped_column(sa.String(8), doc="DSA name.")
    smsdsalimit: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current DSA limit.")
    smsedsalimit: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current EDSA limit.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smsdsaname),
        sa.ForeignKeyConstraint(
            ['smfstsid', 'smfstprn', 'smfstspn', 'datetime'],
            ['smsglobal_hr.smfstsid', 'smsglobal_hr.smfstprn', 'smsglobal_hr.smfstspn', 'smsglobal_hr.datetime']),
    )

    smsglobal_hr: so.Mapped['SmsglobalHr'] = so.relationship(back_populates='smsbody_hrs', viewonly=True)


class Dfha24dsHr(ReprMixin, Base1102Hr, Dfha24dsBase):
    """The Dfha24dsHr class stores the hourly Dfha24ds record in the dfha24ds_hr table."""

    __tablename__ = "dfha24ds_hr"
    a24targ: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Target name.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, a24targ),
    )


class Dfha23dsHr(ReprMixin, Base1102Hr, Dfha23dsBase):
    """The Dfha23dsHr class stores the hourly Dfha23ds record in the dfha23ds_hr table."""

    __tablename__ = "dfha23ds_hr"
    a23pool: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Pool name.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, a23pool),
    )


class DfhtqgdsHr(ReprMixin, Base1102Hr, DfhtqgdsBase):
    """The DfhtqgdsHr class stores the hourly Dfhtqgds record in the dfhtqgds_hr table."""

    __tablename__ = "dfhtqgds_hr"
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime),
    )


class DfhwbrdsHr(ReprMixin, Base1102Hr, DfhwbrdsBase):
    """The DfhwbrdsHr class stores the hourly Dfhwbrds record in the dfhwbrds_hr table."""

    __tablename__ = "dfhwbrds_hr"
    wbr_urimap_name: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Urimap name.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, wbr_urimap_name),
    )


class Dfhcfs6dHr(ReprMixin, Base1102Hr, Dfhcfs6dBase):
    """The Dfhcfs6dHr class stores the hourly Dfhcfs6d record in the dfhcfs6d_hr table."""

    __tablename__ = "dfhcfs6d_hr"
    s6name: so.Mapped[str] = so.mapped_column(sa.String(16), doc="Full name of list structure.")
    s6pool: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Pool name part of structure name.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, s6name, s6pool),
    )


class Dfhcfs7dHr(ReprMixin, Base1102Hr, Dfhcfs7dBase):
    """The Dfhcfs7dHr class stores the hourly Dfhcfs7d record in the dfhcfs7d_hr table."""

    __tablename__ = "dfhcfs7d_hr"
    s7table: so.Mapped[str] = so.mapped_column(sa.String(16), doc="Table name padded with spaces.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, s7table),
    )


class Dfha22dsHr(ReprMixin, Base1102Hr, Dfha22dsBase):
    """The Dfha22dsHr class stores the hourly Dfha22ds record in the dfha22ds_hr table."""

    __tablename__ = "dfha22ds_hr"
    a22pool: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Pool name.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, a22pool),
    )


class LdgglobalHr(ReprMixin, Base1102Hr, ldgglobal):
    """The LdgglobalHr class stores the hourly Ldgglobal record in the ldgglobal_hr table."""

    __tablename__ = "ldgglobal_hr"
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime),
    )

    ldgdsastat_hrs: so.Mapped[List['LdgdsastatHr']] = so.relationship(back_populates='ldgglobal_hr', viewonly=True)


class DfhpgedsHr(ReprMixin, Base1102Hr, DfhpgedsBase):
    """The DfhpgedsHr class stores the hourly Dfhpgeds record in the dfhpgeds_hr table."""

    __tablename__ = "dfhpgeds_hr"
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime),
    )


class DfhxmgdsHr(ReprMixin, Base1102Hr, DfhxmgdsBase):
    """The DfhxmgdsHr class stores the hourly Dfhxmgds record in the dfhxmgds_hr table."""

    __tablename__ = "dfhxmgds_hr"
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime),
    )


class DfhsmtdsHr(ReprMixin, Base1102Hr, DfhsmtdsBase):
    """The DfhsmtdsHr class stores the hourly Dfhsmtds record in the dfhsmtds_hr table."""

    __tablename__ = "dfhsmtds_hr"
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime),
    )

    smtbody_hrs: so.Mapped[List['SmtbodyHr']] = so.relationship(back_populates='dfhsmtds_hr', viewonly=True)


class DfhldrdsHr(ReprMixin, Base1102Hr, DfhldrdsBase):
    """The DfhldrdsHr class stores the hourly Dfhldrds record in the dfhldrds_hr table."""

    __tablename__ = "dfhldrds_hr"
    ldrpname: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Program name.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, ldrpname),
    )


class DfhtqrdsHr(ReprMixin, Base1102Hr, DfhtqrdsBase):
    """The DfhtqrdsHr class stores the hourly Dfhtqrds record in the dfhtqrds_hr table."""

    __tablename__ = "dfhtqrds_hr"
    tqrqid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="TD Queue identifier.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, tqrqid),
    )


class Dfha17dsHr(ReprMixin, Base1102Hr, Dfha17dsBase):
    """The Dfha17dsHr class stores the hourly Dfha17ds record in the dfha17ds_hr table."""

    __tablename__ = "dfha17ds_hr"
    a17fnam: so.Mapped[str] = so.mapped_column(sa.String(8), doc="File name.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, a17fnam),
    )


class Dfha09dsHr(ReprMixin, Base1102Hr, Dfha09dsBase):
    """The Dfha09dsHr class stores the hourly Dfha09ds record in the dfha09ds_hr table."""

    __tablename__ = "dfha09ds_hr"
    a09dsid: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Filename.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, a09dsid),
    )


class DfhdsrdsHr(ReprMixin, Base1102Hr, DfhdsrdsBase):
    """The DfhdsrdsHr class stores the hourly Dfhdsrds record in the dfhdsrds_hr table."""

    __tablename__ = "dfhdsrds_hr"
    dsrds_tcb_address: so.Mapped[str] = so.mapped_column(sa.String(10), doc="Address of MVS TCB.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, dsrds_tcb_address),
    )


class DfhsdgdsHr(ReprMixin, Base1102Hr, DfhsdgdsBase):
    """The DfhsdgdsHr class stores the hourly Dfhsdgds record in the dfhsdgds_hr table."""

    __tablename__ = "dfhsdgds_hr"
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime),
    )


class DfhdstdsHr(ReprMixin, Base1102Hr, DfhdstdsBase):
    """The DfhdstdsHr class stores the hourly Dfhdstds record in the dfhdstds_hr table."""

    __tablename__ = "dfhdstds_hr"
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime),
    )


class LdbDsnamesHr(ReprMixin, Base1102Hr):
    """The LdbDsnamesHr class stores the hourly LdbDsnames record in the ldb_dsnames_hr table."""

    __tablename__ = "ldb_dsnames_hr"
    ldb_dsname: so.Mapped[str] = so.mapped_column(sa.String(44), doc="Library Dsname.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    ldb_library_name: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Library name.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, ldb_library_name, ldb_dsname),
        sa.ForeignKeyConstraint(
            ['smfstsid', 'smfstprn', 'smfstspn', 'datetime', 'ldb_library_name'],
            ['dfhldbds_hr.smfstsid', 'dfhldbds_hr.smfstprn', 'dfhldbds_hr.smfstspn', 'dfhldbds_hr.datetime',
             'dfhldbds_hr.ldb_library_name']),
    )

    dfhldbds_hr: so.Mapped['DfhldbdsHr'] = so.relationship(back_populates='ldb_dsnames_hrs', viewonly=True)


class Dfha06dsHr(ReprMixin, Base1102Hr, Dfha06dsBase):
    """The Dfha06dsHr class stores the hourly Dfha06ds record in the dfha06ds_hr table."""

    __tablename__ = "dfha06ds_hr"
    a06teti: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Terminal id.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, a06teti),
    )


class Dfhw2rdsHr(ReprMixin, Base1102Hr, Dfhw2rdsBase):
    """The Dfhw2rdsHr class stores the hourly Dfhw2rds record in the dfhw2rds_hr table."""

    __tablename__ = "dfhw2rds_hr"
    w2r_atomserv_name: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Atomservice name.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, w2r_atomserv_name),
    )


class NqgbodyHr(ReprMixin, Base1102Hr, NqgbodyBase):
    """The NqgbodyHr class stores the hourly Nqgbody record in the nqgbody_hr table."""

    __tablename__ = "nqgbody_hr"
    nqgpool: so.Mapped[str] = so.mapped_column(sa.String(8), doc="ENQ pool id.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, nqgpool),
        sa.ForeignKeyConstraint(
            ['smfstsid', 'smfstprn', 'smfstspn', 'datetime'],
            ['dfhnqgds_hr.smfstsid', 'dfhnqgds_hr.smfstprn', 'dfhnqgds_hr.smfstspn', 'dfhnqgds_hr.datetime']),
    )

    dfhnqgds_hr: so.Mapped['DfhnqgdsHr'] = so.relationship(back_populates='nqgbody_hrs', viewonly=True)


class SmsglobalHr(ReprMixin, Base1102Hr, SmsglobalBase, DfhsmsdsBase):
    """The SmsglobalHr class stores the hourly Smsglobal record in the smsglobal_hr table."""

    __tablename__ = "smsglobal_hr"
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime),
    )

    smsbody_hrs: so.Mapped[List['SmsbodyHr']] = so.relationship(back_populates='smsglobal_hr', viewonly=True)


class DfhsdrdsHr(ReprMixin, Base1102Hr, DfhsdrdsBase):
    """The DfhsdrdsHr class stores the hourly Dfhsdrds record in the dfhsdrds_hr table."""

    __tablename__ = "dfhsdrds_hr"
    sdrcode: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Dumpcode.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, sdrcode),
    )


class DfhpgddsHr(ReprMixin, Base1102Hr, DfhpgddsBase):
    """The DfhpgddsHr class stores the hourly Dfhpgdds record in the dfhpgdds_hr table."""

    __tablename__ = "dfhpgdds_hr"
    pgd_program_name: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Program Name.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, pgd_program_name),
    )


class Dfha14dsHr(ReprMixin, Base1102Hr, Dfha14dsBase):
    """The Dfha14dsHr class stores the hourly Dfha14ds record in the dfha14ds_hr table."""

    __tablename__ = "dfha14ds_hr"
    a14cntn: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Connection name.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, a14cntn),
    )


class Dfha20dsHr(ReprMixin, Base1102Hr, Dfha20dsBase):
    """The Dfha20dsHr class stores the hourly Dfha20ds record in the dfha20ds_hr table."""

    __tablename__ = "dfha20ds_hr"
    a20sysn: so.Mapped[str] = so.mapped_column(sa.String(4), doc="System name.")
    a20mode: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Mode name.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, a20sysn, a20mode),
    )


class DfhmprdsHr(ReprMixin, Base1102Hr, DfhmprdsBase):
    """The DfhmprdsHr class stores the hourly Dfhmprds record in the dfhmprds_hr table."""

    __tablename__ = "dfhmprds_hr"
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime),
    )


class A08bssdsHr(ReprMixin, Base1102Hr, A08bssdsBase):
    """The A08bssdsHr class stores the hourly A08bssds record in the a08bssds_hr table."""

    __tablename__ = "a08bssds_hr"
    a08bkbsz: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Buffer size.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    isIndxBuffer: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Is index buffer.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    a08srpid: so.Mapped[int] = so.mapped_column(sa.Integer, doc="LSR pool number.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, a08srpid, a08bkbsz, isIndxBuffer),
        sa.ForeignKeyConstraint(
            ['smfstsid', 'smfstprn', 'smfstspn', 'datetime', 'a08srpid'],
            ['dfha08ds_hr.smfstsid', 'dfha08ds_hr.smfstprn', 'dfha08ds_hr.smfstspn', 'dfha08ds_hr.datetime',
             'dfha08ds_hr.a08srpid']),
    )

    dfha08ds_hr: so.Mapped['Dfha08dsHr'] = so.relationship(back_populates='a08bssds_hrs', viewonly=True)


class Dfha08dsHr(ReprMixin, Base1102Hr, Dfha08dsBase):
    """The Dfha08dsHr class stores the hourly Dfha08ds record in the dfha08ds_hr table."""

    __tablename__ = "dfha08ds_hr"
    a08srpid: so.Mapped[int] = so.mapped_column(sa.Integer, doc="LSR pool number.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, a08srpid),
    )

    a08bssds_hrs: so.Mapped[List['A08bssdsHr']] = so.relationship(back_populates='dfha08ds_hr', viewonly=True)


class DfhpirdsHr(ReprMixin, Base1102Hr, DfhpirdsBase):
    """The DfhpirdsHr class stores the hourly Dfhpirds record in the dfhpirds_hr table."""

    __tablename__ = "dfhpirds_hr"
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime),
    )


class A16statsHr(ReprMixin, Base1102Hr, A16statsBase):
    """The A16statsHr class stores the hourly A16stats record in the a16stats_hr table."""

    __tablename__ = "a16stats_hr"
    a16tnam: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Table name.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, a16tnam),
        sa.ForeignKeyConstraint(
            ['smfstsid', 'smfstprn', 'smfstspn', 'datetime'],
            ['dfha16ds_hr.smfstsid', 'dfha16ds_hr.smfstprn', 'dfha16ds_hr.smfstspn', 'dfha16ds_hr.datetime']),
    )

    dfha16ds_hr: so.Mapped['Dfha16dsHr'] = so.relationship(back_populates='a16stats_hrs', viewonly=True)


class DfhtdgdsHr(ReprMixin, Base1102Hr, DfhtdgdsBase):
    """The DfhtdgdsHr class stores the hourly Dfhtdgds record in the dfhtdgds_hr table."""

    __tablename__ = "dfhtdgds_hr"
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime),
    )


class LdyDsnamesHr(ReprMixin, Base1102Hr):
    """The LdyDsnamesHr class stores the hourly LdyDsnames record in the ldy_dsnames_hr table."""

    __tablename__ = "ldy_dsnames_hr"
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    ldy_library_platform_name: so.Mapped[str] = so.mapped_column(sa.String(64), doc="Platform name.")
    ldy_library_application_name: so.Mapped[str] = so.mapped_column(sa.String(64), doc="Application name.")
    ldb_dsname: so.Mapped[str] = so.mapped_column(sa.String(44), doc="Library Dsname.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, ldy_library_platform_name,
                                ldy_library_application_name, ldb_dsname),
        sa.ForeignKeyConstraint(
            ['smfstsid', 'smfstprn', 'smfstspn', 'datetime', 'ldy_library_platform_name',
             'ldy_library_application_name'],
            ['dfhldyds_hr.smfstsid', 'dfhldyds_hr.smfstprn', 'dfhldyds_hr.smfstspn', 'dfhldyds_hr.datetime',
             'dfhldyds_hr.ldy_library_platform_name', 'dfhldyds_hr.ldy_library_application_name']),
    )

    dfhldyds_hr: so.Mapped['DfhldydsHr'] = so.relationship(back_populates='ldy_dsnames_hrs', viewonly=True)


class DfhepgdsHr(ReprMixin, Base1102Hr, DfhepgdsBase):
    """The DfhepgdsHr class stores the hourly Dfhepgds record in the dfhepgds_hr table."""

    __tablename__ = "dfhepgds_hr"
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime),
    )


class DfheprdsHr(ReprMixin, Base1102Hr, DfheprdsBase):
    """The DfheprdsHr class stores the hourly Dfheprds record in the dfheprds_hr table."""

    __tablename__ = "dfheprds_hr"
    epr_adapter_name: so.Mapped[str] = so.mapped_column(sa.String(32), doc="EP adapter name.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, epr_adapter_name),
    )


class DfhasgdsHr(ReprMixin, Base1102Hr, DfhasgdsBase):
    """The DfhasgdsHr class stores the hourly Dfhasgds record in the dfhasgds_hr table."""

    __tablename__ = "dfhasgds_hr"
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime),
    )


class DfhdhddsHr(ReprMixin, Base1102Hr, DfhdhddsBase):
    """The DfhdhddsHr class stores the hourly Dfhdhdds record in the dfhdhdds_hr table."""

    __tablename__ = "dfhdhdds_hr"
    dhd_doctemplate_name: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Doctemplate name.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, dhd_doctemplate_name),
    )


class Dfha03dsHr(ReprMixin, Base1102Hr, Dfha03dsBase):
    """The Dfha03dsHr class stores the hourly Dfha03ds record in the dfha03ds_hr table."""

    __tablename__ = "dfha03ds_hr"
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime),
    )


class DfhsjsdsHr(ReprMixin, Base1102Hr, DfhsjsdsBase):
    """The DfhsjsdsHr class stores the hourly Dfhsjsds record in the dfhsjsds_hr table."""

    __tablename__ = "dfhsjsds_hr"
    sjs_jvmserver_name: so.Mapped[str] = so.mapped_column(sa.String(8), doc="JVMSERVER name.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, sjs_jvmserver_name),
    )


class DfhpiwdsHr(ReprMixin, Base1102Hr, DfhpiwdsBase):
    """The DfhpiwdsHr class stores the hourly Dfhpiwds record in the dfhpiwds_hr table."""

    __tablename__ = "dfhpiwds_hr"
    piw_webservice_name: so.Mapped[str] = so.mapped_column(sa.String(32), doc="Webservice name.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, piw_webservice_name),
    )


class Dfha21dsHr(ReprMixin, Base1102Hr, Dfha21dsBase):
    """The Dfha21dsHr class stores the hourly Dfha21ds record in the dfha21ds_hr table."""

    __tablename__ = "dfha21ds_hr"
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime),
    )


class DfhxmcdsHr(ReprMixin, Base1102Hr, DfhxmcdsBase):
    """The DfhxmcdsHr class stores the hourly Dfhxmcds record in the dfhxmcds_hr table."""

    __tablename__ = "dfhxmcds_hr"
    xmctcl: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Tclass name.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, xmctcl),
    )


class DfhtsgdsHr(ReprMixin, Base1102Hr, DfhtsgdsBase):
    """The DfhtsgdsHr class stores the hourly Dfhtsgds record in the dfhtsgds_hr table."""

    __tablename__ = "dfhtsgds_hr"
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime),
    )


class Dfha04dsHr(ReprMixin, Base1102Hr, Dfha04dsBase):
    """The Dfha04dsHr class stores the hourly Dfha04ds record in the dfha04ds_hr table."""

    __tablename__ = "dfha04ds_hr"
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime),
    )


class DfheccdsHr(ReprMixin, Base1102Hr, DfheccdsBase):
    """The DfheccdsHr class stores the hourly Dfheccds record in the dfheccds_hr table."""

    __tablename__ = "dfheccds_hr"
    ecc_eventbinding_name: so.Mapped[str] = so.mapped_column(sa.String(32), doc="Eventbinding name.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, ecc_eventbinding_name),
    )


class DfhrlrdsHr(ReprMixin, Base1102Hr, DfhrlrdsBase):
    """The DfhrlrdsHr class stores the hourly Dfhrlrds record in the dfhrlrds_hr table."""

    __tablename__ = "dfhrlrds_hr"
    rlr_bundle_name: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Bundle name.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, rlr_bundle_name),
    )


class SmtbodyHr(ReprMixin, Base1102Hr, SmtbodyBase):
    """The SmtbodyHr class stores the hourly Smtbody record in the smtbody_hr table."""

    __tablename__ = "smtbody_hr"
    smtdsaname: so.Mapped[str] = so.mapped_column(sa.String(8), doc="DSA name.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smtdsaname),
        sa.ForeignKeyConstraint(
            ['smfstsid', 'smfstprn', 'smfstspn', 'datetime'],
            ['dfhsmtds_hr.smfstsid', 'dfhsmtds_hr.smfstprn', 'dfhsmtds_hr.smfstspn', 'dfhsmtds_hr.datetime']),
    )

    dfhsmtds_hr: so.Mapped['DfhsmtdsHr'] = so.relationship(back_populates='smtbody_hrs', viewonly=True)


class DfhnqgdsHr(ReprMixin, Base1102Hr, DfhnqgdsBase):
    """The DfhnqgdsHr class stores the hourly Dfhnqgds record in the dfhnqgds_hr table."""

    __tablename__ = "dfhnqgds_hr"
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime),
    )

    nqgbody_hrs: so.Mapped[List['NqgbodyHr']] = so.relationship(back_populates='dfhnqgds_hr', viewonly=True)


class DfhdsgdsHr(ReprMixin, Base1102Hr, DfhdsgdsBase):
    """The DfhdsgdsHr class stores the hourly Dfhdsgds record in the dfhdsgds_hr table."""

    __tablename__ = "dfhdsgds_hr"
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime),
    )

    dsgtcbm_hrs: so.Mapped[List['DsgtcbmHr']] = so.relationship(back_populates='dfhdsgds_hr', viewonly=True)
    dsgtcbp_hrs: so.Mapped[List['DsgtcbpHr']] = so.relationship(back_populates='dfhdsgds_hr', viewonly=True)


class Dfhxqs1dHr(ReprMixin, Base1102Hr, Dfhxqs1dBase):
    """The Dfhxqs1dHr class stores the hourly Dfhxqs1d record in the dfhxqs1d_hr table."""

    __tablename__ = "dfhxqs1d_hr"
    s1name: so.Mapped[str] = so.mapped_column(sa.String(16), doc="Full name of list structure.")
    s1pool: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Pool name part of structure name.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, s1name, s1pool),
    )


class Dfhcfs8dHr(ReprMixin, Base1102Hr, Dfhcfs8dBase):
    """The Dfhcfs8dHr class stores the hourly Dfhcfs8d record in the dfhcfs8d_hr table."""

    __tablename__ = "dfhcfs8d_hr"
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime),
    )


class DfhtdrdsHr(ReprMixin, Base1102Hr, DfhtdrdsBase):
    """The DfhtdrdsHr class stores the hourly Dfhtdrds record in the dfhtdrds_hr table."""

    __tablename__ = "dfhtdrds_hr"
    tdrcode: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Dumpcode.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, tdrcode),
    )


class DfhsjndsHr(ReprMixin, Base1102Hr, DfhsjndsBase):
    """The DfhsjndsHr class stores the hourly Dfhsjnds record in the dfhsjnds_hr table."""

    __tablename__ = "dfhsjnds_hr"
    sjn_nodejsapp_name: so.Mapped[str] = so.mapped_column(sa.String(32), doc="NODEJSAPP name.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, sjn_nodejsapp_name),
    )


class DfhlgsdsHr(ReprMixin, Base1102Hr, DfhlgsdsBase):
    """The DfhlgsdsHr class stores the hourly Dfhlgsds record in the dfhlgsds_hr table."""

    __tablename__ = "dfhlgsds_hr"
    lgsstrnam: so.Mapped[str] = so.mapped_column(sa.String(26), doc="Log stream name.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, lgsstrnam),
    )


class DfhsmddsHr(ReprMixin, Base1102Hr, DfhsmddsBase):
    """The DfhsmddsHr class stores the hourly Dfhsmdds record in the dfhsmdds_hr table."""

    __tablename__ = "dfhsmdds_hr"
    smdspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Subpool name.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smdspn),
    )


class DfhldydsHr(ReprMixin, Base1102Hr, DfhldydsBase):
    """The DfhldydsHr class stores the hourly Dfhldyds record in the dfhldyds_hr table."""

    __tablename__ = "dfhldyds_hr"
    ldy_library_platform_name: so.Mapped[str] = so.mapped_column(sa.String(64), doc="Platform name.")
    ldy_library_application_name: so.Mapped[str] = so.mapped_column(sa.String(64), doc="Application name.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, ldy_library_platform_name,
                                ldy_library_application_name),
    )

    ldy_dsnames_hrs: so.Mapped[List['LdyDsnamesHr']] = so.relationship(back_populates='dfhldyds_hr', viewonly=True)


class LdgdsastatHr(ReprMixin, Base1102Hr, LdgdsastatBase):
    """The LdgdsastatHr class stores the hourly Ldgdsastat record in the ldgdsastat_hr table."""

    __tablename__ = "ldgdsastat_hr"
    ldgdsaindex: so.Mapped[int] = so.mapped_column(sa.Integer, doc="DSA index.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, ldgdsaindex),
        sa.ForeignKeyConstraint(
            ['smfstsid', 'smfstprn', 'smfstspn', 'datetime'],
            ['ldgglobal_hr.smfstsid', 'ldgglobal_hr.smfstprn', 'ldgglobal_hr.smfstspn', 'ldgglobal_hr.datetime']),
    )

    ldgglobal_hr: so.Mapped['LdgglobalHr'] = so.relationship(back_populates='ldgdsastat_hrs', viewonly=True)


class DfhpgpdsHr(ReprMixin, Base1102Hr, DfhpgpdsBase):
    """The DfhpgpdsHr class stores the hourly Dfhpgpds record in the dfhpgpds_hr table."""

    __tablename__ = "dfhpgpds_hr"
    pgp_jvmprogram_platform_name: so.Mapped[str] = so.mapped_column(sa.String(64), doc="Platform name.")
    pgp_jvmprogram_application_name: so.Mapped[str] = so.mapped_column(sa.String(64), doc="Application name.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, pgp_jvmprogram_platform_name,
                                pgp_jvmprogram_application_name),
    )


class DfhsordsHr(ReprMixin, Base1102Hr, DfhsordsBase):
    """The DfhsordsHr class stores the hourly Dfhsords record in the dfhsords_hr table."""

    __tablename__ = "dfhsords_hr"
    sor_service_name: so.Mapped[str] = so.mapped_column(sa.String(8), doc="TCP/IP Service name.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, sor_service_name),
    )


class Dfhncs5dHr(ReprMixin, Base1102Hr, Dfhncs5dBase):
    """The Dfhncs5dHr class stores the hourly Dfhncs5d record in the dfhncs5d_hr table."""

    __tablename__ = "dfhncs5d_hr"
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime),
    )


class DfhlgrdsHr(ReprMixin, Base1102Hr, DfhlgrdsBase):
    """The DfhlgrdsHr class stores the hourly Dfhlgrds record in the dfhlgrds_hr table."""

    __tablename__ = "dfhlgrds_hr"
    lgrjnlname: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Journal name.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, lgrjnlname),
    )


class DfhecgdsHr(ReprMixin, Base1102Hr, DfhecgdsBase):
    """The DfhecgdsHr class stores the hourly Dfhecgds record in the dfhecgds_hr table."""

    __tablename__ = "dfhecgds_hr"
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime),
    )


class DfhecrdsHr(ReprMixin, Base1102Hr, DfhecrdsBase):
    """The DfhecrdsHr class stores the hourly Dfhecrds record in the dfhecrds_hr table."""

    __tablename__ = "dfhecrds_hr"
    ecr_eventbinding_name: so.Mapped[str] = so.mapped_column(sa.String(32), doc="Eventbinding name.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, ecr_eventbinding_name),
    )


class DfhlggdsHr(ReprMixin, Base1102Hr, DfhlggdsBase):
    """The DfhlggdsHr class stores the hourly Dfhlggds record in the dfhlggds_hr table."""

    __tablename__ = "dfhlggds_hr"
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime),
    )


class DfhmngdsHr(ReprMixin, Base1102Hr, DfhmngdsBase):
    """The DfhmngdsHr class stores the hourly Dfhmngds record in the dfhmngds_hr table."""

    __tablename__ = "dfhmngds_hr"
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime),
    )


class Dfhd2gdsHr(ReprMixin, Base1102Hr, Dfhd2gdsBase):
    """The Dfhd2gdsHr class stores the hourly Dfhd2gds record in the dfhd2gds_hr table."""

    __tablename__ = "dfhd2gds_hr"
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime),
    )


class DfhldpdsHr(ReprMixin, Base1102Hr, DfhldpdsBase):
    """The DfhldpdsHr class stores the hourly Dfhldpds record in the dfhldpds_hr table."""

    __tablename__ = "dfhldpds_hr"
    ldp_platform_name: so.Mapped[str] = so.mapped_column(sa.String(64), doc="Platform name.")
    ldp_application_name: so.Mapped[str] = so.mapped_column(sa.String(64), doc="Application name.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, ldp_platform_name, ldp_application_name),
    )


class Dfhxqs3dHr(ReprMixin, Base1102Hr, Dfhxqs3dBase):
    """The Dfhxqs3dHr class stores the hourly Dfhxqs3d record in the dfhxqs3d_hr table."""

    __tablename__ = "dfhxqs3d_hr"
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime),
    )


class Dfhd2rdsHr(ReprMixin, Base1102Hr, Dfhd2rdsBase):
    """The Dfhd2rdsHr class stores the hourly Dfhd2rds record in the dfhd2rds_hr table."""

    __tablename__ = "dfhd2rds_hr"
    d2r_db2entry_name: so.Mapped[str] = so.mapped_column(sa.String(8), doc="name of the DB2ENTRY.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, d2r_db2entry_name),
    )


class DfhstgdsHr(ReprMixin, Base1102Hr, DfhstgdsBase):
    """The DfhstgdsHr class stores the hourly Dfhstgds record in the dfhstgds_hr table."""

    __tablename__ = "dfhstgds_hr"
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime),
    )


class DfhsogdsHr(ReprMixin, Base1102Hr, DfhsogdsBase):
    """The DfhsogdsHr class stores the hourly Dfhsogds record in the dfhsogds_hr table."""

    __tablename__ = "dfhsogds_hr"
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime),
    )


class Dfhxqs2dHr(ReprMixin, Base1102Hr, Dfhxqs2dBase):
    """The Dfhxqs2dHr class stores the hourly Dfhxqs2d record in the dfhxqs2d_hr table."""

    __tablename__ = "dfhxqs2d_hr"
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime),
    )


class DfhpggdsHr(ReprMixin, Base1102Hr, DfhpggdsBase):
    """The DfhpggdsHr class stores the hourly Dfhpggds record in the dfhpggds_hr table."""

    __tablename__ = "dfhpggds_hr"
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime),
    )


class Dfhcfs9dHr(ReprMixin, Base1102Hr, Dfhcfs9dBase):
    """The Dfhcfs9dHr class stores the hourly Dfhcfs9d record in the dfhcfs9d_hr table."""

    __tablename__ = "dfhcfs9d_hr"
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime),
    )


class DsgtcbmHr(ReprMixin, Base1102Hr, DsgtcbmBase):
    """The DsgtcbmHr class stores the hourly Dsgtcbm record in the dsgtcbm_hr table."""

    __tablename__ = "dsgtcbm_hr"
    dsgtcbnm: so.Mapped[str] = so.mapped_column(sa.String(2), doc="TCB Mode Name.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, dsgtcbnm),
        sa.ForeignKeyConstraint(
            ['smfstsid', 'smfstprn', 'smfstspn', 'datetime'],
            ['dfhdsgds_hr.smfstsid', 'dfhdsgds_hr.smfstprn', 'dfhdsgds_hr.smfstspn', 'dfhdsgds_hr.datetime']),
    )

    dfhdsgds_hr: so.Mapped['DfhdsgdsHr'] = so.relationship(back_populates='dsgtcbm_hrs', viewonly=True)


class Dfhncs4dHr(ReprMixin, Base1102Hr, Dfhncs4dBase):
    """The Dfhncs4dHr class stores the hourly Dfhncs4d record in the dfhncs4d_hr table."""

    __tablename__ = "dfhncs4d_hr"
    s4name: so.Mapped[str] = so.mapped_column(sa.String(16), doc="Full name of list structure.")
    s4pool: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Pool name part of structure name.")
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, s4name, s4pool),
    )


class DfhrmgdsHr(ReprMixin, Base1102Hr, DfhrmgdsBase):
    """The DfhrmgdsHr class stores the hourly Dfhrmgds record in the dfhrmgds_hr table."""

    __tablename__ = "dfhrmgds_hr"
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime),
    )


class DfhusgdsHr(ReprMixin, Base1102Hr, DfhusgdsBase):
    """The DfhusgdsHr class stores the hourly Dfhusgds record in the dfhusgds_hr table."""

    __tablename__ = "dfhusgds_hr"
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime),
    )
