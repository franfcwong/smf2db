import datetime as dt
from typing import List, Optional

import sqlalchemy as sa
import sqlalchemy.orm as so

from .smf1102_base import ReprMixin, Base1102Da, DfhwbgdsBase, DfhisrdsBase, DfhxmrdsBase, DfhmlrdsBase, DfhmqrdsBase, \
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


class DfhwbgdsDa(ReprMixin, Base1102Da, DfhwbgdsBase):
    """The DfhwbgdsDa class stores the daily Dfhwbgds record in the dfhwbgds_da table."""

    __tablename__ = "dfhwbgds_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date),
    )


class DfhisrdsDa(ReprMixin, Base1102Da, DfhisrdsBase):
    """The DfhisrdsDa class stores the daily Dfhisrds record in the dfhisrds_da table."""

    __tablename__ = "dfhisrds_da"
    isr_ipconn_name: so.Mapped[str] = so.mapped_column(sa.String(8), doc="IPCONN name.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, isr_ipconn_name),
    )


class DfhxmrdsDa(ReprMixin, Base1102Da, DfhxmrdsBase):
    """The DfhxmrdsDa class stores the daily Dfhxmrds record in the dfhxmrds_da table."""

    __tablename__ = "dfhxmrds_da"
    xmrti: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Transaction ID.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, xmrti),
    )


class DfhmlrdsDa(ReprMixin, Base1102Da, DfhmlrdsBase):
    """The DfhmlrdsDa class stores the daily Dfhmlrds record in the dfhmlrds_da table."""

    __tablename__ = "dfhmlrds_da"
    mlr_xmltransform_name: so.Mapped[str] = so.mapped_column(sa.String(32), doc="Xmltransform name.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, mlr_xmltransform_name),
    )


class DfhmqrdsDa(ReprMixin, Base1102Da, DfhmqrdsBase):
    """The DfhmqrdsDa class stores the daily Dfhmqrds record in the dfhmqrds_da table."""

    __tablename__ = "dfhmqrds_da"
    mqr_name: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Resource name.")
    mqr_qname: so.Mapped[str] = so.mapped_column(sa.String(48), doc="MQ Queue name.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, mqr_name, mqr_qname),
    )


class DfhmqgdsDa(ReprMixin, Base1102Da, DfhmqgdsBase):
    """The DfhmqgdsDa class stores the daily Dfhmqgds record in the dfhmqgds_da table."""

    __tablename__ = "dfhmqgds_da"
    mqg_qmgr_name: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Queue manager name.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, mqg_qmgr_name),
    )


class DfhpgrdsDa(ReprMixin, Base1102Da, DfhpgrdsBase):
    """The DfhpgrdsDa class stores the daily Dfhpgrds record in the dfhpgrds_da table."""

    __tablename__ = "dfhpgrds_da"
    pgr_jvmprogram_name: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Jvmprogram Name.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, pgr_jvmprogram_name),
    )


class Dfha16dsDa(ReprMixin, Base1102Da, Dfha16dsBase):
    """The Dfha16dsDa class stores the daily Dfha16ds record in the dfha16ds_da table."""

    __tablename__ = "dfha16ds_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date),
    )

    a16stats_das: so.Mapped[List['A16statsDa']] = so.relationship(back_populates='dfha16ds_da', viewonly=True)


class DfhldbdsDa(ReprMixin, Base1102Da, DfhldbdsBase):
    """The DfhldbdsDa class stores the daily Dfhldbds record in the dfhldbds_da table."""

    __tablename__ = "dfhldbds_da"
    ldb_library_name: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Library name.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, ldb_library_name),
    )

    ldb_dsnames_das: so.Mapped[List['LdbDsnamesDa']] = so.relationship(back_populates='dfhldbds_da', viewonly=True)


class DsgtcbpDa(ReprMixin, Base1102Da, DsgtcbpBase):
    """The DsgtcbpDa class stores the daily Dsgtcbp record in the dsgtcbp_da table."""

    __tablename__ = "dsgtcbp_da"
    dsgtcbpn: so.Mapped[int] = so.mapped_column(sa.Integer, doc="TCB Pool Number.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, dsgtcbpn),

        sa.ForeignKeyConstraint(
            ['smfstsid', 'smfstprn', 'smfstspn', 'date'],
            ['dfhdsgds_da.smfstsid', 'dfhdsgds_da.smfstprn', 'dfhdsgds_da.smfstspn', 'dfhdsgds_da.date']),
    )

    dfhdsgds_da: so.Mapped['DfhdsgdsDa'] = so.relationship(back_populates='dsgtcbp_das', viewonly=True)


class SmsbodyDa(ReprMixin, Base1102Da, SmsbodyBase):
    """The SmsbodyDa class stores the daily Smsbody record in the smsbody_da table."""

    __tablename__ = "smsbody_da"
    smsdsaname: so.Mapped[str] = so.mapped_column(sa.String(8), doc="DSA name.")
    smsdsalimit: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current DSA limit.")
    smsedsalimit: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current EDSA limit.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, smsdsaname),

        sa.ForeignKeyConstraint(
            ['smfstsid', 'smfstprn', 'smfstspn', 'date'],
            ['smsglobal_da.smfstsid', 'smsglobal_da.smfstprn', 'smsglobal_da.smfstspn', 'smsglobal_da.date']),
    )

    smsglobal_da: so.Mapped['SmsglobalDa'] = so.relationship(back_populates='smsbody_das', viewonly=True)


class Dfha24dsDa(ReprMixin, Base1102Da, Dfha24dsBase):
    """The Dfha24dsDa class stores the daily Dfha24ds record in the dfha24ds_da table."""

    __tablename__ = "dfha24ds_da"
    a24targ: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Target name.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, a24targ),
    )


class Dfha23dsDa(ReprMixin, Base1102Da, Dfha23dsBase):
    """The Dfha23dsDa class stores the daily Dfha23ds record in the dfha23ds_da table."""

    __tablename__ = "dfha23ds_da"
    a23pool: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Pool name.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, a23pool),
    )


class DfhtqgdsDa(ReprMixin, Base1102Da, DfhtqgdsBase):
    """The DfhtqgdsDa class stores the daily Dfhtqgds record in the dfhtqgds_da table."""

    __tablename__ = "dfhtqgds_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date),
    )


class DfhwbrdsDa(ReprMixin, Base1102Da, DfhwbrdsBase):
    """The DfhwbrdsDa class stores the daily Dfhwbrds record in the dfhwbrds_da table."""

    __tablename__ = "dfhwbrds_da"
    wbr_urimap_name: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Urimap name.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, wbr_urimap_name),
    )


class Dfhcfs6dDa(ReprMixin, Base1102Da, Dfhcfs6dBase):
    """The Dfhcfs6dDa class stores the daily Dfhcfs6d record in the dfhcfs6d_da table."""

    __tablename__ = "dfhcfs6d_da"
    s6name: so.Mapped[str] = so.mapped_column(sa.String(16), doc="Full name of list structure.")
    s6pool: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Pool name part of structure name.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, s6name, s6pool),
    )


class Dfhcfs7dDa(ReprMixin, Base1102Da, Dfhcfs7dBase):
    """The Dfhcfs7dDa class stores the daily Dfhcfs7d record in the dfhcfs7d_da table."""

    __tablename__ = "dfhcfs7d_da"
    s7table: so.Mapped[str] = so.mapped_column(sa.String(16), doc="Table name padded with spaces.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, s7table),
    )


class Dfha22dsDa(ReprMixin, Base1102Da, Dfha22dsBase):
    """The Dfha22dsDa class stores the daily Dfha22ds record in the dfha22ds_da table."""

    __tablename__ = "dfha22ds_da"
    a22pool: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Pool name.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, a22pool),
    )


class LdgglobalDa(ReprMixin, Base1102Da, ldgglobal):
    """The LdgglobalDa class stores the daily Ldgglobal record in the ldgglobal_da table."""

    __tablename__ = "ldgglobal_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date),
    )

    ldgdsastat_das: so.Mapped[List['LdgdsastatDa']] = so.relationship(back_populates='ldgglobal_da', viewonly=True)


class DfhpgedsDa(ReprMixin, Base1102Da, DfhpgedsBase):
    """The DfhpgedsDa class stores the daily Dfhpgeds record in the dfhpgeds_da table."""

    __tablename__ = "dfhpgeds_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date),
    )


class DfhxmgdsDa(ReprMixin, Base1102Da, DfhxmgdsBase):
    """The DfhxmgdsDa class stores the daily Dfhxmgds record in the dfhxmgds_da table."""

    __tablename__ = "dfhxmgds_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date),
    )


class DfhsmtdsDa(ReprMixin, Base1102Da, DfhsmtdsBase):
    """The DfhsmtdsDa class stores the daily Dfhsmtds record in the dfhsmtds_da table."""

    __tablename__ = "dfhsmtds_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date),
    )

    smtbody_das: so.Mapped[List['SmtbodyDa']] = so.relationship(back_populates='dfhsmtds_da', viewonly=True)


class DfhldrdsDa(ReprMixin, Base1102Da, DfhldrdsBase):
    """The DfhldrdsDa class stores the daily Dfhldrds record in the dfhldrds_da table."""

    __tablename__ = "dfhldrds_da"
    ldrpname: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Program name.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, ldrpname),
    )


class DfhtqrdsDa(ReprMixin, Base1102Da, DfhtqrdsBase):
    """The DfhtqrdsDa class stores the daily Dfhtqrds record in the dfhtqrds_da table."""

    __tablename__ = "dfhtqrds_da"
    tqrqid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="TD Queue identifier.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, tqrqid),
    )


class Dfha17dsDa(ReprMixin, Base1102Da, Dfha17dsBase):
    """The Dfha17dsDa class stores the daily Dfha17ds record in the dfha17ds_da table."""

    __tablename__ = "dfha17ds_da"
    a17fnam: so.Mapped[str] = so.mapped_column(sa.String(8), doc="File name.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, a17fnam),
    )


class Dfha09dsDa(ReprMixin, Base1102Da, Dfha09dsBase):
    """The Dfha09dsDa class stores the daily Dfha09ds record in the dfha09ds_da table."""

    __tablename__ = "dfha09ds_da"
    a09dsid: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Filename.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, a09dsid),
    )


class DfhdsrdsDa(ReprMixin, Base1102Da, DfhdsrdsBase):
    """The DfhdsrdsDa class stores the daily Dfhdsrds record in the dfhdsrds_da table."""

    __tablename__ = "dfhdsrds_da"
    dsrds_tcb_address: so.Mapped[str] = so.mapped_column(sa.String(10), doc="Address of MVS TCB.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, dsrds_tcb_address),
    )


class DfhsdgdsDa(ReprMixin, Base1102Da, DfhsdgdsBase):
    """The DfhsdgdsDa class stores the daily Dfhsdgds record in the dfhsdgds_da table."""

    __tablename__ = "dfhsdgds_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date),
    )


class DfhdstdsDa(ReprMixin, Base1102Da, DfhdstdsBase):
    """The DfhdstdsDa class stores the daily Dfhdstds record in the dfhdstds_da table."""

    __tablename__ = "dfhdstds_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date),
    )


class LdbDsnamesDa(ReprMixin, Base1102Da):
    """The LdbDsnamesDa class stores the daily LdbDsnames record in the ldb_dsnames_da table."""

    __tablename__ = "ldb_dsnames_da"
    ldb_dsname: so.Mapped[str] = so.mapped_column(sa.String(44), doc="Library Dsname.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    ldb_library_name: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Library name.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, ldb_library_name, ldb_dsname),

        sa.ForeignKeyConstraint(
            ['smfstsid', 'smfstprn', 'smfstspn', 'date', 'ldb_library_name'],
            ['dfhldbds_da.smfstsid', 'dfhldbds_da.smfstprn', 'dfhldbds_da.smfstspn', 'dfhldbds_da.date',
             'dfhldbds_da.ldb_library_name']),
    )

    dfhldbds_da: so.Mapped['DfhldbdsDa'] = so.relationship(back_populates='ldb_dsnames_das', viewonly=True)


class Dfha06dsDa(ReprMixin, Base1102Da, Dfha06dsBase):
    """The Dfha06dsDa class stores the daily Dfha06ds record in the dfha06ds_da table."""

    __tablename__ = "dfha06ds_da"
    a06teti: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Terminal id.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, a06teti),
    )


class Dfhw2rdsDa(ReprMixin, Base1102Da, Dfhw2rdsBase):
    """The Dfhw2rdsDa class stores the daily Dfhw2rds record in the dfhw2rds_da table."""

    __tablename__ = "dfhw2rds_da"
    w2r_atomserv_name: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Atomservice name.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, w2r_atomserv_name),
    )


class NqgbodyDa(ReprMixin, Base1102Da, NqgbodyBase):
    """The NqgbodyDa class stores the daily Nqgbody record in the nqgbody_da table."""

    __tablename__ = "nqgbody_da"
    nqgpool: so.Mapped[str] = so.mapped_column(sa.String(8), doc="ENQ pool id.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, nqgpool),

        sa.ForeignKeyConstraint(
            ['smfstsid', 'smfstprn', 'smfstspn', 'date'],
            ['dfhnqgds_da.smfstsid', 'dfhnqgds_da.smfstprn', 'dfhnqgds_da.smfstspn', 'dfhnqgds_da.date']),
    )

    dfhnqgds_da: so.Mapped['DfhnqgdsDa'] = so.relationship(back_populates='nqgbody_das', viewonly=True)


class SmsglobalDa(ReprMixin, Base1102Da, SmsglobalBase, DfhsmsdsBase):
    """The SmsglobalDa class stores the daily Smsglobal record in the smsglobal_da table."""

    __tablename__ = "smsglobal_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date),
    )

    smsbody_das: so.Mapped[List['SmsbodyDa']] = so.relationship(back_populates='smsglobal_da', viewonly=True)


class DfhsdrdsDa(ReprMixin, Base1102Da, DfhsdrdsBase):
    """The DfhsdrdsDa class stores the daily Dfhsdrds record in the dfhsdrds_da table."""

    __tablename__ = "dfhsdrds_da"
    sdrcode: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Dumpcode.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, sdrcode),
    )


class DfhpgddsDa(ReprMixin, Base1102Da, DfhpgddsBase):
    """The DfhpgddsDa class stores the daily Dfhpgdds record in the dfhpgdds_da table."""

    __tablename__ = "dfhpgdds_da"
    pgd_program_name: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Program Name.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, pgd_program_name),
    )


class Dfha14dsDa(ReprMixin, Base1102Da, Dfha14dsBase):
    """The Dfha14dsDa class stores the daily Dfha14ds record in the dfha14ds_da table."""

    __tablename__ = "dfha14ds_da"
    a14cntn: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Connection name.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, a14cntn),
    )


class Dfha20dsDa(ReprMixin, Base1102Da, Dfha20dsBase):
    """The Dfha20dsDa class stores the daily Dfha20ds record in the dfha20ds_da table."""

    __tablename__ = "dfha20ds_da"
    a20sysn: so.Mapped[str] = so.mapped_column(sa.String(4), doc="System name.")
    a20mode: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Mode name.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, a20sysn, a20mode),
    )


class DfhmprdsDa(ReprMixin, Base1102Da, DfhmprdsBase):
    """The DfhmprdsDa class stores the daily Dfhmprds record in the dfhmprds_da table."""

    __tablename__ = "dfhmprds_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date),
    )


class A08bssdsDa(ReprMixin, Base1102Da, A08bssdsBase):
    """The A08bssdsDa class stores the daily A08bssds record in the a08bssds_da table."""

    __tablename__ = "a08bssds_da"
    a08bkbsz: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Buffer size.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    isIndxBuffer: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Is index buffer.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    a08srpid: so.Mapped[int] = so.mapped_column(sa.Integer, doc="LSR pool number.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, a08srpid, a08bkbsz, isIndxBuffer),

        sa.ForeignKeyConstraint(
            ['smfstsid', 'smfstprn', 'smfstspn', 'date', 'a08srpid'],
            ['dfha08ds_da.smfstsid', 'dfha08ds_da.smfstprn', 'dfha08ds_da.smfstspn', 'dfha08ds_da.date',
             'dfha08ds_da.a08srpid']),
    )

    dfha08ds_da: so.Mapped['Dfha08dsDa'] = so.relationship(back_populates='a08bssds_das', viewonly=True)


class Dfha08dsDa(ReprMixin, Base1102Da, Dfha08dsBase):
    """The Dfha08dsDa class stores the daily Dfha08ds record in the dfha08ds_da table."""

    __tablename__ = "dfha08ds_da"
    a08srpid: so.Mapped[int] = so.mapped_column(sa.Integer, doc="LSR pool number.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, a08srpid),
    )

    a08bssds_das: so.Mapped[List['A08bssdsDa']] = so.relationship(back_populates='dfha08ds_da', viewonly=True)


class DfhpirdsDa(ReprMixin, Base1102Da, DfhpirdsBase):
    """The DfhpirdsDa class stores the daily Dfhpirds record in the dfhpirds_da table."""

    __tablename__ = "dfhpirds_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date),
    )


class A16statsDa(ReprMixin, Base1102Da, A16statsBase):
    """The A16statsDa class stores the daily A16stats record in the a16stats_da table."""

    __tablename__ = "a16stats_da"
    a16tnam: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Table name.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, a16tnam),

        sa.ForeignKeyConstraint(
            ['smfstsid', 'smfstprn', 'smfstspn', 'date'],
            ['dfha16ds_da.smfstsid', 'dfha16ds_da.smfstprn', 'dfha16ds_da.smfstspn', 'dfha16ds_da.date']),
    )

    dfha16ds_da: so.Mapped['Dfha16dsDa'] = so.relationship(back_populates='a16stats_das', viewonly=True)


class DfhtdgdsDa(ReprMixin, Base1102Da, DfhtdgdsBase):
    """The DfhtdgdsDa class stores the daily Dfhtdgds record in the dfhtdgds_da table."""

    __tablename__ = "dfhtdgds_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date),
    )


class LdyDsnamesDa(ReprMixin, Base1102Da):
    """The LdyDsnamesDa class stores the daily LdyDsnames record in the ldy_dsnames_da table."""

    __tablename__ = "ldy_dsnames_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    ldy_library_platform_name: so.Mapped[str] = so.mapped_column(sa.String(64), doc="Platform name.")
    ldy_library_application_name: so.Mapped[str] = so.mapped_column(sa.String(64), doc="Application name.")
    ldb_dsname: so.Mapped[str] = so.mapped_column(sa.String(44), doc="Library Dsname.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, ldy_library_platform_name,
                                ldy_library_application_name, ldb_dsname),

        sa.ForeignKeyConstraint(
            ['smfstsid', 'smfstprn', 'smfstspn', 'date', 'ldy_library_platform_name', 'ldy_library_application_name'],
            ['dfhldyds_da.smfstsid', 'dfhldyds_da.smfstprn', 'dfhldyds_da.smfstspn', 'dfhldyds_da.date',
             'dfhldyds_da.ldy_library_platform_name', 'dfhldyds_da.ldy_library_application_name']),
    )

    dfhldyds_da: so.Mapped['DfhldydsDa'] = so.relationship(back_populates='ldy_dsnames_das', viewonly=True)


class DfhepgdsDa(ReprMixin, Base1102Da, DfhepgdsBase):
    """The DfhepgdsDa class stores the daily Dfhepgds record in the dfhepgds_da table."""

    __tablename__ = "dfhepgds_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date),
    )


class DfheprdsDa(ReprMixin, Base1102Da, DfheprdsBase):
    """The DfheprdsDa class stores the daily Dfheprds record in the dfheprds_da table."""

    __tablename__ = "dfheprds_da"
    epr_adapter_name: so.Mapped[str] = so.mapped_column(sa.String(32), doc="EP adapter name.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, epr_adapter_name),
    )


class DfhasgdsDa(ReprMixin, Base1102Da, DfhasgdsBase):
    """The DfhasgdsDa class stores the daily Dfhasgds record in the dfhasgds_da table."""

    __tablename__ = "dfhasgds_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date),
    )


class DfhdhddsDa(ReprMixin, Base1102Da, DfhdhddsBase):
    """The DfhdhddsDa class stores the daily Dfhdhdds record in the dfhdhdds_da table."""

    __tablename__ = "dfhdhdds_da"
    dhd_doctemplate_name: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Doctemplate name.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, dhd_doctemplate_name),
    )


class Dfha03dsDa(ReprMixin, Base1102Da, Dfha03dsBase):
    """The Dfha03dsDa class stores the daily Dfha03ds record in the dfha03ds_da table."""

    __tablename__ = "dfha03ds_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date),
    )


class DfhsjsdsDa(ReprMixin, Base1102Da, DfhsjsdsBase):
    """The DfhsjsdsDa class stores the daily Dfhsjsds record in the dfhsjsds_da table."""

    __tablename__ = "dfhsjsds_da"
    sjs_jvmserver_name: so.Mapped[str] = so.mapped_column(sa.String(8), doc="JVMSERVER name.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, sjs_jvmserver_name),
    )


class DfhpiwdsDa(ReprMixin, Base1102Da, DfhpiwdsBase):
    """The DfhpiwdsDa class stores the daily Dfhpiwds record in the dfhpiwds_da table."""

    __tablename__ = "dfhpiwds_da"
    piw_webservice_name: so.Mapped[str] = so.mapped_column(sa.String(32), doc="Webservice name.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, piw_webservice_name),
    )


class Dfha21dsDa(ReprMixin, Base1102Da, Dfha21dsBase):
    """The Dfha21dsDa class stores the daily Dfha21ds record in the dfha21ds_da table."""

    __tablename__ = "dfha21ds_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date),
    )


class DfhxmcdsDa(ReprMixin, Base1102Da, DfhxmcdsBase):
    """The DfhxmcdsDa class stores the daily Dfhxmcds record in the dfhxmcds_da table."""

    __tablename__ = "dfhxmcds_da"
    xmctcl: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Tclass name.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, xmctcl),
    )


class DfhtsgdsDa(ReprMixin, Base1102Da, DfhtsgdsBase):
    """The DfhtsgdsDa class stores the daily Dfhtsgds record in the dfhtsgds_da table."""

    __tablename__ = "dfhtsgds_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date),
    )


class Dfha04dsDa(ReprMixin, Base1102Da, Dfha04dsBase):
    """The Dfha04dsDa class stores the daily Dfha04ds record in the dfha04ds_da table."""

    __tablename__ = "dfha04ds_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date),
    )


class DfheccdsDa(ReprMixin, Base1102Da, DfheccdsBase):
    """The DfheccdsDa class stores the daily Dfheccds record in the dfheccds_da table."""

    __tablename__ = "dfheccds_da"
    ecc_eventbinding_name: so.Mapped[str] = so.mapped_column(sa.String(32), doc="Eventbinding name.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, ecc_eventbinding_name),
    )


class DfhrlrdsDa(ReprMixin, Base1102Da, DfhrlrdsBase):
    """The DfhrlrdsDa class stores the daily Dfhrlrds record in the dfhrlrds_da table."""

    __tablename__ = "dfhrlrds_da"
    rlr_bundle_name: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Bundle name.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, rlr_bundle_name),
    )


class SmtbodyDa(ReprMixin, Base1102Da, SmtbodyBase):
    """The SmtbodyDa class stores the daily Smtbody record in the smtbody_da table."""

    __tablename__ = "smtbody_da"
    smtdsaname: so.Mapped[str] = so.mapped_column(sa.String(8), doc="DSA name.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, smtdsaname),

        sa.ForeignKeyConstraint(
            ['smfstsid', 'smfstprn', 'smfstspn', 'date'],
            ['dfhsmtds_da.smfstsid', 'dfhsmtds_da.smfstprn', 'dfhsmtds_da.smfstspn', 'dfhsmtds_da.date']),
    )

    dfhsmtds_da: so.Mapped['DfhsmtdsDa'] = so.relationship(back_populates='smtbody_das', viewonly=True)


class DfhnqgdsDa(ReprMixin, Base1102Da, DfhnqgdsBase):
    """The DfhnqgdsDa class stores the daily Dfhnqgds record in the dfhnqgds_da table."""

    __tablename__ = "dfhnqgds_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date),
    )

    nqgbody_das: so.Mapped[List['NqgbodyDa']] = so.relationship(back_populates='dfhnqgds_da', viewonly=True)


class DfhdsgdsDa(ReprMixin, Base1102Da, DfhdsgdsBase):
    """The DfhdsgdsDa class stores the daily Dfhdsgds record in the dfhdsgds_da table."""

    __tablename__ = "dfhdsgds_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date),
    )

    dsgtcbm_das: so.Mapped[List['DsgtcbmDa']] = so.relationship(back_populates='dfhdsgds_da', viewonly=True)
    dsgtcbp_das: so.Mapped[List['DsgtcbpDa']] = so.relationship(back_populates='dfhdsgds_da', viewonly=True)


class Dfhxqs1dDa(ReprMixin, Base1102Da, Dfhxqs1dBase):
    """The Dfhxqs1dDa class stores the daily Dfhxqs1d record in the dfhxqs1d_da table."""

    __tablename__ = "dfhxqs1d_da"
    s1name: so.Mapped[str] = so.mapped_column(sa.String(16), doc="Full name of list structure.")
    s1pool: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Pool name part of structure name.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, s1name, s1pool),
    )


class Dfhcfs8dDa(ReprMixin, Base1102Da, Dfhcfs8dBase):
    """The Dfhcfs8dDa class stores the daily Dfhcfs8d record in the dfhcfs8d_da table."""

    __tablename__ = "dfhcfs8d_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date),
    )


class DfhtdrdsDa(ReprMixin, Base1102Da, DfhtdrdsBase):
    """The DfhtdrdsDa class stores the daily Dfhtdrds record in the dfhtdrds_da table."""

    __tablename__ = "dfhtdrds_da"
    tdrcode: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Dumpcode.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, tdrcode),
    )


class DfhsjndsDa(ReprMixin, Base1102Da, DfhsjndsBase):
    """The DfhsjndsDa class stores the daily Dfhsjnds record in the dfhsjnds_da table."""

    __tablename__ = "dfhsjnds_da"
    sjn_nodejsapp_name: so.Mapped[str] = so.mapped_column(sa.String(32), doc="NODEJSAPP name.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, sjn_nodejsapp_name),
    )


class DfhlgsdsDa(ReprMixin, Base1102Da, DfhlgsdsBase):
    """The DfhlgsdsDa class stores the daily Dfhlgsds record in the dfhlgsds_da table."""

    __tablename__ = "dfhlgsds_da"
    lgsstrnam: so.Mapped[str] = so.mapped_column(sa.String(26), doc="Log stream name.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, lgsstrnam),
    )


class DfhsmddsDa(ReprMixin, Base1102Da, DfhsmddsBase):
    """The DfhsmddsDa class stores the daily Dfhsmdds record in the dfhsmdds_da table."""

    __tablename__ = "dfhsmdds_da"
    smdspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Subpool name.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, smdspn),
    )


class DfhldydsDa(ReprMixin, Base1102Da, DfhldydsBase):
    """The DfhldydsDa class stores the daily Dfhldyds record in the dfhldyds_da table."""

    __tablename__ = "dfhldyds_da"
    ldy_library_platform_name: so.Mapped[str] = so.mapped_column(sa.String(64), doc="Platform name.")
    ldy_library_application_name: so.Mapped[str] = so.mapped_column(sa.String(64), doc="Application name.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, ldy_library_platform_name,
                                ldy_library_application_name),
    )

    ldy_dsnames_das: so.Mapped[List['LdyDsnamesDa']] = so.relationship(back_populates='dfhldyds_da', viewonly=True)


class LdgdsastatDa(ReprMixin, Base1102Da, LdgdsastatBase):
    """The LdgdsastatDa class stores the daily Ldgdsastat record in the ldgdsastat_da table."""

    __tablename__ = "ldgdsastat_da"
    ldgdsaindex: so.Mapped[int] = so.mapped_column(sa.Integer, doc="DSA index.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, ldgdsaindex),

        sa.ForeignKeyConstraint(
            ['smfstsid', 'smfstprn', 'smfstspn', 'date'],
            ['ldgglobal_da.smfstsid', 'ldgglobal_da.smfstprn', 'ldgglobal_da.smfstspn', 'ldgglobal_da.date']),
    )

    ldgglobal_da: so.Mapped['LdgglobalDa'] = so.relationship(back_populates='ldgdsastat_das', viewonly=True)


class DfhpgpdsDa(ReprMixin, Base1102Da, DfhpgpdsBase):
    """The DfhpgpdsDa class stores the daily Dfhpgpds record in the dfhpgpds_da table."""

    __tablename__ = "dfhpgpds_da"
    pgp_jvmprogram_platform_name: so.Mapped[str] = so.mapped_column(sa.String(64), doc="Platform name.")
    pgp_jvmprogram_application_name: so.Mapped[str] = so.mapped_column(sa.String(64), doc="Application name.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, pgp_jvmprogram_platform_name,
                                pgp_jvmprogram_application_name),
    )


class DfhsordsDa(ReprMixin, Base1102Da, DfhsordsBase):
    """The DfhsordsDa class stores the daily Dfhsords record in the dfhsords_da table."""

    __tablename__ = "dfhsords_da"
    sor_service_name: so.Mapped[str] = so.mapped_column(sa.String(8), doc="TCP/IP Service name.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, sor_service_name),
    )


class Dfhncs5dDa(ReprMixin, Base1102Da, Dfhncs5dBase):
    """The Dfhncs5dDa class stores the daily Dfhncs5d record in the dfhncs5d_da table."""

    __tablename__ = "dfhncs5d_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date),
    )


class DfhlgrdsDa(ReprMixin, Base1102Da, DfhlgrdsBase):
    """The DfhlgrdsDa class stores the daily Dfhlgrds record in the dfhlgrds_da table."""

    __tablename__ = "dfhlgrds_da"
    lgrjnlname: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Journal name.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, lgrjnlname),
    )


class DfhecgdsDa(ReprMixin, Base1102Da, DfhecgdsBase):
    """The DfhecgdsDa class stores the daily Dfhecgds record in the dfhecgds_da table."""

    __tablename__ = "dfhecgds_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date),
    )


class DfhecrdsDa(ReprMixin, Base1102Da, DfhecrdsBase):
    """The DfhecrdsDa class stores the daily Dfhecrds record in the dfhecrds_da table."""

    __tablename__ = "dfhecrds_da"
    ecr_eventbinding_name: so.Mapped[str] = so.mapped_column(sa.String(32), doc="Eventbinding name.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, ecr_eventbinding_name),
    )


class DfhlggdsDa(ReprMixin, Base1102Da, DfhlggdsBase):
    """The DfhlggdsDa class stores the daily Dfhlggds record in the dfhlggds_da table."""

    __tablename__ = "dfhlggds_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date),
    )


class DfhmngdsDa(ReprMixin, Base1102Da, DfhmngdsBase):
    """The DfhmngdsDa class stores the daily Dfhmngds record in the dfhmngds_da table."""

    __tablename__ = "dfhmngds_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date),
    )


class Dfhd2gdsDa(ReprMixin, Base1102Da, Dfhd2gdsBase):
    """The Dfhd2gdsDa class stores the daily Dfhd2gds record in the dfhd2gds_da table."""

    __tablename__ = "dfhd2gds_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date),
    )


class DfhldpdsDa(ReprMixin, Base1102Da, DfhldpdsBase):
    """The DfhldpdsDa class stores the daily Dfhldpds record in the dfhldpds_da table."""

    __tablename__ = "dfhldpds_da"
    ldp_platform_name: so.Mapped[str] = so.mapped_column(sa.String(64), doc="Platform name.")
    ldp_application_name: so.Mapped[str] = so.mapped_column(sa.String(64), doc="Application name.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, ldp_platform_name, ldp_application_name),
    )


class Dfhxqs3dDa(ReprMixin, Base1102Da, Dfhxqs3dBase):
    """The Dfhxqs3dDa class stores the daily Dfhxqs3d record in the dfhxqs3d_da table."""

    __tablename__ = "dfhxqs3d_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date),
    )


class Dfhd2rdsDa(ReprMixin, Base1102Da, Dfhd2rdsBase):
    """The Dfhd2rdsDa class stores the daily Dfhd2rds record in the dfhd2rds_da table."""

    __tablename__ = "dfhd2rds_da"
    d2r_db2entry_name: so.Mapped[str] = so.mapped_column(sa.String(8), doc="name of the DB2ENTRY.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, d2r_db2entry_name),
    )


class DfhstgdsDa(ReprMixin, Base1102Da, DfhstgdsBase):
    """The DfhstgdsDa class stores the daily Dfhstgds record in the dfhstgds_da table."""

    __tablename__ = "dfhstgds_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date),
    )


class DfhsogdsDa(ReprMixin, Base1102Da, DfhsogdsBase):
    """The DfhsogdsDa class stores the daily Dfhsogds record in the dfhsogds_da table."""

    __tablename__ = "dfhsogds_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date),
    )


class Dfhxqs2dDa(ReprMixin, Base1102Da, Dfhxqs2dBase):
    """The Dfhxqs2dDa class stores the daily Dfhxqs2d record in the dfhxqs2d_da table."""

    __tablename__ = "dfhxqs2d_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date),
    )


class DfhpggdsDa(ReprMixin, Base1102Da, DfhpggdsBase):
    """The DfhpggdsDa class stores the daily Dfhpggds record in the dfhpggds_da table."""

    __tablename__ = "dfhpggds_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date),
    )


class Dfhcfs9dDa(ReprMixin, Base1102Da, Dfhcfs9dBase):
    """The Dfhcfs9dDa class stores the daily Dfhcfs9d record in the dfhcfs9d_da table."""

    __tablename__ = "dfhcfs9d_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date),
    )


class DsgtcbmDa(ReprMixin, Base1102Da, DsgtcbmBase):
    """The DsgtcbmDa class stores the daily Dsgtcbm record in the dsgtcbm_da table."""

    __tablename__ = "dsgtcbm_da"
    dsgtcbnm: so.Mapped[str] = so.mapped_column(sa.String(2), doc="TCB Mode Name.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, dsgtcbnm),

        sa.ForeignKeyConstraint(
            ['smfstsid', 'smfstprn', 'smfstspn', 'date'],
            ['dfhdsgds_da.smfstsid', 'dfhdsgds_da.smfstprn', 'dfhdsgds_da.smfstspn', 'dfhdsgds_da.date']),
    )

    dfhdsgds_da: so.Mapped['DfhdsgdsDa'] = so.relationship(back_populates='dsgtcbm_das', viewonly=True)


class Dfhncs4dDa(ReprMixin, Base1102Da, Dfhncs4dBase):
    """The Dfhncs4dDa class stores the daily Dfhncs4d record in the dfhncs4d_da table."""

    __tablename__ = "dfhncs4d_da"
    s4name: so.Mapped[str] = so.mapped_column(sa.String(16), doc="Full name of list structure.")
    s4pool: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Pool name part of structure name.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date, s4name, s4pool),
    )


class DfhrmgdsDa(ReprMixin, Base1102Da, DfhrmgdsBase):
    """The DfhrmgdsDa class stores the daily Dfhrmgds record in the dfhrmgds_da table."""

    __tablename__ = "dfhrmgds_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date),
    )


class DfhusgdsDa(ReprMixin, Base1102Da, DfhusgdsBase):
    """The DfhusgdsDa class stores the daily Dfhusgds record in the dfhusgds_da table."""

    __tablename__ = "dfhusgds_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, date),
    )
