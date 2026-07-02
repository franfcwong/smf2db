from typing import List, Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
import datetime as dt
from .smf30_base import ReprMixin, Base30, Smf30id, Smf30pss, Smf30cmp, Smf30ura, Smf30prf, Smf30cas, Smf30sap, \
    Smf30ops, Smf30exp, Smf30op, Smf30ud, Smf30uss


class Smf30Id(ReprMixin, Base30, Smf30id, Smf30pss, Smf30cmp):
    """The Smf30Id class stores the Smf30Id section in the smf30_id table."""

    __tablename__ = "smf30_id"
    smf30jbn: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Job or session name. The job name, time, and date that the reader recognized the JOB card (for this job) constitute the job log identification.")
    smf30jnm: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="JES job identifier. Jobs scheduled by the APPC/MVS transaction scheduler (ASCH) start with an 'A' followed by a seven-digit number.")
    smf30stn: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Step number (first step = 1, and so on).")
    smf30asi: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Address space identifier.")
    smf30tme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                  doc="Time since midnight, in hundredths of a second, that the record was moved to the SMF buffer.")
    datetime: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf30arb: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Maximum virtual storage, in bytes, allocated from the local system queue area (LSQA) and the SWA subpools (less than 16 MB).")
    smf30ear: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Maximum virtual storage in bytes allocated from the local system queue area (LSQA) and the SWA subpools (greater than 16 MB).")
    smf30urb: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Maximum virtual storage in bytes allocated from the user subpools (less than 16 MB).")
    smf30eur: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Maximum virtual storage in bytes allocated from the user subpools (greater than 16 MB).")
    smf30hvo: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Amount of 64-bit private storage in bytes that is obtained by this step or job. This includes guarded virtual storage. The SMF30HVO field contains a snapshot value of high virtual private storage allocation. As the memory objects owned by the executed program have already been detached at the time the step or job goes through termination, SMF30HVO contains the memory object size still allocated to the initiator address space, but no longer reflects the memory objects that may have been allocated by the program executed in the job step. In contrast to SMF30HVO, the SMF30HVH field is maintained as a high water mark. Its content reflects the high virtual memory object size that was once allocated by the job step being executed under the initiator address space.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf30syp: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Sysplex name (from the SYSPLEX parameter in the COUPLExx parmlib member).")
    smf30syn: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="System name (from the SYSNAME parameter in the IEASYSxx parmlib member).")
    start_interval: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                              doc="the record written datetime in 5-minute interval.")
    wkl: so.Mapped[str] = so.mapped_column(sa.String(7), doc="the workload group based on the problem program run.")
    smf30typ: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="Subtype identification Value Meaning 1 Job start or start of other work unit. 2 Activity since previous interval ended. Produced only when interval recording is active. 3 Activity for the last interval before step termination. Produced only when interval recording is active. 4 Step total 5 Job termination or termination of other work unit. 6")
    gid: so.Mapped[int] = so.mapped_column(sa.BigInteger,
                                           doc="a hash number generated from the Identification Section.")
    suffix: so.Mapped[int] = so.mapped_column(sa.Integer,
                                              doc="a sequence number for the records which share the same gid.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf30syp, smf30syn, start_interval, wkl, smf30typ, smf30jbn, smf30asi, smf30jnm,
                                smf30stn, gid, suffix),
    )

    smf30_ura: so.Mapped["Smf30Ura"] = so.relationship(back_populates="smf30_id", viewonly=True)
    smf30_prf: so.Mapped["Smf30Prf"] = so.relationship(back_populates="smf30_id", viewonly=True)
    smf30_cas: so.Mapped["Smf30Cas"] = so.relationship(back_populates="smf30_id", viewonly=True)
    smf30_sap: so.Mapped["Smf30Sap"] = so.relationship(back_populates="smf30_id", viewonly=True)
    smf30_ops: so.Mapped["Smf30Ops"] = so.relationship(back_populates="smf30_id", viewonly=True)
    smf30_exps: so.Mapped[List['Smf30Exp']] = so.relationship(back_populates='smf30_id', viewonly=True)
    smf30_opes: so.Mapped[List['Smf30Op']] = so.relationship(back_populates='smf30_id', viewonly=True)
    smf30_uds: so.Mapped[List['Smf30Ud']] = so.relationship(back_populates='smf30_id', viewonly=True)
    smf30_usss: so.Mapped[List['Smf30Uss']] = so.relationship(back_populates='smf30_id', viewonly=True)


class Smf30Ura(ReprMixin, Base30, Smf30ura):
    """The Smf30Ura class stores the Smf30Ura section in the smf30_ura table."""

    __tablename__ = "smf30_ura"
    smf30rdr: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                          doc="Reader device class as defined in JESPARMS. 0 - for TSO/E sessions or started tasks.")
    smf30rdt: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                          doc="Reader device type as defined in JESPARMS. 0 - for TSO/E sessions or started tasks.")
    smf30dcf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Flag word Bit Meaning when set 0 Device connect time may be incorrect If this flag is set, the system resources manager (SRM) disabled the channel measurement while the job was running. If channel measurement is disabled, device connect time is not recorded. Thus, if this bit is set, SMF30TCN and SMF30DCT reflect less than the actual total connect time. 1 If this bit is on, the following fields contain incomplete data: (SRM could not deliver deltas or values for this interval) SMF30AIC  SMF30EIC SMF30AID  SMF30EID SMF30AIW  SMF30EIW SMF30AIS  SMF30EIS 2 Field SMF30TEP is invalid")
    smf30tme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                  doc="Time since midnight, in hundredths of a second, that the record was moved to the SMF buffer.")
    datetime: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    device_connect_time_incorrect: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                               doc="smf30dcf (Bit 0) showing device connect time may be incoorect. If this flag is set, the system resources manager (SRM) disabled the channel measurement while the job was running. If channel measurement is disabled, device connect time is not recorded. Thus, if this bit is set, smf30tcn and smf30dct reflect less than the actual total connect time.")
    dcf_incomplete: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                doc="smf30dcf (Bit 1) showing if this bit is on, the following fields contain incomplete data: (SRM could not deliver deltas or values for this interval) smf30aic, smf30aid, smf30aiw, smf30ais, smf30eic, smf30eid, smf30eiw and smf30eis.")
    smf30tep_inv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="smf30dcf (Bit 2) showing field smf30tep is invalid.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf30syp: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Sysplex name (from the SYSPLEX parameter in the COUPLExx parmlib member).")
    smf30syn: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="System name (from the SYSNAME parameter in the IEASYSxx parmlib member).")
    start_interval: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                              doc="the record written datetime in 5-minute interval.")
    wkl: so.Mapped[str] = so.mapped_column(sa.String(7), doc="the workload group based on the problem program run.")
    smf30typ: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="Subtype identification Value Meaning 1 Job start or start of other work unit. 2 Activity since previous interval ended. Produced only when interval recording is active. 3 Activity for the last interval before step termination. Produced only when interval recording is active. 4 Step total 5 Job termination or termination of other work unit. 6")
    smf30jbn: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Job or session name. The job name, time, and date that the reader recognized the JOB card (for this job) constitute the job log identification.")
    smf30asi: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Address space identifier.")
    smf30jnm: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="JES job identifier. Jobs scheduled by the APPC/MVS transaction scheduler (ASCH) start with an 'A' followed by a seven-digit number.")
    smf30stn: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Step number (first step = 1, and so on).")
    gid: so.Mapped[int] = so.mapped_column(sa.BigInteger,
                                           doc="a hash number generated from the Identification Section.")
    suffix: so.Mapped[int] = so.mapped_column(sa.Integer,
                                              doc="a sequence number for the records which share the same gid.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf30syp, smf30syn, start_interval, wkl, smf30typ, smf30jbn, smf30asi, smf30jnm,
                                smf30stn, gid, suffix),
        sa.ForeignKeyConstraint(
            ['csc', 'smf30syp', 'smf30syn', 'start_interval', 'wkl', 'smf30typ', 'smf30jbn', 'smf30asi', 'smf30jnm',
             'smf30stn', 'gid', 'suffix'],
            ['smf30_id.csc', 'smf30_id.smf30syp', 'smf30_id.smf30syn', 'smf30_id.start_interval', 'smf30_id.wkl',
             'smf30_id.smf30typ', 'smf30_id.smf30jbn', 'smf30_id.smf30asi', 'smf30_id.smf30jnm', 'smf30_id.smf30stn',
             'smf30_id.gid', 'smf30_id.suffix']),
    )

    smf30_id: so.Mapped["Smf30Id"] = so.relationship(back_populates="smf30_ura", viewonly=True)


class Smf30Prf(ReprMixin, Base30, Smf30prf):
    """The Smf30Prf class stores the Smf30Prf section in the smf30_prf table."""

    __tablename__ = "smf30_prf"
    smf30wlm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="Workload name. This field is blank (X'40') when in workload management compatibility mode.")
    smf30scn: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="Service class name. This field will contain SYSOTHER during the time of a WLM POLICY switch.")
    smf30grn: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), doc="Resource group name.")
    smf30rcn: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="Report class name. This field is blank (X'40') during the time of a WLM POLICY switch.")
    smf30pfl: so.Mapped[Optional[str]] = so.mapped_column(sa.String(16),
                                                          doc="Scheduling environment name. Binary zeros if no scheduling environment is specified.")
    smf30pf1: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Performance section flag byte: Value (Name) Meaning X'80' (SMF30PFJ) Job service class association was modified by a system operator prior to job initiation. X'40' (SMF30PFR) Job service class association was modified by a system operator during job execution. X'20' (SMF30PFF) Job initiation forced by a system operator. X'10' (SMF30RTR) Job has been restarted. There is one set of SMF30 records for each time the job is restarted. X'08' (SMF30MSI) Remote system data is incomplete. X'04' (SMF30WMI) Job is executing in a workload manager batch initiator. X'02' (SMF30CCP) Service class assigned to the address space was designated CPU-critical in the WLM service definition. X'01' (SMF30CSP) Service class assigned to the address space was designated storage-critical in the WLM service definition.")
    smf30pf2: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Performance section flag byte: Value (Name) Meaning X'80' (SMF30ASP) Address space was designated storage-critical. X'40' (SMF30SME) Address space cannot be managed to transaction goals, because 'manage region to goals of region' was specified in the WLM service definition. X'20' (SMF30CPR) Address space is currently CPU-protected. X'10' (SMF30SPR) Address space is currently storage-protected. X'08' (SMF30PIN) If this bit is on, the following fields contain incomplete data:")
    smf30inv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Performance section flag byte: Value (Name) Meaning X'80' (SMF30SRV_INV) When this bit is on, it indicates that the value in SMF30SRV has grown past its four byte maximum value capacity of X'FFFFFFFF' and has wrapped back to zero. SMF30SRV_L is the 8-byte equivalent of SMF30SRV. X'40' (SMF30CSU_INV) When this bit is on, it indicates that the value in SMF30CSU has grown past its four byte maximum value capacity of X'FFFFFFFF' and has wrapped back to zero. SMF30CSU_L is the 8-byte equivalent of SMF30CSU. X'20' (SMF30SRB_INV) When this bit is on, it indicates that the value in SMF30SRB has grown past its four byte maximum value capacity of X'FFFFFFFF' and has wrapped back to zero. SMF30SRB_L is the 8-byte equivalent of SMF30SRB. X'10' (SMF30IO_INV) When this bit is on, it indicates that the value in SMF30IO has grown past its four byte maximum value capacity of X'FFFFFFFF' and has wrapped back to zero. SMF30IO_L is the 8-byte equivalent of SMF30IO. X'08' (SMF30MSO_INV) When this bit is on, it indicates that the value in SMF30MSO has grown past its four byte maximum value capacity of X'FFFFFFFF' and has wrapped back to zero. SMF30MSO_L is the 8-byte equivalent of SMF30MSO. X'04 (SMF30ESU_INV) When this bit is on, it indicates that the value in SMF30ESU has grown past its four byte maximum value capacity of")
    smf30zep: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4),
                                                          doc="Contains information associated with a potential future function and no further details are available at this time.")
    smf30jpn: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="Subsystem collection name from IWMCLSFY SUBCOLN.")
    smf30acb: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4),
                                                          doc="Contains information associated with a potential future function, no further details are provided at this time.")
    smf30cr: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4),
                                                         doc="Contains information associated with a potential future function, no further details are provided at this time.")
    smf30_capacity_change_rsn: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4),
                                                                           doc="Indicates the reason that is associated with the present value contained in SMF30_Capacity_Adjustment_Ind. The bit values of this field correspond to those described in RMCTZ_Capacity_Adjustment_Indication of the IRARMCTZ mapping macro. (See MVS Data Areas . )")
    smf30_capacity_flags: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                      doc="Processor capacity flags. Bit (Name) Meaning when set 0 (SMF30_Event_Driven_Intvl_Rec) Indicates that the current interval record was generated as a result of an event, rather than as a result of standard interval expiration based on time. 1 (SMF30_RQSVSUS_Err) Indicates that an error occurred while collecting the data for SMF30SUS following a change in processor capacity. If this bit is found to be on when the record is being written, an additional attempt to collect the data from SRM is made. If that attempt is successful, the data is filled in at that time and the SMF30PIN error bit will be off. 2 (SMF30_Capacity_Data_Err) Indicates that error occurred while collecting the processor capacity data, therefore the following fields are unreliable: SMF30_RCTPCPUA_Actual SMF30_RCTPCPUA_Nominal SMF30_RCTPCPUA_scaling_factor SMF30_Capacity_Adjustment_Ind SMF30_Capacity_Change_Rsn 3 (SMF30_PCD_Rsvd_Exists) Indicates records generated on systems running z/OS V1R7 through z/OS V1R9. When off, this bit indicates records generated on systems running z/OS V1R10 and later.")
    smf30tme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                  doc="Time since midnight, in hundredths of a second, that the record was moved to the SMF buffer.")
    datetime: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf30pfj: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="smf30pf1 (Bit 0) showing job service class association was modified by a system operator prior to job initiation.")
    smf30pfr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="smf30pf1 (Bit 1) showing job service class association was modified by a system operator during job execution.")
    smf30pff: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="smf30pf1 (Bit 2) showing job initiation forced by a system operator.")
    smf30rtr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="smf30pf1 (Bit 3) showing job has been restarted. There is one set of smf30 records for each time the job is restarted.")
    smf30msi: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="smf30pf1 (Bit 4) showing remote system data is incomplete.")
    smf30wmi: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="smf30pf1 (Bit 5) showing job is executing in a workload manager batch initiator.")
    smf30ccp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="smf30pf1 (Bit 6) showing service class assigned to the address space was designated CPU-critical in the WLM service definition.")
    smf30csp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="smf30pf1 (Bit 7) showing service class assigned to the address space was designated stroage-critical in the WLM service definition.")
    smf30asp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="smf30pf2 (Bit 0) showing address space was designated storage-critical.")
    smf30sme: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="smf30pf2 (Bit 1) showing address space cannot be managed to transaction goals, because 'manage region to goals of region' was specified in the WLM service definition.")
    smf30cpr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="smf30pf2 (Bit 2) showing address space is currently CPU-protected.")
    smf30spr: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="smf30pf2 (Bit 3) showing address space is currently storage-protected.")
    smf30pin: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="smf30pf2 (Bit 4) showing if this bit is on , the following fields contain incomplete data: (SRM could not deliver deltas or values for this interval) smf30csu, smf30esu, smf30eta, smf30etc, smf30grn, smf30hqt, smf30io, smf30jpn, smf30jqt, smf30srv_l, smf30srb_l, smf30mso_l, smf30mso, smf30pfl, smf30pfr, smf30rcn, smf30res, smf30rqt, smf30rtr, smf30scn, smf30sme, smf30csu_l, smf30io_l, smf30esu_l, smf30spr, smf30sqt, smf30srb, smf30srv, smf30sus, smf30tat, smf30trs, smf30wlm and smf30crm.")
    smf30crm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="smf30pf2 (Bit 5) showing if this bit is on, it indicates that the address space matched a classification rule that specified 'manage region using goals of both', which means it is managed towards the velocity goal of the region. But transaction completions are reported and used for management of the transaction service classes with response time goals. This option must only be used with CICS TORs. The associated AORs must remain at hte default 'manage region using goals of transaction'.")
    smf30srv_inv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="smf30inv (Bit 0) showing when this bit is on, it indicates that the value in smf30srv has gron past its four byte maximum value capacity of 0xFFFFFFFF and has wrapped back to zero. smf30srv_l is the 8-byte equivalent of smf30srv.")
    smf30csu_inv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="smf30inv (Bit 1) showing when this bit is on, it indicates that the value in smf30csu has gron past its four byte maximum value capacity of 0xFFFFFFFF and has wrapped back to zero. smf30csu_l is the 8-byte equivalent of smf30csu.")
    smf30srb_inv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="smf30inv (Bit 2) showing when this bit is on, it indicates that the value in smf30srb has gron past its four byte maximum value capacity of 0xFFFFFFFF and has wrapped back to zero. smf30srb_l is the 8-byte equivalent of smf30srb.")
    smf30io_inv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                             doc="smf30inv (Bit 3) showing when this bit is on, it indicates that the value in smf30io has gron past its four byte maximum value capacity of 0xFFFFFFFF and has wrapped back to zero. smf30io_l is the 8-byte equivalent of smf30io.")
    smf30mso_inv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="smf30inv (Bit 4) showing when this bit is on, it indicates that the value in smf30mso has gron past its four byte maximum value capacity of 0xFFFFFFFF and has wrapped back to zero. smf30mso_l is the 8-byte equivalent of smf30mso.")
    smf30esu_inv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="smf30inv (Bit 5) showing when this bit is on, it indicates that the value in smf30esu has gron past its four byte maximum value capacity of 0xFFFFFFFF and has wrapped back to zero. smf30esu_l is the 8-byte equivalent of smf30esu.")
    smf30_event_driven_intvl_rec: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                              doc="smf30_capacity_flags (Bit 0) indicates that the current interval record was generated as a result of an event, rather than as a result of standard interval expiration based on time.")
    smf30_rqsvsus_err: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                   doc="smf30_capacity_flags (Bit 1) indicates that an error occured while collecting the data from smf30sus following a change in processor capacity. If this bit is found to be on when the record is being written, an additional attempt to collect the data from SRM is made. If the attempt is successful, the data is filled in at that time and the smf30pin error bit will be off.")
    smf30_capacity_data_err: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                         doc="smf30_capacity_flags (Bit 2) indicates that error occurred while collecting the processor capacity data, therefore the following fields are unreliable: smf30_rctpcpua_actual, smf30_rctpcpua_nominal, smf30_rctpcpua_scaling_factor, smf30_capacity_adjustment_ind and smf30_capacity_change_rsn.")
    smf30_pcd_rsvd_exists: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                       doc="smf30_capacity_flags (Bit 3) indicates record generated on system runing z/OS V1R7 through z/OS V1R9. When off, this bit indicates records generated on systems running z/OS V1R10 and later.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf30syp: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Sysplex name (from the SYSPLEX parameter in the COUPLExx parmlib member).")
    smf30syn: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="System name (from the SYSNAME parameter in the IEASYSxx parmlib member).")
    start_interval: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                              doc="the record written datetime in 5-minute interval.")
    wkl: so.Mapped[str] = so.mapped_column(sa.String(7), doc="the workload group based on the problem program run.")
    smf30typ: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="Subtype identification Value Meaning 1 Job start or start of other work unit. 2 Activity since previous interval ended. Produced only when interval recording is active. 3 Activity for the last interval before step termination. Produced only when interval recording is active. 4 Step total 5 Job termination or termination of other work unit. 6")
    smf30jbn: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Job or session name. The job name, time, and date that the reader recognized the JOB card (for this job) constitute the job log identification.")
    smf30asi: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Address space identifier.")
    smf30jnm: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="JES job identifier. Jobs scheduled by the APPC/MVS transaction scheduler (ASCH) start with an 'A' followed by a seven-digit number.")
    smf30stn: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Step number (first step = 1, and so on).")
    gid: so.Mapped[int] = so.mapped_column(sa.BigInteger,
                                           doc="a hash number generated from the Identification Section.")
    suffix: so.Mapped[int] = so.mapped_column(sa.Integer,
                                              doc="a sequence number for the records which share the same gid.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf30syp, smf30syn, start_interval, wkl, smf30typ, smf30jbn, smf30asi, smf30jnm,
                                smf30stn, gid, suffix),
        sa.ForeignKeyConstraint(
            ['csc', 'smf30syp', 'smf30syn', 'start_interval', 'wkl', 'smf30typ', 'smf30jbn', 'smf30asi', 'smf30jnm',
             'smf30stn', 'gid', 'suffix'],
            ['smf30_id.csc', 'smf30_id.smf30syp', 'smf30_id.smf30syn', 'smf30_id.start_interval', 'smf30_id.wkl',
             'smf30_id.smf30typ', 'smf30_id.smf30jbn', 'smf30_id.smf30asi', 'smf30_id.smf30jnm', 'smf30_id.smf30stn',
             'smf30_id.gid', 'smf30_id.suffix']),
    )

    smf30_id: so.Mapped["Smf30Id"] = so.relationship(back_populates="smf30_prf", viewonly=True)


class Smf30Cas(ReprMixin, Base30, Smf30cas):
    """The Smf30Cas class stores the Smf30Cas section in the smf30_cas table."""

    __tablename__ = "smf30_cas"
    smf30tfl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Invalid timer flags: Bit Meaning when set 0 Indicates that timer flags are used. 1 SMF30CPT has an invalid value due to a timer value calculation error. 2 SMF30CPS has an invalid value due to a timer value calculation error. 3 SMF30JVU has an invalid value due to a timer value calculation error. 4 SMF30JVA has an invalid value due to a timer value calculation error. 5 SMF30ISB has an invalid value due to a timer value calculation error. 6 SMF30ICU has an invalid value due to a timer value calculation error. 7 SMF30IVU has an invalid value due to a timer value calculation error. 8 SMF30IVA has an invalid value due to a timer value calculation error. 9 SMF30IIP has an invalid value due to a timer value calculation error. 10 SMF30HPT has an invalid value due to a timer value calculation error. 11 SMF30RCT has an invalid value due to a timer value calculation error. 12 SMF30ASR has an invalid value due to a timer value calculation error. 13 SMF30ENC has an invalid value due to a timer value calculation error. 14 SMF30DET has an invalid value due to a timer value calculation error. 15")
    smf30ist: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                  doc="Interval start time for type 30 subtype 2 and 3 records, in hundredths of a second.")
    smf30tf2: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Additional timer flags. Bit Meaning when set 0 (SMF30_TIME_ON_IFA_F) SMF30_TIME_ON_IFA has an invalid value due to a timer value calculation error. 1 (SMF30_ENCLAVE_TIME_ON_IFA_F) SMF30_ENCLAVE_TIME_ON_IFA has an invalid value due to a timer value calculation error. 2 (SMF30_DEP_ENCLAVE_TIME_ON_IFA_F) SMF30_DEP_ENCLAVE_TIME_ON_IFA has an invalid value due to a timer value calculation error. 3 (SMF30_TIME_IFA_ON_CP_F) SMF30_TIME_IFA_ON_CP has an invalid value due to a timer value calculation error. 4 (SMF30_ENCLAVE_TIME_IFA_ON_CP_F) SMF30_ENCLAVE_TIME_IFA_ON_CP has an invalid value due to a timer value calculation error. 5 (SMF30_DEP_ENCLAVE_TIME_IFA_ON_CP_F) SMF30_DEP_ENCLAVE_TIME_IFA_ON_CP has an invalid value due to a timer value calculation error. 6 (SMF30_CEPI_F) Indicates failure in SMF30CEPI. 7 (SMF30CRP_F) Indicates failure in SMF30CRP.")
    smf30t32: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Description Additional failure flags. Bit Meaning when set 0 (SMF30_TIME_ON_zIIP_F) SMF30_TIME_ON_zIIP has an invalid value due to a timer value calculation error. 0 (SMF30_TIME_ON_SUP_F) SMF30_TIME_ON_SUP has an invalid value due to a timer value calculation error. 1 (SMF30_ENCLAVE_TIME_ON_zIIP_F) SMF30_ENCLAVE_TIME_ON_zIIP has an invalid value due to a timer value calculation error. 1 (SMF30_ENCLAVE_TIME_ON_SUP_F) SMF30_ENCLAVE_TIME_ON_SUP has an invalid value due to a timer value calculation error. 2 (SMF30_DEP_ENCLAVE_TIME_ON_zIIP_F) SMF30_DEP_ENCLAVE_TIME_ON_zIIP has an invalid value due to a timer value calculation error. 2 (SMF30_DEP_ENCLAVE_TIME_ON_SUP_F) SMF30_DEP_ENCLAVE_TIME_ON_SUP has an invalid value due to a timer value calculation error. 3 (SMF30_TIME_zIIP_ON_CP_F) SMF30_TIME_zIIP_ON_CP has an invalid value due to a timer value calculation error. 3 (SMF30_TIME_SUP_ON_CP_F) SMF30_TIME_SUP_ON_CP has an invalid value due to a timer value calculation error. 4 (SMF30_ENCLAVE_TIME_zIIP_ON_CP_F) SMF30_ENCLAVE_TIME_zIIP_ON_CP has an invalid value due to a timer value calculation error. 4 (SMF30_ENCLAVE_TIME_SUP_ON_CP_F) SMF30_ENCLAVE_TIME_SUP_ON_CP has an invalid value due to a timer value calculation error. 5 (SMF30_DEPENC_TIME_zIIP_ON_CP_F) SMF30_DEPENC_TIME_zIIP_ON_CP has an invalid value due to a timer value calculation error. 5 (SMF30_DEPENC_TIME_SUP_ON_CP_F) SMF30_DEPENC_TIME_SUP_ON_CP has an invalid value due to a timer value calculation error. 6 (SMF30_Time_Java_On_zIIP_F)")
    smf30t33: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Additional failure flags. Bit Meaning when set 0 - 3 Reserved. 4 (SMF30_DEPENC_Time_Java_On_zIIP_F) SMF30_DEPENC_Time_Java_On_zIIP has an invalid value due to a timer value calculation error. 5 (SMF30_Time_Java_On_CP_F) SMF30_Time_Java_On_CP has an invalid value due to a timer value calculation error. 6 (SMF30_ENCLAVE_Time_Java_On_CP_F) SMF30_ENCLAVE_Time_Java_On_CP has an invalid value due to a timer value calculation error. 7 (SMF30_DEPENC_Time_Java_On_CP_F) SMF30_DEPENC_Time_Java_On_CP has an invalid value due to a timer value calculation error.")
    smf30cas_oa54589: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                  doc="OSPROTECT-related flags. These flags are specific to a job step. A job-end (subtype 5) record represents an accumulation of all of the bits defined for each byte, across all job steps; therefore, that data might not be usable to determine the trust state of any individual job step. With respect to OSPROTECT, a job or address space that is not APF-authorized and that has at least one task running in a user key (8 - 15) is considered to be untrusted; otherwise, a")
    smf30tme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                  doc="Time since midnight, in hundredths of a second, that the record was moved to the SMF buffer.")
    datetime: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    timer_used: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                            doc="smf30tfl (Bit 0) indicates that timer flags are used.")
    smf30cpt_inv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="smf30tfl (Bit 1) indicates smf30cpt has an invalid value due to a timer value calculation error.")
    smf30cps_inv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="smf30tfl (Bit 2) indicates smf30cps has an invalid value due to a timer value calculation error.")
    smf30jvu_inv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="smf30tfl (Bit 3) indicates smf30jvu has an invalid value due to a timer value calculation error.")
    smf30jva_inv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="smf30tfl (Bit 4) indicates smf30jva has an invalid value due to a timer value calculation error.")
    smf30isb_inv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="smf30tfl (Bit 5) indicates smf30isb has an invalid value due to a timer value calculation error.")
    smf30icu_inv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="smf30tfl (Bit 6) indicates smf30icu has an invalid value due to a timer value calculation error.")
    smf30ivu_inv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="smf30tfl (Bit 7) indicates smf30ivu has an invalid value due to a timer value calculation error.")
    smf30iva_inv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="smf30tfl (Bit 8) indicates smf30iva has an invalid value due to a timer value calculation error.")
    smf30iip_inv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="smf30tfl (Bit 9) indicates smf30iip has an invalid value due to a timer value calculation error.")
    smf30hpt_inv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="smf30tfl (Bit 10) indicates smf30hpt has an invalid value due to a timer value calculation error.")
    smf30rct_inv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="smf30tfl (Bit 11) indicates smf30rct has an invalid value due to a timer value calculation error.")
    smf30asr_inv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="smf30tfl (Bit 12) indicates smf30asr has an invalid value due to a timer value calculation error.")
    smf30enc_inv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="smf30tfl (Bit 13) indicates smf30enc has an invalid value due to a timer value calculation error.")
    smf30det_inv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="smf30tfl (Bit 14) indicates smf30det has an invalid value due to a timer value calculation error.")
    smf30cep_inv: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                              doc="smf30tfl (Bit 15) indicates smf30cep has an invalid value due to a timer value calculation error.")
    smf30_time_on_ifa_f: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                     doc="smf30tf2 (Bit 0) indicates smf30_time_on_ifa has an invalid value due to timer calculation error.")
    smf30_enclave_time_on_ifa_f: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                             doc="smf30tf2 (Bit 1) indicates smf30_enclave_time_ifa has an invalid value due to timer calculation error.")
    smf30_dep_enclave_time_on_ifa_f: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                                 doc="smf30tf2 (Bit 2) indicates smf30_dep_enclave_time_on_ifa has an invalid value due to timer calculation error.")
    smf30_time_ifa_on_cp_f: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                        doc="smf30tf2 (Bit 3) indicates smf30_time_ifa_on_cp has an invalid value due to timer calculation error.")
    smf30_enclave_time_ifa_on_cp_f: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                                doc="smf30tf2 (Bit 4) indicates smf30_enclave_time_ifa_on_cp has an invalid value due to timer calculation error.")
    smf30_dep_enclave_time_ifa_on_cp_f: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                                    doc="smf30tf2 (Bit 5) indicates smf30_dep_encalve_time_ifa_on_cp has an invalid value due to timer calculation error.")
    smf30_cepi_failed: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                   doc="smf30tf2 (Bit 6) indicates failure in smf30cepi.")
    smf30crp_failed: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                 doc="smf30tf2 (Bit 7) indicates failure in smf30crp.")
    smf30_time_on_ziip_f: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                      doc="smf30t32 (Bit 0) indicates smf30_time_on_ziip has an invalid value due to timer calculation error.")
    smf30_enclave_time_on_ziip_f: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                              doc="smf30t32 (Bit 1) indicates smf30_enclave_time_on_ziip has an invalid value due to timer calculation error.")
    smf30_dep_time_on_ziip_f: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                          doc="smf30t32 (Bit 2) indicates smf30_dep_time_on_ziip has an invalid value due to timer calculation error.")
    smf30_time_ziip_on_cp_f: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                         doc="smf30t32 (Bit 3) indicates smf30_time_ziip_on_cp has an invalid value due to timer calculation error.")
    smf30_enclave_time_ziip_on_cp_f: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                                 doc="smf30t32 (Bit 4) indicates smf30_enclave_time_ziip_on_cp has an invalid value due to timer calculation error.")
    smf30_depenc_time_ziip_on_cp_f: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                                doc="smf30t32 (Bit 5) indicates smf30_depenc_time_ziip_on_cp has an invalid value due to timer calculation error.")
    smf30_time_java_on_ziip_f: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                           doc="smf30t32 (Bit 6) indicates smf30_time_java_on_ziip has an invalid value due to timer calculation error.")
    smf30_enclave_time_java_on_ziip_f: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                                   doc="smf30t32 (Bit 7) indicates smf30_enclave_time_java_on_ziip has an invalid value due to timer calculation error.")
    smf30_enclave_time_ziip_qual_f: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                                doc="smf30t33 (Bit 6) indicates smf30_enclave_time_ziip_qual has an invalid value due to timer calculation error.")
    smf30_depenc_time_ziip_qual_f: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                               doc="smf30t33 (Bit 7) indicates smf30_depenc_time_ziip_qual has an invalid value due to timer calculation error.")
    smf30cas_inelighonorpriority: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                              doc="smf30cas_flag (Bit 0) indicates eligible work in this address space is not offloaded to CPs for help processing. Once this bit is set on for a job interval or step-end record, this bit will also be set on for step-total and job-end records.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf30syp: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Sysplex name (from the SYSPLEX parameter in the COUPLExx parmlib member).")
    smf30syn: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="System name (from the SYSNAME parameter in the IEASYSxx parmlib member).")
    start_interval: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                              doc="the record written datetime in 5-minute interval.")
    wkl: so.Mapped[str] = so.mapped_column(sa.String(7), doc="the workload group based on the problem program run.")
    smf30typ: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="Subtype identification Value Meaning 1 Job start or start of other work unit. 2 Activity since previous interval ended. Produced only when interval recording is active. 3 Activity for the last interval before step termination. Produced only when interval recording is active. 4 Step total 5 Job termination or termination of other work unit. 6")
    smf30jbn: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Job or session name. The job name, time, and date that the reader recognized the JOB card (for this job) constitute the job log identification.")
    smf30asi: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Address space identifier.")
    smf30jnm: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="JES job identifier. Jobs scheduled by the APPC/MVS transaction scheduler (ASCH) start with an 'A' followed by a seven-digit number.")
    smf30stn: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Step number (first step = 1, and so on).")
    gid: so.Mapped[int] = so.mapped_column(sa.BigInteger,
                                           doc="a hash number generated from the Identification Section.")
    suffix: so.Mapped[int] = so.mapped_column(sa.Integer,
                                              doc="a sequence number for the records which share the same gid.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf30syp, smf30syn, start_interval, wkl, smf30typ, smf30jbn, smf30asi, smf30jnm,
                                smf30stn, gid, suffix),
        sa.ForeignKeyConstraint(
            ['csc', 'smf30syp', 'smf30syn', 'start_interval', 'wkl', 'smf30typ', 'smf30jbn', 'smf30asi', 'smf30jnm',
             'smf30stn', 'gid', 'suffix'],
            ['smf30_id.csc', 'smf30_id.smf30syp', 'smf30_id.smf30syn', 'smf30_id.start_interval', 'smf30_id.wkl',
             'smf30_id.smf30typ', 'smf30_id.smf30jbn', 'smf30_id.smf30asi', 'smf30_id.smf30jnm', 'smf30_id.smf30stn',
             'smf30_id.gid', 'smf30_id.suffix']),
    )

    smf30_id: so.Mapped["Smf30Id"] = so.relationship(back_populates="smf30_cas", viewonly=True)


class Smf30Exp(ReprMixin, Base30, Smf30exp):
    """The Smf30Exp class stores the Smf30Exp section in the smf30_exp table."""

    __tablename__ = "smf30_exp"
    smf30cua: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Device number.")
    smf30ddn: so.Mapped[str] = so.mapped_column(sa.String(8), doc="DD Name used to access the data set.")
    smf30dct: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="Device connect time for this data set (in 128 micro-second units). For DIV object, device connect time is not collected by SMF; however, this field may not always be zero. For example, if a user is using a DIV data set and calls a VSAM utility to process it using the same DD statement, this will result in device connect time being charged by VSAM to the DIV object.")
    smf30tme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                  doc="Time since midnight, in hundredths of a second, that the record was moved to the SMF buffer.")
    datetime: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf30syp: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Sysplex name (from the SYSPLEX parameter in the COUPLExx parmlib member).")
    smf30syn: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="System name (from the SYSNAME parameter in the IEASYSxx parmlib member).")
    start_interval: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                              doc="the record written datetime in 5-minute interval.")
    wkl: so.Mapped[str] = so.mapped_column(sa.String(7), doc="the workload group based on the problem program run.")
    smf30typ: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="Subtype identification Value Meaning 1 Job start or start of other work unit. 2 Activity since previous interval ended. Produced only when interval recording is active. 3 Activity for the last interval before step termination. Produced only when interval recording is active. 4 Step total 5 Job termination or termination of other work unit. 6")
    smf30jbn: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Job or session name. The job name, time, and date that the reader recognized the JOB card (for this job) constitute the job log identification.")
    smf30asi: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Address space identifier.")
    smf30jnm: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="JES job identifier. Jobs scheduled by the APPC/MVS transaction scheduler (ASCH) start with an 'A' followed by a seven-digit number.")
    smf30stn: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Step number (first step = 1, and so on).")
    gid: so.Mapped[int] = so.mapped_column(sa.BigInteger,
                                           doc="a hash number generated from the Identification Section.")
    suffix: so.Mapped[int] = so.mapped_column(sa.Integer,
                                              doc="a sequence number for the records which share the same gid.")
    dd_idx: so.Mapped[int] = so.mapped_column(sa.Integer, doc="the index of the EXCP record in the section.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf30syp, smf30syn, start_interval, wkl, smf30typ, smf30jbn, smf30asi, smf30jnm,
                                smf30stn, gid, suffix, smf30cua, smf30ddn, dd_idx),
        sa.ForeignKeyConstraint(
            ['csc', 'smf30syp', 'smf30syn', 'start_interval', 'wkl', 'smf30typ', 'smf30jbn', 'smf30asi', 'smf30jnm',
             'smf30stn', 'gid', 'suffix'],
            ['smf30_id.csc', 'smf30_id.smf30syp', 'smf30_id.smf30syn', 'smf30_id.start_interval', 'smf30_id.wkl',
             'smf30_id.smf30typ', 'smf30_id.smf30jbn', 'smf30_id.smf30asi', 'smf30_id.smf30jnm', 'smf30_id.smf30stn',
             'smf30_id.gid', 'smf30_id.suffix']),
    )

    smf30_id: so.Mapped['Smf30Id'] = so.relationship(back_populates='smf30_exps', viewonly=True)


class Smf30Op(ReprMixin, Base30, Smf30op):
    """The Smf30Op class stores the Smf30Op section in the smf30_op table."""

    __tablename__ = "smf30_op"
    smf30opi: so.Mapped[int] = so.mapped_column(sa.Integer, doc="z/OS UNIX process ID.")
    smf30opg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="z/OS UNIX process group ID.")
    smf30oui: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="z/OS UNIX process user ID.")
    smf30oug: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="z/OS UNIX process user group ID.")
    smf30osi: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="z/OS UNIX process session ID.")
    smf30opp: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, doc="Parent process ID.")
    gid: so.Mapped[int] = so.mapped_column(sa.BigInteger,
                                           doc="a hash number generated from the Identification Section.")
    smf30tme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                  doc="Time since midnight, in hundredths of a second, that the record was moved to the SMF buffer.")
    datetime: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf30syp: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Sysplex name (from the SYSPLEX parameter in the COUPLExx parmlib member).")
    smf30syn: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="System name (from the SYSNAME parameter in the IEASYSxx parmlib member).")
    start_interval: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                              doc="the record written datetime in 5-minute interval.")
    wkl: so.Mapped[str] = so.mapped_column(sa.String(7), doc="the workload group based on the problem program run.")
    smf30typ: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="Subtype identification Value Meaning 1 Job start or start of other work unit. 2 Activity since previous interval ended. Produced only when interval recording is active. 3 Activity for the last interval before step termination. Produced only when interval recording is active. 4 Step total 5 Job termination or termination of other work unit. 6")
    smf30jbn: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Job or session name. The job name, time, and date that the reader recognized the JOB card (for this job) constitute the job log identification.")
    smf30asi: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Address space identifier.")
    smf30jnm: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="JES job identifier. Jobs scheduled by the APPC/MVS transaction scheduler (ASCH) start with an 'A' followed by a seven-digit number.")
    smf30stn: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Step number (first step = 1, and so on).")
    suffix: so.Mapped[int] = so.mapped_column(sa.Integer,
                                              doc="a sequence number for the records which share the same gid.")
    proc_idx: so.Mapped[int] = so.mapped_column(sa.Integer, doc="the index of the process record in the section.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf30syp, smf30syn, start_interval, wkl, smf30typ, smf30jbn, smf30asi, smf30jnm,
                                smf30stn, gid, suffix, smf30opi, proc_idx),
        sa.ForeignKeyConstraint(
            ['csc', 'smf30syp', 'smf30syn', 'start_interval', 'wkl', 'smf30typ', 'smf30jbn', 'smf30asi', 'smf30jnm',
             'smf30stn', 'gid', 'suffix'],
            ['smf30_id.csc', 'smf30_id.smf30syp', 'smf30_id.smf30syn', 'smf30_id.start_interval', 'smf30_id.wkl',
             'smf30_id.smf30typ', 'smf30_id.smf30jbn', 'smf30_id.smf30asi', 'smf30_id.smf30jnm', 'smf30_id.smf30stn',
             'smf30_id.gid', 'smf30_id.suffix']),
    )

    smf30_id: so.Mapped['Smf30Id'] = so.relationship(back_populates='smf30_opes', viewonly=True)


class Smf30Ops(ReprMixin, Base30, Smf30ops):
    """The Smf30Ops class stores the Smf30Ops section in the smf30_ops table."""

    __tablename__ = "smf30_ops"
    smf30tme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                  doc="Time since midnight, in hundredths of a second, that the record was moved to the SMF buffer.")
    datetime: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf30syp: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Sysplex name (from the SYSPLEX parameter in the COUPLExx parmlib member).")
    smf30syn: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="System name (from the SYSNAME parameter in the IEASYSxx parmlib member).")
    start_interval: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                              doc="the record written datetime in 5-minute interval.")
    wkl: so.Mapped[str] = so.mapped_column(sa.String(7), doc="the workload group based on the problem program run.")
    smf30typ: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="Subtype identification Value Meaning 1 Job start or start of other work unit. 2 Activity since previous interval ended. Produced only when interval recording is active. 3 Activity for the last interval before step termination. Produced only when interval recording is active. 4 Step total 5 Job termination or termination of other work unit. 6")
    smf30jbn: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Job or session name. The job name, time, and date that the reader recognized the JOB card (for this job) constitute the job log identification.")
    smf30asi: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Address space identifier.")
    smf30jnm: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="JES job identifier. Jobs scheduled by the APPC/MVS transaction scheduler (ASCH) start with an 'A' followed by a seven-digit number.")
    smf30stn: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Step number (first step = 1, and so on).")
    gid: so.Mapped[int] = so.mapped_column(sa.BigInteger,
                                           doc="a hash number generated from the Identification Section.")
    suffix: so.Mapped[int] = so.mapped_column(sa.Integer,
                                              doc="a sequence number for the records which share the same gid.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf30syp, smf30syn, start_interval, wkl, smf30typ, smf30jbn, smf30asi, smf30jnm,
                                smf30stn, gid, suffix),
        sa.ForeignKeyConstraint(
            ['csc', 'smf30syp', 'smf30syn', 'start_interval', 'wkl', 'smf30typ', 'smf30jbn', 'smf30asi', 'smf30jnm',
             'smf30stn', 'gid', 'suffix'],
            ['smf30_id.csc', 'smf30_id.smf30syp', 'smf30_id.smf30syn', 'smf30_id.start_interval', 'smf30_id.wkl',
             'smf30_id.smf30typ', 'smf30_id.smf30jbn', 'smf30_id.smf30asi', 'smf30_id.smf30jnm', 'smf30_id.smf30stn',
             'smf30_id.gid', 'smf30_id.suffix']),
    )

    smf30_id: so.Mapped["Smf30Id"] = so.relationship(back_populates="smf30_ops", viewonly=True)


class Smf30Ud(ReprMixin, Base30, Smf30ud):
    """The Smf30Ud class stores the Smf30Ud section in the smf30_ud table."""

    __tablename__ = "smf30_ud"
    smf30upo: so.Mapped[Optional[str]] = so.mapped_column(sa.String(16),
                                                          doc="Product owner or vendor name (specified on the PRODOWNER option of the IFAUSAGE macro).")
    smf30upn: so.Mapped[str] = so.mapped_column(sa.String(16),
                                                doc="Product name (specified on the PRODNAME option of the IFAUSAGE macro).")
    smf30upv: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Product version (if specified on the PRODVERS option of the IFAUSAGE macro or 'NONE').")
    smf30upq: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Product qualifier (if specified on the PRODQUAL option of the IFAUSAGE macro or 'NONE').")
    smf30upi: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Product ID (if specified on the PRODID option of the IFAUSAGE macro or 'NONE').")
    smf30urd: so.Mapped[Optional[str]] = so.mapped_column(sa.String(18),
                                                          doc="Product specific resource data (specified on the DATA option on the IFAUSAGE macro FUNCTIONDATA request). SMF30UDF identifies the format of the data in this field.")
    smf30udf: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Data format of value in SMF30URD Value Meaning 0 No data specified. 1 CPU time in long floating Point (in hundredths of a second). 2 Binary (64-bit). 3 Long floating point.")
    smf30ufg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Usage entry flags Bit Meaning when set 0 Unauthorized register 1-7 Unused")
    smf30tme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                  doc="Time since midnight, in hundredths of a second, that the record was moved to the SMF buffer.")
    datetime: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    unauth_register_requested: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                           doc="smf30ufg (Bit 0) indicates unauthorized register.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf30syp: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Sysplex name (from the SYSPLEX parameter in the COUPLExx parmlib member).")
    smf30syn: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="System name (from the SYSNAME parameter in the IEASYSxx parmlib member).")
    start_interval: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                              doc="the record written datetime in 5-minute interval.")
    wkl: so.Mapped[str] = so.mapped_column(sa.String(7), doc="the workload group based on the problem program run.")
    smf30typ: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="Subtype identification Value Meaning 1 Job start or start of other work unit. 2 Activity since previous interval ended. Produced only when interval recording is active. 3 Activity for the last interval before step termination. Produced only when interval recording is active. 4 Step total 5 Job termination or termination of other work unit. 6")
    smf30jbn: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Job or session name. The job name, time, and date that the reader recognized the JOB card (for this job) constitute the job log identification.")
    smf30asi: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Address space identifier.")
    smf30jnm: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="JES job identifier. Jobs scheduled by the APPC/MVS transaction scheduler (ASCH) start with an 'A' followed by a seven-digit number.")
    smf30stn: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Step number (first step = 1, and so on).")
    gid: so.Mapped[int] = so.mapped_column(sa.BigInteger,
                                           doc="a hash number generated from the Identification Section.")
    suffix: so.Mapped[int] = so.mapped_column(sa.Integer,
                                              doc="a sequence number for the records which share the same gid.")
    prod_idx: so.Mapped[int] = so.mapped_column(sa.Integer, doc="the index of the Usage Data record in the section.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf30syp, smf30syn, start_interval, wkl, smf30typ, smf30jbn, smf30asi, smf30jnm,
                                smf30stn, gid, suffix, smf30upi, smf30upn, smf30upq, smf30upv, prod_idx),
        sa.ForeignKeyConstraint(
            ['csc', 'smf30syp', 'smf30syn', 'start_interval', 'wkl', 'smf30typ', 'smf30jbn', 'smf30asi', 'smf30jnm',
             'smf30stn', 'gid', 'suffix'],
            ['smf30_id.csc', 'smf30_id.smf30syp', 'smf30_id.smf30syn', 'smf30_id.start_interval', 'smf30_id.wkl',
             'smf30_id.smf30typ', 'smf30_id.smf30jbn', 'smf30_id.smf30asi', 'smf30_id.smf30jnm', 'smf30_id.smf30stn',
             'smf30_id.gid', 'smf30_id.suffix']),
    )

    smf30_id: so.Mapped['Smf30Id'] = so.relationship(back_populates='smf30_uds', viewonly=True)


class Smf30Uss(ReprMixin, Base30, Smf30uss):
    """The Smf30Uss class stores the Smf30Uss section in the smf30_uss table."""

    __tablename__ = "smf30_uss"
    smf30tme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                  doc="Time since midnight, in hundredths of a second, that the record was moved to the SMF buffer.")
    datetime: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf30syp: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Sysplex name (from the SYSPLEX parameter in the COUPLExx parmlib member).")
    smf30syn: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="System name (from the SYSNAME parameter in the IEASYSxx parmlib member).")
    start_interval: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                              doc="the record written datetime in 5-minute interval.")
    wkl: so.Mapped[str] = so.mapped_column(sa.String(7), doc="the workload group based on the problem program run.")
    smf30typ: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="Subtype identification Value Meaning 1 Job start or start of other work unit. 2 Activity since previous interval ended. Produced only when interval recording is active. 3 Activity for the last interval before step termination. Produced only when interval recording is active. 4 Step total 5 Job termination or termination of other work unit. 6")
    smf30jbn: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Job or session name. The job name, time, and date that the reader recognized the JOB card (for this job) constitute the job log identification.")
    smf30asi: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Address space identifier.")
    smf30jnm: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="JES job identifier. Jobs scheduled by the APPC/MVS transaction scheduler (ASCH) start with an 'A' followed by a seven-digit number.")
    smf30stn: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Step number (first step = 1, and so on).")
    gid: so.Mapped[int] = so.mapped_column(sa.BigInteger,
                                           doc="a hash number generated from the Identification Section.")
    suffix: so.Mapped[int] = so.mapped_column(sa.Integer,
                                              doc="a sequence number for the records which share the same gid.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf30syp, smf30syn, start_interval, wkl, smf30typ, smf30jbn, smf30asi, smf30jnm,
                                smf30stn, gid, suffix),
        sa.ForeignKeyConstraint(
            ['csc', 'smf30syp', 'smf30syn', 'start_interval', 'wkl', 'smf30typ', 'smf30jbn', 'smf30asi', 'smf30jnm',
             'smf30stn', 'gid', 'suffix'],
            ['smf30_id.csc', 'smf30_id.smf30syp', 'smf30_id.smf30syn', 'smf30_id.start_interval', 'smf30_id.wkl',
             'smf30_id.smf30typ', 'smf30_id.smf30jbn', 'smf30_id.smf30asi', 'smf30_id.smf30jnm', 'smf30_id.smf30stn',
             'smf30_id.gid', 'smf30_id.suffix']),
    )

    smf30_id: so.Mapped['Smf30Id'] = so.relationship(back_populates='smf30_usss', viewonly=True)


class Smf30Sap(ReprMixin, Base30, Smf30sap):
    """The Smf30Sap class stores the Smf30Sap section in the smf30_sap table."""

    __tablename__ = "smf30_sap"
    smf30sfl: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Description Storage Flags. If storage was not allocated (job step was flushed), these fields equal zero. Bit Meaning when set 0 V=R is specified. This bit has no meaning for subtype 5 records. 1 IEFUSI changed region limit values for the extended private area 2 IEFUSI set MEMLIMIT value (even if IEFUSI did not change the value). 3 If this bit is on, the following fields contain incomplete data: (SRM could not deliver deltas or values for this interval) SMF30ERS,SMF30KIE,SMF30POA,SMF30BIA,SMF30KOA,SMF30POE,SMF30BIE,SMF30KOE,SMF30PSC,SMF30BOA,SMF30LPI,SMF30PSF,SMF30BOE,SMF30NSW,SMF30PSO,SMF30CPI,SMF30PAI,SMF30PST,SMF30CPM,SMF30PEI,SMF30VPI,SMF30HPI,SMF30PIA,SMF30VPO,SMF30HPO,SMF30PIE,SMF30VPR,SMF30KIA 4 Reserved. 5 When this bit is on, the following fields are not valid: SMF30TIH SMF30TIU SMF30TIS")
    smf30spk: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4),
                                                          doc="Storage protect key, in the form xxxx 0000 , where xxxx is the key.")
    smf30prv: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Largest amount of storage used from bottom of private area, in 1 K units. This storage area includes subpools 0-127, 129- 132, 244, 251 and 252. If ADDRSPC=REAL is specified, this field equals the amount of contiguous real storage that was used.")
    smf30sys: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Largest amount of storage used from top of private area, in 1K units. This storage area includes the local system queue area (LSQA) and the SWA - subpools 229, 230, 236, 237, 249, and 253-255. If ADDRSPC=REAL is specified, this field equals the amount of storage used that was not from the contiguous real storage reserved for the program.")
    smf30rgb: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Maximum possible below-16 MB region size, in bytes.")
    smf30erg: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Maximum possible above-16 MB region size, in bytes.")
    smf30rgn: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Region size established, in 1K units, rounded up to a 4K boundary. The contents of this field is determined as follows: • If the ADDRSPC=REAL parameter is specified in the JCL, the contents of this field equals the amount of contiguous central storage reserved for the program. • If the REGION= parameter value in the JCL exceeds 16 MB: - If the IEFUSI exit changes the region limit or size above 16 MB, the contents of this field equals the changed region limit or size - Otherwise, the contents of this field equals the REGION parameter value (minimum value of 32 MB). • If the REGION= parameter value in the JCL equals or is less than 16 MB: - If the IEFUSI exit changes the region limit or size below 16 MB, the contents of this field equals the changed region limit or size - Otherwise, the contents of this field equals the REGION parameter value. Note: If both the region limit and size are changed, but do not match, the contents of this field equals the smaller of the changed region limit or size.")
    smf30dsv: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Amount of user key data space and hiperspace virtual storage (high water mark) used during the step/job (in megabytes). Must be in key 8 or higher, and the creator of the dataspace must be in problem program state. If these two conditions are not true, this field contains zeros.")
    smf30mem: so.Mapped[Optional[str]] = so.mapped_column(sa.String(18),
                                                          doc="MEMLIMIT value, in 1MB units, as determined at step initialization time, after IEFUSI and SMFLIMxx processing. Changes to the MEMLIMIT value after step initialization time are not reflected here. See Limiting the use of private memory objects in z/OS MVS Programming: Extended Addressability Guide to see how the MEMLIMIT value can change. The maximum value of this field is X'00000FFFFFFFF000', which is equivalent to MEMLIMIT having no limit.")
    smf30mes: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                          doc="Source of MEMLIMIT, which is one of the following: Value Meaning X'01' MEMLIMIT set by SMF. X'02' MEMLIMIT set explicitly in the JCL with MEMLIMIT parameter on JOB or EXEC statement. X'03' MEMLIMIT is unlimited based on REGION=0 specification. X'04' MEMLIMIT set by IEFUSI (even if IEFUSI did not change the value). X'0A' System provided a default for MEMLIMIT based on REGION=0 specification and a subsequent curtailment")
    smf30slm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="Flags that indicate the actions taken on the job step region or MEMLIMIT due to a rule defined in the SMFLIMxx member of parmlib. For subtype 5, this will be a copy of the SMF30SLM value for the last executed job step. Value Meaning X'80' SMFLIM REGIONBELOW acted on the non-extended REGION for this step. X'40' SMFLIM REGIONABOVE acted on the extended REGION for this step. X'20' SMFLIM SYSRESVBELOW acted on the non-extended REGION for this step. X'10' SMFLIM SYSRESVABOVE acted on the extended REGION for this step. X'08' SMFLIM MEMLIMIT acted on the MEMLIMIT for this step. X'04' The IEFUSI exit set the output flag that caused all SMFLIM decision making to be bypassed. X'02' SMFLIM REGIONLIMITBELOW acted on the non- extended REGION for this step. X'01' SMFLIM REGIONLIMITABOVE acted on the extended")
    smf30_raxflags: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                doc="Description Bit Meaning when set 0 (SMF30_USERKEYCOMMONAUDITENABLED) When SMF30_USERKEYCOMMONAUDITENABLED is on, auditing of successful and unsuccessful user-key common storage usage attempts enabled for this step/ job. The following fields are only applicable when this flag is on: SMF30_USERKEYCSAUSAGE")
    smf30hvh: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="High water mark for the number of usable bytes of 64-bit private storage that are obtained by this step or job. This does not include guarded virtual storage. Note: This is not the amount of 64-bit high virtual storage that is charged toward the MEMLIMIT, as it also includes IARV64 MEMLIMIT=NO storage.")
    smf30hso: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Amount of 64-bit IARV64 REQUEST=SHAREMEMOBJ shared storage, in bytes, to which this step or job has addressability or access.")
    smf30hsh: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="High water mark for the number of usable bytes of 64-bit IARV64 REQUEST=SHAREMEMOBJ shared storage to which this step or job has access. This does not include guard areas which, by definition, are not usable.")
    smf30tiu: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Current TIOT space used for TIOT entries (in bytes.) This will only contain a non-zero value for interval records, since TIOT entries are freed by unallocation processing at step end and job end.")
    smf30tis: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Size of the TIOT available for TIOT entries (in bytes). This does not include the space reserved by the system for the TIOT")
    smf30tme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                  doc="Time since midnight, in hundredths of a second, that the record was moved to the SMF buffer.")
    datetime: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    storage_vr_specified_flg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                          doc="smf30sfl (Bit 0) indicates V=R is specified. This bit has no meaning for subtype 5 records.")
    storage_iefusi_changed_flg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                            doc="smf30sfl (Bit 1) indicates IEFUSI changed region limit values for the extended private area.")
    storage_memlimit_set_flg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                          doc="smf30sfl (Bit 2) indicates IEFUSI set MEMLIMIT value (even if IEFUSI did not change the value).")
    storage_incomp_flg: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                    doc="smf30sfl (Bit 3) indicates if htis bit is on, the following fields contain incomplete data: (SRM could not deliver deltas or values for this interval) smf30ers, smf30bia, smf30bie, smf30boa, smf30boe, smf30cpi, smf30cpm, smf30hpi, smf30hpo, smf30kia, smf30kie, smf30koa, smf30koe, smf30lpi, smf30nsw, smf30pai, smf30pei, smf30pia, smf30pie, smf30poa, smf30poe, smf30psc, smf30psf, smf30pso, smf30pst, smf30vpi, smf30vpo, smf30vpr.")
    nohonor_iefusi_set: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                    doc="smf30sfl (Bit 4) indicates the NOHONORIEFUSIREGION (no honor IEFUSI region settings) was set in the Program Properties Table (PPT) when on. Region and MEMLIMIT values and limits set or affected by the IEFUSI exit are not honored when this bit is on.")
    rsvdhbb77b0_exists: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                    doc="smf30sfl (Bit 5) indicates when this bit is on the following fields are not valid: smf30tih, smf30tiu, smf30tis.")
    sl1: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                     doc="smf30slm (Bit 0) indicates SMFLIM REGIONBELOW acted on the non-extended REGION for this step.")
    sl2: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                     doc="smf30slm (Bit 1) indicates SMFLIM REGIONABOVE acted on the extended REGION for this step.")
    sl3: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                     doc="smf30slm (Bit 2) indicates SMFLIM SYSRESVBELOW acted on the non-extended REGION for this step.")
    sl4: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                     doc="smf30slm (Bit 3) indicates SMFLIM SYSRESVABOVE acted on the extended REGION for this step.")
    sl5: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                     doc="smf30slm (Bit 4) indicates SMFLIM MEMLIMIT acted on the MEMLIMIT for this step.")
    sl6: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                     doc="smf30slm (Bit 5) indicates the IEFUSI exit set the output flag that caused all SMFLIM decision-making to be bypassed.")
    sl7: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                     doc="smf30slm (Bit 6) indicates SMFLIM REGIONLIMITBELOW acted on the non-extended REGION for this step.")
    sl8: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                     doc="smf30slm (Bit 7) indicates SMFLIM REGIONLIMITABOVE acted on the extended REGION for this step.")
    smf30_userkeycommonauditenabled: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                                                 doc="smf30_raxflags (Bit 0) indicates auditing of successful and unsuccessful user-key common storage usage attempts enabled for this step/job when on. The following fields are only aplicable when this flag is on: smf30_userkeycsausage, smf30_userkeycadsusage, smf30_userkeychangkeyusage, smf30_userkeyrucsausage.")
    smf30_userkeycsausage: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                       doc="smf30_raxflags (Bit 1) indicates successful or unsuccessful attempts were made to obtain user-key CSA or RUCSA storage for this step/job when on. This bit is only valid when smf30_userkeycommonauditenabled is on. Once this bit is set within a step, it stays on for that step. THis bit will be on in job end records if it is on for any step in the job.")
    smf30_userkeycadsusage: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                        doc="smf30_raxflags (Bit 2) indicates successful or unsuccessful attempts were mad to create a user-key CADS for this step/job when on. This bit is only valid when smf30_userkeycommonauditenabled is on. Once this bit is set within a step, it stays on for that step. This bit will be on in job end records if it is on for any step in the job.")
    smf30_userkeychangkeyusage: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                            doc="smf30_raxflags (Bit 3) indicates successful or unsuccessful attempts were made to change the key of common ESQA storage to a user key (via CHANGKEY) for this step/job when on. This bit is only valid when smf30_userkeycommonauditenabled is on. Once this bit is set with a step, it stays on for that step. This bit will be in job end records if is on for any step in the job.")
    smf30_userkeyrucsausage: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                         doc="smf30_raxflags (Bit 4) indicates successful or unsuccessful attemps were made to obtain, reference, free or change the state of RUCSA storage for this step. Once this bit is set within a step, it stays on for that step. This bit will be on in job end records if it is on for any step in the job.")
    smf30_rucsaearlyusage: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                                       doc="smf30_raxflags (Bit 5) indicates attempts were made to obtain, reference, free or change the state of user key RUCSA which were permitted during early IPL or started task initialization due to DIAGxx VSM AllowEarlyRUCSA(Yes). Once this bit is set on, it remains on for the life of the address space.")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf30syp: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Sysplex name (from the SYSPLEX parameter in the COUPLExx parmlib member).")
    smf30syn: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="System name (from the SYSNAME parameter in the IEASYSxx parmlib member).")
    start_interval: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                              doc="the record written datetime in 5-minute interval.")
    wkl: so.Mapped[str] = so.mapped_column(sa.String(7), doc="the workload group based on the problem program run.")
    smf30typ: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="Subtype identification Value Meaning 1 Job start or start of other work unit. 2 Activity since previous interval ended. Produced only when interval recording is active. 3 Activity for the last interval before step termination. Produced only when interval recording is active. 4 Step total 5 Job termination or termination of other work unit. 6")
    smf30jbn: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Job or session name. The job name, time, and date that the reader recognized the JOB card (for this job) constitute the job log identification.")
    smf30asi: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Address space identifier.")
    smf30jnm: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="JES job identifier. Jobs scheduled by the APPC/MVS transaction scheduler (ASCH) start with an 'A' followed by a seven-digit number.")
    smf30stn: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Step number (first step = 1, and so on).")
    gid: so.Mapped[int] = so.mapped_column(sa.BigInteger,
                                           doc="a hash number generated from the Identification Section.")
    suffix: so.Mapped[int] = so.mapped_column(sa.Integer,
                                              doc="a sequence number for the records which share the same gid.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf30syp, smf30syn, start_interval, wkl, smf30typ, smf30jbn, smf30asi, smf30jnm,
                                smf30stn, gid, suffix),
        sa.ForeignKeyConstraint(
            ['csc', 'smf30syp', 'smf30syn', 'start_interval', 'wkl', 'smf30typ', 'smf30jbn', 'smf30asi', 'smf30jnm',
             'smf30stn', 'gid', 'suffix'],
            ['smf30_id.csc', 'smf30_id.smf30syp', 'smf30_id.smf30syn', 'smf30_id.start_interval', 'smf30_id.wkl',
             'smf30_id.smf30typ', 'smf30_id.smf30jbn', 'smf30_id.smf30asi', 'smf30_id.smf30jnm', 'smf30_id.smf30stn',
             'smf30_id.gid', 'smf30_id.suffix']),
    )

    smf30_id: so.Mapped["Smf30Id"] = so.relationship(back_populates="smf30_sap", viewonly=True)


class Smf306(ReprMixin, Base30, Smf30ura, Smf30prf, Smf30cas, Smf30sap, Smf30ops, Smf30cmp):
    """The Smf306 class stores the Smf306 section in the smf30_6 table."""

    __tablename__ = "smf30_6"
    smf30tme: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                  doc="Time since midnight, in hundredths of a second, that the record was moved to the SMF buffer.")
    datetime: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime, doc="the hour of the record.")
    smf30arb: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Maximum virtual storage, in bytes, allocated from the local system queue area (LSQA) and the SWA subpools (less than 16 MB).")
    smf30ear: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Maximum virtual storage in bytes allocated from the local system queue area (LSQA) and the SWA subpools (greater than 16 MB).")
    smf30urb: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Maximum virtual storage in bytes allocated from the user subpools (less than 16 MB).")
    smf30eur: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Maximum virtual storage in bytes allocated from the user subpools (greater than 16 MB).")
    smf30hvo: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                          doc="Amount of 64-bit private storage in bytes that is obtained by this step or job. This includes guarded virtual storage. The SMF30HVO field contains a snapshot value of high virtual private storage allocation. As the memory objects owned by the executed program have already been detached at the time the step or job goes through termination, SMF30HVO contains the memory object size still allocated to the initiator address space, but no longer reflects the memory objects that may have been allocated by the program executed in the job step. In contrast to SMF30HVO, the SMF30HVH field is maintained as a high water mark. Its content reflects the high virtual memory object size that was once allocated by the job step being executed under the initiator address space.")
    smf30rvn: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                          doc="Record version number Value Meaning '05' MVS/SP Version 5 '04' MVS/SP Version 4 '03' MVS/SP Version 3 '02' MVS/SP Version 2 '01' VS2")
    smf30pnm: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="Subsystem or product name, for example SMF.")
    smf30osl: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8),
                                                          doc="Code string for the operating system level to represent the version, release, and modification level, as described for CVTPRODN. Guaranteed to be larger in each release.")
    smf30cls: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2),
                                                          doc="Job class (blank for TSO/E session or started tasks).")
    smf30jpt: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer,
                                                          doc="JES input priority. If no value is specified for the PRTY parameter (on the JOB card), this field contains: • For JES3, the default priority specified on the JES3 STANDARDS initialization card • For JES2, a zero. Note that JES2 does not use the priority value reported in the field. (The JES2 job selection priority is requested using the JES2")
    gid: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger,
                                                     doc="a hash number generated from the Identification Section.")
    prev_start_interval: so.Mapped[Optional[dt.datetime]] = so.mapped_column(sa.DateTime,
                                                                             doc="the previous record written datetime in 5-minute interval.")
    duration: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="the duration of the job.")
    tcb_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="the calculated TCB time based on the service units.")
    srb_time: so.Mapped[Optional[float]] = so.mapped_column(sa.Float,
                                                            doc="the calculated SRB time base on the service units.")
    cpu_total: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="the total CPU time.")
    consumed_msu: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, doc="the total MSU consumed.")
    smf30stn: so.Mapped[int] = so.mapped_column(sa.Integer, doc="Step number (first step = 1, and so on).")
    csc: so.Mapped[str] = so.mapped_column(sa.String(8),
                                           doc="the identifier or serial number of Central Processor Complexes (CPC).")
    smf30syp: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Sysplex name (from the SYSPLEX parameter in the COUPLExx parmlib member).")
    smf30syn: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="System name (from the SYSNAME parameter in the IEASYSxx parmlib member).")
    start_interval: so.Mapped[dt.datetime] = so.mapped_column(sa.DateTime,
                                                              doc="the record written datetime in 5-minute interval.")
    wkl: so.Mapped[str] = so.mapped_column(sa.String(7), doc="the workload group based on the problem program run.")
    smf30typ: so.Mapped[int] = so.mapped_column(sa.Integer,
                                                doc="Subtype identification Value Meaning 1 Job start or start of other work unit. 2 Activity since previous interval ended. Produced only when interval recording is active. 3 Activity for the last interval before step termination. Produced only when interval recording is active. 4 Step total 5 Job termination or termination of other work unit. 6")
    smf30jbn: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="Job or session name. The job name, time, and date that the reader recognized the JOB card (for this job) constitute the job log identification.")
    smf30asi: so.Mapped[str] = so.mapped_column(sa.String(4), doc="Address space identifier.")
    smf30jnm: so.Mapped[str] = so.mapped_column(sa.String(8),
                                                doc="JES job identifier. Jobs scheduled by the APPC/MVS transaction scheduler (ASCH) start with an 'A' followed by a seven-digit number.")

    __table_args__ = (
        sa.PrimaryKeyConstraint(csc, smf30syp, smf30syn, start_interval, wkl, smf30typ, smf30jbn, smf30asi, smf30jnm,
                                smf30stn),
    )
