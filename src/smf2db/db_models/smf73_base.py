import datetime as dt
from typing import Optional

import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.ext.declarative import AbstractConcreteBase


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


class Base73(Base):
    __abstract__ = True
    metadata = sa.MetaData(schema='smf73', naming_convention=convention)


class Base73Hr(Base):
    __abstract__ = True
    metadata = sa.MetaData(schema='smf73', naming_convention=convention)


class Base73Da(Base):
    __abstract__ = True
    metadata = sa.MetaData(schema='smf73', naming_convention=convention)


class Smf73pro(AbstractConcreteBase):
    """Abstract class for structure Smf73Pro - RMF product section."""

    smf73mfv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="RMF version number.")
    smf73prd: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Product name ('RMF').")
    smf73int: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Duration of the RMF measurement interval, in the form mmsstttF where mm is the minutes, ss is the seconds, ttt is the milliseconds, and F is the sign. The end of the measurement interval is the sum of the recorded start time (and this field.)")
    smf73sam: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of RMF samples.")
    smf73fla: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Flags Bit Meaning when set 0 Reserved 1 Samples have been skipped 2 Record was written by RMF Monitor III 3 Interval was synchronized with SMF 4 SMF record converted to lower service level. 5 SMF record converted to higher release or service level. 6 Running under an alternate virtual machine.")
    smf73cyc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Sampling cycle length, in the form 000ttttF , where tttt is the milliseconds and F is the sign (taken from CYCLE option). The range of values is 0.050 to 9.999 seconds.")
    smf73mvs: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="z/OS software level (consists of an acronym and the version, release, and modification level - ZVvvrrmm).")
    smf73iml: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Indicates the type of processor complex on which data measurements were taken. Value Meaning 3")
    smf73prf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Processor flags. Meaning when set 0 The system has expanded storage 1 The processor is enabled for ES connection architecture (ESCA) 2 There is an ES connection director in the configuration 3 System is running in z/Architecture mode 4 At least one zAAP is currently installed 5 At least one zIIP is currently installed 6 Enhanced DAT facility 1 available 7 Enhanced DAT facility 2 available")
    smf73ptn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="PR/SM partition number of the partition that wrote this record.")
    smf73srl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="SMF record level change number. This field enables processing of SMF record level changes in an existing release. SMF 73 record level for current z/OS release: X'8F' (APAR OA66014)")
    smf73lgo: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Offset GMT to local time (STCK format).")
    smf73oil: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Original interval length as defined in the session or by SMF (in seconds).")
    smf73syn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="SYNC value in seconds.")
    smf73gie: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                  doc="Projected gathering interval end (STCK format) GMT time.")
    smf73xnm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf73snm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="System name for current system as defined in parmlib member IEASYSxx SYSNAME parameter.")
    smf73flg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="System indicator Bit Meaning when set 0 New record format 1 Subtypes used 2 Reserved 3-6 Version indicators* 7 System is running in PR/SM mode. *See 'Standard and extended SMF record headers' on page 164 for a detailed description.")


class Smf73ctl(AbstractConcreteBase):
    """Abstract class for structure Smf73Ctl - Channel path control section."""

    smf73smp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="This field contains the number of samples while the busy count is stored in field SMF73BSY. Only valid if bit 2 of SMF73SFL is not set.")
    smf73cfl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Configuration change flags Bit Meaning when set 0 Configuration changed. Used to decide whether to provide the text 'POR' or 'ACTIVATE' on reports. Also used to check whether data can be combined in a duration report. 1 Configuration change since power-on-reset (POR). 2 POR using IODF data set that supports dynamic configuration change (contains I/O token). 3 I/O token is valid. 4 Record may include data sections that are not valid. 5 CPMF (channel path measurement facility) available. 6 Reserved. 7 CPMF mode has changed.")
    smf73sfl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Status flags. Bit Meaning when set 0 DCM supported by hardware. 1 Configuration contains DCM managed channels. 2 Hardware allows multiple logical channel subsystems. 3 Enhanced channel measurement facility available. 4-7 Reserved.")
    smf73tnm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(44), doc="IODF name.")
    smf73tsf: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2), doc="IODF name suffix.")
    smf73tdt: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                  doc="IODF creation date, in the form mm/dd/yy.")
    smf73crc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="CPMF (channel path measurement facility) restart count")
    smf73csc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Last CPMF (channel path measurement facility) sample count")
    smf73tdy: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                  doc="IODF creation date, in the form mm/dd/yyyy")
    smf73cmi: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="CPMF mode. Value Meaning 0 CPMF is not active 1 Compatibility mode 2 Extended mode")
    smf73css: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4),
                                                          doc="Channel subsystem ID. Only valid if bit 2 of SMF73SFL is set.")
    config_changed: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                  doc="smf73cfl (Bit 0) showing configuration changed. Used to decide whether ot provide 'POR' or 'ACTIVATE' on reports. Also used to check whether data can be combined in a duration report.")
    config_changed_since_ipl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                          doc="smf73cfl (Bit 1) showing configuration change since power-on-reset(POR).")
    ipl_iodf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="smf73cfl (Bit 2) showing POR using IODF data set that supports dynamic configuration change (contains I/O token).")
    io_token_valid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                doc="smf73cfl (Bit 3) showing I/O token is valid.")
    invalid_ds: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                            doc="smf73cfl (Bit 4) showing record may include data sections that are not valid.")
    cpmf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                      doc="smf73cfl (Bit 5) showing CPMF (channel path measurement faility) available.")
    cpmf_changed: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="smf73cfl (Bit 7) showing CPMF mode has changed.")
    dcm_supported: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="smf73sfl (Bit 0) showing DCM supported by hardware.")
    dcm_ch: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                        doc="smf73sfl (Bit 1) showing configuration contains DCM managed channels.")
    mcs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                     doc="smf73sfl (Bit 2) showing hardware allows mulitple logical chnnel subsystems.")
    ench_ch_measurement: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                     doc="smf73sfl (Bit 3) showing enhanced channel measurement faility available.")


class Smf73cha(AbstractConcreteBase):
    """Abstract class for structure Smf73cha - Channel path data section."""

    smf73pid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                          doc="Channel path identification. The range of values is X'0' to X'FF'. Support for dynamic I/0. There are always X'FF' path data sections in record type 73, even though there might not be X'FF' CHPIDs defined in the system. These dummy data sections in the SMF records only contain the channel path ID. The rest is filled with hexadecimal zeroes.")
    smf73fg2: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Channel flags Bit Meaning when set 0-1 Reserved 2 Block multiplexor 3 Byte multiplexor 4 Reserved 5 Only partial statistics available 6 Data recorded is incorrect because channel path was reconfigured during interval 7 Channel path is currently online.")
    smf73fg3: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Channel flags extension Bit Meaning when set 0 ES connection channel 1 ES connection director attached to channel path 2 ES connection converter attached to this channel 3 Channel path modified 4 Channel path deleted 5 Channel path added 6 Valid path 7 Channel path is shared between logical partitions")
    smf73fg4: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Channel path flags Bit Meaning when set 0 CPMB (channel path measurement block) entry not valid 1 Channel path is CTC defined 2 Channel conversion 3090 3 Reserved 4 Channel path is DCM managed 5 Channel characteristics changed during interval 6 Extended channel path measurements are supported 7 Physical-network identifiers SMF73NT1 and SMF73NT2 are valid.")
    smf73bsy: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of store channel path status (STCPS) samples taken by SRM in which the channel path related to this entry was found busy. This count is normalized (broken down into the simplest expression).")
    smf73pby: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Partition's channel-path-busy-time since last RMF interval, in units of 1024 microseconds.")
    smf73pti: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Partition's channel-path measurement interval, in units of 1024 microseconds.")
    smf73cpd: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4),
                                                          doc="Channel path description. For an explanation, you can issue the command D M=CHP.")
    smf73acr: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="Channel path acronym.")
    smf73cmg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="CPMF Channel measurement group.")
    smf73fg5: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="CPMF validation flags - each bit (if on) indicates that the corresponding measurement data is available and valid. This refers to the first five words of the channel measurement data in field SMF73CCM. Bit Measurement data 0 Channel measurement data - word 1 1 Channel measurement data - word 2 2 Channel measurement data - word 3 3 Channel measurement data - word 4 4 Channel measurement data - word 5 5-7 Reserved.")
    smf73cpp: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="Channel path parameter.")
    smf73gen: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="Channel type generation.")
    smf73eix: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Index to Extended Channel Path data section. Only valid if bit 6 of SMF73FG4 is set.")
    smf73spd: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Channel path speed at the end of interval. If channel path power (bits 4-7 of SMF73MSC) is zero, the channel path speed is in units of 100 megabits per second. Otherwise, this value must be multiplied by 10**Power to get the speed in units of bits per second.")
    smf73msc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Miscellaneous 0-3 Reserved. 4 -7 Channel path power at the end of interval. If non-zero, this value can be used to calculate the channel path speed (SMF73SPD * 10**Power).")
    smf73ioen: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                           doc="I/O engine number for which the measurements are collected. Valid if SMF73CMG is 4 or 5.")
    smf73nt1: so.Mapped[Optional[str]] = so.mapped_column(sa.String(16),
                                                          doc="Physical-network identifier (PNET ID) of an Ethernet network that is accessible from the first port of the channel path. Only valid for OSD and IQD channel path types and if bit 7 of SMF73FG4 is set.")
    smf73nt2: so.Mapped[Optional[str]] = so.mapped_column(sa.String(16),
                                                          doc="Physical-network identifier (PNET ID) of an Ethernet network that is accessible from the second port of the channel path. Only valid for OSD channel path type and if bit 7 of SMF73FG4 is set.")
    block_multiplexor: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                   doc="smf73fg2 (Bit 2) showing Block multiplexor.")
    byte_multiplexor: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                  doc="smf73fg2 (Bit 3) showing Byte multiplexor.")
    partial_stat: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="smf73fg2 (Bit 5) showing only partial statistics available.")
    data_invalid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="smf73fg2 (Bit 6) showing data record is incorrect because channel path was reconfigured during interval.")
    ch_path_online: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                doc="smf73fg2 (Bit 7) showing channel path is currently online.")
    es_connection_ch: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                  doc="smf73fg3 (Bit 0) showing ES connection channel.")
    es_connection_dir: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                   doc="smf73fg3 (Bit 1) showing ES connection director attached to channel path.")
    es_conv_ch: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                            doc="smf73fg3 (Bit 2) showing ES connection converter attached to this channel.")
    ch_path_modified: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                  doc="smf73fg3 (Bit 3) showing channel path modified.")
    ch_path_deleted: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                 doc="smf73fg3 (Bit 4) showing channel path deleted.")
    ch_path_inserted: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                  doc="smf73fg3 (Bit 5) showing channel path added.")
    valid_path: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="smf73fg3 (Bit 6) showing valid path.")
    ch_path_shared: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                doc="smf73fg3 (Bit 7) showing channel path is shared between logical partitions.")
    cpmb_invalid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="smf73fg4 (Bit 0) showing channel path measurement block entry not valid.")
    ctc_defined: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                             doc="smf73fg4 (Bit 1) showing channel path is CTC defined.")
    ch_conversion: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="smf73fg4 (Bit 2) showing channel conversion 3090.")
    ch_path_dcm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                             doc="smf73fg4 (Bit 4) showing channel path is DCM managed.")
    ch_charact_changed: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                    doc="smf73fg4 (Bit 5) showing channel characteristics changed during interval.")
    ch_path_extended: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                  doc="smf73fg4 (Bit 6) showing extended channel path measurements are supported.")
    physical_network: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                  doc="smf73fg4 (Bit 7) showing physical-network id smf73nt1 and nt2 are valid.")
    cpmf_word1: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                            doc="smf73fg5 (Bit 0) showing channel measurement data - word 1.")
    cpmf_word2: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                            doc="smf73fg5 (Bit 1) showing channel measurement data - word 2.")
    cpmf_word3: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                            doc="smf73fg5 (Bit 2) showing channel measurement data - word 3.")
    cpmf_word4: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                            doc="smf73fg5 (Bit 3) showing channel measurement data - word 4.")
    cpmf_word5: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                            doc="smf73fg5 (Bit 4) showing channel measurement data - word 5.")


class Smf73ccm1(AbstractConcreteBase):
    """Abstract class for structure Smf73ccm1 - CPMF channel measurement data in the SMF73CCM field for measurement group 1."""

    smf73tut: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total channel path busy time (in units of 128 microseconds).")
    smf73put: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="LPAR channel path busy time (in units of 128 microseconds).")


class Smf73ccm2(AbstractConcreteBase):
    """Abstract class for structure Smf73ccm2 - CPMF channel measurement data in the SMF73CCM field for measurement group 2."""

    smf73mbc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Maximum bus cycles per second - word 1.")
    smf73mcu: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Maximum channel work units per second - word 2.")
    smf73mwu: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Maximum WRITE data units per second - word 3.")
    smf73mru: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Maximum READ data units per second - word 4.")
    smf73us: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Data unit size (in bytes) - word 5.")
    smf73tbc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Total bus cycles count.")
    smf73tuc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Total channel work unit count.")
    smf73puc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="LPAR channel work units count.")
    smf73twu: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Total WRITE data units count.")
    smf73pwu: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="LPAR WRITE data units count.")
    smf73tru: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Total READ data units count.")
    smf73pru: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="LPAR READ data units count.")


class Smf73ccm3(AbstractConcreteBase):
    """Abstract class for structure Smf73ccm3 - CPMF channel measurement data in the SMF73CCM field for measurement group 3."""

    smf73pdu: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="LPAR data unit size (in bytes) - word 1.")
    smf73tdu: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Total data unit size (in bytes) - word 2.")
    smf73pum: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="LPAR message sent unit size (in bytes) - word 3.")
    smf73tum: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total message sent unit size (in bytes) - word 4.")
    smf73pms: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="LPAR count of message sent units.")
    smf73tms: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Total count of message sent units.")
    smf73pus: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="LPAR count of unsuccessful attempts to send messages.")
    smf73pub: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="LPAR count of unsuccessful attempts to receive messages due to unavailable buffers.")
    smf73tub: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total count of unsuccessful attempts to receive messages due to unavailable buffers.")
    smf73pds: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="LPAR count of data units sent.")
    smf73tds: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Total count of data units sent.")


class Smf73ccm4(AbstractConcreteBase):
    """Abstract class for structure Smf73ccm4 - CPMF channel measurement data in the SMF73CCM field for measurement group 4."""

    smf73g4mbc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Maximum bus cycles per second - word 1.")
    smf73g4mcu: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="Maximum channel work units per second - word 2.")
    smf73g4mwu: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="Maximum WRITE data units per second - word 3.")
    smf73g4mru: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="Maximum READ data units per second - word 4.")
    smf73g4ioec: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                             doc="Number of I/O Engine (IOE) Cores - byte 1 of word 5.")
    smf73g4us: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                           doc="Data unit size (in bytes) - bytes 2-4 of word 5.")
    smf73g4tbc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Total bus cycles count.")
    smf73g4tuc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Total channel work units count.")
    smf73g4puc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="LPAR channel work units count.")
    smf73g4twu: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Total WRITE data units count.")
    smf73g4pwu: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="LPAR WRITE data units count.")
    smf73g4tru: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Total READ data units count.")
    smf73g4pru: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="LPAR READ data units count.")


class Smf73ccm5(AbstractConcreteBase):
    """Abstract class for structure Smf73ccm5 - CPMF channel measurement data in the SMF73CCM field for measurement group 5."""

    smf73g5mbc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Maximum bus cycles per second - word 1.")
    smf73g5mcu: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="Maximum channel work units per second - word 2.")
    smf73g5mwu: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="Maximum WRITE data units per second - word 3.")
    smf73g5mru: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="Maximum READ data units per second - word 4.")
    smf73g5ioec: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                             doc="Number of I/O Engine (IOE) Cores - byte 1 of word 5.")
    smf73g5us: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                           doc="Data unit size (in bytes) - bytes 2-4 of word 5.")
    smf73g5tbc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Total bus cycles count.")
    smf73g5tuc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Total channel work units count.")
    smf73g5puc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="LPAR channel work units count.")
    smf73g5twu: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Total WRITE data units count.")
    smf73g5pwu: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="LPAR WRITE data units count.")
    smf73g5tru: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Total READ data units count.")
    smf73g5pru: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="LPAR READ data units count.")


class Smf73edt2(AbstractConcreteBase):
    """Abstract class for structure Smf73edt2 - CPMF extended channel path measurement data in the SMF73EDT field for measurement group 2."""

    smf73eoc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total number of FICON command-mode operations (CPC) that have been attempted by the channel.")
    smf73eod: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total number of FICON command-mode operations (CPC) that could not be initiated by the channel because of a lack of available resources.")
    smf73eos: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Summation count of FICON command-mode operations (CPC). Each time the number of FICON command-mode operations is incremented, the number of FICON command-mode operations active at the channel, including the one being initiated, is added to this field.")
    smf73etc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total number of FICON transport-mode operations (CPC) that have been attempted by the channel. Zero when zHPF is not available.")
    smf73etd: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total number of FICON transport-mode operations (CPC) that could not be initiated by the channel because of a lack of available resources. Zero when zHPF is not available.")
    smf73ets: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Summation count of FICON transport-mode operations (CPC). Each time the number of FICON transport-mode operations is incremented, the number of transport-mode operations active at the channel, including the one being initiated, is added to this field. Zero when zHPF is not available.")


class Smf73edt4(AbstractConcreteBase):
    """Abstract class for structure Smf73edt4 - CPMF extended channel path measurement data in the SMF73EDT field for measurement group 4."""

    smf73g4ecet: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                               doc="Total channel execution time (per cycle) this channel has been active.")
    smf73g4eioet: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="Total I/O Engine (IOE) execution time (per cycle) for the IOE complex this channel has been active. The IOE complex consists of the number of I/O Engine Cores specified in byte 1 of word 5 (SMF73G4IOEC).")


class Smf73edt5(AbstractConcreteBase):
    """Abstract class for structure Smf73edt5 - CPMF extended channel path measurement data in the SMF73EDT field for measurement group 5."""

    smf73g5ecet: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                               doc="Total channel execution time (per cycle) this channel has been active.")
    smf73g5eioet: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="Total I/O Engine (IOE) execution time (per cycle) for the IOE complex this channel has been active. The IOE complex consists of the number of I/O Engine Cores specified in byte 1 of word 5 (SMF73G5IOEC).")
    smf73g5eoc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="Total number of FICON command-mode operations (CPC) that have been attempted by the channel.")
    smf73g5eod: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="Total number of FICON command-mode operations (CPC) that could not be initiated by the channel because of a lack of available resources.")
    smf73g5eos: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="Summation count of FICON command-mode operations (CPC). Each time the number of FICON command-mode operations is incremented, the number of FICON command-mode operations active at the channel, including the one being initiated, is added to this field.")
    smf73g5etc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="Total number of FICON transport-mode operations (CPC) that have been attempted by the channel. Zero when zHPF is not available.")
    smf73g5etd: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="Total number of FICON transport-mode operations (CPC) that could not be initiated by the channel because of a lack of available resources. Zero when zHPF is not available.")
    smf73g5ets: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="Summation count of FICON transport-mode operations (CPC). Each time the number of FICON transport- mode operations is incremented, the number of transport-mode operations active at the channel, including the one being initiated, is added to this field. Zero when zHPF is not available.")
