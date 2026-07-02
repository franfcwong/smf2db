import datetime as dt
from typing import List, Optional

import sqlalchemy as sa
import sqlalchemy.orm as so

from .smf73_base import ReprMixin, Base73, Smf73ccm1, Smf73ccm2, Smf73ccm3, Smf73ccm4, Smf73ccm5, Smf73edt2, Smf73edt4, \
    Smf73edt5, Smf73cha, Smf73pro, Smf73ctl


class Smf73Pro(ReprMixin, Base73, Smf73pro):
    """The Smf73Pro class stores the Smf73Pro section in the smf73_pro table."""

    __tablename__ = "smf73_pro"
    smf73ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf73iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval was synchronized with SMF).")
    speed_boost: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                             doc="smf73fla (Bit 10) indcating speed boost was active during entire interval.")
    ziip_boost: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                            doc="smf73fla (Bit 9) indciating zIIP boost was active during entire interval.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf_type: so.Mapped[str] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf73sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(datetime, smf73ist, smf73iet, smf_type, csc, smf73sid),
        sa.ForeignKeyConstraint(
            ['csc', 'smf73sid', 'datetime', 'smf73ist', 'smf73iet'],
            ['smf73_ctl.csc', 'smf73_ctl.smf73sid', 'smf73_ctl.datetime', 'smf73_ctl.smf73ist', 'smf73_ctl.smf73iet']),
    )

    smf73_ctl: so.Mapped["Smf73Ctl"] = so.relationship(back_populates="smf73_pro", viewonly=True)


class Smf73Ctl(ReprMixin, Base73, Smf73ctl):
    """The Smf73Ctl class stores the Smf73Ctl section in the smf73_ctl table."""

    __tablename__ = "smf73_ctl"
    date: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date, doc="the date of the record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf73sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf73ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf73iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval was synchronized with SMF).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf73sid, datetime, smf73ist, smf73iet),
    )

    smf73_pro: so.Mapped["Smf73Pro"] = so.relationship(back_populates="smf73_ctl", viewonly=True)
    smf73_cha1s: so.Mapped[List['Smf73Cha1']] = so.relationship(back_populates='smf73_ctl', viewonly=True)
    smf73_cha2s: so.Mapped[List['Smf73Cha2']] = so.relationship(back_populates='smf73_ctl', viewonly=True)
    smf73_cha3s: so.Mapped[List['Smf73Cha3']] = so.relationship(back_populates='smf73_ctl', viewonly=True)
    smf73_cha4s: so.Mapped[List['Smf73Cha4']] = so.relationship(back_populates='smf73_ctl', viewonly=True)
    smf73_cha5s: so.Mapped[List['Smf73Cha5']] = so.relationship(back_populates='smf73_ctl', viewonly=True)


class Smf73Cha1(ReprMixin, Base73, Smf73cha, Smf73ccm1):
    """The Smf73Cha1 class stores the Smf73Cha1 section in the smf73_cha1 table."""

    __tablename__ = "smf73_cha1"
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
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf73ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf73iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval was synchronized with SMF).")
    smf73pid: so.Mapped[str] = so.mapped_column(sa.String(2),
                                                doc="Channel path identification. The range of values is X'0' to X'FF'. Support for dynamic I/0. There are always X'FF' path data sections in record type 73, even though there might not be X'FF' CHPIDs defined in the system. These dummy data sections in the SMF records only contain the channel path ID. The rest is filled with hexadecimal zeroes.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf73sid, datetime, smf73ist, smf73iet, smf73pid),
        sa.ForeignKeyConstraint(
            ['csc', 'smf73sid', 'datetime', 'smf73ist', 'smf73iet'],
            ['smf73_ctl.csc', 'smf73_ctl.smf73sid', 'smf73_ctl.datetime', 'smf73_ctl.smf73ist', 'smf73_ctl.smf73iet']),
    )

    smf73_ctl: so.Mapped['Smf73Ctl'] = so.relationship(back_populates='smf73_cha1s', viewonly=True)


class Smf73Cha2(ReprMixin, Base73, Smf73cha, Smf73ccm2, Smf73edt2):
    """The Smf73Cha2 class stores the Smf73Cha2 section in the smf73_cha2 table."""

    __tablename__ = "smf73_cha2"
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
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf73sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf73ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf73iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval was synchronized with SMF).")
    smf73pid: so.Mapped[str] = so.mapped_column(sa.String(2),
                                                doc="Channel path identification. The range of values is X'0' to X'FF'. Support for dynamic I/0. There are always X'FF' path data sections in record type 73, even though there might not be X'FF' CHPIDs defined in the system. These dummy data sections in the SMF records only contain the channel path ID. The rest is filled with hexadecimal zeroes.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf73sid, datetime, smf73ist, smf73iet, smf73pid),
        sa.ForeignKeyConstraint(
            ['csc', 'smf73sid', 'datetime', 'smf73ist', 'smf73iet'],
            ['smf73_ctl.csc', 'smf73_ctl.smf73sid', 'smf73_ctl.datetime', 'smf73_ctl.smf73ist', 'smf73_ctl.smf73iet']),
    )

    smf73_ctl: so.Mapped['Smf73Ctl'] = so.relationship(back_populates='smf73_cha2s', viewonly=True)


class Smf73Cha3(ReprMixin, Base73, Smf73cha, Smf73ccm3):
    """The Smf73Cha3 class stores the Smf73Cha3 section in the smf73_cha3 table."""

    __tablename__ = "smf73_cha3"
    part_read_rate: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                  doc="data transfer rates from the control unit to the channel for this partition.")
    total_read_rate: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                   doc="data transfer rates from the control unit to the channel for the CPC.")
    part_write_rate: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                   doc="data transfer rates from the channel to the control unit for this partition.")
    total_write_rate: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="data transfer rates from the channel to the control unit for the CPC.")
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
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf73ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf73iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval was synchronized with SMF).")
    smf73pid: so.Mapped[str] = so.mapped_column(sa.String(2),
                                                doc="Channel path identification. The range of values is X'0' to X'FF'. Support for dynamic I/0. There are always X'FF' path data sections in record type 73, even though there might not be X'FF' CHPIDs defined in the system. These dummy data sections in the SMF records only contain the channel path ID. The rest is filled with hexadecimal zeroes.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf73sid, datetime, smf73ist, smf73iet, smf73pid),
        sa.ForeignKeyConstraint(
            ['csc', 'smf73sid', 'datetime', 'smf73ist', 'smf73iet'],
            ['smf73_ctl.csc', 'smf73_ctl.smf73sid', 'smf73_ctl.datetime', 'smf73_ctl.smf73ist', 'smf73_ctl.smf73iet']),
    )

    smf73_ctl: so.Mapped['Smf73Ctl'] = so.relationship(back_populates='smf73_cha3s', viewonly=True)


class Smf73Cha4(ReprMixin, Base73, Smf73cha, Smf73ccm4, Smf73edt4):
    """The Smf73Cha4 class stores the Smf73Cha4 section in the smf73_cha4 table."""

    __tablename__ = "smf73_cha4"
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
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf73sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf73ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf73iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval was synchronized with SMF).")
    smf73pid: so.Mapped[str] = so.mapped_column(sa.String(2),
                                                doc="Channel path identification. The range of values is X'0' to X'FF'. Support for dynamic I/0. There are always X'FF' path data sections in record type 73, even though there might not be X'FF' CHPIDs defined in the system. These dummy data sections in the SMF records only contain the channel path ID. The rest is filled with hexadecimal zeroes.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf73sid, datetime, smf73ist, smf73iet, smf73pid),
        sa.ForeignKeyConstraint(
            ['csc', 'smf73sid', 'datetime', 'smf73ist', 'smf73iet'],
            ['smf73_ctl.csc', 'smf73_ctl.smf73sid', 'smf73_ctl.datetime', 'smf73_ctl.smf73ist', 'smf73_ctl.smf73iet']),
    )

    smf73_ctl: so.Mapped['Smf73Ctl'] = so.relationship(back_populates='smf73_cha4s', viewonly=True)


class Smf73Cha5(ReprMixin, Base73, Smf73cha, Smf73ccm5, Smf73edt5):
    """The Smf73Cha5 class stores the Smf73Cha5 section in the smf73_cha5 table."""

    __tablename__ = "smf73_cha5"
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
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf73sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf73ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf73iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval was synchronized with SMF).")
    smf73pid: so.Mapped[str] = so.mapped_column(sa.String(2),
                                                doc="Channel path identification. The range of values is X'0' to X'FF'. Support for dynamic I/0. There are always X'FF' path data sections in record type 73, even though there might not be X'FF' CHPIDs defined in the system. These dummy data sections in the SMF records only contain the channel path ID. The rest is filled with hexadecimal zeroes.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf73sid, datetime, smf73ist, smf73iet, smf73pid),
        sa.ForeignKeyConstraint(
            ['csc', 'smf73sid', 'datetime', 'smf73ist', 'smf73iet'],
            ['smf73_ctl.csc', 'smf73_ctl.smf73sid', 'smf73_ctl.datetime', 'smf73_ctl.smf73ist', 'smf73_ctl.smf73iet']),
    )

    smf73_ctl: so.Mapped['Smf73Ctl'] = so.relationship(back_populates='smf73_cha5s', viewonly=True)
