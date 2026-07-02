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


class Base74(Base):
    __abstract__ = True
    metadata = sa.MetaData(schema='smf74', naming_convention=convention)


class Base74Hr(Base):
    __abstract__ = True
    metadata = sa.MetaData(schema='smf74', naming_convention=convention)


class Base74Da(Base):
    __abstract__ = True
    metadata = sa.MetaData(schema='smf74', naming_convention=convention)


class Smf74pro(AbstractConcreteBase):
    """Abstract class for structure Smf74Pro - RMF product section."""

    smf74mfv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="RMF version number.")
    smf74prd: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Product name ('RMF').")
    smf74int: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Duration of RMF measurement interval, in the form mmsstttF where mm is the minutes, ss is the seconds, ttt is the milliseconds, and F is the sign. The end of the measurement interval is the sum of the recorded start time and this field.")
    smf74sam: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of RMF samples.")
    smf74fla: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Flags Bit Meaning when set 0 Reserved. 1 Samples have been skipped 2 Record was written by RMF Monitor III 3 Interval was synchronized with SMF 4 SMF record converted to lower service level. 5 SMF record converted to higher release or service level. 6 Running under an alternate virtual machine. 7-15")
    smf74cyc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Sampling cycle length, in the form 000 ttttF , where tttt is the milliseconds and F is the sign (taken from CYCLE option). The range")
    smf74mvs: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="z/OS software level (consists of an acronym and the version, release, and modification level - ZV vvrrmm ).")
    smf74iml: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Indicates the type of processor complex on which data measurements were taken. Value Meaning 3 9672, zSeries")
    smf74prf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Processor flags. Bit Meaning when set 0 The system has expanded storage 1 The processor is enabled for ES connection architecture (ESCA) 2 There is an ES connection director in the configuration 3 System is running in z/Architecture mode 4 At least one zAAP is currently installed 5 At least one zIIP is currently installed 6 Enhanced DAT facility 1 available 7")
    smf74ptn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="PR/SM partition number of the partition that wrote this record.")
    smf74srl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="SMF record level change number. This field enables processing of SMF record level changes in an existing release. SMF type 74 record levels for the current z/OS release: Subtype Record level 1-3 X'8E' 4 X'8F' (APAR OA61041) 5-7 X'8E' 8 X'8F' (APAR OA66017) 9-10 X'8E'")
    smf74lgo: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Offset GMT to local time (STCK format).")
    smf74oil: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Original interval length as defined in the session or by SMF (in seconds).")
    smf74syn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="SYNC value in seconds.")
    smf74gie: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                  doc="Projected gathering interval end (STCK format) GMT time.")
    smf74xnm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf74snm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="System name for current system as defined in parmlib member IEASYSxx SYSNAME parameter.")
    smf74flg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="System indicator Bit Meaning when set 0 New record format 1 Subtypes used 2 Reserved. 3-6 Version indicators (See 'Standard and extended SMF record headers' on page 164 for details.) 7 System is running in PR/SM mode.")


class Smf74dma0(AbstractConcreteBase):
    """Abstract class for structure Smf74dma0 - PCIE function type data section for format x'00'."""

    r749dmar: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="DMA read counter that reports the number of bytes transferred from all defined DMA address spaces to the PCIE function.")
    r749dmaw: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="DMA write counter that reports the number of bytes transferred from the PCIE function to all defined DMA address spaces.")
    r749dfmt: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="Format x'00'")


class Smf74dma1(AbstractConcreteBase):
    """Abstract class for structure Smf74dma1 - PCIE function type data section for format x'01'."""

    r749dbyr: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Number of bytes received on the external Ethernet interface.")
    r749dbyt: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Number of bytes transmitted on the external Ethernet interface.")
    r749dfmt: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="Format x'01'")
    r749dpkr: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Number of packets received on the external Ethernet interface.")
    r749dpkt: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Number of packets transmitted on the external Ethernet interface.")


class Smf74dma2(AbstractConcreteBase):
    """Abstract class for structure Smf74dma2 - PCIE function type data section for format x'02'."""

    r749dwup: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Number of work units processed by the PCI function.")
    r749dwum: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Maximum number of work units that the PCI function is capable of processing per second.")
    r749dfmt: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="Format x'02'")


class Smf74dma3(AbstractConcreteBase):
    """Abstract class for structure Smf74dma3 - PCIE function type data section for format x'03'."""

    r749dbyx: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Number of bytes transmitted by the PCI function.")
    r749dfmt: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="Format x'03'")


class Smf74dma4(AbstractConcreteBase):
    """Abstract class for structure Smf74dma4 - PCIE function type data section for format x'04'."""

    r749srbf: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Number of bytes read by this synchronous I/O function.")
    r749swbf: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Number of bytes written by this synchronous I/O function.")
    r749dfmt: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="Format x'04'")
    r749ssrf: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Number of successful requests for this synchronous I/O function.")
    r749slrf: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Number of times the command was rejected by the processor (local rejects) for this synchronous I/O function.")
    r749srrf: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Number of times the command was rejected by the storage controller (remote rejects) for this synchronous I/O function.")
    r749stpf: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total processing time in microseconds for this synchronous I/O function.")
    r749srbc: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Number of bytes read by all synchronous I/O functions that are using this synchronous I/O link on this CPC. Only valid, if bit 3 of R749FLAG is set.")
    r749swbc: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Number of bytes written by all synchronous I/O functions that are using this synchronous I/O link on this CPC. Only valid, if bit 3 of R749FLAG is set.")
    r749ssrc: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Number of requests successfully processed by all synchronous I/O functions that are using this synchronous I/O link on this CPC. Only valid, if bit 3 of R749FLAG is set.")
    r749slrc: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Number of local rejects of all synchronous I/O functions that are using this synchronous I/O link on this CPC. Only valid, if bit 3 of R749FLAG is set.")
    r749srrc: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Number of remote rejects of all synchronous I/O functions that are using this synchronous I/O link on this CPC. Only valid, if bit 3 of R749FLAG is set.")
    r749stpc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total processing time in microseconds of all synchronous I/O functions that are using this synchronous I/O link on this CPC. Only valid, if bit 3 of R749FLAG is set.")


class Smf74pstat(AbstractConcreteBase):
    """Abstract class for structure Smf74pstat - FCD port statistics."""

    r747pfpt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Frame pacing time (in units of 2.5 microseconds).")
    r747pnwr: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Number of words received.")
    r747pnwt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Number of words transmitted.")
    r747pnfr: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Number of frames received.")
    r747pnft: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Number of frames transmitted.")
    r747pner: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Number of errors.")


class Smf741dev(AbstractConcreteBase):
    """Abstract class for structure Smf741dev - RAID rank/extent pool data Section."""

    r7451rmr: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Record mode read request.")
    r7451xsf: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Extended-Remote-Copy(XRC) or Concurrent-Copy(CC) sidefile read request.")
    r7451xcw: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="XRC or CC contaminated writes.")
    r7451tsp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of tracks transferred to secondary Peer-to-Peer-Remote- Copy(PPRC) volume.")
    r7451nvs: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="NVS space allocation.")
    r7451ct1: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Bytes read. For units, see bits 5 and 6 of R7451INC.")
    r7451ct2: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Bytes written. For units, see bits 5 and 6 of R7451INC.")
    r7451ct3: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Read response time. For units, see bits 5 and 6 of R7451INC.")
    r7451ct4: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Write response time. For units, see bits 5 and 6 of R7451INC.")
    r7451ct5: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of zHPF read I/O requests (valid if bit 4 in R7451INC is set).")
    r7451ct6: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of zHPF write I/O requests (valid if bit 4 in R7451INC is set).")
    r7451zhl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="zHPF List Pre-fetch I/O Requests. Number of command chains, where the Transport Mode operation specified a non-zero Imbedded Locate Record Count.")
    r7451zhh: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="zHPF List Pre-fetch I/O Request Hits. Number of command chains, where • the Transport Mode operation specified a non-zero Imbedded Locate Record Count. • the chain was completed without requiring access to any DDM.")
    r7451gsf: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Global Mirror Collisions sidefile count. A GMC occurs when, during the sending of data in the secondary to create a consistency group, a subsequent host update is attempted before the modified track has been transmitted to the secondary volume. The modified track will be moved to the sidefile before allowing a new host write. The counter will be incremented by one when a track is added to the sidefile.")
    r7451gss: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Global Mirror Collisions synchronous count. When a write collision occurs, the modified track data which belongs to the current consistency group may be sent to the remote control unit before allowing the write. The data may come from the sidefile if it is full or from cache if the collision sidefile is not being utilized.")
    r7451srr: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of synchronous I/O cache read requests. (Valid if bit 3 of R7451INC is set.)")
    r7451srh: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of synchronous I/O cache read request hits. (Valid if bit 3 of R7451INC is set.)")
    r7451swr: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of synchronous I/O cache write requests. (Valid if bit 3 of R7451INC is set.)")
    r7451swh: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of synchronous I/O cache write request hits. (Valid if bit 3 of R7451INC is set.)")
    r7451unt: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                          doc="r7451inc (Bit 5-6) showing measurement units ('00' - Bytes in units of 128K, and times in units of 16 milliseconds)")


class Smf74gsrg(AbstractConcreteBase):
    """Abstract class for structure Smf74gsrg - Coupling Facility storage data section."""

    r744gcsd: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Total amount of control storage defined (4K-block units).")
    r744gcsf: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Amount of free control storage (4K-block units).")
    r744gtsd: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Total amount of coupling facility storage defined (4K-block units).")
    r744gtsf: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Amount of free coupling facility storage (4K-block units).")
    r744gdsa: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Amount of dump space allocated (4K-block units).")
    r744gdsf: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Amount of free dump space (4K-block units).")
    r744gdsr: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Maximum amount of dump space requested (4K-block units).")
    r744gtsc: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Total amount of coupling facility storage class memory (4K-block units) which may be concurrently used as structure extensions.")
    r744gfsc: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Amount of free coupling facility storage class memory (4K-block units).")
    r744gisc: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Amount of storage class memory increment. This is the number of 4K blocks that are assigned to a single storage class memory segment.")


class Smf74lcf(AbstractConcreteBase):
    """Abstract class for structure Smf74Lcf - Local Coupling Facility data section."""

    r744fpbc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of times coupling facility requests are delayed due to path busy.")
    r744fscg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of subchannels defined.")
    r744fscu: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of subchannels currently in use.")
    r744fscl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of subchannels that can be used (limit).")
    r744fscc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Subchannel contention count (all subchannel busy).")
    r744ftor: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Total number of requests from this system.")
    r744fail: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of unsuccessful requests from this system.")
    r744ftim: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total service time for unsuccessful requests in microseconds.")
    r744fsqu: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total squares of service time for unsuccessful requests (in square- microseconds).")
    r744fctm: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total contention time (microseconds) for waiting for subchannels to become free for synchronous immediate operations.")
    r744fcsq: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total squares of contention time for waiting for subchannels to become free for synchronous immediate operations.")
    smf74sam: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of RMF samples.")


class Smf74arry(AbstractConcreteBase):
    """Abstract class for structure Smf74Arry - Rank array data section."""

    r748aebc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(16),
                                                          doc="Description of array type, for example: RAID-10.")
    r748atyp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Array type: Value Meaning 1 RAID-5 2 RAID-10 3")
    r748aasp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Array speed in 1000 RPM.")
    r748aawd: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Array width.")
    r748aacp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Array effective DDM capacity, in GB. For compression drives, this is the total logical capacity.")
    r748aast: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Array device class and array status Bit Meaning when set 0-1 Device class. B'00' = Enterprise drive B'01' = Near-line drive B'10' = SATA drive B'11' = Solid state drive 2 Raid degraded. 3 DDM throttling. 4 RPM exception. 5 Reserved. 6 DDM class is compression. 7 Reserved.")
    r748adc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                         doc="r748aast (Bit 0-1) showing array device class.")
    r748ard: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="r748aast (Bit 2) showing raid degraded.")
    r748adt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="r748aast (Bit 3) showing DDM throttling.")
    r748are: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="r748aast (Bit 4) showing RPM exception.")
    r748acmp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r748aast (Bit 6) showing DDM class is compression.")
    rank_cap: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="rank capacity.")


class Smf74cdata(AbstractConcreteBase):
    """Abstract class for section Smf74cdata."""

    r745svol: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Volume serial of device.")
    r745sunt: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Unit address for sense command.")
    r745sdev: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Device number.")
    r745sln: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length of data section.")
    r745sft: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                         doc="Status data format. Bit Meaning 0 - 3 Reserved. 4 - 7 Format of data returned: B'0000' = 40 bytes sense B'0001' = 44 bytes sense/unit KB")
    r745sdid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="Device ID.")
    r745snad: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of attached devices.")
    r745snss: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of statistic sets.")
    r745scs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                         doc="Caching status. Bit Meaning 0-2 Overall caching status: B'000' = Caching active. B'001' = Reserved. B'010' = Subsystem error. B'011' - B'111' = Reserved. 3-6")
    r745svss: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Bit Meaning 0 Host termination. 1 Problem termination. 2 DFW inhibited. 3 Disabled for maintenance. 4 Pending due to problem. 5-7")
    r745scln: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length of subsystem count area.")
    r745scsf: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="State of Copy Services function.")
    r745scnf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Configured subsystem storage: • In bytes, if R745SFT = 0 • In kilobytes (KB), if R745SFT = 1 or 2")
    r745savl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Available subsystem storage: • In bytes, if R745SFT = 0 • In kilobytes (KB), if R745SFT = 1 or 2")
    r745spin: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Pinned subsystem storage: • In bytes, if R745SFT = 0 • In kilobytes (KB), if R745SFT = 1 or 2")
    r745soff: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Offline subsystem storage: • In bytes, if R745SFT = 0 • In kilobytes (KB), if R745SFT = 1 or 2")
    r745sds1: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Addressed device status 1. Bit Meaning 0-1 Device caching status: B'00' = Caching activated. 2-3 DASD fast write status: B'00' = DFW allowed. 4 PPRC copy pair is suspended. 5 PPRC copy pair is duplex pending. 6-7 Duplex pair status: B'00' = PPRC pair available (full duplex). B'01' = PPRC pair pending. B'10' = Not used. B'11' = Suspended.")
    r745sds2: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Description Addressed device status 2. If R745SFT = 0: Bit Meaning 0 - 1 Pinned data: B'00' = No pinned data exists for the device. B'01' = Pinned data exists for the device. B'10' = Reserved. B'11' = Not used. 2 - 5 Not used. 6 Advanced FlashCopy enabled. 7 FlashCopy volume enabled. If R745SFT = 1 or 2: Bit Meaning 0 - 2 Global Mirror state: B'000' = No Global Mirror configured. B'001' = Global Mirror running - optimal. B'010' = Global Mirror running - suboptimal. B'011' = Global Mirror running - consistency groups failing. B'100' = Global Mirror paused. B'101' = Global Mirror fatal. B'110' = More than one Global Mirror session is running. B'111' = Reserved. 3 Session member is pending. 4 Volume not allowed online. 5 Reserved. 6 Advanced FlashCopy enabled.")
    r745scnv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Configured non-volatile cache: • In bytes, if R745SFT = 0 • In kilobytes (KB), if R745SFT = 1 or 2")
    r745spnd: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Pinned non-volatile cache: • In bytes, if R745SFT = 0 • In kilobytes (KB), if R745SFT = 1 or 2")
    r745sg2: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                         doc="Device status group 2. Bit Meaning 0-1 Volume space management: B'00' = Standard volume B'01' = Track space efficient volume B'10' = Extent space efficient volume B'11' = Reserved 2 Data exists on failed NVS. 3 Device is in a soft fenced state. 4 Device is in a SPID fenced state. 5 Volume is part of a RAID rank that is undergoing RAID rebuild. 6-7 (if R745SFT = 1 or 2) Pinned data: B'00' = No pinned data exists for the device. B'01' = Pinned data exists for the device. B'10' = Reserved.")
    r745sgl: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4),
                                                         doc="Global status. Bit Meaning 0 CFW and DFW suspended. 1-7")
    r745sos: so.Mapped[Optional[str]] = so.mapped_column(sa.String(3), doc=" overall caching status.")
    r745snr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                         doc=" r745scs (Bit 7) showing non-retentive deactivated.")
    r745snht: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc=" r745svss (Bit 0) showing non-volatile storage host termination.")
    r745snis: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc=" r745svss (Bit 1) showing non-volatile storage problem termination.")
    r745dfwi: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc=" r745svss (Bit 2) showing non-volatile storage DFW inhibited.")
    r745snds: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc=" r745svss (Bit 3) showing non-volatile storage disabled for maintenance.")
    r745snpe: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc=" r745svss (Bit 4) showing non-volatile storage pending due to problem.")
    r745sdcs: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                          doc=" r745sds1 (Bit 0-1) showing device caching status.")
    r745sdfw: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                          doc=" r745sds1 (Bit 2-3) showing DASD fast write status.")
    r745spdp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc=" r745sds1 (Bit 4) showing  PPRC copy pair suspended.")
    r745ssdp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc=" r745sds1 (Bit 5) showing  PPRC copy pair is duplex pending.")
    r745sdps: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                          doc=" r745sds1 (Bit 6-7) showing PPRC pair status.")
    r745scol: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                          doc=" r745sg2 (Bit 0-1) showing volume space management.")
    r745sfvs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc=" r745sg2 (Bit 2) showing data exists on failed NVS.")
    r745sdbp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc=" r745sg2 (Bit 3) showing device in a soft fenced state.")
    r745spda: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                          doc=" r745sg2 (Bit 6-7) showing pinned data status.")


class Smf74cdev(AbstractConcreteBase):
    """Abstract class for structure Smf74Cdev - Cache device data section."""

    r745drcr: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Search read caching requests.")
    r745dcrh: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Search read caching hits.")
    r745dwrc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Write caching requests.")
    r745dwch: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Write caching request hits.")
    r745drsr: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Read sequential requests.")
    r745drsh: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Read sequential request hits.")
    r745dwsr: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Write sequential requests.")
    r745dwsh: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Write sequential request hits.")
    r745drnr: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Search read non-retentive requests.")
    r745dnrh: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Search read non-retentive request hits.")
    r745dwnr: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Write non-retentive requests.")
    r745dwnh: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Write non-retentive hits.")
    r745dicl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Inhibit cache load requests.")
    r745dbcr: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Bypass cache requests.")
    r745dtc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Sequential DASD to cache XFRs.")
    r745dntd: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Normal cache requests DASD to cache XFRs.")
    r745dctd: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Cache to DASD XFRs.")
    r745dfwb: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="DASD Fast Write operations delayed due to non-volatile storage space constraints.")
    r745dfwc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Fast write caching requests.")
    r745dfws: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Fast write sequential requests.")
    r745dcrm: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Record cache read misses.")
    r745dcwp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="RCD cache write promotions.")
    r745dkdw: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="CKD writes, collected for 3990-03/06 and 2105.")
    r745dkdh: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="CKD write hits, collected for 3990-03/06 and 2105.")
    r745dfwr: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Operations delayed due to cache space constraints.")
    r745bytr: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Bytes read.")
    r745bytw: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Bytes written.")
    r745rtir: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Response time to read bytes.")
    r745rtiw: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Response time to write bytes.")
    r745cint: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of seconds since subsystem statistics last collected.")
    total_io: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="total number of I/O requests to cached device.")
    cache_io: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="total number of cacheable I/O request to cached device. This value excludes INHIBIT CACHE LOAD and CACHE BYPASS I/O requests.")
    total_hits: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="total number of requests that completed without accessing the DASD.")
    total_reads: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="total number of SEARCH/READ requests.")
    read_hits: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                             doc="number of SEARCH/READ requests that completed without accessing the DASD.")
    total_writes: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="total number WRITE requests.")
    fast_writes: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                               doc="total number of DASD/CACHE FAST WRITE requests.")
    write_hits: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="number of DASD/CACHE FAST WRITE requests that completed without accessing the DASD (fast write hit).")
    dasd_io: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="total number of requests that accessed DASD.")


class Smf74rank(AbstractConcreteBase):
    """Abstract class for structure Smf74Rank - Rank statistics section."""

    r748rcnt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of arrays in rank.")
    r748rbyr: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Rank 128 KB read.")
    r748rbyw: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Rank 128 KB write.")
    r748rrop: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Rank read operations.")
    r748rwop: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Rank write operations.")
    r748rkrt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Rank read response time in units of 16 milliseconds.")
    r748rkwt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Rank write response time in units of 16 milliseconds.")
    r748rtq: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                         doc="Rank type qualifier: Bit Meaning when set 0 Data encrypted rank. 1 Compression rank. 2-6 Reserved. 7 Rank adapter pair ID is valid.")
    r748rai: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="Rank adapter pair ID")
    data_encrypted_rank: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                     doc="r748rtq (Bit 0) showing data encrypted rank.")
    compression_rank: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                  doc="r748rtq (Bit 1) showing compression rank.")
    rank_adapter_id_valid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                       doc="r748rtq (Bit 7) showing rank adapter pair ID is valid.")


class Smf74xpool(AbstractConcreteBase):
    """Abstract class for structure Smf74Xpool - Extent pool data section."""

    r7451scs: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2), doc="Subchannel set ID.")
    r7451rsv: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Lower interface I/O response time (in milliseconds).")
    r7451flg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Flag. Value Meaning 0 No additional information 1 RAID rank data. 2 Extent pool and physical storage data.")
    r7452xty: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4),
                                                          doc="Extent type: Value Meaning X'04' FB 1Gb X'84' CKD 1Gb")
    r7451sio: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r7451inc (Bit 3) showing synchronous I/O cache data are valid.")
    r7451hpf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r7451inc (Bit 4) showing zHPF read and write I/O requests r7451ct5 and r7451ct6 are available.")
    r7451xfl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r7451inc (Bit 7) showing transfer statistics r7451xfr are valid.")
    r7452dxa: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r7452xfl (Bit 0) showing dynamic extent allocation.")
    r7452dsh: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="r7452xfl (Bit 1) showing data sharing.")
    r7452mis: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r7452xfl (Bit 2) showing migrating/migration state.")


class Smf74adup(AbstractConcreteBase):
    """Abstract class for structure Smf74Adup - Asynchronous CF duplexing data Section."""

    r744afo: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                         doc="The most current failed operation sequence number.")
    r744aheo: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Highest operation sequence number that can be executed and completed in the secondary CF.")
    r744alaoh: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                           doc="Highest sequence number of the operation that has been executed in the primary structure. (Valid if bit 4 of R744SFLG is set.)")
    r744alaosh: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                            doc="Highest sequence number of the operation that has completed in the primary and has been recognized by the secondary structure.")
    r744alcoh: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                           doc="Highest sequence number of the operation that has completed in the secondary structure. (Valid if bit 5 of R744SFLG is set.)")
    r744alcoph: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                            doc="Highest sequence number of the operation that has completed in the secondary structure and that has been recognized by the primary structure.")
    r744alao: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Number of asynchronous duplex operations that have been executed in the primary structure. (Valid if bit 4 of R744SFLG is set.)")
    r744alaos: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                           doc="Number of asynchronous duplex operations that have executed in the primary and have been recognized in the secondary structure.")
    r744alco: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Number of asynchronous duplex operations transmitted from the primary to the secondary structure that completed in the secondary structure. (Valid if bit 5 of R744SFLG is set.)")
    r744alcop: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                           doc="Number of asynchronous duplex operations that have been completed both in the primary and in the secondary structure that has been recognized by the primary structure.")
    r744atpoct: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                            doc="Total number of asynchronous duplex operations that have been transmitted from the primary to the secondary structure.")
    r744atpoc: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                           doc="Number of asynchronous duplex operations transmitted from the primary to the secondary structure in this interval.")
    r744arcpot: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                            doc="Total number of asynchronous duplex operations that have completed in the secondary and have been recognized as complete to the primary structure.")
    r744arcpo: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                           doc="Number of asynchronous duplex operations transmitted from the primary to the secondary structure and recognized as complete to the primary structure in this interval.")
    r744acqsc: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                           doc="Number of stalls in the processing of the secondary operation queue.")
    r744apdt: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Total amount of primary delay time for asynchronous duplex operations, in microseconds. The primary delay time is the elapsed time in the primary CF between the assignment of the operation to the queue buffer and the first attempt to send the")
    r744apdq: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Total amount of squares of primary delay time for asynchronous duplex operations, in square of microseconds.")
    r744amdt: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Total amount of message delay time for asynchronous duplex operations, in microseconds. The message delay time is the elapsed time from the first attempt to send the asynchronous duplex operation in the primary CF to the time that the secondary CF assigns the asynchronous duplex operation to a secondary queue entry.")
    r744amdq: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Total amount of squares of message delay time for asynchronous duplex operations, in square of microseconds.")
    r744aqdt: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Total amount of secondary queue delay time for asynchronous duplex operations, in microseconds. The secondary queue delay time is the elapsed time from the time the asynchronous duplex operation is assigned to a secondary queue entry to the time of")
    r744aqdq: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Total amount of squares of secondary queue delay time for asynchronous duplex operations, in square of microseconds.")
    r744aqst: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Total amount of secondary queue stall time for asynchronous duplex operations, in microseconds.")
    r744aqsq: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Total amount of squares of secondary queue stall time for asynchronous duplex operations, in square of microseconds.")
    r744acdt: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Total amount of secondary reported completion delay time for asynchronous duplex operations, in microseconds. The secondary reported completion delay time is the elapsed time in the secondary CF, from the time the asynchronous duplex operation completes in the secondary to the time that the completion is reported to the primary.")
    r744acdq: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Total amount of squares of secondary reported completion delay time for asynchronous duplex operations, in square of microseconds.")
    r744ardt: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Total amount of response delay time for asynchronous duplex operations, in microseconds. The response delay time is the elapsed time from the launch of the operation response in the secondary CF to the time that the primary CF recognizes the response.")
    r744ardq: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Total amount of squares of response delay time for asynchronous duplex operations, in square of microseconds.")
    r744aott: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Total amount of operation transmission time for operations sent from the primary to the secondary structure, in microseconds. (Valid if bit 5 of R744SFLG is set.)")
    r744aotq: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Total amount of squares of operation transmission time, in square of microseconds. (Valid if bit 5 of R744SFLG is set.)")
    r744astt: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Total amount of service time to transfer the asynchronous duplex operations to the secondary structure and complete the operations in the secondary structure, in microseconds. (Valid if bit 5 of R744SFLG is set.)")
    r744astq: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Total amount of squares of service time to transfer the asynchronous duplex operations to the secondary structure and complete the operations in the secondary structure, in square of microseconds. (Valid if bit 5 of R744SFLG is set.)")


class Smf74cach(AbstractConcreteBase):
    """Abstract class for structure Smf74Cach - Coupling Facility cache data section."""

    r744crhc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Read hit counter.")
    r744crmd: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Read miss, directory hit counter.")
    r744crma: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Read miss, assignment suppressed counter.")
    r744crmn: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Read miss, name assigned counter.")
    r744crmt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Read miss, target storage class full.")
    r744cwh0: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Write hit change bit 0 - number of times unchanged data was written.")
    r744cwh1: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Write hit change bit 1 - number of times changed data was written.")
    r744cwmn: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Write miss not registered counter.")
    r744cwmi: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Write miss invalid state counter.")
    r744cwmt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Write miss storage class full counter.")
    r744cder: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Directory entry reclaim counter.")
    r744cdtr: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Data entry reclaim counter.")
    r744cxdr: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="XI directory reclaim counter.")
    r744cxfw: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="XI write counter.")
    r744cxni: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="XI name invalidation counter.")
    r744cxci: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="XI complement invalidation counter.")
    r744ccoc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Castout counter.")
    r744crsm: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Reference signal miss counter.")
    r744ctsf: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Target storage class full counter.")
    r744cdec: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Directory entry counter snapshot.")
    r744cdac: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Data element counter snapshot.")
    r744ctcc: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Total changed counter.")
    r744cdta: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Data area counter.")
    r744crlc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Completed reference list counter.")
    r744cprl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Partially completed reference list counter.")
    r744cxrl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="XI for local cache vector index replacement.")
    r744cwuc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Write unchanged counter.")


class Smf74cachsys(AbstractConcreteBase):
    """Abstract class for structure Smf74Cachsys - Cache subsystem control data section."""

    r745clvl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Gatherer level.")
    r745cmdl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Caching subsystem model.")
    r745cuid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="Real control unit ID.")
    r745csc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                         doc="Status code. Value Meaning 0 Successful processed. 4 IOS return code R745CIOC ¬= 0. 8 IDCSS01 return code R745CRTN ¬= 0. 98 SYSTEM or USER ABEND R745CEA ¬= 0.")
    r745cae: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                         doc="ABEND CODE (SDWACMPC): First 12 bits = System completion code. Second 12 bits = User completion code.")
    r745crtn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="IDCSS01 return code. If not zero, record has no Device data sections (SMF745DN=0).")
    r745cioc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="IOS return code. If not zero, record has no Device data sections (SMF745DN = 0).")
    r745cint: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of seconds since subsystem statistics last collected.")
    r745cfdv: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Failing device")
    r745ccmt_typen: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="hardware type.")
    r745ccmt_modn: so.Mapped[Optional[str]] = so.mapped_column(sa.String(3), doc="hardware model.")
    r745ccmt_manuf: so.Mapped[Optional[str]] = so.mapped_column(sa.String(3), doc="control Unit Manufacturer Code.")
    r745ccmt_pmanu: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2), doc="control Unit Manuflacturer Plant.")
    r745ccmt_seqn: so.Mapped[Optional[str]] = so.mapped_column(sa.String(12), doc="control Unit Serial Number.")
    r745ccmt_tag: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="hardare tag.")


class Smf74cfrf(AbstractConcreteBase):
    """Abstract class for structure Smf74Cfrf - Remote facility data section."""

    r744rres: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Ready-to-execute signal counter.")
    r744rrcs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Ready-to-complete signal counter.")
    r744rhes: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Halt-execution signal counter.")
    r744rrss: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Request-for-suppression signal counter.")
    r744rrsa: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Request-for-suppression-accepted signal counter.")
    r744rsst: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Unused. Value is now in R744RSSE.")
    r744rsss: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Total squares of signal service times.")
    r744rdsc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Delayed signal counter.")
    r744rsdt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Total signal delay times in microseconds.")
    r744rssd: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Total squares of signal times.")
    r744rsrs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Signal-redrives signal counter.")
    r744rtap_1: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5),
                                                            doc="engine 1 - Channel path type acronym. A CHPID type is provided for each active receiver/peer message path in the path group. The number of valid entries is equal to the receiver path group size.")
    r744rtap_2: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5),
                                                            doc="engine 2 - Channel path type acronym. A CHPID type is provided for each active receiver/peer message path in the path group. The number of valid entries is equal to the receiver path group size.")
    r744rtap_3: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5),
                                                            doc="engine 3 - Channel path type acronym. A CHPID type is provided for each active receiver/peer message path in the path group. The number of valid entries is equal to the receiver path group size.")
    r744rtap_4: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5),
                                                            doc="engine 4 - Channel path type acronym. A CHPID type is provided for each active receiver/peer message path in the path group. The number of valid entries is equal to the receiver path group size.")
    r744rtap_5: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5),
                                                            doc="engine 5 - Channel path type acronym. A CHPID type is provided for each active receiver/peer message path in the path group. The number of valid entries is equal to the receiver path group size.")
    r744rtap_6: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5),
                                                            doc="engine 6 - Channel path type acronym. A CHPID type is provided for each active receiver/peer message path in the path group. The number of valid entries is equal to the receiver path group size.")
    r744rtap_7: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5),
                                                            doc="engine 7 - Channel path type acronym. A CHPID type is provided for each active receiver/peer message path in the path group. The number of valid entries is equal to the receiver path group size.")
    r744rtap_8: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5),
                                                            doc="engine 8 - Channel path type acronym. A CHPID type is provided for each active receiver/peer message path in the path group. The number of valid entries is equal to the receiver path group size.")
    r744rsse: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Sum of signal service times in microseconds.")
    r744ridp_1: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                            doc="engine 1 - Channel path identifier for the receiver/peer channel path. The range of values is X'00' to X'FF'.")
    r744ridp_2: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                            doc="engine 2 - Channel path identifier for the receiver/peer channel path. The range of values is X'00' to X'FF'.")
    r744ridp_3: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                            doc="engine 3 - Channel path identifier for the receiver/peer channel path. The range of values is X'00' to X'FF'.")
    r744ridp_4: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                            doc="engine 4 - Channel path identifier for the receiver/peer channel path. The range of values is X'00' to X'FF'.")
    r744ridp_5: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                            doc="engine 5 - Channel path identifier for the receiver/peer channel path. The range of values is X'00' to X'FF'.")
    r744ridp_6: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                            doc="engine 6 - Channel path identifier for the receiver/peer channel path. The range of values is X'00' to X'FF'.")
    r744ridp_7: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                            doc="engine 7 - Channel path identifier for the receiver/peer channel path. The range of values is X'00' to X'FF'.")
    r744ridp_8: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                            doc="engine 8 - Channel path identifier for the receiver/peer channel path. The range of values is X'00' to X'FF'.")
    r744rcpi: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Index to first channel path data section associated with this remote coupling facility.")
    r744rcpn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of channel path data sections for channel paths of type CIB, CFP, CL5, CS5, or CL6 connected to this remote coupling facility (CF). This includes the receiver/peer channel paths over which signals can be sent from the subject CF to this remote CF and the sender/peer channel paths returning signals from this remote CF to the subject CF. This count matches the number of subsequent channel path data sections associated with this remote CF.")
    r744rsgs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Sender path group size.")
    r744rsap_1: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5),
                                                            doc="engine 1 - Channel path type acronym. A CHPID type is provided for each active sender/peer message path in the path group. The number")
    r744rsap_2: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5),
                                                            doc="engine 2 - Channel path type acronym. A CHPID type is provided for each active sender/peer message path in the path group. The number")
    r744rsap_3: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5),
                                                            doc="engine 3 - Channel path type acronym. A CHPID type is provided for each active sender/peer message path in the path group. The number")
    r744rsap_4: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5),
                                                            doc="engine 4 - Channel path type acronym. A CHPID type is provided for each active sender/peer message path in the path group. The number")
    r744rsap_5: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5),
                                                            doc="engine 5 - Channel path type acronym. A CHPID type is provided for each active sender/peer message path in the path group. The number")
    r744rsap_6: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5),
                                                            doc="engine 6 - Channel path type acronym. A CHPID type is provided for each active sender/peer message path in the path group. The number")
    r744rsap_7: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5),
                                                            doc="engine 7 - Channel path type acronym. A CHPID type is provided for each active sender/peer message path in the path group. The number")
    r744rsap_8: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5),
                                                            doc="engine 8 - Channel path type acronym. A CHPID type is provided for each active sender/peer message path in the path group. The number")
    r744rsid_1: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                            doc="engine 1 - Channel path identifier for sender/peer channel path. The range of values is X'00' to X'FF'.")
    r744rsid_2: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                            doc="engine 2 - Channel path identifier for sender/peer channel path. The range of values is X'00' to X'FF'.")
    r744rsid_3: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                            doc="engine 3 - Channel path identifier for sender/peer channel path. The range of values is X'00' to X'FF'.")
    r744rsid_4: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                            doc="engine 4 - Channel path identifier for sender/peer channel path. The range of values is X'00' to X'FF'.")
    r744rsid_5: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                            doc="engine 5 - Channel path identifier for sender/peer channel path. The range of values is X'00' to X'FF'.")
    r744rsid_6: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                            doc="engine 6 - Channel path identifier for sender/peer channel path. The range of values is X'00' to X'FF'.")
    r744rsid_7: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                            doc="engine 7 - Channel path identifier for sender/peer channel path. The range of values is X'00' to X'FF'.")
    r744rsid_8: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                            doc="engine 8 - Channel path identifier for sender/peer channel path. The range of values is X'00' to X'FF'.")
    r744rsc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                         doc="Number of subchannels associated with the remote CF.")
    r744ramc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of asynchronous messages that are sent to this remote CF. The count includes the number of asynchronous commands that are sent and excludes path management commands and redrives of asynchronous commands.")
    r744ramst: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                             doc="Total amount of service time for asynchronous messages sent to this remote CF, in microseconds.")
    r744ramsq: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                           doc="Total amount of squares of service time for asynchronous messages sent to this remote CF, in square of microseconds.")
    r744rampb: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Asynchronous message path busy count.")
    r744ramns: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Asynchronous message no subchannel count.")
    ndeconfigcode: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                               doc="ND associated with switch device configuration code.")
    ndetype: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="ND associated with switch device type.")
    ndemodel: so.Mapped[Optional[str]] = so.mapped_column(sa.String(3), doc="ND associated with switch device model.")
    ndemfg: so.Mapped[Optional[str]] = so.mapped_column(sa.String(3),
                                                        doc="ND associated with switch device manufacturer.")
    ndeplant: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                          doc="ND associated with switch device plant code.")
    ndesequence: so.Mapped[Optional[str]] = so.mapped_column(sa.String(12),
                                                             doc="ND associated with switch device sequence number.")
    ndecpcid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="ND associated with switch device CPC id.")


class Smf74chpa(AbstractConcreteBase):
    """Abstract class for structure Smf74chpa - Channel path data section."""

    r744hcpi: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                          doc="Channel path identifier. The range of values is X'00' to X'FF'.")
    r744htap: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="Channel path type acronym.")
    r744hopm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4),
                                                          doc="Channel path operation mode. It describes the channel path type, data rate, protocol and adapter type. Value Meaning X'01' CFP path supporting a 1.0625 Gbit/s data rate X'02' CFP path supporting a 2.125 Gbit/s data rate X'10' CIB path operating at 1x bandwidth using the IFB protocol, adapter type HCA2-O LR X'11' CIB path operating at 12x bandwidth using the IFB protocol, adapter type HCA2-O X'20' CIB path operating at 1x bandwidth using the IFB protocol, adapter type HCA3-O LR X'21' CIB path operating at 12x bandwidth using the IFB protocol, adapter type HCA3-O X'30' CIB path operating at 12x bandwidth using the IFB3 protocol, adapter type HCA3-O X'40' CS5 path operating at 8x bandwidth using the PCIe third generation protocol, adapter type PCIe-O X'50' CL5 path supporting a 10 Gbit/s data rate using the Converged Enhanced Ethernet protocol, adapter type RoCE X'51' CL6 path supporting a 25 Gbit/s data rate using the Converged Enhanced Ethernet protocol, adapter type RoCE Other Unknown")
    r744hlat: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Channel path latency time. This is the average round-trip path time in microseconds. A value of 0 means that the time was not measured. A value of 1 means a time less than or equal to one microsecond.")
    r744hpcp: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="Physical channel ID (PCHID)")
    r744haid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4),
                                                          doc="Coupling adapter identifier associated with the CHPID.")
    r744hapn: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                          doc="Number of the port associated with the CHPID.")
    r744hsap_1: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                            doc="engine 1 - I/O processor (System Assist Processor) to which this path is accessible. The range of values is X'00' to X'FF'.")
    r744hsap_2: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                            doc="engine 2 - I/O processor (System Assist Processor) to which this path is accessible. The range of values is X'00' to X'FF'.")
    r744hsap_3: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                            doc="engine 3 - I/O processor (System Assist Processor) to which this path is accessible. The range of values is X'00' to X'FF'.")
    r744hsap_4: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                            doc="engine 4 - I/O processor (System Assist Processor) to which this path is accessible. The range of values is X'00' to X'FF'.")
    r744hhca: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r744hfl1 (Bit 0) showing coupling adapter ID and port number are valid.")
    r744hmov: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r744hfl1 (Bit 1) showing channel path operation mode is valid.")
    r744hlav: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r744hfl1 (Bit 2) showing channel path latency time is valid.")
    r744hdev: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r744hfl1 (Bit 3) showing degraded status flag is valid.")
    r744hsav1: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                           doc="r744hfl1 (Bit 4) showing the corresponding field in the array of I/O processors is valid.")
    r744hsav2: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                           doc="r744hfl1 (Bit 5) showing the corresponding field in the array of I/O processors is valid.")
    r744hsav3: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                           doc="r744hfl1 (Bit 6) showing the corresponding field in the array of I/O processors is valid.")
    r744hsav4: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                           doc="r744hfl1 (Bit 7) showing the corresponding field in the array of I/O processors is valid.")
    r744hpcv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r744hfl2 (Bit 0) showing channel (CHID) is valid.")
    r744hdeg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r744hchf (Bit 0) showing channel path is operating at reduced capacity (degraded) or is not operating at the end of the interval.")
    r744hsnd: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r744hchf (Bit 1) showing channel path is a sender channel.")


class Smf74cntl(AbstractConcreteBase):
    """Abstract class for structure Smf74Cntl - Enterprise disk system statistics control data section."""

    r748clvl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Gatherer level.")
    r748ctyp: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Control unit type.")
    r748cmdl: so.Mapped[Optional[str]] = so.mapped_column(sa.String(3), doc="Control unit model.")
    r748cvsn: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4),
                                                          doc="Version of link statistics definition: X'00' = Original version of link statistics X'01' = Link statistics extended X'02' = Link statistics V2 format")
    r748cae: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                         doc="Abend code (SDWACMPC) with: First 12 bits = System completion code Second 12 bits = User completion code")
    r748crtn: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="IDCSS01 return code.")
    r748csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4),
                                                         doc="Status code: 00 successfully processed. 04 IOS return code. R748CIOC ¬= 0. 08 IDCSS01 return code. R748CRTN ¬= 0. 98")
    r748cioc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4),
                                                          doc="IOS return code. If this field is not zero, no Link Statistic sections are available.")
    r748cfdv: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Failing device.")
    r748cvol: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6),
                                                          doc="Volume serial of the device from which statistics are measured.")
    r748cdev: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6),
                                                          doc="Device number of the device from which statistics are measured.")
    r748cflg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Flags Bit Meaning when set 0 Extent pool statistics valid 1 Extent pool statistics valid 2 2 Extent pool statistics valid 3 3-7 Reserved")
    r748cscs: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                          doc="ID of the subchannel set which is physically configured to the device from which statistics are measured.")
    r748cint: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of seconds that passed since the link statistics have been collected for the last time.")
    r748cftm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(10),
                                                          doc="Time when first record was written. Reserved for duration processing.")
    r748cfdt: so.Mapped[Optional[str]] = so.mapped_column(sa.String(10),
                                                          doc="Date when first record was written. Reserved for duration processing.")
    r748cfci: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Interval length of first record. Reserved for duration processing.")
    r748cfsc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2), doc="Subchannel set ID of failing device.")
    r748cxvl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r748cflg (Bit 0) showing extent pool statistics valid.")


class Smf74connector(AbstractConcreteBase):
    """Abstract class for structure Smf74Connector - FCD connector data section."""

    r747ctfl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Port type flags. Bit Meaning when set 0 Port type is single CU. 1 Port type is multiple CU. 2 Port type is CHPID. 3 Port type is switch.")
    r747csfl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Status flags. Bit Meaning when set 0 Port type is not unique. 1 ID is not unique or not known. 2 Channel on caller's system. 3 Port installed. 4 Port status changed. 5 Port has been removed. 6 Port has been activated. 7 No measurement data available for this port.")
    r747ccun: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of connector CUs.")
    r747cscu: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r747ctfl (Bit 0) showing port type is single CU.")
    r747cmcu: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r747ctfl (Bit 1) showing port type is multiple CU.")
    r747cchp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r747ctfl (Bit 2) showing port type is CHPID.")
    r747csw: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                         doc="r747ctfl (Bit 3) showing port type is switch.")
    r747ctnu: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r747csfl (Bit 0) showing port type is not unique.")
    r747cinu: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r747csfl (Bit 1) showing ID is not unique or not known.")
    r747cosy: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r747csfl (Bit 2) showing channel on caller's system.")
    r747cins: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="r747csfl (Bit 3) showing port installed.")
    r747cvar: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r747csfl (Bit 4) showing port status changed.")
    r747crem: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r747csfl (Bit 5) showing port has been removed.")
    r747cact: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r747csfl (Bit 6) showing port has been activated.")
    r747cnmd: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r747csfl (Bit 7) showing no measurement data available for this port.")


class Smf74dctl(AbstractConcreteBase):
    """Abstract class for structure Smf74Dctl - Device control data section."""

    smf74tot: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of Device data sections in all records for this logical device class record.")
    smf74gen: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of devices specified for all classes at system installation.")
    smf74dcf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Flags for DASD class Bit Meaning when set 0 Both sections of report requested 1 Sort by storage group 2-7 Reserved.")
    smf74dms: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Message flag Bit Meaning when set 0 Message issued that SMS not available 1 SMS interface error 2-7")
    smf74enf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Flags for environment. Bit Meaning when set 0 Extended CMB 1 Model-dependent data not available by STSCH 2 Initial command response time valid (SMF74CMR) 3 Interrupt-Delay-Time facility is provided by channel subsystem")
    smf74smf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Logical SMF record flag Bit Meaning when set 0 There are more logical SMF records for this device class 1-7")
    smf74s15: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Contents of register 15 after SMS interface call, zero if normal return.")
    smf74src: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Return code from SMS interface, zero if normal return.")
    smf74srs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Reason code from SMS interface, zero if normal return.")
    smf74tsr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of small SMF records.")
    smf74cfl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Configuration change flags Bit Meaning when set 0 Configuration changed. Used to decide whether to provide the text 'POR' or 'ACTIVATE' on reports. Also used to check whether data can be combined in a duration report. 1 Configuration change since power-on-reset (POR). 2 POR using IOC data set that contains a token. 3 Configuration token is valid. 4-7 Reserved.")
    smf74tnm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(44), doc="IODF name.")
    smf74tsf: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2), doc="IODF name suffix.")
    smf74tdt: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                  doc="IODF creation date, in the form mm/dd/yy .")
    smf74mct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Maximum number of allocated tape devices. This field is zero for devices other than tape.")
    smf74tdy: so.Mapped[Optional[dt.date]] = so.mapped_column(sa.Date,
                                                              doc="IODF creation date, in the form mm / dd / yyyy .")
    smf74int: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Duration of RMF measurement interval, in the form mmsstttF where mm is the minutes, ss is the seconds, ttt is the milliseconds, and F is the sign. The end of the measurement interval is the sum of the recorded start time and this field.")
    smf74sam: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of RMF samples.")
    nrf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                     doc="smf74dcf (Bit 0) showing both sections of report requested.")
    sgf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                     doc="smf74dcf (Bit 1) showing DASD class sort by storage group.")
    _429: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                      doc="smf74dms (Bit 0) showing message issued that SMS not available.")
    sme: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="smf74dms (Bit 1) showing SMS interface error.")
    ecm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                     doc="smf74enf (Bit 0) showing environment is extended CMB.")
    sts: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                     doc="smf74enf (Bit 1) showing model-independent data not available by STSCH.")
    fcm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                     doc="smf74enf (Bit 2) showing initial command response time valid (smf73cmr).")
    fid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                     doc="smf74enf (Bit 3) showing interrupt-delay-time-facility is provided by channel subsystem.")
    config_changed: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                doc="smf74cfl (Bit 0) showing configuration changed. Used to decide whether to provide the next 'POR' or 'ACTIVATE' on reports.Also used to check whether data can be combined in a duration report.")
    config_changed_since_ipl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                          doc="smf74cfl (Bit 1) showing configuration change since power-on-reset (POR).")
    ipl_iodf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="smf74cfl (Bit 2) showing POR using IOC data set that contains a token.")
    io_token_valid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                doc="smf74cfl (Bit 3) showing configuration token is valid.")


class Smf74dev(AbstractConcreteBase):
    """Abstract class for structure Smf74Dev - Device data section."""

    smf74cnf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Device indicator Bit Meaning when set 0 No longer used. 1 No logical control unit information. 2 Data contained in fields SMF74SSC through SMF74DIS is incorrect. 3 Device has been deleted. 4 Only partial statistics are available. 5 Reserved. 6 Data recorded is incorrect because device was configured during interval. 7 Device is currently online.")
    smf74ser: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6),
                                                          doc="Volume serial of the volume mounted on this device (tape or direct access device only).")
    smf74typ: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Unit type.")
    smf74nux: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of unit control blocks (UCBs) for a parallel access volume. For HyperPAV base devices (bit 6 of SMF74CNX is set), this is the accumulated number of HyperPAV aliases.")
    smf74ssc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Start subchannel count. This is the number of physical requests to the device and includes SSCH and RSSCH instructions.")
    smf74mec: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Measurement event count (number of SSCH instructions for which connect, pending, and active times were stored).")
    smf74cnn: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Device connect time (in 128-microsecond units).")
    smf74pen: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Device pending time (in 128-microsecond units).")
    smf74atv: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Device active time (in 128-microsecond units).")
    smf74dis: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Device disconnect time (in 128-microsecond units).")
    smf74que: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of requests queued in IOS for this device.")
    smf74utl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of samples when the device was reserved but an SSCH instruction had not been issued to the device.")
    smf74rsv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of samples taken when the device was reserved.")
    smf74alc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of samples taken that indicated that the device was allocated.")
    smf74mtp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of samples taken that indicated a mount pending condition.")
    smf74nrd: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of samples taken that indicated that the device was not ready.")
    smf74cof: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of requests that had hardware timer overflow for connect time measurement.")
    smf74ict: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="No longer used.")
    smf74dvb: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Device busy delay time, from subchannel information block (SCHIB) (in 128-microsecond units).")
    smf74clf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Bit Meaning when set 0 Number option active indicator 1 Storage group option active indicator 2 Storage group name changed during the interval 3 Mount pending condition exists at the start of the interval 4 Mount pending condition exists at end of the interval 5 Reserved 6 CTC with special protocol 7 Reserved. Reserved.")
    smf74sgn: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Storage group name as defined by DFSMS.")
    smf74nda: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of allocations in effect for the device.")
    smf74dev: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="Device model name. This field is blank if device name cannot be determined.")
    smf74cu: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                         doc="Control unit name. Blank if control unit name cannot be determined.")
    smf74cnx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Reserved. Device flag extensions: Bit Meaning when set 0 Device dynamically changed 1 Device disconnect time is not valid 2 Base exposure of a parallel access volume 3 Number of alias exposures has changed 4 Timing facility not active 5 Device connect time is invalid 6 HyperPAV base device 7")
    smf74cn2: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Device flag extension 2 Bit Meaning when set 0 HyperWrite requested 1 Device in SuperPAV mode 2 Device is capable of performing synchronous I/O read requests 3 Device is capable of performing synchronous I/O write requests 4-7 Reserved.")
    smf74mtc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of tape mounts detected against the device during the interval.")
    smf74dts: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Shared Device report control flag Bit Meaning when set 0 Valid node descriptor ID retrieved 1 No valid node descriptor ID retrieved 2 Reserved 3 SMF74SHR is valid 4 Device is shared/assigned to multiple systems 5-7")
    smf74dct: so.Mapped[Optional[str]] = so.mapped_column(sa.String(28),
                                                          doc="Node descriptor ID for selfdescribing devices (if bit 0 of SMF74SRD on). 4-byte device number in EBCDIC format left justified with trailing blanks (if bit 1 of SMF74DTS is on).")
    smf74hpc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of HyperPAV aliases configured for that LSS.")
    smf74nss: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of skipped samples caused by too large delta values.")
    smf74psm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of successful PAV samples.")
    smf74pct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of unsuccessful PAV counts.")
    smf74cmr: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Command response time in units of 128 microseconds.")
    smf74cap: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="DASD volume capacity (specified by the number of available cylinders).")
    smf74idt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Interrupt delay time in units of 128 microseconds. This field is zero if not supported by the hardware.")
    smf74cuq: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Control Unit Queuing Time.")
    smf74nm2: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="Device number (same as SMF74NUM).")
    smf74atd: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of times I/Os were subjected to imposed delays due to PAV alias throttling.")
    smf74agc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="The alias management group number defined on the physical controller for this device. This number is valid if the device belongs to a DASD subsystem that supports alias management groups and bit 1 of SMF74CN2 is set.")
    smf74ags: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="The alias management group number assigned by z/OS for this device on this system. This number is valid if the device belongs to a DASD subsystem that supports alias management groups and bit 1 of SMF74CN2 is set.")
    smf74sbr: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of synchronous I/O read bytes transferred.")
    smf74sbw: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of synchronous I/O write bytes transferred.")
    smf74sqr: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of successfully completed synchronous I/O read requests.")
    smf74sqw: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of successfully completed synchronous I/O write requests.")
    smf74spr: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Processing time (in 0.5 microsecond units) for successful synchronous I/O read requests.")
    smf74spw: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Processing time (in 0.5 microsecond units) for successful synchronous I/O write requests.")
    smf74sftr: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                             doc="Elapsed time (in 0.5 microsecond units) for unsuccessful synchronous I/O read requests.")
    smf74sftw: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                             doc="Elapsed time (in 0.5 microsecond units) for unsuccessful synchronous I/O write requests.")
    smf74slbr: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                             doc="Number of synchronous I/O read link busy conditions.")
    smf74slbw: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                             doc="Number of synchronous I/O write link busy conditions.")
    smf74scmr: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                             doc="Number of cache miss conditions for synchronous I/O read requests.")
    smf74snis: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                             doc="Number of synchronous I/O write requests where the write data could not be immediately stored.")
    smf74stor: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                             doc="Number of synchronous I/O read timeout conditions.")
    smf74stow: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                             doc="Number of synchronous I/O write timeout conditions.")
    smf74sor: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of synchronous I/O read requests rejected for reasons other than link busy, read cache miss or timeout conditions.")
    smf74sow: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of synchronous I/O write requests rejected for reasons other than link busy, timeout or deferred write conditions.")
    smf74ios: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="IOS Queue time in microseconds")
    smf74int: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Duration of RMF measurement interval, in the form mmsstttF where mm is the minutes, ss is the seconds, ttt is the milliseconds, and F is the sign. The end of the measurement interval is the sum of the recorded start time and this field.")
    smf74sam: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of RMF samples.")
    lcd: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                     doc="smf74cnf (Bit 1) showing no logical control unit information.")
    cmb: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                     doc="smf74cnf (Bit 2) showing data contained in fields smf74ssc through smf73dis is incorrect.")
    del_: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                      doc="smf74cnf (Bit 3) showing device has been deleted.")
    par: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                     doc="smf74cnf (Bit 4) showing only partial statistics are available.")
    vac: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                     doc="smf74cnf (Bit 6) showing data recorded is incorrect because device was configured during interval.")
    sta: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                     doc="smf74cnf (Bit 7) showing device is currently online.")
    rnr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                     doc="smf74clf (Bit 0) showing number option active indicator.")
    rsg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                     doc="smf74clf (Bit 1) showing storage group option active indicator.")
    rcs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                     doc="smf74clf (Bit 2) showing storage group name changed duirng the interval.")
    mts: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                     doc="smf74clf (Bit 3) showing mount pending condition exists at the start of the interval.")
    mte: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                     doc="smf74clf (Bit 4) showing mount pending condiiton exists at tned of the interval.")
    ctw: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                     doc="smf74clf (Bit 6) showing CTC with special protocol.")
    dyc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                     doc="smf74cnx (Bit 0) showing device dynamically changed.")
    ddt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                     doc="smf74cnx (Bit 1) showing device disconnect time is not valid.")
    pav: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                     doc="smf74cnx (Bit 2) showing base exposure of a parallel access volume.")
    nxc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                     doc="smf74cnx (Bit 3) showing number of alias exposures has changed.")
    ntf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                     doc="smf74cnx (Bit 4) showing timing facility not active.")
    cni: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                     doc="smf74cnx (Bit 5) showing device connect time is invalid.")
    hpv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="smf74cnx (Bit 6) showing HyperPAV base device.")
    cfc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                     doc="smf74cnx (Bit 7) showing device connnected to FICON.")
    hwr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="smf74cn2 (Bit 0) showing HperWrite requested.")
    xpv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                     doc="smf74cn2 (Bit 1) showing device in SuperPAV mode.")
    sir: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                     doc="smf74cn2 (Bit 2) showing device is capable of performing synchronous I/O read requests.")
    siw: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                     doc="smf74cn2 (Bit 3) showing device is capable of performing synchronous I/O write requests.")
    srd: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                     doc="smf74dts (Bit 0) showing valid node descriptor ID retrieved.")
    snd: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                     doc="smf74dts (Bit 1) showing no valid node descriptor ID retrieved.")
    shv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="smf74dts (Bit 3) showing smf74shr is valid.")
    shr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                     doc="smf74dts (Bit 4) showing device is shared/assigned to multiple systems.")
    smf74dct_hex2: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4),
                                                               doc="4 byte device number in EBCDIC format left justified with trailing blanks (if bit 1 of smf74dts is on).")
    sync_device_read_activity_rate: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                  doc="the rate of successfully completed synchronous I/O read requests.")
    sync_device_write_activity_rate: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                   doc="the rate of synchronous I/O write requests which completed successfully during the interval.")
    sync_avg_read_resp_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                           doc="the average processing time per successful synchronous I/O read request.")
    sync_avg_write_resp_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                            doc="the average processing time per successful synchronous I/O write request.")
    sync_read_xfer_rate: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                       doc="the number of megabytes per second read during synchronous I/O processing on the device.")
    sync_write_xfer_rate: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                        doc="the number of megabytes per second written during synchronous I/O processing on the device.")
    sync_req_success: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="percentage of synchronous I/O requests that completed successfully.")
    sync_link_busy: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                  doc="percentage of synchronous I/O requests that hit a link busy condition when trying to use a synchronous I/O link.")
    sync_cache_miss: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                   doc="percentage of synchronous I/O read requests that hit a cache miss condition.")
    sync_timeout: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="the total number of synchronous I/O read and write timeout conditions.")
    sync_rej_read: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="the percentage of synchronous I/O read requests that were rejected for reasons other than a link busy condition or a read cache miss.")
    sync_rej_write: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                  doc="the percentage of synchronouos I/O write requests that were rejected for reasons other than a link busy condiiton.")
    sync_total_req: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                  doc="total number of synchronous I/O requests.")
    device_activity_rate: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                        doc="the number of physical requests to the device rate during the interval.")
    avg_resp_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="the average response time the device required to complete the asynchronous I/O request.")
    avg_iosq_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="the time an I/O request must wait on an IOS queue before a SSCH instruction can be issued.")
    avg_cmr_dly: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                               doc="the average delay time that a successfully inititated start or resume function needs until the first command is indicated as accepted by the device. It allows to distinguish between real H/W errors versus workload spikes (contention in the fabric and at the destination port).")
    avg_db_dly: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="the average delay time that I/O requests to this device encountered because the device was busy. Device busy might mean another system is using the volume, another system reserved the device, head of string busy conditions caused contention or some combination of these three conditions has occurred.")
    avg_int_dly: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                               doc="the average interrupt delay time encountered for I/O requests to this device. For each I/O request, the time is measured from when the I/O operation is complete to when the operating system begins to process the status.")
    avg_pend_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="the average time an I/O request must wait in the hardware. This value reflects the time between acceptance of the SSCH function by the channel subsystem (SSCH-function pending) and acceptance of the first command associated with the SSCH function at the device (subchannel active). This value also includes the time waiting for an available channel path and control unit as well as the delya due to shared DASD condition.")
    avg_disc_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="the average time the device was disconnected while processing an SSCH instruction. This value reflects the time when the device was in use but not transferring data. It includes the overhead time when a device might disconnect to perform positioning functions such as SEEK/SET SECTOR, as well as any reconnection delay.")
    avg_conn_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="the average time the device was connected to a channel path and actually transferring data between the device and central storage. Typically, this value, measures data transfer time but also includes the search time needed to maintain channel path, control unit, and device connection.")
    dev_conn_percent: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="the percentage of time during the interval when the device was connected to a channel path.")
    dev_util_percent: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="the percentage of time during the interval when the device was in use. This percentage includes both the time when the device was involved in I/O operations (connect and disconnect time) and the time when it was reserved but not involeved in an I/O operation.")
    dev_resv_percent: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="the percentage of time during the interval when a shared device was reserved by the procesor on which RMF was started. At each RMF cycle, RMF checks to see if a device is reserved, and a counter is kept of all such samples. At the end of the interval, the percentage is computed.")
    avg_numbr_alloc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                   doc="the average number of data control blocks (DCBs) and access method control blocks (ACBs) concurrently allocated for each volume. This field is reported only for direct access storage devices.")
    any_alloc_percent: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                     doc="the percentage of time during the reporting interval when the device was allocated to one or more data sets. Permanently mounted direct access devices show a 100% allocation, regardless of whether a data set was actually allocated.")
    mt_pend_percent: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                   doc="the percentage ot time during the interval when a mount was pending for the device. This field is reported only for direct access devices and magnetic tape devices.")
    not_ready_percent: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                     doc="the percentage of time during the reporting interval when the device was not ready for use. For example, when a tape has just been mounted but is not yet ready to be used to the system. This field is not reported for direct access devices.")
    num_of_mts: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                            doc="the number of tape mounts, shown as an integer value, detected by RMF.")
    avg_mt_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                               doc="the average mount time pending for every device. If the mount count or the sample count is zero, the result is zero.")
    time_dev_alloc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                  doc="the total time the device as allocated during the interval. If the sample count is zero, the result is zero.")


class Smf74eadm(AbstractConcreteBase):
    """Abstract class for structure Smf74Eadm - Extended Asynchronous Data Mover (EADM) device (subChannel) information section."""

    r7410dsct: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="SSCH count across all devices.")
    r7410dnum: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                           doc="Number of updates to the time accumulation fields.")
    r7410dfpt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                             doc="Sum of function pending times across all devices in units of 128 microseconds. The time lapse between the SSCH being issued and the acceptance of the first command of the channel program at the device.")
    r7410diqt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                             doc="Sum of IOP queue times across all devices in units of 128 microseconds. The amount of time the request is not accepted at the SCM resource because it would exceed its maximum capacity.")
    r7410dcrt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                             doc="Sum of initial command response times across all devices in units of 128 microseconds. The time from when the first command does not immediately proceed to execute until the successful start of execution at the SCM resource part.")
    r7410dflg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                           doc="Device information flags. Bit Meaning when set 0 EADM compression facility is available. 1 - 7 Reserved.")
    r7410docc: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Number of compression operations.")
    r7410docd: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Number of decompression operations.")
    r7410disc: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                           doc="Number of 1 MB input blocks consumed for compression.")
    r7410dosc: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                           doc="Number of 1 MB output blocks consumed for compression.")
    r7410disd: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                           doc="Number of 1 MB input blocks consumed for decompression.")
    r7410dosd: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                           doc="Number of 1 MB output blocks consumed for decompression.")
    smf74int: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Duration of RMF measurement interval, in the form mmsstttF where mm is the minutes, ss is the seconds, ttt is the milliseconds, and F is the sign. The end of the measurement interval is the sum of the recorded start time and this field.")
    r7410ecpr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                           doc="r7410dflg (Bit 0) showing EADM compresssion facility is available.")


class Smf74extp(AbstractConcreteBase):
    """Abstract class for structure Smf74Extp - Extent pool statistics section."""

    r748xplt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Extent type: Value Meaning 0-3 Reserved 4 FIBER 1Gb 5-131 Reserved 132 CKD 1Gb 133-255 Reserved.")
    r748xptq: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Extent pool type qualifier: Bit Meaning when set 0 Data encrypted extent pool 1 Compression extent pool 2-6 Reserved 7")
    r748xrcp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Real extent pool capacity in GB.")
    r748xrns: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of real extents in extent pool.")
    r748xrna: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of allocated real extents in extent pool.")
    r748xrsc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Real extent conversions. Valid if bit 0 of R748CFLG is set.")
    r748xvcp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Virtual extent pool capacity in GB. Valid if bit 0 of R748CFLG is set.")
    r748xvns: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of virtual extents in extent pool. Valid if bit 0 of R748CFLG is set.")
    r748xvsc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Virtual extent conversions. Valid if bit 0 of R748CFLG is set.")
    r748xsdy: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of extents that were sources of dynamic extent relocations. Valid if bit 0 of R748CFLG is set.")
    r748xtdy: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of extents that were targets of dynamic extent relocations. Valid if bit 0 of R748CFLG is set.")
    r748xeps: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Extent sizes in extent pool. Valid if bit 7 of R748XPTQ is set. Value Description 0 Reserved 1 1 GB extents (CKD 1113 cylinders) 2-6 Reserved")
    r748xtpc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total physical capacity (in units as defined in R748XEPS). Valid if bit 2 of R748CFLG is set.")
    r748xupc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Used physical capacity (in units as defined in R748XEPS). Valid if bit 2 of R748CFLG is set.")
    r748xtlc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total logical capacity (in units as defined in R748XEPS). Valid if bit 2 of R748CFLG is set.")
    r748xulc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Used logical capacity (in units as defined in R748XEPS). Valid if bit 2 of R748CFLG is set.")
    encrypted_extent_pool: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                       doc="r748xptq (Bit 0) showing data encrypted extent pool.")
    compression_extent_pool: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                         doc="r748xptq (Bit 1) showing compression extent pool.")
    extent_sizes_valid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                    doc="r748xptq (Bit 1) showing compression extent pool.")


class Smf74fcd(AbstractConcreteBase):
    """Abstract class for structure Smf74Fcd - FCD global data section."""

    r747gcfl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Configuration change flags. Bit Meaning when set 0 Configuration changed during interval. 1 Configuration changed since IPL. 2 System IPLed by way of IODF. 3 I/O configuration token is valid. 4-7 Reserved.")
    r747gnfd: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of installed FCD switches.")
    r747ginm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(44), doc="IODF name.")
    r747gisf: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2), doc="Suffix of IODF name.")
    r747gict: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="IODF creation time (hh.mm.ss).")
    r747gdca: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r747gcfl (Bit 0) showing configuration changed during interval.")
    r747giac: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r747gcfl (Bit 1) showing configuration changed since IPL.")
    r747giod: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r747gcfl (Bit 2) showing system IPLed by way of IODF.")
    r747gicv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r747gcfl (Bit 3) showing I/O configuration token is valid.")


class Smf74fsys(AbstractConcreteBase):
    """Abstract class for structure Smf74Fsys - HFS file system section."""

    r746fsnl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Length of file system name.")
    r746fsfl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Status flags. Bit Meaning when set 0 No HFS file system statistics. 1 Mount time changed. 2 File system now mounted. 3-7 Reserved.")
    r746fmtm: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Mount time stamp.")
    r746fsf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Size of file system (in pages).")
    r746fpf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of pages internally used by HFS.")
    r746fpd: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                         doc="Number of pages used for the attribute directory.")
    r746fpc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                         doc="Number of data buffer pages cached by this file system.")
    r746fsfi: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of sequential file data I/O requests issued.")
    r746frfi: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of random file data I/O requests issued.")
    r746fmc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="Number of times the metadata for a file was found in virtual storage (cache) during file lookup.")
    r746fmnc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of times the metadata for a file was not found in virtual storage (cache) during file lookup and an index call was necessary which may result in an I/O.")
    r746f1c: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="Number of times the first page of a data file was requested and found in virtual storage (cache).")
    r746f1nc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of times the first page of a data file was requested and not found in virtual storage (cache) and an I/O was necessary.")
    r746fint: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Number of index new tops.")
    r746fis: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Number of index splits.")
    r746fij: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Number of index joins.")
    r746firh: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Number of index page read hits.")
    r746firm: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Number of index page read misses.")
    r746fiwh: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Number of index page write hits.")
    r746fiwm: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Number of index page write misses.")
    r746fsrc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Return code from OMVS BPX1PCT for DisplayFSStats command.")
    r746fsrs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Reason code from OMVS BPX1PCT for DisplayFSStats command.")
    r746fnhs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r746fsfl (Bit 0) showing no HFS file system statistics.")
    r746fmtc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r746fsfl (Bit 1) showing mount time changed.")
    r746ffsm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r746fsfl (Bit 2) showing file system now mounted.")


class Smf74gbuf(AbstractConcreteBase):
    """Abstract class for structure Smf74Gbuf - HFS global buffer section."""

    r746gsb: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Size of buffers in buffer pool (in pages).")
    r746gnds: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of data spaces for buffer pool.")
    r746gsbp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Size of buffer pool (in pages).")
    r746gsbf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Size of permanently fixed buffers in buffer pool (in pages).")
    r746gbf: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="Number of times a buffer was already fixed prior to an I/O request in buffer pool.")
    r746gbnf: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of times a buffer was not already fixed prior to an I/O request in buffer pool.")


class Smf74hfs(AbstractConcreteBase):
    """Abstract class for structure Smf74Hfs - HFS global data section."""

    r746gmxv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Value of VIRTUAL(MAX) (in MB).")
    r746gusv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total amount (in pages) of virtual storage in use.")
    r746gmnf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Value of FIXED(MIN) (in MB).")
    r746gusf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total amount (in pages ) of permanently fixed storage in use.")
    r746gmc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="Number of times the metadata for a file was found in virtual storage (cache) during file lookup.")
    r746gmnc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of times the metadata for a file was not found in virtual storage (cache) during file lookup and an index call was necessary which may result in an I/O.")
    r746g1c: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="Number of times the first page of a data file was requested and found in virtual storage (cache).")
    r746g1nc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of times the first page of a data file was requested and not found in virtual storage (cache) and an I/O was necessary.")
    r746glrc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="Return code from OMVS BPX1PCT for DisplayBufferLimits command.")
    r746glrs: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="Reason code from OMVS BPX1PCT for DisplayBufferLimits command.")
    r746gsrc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="Return code from OMVS BPX1PCT for DisplayGlobalStats command.")
    r746gsrs: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="Reason code from OMVS BPX1PCT for DisplayGlobalStats command.")
    r746gsfl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Status flags. Bit Meaning when set 0 OMVS kernel not ready 1 No buffer limit data 2 No global data 3 Partial global data 4-7 Reserved.")
    r746gonr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r746gsfl (Bit 0) showing OMVS kernel not ready.")
    r746gnbl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r746gsfl (Bit 1) showing no buffer limit data.")
    r746gngd: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="r746gsfl (Bit 2) showing no global data.")
    r746gpgd: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r746gsfl (Bit 3) showing partial global data.")


class Smf74hwa(AbstractConcreteBase):
    """Abstract class for structure Smf74hwa - Hardware accelerator data Section."""

    r749ftyp: so.Mapped[Optional[str]] = so.mapped_column(sa.String(10), doc="Hardware accelerator application type.")
    r749fdsc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(32),
                                                          doc="Hardware accelerator application description.")
    r749frqc: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Total number of hardware accelerator requests that completed successfully.")
    r749frqe: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Total number of hardware accelerator requests that completed with an error. Statistics for these requests are not included in the other fields of this data section.")
    r749fqfl: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Number of times that the adapter queue was full when a new request was submitted.")
    r749ftet: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total execution time of all requests in microseconds.")
    r749fsqe: so.Mapped[Optional[str]] = so.mapped_column(sa.String(34),
                                                          doc="Sum of the squares of the individual execution times.")
    r749ftqt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total queue time of all requests in microseconds.")
    r749fsqq: so.Mapped[Optional[str]] = so.mapped_column(sa.String(34),
                                                          doc="Sum of the squares of the individual queue times.")
    r749fdrd: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Total DMA reads in units of 256 bytes.")
    r749fdwr: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Total DMA writes in units of 256 bytes.")
    stdd_ftet: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="the standard deviation of r749ftet.")
    stdd_ftqt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="the standard deviation of r749ftqt.")


class Smf74hwa1(AbstractConcreteBase):
    """Abstract class for structure Smf74hwa1 - Hardware accelerator compression data Section."""

    r7491dib: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Total number of deflate input bytes.")
    r7491dis: so.Mapped[Optional[str]] = so.mapped_column(sa.String(34),
                                                          doc="Sum of the squares of the individual deflate input bytes.")
    r7491dob: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Total number of deflate output bytes.")
    r7491dos: so.Mapped[Optional[str]] = so.mapped_column(sa.String(34),
                                                          doc="Sum of the squares of the individual deflate output bytes.")
    r7491dct: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Total number of deflate requests.")
    r7491iib: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Total number of inflate input bytes.")
    r7491iis: so.Mapped[Optional[str]] = so.mapped_column(sa.String(34),
                                                          doc="Sum of the squares of the individual inflate input bytes.")
    r7491iob: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Total number of inflate output bytes.")
    r7491ios: so.Mapped[Optional[str]] = so.mapped_column(sa.String(34),
                                                          doc="Sum of the squares of the individual inflate output bytes.")
    r7491ict: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Total number of inflate requests.")
    r7491bps: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Total size of memory in megabytes allocated to the buffer pool.")
    r7491bpc: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Accumulated size of memory in megabytes for in-use buffers.")
    stdd_1dib: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="the standard deviation of r7491dib.")
    stdd_1dob: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="the standard deviation of r7491dob.")
    stdd_1iib: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="the standard deviation of r7491iib.")
    stdd_1iob: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="the standard deviation of r7491iob.")


class Smf74lss(AbstractConcreteBase):
    """Abstract class for structure Smf74Lss - Link statistics section."""

    r748ltyp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Link type: 1 ESCON 2 Fibre Channel 1 Gbit/s 3 Fibre Channel 2 Gbit/s 4 Fibre Channel 4 Gbit/s 5 Fibre Channel 8 Gbit/s 6 Fibre Channel 16 Gbit/s 7 Fibre Channel 32 Gbit/s 10 Ethernet Channel 10 Gbit/s 11 Ethernet Channel 40 Gbit/s")
    r748lflg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Flags. Bit Meaning when set 0 Units of bytes indeterminable. Byte values incorrect. 1")
    r748lerb: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="ECKD read activity in units of 128KB.")
    r748lewb: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="ECKD write activity in units of 128KB.")
    r748lero: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of ECKD read operations. For ESCON ports, one count is added per chain which transfers customer data (no administration data) to the host. For FICON ports, one count is added per command which transfers customer data to the host.")
    r748lewo: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of ECKD write operations. For ESCON ports, one count is added per chain which transfers customer data (no administration data) from the host. For FICON ports, one count is added per command which transfers customer data from the host.")
    r748lert: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Accumulated time for ECKD read activity on the channel in milliseconds. The active processing time for each command is accumulated.")
    r748lewt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Accumulated time for ECKD write activity on the channel in milliseconds. The active processing time for each command is accumulated.")
    r748lpsb: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="PPRC send activity in units of 128KB.")
    r748lprb: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="PPRC received activity in units of 128KB.")
    r748lpso: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="PPRC send operations. Each PPRC write command sent by the PPRC primary is counted.")
    r748lpro: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="PPRC received operations. Each PPRC write command received by the PPRC secondary is counted.")
    r748lpst: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Accumulated time for PPRC send activity in milliseconds.")
    r748lprt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Accumulated time for PPRC received activity in milliseconds.")
    r748lsrb: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="SCSI read activity in units of 128KB.")
    r748lswb: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="SCSI write activity in units of 128KB.")
    r748lsro: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="SCSI read operations. Each read operation is counted.")
    r748lswo: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="SCSI write operations. Each write operation is counted.")
    r748lsrt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Accumulated time for SCSI read operations on the channel in milliseconds.")
    r748lswt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Accumulated time for SCSI write operations on the channel in milliseconds.")
    r748lflf: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Fibre channel link failures. Number of times the port lost meaningful communication on the link. This can cause I/O failures.")
    r748lfly: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Fibre channel synchronization failures. Number of times the fibre channel signal lost synchronization.")
    r748lfls: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Fibre channel signal failures. Number of times the fibre channel signal was lost.")
    r748lfpq: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of fibre channel primitive sequence errors. Such errors can occur during loss of synchronization, loss of signal, or during a link failure.")
    r748lfit: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Fibre channel invalid transmission word errors. Number of bit errors, which can lead to a loss of synchronization and/or to lost fibre channel traffic.")
    r748lfcr: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Fibre channel Cyclic Redundancy Check (CRC) errors. Number of fibre channel frames lost due to CRC errors. This causes an I/O abort or timeout.")
    r748lfr1: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Fibre channel link recovery (LR) sent. Number of times the ESS port reset the link due to a timeout on fibre channel buffer-to-buffer credit to send a frame. Such errors can cause timeouts or aborts or queued I/O frames to be lost.")
    r748lfr2: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Fibre channel link recovery (LR) received. Number of times the attached port reset the link due to a timeout on fibre channel buffer- to-buffer credit to send a frame. Such errors can cause timeouts or aborts or queued I/O frames to be lost.")
    r748lfif: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Fibre channel illegal frame errors. Number of frames that violated the Fibre channel protocol. The most common cause is a missing frame. Another example is an invalid frame header. Illegal frames will cause I/O aborts or timeouts.")
    r748lfod: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Fibre channel out of order data errors. Number of times that an out of order frame is detected. The most common cause is a missing frame. Such errors will cause I/O aborts or timeouts.")
    r748lfoa: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Fibre channel out of order ACK errors. Number of ACK frames identified as out of order. The most common cause is a missing frame. Such errors are not expected during I/O, since I/O does not use ACK.")
    r748lfdf: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Fibre channel duplicate frame errors. Number of times a duplicate frame was received. Such errors will cause I/O aborts or timeouts.")
    r748lfio: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Fibre channel invalid relative offset failures. Number of frames that were received with an invalid relative offset field in the frame header. Such errors will cause I/O aborts or timeouts.")
    r748lftc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Fibre channel sequence timeout errors. Number of times the ESS port has detected a timeout on a receiving sequence initiative for a fibre channel exchange.")
    r748lfbc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Fibre channel bit error rate. A non-zero rate means that bit errors have occurred on the link within the last five minutes. This is not an accumulated error rate, but a snapshot of the last five minute interval.")
    r748lbyt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r748lflg (Bit 0) showing units of bytes indeterminable. Byte values incorrect.")
    r748ltim: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r748lflg (Bit 1) showing units of time indeterminable. Time values incorrect.")


class Smf74mbr(AbstractConcreteBase):
    """Abstract class for structure Smf74Mbr - Member data section."""

    r742mstf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Status flags Bit Meaning when set 0 Member became active during this interval 1 Member became inactive during this interval 2 Counts reset by XCF during this interval 3 Partially not active during RMF Postprocessor interval. 4 No information returned from IXCQUERY. 5-7")
    r742mst1: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Extended member state (1): 2=CREATED 3=ACTIVE 4=QUIESCED 5=FAILED")
    r742mst2: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Extended member state (2): Bit Meaning when set 0 System status update missing 1 System termination started 2 Reserved 3 Status update missing (confirmed) 4 Status update missing (not confirmed) 5 Reserved 6 Monitoring has been removed 7")
    r742msnt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of signals sent by member.")
    r742mrcv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of signals received by member.")
    r742mint: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Status checking interval.")
    r742mjob: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Job name that joined the member.")
    r742mact: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r743mstf (Bit 0) showing member became active during this interval.")
    r742miac: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r743mstf (Bit 1) showing member became inactive during this interval.")
    r742mres: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r743mstf (Bit 2) showing counts reset by XCF during this interval.")
    r742mpar: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r743mstf (Bit 3) showing partially not active during RMF Postprocessor interval.")
    r742mnoq: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r743mstf (Bit 4) showing no information returned from IXCQUERY.")
    r742mssm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r743mst2 (Bit 0) showing system status update missing.")
    r742mtrm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r743mst2 (Bit 1) showing system termination started.")
    r742mmsm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r743mst2 (Bit 3) showing status update missing (confirmed).")
    r742mmsd: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r743mst2 (Bit 4) showing status update missing (not confirmed).")
    r742mrem: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r743mst2 (Bit 6) showing monitoring has been removed.")


class Smf74mscm(AbstractConcreteBase):
    """Abstract class for structure Smf74Mscm - Storage Class Memory data section."""

    r744msma: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Maximum amount of storage class memory the structure can use (4K-block units).")
    r744malg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="SCM algorithm type.")
    r744mfau: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Fixed augmented space (4K-block units).")
    r744miua: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Amount of augmented space that is in use by this structure (4K- block units).")
    r744mius: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Amount of storage class memory that is in use by this structure (4K-block units).")
    r744mema: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Estimated maximum amount of space that may be assigned as augmented space for this structure (4K-block units).")
    r744meml: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Estimated maximum number of list entries that may reside in storage class memory for this structure.")
    r744meme: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Estimated maximum number of list elements that may reside in storage class memory for this structure.")
    r744menl: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Number of existing structure list entries that reside in storage class memory for this structure.")
    r744mene: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Number of existing structure list elements that reside in storage class memory for this structure.")
    r744mslt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Percentage of the list entry and list element counts that determines the lower threshold for migration from storage class memory to CF storage.")
    r744msut: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Percentage of the list entry and list element counts that determines the upper threshold for migration from CF storage to storage class memory.")
    r744mslr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Percentage of the list entry and list element counts that determines the lower threshold regulator for migration from CF storage class memory to CF real storage.The lower threshold regulators are used to stop migration from CF SCM into CF real storage after being triggered by the lower threshold.")
    r744msur: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Percentage of the list entry and list element counts that determines the upper threshold regulator for migration from CF real storage to CF storage class memory. The upper threshold regulators are used to stop migration from CF real storage into CF SCM after being triggered by the upper threshold.")
    r744mswc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="SCM write count. The number of list write operations performed to storage class memory.")
    r744mrfc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="The number of read operations against storage class memory that were initiated by a reference to list structure objects residing in storage class memory.")
    r744mrpc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="The number of read operations against storage class memory that were initiated as a prefetch operation in order to retrieve list structure objects in storage class memory that are expected to be referenced.")
    r744mrst: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total amount of service times for read operations from storage class memory in microseconds.")
    r744mrsq: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Total amount of squares of service times for read operations from storage class memory in square-microseconds.")
    r744mwst: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total amount of service times for write operations to storage class memory in microseconds.")
    r744mwsq: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Total amount of squares of service times for write operations to storage class memory in square-microseconds.")
    r744mrbt: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="SCM read bytes transferred. This is the number of bytes in 4K units transferred from storage class memory to CF storage.")
    r744mwbt: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="SCM write bytes transferred. This is the number of bytes in 4K units transferred from CF storage to storage class memory.")
    r744maec: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="SCM auxiliary enabled command count. This is the number of commands that required the use of CF auxiliary frames.")
    r744msrl: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="The number of references against storage class memory to locate list structure objects.")
    r744msrr: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="The number of references against storage class memory to resolve list entry key hashing.")
    r744msrm: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="The number of references against storage class memory for the purpose of migrating list structure objects from CF storage to storage class memory to allow the creation of new list structure objects in CF storage.")
    r744mmbl: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="The maximum number of list entries that can be stored in a single storage class memory buffer.")
    r744mmbe: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="The maximum number of list elements that can be stored in a single storage class memory buffer.")
    r744mnel: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="The minimum number of list elements that must be available for assignment after the specified allocation process completes.")
    r744mnec: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="The minimum number of list entries that must be available for assignment after the specified allocation process completes.")
    r744msrk: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="The number of references against storage class memory for the purpose of migrating list structure objects from storage class memory to CF storage to allow for key-range initialization to complete.")


class Smf74omvs(AbstractConcreteBase):
    """Abstract class for structure Smf74Omvs - OMVS control data section."""

    r743cycu: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="The number of cycle units elapsed between first and last measured sample.")
    r743cyct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="The cycle time value obtained from Monitor III options (in milliseconds).")
    r743flg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                         doc="Processing Flags Bit Meaning when set 0 Kernel address space is terminated or reinstated this interval. 1 Maximum number of processes changed during reporting interval. 2 Maximum number of users changed during reporting interval. 3 Maximum number of processes per user changed during reporting interval. 4 Maximum number of message queue ids changed during reporting interval when set. 5 Maximum number of semaphore ids changed during reporting interval when set. 6 Maximum number of shared memory ids changed during reporting interval when set. 7 Maximum number of shared memory pages changed during reporting interval when set. 8 Maximum number of memory map storage pages changed during reporting interval when set. 9 Maximum number of shared storage pages changed during reporting interval when set. 10 Maximum size of shared library region changed during reporting interval when set. 11 Maximum number of queued signals per process changed during reporting interval when set. 12-31")
    r743sysc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="The total number of kernel callable services invoked during the interval.")
    r743scmn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="The minimum number of kernel callable services invoked during one cycle.")
    r743scmx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="The maximum number of kernel callable services invoked during one cycle.")
    r743cpu: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="Total CPU time spent processing callable services in the kernel address space during the interval (in 10-millisecond units).")
    r743ctmn: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Minimum CPU time spent processing callable services in the kernel address space during one cycle (in 10-millisecond units).")
    r743ctmx: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Maximum CPU time spent processing callable services in the kernel address space during one cycle (in 10-millisecond units).")
    r743opr: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="Count of times fork() or dub failed because the maximum number of processes was exceeded during the interval.")
    r743opmn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Minimum number of times fork() or dub failed because the maximum number of processes was exceeded during one cycle.")
    r743opmx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Maximum number of times fork() or dub failed because the maximum number of processes was exceeded during one cycle.")
    r743ous: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="Count of times fork() or dub failed because the maximum number of users was exceeded during the interval.")
    r743oumn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Minimum number of times fork() or dub failed because the maximum number of users was exceeded during one cycle.")
    r743oumx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Maximum number of times fork() or dub failed because the maximum number of users was exceeded during one cycle.")
    r743opru: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Count of times fork() or dub failed because the maximum number of processes per user was exceeded during the interval.")
    r743ormn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Minimum number of times fork() or dub failed because the maximum number of processes per user was exceeded during one cycle.")
    r743ormx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Maximum number of times fork() or dub failed because the maximum number of processes per user was exceeded during one cycle.")
    r743maxp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Maximum number of processes.")
    r743maxu: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Maximum number of users.")
    r743mxpu: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Maximum number of processes per user.")
    r743curp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Accumulated number of processes during the interval.")
    r743cpmn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Minimum number of processes during one cycle.")
    r743cpmx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Maximum number of processes during one cycle.")
    r743curu: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Accumulated number of users during the interval.")
    r743cumn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Minimum number of users during one cycle.")
    r743cumx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Maximum number of users during one cycle.")
    r743mmsg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Maximum number of message queue IDs (constant).")
    r743msem: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Maximum number of semaphore IDs (constant).")
    r743mshm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Maximum number of shared memory IDs (constant).")
    r743mspg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Maximum number of shared memory pages (constant).")
    r743cmsg: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Accumulated number of message queue IDs during one interval.")
    r743cmmn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Minimum number of message queue IDs per cycle.")
    r743cmmx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Maximum number of message queue IDs per cycle.")
    r743csem: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Accumulated number of semaphore IDs during one interval.")
    r743csmn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Minimum number of semaphore IDs per cycle.")
    r743csmx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Maximum number of semaphore IDs per cycle.")
    r743cshm: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Accumulated number of shared memory IDs during one interval.")
    r743chmn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Minimum number of shared memory IDs per cycle.")
    r743chmx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Maximum number of shared memory IDs per cycle.")
    r743cspg: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Accumulated number of shared memory pages during one interval.")
    r743cgmn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Minimum number of shared memory pages per cycle.")
    r743cgmx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Maximum number of shared memory pages per cycle.")
    r743omsg: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Accumulated number of attempts to exceed maximum number of message queue IDs during one interval.")
    r743ommn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Minimum number of attempts to exceed maximum number of message queue IDs per cycle.")
    r743ommx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Maximum number of attempts to exceed maximum number of message queue IDs per cycle.")
    r743osem: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Accumulated number of attempts to exceed maximum number of semaphore IDs during one interval.")
    r743osmn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Minimum number of attempts to exceed maximum number of semaphore IDs per cycle.")
    r743osmx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Maximum number of attempts to exceed maximum number of semaphore IDs per cycle.")
    r743oshm: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Accumulated number of attempts to exceed maximum number of shared memory IDs during one interval.")
    r743ohmn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Minimum number of attempts to exceed maximum number of shared memory IDs per cycle.")
    r743ohmx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Maximum number of attempts to exceed maximum number of shared memory IDs per cycle.")
    r743ospg: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Accumulated number of attempts to exceed maximum number of shared memory pages during one interval.")
    r743ogmn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Minimum number of attempts to exceed maximum number of shared memory pages per cycle.")
    r743ogmx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Maximum number of attempts to exceed maximum number of shared memory pages per cycle.")
    r743mmap: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Maximum number of memory map storage pages (constant).")
    r743cmap: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Accumulated number of memory map storage pages during one interval.")
    r743camn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Minimum number of memory map storage pages per cycle.")
    r743camx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Maximum number of memory map storage pages per cycle.")
    r743omap: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Accumulated number of attempts to exceed maximum number of memory map storage pages during one interval.")
    r743oamn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Minimum number of attempts to exceed maximum number of memory map storage pages per cycle.")
    r743oamx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Maximum number of attempts to exceed maximum number of memory map storage pages per cycle.")
    r743mpag: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Maximum number of shared storage pages (constant).")
    r743cpag: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Accumulated number of shared storage pages during one interval.")
    r743cxmn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Minimum number of shared storage pages per cycle.")
    r743cxmx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Maximum number of shared storage pages per cycle.")
    r743opag: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Accumulated number of attempts to exceed maximum number of shared storage pages during one interval.")
    r743oxmn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Minimum number of attempts to exceed maximum number of shared storage pages per cycle.")
    r743oxmx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Maximum number of attempts to exceed maximum number of shared storage pages per cycle.")
    r743mslr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Maximum amount of storage (MB) available for shared library region.")
    r743cslr: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Accumulated amount of shared library storage (MB) allocated in one interval.")
    r743clmn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Minimum amount of shared library storage (MB) allocated per cycle.")
    r743clmx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Maximum number of shared library storage (MB) allocated per cycle.")
    r743oslr: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Accumulated number of attempts to exceed maximum amount of shared library region size during one interval.")
    r743olmn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Minimum number of attempts to exceed maximum amount of shared library region per cycle.")
    r743olmx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Maximum number of attempts to exceed maximum amount of shared library region per cycle.")
    r743mqds: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Maximum amount of queued signals allowed per process.")
    r743oqds: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Accumulated number of attempts to exceed maximum amount of queued signals per interval.")
    r743oqmn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Minimum number of attempts to exceed maximum amount of queued signals per cycle.")
    r743oqmx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Maximum number of attempts to exceed maximum amount of queued signals per cycle.")
    r743ter: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                         doc="r743flg (Bit 0) showing kernel address space is terminated or reinstated this interval.")
    r743chpr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r743flg (Bit 1) showing maximum number of processes changed during reporting interval.")
    r743chus: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r743flg (Bit 2) showing maximum number of users changed during reporting inteval.")
    r743chpu: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r743flg (Bit 3) showing maximum number of processes per user changed during reporting interval.")
    r743chms: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r743flg (Bit 4) showing maximum number of message queue ids changed during reporting interval when set.")
    r743chse: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r743flg (Bit 5) showing maximum number of semaphore ids changed during reporting interval when set.")
    r743chsh: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r743flg (Bit 6) showing maximum number of shared memory ids changed during reporting interval when set.")
    r743chsp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r743flg (Bit 7) showing maximum number of shared memory pages changed during reporting interval when set.")
    r743chma: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r743flg (Bit 8) showing maximum number of memory map storage pages changed during reporting interval when set.")
    r743chpa: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r743flg (Bit 9) showing maximum number of shared storage pages changed during reporting interval when set.")
    r743chlr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r743flg (Bit 10) showing maximum size of shared library region changed during reporting interval when set.")
    r743cqsg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r743flg (Bit 11) showing maximum number of queued signals per process changed during reporting interval when set.")


class Smf74path(AbstractConcreteBase):
    """Abstract class for structure Smf74Path - Path data section."""

    r742pdev: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="Device number.")
    r742pstf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Status flags Bit Meaning when set 0 Path became active during this interval 1 Path became inactive during this interval. 2 Counts reset by XCF during this interval. 3-7 Reserved.")
    r742podv: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4),
                                                          doc="Device number on other end if known, otherwise blanks.")
    r742psta: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Path status Bit Meaning when set 0 Starting 1 Restarting 2 Working 3 Stopping 4 Waiting for completion of communication link 5 Not operational. Path defined to XCF, but not usable until hardware and/or definition problems are resolved. 6 Stop failed 7 Rebuilding. More path status flags:")
    r742pstm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="More path status flags: Bit Meaning when set 0 Quiescing 1 Quiesced 2-7 Reserved.")
    r742pret: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Path retry limit.")
    r742prst: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of restarts.")
    r742pmxm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Maximum number of 1K blocks of message buffer space.")
    r742psig: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of outbound (inbound) signals sent (received) over path.")
    r742pqln: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of outbound signals pending transfer on path.")
    r742pibr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of inbound signals refused due to maximum message limit.")
    r742psus: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of times this signalling path was not busy when it was selected to transfer a message.")
    r742papp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of times this signalling path was busy when it was selected to transfer a message.")
    r742piot: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="For inbound paths: Average I/O transfer time (microseconds) for the observed in the last minute of the RMF reporting interval, or X'FFFFFFFF' (if time > 35 minutes).")
    r742prct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Path retry count.")
    r742ppnd: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="The current number of signals pending for transfer on the path (outbound only).")
    r742puse: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="The current number of 1KB blocks of message buffer space in use by this path.")
    r742plin: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="List number within structure.")
    r742pusg_timesum_1: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                      doc="engine 1 - Time (in microseconds) this path was in use at the indicated percent utilization.")
    r742pusg_timesum_2: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                      doc="engine 2 - Time (in microseconds) this path was in use at the indicated percent utilization.")
    r742pusg_timesum_3: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                      doc="engine 3 - Time (in microseconds) this path was in use at the indicated percent utilization.")
    r742pusg_timesum_4: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                      doc="engine 4 - Time (in microseconds) this path was in use at the indicated percent utilization.")
    r742pusg_timessq_1: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                      doc="engine 1 - Squared microseconds this path was in use at the indicated percent utilization.")
    r742pusg_timessq_2: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                      doc="engine 2 - Squared microseconds this path was in use at the indicated percent utilization.")
    r742pusg_timessq_3: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                      doc="engine 3 - Squared microseconds this path was in use at the indicated percent utilization.")
    r742pusg_timessq_4: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                      doc="engine 4 - Squared microseconds this path was in use at the indicated percent utilization.")
    r742pusg_timenum_1: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                    doc="engine 1 - Number of times this path was in use at the indicated percent utilization.")
    r742pusg_timenum_2: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                    doc="engine 2 - Number of times this path was in use at the indicated percent utilization.")
    r742pusg_timenum_3: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                    doc="engine 3 - Number of times this path was in use at the indicated percent utilization.")
    r742pusg_timenum_4: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                    doc="engine 4 - Number of times this path was in use at the indicated percent utilization.")
    r742pusg_sigcnt_1: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                   doc="engine 1 - Number of signals sent for this usage entry.")
    r742pusg_sigcnt_2: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                   doc="engine 2 - Number of signals sent for this usage entry.")
    r742pusg_sigcnt_3: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                   doc="engine 3 - Number of signals sent for this usage entry.")
    r742pusg_sigcnt_4: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                   doc="engine 4 - Number of signals sent for this usage entry.")
    r742pusg_percent_1: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                    doc="engine 1 - Percent utilization that this entry represents.")
    r742pusg_percent_2: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                    doc="engine 2 - Percent utilization that this entry represents.")
    r742pusg_percent_3: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                    doc="engine 3 - Percent utilization that this entry represents.")
    r742pusg_percent_4: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                    doc="engine 4 - Percent utilization that this entry represents.")
    r742pnib_timesum: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="Total time (in microseconds) this path had a no-inbound-buffer impact condition.")
    r742pnib_timessq: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="Squared microseconds for each no-inbound-buffer impact condition.")
    r742pnib_timenum: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                  doc="Number of times this path was impacted by a no-inbound-buffer condition.")
    r742pact: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r742pstf (Bit 0) showing path became active during this interval.")
    r742piac: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r742pstf (Bit 1) showing path became inactive during this interval.")
    r742pres: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r742pstf (Bit 2) showing counts reset by XCF during this interval.")
    r742pst: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="r742psta (Bit 0) showing path starting.")
    r742prs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="r742psta (Bit 1) showing path restarting.")
    r742pwk: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="r742psta (Bit 2) showing path working.")
    r742psp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="r742psta (Bit 3) showing path stopping.")
    r742plk: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                         doc="r742psta (Bit 4) showing path waiting for completion of communication link.")
    r742pnp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                         doc="r742psta (Bit 5) showing path not operational. Path defined to XCF, but not usable until hardware and/or definition problems are resolved.")
    r742psf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="r742psta (Bit 6) showing path stop failed.")
    r742prb: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="r742psta (Bit 7) showing path rebuilding.")
    r742pqg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="r742pstm (Bit 0) showing path quiescing.")
    r742pqd: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="r742pstm (Bit 1) showing path quiesced.")


class Smf74pcie(AbstractConcreteBase):
    """Abstract class for structure Smf74Pcie - PCIE function data section."""

    r749pffl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="PFID function status merged over all MINTIME intervals for this reporting interval. Bit Meaning when set 0 PFID was allocated during this interval. 1 PFID was in status De-Allocate-Pending during this interval. 2 PFID was in error during this interval. 3-15 Reserved.")
    r749pff1: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Final PFID function status at the end of this reporting interval. Bit Meaning when set 0 PFID is de-allocated at the end of this interval. 1 PFID is re-allocated at the end of this interval. 2-15 Reserved.")
    r749errt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Time in milliseconds for which no valid data was reported for the PCIE function within this reporting interval.")
    r749devt: so.Mapped[Optional[str]] = so.mapped_column(sa.String(10), doc="Device type for the PCIE function.")
    r749devn: so.Mapped[Optional[str]] = so.mapped_column(sa.String(24), doc="Device name for the PCIE function.")
    r749jobn: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="Job name of owner who allocated the PCIE function.")
    r749asid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6),
                                                          doc="Address space ID of owner who allocated the PCIE function.")
    r749pcid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6),
                                                          doc="Physical or virtual channel identifier for the PCIE function.")
    r749atst: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                  doc="Timestamp in STCK format, showing the last point in time when a PCIE function was allocated.")
    r749allt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Time in milliseconds for which the PCIE function was allocated or was in status De-Allocate- Pending .")
    r749scnt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Sequence number for the last time the PCI operations counters or DMA read/write counters have been updated by the firmware.")
    r749loop: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Count of PCI Load operations for the PCIE function. Only valid, if bit 2 of R749FLAG is not set.")
    r749stop: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Count of PCI Store operations for the PCIE function. Only valid, if bit 2 of R749FLAG is not set.")
    r749sbop: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Count of PCI Store Block operations for the PCIE function. Only valid, if bit 2 of R749FLAG is not set.")
    r749rfop: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Count of PCI Refresh Translation operations for the PCIE function. Only valid, if bit 2 of R749FLAG is not set.")
    r749dmao: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="The PCIE Function Type data blocks for all PCIE functions are grouped together in the record. To get to the PCIE Function Type data block associated with this PCIE Function data section, skip over the number of PCIE Function Type data blocks specified by this field, starting at the first PCIE Function Type data block in the record.")
    r749dman: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of PCIE Function Type data blocks allocated for this PCIE function data section.")
    r749fpfo: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="The data blocks for all hardware accelerators are grouped together in the record. To get to the hardware accelerator data block associated with this PCIE Function data section, skip over the number of hardware accelerator data blocks specified by this field, starting at the first hardware accelerator block in the record.")
    r749fpfn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of hardware accelerator data blocks")
    r749fp1o: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="The data blocks for all hardware accelerators used for compression acceleration are grouped together in the record. To get to the hardware accelerator compression data block associated with this PCIE Function data section, skip over the number of hardware accelerator compression data blocks specified by this field, starting at the first hardware accelerator")
    r749fp1n: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of hardware accelerator compression data blocks allocated for this PCIE Function data section.")
    r749flag: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Validity flag. Bit Meaning when set 0 Physical-network identifiers R749NET1 and R749NET2 are valid. 1 PCIE function type R749PFT is valid. 2 PCI operation rates are invalid. 3 Global Performance Reporting is enabled. 4-7 Reserved.")
    r749port: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Physical port number for which this PCIE function is associated. If zero, then either the port field is not applicable, or there is more than")
    r749pft: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="PCIE function type.")
    r749net1: so.Mapped[Optional[str]] = so.mapped_column(sa.String(16),
                                                          doc="Physical-network identifier (PNET ID) that identifies the first port of the adapter. This field is only valid when the PCIE device type is defined as RoCE Express or ISM.")
    r749net2: so.Mapped[Optional[str]] = so.mapped_column(sa.String(16),
                                                          doc="Physical-network identifier (PNET ID) that identifies the second port of the adapter. Only valid when the PCIE device type is defined as RoCE Express.")
    r749wwnn: so.Mapped[Optional[str]] = so.mapped_column(sa.String(18),
                                                          doc="Worldwide node name (WWNN) of the storage controller the synchronous I/O link is connected to.")
    r749sioo: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="The data blocks for all Synchronous I/O links are grouped together in the record. To get the Synchronous I/O link data block associated with this PCIE Function data section, skip over the number of data blocks specified by this field, starting at the first Synchronous I/O link data block in the record.")
    r749sion: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of Synchronous I/O link data blocks allocated for this PCIE Function data section.")
    r749rtdo: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="The data blocks for all Synchronous I/O response time distribution buckets are grouped together in the record. To get the first Synchronous I/O response time distribution data block associated with this PCIE Function data section, skip over the number of data blocks specified by this field, starting at the first Synchronous I/O response time distribution data block in the record.")
    r749rtdn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of Synchronous I/O response time distribution data blocks allocated for this PCIE Function data section.")
    r749lkid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="The identifier of the synchronous I/O link that is configured in the storage controller.")
    r749sndt: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="from r749snd showing type number.")
    r749sndm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(3), doc="from r749snd showing model number.")
    r749sndn: so.Mapped[Optional[str]] = so.mapped_column(sa.String(3), doc="from r749snd showing manufacturer.")
    r749sndp: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                          doc="from r749snd showing plant of manudfacture.")
    r749snds: so.Mapped[Optional[str]] = so.mapped_column(sa.String(12), doc="from r749snd showing sequence number.")
    status: so.Mapped[Optional[str]] = so.mapped_column(sa.String(20),
                                                        doc="from r749pffl and r749pff1 showing PFID function status.")
    physical_network: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                  doc="r749flag (Bit 0) showing physical-network identifiers r749net1 and r749net2 are valid.")
    pcie_valid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                            doc="r749flag (Bit 1) showing PCIE function type r749pft is valid.")
    pci_oper_rates_invalid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                        doc="r749flag (Bit 2) showing PCI operation rates are invalid.")
    global_performance: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                    doc="r749flag (Bit 3) showing Global Performance Reporting is enabled.")
    pciload: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="rate of PCI Load operations executed during the reporting interval. This value is not reported for synchronous I/O functions.")
    pcistor: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="rate of PCI Store operations executed during the reporting interval. This value is not reported for synchronous I/O functions.")
    pcistbl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="rate of PCI Store Block operations executed during the reporting interval. This value is not reported for synchronous I/O functions.")
    pcirptr: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="rate of Refersh PCI Translations operations executed during the reporting interval. This value is not reported for synchronous I/O functions.")
    pcidmar: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="DMA read rate (on zEC12 or zBC12 hardware only).")
    pcidmaw: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="DMA write rate (on zEC12 or zBC12 hardware only).")
    fpgbusy: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="the percentage of time that this partition kept the hardware accelerator busy.")
    fpgrtim: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="the average time the hardware accelerator used to process a request.")
    fpgqtim: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="the average queue time that was spent for a request. This value has single system scope but is affected by activity from other partitions sharing the hardware accelerator.")
    fpgbytr: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="the average number of kilobytes transferred per request.")
    fpgbyts: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="the number of megabytes per second transferred to and from the PCIE function. For ISM functions, this value reports the number of megabytes transmitted to the function.")
    fpgcors: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="the number of compression requests per second.")
    fpgcobs: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="the number of megabytes compressed per second.")
    fpgcort: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="the ratio between input and output bytes compressed within this interval.")
    fpgdcrs: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="the number of decompression requests per second.")
    fpgdcbs: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="the number of megabytes decompressed per second.")
    fpgdcrt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="the ratio between input and output bytes decompressed with this interval.")
    fpgbprt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="the average utilization of the buffer pool that z/OS kept for in-use buffers.")
    pcibytr: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="number of megabytes received per second (RoCE on z13 or later and synchronous I/O).")
    pcibytt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="number of megabytes transmitted per second (RoCE on z13 or later, ISM and synchronous I/O).")
    pcipakr: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="number of packets received per second (RoCE on z13 and later only).")
    pcipakt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="number of packets transmitted per second (RoCE on z13 and later only).")
    pciwup: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                          doc="number of work units processed per second (zEDC onz13 and later only).")
    pciutil: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="PCI function utilization (zEDC on z13 and later only).")
    synctr: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                          doc="the total number of synchronous I/O requests per second for this function.")
    syncsr: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                          doc="the total number of synchronous I/O requests per second that completed succesfully for this function.")
    pcibytr_ratio: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="the number of megabytes read per request processed by this synchronous I/O function.")
    pcibytt_ratio: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="the number of meagbytes written per request processed by this synchronous I/O function.")
    cpcsynctr: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                             doc="the total number of synchronous I/O requests per second for the synchronous I/O link this function is defined on.")
    cpcsyncsr: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                             doc="the total number of synchronous I/O requests per second that completed succesfully for the synchronous I/O link this function is defined on.")
    cpcpcibytr: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="number of megabytes per second that were read from the storage controller on the synchronous I/O link this function is defined on.")
    cpcpcibytt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="number of megabytes per second that were written to the storage controller on the synchronous I/O link this function is defined on.")
    cpcfpgbusy: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="the percentage of time spent on synchronous I/O processing on the synchronous I/O link this function is defined on.")
    cpcpcibytr_ratio: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="the number of megabytes read per request processed on the synchronous I/O link this function is defined on.")
    cpcpcibytt_ratio: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="the number of megabytes written per reequest processed on the synchronous I/O link this function is defined on.")
    pcitosir: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="total synchronous I/O read bucket counts.")
    pcitosiw: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="total synchronous I/O write bucket counts.")
    pcipcr1: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="percentage of synchronous I/O read samples with a response time less than n microseconds.")
    pcipcr2: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="percentage of synchronous I/O read samples with a response time less than n microseconds and greater or equal to the pcipcr1.")
    pcipcr3: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="percentage of synchronous I/O read samples with a response time less than n microseconds and greater or equal to the pcipcr2.")
    pcipcr4: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="percentage of synchronous I/O read samples with a response time less than n microseconds and greater or equal to the pcipcr3.")
    pcipcr5: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="percentage of synchronous I/O read samples with a response time less than n microseconds and greater or equal to the pcipcr4.")
    pcipcr6: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="percentage of synchronous I/O read samples with a response time less than n microseconds and greater or equal to the pcipcr5.")
    pcipcr7: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="percentage of synchronous I/O read samples with a response time less than n microseconds and greater or equal to the pcipcr6.")
    pcipcr8: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="percentage of synchronous I/O read samples with a response time less than n microseconds and greater or equal to the pcipcr7.")
    pcipcr9: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="percentage of synchronous I/O read samples with a response time less than n microseconds and greater or equal to the pcipcr8.")
    pcipcr10: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="percentage of synchronous I/O read samples with a response greater or equal to n microseconds.")
    pcipcw1: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="percentage of synchronous I/O write samples with a response time less than n microseconds.")
    pcipcw2: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="percentage of synchronous I/O write samples with a response time less than n microseconds and greater or equal to the pcipcw1.")
    pcipcw3: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="percentage of synchronous I/O write samples with a response time less than n microseconds and greater or equal to the pcipcw2.")
    pcipcw4: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="percentage of synchronous I/O write samples with a response time less than n microseconds and greater or equal to the pcipcw3.")
    pcipcw5: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="percentage of synchronous I/O write samples with a response time less than n microseconds and greater or equal to the pcipcw4.")
    pcipcw6: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="percentage of synchronous I/O write samples with a response time less than n microseconds and greater or equal to the pcipcw5.")
    pcipcw7: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="percentage of synchronous I/O write samples with a response time less than n microseconds and greater or equal to the pcipcw6.")
    pcipcw8: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="percentage of synchronous I/O write samples with a response time less than n microseconds and greater or equal to the pcipcw7.")
    pcipcw9: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="percentage of synchronous I/O write samples with a response time less than n microseconds and greater or equal to the pcipcw8.")
    pcipcw10: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="percentage of synchronous I/O write samples with a response time greater or equal to n microseconds.")


class Smf74port(AbstractConcreteBase):
    """Abstract class for structure Smf74Port - FCD port data section."""

    r747ppir: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r744ppfl (Bit 0) showing port information was returned at least once for this port.")
    r747pnti: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r744ppfl (Bit 1) showing port information showed this prot not installed.")
    r747plf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                         doc="r744ppfl (Bit 2) showing port information showed link failure condition.")
    r747poff: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r744ppfl (Bit 3) showing port information showed this port offline.")
    r747pscr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r744ppfl (Bit 4) showing statistics were returned at least once for this port.")
    ndeconfigcode: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                               doc="ND associated with switch device configuration code.")
    ndetype: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="ND associated with switch device type.")
    ndemodel: so.Mapped[Optional[str]] = so.mapped_column(sa.String(3), doc="ND associated with switch device model.")
    ndemfg: so.Mapped[Optional[str]] = so.mapped_column(sa.String(3),
                                                        doc="ND associated with switch device manufacturer.")
    ndeplant: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                          doc="ND associated with switch device plant code.")
    ndesequence: so.Mapped[Optional[str]] = so.mapped_column(sa.String(12),
                                                             doc="ND associated with switch device sequence number.")
    ndecpcid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="ND associated with switch device CPC id.")


class Smf74proc(AbstractConcreteBase):
    """Abstract class for structure Smf74Proc - Coupling Facility processor utilization data section."""

    r744pbsy: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Busy time (in microseconds).")
    r744pwai: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Wait time (in microseconds).")
    r744ptyp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Processor flags Bit Meaning when set 0 Processor is dedicated. Valid if R744FLVL > 14. 1-7 Reserved.")
    r744pwgt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Shared processor weight. Valid if R744FLVL > 14.")
    r744pbsg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Assigned buffer summary group. Valid if R744FLVL > 24.")
    r744pcct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Processor command count. Valid if R744FLVL > 24.")
    r744ptle: so.Mapped[Optional[str]] = so.mapped_column(sa.String(16),
                                                          doc="CPU-type topology list entry, as returned by the STSI instruction SYSIB 15.1.2 (Configuration Topology). See IBM z/Architecture Principles of Operation for the format. Valid if R744FLVL > 24.")
    r744ptde: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r744ptyp (Bit 0) showing processor is dedicated. Valid if r744flvl > 14.")


class Smf74scm(AbstractConcreteBase):
    """Abstract class for structure Smf74Scm - Storage Class Memory (SCM) configuration measurement section."""

    r7410cdus: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Data unit size in bytes.")
    r7410crqc: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                           doc="Internal requests processed at CPC level.")
    r7410crq: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Internal requests processed at LPAR level.")
    r7410cdwc: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Data units written at CPC level.")
    r7410cdw: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Data units written at LPAR level.")
    r7410cdrc: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Data units read at CPC level.")
    r7410cdr: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="Data units read at LPAR level.")
    r7410crtc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                             doc="Aggregate time spent on execution of requests involving resource part in units of 128 microseconds at CPC level.")
    r7410crt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Aggregate time spent on execution of requests involving resource part in units of 128 microseconds at LPAR level.")
    r7410ciqc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                             doc="Accumulated IOP queue time in units of 128 microseconds at CPC level.")
    r7410cwuc: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                           doc="Utilization at CPC level. This value designates the sum of the average CPC utilization per second in percent multiplied by the number of seconds of this interval.")
    r7410cwu: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Utilization at LPAR level. This value designates the sum of the average LPAR utilization per second in percent multiplied by the number of seconds of this interval.")
    r7410flg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Flag byte. Bit Meaning when set 0 SCM resource type is Virtual Flash Memory 1-7 Reserved")
    smf74int: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Duration of RMF measurement interval, in the form mmsstttF where mm is the minutes, ss is the seconds, ttt is the milliseconds, and F is the sign. The end of the measurement interval is the sum of the recorded start time and this field.")
    r7410vfm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r7410flg (Bit 0) showing SCM resource type is Virtual Flash Memory.")
    r7410cdwc_bytes: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="total bytes written at CPC level.")
    r7410cdw_bytes: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="total bytes written at LPAR level.")
    r7410cdrc_bytes: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="total bytes read at CPC level.")
    r7410cdr_bytes: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, doc="total bytes read at LPAR level.")


class Smf74siol(AbstractConcreteBase):
    """Abstract class for structure Smf74Siol - Synchronous I/O link statistics section."""

    r748styp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Synchronous I/O link type. Value Meaning 00 Not used 01 Optical PCIe 02-FF Not used")
    r748sspd: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Synchronous I/O link speed. Value Meaning 00 Not used 01 PCIe Gen 1 02 PCIe Gen 2 03 PCIe Gen 3 04 PCIe Gen 4 05-FF Not used")
    r748swdh: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Synchronous I/O link width. This number is the number of PCIe lanes.")
    r748sste: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Value Meaning 00 Not used 01 Link not Trained 02 Link handshake incomplete 03 Link handshake complete and link operational 04 Link in service mode (i.e. link quiesced) 05-FF Not used")
    r748sflg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Flags. Bit Meaning when set 0 Unit of bytes indeterminable. Byte values incorrect. 1")
    r748scbr: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Synchronous I/O cache bytes read in units of 128K bytes.")
    r748scro: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total number of synchronous I/O cache read operations.")
    r748scrs: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of successful synchronous I/O cache read operations.")
    r748scrt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Synchronous I/O cache read accumulated time in milliseconds.")
    r748scbw: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Synchronous I/O cache bytes written in units of 128K bytes.")
    r748scwo: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total number of synchronous I/O cache write operations.")
    r748scws: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of successful synchronous I/O cache write operations.")
    r748scwt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Synchronous I/O cache write accumulated time in milliseconds.")
    r748snbw: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="NVS bytes written in units of 128K bytes.")
    r748snwo: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Total number of NVS write operations.")
    r748snws: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Number of successful NVS write operations.")
    r748snwt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="NVS write accumulated time in milliseconds.")
    r748sbyt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r748sflg (Bit 0) showing unit of bytes indeterminable. Byte values incorrect.")
    r748stim: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r748sflg (Bit 1) showing unit of time indeterminable. Time values incorrect.")


class Smf74sreq(AbstractConcreteBase):
    """Abstract class for structure Smf74Sreq - Coupling Facility request data section."""

    r744styp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Structure type identifier. Value Meaning 1 Unserialized List structure 2 Serialized List structure 3 Lock structure 4 Cache structure")
    r744sflg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Status Flags. Bit Meaning when set 0 Structure was connected to the system at the end of the interval. 1 Structure became active during the interval. 2 Structure is capable to participate in asynchronous duplexing. (Valid if bit 5 of R744FFLG is not set.) 3 Structure is in the duplexing active state. (Valid if bit 5 of R744FFLG is not set.) 4 Structure is primary instance of an asynchronously duplexed structure. (Valid if bit 5 of R744FFLG is not set.) 5 Structure is secondary instance of an asynchronously duplexed structure. (Valid if bit 5 of R744FFLG is not set.) 6 Structure is encrypted. (Valid if bit 5 of R744FFLG is not set.) 7")
    r744slec: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Lock structure only: lock table entry characteristic. (Valid if bit 5 of")
    r744slel: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="List structure: limit on number of list entries. The estimated maximum number of list entries that may reside in storage class memory is not included. Lock structure: limit on number of data elements. (Valid if bit 5 of R744FFLG is not set.)")
    r744slem: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="List structure: current number of list entries in use. The number of list entries that currently reside in storage class memory is not included. Lock structure: current number of data elements in use. (Valid if bit 5 of R744FFLG is not set.)")
    r744sltl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Lock structure only: limit on number of lock table entries. (Valid if bit 5 of R744FFLG is not set.)")
    r744sltm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Lock structure only: Current number of lock table entries in use. (Valid if bit 5 of R744FFLG is not set.)")
    r744ssta: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="The number of list, lock, or cache requests that were to be executed synchronously at the coupling facility, but which were changed to an asynchronous operation due to lack of resources.")
    r744strc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="The total number of IXLLIST, IXLCACHE, or IXLLOCK requests made. This field will not necessarily equal the sum or R744SSRC, R744SARC, and R744SSTA due to internal processing. Use of the batch unlock function can produce large discrepancies because R744STRC is incremented for each lock being released, but only one coupling facility operation is executed.")
    r744stac: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="The total number of IXLLOCK requests that could not be satisfied immediately because of lock contention.")
    r744sarc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="The total number of operations executed asynchronously at the coupling facility.")
    r744satm: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Summed service time for asynchronous requests in microseconds.")
    r744sasq: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Summed squares of service time for asynchronous requests.")
    r744ssrc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Count of number of times for synchronous requests.")
    r744sstm: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Summed service time for synchronous requests in microseconds.")
    r744sssq: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Summed squares of service time for synchronous requests.")
    r744sqrc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Count of number of times for queued requests.")
    r744sqtm: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Summed queue delay time in microseconds.")
    r744sqsq: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Summed squares of delay time for queued requests.")
    r744sdrc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of times a request was found delayed in case of dump serialization.")
    r744sdtm: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Summed dump delay time in microseconds.")
    r744sdsq: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Summed squares of dump delay time.")
    r744sdmp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of times dump serialization was found for this structure (list and cache structures only).")
    r744shto: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total number of requests waiting on the high priority queue.")
    r744shmn: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Minimum number of requests waiting on the high priority queue during this interval.")
    r744shmx: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Maximum number of requests waiting on the high priority queue during this interval.")
    r744slto: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total number of requests waiting on the low priority queue.")
    r744slmn: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Minimum number of requests waiting on the low priority queue during this interval.")
    r744slmx: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Maximum number of requests waiting on the low priority queue during this interval.")
    r744sdto: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total number of requests delayed because dump serialization is in progress.")
    r744sdmn: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Minimum number of requests delayed because dump serialization is in progress during this interval.")
    r744sdmx: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Maximum number of requests delayed because dump serialization is in progress during this interval.")
    r744scn: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="Lock structure only: number of times any request encountered lock contention.")
    r744sfcn: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Lock structure only: number of times any request encountered false lock contention (storage contention within the structure).")
    r744ssiz: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Allocated size of structure (units = 4K byte blocks). (Valid if bit 5 of R744FFLG is not set.)")
    r744smas: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Maximum structure size. (Valid if bit 5 of R744FFLG is not set.)")
    r744smis: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Minimum structure size. (Valid if bit 5 of R744FFLG is not set.)")
    r744sdec: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Cache structure only: Total directory entry count. (Valid if bit 5 of R744FFLG is not set.)")
    r744sdel: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Cache structure only: Total data element count. (Valid if bit 5 of R744FFLG is not set.)")
    r744snlh: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="List structure only: Number of list headers. (Valid if bit 5 of R744FFLG is not set.)")
    r744smae: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="List structure only: maximum number of elements. The estimated maximum number of list elements that may reside in storage class memory is not included. (Valid if bit 5 of R744FFLG is not set.)")
    r744scue: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="List structure only: current number of elements in use. The number of list elements that currently reside in storage class memory is not included. (Valid if bit 5 of R744FFLG is not set.)")
    r744cdsi: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Index to first Cache data section.")
    r744cdne: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of Cache data section entries.")
    r744spln: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Count of peer-link-not-available conditions.")
    r744spes: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Count of execution-suppressed conditions.")
    r744sptc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Count of waiting-for-peer-subchannel conditions.")
    r744spst: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total peer-subchannel-wait time (microseconds).")
    r744spss: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Square of total peer-subchannel-wait time (microseconds squared).")
    r744srtc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Count of condition 'waiting for peer subchannel with reserve held'.")
    r744srst: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total peer-subchannel-wait-with-reserve time (microseconds).")
    r744srss: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Square of total peer-subchannel-wait-with-reserve time (microseconds squared).")
    r744sctc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Count of condition 'waiting for peer completion'.")
    r744scst: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total waiting-for-peer-completion time (microseconds).")
    r744scss: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Square of total waiting-for-peer-completion time (microseconds squared).")
    r744slsv: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Logical structure version number.")
    r744setm: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Structure execution time (microseconds). Valid if R744FLVL > 14. (Valid if bit 5 of R744FFLG is not set.)")
    r744sisc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Index to Storage Class Memory data section. This field is zero if there is no SCM information available.")
    r744snsc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of Storage Class Memory data sections.")
    r744ssac: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of Storage Class Memory Access Required conditions that require the request to be restarted.")
    r744sosa: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of successful operations to the coupling facility that encountered an SCM Access Required condition.")
    r744siad: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Index to Asynchronous CF Duplexing data section. This field is zero if there is no Asynchronous CF Duplexing data available.")
    r744sadn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of Asynchronous CF Duplexing data sections.")
    r744sixc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of asynchronous duplex requests that requested sync up with the primary. (Valid if bit 1 of R744SXFL is set.)")
    r744sxsc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of asynchronous duplex requests that were suspended waiting for the operations to complete in the secondary structure of the current duplexing instance. (Valid if bit 1 of R744SXFL is set.)")
    r744sxst: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Summed suspend time, in microseconds, for suspended requests that were waiting for asynchronous duplex operations to complete in the secondary structure of the current duplexing instance. (Valid if bit 1 of R744SXFL is set.)")
    r744sxsq: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Square of summed suspend times, in square of microseconds, for suspended requests that were waiting for the asynchronous duplex operations to complete in the secondary structure of the current duplexing instance. (Valid if bit 1 of R744SXFL is set.)")
    r744sado: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of asynchronous duplex operations that were delayed because the primary structure was unable to accept new requests either because it could not forward requests to the secondary CF or because the secondary CF could not process incoming requests. (Valid if bit 0 of R744SXFL is set.)")
    r744sadr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of asynchronous duplex requests that experienced a delayed operation because the primary CF was unable to accept new requests. (Valid if bit 0 of R744SXFL is set.)")
    r744sqch: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Asynchronous duplex operation queue characteristic. The number of queue entries is the product of: 4096 × 2 ** R744SQCH")
    r744sxfl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Meaning when set 0 Data for primary instance of asynchronous duplexed structure is valid. 1 Data for secondary instance of asynchronous duplexed structure is valid. 2 Data for Write and Read Request Measurements is valid. 3 Data for CF monopolization delays is valid. 4 - 7")
    r744swdr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of requests to write data to the CF structure. (Valid if bit 2 of R744SXFL is set.)")
    r744swac: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of adjunct areas written to the CF structure. (Valid if bit 2 of R744SXFL is set.)")
    r744srdr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of requests to read data from the CF structure. (Valid if bit 2 of R744SXFL is set.)")
    r744srac: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of adjunct areas read from the CF structure. (Valid if bit 2 of R744SXFL is set.)")
    r744swec: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Number of data entries with data elements that have been written to the CF structure. Includes both single and multi entry write requests. (Valid if bit 2 of R744SXFL is set.)")
    r744srec: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of data entries with data elements that have been read from the CF structure. Includes both single and multi entry read requests. (Valid if bit 2 of R744SXFL is set.)")
    r744swed: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Sum of 256-byte increments accumulated for entry data with data elements written to the CF structure. (Valid if bit 2 of R744SXFL is set.)")
    r744swes: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Square of summed number of 256-byte increments accumulated for entry data with data elements written to the CF structure. (Valid if bit 2 of R744SXFL is set.)")
    r744sred: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Sum of 256-byte increments accumulated for entry data with data elements read from the CF structure. (Valid if bit 2 of R744SXFL is set.)")
    r744sres: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Square of summed number of 256-byte increments accumulated for entry data with data elements read from the CF structure. (Valid if bit 2 of R744SXFL is set.)")
    r744smrc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of times a request was found delayed due to coupling facility resource monopolization. (Valid if bit 3 of R744SXFL is set.)")
    r744smtm: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Summed queue time (in microseconds) for operations queued due to coupling facility resource monopolization. (Valid if bit 3 of R744SXFL is set.)")
    r744smsq: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Summed queue time squared for operations queued due to coupling facility resource monopolization, in microseconds squared. (Valid if bit 3 of R744SXFL is set.)")
    r744smto: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total number of operations queued for CF monopolization avoidance. (Valid if bit 3 of R744SXFL is set.)")
    r744smht: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Total number of high-priority operations queued for CF monopolization avoidance. (Valid if bit 3 of R744SXFL is set.)")
    r744smmn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Minimum number of operations queued for CF monopolization avoidance during this interval. (Valid if bit 3 of R744SXFL is set.)")
    r744smmx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Maximum number of operations queued for CF monopolization avoidance during this interval. (Valid if bit 3 of R744SXFL is set.)")
    r744smhn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Minimum number of high-priority operations queued for CF monopolization avoidance during this interval. (Valid if bit 3 of R744SXFL is set.)")
    r744smhx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Maximum number of high-priority operations queued for CF monopolization avoidance during this interval. (Valid if bit 3 of R744SXFL is set.)")
    r744scei: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r744sflg (Bit 0) showing structure was connected to the system at the end of the interval.")
    r744sadi: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r744sflg (Bit 1) showing structure became active during the interval.")
    r744scad: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r744sflg (Bit 2) showing structure is capable to participate in asynchronous duiplexing. (Valid if bit 5 of r744fflg is not set.)")
    r744sdas: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r744sflg (Bit 3) showing structure is in the duplexing active state. (Valid if bit 5 of r744fflg is not set.)")
    r744spri: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r744sflg (Bit 4) showing structure is primary instance of an asynchronously duplexed structure. (Valid if bit 5 of r744fflg is not set.)")
    r744ssec: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r744sflg (Bit 5) showing structure is secondary instance of an asynchronously duplexed structure. (Valid if bit 5 of r744fflg is not set.)")
    r744senc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r744sflg (Bit 6) showing structure is encrypted. (Valid if bit 5 of r744fflg is not set.)")
    r744sxap: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r744sxfl (Bit 0) showing data for priamry instance of asynchronous duplexed structure is valid.")
    r744sxas: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r744sxfl (Bit 1) showing data for secondary instance of asynchronouos duplexed structure is valid.")
    r744sxcm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r744sxfl (Bit 2) showing data for Write and Read Request Measuremens is valid.")
    r744sxmo: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r744sxfl (Bit 3) showing data for CF monopolization delays is valid.")


class Smf74srtd(AbstractConcreteBase):
    """Abstract class for section Smf74Srtd."""

    r749rflg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Response time distribution bucket flag. Bit Meaning 0 If set, response time data measured for synchronous I/O read instructions. 1 If set, response time data measured for synchronous I/O write instructions. 2-7 Reserved.")
    r749rtsc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Response time distribution bucket sample count.")


class Smf74str(AbstractConcreteBase):
    """Abstract class for structure Smf74Str - Coupling Facility structure data section."""

    r744qsiz: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Structure size requested to be allocated (4K-block units).")
    r744qver: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Structure version number.")
    r744qflg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Status Flags. Bit Meaning when set 0 Active instance of structure (normal case). 1 New instance during rebuild. 2 Old instance during rebuild. 3 Instance is just being added or deleted (in transition). 4 Instance in hold, deletion could not be finished. 5 Dump was initiated for this structure. 6 Structure rebuild in progress. 7 The in-progress rebuild is a duplexing rebuild.")
    r744qfl1: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Status Flags 0 Duplexing is active using system-managed asynchronous duplexing. 1-7 Reserved")
    r744qact: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r744qflg (Bit 0) showing active instance of structure (normal case).")
    r744qrbn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r744qflg (Bit 1) showing new instance during rebuild.")
    r744qrbo: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r744qflg (Bit 2) showing old instance during rebuild.")
    r744qtra: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r744qflg (Bit 3) showing instance is just being added or deleted (in transition).")
    r744qhol: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r744qflg (Bit 4) showing instance in hold, deletion could not be finished.")
    r744qdpt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r744qflg (Bit 5) showing dump was initiate for this structure.")
    r744qrbp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r744qflg (Bit 6) showing structure rebuild in progress.")
    r744qrbd: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r744qflg (Bit 7) showing the in-progress rebuild is a duplexing rebuild.")
    r744qaad: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r744qfl1 (Bit 0) showing duplexing is active using system-managed asynchronous duplexing.")


class Smf74switch(AbstractConcreteBase):
    """Abstract class for structure Smf74Switch - FCD switch data section."""

    r747slsn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Logical switch number.")
    r747spfl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Switch processing flags. Bit Meaning when set 0 Status of switch has changed. 1 Number of ports has changed. 2 Switch is offline. 3 Switch is now online. 4 Cascaded switch. 5-7 Reserved.")
    r747snsp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of supported ports for this switch.")
    r747snip: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of installed ports for this switch.")
    r747svar: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r747spfl (Bit 0) showing status of swtich has changed.")
    r747snpc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r747spfl (Bit 1) showing number of ports has changed.")
    r747soff: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="r747spfl (Bit 2) showing switch is offline.")
    r747snol: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r747spfl (Bit 3) showing switch is now online.")
    r747sfcs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="r747spfl (Bit 4) showing cascaded switch.")
    ndeconfigcode: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                               doc="ND associated with switch device configuration code.")
    ndetype: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="ND associated with switch device type.")
    ndemodel: so.Mapped[Optional[str]] = so.mapped_column(sa.String(3), doc="ND associated with switch device model.")
    ndemfg: so.Mapped[Optional[str]] = so.mapped_column(sa.String(3),
                                                        doc="ND associated with switch device manufacturer.")
    ndeplant: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                          doc="ND associated with switch device plant code.")
    ndesequence: so.Mapped[Optional[str]] = so.mapped_column(sa.String(12),
                                                             doc="ND associated with switch device sequence number.")
    ndecpcid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="ND associated with switch device CPC id.")


class Smf74sys(AbstractConcreteBase):
    """Abstract class for structure Smf74Sys - System data section."""

    r742sstf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Status flags Bit Meaning when set 0 System became active during this interval 1 System became inactive during this interval 2 Counts reset by XCF during this interval 3 Partially not active during RMF Postprocessor interval. 4-7 Reserved.")
    r742spth: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Current number of signalling paths in service (zero for local entry). If outbound entry, count is for the indicated transport class.")
    r742sbsy: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of no buffer conditions. For local or outbound entry, count is for the indicated transport class.")
    r742snop: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of no path conditions (zero for local entry). For outbound entry, count is for the indicated transport class.")
    r742smxb: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Maximum 1K blocks of message buffer space. For local or outbound entry, count is for the indicated transport class.")
    r742sbig: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of big message conditions (zero for inbound entry).")
    r742sfit: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of message fit conditions (zero for inbound entry).")
    r742ssml: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of small message conditions (zero for inbound entry).")
    r742sovr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of big messages that exceeded the message length for which XCF was optimized (zero for inbound entry).")
    r742stcl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Message length for transport class (zero for inbound entry).")
    r742sact: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r742sstf (Bit 0) showing system became active during this interval.")
    r742siac: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r742sstf (Bit 1) showing system became inactive during this interval.")
    r742sres: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r742sstf (Bit 2) showing counts reset by XCF during this interval.")
    r742spar: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r742sstf (Bit 3) showing partially not active during RMF Postprocessor interval.")


class Smf74raid(AbstractConcreteBase):
    """Abstract class for structure Smf74Raid - RAID rank data section."""

    r7451scs: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2), doc="Subchannel set ID.")
    r7451rsv: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Lower interface I/O response time (in milliseconds).")
    r7451flg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Flag. Value Meaning 0 No additional information 1 RAID rank data. 2 Extent pool and physical storage data.")
    r7451aid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4),
                                                          doc="Device adapter ID. Only valid with RAID rank data.")
    r7451hdd: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of HDDs in RAID rank.")
    r7451rty: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="RAID rank type. Value Type 0 RAID-5 1 JBOD 2")
    r7451hss: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="HDD sector size.")
    r7451rrq: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="RAID rank read requests.")
    r7451wrq: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="RAID rank write requests.")
    r7451sr: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="RAID rank FB sectors read.")
    r7451sw: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="RAID rank FB sectors written.")
    r7451rrt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="RAID rank read response time (in milliseconds).")
    r7451wrt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="RAID rank write response time (in milliseconds).")
    r7451sio: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r7451inc (Bit 3) showing synchronous I/O cache data are valid.")
    r7451hpf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r7451inc (Bit 4) showing zHPF read and write I/O requests r7451ct5 and r7451ct6 are available.")
    r7451xfl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r7451inc (Bit 7) showing transfer statistics r7451xfr are valid.")


class Smf74cf(AbstractConcreteBase):
    """Abstract class for structure Smf74Cf - Coupling Facility data."""

    smf74mfv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="RMF version number.")
    smf74int: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Duration of RMF measurement interval, in the form mmsstttF where mm is the minutes, ss is the seconds, ttt is the milliseconds, and F is the sign. The end of the measurement interval is the sum of the recorded start time and this field.")
    smf74sam: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of RMF samples.")
    smf74cyc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Sampling cycle length, in the form 000 ttttF , where tttt is the milliseconds and F is the sign (taken from CYCLE option). The range")
    smf74mvs: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="z/OS software level (consists of an acronym and the version, release, and modification level - ZV vvrrmm ).")
    r744fflg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Status Flags. Bit Meaning when set 0 Coupling facility was connected to the system at the end of the interval 1 Coupling facility became active during the interval 2 Permanent error in cycle gatherer during the complete interval 3 Dynamic dispatching is active. Valid if R744FLVL > 14. 4 Thin interrupts are enabled. Valid if R744FLVL > 18. 5 No coupling facility hardware statistics available since optimized CF HW data gathering was active. 6 - 7 Reserved.")
    r744fflc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Informational flags. Bit Meaning when set 0 No longer used. 1-7 Reserved.")
    r744famv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="IXLYAMDA Version.")
    r744fpam: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of paths available to the coupling facility.")
    r744fmod: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6),
                                                          doc="Coupling facility type. The type is right-aligned with leading blanks if necessary.")
    r744fver: so.Mapped[Optional[str]] = so.mapped_column(sa.String(3), doc="Coupling facility model.")
    r744fmpc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                          doc="Manufacturer plant code of the coupling facility.")
    r744flpn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Partition identifier of CF. Valid with SMF74SRL ≥ X'55' (85) and RMF version number SMF74MFV ≥ 718F")
    r744flvl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Coupling facility level.")
    r744fseq: so.Mapped[Optional[str]] = so.mapped_column(sa.String(12),
                                                          doc="Sequence number of this coupling facility.")
    r744fpsn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of shared processors. Valid if R744FLVL > 14.")
    r744fpdn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of dedicated processors. Valid if R744FLVL > 14.")
    r744fcei: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r744fflg (Bit 0) showing coupling facility was connected to the system at the end of interval.")
    r744fadi: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r744fflg (Bit 1) showing coupling facility became active during the interval.")
    r744fpec: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r744fflg (Bit 2) showing permanent error in cycle gatherer during the complete interval.")
    r744fdyd: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r744fflg (Bit 3) showing dynamic dispatching is active. Valid if r744flvl > 14.")
    r744fthn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r744fflg (Bit 4) showing thin interrupts are enabled. Valid if r744flvl > 18.")
    r744fnohw: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                           doc="r744fflg (Bit 5) showing no coupling facility hardware statistics available since optimized CF HW dat gathering was active.")
    r744fcho: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r744fflc (Bit 0) showing CHPIDs set offline during the interval.")
    total_str_alloc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                 doc="the total allocated size of structures (i.e. r744ssiz) (unit = 4K byte blocks).")
    total_augmented_alloc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                       doc="total fixed augmented space by all structures (i.e. r744mfau) (4K-block units).")
    total_max_scm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="the maximum amount of storage class memory of the structures can use (i.e. r744msma) (4K-block units).")
    total_processor_busy: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                        doc="total busy time of all structures (i.e. r744pbsy).")
    total_processor_wait: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                        doc="total wait time of all structures (i.e. r744pwai).")
    avg_processor_weight: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="the average processor weight.")
