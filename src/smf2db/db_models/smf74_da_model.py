import datetime as dt
from typing import List, Optional

import sqlalchemy as sa
import sqlalchemy.orm as so

from .smf74_base import ReprMixin, Base74Da, Smf74pro, Smf74dctl, Smf74dev, Smf74cf, Smf74lcf, Smf74gsrg, Smf74proc, \
    Smf74str, Smf74sreq, Smf74cach, Smf74mscm, Smf74adup, Smf74cfrf, Smf74chpa, Smf74sys, Smf74path, Smf74mbr, \
    Smf74omvs, Smf74cachsys, Smf74cdata, Smf74cdev, Smf741dev, Smf74raid, Smf74xpool, Smf74hfs, Smf74gbuf, Smf74fsys, \
    Smf74fcd, Smf74pstat, Smf74switch, Smf74port, Smf74connector, Smf74cntl, Smf74lss, Smf74extp, Smf74rank, Smf74arry, \
    Smf74siol, Smf74pcie, Smf74dma0, Smf74dma1, Smf74dma2, Smf74dma3, Smf74dma4, Smf74hwa, Smf74hwa1, Smf74srtd, \
    Smf74scm, Smf74eadm


class Smf74ProDa(ReprMixin, Base74Da, Smf74pro):
    """The Smf74ProDa class stores the daily Smf74Pro record in the smf74_pro_da table."""

    __tablename__ = "smf74_pro_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    speed_boost: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                             doc="smf74fla (Bit 10) indcating speed boost was active during entire interval.")
    ziip_boost: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                            doc="smf74fla (Bit 9) indciating zIIP boost was active during entire interval.")
    smf_type: so.Mapped[str] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf74sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(date, smf_type, csc, smf74sid),
    )

    smf74_xctl_da: so.Mapped['Smf74XctlDa'] = so.relationship(back_populates='smf74_pro_da', viewonly=True)
    smf74_omvs_da: so.Mapped['Smf74OmvsDa'] = so.relationship(back_populates='smf74_pro_da', viewonly=True)
    smf74_hfs_da: so.Mapped['Smf74HfsDa'] = so.relationship(back_populates='smf74_pro_da', viewonly=True)
    smf74_fcd_da: so.Mapped['Smf74FcdDa'] = so.relationship(back_populates='smf74_pro_das', viewonly=True,
                                                            foreign_keys=[date, smf_type],
                                                            primaryjoin='and_(Smf74ProDa.date==Smf74FcdDa.date, Smf74ProDa.smf_type==Smf74FcdDa.smf_type)', )
    smf74_cntl_da: so.Mapped['Smf74CntlDa'] = so.relationship(back_populates='smf74_pro_das', viewonly=True,
                                                              foreign_keys=[date, smf_type],
                                                              primaryjoin='and_(Smf74ProDa.date==Smf74CntlDa.date, Smf74ProDa.smf_type==Smf74CntlDa.smf_type)', )
    smf74_cachsys_da: so.Mapped['Smf74CachsysDa'] = so.relationship(back_populates='smf74_pro_das', viewonly=True,
                                                                    foreign_keys=[date, smf_type],
                                                                    primaryjoin='and_(Smf74ProDa.date==Smf74CachsysDa.date, Smf74ProDa.smf_type==Smf74CachsysDa.smf_type)', )
    smf74_pcie_da: so.Mapped['Smf74PcieDa'] = so.relationship(back_populates='smf74_pro_das', viewonly=True,
                                                              foreign_keys=[date, smf_type],
                                                              primaryjoin='and_(Smf74ProDa.date==Smf74PcieDa.date, Smf74ProDa.smf_type==Smf74PcieDa.smf_type)', )
    smf74_scm_da: so.Mapped['Smf74ScmDa'] = so.relationship(back_populates='smf74_pro_das', viewonly=True)
    smf74_eadm_da: so.Mapped['Smf74EadmDa'] = so.relationship(back_populates='smf74_pro_das', viewonly=True)
    smf74_dctl_das: so.Mapped[List['Smf74DctlDa']] = so.relationship(back_populates='smf74_pro_da', viewonly=True)
    smf74_lcf_das: so.Mapped[List['Smf74LcfDa']] = so.relationship(back_populates='smf74_pro_da', viewonly=True)


class Smf74LcfDa(ReprMixin, Base74Da, Smf74lcf):
    """The Smf74LcfDa class stores the daily Smf74Lcf record in the smf74_lcf_da table."""

    __tablename__ = "smf74_lcf_da"
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
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
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
    smf74sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf74xnm, date, r744fnam, smf74sid),

        sa.ForeignKeyConstraint(
            ['date', 'smf_type', 'csc', 'smf74sid'],
            ['smf74_pro_da.date', 'smf74_pro_da.smf_type', 'smf74_pro_da.csc', 'smf74_pro_da.smf74sid']),
        sa.ForeignKeyConstraint(
            ['smf74xnm', 'date', 'r744fnam'],
            ['smf74_cf_da.smf74xnm', 'smf74_cf_da.date', 'smf74_cf_da.r744fnam']),
    )

    smf74_cf_da: so.Mapped['Smf74CfDa'] = so.relationship(back_populates='smf74_lcf_das', viewonly=True)
    smf74_pro_da: so.Mapped['Smf74ProDa'] = so.relationship(back_populates='smf74_lcf_das', viewonly=True)
    smf74_sreq_das: so.Mapped[List['Smf74SreqDa']] = so.relationship(back_populates='smf74_lcf_da', viewonly=True)


class Smf74ArryDa(ReprMixin, Base74Da, Smf74arry):
    """The Smf74ArryDa class stores the daily Smf74Arry record in the smf74_arry_da table."""

    __tablename__ = "smf74_arry_da"
    r748aaid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Rank array identifier.")
    r748arid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Rank identifier.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    r748cser: so.Mapped[str] = so.mapped_column(sa.String(10), doc="Primary control unit serial number.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(date, r748cser, r748arid, r748aaid),

        sa.ForeignKeyConstraint(
            ['date', 'r748cser', 'r748arid'],
            ['smf74_rank_da.date', 'smf74_rank_da.r748cser', 'smf74_rank_da.r748rrid']),
    )

    smf74_rank_da: so.Mapped['Smf74RankDa'] = so.relationship(back_populates='smf74_arry_das', viewonly=True)


class Smf74CdevDa(ReprMixin, Base74Da, Smf74cdev, Smf741dev):
    """The Smf74CdevDa class stores the daily Smf74Cdev record in the smf74_cdev_da table."""

    __tablename__ = "smf74_cdev_da"
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
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
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

    __table_args__ = (
        sa.PrimaryKeyConstraint(date, r745dsid, r745devn),

        sa.ForeignKeyConstraint(
            ['date', 'r745dsid'],
            ['smf74_cachsys_da.date', 'smf74_cachsys_da.r745ssid']),
    )

    smf74_raid_da: so.Mapped['Smf74RaidDa'] = so.relationship(back_populates='smf74_cdev_da', viewonly=True)
    smf74_xpool_da: so.Mapped['Smf74XpoolDa'] = so.relationship(back_populates='smf74_cdev_da', viewonly=True)
    smf74_cachsys_da: so.Mapped['Smf74CachsysDa'] = so.relationship(back_populates='smf74_cdev_das', viewonly=True)


class Smf74RankDa(ReprMixin, Base74Da, Smf74rank, Smf74arry):
    """The Smf74RankDa class stores the daily Smf74Rank record in the smf74_rank_da table."""

    __tablename__ = "smf74_rank_da"
    r748rrid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Rank identifier.")
    r748rpnm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="Extent pool number.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    r748cser: so.Mapped[str] = so.mapped_column(sa.String(10), doc="Primary control unit serial number.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(date, r748cser, r748rrid),

        sa.ForeignKeyConstraint(
            ['date', 'r748cser'],
            ['smf74_cntl_da.date', 'smf74_cntl_da.r748cser']),
        sa.ForeignKeyConstraint(
            ['date', 'r748cser', 'r748rpnm'],
            ['smf74_extp_da.date', 'smf74_extp_da.r748cser', 'smf74_extp_da.r748xpid']),
    )

    smf74_cntl_da: so.Mapped['Smf74CntlDa'] = so.relationship(back_populates='smf74_rank_das', viewonly=True)
    smf74_extp_da: so.Mapped['Smf74ExtpDa'] = so.relationship(back_populates='smf74_rank_das', viewonly=True)
    smf74_arry_das: so.Mapped[List['Smf74ArryDa']] = so.relationship(back_populates='smf74_rank_da', viewonly=True)


class Smf74XpoolDa(ReprMixin, Base74Da, Smf74xpool, Smf741dev):
    """The Smf74XpoolDa class stores the daily Smf74Xpool record in the smf74_xpool_da table."""

    __tablename__ = "smf74_xpool_da"
    r748xpid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="Extent pool identifier.")
    ccmt_seqn: so.Mapped[Optional[str]] = so.mapped_column(sa.String(10),
                                                           doc="the sequence number of the subsystem control unit.")
    r745dvol: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Volume serial of device")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    r745ssid: so.Mapped[str] = so.mapped_column(sa.String(6), doc="Subsystem ID.")
    r7451dvn: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Device number (binary).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(date, r745ssid, r7451dvn),

        sa.ForeignKeyConstraint(
            ['date', 'r745ssid', 'r7451dvn'],
            ['smf74_cdev_da.date', 'smf74_cdev_da.r745dsid', 'smf74_cdev_da.r745devn']),
    )

    smf74_cdev_da: so.Mapped['Smf74CdevDa'] = so.relationship(back_populates='smf74_xpool_da', viewonly=True)


class Smf74AdupDa(ReprMixin, Base74Da, Smf74adup):
    """The Smf74AdupDa class stores the daily Smf74Adup record in the smf74_adup_da table."""

    __tablename__ = "smf74_adup_da"
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smf74xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    r744fnam: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Name of coupling facility as defined in parmlib member COUPLExx.")
    r744snam: so.Mapped[str] = so.mapped_column(sa.String(16),
                                                doc="Name of connected structure in this coupling facility.")
    smf74sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf74xnm, date, r744fnam, r744snam, smf74sid),

        sa.ForeignKeyConstraint(
            ['smf74xnm', 'date', 'r744fnam', 'r744snam', 'smf74sid'],
            ['smf74_sreq_da.smf74xnm', 'smf74_sreq_da.date', 'smf74_sreq_da.r744fnam', 'smf74_sreq_da.r744snam',
             'smf74_sreq_da.smf74sid']),
        sa.ForeignKeyConstraint(
            ['smf74xnm', 'date', 'r744fnam', 'r744snam'],
            ['smf74_str_da.smf74xnm', 'smf74_str_da.date', 'smf74_str_da.r744fnam', 'smf74_str_da.r744qstr']),
    )

    smf74_sreq_da: so.Mapped['Smf74SreqDa'] = so.relationship(back_populates='smf74_adup_das', viewonly=True)
    smf74_str_da: so.Mapped['Smf74StrDa'] = so.relationship(back_populates='smf74_adup_das', viewonly=True)


class Smf74CachDa(ReprMixin, Base74Da, Smf74cach):
    """The Smf74CachDa class stores the daily Smf74Cach record in the smf74_cach_da table."""

    __tablename__ = "smf74_cach_da"
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smf74xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    r744fnam: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Name of coupling facility as defined in parmlib member COUPLExx.")
    r744snam: so.Mapped[str] = so.mapped_column(sa.String(16),
                                                doc="Name of connected structure in this coupling facility.")
    smf74sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf74xnm, date, r744fnam, r744snam, smf74sid),

        sa.ForeignKeyConstraint(
            ['smf74xnm', 'date', 'r744fnam', 'r744snam', 'smf74sid'],
            ['smf74_sreq_da.smf74xnm', 'smf74_sreq_da.date', 'smf74_sreq_da.r744fnam', 'smf74_sreq_da.r744snam',
             'smf74_sreq_da.smf74sid']),
    )

    smf74_sreq_da: so.Mapped['Smf74SreqDa'] = so.relationship(back_populates='smf74_cach_das', viewonly=True)


class Smf74CachsysDa(ReprMixin, Base74Da, Smf74cachsys, Smf74cdata, Smf74cdev, Smf741dev):
    """The Smf74CachsysDa class stores the daily Smf74Cachsys record in the smf74_cachsys_da table."""

    __tablename__ = "smf74_cachsys_da"
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
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    r745ssid: so.Mapped[str] = so.mapped_column(sa.String(6), doc="Subsystem ID.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(date, r745ssid),
    )

    smf74_pro_das: so.Mapped[List['Smf74ProDa']] = so.relationship(back_populates='smf74_cachsys_da', viewonly=True,
                                                                   foreign_keys='Smf74ProDa.date, Smf74ProDa.smf_type',
                                                                   primaryjoin='and_(Smf74CachsysDa.date==Smf74ProDa.date, Smf74CachsysDa.smf_type==Smf74ProDa.smf_type)', )
    smf74_cdev_das: so.Mapped[List['Smf74CdevDa']] = so.relationship(back_populates='smf74_cachsys_da', viewonly=True)
    smf74_rrank_das: so.Mapped[List['Smf74RrankDa']] = so.relationship(back_populates='smf74_cachsys_da', viewonly=True)


class Smf74CfrfDa(ReprMixin, Base74Da, Smf74cfrf):
    """The Smf74CfrfDa class stores the daily Smf74Cfrf record in the smf74_cfrf_da table."""

    __tablename__ = "smf74_cfrf_da"
    r744rsys: so.Mapped[Optional[str]] = so.mapped_column(sa.String(18),
                                                          doc="System identification value for the remotely connected CF.")
    r744rnam: so.Mapped[str] = so.mapped_column(sa.String(8), doc="CF name (if applicable, else X'0').")
    r744rpgs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Receiver path group size.")
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    ndepartition: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="r744rnde indicating the partition number of the remotely connected CF.")
    smf74xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    r744fnam: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Name of coupling facility as defined in parmlib member COUPLExx.")
    smf74sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf74xnm, date, r744fnam, r744rnam, smf74sid),

        sa.ForeignKeyConstraint(
            ['smf74xnm', 'date', 'r744fnam'],
            ['smf74_cf_da.smf74xnm', 'smf74_cf_da.date', 'smf74_cf_da.r744fnam']),
    )

    smf74_cf_da: so.Mapped['Smf74CfDa'] = so.relationship(back_populates='smf74_cfrf_das', viewonly=True)
    smf74_dupchpa_das: so.Mapped[List['Smf74DupchpaDa']] = so.relationship(back_populates='smf74_cfrf_da',
                                                                           viewonly=True)


class Smf74DupchpaDa(ReprMixin, Base74Da, Smf74chpa):
    """The Smf74DupchpaDa class stores the daily Smf74Dupchpa record in the smf74_dupchpa_da table."""

    __tablename__ = "smf74_dupchpa_da"
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smf74xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
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
        sa.PrimaryKeyConstraint(smf74xnm, date, r744fnam, r744rnam, r744hcpi, r744hsnd, smf74sid),

        sa.ForeignKeyConstraint(
            ['smf74xnm', 'date', 'r744fnam', 'r744rnam', 'smf74sid'],
            ['smf74_cfrf_da.smf74xnm', 'smf74_cfrf_da.date', 'smf74_cfrf_da.r744fnam', 'smf74_cfrf_da.r744rnam',
             'smf74_cfrf_da.smf74sid']),
    )

    smf74_cfrf_da: so.Mapped['Smf74CfrfDa'] = so.relationship(back_populates='smf74_dupchpa_das', viewonly=True)


class Smf74SubchpaDa(ReprMixin, Base74Da, Smf74chpa):
    """The Smf74SubchpaDa class stores the daily Smf74Subchpa record in the smf74_subchpa_da table."""

    __tablename__ = "smf74_subchpa_da"
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smf74xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    r744fnam: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Name of coupling facility as defined in parmlib member COUPLExx.")
    smf74sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    r744hcpi: so.Mapped[str] = so.mapped_column(sa.String(2),
                                                doc="Channel path identifier. The range of values is X'00' to X'FF'.")
    r744hsnd: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="r744hchf (Bit 1) showing channel path is a sender channel.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf74xnm, date, r744fnam, smf74sid, r744hcpi, r744hsnd),

        sa.ForeignKeyConstraint(
            ['smf74xnm', 'date', 'r744fnam'],
            ['smf74_cf_da.smf74xnm', 'smf74_cf_da.date', 'smf74_cf_da.r744fnam']),
    )

    smf74_cf_da: so.Mapped['Smf74CfDa'] = so.relationship(back_populates='smf74_subchpa_das', viewonly=True)


class Smf74CntlDa(ReprMixin, Base74Da, Smf74cntl):
    """The Smf74CntlDa class stores the daily Smf74Cntl record in the smf74_cntl_da table."""

    __tablename__ = "smf74_cntl_da"
    r748cser: so.Mapped[str] = so.mapped_column(sa.String(10), doc="Primary control unit serial number.")
    smf_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(date, r748cser),
    )

    smf74_pro_das: so.Mapped[List['Smf74ProDa']] = so.relationship(back_populates='smf74_cntl_da', viewonly=True,
                                                                   foreign_keys='Smf74ProDa.date, Smf74ProDa.smf_type',
                                                                   primaryjoin='and_(Smf74CntlDa.date==Smf74ProDa.date, Smf74CntlDa.smf_type==Smf74ProDa.smf_type)', )
    smf74_lss_das: so.Mapped[List['Smf74LssDa']] = so.relationship(back_populates='smf74_cntl_da', viewonly=True)
    smf74_extp_das: so.Mapped[List['Smf74ExtpDa']] = so.relationship(back_populates='smf74_cntl_da', viewonly=True)
    smf74_rank_das: so.Mapped[List['Smf74RankDa']] = so.relationship(back_populates='smf74_cntl_da', viewonly=True)
    smf74_siol_das: so.Mapped[List['Smf74SiolDa']] = so.relationship(back_populates='smf74_cntl_da', viewonly=True)


class Smf74ConnectorDa(ReprMixin, Base74Da, Smf74connector):
    """The Smf74ConnectorDa class stores the daily Smf74Connector record in the smf74_connector_da table."""

    __tablename__ = "smf74_connector_da"
    r747cnum: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Port number.")
    r747cadr: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Port address.")
    r747ccu: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Connector id (CU).")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    r747sdev: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Switch device number.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(date, r747sdev, r747cadr, r747cnum, r747ccu),

        sa.ForeignKeyConstraint(
            ['date', 'r747sdev', 'r747cadr', 'r747cnum'],
            ['smf74_port_da.date', 'smf74_port_da.r747sdev', 'smf74_port_da.r747padr', 'smf74_port_da.r747pnum']),
    )

    smf74_port_da: so.Mapped['Smf74PortDa'] = so.relationship(back_populates='smf74_connector_das', viewonly=True)


class Smf74DctlDa(ReprMixin, Base74Da, Smf74dctl):
    """The Smf74DctlDa class stores the daily Smf74Dctl record in the smf74_dctl_da table."""

    __tablename__ = "smf74_dctl_da"
    smf74sub: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="Device class code: Bit Configuration Meaning X'0080' Magnetic tape device X'0040' Communication equipment X'0020' Direct access devices X'0010' Graphics devices X'0008' Unit record devices X'0004' Character reader devices.")
    smf_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf74sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf74sid, date, smf74sub),

        sa.ForeignKeyConstraint(
            ['date', 'smf_type', 'csc', 'smf74sid'],
            ['smf74_pro_da.date', 'smf74_pro_da.smf_type', 'smf74_pro_da.csc', 'smf74_pro_da.smf74sid']),
    )

    smf74_pro_da: so.Mapped['Smf74ProDa'] = so.relationship(back_populates='smf74_dctl_das', viewonly=True)
    smf74_dev_das: so.Mapped[List['Smf74DevDa']] = so.relationship(back_populates='smf74_dctl_da', viewonly=True)


class Smf74DevDa(ReprMixin, Base74Da, Smf74dev):
    """The Smf74DevDa class stores the daily Smf74Dev record in the smf74_dev_da table."""

    __tablename__ = "smf74_dev_da"
    smf74num: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Device number, in the range X'0000' to X'FFFF'.")
    smf74lcu: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="Logical control unit number, in the range X'0000' to X'FFFF'.")
    smf74scs: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Subchannel set ID.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf74sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")
    smf74sub: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="Device class code: Bit Configuration Meaning X'0080' Magnetic tape device X'0040' Communication equipment X'0020' Direct access devices X'0010' Graphics devices X'0008' Unit record devices X'0004' Character reader devices.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf74sid, date, smf74sub, smf74lcu, smf74scs, smf74num),

        sa.ForeignKeyConstraint(
            ['csc', 'smf74sid', 'date', 'smf74sub'],
            ['smf74_dctl_da.csc', 'smf74_dctl_da.smf74sid', 'smf74_dctl_da.date', 'smf74_dctl_da.smf74sub']),
    )

    smf74_dctl_da: so.Mapped['Smf74DctlDa'] = so.relationship(back_populates='smf74_dev_das', viewonly=True)


class Smf74EadmDa(ReprMixin, Base74Da, Smf74eadm):
    """The Smf74EadmDa class stores the daily Smf74Eadm record in the smf74_eadm_da table."""

    __tablename__ = "smf74_eadm_da"
    smf_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf74sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf74sid, date),

        sa.ForeignKeyConstraint(
            ['date', 'smf_type', 'csc', 'smf74sid'],
            ['smf74_pro_da.date', 'smf74_pro_da.smf_type', 'smf74_pro_da.csc', 'smf74_pro_da.smf74sid']),
    )

    smf74_pro_das: so.Mapped[List['Smf74ProDa']] = so.relationship(back_populates='smf74_eadm_da', viewonly=True)


class Smf74ExtpDa(ReprMixin, Base74Da, Smf74extp, Smf74rank, Smf74arry):
    """The Smf74ExtpDa class stores the daily Smf74Extp record in the smf74_extp_da table."""

    __tablename__ = "smf74_extp_da"
    r748xpid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Extent pool identifier.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    r748cser: so.Mapped[str] = so.mapped_column(sa.String(10), doc="Primary control unit serial number.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(date, r748cser, r748xpid),

        sa.ForeignKeyConstraint(
            ['date', 'r748cser'],
            ['smf74_cntl_da.date', 'smf74_cntl_da.r748cser']),
    )

    smf74_cntl_da: so.Mapped['Smf74CntlDa'] = so.relationship(back_populates='smf74_extp_das', viewonly=True)
    smf74_rank_das: so.Mapped[List['Smf74RankDa']] = so.relationship(back_populates='smf74_extp_da', viewonly=True)


class Smf74FcdDa(ReprMixin, Base74Da, Smf74fcd, Smf74pstat):
    """The Smf74FcdDa class stores the daily Smf74Fcd record in the smf74_fcd_da table."""

    __tablename__ = "smf74_fcd_da"
    smf_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(date),
    )

    smf74_pro_das: so.Mapped[List['Smf74ProDa']] = so.relationship(back_populates='smf74_fcd_da', viewonly=True,
                                                                   foreign_keys='Smf74ProDa.date, Smf74ProDa.smf_type',
                                                                   primaryjoin='and_(Smf74FcdDa.date==Smf74ProDa.date, Smf74FcdDa.smf_type==Smf74ProDa.smf_type)', )
    smf74_switch_das: so.Mapped[List['Smf74SwitchDa']] = so.relationship(back_populates='smf74_fcd_da', viewonly=True)


class Smf74FsysDa(ReprMixin, Base74Da, Smf74fsys):
    """The Smf74FsysDa class stores the daily Smf74Fsys record in the smf74_fsys_da table."""

    __tablename__ = "smf74_fsys_da"
    r746fsnm: so.Mapped[str] = so.mapped_column(sa.String(44), doc="File system name (cataloged dataset name).")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf74sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf74sid, date, r746fsnm),

        sa.ForeignKeyConstraint(
            ['csc', 'smf74sid', 'date'],
            ['smf74_hfs_da.csc', 'smf74_hfs_da.smf74sid', 'smf74_hfs_da.date']),
    )

    smf74_hfs_da: so.Mapped['Smf74HfsDa'] = so.relationship(back_populates='smf74_fsys_das', viewonly=True)


class Smf74GbufDa(ReprMixin, Base74Da, Smf74gbuf):
    """The Smf74GbufDa class stores the daily Smf74Gbuf record in the smf74_gbuf_da table."""

    __tablename__ = "smf74_gbuf_da"
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    pool_number: so.Mapped[int] = so.mapped_column(sa.Integer, doc="buffer pool number.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf74sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf74sid, date, pool_number),

        sa.ForeignKeyConstraint(
            ['csc', 'smf74sid', 'date'],
            ['smf74_hfs_da.csc', 'smf74_hfs_da.smf74sid', 'smf74_hfs_da.date']),
    )

    smf74_hfs_da: so.Mapped['Smf74HfsDa'] = so.relationship(back_populates='smf74_gbuf_das', viewonly=True)


class Smf74HfsDa(ReprMixin, Base74Da, Smf74hfs):
    """The Smf74HfsDa class stores the daily Smf74Hfs record in the smf74_hfs_da table."""

    __tablename__ = "smf74_hfs_da"
    smf_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf74sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf74sid, date),

        sa.ForeignKeyConstraint(
            ['date', 'smf_type', 'csc', 'smf74sid'],
            ['smf74_pro_da.date', 'smf74_pro_da.smf_type', 'smf74_pro_da.csc', 'smf74_pro_da.smf74sid']),
    )

    smf74_pro_da: so.Mapped['Smf74ProDa'] = so.relationship(back_populates='smf74_hfs_da', viewonly=True)
    smf74_gbuf_das: so.Mapped[List['Smf74GbufDa']] = so.relationship(back_populates='smf74_hfs_da', viewonly=True)
    smf74_fsys_das: so.Mapped[List['Smf74FsysDa']] = so.relationship(back_populates='smf74_hfs_da', viewonly=True)


class Smf74LssDa(ReprMixin, Base74Da, Smf74lss):
    """The Smf74LssDa class stores the daily Smf74Lss record in the smf74_lss_da table."""

    __tablename__ = "smf74_lss_da"
    r748laid: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Adapter ID.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    r748cser: so.Mapped[str] = so.mapped_column(sa.String(10), doc="Primary control unit serial number.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(date, r748cser, r748laid),

        sa.ForeignKeyConstraint(
            ['date', 'r748cser'],
            ['smf74_cntl_da.date', 'smf74_cntl_da.r748cser']),
    )

    smf74_cntl_da: so.Mapped['Smf74CntlDa'] = so.relationship(back_populates='smf74_lss_das', viewonly=True)


class Smf74MbrDa(ReprMixin, Base74Da, Smf74mbr):
    """The Smf74MbrDa class stores the daily Smf74Mbr record in the smf74_mbr_da table."""

    __tablename__ = "smf74_mbr_da"
    r742msys: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="System name (as defined in parmlib member IEASYSxx SYSNAME parameter) where the member resides.")
    r742mgrp: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Group name.")
    r742mmem: so.Mapped[str] = so.mapped_column(sa.String(16), doc="Member name.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf74sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf74sid, date, r742mgrp, r742mmem, r742msys),

        sa.ForeignKeyConstraint(
            ['csc', 'smf74sid', 'date'],
            ['smf74_xctl_da.csc', 'smf74_xctl_da.smf74sid', 'smf74_xctl_da.date']),
    )

    smf74_xctl_da: so.Mapped['Smf74XctlDa'] = so.relationship(back_populates='smf74_mbr_das', viewonly=True)


class Smf74MscmDa(ReprMixin, Base74Da, Smf74mscm):
    """The Smf74MscmDa class stores the daily Smf74Mscm record in the smf74_mscm_da table."""

    __tablename__ = "smf74_mscm_da"
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smf74xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    r744fnam: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Name of coupling facility as defined in parmlib member COUPLExx.")
    r744snam: so.Mapped[str] = so.mapped_column(sa.String(16),
                                                doc="Name of connected structure in this coupling facility.")
    smf74sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf74xnm, date, r744fnam, r744snam, smf74sid),

        sa.ForeignKeyConstraint(
            ['smf74xnm', 'date', 'r744fnam', 'r744snam', 'smf74sid'],
            ['smf74_sreq_da.smf74xnm', 'smf74_sreq_da.date', 'smf74_sreq_da.r744fnam', 'smf74_sreq_da.r744snam',
             'smf74_sreq_da.smf74sid']),
        sa.ForeignKeyConstraint(
            ['smf74xnm', 'date', 'r744fnam'],
            ['smf74_cf_da.smf74xnm', 'smf74_cf_da.date', 'smf74_cf_da.r744fnam']),
        sa.ForeignKeyConstraint(
            ['smf74xnm', 'date', 'r744fnam', 'r744snam'],
            ['smf74_str_da.smf74xnm', 'smf74_str_da.date', 'smf74_str_da.r744fnam', 'smf74_str_da.r744qstr']),
    )

    smf74_sreq_da: so.Mapped['Smf74SreqDa'] = so.relationship(back_populates='smf74_mscm_das', viewonly=True)
    smf74_str_da: so.Mapped['Smf74StrDa'] = so.relationship(back_populates='smf74_mscm_das', viewonly=True)
    smf74_cf_da: so.Mapped['Smf74CfDa'] = so.relationship(back_populates='smf74_mscm_das', viewonly=True)


class Smf74OmvsDa(ReprMixin, Base74Da, Smf74omvs):
    """The Smf74OmvsDa class stores the daily Smf74Omvs record in the smf74_omvs_da table."""

    __tablename__ = "smf74_omvs_da"
    smf_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf74sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf74sid, date),

        sa.ForeignKeyConstraint(
            ['date', 'smf_type', 'csc', 'smf74sid'],
            ['smf74_pro_da.date', 'smf74_pro_da.smf_type', 'smf74_pro_da.csc', 'smf74_pro_da.smf74sid']),
    )

    smf74_pro_da: so.Mapped['Smf74ProDa'] = so.relationship(back_populates='smf74_omvs_da', viewonly=True)


class Smf74PathDa(ReprMixin, Base74Da, Smf74path):
    """The Smf74PathDa class stores the daily Smf74Path record in the smf74_path_da table."""

    __tablename__ = "smf74_path_da"
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
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf74sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf74sid, date, r742pnme, r742pdir, r742pona, r742ptyp, r742pstr, r742ptcn),

        sa.ForeignKeyConstraint(
            ['csc', 'smf74sid', 'date'],
            ['smf74_xctl_da.csc', 'smf74_xctl_da.smf74sid', 'smf74_xctl_da.date']),
    )

    smf74_xctl_da: so.Mapped['Smf74XctlDa'] = so.relationship(back_populates='smf74_path_das', viewonly=True)


class Smf74PcieDa(ReprMixin, Base74Da, Smf74pcie, Smf74dma0, Smf74dma1, Smf74dma2, Smf74dma3, Smf74dma4, Smf74hwa,
                  Smf74hwa1):
    """The Smf74PcieDa class stores the daily Smf74Pcie record in the smf74_pcie_da table."""

    __tablename__ = "smf74_pcie_da"
    r749pfid: so.Mapped[str] = so.mapped_column(sa.String(10),
                                                doc="PCIE Function ID (PFID) for the PCIE function for which performance data is returned.")
    smf_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf74sid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4),
                                                          doc="System identification (from the SMFPRMxx SID parameter).")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(date, r749pfid),
    )

    smf74_pro_das: so.Mapped[List['Smf74ProDa']] = so.relationship(back_populates='smf74_pcie_da', viewonly=True,
                                                                   foreign_keys='Smf74ProDa.date, Smf74ProDa.smf_type',
                                                                   primaryjoin='and_(Smf74PcieDa.date==Smf74ProDa.date, Smf74PcieDa.smf_type==Smf74ProDa.smf_type)', )
    smf74_srtd_das: so.Mapped[List['Smf74SrtdDa']] = so.relationship(back_populates='smf74_pcie_da', viewonly=True)


class Smf74PortDa(ReprMixin, Base74Da, Smf74port, Smf74pstat):
    """The Smf74PortDa class stores the daily Smf74Port record in the smf74_port_da table."""

    __tablename__ = "smf74_port_da"
    smf74sid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4),
                                                          doc="System identification (from the SMFPRMxx SID parameter).")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    r747sdev: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Switch device number.")
    r747padr: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Port address.")
    r747pnum: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Port number.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(date, r747sdev, r747padr, r747pnum),

        sa.ForeignKeyConstraint(
            ['date', 'r747sdev'],
            ['smf74_switch_da.date', 'smf74_switch_da.r747sdev']),
    )

    smf74_switch_da: so.Mapped['Smf74SwitchDa'] = so.relationship(back_populates='smf74_port_das', viewonly=True)
    smf74_connector_das: so.Mapped[List['Smf74ConnectorDa']] = so.relationship(back_populates='smf74_port_da',
                                                                               viewonly=True)


class Smf74ProcDa(ReprMixin, Base74Da, Smf74proc):
    """The Smf74ProcDa class stores the daily Smf74Proc record in the smf74_proc_da table."""

    __tablename__ = "smf74_proc_da"
    r744pnum: so.Mapped[int] = so.mapped_column(sa.Integer, doc="CPU number.")
    r744fsys: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="Name of this system (from IEASYSxx parmlib member, SYSNAME parameter).")
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smf74xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    r744fnam: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Name of coupling facility as defined in parmlib member COUPLExx.")
    smf74sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf74xnm, date, r744fnam, r744pnum, smf74sid),

        sa.ForeignKeyConstraint(
            ['smf74xnm', 'date', 'r744fnam'],
            ['smf74_cf_da.smf74xnm', 'smf74_cf_da.date', 'smf74_cf_da.r744fnam']),
    )

    smf74_cf_da: so.Mapped['Smf74CfDa'] = so.relationship(back_populates='smf74_proc_das', viewonly=True)


class Smf74ScmDa(ReprMixin, Base74Da, Smf74scm):
    """The Smf74ScmDa class stores the daily Smf74Scm record in the smf74_scm_da table."""

    __tablename__ = "smf74_scm_da"
    r7410crid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="SCM resource identifier.")
    r7410cpid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Part identifier.")
    smf_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf74sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf74sid, date, r7410crid, r7410cpid),

        sa.ForeignKeyConstraint(
            ['date', 'smf_type', 'csc', 'smf74sid'],
            ['smf74_pro_da.date', 'smf74_pro_da.smf_type', 'smf74_pro_da.csc', 'smf74_pro_da.smf74sid']),
    )

    smf74_pro_das: so.Mapped[List['Smf74ProDa']] = so.relationship(back_populates='smf74_scm_da', viewonly=True)


class Smf74SiolDa(ReprMixin, Base74Da, Smf74siol):
    """The Smf74SiolDa class stores the daily Smf74Siol record in the smf74_siol_da table."""

    __tablename__ = "smf74_siol_da"
    r748siid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Synchronous I/O link (IBM zHyperLink) interface ID.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    r748cser: so.Mapped[str] = so.mapped_column(sa.String(10), doc="Primary control unit serial number.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(date, r748cser, r748siid),

        sa.ForeignKeyConstraint(
            ['date', 'r748cser'],
            ['smf74_cntl_da.date', 'smf74_cntl_da.r748cser']),
    )

    smf74_cntl_da: so.Mapped['Smf74CntlDa'] = so.relationship(back_populates='smf74_siol_das', viewonly=True)


class Smf74SreqDa(ReprMixin, Base74Da, Smf74sreq, Smf74cach):
    """The Smf74SreqDa class stores the daily Smf74Sreq record in the smf74_sreq_da table."""

    __tablename__ = "smf74_sreq_da"
    r744snam: so.Mapped[str] = so.mapped_column(sa.String(16),
                                                doc="Name of connected structure in this coupling facility.")
    r744sver: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="Structure version number.")
    csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                     doc="the identifier or serial number of Central Processor Complexes (CPC).")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    smf74xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    r744fnam: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Name of coupling facility as defined in parmlib member COUPLExx.")
    smf74sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf74xnm, date, r744fnam, r744snam, smf74sid),

        sa.ForeignKeyConstraint(
            ['smf74xnm', 'date', 'r744fnam', 'r744snam'],
            ['smf74_str_da.smf74xnm', 'smf74_str_da.date', 'smf74_str_da.r744fnam', 'smf74_str_da.r744qstr']),
        sa.ForeignKeyConstraint(
            ['smf74xnm', 'date', 'r744fnam', 'smf74sid'],
            ['smf74_lcf_da.smf74xnm', 'smf74_lcf_da.date', 'smf74_lcf_da.r744fnam', 'smf74_lcf_da.smf74sid']),
    )

    smf74_lcf_da: so.Mapped['Smf74LcfDa'] = so.relationship(back_populates='smf74_sreq_das', viewonly=True)
    smf74_str_da: so.Mapped['Smf74StrDa'] = so.relationship(back_populates='smf74_sreq_das', viewonly=True)
    smf74_cach_das: so.Mapped[List['Smf74CachDa']] = so.relationship(back_populates='smf74_sreq_da', viewonly=True)
    smf74_mscm_das: so.Mapped[List['Smf74MscmDa']] = so.relationship(back_populates='smf74_sreq_da', viewonly=True)
    smf74_adup_das: so.Mapped[List['Smf74AdupDa']] = so.relationship(back_populates='smf74_sreq_da', viewonly=True)


class Smf74SrtdDa(ReprMixin, Base74Da, Smf74srtd):
    """The Smf74SrtdDa class stores the daily Smf74Srtd record in the smf74_srtd_da table."""

    __tablename__ = "smf74_srtd_da"
    r749rtrv: so.Mapped[float] = so.mapped_column(sa.Float,
                                                  doc="Response time distribution bucket range value. The range value of the first read and the first write bucket of a Synchronous I/O link represents response times less than the range value. For example, if the read range value is 10, then this bucket represents read response times less than 10 microseconds. The range value of the remaining buckets represents response times less than this range value and greater than or equal to the prior range value. For example, if the range value is 30 and the prior range value was 20, this represents responses r in the range: 20 microseconds <= r < 30 microseconds ")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    srtd_idx: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="the index of synchronous I/O response time distribution data record in the section.")
    response_time_for_sync_io_read: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                                doc="r749rflg (Bit 0) indicating if set, response time data measured for synchronous I/O read instructions.")
    response_time_for_sync_io_write: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                                       doc="r749rflg (Bit 1) indicating if set, response time data measured for synchronous I/O write instructions.")
    r749pfid: so.Mapped[str] = so.mapped_column(sa.String(10),
                                                doc="PCIE Function ID (PFID) for the PCIE function for which performance data is returned.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(date, r749pfid, response_time_for_sync_io_write, srtd_idx, r749rtrv),

        sa.ForeignKeyConstraint(
            ['date', 'r749pfid'],
            ['smf74_pcie_da.date', 'smf74_pcie_da.r749pfid']),
    )

    smf74_pcie_da: so.Mapped['Smf74PcieDa'] = so.relationship(back_populates='smf74_srtd_das', viewonly=True)


class Smf74StrDa(ReprMixin, Base74Da, Smf74str, Smf74sreq, Smf74cach, Smf74mscm, Smf74adup):
    """The Smf74StrDa class stores the daily Smf74Str record in the smf74_str_da table."""

    __tablename__ = "smf74_str_da"
    r744qstr: so.Mapped[str] = so.mapped_column(sa.String(16),
                                                doc="Name of structure allocated in this coupling facility.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    smf74xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    r744fnam: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Name of coupling facility as defined in parmlib member COUPLExx.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf74xnm, date, r744fnam, r744qstr),

        sa.ForeignKeyConstraint(
            ['smf74xnm', 'date', 'r744fnam'],
            ['smf74_cf_da.smf74xnm', 'smf74_cf_da.date', 'smf74_cf_da.r744fnam']),
    )

    smf74_cf_da: so.Mapped['Smf74CfDa'] = so.relationship(back_populates='smf74_str_das', viewonly=True)
    smf74_sreq_das: so.Mapped[List['Smf74SreqDa']] = so.relationship(back_populates='smf74_str_da', viewonly=True)
    smf74_mscm_das: so.Mapped[List['Smf74MscmDa']] = so.relationship(back_populates='smf74_str_da', viewonly=True)
    smf74_adup_das: so.Mapped[List['Smf74AdupDa']] = so.relationship(back_populates='smf74_str_da', viewonly=True)


class Smf74SwitchDa(ReprMixin, Base74Da, Smf74switch, Smf74pstat):
    """The Smf74SwitchDa class stores the daily Smf74Switch record in the smf74_switch_da table."""

    __tablename__ = "smf74_switch_da"
    r747sdev: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Switch device number.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(date, r747sdev),

        sa.ForeignKeyConstraint(
            ['date'],
            ['smf74_fcd_da.date']),
    )

    smf74_fcd_da: so.Mapped['Smf74FcdDa'] = so.relationship(back_populates='smf74_switch_das', viewonly=True)
    smf74_port_das: so.Mapped[List['Smf74PortDa']] = so.relationship(back_populates='smf74_switch_da', viewonly=True)


class Smf74SysDa(ReprMixin, Base74Da, Smf74sys):
    """The Smf74SysDa class stores the daily Smf74Sys record in the smf74_sys_da table."""

    __tablename__ = "smf74_sys_da"
    r742snme: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="System name as defined in parmlib member IEASYSxx SYSNAME parameter.")
    r742sdir: so.Mapped[str] = so.mapped_column(sa.String(3),
                                                doc="Direction of the message traffic Bit Meaning when set 0 Inbound. The R742SNME system sent messages to the local system. 1 Outbound. The R742SNME system receives messages from the local system. 2 Local. This means that the message traffic is within the local system. 3-7 Reserved.")
    r742stcn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Transport class name (blanks for inbound entry).")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf74sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf74sid, date, r742snme, r742stcn, r742sdir),

        sa.ForeignKeyConstraint(
            ['csc', 'smf74sid', 'date'],
            ['smf74_xctl_da.csc', 'smf74_xctl_da.smf74sid', 'smf74_xctl_da.date']),
    )

    smf74_xctl_da: so.Mapped['Smf74XctlDa'] = so.relationship(back_populates='smf74_sys_das', viewonly=True)


class Smf74XctlDa(ReprMixin, Base74Da):
    """The Smf74XctlDa class stores the daily Smf74Xctl record in the smf74_xctl_da table."""

    __tablename__ = "smf74_xctl_da"
    smf_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf74sid: so.Mapped[str] = so.mapped_column(sa.String(4),
                                                doc="System identification (from the SMFPRMxx SID parameter).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf74sid, date),

        sa.ForeignKeyConstraint(
            ['date', 'smf_type', 'csc', 'smf74sid'],
            ['smf74_pro_da.date', 'smf74_pro_da.smf_type', 'smf74_pro_da.csc', 'smf74_pro_da.smf74sid']),
    )

    smf74_pro_da: so.Mapped['Smf74ProDa'] = so.relationship(back_populates='smf74_xctl_da', viewonly=True)
    smf74_sys_das: so.Mapped[List['Smf74SysDa']] = so.relationship(back_populates='smf74_xctl_da', viewonly=True)
    smf74_path_das: so.Mapped[List['Smf74PathDa']] = so.relationship(back_populates='smf74_xctl_da', viewonly=True)
    smf74_mbr_das: so.Mapped[List['Smf74MbrDa']] = so.relationship(back_populates='smf74_xctl_da', viewonly=True)


class Smf74RaidDa(ReprMixin, Base74Da, Smf74raid, Smf741dev):
    """The Smf74RaidDa class stores the daily Smf74Raid record in the smf74_raid_da table."""

    __tablename__ = "smf74_raid_da"
    r7451rid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4), doc="RAID rank ID.")
    r745dvol: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Volume serial of device")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    r745ssid: so.Mapped[str] = so.mapped_column(sa.String(6), doc="Subsystem ID.")
    r7451dvn: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Device number (binary).")

    __table_args__ = (
        sa.PrimaryKeyConstraint(date, r745ssid, r7451dvn),

        sa.ForeignKeyConstraint(
            ['date', 'r7451rid'],
            ['smf74_rrank_da.date', 'smf74_rrank_da.r7451rid']),
        sa.ForeignKeyConstraint(
            ['date', 'r745ssid', 'r7451dvn'],
            ['smf74_cdev_da.date', 'smf74_cdev_da.r745dsid', 'smf74_cdev_da.r745devn']),
    )

    smf74_cdev_da: so.Mapped['Smf74CdevDa'] = so.relationship(back_populates='smf74_raid_da', viewonly=True)
    smf74_rrank_da: so.Mapped['Smf74RrankDa'] = so.relationship(back_populates='smf74_raid_das', viewonly=True)


class Smf74RrankDa(ReprMixin, Base74Da, Smf74raid, Smf741dev):
    """The Smf74RrankDa class stores the daily Smf74Rrank record in the smf74_rrank_da table."""

    __tablename__ = "smf74_rrank_da"
    r745ssid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="Subsystem ID.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    r7451rid: so.Mapped[str] = so.mapped_column(sa.String(4), doc="RAID rank ID.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(date, r7451rid),

        sa.ForeignKeyConstraint(
            ['date', 'r745ssid'],
            ['smf74_cachsys_da.date', 'smf74_cachsys_da.r745ssid']),
    )

    smf74_cachsys_da: so.Mapped['Smf74CachsysDa'] = so.relationship(back_populates='smf74_rrank_das', viewonly=True)
    smf74_raid_das: so.Mapped[List['Smf74RaidDa']] = so.relationship(back_populates='smf74_rrank_da', viewonly=True)


class Smf74CfDa(ReprMixin, Base74Da, Smf74cf, Smf74lcf, Smf74gsrg):
    """The Smf74CfDa class stores the daily Smf74Cf record in the smf74_cf_da table."""

    __tablename__ = "smf74_cf_da"
    r744pwgt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Shared processor weight. Valid if R744FLVL > 14.")
    last_update_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                          doc="last update time of this record.")
    date: so.Mapped[dt.date] = so.mapped_column(sa.Date, doc="the date of the record.")
    smf74xnm: so.Mapped[str] = so.mapped_column(sa.String(8), doc="Sysplex name as defined in parmlib member COUPLExx.")
    r744fnam: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Name of coupling facility as defined in parmlib member COUPLExx.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(smf74xnm, date, r744fnam),
    )

    smf74_lcf_das: so.Mapped[List['Smf74LcfDa']] = so.relationship(back_populates='smf74_cf_da', viewonly=True)
    smf74_str_das: so.Mapped[List['Smf74StrDa']] = so.relationship(back_populates='smf74_cf_da', viewonly=True)
    smf74_cfrf_das: so.Mapped[List['Smf74CfrfDa']] = so.relationship(back_populates='smf74_cf_da', viewonly=True)
    smf74_proc_das: so.Mapped[List['Smf74ProcDa']] = so.relationship(back_populates='smf74_cf_da', viewonly=True)
    smf74_subchpa_das: so.Mapped[List['Smf74SubchpaDa']] = so.relationship(back_populates='smf74_cf_da', viewonly=True)
    smf74_mscm_das: so.Mapped[List['Smf74MscmDa']] = so.relationship(back_populates='smf74_cf_da', viewonly=True)
