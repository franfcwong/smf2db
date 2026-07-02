import datetime as dt
from typing import List, Optional

import sqlalchemy as sa
import sqlalchemy.orm as so

from .smf74_base import ReprMixin, Base74, Smf74pro, Smf74dctl, Smf74dev, Smf74cf, Smf74lcf, Smf74gsrg, Smf74proc, \
    Smf74str, Smf74sreq, Smf74cach, Smf74mscm, Smf74adup, Smf74cfrf, Smf74chpa, Smf74sys, Smf74path, Smf74mbr, \
    Smf74omvs, Smf74cachsys, Smf74cdata, Smf74cdev, Smf741dev, Smf74raid, Smf74xpool, Smf74hfs, Smf74gbuf, Smf74fsys, \
    Smf74fcd, Smf74pstat, Smf74switch, Smf74port, Smf74connector, Smf74cntl, Smf74lss, Smf74extp, Smf74rank, Smf74arry, \
    Smf74siol, Smf74pcie, Smf74dma0, Smf74dma1, Smf74dma2, Smf74dma3, Smf74dma4, Smf74hwa, Smf74hwa1, Smf74srtd, \
    Smf74scm, Smf74eadm


class Smf74Pro(ReprMixin, Base74, Smf74pro):
    """The Smf74Pro class stores the Smf74Pro section in the smf74_pro table."""

    __tablename__ = "smf74_pro"
    smf74ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf74iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")
    speed_boost: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                             doc="smf74fla (Bit 10) indcating speed boost was active during entire interval.")
    ziip_boost: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                            doc="smf74fla (Bit 9) indciating zIIP boost was active during entire interval.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf_type: so.Mapped[str] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf74sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(datetime, smf74ist, smf74iet, smf_type, csc, smf74sid),
    )

    smf74_xctl: so.Mapped["Smf74Xctl"] = so.relationship(back_populates="smf74_pro", viewonly=True)
    smf74_omvs: so.Mapped["Smf74Omvs"] = so.relationship(back_populates="smf74_pro", viewonly=True)
    smf74_hfs: so.Mapped["Smf74Hfs"] = so.relationship(back_populates="smf74_pro", viewonly=True)
    smf74_fcd: so.Mapped['Smf74Fcd'] = so.relationship(back_populates='smf74_pros', viewonly=True,
                                                       foreign_keys=[datetime, smf74ist, smf74iet, smf_type],
                                                       primaryjoin='and_(Smf74Pro.datetime==Smf74Fcd.datetime, Smf74Pro.smf74ist==Smf74Fcd.smf74ist, Smf74Pro.smf74iet==Smf74Fcd.smf74iet, Smf74Pro.smf_type==Smf74Fcd.smf_type)', )
    smf74_cntl: so.Mapped['Smf74Cntl'] = so.relationship(back_populates='smf74_pros', viewonly=True,
                                                         foreign_keys=[datetime, smf74ist, smf74iet, smf_type],
                                                         primaryjoin='and_(Smf74Pro.datetime==Smf74Cntl.datetime, Smf74Pro.smf74ist==Smf74Cntl.smf74ist, Smf74Pro.smf74iet==Smf74Cntl.smf74iet, Smf74Pro.smf_type==Smf74Cntl.smf_type)', )
    smf74_cachsys: so.Mapped['Smf74Cachsys'] = so.relationship(back_populates='smf74_pros', viewonly=True,
                                                               foreign_keys=[datetime, smf74ist, smf74iet, smf_type],
                                                               primaryjoin='and_(Smf74Pro.datetime==Smf74Cachsys.datetime, Smf74Pro.smf74ist==Smf74Cachsys.smf74ist, Smf74Pro.smf74iet==Smf74Cachsys.smf74iet, Smf74Pro.smf_type==Smf74Cachsys.smf_type)', )
    smf74_pcie: so.Mapped['Smf74Pcie'] = so.relationship(back_populates='smf74_pros', viewonly=True,
                                                         foreign_keys=[datetime, smf74ist, smf74iet, smf_type],
                                                         primaryjoin='and_(Smf74Pro.datetime==Smf74Pcie.datetime, Smf74Pro.smf74ist==Smf74Pcie.smf74ist, Smf74Pro.smf74iet==Smf74Pcie.smf74iet, Smf74Pro.smf_type==Smf74Pcie.smf_type)', )
    smf74_scm: so.Mapped['Smf74Scm'] = so.relationship(back_populates='smf74_pros', viewonly=True)
    smf74_eadm: so.Mapped['Smf74Eadm'] = so.relationship(back_populates='smf74_pros', viewonly=True)
    smf74_dctls: so.Mapped[List['Smf74Dctl']] = so.relationship(back_populates='smf74_pro', viewonly=True)
    smf74_lcfs: so.Mapped[List['Smf74Lcf']] = so.relationship(back_populates='smf74_pro', viewonly=True)


class Smf74Lcf(ReprMixin, Base74, Smf74lcf):
    """The Smf74Lcf class stores the Smf74Lcf section in the smf74_lcf table."""

    __tablename__ = "smf74_lcf"
    r744fnam: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Name of coupling facility as defined in parmlib member COUPLExx.")
    r744fpas: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="Path-available mask for CF links.")
    r744fpis: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="Path-installed mask for CF links.")
    r744fpcm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4),
                                                          doc="Composite-path mask: paths that have a physical or logical connection to the facility or that are connected to the facility in the active policy.")
    r744ftap_1: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="engine 1 - Channel path type acronym.")
    r744ftap_2: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="engine 2 - Channel path type acronym.")
    r744ftap_3: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="engine 3 - Channel path type acronym.")
    r744ftap_4: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="engine 4 - Channel path type acronym.")
    r744ftap_5: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="engine 5 - Channel path type acronym.")
    r744ftap_6: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="engine 6 - Channel path type acronym.")
    r744ftap_7: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="engine 7 - Channel path type acronym.")
    r744ftap_8: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="engine 8 - Channel path type acronym.")
    r744fidp_1: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                            doc="engine 1 - Channel path identifier. The range of values is X'00' - X'FF'.")
    r744fidp_2: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                            doc="engine 2 - Channel path identifier. The range of values is X'00' - X'FF'.")
    r744fidp_3: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                            doc="engine 3 - Channel path identifier. The range of values is X'00' - X'FF'.")
    r744fidp_4: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                            doc="engine 4 - Channel path identifier. The range of values is X'00' - X'FF'.")
    r744fidp_5: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                            doc="engine 5 - Channel path identifier. The range of values is X'00' - X'FF'.")
    r744fidp_6: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                            doc="engine 6 - Channel path identifier. The range of values is X'00' - X'FF'.")
    r744fidp_7: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                            doc="engine 7 - Channel path identifier. The range of values is X'00' - X'FF'.")
    r744fidp_8: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                            doc="engine 8 - Channel path identifier. The range of values is X'00' - X'FF'.")
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    r744fsys: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="Name of this system (from IEASYSxx parmlib member, SYSNAME parameter).")
    r744fcpi: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Index to first channel path data section associated with this coupling facility.")
    r744fcpn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of channel path data sections for channel paths of type CIB, CFP, CL5, CS5, or CL6 connected to this coupling facility. This count matches the number of subsequent channel path data sections.")
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
    total_list_r744ssrc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                     doc="total count of number of times for synchronous requests of all list structures.")
    total_cache_r744ssrc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                      doc="total count of number of times for synchronous requests of all cache structures.")
    total_lock_r744ssrc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                     doc="total count of number of times for synchronous requests of all lock structures.")
    total_list_r744sarc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                     doc="the total number of operations executed asynchronously at the coupling facility of all list structures.")
    total_cache_r744sarc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                      doc="the total number of operations executed asynchronously at the coupling facility of all cache structures.")
    total_lock_r744sarc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                     doc="the total number of operations executed asynchronously at the coupling facility of all lock structures.")
    total_list_delayed_reqs: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                           doc="total number of delayed requests of all list structures.")
    total_cache_delayed_reqs: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                            doc="total number of delayed requests of all cache structures.")
    total_lock_delayed_reqs: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                           doc="total number of delayed requests of all lock structures.")
    total_list_delay_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                         doc="total delay time of possible contention requests of all list structures.")
    total_cache_delay_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                          doc="total delay time of possible contention requests of all cache structures.")
    total_lock_delay_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                         doc="total delay time of possible contention requests of all lock structures.")
    total_list_delay_sq_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                            doc="total squared of delay time of possible contention requests of all list structures.")
    total_cache_delay_sq_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                             doc="total squared of delay time of possible contention requests of all cache structures.")
    total_lock_delay_sq_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                            doc="total squared of delay time of possible contention requests of all lock structures.")
    smf74xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf74ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf74iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")
    smf74sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf74xnm, datetime, smf74ist, smf74iet, r744fnam, smf74sid),
        sa.ForeignKeyConstraint(
            ['datetime', 'smf74ist', 'smf74iet', 'smf_type', 'csc', 'smf74sid'],
            ['smf74_pro.datetime', 'smf74_pro.smf74ist', 'smf74_pro.smf74iet', 'smf74_pro.smf_type', 'smf74_pro.csc',
             'smf74_pro.smf74sid']),
        sa.ForeignKeyConstraint(
            ['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'r744fnam'],
            ['smf74_cf.smf74xnm', 'smf74_cf.datetime', 'smf74_cf.smf74ist', 'smf74_cf.smf74iet', 'smf74_cf.r744fnam']),
    )

    smf74_cf: so.Mapped['Smf74Cf'] = so.relationship(back_populates='smf74_lcfs', viewonly=True)
    smf74_pro: so.Mapped['Smf74Pro'] = so.relationship(back_populates='smf74_lcfs', viewonly=True)
    smf74_sreqs: so.Mapped[List['Smf74Sreq']] = so.relationship(back_populates='smf74_lcf', viewonly=True)


class Smf74Arry(ReprMixin, Base74, Smf74arry):
    """The Smf74Arry class stores the Smf74Arry section in the smf74_arry table."""

    __tablename__ = "smf74_arry"
    r748aaid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Rank array identifier.")
    r748arid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Rank identifier.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf74ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf74iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")
    r748cser: so.Mapped[str] = so.mapped_column(sa.String(10), doc="Primary control unit serial number.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(datetime, smf74ist, smf74iet, r748cser, r748arid, r748aaid),
        sa.ForeignKeyConstraint(
            ['datetime', 'smf74ist', 'smf74iet', 'r748cser', 'r748arid'],
            ['smf74_rank.datetime', 'smf74_rank.smf74ist', 'smf74_rank.smf74iet', 'smf74_rank.r748cser',
             'smf74_rank.r748rrid']),
    )

    smf74_rank: so.Mapped['Smf74Rank'] = so.relationship(back_populates='smf74_arrys', viewonly=True)


class Smf74Cdev(ReprMixin, Base74, Smf74cdev, Smf741dev):
    """The Smf74Cdev class stores the Smf74Cdev section in the smf74_cdev table."""

    __tablename__ = "smf74_cdev"
    r745dvol: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Volume serial of device")
    r745dfl4: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Flags Bit Meaning when set 0 4-digit device address. 1 Reserved. 2-3 Subchannel set ID: 00 = Subchannel set ID 0 01 = Subchannel set ID 1 10 = Subchannel set ID 2 11 = Subchannel set ID 3 4-7")
    r745dcid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="Real control unit type code.")
    r745dccu: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4),
                                                          doc="Configured control unit type code if R745CMDL = 1.")
    r745dunt: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Unit address for sense command.")
    r745devn: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Device number.")
    r745dflg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Flags Bit Meaning when set 0 Cache storage is not available; set to 0 for DS8000. 1-3 Format of data returned: B'000' = 3990 format B'001' = DS8000 disk controller format 4-7 Format of data returned: B'0000' = 3990 Models 1, 2, and 3, or Basic Operation Mode B'0001' = 3990-6 Enhanced Operation Mode 1, or host supports DS8000 disk ")
    r745dvid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="Device address.")
    r745dvs1: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Addressed device status flag # 1: Bit Meaning 0-1 Device caching status: B'00' = Caching activated. 2-3 DASD fast write device status: B'00' = DFW allowed. 4 PPRC copy pair suspended. 5 PPRC copy pair is duplex pending. 6-7 PPRC pair status: B'00' = PPRC pair available (full duplex). B'01' = PPRC pair pending. B'10' = Not used.. B'11' = Suspended.")
    r745dvs2: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="Addressed device status flag # 2. If R745SFT = 0: Bit Meaning 0 - 1 Pinned data: B'00' = No pinned data exists for the device. B'01' = Pinned data exists for the device. B'10' = Reserved. B'11' = Not used. 2 - 5 Not used. 6 Advanced FlashCopy enabled. 7 FlashCopy full volume enabled. If R745SFT = 1 or 2: Bit Meaning 0 - 2 Global Mirror state: B'000' = No Global Mirror configured. B'001' = Global Mirror running - optimal. B'010' = Global Mirror running - suboptimal. B'011' = Global Mirror running - consistency groups failing. B'100' = Global Mirror paused. B'101' = Global Mirror fatal. B'110' = More than one Global Mirror session is running. B'111' = Reserved. 3 Session member is pending. 4 Volume not allowed online. 5 Not used. 6 Advanced FlashCopy enabled. 7 FlashCopy full volume enabled.")
    r745dsg2: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Device status group 2. Bit Meaning 0-1 Volume space management: B'00' = Standard volume B'01' = Track space efficient volume B'10' = Extent space efficient volume B'11' = Reserved. 2 Data exits in failed NVS. 3 Device in a soft fenced state. 4 Reserved. 5 Reserved. 6-7 (if R745SFT = 1 or 2) Pinned data: B'00' = No pinned data exists for the device. B'01' = Pinned data exists for the device. B'10' = Reserved. B'11' = Not used.")
    r745incr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Reserved.")
    r745dsid: so.Mapped[str] = so.mapped_column(sa.String(6), doc="Subsystem ID.")
    r7452pro: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Physical storage read operations.")
    r7452pwo: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Physical storage write operations.")
    r7452pbr: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Physical storage bytes read. For units, see bits 5 and 6 of R7451INC.")
    r7452pbw: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Physical storage bytes written. For units, see bits 5 and 6 of R7451INC.")
    r7452prt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Physical storage read response time. For units, see bits 5 and 6 of R7451INC.")
    r7452pwt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Physical storage write response time. For units, see bits 5 and 6 of R7451INC.")
    r7451rrq: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="RAID rank read requests.")
    r7451wrq: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="RAID rank write requests.")
    r7451sr: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="RAID rank FB sectors read.")
    r7451sw: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="RAID rank FB sectors written.")
    r7451rrt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="RAID rank read response time (in milliseconds).")
    r7451wrt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="RAID rank write response time (in milliseconds).")
    r745dev4: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r745dfl4 (Bit 0) indicating 4-digit device address.")
    r745dscs: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                          doc="r745dfl4 (Bit 2-3) indciating subchannel set ID.")
    r745dnav: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r745dflg (Bit 0) indicating cache storage is not available; set to 0 for DS8000.")
    r745dpdf: so.Mapped[Optional[str]] = so.mapped_column(sa.String(3),
                                                          doc="r745dflg (Bit 1-3) indicating format of data returned.")
    r745dfrm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4),
                                                          doc="r745dflg (Bit 4-7) indicating format of data returned.")
    r745dsdv: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                          doc="r745dflg (Bit 0-1) indicating device caching status.")
    r745dsfw: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                          doc="r745dflg (Bit 2-3) indicating DASD fast write device status.")
    r745dspd: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r745dflg (Bit 4) indicating PPRC copy pair suspended.")
    r745dssd: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r745dflg (Bit 5) indicating PPRC copy pair is duplex pending.")
    r745dsdp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r745dflg (Bit 6-7) indicating PPRC pair status.")
    r745dcol: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                          doc="r745dsg2 (Bit 0-1) indicating volume space management.")
    r745defn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r745dsg2 (Bit 2) indicating data exists in failed NVS.")
    r745dbdp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="r745dsg2 (Bit 3) indicating device in a soft fenced state.")
    r745dpdt: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                          doc="r745dsg2 (Bit 6-7) indicating pinned data.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf74ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf74iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")

    __table_args__ = (
        sa.PrimaryKeyConstraint(datetime, smf74ist, smf74iet, r745dsid, r745devn),
        sa.ForeignKeyConstraint(
            ['datetime', 'smf74ist', 'smf74iet', 'r745dsid'],
            ['smf74_cachsys.datetime', 'smf74_cachsys.smf74ist', 'smf74_cachsys.smf74iet', 'smf74_cachsys.r745ssid']),
    )

    smf74_raid: so.Mapped["Smf74Raid"] = so.relationship(back_populates="smf74_cdev", viewonly=True)
    smf74_xpool: so.Mapped["Smf74Xpool"] = so.relationship(back_populates="smf74_cdev", viewonly=True)
    smf74_cachsys: so.Mapped['Smf74Cachsys'] = so.relationship(back_populates='smf74_cdevs', viewonly=True)


class Smf74Rank(ReprMixin, Base74, Smf74rank, Smf74arry):
    """The Smf74Rank class stores the Smf74Rank section in the smf74_rank table."""

    __tablename__ = "smf74_rank"
    r748rrid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Rank identifier.")
    r748rpnm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="Extent pool number.")
    r748raix: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Index to first Array section of rank.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf74ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf74iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")
    r748cser: so.Mapped[str] = so.mapped_column(sa.String(10), doc="Primary control unit serial number.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(datetime, smf74ist, smf74iet, r748cser, r748rrid),
        sa.ForeignKeyConstraint(
            ['datetime', 'smf74ist', 'smf74iet', 'r748cser'],
            ['smf74_cntl.datetime', 'smf74_cntl.smf74ist', 'smf74_cntl.smf74iet', 'smf74_cntl.r748cser']),
        sa.ForeignKeyConstraint(
            ['datetime', 'smf74ist', 'smf74iet', 'r748cser', 'r748rpnm'],
            ['smf74_extp.datetime', 'smf74_extp.smf74ist', 'smf74_extp.smf74iet', 'smf74_extp.r748cser',
             'smf74_extp.r748xpid']),
    )

    smf74_cntl: so.Mapped['Smf74Cntl'] = so.relationship(back_populates='smf74_ranks', viewonly=True)
    smf74_extp: so.Mapped['Smf74Extp'] = so.relationship(back_populates='smf74_ranks', viewonly=True)
    smf74_arrys: so.Mapped[List['Smf74Arry']] = so.relationship(back_populates='smf74_rank', viewonly=True)


class Smf74Xpool(ReprMixin, Base74, Smf74xpool, Smf741dev):
    """The Smf74Xpool class stores the Smf74Xpool section in the smf74_xpool table."""

    __tablename__ = "smf74_xpool"
    r748xpid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="Extent pool identifier.")
    ccmt_seqn: so.Mapped[Optional[str]] = so.mapped_column(sa.String(10),
                                                           doc="the sequence number of the subsystem control unit.")
    r745dvol: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Volume serial of device")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf74ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf74iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")
    r745ssid: so.Mapped[str] = so.mapped_column(sa.String(6), doc="Subsystem ID.")
    r7451dvn: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Device number (binary).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(datetime, smf74ist, smf74iet, r745ssid, r7451dvn),
        sa.ForeignKeyConstraint(
            ['datetime', 'smf74ist', 'smf74iet', 'r745ssid', 'r7451dvn'],
            ['smf74_cdev.datetime', 'smf74_cdev.smf74ist', 'smf74_cdev.smf74iet', 'smf74_cdev.r745dsid',
             'smf74_cdev.r745devn']),
    )

    smf74_cdev: so.Mapped["Smf74Cdev"] = so.relationship(back_populates="smf74_xpool", viewonly=True)


class Smf74Adup(ReprMixin, Base74, Smf74adup):
    """The Smf74Adup class stores the Smf74Adup section in the smf74_adup table."""

    __tablename__ = "smf74_adup"
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf74xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf74ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf74iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")
    r744fnam: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Name of coupling facility as defined in parmlib member COUPLExx.")
    r744snam: so.Mapped[str] = so.mapped_column(sa.String(16),
                                                doc="Name of connected structure in this coupling facility.")
    smf74sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf74xnm, datetime, smf74ist, smf74iet, r744fnam, r744snam, smf74sid),
        sa.ForeignKeyConstraint(
            ['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'r744fnam', 'r744snam', 'smf74sid'],
            ['smf74_sreq.smf74xnm', 'smf74_sreq.datetime', 'smf74_sreq.smf74ist', 'smf74_sreq.smf74iet',
             'smf74_sreq.r744fnam', 'smf74_sreq.r744snam', 'smf74_sreq.smf74sid']),
        sa.ForeignKeyConstraint(
            ['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'r744fnam', 'r744snam'],
            ['smf74_str.smf74xnm', 'smf74_str.datetime', 'smf74_str.smf74ist', 'smf74_str.smf74iet',
             'smf74_str.r744fnam', 'smf74_str.r744qstr']),
    )

    smf74_sreq: so.Mapped['Smf74Sreq'] = so.relationship(back_populates='smf74_adups', viewonly=True)
    smf74_str: so.Mapped['Smf74Str'] = so.relationship(back_populates='smf74_adups', viewonly=True)


class Smf74Cach(ReprMixin, Base74, Smf74cach):
    """The Smf74Cach class stores the Smf74Cach section in the smf74_cach table."""

    __tablename__ = "smf74_cach"
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    cach_idx: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="the location of the Cache Data Section in the SMF record.")
    smf74xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf74ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf74iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")
    r744fnam: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Name of coupling facility as defined in parmlib member COUPLExx.")
    r744snam: so.Mapped[str] = so.mapped_column(sa.String(16),
                                                doc="Name of connected structure in this coupling facility.")
    smf74sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf74xnm, datetime, smf74ist, smf74iet, r744fnam, r744snam, smf74sid, cach_idx),
        sa.ForeignKeyConstraint(
            ['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'r744fnam', 'r744snam', 'smf74sid'],
            ['smf74_sreq.smf74xnm', 'smf74_sreq.datetime', 'smf74_sreq.smf74ist', 'smf74_sreq.smf74iet',
             'smf74_sreq.r744fnam', 'smf74_sreq.r744snam', 'smf74_sreq.smf74sid']),
    )

    smf74_sreq: so.Mapped['Smf74Sreq'] = so.relationship(back_populates='smf74_cachs', viewonly=True)


class Smf74Cachsys(ReprMixin, Base74, Smf74cachsys, Smf74cdata, Smf74cdev, Smf741dev):
    """The Smf74Cachsys class stores the Smf74Cachsys section in the smf74_cachsys table."""

    __tablename__ = "smf74_cachsys"
    r745ccnt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Record sequence number.")
    ccmt_seqn: so.Mapped[Optional[str]] = so.mapped_column(sa.String(10),
                                                           doc="the sequence number of the subsystem control unit.")
    smf_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    r7452pro: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Physical storage read operations.")
    r7452pwo: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Physical storage write operations.")
    r7452pbr: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Physical storage bytes read. For units, see bits 5 and 6 of R7451INC.")
    r7452pbw: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Physical storage bytes written. For units, see bits 5 and 6 of R7451INC.")
    r7452prt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Physical storage read response time. For units, see bits 5 and 6 of R7451INC.")
    r7452pwt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Physical storage write response time. For units, see bits 5 and 6 of R7451INC.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf74ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf74iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")
    r745ssid: so.Mapped[str] = so.mapped_column(sa.String(6), doc="Subsystem ID.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(datetime, smf74ist, smf74iet, r745ssid),
    )

    smf74_pros: so.Mapped[List['Smf74Pro']] = so.relationship(back_populates='smf74_cachsys', viewonly=True,
                                                              foreign_keys='Smf74Pro.datetime, Smf74Pro.smf74ist, Smf74Pro.smf74iet, Smf74Pro.smf_type',
                                                              primaryjoin='and_(Smf74Cachsys.datetime==Smf74Pro.datetime, Smf74Cachsys.smf74ist==Smf74Pro.smf74ist, Smf74Cachsys.smf74iet==Smf74Pro.smf74iet, Smf74Cachsys.smf_type==Smf74Pro.smf_type)', )
    smf74_cdevs: so.Mapped[List['Smf74Cdev']] = so.relationship(back_populates='smf74_cachsys', viewonly=True)
    smf74_rranks: so.Mapped[List['Smf74Rrank']] = so.relationship(back_populates='smf74_cachsys', viewonly=True)


class Smf74Cfrf(ReprMixin, Base74, Smf74cfrf):
    """The Smf74Cfrf class stores the Smf74Cfrf section in the smf74_cfrf table."""

    __tablename__ = "smf74_cfrf"
    r744rsys: so.Mapped[Optional[str]] = so.mapped_column(sa.String(18),
                                                          doc="System identification value for the remotely connected CF.")
    r744rnam: so.Mapped[str] = so.mapped_column(sa.String(8), doc="CF name (if applicable, else X'0').")
    r744rpgs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Receiver path group size.")
    r744rflg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Status flags: Bit Meaning when set 0 CF remote facility was connected at the end of the interval. 1")
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    ndepartition: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="r744rnde indicating the partition number of the remotely connected CF.")
    smf74xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf74ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf74iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")
    r744fnam: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Name of coupling facility as defined in parmlib member COUPLExx.")
    smf74sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf74xnm, datetime, smf74ist, smf74iet, r744fnam, r744rnam, smf74sid),
        sa.ForeignKeyConstraint(
            ['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'r744fnam'],
            ['smf74_cf.smf74xnm', 'smf74_cf.datetime', 'smf74_cf.smf74ist', 'smf74_cf.smf74iet', 'smf74_cf.r744fnam']),
    )

    smf74_cf: so.Mapped['Smf74Cf'] = so.relationship(back_populates='smf74_cfrfs', viewonly=True)
    smf74_dupchpas: so.Mapped[List['Smf74Dupchpa']] = so.relationship(back_populates='smf74_cfrf', viewonly=True)


class Smf74Dupchpa(ReprMixin, Base74, Smf74chpa):
    """The Smf74Dupchpa class stores the Smf74Dupchpa section in the smf74_dupchpa table."""

    __tablename__ = "smf74_dupchpa"
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf74xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf74ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf74iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")
    r744fnam: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Name of coupling facility as defined in parmlib member COUPLExx.")
    r744rnam: so.Mapped[str] = so.mapped_column(sa.String(8), doc="CF name (if applicable, else X'0').")
    r744hcpi: so.Mapped[str] = so.mapped_column(sa.String(2),
                                                doc="Channel path identifier. The range of values is X'00' to X'FF'.")
    r744hsnd: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="r744hchf (Bit 1) showing channel path is a sender channel.")
    smf74sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf74xnm, datetime, smf74ist, smf74iet, r744fnam, r744rnam, r744hcpi, r744hsnd,
                                smf74sid),
        sa.ForeignKeyConstraint(
            ['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'r744fnam', 'r744rnam', 'smf74sid'],
            ['smf74_cfrf.smf74xnm', 'smf74_cfrf.datetime', 'smf74_cfrf.smf74ist', 'smf74_cfrf.smf74iet',
             'smf74_cfrf.r744fnam', 'smf74_cfrf.r744rnam', 'smf74_cfrf.smf74sid']),
    )

    smf74_cfrf: so.Mapped['Smf74Cfrf'] = so.relationship(back_populates='smf74_dupchpas', viewonly=True)


class Smf74Subchpa(ReprMixin, Base74, Smf74chpa):
    """The Smf74Subchpa class stores the Smf74Subchpa section in the smf74_subchpa table."""

    __tablename__ = "smf74_subchpa"
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf74xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf74ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf74iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")
    r744fnam: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Name of coupling facility as defined in parmlib member COUPLExx.")
    smf74sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    r744hcpi: so.Mapped[str] = so.mapped_column(sa.String(2),
                                                doc="Channel path identifier. The range of values is X'00' to X'FF'.")
    r744hsnd: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="r744hchf (Bit 1) showing channel path is a sender channel.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf74xnm, datetime, smf74ist, smf74iet, r744fnam, smf74sid, r744hcpi, r744hsnd),
        sa.ForeignKeyConstraint(
            ['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'r744fnam'],
            ['smf74_cf.smf74xnm', 'smf74_cf.datetime', 'smf74_cf.smf74ist', 'smf74_cf.smf74iet', 'smf74_cf.r744fnam']),
    )

    smf74_cf: so.Mapped['Smf74Cf'] = so.relationship(back_populates='smf74_subchpas', viewonly=True)


class Smf74Cntl(ReprMixin, Base74, Smf74cntl):
    """The Smf74Cntl class stores the Smf74Cntl section in the smf74_cntl table."""

    __tablename__ = "smf74_cntl"
    r748cser: so.Mapped[str] = so.mapped_column(sa.String(10), doc="Primary control unit serial number.")
    smf_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf74ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf74iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")

    __table_args__ = (
        sa.PrimaryKeyConstraint(datetime, smf74ist, smf74iet, r748cser),
    )

    smf74_pros: so.Mapped[List['Smf74Pro']] = so.relationship(back_populates='smf74_cntl', viewonly=True,
                                                              foreign_keys='Smf74Pro.datetime, Smf74Pro.smf74ist, Smf74Pro.smf74iet, Smf74Pro.smf_type',
                                                              primaryjoin='and_(Smf74Cntl.datetime==Smf74Pro.datetime, Smf74Cntl.smf74ist==Smf74Pro.smf74ist, Smf74Cntl.smf74iet==Smf74Pro.smf74iet, Smf74Cntl.smf_type==Smf74Pro.smf_type)', )
    smf74_lsss: so.Mapped[List['Smf74Lss']] = so.relationship(back_populates='smf74_cntl', viewonly=True)
    smf74_extps: so.Mapped[List['Smf74Extp']] = so.relationship(back_populates='smf74_cntl', viewonly=True)
    smf74_ranks: so.Mapped[List['Smf74Rank']] = so.relationship(back_populates='smf74_cntl', viewonly=True)
    smf74_siols: so.Mapped[List['Smf74Siol']] = so.relationship(back_populates='smf74_cntl', viewonly=True)


class Smf74Connector(ReprMixin, Base74, Smf74connector):
    """The Smf74Connector class stores the Smf74Connector section in the smf74_connector table."""

    __tablename__ = "smf74_connector"
    r747cnum: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Port number.")
    r747cadr: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Port address.")
    r747ccu: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Connector id (CU).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf74ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf74iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")
    r747sdev: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Switch device number.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(datetime, smf74ist, smf74iet, r747sdev, r747cadr, r747cnum, r747ccu),
        sa.ForeignKeyConstraint(
            ['datetime', 'smf74ist', 'smf74iet', 'r747sdev', 'r747cadr', 'r747cnum'],
            ['smf74_port.datetime', 'smf74_port.smf74ist', 'smf74_port.smf74iet', 'smf74_port.r747sdev',
             'smf74_port.r747padr', 'smf74_port.r747pnum']),
    )

    smf74_port: so.Mapped['Smf74Port'] = so.relationship(back_populates='smf74_connectors', viewonly=True)


class Smf74Dctl(ReprMixin, Base74, Smf74dctl):
    """The Smf74Dctl class stores the Smf74Dctl section in the smf74_dctl table."""

    __tablename__ = "smf74_dctl"
    smf74sub: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="Device class code: Bit Configuration Meaning X'0080' Magnetic tape device X'0040' Communication equipment X'0020' Direct access devices X'0010' Graphics devices X'0008' Unit record devices X'0004' Character reader devices.")
    smf_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    msm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                     doc="smf74smf (Bit 0) indicating there are more logical SMF records for this device class.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf74sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf74ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf74iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf74sid, datetime, smf74ist, smf74iet, smf74sub),
        sa.ForeignKeyConstraint(
            ['datetime', 'smf74ist', 'smf74iet', 'smf_type', 'csc', 'smf74sid'],
            ['smf74_pro.datetime', 'smf74_pro.smf74ist', 'smf74_pro.smf74iet', 'smf74_pro.smf_type', 'smf74_pro.csc',
             'smf74_pro.smf74sid']),
    )

    smf74_pro: so.Mapped['Smf74Pro'] = so.relationship(back_populates='smf74_dctls', viewonly=True)
    smf74_devs: so.Mapped[List['Smf74Dev']] = so.relationship(back_populates='smf74_dctl', viewonly=True)


class Smf74Dev(ReprMixin, Base74, Smf74dev):
    """The Smf74Dev class stores the Smf74Dev section in the smf74_dev table."""

    __tablename__ = "smf74_dev"
    smf74num: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Device number, in the range X'0000' to X'FFFF'.")
    smf74lcu: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="Logical control unit number, in the range X'0000' to X'FFFF'.")
    smf74scs: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Subchannel set ID.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf74sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf74ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf74iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")
    smf74sub: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="Device class code: Bit Configuration Meaning X'0080' Magnetic tape device X'0040' Communication equipment X'0020' Direct access devices X'0010' Graphics devices X'0008' Unit record devices X'0004' Character reader devices.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf74sid, datetime, smf74ist, smf74iet, smf74sub, smf74lcu, smf74scs, smf74num),
        sa.ForeignKeyConstraint(
            ['csc', 'smf74sid', 'datetime', 'smf74ist', 'smf74iet', 'smf74sub'],
            ['smf74_dctl.csc', 'smf74_dctl.smf74sid', 'smf74_dctl.datetime', 'smf74_dctl.smf74ist',
             'smf74_dctl.smf74iet', 'smf74_dctl.smf74sub']),
    )

    smf74_dctl: so.Mapped['Smf74Dctl'] = so.relationship(back_populates='smf74_devs', viewonly=True)


class Smf74Eadm(ReprMixin, Base74, Smf74eadm):
    """The Smf74Eadm class stores the Smf74Eadm section in the smf74_eadm table."""

    __tablename__ = "smf74_eadm"
    smf_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf74sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf74ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf74iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf74sid, datetime, smf74ist, smf74iet),
        sa.ForeignKeyConstraint(
            ['datetime', 'smf74ist', 'smf74iet', 'smf_type', 'csc', 'smf74sid'],
            ['smf74_pro.datetime', 'smf74_pro.smf74ist', 'smf74_pro.smf74iet', 'smf74_pro.smf_type', 'smf74_pro.csc',
             'smf74_pro.smf74sid']),
    )

    smf74_pros: so.Mapped[List['Smf74Pro']] = so.relationship(back_populates='smf74_eadm', viewonly=True)


class Smf74Extp(ReprMixin, Base74, Smf74extp, Smf74rank, Smf74arry):
    """The Smf74Extp class stores the Smf74Extp section in the smf74_extp table."""

    __tablename__ = "smf74_extp"
    r748xpid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Extent pool identifier.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf74ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf74iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")
    r748cser: so.Mapped[str] = so.mapped_column(sa.String(10), doc="Primary control unit serial number.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(datetime, smf74ist, smf74iet, r748cser, r748xpid),
        sa.ForeignKeyConstraint(
            ['datetime', 'smf74ist', 'smf74iet', 'r748cser'],
            ['smf74_cntl.datetime', 'smf74_cntl.smf74ist', 'smf74_cntl.smf74iet', 'smf74_cntl.r748cser']),
    )

    smf74_cntl: so.Mapped['Smf74Cntl'] = so.relationship(back_populates='smf74_extps', viewonly=True)
    smf74_ranks: so.Mapped[List['Smf74Rank']] = so.relationship(back_populates='smf74_extp', viewonly=True)


class Smf74Fcd(ReprMixin, Base74, Smf74fcd, Smf74pstat):
    """The Smf74Fcd class stores the Smf74Fcd section in the smf74_fcd table."""

    __tablename__ = "smf74_fcd"
    smf_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf74ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf74iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")

    __table_args__ = (
        sa.PrimaryKeyConstraint(datetime, smf74ist, smf74iet),
    )

    smf74_pros: so.Mapped[List['Smf74Pro']] = so.relationship(back_populates='smf74_fcd', viewonly=True,
                                                              foreign_keys='Smf74Pro.datetime, Smf74Pro.smf74ist, Smf74Pro.smf74iet, Smf74Pro.smf_type',
                                                              primaryjoin='and_(Smf74Fcd.datetime==Smf74Pro.datetime, Smf74Fcd.smf74ist==Smf74Pro.smf74ist, Smf74Fcd.smf74iet==Smf74Pro.smf74iet, Smf74Fcd.smf_type==Smf74Pro.smf_type)', )
    smf74_switchs: so.Mapped[List['Smf74Switch']] = so.relationship(back_populates='smf74_fcd', viewonly=True)


class Smf74Fsys(ReprMixin, Base74, Smf74fsys):
    """The Smf74Fsys class stores the Smf74Fsys section in the smf74_fsys table."""

    __tablename__ = "smf74_fsys"
    r746fsnm: so.Mapped[str] = so.mapped_column(sa.String(44), doc="File system name (cataloged dataset name).")
    r746fctm: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                  doc="Current time stamp (when was data obtained).")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf74sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf74ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf74iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf74sid, datetime, smf74ist, smf74iet, r746fsnm),
        sa.ForeignKeyConstraint(
            ['csc', 'smf74sid', 'datetime', 'smf74ist', 'smf74iet'],
            ['smf74_hfs.csc', 'smf74_hfs.smf74sid', 'smf74_hfs.datetime', 'smf74_hfs.smf74ist', 'smf74_hfs.smf74iet']),
    )

    smf74_hfs: so.Mapped['Smf74Hfs'] = so.relationship(back_populates='smf74_fsyss', viewonly=True)


class Smf74Gbuf(ReprMixin, Base74, Smf74gbuf):
    """The Smf74Gbuf class stores the Smf74Gbuf section in the smf74_gbuf table."""

    __tablename__ = "smf74_gbuf"
    pool_number: so.Mapped[int] = so.mapped_column(sa.Integer, doc="buffer pool number.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf74sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf74ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf74iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf74sid, datetime, smf74ist, smf74iet, pool_number),
        sa.ForeignKeyConstraint(
            ['csc', 'smf74sid', 'datetime', 'smf74ist', 'smf74iet'],
            ['smf74_hfs.csc', 'smf74_hfs.smf74sid', 'smf74_hfs.datetime', 'smf74_hfs.smf74ist', 'smf74_hfs.smf74iet']),
    )

    smf74_hfs: so.Mapped['Smf74Hfs'] = so.relationship(back_populates='smf74_gbufs', viewonly=True)


class Smf74Hfs(ReprMixin, Base74, Smf74hfs):
    """The Smf74Hfs class stores the Smf74Hfs section in the smf74_hfs table."""

    __tablename__ = "smf74_hfs"
    smf_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf74sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf74ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf74iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf74sid, datetime, smf74ist, smf74iet),
        sa.ForeignKeyConstraint(
            ['datetime', 'smf74ist', 'smf74iet', 'smf_type', 'csc', 'smf74sid'],
            ['smf74_pro.datetime', 'smf74_pro.smf74ist', 'smf74_pro.smf74iet', 'smf74_pro.smf_type', 'smf74_pro.csc',
             'smf74_pro.smf74sid']),
    )

    smf74_pro: so.Mapped["Smf74Pro"] = so.relationship(back_populates="smf74_hfs", viewonly=True)
    smf74_gbufs: so.Mapped[List['Smf74Gbuf']] = so.relationship(back_populates='smf74_hfs', viewonly=True)
    smf74_fsyss: so.Mapped[List['Smf74Fsys']] = so.relationship(back_populates='smf74_hfs', viewonly=True)


class Smf74Lss(ReprMixin, Base74, Smf74lss):
    """The Smf74Lss class stores the Smf74Lss section in the smf74_lss table."""

    __tablename__ = "smf74_lss"
    r748laid: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Adapter ID.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf74ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf74iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")
    r748cser: so.Mapped[str] = so.mapped_column(sa.String(10), doc="Primary control unit serial number.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(datetime, smf74ist, smf74iet, r748cser, r748laid),
        sa.ForeignKeyConstraint(
            ['datetime', 'smf74ist', 'smf74iet', 'r748cser'],
            ['smf74_cntl.datetime', 'smf74_cntl.smf74ist', 'smf74_cntl.smf74iet', 'smf74_cntl.r748cser']),
    )

    smf74_cntl: so.Mapped['Smf74Cntl'] = so.relationship(back_populates='smf74_lsss', viewonly=True)


class Smf74Mbr(ReprMixin, Base74, Smf74mbr):
    """The Smf74Mbr class stores the Smf74Mbr section in the smf74_mbr table."""

    __tablename__ = "smf74_mbr"
    r742msys: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="System name (as defined in parmlib member IEASYSxx SYSNAME parameter) where the member resides.")
    r742mgrp: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Group name.")
    r742mmem: so.Mapped[str] = so.mapped_column(sa.String(16), doc="Member name.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf74sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf74ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf74iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf74sid, datetime, smf74ist, smf74iet, r742mgrp, r742mmem, r742msys),
        sa.ForeignKeyConstraint(
            ['csc', 'smf74sid', 'datetime', 'smf74ist', 'smf74iet'],
            ['smf74_xctl.csc', 'smf74_xctl.smf74sid', 'smf74_xctl.datetime', 'smf74_xctl.smf74ist',
             'smf74_xctl.smf74iet']),
    )

    smf74_xctl: so.Mapped['Smf74Xctl'] = so.relationship(back_populates='smf74_mbrs', viewonly=True)


class Smf74Mscm(ReprMixin, Base74, Smf74mscm):
    """The Smf74Mscm class stores the Smf74Mscm section in the smf74_mscm table."""

    __tablename__ = "smf74_mscm"
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf74xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf74ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf74iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")
    r744fnam: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Name of coupling facility as defined in parmlib member COUPLExx.")
    r744snam: so.Mapped[str] = so.mapped_column(sa.String(16),
                                                doc="Name of connected structure in this coupling facility.")
    smf74sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf74xnm, datetime, smf74ist, smf74iet, r744fnam, r744snam, smf74sid),
        sa.ForeignKeyConstraint(
            ['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'r744fnam', 'r744snam', 'smf74sid'],
            ['smf74_sreq.smf74xnm', 'smf74_sreq.datetime', 'smf74_sreq.smf74ist', 'smf74_sreq.smf74iet',
             'smf74_sreq.r744fnam', 'smf74_sreq.r744snam', 'smf74_sreq.smf74sid']),
        sa.ForeignKeyConstraint(
            ['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'r744fnam'],
            ['smf74_cf.smf74xnm', 'smf74_cf.datetime', 'smf74_cf.smf74ist', 'smf74_cf.smf74iet', 'smf74_cf.r744fnam']),
        sa.ForeignKeyConstraint(
            ['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'r744fnam', 'r744snam'],
            ['smf74_str.smf74xnm', 'smf74_str.datetime', 'smf74_str.smf74ist', 'smf74_str.smf74iet',
             'smf74_str.r744fnam', 'smf74_str.r744qstr']),
    )

    smf74_sreq: so.Mapped['Smf74Sreq'] = so.relationship(back_populates='smf74_mscms', viewonly=True)
    smf74_str: so.Mapped['Smf74Str'] = so.relationship(back_populates='smf74_mscms', viewonly=True)
    smf74_cf: so.Mapped['Smf74Cf'] = so.relationship(back_populates='smf74_mscms', viewonly=True)


class Smf74Omvs(ReprMixin, Base74, Smf74omvs):
    """The Smf74Omvs class stores the Smf74Omvs section in the smf74_omvs table."""

    __tablename__ = "smf74_omvs"
    smf_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf74sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf74ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf74iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf74sid, datetime, smf74ist, smf74iet),
        sa.ForeignKeyConstraint(
            ['datetime', 'smf74ist', 'smf74iet', 'smf_type', 'csc', 'smf74sid'],
            ['smf74_pro.datetime', 'smf74_pro.smf74ist', 'smf74_pro.smf74iet', 'smf74_pro.smf_type', 'smf74_pro.csc',
             'smf74_pro.smf74sid']),
    )

    smf74_pro: so.Mapped["Smf74Pro"] = so.relationship(back_populates="smf74_omvs", viewonly=True)


class Smf74Path(ReprMixin, Base74, Smf74path):
    """The Smf74Path class stores the Smf74Path section in the smf74_path table."""

    __tablename__ = "smf74_path"
    r742pnme: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="System name as defined in parmlib member IEASYSxx SYSNAME parameter.")
    r742pdir: so.Mapped[str] = so.mapped_column(sa.String(3),
                                                doc="Direction path Bit Meaning when set 0 Inbound path 1 Outbound path 2-7")
    r742ptyp: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="Path type indicator. Value Meaning 1 CTC 3 List structure.")
    r742pona: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Name of system on other end if known, otherwise blanks.")
    r742ptcn: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Transport class name For an outbound path, the class to which the path is assigned. For an inbound path, the class to which the outbound side of the path is assigned, blanks if not known.")
    r742pstr: so.Mapped[str] = so.mapped_column(sa.String(16),
                                                doc="Name of XES list structure being used as a path, blank for CTCs.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf74sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf74ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf74iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf74sid, datetime, smf74ist, smf74iet, r742pnme, r742pdir, r742pona, r742ptyp,
                                r742pstr, r742ptcn),
        sa.ForeignKeyConstraint(
            ['csc', 'smf74sid', 'datetime', 'smf74ist', 'smf74iet'],
            ['smf74_xctl.csc', 'smf74_xctl.smf74sid', 'smf74_xctl.datetime', 'smf74_xctl.smf74ist',
             'smf74_xctl.smf74iet']),
    )

    smf74_xctl: so.Mapped['Smf74Xctl'] = so.relationship(back_populates='smf74_paths', viewonly=True)


class Smf74Pcie(ReprMixin, Base74, Smf74pcie, Smf74dma0, Smf74dma1, Smf74dma2, Smf74dma3, Smf74dma4, Smf74hwa,
                Smf74hwa1):
    """The Smf74Pcie class stores the Smf74Pcie section in the smf74_pcie table."""

    __tablename__ = "smf74_pcie"
    r749pfid: so.Mapped[str] = so.mapped_column(sa.String(10),
                                                doc="PCIE Function ID (PFID) for the PCIE function for which performance data is returned.")
    smf_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf74sid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4),
                                                          doc="System identification (from the SMFPRMxx SID parameter).")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf74ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf74iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")

    __table_args__ = (
        sa.PrimaryKeyConstraint(datetime, smf74ist, smf74iet, r749pfid),
    )

    smf74_pros: so.Mapped[List['Smf74Pro']] = so.relationship(back_populates='smf74_pcie', viewonly=True,
                                                              foreign_keys='Smf74Pro.datetime, Smf74Pro.smf74ist, Smf74Pro.smf74iet, Smf74Pro.smf_type',
                                                              primaryjoin='and_(Smf74Pcie.datetime==Smf74Pro.datetime, Smf74Pcie.smf74ist==Smf74Pro.smf74ist, Smf74Pcie.smf74iet==Smf74Pro.smf74iet, Smf74Pcie.smf_type==Smf74Pro.smf_type)', )
    smf74_srtds: so.Mapped[List['Smf74Srtd']] = so.relationship(back_populates='smf74_pcie', viewonly=True)


class Smf74Port(ReprMixin, Base74, Smf74port, Smf74pstat):
    """The Smf74Port class stores the Smf74Port section in the smf74_port table."""

    __tablename__ = "smf74_port"
    smf74sid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4),
                                                          doc="System identification (from the SMFPRMxx SID parameter).")
    r747pnpc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of Connector sections.")
    r747pxpc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Index of first Connector section.")
    r747ptfl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Port type flags. Bit Meaning when set Port type is single CU. Port type is multiple CU. Port type is CHPID. Port type is switch. 4-7 Reserved.")
    r747psfl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Status flags. Bit Meaning when set 0 Port type is not unique. 1 ID is not unique or not known. 2 Channel on caller's system. 3 Port installed. 4 Port status changed. 5 Port has been removed. 6 Port has been activated. 7 No measurement data available for this port.")
    r747ppfl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Bit Meaning when set 0 Port information was returned at least once for this port. 1 Port information showed this port not installed. 2 Port information showed link failure condition. 3 Port information showed this port offline. 4 Statistics were returned at least once for this port. 5-7 Reserved.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf74ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf74iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")
    r747sdev: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Switch device number.")
    r747padr: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Port address.")
    r747pnum: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Port number.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(datetime, smf74ist, smf74iet, r747sdev, r747padr, r747pnum),
        sa.ForeignKeyConstraint(
            ['datetime', 'smf74ist', 'smf74iet', 'r747sdev'],
            ['smf74_switch.datetime', 'smf74_switch.smf74ist', 'smf74_switch.smf74iet', 'smf74_switch.r747sdev']),
    )

    smf74_switch: so.Mapped['Smf74Switch'] = so.relationship(back_populates='smf74_ports', viewonly=True)
    smf74_connectors: so.Mapped[List['Smf74Connector']] = so.relationship(back_populates='smf74_port', viewonly=True)


class Smf74Proc(ReprMixin, Base74, Smf74proc):
    """The Smf74Proc class stores the Smf74Proc section in the smf74_proc table."""

    __tablename__ = "smf74_proc"
    r744pnum: so.Mapped[int] = so.mapped_column(sa.Integer, doc="CPU number.")
    r744fsys: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="Name of this system (from IEASYSxx parmlib member, SYSNAME parameter).")
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf74xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf74ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf74iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")
    r744fnam: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Name of coupling facility as defined in parmlib member COUPLExx.")
    smf74sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf74xnm, datetime, smf74ist, smf74iet, r744fnam, r744pnum, smf74sid),
        sa.ForeignKeyConstraint(
            ['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'r744fnam'],
            ['smf74_cf.smf74xnm', 'smf74_cf.datetime', 'smf74_cf.smf74ist', 'smf74_cf.smf74iet', 'smf74_cf.r744fnam']),
    )

    smf74_cf: so.Mapped['Smf74Cf'] = so.relationship(back_populates='smf74_procs', viewonly=True)


class Smf74Scm(ReprMixin, Base74, Smf74scm):
    """The Smf74Scm class stores the Smf74Scm section in the smf74_scm table."""

    __tablename__ = "smf74_scm"
    r7410crid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="SCM resource identifier.")
    r7410cpid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Part identifier.")
    smf_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf74sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf74ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf74iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf74sid, datetime, smf74ist, smf74iet, r7410crid, r7410cpid),
        sa.ForeignKeyConstraint(
            ['datetime', 'smf74ist', 'smf74iet', 'smf_type', 'csc', 'smf74sid'],
            ['smf74_pro.datetime', 'smf74_pro.smf74ist', 'smf74_pro.smf74iet', 'smf74_pro.smf_type', 'smf74_pro.csc',
             'smf74_pro.smf74sid']),
    )

    smf74_pros: so.Mapped[List['Smf74Pro']] = so.relationship(back_populates='smf74_scm', viewonly=True)


class Smf74Siol(ReprMixin, Base74, Smf74siol):
    """The Smf74Siol class stores the Smf74Siol section in the smf74_siol table."""

    __tablename__ = "smf74_siol"
    r748siid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Synchronous I/O link (IBM zHyperLink) interface ID.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf74ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf74iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")
    r748cser: so.Mapped[str] = so.mapped_column(sa.String(10), doc="Primary control unit serial number.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(datetime, smf74ist, smf74iet, r748cser, r748siid),
        sa.ForeignKeyConstraint(
            ['datetime', 'smf74ist', 'smf74iet', 'r748cser'],
            ['smf74_cntl.datetime', 'smf74_cntl.smf74ist', 'smf74_cntl.smf74iet', 'smf74_cntl.r748cser']),
    )

    smf74_cntl: so.Mapped['Smf74Cntl'] = so.relationship(back_populates='smf74_siols', viewonly=True)


class Smf74Sreq(ReprMixin, Base74, Smf74sreq, Smf74cach):
    """The Smf74Sreq class stores the Smf74Sreq section in the smf74_sreq table."""

    __tablename__ = "smf74_sreq"
    r744snam: so.Mapped[str] = so.mapped_column(sa.String(16),
                                                doc="Name of connected structure in this coupling facility.")
    r744sver: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Structure version number.")
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf74xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf74ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf74iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")
    r744fnam: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Name of coupling facility as defined in parmlib member COUPLExx.")
    smf74sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf74xnm, datetime, smf74ist, smf74iet, r744fnam, r744snam, smf74sid),
        sa.ForeignKeyConstraint(
            ['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'r744fnam', 'r744snam'],
            ['smf74_str.smf74xnm', 'smf74_str.datetime', 'smf74_str.smf74ist', 'smf74_str.smf74iet',
             'smf74_str.r744fnam', 'smf74_str.r744qstr']),
        sa.ForeignKeyConstraint(
            ['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'r744fnam', 'smf74sid'],
            ['smf74_lcf.smf74xnm', 'smf74_lcf.datetime', 'smf74_lcf.smf74ist', 'smf74_lcf.smf74iet',
             'smf74_lcf.r744fnam', 'smf74_lcf.smf74sid']),
    )

    smf74_lcf: so.Mapped['Smf74Lcf'] = so.relationship(back_populates='smf74_sreqs', viewonly=True)
    smf74_str: so.Mapped['Smf74Str'] = so.relationship(back_populates='smf74_sreqs', viewonly=True)
    smf74_cachs: so.Mapped[List['Smf74Cach']] = so.relationship(back_populates='smf74_sreq', viewonly=True)
    smf74_mscms: so.Mapped[List['Smf74Mscm']] = so.relationship(back_populates='smf74_sreq', viewonly=True)
    smf74_adups: so.Mapped[List['Smf74Adup']] = so.relationship(back_populates='smf74_sreq', viewonly=True)


class Smf74Srtd(ReprMixin, Base74, Smf74srtd):
    """The Smf74Srtd class stores the Smf74Srtd section in the smf74_srtd table."""

    __tablename__ = "smf74_srtd"
    r749rtrv: so.Mapped[float] = so.mapped_column(sa.Float,
                                                  doc="Response time distribution bucket range value. The range value of the first read and the first write bucket of a Synchronous I/O link represents response times less than the range value. For example, if the read range value is 10, then this bucket represents read response times less than 10 microseconds. The range value of the remaining buckets represents response times less than this range value and greater than or equal to the prior range value. For example, if the range value is 30 and the prior range value was 20, this represents responses r in the range: 20 microseconds <= r < 30 microseconds ")
    srtd_idx: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="the index of synchronous I/O response time distribution data record in the section.")
    response_time_for_sync_io_read: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                                doc="r749rflg (Bit 0) indicating if set, response time data measured for synchronous I/O read instructions.")
    response_time_for_sync_io_write: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                                       doc="r749rflg (Bit 1) indicating if set, response time data measured for synchronous I/O write instructions.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf74ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf74iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")
    r749pfid: so.Mapped[str] = so.mapped_column(sa.String(10),
                                                doc="PCIE Function ID (PFID) for the PCIE function for which performance data is returned.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(datetime, smf74ist, smf74iet, r749pfid, response_time_for_sync_io_write, srtd_idx,
                                r749rtrv),
        sa.ForeignKeyConstraint(
            ['datetime', 'smf74ist', 'smf74iet', 'r749pfid'],
            ['smf74_pcie.datetime', 'smf74_pcie.smf74ist', 'smf74_pcie.smf74iet', 'smf74_pcie.r749pfid']),
    )

    smf74_pcie: so.Mapped['Smf74Pcie'] = so.relationship(back_populates='smf74_srtds', viewonly=True)


class Smf74Str(ReprMixin, Base74, Smf74str, Smf74sreq, Smf74cach, Smf74mscm, Smf74adup):
    """The Smf74Str class stores the Smf74Str section in the smf74_str table."""

    __tablename__ = "smf74_str"
    r744qstr: so.Mapped[str] = so.mapped_column(sa.String(16),
                                                doc="Name of structure allocated in this coupling facility.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smf74xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf74ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf74iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")
    r744fnam: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Name of coupling facility as defined in parmlib member COUPLExx.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf74xnm, datetime, smf74ist, smf74iet, r744fnam, r744qstr),
        sa.ForeignKeyConstraint(
            ['smf74xnm', 'datetime', 'smf74ist', 'smf74iet', 'r744fnam'],
            ['smf74_cf.smf74xnm', 'smf74_cf.datetime', 'smf74_cf.smf74ist', 'smf74_cf.smf74iet', 'smf74_cf.r744fnam']),
    )

    smf74_cf: so.Mapped['Smf74Cf'] = so.relationship(back_populates='smf74_strs', viewonly=True)
    smf74_sreqs: so.Mapped[List['Smf74Sreq']] = so.relationship(back_populates='smf74_str', viewonly=True)
    smf74_mscms: so.Mapped[List['Smf74Mscm']] = so.relationship(back_populates='smf74_str', viewonly=True)
    smf74_adups: so.Mapped[List['Smf74Adup']] = so.relationship(back_populates='smf74_str', viewonly=True)


class Smf74Switch(ReprMixin, Base74, Smf74switch, Smf74pstat):
    """The Smf74Switch class stores the Smf74Switch section in the smf74_switch table."""

    __tablename__ = "smf74_switch"
    r747sdev: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Switch device number.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf74ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf74iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")

    __table_args__ = (
        sa.PrimaryKeyConstraint(datetime, smf74ist, smf74iet, r747sdev),
        sa.ForeignKeyConstraint(
            ['datetime', 'smf74ist', 'smf74iet'],
            ['smf74_fcd.datetime', 'smf74_fcd.smf74ist', 'smf74_fcd.smf74iet']),
    )

    smf74_fcd: so.Mapped['Smf74Fcd'] = so.relationship(back_populates='smf74_switchs', viewonly=True)
    smf74_ports: so.Mapped[List['Smf74Port']] = so.relationship(back_populates='smf74_switch', viewonly=True)


class Smf74Sys(ReprMixin, Base74, Smf74sys):
    """The Smf74Sys class stores the Smf74Sys section in the smf74_sys table."""

    __tablename__ = "smf74_sys"
    r742snme: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="System name as defined in parmlib member IEASYSxx SYSNAME parameter.")
    r742sdir: so.Mapped[str] = so.mapped_column(sa.String(3),
                                                doc="Direction of the message traffic Bit Meaning when set 0 Inbound. The R742SNME system sent messages to the local system. 1 Outbound. The R742SNME system receives messages from the local system. 2 Local. This means that the message traffic is within the local system. 3-7 Reserved.")
    r742stcn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Transport class name (blanks for inbound entry).")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf74sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf74ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf74iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf74sid, datetime, smf74ist, smf74iet, r742snme, r742stcn, r742sdir),
        sa.ForeignKeyConstraint(
            ['csc', 'smf74sid', 'datetime', 'smf74ist', 'smf74iet'],
            ['smf74_xctl.csc', 'smf74_xctl.smf74sid', 'smf74_xctl.datetime', 'smf74_xctl.smf74ist',
             'smf74_xctl.smf74iet']),
    )

    smf74_xctl: so.Mapped['Smf74Xctl'] = so.relationship(back_populates='smf74_syss', viewonly=True)


class Smf74Xctl(ReprMixin, Base74):
    """The Smf74Xctl class stores the Smf74Xctl section in the smf74_xctl table."""

    __tablename__ = "smf74_xctl"
    r742stot: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of System data sections in all SMF records.")
    r742ptot: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of Path data sections in all SMF records.")
    r742mtot: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of Member data sections in all SMF records.")
    smf_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf74sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf74ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf74iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf74sid, datetime, smf74ist, smf74iet),
        sa.ForeignKeyConstraint(
            ['datetime', 'smf74ist', 'smf74iet', 'smf_type', 'csc', 'smf74sid'],
            ['smf74_pro.datetime', 'smf74_pro.smf74ist', 'smf74_pro.smf74iet', 'smf74_pro.smf_type', 'smf74_pro.csc',
             'smf74_pro.smf74sid']),
    )

    smf74_pro: so.Mapped["Smf74Pro"] = so.relationship(back_populates="smf74_xctl", viewonly=True)
    smf74_syss: so.Mapped[List['Smf74Sys']] = so.relationship(back_populates='smf74_xctl', viewonly=True)
    smf74_paths: so.Mapped[List['Smf74Path']] = so.relationship(back_populates='smf74_xctl', viewonly=True)
    smf74_mbrs: so.Mapped[List['Smf74Mbr']] = so.relationship(back_populates='smf74_xctl', viewonly=True)


class Smf74Raid(ReprMixin, Base74, Smf74raid, Smf741dev):
    """The Smf74Raid class stores the Smf74Raid section in the smf74_raid table."""

    __tablename__ = "smf74_raid"
    r7451rid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="RAID rank ID.")
    r745dvol: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Volume serial of device")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf74ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf74iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")
    r745ssid: so.Mapped[str] = so.mapped_column(sa.String(6), doc="Subsystem ID.")
    r7451dvn: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Device number (binary).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(datetime, smf74ist, smf74iet, r745ssid, r7451dvn),
        sa.ForeignKeyConstraint(
            ['datetime', 'smf74ist', 'smf74iet', 'r7451rid'],
            ['smf74_rrank.datetime', 'smf74_rrank.smf74ist', 'smf74_rrank.smf74iet', 'smf74_rrank.r7451rid']),
        sa.ForeignKeyConstraint(
            ['datetime', 'smf74ist', 'smf74iet', 'r745ssid', 'r7451dvn'],
            ['smf74_cdev.datetime', 'smf74_cdev.smf74ist', 'smf74_cdev.smf74iet', 'smf74_cdev.r745dsid',
             'smf74_cdev.r745devn']),
    )

    smf74_cdev: so.Mapped["Smf74Cdev"] = so.relationship(back_populates="smf74_raid", viewonly=True)
    smf74_rrank: so.Mapped['Smf74Rrank'] = so.relationship(back_populates='smf74_raids', viewonly=True)


class Smf74Rrank(ReprMixin, Base74, Smf74raid, Smf741dev):
    """The Smf74Rrank class stores the Smf74Rrank section in the smf74_rrank table."""

    __tablename__ = "smf74_rrank"
    r745ssid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Subsystem ID.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf74ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf74iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")
    r7451rid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="RAID rank ID.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(datetime, smf74ist, smf74iet, r7451rid),
        sa.ForeignKeyConstraint(
            ['datetime', 'smf74ist', 'smf74iet', 'r745ssid'],
            ['smf74_cachsys.datetime', 'smf74_cachsys.smf74ist', 'smf74_cachsys.smf74iet', 'smf74_cachsys.r745ssid']),
    )

    smf74_cachsys: so.Mapped['Smf74Cachsys'] = so.relationship(back_populates='smf74_rranks', viewonly=True)
    smf74_raids: so.Mapped[List['Smf74Raid']] = so.relationship(back_populates='smf74_rrank', viewonly=True)


class Smf74Cf(ReprMixin, Base74, Smf74cf, Smf74lcf, Smf74gsrg):
    """The Smf74Cf class stores the Smf74Cf section in the smf74_cf table."""

    __tablename__ = "smf74_cf"
    r744pwgt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Shared processor weight. Valid if R744FLVL > 14.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smf74xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    datetime: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf74ist: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                        doc="Time that the RMF measurement interval started, in the form 0 hhmmssF , where hh is the hours, mm is the minutes, ss is the seconds, and F is the sign.")
    smf74iet: so.Mapped[str] = so.mapped_column(sa.String(18),
                                                doc="Interval expiration time token. This token can be used to identify other than RMF records that belong to the same interval (if interval")
    r744fnam: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Name of coupling facility as defined in parmlib member COUPLExx.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf74xnm, datetime, smf74ist, smf74iet, r744fnam),
    )

    smf74_lcfs: so.Mapped[List['Smf74Lcf']] = so.relationship(back_populates='smf74_cf', viewonly=True)
    smf74_strs: so.Mapped[List['Smf74Str']] = so.relationship(back_populates='smf74_cf', viewonly=True)
    smf74_cfrfs: so.Mapped[List['Smf74Cfrf']] = so.relationship(back_populates='smf74_cf', viewonly=True)
    smf74_procs: so.Mapped[List['Smf74Proc']] = so.relationship(back_populates='smf74_cf', viewonly=True)
    smf74_subchpas: so.Mapped[List['Smf74Subchpa']] = so.relationship(back_populates='smf74_cf', viewonly=True)
    smf74_mscms: so.Mapped[List['Smf74Mscm']] = so.relationship(back_populates='smf74_cf', viewonly=True)
