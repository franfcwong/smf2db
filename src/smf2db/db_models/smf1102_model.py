import datetime as dt
from typing import List, Optional

import sqlalchemy as sa
import sqlalchemy.orm as so

from .smf1102_base import ReprMixin, Base1102, DfhwbgdsBase, DfhisrdsBase, DfhxmrdsBase, DfhmlrdsBase, DfhmqrdsBase, \
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


class Dfhwbgds(ReprMixin, Base1102, DfhwbgdsBase):
    """The Dfhwbgds class stores the Dfhwbgds section in the dfhwbgds table."""

    __tablename__ = "dfhwbgds"
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme),
    )


class Dfhisrds(ReprMixin, Base1102, DfhisrdsBase):
    """The Dfhisrds class stores the Dfhisrds section in the dfhisrds table."""

    __tablename__ = "dfhisrds"
    isr_ipconn_name: so.Mapped[str] = so.mapped_column(sa.String(8), doc="IPCONN name.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, isr_ipconn_name),
    )


class Dfhxmrds(ReprMixin, Base1102, DfhxmrdsBase):
    """The Dfhxmrds class stores the Dfhxmrds section in the dfhxmrds table."""

    __tablename__ = "dfhxmrds"
    xmrti: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Transaction ID.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, xmrti),
    )


class Dfhmlrds(ReprMixin, Base1102, DfhmlrdsBase):
    """The Dfhmlrds class stores the Dfhmlrds section in the dfhmlrds table."""

    __tablename__ = "dfhmlrds"
    mlr_xmltransform_name: so.Mapped[str] = so.mapped_column(sa.String(32), doc="Xmltransform name.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, mlr_xmltransform_name),
    )


class Dfhmqrds(ReprMixin, Base1102, DfhmqrdsBase):
    """The Dfhmqrds class stores the Dfhmqrds section in the dfhmqrds table."""

    __tablename__ = "dfhmqrds"
    mqr_name: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Resource name.")
    mqr_qname: so.Mapped[str] = so.mapped_column(sa.String(48), doc="MQ Queue name.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, mqr_name, mqr_qname),
    )


class Dfhmqgds(ReprMixin, Base1102, DfhmqgdsBase):
    """The Dfhmqgds class stores the Dfhmqgds section in the dfhmqgds table."""

    __tablename__ = "dfhmqgds"
    mqg_qmgr_name: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Queue manager name.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, mqg_qmgr_name),
    )


class Dfhpgrds(ReprMixin, Base1102, DfhpgrdsBase):
    """The Dfhpgrds class stores the Dfhpgrds section in the dfhpgrds table."""

    __tablename__ = "dfhpgrds"
    pgr_jvmprogram_name: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Jvmprogram Name.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, pgr_jvmprogram_name),
    )


class Dfha16ds(ReprMixin, Base1102, Dfha16dsBase):
    """The Dfha16ds class stores the Dfha16ds section in the dfha16ds table."""

    __tablename__ = "dfha16ds"
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme),
    )

    a16statss: so.Mapped[List['A16stats']] = so.relationship(back_populates='dfha16ds', viewonly=True)


class Dfhldbds(ReprMixin, Base1102, DfhldbdsBase):
    """The Dfhldbds class stores the Dfhldbds section in the dfhldbds table."""

    __tablename__ = "dfhldbds"
    ldb_library_name: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Library name.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, ldb_library_name),
    )

    ldb_dsnamess: so.Mapped[List['LdbDsnames']] = so.relationship(back_populates='dfhldbds', viewonly=True)


class Dsgtcbp(ReprMixin, Base1102, DsgtcbpBase):
    """The Dsgtcbp class stores the Dsgtcbp section in the dsgtcbp table."""

    __tablename__ = "dsgtcbp"
    dsgtcbpn: so.Mapped[int] = so.mapped_column(sa.Integer, doc="TCB Pool Number.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, dsgtcbpn),
        sa.ForeignKeyConstraint(
            ['smfstsid', 'smfstprn', 'smfstspn', 'datetime', 'smfsttme'],
            ['dfhdsgds.smfstsid', 'dfhdsgds.smfstprn', 'dfhdsgds.smfstspn', 'dfhdsgds.datetime', 'dfhdsgds.smfsttme']),
    )

    dfhdsgds: so.Mapped['Dfhdsgds'] = so.relationship(back_populates='dsgtcbps', viewonly=True)


class Smsbody(ReprMixin, Base1102, SmsbodyBase):
    """The Smsbody class stores the Smsbody section in the smsbody table."""

    __tablename__ = "smsbody"
    smsdsaname: so.Mapped[str] = so.mapped_column(sa.String(8), doc="DSA name.")
    smsdsalimit: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current DSA limit.")
    smsedsalimit: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Current EDSA limit.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, smsdsaname),
        sa.ForeignKeyConstraint(
            ['smfstsid', 'smfstprn', 'smfstspn', 'datetime', 'smfsttme'],
            ['smsglobal.smfstsid', 'smsglobal.smfstprn', 'smsglobal.smfstspn', 'smsglobal.datetime',
             'smsglobal.smfsttme']),
    )

    smsglobal: so.Mapped['Smsglobal'] = so.relationship(back_populates='smsbodys', viewonly=True)


class Dfha24ds(ReprMixin, Base1102, Dfha24dsBase):
    """The Dfha24ds class stores the Dfha24ds section in the dfha24ds table."""

    __tablename__ = "dfha24ds"
    a24targ: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Target name.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, a24targ),
    )


class Dfha23ds(ReprMixin, Base1102, Dfha23dsBase):
    """The Dfha23ds class stores the Dfha23ds section in the dfha23ds table."""

    __tablename__ = "dfha23ds"
    a23pool: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Pool name.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, a23pool),
    )


class Dfhtqgds(ReprMixin, Base1102, DfhtqgdsBase):
    """The Dfhtqgds class stores the Dfhtqgds section in the dfhtqgds table."""

    __tablename__ = "dfhtqgds"
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme),
    )


class Dfhwbrds(ReprMixin, Base1102, DfhwbrdsBase):
    """The Dfhwbrds class stores the Dfhwbrds section in the dfhwbrds table."""

    __tablename__ = "dfhwbrds"
    wbr_urimap_name: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Urimap name.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, wbr_urimap_name),
    )


class Dfhcfs6d(ReprMixin, Base1102, Dfhcfs6dBase):
    """The Dfhcfs6d class stores the Dfhcfs6d section in the dfhcfs6d table."""

    __tablename__ = "dfhcfs6d"
    s6name: so.Mapped[str] = so.mapped_column(sa.String(16), doc="Full name of list structure.")
    s6pool: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Pool name part of structure name.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, s6name, s6pool),
    )


class Dfhcfs7d(ReprMixin, Base1102, Dfhcfs7dBase):
    """The Dfhcfs7d class stores the Dfhcfs7d section in the dfhcfs7d table."""

    __tablename__ = "dfhcfs7d"
    s7table: so.Mapped[str] = so.mapped_column(sa.String(16), doc="Table name padded with spaces.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, s7table),
    )


class Dfha22ds(ReprMixin, Base1102, Dfha22dsBase):
    """The Dfha22ds class stores the Dfha22ds section in the dfha22ds table."""

    __tablename__ = "dfha22ds"
    a22pool: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Pool name.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, a22pool),
    )


class Ldgglobal(ReprMixin, Base1102, ldgglobal):
    """The Ldgglobal class stores the Ldgglobal section in the ldgglobal table."""

    __tablename__ = "ldgglobal"
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme),
    )

    ldgdsastats: so.Mapped[List['Ldgdsastat']] = so.relationship(back_populates='ldgglobal', viewonly=True)


class Dfhpgeds(ReprMixin, Base1102, DfhpgedsBase):
    """The Dfhpgeds class stores the Dfhpgeds section in the dfhpgeds table."""

    __tablename__ = "dfhpgeds"
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme),
    )


class Dfhxmgds(ReprMixin, Base1102, DfhxmgdsBase):
    """The Dfhxmgds class stores the Dfhxmgds section in the dfhxmgds table."""

    __tablename__ = "dfhxmgds"
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme),
    )


class Dfhsmtds(ReprMixin, Base1102, DfhsmtdsBase):
    """The Dfhsmtds class stores the Dfhsmtds section in the dfhsmtds table."""

    __tablename__ = "dfhsmtds"
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme),
    )

    smtbodys: so.Mapped[List['Smtbody']] = so.relationship(back_populates='dfhsmtds', viewonly=True)


class Dfhldrds(ReprMixin, Base1102, DfhldrdsBase):
    """The Dfhldrds class stores the Dfhldrds section in the dfhldrds table."""

    __tablename__ = "dfhldrds"
    ldrpname: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Program name.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, ldrpname),
    )


class Dfhtqrds(ReprMixin, Base1102, DfhtqrdsBase):
    """The Dfhtqrds class stores the Dfhtqrds section in the dfhtqrds table."""

    __tablename__ = "dfhtqrds"
    tqrqid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="TD Queue identifier.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, tqrqid),
    )


class Dfha17ds(ReprMixin, Base1102, Dfha17dsBase):
    """The Dfha17ds class stores the Dfha17ds section in the dfha17ds table."""

    __tablename__ = "dfha17ds"
    a17fnam: so.Mapped[str] = so.mapped_column(sa.String(8), doc="File name.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, a17fnam),
    )


class Dfha09ds(ReprMixin, Base1102, Dfha09dsBase):
    """The Dfha09ds class stores the Dfha09ds section in the dfha09ds table."""

    __tablename__ = "dfha09ds"
    a09dsid: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Filename.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, a09dsid),
    )


class Dfhdsrds(ReprMixin, Base1102, DfhdsrdsBase):
    """The Dfhdsrds class stores the Dfhdsrds section in the dfhdsrds table."""

    __tablename__ = "dfhdsrds"
    dsrds_tcb_address: so.Mapped[str] = so.mapped_column(sa.String(10), doc="Address of MVS TCB.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, dsrds_tcb_address),
    )


class Dfhsdgds(ReprMixin, Base1102, DfhsdgdsBase):
    """The Dfhsdgds class stores the Dfhsdgds section in the dfhsdgds table."""

    __tablename__ = "dfhsdgds"
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme),
    )


class Dfhdstds(ReprMixin, Base1102, DfhdstdsBase):
    """The Dfhdstds class stores the Dfhdstds section in the dfhdstds table."""

    __tablename__ = "dfhdstds"
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme),
    )


class LdbDsnames(ReprMixin, Base1102):
    """The LdbDsnames class stores the LdbDsnames section in the ldb_dsnames table."""

    __tablename__ = "ldb_dsnames"
    ldb_dsname: so.Mapped[str] = so.mapped_column(sa.String(44), doc="Library Dsname.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")
    ldb_library_name: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Library name.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, ldb_library_name, ldb_dsname),
        sa.ForeignKeyConstraint(
            ['smfstsid', 'smfstprn', 'smfstspn', 'datetime', 'smfsttme', 'ldb_library_name'],
            ['dfhldbds.smfstsid', 'dfhldbds.smfstprn', 'dfhldbds.smfstspn', 'dfhldbds.datetime', 'dfhldbds.smfsttme',
             'dfhldbds.ldb_library_name']),
    )

    dfhldbds: so.Mapped['Dfhldbds'] = so.relationship(back_populates='ldb_dsnamess', viewonly=True)


class Dfha06ds(ReprMixin, Base1102, Dfha06dsBase):
    """The Dfha06ds class stores the Dfha06ds section in the dfha06ds table."""

    __tablename__ = "dfha06ds"
    a06teti: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Terminal id.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, a06teti),
    )


class Dfhw2rds(ReprMixin, Base1102, Dfhw2rdsBase):
    """The Dfhw2rds class stores the Dfhw2rds section in the dfhw2rds table."""

    __tablename__ = "dfhw2rds"
    w2r_atomserv_name: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Atomservice name.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, w2r_atomserv_name),
    )


class Nqgbody(ReprMixin, Base1102, NqgbodyBase):
    """The Nqgbody class stores the Nqgbody section in the nqgbody table."""

    __tablename__ = "nqgbody"
    nqgpool: so.Mapped[str] = so.mapped_column(sa.String(8), doc="ENQ pool id.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, nqgpool),
        sa.ForeignKeyConstraint(
            ['smfstsid', 'smfstprn', 'smfstspn', 'datetime', 'smfsttme'],
            ['dfhnqgds.smfstsid', 'dfhnqgds.smfstprn', 'dfhnqgds.smfstspn', 'dfhnqgds.datetime', 'dfhnqgds.smfsttme']),
    )

    dfhnqgds: so.Mapped['Dfhnqgds'] = so.relationship(back_populates='nqgbodys', viewonly=True)


class Smsglobal(ReprMixin, Base1102, SmsglobalBase, DfhsmsdsBase):
    """The Smsglobal class stores the Smsglobal section in the smsglobal table."""

    __tablename__ = "smsglobal"
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme),
    )

    smsbodys: so.Mapped[List['Smsbody']] = so.relationship(back_populates='smsglobal', viewonly=True)


class Dfhsdrds(ReprMixin, Base1102, DfhsdrdsBase):
    """The Dfhsdrds class stores the Dfhsdrds section in the dfhsdrds table."""

    __tablename__ = "dfhsdrds"
    sdrcode: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Dumpcode.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, sdrcode),
    )


class Dfhpgdds(ReprMixin, Base1102, DfhpgddsBase):
    """The Dfhpgdds class stores the Dfhpgdds section in the dfhpgdds table."""

    __tablename__ = "dfhpgdds"
    pgd_program_name: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Program Name.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, pgd_program_name),
    )


class Dfha14ds(ReprMixin, Base1102, Dfha14dsBase):
    """The Dfha14ds class stores the Dfha14ds section in the dfha14ds table."""

    __tablename__ = "dfha14ds"
    a14cntn: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Connection name.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, a14cntn),
    )


class Dfha20ds(ReprMixin, Base1102, Dfha20dsBase):
    """The Dfha20ds class stores the Dfha20ds section in the dfha20ds table."""

    __tablename__ = "dfha20ds"
    a20sysn: so.Mapped[str] = so.mapped_column(sa.String(4), doc="System name.")
    a20mode: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Mode name.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, a20sysn, a20mode),
    )


class Dfhmprds(ReprMixin, Base1102, DfhmprdsBase):
    """The Dfhmprds class stores the Dfhmprds section in the dfhmprds table."""

    __tablename__ = "dfhmprds"
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme),
    )


class A08bssds(ReprMixin, Base1102, A08bssdsBase):
    """The A08bssds class stores the A08bssds section in the a08bssds table."""

    __tablename__ = "a08bssds"
    a08bkbsz: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Buffer size.")
    isIndxBuffer: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Is index buffer.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")
    a08srpid: so.Mapped[int] = so.mapped_column(sa.Integer, doc="LSR pool number.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, a08srpid, a08bkbsz, isIndxBuffer),
        sa.ForeignKeyConstraint(
            ['smfstsid', 'smfstprn', 'smfstspn', 'datetime', 'smfsttme', 'a08srpid'],
            ['dfha08ds.smfstsid', 'dfha08ds.smfstprn', 'dfha08ds.smfstspn', 'dfha08ds.datetime', 'dfha08ds.smfsttme',
             'dfha08ds.a08srpid']),
    )

    dfha08ds: so.Mapped['Dfha08ds'] = so.relationship(back_populates='a08bssdss', viewonly=True)


class Dfha08ds(ReprMixin, Base1102, Dfha08dsBase):
    """The Dfha08ds class stores the Dfha08ds section in the dfha08ds table."""

    __tablename__ = "dfha08ds"
    a08srpid: so.Mapped[int] = so.mapped_column(sa.Integer, doc="LSR pool number.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, a08srpid),
    )

    a08bssdss: so.Mapped[List['A08bssds']] = so.relationship(back_populates='dfha08ds', viewonly=True)


class Dfhpirds(ReprMixin, Base1102, DfhpirdsBase):
    """The Dfhpirds class stores the Dfhpirds section in the dfhpirds table."""

    __tablename__ = "dfhpirds"
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme),
    )


class A16stats(ReprMixin, Base1102, A16statsBase):
    """The A16stats class stores the A16stats section in the a16stats table."""

    __tablename__ = "a16stats"
    a16tnam: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Table name.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, a16tnam),
        sa.ForeignKeyConstraint(
            ['smfstsid', 'smfstprn', 'smfstspn', 'datetime', 'smfsttme'],
            ['dfha16ds.smfstsid', 'dfha16ds.smfstprn', 'dfha16ds.smfstspn', 'dfha16ds.datetime', 'dfha16ds.smfsttme']),
    )

    dfha16ds: so.Mapped['Dfha16ds'] = so.relationship(back_populates='a16statss', viewonly=True)


class Dfhtdgds(ReprMixin, Base1102, DfhtdgdsBase):
    """The Dfhtdgds class stores the Dfhtdgds section in the dfhtdgds table."""

    __tablename__ = "dfhtdgds"
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme),
    )


class LdyDsnames(ReprMixin, Base1102):
    """The LdyDsnames class stores the LdyDsnames section in the ldy_dsnames table."""

    __tablename__ = "ldy_dsnames"
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")
    ldy_library_platform_name: so.Mapped[str] = so.mapped_column(sa.String(64), doc="Platform name.")
    ldy_library_application_name: so.Mapped[str] = so.mapped_column(sa.String(64), doc="Application name.")
    ldb_dsname: so.Mapped[str] = so.mapped_column(sa.String(44), doc="Library Dsname.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, ldy_library_platform_name,
                                ldy_library_application_name, ldb_dsname),
        sa.ForeignKeyConstraint(
            ['smfstsid', 'smfstprn', 'smfstspn', 'datetime', 'smfsttme', 'ldy_library_platform_name',
             'ldy_library_application_name'],
            ['dfhldyds.smfstsid', 'dfhldyds.smfstprn', 'dfhldyds.smfstspn', 'dfhldyds.datetime', 'dfhldyds.smfsttme',
             'dfhldyds.ldy_library_platform_name', 'dfhldyds.ldy_library_application_name']),
    )

    dfhldyds: so.Mapped['Dfhldyds'] = so.relationship(back_populates='ldy_dsnamess', viewonly=True)


class Dfhepgds(ReprMixin, Base1102, DfhepgdsBase):
    """The Dfhepgds class stores the Dfhepgds section in the dfhepgds table."""

    __tablename__ = "dfhepgds"
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme),
    )


class Dfheprds(ReprMixin, Base1102, DfheprdsBase):
    """The Dfheprds class stores the Dfheprds section in the dfheprds table."""

    __tablename__ = "dfheprds"
    epr_adapter_name: so.Mapped[str] = so.mapped_column(sa.String(32), doc="EP adapter name.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, epr_adapter_name),
    )


class Dfhasgds(ReprMixin, Base1102, DfhasgdsBase):
    """The Dfhasgds class stores the Dfhasgds section in the dfhasgds table."""

    __tablename__ = "dfhasgds"
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme),
    )


class Dfhdhdds(ReprMixin, Base1102, DfhdhddsBase):
    """The Dfhdhdds class stores the Dfhdhdds section in the dfhdhdds table."""

    __tablename__ = "dfhdhdds"
    dhd_doctemplate_name: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Doctemplate name.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, dhd_doctemplate_name),
    )


class Dfha03ds(ReprMixin, Base1102, Dfha03dsBase):
    """The Dfha03ds class stores the Dfha03ds section in the dfha03ds table."""

    __tablename__ = "dfha03ds"
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme),
    )


class Dfhsjsds(ReprMixin, Base1102, DfhsjsdsBase):
    """The Dfhsjsds class stores the Dfhsjsds section in the dfhsjsds table."""

    __tablename__ = "dfhsjsds"
    sjs_jvmserver_name: so.Mapped[str] = so.mapped_column(sa.String(8), doc="JVMSERVER name.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, sjs_jvmserver_name),
    )


class Dfhpiwds(ReprMixin, Base1102, DfhpiwdsBase):
    """The Dfhpiwds class stores the Dfhpiwds section in the dfhpiwds table."""

    __tablename__ = "dfhpiwds"
    piw_webservice_name: so.Mapped[str] = so.mapped_column(sa.String(32), doc="Webservice name.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, piw_webservice_name),
    )


class Dfha21ds(ReprMixin, Base1102, Dfha21dsBase):
    """The Dfha21ds class stores the Dfha21ds section in the dfha21ds table."""

    __tablename__ = "dfha21ds"
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme),
    )


class Dfhxmcds(ReprMixin, Base1102, DfhxmcdsBase):
    """The Dfhxmcds class stores the Dfhxmcds section in the dfhxmcds table."""

    __tablename__ = "dfhxmcds"
    xmctcl: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Tclass name.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, xmctcl),
    )


class Dfhtsgds(ReprMixin, Base1102, DfhtsgdsBase):
    """The Dfhtsgds class stores the Dfhtsgds section in the dfhtsgds table."""

    __tablename__ = "dfhtsgds"
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme),
    )


class Dfha04ds(ReprMixin, Base1102, Dfha04dsBase):
    """The Dfha04ds class stores the Dfha04ds section in the dfha04ds table."""

    __tablename__ = "dfha04ds"
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme),
    )


class Dfheccds(ReprMixin, Base1102, DfheccdsBase):
    """The Dfheccds class stores the Dfheccds section in the dfheccds table."""

    __tablename__ = "dfheccds"
    ecc_eventbinding_name: so.Mapped[str] = so.mapped_column(sa.String(32), doc="Eventbinding name.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, ecc_eventbinding_name),
    )


class Dfhrlrds(ReprMixin, Base1102, DfhrlrdsBase):
    """The Dfhrlrds class stores the Dfhrlrds section in the dfhrlrds table."""

    __tablename__ = "dfhrlrds"
    rlr_bundle_name: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Bundle name.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, rlr_bundle_name),
    )


class Smtbody(ReprMixin, Base1102, SmtbodyBase):
    """The Smtbody class stores the Smtbody section in the smtbody table."""

    __tablename__ = "smtbody"
    smtdsaname: so.Mapped[str] = so.mapped_column(sa.String(8), doc="DSA name.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, smtdsaname),
        sa.ForeignKeyConstraint(
            ['smfstsid', 'smfstprn', 'smfstspn', 'datetime', 'smfsttme'],
            ['dfhsmtds.smfstsid', 'dfhsmtds.smfstprn', 'dfhsmtds.smfstspn', 'dfhsmtds.datetime', 'dfhsmtds.smfsttme']),
    )

    dfhsmtds: so.Mapped['Dfhsmtds'] = so.relationship(back_populates='smtbodys', viewonly=True)


class Dfhnqgds(ReprMixin, Base1102, DfhnqgdsBase):
    """The Dfhnqgds class stores the Dfhnqgds section in the dfhnqgds table."""

    __tablename__ = "dfhnqgds"
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme),
    )

    nqgbodys: so.Mapped[List['Nqgbody']] = so.relationship(back_populates='dfhnqgds', viewonly=True)


class Dfhdsgds(ReprMixin, Base1102, DfhdsgdsBase):
    """The Dfhdsgds class stores the Dfhdsgds section in the dfhdsgds table."""

    __tablename__ = "dfhdsgds"
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme),
    )

    dsgtcbms: so.Mapped[List['Dsgtcbm']] = so.relationship(back_populates='dfhdsgds', viewonly=True)
    dsgtcbps: so.Mapped[List['Dsgtcbp']] = so.relationship(back_populates='dfhdsgds', viewonly=True)


class Dfhxqs1d(ReprMixin, Base1102, Dfhxqs1dBase):
    """The Dfhxqs1d class stores the Dfhxqs1d section in the dfhxqs1d table."""

    __tablename__ = "dfhxqs1d"
    s1name: so.Mapped[str] = so.mapped_column(sa.String(16), doc="Full name of list structure.")
    s1pool: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Pool name part of structure name.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, s1name, s1pool),
    )


class Dfhcfs8d(ReprMixin, Base1102, Dfhcfs8dBase):
    """The Dfhcfs8d class stores the Dfhcfs8d section in the dfhcfs8d table."""

    __tablename__ = "dfhcfs8d"
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme),
    )


class Dfhtdrds(ReprMixin, Base1102, DfhtdrdsBase):
    """The Dfhtdrds class stores the Dfhtdrds section in the dfhtdrds table."""

    __tablename__ = "dfhtdrds"
    tdrcode: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Dumpcode.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, tdrcode),
    )


class Dfhsjnds(ReprMixin, Base1102, DfhsjndsBase):
    """The Dfhsjnds class stores the Dfhsjnds section in the dfhsjnds table."""

    __tablename__ = "dfhsjnds"
    sjn_nodejsapp_name: so.Mapped[str] = so.mapped_column(sa.String(32), doc="NODEJSAPP name.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, sjn_nodejsapp_name),
    )


class Dfhlgsds(ReprMixin, Base1102, DfhlgsdsBase):
    """The Dfhlgsds class stores the Dfhlgsds section in the dfhlgsds table."""

    __tablename__ = "dfhlgsds"
    lgsstrnam: so.Mapped[str] = so.mapped_column(sa.String(26), doc="Log stream name.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, lgsstrnam),
    )


class Dfhsmdds(ReprMixin, Base1102, DfhsmddsBase):
    """The Dfhsmdds class stores the Dfhsmdds section in the dfhsmdds table."""

    __tablename__ = "dfhsmdds"
    smdspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Subpool name.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, smdspn),
    )


class Dfhldyds(ReprMixin, Base1102, DfhldydsBase):
    """The Dfhldyds class stores the Dfhldyds section in the dfhldyds table."""

    __tablename__ = "dfhldyds"
    ldy_library_platform_name: so.Mapped[str] = so.mapped_column(sa.String(64), doc="Platform name.")
    ldy_library_application_name: so.Mapped[str] = so.mapped_column(sa.String(64), doc="Application name.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, ldy_library_platform_name,
                                ldy_library_application_name),
    )

    ldy_dsnamess: so.Mapped[List['LdyDsnames']] = so.relationship(back_populates='dfhldyds', viewonly=True)


class Ldgdsastat(ReprMixin, Base1102, LdgdsastatBase):
    """The Ldgdsastat class stores the Ldgdsastat section in the ldgdsastat table."""

    __tablename__ = "ldgdsastat"
    ldgdsaindex: so.Mapped[int] = so.mapped_column(sa.Integer, doc="DSA index.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, ldgdsaindex),
        sa.ForeignKeyConstraint(
            ['smfstsid', 'smfstprn', 'smfstspn', 'datetime', 'smfsttme'],
            ['ldgglobal.smfstsid', 'ldgglobal.smfstprn', 'ldgglobal.smfstspn', 'ldgglobal.datetime',
             'ldgglobal.smfsttme']),
    )

    ldgglobal: so.Mapped['Ldgglobal'] = so.relationship(back_populates='ldgdsastats', viewonly=True)


class Dfhpgpds(ReprMixin, Base1102, DfhpgpdsBase):
    """The Dfhpgpds class stores the Dfhpgpds section in the dfhpgpds table."""

    __tablename__ = "dfhpgpds"
    pgp_jvmprogram_platform_name: so.Mapped[str] = so.mapped_column(sa.String(64), doc="Platform name.")
    pgp_jvmprogram_application_name: so.Mapped[str] = so.mapped_column(sa.String(64), doc="Application name.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, pgp_jvmprogram_platform_name,
                                pgp_jvmprogram_application_name),
    )


class Dfhsords(ReprMixin, Base1102, DfhsordsBase):
    """The Dfhsords class stores the Dfhsords section in the dfhsords table."""

    __tablename__ = "dfhsords"
    sor_service_name: so.Mapped[str] = so.mapped_column(sa.String(8), doc="TCP/IP Service name.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, sor_service_name),
    )


class Dfhncs5d(ReprMixin, Base1102, Dfhncs5dBase):
    """The Dfhncs5d class stores the Dfhncs5d section in the dfhncs5d table."""

    __tablename__ = "dfhncs5d"
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme),
    )


class Dfhlgrds(ReprMixin, Base1102, DfhlgrdsBase):
    """The Dfhlgrds class stores the Dfhlgrds section in the dfhlgrds table."""

    __tablename__ = "dfhlgrds"
    lgrjnlname: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Journal name.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, lgrjnlname),
    )


class Dfhecgds(ReprMixin, Base1102, DfhecgdsBase):
    """The Dfhecgds class stores the Dfhecgds section in the dfhecgds table."""

    __tablename__ = "dfhecgds"
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme),
    )


class Dfhecrds(ReprMixin, Base1102, DfhecrdsBase):
    """The Dfhecrds class stores the Dfhecrds section in the dfhecrds table."""

    __tablename__ = "dfhecrds"
    ecr_eventbinding_name: so.Mapped[str] = so.mapped_column(sa.String(32), doc="Eventbinding name.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, ecr_eventbinding_name),
    )


class Dfhlggds(ReprMixin, Base1102, DfhlggdsBase):
    """The Dfhlggds class stores the Dfhlggds section in the dfhlggds table."""

    __tablename__ = "dfhlggds"
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme),
    )


class Dfhmngds(ReprMixin, Base1102, DfhmngdsBase):
    """The Dfhmngds class stores the Dfhmngds section in the dfhmngds table."""

    __tablename__ = "dfhmngds"
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme),
    )


class Dfhd2gds(ReprMixin, Base1102, Dfhd2gdsBase):
    """The Dfhd2gds class stores the Dfhd2gds section in the dfhd2gds table."""

    __tablename__ = "dfhd2gds"
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme),
    )


class Dfhldpds(ReprMixin, Base1102, DfhldpdsBase):
    """The Dfhldpds class stores the Dfhldpds section in the dfhldpds table."""

    __tablename__ = "dfhldpds"
    ldp_platform_name: so.Mapped[str] = so.mapped_column(sa.String(64), doc="Platform name.")
    ldp_application_name: so.Mapped[str] = so.mapped_column(sa.String(64), doc="Application name.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, ldp_platform_name,
                                ldp_application_name),
    )


class Dfhxqs3d(ReprMixin, Base1102, Dfhxqs3dBase):
    """The Dfhxqs3d class stores the Dfhxqs3d section in the dfhxqs3d table."""

    __tablename__ = "dfhxqs3d"
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme),
    )


class Dfhd2rds(ReprMixin, Base1102, Dfhd2rdsBase):
    """The Dfhd2rds class stores the Dfhd2rds section in the dfhd2rds table."""

    __tablename__ = "dfhd2rds"
    d2r_db2entry_name: so.Mapped[str] = so.mapped_column(sa.String(8), doc="name of the DB2ENTRY.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, d2r_db2entry_name),
    )


class Dfhstgds(ReprMixin, Base1102, DfhstgdsBase):
    """The Dfhstgds class stores the Dfhstgds section in the dfhstgds table."""

    __tablename__ = "dfhstgds"
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme),
    )


class Dfhsogds(ReprMixin, Base1102, DfhsogdsBase):
    """The Dfhsogds class stores the Dfhsogds section in the dfhsogds table."""

    __tablename__ = "dfhsogds"
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme),
    )


class Dfhxqs2d(ReprMixin, Base1102, Dfhxqs2dBase):
    """The Dfhxqs2d class stores the Dfhxqs2d section in the dfhxqs2d table."""

    __tablename__ = "dfhxqs2d"
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme),
    )


class Dfhpggds(ReprMixin, Base1102, DfhpggdsBase):
    """The Dfhpggds class stores the Dfhpggds section in the dfhpggds table."""

    __tablename__ = "dfhpggds"
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme),
    )


class Dfhcfs9d(ReprMixin, Base1102, Dfhcfs9dBase):
    """The Dfhcfs9d class stores the Dfhcfs9d section in the dfhcfs9d table."""

    __tablename__ = "dfhcfs9d"
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme),
    )


class Dsgtcbm(ReprMixin, Base1102, DsgtcbmBase):
    """The Dsgtcbm class stores the Dsgtcbm section in the dsgtcbm table."""

    __tablename__ = "dsgtcbm"
    dsgtcbnm: so.Mapped[str] = so.mapped_column(sa.String(2), doc="TCB Mode Name.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, dsgtcbnm),
        sa.ForeignKeyConstraint(
            ['smfstsid', 'smfstprn', 'smfstspn', 'datetime', 'smfsttme'],
            ['dfhdsgds.smfstsid', 'dfhdsgds.smfstprn', 'dfhdsgds.smfstspn', 'dfhdsgds.datetime', 'dfhdsgds.smfsttme']),
    )

    dfhdsgds: so.Mapped['Dfhdsgds'] = so.relationship(back_populates='dsgtcbms', viewonly=True)


class Dfhncs4d(ReprMixin, Base1102, Dfhncs4dBase):
    """The Dfhncs4d class stores the Dfhncs4d section in the dfhncs4d table."""

    __tablename__ = "dfhncs4d"
    s4name: so.Mapped[str] = so.mapped_column(sa.String(16), doc="Full name of list structure.")
    s4pool: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Pool name part of structure name.")
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme, s4name, s4pool),
    )


class Dfhrmgds(ReprMixin, Base1102, DfhrmgdsBase):
    """The Dfhrmgds class stores the Dfhrmgds section in the dfhrmgds table."""

    __tablename__ = "dfhrmgds"
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme),
    )


class Dfhusgds(ReprMixin, Base1102, DfhusgdsBase):
    """The Dfhusgds class stores the Dfhusgds section in the dfhusgds table."""

    __tablename__ = "dfhusgds"
    smfstsid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Subystem identification.")
    smfstprn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (generic Applid).")
    smfstspn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Product name (specific Applid).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smfsttme: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="Date and time record moved to SMF.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smfstsid, smfstprn, smfstspn, datetime, smfsttme),
    )
