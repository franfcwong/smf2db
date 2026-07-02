from typing import List, Optional

import sqlalchemy as sa
import sqlalchemy.orm as so
import datetime as dt

class ReprMixin(object):
    """A mixin to implement a generic __repr__ method"""

    def as_dict(self):
        """return instance as a dictionary"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return '<%s(%s)>' % (self.__class__.__name__,
                             ', '.join([f'{c.name} = {getattr(self, c.name)}' for c in self.__table__.primary_key]))


convention = {
    'all_column_names': lambda constraint, table: '_'.join(
        [column.name for column in constraint.columns.values()]
    ),
    'ix': 'ix__%(table_name)s__%(all_column_names)s',
    'uq': 'uq__%(table_name)s__%(all_column_names)s',
    'ck': 'ck__%(table_name)s__%(constraint_name)s',
    'fk': 'fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s',
    'pk': 'pk__%(table_name)s',
}


class Base(so.DeclarativeBase):
    pass

# declarative base class
class Base7x(Base):
    __abstract__ = True
    metadata = sa.MetaData(schema='smf', naming_convention=convention)


class SmfCpc(ReprMixin, Base7x):
    """The SmfCpc object stores the serial no. of a CPC (Central processor complex) in the smf_cpc table.

    Attributes:
        csc: A string indicating the serial number of the CPC.

    """

    __tablename__ = 'smf_cpc'
    csc: so.Mapped[str] = so.mapped_column(sa.String(8), primary_key=True)

    # Define the n:1 relationship between smf_lpars and smf_cpc.
    smf_lpars: so.Mapped[List["SmfLpar"]] = so.relationship(back_populates="smf_cpc")

    def __init__(self, csc: str):

        super().__init__()
        self.csc = csc


class SmfLpar(ReprMixin, Base7x):
    """The SmfLpar object stores the Lpar information in the smf_lpar table.

    Attributes:
        csc: A string indicating the identifier or serial number of Central Processor Complexes (CPC).
        lpar_system_name: A string indicating combining lpar long name with lpar short name.
        smf70lpm: A string indicating lpar name.
        system_name: A string indicating the partition system name.
        lpar_number: A integer of PR/SM partition number of the partition.
        sysplex_name: A string indicating the sysplex name which this partition belongs to.
        smf70cpa_actual: A integer of physical CPU adjustement factor based on Model Capacity Rating.
        smf70cpa_scaling_factor: A integer of scaling factor for smf70cpa_actual.
        is_CF: A interger indicating whether this lpar is a CF.
        last_update_time: A DateTime indicating last update time of this record.
    """
    __tablename__ = 'smf_lpar'
    csc = so.mapped_column(sa.ForeignKey("smf_cpc.csc"))
    lpar_system_name: so.Mapped[str] = so.mapped_column(sa.String(17))
    smf70lpm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8))
    system_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8))
    lpar_number: so.Mapped[int] = so.mapped_column(sa.Integer)
    sysplex_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8))
    smf70cpa_actual: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer)
    smf70cpa_scaling_factor: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer)
    is_CF: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer)
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime)

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, lpar_number),
        sa.UniqueConstraint('csc', 'lpar_system_name', 'lpar_number'),)

    # Define the 1:n relationship between smf_cpc and smf_lpars.
    smf_cpc = so.relationship("SmfCpc", back_populates="smf_lpars")

    def __init__(self, csc: str, lpar_name: str, system_name: str, lpar_number: int, sysplex_name: str, is_cf: int,
                 last_update_time: dt.datetime):

        super().__init__()
        self.csc = csc
        self.smf70lpm = lpar_name
        self.lpar_system_name = lpar_name + '-' + system_name
        self.lpar_number = lpar_number
        self.sysplex_name = sysplex_name
        self.system_name = system_name
        self.is_CF = is_cf
        self.last_update_time = last_update_time

    @classmethod
    def from_all(cls, csc: str, lpar_name: str, system_name: str, lpar_number: int, sysplex_name: str, is_cf: int,
                 last_update_time: dt.datetime, smf70cpa_actual: int, smf70cpa_scaling_factor: int):
        l = cls(csc, lpar_name, system_name, lpar_number, sysplex_name, is_cf, last_update_time)
        l.smf70cpa_actual = smf70cpa_actual
        l.smf70cpa_scaling_factor = smf70cpa_scaling_factor
        return l
