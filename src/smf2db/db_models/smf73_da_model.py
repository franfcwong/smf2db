import datetime as dt
from typing import List, Optional

import sqlalchemy as sa
import sqlalchemy.orm as so

from .smf73_base import ReprMixin, Base73Da, Smf73ccm1, Smf73ccm2, Smf73ccm3, Smf73ccm4, Smf73ccm5, Smf73edt2, \
    Smf73edt4, Smf73edt5, Smf73cha, Smf73pro, Smf73ctl


class Smf73ProDa(ReprMixin, Base73Da, Smf73pro):
    """The Smf73ProDa class stores the daily Smf73Pro record in the smf73_pro_da table."""

    __tablename__ = "smf73_pro_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    speed_boost: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                             doc="smf73fla (Bit 10) indcating speed boost was active during entire interval.")
    ziip_boost: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                            doc="smf73fla (Bit 9) indciating zIIP boost was active during entire interval.")
    smf_type: so.Mapped[str] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf73sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(date, smf_type, csc, smf73sid),

        sa.ForeignKeyConstraint(
            ['csc', 'smf73sid', 'date'],
            ['smf73_ctl_da.csc', 'smf73_ctl_da.smf73sid', 'smf73_ctl_da.date']),
    )

    smf73_ctl_da: so.Mapped['Smf73CtlDa'] = so.relationship(back_populates='smf73_pro_da', viewonly=True)


class Smf73CtlDa(ReprMixin, Base73Da, Smf73ctl):
    """The Smf73CtlDa class stores the daily Smf73Ctl record in the smf73_ctl_da table."""

    __tablename__ = "smf73_ctl_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf73sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf73sid, date),
    )

    smf73_pro_da: so.Mapped['Smf73ProDa'] = so.relationship(back_populates='smf73_ctl_da', viewonly=True)
    smf73_cha1_das: so.Mapped[List['Smf73Cha1Da']] = so.relationship(back_populates='smf73_ctl_da', viewonly=True)
    smf73_cha2_das: so.Mapped[List['Smf73Cha2Da']] = so.relationship(back_populates='smf73_ctl_da', viewonly=True)
    smf73_cha3_das: so.Mapped[List['Smf73Cha3Da']] = so.relationship(back_populates='smf73_ctl_da', viewonly=True)
    smf73_cha4_das: so.Mapped[List['Smf73Cha4Da']] = so.relationship(back_populates='smf73_ctl_da', viewonly=True)
    smf73_cha5_das: so.Mapped[List['Smf73Cha5Da']] = so.relationship(back_populates='smf73_ctl_da', viewonly=True)


class Smf73Cha1Da(ReprMixin, Base73Da, Smf73cha, Smf73ccm1):
    """The Smf73Cha1Da class stores the daily Smf73Cha1 record in the smf73_cha1_da table."""

    __tablename__ = "smf73_cha1_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    part_utilization_pct: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                        doc="the channel path utilization percentage for an individual logical partition.")
    total_utilization_pct: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                         doc="the channel path utilization percentage for the CPC during an interval.")
    bus_utilization_pct: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                       doc="percentage of busy cycles, the bus has been found busy for this channel in relation to the theoretical limit.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf73sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    smf73pid: so.Mapped[str] = so.mapped_column(sa.String(2),
                                                doc="Channel path identification. The range of values is X'0' to X'FF'. Support for dynamic I/0. There are always X'FF' path data sections in record type 73, even though there might not be X'FF' CHPIDs defined in the system. These dummy data sections in the SMF records only contain the channel path ID. The rest is filled with hexadecimal zeroes.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf73sid, date, smf73pid),

        sa.ForeignKeyConstraint(
            ['csc', 'smf73sid', 'date'],
            ['smf73_ctl_da.csc', 'smf73_ctl_da.smf73sid', 'smf73_ctl_da.date']),
    )

    smf73_ctl_da: so.Mapped['Smf73CtlDa'] = so.relationship(back_populates='smf73_cha1_das', viewonly=True)


class Smf73Cha2Da(ReprMixin, Base73Da, Smf73cha, Smf73ccm2, Smf73edt2):
    """The Smf73Cha2Da class stores the daily Smf73Cha2 record in the smf73_cha2_da table."""

    __tablename__ = "smf73_cha2_da"
    part_utilization_pct: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                        doc="the channel path utilization percentage for an individual logical partition.")
    total_utilization_pct: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                         doc="the channel path utilization percentage for the CPC during an interval.")
    bus_utilization_pct: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                       doc="percentage of busy cycles, the bus has been found busy for this channel in relation to the theoretical limit.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    part_read_rate: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                  doc="data transfer rates from the control unit to the channel for this partition.")
    total_read_rate: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                   doc="data transfer rates from the control unit to the channel for the CPC.")
    part_write_rate: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                   doc="data transfer rates from the channel to the control unit for this partition.")
    total_write_rate: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="data transfer rates from the channel to the control unit for the CPC.")
    ficon_operations_rate: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                         doc="number of native FICON operations per second.")
    ficon_operations_active: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                           doc="the average number of native FICON operations that are concurrently active during the reporting interval.")
    ficon_operations_defer: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                          doc="number of deferred native FICON operations per second that could not be inititated by the channel due to the lack of available resources.")
    zhpf_operations_rate: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                        doc="number of zHPF (High Performance FICON) operations per second.")
    zhpf_operations_active: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                          doc="the active number of zHPF operations that are concurrently active during the reporting interval.")
    zhpf_operations_defer: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                         doc="number of deferred zHPF operations per second that could not be initiated by the channel due to the lack of available resources.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf73sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    smf73pid: so.Mapped[str] = so.mapped_column(sa.String(2),
                                                doc="Channel path identification. The range of values is X'0' to X'FF'. Support for dynamic I/0. There are always X'FF' path data sections in record type 73, even though there might not be X'FF' CHPIDs defined in the system. These dummy data sections in the SMF records only contain the channel path ID. The rest is filled with hexadecimal zeroes.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf73sid, date, smf73pid),

        sa.ForeignKeyConstraint(
            ['csc', 'smf73sid', 'date'],
            ['smf73_ctl_da.csc', 'smf73_ctl_da.smf73sid', 'smf73_ctl_da.date']),
    )

    smf73_ctl_da: so.Mapped['Smf73CtlDa'] = so.relationship(back_populates='smf73_cha2_das', viewonly=True)


class Smf73Cha3Da(ReprMixin, Base73Da, Smf73cha, Smf73ccm3):
    """The Smf73Cha3Da class stores the daily Smf73Cha3 record in the smf73_cha3_da table."""

    __tablename__ = "smf73_cha3_da"
    part_read_rate: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                  doc="data transfer rates from the control unit to the channel for this partition.")
    total_read_rate: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                   doc="data transfer rates from the control unit to the channel for the CPC.")
    part_write_rate: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                   doc="data transfer rates from the channel to the control unit for this partition.")
    total_write_rate: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="data transfer rates from the channel to the control unit for the CPC.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    message_rate_part: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                     doc="rate of messages sent by this partition.")
    message_rate_total: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="rate of messages sent by the CPC.")
    message_size_part: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                     doc="average size of messages sent by this partition.")
    message_size_total: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                      doc="average size of messages sent by the CPC.")
    send_fail_part: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                  doc="rate of messages (sent by this partiiton) that failed. This field is for HiperSockets.")
    receive_fail_part: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                     doc="rate of messages (received by this partition) that failed due to unavailable buffers. The value could indicate, that more receive buffers are required.")
    receive_fail_total: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                      doc="rate of messages (received by the CPC) that failed due to unavailable buffers. This field is for HiperSockets.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf73sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    smf73pid: so.Mapped[str] = so.mapped_column(sa.String(2),
                                                doc="Channel path identification. The range of values is X'0' to X'FF'. Support for dynamic I/0. There are always X'FF' path data sections in record type 73, even though there might not be X'FF' CHPIDs defined in the system. These dummy data sections in the SMF records only contain the channel path ID. The rest is filled with hexadecimal zeroes.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf73sid, date, smf73pid),

        sa.ForeignKeyConstraint(
            ['csc', 'smf73sid', 'date'],
            ['smf73_ctl_da.csc', 'smf73_ctl_da.smf73sid', 'smf73_ctl_da.date']),
    )

    smf73_ctl_da: so.Mapped['Smf73CtlDa'] = so.relationship(back_populates='smf73_cha3_das', viewonly=True)


class Smf73Cha4Da(ReprMixin, Base73Da, Smf73cha, Smf73ccm4, Smf73edt4):
    """The Smf73Cha4Da class stores the daily Smf73Cha4 record in the smf73_cha4_da table."""

    __tablename__ = "smf73_cha4_da"
    part_utilization_pct: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                        doc="the channel path utilization percentage for an individual logical partition.")
    total_utilization_pct: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                         doc="the channel path utilization percentage for the CPC during an interval.")
    bus_utilization_pct: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                       doc="percentage of busy cycles, the bus has been found busy for this channel in relation to the theoretical limit.")
    part_read_rate: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                  doc="data transfer rates from the control unit to the channel for this partition.")
    total_read_rate: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                   doc="data transfer rates from the control unit to the channel for the CPC.")
    part_write_rate: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                   doc="data transfer rates from the channel to the control unit for this partition.")
    total_write_rate: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="data transfer rates from the channel to the control unit for the CPC.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf73sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    smf73pid: so.Mapped[str] = so.mapped_column(sa.String(2),
                                                doc="Channel path identification. The range of values is X'0' to X'FF'. Support for dynamic I/0. There are always X'FF' path data sections in record type 73, even though there might not be X'FF' CHPIDs defined in the system. These dummy data sections in the SMF records only contain the channel path ID. The rest is filled with hexadecimal zeroes.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf73sid, date, smf73pid),

        sa.ForeignKeyConstraint(
            ['csc', 'smf73sid', 'date'],
            ['smf73_ctl_da.csc', 'smf73_ctl_da.smf73sid', 'smf73_ctl_da.date']),
    )

    smf73_ctl_da: so.Mapped['Smf73CtlDa'] = so.relationship(back_populates='smf73_cha4_das', viewonly=True)


class Smf73Cha5Da(ReprMixin, Base73Da, Smf73cha, Smf73ccm5, Smf73edt5):
    """The Smf73Cha5Da class stores the daily Smf73Cha5 record in the smf73_cha5_da table."""

    __tablename__ = "smf73_cha5_da"
    part_utilization_pct: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                        doc="the channel path utilization percentage for an individual logical partition.")
    total_utilization_pct: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                         doc="the channel path utilization percentage for the CPC during an interval.")
    bus_utilization_pct: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                       doc="percentage of busy cycles, the bus has been found busy for this channel in relation to the theoretical limit.")
    part_read_rate: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                  doc="data transfer rates from the control unit to the channel for this partition.")
    total_read_rate: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                   doc="data transfer rates from the control unit to the channel for the CPC.")
    part_write_rate: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                   doc="data transfer rates from the channel to the control unit for this partition.")
    total_write_rate: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="data transfer rates from the channel to the control unit for the CPC.")
    ficon_operations_rate: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                         doc="number of native FICON operations per second.")
    ficon_operations_active: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                           doc="the average number of native FICON operations that are concurrently active during the reporting interval.")
    ficon_operations_defer: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                          doc="number of deferred native FICON operations per second that could not be inititated by the channel due to the lack of available resources.")
    zhpf_operations_rate: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                        doc="number of zHPF (High Performance FICON) operations per second.")
    zhpf_operations_active: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                          doc="the active number of zHPF operations that are concurrently active during the reporting interval.")
    zhpf_operations_defer: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                         doc="number of deferred zHPF operations per second that could not be initiated by the channel due to the lack of available resources.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf73sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    smf73pid: so.Mapped[str] = so.mapped_column(sa.String(2),
                                                doc="Channel path identification. The range of values is X'0' to X'FF'. Support for dynamic I/0. There are always X'FF' path data sections in record type 73, even though there might not be X'FF' CHPIDs defined in the system. These dummy data sections in the SMF records only contain the channel path ID. The rest is filled with hexadecimal zeroes.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf73sid, date, smf73pid),

        sa.ForeignKeyConstraint(
            ['csc', 'smf73sid', 'date'],
            ['smf73_ctl_da.csc', 'smf73_ctl_da.smf73sid', 'smf73_ctl_da.date']),
    )

    smf73_ctl_da: so.Mapped['Smf73CtlDa'] = so.relationship(back_populates='smf73_cha5_das', viewonly=True)
