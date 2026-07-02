from typing import Optional

import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.ext.declarative import AbstractConcreteBase
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


class Base70(Base):
    __abstract__ = True
    metadata = sa.MetaData(schema='smf70', naming_convention=convention)


class Base70Hr(Base):
    __abstract__ = True
    metadata = sa.MetaData(schema='smf70', naming_convention=convention)


class Base70Da(Base):
    __abstract__ = True
    metadata = sa.MetaData(schema='smf70', naming_convention=convention)


class Smf70pro(AbstractConcreteBase):
    """Abstract class for structure Smf70Pro - RMF product section."""

    smf70mfv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="RMF version number.")
    smf70prd: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Product name ('RMF').")
    smf70int: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Duration of the RMF measurement interval, in the form mmsstttF where mm is the minutes, ss is the seconds, ttt is the milliseconds, and F is the sign. (The end of the measurement interval is the sum of the recorded start time and this field.)")
    smf70sam: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of RMF samples.")
    smf70fla: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Flags Bit Meaning when set 0 Reserved. 1 Samples have been skipped. 2 Record was written by RMF Monitor III. 3 Interval was synchronized with SMF. 4 SMF record converted to lower service level. 5 SMF record converted to higher release or service level. 6 Running under an alternate virtual machine. 7 - 8 Reserved. 9 zIIP boost was active during entire interval. 10 Speed boost was active during entire interval. 11 - 12 Reserved. 13 - 15 Boost class: 001 : IPL 010 : Shutdown 011 : Recovery process")
    smf70cyc: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Sampling cycle length, in the form 000 ttttF , where tttt is the milliseconds and F is the sign (taken from CYCLE option). The range of values is 0.050 to 9.999 seconds.")
    smf70mvs: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="z/OS software level (consists of an acronym and the version, release, and modification level - ZV vvrrmm ).")
    smf70iml: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Indicates the type of processor complex on which data measurements were taken. Value Meaning 3")
    smf70prf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Processor flags. Bit Meaning when set 0 The system has expanded storage 1 The processor is enabled for ES connection architecture (ESCA) 2 There is an ES connection director in the configuration 3 System is running in z/Architecture ® mode 4 At least one zAAP is currently installed 5 At least one zIIP is currently installed 6 Enhanced DAT facility 1 available")
    smf70ptn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="PR/SM partition number of the partition that wrote this record.")
    smf70srl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="SMF record level change number. This field enables processing of SMF record level changes in an existing release. SMF type 70 record levels for the current z/OS release: Subtype Record level 1 X'94' (APAR OA66812) 2 X'8F' (APAR OA59330)")
    smf70lgo: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Offset GMT to local time (STCK format).")
    smf70oil: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Original interval length as defined in the session or by SMF (in seconds).")
    smf70syn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="SYNC value in seconds.")
    smf70gie: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                  doc="Projected gathering interval end (STCK format) GMT time.")
    smf70xnm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf70snm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="System name for current system as defined in parmlib member IEASYSxx SYSNAME parameter.")
    smf70flg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="System indicator: Bit Meaning when set 0 New record format 1 Subtypes used 2 Reserved. 3-6 Version indicators* 7 System is running in PR/SM mode. *See 'Standard and extended SMF record headers' on page 164 for")
    speed_boost: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                             doc="smf70fla (Bit 10) indcating speed boost was active during entire interval.")
    ziip_boost: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                            doc="smf70fla (Bit 9) indciating zIIP boost was active during entire interval.")


class Smf70ctl(AbstractConcreteBase):
    """Abstract class for structure Smf70Ctl - CPU control section."""

    smf70mod: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="CPU processor family.")
    smf70ver: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="CPU version number - meaning varies with model number.")
    smf70bnp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of physical processors assigned for use by PR/SM.")
    smf70inb: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="PR/SM indicator bits. Bit Meaning when set 0 PR/SM diagnose X'204' failure. 1 Number of physical processors has changed. 2 Dispatch interval time has been changed. 3 An additional partition, that is not included in the count of configured partitions, is presented with a name of 'PHYSICAL'. This partition includes all of the uncaptured time that was used by the LPAR management time support feature but could not be attributed to a specific logical partition. 4 PR/SM - Diagnose X'204' extended data is supported. 5 Simplified Diagnose X'204' data provided for system running as z/VM ® guest. CPU consumption by z/VM itself provided with partition data section for logical partition named PHYSICAL . 6 Power information is available. 7")
    smf70stf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Flags. Bit Meaning when set 0 The STSI facility is available for the CPC. 1 Physical CPU adjustment factor has been changed. 2 Service units available to MVS image have been changed. 3 SMF70LAC is provided for systems running in LPAR mode, as a z/VM guest, or under an alternate virtual machine. The value no longer includes CPU wait times. 4 SMF70MDL is the model-capacity identifier and SMF70HWM is the physical model. If this bit is OFF, SMF70MDL represents both model-capacity and physical model. 5 OPT parameter BLWLTRPCT changed. 6 OPT parameter BLWLINTHD changed. 7 Field SMF70GAU is valid. Dispatch accumulated interval time in milliseconds.")
    smf70gts: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Dispatch accumulated interval time in milliseconds. A zero value indicates that the dispatch interval was dynamically determined.")
    smf70mdl: so.Mapped[Optional[str]] = so.mapped_column(sa.String(16),
                                                          doc="CPC model identifier indicating the total capacity of the CPC, including all types of active capacity. See bit 4 of SMF70STF.")
    smf70dsa: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of Diagnose samples.")
    smf70ifa: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of zAAPs online at the end of the interval.")
    smf70cpa: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Physical CPU adjustment factor based on alternate CPU capability. This value is replaced by SMF70CPA_actual and SMF70CPA_scaling_factor.")
    smf70wla: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Processor capacity available to MVS image measured in MSUs (millions of service units) per hour. The value takes into account whether or not the image has a defined capacity limit. (For systems running as VM guest, this is the VM capacity).")
    smf70lac: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Long-term average of CPU service (millions of service units). Scope of the value depends on bit 3 of SMF70STF.")
    smf70hof: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Hypervisor date/time offset in STCK format (aka Sysplex timer offset).")
    smf70hwm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(16),
                                                          doc="CPC physical model identifier. Valid if bit 4 of SMF70STF is set.")
    smf70sup: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of zIIPs online at the end of the interval.")
    smf70gjt: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                  doc="Time in STCK format when the partition that wrote this record has joined or left a capacity group (last change of group name). Also set at IPL time, when the partition is not a member of a capacity group.")
    smf70pom: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4),
                                                          doc="EBCDIC plant code that identifies the plant of manufacture for the configuration. The plant code is left-justified with trailing blank characters if necessary.")
    smf70csc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(16),
                                                          doc="EBCDIC sequence code of the configuration. The sequence code is right-justified with leading EBCDIC zeroes if necessary.")
    smf70hhf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Additional flags. Bit Meaning when set 0 HiperDispatch mode supported 1 HiperDispatch mode is active 2 HiperDispatch mode changed during interval 3 Failure returned by HISMT service. Values in Logical Core data section and values provided in SMF70MCF, SMF70MCFS, SMF70MCFI, SMF70CF, SMF70CFS, SMF70CFI, SMF70ATD, SMF70ATDS, and SMF70ATDI are invalid. 4 Absolute MSU capping is active for this partition. 5 SMF70OS_PRTCT is valid. 6-7")
    smf70pmi: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Accumulated number of blocked dispatchable units per second that may get promoted in their dispatch priority. To get the average promote event rate, divide SMF70PMI by SMF70SAM.")
    smf70pmu: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of blocked dispatchable units being promoted during the interval.")
    smf70pmw: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Accumulated number of address spaces and enclaves being blocked during the interval. To get the average number of waiters for promote, divide SMF70PMW by SMF70SAM.")
    smf70pmp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Maximum number of address spaces and enclaves found being blocked during the interval.")
    smf70pmt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="1/1000s of the CPU capacity for promote slices (OPT parameter BLWLTRPCT).")
    smf70pml: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Swapped-in starvation threshold. When an address space or enclave has not received CPU service within this time interval although it has ready-to-run work, it is considered being blocked (OPT parameter BLWLINTHD).")
    smf70mpc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(16),
                                                          doc="CPC model identifier indicating the permanent capacity of the CPC, without the temporarily increased capacity, the temporarily available replacement capacity, and the corridor capacity. The identifier is left justified with trailing blanks if necessary. This field is zero, if not supported by the hardware.")
    smf70mtc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(16),
                                                          doc="CPC model identifier indicating the temporary capacity of the CPC, which is the total of permanent capacity and temporarily increased capacity, without the temporarily available replacement capacity and the corridor capacity. The identifier is left justified with trailing blanks if necessary. This field is zero, if not supported by the hardware.")
    smf70mcr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="CPC model capacity rating associated with the model as identified by SMF70MDL. This field is zero, if not supported by the hardware.")
    smf70mpr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="CPC permanent model capacity rating associated with the model as identified by SMF70MPC. This field is zero, if not supported by the hardware.")
    smf70mtr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="CPC temporary model capacity rating associated with the model as identified by SMF70MTC. This field is zero, if not supported by the hardware.")
    smf70nrm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Normalization factor for zIIP. Multiply zIIP time by this value and divide by 256 to get the equivalent time on a CP.")
    smf70gau: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Long-term average of CPU service in millions of service units which would be allowed by the limit of the capacity group but is not used by its members. If the value is negative, the group is capped. Valid if bit 7 of SMF70STF is set.")
    smf70ncr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Nominal model-capacity rating in MSU/hour. When non-zero, this value is associated with the nominal model capacity as identified in field SMF70MDL. When field SMF70CAI contains a value of 100, this value equals the value in field SMF70MCR.")
    smf70npr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Nominal permanent model-capacity rating in MSU/ hour. When non-zero, this value is associated with the nominal permanent model capacity as identified in field SMF70MPC. When field SMF70CAI contains a value of 100, this value equals the value in field SMF70MPR.")
    smf70ntr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Nominal temporary model-capacity rating in MSU/ hour. When non-zero, this value is associated with the nominal temporary model capacity as identified in field SMF70MTC. When field SMF70CAI contains a value of 100, this value equals the value in field SMF70MTR.")
    smf70cai: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Capacity-adjustment indication. When zero, the indication is not reported. When in the range from 1 to 99, some amount of reduction is indicated. When 100, the machine is operating at its normal capacity. Temporary capacity changes that affect machine performance (for example, CBU or OOCoD) are not included.")
    smf70ccr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Capacity-change reason. Valid if SMF70CAI is non- zero. When 0, no capacity change took place. When 1, the capacity change is due to the setting of a manual control. When greater than 1, the capacity change is due to an internal machine condition or due to an external machine exception.")
    smf70mcp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Maximum CPU ID available for this IPL.")
    smf70icp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Highest CPU ID installed at IPL time.")
    smf70ccp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Highest CPU ID currently installed. This number can increase upon dynamic CPU addition.")
    smf70cpa_actual: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                 doc="Physical CPU adjustment factor based on Model Capacity Rating (will be used for converting processor time to service units). This value together with SMF70CPA_scaling_factor replaces SMF70CPA.")
    smf70cpa_scaling_factor: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                         doc="Scaling factor for SMF70CPA_actual.")
    smf70mcf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Multithreading maximum capacity numerator for general purpose processors. Divide this value by 1024 to get the multithreading maximum capacity factor for all general purpose processors that were configured ONLINE for the complete interval.")
    smf70mcfs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                           doc="Multithreading maximum capacity numerator for zIIP. Divide this value by 1024 to get the multithreading maximum capacity factor for all zIIPs that were configured ONLINE for the complete interval. A zero value is reported if no zIIP is currently installed.")
    smf70mcfi: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                           doc="Multithreading maximum capacity numerator for zAAP. Divide this value by 1024 to get the multithreading maximum capacity factor for all zAAPs that were configured ONLINE for the complete interval. A zero value is reported if no zAAP is currently installed.")
    smf70cf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                         doc="Multithreading capacity numerator for general purpose processors. Divide this value by 1024 to get the multithreading capacity factor for all general purpose processors that were configured ONLINE for the complete interval.")
    smf70cfs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Multithreading capacity numerator for zIIP. Divide this value by 1024 to get the multithreading capacity factor for all zIIPs that were configured ONLINE for the complete interval. A zero value is reported if no zIIP is currently installed.")
    smf70cfi: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Multithreading capacity numerator for zAAP. Divide this value by 1024 to get the multithreading capacity factor for all zAAPs that were configured ONLINE for the complete interval. A zero value is reported if no zAAP is currently installed.")
    smf70atd: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Average Thread Density numerator for general purpose processors . Divide this value by 1024 to get the average number of active threads for all general purpose processors that were dispatched to physical hardware and configured ONLINE for the complete interval.")
    smf70atds: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                           doc="Average Thread Density numerator for zIIP. Divide this value by 1024 to get the average number of active threads for all zIIPs that were dispatched to physical hardware and configured ONLINE for the complete interval. A zero value is reported if no zIIP is currently installed.")
    smf70atdi: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                           doc="Average Thread Density numerator for zAAP. Divide this value by 1024 to get the average number of active threads for all zAAPs that were dispatched to physical hardware and configured ONLINE for the complete interval. A zero value is reported if no zAAP is currently installed.")
    smf70lacm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                           doc="Long-term average of CPU service (millions of service units) consumed by transactions classified with reporting attribute MOBILE. If an address space or enclave is part of a tenant resource group, it will not contribute to SMF70LACM.")
    smf70laca: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                           doc="Long-term average of CPU service (millions of service units) consumed by transactions classified with reporting attribute CATEGORYA. If an address space or enclave is part of a tenant resource group, it will not contribute to SMF70LACA.")
    smf70lacb: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                           doc="Long-term average of CPU service (millions of service units) consumed by transactions classified with reporting attribute CATEGORYB. If an address space or enclave is part of a tenant resource group, it will not contribute to SMF70LACB.")
    smf70adj: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Logical adjustment factor for CPU rate.")
    smf70laccr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                            doc="Long-term average of CPU service (millions of service units) consumed by DFSMS data set encryption. Valid only for IBM z14 ® and later CPCs.")
    smf70maxpu: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                            doc="When non-zero, this field indicates how many processor cores are physically available in this particular machine. When the value is 0, it is not defined for this model.")
    smf70os_prtct: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="When non-zero, the OSPROTECT system parameter with a value other than SYSTEM is in effect. X'01' indicates OSPROTECT=1. For machines after IBM z14, may be 0 with OSPROTECT=1.")
    smf70mdl_cbp: so.Mapped[Optional[str]] = so.mapped_column(sa.String(34), doc="Reserved for future use.")
    smf70mcr_cbp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Reserved for future use.")
    smf70ncr_cbp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Reserved for future use.")
    smf70lac_cbp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Reserved for future use.")
    smf70cpa_actual_cbp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Reserved for future use.")
    smf70_ipl_time: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                        doc="IPL time of partition, in TOD format.")
    smf70_trg_m_cnt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                 doc="Number of times sampling of tenant resource group memory consumption happened.")
    smf70cpc_type: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="CPC Type.")
    smf70mdl_var: so.Mapped[Optional[str]] = so.mapped_column(sa.String(34),
                                                              doc="CPC model identifier indicating the variable capacity of the CPC. The identifier is left-justified with trailing blanks, if necessary. This field is zero if not supported by the hardware.")
    smf70mvcr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                           doc="Model variable capacity rating. When non-zero, this value is associated with the model capacity as identified in the SMF70MDL_VAR field.")
    smf70nvcr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                           doc="Nominal model variable capacity rating. When non-zero, this value is associated with the nominal model capacity as identified in the SMF70MDL_VAR field. When the SMF70CAI field contains a value of 100, this value equals the value in the SMF70MVCR field.")
    smf70zsu_on_ziip: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                  doc="Unweighted zIIP-eligible service units spent on zIIP for the entire system.")
    smf70zsu_on_cp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                doc="Unweighted zIIP-eligible service units spent on CP for the entire system.")
    smf70jsu_on_ziip: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                  doc="Unweighted zIIP-eligible Java service units spent on zIIP for the entire system.")
    smf70jsu_on_cp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                doc="Unweighted zIIP-eligible Java service units spent on CP for the entire system.")
    smf70cpe_lo: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                             doc="Low threshold value of OPT parameter CPENABLE.")
    smf70cpe_hi: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                             doc="High threshold value of OPT parameter CPENABLE.")
    smf70mdl_rep: so.Mapped[Optional[str]] = so.mapped_column(sa.String(16),
                                                              doc="CPC model identifier indicating the replacement capacity of the CPC, which is the total of permanent capacity, temporarily increased capacity, and temporarily available replacement capacity, without the corridor capacity. The identifier is left-justified with trailing blanks, if necessary. This field is zero if not supported by the hardware.")
    smf70mrcr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                           doc="Model replacement capacity rating. When non-zero, this value is associated with the model capacity as identified in the SMF70MDL_REP field.")
    smf70nrcr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                           doc="Nominal model-replacement-capacity rating. When non-zero, this value is associated with the nominal model capacity as identified in the SMF70MDL_REP field. When the SMF70CAI field contains a value of 100, this value equals the value in the SMF70MRCR field.")
    smf70_cpupower: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                doc="Accumulated microwatts for all CPU resources allocated to the LPAR during the interval. Divide by SMF70_NumPowerSamples to retrieve the average power consumption of the interval.")
    smf70_storagepower: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                    doc="Accumulated microwatts for all storage resources allocated to the LPAR during the interval. Divide by SMF70_NumPowerSamples to retrieve the average power consumption of the interval.")
    smf70_iopower: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Accumulated microwatts for all I/O resources allocated to the LPAR during the interval. Divide by SMF70_NumPowerSamples to retrieve the average power consumption of the interval.")
    smf70_cpctotalpower: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                     doc="Accumulated microwatts for all electrical and mechanical components in the CPC. Divide by SMF70_NumPowerSamples to retrieve the average power consumption of the interval.")
    smf70_cpcunassrespower: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                        doc="Accumulated microwatts for all types of resources in the standby or reserved state. Divide by SMF70_NumPowerSamples to retrieve the average power consumption of the interval.")
    smf70_cpcinfrapower: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                     doc="Accumulated microwatts for all subsystems in the CPC which do not provide CPU, storage, or I/O resources to logical partitions. These include service elements, cooling systems, power distribution, and network switches, among others. Divide by SMF70_NumPowerSamples to retrieve the average power consumption of the interval.")
    smf70_numpowersamples: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                       doc="Number of power samples for the interval.")
    smf70_powerpartitionname: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                                          doc="The name of the LPAR to which the LPAR-specific power fields apply.")
    smf70int: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Duration of the RMF measurement interval, in the form mmsstttF where mm is the minutes, ss is the seconds, ttt is the milliseconds, and F is the sign. (The end of the measurement interval is the sum of the recorded start time and this field.)")
    smf70ptn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="PR/SM partition number of the partition that wrote this record.")
    smf70snm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="System name for current system as defined in parmlib member IEASYSxx SYSNAME parameter.")
    smf70xnm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf70mtid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                           doc="Maximum Thread Identification. A non-zero value indicates that PROCVIEW CORE is effective for this partition and the hardware supports multithreading.")
    smf70lpm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Logical partition name.")
    smf_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    cpu_count_CP: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="from smf70ctn - Number of physical CPUs of CP at interval end.")
    cpu_count_accumulated_CP: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                          doc="from smf70can - Accumulated number of physcial CPUs of CP.")
    cpu_count_IFL: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="from smf70ctn - Number of physical CPUs of IFL at interval end.")
    cpu_count_accumulated_IFL: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                           doc="from smf70can - Accumulated number of physcial CPUs of IFL.")
    cpu_count_ICF: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="from smf70ctn - Number of physical CPUs of ICF at interval end.")
    cpu_count_accumulated_ICF: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                           doc="from smf70can - Accumulated number of physcial CPUs of ICF.")
    cpu_count_IIP: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="from smf70ctn - Number of physical CPUs of IIP at interval end.")
    cpu_count_accumulated_IIP: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                           doc="from smf70can - Accumulated number of physcial CPUs of IIP.")
    cpu_count_CBP: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="from smf70ctn - Number of physical CPUs of CBP at interval end.")
    cpu_count_accumulated_CBP: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                           doc="from smf70can - Accumulated number of physcial CPUs of CBP.")
    cpu_count_IFA: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="from smf70ctn - Number of physical CPUs of IFA at interval end.")
    cpu_count_accumulated_IFA: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                           doc="from smf70can - Accumulated number of physcial CPUs of IFA.")
    lpar_number: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                             doc="PR/SM partition number of the partition that wrote this record.")
    lpar_system_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(17),
                                                                  doc="combining lpar long name with lpar short name.")
    cpu_adjustment_factor_effective: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                                 doc="smf70cpa_actual if smf70cpa_actual is not zero, otherwise it is the value of smf70cpa.")
    cpa_scaling_factor_effective: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                              doc="smf70cpa_scaling_factor if smf70cpa_actual is not zero, otherwise 1.")
    wgt_cp: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6),
                                                        doc="the processor weight of general process CPs.")
    wgt_ifl: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="the processor weight of IFL processors.")
    wgt_icf: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="the processor weight of ICF processors.")
    wgt_iip: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="the processor weight of zIIP processors.")
    wgt_cbp: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="the processor weight of CBP processors.")
    wgt_ifa: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="the processor weight of zAAP processors.")
    multithreading: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="multithreading is supported.")
    numproc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="the number of general purpose processors online.")
    lpar_busy_total_cp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                      doc="the total lpar busy for general purpose processors.")
    mvs_busy_total_cp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                     doc="the total MVS busy for general purpose processors.")
    mvs_busy_unpark_total_cp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                            doc="the total MVS busy for unparked general purpose processors.")
    total_log_proc_share_cp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                           doc="the percentage of the physical processor that the logical general purpose processor is entitled to use.")
    med_log_proc_share_cp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                         doc="the percentage of the physical processor that the logical general purpose processor with MED HiperDispatch priority is entitled to use.")
    mt_prod_total_cp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="the percentage of the maximum core capacity that was used in the reporting interval while the logical core of general purpose processor was dsipatched to physical hardware.")
    mt_util_total_cp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                    doc="the percentage of the maximum core capacity of general purpose processor that was used in the reporting interval.")
    rate_io_interrupt_total: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                           doc="the total rate per second that this processor handled I/O interrupts.")
    rate_io_interrupt_by_tpi_total: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                  doc="the percentage of the total Test Pending interrupts for this processor during the interval that are handled by the I/O supervisor without re-enabling.")
    lpar_busy_total_iip: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                       doc="the total lpar busy for zIIP processors.")
    mvs_busy_total_iip: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                      doc="the total MVS busy for zIIP processors.")
    mvs_busy_unpark_total_iip: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                             doc="the total MVS busy for unparked zIIP processors.")
    total_log_proc_share_iip: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                            doc="the percentage of the physical processor that the logical zIIP processor is entitled to use.")
    med_log_proc_share_iip: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                          doc="the percentage of the physical processor that the logical zIIP processor with MED HiperDispatch priority is entitled to use.")
    mt_prod_total_iip: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                     doc="the percentage of the maximum core capacity that was used in the reporting interval while the logical core of zIIP processor was dsipatched to physical hardware.")
    mt_util_total_iip: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                     doc="the percentage of the maximum core capacity of zIIP processor that was used in the reporting interval.")
    lpar_busy_total_aap: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                       doc="the total lpar busy for zAAP processors.")
    mvs_busy_total_aap: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                      doc="the total MVS busy for zAAP processors.")
    mvs_busy_unpark_total_aap: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                             doc="the total MVS busy for unparked zAAP processors.")
    total_log_proc_share_aap: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                            doc="the percentage of the physical processor that the logical zAAP processor is entitled to use.")
    med_log_proc_share_aap: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                          doc="the percentage of the physical processor that the logical zAAP processor with MED HiperDispatch priority is entitled to use.")
    mt_prod_total_aap: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                     doc="the percentage of the maximum core capacity that was used in the reporting interval while the logical core of zAAP processor was dsipatched to physical hardware.")
    mt_util_total_aap: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                     doc="the percentage of the maximum core capacity of zAAP processor that was used in the reporting interval.")
    total_weight_cp: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6),
                                                                 doc="the total weightings of general process CPs.")
    total_weight_ifl: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6),
                                                                  doc="the total weightings of IFL procesors.")
    total_weight_iip: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6),
                                                                  doc="the total weightings of zIIP processors.")
    total_weight_icf: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6),
                                                                  doc="the total weightings of ICF processors.")
    total_weight_aap: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6),
                                                                  doc="the total weightings of zAAP processors.")
    smf70edt_total_cp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                     doc="the total logical general purpose processor effective dispatch time.")
    smf70edt_total_ifl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                      doc="the total logical IFL processor effective dispatch time.")
    smf70edt_total_iip: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                      doc="the total logical zIIP processor effective dispatch time.")
    smf70edt_total_icf: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                      doc="the total logical ICF processor effective dispatch time.")
    smf70edt_total_aap: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                      doc="the total logical zAAP processor effective dispatch time.")
    smf70pdt_cp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                               doc="the total logical general purpose processor dispatch time.")
    smf70pdt_ifl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="the total logical IFL processor dispatch time.")
    smf70pdt_iip: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="the total logical zIIP processor dispatch time.")
    smf70pdt_icf: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="the total logical ICF processor dispatch time.")
    smf70pdt_aap: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="the total logical zAAP processor dispatch time.")
    lpar_management_total_cp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                            doc="LPAR management time for logical general purpose processors.")
    lpar_management_total_ifl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                             doc="LPAR management time for logical IFL processors.")
    lpar_management_total_iip: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                             doc="LPAR management time for logical zIIP processors.")
    lpar_management_total_icf: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                             doc="LPAR management time for logical ICF processors.")
    lpar_management_total_aap: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                             doc="LPAR management time for logical zAAP processors.")
    physical_processor_effective_total_cp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                         doc="the effective utilization of the physical general purpose processors resource by the partiiton.")
    physical_processor_effective_total_ifl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                          doc="the effective utilization of the physical IFL processors resource by the partiiton.")
    physical_processor_effective_total_iip: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                          doc="the effective utilization of the physical zIIP processors resource by the partiiton.")
    physical_processor_effective_total_icf: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                          doc="the effective utilization of the physical ICF processors resource by the partiiton.")
    physical_processor_effective_total_aap: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                          doc="the effective utilization of the physical zAAP processors resource by the partiiton.")
    physical_processor_total_total_cp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                     doc="the total utilization of the physical general purpose processors resource by the partiiton.")
    physical_processor_total_total_ifl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                      doc="the total utilization of the physical IFL processors resource by the partiiton.")
    physical_processor_total_total_iip: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                      doc="the total utilization of the physical zIIP processors resource by the partiiton.")
    physical_processor_total_total_icf: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                      doc="the total utilization of the physical ICF processors resource by the partiiton.")
    physical_processor_total_total_aap: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                      doc="the total utilization of the physical zAAP processors resource by the partiiton.")


class Smf70aid(AbstractConcreteBase):
    """Abstract class for structure Smf70Aid - ASID data area section."""

    smf70rmn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Ready minimum value over interval.")
    smf70rmm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Ready maximum value over interval.")
    smf70rtt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Ready total value over interval.")
    smf70r00: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times ready value was zero.")
    smf70r01: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times ready value was 1.")
    smf70r02: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times ready value was 2.")
    smf70r03: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times ready value was 3.")
    smf70r04: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times ready value was 4.")
    smf70r05: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times ready value was 5.")
    smf70r06: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times ready value was 6.")
    smf70r07: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times ready value was 7.")
    smf70r08: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times ready value was 8.")
    smf70r09: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times ready value was 9.")
    smf70r10: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times ready value was 10.")
    smf70r11: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times ready value was 11.")
    smf70r12: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times ready value was 12.")
    smf70r13: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times ready value was 13.")
    smf70r14: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times ready value was 14.")
    smf70r15: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times ready value was 15 or more.")
    smf70imn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="IN users minimum over interval.")
    smf70imm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="IN users maximum over interval.")
    smf70itt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="IN users total value over interval.")
    smf70i00: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times IN users was zero.")
    smf70i01: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times IN users was 1 or 2.")
    smf70i02: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times IN users was 3 or 4.")
    smf70i03: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times IN users was 5 or 6.")
    smf70i04: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times IN users was 7 or 8.")
    smf70i05: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times IN users was 9 or 10.")
    smf70i06: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times IN users was 11 - 15.")
    smf70i07: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times IN users was 16 - 20.")
    smf70i08: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times IN users was 21 - 25.")
    smf70i09: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times IN users was 26 - 30.")
    smf70i10: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times IN users was 31 - 35.")
    smf70i11: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times IN users was 36 or more.")
    smf70omn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Out users minimum over interval.")
    smf70omm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Out users maximum over interval.")
    smf70ott: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Out users total value over interval.")
    smf70o00: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times out users was zero.")
    smf70o01: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times out users was 1 or 2.")
    smf70o02: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times out users was 3 or 4.")
    smf70o03: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times out users was 5 or 6.")
    smf70o04: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times out users was 7 or 8.")
    smf70o05: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times out users was 9 or 10.")
    smf70o06: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times out users was 11 - 15.")
    smf70o07: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times out users was 16 - 20.")
    smf70o08: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times out users was 21 - 25.")
    smf70o09: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times out users was 26 - 30.")
    smf70o10: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times out users was 31 - 35.")
    smf70o11: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times out users was 36 or more.")
    smf70wmn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Wait user minimum over interval.")
    smf70wmm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Wait users maximum over interval.")
    smf70wtt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Wait users total value over interval.")
    smf70w00: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times wait users was zero.")
    smf70w01: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times wait users was 1 or 2.")
    smf70w02: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times wait users was 3 or 4.")
    smf70w03: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times wait users was 5 or 6.")
    smf70w04: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times wait users was 7 or 8.")
    smf70w05: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times wait users was 9 or 10.")
    smf70w06: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times wait users was 11 - 15.")
    smf70w07: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times wait users was 16 - 20.")
    smf70w08: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times wait users was 21 - 25.")
    smf70w09: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times wait users was 26 - 30.")
    smf70w10: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times wait users was 31 - 35.")
    smf70w11: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times wait users was 36 or more.")
    smf70bmn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Batch users minimum over interval.")
    smf70bmm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Batch users maximum over interval.")
    smf70btt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Batch users total value over interval.")
    smf70b00: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times batch users was zero.")
    smf70b01: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times batch users was 1 or 2.")
    smf70b02: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times batch users was 3 or 4.")
    smf70b03: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times batch users was 5 or 6.")
    smf70b04: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times batch users was 7 or 8.")
    smf70b05: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times batch users was 9 or 10")
    smf70b06: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times batch users was 11 - 15.")
    smf70b07: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times batch users was 16 - 20.")
    smf70b08: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times batch users was 21 - 25.")
    smf70b09: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times batch users was 26 - 30.")
    smf70b10: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times batch users was 31 - 35.")
    smf70b11: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times batch users was 36 or more.")
    smf70smn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Started users minimum over interval.")
    smf70smm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Started users maximum over interval.")
    smf70stt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Started users total value over interval.")
    smf70s00: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times users was zero.")
    smf70s01: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times users was 1 or 2.")
    smf70s02: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times users was 3 or 4.")
    smf70s03: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times users was 5 or 6.")
    smf70s04: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times users was 7 or 8.")
    smf70s05: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times users was 9 or 10.")
    smf70s06: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times users was 11 - 15.")
    smf70s07: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times users was 16 - 20.")
    smf70s08: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times users was 21 - 25.")
    smf70s09: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times users was 26 - 30.")
    smf70s10: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times users was 31 - 35.")
    smf70s11: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times users was 36 or more.")
    smf70tmn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="TSO/E users minimum over interval.")
    smf70tmm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="TSO/E users maximum over interval.")
    smf70ttt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="TSO/E users total value over interval.")
    smf70t00: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times TSO/E users was zero.")
    smf70t01: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times TSO/E users was 1 or 2.")
    smf70t02: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times TSO/E users was 3 or 4.")
    smf70t03: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times TSO/E users was 5 or 6.")
    smf70t04: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times TSO/E users was 7 or 8.")
    smf70t05: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times TSO/E users was 9 or 10.")
    smf70t06: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times TSO/E users was 11 - 15.")
    smf70t07: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times TSO/E users was 16 - 20.")
    smf70t08: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times TSO/E users was 21 - 25.")
    smf70t09: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times TSO/E users was 26 - 30.")
    smf70t10: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times TSO/E users was 31 - 35.")
    smf70t11: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times TSO/E users was 36 or more.")
    smf70lmn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Logical ready users minimum over interval.")
    smf70lmm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Logical ready users maximum over interval.")
    smf70ltt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Logical ready users total value over interval.")
    smf70l00: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of times the number of logical ready users was zero.")
    smf70l01: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of times the number of logical ready users was 1 or 2.")
    smf70l02: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of times the number of logical ready users was 3 or 4.")
    smf70l03: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of times the number of logical ready users was 5 or 6.")
    smf70l04: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of times the number of logical ready users was 7 or 8.")
    smf70l05: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of times the number of logical ready users was 9 or 10.")
    smf70l06: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of times the number of logical ready users was 11 - 15.")
    smf70l07: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of times the number of logical ready users was 16 - 20.")
    smf70l08: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of times the number of logical ready users was 21 - 25.")
    smf70l09: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of times the number of logical ready users was 26 - 30.")
    smf70l10: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of times the number of logical ready users was 31 - 35.")
    smf70l11: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of times the number of logical ready users was 36 or more.")
    smf70amn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Logical wait users minimum over interval.")
    smf70amm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Logical wait users maximum over interval.")
    smf70att: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Logical wait users total value over interval.")
    smf70a00: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of times the number of logical wait users was zero.")
    smf70a01: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of times the number of logical wait users was 1 or 2.")
    smf70a02: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of times the number of logical wait users was 3 or 4.")
    smf70a03: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of times the number of logical wait users was 5 or 6.")
    smf70a04: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of times the number of logical wait users was 7 or 8.")
    smf70a05: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of times the number of logical wait users was 9 or 10.")
    smf70a06: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of times the number of logical wait users was 11 - 15.")
    smf70a07: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of times the number of logical wait users was 16 - 20.")
    smf70a08: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of times the number of logical wait users was 21 - 25.")
    smf70a09: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of times the number of logical wait users was 26 - 30.")
    smf70a10: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of times the number of logical wait users was 31 - 35.")
    smf70a11: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of times the number of logical wait users was 36 or more.")
    smf70pmn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Minimum number of ASCH address spaces. An ASCH address space is scheduled by the APPC/MVS transaction scheduler.")
    smf70pmm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Maximum number of ASCH address spaces.")
    smf70ptt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of ASCH address spaces.")
    smf70p00: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of times when 0 ASCH address spaces were found.")
    smf70p01: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of times when 1 - 2 ASCH address spaces were found.")
    smf70p02: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of times when 3 - 4 ASCH address spaces were found.")
    smf70p03: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of times when 5 - 6 ASCH address spaces were found.")
    smf70p04: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of times when 7 - 8 ASCH address spaces were found.")
    smf70p05: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of times when 9 - 10 ASCH address spaces were found.")
    smf70p06: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of times when 11 - 15 ASCH address spaces were found.")
    smf70p07: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of times when 16 - 20 ASCH address spaces were found.")
    smf70p08: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of times when 21 - 25 ASCH address spaces were found.")
    smf70p09: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of times when 26 - 30 ASCH address spaces were found.")
    smf70p10: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of times when 31 - 35 ASCH address spaces were found.")
    smf70p11: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of times when 36 or more ASCH address spaces were found.")
    smf70xmn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Minimum number of OMVS address spaces.")
    smf70xmm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Maximum number of OMVS address spaces.")
    smf70xtt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of OMVS address spaces.")
    smf70x00: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of times when zero OMVS address spaces were found.")
    smf70x01: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of times when 1 - 2 OMVS address spaces were found.")
    smf70x02: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of times when 3 - 4 OMVS address spaces were found.")
    smf70x03: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of times when 5 - 6 OMVS address spaces were found.")
    smf70x04: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of times when 7 - 8 OMVS address spaces were found.")
    smf70x05: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of times when 9 - 10 OMVS address spaces were found.")
    smf70x06: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of times when 11 - 15 OMVS address spaces were found.")
    smf70x07: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of times when 16 - 20 OMVS address spaces were found.")
    smf70x08: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of times when 21 - 25 OMVS address spaces were found.")
    smf70x09: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of times when 26 - 30 OMVS address spaces were found.")
    smf70x10: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of times when 31 - 35 OMVS address spaces were found.")
    smf70x11: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of times when 36 or more OMVS address spaces were found.")
    smf70q00: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of times In Ready users was less or equal N.")
    smf70q01: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times In Ready users was N+1.")
    smf70q02: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times In Ready users was N+2.")
    smf70q03: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Count of times In Ready users was N+3.")
    smf70q04: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of times In Ready users was N+4 or N+5.")
    smf70q05: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of times In Ready users was N+6 to N+10.")
    smf70q06: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of times In Ready users was N+11 to N+15.")
    smf70q07: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of times In Ready users was N+16 to N+20.")
    smf70q08: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of times In Ready users was N+21 to N+30.")
    smf70q09: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of times In Ready users was N+31 to N+40.")
    smf70q10: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of times In Ready users was N+41 to N+60.")
    smf70q11: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of times In Ready users was N+61 or N+80.")
    smf70q12: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of times In Ready users was greater than N+80.")
    smf70srm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of samples taken by SRM")
    smf70cmn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Minimum number of work units for general purpose processors over interval.")
    smf70cmm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Maximum number of work units for general purpose processors over interval.")
    smf70ctt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of work units for general purpose processors over interval.")
    smf70dmn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Minimum number of work units for zAAPs over interval.")
    smf70dmm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Maximum number of work units for zAAPs over interval.")
    smf70dtt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of work units for zAAPs over interval.")
    smf70emn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Minimum number of work units for zIIPs over interval.")
    smf70emm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Maximum number of work units for zIIPs over interval.")
    smf70ett: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Total number of work units for zIIPs over interval.")
    smf70u00: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of times the number of work units was less or equal N.")
    smf70u01: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of times the number of work units was N+1.")
    smf70u02: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of times the number of work units was N+2.")
    smf70u03: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of times the number of work units was N+3.")
    smf70u04: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of times the number of work units was N+4 or N+5.")
    smf70u05: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of times the number of work units was between N+6 and N+10.")
    smf70u06: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of times the number of work units was between N+11 and N+15.")
    smf70u07: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of times the number of work units was between N+16 and N+20.")
    smf70u08: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of times the number of work units was between N+21 and N+30.")
    smf70u09: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of times the number of work units was between N+31 and N+40.")
    smf70u10: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of times the number of work units was between N+41 and N+60.")
    smf70u11: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of times the number of work units was between N+61 and N+80.")
    smf70u12: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of times the number of work units was between N+81 and N+100.")
    smf70u13: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of times the number of work units was between N+101 and N+120.")
    smf70u14: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of times the number of work units was between N+121 and N+150.")
    smf70u15: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Count of times the number of work units was greater N+150.")


class Smf70cpu(AbstractConcreteBase):
    """Abstract class for structure Smf70Cpu - CPU data section."""

    smf70wat: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="CPU wait time, where bit 51 = 1 microsecond. That is, the amount of time that the CPU is not processing instructions (PSW wait state bit is on). Data could be incorrect if a SET CLOCK occurred during the RMF interval. SMF70WAT is used in RMF report calculations Note: This field is incorrect if MVS is running under VM.")
    smf70cnf: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Configuration activity indicator. Bit Meaning when set 0-3 Reserved. 4 Data available for complete interval. 5 CPU reconfigured during post processor duration interval. 6 CPU reconfigured during the measurement interval (data for this CPU is incorrect). 7 CPU online at end of interval.")
    smf70ser: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="CPU serial number (6 hexadecimal digits).")
    smf70typ: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4),
                                                          doc="CPU type. Value Meaning 0 General purpose CP 1 zAAP 2")
    smf70slh: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of entries to the I/O SLIH; number of I/O interruptions that this processor handled by entry into the I/O interrupt handler.")
    smf70tpi: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of TPI (test pending interrupt) with CC=1; number of I/O interruptions that this processor handled from issuing the TPI instruction.")
    smf70vfs: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of samples when the vector bit in the PSA image was on, which is used to determine the percentage of time vector affinity")
    smf70v: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                        doc="Vector configuration Bit Meaning when set 0 Vector was online 1-7 Reserved.")
    smf70pat: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="CPU parked time, where bit 51 = 1 microsecond.")
    smf70tcb: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Number of TCB dispatches for this CPU.")
    smf70srb: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Number of SRB dispatches for this CPU.")
    smf70nio: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Number of I/Os for this CPU.")
    smf70sig: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Total number of SIGPs done by this CPU.")
    smf70wtd: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Wait dispatch count for this CPU.")
    smf70wts: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="The number of times PR/SM issued a warning-track interruption to a logical processor and z/OS was able to return the logical processor")
    smf70wtu: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="The number of times PR/SM issued a warning-track interruption to a logical processor and z/OS was unable to return the logical processor within the grace period.")
    smf70wti: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Amount of time in milliseconds that a logical processor was yielded to PR/SM due to warning-track processing.")
    smf70int: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Duration of the RMF measurement interval, in the form mmsstttF where mm is the minutes, ss is the seconds, ttt is the milliseconds, and F is the sign. (The end of the measurement interval is the sum of the recorded start time and this field.)")
    smf70_core_id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Core identification.")
    smf70_core_flg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                doc="Logical Core Information Bit Meaning when set 0 Core LPAR Busy time is valid. 1-7 Reserved.")
    smf70_cpu_num: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Number of CPU data sections for this core. This value represents the number of threads that are active on this core.")
    smf70_prod: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                            doc="Multithreading core productivity numerator. Divide this value by 1024 to get the multithreading core productivity. A zero value is reported if the core was not configured ONLINE for the complete interval. If SMF70_CPU_NUM is greater than 1, the core productivity represents the percentage of how much work the core resources accomplished while dispatched to physical hardware over the maximum amount of work the core resources could have accomplished while dispatched to physical hardware.")
    smf70_lpar_busy: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                   doc="Multithreading core LPAR Busy Time in milliseconds. This field is valid if bit 0 of SMF70_CORE_FLG is set.")
    smf70pdt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Logical processor dispatch time, in microseconds. This is the number of microseconds that were accumulated during the measurement interval (during which a physical CPU was assigned to this logical CPU). When associated with partition name PHYSICAL , this field contains the accumulated number of microseconds during which a physical CPU was busy, but the time could not be attributed to a specific logical partition. This time includes the time PR/SM was controlling the physical processor (LPAR management time), as well as any other time the processor was busy for any reason such as managing coupling facility traffic.")
    smf70edt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Logical processor effective dispatch time, in microseconds. The number of microseconds that were accumulated during the measurement interval (excluding LPAR management time), during which a physical CPU was assigned to this logical CPU. When associated with partition name PHYSICAL , this field contains the accumulated number of microseconds during which a physical CPU was busy, but the time could not be attributed to a specific logical partition or to LPAR management of the physical processor. One example is time used for managing coupling facility traffic. This field is zero, if not supported by the hardware. LPAR management time is the time from SMF70PDT associated")
    smf70bps: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6),
                                                          doc="Partition processor resource weight factor. If the value is X'FFFF', then the partition has been assigned dedicated processors.")
    smf70ont: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Logical processor online time.")
    smf70wst: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Logical processor wait state time. SMF70WST is used only for internal purposes.")
    smf70mtit: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                             doc="Multithreading Idle Time in microseconds accumulated for all threads of a dispatched core. This field is only valid if SMF70MTID is not zero for this")
    smf70vpf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Logical processor flags Bit Meaning when set 0 Wait completion is enabled 1 Wait completion status has changed during interval 2 Weight has changed during interval 3 'Initial Capping' was set to 'ON' on the Hardware Management Console 4 'Initial Capping' status has changed during the interval 5 Logical processor varied online during the measurement interval 6 SMF70HW_Cap_Limit has changed during the interval 7 SMF70HWGr_Name or SMF70HWGr_Cap_Limit has changed during the interval")
    smf70pof: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Polarization flags Bit Meaning when set 0 - 1 Polarization indicator: 00 Horizontally polarized or polarization not indicated 01 Vertically polarized with low entitlement 10 Vertically polarized with medium entitlement 11 Vertically polarized with high entitlement 2 Polarization indication changed during interval")
    sub_core_idx: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="sub core index.")
    rate_io_interrupt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                     doc="the total rate per second that this processor handled I/O interrupts.")
    rate_io_interrupt_by_tpi: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                            doc="the percentage of the total interrupts for this processor during the interval that are handled by the I/O supervisor without re-enabling.")
    cpu_unparked_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                     doc="the time the logical processor was unaprked.")
    cpu_parked_percentage: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                         doc="the percentage of time that the logical processor was parked.")
    cpu_unparked_percentage: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                           doc="the percentage of time that the logical processor was unparked.")
    cpu_busy_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="the time the logical processor was busy.")
    cpu_busy_percentage: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                       doc="the percentage of the online time that the logical processor was dispatched.")
    mvs_busy_percentage: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                       doc="the percentage of the online time that the logical processor was busy.")
    rate_tcb: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="the rate per second that this processor dispatched TCB.")
    rate_srb: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="the rate per second that this processor dispatched SRB.")
    rate_io: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="the rate per second that this processor dispatched IO.")
    lpar_busy_percentage: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                        doc="the percentage of this processor lpar busy time.")
    lpb_valid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                           doc="smf70_core_flg (Bit 0) indicating core LPAR Busy time is valid.")
    wait_completion_status: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                        doc="smf70vpf (Bit 0) - Wait completion is enabled.")
    cpu_polarization: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4),
                                                                  doc="smf70pof (Bit 0 - 1) Polarization indicator.")
    mt_prod: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="the percentage of the maximum core capacity that was used in the reporting interval while the logical core of this processor was dsipatched to physical hardware.")
    mt_util: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="the percentage of the maximum core capacity of this processor that was used in the reporting interval.")
    cpu_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="the actual processor busy time.")
    time_range: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="the actual processor available to dispatch time.")
    mvs_busy_total: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                  doc="the online time that the processor was busy.")


class Smf70typ3(AbstractConcreteBase):
    """Abstract class for structure Smf70Typ3 - Cryptographic CCA Coprocessor data section."""

    r7023ct: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6),
                                                         doc="Crypto processor type: Value Meaning 11 CEX5C 12 CEX6C 13 CEX7C 14 CEX8C")
    r7023msk: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Validity bit mask. Each bit position represents the validity of a timer-counter pair that measures the execution time and number of operations on a cryptographic coprocessor card. Bit Meaning when set 0 Valid data for all operations 1 Valid data for RSA-key-generation operations 2-7 Reserved. Valid with SMF70SRL ≥ X'61'(97).")
    r7023mt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Reserved for diagnostic purposes.")
    r7023sf: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="Scaling factor for this cryptographic coprocessor. Execution times in this data section have to be multiplied by this scaling factor to achieve a value in seconds.")
    r7023t0: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="Execution time of all operations on the specified cryptographic coprocessor.")
    r7023c0: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="Number of all operations on the specified cryptographic coprocessor.")
    r7023c1: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Number of all RSA-key-generation operations.")
    r7023did: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Domain ID")
    smf70int: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Duration of the RMF measurement interval, in the form mmsstttF where mm is the minutes, ss is the seconds, ttt is the milliseconds, and F is the sign. (The end of the measurement interval is the sum of the recorded start time and this field.)")
    smf_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    smf70ptn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="PR/SM partition number of the partition that wrote this record.")


class Smf70typ4(AbstractConcreteBase):
    """Abstract class for structure Smf70Typ4 - Cryptographic accelerator data section."""

    r7024ct: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6),
                                                         doc="Crypto processor type: Value Meaning 11 CEX5A 12 CEX6A 13 CEX7A 14 CEX8A")
    r7024msk: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Validity bit mask. Each bit position represents the validity of a timer-counter pair that measures the execution time and number of operations on a cryptographic accelerator card for a certain type of RSA operations. Bit Meaning when set 0 Valid data for 1024-bit ME-format RSA operations 1 Valid data for 2048-bit ME-format RSA operations 2 Valid data for 1024-bit CRT-format RSA operations 3 Valid data for 2048-bit CRT-format RSA operations 4 Valid data for 4096-bit ME-format RSA operations 5 Valid data for 4096-bit CRT-format RSA operations 6-7 Reserved Valid with SMF70SRL ≥ X'5B'(91).")
    r7024mt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Reserved for diagnostic purposes.")
    r7024en: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                         doc="Number of engines on the Crypto accelerator card. Specifies the number of valid entries in the R7024TC array.")
    r7024sf: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="Scaling factor for this cryptographic accelerator. Execution times in this data section have to be multiplied by this scaling factor to")
    r7021met_1: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="engine 1 - Execution time for all operations in 1024-bit-ME format.")
    r7021met_2: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="engine 2 - Execution time for all operations in 1024-bit-ME format.")
    r7021met_3: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="engine 3 - Execution time for all operations in 1024-bit-ME format.")
    r7021met_4: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="engine 4 - Execution time for all operations in 1024-bit-ME format.")
    r7021met_5: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="engine 5 - Execution time for all operations in 1024-bit-ME format.")
    r7021mec_1: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="engine 1 - Number of all operations in 1024-bit-ME format.")
    r7021mec_2: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="engine 2 - Number of all operations in 1024-bit-ME format.")
    r7021mec_3: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="engine 3 - Number of all operations in 1024-bit-ME format.")
    r7021mec_4: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="engine 4 - Number of all operations in 1024-bit-ME format.")
    r7021mec_5: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="engine 5 - Number of all operations in 1024-bit-ME format.")
    r7022met_1: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="engine 1 - Execution time for all operations in 2048-bit-ME format.")
    r7022met_2: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="engine 2 - Execution time for all operations in 2048-bit-ME format.")
    r7022met_3: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="engine 3 - Execution time for all operations in 2048-bit-ME format.")
    r7022met_4: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="engine 4 - Execution time for all operations in 2048-bit-ME format.")
    r7022met_5: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="engine 5 - Execution time for all operations in 2048-bit-ME format.")
    r7022mec_1: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="engine 1 - Number of all operations in 2048-bit-ME format.")
    r7022mec_2: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="engine 2 - Number of all operations in 2048-bit-ME format.")
    r7022mec_3: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="engine 3 - Number of all operations in 2048-bit-ME format.")
    r7022mec_4: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="engine 4 - Number of all operations in 2048-bit-ME format.")
    r7022mec_5: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="engine 5 - Number of all operations in 2048-bit-ME format.")
    r7021crt_1: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="engine 1 - Execution time for all operations in 1024-bit-CRT format.")
    r7021crt_2: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="engine 2 - Execution time for all operations in 1024-bit-CRT format.")
    r7021crt_3: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="engine 3 - Execution time for all operations in 1024-bit-CRT format.")
    r7021crt_4: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="engine 4 - Execution time for all operations in 1024-bit-CRT format.")
    r7021crt_5: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="engine 5 - Execution time for all operations in 1024-bit-CRT format.")
    r7021crc_1: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="engine 1 - Number of all operations in 1024-bit-CRT format.")
    r7021crc_2: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="engine 2 - Number of all operations in 1024-bit-CRT format.")
    r7021crc_3: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="engine 3 - Number of all operations in 1024-bit-CRT format.")
    r7021crc_4: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="engine 4 - Number of all operations in 1024-bit-CRT format.")
    r7021crc_5: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="engine 5 - Number of all operations in 1024-bit-CRT format.")
    r7022crt_1: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="engine 1 - Execution time for all operations in 2048-bit-CRT format.")
    r7022crt_2: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="engine 2 - Execution time for all operations in 2048-bit-CRT format.")
    r7022crt_3: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="engine 3 - Execution time for all operations in 2048-bit-CRT format.")
    r7022crt_4: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="engine 4 - Execution time for all operations in 2048-bit-CRT format.")
    r7022crt_5: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="engine 5 - Execution time for all operations in 2048-bit-CRT format.")
    r7022crc_1: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="engine 1 - Number of all operations in 2048-bit-CRT format.")
    r7022crc_2: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="engine 2 - Number of all operations in 2048-bit-CRT format.")
    r7022crc_3: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="engine 3 - Number of all operations in 2048-bit-CRT format.")
    r7022crc_4: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="engine 4 - Number of all operations in 2048-bit-CRT format.")
    r7022crc_5: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                              doc="engine 5 - Number of all operations in 2048-bit-CRT format.")
    r7023met: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Execution time for all operations in 4096-bit ME-format.")
    r7023mec: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of all operations in 4096-bit ME-format.")
    r7023crt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Execution time for all operations in 4096-bit CRT-format.")
    r7023crc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of all operations in 4096-bit CRT-format.")
    r7024did: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Domain ID")
    smf_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    smf70int: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Duration of the RMF measurement interval, in the form mmsstttF where mm is the minutes, ss is the seconds, ttt is the milliseconds, and F is the sign. (The end of the measurement interval is the sum of the recorded start time and this field.)")
    smf70ptn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="PR/SM partition number of the partition that wrote this record.")


class Smf70typ5(AbstractConcreteBase):
    """Abstract class for structure Smf70Typ5 - Cryptographic PKCS11 coprocessor data section."""

    r7025ct: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6),
                                                         doc="Crypto processor type: Value Meaning 11 CEX5P 12 CEX6P 13 CEX7P 14")
    r7025msk: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Validity bit mask. Each bit position represents the validity of a timer-counter pair that measures the execution time and number of operations by functions on a cryptographic PKCS11 coprocessor. Bit Meaning when set 0 Valid data for operations by slow asymmetric-key functions 1 Valid data for operations by fast asymmetric-key functions 2 Valid data for operations by symmetric-key functions (partial or incremental results) 3 Valid data for operations by symmetric-key functions (complete or final result) 4 Valid data for operations by asymmetric-key generation functions 5-7")
    r7025mt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Reserved for diagnostic purposes.")
    r7025sf: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                           doc="Scaling factor for this cryptographic PKCS11 coprocessor. Execution times in this data section have to be multiplied by this scaling factor to achieve a value in seconds.")
    r7025sat: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Aggregate execution time of operations by slow asymmetric-key functions.")
    r7025sac: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of operations by slow asymmetric-key functions.")
    r7025fat: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Aggregate execution time of operations by fast asymmetric-key functions.")
    r7025fac: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of operations by fast asymmetric-key functions.")
    r7025spt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Aggregate execution time of operations by symmetric-key functions that return partial or incremental results.")
    r7025spc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of operations by symmetric-key functions that return partial or incremental results.")
    r7025sct: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Aggregate execution time of operations by symmetric-key functions that return a complete or final result.")
    r7025scc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of operations by symmetric-key functions that return a complete or final result.")
    r7025agt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Aggregate execution time of operations by asymmetric-key generation function.")
    r7025agc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of operations by asymmetric-key generation function.")
    r7025did: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Domain ID")
    smf70int: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Duration of the RMF measurement interval, in the form mmsstttF where mm is the minutes, ss is the seconds, ttt is the milliseconds, and F is the sign. (The end of the measurement interval is the sum of the recorded start time and this field.)")
    smf_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    smf70ptn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="PR/SM partition number of the partition that wrote this record.")


class Smf70ccf(AbstractConcreteBase):
    """Abstract class for structure Smf70Ccf - ICSF service data section."""

    r702snec: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Single DES: Number of calls to encipher the data.")
    r702sneb: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Single DES: Number of bytes of data enciphered.")
    r702snei: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Single DES: Number of instructions used to encipher the data.")
    r702tnec: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Triple DES: Number of calls to encipher the data.")
    r702tneb: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Triple DES: Number of bytes of data enciphered.")
    r702tnei: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Triple DES: Number of instructions used to encipher the data.")
    r702sndc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Single DES: Number of calls to decipher the data.")
    r702sndb: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Single DES: Number of bytes of data deciphered.")
    r702sndi: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Single DES: Number of instructions used to decipher the data.")
    r702tndc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Triple DES: Number of calls to decipher the data.")
    r702tndb: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Triple DES: Number of bytes of data deciphered.")
    r702tndi: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Triple DES: Number of instructions used to decipher the data.")
    r702nmgc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of calls to generate the message authentication code (MAC).")
    r702nmgb: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of bytes of data for which the MAC was generated.")
    r702nmgi: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of PCMF instructions used to generate the MAC.")
    r702nmvc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Number of calls to verify the MAC.")
    r702nmvb: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of bytes of data for which the MAC was verified.")
    r702nmvi: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of PCMF instructions used to verify the MAC.")
    r702nhac: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="For SHA-1 hashing: Number of calls to hash the data.")
    r702nhab: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="For SHA-1 hashing: Number of bytes of data which was hashed.")
    r702nhai: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="For SHA-1 hashing: Number of PCMF instructions used to hash the data.")
    r702nptc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Number of calls to translate the PIN.")
    r702npvc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Number of calls to verify the PIN.")
    r702nh2c: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="For SHA-224 and SHA-256 hashing: Number of calls to hash the data.")
    r702nh2b: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="For SHA-224 and SHA-256 hashing: Number of bytes of data which was hashed.")
    r702nh2i: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="For SHA-224 and SHA-256 hashing: Number of PCMF instructions used to hash the data.")
    r702nh5c: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="For SHA-384 and SHA-512 hashing: Number of calls to hash the data.")
    r702nh5b: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="For SHA-384 and SHA-512 hashing: Number of bytes of data which was hashed.")
    r702nh5i: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="For SHA-384 and SHA-512 hashing: Number of PCMF instructions used to hash the data.")
    r702cdlv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="ICSF data level.")
    r702aesc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of AES encipher calls sent to a coprocessor.")
    r702aesb: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of bytes processed by the AES encipher services handled by a coprocessor.")
    r702aesi: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of operations required to complete the AES encipher service calls to a coprocessor.")
    r702asdc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of AES decipher calls sent to a coprocessor.")
    r702asdb: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of bytes processed by the AES decipher services handled by a coprocessor.")
    r702asdi: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of operations required to complete the AES decipher service calls to a coprocessor.")
    r702drgc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of calls to generate the RSA digital signatures.")
    r702drvc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of calls to verify the RSA digital signatures.")
    r702degc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of calls to generate the ECC digital signatures.")
    r702devc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of calls to verify the ECC digital signatures.")
    r702amgc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Number of calls to generate the AES MACs.")
    r702amgb: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of bytes of data for which the AES MACs were generated.")
    r702amgi: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of instructions used to generate the AES MACs.")
    r702amvc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Number of calls to verify the AES MACs.")
    r702amvb: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of bytes of data for which the AES MACs were verified.")
    r702amvi: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of instructions used to verify the AES MACs.")
    r702fpec: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Number of calls to encipher data using FPE.")
    r702fpeb: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of bytes of data enciphered using FPE.")
    r702fpei: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of instructions used to encipher the data using FPE.")
    r702fpdc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Number of calls to decipher data using FPE.")
    r702fpdb: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of bytes of data deciphered using FPE.")
    r702fpdi: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of instructions used to decipher the data using FPE.")
    r702fptc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of calls to translate data using FPE.")
    r702fptb: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of bytes of data translated using FPE.")
    r702fpti: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of instructions used to translate the data using FPE.")
    r702fxec: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Number of calls to encipher data using FFX.")
    r702fxeb: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of bytes of data enciphered using FFX.")
    r702fxei: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of instructions used to encipher the data using FFX.")
    r702fxdc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Number of calls to decipher data using FFX.")
    r702fxdb: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of bytes of data deciphered using FFX.")
    r702fxdi: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of instructions used to decipher the data using FFX.")
    r702fxtc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of calls to translate data using FFX.")
    r702fxtb: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of bytes of data translated using FFX.")
    r702fxti: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of instructions used to translate the data using FFX.")
    r702dqgc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of calls to generate the QSA digital signatures.")
    r702dqvc: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Number of calls to verify the QSA digital signatures.")
    smf_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), doc="the SMF type and subtype.")
    smf70ptn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="PR/SM partition number of the partition that wrote this record.")


class Smf70bpd(AbstractConcreteBase):
    """Abstract class for structure Smf70Bpd - PR/SM logical processor data section."""

    smf70pdt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Logical processor dispatch time, in microseconds. This is the number of microseconds that were accumulated during the measurement interval (during which a physical CPU was assigned to this logical CPU). When associated with partition name PHYSICAL , this field contains the accumulated number of microseconds during which a physical CPU was busy, but the time could not be attributed to a specific logical partition. This time includes the time PR/SM was controlling the physical processor (LPAR management time), as well as any other time the processor was busy for any reason such as managing coupling facility traffic.")
    smf70bps: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6),
                                                          doc="Partition processor resource weight factor. If the value is X'FFFF', then the partition has been assigned dedicated processors.")
    smf70vpf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Logical processor flags Bit Meaning when set 0 Wait completion is enabled 1 Wait completion status has changed during interval 2 Weight has changed during interval 3 'Initial Capping' was set to 'ON' on the Hardware Management Console 4 'Initial Capping' status has changed during the interval 5 Logical processor varied online during the measurement interval 6 SMF70HW_Cap_Limit has changed during the interval 7 SMF70HWGr_Name or SMF70HWGr_Cap_Limit has changed during the interval")
    smf70pof: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Polarization flags Bit Meaning when set 0 - 1 Polarization indicator: 00 Horizontally polarized or polarization not indicated 01 Vertically polarized with low entitlement 10 Vertically polarized with medium entitlement 11 Vertically polarized with high entitlement 2 Polarization indication changed during interval")
    smf70cix: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4),
                                                          doc="EBCDIC name corresponding to the CPU type of the logical processor in CPU-identification name section.")
    smf70edt: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Logical processor effective dispatch time, in microseconds. The number of microseconds that were accumulated during the measurement interval (excluding LPAR management time), during which a physical CPU was assigned to this logical CPU. When associated with partition name PHYSICAL , this field contains the accumulated number of microseconds during which a physical CPU was busy, but the time could not be attributed to a specific logical partition or to LPAR management of the physical processor. One example is time used for managing coupling facility traffic. This field is zero, if not supported by the hardware. LPAR management time is the time from SMF70PDT associated")
    smf70acs: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Accumulated processor actual share. To get the average processor actual share, this value has to be divided by the number of Diagnose samples (field SMF70DSA in the CPU control section).")
    smf70mis: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Processor minimum share.")
    smf70mas: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Processor maximum share.")
    smf70nsi: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of samples within 10% of the specified minimum.")
    smf70nsa: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of samples within 10% of the specified maximum.")
    smf70ont: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="Logical processor online time.")
    smf70wst: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Logical processor wait state time. SMF70WST is used only for internal purposes.")
    smf70pma: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Average adjustment weight for pricing management. This value may be negative.")
    smf70nsw: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of diagnose samples where WLM considers to cap the set of logical CPUs of type SMF70CIX within the logical partition (see also SMF70NCA).")
    smf70pow: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Polarization weight for the logical CPU when HiperDispatch mode is active. See bit 2 of SMF70PFL. Multiplied by a factor of 4096 for more granularity. The value may be the same or different for all shared CPUs of type SMF70CIX. This is an accumulated value. Divide by the number of Diagnose samples SMF70DSA to get average weight value for the interval.")
    smf70nca: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of diagnose samples where capping actually limited the usage of processor resources for the set of logical CPUs of type SMF70CIX within the logical partition.")
    smf70hw_cap_limit: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                   doc="If not zero, absolute limit on partition usage of all CPUs of the type indicated in SMF70CIX in terms of a number specified in hundredths of a CPU. For example, a value of 250 indicates that the partition is limited to using 2.5 CPUs.")
    smf70hwgr_cap_limit: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                     doc="If not zero, absolute limit on partition usage of all CPUs of the type indicated in SMF70CIX that are members of the same hardware group, in terms of a number specified in hundredths of a CPU. For example, a value of 250 indicates that the hardware group is limited to using 2.5 CPUs.")
    smf70mtit: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                             doc="Multithreading Idle Time in microseconds accumulated for all threads of a dispatched core. This field is only valid if SMF70MTID is not zero for this")
    smf70lpf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Additional processor flags. Bit Meaning when set 0 Topology has changed during this interval. 1 - 7")
    smf70maxnl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                            doc="with a maximum of 6. Value Meaning 0 The model does not provide information about the topological nesting levels. 1 There is no actual topological nesting structure. 2 - 6 Topological nesting levels are available, beginning with field")
    smf70cordl1: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                             doc="Coordinate of the preferred dispatch location of the logical core at topological nesting level 1. Valid if SMF70MaxNL > 0.")
    smf70cordl2: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                             doc="Coordinate of the preferred dispatch location of the logical core at topological nesting level 2. Valid if SMF70MaxNL > 1.")
    smf70cordl3: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                             doc="Coordinate of the preferred dispatch location of the logical core at topological nesting level 3. Valid if SMF70MaxNL > 2")
    smf70cordl4: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                             doc="Coordinate of the preferred dispatch location of the logical core at topological nesting level 4. Valid if SMF70MaxNL > 3")
    smf70cordl5: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                             doc="Coordinate of the preferred dispatch location of the logical core at topological nesting level 5. Valid if SMF70MaxNL > 4")
    smf70cordl6: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                             doc="Coordinate of the preferred dispatch location of the logical core at topological nesting level 6. Valid if SMF70MaxNL > 5")
    smf70lpm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Logical partition name.")
    smf70stn: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="System name. Blank, if not provided or supported by the operating system in the logical partition.")
    smf70lpn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Logical partition number.")
    share_current: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                 doc="the accumulated processor current share.")
    cpu_count: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                           doc="the number of logical processors of this kind in this partition.")
    physical_cpu_count: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                    doc="the number of physical processors of this kind in this box.")
    msu_physical: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="the physical MSU of this processor.")
    processor_weight_online: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                           doc="the weight of this processor on the online time.")
    msu_effective: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="the effective MSU of this processor.")
    logical_processor_is_online: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                             doc="this processor is online.")
    utilization_per_cpu_physical: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                doc="the physical utilization of this processor.")
    lpar_management_per_cpu: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                           doc="the lpar management time of this processor.")


class Smf70bct(AbstractConcreteBase):
    """Abstract class for structure Smf70Bct - PR/SM partition data section."""

    smf70lpm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Logical partition name.")
    smf70lpn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Logical partition number.")
    smf70pfg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Partition flags Bit Meaning when set 0 Partition has changed from activated to deactivated, or from deactivated to activated, during interval. 1 Number of logical processors in partition has changed. 2 Number of dedicated processors in partition has changed. 3 Number of shared processors in partition has changed. 4 WLM LPAR management is active for this partition. 5 Wait time field (SMF70WST) is defined. 6 Defined capacity limit has been changed. 7 Reserved.")
    smf70bdn: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of logical CPUs assigned to this partition. This count matches the number of subsequent PR/SM Logical Processor data sections. Starting with z900 processors, SMF70BDN has a different meaning if bit 4 of SMF70INB is set. It then contains the maximum logical processors defined as shown at the HMC. Active logical processors have an online time SMF70ONT greater than zero.")
    smf70bds: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="The PR/SM logical processor data blocks for all partitions are grouped together in the record. PR/SM logical processor data blocks for a given partition are grouped together. To get to the first logical processor data block associated with this partition, skip over the number of logical processor data blocks specified by this field, starting at the first logical processor data block in the record.")
    smf70bda: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Accumulated number of active logical processors at a WLM partition. This value is updated at each measurement cycle. It does not cover the logical processors for a non WLM managed partition. (A partition is WLM managed, if bit 4 of SMF70PFG is set.) To get the average number of logical CPUs, this value has to be divided by the number of Diagnose samples (field SMF70DSA in the CPU control section).")
    smf70spn: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="LPAR cluster name. For z/OS, the LPAR cluster name is the sysplex name. For any other logical partition, the LPAR cluster name is the name provided in the HMC definition of this logical partition. Blank, if partition is not a cluster member.")
    smf70stn: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="System name. Blank, if not provided or supported by the operating system in the logical partition.")
    smf70csf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of megabytes of central storage currently online to this partition.")
    smf70esf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Number of megabytes of expanded storage currently online to this partition.")
    smf70msu: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Defined capacity limit (in millions of service units).")
    smf70pfl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Additional partition flags. Bit Meaning when set 0 Content of SMF70UPI is valid. 1 Group flag. This partition is member of a capacity group. 2 Polarization flag. This partition is vertically polarized. That is, HiperDispatch mode is active. The SMF70POW fields in the logical processor data section are valid for CPUs of this partition. 3 Initial weight instead of current weight should be used to project usage of the members in the capacity group. 4 -15")
    smf70upi: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="User partition ID. Valid if bit 0 of SMF70PFL is set.")
    smf70mtid: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                           doc="Maximum Thread Identification. A non-zero value indicates that PROCVIEW CORE is effective for this partition and the hardware supports multithreading.")
    smf70gnm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="Name of the capacity group to which this partition belongs. Valid if bit 1 of SMF70PFL is set.")
    smf70gmu: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Maximum licensing units of a group. The maximum number of processor licensing units for the group of logical partitions of which this partition is a member, and which may be consumed per unit of time, on average. Valid if bit 1 of SMF70PFL is set.")
    smf70hwgr_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                                doc="Name of the hardware group to which this partition belongs.")
    smf70_boostinfo: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                 doc="Boost information Bit Meaning when set 0 zIIP boost was active at some point within the interval. 1 Speed boost was active at some point within the interval. 2-7 Reserved.")
    smf70int: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Duration of the RMF measurement interval, in the form mmsstttF where mm is the minutes, ss is the seconds, ttt is the milliseconds, and F is the sign. (The end of the measurement interval is the sum of the recorded start time and this field.)")
    smf70xnm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="Sysplex name as defined in parmlib member COUPLExx.")
    smf70cpa_actual: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                 doc="Physical CPU adjustment factor based on Model Capacity Rating (will be used for converting processor time to service units). This value together with SMF70CPA_scaling_factor replaces SMF70CPA.")
    smf70cpa_scaling_factor: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                         doc="Scaling factor for SMF70CPA_actual.")
    defined_cpu_count_cp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                      doc="number of CP defined on this box.")
    defined_cpu_count_iip: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                       doc="number of zIIP defined on this box.")
    defined_cpu_count_icf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                       doc="number of ICF defined on this box.")
    sysplex_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="the sysplex name.")
    system_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="the partition system name.")
    smf70acs_cp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                               doc="accumulated general purpose processor actual share.")
    total_smf70acs_cp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                     doc="total accumulated general purpose processor actual share.")
    min_entitlement: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                   doc="the minimum entitlement of this partiion.")
    max_entitlement: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                   doc="the maximum entitlement of this partiont.")
    wgt_cp: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6),
                                                        doc="the processor weight of general process CPs.")
    wgt_ifl: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="the processor weight of IFL processors.")
    wgt_icf: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="the processor weight of ICF processors.")
    wgt_iip: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="the processor weight of zIIP processors.")
    wgt_cbp: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="the processor weight of CBP processors.")
    wgt_ifa: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6), doc="the processor weight of zAAP processors.")
    total_weight_cp: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6),
                                                                 doc="the total weightings of general process CPs.")
    total_weight_ifl: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6),
                                                                  doc="the total weightings of IFL procesors.")
    total_weight_iip: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6),
                                                                  doc="the total weightings of zIIP processors.")
    total_weight_icf: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6),
                                                                  doc="the total weightings of ICF processors.")
    total_weight_aap: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6),
                                                                  doc="the total weightings of zAAP processors.")
    smf70edt_total_cp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                     doc="the total logical general purpose processor effective dispatch time.")
    smf70edt_total_ifl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                      doc="the total logical IFL processor effective dispatch time.")
    smf70edt_total_iip: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                      doc="the total logical zIIP processor effective dispatch time.")
    smf70edt_total_icf: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                      doc="the total logical ICF processor effective dispatch time.")
    smf70edt_total_aap: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                      doc="the total logical zAAP processor effective dispatch time.")
    smf70pdt_cp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                               doc="the total logical general purpose processor dispatch time.")
    smf70pdt_ifl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="the total logical IFL processor dispatch time.")
    smf70pdt_iip: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="the total logical zIIP processor dispatch time.")
    smf70pdt_icf: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="the total logical ICF processor dispatch time.")
    smf70pdt_aap: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                doc="the total logical zAAP processor dispatch time.")
    lpar_management_total_cp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                            doc="LPAR management time for logical general purpose processors.")
    lpar_management_total_ifl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                             doc="LPAR management time for logical IFL processors.")
    lpar_management_total_iip: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                             doc="LPAR management time for logical zIIP processors.")
    lpar_management_total_icf: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                             doc="LPAR management time for logical ICF processors.")
    lpar_management_total_aap: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                             doc="LPAR management time for logical zAAP processors.")
    physical_processor_effective_total_cp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                         doc="the effective utilization of the physical general purpose processors resource by the partiiton.")
    physical_processor_effective_total_ifl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                          doc="the effective utilization of the physical IFL processors resource by the partiiton.")
    physical_processor_effective_total_iip: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                          doc="the effective utilization of the physical zIIP processors resource by the partiiton.")
    physical_processor_effective_total_icf: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                          doc="the effective utilization of the physical ICF processors resource by the partiiton.")
    physical_processor_effective_total_aap: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                          doc="the effective utilization of the physical zAAP processors resource by the partiiton.")
    physical_processor_total_total_cp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                     doc="the total utilization of the physical general purpose processors resource by the partiiton.")
    physical_processor_total_total_ifl: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                      doc="the total utilization of the physical IFL processors resource by the partiiton.")
    physical_processor_total_total_iip: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                      doc="the total utilization of the physical zIIP processors resource by the partiiton.")
    physical_processor_total_total_icf: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                      doc="the total utilization of the physical ICF processors resource by the partiiton.")
    physical_processor_total_total_aap: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                                                      doc="the total utilization of the physical zAAP processors resource by the partiiton.")


class Smf70trg(AbstractConcreteBase):
    """Abstract class for structure Smf70Trg - Tenant Resource Group data section."""

    smf70_trg_desc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(32), doc="Tenant resource group description.")
    smf70_trg_tntname: so.Mapped[Optional[str]] = so.mapped_column(sa.String(32), doc="Tenant name.")
    smf70_trg_sbid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64), doc="Solution ID.")
    smf70_trg_sucp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                doc="Service units on CPs consumed by tenant resource group.")
    smf70_trg_suifa: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                 doc="Service units on zAAPs consumed by tenant resource group.")
    smf70_trg_susup: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                 doc="Service units on zIIPs consumed by tenant resource group.")
    smf70_trg_lac: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Long-term average service on general purpose processors in millions of service units per hour consumed by tenant resource group.")
    smf70_trg_lac_cbp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Reserved for future use.")
    smf70_trg_flags: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Reserved for future use.")
    smf70_trg_mem: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                               doc="Memory consumption of tenant resource group in units of 4K frames.")


class Smf70wc(AbstractConcreteBase):
    """Abstract class for section Smf70Wc."""

    smf70wc_array_offset: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                      doc="Offset to workload classification samples array (relative to the start of this data section).")
    smf70wc_element_size: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                      doc="Size of an element in the samples array.")
    smf70wc_classes_num: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                     doc="Number of workload classes in the samples array (equal to its dimension).")
