import math
from operator import itemgetter
from statistics import mean
import tabulate as tb
import pandas as pd
import numpy as np
import datetime as dt

from smf2db.api.util import round_, format_time, is_bit_set

DB_70 = 'db_70'
DB_RMF = 'db_rmf'
tb.PRESERVE_WHITESPACE = True
smf70typ_cpu_type = {0: 'CP', 1: 'IFA', 2: 'IIP'}


def format_s2min(s):
    if isinstance(s, int):
        f = '0'
    else:
        s, f = str(s).split('.')
        s = int(s)
        if len(f) > 6:
            f = f[0:6]
    minutes = s // 60
    seconds = s - (minutes * 60)
    return f"{str(int(minutes)).zfill(2)}:{int(seconds):02}.{f.ljust(6, '0'):6}"


def format_s2hr(s):
    if isinstance(s, int):
        f = '0'
    else:
        s, f = str(s).split('.')
        s = int(s)
        if len(f) > 6:
            f = f[0:6]

    hours = s // 3600
    s = s - (hours * 3600)
    minutes = s // 60
    seconds = s - (minutes * 60)
    return f"{str(int(hours)).zfill(2)}:{int(minutes):02}:{int(seconds):02}.{f.ljust(6, '0'):6}"


def convert_bi(val: int, width: int, decimal=0, comma=False, unit="") -> str:
    power_labels = {10: 'K', 20: 'M', 30: 'G', 40: 'T', 50: 'P'}
    if unit == "":
        achieved = True
    else:
        achieved = False
        if decimal == 0 and val > 0:
            decimal = 3
    new_decimal = decimal
    if len(str(f"{val:{width}{',' if comma else ''}.{new_decimal}f}")) > width or not achieved:
        if new_decimal > 0 and achieved:
            current_decimal = new_decimal
            while current_decimal > 0 and \
                    len(str(
                        f"{round_(val, current_decimal):{width}{',' if comma else ''}.{current_decimal}f}")) > width:
                current_decimal -= 1
            if len(str(f"{round_(val, current_decimal):{width}{',' if comma else ''}.{current_decimal}f}")) <= width:
                return f"{round_(val, current_decimal):{width}{',' if comma else ''}.{current_decimal}f}"
        for power, label in power_labels.items():
            new_decimal = decimal
            if label == unit:
                achieved = True
            approx_val = round_(val / 2 ** power, new_decimal)
            if (approx_val % 1 == 0) and unit != "":
                new_decimal = 0
            if len(str(f"{approx_val:{width}{',' if comma else ''}.{new_decimal}f}")) <= width and achieved:
                return f"{approx_val:{width}{',' if comma else ''}.{new_decimal}f}{label}"
            elif new_decimal > 0 and achieved:
                current_decimal = new_decimal
                while current_decimal > 0 and \
                        len(str(
                            f"{round_(approx_val, current_decimal):{width}{',' if comma else ''}.{current_decimal}f}")) > width:
                    current_decimal -= 1
                if len(str(
                        f"{round_(approx_val, current_decimal):{width}{',' if comma else ''}.{current_decimal}f}")) <= width and achieved:
                    return f"{round_(approx_val, current_decimal):{width}{',' if comma else ''}.{current_decimal}f}{label}"

    return f"{val:{width}{',' if comma else ''}.{new_decimal}f}"


def extractKBits(num, len, loc_start, loc_end=None):
    # convert number into binary first
    binary = "{0:0{l}b}".format(num, l=len)

    if loc_end is None:
        return binary[loc_start:]
    else:
        return binary[loc_start:loc_end]

def format_cpu_header(ctl, pro, report_type: str):
    if 'date' in pro.keys() and 'datetime' in pro.keys():
        report_date = pro['date']
        report_time = pro['datetime'].time().strftime('%H.%M.%S')
        interval = format_s2min(pro['smf70int'])
    elif 'date' in pro.keys():
        report_date = pro['date']
        report_time = '00.00.00'
        interval = format_s2hr(pro['smf70int'])
    else:
        report_date = pro['smf70ist'].date()
        report_time = pro['smf70ist'].time().strftime('%H.%M.%S')
        interval = format_s2min(pro['smf70int'])

    zos_ver = 'V' + pro['smf70mvs'][2:4].lstrip('0') + 'R' + pro['smf70mvs'][4:6].lstrip('0')
    interval_x = f"{interval[:-3]}"
    if ctl['smf70cai'] != 0 and ctl['smf70ccr'] == 0:
        change_reason = 'None'
    elif ctl['smf70cai'] != 0 and ctl['smf70ccr'] == 1:
        change_reason = 'Powersave'
    elif ctl['smf70cai'] != 0 and ctl['smf70ccr'] > 1:
        change_reason = 'Machine'
    else:
        change_reason = 'N/A'

    if is_bit_set(pro['smf70fla'], 16,10) and not is_bit_set(pro['smf70fla'], 16,9):
        boost_type = 'Speed'
    elif not is_bit_set(pro['smf70fla'], 16,10) and is_bit_set(pro['smf70fla'], 16,9):
        boost_type = 'zIIP'
    elif is_bit_set(pro['smf70fla'], 16,10) and is_bit_set(pro['smf70fla'], 16,9):
        boost_type = 'All'
    else:
        boost_type = 'None'
    pro_boost_class = extractKBits(pro['smf70fla'], 16, 13, 16)

    if boost_type != 'None':
        if pro_boost_class == '001':
            boost_class = 'IPL'
        elif pro_boost_class == '010':
            boost_class = 'Shutdown'
        elif pro_boost_class == '011':
            boost_class = 'Recovery'
        else:
            boost_class = 'None'
    else:
        boost_class = 'None'
    whitespace = ' '
    header1 = [["                                                          C P U  A C T I V I T Y"]]
    header2 = [
        [f"{whitespace:>12}", f"z/OS {zos_ver}", f"{whitespace:>13}", f"System ID {ctl['smf70sid']}", f"{whitespace:>6}",
         f"Date {report_date:%m/%d/%Y}", f"{whitespace:>11}", f"Interval {interval_x}"],
        ["", "", "", f"RMF Version {pro['smf70mfv']:<5}", "", f"Time {report_time}", "",
         f"Cycle {pro['smf70cyc'] / 1000:5.3f} Seconds"]
    ]
    header3 = [
        [f"CPU        {ctl['smf70mod']:>4}", "   ", f"CPC Capacity{ctl['smf70mcr']:>6}",
         f"Sequence Code {ctl['csc'].zfill(16)}"],
        [f"Model     {ctl['smf70mdl']:>4}", "", "",
         f"Hiperdispatch={'Yes' if is_bit_set(ctl['smf70hhf'], 8, 1) else 'No ' if not is_bit_set(ctl['smf70hhf'], 8, 1) and is_bit_set(ctl['smf70hhf'], 8, 0) else 'N/A'}"],
        [f"H/W Model  {ctl['smf70hwm']:>3}", "", f"Change Reason={change_reason:<9}",
         f"Boost Type={boost_type:<5}   Boost Class={boost_class:<8}"]
    ]
    if report_type == 'CPU Activity MT':
        header4 = [
            ["", "---CPU---", "  ", "---------------- Time % -----------------", "---- MT % ----", "", "Log Proc",
             "    ", "---I/O Interrupts--"]]
        return (tb.tabulate(header1, tablefmt="plain") + "\n" + tb.tabulate(header2, tablefmt="plain") + "\n" +
                tb.tabulate(header3, tablefmt="plain") + "\n" + tb.tabulate(header4, tablefmt="plain") + "\n")
    elif report_type == 'CPU Activity':
        header4 = [
            ["  ---CPU---       ---------------- Time % ----------------     Log Proc          --I/O Interrupts--"]]
        return (tb.tabulate(header1, tablefmt="plain") + "\n" + tb.tabulate(header2, tablefmt="plain") + "\n" +
                tb.tabulate(header3, tablefmt="plain") + "\n" + tb.tabulate(header4, tablefmt="plain") + "\n")
    elif report_type == 'Aid Analysis':
        header4 = [
            ["System Address Space And Work Unit Analysis", "  ", ""],
            ["---------Number of Address Spaces-----------", "",
             "-----------------------Distribution of In-Ready Work Unit Queue--------------"],
        ]
        return (tb.tabulate(header1, tablefmt="plain") + "\n" + tb.tabulate(header2, tablefmt="plain") + "\n" +
                tb.tabulate(header4, tablefmt="plain") + "\n")
    elif report_type == 'Partition Data Report':
        header1 = [["                                              P A R T I T I O N  D A T A  R E P O R T"]]
        return tb.tabulate(header1, tablefmt="plain") + "\n" + tb.tabulate(header2, tablefmt="plain") + "\n"
    elif report_type == 'Lpar Cluster Report':
        header1 = [["                                                L P A R  C L U S T E R  R E P O R T"]]
        header4 = [
            ["                                ", "<---------- Weighting\n------ Defined -----",
             "Statistics ---------->\n------- Actual -------",
             "<------ Processor\n------ Number -----", "Statistics ---->\n---- Total% ----",
             "<-- Storage\n--Central--", "Statistics >\n--Expanded--"]
        ]
        return (tb.tabulate(header1, tablefmt="plain") + "\n\n" + tb.tabulate(header2, tablefmt="plain") + "\n" +
                tb.tabulate(header4, tablefmt="plain") + "\n")
    elif report_type == 'Group Capacity Report':
        header1 = [["                                           G R O U P  C A P A C I T Y  R E P O R T"]]
        return tb.tabulate(header1, tablefmt="plain") + "\n\n" + tb.tabulate(header2, tablefmt="plain") + "\n"
    else:
        return None


def convert_si(val: int, width: int, decimal=0, comma=False, unit="") -> str:
    if val is None:
        val = 0
    power_labels = {3: 'K', 6: 'M', 9: 'G', 12: 'T', 15: 'P'}
    if unit == "":
        achieved = True
    else:
        achieved = False
        if decimal == 0 and val > 0:
            decimal = 3
    new_decimal = decimal
    if len(str(f"{val:{width}{',' if comma else ''}.{new_decimal}f}")) > width or not achieved:
        if new_decimal > 0 and achieved:
            current_decimal = new_decimal
            while current_decimal > 0 and \
                    len(str(
                        f"{round_(val, current_decimal):{width}{',' if comma else ''}.{current_decimal}f}")) > width:
                current_decimal -= 1
            if len(str(f"{round_(val, current_decimal):{width}{',' if comma else ''}.{current_decimal}f}")) <= width:
                return f"{round_(val, current_decimal):{width}{',' if comma else ''}.{current_decimal}f}"
        for power, label in power_labels.items():
            new_decimal = decimal
            if label == unit:
                achieved = True
            approx_val = round_(val / 10 ** power, new_decimal)
            if (approx_val % 1 == 0) and unit != "":
                new_decimal = 0
            if len(str(f"{approx_val:{width}{',' if comma else ''}.{new_decimal}f}")) <= width and achieved:
                return f"{approx_val:{width}{',' if comma else ''}.{new_decimal}f}{label}"
            elif new_decimal > 0 and achieved:
                current_decimal = new_decimal
                while current_decimal > 0 and \
                        len(str(
                            f"{round_(approx_val, current_decimal):{width}{',' if comma else ''}.{current_decimal}f}")) > width:
                    current_decimal -= 1
                if len(str(
                        f"{round_(approx_val, current_decimal):{width}{',' if comma else ''}.{current_decimal}f}")) <= width and achieved:
                    return f"{round_(approx_val, current_decimal):{width}{',' if comma else ''}.{current_decimal}f}{label}"

    return f"{val:{width}{',' if comma else ''}.{new_decimal}f}"


def format_cpu_activity(ctl, pro, cpus: list):
    if len(cpus) == 0:
        return None
    if ctl['multithreading'] >= 1:
        report_content = format_cpu_header(ctl, pro, 'CPU Activity MT')
    else:
        report_content = format_cpu_header(ctl, pro, 'CPU Activity')
    report_detail = {'CP': [], 'IIP': [], 'AAP': []}
    cp_mode = 1
    iip_mode = 1
    previous_core_id = None
    filler = '-----'
    for cpu in cpus:
        if cpu['cpu_is_online'] == 1:
            if ctl['multithreading'] == 1:  # multithreading
                if cpu['smf70_core_id'] != previous_core_id:
                    online = cpu['smf70ont'] / ctl['smf70int'] * 100
                    if cpu['smf70typ'] == 'CP':
                        log_proc_share = 100.0 if cpu['cpu_polarization'] == 'HIGH' else ctl['med_log_proc_share_cp'] if \
                            cpu['cpu_polarization'] == 'MED' else 0
                    elif cpu['smf70typ'] == 'IIP':
                        log_proc_share = 100.0 if cpu['cpu_polarization'] == 'HIGH' else ctl[
                            'med_log_proc_share_iip'] if cpu['cpu_polarization'] == 'MED' else 0
                    elif cpu['smf70typ'] == 'AAP':
                        log_proc_share = 100.0 if cpu['cpu_polarization'] == 'HIGH' else ctl[
                            'med_log_proc_share_aap'] if cpu['cpu_polarization'] == 'MED' else 0
                    else:
                        log_proc_share = filler
                    d_list = [f"{cpu['smf70_core_id']:^3X}", f"{cpu['smf70typ']:^4}", f"{online:>6.2f}",
                              f"{cpu['lpar_busy_percentage']:>6.2f}",
                              f"{cpu['mvs_busy_percentage'] if pd.notna(cpu['mvs_busy_percentage']) else filler:{'>6.2f' if str(cpu['mvs_busy_percentage']).replace('.', '', 1).isdigit() else '>6'}}",
                              f"{cpu['cpu_parked_percentage']:>6.2f}",
                              f"{cpu['mt_prod'] if pd.notna(cpu['mt_prod']) else filler:{'>6.2f' if pd.notna(cpu['mt_prod']) else '>6'}}",
                              f"{cpu['mt_util']:>6.2f}",
                              f"{log_proc_share:{'>6' if isinstance(log_proc_share, str) else '>6.1f'}}",
                              f"{cpu['cpu_polarization'] if pd.notna(cpu['cpu_polarization']) else ' ':<4}"]
                    if cpu['smf70typ'] == 'CP':
                        d_list = d_list + [f"{convert_si(cpu['rate_io_interrupt'], 6, 2):>7}",
                                           f"{cpu['rate_io_interrupt_by_tpi'] if pd.notna(cpu['rate_io_interrupt_by_tpi']) else 0:>6.2f}"]
                    report_detail[cpu['smf70typ']].append(d_list)
                    previous_core_id = cpu['smf70_core_id']
                else:  # other theads
                    if cpu['smf70typ'] == 'IIP':
                        iip_mode = 2
                    if pd.notna(cpu['mvs_busy_percentage']) and cpu['mvs_busy_percentage'] > 0:
                        report_detail[cpu['smf70typ']].append(["", "", "", "", f"{cpu['mvs_busy_percentage']:>6.2f}",
                                                               f"{cpu['cpu_parked_percentage']:>6.2f}", "", "", "", ""])
                    else:
                        report_detail[cpu['smf70typ']].append(
                            ["", "", "", "", f"{filler:>6}", f"{cpu['cpu_parked_percentage']:>6.2f}", "", "", "", ""])

            else:
                online = cpu['smf70ont'] / ctl['smf70int'] * 100
                if cpu['smf70typ'] == 'CP':
                    log_proc_share = 100.0 if cpu['cpu_polarization'] == 'HIGH' else ctl['med_log_proc_share_cp'] if \
                        cpu['cpu_polarization'] == 'MED' else 0 if cpu['cpu_polarization'] != 'N/A' else filler
                elif cpu['smf70typ'] == 'IIP':
                    log_proc_share = 100.0 if cpu['cpu_polarization'] == 'HIGH' else ctl['med_log_proc_share_iip'] if \
                        cpu['cpu_polarization'] == 'MED' else 0 if cpu['cpu_polarization'] != 'N/A' else filler
                elif cpu['smf70typ'] == 'AAP':
                    log_proc_share = 100.0 if cpu['cpu_polarization'] == 'HIGH' else ctl['med_log_proc_share_aap'] if \
                        cpu['cpu_polarization'] == 'MED' else 0 if cpu['cpu_polarization'] != 'N/A' else filler
                else:
                    log_proc_share = filler
                d_list = [f"{cpu['smf70cid']:^3X}", f"{cpu['smf70typ']:^4}", f"{online:>6.2f}",
                          f"{cpu['lpar_busy_percentage'] if pd.notna(cpu['lpar_busy_percentage']) else 0:>6.2f}",
                          f"{cpu['mvs_busy_percentage'] if pd.notna(cpu['mvs_busy_percentage']) else filler:{'>6.2f' if str(cpu['mvs_busy_percentage']).replace('.', '', 1).isdigit() else '>6'}}",
                          f"{cpu['cpu_parked_percentage'] if pd.notna(cpu['cpu_parked_percentage']) else 0:>6.2f}",
                          f"{log_proc_share:{'>6' if isinstance(log_proc_share, str) else '>6.1f'}}",
                          f"{cpu['cpu_polarization'] if cpu['cpu_polarization'] != 'N/A' else '   ':<4}"]
                # f"{filler:>6}",""]
                if cpu['smf70typ'] == 'CP':
                    d_list = d_list + [f"{convert_si(cpu['rate_io_interrupt'], 6, 2):>7}",
                                       f"{cpu['rate_io_interrupt_by_tpi'] if pd.notna(cpu['rate_io_interrupt_by_tpi']) else 0:>7.2f}"]
                report_detail[cpu['smf70typ']].append(d_list)
    if ctl['multithreading']:
        report_detail['CP'].append(["Total", "/Average:", "",
                                    f"{ctl['lpar_busy_total_cp'] if pd.notna(ctl['lpar_busy_total_cp']) else filler:{'>6.2f' if pd.notna(ctl['lpar_busy_total_cp']) else '>6'}}",
                                    f"{ctl['mvs_busy_total_cp'] if pd.notna(ctl['mvs_busy_total_cp']) else filler:{'>6.2f' if pd.notna(ctl['mvs_busy_total_cp']) else '>6'}}",
                                    "",
                                    f"{ctl['mt_prod_total_cp'] if pd.notna(ctl['mt_prod_total_cp']) else filler:{'>6.2f' if pd.notna(ctl['mt_prod_total_cp']) else '>6'}}",
                                    f"{ctl['mt_util_total_cp'] if pd.notna(ctl['mt_util_total_cp']) else filler:{'>6.2f' if pd.notna(ctl['mt_util_total_cp']) else '>6'}}",
                                    f"{ctl['total_log_proc_share_cp']:>6.1f}",
                                    "",
                                    f"{convert_si(ctl['rate_io_interrupt_total'], 12, 2):>8}",
                                    f"{ctl['rate_io_interrupt_by_tpi_total']:>6.2f}"])
        report_detail['CP'].append(tb.SEPARATING_LINE)

        if len(report_detail['IIP']) > 0:
            report_detail['IIP'].append(["Total", "/Average:", "",
                                         f"{ctl['lpar_busy_total_iip'] if pd.notna(ctl['lpar_busy_total_iip']) else filler:{'>6.2f' if pd.notna(ctl['lpar_busy_total_iip']) else '>6'}}",
                                         f"{ctl['mvs_busy_total_iip'] if pd.notna(ctl['mvs_busy_total_iip']) else filler:{'>6.2f' if pd.notna(ctl['mvs_busy_total_iip']) else '>6'}}",
                                         "",
                                         f"{ctl['mt_prod_total_iip'] if pd.notna(ctl['mt_prod_total_iip']) else filler:{'>6.2f' if pd.notna(ctl['mt_prod_total_iip']) else '>6'}}",
                                         f"{ctl['mt_util_total_iip'] if pd.notna(ctl['mt_util_total_iip']) else filler:{'>6.2f' if pd.notna(ctl['mt_util_total_iip']) else '>6'}}",
                                         f"{ctl['total_log_proc_share_iip']:>6.1f}",
                                         ""])
            report_detail['CP'] = report_detail['CP'] + report_detail['IIP']
        if len(report_detail['AAP']) > 0:
            report_detail['AAP'].append(["Total", "/Average:", "",
                                         f"{ctl['lpar_busy_total_aap'] if pd.notna(ctl['lpar_busy_total_aap']) else filler:{'>6.2f' if pd.notna(ctl['lpar_busy_total_aap']) else '>6'}}",
                                         f"{ctl['mvs_busy_total_aap'] if pd.notna(ctl['mvs_busy_total_aap']) else filler:{'>6.2f' if pd.notna(ctl['mvs_busy_total_aap']) else '>6'}}",
                                         "",
                                         f"{ctl['mt_prod_total_aap'] if pd.notna(ctl['mt_prod_total_aap']) else filler:{'>6.2f' if pd.notna(ctl['mt_prod_total_aap']) else '>6'}}",
                                         f"{ctl['mt_util_total_aap'] if pd.notna(ctl['mt_util_total_aap']) else filler:{'>6.2f' if pd.notna(ctl['mt_util_total_aap']) else '>6'}}",
                                         f"{ctl['total_log_proc_share_aap']:>6.1f}",
                                         ""])
            report_detail['CP'] = report_detail['CP'] + report_detail['AAP']

        mode_data = [
            ['CP', f"{cp_mode:1}", f"{ctl['smf70mcf']:>5.3f}", f"{ctl['smf70cf']:>5.3f}",
             f"{ctl['smf70atd'] / 1024:>5.3f}"],
            ['IIP', f"{iip_mode:1}", f"{ctl['smf70mcfs']:>5.3f}", f"{ctl['smf70cfs']:>5.3f}",
             f"{ctl['smf70atds'] / 1024:>5.3f}"]
        ]

        report_content += tb.tabulate(report_detail['CP'], tablefmt="plain",
                                      floatfmt=(".0f", "", ".2f", ".2f", ".2f", ".2f", ".2f", ".2f", ".1f", "", "",
                                                ".2f"),
                                      headers=["Num", "Type", "Online", "Lpar Busy", "MVS Busy", "Parked", "Prod",
                                               "Util",
                                               "Share %", " ",
                                               "Rate", "% Via TPI"])
        report_content += '\n\n -----------Multi-threading Analysis----------------\n'
        report_content += tb.tabulate(mode_data, tablefmt="plain",
                                      headers=["CPU Type", "Mode", "Max CF", "CF", "Avg TD"],
                                      colalign=('center', 'center'), floatfmt=".3f")
    else:
        report_detail['CP'].append(["Total", "/Average:", "",
                                    f"{ctl['lpar_busy_total_cp']:>6.2f}",
                                    f"{ctl['mvs_busy_total_cp'] if pd.notna(ctl['mvs_busy_total_cp']) else filler:{'>6.2f' if pd.notna(ctl['mvs_busy_total_cp']) else '>6'}}",
                                    "", f"{filler:>6}", "",
                                    f"{ctl['rate_io_interrupt_total']:>8.2f}",
                                    f"{ctl['rate_io_interrupt_by_tpi_total']:>8.2f}"])
        if len(report_detail['IIP']) > 0:
            report_detail['IIP'].append(["Total", "/Average:", "",
                                         f"{ctl['lpar_busy_total_iip']:>6.2f}",
                                         f"{ctl['mvs_busy_total_iip'] if pd.notna(ctl['mvs_busy_total_iip']) else filler:{'>6.2f' if pd.notna(ctl['mvs_busy_total_iip']) else '>6'}}",
                                         "", f"{filler:>6}"])
            report_detail['CP'] = report_detail['CP'] + report_detail['IIP']
        if len(report_detail['AAP']) > 0:
            report_detail['AAP'].append(["Total", "/Average:", "",
                                         f"{ctl['lpar_busy_total_aap']:>6.2f}",
                                         f"{ctl['mvs_busy_total_aap'] if pd.notna(ctl['mvs_busy_total_aap']) else filler:{'>6.2f' if pd.notna(ctl['mvs_busy_total_aap']) else '>6'}}",
                                         "", f"{filler:>6}"])
            report_detail['CP'] = report_detail['CP'] + report_detail['AAP']
        report_content += tb.tabulate(report_detail['CP'], tablefmt="plain",
                                      floatfmt=(".0f", "", ".2f", ".2f", ".2f", ".2f", ".2f", ".2f", "", ".2f"),
                                      headers=["Num", "Type", "Online", "Lpar Busy", "MVS Busy", "Parked", "Share %",
                                               " ",
                                               "Rate", "% Via TPI"])
    return report_content


def format_aid_analysis(ctl: dict, pro: dict, aid: dict):
    report_content = format_cpu_header(ctl, pro, 'Aid Analysis')

    # system address space and work unit analysis
    u00 = aid['smf70u00'] / aid['smf70srm']
    u01 = aid['smf70u01'] / aid['smf70srm']
    u02 = aid['smf70u02'] / aid['smf70srm']
    u03 = aid['smf70u03'] / aid['smf70srm']
    u04 = aid['smf70u04'] / aid['smf70srm']
    u05 = aid['smf70u05'] / aid['smf70srm']
    u06 = aid['smf70u06'] / aid['smf70srm']
    u07 = aid['smf70u07'] / aid['smf70srm']
    u08 = aid['smf70u08'] / aid['smf70srm']
    u09 = aid['smf70u09'] / aid['smf70srm']
    u10 = aid['smf70u10'] / aid['smf70srm']
    u11 = aid['smf70u11'] / aid['smf70srm']
    u12 = aid['smf70u12'] / aid['smf70srm']
    u13 = aid['smf70u13'] / aid['smf70srm']
    u14 = aid['smf70u14'] / aid['smf70srm']
    u15 = aid['smf70u15'] / aid['smf70srm']
    report_data = [
        ["IN", "", f"{aid['smf70imn']:>,}", f"{aid['smf70imm']:>,}", f"{aid['smf70itt'] / pro['smf70sam']:>,.1f}"],
        ["IN READY", "", f"{aid['smf70rmn']:>,}", f"{aid['smf70rmm']:>,}", f"{aid['smf70rtt'] / pro['smf70sam']:>,.1f}",
         "<=  N", f"{u00 * 100:>6.2f}",
         f"{'>' * int(u00 * 51)}"],
        ["", "", "", "", "", " =  N +  1", f"{u01 * 100:>6.2f}", f"{'>' * int(u01 * 51)}"],
        ["OUT READY", "", f"{aid['smf70omn']:>,}", f"{aid['smf70omm']:>,}",
         f"{aid['smf70ott'] / pro['smf70sam']:>,.1f}", " =  N +  2",
         f"{u02 * 100:>6.2f}", f"{'>' * int(u02 * 51)}"],
        ["OUT WAIT", "", f"{aid['smf70wmn']:>,}", f"{aid['smf70wmm']:>,}", f"{aid['smf70wtt'] / pro['smf70sam']:>,.1f}",
         " =  N +  3",
         f"{u03 * 100:>6.2f}", f"{'>' * int(u03 * 51)}"],
        ["", "", "", "", "", "<=  N +  5", f"{u04 * 100:>6.2f}", f"{'>' * int(u04 * 51)}"],
        ["LOGICAL OUT RDY", "", f"{aid['smf70lmn']:>,}", f"{aid['smf70lmm']:>,}",
         f"{aid['smf70ltt'] / pro['smf70sam']:>,.1f}", "<=  N + 10",
         f"{u05 * 100:>6.2f}", f"{'>' * int(u05 * 51)}"],
        ["LOGICAL OUT WAIT", "", f"{aid['smf70amn']:>,}", f"{aid['smf70amm']:>,}",
         f"{aid['smf70att'] / pro['smf70sam']:>,.1f}", "<=  N + 15",
         f"{u06 * 100:>6.2f}", f"{'>' * int(u06 * 51)}"],
        ["", "", "", "", "", "<=  N + 20", f"{u07 * 100:>6.2f}", f"{'>' * int(u07 * 51)}"],
        ["Address Space Types", "", "", "", "", "<=  N + 30", f"{u08 * 100:>6.2f}", f"{'>' * int(u08 * 51)}"],
        ["", "", "", "", "", "<=  N + 40", f"{u09 * 100:>6.2f}", f"{'>' * int(u09 * 51)}"],
        ["BATCH", "", f"{aid['smf70bmn']:>,}", f"{aid['smf70bmm']:>,}", f"{aid['smf70btt'] / pro['smf70sam']:>,.1f}",
         "<=  N + 60",
         f"{u10 * 100:>6.2f}", f"{'>' * int(u10 * 51)}"],
        ["STC", "", f"{aid['smf70smn']:>,}", f"{aid['smf70smm']:>,}", f"{aid['smf70stt'] / pro['smf70sam']:>,.1f}",
         "<=  N + 80", f"{u11 * 100:>6.2f}",
         f"{'>' * int(u11 * 51)}"],
        ["TSO", "", f"{aid['smf70tmn']:>,}", f"{aid['smf70tmm']:>,}", f"{aid['smf70ttt'] / pro['smf70sam']:>,.1f}",
         "<=  N + 100", f"{u12 * 100:>6.2f}",
         f"{'>' * int(u12 * 51)}"],
        ["ASCH", "", f"{aid['smf70pmn']:>,}", f"{aid['smf70pmm']:>,}", f"{aid['smf70ptt'] / pro['smf70sam']:>,.1f}",
         "<=  N + 120",
         f"{u13 * 100:>6.2f}", f"{'>' * int(u13 * 51)}"],
        ["OMVS", "", f"{aid['smf70xmn']:>,}", f"{aid['smf70xmm']:>,}", f"{aid['smf70xtt'] / pro['smf70sam']:>,.1f}",
         "<=  N + 150",
         f"{u14 * 100:>6.2f}", f"{'>' * int(u14 * 51)}"],
        ["", "", "", "", "", ">   N + 150", f"{u15 * 100:>6.2f}", f"{'>' * int(u15 * 51)}"]
    ]

    report_data2 = [
        ["CP", f"{aid['smf70cmn']:>,}", "", f"{aid['smf70cmm']:>,}", "", f"{aid['smf70ctt'] / aid['smf70srm']:>,.1f}",
         ""],
        ["IIP", f"{aid['smf70emn']:>,}", "", f"{aid['smf70emm']:>,}", "", f"{aid['smf70ett'] / aid['smf70srm']:>,.1f}",
         ""]
    ]
    if aid['smf70dtt'] > 0:
        report_data2.append(
            ["AAP", f"{aid['smf70dmn']:>,}", "", f"{aid['smf70dmm']:>,}", "",
             f"{aid['smf70dtt'] / aid['smf70srm']:>,.1f}", ""])

    report_content += tb.tabulate(report_data, tablefmt="plain", colalign=("left", "left", "right", "right", "right",),
                                  headers=["Queue Types", " ", "Min", "Max", "Avg", "Number of\nWork Units", "(%)",
                                           "0    10   20   30   40   50   60   70   80   90   100\n!....!....!....!....!....!....!....!....!....!....!  "])
    report_content += "\n\n---------Number of Work Units-------------\n"
    report_content += tb.tabulate(report_data2, tablefmt="plain", floatfmt=("", ".0f", "", ".0f", "", ".1f",),
                                  headers=["CPU Types", "Min", "", "Max", "", "Avg",
                                           f"N = Number of processors online unparked ({ctl['numproc']:4.1f} on avg)"])
    report_content += "\n\nBlocked Workload Analysis\n"
    report_content += tb.tabulate([
        ["OPT Parameters: BLWLTRPCT (%)", f"{ctl['smf70pmt'] * 100.0:#.1f}", "Promote Rate:  Defined",
         f"{ctl['smf70pmi'] / pro['smf70sam']:.0f}",
         "Waiters for Promote:  Avg", f"{ctl['smf70pmw'] / pro['smf70sam']:#.3f}"],
        ["BLWLINTHD", f"{ctl['smf70pml']}", "Used (%)",
         f"{100 * ctl['smf70pmu'] / ((ctl['smf70pmi'] / pro['smf70sam']) * ctl['smf70int']):#.1f}",
         "Peak", f"{ctl['smf70pmp']}"]
    ], tablefmt="plain",  # floatfmt=("",".1f","",".1f","",".3f"),
        colalign=("right", "right", "right", "right", "right", "right"))
    return report_content


def format_partition_report(ctl: dict, pro: dict, bcts: list):
    if len(bcts) == 0:
        return None
    report_content = format_cpu_header(ctl, pro, 'Partition Data Report')
    report_part = {'CP': [], 'IFL': [], 'IIP': [], 'ICF': [], 'AAP': [], 'Deactivated': []}
    filler = '-----'
    header_data = []
    for bct in bcts:
        if bct['smf70bdn'] == 0:
            lpar_status = 'D'
            report_part['Deactivated'].append(
                [f"{bct['smf70lpm']}", f"{lpar_status:1}"])
            continue

        for cpu in bct['bct_cpus']:
            if cpu['smf70cix'] == 'CP':
                if ctl['smf70ptn'] == bct['lpar_number']:  # identify the requested bct
                    cpu_key = []
                    cpu_count = []
                    if pd.notna(ctl['cpu_count_IFL']) and ctl['cpu_count_IFL'] > 0:
                        cpu_key.append('IFL')
                        cpu_count.append(ctl['cpu_count_IFL'])
                    if pd.notna(ctl['cpu_count_ICF']) and ctl['cpu_count_ICF'] > 0:
                        cpu_key.append('ICF')
                        cpu_count.append(ctl['cpu_count_ICF'])
                    if pd.notna(ctl['cpu_count_IIP']) and ctl['cpu_count_IIP'] > 0:
                        cpu_key.append('IIP')
                        cpu_count.append(ctl['cpu_count_IIP'])
                    if pd.notna(ctl['cpu_count_CBP']) and ctl['cpu_count_CBP'] > 0:
                        cpu_key.append('CBP')
                        cpu_count.append(ctl['cpu_count_CBP'])
                    if pd.notna(ctl['cpu_count_IFA']) and ctl['cpu_count_IFA'] > 0:
                        cpu_key.append('AAP')
                        cpu_count.append(ctl['cpu_count_IFA'])

                    header_data = [
                        ["MVS Partition Name", f"{ctl['smf70lpm']}", " ", "Phys Proc Num", f"{ctl['smf70bnp']}",
                         "     ",
                         "Group Name", f"{bct['smf70gnm'] if bct['smf70gnm'] != '' else 'DEFAULT'}",
                         "     ",
                         "Initial Cap", f"{'YES' if cpu['initial_cap_indicator'] == 'Y' else 'NO'}"],
                        ["Image Capacity", f"{ctl['smf70wla']}", " ", "CP", f"{ctl['cpu_count_CP']}", "     ",
                         "Limit",
                         f"{bct['smf70gmu'] if bct['smf70gnm'] != '' else 0:>3}{'*' if is_bit_set(bct['smf70pfg'],8, 6) else ' ':1}",
                         "     ",
                         "Lpar HW Cap", f"{'YES' if cpu['cap_absolute_indicator'] == 'Y' else 'NO'}"]
                    ]
                    if len(cpu_key) > 0 and cpu_count[0] > 0:
                        header_data.append(
                            ["Number of Configured Partitions", f"{len(bcts) - 1}", " ",
                             f"{cpu_key[0]:3}", f"{cpu_count[0]:>5}", " ",
                             "Available", f"{ctl['smf70gau'] if bct['smf70gnm'] != '' else 0:>3}", " ",
                             "HW Group Cap", f"{'YES' if cpu['cap_absolute_group_indicator'] == 'Y' else 'NO'}"])
                    else:
                        header_data.append(
                            ["Number of Configured Partitions", f"{len(bcts) - 1}", " ",
                             "", "", "",
                             "Available", f"{ctl['smf70gau'] if bct['smf70gnm'] != '' else 0:>3}", " ",
                             "HW Group Cap", f"{'YES' if cpu['cap_absolute_group_indicator'] == 'Y' else 'NO'}"])
                    if len(cpu_key) > 1:
                        header_data.append(
                            ["Wait Completion", f"{cpu['wait_completion_status']}", " ",
                             f"{cpu_key[1]:3}", f"{cpu_count[1]:>5}", " ",
                             "", "", "",
                             "ABS MSU Cap", f"{'YES' if is_bit_set(ctl['smf70hhf'], 8, 4) else 'NO'}"])
                    else:
                        header_data.append(
                            ["Wait Completion", f"{cpu['wait_completion_status']}", " ",
                             "", "", " ",
                             "", "", "",
                             "ABS MSU Cap", f"{'YES' if is_bit_set(ctl['smf70hhf'], 8, 4) else 'NO'}"])
                    if len(cpu_key) > 2:
                        header_data.append(
                            ["Dispatch Interval",
                             f"{'Dynamic' if ctl['smf70gts'] == 0 else ctl['smf70gts']}", " ",
                             f"{cpu_key[2]:3}", f"{cpu_count[2]:>5}"])
                    else:
                        header_data.append(
                            ["Dispatch Interval",
                             f"{'Dynamic' if ctl['smf70gts'] == 0 else ctl['smf70gts']}"])
                    if len(cpu_key) > 3:
                        header_data.append(
                            ["", "", "", f"{cpu_key[3]:3}", f"{cpu_count[3]:>5}"])
                    if len(cpu_key) > 4:
                        header_data.append(
                            ["", "", "", f"{cpu_key[4]:3}", f"{cpu_count[4]:>5}"])
                    if len(cpu_key) > 5:
                        header_data.append(
                            ["", "", "", f"{cpu_key[5]:3}", f"{cpu_count[5]:>5}"])
                if 'PHYSICAL' not in bct['smf70lpm']:  # if smf70lpm != '*PHYSICAL*':
                    report_part['CP'].append(
                        [f"{bct['smf70lpm']}", f"{'D' if bct['smf70bdn'] == 0 else 'A':1}",
                         f"{'S' if not pd.isna(bct['smf70_boostinfo']) and is_bit_set(bct['smf70_boostinfo'],8,1) else 'N'}", f"{cpu['wgt']}",
                         f"{bct['smf70msu']}", f"{cpu['effective_consumed_msu']:.0f}",
                         f"{cpu['initial_cap_indicator']:1} {cpu['cap_absolute_indicator']:1} {cpu['cap_absolute_group_indicator']:1}",
                         f"{cpu['smf70nsw']:.1f}", f"{cpu['cpu_count']}", f"{cpu['smf70cix']}",
                         f"{(pd.to_datetime(0) + dt.timedelta(seconds=cpu['smf70edt'])).strftime('%H.%M.%S.%f')[:-3]}",
                         f"{(pd.to_datetime(0) + dt.timedelta(seconds=cpu['smf70pdt'])).strftime('%H.%M.%S.%f')[:-3]}",
                         f"{cpu['logical_processor_effective']:.2f}", f"{cpu['logical_processor_total']:.2f}",
                         f"{cpu['lpar_management_per_cpu'] if pd.notna(cpu['lpar_management_per_cpu']) else filler:{'.2f' if pd.notna(cpu['lpar_management_per_cpu']) else '>5'}}",
                         f"{cpu['physical_processor_effective'] if pd.notna(cpu['physical_processor_effective']) else filler:{'.2f' if pd.notna(cpu['physical_processor_effective']) else '>5'}}",
                         f"{cpu['physical_processor_total'] if pd.notna(cpu['physical_processor_total']) else filler:{'.2f' if pd.notna(cpu['physical_processor_total']) else '>5'}}"
                         ])
                else:
                    report_part['CP'].append(
                        ["*PHYSICAL*", "", "", "", "", "", "", "", "", "", "",
                         f"{(pd.to_datetime(0) + dt.timedelta(seconds=cpu['smf70pdt'])).strftime('%H.%M.%S.%f')[:-3]}",
                         "", "",
                         f"{cpu['lpar_management_per_cpu'] if pd.notna(cpu['lpar_management_per_cpu']) else filler:{'.2f' if pd.notna(cpu['lpar_management_per_cpu']) else '>5'}}",
                         "",
                         f"{cpu['physical_processor_total'] if pd.notna(cpu['physical_processor_total']) else filler:{'.2f' if pd.notna(cpu['physical_processor_total']) else '>5'}}"
                         ])
            elif pd.notna(cpu['cpu_count']) and cpu['cpu_count'] > 0:
                if 'PHYSICAL' not in bct['smf70lpm']:  # if smf70lpm != '*PHYSICAL*':
                    report_part[cpu['smf70cix']].append(
                        [f"{bct['smf70lpm']}", f"{'D' if bct['smf70bdn'] == 0 else 'A':1}",
                         f"{'I' if cpu['smf70cix'] == 'IIP' and not pd.isna(bct['smf70_boostinfo']) and is_bit_set(bct['smf70_boostinfo'],8,0) else 'N' if cpu['smf70cix'] == 'IIP' else ' '}",
                         f"{cpu['wgt']}", "", "",
                         f"{cpu['initial_cap_indicator'] if cpu['wgt'] != 'DED' else ' ':1} {cpu['cap_absolute_indicator'] if cpu['wgt'] != 'DED' else ' ':1} {cpu['cap_absolute_group_indicator'] if cpu['wgt'] != 'DED' else ' ':1}",
                         "", f"{cpu['cpu_count']}", f"{cpu['smf70cix']}",
                         f"{(pd.to_datetime(0) + dt.timedelta(seconds=cpu['smf70edt'])).strftime('%H.%M.%S.%f')[:-3]}",
                         f"{(pd.to_datetime(0) + dt.timedelta(seconds=cpu['smf70pdt'])).strftime('%H.%M.%S.%f')[:-3]}",
                         f"{cpu['logical_processor_effective'] if pd.notna(cpu['logical_processor_effective']) else filler:{'.2f' if pd.notna(cpu['logical_processor_effective']) else '>6'}}",
                         f"{cpu['logical_processor_total'] if pd.notna(cpu['logical_processor_total']) else filler:{'.2f' if pd.notna(cpu['logical_processor_total']) else '>6'}}",
                         f"{cpu['lpar_management_per_cpu'] if pd.notna(cpu['lpar_management_per_cpu']) else filler:{'.2f' if pd.notna(cpu['lpar_management_per_cpu']) else '>5'}}",
                         f"{cpu['physical_processor_effective'] if pd.notna(cpu['physical_processor_effective']) else filler:{'.2f' if pd.notna(cpu['physical_processor_effective']) else '>5'}}",
                         f"{cpu['physical_processor_total'] if pd.notna(cpu['physical_processor_total']) else filler:{'.2f' if pd.notna(cpu['physical_processor_total']) else '>5'}}"
                         ])
                else:
                    report_part[cpu['smf70cix']].append(
                        ["*PHYSICAL*", "", "", "", "", "", "", "", "", "", "",
                         f"{(pd.to_datetime(0) + dt.timedelta(seconds=cpu['smf70pdt'])).strftime('%H.%M.%S.%f')[:-3]}",
                         "", "",
                         f"{cpu['lpar_management_per_cpu'] if pd.notna(cpu['lpar_management_per_cpu']) else filler:{'.2f' if pd.notna(cpu['lpar_management_per_cpu']) else '>5'}}",
                         "",
                         f"{cpu['physical_processor_total'] if pd.notna(cpu['physical_processor_total']) else filler:{'.2f' if pd.notna(cpu['physical_processor_total']) else '>5'}}"
                         ])
    separating_line = ["", "", "", "------", "", "", "", "", "", "", "------------", "------------", "", "", "-----",
                       "------", "-----"]
    # for cpu_type in ['CP', 'ICF', 'IFL', 'IIP', 'AAP']:
    if len(report_part['CP']) > 0:
        report_part['CP'].append(separating_line)
        report_part['CP'].append(
            # f"             ------                                        ------------  ------------                        -----     ------  -----\n"\
            ["Total", "", "",
             f"{int(float(ctl['total_weight_cp'])) if isinstance(ctl['total_weight_cp'], str) and ctl['total_weight_cp'].replace('.', '', 1).isdigit() else ctl['total_weight_cp']}",
             "", "", "", "", "", "",
             f"{(pd.to_datetime(0) + dt.timedelta(seconds=ctl['smf70edt_total_cp'])).strftime('%H.%M.%S.%f')[:-3]}",
             f"{(pd.to_datetime(0) + dt.timedelta(seconds=ctl['smf70pdt_cp'])).strftime('%H.%M.%S.%f')[:-3]}",
             "", "",
             f"{ctl['lpar_management_total_cp']:.2f}", f"{ctl['physical_processor_effective_total_cp']:.2f}",
             f"{ctl['physical_processor_total_total_cp']:.2f}"])
        report_part['CP'].append(tb.SEPARATING_LINE)
    if len(report_part['IIP']) > 0:
        report_part['IIP'].append(separating_line)
        report_part['IIP'].append(
            # f"             ------                                        ------------  ------------                        -----     ------  -----\n"\
            ["Total", "", "",
             f"{int(float(ctl['total_weight_iip'])) if isinstance(ctl['total_weight_iip'], str) and ctl['total_weight_iip'].replace('.', '', 1).isdigit() else ctl['total_weight_iip']}",
             "", "", "", "", "", "",
             f"{(pd.to_datetime(0) + dt.timedelta(seconds=ctl['smf70edt_total_iip'])).strftime('%H.%M.%S.%f')[:-3]}",
             f"{(pd.to_datetime(0) + dt.timedelta(seconds=ctl['smf70pdt_iip'])).strftime('%H.%M.%S.%f')[:-3]}",
             "", "",
             f"{ctl['lpar_management_total_iip']:.2f}", f"{ctl['physical_processor_effective_total_iip']:.2f}",
             f"{ctl['physical_processor_total_total_iip']:.2f}"])
        report_part['IIP'].append(tb.SEPARATING_LINE)
    if len(report_part['ICF']) > 0:
        report_part['ICF'].append(separating_line)
        report_part['ICF'].append(
            # f"             ------                                        ------------  ------------                        -----     ------  -----\n"\
            ["Total", "", "",
             f"{int(float(ctl['total_weight_icf'])) if isinstance(ctl['total_weight_icf'], str) and ctl['total_weight_icf'].replace('.', '', 1).isdigit() else ctl['total_weight_icf']}",
             "", "", "", "", "", "",
             f"{(pd.to_datetime(0) + dt.timedelta(seconds=ctl['smf70edt_total_icf'])).strftime('%H.%M.%S.%f')[:-3]}",
             f"{(pd.to_datetime(0) + dt.timedelta(seconds=ctl['smf70pdt_icf'])).strftime('%H.%M.%S.%f')[:-3]}",
             "", "",
             f"{ctl['lpar_management_total_icf']:.2f}", f"{ctl['physical_processor_effective_total_icf']:.2f}",
             f"{ctl['physical_processor_total_total_icf']:.2f}"])
        report_part['ICF'].append(tb.SEPARATING_LINE)
    if len(report_part['IFL']) > 0:
        report_part['IFL'].append(separating_line)
        report_part['IFL'].append(
            # f"             ------                                        ------------  ------------                        -----     ------  -----\n"\
            ["Total", "", "",
             f"{int(float(ctl['total_weight_ifl'])) if isinstance(ctl['total_weight_ifl'], str) and ctl['total_weight_ifl'].replace('.', '', 1).isdigit() else ctl['total_weight_ifl']}",
             "", "", "", "", "", "",
             f"{(pd.to_datetime(0) + dt.timedelta(seconds=ctl['smf70edt_total_ifl'])).strftime('%H.%M.%S.%f')[:-3]}",
             f"{(pd.to_datetime(0) + dt.timedelta(seconds=ctl['smf70pdt_ifl'])).strftime('%H.%M.%S.%f')[:-3]}",
             "", "",
             f"{ctl['lpar_management_total_ifl']:.2f}", f"{ctl['physical_processor_effective_total_ifl']:.2f}",
             f"{ctl['physical_processor_total_total_ifl']:.2f}"])
        report_part['IFL'].append(tb.SEPARATING_LINE)
    if len(report_part['AAP']) > 0:
        report_part['AAP'].append(separating_line)
        report_part['AAP'].append(
            # f"             ------                                        ------------  ------------                        -----     ------  -----\n"\
            ["Total", "", "",
             f"{int(float(ctl['total_weight_aap'])) if isinstance(ctl['total_weight_aap'], str) and ctl['total_weight_aap'].replace('.', '', 1).isdigit() else ctl['total_weight_aap']}",
             "", "", "", "", "", "",
             f"{(pd.to_datetime(0) + dt.timedelta(seconds=ctl['smf70edt_total_aap'])).strftime('%H.%M.%S.%f')[:-3]}",
             f"{(pd.to_datetime(0) + dt.timedelta(seconds=ctl['smf70pdt_aap'])).strftime('%H.%M.%S.%f')[:-3]}",
             "", "",
             f"{ctl['lpar_management_total_aap']:.2f}", f"{ctl['physical_processor_effective_total_aap']:.2f}",
             f"{ctl['physical_processor_total_total_aap']:.2f}"])
        report_part['AAP'].append(tb.SEPARATING_LINE)
    subheader = [
        ["--------------------- Partition Data ---------------------", "---- Logical Partition Processor Data ---",
         "------ Average Processor Utilization Percentages ------"],
        ["                               ----MSU----    --Capping---", "--Processor--  ----Dispatch Time Data----",
         "  Logical Processors  ------ Physical Processors ------"]
    ]
    report_content += tb.tabulate(header_data, tablefmt='plain',
                                  colalign=("left", "right", "", "right", "right",))
    report_content += '\n'
    report_content += tb.tabulate(subheader, tablefmt='plain')
    report_content += '\n'
    if len(report_part['IFL']) > 0:
        report_part['CP'] = report_part['CP'] + report_part['IFL']
    if len(report_part['ICF']) > 0:
        report_part['CP'] = report_part['CP'] + report_part['ICF']
    if len(report_part['IIP']) > 0:
        report_part['CP'] = report_part['CP'] + report_part['IIP']
    if len(report_part['AAP']) > 0:
        report_part['CP'] = report_part['CP'] + report_part['AAP']
    if len(report_part['Deactivated']) > 0:
        report_part['CP'] = report_part['CP'] + report_part['Deactivated']
    report_content += tb.tabulate(report_part['CP'], tablefmt='plain',  # tablefmt="simple",
                                  colalign=(
                                      "left", "center", "center", "right", "right", "right", "center", "right", "right",
                                      "center",
                                      "center", "center",
                                      "right", "right", "right", "right", "right",),
                                  headers=["Name", "S", "BT", "Wgt", "Def", "Act", "Def", "WLM%", "Num", "Type",
                                           "Effective",
                                           "Total",
                                           "Effective", "Total", "Lpar Mgmt", "Effective", "Total"])

    return report_content


def format_lpar_cluster_report(ctl: dict, pro, bcts: list):
    if len(bcts) == 0:
        return ''

    report_content = format_cpu_header(ctl, pro, 'Lpar Cluster Report')
    cluster_dict = {}
    for bct in bcts:
        if len(bct['bct_cpus']) > 0:
            if bct['smf70spn'] not in cluster_dict.keys():
                cluster_dict[bct['smf70spn']] = []

            total_processor_online_time = sum([bct_cpu['smf70ont'] for bct_cpu in bct['bct_cpus']])
            total_dispatch_time_total = sum([bct_cpu['smf70pdt'] for bct_cpu in bct['bct_cpus']])

            cluster_dict[bct['smf70spn']].append([bct['smf70lpm'], bct['system_name'], bct['bct_cpus'][0]['smf70bps'],
                                                  bct['bct_cpus'][0]['smf70mis'], bct['bct_cpus'][0]['smf70mas'],
                                                  f"{bct['bct_cpus'][0]['smf70acs'] / ctl['smf70dsa']:>.0f}",
                                                  f"{bct['bct_cpus'][0]['smf70nsi'] / ctl['smf70dsa'] * 100:>.1f}",
                                                  f"{bct['bct_cpus'][0]['smf70nsa'] / ctl['smf70dsa'] * 100:>.1f}",
                                                  bct['defined_cpu_count_cp'],
                                                  f"{total_processor_online_time / bct['smf70int']:>.1f}",
                                                  total_dispatch_time_total / total_processor_online_time * 100,
                                                  total_dispatch_time_total / (
                                                          ctl['cpu_count_CP'] * bct['smf70int']) * 100,
                                                  bct['smf70csf'], bct['smf70esf']])
    report_detail = []
    for cluster in cluster_dict.keys():
        for idx, detail_line in enumerate(cluster_dict[cluster]):
            if idx == 0:
                detail = [cluster]
            else:
                detail = [""]
            detail += detail_line[:-1]
            detail.append(detail_line[-1] if int(detail_line[-1]) > 0 else 'N/A')
            report_detail.append(detail)
        report_detail.append(tb.SEPARATING_LINE)
        total_line = ["", "", "Total",
                      sum([int(item[2]) if pd.notna(item[2]) else 0 for item in cluster_dict[cluster]]), "", "", "",
                      "", "",
                      sum([item[8] if pd.notna(item[8]) else 0 for item in cluster_dict[cluster]]), "",
                      sum([item[10] if pd.notna(item[10]) else 0 for item in cluster_dict[cluster]]),
                      sum([item[11] if pd.notna(item[11]) else 0 for item in cluster_dict[cluster]]),
                      sum([int(item[12]) if pd.notna(item[12]) else 0 for item in cluster_dict[cluster]])]
        if sum([int(item[13]) if pd.notna(item[13]) else 0 for item in cluster_dict[cluster]]) > 0:
            total_line.append(sum([int(item[13]) if pd.notna(item[13]) else 0 for item in cluster_dict[cluster]]))
        else:
            total_line.append('N/A')
        report_detail.append(total_line)
        report_detail.append([" "])
    return report_content + '\n' + tb.tabulate(report_detail,
                                               headers=['Cluster', 'Partition', 'System', 'Init', 'Min', 'Max', 'Avg',
                                                        'Min %', 'Max %',
                                                        'Defined', 'Actual', 'LBusy', 'PBusy', '         ',
                                                        '          '],
                                               colalign=('left', 'left', 'left', 'right', 'right', 'right', 'right',
                                                         'right', 'right'
                                                             , 'right', 'right', 'right', 'right', 'right', 'right'),
                                               floatfmt=('', '', '', '', '', '', '', '', '', '.1f', '.1f', '.2f', '.2f')
                                               # ,  '.0f',  '.0f',  '.0f',  '.0f',  '.1f',
                                               #          '.0f', '.1f',)
                                               ) + '\n'


def format_group_capacity_report(ctl, pro, bcts):
    if len(bcts) == 0:
        return ''
    report_content = format_cpu_header(ctl, pro, 'Group Capacity Report')
    group_dict = {}
    for bct in bcts:
        if len(bct['bct_cpus']) > 0:
            if bct['smf70gnm'] not in group_dict.keys():
                group_dict[(bct['smf70gnm'], bct['smf70gmu'])] = []

            group_dict[bct['smf70gnm'], bct['smf70gmu']].append([bct['smf70lpm'], bct['system_name'], bct['smf70msu'],
                                                                 bct['bct_cpus'][0]['actual_consumed_msu'],
                                                                 bct['bct_cpus'][0]['smf70bps'],
                                                                 f"{'YES' if bct['bct_cpus'][0]['initial_cap_indicator'] == 'Y' else 'NO'}",
                                                                 f"{bct['bct_cpus'][0]['smf70nsw']:>.01f}",
                                                                 f"{bct['bct_cpus'][0]['smf70nca']:>.01f}",
                                                                 bct['min_entitlement'], bct['max_entitlement']
                                                                 ])
    report_detail = []
    for group in group_dict.keys():
        for idx, detail_line in enumerate(group_dict[group]):
            if idx == 0:
                detail = [group[0], group[1]]
            else:
                detail = ["", ""]
            detail += detail_line
            report_detail.append(detail)
        report_detail.append(tb.SEPARATING_LINE)

        report_detail.append(["", "", "", "Total", "", sum([item[3] for item in group_dict[group]]),
                              sum([int(item[4]) if pd.notna(item[4]) else 0 for item in group_dict[group]])])
        report_detail.append([" "])
    return report_content + tb.tabulate(report_detail,
                                        headers=['Group-\nName', 'Capacity\nLimit', 'Partition\n', 'System\n',
                                                 '<- MSU\nDef  ', '-->\nAct', 'Wgt\n', '<---\nDef',
                                                 'Capping\nWLM%  ', '---->\nAct%', '-Entitle-\nMinimum',
                                                 'ment -\nMaximum'],
                                        colalign=(
                                            'left', 'right', 'left', 'left', 'right', 'right', 'right'
                                            , 'right', 'right', 'right', 'right', 'right'),
                                        # floatfmt=('', '', '', '', '', '', '', '', '', '.1f', '.1f', '.2f', '.2f')
                                        # ,  '.0f',  '.0f',  '.0f',  '.0f',  '.1f',
                                        #          '.0f', '.1f',)
                                        ) + '\n'


def format_crypto_header(pro):
    if 'date' in pro.keys() and 'datetime' in pro.keys():
        report_date = pro['date']
        report_time = pro['datetime'].time().strftime('%H.%M.%S')
        interval = format_s2min(pro['smf70int'])
    elif 'date' in pro.keys():
        report_date = pro['date']
        report_time = '00.00.00'
        interval = format_s2hr(pro['smf70int'])
    else:
        report_date = pro['smf70ist'].date()
        report_time = pro['smf70ist'].time().strftime('%H.%M.%S')
        interval = format_s2min(pro['smf70int'])
    zos_ver = 'V' + pro['smf70mvs'][2:4].lstrip('0') + 'R' + pro['smf70mvs'][4:6].lstrip('0')
    interval_x = f"{interval[:-3]}"
    whitespace = ' '
    header1 = [["                                       C R Y P T O     H A R D W A R E     A C T I V I T Y"]]
    header2 = [
        [f"{whitespace:>12}", f"z/OS {zos_ver}", f"{whitespace:>13}", f"System ID {pro[ 'smf70sid']}", f"{whitespace:>6}",
         f"Date {report_date:%m/%d/%Y}", f"{whitespace:>11}", f"Interval {interval_x}"],
        ["", "", "", f"RMF Version {pro['smf70mfv']:<5}", "", f"Time {report_time}", "",
         f"Cycle {pro['smf70cyc'] / 1000:5.3f} Seconds"]
    ]
    return tb.tabulate(header1, tablefmt="plain") + "\n" + tb.tabulate(header2, tablefmt="plain") + "\n"


def format_ccf_detail(pro, ccf):
    if ccf is None:
        return None

    report_content = (
        "-------- ICSF Services -----------------------------------------------------------------------------------------------------------\n"
        "      ----- Encryption ----  ----- Decryption ----  ----------- Hash ------------  ------- Pin ---------\n")
    report_content += tb.tabulate([
        ["Rate", f"{ccf['r702snec'] / pro['smf70int']:>9.2f}", f"{ccf['r702tnec'] / pro['smf70int']:>9.2f}",
         f"{ccf['r702aesc'] / pro['smf70int']:>9.2f}",
         f"{ccf['r702sndc'] / pro['smf70int']:>9.2f}", f"{ccf['r702tndc'] / pro['smf70int']:>9.2f}",
         f"{ccf['r702asdc'] / pro['smf70int']:>9.2f}",
         f"{ccf['r702nhac'] / pro['smf70int']:>9.2f}", f"{ccf['r702nh2c'] / pro['smf70int']:>9.2f}",
         f"{ccf['r702nh5c'] / pro['smf70int']:>9.2f}",
         f"{ccf['r702nptc'] / pro['smf70int']:>9.2f}", f"{ccf['r702npvc'] / pro['smf70int']:>9.2f}"],
        ["Size", f"{ccf['r702sneb'] / ccf['r702snec'] if ccf['r702snec'] > 0 else 0:>9.2f}",
         f"{ccf['r702tneb'] / ccf['r702tnec'] if ccf['r702tnec'] > 0 else 0:>9.2f}",
         f"{ccf['r702aesb'] / ccf['r702aesc'] if ccf['r702aesc'] > 0 else 0:>9.2f}",
         f"{ccf['r702sndb'] / ccf['r702sndc'] if ccf['r702sndc'] > 0 else 0:>9.2f}",
         f"{ccf['r702tndb'] / ccf['r702tndc'] if ccf['r702tndc'] > 0 else 0:>9.2f}",
         f"{ccf['r702asdb'] / ccf['r702asdc'] if ccf['r702asdc'] > 0 else 0:>9.2f}",
         f"{ccf['r702nhab'] / ccf['r702nhac'] if ccf['r702nhac'] > 0 else 0:>9.2f}",
         f"{ccf['r702nh2b'] / ccf['r702nh2c'] if ccf['r702nh2c'] > 0 else 0:>9.2f}",
         f"{ccf['r702nh5b'] / ccf['r702nh5c'] if ccf['r702nh5c'] > 0 else 0:>9.2f}"]],
        headers=[" ", "SDES", "TDES", "AES", "SDES", "TDES", "AES", "SHA-1", "SHA-256", "SHA-512", "Translate",
                 "Verify"],
        colalign=('left', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right',
                  'right'),
        floatfmt=('', '.2f', '.2f', '.2f', '.2f', '.2f', '.2f', '.2f', '.2f', '.2f', '.2f', '.2f')
    )
    report_content += (
        "\n      -------- MAC -------  ------- AES MAC ----  ------ RSA DSig -----  ----- ECC DSig ------  -- Format Preserving Encryption --\n"
    )
    report_content += tb.tabulate([
        ["Rate", f"{ccf['r702nmgc'] / pro['smf70int']:>9.2f}", f"{ccf['r702nmvc'] / pro['smf70int']:>9.2f}",
         f"{ccf['r702amgc'] / pro['smf70int']:>9.2f}", f"{ccf['r702amvc'] / pro['smf70int']:>9.2f}",
         f"{ccf['r702drgc'] / pro['smf70int']:>9.2f}", f"{ccf['r702drvc'] / pro['smf70int']:>9.2f}",
         f"{ccf['r702degc'] / pro['smf70int']:>9.2f}", f"{ccf['r702devc'] / pro['smf70int']:>9.2f}",
         f"{ccf['r702fpec'] / pro['smf70int']:>9.2f}", f"{ccf['r702fpdc'] / pro['smf70int']:>9.2f}",
         f"{ccf['r702fptc'] / pro['smf70int']:>9.2f}"],
        ["Size", f"{ccf['r702nmgb'] / ccf['r702nmgc'] if ccf['r702nmgc'] > 0 else 0:>9.2f}",
         f"{ccf['r702nmvb'] / ccf['r702nmvc'] if ccf['r702nmvc'] > 0 else 0:>9.2f}",
         f"{ccf['r702amgb'] / ccf['r702amgc'] if ccf['r702amgc'] > 0 else 0:>9.2f}",
         f"{ccf['r702amvb'] / ccf['r702amvc'] if ccf['r702amvc'] > 0 else 0:>9.2f}", "", "", "", "",
         f"{ccf['r702fpeb'] / ccf['r702fpec'] if ccf['r702fpec'] > 0 else 0:>9.2f}",
         f"{ccf['r702fpdb'] / ccf['r702fpdc'] if ccf['r702fpdc'] > 0 else 0:>9.2f}",
         f"{ccf['r702fptb'] / ccf['r702fptc'] if ccf['r702fptc'] > 0 else 0:>9.2f}"]],
        headers=["", "Generate", "Verify", "Generate", "Verify", "Generate", "Verify", "Generate", "Verify", "Encipher",
                 "Decipher", "Translate"],
        colalign=('left', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right',
                  'right'),
        floatfmt=('', '.2f', '.2f', '.2f', '.2f', '.2f', '.2f', '.2f', '.2f', '.2f', '.2f', '.2f')
    )
    report_content += (
        "\n      ------ QSA Dsig -----  ----- Feistl-based Encryption -----\n"
    )
    report_content += tb.tabulate([
        ["Rate", f"{ccf['r702dqgc'] / pro['smf70int'] if pd.notna(ccf['r702dqgc']) else 'N/A'}",
         f"{ccf['r702dqvc'] / pro['smf70int'] if pd.notna(ccf['r702dqvc']) else 'N/A'}",
         f"{ccf['r702fxec'] / pro['smf70int'] if pd.notna(ccf['r702fxec']) else 'N/A'}",
         f"{ccf['r702fxdc'] / pro['smf70int'] if pd.notna(ccf['r702fxdc']) else 'N/A'}",
         f"{ccf['r702fxtc'] / pro['smf70int'] if pd.notna(ccf['r702fxtc']) else 'N/A'}"],
        ["Size", "", "",
         f"{ccf['r702fxeb'] / ccf['r702fxec'] if pd.notna(ccf['r702fxec']) and ccf['r702fxec'] > 0 else 0}",
         f"{ccf['r702fxdb'] / ccf['r702fxdc'] if pd.notna(ccf['r702fxdc']) and ccf['r702fxdc'] > 0 else 0}",
         f"{ccf['r702fxtb'] / ccf['r702fxtc'] if pd.notna(ccf['r702fxtc']) and ccf['r702fxtc'] > 0 else 0}"]],
        headers=["", "Generate", "Verify", "Encipher", "Decipher", "Translate"],
        colalign=('left', 'right', 'right', 'right', 'right', 'right'),
        floatfmt=('', '.2f', '.2f', '.2f', '.2f', '.2f')
    )
    return report_content


def format_cca_coprocessor_detail(typ3s):
    if len(typ3s) == 0:
        return None

    typ3s_lpar = [typ3 for typ3 in typ3s if typ3['r7023scope'] == 1]
    typ3s_cpc = [typ3 for typ3 in typ3s if typ3['r7023scope'] == 0]

    if len(typ3s_cpc) == 0:
        return None

    report_content = \
        "-------- Cryptogaphic CCA Coprocessor --------------------------------------------------\n" \
        "              ----------- Lpar ------------  ------------ CPC ------------  ---- Lpar ----  ----- CPC ----\n"
    previous_r7023ct = None
    lpar_detail1 = {}  # Exec & Util info
    lpar_detail2 = {}  # Key-gen rate
    report_detail = []
    for typ3 in typ3s_lpar:
        lpar_detail1[typ3['r7023ax']] = [f"{typ3['r7023c0'] / typ3['smf70int']:>7.2f}",
                                         f"{typ3['r7023t0'] * typ3['r7023sf'] / typ3['r7023c0'] * 1000 if typ3['r7023c0'] > 0 else 0:>9.3f}",
                                         f"{typ3['r7023t0'] * typ3['r7023sf'] * 100 / typ3['smf70int']:>7.1f}"]
        lpar_detail2[typ3['r7023ax']] = [f"{typ3['r7023c1'] / typ3['smf70int']:>7.2f}"]

    for typ3 in typ3s_cpc:
        if len(typ3s_lpar) == 0 or typ3['r7023ax'] not in lpar_detail1.keys():
            if typ3['r7023ct'] != previous_r7023ct:
                line_detail = [f"{typ3['r7023ct']:<5}", f"{typ3['r7023ax']:>3}", "", "", ""]
                previous_r7023ct = typ3['r7023ct']
            else:
                line_detail = ["", f"{typ3['r7023ax']:>3}", "", "", ""]
        else:
            if typ3['r7023ct'] != previous_r7023ct:
                line_detail = [f"{typ3['r7023ct']:<5}", f"{typ3['r7023ax']:>3}"]
                previous_r7023ct = typ3['r7023ct']
            else:
                line_detail = ["", f"{typ3['r7023ax']:>3}"]
            line_detail += lpar_detail1[typ3['r7023ax']]
        line_detail += [f"{typ3['r7023c0'] / typ3['smf70int']:>7.2f}",
                        f"{typ3['r7023t0'] * typ3['r7023sf'] / typ3['r7023c0'] * 1000 if typ3['r7023c0'] > 0 else 0:>8.3f}",
                        f"{typ3['r7023t0'] * typ3['r7023sf'] * 100 / typ3['smf70int']:>7.1f}"]
        if typ3['r7023ax'] in lpar_detail2.keys():
            line_detail += lpar_detail2[typ3['r7023ax']]
        else:
            line_detail += [""]
        line_detail += [f"{typ3['r7023c1'] / typ3['smf70int']:>7.2f}"]
        report_detail.append(line_detail)

    return report_content + tb.tabulate(report_detail,
                                        headers=["Type", "Id", "Rate", "Exec Time", "Util%", "Rate", "Exec Time",
                                                 "Util%",
                                                 "Key-Gen Rate", "Key-Gen Rate"],
                                        colalign=('left', 'right', 'right', 'right', 'right', 'right', 'right', 'right',
                                                  'right', 'right'),
                                        floatfmt=('', '', '.2f', '.3f', '.1f', '.2f', '.3f', '.1f', '.2f',
                                                  '.2f')) + '\n'


def format_pkcs11_coprocessor_detail(typ5s):
    typ5s_lpar = [typ5 for typ5 in typ5s if typ5['r7025scope'] == 1]
    typ5s_cpc = [typ5 for typ5 in typ5s if typ5['r7025scope'] == 0]

    if len(typ5s_cpc) == 0:
        return None

    report_content = (
        "-------- Cryptogaphic PKCS11 Coprocessor ------------------------------------------------------------------------------------------------------------\n"
        "              ------------ Lpar -----------  ----------- CPC -------------                 ----------- Lpar -----------  ------------ CPC -----------\n"
    )
    previous_r7025ct = None
    lpar_detail1 = {}
    lpar_asym_fast = {}
    lpar_asym_gen = {}
    lpar_asym_slow = {}
    lpar_symm_complete = {}
    lpar_symm_partial = {}
    report_detail = []
    for typ5 in typ5s_lpar:
        cryptr = (typ5['r7025sac'] + typ5['r7025fac'] + typ5['r7025spc'] + typ5['r7025scc'] + typ5['r7025agc']) / typ5[
            'smf70int']
        cryptu = (
                         typ5['r7025sat'] + typ5['r7025fat'] + typ5['r7025spt'] + typ5['r7025sct'] + typ5['r7025agt']) * \
                 typ5['r7025sf'] * 100 / typ5['smf70int']
        if cryptr > 0:
            crypte = (
                             typ5['r7025sat'] + typ5['r7025fat'] + typ5['r7025spt'] + typ5['r7025sct'] + typ5[
                         'r7025agt']) * typ5['r7025sf'] * 1000 \
                     / (typ5['r7025sac'] + typ5['r7025fac'] + typ5['r7025spc'] + typ5['r7025scc'] + typ5['r7025agc'])
        else:
            crypte = 0

        lpar_detail1[typ5['r7025ax']] = [f"{cryptr:>7.0f}", f"{crypte:>8.3f}", f"{cryptu:>7.1f}"]
        lpar_asym_fast[typ5['r7025ax']] = \
            [f"{typ5['r7025fac'] / typ5['smf70int']:>8.2f}",
             f"{typ5['r7025fat'] * typ5['r7025sf'] / typ5['r7025fac'] * 1000 if typ5['r7025fac'] > 0 else 0:>9.3f}",
             f"{typ5['r7025fat'] * typ5['r7025sf'] * 100 / typ5['smf70int']:>7.1f}"]
        lpar_asym_gen[typ5['r7025ax']] = \
            [f"{typ5['r7025agc'] / typ5['smf70int']:>8.2f}",
             f"{typ5['r7025agt'] * typ5['r7025sf'] / typ5['r7025agc'] * 1000 if typ5['r7025agc'] > 0 else 0:>9.3f}",
             f"{typ5['r7025agt'] * typ5['r7025sf'] * 100 / typ5['smf70int']:>7.1f}"]
        lpar_asym_slow[typ5['r7025ax']] = \
            [f"{typ5['r7025sac'] / typ5['smf70int']:>8.2f}",
             f"{typ5['r7025sat'] * typ5['r7025sf'] / typ5['r7025sac'] * 1000 if typ5['r7025sac'] > 0 else 0:>9.3f}",
             f"{typ5['r7025sat'] * typ5['r7025sf'] * 100 / typ5['smf70int']:>7.1f}"]
        lpar_symm_complete[typ5['r7025ax']] = \
            [f"{typ5['r7025scc'] / typ5['smf70int']:>8.2f}",
             f"{typ5['r7025sct'] * typ5['r7025sf'] / typ5['r7025scc'] * 1000 if typ5['r7025scc'] > 0 else 0:>9.3f}",
             f"{typ5['r7025sct'] * typ5['r7025sf'] * 100 / typ5['smf70int']:>7.1f}"]
        lpar_symm_partial[typ5['r7025ax']] = \
            [f"{typ5['r7025spc'] / typ5['smf70int']:>8.2f}",
             f"{typ5['r7025spt'] * typ5['r7025sf'] / typ5['r7025spc'] * 1000 if typ5['r7025spc'] > 0 else 0:>9.3f}",
             f"{typ5['r7025spt'] * typ5['r7025sf'] * 100 / typ5['smf70int']:>7.1f}"]

    for typ5 in typ5s_cpc:
        cryptr = (typ5['r7025sac'] + typ5['r7025fac'] + typ5['r7025spc'] + typ5['r7025scc'] + typ5['r7025agc']) / typ5[
            'smf70int']
        cryptu = (
                         typ5['r7025sat'] + typ5['r7025fat'] + typ5['r7025spt'] + typ5['r7025sct'] + typ5['r7025agt']) * \
                 typ5['r7025sf'] * 100 / typ5['smf70int']
        if cryptr > 0:
            crypte = (
                             typ5['r7025sat'] + typ5['r7025fat'] + typ5['r7025spt'] + typ5['r7025sct'] + typ5[
                         'r7025agt']) * typ5['r7025sf'] * 1000 \
                     / (typ5['r7025sac'] + typ5['r7025fac'] + typ5['r7025spc'] + typ5['r7025scc'] + typ5['r7025agc'])
        else:
            crypte = 0
        if len(typ5s_lpar) == 0 or typ5['r7025ax'] not in lpar_detail1.keys():
            if typ5['r7025ct'] != previous_r7025ct:
                line_detail = [f"{typ5['r7025ct']:<5}", f"{typ5['r7025ax']:>3}", "", "", "",
                               f"{cryptr:>7.0f}", f"{crypte:>8.3f}", f"{cryptu:>7.1f}",
                               "Asym Fast", "", "", "",
                               f" {typ5['r7025fac'] / typ5['smf70int']:>8.2f}",
                               f"{typ5['r7025fat'] * typ5['r7025sf'] / typ5['r7025fac'] * 1000 if typ5['r7025fac'] > 0 else 0:>9.3f}",
                               f"{typ5['r7025fat'] * typ5['r7025sf'] * 100 / typ5['smf70int']:>7.1f}"]
                previous_r7025ct = typ5['r7025ct']
            else:
                line_detail = ["", f"{typ5['r7025ax']:>3}", "", "", "",
                               f"{cryptr:>7.0f}", f"{crypte:>8.3f}", f"{cryptu:>7.1f}",
                               "Asym Fast", "", "", "",
                               f"{typ5['r7025fac'] / typ5['smf70int']:>8.2f}",
                               f"{typ5['r7025fat'] * typ5['r7025sf'] / typ5['r7025fac'] * 1000 if typ5['r7025fac'] > 0 else 0:>9.3f}",
                               f"{typ5['r7025fat'] * typ5['r7025sf'] * 100 / typ5['smf70int']:>7.1f}"]
            report_detail.append(line_detail)
            line_detail = ["", "", "", "", "", "", "", "",
                           "Asym Gen", "", "", "",
                           f"{typ5['r7025agc'] / typ5['smf70int']:>8.2f}",
                           f"{typ5['r7025agt'] * typ5['r7025sf'] / typ5['r7025agc'] * 1000 if typ5['r7025agc'] > 0 else 0:>9.3f}",
                           f"{typ5['r7025agt'] * typ5['r7025sf'] * 100 / typ5['smf70int']:>7.1f}"]
            report_detail.append(line_detail)
            line_detail = ["", "", "", "", "", "", "", "",
                           "Asym Slow", "", "", "",
                           f"{typ5['r7025sac'] / typ5['smf70int']:>8.2f}",
                           f"{typ5['r7025sat'] * typ5['r7025sf'] / typ5['r7025sac'] * 1000 if typ5['r7025sac'] > 0 else 0:>9.3f}",
                           f"{typ5['r7025sat'] * typ5['r7025sf'] * 100 / typ5['smf70int']:>7.1f}"]
            report_detail.append(line_detail)
            line_detail = ["", "", "", "", "", "", "", "",
                           "Synm Complete", "", "", "",
                           f"{typ5['r7025scc'] / typ5['smf70int']:>8.2f}",
                           f"{typ5['r7025sct'] * typ5['r7025sf'] / typ5['r7025scc'] * 1000 if typ5['r7025scc'] > 0 else 0:>9.3f}",
                           f"{typ5['r7025sct'] * typ5['r7025sf'] * 100 / typ5['smf70int']:>7.1f}"]
            report_detail.append(line_detail)
            line_detail = ["", "", "", "", "", "", "", "",
                           "Synm Partial", "", "", "",
                           f"{typ5['r7025spc'] / typ5['smf70int']:>8.2f}",
                           f"{typ5['r7025spt'] * typ5['r7025sf'] / typ5['r7025spc'] * 1000 if typ5['r7025spc'] > 0 else 0:>9.3f}",
                           f"{typ5['r7025spt'] * typ5['r7025sf'] * 100 / typ5['smf70int']:>7.1f}"]
            report_detail.append(line_detail)
        else:
            if typ5['r7025ct'] != previous_r7025ct:
                line_detail = [f"{typ5['r7025ct']:<5}", f"{typ5['r7025ax']:>3}"]
                previous_r7025ct = typ5['r7025ct']
            else:
                line_detail = ["", f"{typ5['r7025ax']:>3}"]
            line_detail += lpar_detail1[typ5['r7025ax']]
            line_detail += [f"{cryptr:>7.0f}", f"{crypte:>8.3f}", f"{cryptu:>7.1f}",
                            "Asym Fast"]
            line_detail += lpar_asym_fast[typ5['r7025ax']]
            line_detail += [f"{typ5['r7025fac'] / typ5['smf70int']:>8.2f}",
                            f"{typ5['r7025fat'] * typ5['r7025sf'] / typ5['r7025fac'] * 1000 if typ5['r7025fac'] > 0 else 0:>9.3f}",
                            f"{typ5['r7025fat'] * typ5['r7025sf'] * 100 / typ5['smf70int']:>7.1f}"]
            report_detail.append(line_detail)
            line_detail = ["", "", "", "", "", "", "", "",
                           "Asym Gen"]
            line_detail += lpar_asym_gen[typ5['r7025ax']]
            line_detail += [f"{typ5['r7025agc'] / typ5['smf70int']:>8.2f}",
                            f"{typ5['r7025agt'] * typ5['r7025sf'] / typ5['r7025agc'] * 1000 if typ5['r7025agc'] > 0 else 0:>9.3f}",
                            f"{typ5['r7025agt'] * typ5['r7025sf'] * 100 / typ5['smf70int']:>7.1f}"]
            report_detail.append(line_detail)
            line_detail = ["", "", "", "", "", "", "", "",
                           "Asym Slow"]
            line_detail += lpar_asym_slow[typ5['r7025ax']]
            line_detail += [f"{typ5['r7025sac'] / typ5['smf70int']:>8.2f}",
                            f"{typ5['r7025sat'] * typ5['r7025sf'] / typ5['r7025sac'] * 1000 if typ5['r7025sac'] > 0 else 0:>9.3f}",
                            f"{typ5['r7025sat'] * typ5['r7025sf'] * 100 / typ5['smf70int']:>7.1f}"]
            report_detail.append(line_detail)
            line_detail = ["", "", "", "", "", "", "", "",
                           "Synm Complete"]
            line_detail += lpar_symm_complete[typ5['r7025ax']]
            line_detail += [f"{typ5['r7025scc'] / typ5['smf70int']:>8.2f}",
                            f"{typ5['r7025sct'] * typ5['r7025sf'] / typ5['r7025scc'] * 1000 if typ5['r7025scc'] > 0 else 0:>9.3f}",
                            f"{typ5['r7025sct'] * typ5['r7025sf'] * 100 / typ5['smf70int']:>7.1f}"]
            report_detail.append(line_detail)
            line_detail = ["", "", "", "", "", "", "", "",
                           "Synm Partial"]
            line_detail += lpar_symm_partial[typ5['r7025ax']]
            line_detail += [f"{typ5['r7025spc'] / typ5['smf70int']:>8.2f}",
                            f"{typ5['r7025spt'] * typ5['r7025sf'] / typ5['r7025spc'] * 1000 if typ5['r7025spc'] > 0 else 0:>9.3f}",
                            f"{typ5['r7025spt'] * typ5['r7025sf'] * 100 / typ5['smf70int']:>7.1f}"]
            report_detail.append(line_detail)
    return report_content + tb.tabulate(report_detail,
                                        headers=["Type", "Id", "Rate", "Exec Time", "Util%", "Rate", "Exec Time",
                                                 "Util%",
                                                 "Function", "Rate", "Exec Time", "Util%", "Rate", "Exec Time",
                                                 "Util%"],
                                        colalign=('left', 'right', 'right', 'right', 'right', 'right', 'right', 'right',
                                                  'left', 'right', 'right', 'right', 'right', 'right', 'right'),
                                        floatfmt=('', '', '.0f', '.3f', '.1f', '.0f', '.3f', '.1f',
                                                  '', '.1f', '.3f', '.1f', '.2f', '.3f', '.1f')) + '\n'


def format_accelerator_detail(typ4s):
    typ4s_lpar = [typ4 for typ4 in typ4s if typ4['r7024scope'] == 1]
    typ4s_cpc = [typ4 for typ4 in typ4s if typ4['r7024scope'] == 0]

    if len(typ4s_cpc) == 0:
        return None

    report_content = (
        "-------- Cryptogaphic Accelerator --------------------------------------------------------------------------------------------------------------------\n"
        "              ------------ Lpar -----------  ----------- CPC -------------                 ----------- Lpar -----------  ------------ CPC ------------\n"
    )
    previous_r7024ct = None
    lpar_detail1 = {}
    lpar_me_1024 = {}
    lpar_me_2048 = {}
    lpar_me_4096 = {}
    lpar_crt_1024 = {}
    lpar_crt_2048 = {}
    lpar_crt_4096 = {}
    report_detail = []
    for typ4 in typ4s_lpar:
        sum_1met = (typ4['r7021met_1'] + typ4['r7021met_2'] + typ4['r7021met_3'] + typ4['r7021met_4'] + typ4[
            'r7021met_5'])
        sum_1mec = (typ4['r7021mec_1'] + typ4['r7021mec_2'] + typ4['r7021mec_3'] + typ4['r7021mec_4'] + typ4[
            'r7021mec_5'])
        sum_2met = (typ4['r7022met_1'] + typ4['r7022met_2'] + typ4['r7022met_3'] + typ4['r7022met_4'] + typ4[
            'r7022met_5'])
        sum_2mec = (typ4['r7022mec_1'] + typ4['r7022mec_2'] + typ4['r7022mec_3'] + typ4['r7022mec_4'] + typ4[
            'r7022mec_5'])
        sum_1crt = (typ4['r7021crt_1'] + typ4['r7021crt_2'] + typ4['r7021crt_3'] + typ4['r7021crt_4'] + typ4[
            'r7021crt_5'])
        sum_1crc = (typ4['r7021crc_1'] + typ4['r7021crc_2'] + typ4['r7021crc_3'] + typ4['r7021crc_4'] + typ4[
            'r7021crc_5'])
        sum_2crt = (typ4['r7022crt_1'] + typ4['r7022crt_2'] + typ4['r7022crt_3'] + typ4['r7022crt_4'] + typ4[
            'r7022crt_5'])
        sum_2crc = (typ4['r7022crc_1'] + typ4['r7022crc_2'] + typ4['r7022crc_3'] + typ4['r7022crc_4'] + typ4[
            'r7022crc_5'])
        cryam1r = sum_1mec / typ4['smf70int']
        cryam1u = sum_1met * typ4['r7024sf'] * 100 / (typ4['smf70int'] * typ4['r7024en'])
        if sum_1mec > 0:
            cryam1e = sum_1met * typ4['r7024sf'] * 1000 / sum_1mec
        else:
            cryam1e = 0
        cryam2r = sum_2mec / typ4['smf70int']
        cryam2u = sum_2met * typ4['r7024sf'] * 100 / (typ4['smf70int'] * typ4['r7024en'])
        if sum_2mec > 0:
            cryam2e = sum_2met * typ4['r7024sf'] * 1000 / sum_2mec
        else:
            cryam2e = 0
        cryam3r = typ4['r7023mec'] / typ4['smf70int']
        cryam3u = typ4['r7023met'] * typ4['r7024sf'] * 100 / (typ4['smf70int'] * typ4['r7024en'])
        if typ4['r7023mec'] > 0:
            cryam3e = typ4['r7023met'] * typ4['r7024sf'] * 1000 / typ4['r7023mec']
        else:
            cryam3e = 0
        cryac1r = sum_1crc / typ4['smf70int']
        cryac1u = sum_1crt * typ4['r7024sf'] * 100 / (typ4['smf70int'] * typ4['r7024en'])
        if sum_1crc > 0:
            cryac1e = sum_1crt * typ4['r7024sf'] * 1000 / sum_1crc
        else:
            cryac1e = 0
        cryac2r = sum_2crc / typ4['smf70int']
        cryac2u = sum_2crt * typ4['r7024sf'] * 100 / (typ4['smf70int'] * typ4['r7024en'])
        if sum_2crc > 0:
            cryac2e = sum_2crt * typ4['r7024sf'] * 1000 / sum_2crc
        else:
            cryac2e = 0
        cryac3r = typ4['r7023crc'] / typ4['smf70int']
        cryac3u = typ4['r7023crt'] * typ4['r7024sf'] * 100 / (typ4['smf70int'] * typ4['r7024en'])
        if typ4['r7023crc'] > 0:
            cryac3e = typ4['r7023crt'] * typ4['r7024sf'] * 1000 / typ4['r7023crc']
        else:
            cryac3e = 0

        total_count = sum_1mec + sum_2mec + typ4['r7023mec'] + sum_1crc + sum_2crc + typ4['r7023crc']
        total_utilization = (sum_1met + sum_2met + typ4['r7023met'] + sum_1crt + sum_2crt + typ4['r7023crt']) \
                            * typ4['r7024sf'] * 100 / (typ4['smf70int'] * typ4['r7024en'])
        if total_count > 0:
            total_exec_time = (sum_1met + sum_2met + typ4['r7023met'] + sum_1crt + sum_2crt + typ4['r7023crt']) \
                              * typ4['r7024sf'] * 1000 / total_count
        else:
            total_exec_time = 0
        lpar_detail1[typ4['r7024ax']] = \
            [f"{cryam1r + cryam2r + cryam3r + cryac1r + cryac2r + cryac3r:>7.0f}",
             f"{total_exec_time:>8.3f}", f"{total_utilization:>7.1f}"]
        lpar_me_1024[typ4['r7024ax']] = [f"{cryam1r:>8.2f}", f"{cryam1e:>9.3f}", f"{cryam1u:>7.1f}"]
        lpar_me_2048[typ4['r7024ax']] = [f"{cryam2r:>8.2f}", f"{cryam2e:>9.3f}", f"{cryam2u:>7.1f}"]
        lpar_me_4096[typ4['r7024ax']] = [f"{cryam3r:>8.2f}", f"{cryam3e:>9.3f}", f"{cryam3u:>7.1f}"]
        lpar_crt_1024[typ4['r7024ax']] = [f"{cryac1r:>8.2f}", f"{cryac1e:>9.3f}", f"{cryac1u:>7.1f}"]
        lpar_crt_2048[typ4['r7024ax']] = [f"{cryac2r:>8.2f}", f"{cryac2e:>9.3f}", f"{cryac2u:>7.1f}"]
        lpar_crt_4096[typ4['r7024ax']] = [f"{cryac3r:>8.2f}", f"{cryac3e:>9.3f}", f"{cryac3u:>7.1f}"]

    for typ4 in typ4s_cpc:
        sum_1met = (typ4['r7021met_1'] + typ4['r7021met_2'] + typ4['r7021met_3'] + typ4['r7021met_4'] + typ4[
            'r7021met_5'])
        sum_1mec = (typ4['r7021mec_1'] + typ4['r7021mec_2'] + typ4['r7021mec_3'] + typ4['r7021mec_4'] + typ4[
            'r7021mec_5'])
        sum_2met = (typ4['r7022met_1'] + typ4['r7022met_2'] + typ4['r7022met_3'] + typ4['r7022met_4'] + typ4[
            'r7022met_5'])
        sum_2mec = (typ4['r7022mec_1'] + typ4['r7022mec_2'] + typ4['r7022mec_3'] + typ4['r7022mec_4'] + typ4[
            'r7022mec_5'])
        sum_1crt = (typ4['r7021crt_1'] + typ4['r7021crt_2'] + typ4['r7021crt_3'] + typ4['r7021crt_4'] + typ4[
            'r7021crt_5'])
        sum_1crc = (typ4['r7021crc_1'] + typ4['r7021crc_2'] + typ4['r7021crc_3'] + typ4['r7021crc_4'] + typ4[
            'r7021crc_5'])
        sum_2crt = (typ4['r7022crt_1'] + typ4['r7022crt_2'] + typ4['r7022crt_3'] + typ4['r7022crt_4'] + typ4[
            'r7022crt_5'])
        sum_2crc = (typ4['r7022crc_1'] + typ4['r7022crc_2'] + typ4['r7022crc_3'] + typ4['r7022crc_4'] + typ4[
            'r7022crc_5'])
        cryam1r = sum_1mec / typ4['smf70int']
        cryam1u = sum_1met * typ4['r7024sf'] * 100 / (typ4['smf70int'] * typ4['r7024en'])
        if sum_1mec > 0:
            cryam1e = sum_1met * typ4['r7024sf'] * 1000 / sum_1mec
        else:
            cryam1e = 0
        cryam2r = sum_2mec / typ4['smf70int']
        cryam2u = sum_2met * typ4['r7024sf'] * 100 / (typ4['smf70int'] * typ4['r7024en'])
        if sum_2mec > 0:
            cryam2e = sum_2met * typ4['r7024sf'] * 1000 / sum_2mec
        else:
            cryam2e = 0
        cryam3r = typ4['r7023mec'] / typ4['smf70int']
        cryam3u = typ4['r7023met'] * typ4['r7024sf'] * 100 / (typ4['smf70int'] * typ4['r7024en'])
        if typ4['r7023mec'] > 0:
            cryam3e = typ4['r7023met'] * typ4['r7024sf'] * 1000 / typ4['r7023mec']
        else:
            cryam3e = 0
        cryac1r = sum_1crc / typ4['smf70int']
        cryac1u = sum_1crt * typ4['r7024sf'] * 100 / (typ4['smf70int'] * typ4['r7024en'])
        if sum_1crc > 0:
            cryac1e = sum_1crt * typ4['r7024sf'] * 1000 / sum_1crc
        else:
            cryac1e = 0
        cryac2r = sum_2crc / typ4['smf70int']
        cryac2u = sum_2crt * typ4['r7024sf'] * 100 / (typ4['smf70int'] * typ4['r7024en'])
        if sum_2crc > 0:
            cryac2e = sum_2crt * typ4['r7024sf'] * 1000 / sum_2crc
        else:
            cryac2e = 0
        cryac3r = typ4['r7023crc'] / typ4['smf70int']
        cryac3u = typ4['r7023crt'] * typ4['r7024sf'] * 100 / (typ4['smf70int'] * typ4['r7024en'])
        if typ4['r7023crc'] > 0:
            cryac3e = typ4['r7023crt'] * typ4['r7024sf'] * 1000 / typ4['r7023crc']
        else:
            cryac3e = 0
        total_count = sum_1mec + sum_2mec + typ4['r7023mec'] + sum_1crc + sum_2crc + typ4['r7023crc']
        total_utilization = (sum_1met + sum_2met + typ4['r7023met'] + sum_1crt + sum_2crt + typ4['r7023crt']) \
                            * typ4['r7024sf'] * 100 / (typ4['smf70int'] * typ4['r7024en'])
        if total_count > 0:
            total_exec_time = (sum_1met + sum_2met + typ4['r7023met'] + sum_1crt + sum_2crt + typ4['r7023crt']) \
                              * typ4['r7024sf'] * 1000 / total_count
        else:
            total_exec_time = 0
        if len(typ4s_lpar) == 0 or typ4['r7024ax'] not in lpar_detail1.keys():
            if typ4['r7024ct'] != previous_r7024ct:
                line_detail = [f"{typ4['r7024ct']:<5}", f"{typ4['r7024ax']:>3}", "", "", ""]
                previous_r7024ct = typ4['r7024ct']
            else:
                line_detail = ["", f"{typ4['r7024ax']:>3}", "", "", ""]
            line_detail += [f"{cryam1r + cryam2r + cryam3r + cryac1r + cryac2r + cryac3r:>7.0f}",
                            f"{total_exec_time:>8.3f}", f"{total_utilization:>7.1f}", "RSA ME   1024"]
            line_detail += ["", "", "", f"{cryam1r:>8.2f}", f"{cryam1e:>9.3f}", f"{cryam1u:>7.1f}"]
            report_detail.append(line_detail)
            line_detail = ["", "", "", "", "", "", "", "", "RSA ME   2048", "", "", "",
                           f"{cryam2r:>8.2f}", f"{cryam2e:>9.3f}", f"{cryam2u:>7.1f}"]
            report_detail.append(line_detail)
            line_detail = ["", "", "", "", "", "", "", "", "RSA ME   4096", "", "", "",
                           f"{cryam3r:>8.2f}", f"{cryam3e:>9.3f}", f"{cryam3u:>7.1f}"]
            report_detail.append(line_detail)
            line_detail = ["", "", "", "", "", "", "", "", "RSA CRT  1024", "", "", "",
                           f"{cryac1r:>8.2f}", f"{cryac1e:>9.3f}", f"{cryac1u:>7.1f}"]
            report_detail.append(line_detail)
            line_detail = ["", "", "", "", "", "", "", "", "RSA CRT  2048", "", "", "",
                           f"{cryac2r:>8.2f}", f"{cryac2e:>9.3f}", f"{cryac2u:>7.1f}"]
            report_detail.append(line_detail)
            line_detail = ["", "", "", "", "", "", "", "", "RSA CRT  4096", "", "", "",
                           f"{cryac3r:>8.2f}", f"{cryac3e:>9.3f}", f"{cryac3u:>7.1f}"]
            report_detail.append(line_detail)
        else:
            if typ4['r7024ct'] != previous_r7024ct:
                line_detail = [f"{typ4['r7024ct']:<5}", f"{typ4['r7024ax']:>3}"]
                previous_r7024ct = typ4['r7024ct']
            else:
                line_detail = ["", f"{typ4['r7024ax']:>3}"]
            line_detail += lpar_detail1[typ4['r7024ax']]
            line_detail += [f"{cryam1r + cryam2r + cryam3r + cryac1r + cryac2r + cryac3r:>7.0f}",
                            f"{total_exec_time:>8.3f}", f"{total_utilization:>7.1f}", "RSA ME   1024"]
            line_detail += lpar_me_1024[typ4['r7024ax']]
            line_detail += [f"{cryam1r:>8.2f}", f"{cryam1e:>9.3f}", f"{cryam1u:>7.1f}"]
            report_detail.append(line_detail)
            line_detail = ["", "", "", "", "", "", "", "", "RSA ME   2048"]
            line_detail += lpar_me_2048[typ4['r7024ax']]
            line_detail += [f"{cryam2r:>8.2f}", f"{cryam2e:>9.3f}", f"{cryam2u:>7.1f}"]
            report_detail.append(line_detail)
            line_detail = ["", "", "", "", "", "", "", "", "RSA ME   4096"]
            line_detail += lpar_me_4096[typ4['r7024ax']]
            line_detail += [f"{cryam3r:>8.2f}", f"{cryam3e:>9.3f}", f"{cryam3u:>7.1f}"]
            report_detail.append(line_detail)
            line_detail = ["", "", "", "", "", "", "", "", "RSA CRT  1024"]
            line_detail += lpar_crt_1024[typ4['r7024ax']]
            line_detail += [f"{cryac1r:>8.2f}", f"{cryac1e:>9.3f}", f"{cryac1u:>7.1f}"]
            report_detail.append(line_detail)
            line_detail = ["", "", "", "", "", "", "", "", "RSA CRT  2048"]
            line_detail += lpar_crt_2048[typ4['r7024ax']]
            line_detail += [f"{cryac2r:>8.2f}", f"{cryac2e:>9.3f}", f"{cryac2u:>7.1f}"]
            report_detail.append(line_detail)
            line_detail = ["", "", "", "", "", "", "", "", "RSA CRT  4096"]
            line_detail += lpar_crt_4096[typ4['r7024ax']]
            line_detail += [f"{cryac3r:>8.2f}", f"{cryac3e:>9.3f}", f"{cryac3u:>7.1f}"]
            report_detail.append(line_detail)
    return report_content + tb.tabulate(report_detail,
                                        headers=["Type", "Id", "Rate", "Exec Time", "Util%", "Rate", "Exec Time",
                                                 "Util%",
                                                 "Function", "Rate", "Exec Time", "Util%", "Rate", "Exec Time",
                                                 "Util%"],
                                        colalign=('left', 'right', 'right', 'right', 'right', 'right', 'right', 'right',
                                                  'left', 'right', 'right', 'right', 'right', 'right', 'right'),
                                        floatfmt=('', '', '.0f', '.3f', '.1f', '.0f', '.3f', '.1f',
                                                  '', '.1f', '.3f', '.1f', '.2f', '.3f', '.1f')) + '\n'


def format_central_storage_paging_rates(pro, pag):
    if 'date' in pro.keys() and 'datetime' in pro.keys():
        report_date = pro['date']
        report_time = pro['datetime'].time().strftime('%H.%M.%S')
        interval = format_s2min(pro['smf71int'])
    elif 'date' in pro.keys():
        report_date = pro['date']
        report_time = '00.00.00'
        interval = format_s2hr(pro['smf71int'])
    else:
        report_date = pro['smf71ist'].date()
        report_time = pro['smf71ist'].time().strftime('%H.%M.%S')
        interval = format_s2min(pro['smf71int'])

    zos_ver = 'V' + pro['smf71mvs'][2:4].lstrip('0') + 'R' + pro['smf71mvs'][4:6].lstrip('0')
    interval_x = f"{interval[:-3]}"
    r1a = pag['smf71lbi'] / pro['smf71int']
    r1b = pag['smf71lni'] / pro['smf71int']
    r1c = r1a + r1b
    r2a = pag['sys_csa_pgin_nswap_blk'] / pro['smf71int']
    r2b = pag['sys_csa_pgin_nswap_nblk'] / pro['smf71int']
    r2c = r2a + r2b
    r2e = pag['smf71sno'] / pro['smf71int']
    r2f = r2e
    r3a = pag['smf71sbi'] / pro['smf71int']
    r3b = pag['smf71sni'] / pro['smf71int']
    r3c = r3a + r3b
    r3e = pag['sys_sum_pgout_nswap'] / pro['smf71int']
    r3f = r3e
    r4a = pag['smf71hin'] / pro['smf71int']
    r4b = r4a
    r4d = pag['smf71hot'] / pro['smf71int']
    r4e = r4d
    r5a = pag['smf71vin'] / pro['smf71int']
    r5b = r5a
    r5d = pag['smf71vot'] / pro['smf71int']
    r5e = r5d
    r6a = pag['smf71sin'] / pro['smf71int']
    r6b = pag['smf71blk'] / pro['smf71int']
    r6c = pag['as_nvio_pgin_nswap_nblk'] / pro['smf71int']
    r6d = r6a + r6b + r6c
    r6f = pag['smf71sot'] / pro['smf71int']
    r6g = pag['smf71pot'] / pro['smf71int']
    r6h = r6f + r6g
    r7a = pag['as_sum_pgin_swap'] / pro['smf71int']
    r7b = pag['as_sum_pgin_nswap_blk'] / pro['smf71int']
    r7c = pag['as_sum_pgin_nswap_nblk'] / pro['smf71int']
    r7d = r7a + r7b + r7c
    r7f = pag['as_sum_pgout_swap'] / pro['smf71int']
    r7g = pag['as_sum_pgout_nswap'] / pro['smf71int']
    r7h = r7f + r7g
    r8a = pag['total_hspace_pgin_nswap_blk'] / pro['smf71int']
    r8b = r8a
    r8d = pag['total_hspace_pgout_nswap'] / pro['smf71int']
    r8e = r8d
    r9a = pag['total_vio_pgin_nswap_blk'] / pro['smf71int']
    r9b = r9a
    r9d = pag['total_vio_pgout_nswap'] / pro['smf71int']
    r9e = r9d
    r10a = pag['total_nvio_pgin_swap'] / pro['smf71int']
    r10b = pag['total_nvio_pgin_nswap_blk'] / pro['smf71int']
    r10c = pag['smf71pin'] / pro['smf71int']
    r10d = r10a + r10b + r10c
    r10f = pag['total_nvio_pgout_swap'] / pro['smf71int']
    r10g = pag['total_nvio_pgout_nswap'] / pro['smf71int']
    r10h = r10f + r10g
    r11a = pag['total_sum_pgin_swap'] / pro['smf71int']
    r11b = pag['total_sum_pgin_nswap_blk'] / pro['smf71int']
    r11c = pag['total_sum_pgin_nswap_nblk'] / pro['smf71int']
    r11d = r11a + r11b + r11c
    r11f = pag['total_sum_pgout_swap'] / pro['smf71int']
    r11g = pag['total_sum_pgout_nswap'] / pro['smf71int']
    r11h = r11f + r11g
    r12a = pag['smf71asi'] / pro['smf71int']
    r12b = r12a
    r12c = pag['smf71aso'] / pro['smf71int']
    r12d = r12c
    r3d = r3c / r11d * 100 if r11d > 0.01 else 0
    r3g = r3f / r11h * 100 if r11h > 0.01 else 0
    r1d = r1c / r11d * 100 if r11d > 0.01 else 0
    r2d = r2c / r11d * 100 if r11d > 0.01 else 0
    r2g = r2e / r11h * 100 if r11h > 0.01 else 0
    r7e = r7d / r11d * 100 if r11d > 0.01 else 0
    r7i = r7h / r11h * 100 if r11h > 0.01 else 0
    r4c = r4b / r11d * 100 if r11d > 0.01 else 0
    r5c = r5b / r11d * 100 if r11d > 0.01 else 0
    r6e = r6d / r11d * 100 if r11d > 0.01 else 0
    r4f = r4e / r11h * 100 if r11h > 0.01 else 0
    r5f = r5e / r11h * 100 if r11h > 0.01 else 0
    r6i = r6h / r11h * 100 if r11h > 0.01 else 0
    r11e = 100 if r11d > 0.01 else 0
    r11i = 100 if r11h > 0.01 else 0
    r8c = r8b / r11d * 100 if r11d > 0.01 else 0
    r8f = r8e / r11h * 100 if r11h > 0.01 else 0
    r9c = r9b / r11d * 100 if r11d > 0.01 else 0
    r9f = r9e / r11h * 100 if r11h > 0.01 else 0
    r10e = r10d / r11d * 100 if r11d > 0.01 else 0
    r10i = r10h / r11h * 100 if r11h > 0.01 else 0
    whitespace = ' '
    header1 = [["                                           P A G I N G  A C T I V I T Y"]]
    header2 = [
        [f"{whitespace:>12}", f"z/OS {zos_ver}", f"{whitespace:>13}", f"System ID {pag['smf71sid']}", f"{whitespace:>6}",
         f"Date {report_date:%m/%d/%Y}", f"{whitespace:>11}", f"Interval {interval_x}"],
        ["", "", "", f"RMF Version {pro['smf71mfv']:<5}", "", f"Time {report_time}", "",
         f"Cycle {pro['smf71cyc'] / 1000:5.3f} Seconds"]
    ]
    header3 = [
        [f"OPT = {pag['smf71opt']:<8}                             Central Storage Paging Rates - in Pages per Second"],
        [
            "------------------------------------------------------------------------------------------------------------------------------------"],
        ["                 ------------------ Page In ------------------     ------------ Page Out ------------"],
        ["                             --- Non Swap ---    ---- Total ---                        ---- Total ---"]]

    report = [
        ["Pageable System"],
        ["Areas (Non-VIO)"],
        ["     LPA", "", f"{r1a:>6.2f}", f"{r1b:>6.2f}", f"{r1c:>6.2f}", f"{r1d:>4.0f}"],
        ["     CSA", "", f"{r2a:>6.2f}", f"{r2b:>6.2f}", f"{r2c:>6.2f}", f"{r2d:>4.0f}", "", f"{r2e:>6.2f}",
         f"{r2f:>6.2f}", f"{r2g:>4.0f}"],
        ["", "", "------", "------", "------", "----", "", "------", "------", "----"],
        ["     Sum", "", f"{r3a:>6.2f}", f"{r3b:>6.2f}", f"{r3c:>6.2f}", f"{r3d:>4.0f}", "", f"{r3e:>6.2f}",
         f"{r3f:>6.2f}", f"{r3g:>4.0f}"],
        ["Address Spaces"],
        ["     Hiperspace", "", f"{r4a:>6.2f}", "", f"{r4b:>6.2f}", f"{r4c:>4.0f}", "", f"{r4d:>6.2f}", f"{r4e:>6.2f}",
         f"{r4f:>4.0f}"],
        ["     VIO", "", f"{r5a:>6.2f}", "", f"{r5b:>6.2f}", f"{r5c:>4.0f}", "", f"{r5d:>6.2f}", f"{r5e:>6.2f}",
         f"{r5f:>4.0f}"],
        ["     Non-VIO", f"{r6a:>6.2f}", f"{r6b:>6.2f}", f"{r6c:>6.2f}", f"{r6d:>6.2f}", f"{r6e:>4.0f}", f"{r6f:>6.2f}",
         f"{r6g:>6.2f}", f"{r6h:>6.2f}", f"{r6i:>4.0f}"],
        ["", "------", "------", "------", "------", "----", "------", "------", "------", "----"],
        ["     Sum", f"{r7a:>6.2f}", f"{r7b:>6.2f}", f"{r7c:>6.2f}", f"{r7d:>6.2f}", f"{r7e:>4.0f}", f"{r7f:>6.2f}",
         f"{r7g:>6.2f}", f"{r7h:>6.2f}", f"{r7i:>4.0f}"],
        ["Total System"],
        ["     Hiperspace", "", f"{r8a:>6.2f}", "", f"{r8b:>6.2f}", f"{r8c:>4.0f}", "", f"{r8d:>6.2f}", f"{r8e:>6.2f}",
         f"{r8f:>4.0f}"],
        ["     VIO", "", f"{r9a:>6.2f}", "", f"{r9b:>6.2f}", f"{r9c:>4.0f}", "", f"{r9d:>6.2f}", f"{r9e:>6.2f}",
         f"{r9f:>4.0f}"],
        ["     Non-VIO", f"{r10a:>6.2f}", f"{r10b:>6.2f}", f"{r10c:>6.2f}", f"{r10d:>6.2f}", f"{r10e:>4.0f}",
         f"{r10f:>6.2f}", f"{r10g:>6.2f}", f"{r10h:>6.2f}", f"{r10i:>4.0f}"],
        ["", "------", "------", "------", "------", "----", "------", "------", "------", "----"],
        ["     Sum", f"{r11a:>6.2f}", f"{r11b:>6.2f}", f"{r11c:>6.2f}", f"{r11d:>6.2f}", f"{r11e:>4.0f}",
         f"{r11f:>6.2f}", f"{r11g:>6.2f}", f"{r11h:>6.2f}", f"{r11i:>4.0f}"],
        ["     Shared", "", "", f"{r12a:>6.2f}", f"{r12b:>6.2f}", "", "", f"{r12c:>6.2f}", f"{r12d:>6.2f}"]]
    report2 = [
        ["Page Movement Within Central Storage          ", f"{pag['pg_mv_rate']:>7.2f}"],
        ["Page Movement Time %", f"{pag['pg_mv_time_percentage']:>7.1f}"],
        ["Average Number of Pages Per Block", f"{pag['avg_pg_per_blk']:>7.1f}"],
        ["Blocks per Second", f"{pag['blk_per_seconds']:>7.2f}"],
        ["Page-in Events (Page Fault Rate)", f"{pag['pg_fault_rate']:>7.2f}"]
    ]
    return (tb.tabulate(header1, tablefmt="plain") + '\n' +
            tb.tabulate(header2, tablefmt="plain") + '\n' +
            tb.tabulate(header3, tablefmt='plain') + '\n' +
            tb.tabulate(report, tablefmt='plain',
                        headers=[" \nCategory\n---------------",
                                 " \nSwap\n------", " \nBlock\n------", "Non\nBlock\n------",
                                 " \nRate\n------", " \n%\n----",
                                 " \nSwap\n------", "Non\nSwap\n------",
                                 " \nRate\n------", " \n%\n----"]) + '\n' +
            tb.tabulate(report2, tablefmt="plain", colalign=('left', 'right'), floatfmt=('', '.2f')))


def format_central_storage_movement_req_rates(pro, pag):
    if 'date' in pro.keys() and 'datetime' in pro.keys():
        report_date = pro['date']
        report_time = pro['datetime'].time().strftime('%H.%M.%S')
        interval = format_s2min(pro['smf71int'])
    elif 'date' in pro.keys():
        report_date = pro['date']
        report_time = '00.00.00'
        interval = format_s2hr(pro['smf71int'])
    else:
        report_date = pro['smf71ist'].date()
        report_time = pro['smf71ist'].time().strftime('%H.%M.%S')
        interval = format_s2min(pro['smf71int'])
    zos_ver = 'V' + pro['smf71mvs'][2:4].lstrip('0') + 'R' + pro['smf71mvs'][4:6].lstrip('0')
    interval_x = f"{interval[:-3]}"
    whitespace = ' '
    header1 = [["                                           P A G I N G  A C T I V I T Y"]]
    header2 = [
        [f"{whitespace:>12}", f"z/OS {zos_ver}", f"{whitespace:>13}", f"System ID {pag['smf71sid']}", f"{whitespace:>6}",
         f"Date {report_date:%m/%d/%Y}", f"{whitespace:>11}", f"Interval {interval_x}"],
        ["", "", "", f"RMF Version {pro['smf71mfv']:<5}", "", f"Time {report_time}", "",
         f"Cycle {pro['smf71cyc'] / 1000:5.3f} Seconds"]
    ]
    header3 = [
        [f"OPT = {pag['smf71opt']:<8}                             Central Storage Movement and Request Rates - in Pages per Second"],
        ["------------------------------------------------------------------------------------------------------------------------------------"],
        [f"System UIC: Min =  {pag['smf71ulc']:>6}    Max = {pag['smf71uhc']:>6}   Avg = {pag['smf71uac']:>6}"]
    ]
    report1 = [
        ["     Hiperspace",
         f"{pag['smf71hws'] / pro['smf71int']:>6.2f}",
         f"{pag['smf71hrs'] / pro['smf71int']:>6.2f}",
         f"{pag['smf71mhi']:>10.0f}",
         f"{pag['smf71xhi']:>10.0f}",
         f"{pag['smf71ahi']:>10.0f}"],
        ["     Vio",
         f"{pag['smf71vws'] / pro['smf71int']:>6.2f}",
         f"{pag['smf71vrs'] / pro['smf71int']:>6.2f}",
         f"{pag['smf71mvi']:>10.0f}",
         f"{pag['smf71xvi']:>10.0f}",
         f"{pag['smf71avi']:>10.0f}"]]
    report2 = [
        ["     Rate",
         f"{convert_si(pag['smf71grn'] / pro['smf71int'], 8, 2, True):>9}",
         f"{convert_si(pag['smf71fbn'] / pro['smf71int'], 8, 2, True):>9}",
         f"{convert_si(pag['smf71frn'] / pro['smf71int'], 8, 2, True):>9}",
         f"{convert_si(pag['smf71ffn'] / pro['smf71int'], 8, 2, True):>9}",
         f"{convert_si(pag['smf711rn'] / pro['smf71int'], 8, 2, True):>9}",
         f"{convert_si(pag['smf71nrn'] / pro['smf71int'], 8, 2, True):>9}"]]
    return (tb.tabulate(header1, tablefmt="plain") + '\n' +
            tb.tabulate(header2, tablefmt="plain") + '\n' +
            tb.tabulate(header3, tablefmt="plain") + '\n' +
            tb.tabulate(report1, tablefmt='plain',
                        headers=["Central Storage\n---------------",
                                 "Page Write\n-- Rate --", "Page Read\n  -- Rate --",
                                 "---------\n-- Min --", "Frame Counts\n-- Max --", "---------\n-- Avg --"],
                        floatfmt=("", ".2f", ".2f", ".2f", ".0f", ".0f", ".0f")) + '\n' +
            "                      --------- GETMAIN -------    --------- Fixed --------- --- Ref Faults ---\n" +
            tb.tabulate(report2, tablefmt='plain',
                        headers=["Storage Requests", "Requests", "Frames Backed", "Req < 2GB", "Frames < 2GB", "1st",
                                 "Non-1st"]))


def format_frame_slot_counts(pro, pag):
    if 'date' in pro.keys() and 'datetime' in pro.keys():
        report_date = pro['date']
        report_time = pro['datetime'].time().strftime('%H.%M.%S')
        interval = format_s2min(pro['smf71int'])
    elif 'date' in pro.keys():
        report_date = pro['date']
        report_time = '00.00.00'
        interval = format_s2hr(pro['smf71int'])
    else:
        report_date = pro['smf71ist'].date()
        report_time = pro['smf71ist'].time().strftime('%H.%M.%S')
        interval = format_s2min(pro['smf71int'])
    zos_ver = 'V' + pro['smf71mvs'][2:4].lstrip('0') + 'R' + pro['smf71mvs'][4:6].lstrip('0')
    interval_x = f"{interval[:-3]}"
    whitespace = ' '
    header1 = [["                                           P A G I N G  A C T I V I T Y"]]
    header2 = [
        [f"{whitespace:>12}", f"z/OS {zos_ver}", f"{whitespace:>13}", f"System ID {pag['smf71sid']}", f"{whitespace:>6}",
         f"Date {report_date:%m/%d/%Y}", f"{whitespace:>11}", f"Interval {interval_x}"],
        ["", "", "", f"RMF Version {pro['smf71mfv']:<5}", "", f"Time {report_time}", "",
         f"Cycle {pro['smf71cyc'] / 1000:5.3f} Seconds"]]
    header3 = [
        [f"OPT = {pag['smf71opt']:<8}                             Central Storage Movement and Request Rates - in Pages per Second"],
        [f"-------------------------------------------------------------------------------------------------------------------------------------"],
        [f"                                                      Frame and Slot Counts"],
        [f"-------------------------------------------------------------------------------------------------------------------------------------"],
        [f"({pro['smf71sam']} Samples)\n"]]
    report1 = [
        ["      Min             ",
         f"{convert_si(pag['smf71fin'] + pag['smf71mnt'], 9, 0, True)}",
         f"{convert_si(pag['smf71mnf'], 9, 0, True)}",
         f"{convert_si(pag['smf71msr'], 9, 0, True)}",
         f"{convert_si(pag['smf71nlp'], 9, 0, True)}",
         f"{convert_si(pag['smf71mnp'], 9, 0, True)}",
         f"{convert_si(pag['smf71mlr'], 9, 0, True)}",
         f"{convert_si(pag['smf71mns'], 10, 0, True)}",
         f"{convert_si(pag['smf71srm'], 9, 0, True)}",
         f"{convert_si(pag['smf71crm'], 9, 0, True)}"],
        ["      Max             ",
         f"{convert_si(pag['smf71fin'] + pag['smf71mxt'], 9, 0, True)}",
         f"{convert_si(pag['smf71mxf'], 9, 0, True)}",
         f"{convert_si(pag['smf71xsr'], 9, 0, True)}",
         f"{convert_si(pag['smf71xlp'], 9, 0, True)}",
         f"{convert_si(pag['smf71mxp'], 9, 0, True)}",
         f"{convert_si(pag['smf71xlr'], 9, 0, True)}",
         f"{convert_si(pag['smf71mxs'], 10, 0, True)}",
         f"{convert_si(pag['smf71srx'], 9, 0, True)}",
         f"{convert_si(pag['smf71crx'], 9, 0, True)}"],
        ["      Avg             ",
         f"{convert_si(pag['smf71fin'] + pag['smf71avt'], 9, 0, True)}",
         f"{convert_si(pag['smf71avf'], 9, 0, True)}",
         f"{convert_si(pag['smf71asr'], 9, 0, True)}",
         f"{convert_si(pag['smf71alp'], 9, 0, True)}",
         f"{convert_si(pag['smf71avp'], 9, 0, True)}",
         f"{convert_si(pag['smf71alr'], 9, 0, True)}",
         f"{convert_si(pag['smf71avs'], 10, 0, True)}",
         f"{convert_si(pag['smf71sra'], 9, 0, True)}",
         f"{convert_si(pag['smf71cra'], 9, 0, True)}"],
        tb.SEPARATING_LINE,
        ["Fixed Frames          \n----------------------",
         "Total\n---------", "Nucleus\n---------", "SQA\n---------", "LPA\n---------",
         "CSA\n---------", "LSQA\n---------", "Regions+SWA\n-----------", "<16 MB\n---------", "16MB-2GB\n---------"],
        ["      Min             ",
         f"{convert_si(pag['smf71fin'] + pag['smf71mnx'], 9, 0, True)}",
         f"{convert_si(pag['smf71fin'], 9, 0, True)}",
         f"{convert_si(pag['smf71mnq'], 9, 0, True)}",
         f"{convert_si(pag['smf71nlf'], 9, 0, True)}",
         f"{convert_si(pag['smf71mnc'], 9, 0, True)}",
         f"{convert_si(pag['smf71nls'], 9, 0, True)}",
         f"{convert_si(pag['smf71mnr'], 10, 0, True)}",
         f"{convert_si(pag['smf71mnl'], 9, 0, True)}",
         f"{convert_si(pag['smf71mfb'], 9, 0, True)}"],
        ["      Max             ",
         f"{convert_si(pag['smf71fin'] + pag['smf71mxx'], 9, 0, True)}",
         f"{convert_si(pag['smf71fin'], 9, 0, True)}",
         f"{convert_si(pag['smf71mxq'], 9, 0, True)}",
         f"{convert_si(pag['smf71xlf'], 9, 0, True)}",
         f"{convert_si(pag['smf71mxc'], 9, 0, True)}",
         f"{convert_si(pag['smf71xls'], 9, 0, True)}",
         f"{convert_si(pag['smf71mxr'], 10, 0, True)}",
         f"{convert_si(pag['smf71mxl'], 9, 0, True)}",
         f"{convert_si(pag['smf71xfb'], 9, 0, True)}"],
        ["      Avg             ",
         f"{convert_si(pag['smf71fin'] + pag['smf71avx'], 9, 0, True)}",
         f"{convert_si(pag['smf71fin'], 9, 0, True)}",
         f"{convert_si(pag['smf71avq'], 9, 0, True)}",
         f"{convert_si(pag['smf71alf'], 9, 0, True)}",
         f"{convert_si(pag['smf71avc'], 9, 0, True)}",
         f"{convert_si(pag['smf71als'], 9, 0, True)}",
         f"{convert_si(pag['smf71avr'], 10, 0, True)}",
         f"{convert_si(pag['smf71avl'], 9, 0, True)}",
         f"{convert_si(pag['smf71afb'], 9, 0, True)}"],
        tb.SEPARATING_LINE,
        ["Shared Frames / Slots\n----------------------", "Total\n---------",
         "Central\n---------", "Storage\n---------", "Fixed Tot\n---------", "Fixed Bel\n---------",
         "HV 1M\n---------", "HV 4K\n-----------", "Aux DASD\n---------", "Aux SCM\n---------"],
        ["      Min             ",
         f"{convert_si(pag['smf71mgt'], 9, 0, True)}", "",
         f"{convert_si(pag['smf71mgc'], 9, 0, True)}",
         f"{convert_si(pag['smf71mgf'], 9, 0, True)}",
         f"{convert_si(pag['smf71mgb'], 9, 0, True)}",
         f"{convert_si(pag['smf71s4m'], 9, 0, True)}",
         f"{convert_si(pag['smf71s3m'], 10, 0, True)}",
         f"{convert_si(pag['smf71mga'], 9, 0, True)}",
         f"{convert_si(pag['smf71s7m'], 9, 0, True) if is_bit_set(pag['smf71rfl'], 32, 0) else 'N/A'}"],
        ["      Max             ",
         f"{convert_si(pag['smf71xgt'], 9, 0, True)}", "",
         f"{convert_si(pag['smf71xgc'], 9, 0, True)}",
         f"{convert_si(pag['smf71xgf'], 9, 0, True)}",
         f"{convert_si(pag['smf71xgb'], 9, 0, True)}",
         f"{convert_si(pag['smf71s4x'], 9, 0, True)}",
         f"{convert_si(pag['smf71s3x'], 10, 0, True)}",
         f"{convert_si(pag['smf71xga'], 9, 0, True)}",
         f"{convert_si(pag['smf71s7x'], 9, 0, True) if is_bit_set(pag['smf71rfl'], 32, 0) else 'N/A'}"],
        ["      Avg             ",
         f"{convert_si(pag['smf71agt'], 9, 0, True)}", "",
         f"{convert_si(pag['smf71agc'], 9, 0, True)}",
         f"{convert_si(pag['smf71agf'], 9, 0, True)}",
         f"{convert_si(pag['smf71agb'], 9, 0, True)}",
         f"{convert_si(pag['smf71s4a'], 9, 0, True)}",
         f"{convert_si(pag['smf71s3a'], 10, 0, True)}",
         f"{convert_si(pag['smf71aga'], 9, 0, True)}",
         f"{convert_si(pag['smf71s7a'], 9, 0, True) if is_bit_set(pag['smf71rfl'], 32, 0) else 'N/A'}"],
        tb.SEPARATING_LINE,
        ["Local Page Data Set Slots\n-------------------------", "Total\n---------",
         "Available\n---------", "Bad\n---------", "Non-VIO\n---------", "VIO\n---------"],
        ["      Min             ",
         f"{convert_si(pag['smf71mna'], 9, 0, True)}",
         f"{convert_si(pag['smf71mnu'], 9, 0, True)}",
         f"{convert_si(pag['smf71mnb'], 9, 0, True)}",
         f"{convert_si(pag['smf71mnm'], 9, 0, True)}",
         f"{convert_si(pag['smf71mnv'], 9, 0, True)}"],
        ["      Max             ",
         f"{convert_si(pag['smf71mxa'], 9, 0, True)}",
         f"{convert_si(pag['smf71mxu'], 9, 0, True)}",
         f"{convert_si(pag['smf71mxb'], 9, 0, True)}",
         f"{convert_si(pag['smf71mxm'], 9, 0, True)}",
         f"{convert_si(pag['smf71mxv'], 9, 0, True)}"],
        ["      Avg             ",
         f"{convert_si(pag['smf71tsc'], 9, 0, True)}",
         f"{convert_si(pag['smf71avu'], 9, 0, True)}",
         f"{convert_si(pag['smf71avb'], 9, 0, True)}",
         f"{convert_si(pag['smf71avm'], 9, 0, True)}",
         f"{convert_si(pag['smf71lvv'], 9, 0, True)}"],
        tb.SEPARATING_LINE,
        ["SCM Paging Blocks     \n----------------------", "Total\n---------",
         "Available\n---------", "Bad\n---------", "In-Use\n---------"],
    ]

    if is_bit_set(pag['smf71rfl'], 32, 0):
        report1 = report1 + [
            ["      Min             ",
             f"{convert_si(pag['smf71tsm'], 9, 0, True)}",
             f"{convert_si(pag['smf71asm'], 9, 0, True)}",
             f"{convert_si(pag['smf71bsm'], 9, 0, True)}",
             f"{convert_si(pag['smf71usm'], 9, 0, True)}"],
            ["      Max             ",
             f"{convert_si(pag['smf71tsx'], 9, 0, True)}",
             f"{convert_si(pag['smf71asx'], 9, 0, True)}",
             f"{convert_si(pag['smf71bsx'], 9, 0, True)}",
             f"{convert_si(pag['smf71usx'], 9, 0, True)}"],
            ["      Avg             ",
             f"{convert_si(pag['smf71tsa'], 9, 0, True)}",
             f"{convert_si(pag['smf71asv'], 9, 0, True)}",
             f"{convert_si(pag['smf71bsa'], 9, 0, True)}",
             f"{convert_si(pag['smf71usa'], 9, 0, True)}"]
        ]

    return (tb.tabulate(header1, tablefmt="plain") + '\n' +
            tb.tabulate(header2, tablefmt="plain") + '\n' +
            tb.tabulate(header3, tablefmt="plain") + '\n' +
            tb.tabulate(report1, tablefmt='plain', stralign="right",
                        colalign=("left", "right", "right", "right", "right", "right", "right", "right", "right",
                                  "right"),
                        headers=["Central Storage Frames\n----------------------",
                                 "Total\n---------",
                                 "Available\n---------",
                                 "SQA\n---------",
                                 "LPA\n---------",
                                 "CSA\n---------",
                                 "LSQA\n---------",
                                 "Regions+SWA\n-----------",
                                 "HV Shared\n---------",
                                 "HV Common\n---------"]))


def format_memory_obj(pro, pag):
    if 'date' in pro.keys() and 'datetime' in pro.keys():
        report_date = pro['date']
        report_time = pro['datetime'].time().strftime('%H.%M.%S')
        interval = format_s2min(pro['smf71int'])
    elif 'date' in pro.keys():
        report_date = pro['date']
        report_time = '00.00.00'
        interval = format_s2hr(pro['smf71int'])
    else:
        report_date = pro['smf71ist'].date()
        report_time = pro['smf71ist'].time().strftime('%H.%M.%S')
        interval = format_s2min(pro['smf71int'])
    zos_ver = 'V' + pro['smf71mvs'][2:4].lstrip('0') + 'R' + pro['smf71mvs'][4:6].lstrip('0')
    interval_x = f"{interval[:-3]}"
    whitespace = ' '
    header1 = [["                                           P A G I N G  A C T I V I T Y"]]
    header2 = [
        [f"{whitespace:>12}", f"z/OS {zos_ver}", f"{whitespace:>13}", f"System ID {pag['smf71sid']}", f"{whitespace:>6}",
         f"Date {report_date:%m/%d/%Y}", f"{whitespace:>11}", f"Interval {interval_x}"],
        ["", "", "", f"RMF Version {pro['smf71mfv']:<5}", "", f"Time {report_time}", "",
         f"Cycle {pro['smf71cyc'] / 1000:5.3f} Seconds"]]
    header3 = [
        [f"OPT = {pag['smf71opt']:<8}                             Memory Objects and High Virtual Storage Frames"],
        ["-------------------------------------------------------------------------------------------------------------------------------------"],
    ]
    report1 = [
        ["1 MB Frames", f"{convert_si(pag['smf71lfa'], 9, 0, True)}"],
        ["2 GB Frames", f"{convert_si(pag['smf71gfx'], 9, 0, True)}"],
        ["Memory Objects\n------------------", "Fixed 1M\n---------", "Fixed 2G\n---------", "Common\n---------",
         "Shared\n---------", "Shared 1M\n---------"],
        ["      Min        ",
         f"{convert_si(pag['smf71lom'], 9, 0, True)}",
         f"{convert_si(pag['smf71gom'], 9, 0, True)}",
         f"{convert_si(pag['smf71com'], 9, 0, True)}",
         f"{convert_si(pag['smf71som'], 9, 0, True)}",
         f"{convert_si(pag['smf71s2m'], 9, 0, True)}"],
        ["      Max        ",
         f"{convert_si(pag['smf71lox'], 9, 0, True)}",
         f"{convert_si(pag['smf71gox'], 9, 0, True)}",
         f"{convert_si(pag['smf71cox'], 9, 0, True)}",
         f"{convert_si(pag['smf71sox'], 9, 0, True)}",
         f"{convert_si(pag['smf71s2x'], 9, 0, True)}"],
        ["      Avg        ",
         f"{convert_si(pag['smf71loa'], 9, 0, True)}",
         f"{convert_si(pag['smf71goa'], 9, 0, True)}",
         f"{convert_si(pag['smf71coa'], 9, 0, True)}",
         f"{convert_si(pag['smf71soa'], 9, 0, True)}",
         f"{convert_si(pag['smf71s2a'], 9, 0, True)}"],
        ["1 MB Frames\n------------------", "----------\nMaximum", "Fixed\nAvailable", "---------------\nIn-Use",
         "Pageable\n--------", "Available\n---------", "Total\n--------"],
        ["      Min        ",
         f"{convert_si(pag['smf71l1m'], 9, 0, True)}",
         f"{convert_si(pag['smf71l7m'], 9, 0, True)}",
         f"{convert_si(pag['smf71lrm'], 9, 0, True)}",
         f"{convert_si(pag['smf71plm'], 9, 0, True)}",
         f"{convert_si(pag['smf71l9m'], 9, 0, True)}",
         f"{convert_si(pag['smf71l8m'], 8, 0, True):>9}"],
        ["      Max        ",
         f"{convert_si(pag['smf71l1x'], 9, 0, True)}",
         f"{convert_si(pag['smf71l7x'], 9, 0, True)}",
         f"{convert_si(pag['smf71lrx'], 9, 0, True)}",
         f"{convert_si(pag['smf71plx'], 9, 0, True)}",
         f"{convert_si(pag['smf71l9x'], 9, 0, True)}",
         f"{convert_si(pag['smf71l8x'], 8, 0, True):>9}"],
        ["      Avg        ",
         f"{convert_si(pag['smf71l1a'], 9, 0, True)}",
         f"{convert_si(pag['smf71l7a'], 9, 0, True)}",
         f"{convert_si(pag['smf71lra'], 9, 0, True)}",
         f"{convert_si(pag['smf71pla'], 9, 0, True)}",
         f"{convert_si(pag['smf71l9a'], 9, 0, True)}",
         f"{convert_si(pag['smf71l8a'], 8, 0, True):>9}"],
        ["2 GB Frames\n------------------", "-----------\nMaximum", "  Fixed\nAvailable", "----------------\nIn-Use"],
        ["      Min        ",
         f"{convert_si(pag['smf71gfm'], 9, 0, True)}",
         f"{convert_si(pag['smf71gam'], 9, 0, True)}",
         f"{convert_si(pag['smf71gum'], 9, 0, True)}"],
        ["      Max        ",
         f"{convert_si(pag['smf71gfx'], 9, 0, True)}",
         f"{convert_si(pag['smf71gax'], 9, 0, True)}",
         f"{convert_si(pag['smf71gux'], 9, 0, True)}"],
        ["      Avg        ",
         f"{convert_si(pag['smf71gfa'], 9, 0, True)}",
         f"{convert_si(pag['smf71gaa'], 9, 0, True)}",
         f"{convert_si(pag['smf71gua'], 9, 0, True)}"],
        ["High Shared Frames\n------------------", "Total\n---------", "", "Central Storage\n---------------",
         "Backed 1M\n---------", "", "", "Aux DASD\n---------", "Aux SCM\n---------"],
        ["      Min        ",
         f"{convert_si(pag['smf71s1m'], 9, 1, True)}", "",
         f"{convert_si(pag['smf71srm'], 9, 0, True)}",
         f"{convert_si(pag['smf71s4m'], 9, 0, True)}", "", "",
         f"{convert_si(pag['smf71s5m'], 9, 0, True)}",
         f"{convert_si(pag['smf71s6m'], 9, 0, True) if is_bit_set(pag['smf71rfl'], 32, 0) else 'N/A'}"],
        ["      Max        ",
         f"{convert_si(pag['smf71s1x'], 9, 1, True)}", "",
         f"{convert_si(pag['smf71srx'], 9, 0, True)}",
         f"{convert_si(pag['smf71s4x'], 9, 0, True)}", "", "",
         f"{convert_si(pag['smf71s5x'], 9, 0, True)}",
         f"{convert_si(pag['smf71s6x'], 9, 0, True) if is_bit_set(pag['smf71rfl'], 32, 0) else 'N/A'}"],
        ["      Avg        ",
         f"{convert_si(pag['smf71s1a'], 9, 1, True)}", "",
         f"{convert_si(pag['smf71sra'], 9, 0, True)}",
         f"{convert_si(pag['smf71s4a'], 9, 0, True)}", "", "",
         f"{convert_si(pag['smf71s5a'], 9, 0, True)}",
         f"{convert_si(pag['smf71s6a'], 9, 0, True) if is_bit_set(pag['smf71rfl'], 32, 0) else 'N/A'}"],
        ["High Common Frames\n------------------", "Total\n---------", "", "Central Storage\n---------------",
         "Backed 1M\n---------", "Fixed\n---------", "Fixed 1M\n---------", "Aux DASD\n---------",
         "Aux SCM\n---------"],
        ["      MIN        ",
         f"{convert_si(pag['smf71c1m'], 9, 1, True)}", "",
         f"{convert_si(pag['smf71crm'], 9, 0, True)}",
         f"{convert_si(pag['smf71c3m'], 9, 0, True)}",
         f"{convert_si(pag['smf71cfm'], 9, 0, True)}",
         f"{convert_si(pag['smf71c2m'], 9, 0, True)}",
         f"{convert_si(pag['smf71csm'], 9, 0, True)}",
         f"{convert_si(pag['smf71c4m'], 9, 0, True) if is_bit_set(pag['smf71rfl'], 32, 0) else 'N/A'}"],
        ["      MAX        ",
         f"{convert_si(pag['smf71c1x'], 9, 1, True)}", "",
         f"{convert_si(pag['smf71crx'], 9, 0, True)}",
         f"{convert_si(pag['smf71c3x'], 9, 0, True)}",
         f"{convert_si(pag['smf71cfx'], 9, 0, True)}",
         f"{convert_si(pag['smf71c2x'], 9, 0, True)}",
         f"{convert_si(pag['smf71csx'], 9, 0, True)}",
         f"{convert_si(pag['smf71c4x'], 9, 0, True) if is_bit_set(pag['smf71rfl'], 32, 0) else 'N/A'}"],
        ["      AVG        ",
         f"{convert_si(pag['smf71c1a'], 9, 1, True)}", "",
         f"{convert_si(pag['smf71cra'], 9, 0, True)}",
         f"{convert_si(pag['smf71c3a'], 9, 0, True)}",
         f"{convert_si(pag['smf71cfa'], 9, 0, True)}",
         f"{convert_si(pag['smf71c2a'], 9, 0, True)}",
         f"{convert_si(pag['smf71csa'], 9, 0, True)}",
         f"{convert_si(pag['smf71c4a'], 9, 0, True) if is_bit_set(pag['smf71rfl'], 32, 0) else 'N/A'}"],
    ]
    return (tb.tabulate(header1, tablefmt="plain") + '\n' +
            tb.tabulate(header2, tablefmt="plain") + '\n' +
            tb.tabulate(header3, tablefmt="plain") + '\n' +
            tb.tabulate(report1, tablefmt='plain', stralign="right",
                        colalign=(
                            "left", "right", "right", "right", "right", "right", "right", "right", "right",),
                        headers=["LFAREA\n------------------",
                                 "Maximum\n---------",
                                 " ",
                                 " ",
                                 " ",
                                 " ",
                                 " ",
                                 " ",
                                 " "]))


def format_channel_header(pro, ctl):
    if 'date' in pro.keys() and 'datetime' in pro.keys():
        report_date = pro['date']
        report_time = pro['datetime'].time().strftime('%H.%M.%S')
        interval = format_s2min(pro['smf73int'])
    elif 'date' in pro.keys():
        report_date = pro['date']
        report_time = '00.00.00'
        interval = format_s2hr(pro['smf73int'])
    else:
        report_date = pro['smf73ist'].date()
        report_time = pro['smf73ist'].time().strftime('%H.%M.%S')
        interval = format_s2min(pro['smf73int'])
    zos_ver = 'V' + pro['smf73mvs'][2:4].lstrip('0') + 'R' + pro['smf73mvs'][4:6].lstrip('0')
    interval_x = f"{interval[:-3]}"
    cpmf_mode = {0: 'Not Available', 1: 'Compatibility Mode', 2: 'Extended Mode'}
    whitespace = ' '
    header1 = [["                                           C H A N N E L   P A T H   A C T I V I T Y"]]
    header2 = [
        [f"{whitespace:>12}", f"z/OS {zos_ver}", f"{whitespace:>13}", f"System ID {ctl['smf73sid']}", f"{whitespace:>6}",
         f"Date {report_date:%m/%d/%Y}", f"{whitespace:>11}", f"Interval {interval_x}"],
        ["", "", "", f"RMF Version {pro['smf73mfv']:<5}", "", f"Time {report_time}", "",
         f"Cycle {pro['smf73cyc'] / 1000:5.3f} Seconds"]
    ]
    header3 = [
        ["IODF =", f"{ctl['smf73tsf']:2}", "  ",
         "Cr-Date:", f"{ctl['smf73tdt'].date():%m/%d/%Y}", "  ",
         "Cr-Time:", f"{ctl['smf73tdt'].time():%H.%M.%S}", "  ",
         "Act:", f"{'Activate' if ctl['config_changed_since_ipl'] else 'POR':<8}", "    ",
         "Mode:", "Lpar", "    ", "CPMF:", f"{cpmf_mode[ctl['smf73cmi']]:<18}", "    ", "CSSID:",
         f"{int(ctl['smf73css'], 0):>2}"]
    ]
    return (tb.tabulate(header1, tablefmt="plain") + "\n" + tb.tabulate(header2, tablefmt="plain") + "\n" +
            tb.tabulate(header3, tablefmt="plain") + "\n")


def format_channel_activity_report(pro, ctl, cha1s, cha2s, cha3s):
    report_detail_dict1 = {}  # for OSD type only
    report_detail_dict2 = {}
    report = format_channel_header(pro, ctl)
    report += \
        "--------------------------------------------------------------------------------------------------------------------------------------------------------\n" \
        "                                                    Details For All Channels Excluding OSA & Hipersockets\n" \
        "--------------------------------------------------------------------------------------------------------------------------------------------------------\n"

    for cha in cha1s:
        if cha['smf73acr'] in ('OSE', 'OSD', 'OSC', 'OSN'):
            if cha['smf73pid'] not in report_detail_dict1.keys():
                report_detail_dict1[cha['smf73pid']] = []
        elif cha['smf73pid'] not in report_detail_dict2.keys():
            report_detail_dict2[cha['smf73pid']] = []
        report_detail = \
            [f"{cha['smf73pid']:2}", f"{cha['smf73acr']:<5}",
             f"{' ' if cha['smf73gen'] == '0x00' else cha['smf73gen'][2:]:>2}",
             f"{cha['smf73spd'] / 1e9 if cha['smf73spd'] > 0 else ' ':{'>4.0f' if cha['smf73spd'] > 0 else '>4'}}{'G' if cha['smf73spd'] > 0 else ' ':1}",
             f"{'Y' if cha['ch_path_shared'] else ' ':1}"]
        if cha['ch_path_online']:
            if cha['smf73pti'] == 0:
                report_detail += ['------', '------', '------']
            else:
                report_detail += [f"{cha['part_utilization_pct']:>6.2f}", f"{cha['total_utilization_pct']:>6.2f}",
                                  f"{cha['busy_utilization_pct']:>6.2f}"]
            if cha['physical_network'] and cha['smf73acr'] in ('OSE', 'OSD', 'OSC', 'OSN'):
                report_detail += ['', '', '', '', f"{cha['smf73nt1']:<8}", f"{cha['smf73nt2']:<8}"]
        else:
            report_detail += ['Offline']
        if cha['smf73acr'] in ('OSE', 'OSD', 'OSC', 'OSN'):
            report_detail_dict1[cha['smf73pid']].append(report_detail)
        else:
            report_detail_dict2[cha['smf73pid']].append(report_detail)
    for cha in cha2s:
        if cha['smf73acr'] in ('OSE', 'OSD', 'OSC', 'OSN'):
            if cha['smf73pid'] not in report_detail_dict1.keys():
                report_detail_dict1[cha['smf73pid']] = []
        elif cha['smf73pid'] not in report_detail_dict2.keys():
            report_detail_dict2[cha['smf73pid']] = []
        report_detail = \
            [f"{cha['smf73pid']:2}", f"{cha['smf73acr']:<5}",
             f"{' ' if cha['smf73gen'] == '0x00' else cha['smf73gen'][2:]:>2}",
             f"{cha['smf73spd'] / 1e9 if cha['smf73spd'] > 0 else ' ':{'>4.0f' if cha['smf73spd'] > 0 else '>4'}}{'G' if cha['smf73spd'] > 0 else ' ':1}",
             f"{'Y' if cha['ch_path_shared'] else ' ':1}",
             ]
        if cha['ch_path_online']:
            if cha['smf73pti'] > 0:
                report_detail += \
                    [f"{cha['part_utilization_pct'] if pd.notna(cha['part_utilization_pct']) else '----':{'> 6.2f' if pd.notna(cha['part_utilization_pct']) else '>6'}}",
                     f"{cha['total_utilization_pct'] if pd.notna(cha['total_utilization_pct']) else '----':{'> 6.2f' if pd.notna(cha['total_utilization_pct']) else '>6'}}",
                     f"{cha['bus_utilization_pct'] if pd.notna(cha['bus_utilization_pct']) else '----':{'> 6.2f' if pd.notna(cha['bus_utilization_pct']) else '>6'}}",
                     f"{convert_si(cha['part_read_rate'], 5, 2):>6}",
                     f"{convert_si(cha['total_read_rate'], 5, 2):>6}",
                     f"{convert_si(cha['part_write_rate'], 5, 2):>6}",
                     f"{convert_si(cha['total_write_rate'], 5, 2):>6}"]
                if cha['ch_path_extended']:  # ficon
                    report_detail += \
                        [f"{convert_si(cha['ficon_operations_rate'], 5, 1):>6}",
                         f"{convert_si(cha['ficon_operations_active'], 5, 1):>6}",
                         f"{convert_si(cha['ficon_operations_defer'], 5, 1):>6}",
                         f"{convert_si(cha['zhpf_operations_rate'], 5, 1):>6}",
                         f"{convert_si(cha['zhpf_operations_active'], 5, 1):>6}",
                         f"{convert_si(cha['zhpf_operations_defer'], 5, 1):>6}"]
                elif cha['smf73acr'] not in ('OSE', 'OSD', 'OSC', 'OSN'):
                    report_detail += ['', '', '', '', '', '']
            else:
                report_detail += ["----", "----", "----", "----", "----", "----", "---- "]
                if cha['ch_path_extended']:  # Ficon
                    report_detail += \
                        ["----", f"{convert_si(cha['ficon_operations_active'], 5, 1):>6}", "---- ",
                         "----", f"{convert_si(cha['zhpf_operations_active'], 5, 1):>6}", "----"]
                elif cha['smf73acr'] not in ('OSE', 'OSD', 'OSC', 'OSN'):
                    report_detail += ['', '', '', '', '', '']

            if cha['physical_network'] and cha['smf73acr'] in ('OSE', 'OSD', 'OSC', 'OSN'):
                report_detail += [f"{cha['smf73nt1']:<8}", f"{cha['smf73nt2']:<8}"]

        else:
            report_detail += ['Offline']

        if cha['smf73acr'] in ('OSE', 'OSD', 'OSC', 'OSN'):
            report_detail_dict1[cha['smf73pid']].append(report_detail)
        else:
            report_detail_dict2[cha['smf73pid']].append(report_detail)

    hipersocket_detail_report = []
    for cha in cha3s:
        hipersocket_detail = \
            [f"{cha['smf73pid']:2}", f"{cha['smf73acr']:<5}",
             f"{' ' if cha['smf73gen'] == '0x00' else cha['smf73gen'][2:]:>2}",
             f"{'Y' if cha['ch_path_shared'] else ' ':1}"]
        if cha['ch_path_online']:
            if cha['smf73pti'] > 0:
                hipersocket_detail += \
                    [f"{convert_si(cha['part_write_rate'], 8, 0):>9}",
                     f"{convert_si(cha['total_write_rate'], 6, 0):>7}",
                     f"{convert_si(cha['message_rate_part'], 7, 0):>8}",
                     f"{convert_si(cha['message_rate_total'], 6, 0):>7}"]
            else:
                hipersocket_detail += ["-------", "-----", "------", "-----"]
            if cha['smf73pms'] > 0:
                hipersocket_detail += [f"{convert_si(cha['message_size_part'], 8, 0):>9}"]
            else:
                hipersocket_detail += ["------"]
            if cha['smf73tms'] > 0:
                hipersocket_detail += [f"{convert_si(cha['message_size_total'], 7, 0):>8}"]
            else:
                hipersocket_detail += ["------"]
            if cha['smf73pti'] > 0:
                hipersocket_detail += \
                    [f"{convert_si(cha['send_fail_part'], 9, 0):>10}",
                     f"{convert_si(cha['receive_fail_part'], 7, 0):>8}",
                     f"{convert_si(cha['receive_fail_total'], 6, 0):>7}", f"{cha['smf73nt1']:<8}"]
            else:
                hipersocket_detail += ["--------", "------", "-----", f"{cha['smf73nt1']:<8}"]
        else:
            hipersocket_detail += ['Offline']
        hipersocket_detail_report.append(hipersocket_detail)
    report_detail1 = []
    report_detail2 = []
    for pid in sorted(report_detail_dict1.keys()):
        report_detail1 += report_detail_dict1[pid]
    for pid in sorted(report_detail_dict2.keys()):
        report_detail2 += report_detail_dict2[pid]
    if len(report_detail2) > 0:
        report += '      Channel Path                     Utilization(%)          Read(MB/Sec)    Write(MB/Sec)       FICON Operations           ZHPF Operations\n'
        report += tb.tabulate(report_detail2, tablefmt='plain',
                              headers=["Id", "Type", "G", "Speed", "Shr", "Part", "Total", "Bus", "Part", "Total",
                                       "Part", "Total", "Rate", "Active", "Defer", "Rate", "Active", "Defer"],
                              floatfmt=('', '', '', '', '', '.2f', '.2f', '.2f', '.2f', '.2f',
                                        '.2f', '.2f', '.2f', '.2f', '.2f', '.2f', '.2f', '.2f')
                              )
        report += '\n\n'
    if len(report_detail1) > 0:
        report += "--------------------------------------------------------------------------------------------------------------------------------------------------------\n" \
                  "                                                    Details For OSA Express\n" \
                  "--------------------------------------------------------------------------------------------------------------------------------------------------------\n"
        report += '      Channel Path                        Utilization(%)        Read(MB/Sec)   Write(MB/Sec)      Physical Network IDs\n'
        report += tb.tabulate(report_detail1, tablefmt='plain',
                              headers=["Id", "Type", "G", "Speed", "Shr", "Part", "Total", "Bus", "Part", "Total",
                                       "Part", "Total", "Port 1", "Port 2"],
                              floatfmt=('', '', '', '', '', '.2f', '.2f', '.2f', '.2f', '.2f',
                                        '.2f', '.2f', '', ''))
        report += '\n'

    if len(hipersocket_detail_report) > 0:
        report += "--------------------------------------------------------------------------------------------------------------------------------------------------------\n" \
                  "                                                    Details For Hipersockets\n" \
                  "--------------------------------------------------------------------------------------------------------------------------------------------------------\n"
        report += '\n      Channel Path             Write(B/Sec)       Message Rate     Message Size      Send Fail    Receive Fail    Physical\n'
        report += tb.tabulate(hipersocket_detail_report, tablefmt='plain',
                              headers=["Id", "Type", "G", "Shr", "Part", "Total",
                                       "Part", "Total", "Part", "Total", "Part",
                                       "Part", "Total", "Network Id"],
                              colalign=('left', 'left', 'center', 'center', 'right', 'right',
                                        'right', 'right', 'right', 'right', 'right',
                                        'right', 'right', 'left'),
                              floatfmt=('', '', '', '', '.0f', '.0f', '.0f', '.0f', '.2f', '.2f', '.2f', '.2f', '.2f',
                                        ''))
    return report


def format_psd_header(pro):
    if 'date' in pro.keys() and 'datetime' in pro.keys():
        report_date = pro['date']
        report_time = pro['datetime'].time().strftime('%H.%M.%S')
        interval = format_s2min(pro['smf75int'])
    elif 'date' in pro.keys():
        report_date = pro['date']
        report_time = '00.00.00'
        interval = format_s2hr(pro['smf75int'])
    else:
        report_date = pro['smf75ist'].date()
        report_time = pro['smf75ist'].time().strftime('%H.%M.%S')
        interval = format_s2min(pro['smf75int'])
    zos_ver = 'V' + pro['smf75mvs'][2:4].lstrip('0') + 'R' + pro['smf75mvs'][4:6].lstrip('0')
    interval_x = f"{interval[:-3]}"
    whitespace = ' '
    header1 = [["                                         P A G E   D A T A  S E T  A C T I V I T Y"]]
    header2 = [
        [f"{whitespace:>12}", f"z/OS {zos_ver}", f"{whitespace:>13}", f"System ID {pro['smf75sid']}", f"{whitespace:>6}",
         f"Date {report_date:%m/%d/%Y}", f"{whitespace:>11}", f"Interval {interval_x}"],
        ["", "", "", f"RMF Version {pro['smf75mfv']:<5}", "", f"Time {report_time}", "",
         f"Cycle {pro['smf75cyc'] / 1000:5.3f} Seconds"]
    ]
    header3 = [
        ["Number of Samples =", f"{pro['smf75sam']:>7}", f"{whitespace:>13}", "Page Data Set And SCM Usage"],
        [" ", " ", " ", "---------------------------"]]
    return (tb.tabulate(header1, tablefmt="plain") + "\n" + tb.tabulate(header2, tablefmt="plain") + "\n\n" +
            tb.tabulate(header3, tablefmt="plain") + "\n")


def format_psd_activity(pro, psds):
    if len(psds) == 0:
        return None
    report = format_psd_header(pro)
    report_detail = []
    for psd in psds:
        detail_line = \
            [f"{'PLPA' if psd['lpa'] else 'COMMON' if psd['com'] else 'LOCAL' if psd['loc'] else 'SCM' if psd['page_space_scm'] else 'UNKNOWN':<7}",
             f"{psd['smf75vol'] if not psd['page_space_scm'] else 'N/A':<6}",
             f"{psd['smf75scs'] if not psd['page_space_scm'] else ''}{psd['smf75cha'] if not psd['page_space_scm'] else 'N/A'}",
             f"{psd['smf75dev'] if not psd['page_space_scm'] else 'N/A':<8}",
             f"{psd['smf75sla']:>7}", f"{psd['smf75mnu']:>7}", f"{psd['smf75mxu']:>7}", f"{psd['smf75avu']:>7}",
             f"{psd['smf75bds']:>7}", f"{psd['psbsy']:>6.2f}",
             f"{psd['psptt'] if pd.notna(psd['psptt']) else 0:>6.3f}", f"{psd['smf75sio']:>7}",
             f"{psd['smf75pgx']:>7}",
             f"{'Y' if psd['ds_accepts_vio'] else ' '}",
             f"{psd['smf75dsn'] if not psd['page_space_scm'] else 'N/A':<44}"]
        report_detail.append(detail_line)

    return report + tb.tabulate(report_detail,
                                headers=["Page\nSpace\nType", "\nVolume\nSerial", "\nDev\nNum", "\nDevice\nType",
                                         "\nSlots\nAlloc", "\n----\nMin", "\nSlots Used\nMax", "\n---\nAvg",
                                         "\nBad\nSlots", "%\nIn\nUse", "Page\nTrans\nTime", "\nNumber\nIO Req",
                                         "\nPages\nXfer'd", "V\nI\nO", "\n\nData Set Name"],
                                colalign=('left', 'left', 'left', 'left', 'right', 'right', 'right', 'right', 'right',
                                          'right',
                                          'right', 'right', 'right', 'center', 'left'),
                                floatfmt=('', '', '', '', '.0f', '.0f', '.0f', '.0f', '.0f', '.2f', '.3f', '.0f', '.0f',
                                          '', ''))


def format_enq_header(pro, ctl):
    if 'date' in pro.keys() and 'datetime' in pro.keys():
        report_date = pro['date']
        report_time = pro['datetime'].time().strftime('%H.%M.%S')
        interval = format_s2min(pro['smf77int'])
    elif 'date' in pro.keys():
        report_date = pro['date']
        report_time = '00.00.00'
        interval = format_s2hr(pro['smf77int'])
    else:
        report_date = pro['smf77ist'].date()
        report_time = pro['smf77ist'].time().strftime('%H.%M.%S')
        interval = format_s2min(pro['smf77int'])
    zos_ver = 'V' + pro['smf77mvs'][2:4].lstrip('0') + 'R' + pro['smf77mvs'][4:6].lstrip('0')
    interval_x = f"{interval[:-3]}"
    whitespace = ' '
    header1 = [["                                                  E N Q U E U E   A C T I V I T Y"]]
    header2 = [
        [f"{whitespace:>12}", f"z/OS {zos_ver}", f"{whitespace:>13}", f"System ID {ctl['smf77sid']}", f"{whitespace:>6}",
         f"Date {report_date:%m/%d/%Y}", f"{whitespace:>11}", f"Interval {interval_x}"],
        ["", "", "", f"RMF Version {pro['smf77mfv']:<5}", "", f"Time {report_time}", "",
         f"Cycle {pro['smf77cyc'] / 1000:5.3f} Seconds"]
    ]
    header3a = [
        [f"Enqueue Detail Activity             GRS Mode: {'RING' if ctl['grs_ring'] and ctl['grs_mode'] else 'NONE'}"],
        ["-Name-  ----- Contention Time -----  -- Jobs at Maximum Contention--  -%QLen Distribution- Avg Q -Request Type - --- Contention ---"]
    ]
    header3b = [
        [f"Enqueue Summary Activity            GRS Mode: {'RING' if ctl['grs_ring'] and ctl['grs_mode'] else 'NONE'}\n"],
        ["-Name-   ------ Contention Time ------   -- Jobs at Max Contention--  -%QLen Distribution-  Avg Q  ---Request Type --  ---- Contention ----\n"]
    ]
    header4 = [
        [f"Major    Min    Max    Tot    Avg    ----- Own ----- ----- Wait ----    1    2    3    4+  Lngth -Excl-  -Share- Event --Stat Chng-\n"],
        [f" Minor                               Tot     Name    Tot     Name                                Min Max Min Max Total Total %NoDet\n"],
        [f"                                              SysName         SysName\n"],
    ]
    if 'date' not in ctl.keys():
        return (tb.tabulate(header1, tablefmt="plain") + "\n" + tb.tabulate(header2, tablefmt="plain") + "\n" +
                tb.tabulate(header3a, tablefmt="plain") + "\n" + tb.tabulate(header4, tablefmt="plain") + "\n")
    else:
        return (tb.tabulate(header1, tablefmt="plain") + "\n" + tb.tabulate(header2, tablefmt="plain") + "\n" +
                tb.tabulate(header3b, tablefmt="plain") + "\n" + tb.tabulate(header4, tablefmt="plain") + "\n")


def format_enq_activity(pro, ctl, enqs):
    if len(enqs) == 0:
        return None
    report_is_empty = True
    report = None
    for enq in enqs:
        tot_qlen = enq['smf77ql1'] + enq['smf77ql2'] + enq['smf77ql3'] + enq['smf77ql4']

        if report_is_empty:
            report = format_enq_header(pro, ctl)
            report_is_empty = False

        report += f"{enq['smf77qnm']:<8} "
        if 'date' not in ctl.keys():
            if bytearray.fromhex(enq['smf77rnm']).decode('cp500').isprintable():
                rnm = bytearray.fromhex(enq['smf77rnm']).decode('cp500')
            else:
                rnm = "x'" + enq['smf77rnm'] + "'"
            report += (
                f"\n"
                f" {rnm}{'(Systems)' if enq['system_scope'] else ''}{'*' if enq['smf77rln'] > 44 else ''}\n"
                f"        {convert_si(enq['smf77wtm'], 5, 3):>6}{convert_si(enq['smf77wtx'], 5, 3):>6}{convert_si(enq['smf77wtt'], 5, 3):>6}"
                f"{convert_si(enq['smf77wtt'] / enq['smf77evt'], 6, 3) if enq['smf77evt'] > 0 else '0.000':>7}"
                f"     {enq['smf77dow']:>2}   "
                f"{enq['smf77do1']:<8}{'(E)' if enq['exclusive_owner'] else '(S)'}"
            )
            # detail_line1 = [f"{rnm}{'(Systems)' if enq['system_scope'] else ''}{'*' if enq['smf77rln'] > 44 else ''}"]
            detail_line2 = [f"{convert_si(enq['smf77wtm'], 5, 3):>6}",
                            f"{convert_si(enq['smf77wtx'], 5, 3):>6}",
                            f"{convert_si(enq['smf77wtt'], 5, 3):>6}",
                            f"{convert_si(enq['smf77wtt'] / enq['smf77evt'], 6, 3) if enq['smf77evt'] > 0 else '0.000':>7}",
                            f"{enq['smf77dow']:>2}",
                            f"{enq['smf77do1']:<8}{'(E)' if enq['exclusive_owner'] else '(S)'}"]
        else:
            report += (
                f"{convert_si(enq['smf77wtm'], 5, 3):>6} {convert_si(enq['smf77wtx'], 5, 3):>6} {convert_si(enq['smf77wtt'], 5, 3):>6}"
                f" {convert_si(enq['smf77wtt'] / enq['smf77evt'], 6, 3) if enq['smf77evt'] > 0 else '0.000':>7}"
                f"   {convert_si(enq['smf77dow'], 6, 0):>7}         {convert_si(enq['smf77dwr'], 6, 0):>7}"
            )
            detail_line2 = [f"{convert_si(enq['smf77wtm'], 5, 3):>6}",
                            f"{convert_si(enq['smf77wtx'], 5, 3):>6}",
                            f"{convert_si(enq['smf77wtt'], 5, 3):>6}",
                            f"{convert_si(enq['smf77wtt'] / enq['smf77evt'], 6, 3) if enq['smf77evt'] > 0 else '0.000':>7}",
                            f"{convert_si(enq['smf77dow'], 6, 0):>7}",
                            f"{convert_si(enq['smf77dwr'], 6, 0):>7}"]
        if 'date' not in ctl.keys():
            report += f"{enq['smf77dwr']:>2} {enq['smf77dw1']:<8}{'(E)' if enq['job_wait_for_exc_usage'] else '(S)'}"
            detail_line2 += [f"{enq['smf77dwr']:>2}", f"{enq['smf77dw1']:<8}",
                             f"{'(E)' if enq['job_wait_for_exc_usage'] else '(S)'}"]
        else:
            report += "     "
            detail_line2 += ["", ""]
        report += (
            f"  {convert_si(enq['smf77ql1'] * 100 / tot_qlen, 4, 1) if tot_qlen > 0 else '0.0':>4}"
            f" {convert_si(enq['smf77ql2'] * 100 / tot_qlen, 4, 1) if tot_qlen > 0 else '0.0':>4}"
            f" {convert_si(enq['smf77ql3'] * 100 / tot_qlen, 4, 1) if tot_qlen > 0 else '0.0':>4}"
            f" {convert_si(enq['smf77ql4'] * 100 / tot_qlen, 4, 1) if tot_qlen > 0 else '0.0':>4}"
        )
        detail_line2 += [f"{convert_si(enq['smf77ql1'] * 100 / tot_qlen, 4, 1) if tot_qlen > 0 else '0.0':>4}",
                         f"{convert_si(enq['smf77ql2'] * 100 / tot_qlen, 4, 1) if tot_qlen > 0 else '0.0':>4}",
                         f"{convert_si(enq['smf77ql3'] * 100 / tot_qlen, 4, 1) if tot_qlen > 0 else '0.0':>4}",
                         f"{convert_si(enq['smf77ql4'] * 100 / tot_qlen, 4, 1) if tot_qlen > 0 else '0.0':>4}"]
        if 'date' not in ctl.keys():
            report += (
                f" {enq['smf77aql'] / tot_qlen if tot_qlen > 0 else 0:>5.2f}  {enq['smf77exm']:>3} {enq['smf77exx']:>3} {enq['smf77shm']:>3} {enq['smf77shx']:>3} "
                f"{enq['smf77evt']:>5} {enq['smf77csc']:>5} {enq['smf77nod'] * 100 / enq['smf77csc'] if enq['smf77csc'] > 0 else 0:>6.3f}\n"
            )
            detail_line2 += [f"{enq['smf77aql'] / tot_qlen if tot_qlen > 0 else 0:>5.2f}",
                             f"{enq['smf77exm']:>3}", f"{enq['smf77exx']:>3}", f"{enq['smf77shm']:>3}",
                             f"{enq['smf77shx']:>3}",
                             f"{enq['smf77evt']:>5}", f"{enq['smf77csc']:>5}",
                             f"{enq['smf77nod'] * 100 / enq['smf77csc'] if enq['smf77csc'] > 0 else 0:>6.3f}"]
        else:
            report += (
                f" {convert_si(enq['smf77aql'] / tot_qlen, 6, 2) if tot_qlen > 0 else '0.00':>7} {convert_si(enq['smf77exm'], 4, 0):>4} "
                f"{convert_si(enq['smf77exx'], 4, 0):>4} {convert_si(enq['smf77shm'], 4, 0):>4} {convert_si(enq['smf77shx'], 4, 0):>4} "
                f"{convert_si(enq['smf77evt'], 5, 0):>6} {convert_si(enq['smf77csc'], 6, 0):>7} {enq['smf77nod'] * 100 / enq['smf77csc'] if enq['smf77csc'] > 0 else 0:>6.3f}\n"
            )
            detail_line2 += [f"{convert_si(enq['smf77aql'] / tot_qlen, 6, 2) if tot_qlen > 0 else '0.00':>7}",
                             f"{convert_si(enq['smf77exm'], 4, 0):>4}",
                             f"{convert_si(enq['smf77exx'], 4, 0):>4}",
                             f"{convert_si(enq['smf77shm'], 4, 0):>4}",
                             f"{convert_si(enq['smf77shx'], 4, 0):>4}",
                             f"{convert_si(enq['smf77evt'], 5, 0):>6}",
                             f"{convert_si(enq['smf77csc'], 6, 0):>7}",
                             f"{enq['smf77nod'] * 100 / enq['smf77csc'] if enq['smf77csc'] > 0 else 0:>6.3f}"]
        if 'date' not in ctl.keys():
            detail_line4 = []
            report += f"                                            {enq['smf77sy1']:<4}          {enq['smf77sy3']:<4}\n"
            # detail_line3 = [f"{enq['smf77sy1']:<4}", f"{enq['smf77sy3']:<4}"]
            if enq['smf77dow'] > 1:
                report += (
                    f"                                           {enq['smf77do1']:<8}{'(E)' if enq['exclusive_owner'] else '(S)'}   "
                )
                detail_line4 = [f"{enq['smf77do1']:<8}{'(E)' if enq['exclusive_owner'] else '(S)'}"]
            elif enq['smf77dwr'] > 1:
                report += "                                                         "
                detail_line4 = []
            if enq['smf77dwr'] > 1:
                report += (
                    f"{enq['smf77dw2']:<8}{'(E)' if enq['job_wait_for_2exc_usage'] else '(S)'}"
                )
                detail_line4 += [f"{enq['smf77dw2']:<8}{'(E)' if enq['job_wait_for_2exc_usage'] else '(S)'}"]
            if enq['smf77dow'] > 1 or enq['smf77dwr'] > 1:
                report += "\n"
                if enq['smf77dow'] > 1:
                    report += (
                        f"                                            {enq['smf77sy2']:<4}          "
                    )
                    detail_line5 = [f"{enq['smf77sy2']:<4}"]
                else:
                    report += "                                                          "
                    detail_line5 = []
                if enq['smf77dwr'] > 1:
                    report += f"{enq['smf77sy4']:<4}\n"
                    detail_line5 += [f"{enq['smf77sy4']:<4}"]
                else:
                    report += "\n"
    return report


def format_io_processors(pro, ioq, iops):
    if 'date' in pro.keys() and 'datetime' in pro.keys():
        report_date = pro['date']
        report_time = pro['datetime'].time().strftime('%H.%M.%S')
        interval = format_s2min(pro['smf78int'])
    elif 'date' in pro.keys():
        report_date = pro['date']
        report_time = '00.00.00'
        interval = format_s2hr(pro['smf78int'])
    else:
        report_date = pro['smf78ist'].date()
        report_time = pro['smf78ist'].time().strftime('%H.%M.%S')
        interval = format_s2min(pro['smf78int'])
    zos_ver = 'V' + pro['smf78mvs'][2:4].lstrip('0') + 'R' + pro['smf78mvs'][4:6].lstrip('0')
    interval_x = f"{interval[:-3]}"
    whitespace = ' '
    header1 = [["                                                I/O   Q U E U I N G   A C T I V I T Y"]]
    header2 = [
        [f"{whitespace:>12}", f"z/OS {zos_ver}", f"{whitespace:>13}", f"System ID {ioq['smf78sid']}", f"{whitespace:>6}",
         f"Date {report_date:%m/%d/%Y}", f"{whitespace:>11}", f"Interval {interval_x}"],
        ["", "", "", f"RMF Version {pro['smf78mfv']:<5}", "", f"Time {report_time}", "",
         f"Cycle {pro['smf78cyc'] / 1000:5.3f} Seconds"]
    ]
    header3 = [
        ["Total Samples =", f"{pro['smf78sam']:>5}", " ",
         "IODF =", f"{ioq['r783tsf']:2}", "  ",
         "Cr-Date:", f"{ioq['r783tdy']}", "  ",
         "Cr-Time:", f"{ioq['r783ttm']}", "  ",
         "Act:", f"{'Activate' if ioq['config_changed_since_ipl'] else 'POR':<8}"]
    ]
    if len(iops) == 0:
        return None
    report = (tb.tabulate(header1, tablefmt="plain") + "\n" + tb.tabulate(header2, tablefmt="plain") + "\n" +
              tb.tabulate(header3, tablefmt="plain") + "\n")
    report_detail = []
    if len(iops) > 0:
        report += (
            "---------------------------------------------------------------------------------------------------------------------------------------------------------------\n"
            "                                                              Input/Output Processors\n"
            "---------------------------------------------------------------------------------------------------------------------------------------------------------------\n"
            "       --Initiative Queue--  ---------------- IOP Utilization -------------------- ------ % I/O Requests Retried -------  ---------- Retries / SSCH -----------\n\n"
        )
        if ioq['data_invalid_ch_failure']:
            report += " * Channel Measurement Facility Not Active or Interrupted *\n"
            return report
        elif ioq['diagnose_failed']:
            report += " * Diagnosis Interface Failure *\n"
            return report
        for iop in iops:
            detail_line = [
                f"{iop['r783iqid'][2:]}", f"{iop['iopac']:>9.3f}", f"{iop['iopql']:>6.2f}", f"{iop['iopipb']:>6.2f}",
                f"{iop['iopecb'] if ioq['eadm_compression_aval'] else ' ':{'>6.2f' if ioq['eadm_compression_aval'] else '>6'}}",
                f"{iop['iopscb'] if ioq['scm_aval'] else ' ':{'>6.2f' if ioq['scm_aval'] else '>6'}}",
                f"{iop['iorifs']:>9.3f}", f"{iop['iorpii']:>9.3f}",
                f"{iop['iopalb']:>6.1f}", f"{iop['iopchb']:>5.1f}", f"{iop['iopdpb']:>5.1f}", f"{iop['iopcub']:>5.1f}",
                f"{iop['iopdvb']:>5.1f}",
                f"{iop['ionalb']:>7.2f}", f"{iop['ionchb']:>6.2f}", f"{iop['iondpb']:>6.2f}", f"{iop['ioncub']:>6.2f}",
                f"{iop['iondvb']:>6.2f}"
            ]
            report_detail.append(detail_line)
        report_detail.append(tb.SEPARATING_LINE)
        report_detail.append([
            "SYS", f"{convert_si(ioq['iopac'], 8, 3):>9}", f"{convert_si(ioq['iopql'], 5, 2):>6}",
            f"{ioq['iopipb'] if pd.notna(ioq['iopipb']) else 0:>6.2f}",
            f"{ioq['iopecb'] if ioq['eadm_compression_aval'] and pd.notna(ioq['iopecb']) else ' ':{'>6.2f' if ioq['eadm_compression_aval'] and pd.notna(ioq['iopecb']) else '>6'}}",
            f"{ioq['iopscb'] if ioq['scm_aval'] and pd.notna(ioq['iopscb']) else ' ':{'>6.2f' if ioq['scm_aval'] and pd.notna(ioq['iopscb']) else '>6'}}",
            f"{convert_si(ioq['iorifs'], 8, 3):>9}", f"{convert_si(ioq['iorpii'], 8, 3):>9}",
            f"{ioq['iopalb']:>6.1f}", f"{ioq['iopchb']:>5.1f}", f"{ioq['iopdpb']:>5.1f}", f"{ioq['iopcub']:>5.1f}",
            f"{ioq['iopdvb']:>5.1f}",
            f"{ioq['ionalb']:>7.2f}", f"{ioq['ionchb']:>6.2f}", f"{ioq['iondpb']:>6.2f}", f"{ioq['ioncub']:>6.2f}",
            f"{ioq['iondvb']:>6.2f}"
        ])

    return report + tb.tabulate(report_detail,
                                headers=["IOP\n", "Activity\n  Rate  ", "Avg Q\nLength", "% IOP\nBusy", "% Cmpr\nBusy",
                                         "% SCM\nBusy", "I/O Start\n  Rate  ", "Interrupt\n  Rate  ", "All",
                                         "CP\nBusy", "DP\nBusy", "CU\nBusy", "DV\nBusy", "All", "CP\nBusy", "DP\nBusy",
                                         "CU\nBusy", "DV\nBusy"],
                                colalign=('right', 'right', 'right', 'right', 'right', 'right', 'right', 'right',
                                          'right', 'right',
                                          'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right',),
                                floatfmt=('', '.3f', '.2f', '.2f', '.2f', '.2f', '.3f', '.3f',
                                          '.1f', '.1f', '.1f', '.1f', '.1f',
                                          '.2f', '.2f', '.2f', '.2f', '.2f')) + '\n'


def format_alias_management_groups(pro, ioq, amgs, chaps_list):
    if len(amgs) == 0:
        return None

    if 'date' in pro.keys() and 'datetime' in pro.keys():
        report_date = pro['date']
        report_time = pro['datetime'].time().strftime('%H.%M.%S')
        interval = format_s2min(pro['smf78int'])
    elif 'date' in pro.keys():
        report_date = pro['date']
        report_time = '00.00.00'
        interval = format_s2hr(pro['smf78int'])
    else:
        report_date = pro['smf78ist'].date()
        report_time = pro['smf78ist'].time().strftime('%H.%M.%S')
        interval = format_s2min(pro['smf78int'])
    zos_ver = 'V' + pro['smf78mvs'][2:4].lstrip('0') + 'R' + pro['smf78mvs'][4:6].lstrip('0')
    interval_x = f"{interval[:-3]}"
    whitespace = ' '
    header1 = [["                                                I/O   Q U E U I N G   A C T I V I T Y"]]
    header2 = [
        [f"{whitespace:>12}", f"z/OS {zos_ver}", f"{whitespace:>13}", f"System ID {ioq['smf78sid']}", f"{whitespace:>6}",
         f"Date {report_date:%m/%d/%Y}", f"{whitespace:>11}", f"Interval {interval_x}"],
        ["", "", "", f"RMF Version {pro['smf78mfv']:<5}", "", f"Time {report_time}", "", f"Cycle {pro['smf78cyc'] / 1000:5.3f} Seconds"]
    ]
    header3 = [
        ["Total Samples =", f"{pro['smf78sam']:>5}", " ",
         "IODF =", f"{ioq['r783tsf']:2}", "  ",
         "Cr-Date:", f"{ioq['r783tdy']}", "  ",
         "Cr-Time:", f"{ioq['r783ttm']}", "  ",
         "Act:", f"{'Activate' if ioq['config_changed_since_ipl'] else 'POR':<8}"]
    ]
    report = (#tb.tabulate(header1, tablefmt="plain") + "\n" + tb.tabulate(header2, tablefmt="plain") + "\n" +
              #tb.tabulate(header3, tablefmt="plain") +
              "\n--------------------------------------------------------------------------------------------------------------------------------------------\n"
              "                                                     Alias Management Groups\n"
              "--------------------------------------------------------------------------------------------------------------------------------------------\n")
    report_detail = []
    if ioq['data_invalid_ch_failure']:
        report += " * Channel Measurement Facility Not Active or Interrupted *\n"
        return report
    elif ioq['diagnose_failed']:
        report += " * Diagnosis Interface Failure *\n"
        return report
    for idx_1, amg in enumerate(amgs):
        previous_amg = None
        for chap in chaps_list[idx_1]:
            if chap['r783amgs'] != previous_amg:
                amg_str = chap['r783amgs']
                previous_amg = amg_str
            else:
                amg_str = ' '
            if chap['ch_path_dcm']:
                detail_line = [f"{amg_str:<8}", f"{chap['r783mcmn']:>3}", f"{chap['r783mcmx']:>3}", f"{chap['r783mcdf']:>3}"]

            else:
                detail_line = [f"{amg_str:<8}", "", "", ""]

            detail_line += [f"{chap['r783cpid']:2}", f"{chap['ioart']:>9.3f}", f"{chap['iodpb']:>6.2f}", f"{chap['iocub']:>6.2f}",
                            f"{chap['iocbt']:>5.1f}", f"{chap['iocmr']:>5.1f}"]
            report_detail.append(detail_line)
        report_detail.append(tb.SEPARATING_LINE)
        report_detail.append([
            "", "", "", "", "*", f"{amg['ioart']:>9.3f}", f"{amg['iodpb']:>6.2f}", f"{amg['iocub']:>6.2f}", f"{amg['iocbt']:>5.1f}",
            f"{amg['iocmr']:>5.1f}",
            f"{amg['ioctr']:>9.3f}", f"{amg['iodlq'] if pd.notna(amg['iodlq']) else 0:>7.2f}", f"{amg['iocss']:>5.1f}",
            f"{amg['iohwait']:>6.3f}", f"{amg['iohmax']:>4.0f}", "", ""
        ])
    return report + tb.tabulate(report_detail,
                                headers=["\nAMG", "\n-DCM\nMin", "\nGroup\nMax", "\n---\nDef", "\nChan\nPaths",
                                         "\nCHPID\nTaken",
                                         "\n% DP\nBusy", "\n% CU\nBusy", "Avg\nCUB\nDly", "Avg\nCmr\nDly",
                                         "\nContention\n  Rate  ",
                                         "Delay\nQ\nLngth", "Avg\nCSS\nDly", "\nHPAV\nWait", "\nHPAV\nMax",
                                         "Avg\nOpen\nExch",
                                         "Data\nXfer\nConc"],
                                colalign=('left', 'right', 'right', 'right', 'left', 'right', 'right', 'right', 'right',
                                          'right',
                                          'right', 'right', 'right', 'right', 'right',),
                                floatfmt=('', '', '', '', '', '.3f', '.2f', '.2f', '.1f', '.1f', '.3f', '.2f', '.1f',
                                          '.3f', '.0f')
                                )


def format_logical_control_units(ioq, pro, lcus, chas_list, amg_list, target_lcu=None):
    if 'date' in pro.keys() and 'datetime' in pro.keys():
        report_date = ioq['date']
        report_time = ioq['datetime'].time().strftime('%H.%M.%S')
        interval = format_s2min(pro['smf78int'])
    elif 'date' in pro.keys():
        report_date = ioq['date']
        report_time = '00.00.00'
        interval = format_s2hr(pro['smf78int'])
    else:
        report_date = ioq['smf78ist'].date()
        report_time = ioq['smf78ist'].time().strftime('%H.%M.%S')
        interval = format_s2min(pro['smf78int'])
    zos_ver = 'V' + pro['smf78mvs'][2:4].lstrip('0') + 'R' + pro['smf78mvs'][4:6].lstrip('0')
    interval_x = f"{interval[:-3]}"
    whitespace = ' '
    header1 = [["                                                I/O   Q U E U I N G   A C T I V I T Y"]]
    header2 = [
        [f"{whitespace:>12}", f"z/OS {zos_ver}", f"{whitespace:>13}", f"System ID {ioq['smf78sid']}", f"{whitespace:>6}",
         f"Date {report_date:%m/%d/%Y}", f"{whitespace:>11}", f"Interval {interval_x}"],
        ["", "", "", f"RMF Version {pro['smf78mfv']:<5}", "", f"Time {report_time}", "", f"Cycle {pro['smf78cyc'] / 1000:5.3f} Seconds"]
    ]
    header3 = [
        ["Total Samples =", f"{pro['smf78sam']:>5}", " ",
         "IODF =", f"{ioq['r783tsf']:2}", "  ",
         "Cr-Date:", f"{ioq['r783tdy']}", "  ",
         "Cr-Time:", f"{ioq['r783ttm']}", "  ",
         "Act:", f"{'Activate' if ioq['config_changed_since_ipl'] else 'POR':<8}"]
    ]
    report = (#tb.tabulate(header1, tablefmt="plain") + "\n" + tb.tabulate(header2, tablefmt="plain") + "\n" +
              #tb.tabulate(header3, tablefmt="plain") +
              "\n--------------------------------------------------------------------------------------------------------------------------------------------------------\n"
              "                                                     Logical Control Units\n"
              "--------------------------------------------------------------------------------------------------------------------------------------------------------\n")
    report_detail = []
    if len(lcus) == 0:
        return None

    path_dict = {0: "NS", 1: "PF", 2: "NP"}
    if ioq['data_invalid_ch_failure']:
        report += " * Channel Measurement Facility Not Active or Interrupted *\n"
        return report
    elif ioq['diagnose_failed']:
        report += " * Diagnosis Interface Failure *\n"
        return report
    report_contains_lcu = False

    for idx_1, lcu in enumerate(lcus):
        if pd.notna(target_lcu) and lcu['r783id2'] != target_lcu:
            continue
        report_contains_lcu = True
        lcu_contains_cha = False
        summary_line = [
            "", "", "", "", "", "*", f"{lcu['ioart'] if pd.notna(lcu['ioart']) else 0:>9.3f}",
            f"{lcu['iodpb'] if pd.notna(lcu['iodpb']) else 0:>6.2f}", f"{lcu['iocub'] if pd.notna(lcu['iocub']) else 0:>6.2f}",
            f"{lcu['iocbt'] if pd.notna(lcu['iocbt']) else 0:>5.1f}", f"{lcu['iocmr'] if pd.notna(lcu['iocmr']) else 0:>5.1f}"
        ]
        if not lcu['no_hw_measurement']:
            summary_line += [f"{lcu['ioctr'] if pd.notna(lcu['ioctr']) else 0:>9.3f}",
                             f"{lcu['iodlq'] if pd.notna(lcu['iodlq']) else 0:>7.2f}"]
        else:
            summary_line += ["* No H/W", "Data *"]
        summary_line += [f"{lcu['iocss'] if pd.notna(lcu['iocss']) else 0:>5.1f}",
                         f"{lcu['iohwait'] if pd.notna(lcu['iohwait']) else 0:>6.3f}",
                         f"{lcu['iohmax'] if pd.notna(lcu['iohmax']) else 0:>4.0f}"]
        if lcu['lcu_has_ficon']:
            summary_line += [f"{(lcu['r783cmrm'] + lcu['r783dctm'] + lcu['r783ddtm']) / lcu['smf78int']:>6.2f}",
                             f"{lcu['r783dctm'] / lcu['smf78int']:>5.2f}"]
        else:
            summary_line += [' ', ' ']
        previous_lcu = None
        previous_amg = None
        for cha in chas_list[idx_1]:
            lcu_contains_cha = True
            if cha['r783id1'] != previous_lcu:
                lcu_id = cha['r783id1']
                cu = lcu['r783cu1']
                previous_lcu = lcu_id
            elif pd.notna(amg_list[idx_1]) and amg_list[idx_1]['r783amgs'] != previous_amg:
                lcu_id = ' ' + amg_list[idx_1]['r783amgs']
                cu = ' '
                previous_amg = amg_list[idx_1]['r783amgs']
            else:
                lcu_id = ' '
                cu = ' '
            if cha['ch_path_dcm']:
                detail_line = [f"{lcu_id:<9}", f"{cu:4}", f"{lcu['r783mcmn']:>3}", f"{lcu['r783mcmx']:>3}",
                               f"{lcu['r783mcdf']:>3}"]
            else:
                detail_line = [f"{lcu_id:<9}", f"{cu:4}", "", "", ""]
            if cha['ch_path_online']:
                detail_line += [
                    f"{cha['r783cpid']:2} {path_dict[cha['r783cpat']] if lcu['path_attr_valid'] else '  '}",
                    f"{cha['ioart'] if pd.notna(cha['ioart']) else '0.000':{'> 8.3f' if pd.notna(cha['ioart']) else '>8'}}",
                    f"{cha['iodpb'] if pd.notna(cha['iodpb']) else '0.00':{'> 6.2f' if pd.notna(cha['iodpb']) else '>6'}}",
                    f"{cha['iocub'] if pd.notna(cha['iocub']) else '0.00':{'> 6.2f' if pd.notna(cha['iocub']) else '>6'}}",
                    f"{cha['iocbt'] if pd.notna(cha['iocbt']) else '0.0':{'> 5.1f' if pd.notna(cha['iocbt']) else '>5'}}",
                    f"{cha['iocmr'] if pd.notna(cha['iocmr']) else '0.0':{'> 5.1f' if pd.notna(cha['iocmr']) else '>5'}}"
                ]
                report_detail.append(detail_line)
            # else:
            #     detail_line += [f"{cha['r783cpid']:2}", "", "", "", "", "", "Path", "Offline"]

        if len(chas_list[idx_1]) == 1 and pd.notna(amg_list[idx_1]):
            detail_line = [f"  {amg_list[idx_1]['r783amgs']:<8}"]
            report_detail.append(detail_line)
        if not lcu_contains_cha:
            report_detail.append(
                [f"{lcu['r783id2']}", "", "", "", "", "", "", "", "", "", "", "* LCU No", "Activity", "*"])

        report_detail += tb.SEPARATING_LINE
        report_detail.append(summary_line)
        report_detail.append([' ', ' '])
    if not report_contains_lcu:
        return None

    return report + tb.tabulate(report_detail,
                                headers=["\nLCU\nAMG", "\nCU", "\n-DCM\nMin", "\nGroup\nMax", "\n---\nDef",
                                         "\nChan\nPaths", "\nCHPID\nTaken",
                                         "\n% DP\nBusy", "\n% CU\nBusy", "Avg\nCUB\nDly", "Avg\nCmr\nDly",
                                         "\nContention\n  Rate  ", "Delay\nQ\nLngth", "Avg\nCSS\nDly",
                                         "\nHPAV\nWait", "\nHPAV\nMax", "Avg\nOpen\nExch", "Data\nXfer\nConc"],
                                colalign=('left', 'left', 'right', 'right', 'right', 'left', 'right', 'right', 'right',
                                          'right', 'right',
                                          'right', 'right', 'right', 'right', 'right', 'right', 'right'),
                                floatfmt=('', '', '', '', '', '', '.3f', '.2f', '.2f', '.1f', '.1f', '.3f', '.2f',
                                          '.1f', '.3f', '.0f', '.2f', '.2f')
                                )


def format_common_storage_detail(comn, pro):
    if 'date' in pro.keys() and 'datetime' in pro.keys():
        report_date = comn['date']
        report_time = comn['datetime'].time().strftime('%H.%M.%S')
        interval = format_s2min(pro['smf78int'])
    elif 'date' in pro.keys():
        report_date = comn['date']
        report_time = '00.00.00'
        interval = format_s2hr(pro['smf78int'])
    else:
        report_date = comn['smf78ist'].date()
        report_time = comn['smf78ist'].time().strftime('%H.%M.%S')
        interval = format_s2min(pro['smf78int'])
    zos_ver = 'V' + pro['smf78mvs'][2:4].lstrip('0') + 'R' + pro['smf78mvs'][4:6].lstrip('0')
    interval_x = f"{interval[:-3]}"
    whitespace = ' '
    header1 = [["                                         V I R T U A L    S T O R A G E    A C T I V I T Y"]]
    header2 = [
        [f"{whitespace:>12}", f"z/OS {zos_ver}", f"{whitespace:>13}", f"System ID {comn['smf78sid']}", f"{whitespace:>6}",
         f"Date {report_date:%m/%d/%Y}", f"{whitespace:>11}", f"Interval {interval_x}"],
        ["", "", "", f"RMF Version {pro['smf78mfv']:<5}", "", f"Time {report_time}", "", f"Cycle {pro['smf78cyc'] / 1000:5.3f} Seconds"]
    ]
    header3 = [
        ["   "],
        ["                                                        Common Storage Detail"],
        ["Allocated CSA BY Subpool By Key (Below 16 Meg)                                  Allocated SQA By Subpool (Below 16M)"]]
    report_detail = [
        ["---", "--------------", "--- Minimum --", "--------------", "--------------"],
        ["0", f"{convert_bi(comn['s227k_vsdbmin_0'], 4, 0, unit='K') if comn['s227k_vsdbmin_0']> 0 else ' ':>5} "
              f"{comn['s227k_vsdbntme_0'].time().strftime('%H.%M.%S') if comn['s227k_vsdbmin_0'] > 0 else '        '}",
         f"{convert_bi(comn['s228k_vsdbmin_0'], 4, 0, unit='K') if comn['s228k_vsdbmin_0'] > 0 else ' ':>5} "
         f"{comn['s228k_vsdbntme_0'].time().strftime('%H.%M.%S') if comn['s228k_vsdbmin_0']> 0 else '        '}",
         f"{convert_bi(comn['s231k_vsdbmin_0'], 4, 0, unit='K') if comn['s231k_vsdbmin_0'] > 0 else ' ':>5} "
         f"{comn['s231k_vsdbntme_0'].time().strftime('%H.%M.%S') if comn['s231k_vsdbmin_0'] > 0 else '        '}",
         f"{convert_bi(comn['s241k_vsdbmin_0'], 4, 0, unit='K') if comn['s241k_vsdbmin_0'] > 0 else ' ':>5} "
         f"{comn['s241k_vsdbntme_0'].time().strftime('%H.%M.%S') if comn['s241k_vsdbmin_0'] > 0 else '        '}",
         "226", f"{convert_bi(comn['s226_vsdbmin'], 4, 0, unit='K'):>5} "
                f"{comn['s226_vsdbntme'].time().strftime('%H.%M.%S') if pd.notna(comn['s226_vsdbntme']) else '        '}",
         f"{convert_bi(comn['s226_vsdbmax'], 4, 0, unit='K'):>5} "
         f"{comn['s226_vsdbxtme'].time().strftime('%H.%M.%S') if pd.notna(comn['s226_vsdbxtme']) else '        '}",
         f"{convert_bi(comn['s226_vsdbtotl'] / pro['smf78sam'], 4, 0, unit='K'):>5}"],
        ["1", f"{convert_bi(comn['s227k_vsdbmin_1'], 4, 0, unit='K') if comn['s227k_vsdbmin_1'] > 0 else ' ':>5} "
              f"{comn['s227k_vsdbntme_1'].time().strftime('%H.%M.%S') if comn['s227k_vsdbmin_1'] > 0 else '        '}",
         f"{convert_bi(comn['s228k_vsdbmin_1'], 4, 0, unit='K') if comn['s228k_vsdbmin_1'] > 0 else ' ':>5} "
         f"{comn['s228k_vsdbntme_1'].time().strftime('%H.%M.%S') if comn['s228k_vsdbmin_1'] > 0 else '        '}",
         f"{convert_bi(comn['s231k_vsdbmin_1'], 4, 0, unit='K') if comn['s231k_vsdbmin_1'] > 0 else ' ':>5} "
         f"{comn['s231k_vsdbntme_1'].time().strftime('%H.%M.%S') if comn['s231k_vsdbmin_1'] > 0 else '        '}",
         f"{convert_bi(comn['s241k_vsdbmin_1'], 4, 0, unit='K') if comn['s241k_vsdbmin_1'] > 0 else ' ':>5} "
         f"{comn['s241k_vsdbntme_1'].time().strftime('%H.%M.%S') if comn['s241k_vsdbmin_1'] > 0 else '        '}",
         "239", f"{convert_bi(comn['s239_vsdbmin'], 4, 0, unit='K'):>5} "
                f"{comn['s239_vsdbntme'].time().strftime('%H.%M.%S') if pd.notna(comn['s239_vsdbntme']) else '        '}",
         f"{convert_bi(comn['s239_vsdbmax'], 4, 0, unit='K'):>5} "
         f"{comn['s239_vsdbxtme'].time().strftime('%H.%M.%S') if pd.notna(comn['s239_vsdbxtme']) else '        '}",
         f"{convert_bi(comn['s239_vsdbtotl'] / pro['smf78sam'], 4, 0, unit='K'):>5}"],
        ["2", f"{convert_bi(comn['s227k_vsdbmin_2'], 4, 0, unit='K') if comn['s227k_vsdbmin_2'] > 0 else ' ':>5} "
              f"{comn['s227k_vsdbntme_2'].time().strftime('%H.%M.%S') if comn['s227k_vsdbmin_2'] > 0 else '        '}",
         f"{convert_bi(comn['s228k_vsdbmin_2'], 4, 0, unit='K') if comn['s228k_vsdbmin_2'] > 0 else ' ':>5} "
         f"{comn['s228k_vsdbntme_2'].time().strftime('%H.%M.%S') if comn['s228k_vsdbmin_2'] > 0 else '        '}",
         f"{convert_bi(comn['s231k_vsdbmin_2'], 4, 0, unit='K') if comn['s231k_vsdbmin_2'] > 0 else ' ':>5} "
         f"{comn['s231k_vsdbntme_2'].time().strftime('%H.%M.%S') if comn['s231k_vsdbmin_2'] > 0 else '        '}",
         f"{convert_bi(comn['s241k_vsdbmin_2'], 4, 0, unit='K') if comn['s241k_vsdbmin_2'] > 0 else ' ':>5} "
         f"{comn['s241k_vsdbntme_2'].time().strftime('%H.%M.%S') if comn['s241k_vsdbmin_2'] > 0 else '        '}",
         "245", f"{convert_bi(comn['s245_vsdbmin'], 4, 0, unit='K'):>5} "
                f"{comn['s245_vsdbntme'].time().strftime('%H.%M.%S') if pd.notna(comn['s245_vsdbntme']) else '        '}",
         f"{convert_bi(comn['s245_vsdbmax'], 4, 0, unit='K'):>5} "
         f"{comn['s245_vsdbxtme'].time().strftime('%H.%M.%S') if pd.notna(comn['s245_vsdbxtme']) else '        '}",
         f" {convert_bi(comn['s245_vsdbtotl'] / pro['smf78sam'], 4, 0, unit='K'):>5}"],
        ["3", f"{convert_bi(comn['s227k_vsdbmin_3'], 4, 0, unit='K') if comn['s227k_vsdbmin_3'] > 0 else ' ':>5} "
              f"{comn['s227k_vsdbntme_3'].time().strftime('%H.%M.%S') if comn['s227k_vsdbmin_3'] > 0 else '        '}",
         f"{convert_bi(comn['s228k_vsdbmin_3'], 4, 0, unit='K') if comn['s228k_vsdbmin_3'] > 0 else ' ':>5} "
         f"{comn['s228k_vsdbntme_3'].time().strftime('%H.%M.%S') if comn['s228k_vsdbmin_3'] > 0 else '        '}",
         f"{convert_bi(comn['s231k_vsdbmin_3'], 4, 0, unit='K') if comn['s231k_vsdbmin_3'] > 0 else ' ':>5} "
         f"{comn['s231k_vsdbntme_3'].time().strftime('%H.%M.%S') if comn['s231k_vsdbmin_3'] > 0 else '        '}",
         f"{convert_bi(comn['s241k_vsdbmin_3'], 4, 0, unit='K') if comn['s241k_vsdbmin_3'] > 0 else ' ':>5} "
         f"{comn['s241k_vsdbntme_3'].time().strftime('%H.%M.%S') if comn['s241k_vsdbmin_3'] > 0 else '        '}"],
        ["4", f"{convert_bi(comn['s227k_vsdbmin_4'], 4, 0, unit='K') if comn['s227k_vsdbmin_4'] > 0 else ' ':>5} "
              f"{comn['s227k_vsdbntme_4'].time().strftime('%H.%M.%S') if comn['s227k_vsdbmin_4'] > 0 else '        '}",
         f"{convert_bi(comn['s228k_vsdbmin_4'], 4, 0, unit='K') if comn['s228k_vsdbmin_4'] > 0 else ' ':>5} "
         f"{comn['s228k_vsdbntme_4'].time().strftime('%H.%M.%S') if comn['s228k_vsdbmin_4'] > 0 else '        '}",
         f"{convert_bi(comn['s231k_vsdbmin_4'], 4, 0, unit='K') if comn['s231k_vsdbmin_4'] > 0 else ' ':>5} "
         f"{comn['s231k_vsdbntme_4'].time().strftime('%H.%M.%S') if comn['s231k_vsdbmin_4'] > 0 else '        '}",
         f"{convert_bi(comn['s241k_vsdbmin_4'], 4, 0, unit='K') if comn['s241k_vsdbmin_4'] > 0 else ' ':>5} "
         f"{comn['s241k_vsdbntme_4'].time().strftime('%H.%M.%S') if comn['s241k_vsdbmin_4'] > 0 else '        '}"],
        ["5", f"{convert_bi(comn['s227k_vsdbmin_5'], 4, 0, unit='K') if comn['s227k_vsdbmin_5'] > 0 else ' ':>5} "
              f"{comn['s227k_vsdbntme_5'].time().strftime('%H.%M.%S') if comn['s227k_vsdbmin_5'] > 0 else '        '}",
         f"{convert_bi(comn['s228k_vsdbmin_5'], 4, 0, unit='K') if comn['s228k_vsdbmin_5'] > 0 else ' ':>5} "
         f"{comn['s228k_vsdbntme_5'].time().strftime('%H.%M.%S') if comn['s228k_vsdbmin_5'] > 0 else '        '}",
         f"{convert_bi(comn['s231k_vsdbmin_5'], 4, 0, unit='K') if comn['s231k_vsdbmin_5'] > 0 else ' ':>5} "
         f"{comn['s231k_vsdbntme_5'].time().strftime('%H.%M.%S') if comn['s231k_vsdbmin_5'] > 0 else '        '}",
         f"{convert_bi(comn['s241k_vsdbmin_5'], 4, 0, unit='K') if comn['s241k_vsdbmin_5'] > 0 else ' ':>5} "
         f"{comn['s241k_vsdbntme_5'].time().strftime('%H.%M.%S') if comn['s241k_vsdbmin_5'] > 0 else '        '}"],
        ["6", f"{convert_bi(comn['s227k_vsdbmin_6'], 4, 0, unit='K') if comn['s227k_vsdbmin_6'] > 0 else ' ':>5} "
              f"{comn['s227k_vsdbntme_6'].time().strftime('%H.%M.%S') if comn['s227k_vsdbmin_6'] > 0 else '        '}",
         f"{convert_bi(comn['s228k_vsdbmin_6'], 4, 0, unit='K') if comn['s228k_vsdbmin_6'] > 0 else ' ':>5} "
         f"{comn['s228k_vsdbntme_6'].time().strftime('%H.%M.%S') if comn['s228k_vsdbmin_6'] > 0 else '        '}",
         f"{convert_bi(comn['s231k_vsdbmin_6'], 4, 0, unit='K') if comn['s231k_vsdbmin_6'] > 0 else ' ':>5} "
         f"{comn['s231k_vsdbntme_6'].time().strftime('%H.%M.%S') if comn['s231k_vsdbmin_6'] > 0 else '        '}",
         f"{convert_bi(comn['s241k_vsdbmin_6'], 4, 0, unit='K') if comn['s241k_vsdbmin_6'] > 0 else ' ':>5} "
         f"{comn['s241k_vsdbntme_6'].time().strftime('%H.%M.%S') if comn['s241k_vsdbmin_6'] > 0 else '        '}"],
        ["7", f"{convert_bi(comn['s227k_vsdbmin_7'], 4, 0, unit='K') if comn['s227k_vsdbmin_7'] > 0 else ' ':>5} "
              f"{comn['s227k_vsdbntme_7'].time().strftime('%H.%M.%S') if comn['s227k_vsdbmin_7'] > 0 else '        '}",
         f"{convert_bi(comn['s228k_vsdbmin_7'], 4, 0, unit='K') if comn['s228k_vsdbmin_7'] > 0 else ' ':>5} "
         f"{comn['s228k_vsdbntme_7'].time().strftime('%H.%M.%S') if comn['s228k_vsdbmin_7'] > 0 else '        '}",
         f"{convert_bi(comn['s231k_vsdbmin_7'], 4, 0, unit='K') if comn['s231k_vsdbmin_7'] > 0 else ' ':>5} "
         f"{comn['s231k_vsdbntme_7'].time().strftime('%H.%M.%S') if comn['s231k_vsdbmin_7'] > 0 else '        '}",
         f"{convert_bi(comn['s241k_vsdbmin_7'], 4, 0, unit='K') if comn['s241k_vsdbmin_7'] > 0 else ' ':>5} "
         f"{comn['s241k_vsdbntme_7'].time().strftime('%H.%M.%S') if comn['s241k_vsdbmin_7'] > 0 else '        '}"],
        ["8-F", f"{convert_bi(comn['s227k_vsdbmin_8'], 4, 0, unit='K') if comn['s227k_vsdbmin_8'] > 0 else ' ':>5} "
                f"{comn['s227k_vsdbntme_8'].time().strftime('%H.%M.%S') if comn['s227k_vsdbmin_8'] > 0 else '        '}",
         f"{convert_bi(comn['s228k_vsdbmin_8'], 4, 0, unit='K') if comn['s228k_vsdbmin_8'] > 0 else ' ':>5} "
         f"{comn['s228k_vsdbntme_8'].time().strftime('%H.%M.%S') if comn['s228k_vsdbmin_8'] > 0 else '        '}",
         f"{convert_bi(comn['s231k_vsdbmin_8'], 4, 0, unit='K') if comn['s231k_vsdbmin_8'] > 0 else ' ':>5} "
         f"{comn['s231k_vsdbntme_8'].time().strftime('%H.%M.%S') if comn['s231k_vsdbmin_8'] > 0 else '        '}",
         f"{convert_bi(comn['s241k_vsdbmin_8'], 4, 0, unit='K') if comn['s241k_vsdbmin_8'] > 0 else ' ':>5} "
         f"{comn['s241k_vsdbntme_8'].time().strftime('%H.%M.%S') if comn['s241k_vsdbmin_8'] > 0 else '        '}"],
        ["All", f"{convert_bi(comn['s227k_vsdbmin_all'], 4, 0, unit='K') if comn['s227k_vsdbmin_all'] > 0 else ' ':>5} "
                f"{comn['s227k_vsdbntme_all'].time().strftime('%H.%M.%S') if comn['s227k_vsdbmin_all'] > 0 else '        '}",
         f"{convert_bi(comn['s228k_vsdbmin_all'], 4, 0, unit='K') if comn['s228k_vsdbmin_all'] > 0 else ' ':>5} "
         f"{comn['s228k_vsdbntme_all'].time().strftime('%H.%M.%S') if comn['s228k_vsdbmin_all'] > 0 else '        '}",
         f"{convert_bi(comn['s231k_vsdbmin_all'], 4, 0, unit='K') if comn['s231k_vsdbmin_all'] > 0 else ' ':>5} "
         f"{comn['s231k_vsdbntme_all'].time().strftime('%H.%M.%S') if comn['s231k_vsdbmin_all'] > 0 else '        '}",
         f"{convert_bi(comn['s241k_vsdbmin_all'], 4, 0, unit='K') if comn['s241k_vsdbmin_all'] > 0 else ' ':>5} "
         f"{comn['s241k_vsdbntme_all'].time().strftime('%H.%M.%S') if comn['s241k_vsdbmin_all'] > 0 else '        '}"],
        ["---", "--------------", "--- Maximum --", "--------------", "--------------"],
        ["0", f"{convert_bi(comn['s227k_vsdbmax_0'], 4, 0, unit='K') if comn['s227k_vsdbmax_0'] > 0 else ' ':>5} "
              f"{comn['s227k_vsdbxtme_0'].time().strftime('%H.%M.%S') if comn['s227k_vsdbmax_0'] > 0 else '        '}",
         f"{convert_bi(comn['s228k_vsdbmax_0'], 4, 0, unit='K') if comn['s228k_vsdbmax_0'] > 0 else ' ':>5} "
         f"{comn['s228k_vsdbxtme_0'].time().strftime('%H.%M.%S') if comn['s228k_vsdbmax_0'] > 0 else '        '}",
         f"{convert_bi(comn['s231k_vsdbmax_0'], 4, 0, unit='K') if comn['s231k_vsdbmax_0'] > 0 else ' ':>5} "
         f"{comn['s231k_vsdbxtme_0'].time().strftime('%H.%M.%S') if comn['s231k_vsdbmax_0'] > 0 else '        '}",
         f"{convert_bi(comn['s241k_vsdbmax_0'], 4, 0, unit='K') if comn['s241k_vsdbmax_0'] > 0 else ' ':>5} "
         f"{comn['s241k_vsdbxtme_0'].time().strftime('%H.%M.%S') if comn['s241k_vsdbmax_0'] > 0 else '        '}"],
        ["1", f"{convert_bi(comn['s227k_vsdbmax_1'], 4, 0, unit='K') if comn['s227k_vsdbmax_1'] > 0 else ' ':>5} "
              f"{comn['s227k_vsdbxtme_1'].time().strftime('%H.%M.%S') if comn['s227k_vsdbmax_1'] > 0 else '        '}",
         f"{convert_bi(comn['s228k_vsdbmax_1'], 4, 0, unit='K') if comn['s228k_vsdbmax_1'] > 0 else ' ':>5} "
         f"{comn['s228k_vsdbxtme_1'].time().strftime('%H.%M.%S') if comn['s228k_vsdbmax_1'] > 0 else '        '}",
         f"{convert_bi(comn['s231k_vsdbmax_1'], 4, 0, unit='K') if comn['s231k_vsdbmax_1'] > 0 else ' ':>5} "
         f"{comn['s231k_vsdbxtme_1'].time().strftime('%H.%M.%S') if comn['s231k_vsdbmax_1'] > 0 else '        '}",
         f"{convert_bi(comn['s241k_vsdbmax_1'], 4, 0, unit='K') if comn['s241k_vsdbmax_1'] > 0 else ' ':>5} "
         f"{comn['s241k_vsdbxtme_1'].time().strftime('%H.%M.%S') if comn['s241k_vsdbmax_1'] > 0 else '        '}"],
        ["2", f"{convert_bi(comn['s227k_vsdbmax_2'], 4, 0, unit='K') if comn['s227k_vsdbmax_2'] > 0 else ' ':>5} "
              f"{comn['s227k_vsdbxtme_2'].time().strftime('%H.%M.%S') if comn['s227k_vsdbmax_2'] > 0 else '        '}",
         f"{convert_bi(comn['s228k_vsdbmax_2'], 4, 0, unit='K') if comn['s228k_vsdbmax_2'] > 0 else ' ':>5} "
         f"{comn['s228k_vsdbxtme_2'].time().strftime('%H.%M.%S') if comn['s228k_vsdbmax_2'] > 0 else '        '}",
         f"{convert_bi(comn['s231k_vsdbmax_2'], 4, 0, unit='K') if comn['s231k_vsdbmax_2'] > 0 else ' ':>5} "
         f"{comn['s231k_vsdbxtme_2'].time().strftime('%H.%M.%S') if comn['s231k_vsdbmax_2'] > 0 else '        '}",
         f"{convert_bi(comn['s241k_vsdbmax_2'], 4, 0, unit='K') if comn['s241k_vsdbmax_2'] > 0 else ' ':>5} "
         f"{comn['s241k_vsdbxtme_2'].time().strftime('%H.%M.%S') if comn['s241k_vsdbmax_2'] > 0 else '        '}"],
        ["3", f"{convert_bi(comn['s227k_vsdbmax_3'], 4, 0, unit='K') if comn['s227k_vsdbmax_3'] > 0 else ' ':>5} "
              f"{comn['s227k_vsdbxtme_3'].time().strftime('%H.%M.%S') if comn['s227k_vsdbmax_3'] > 0 else '        '}",
         f"{convert_bi(comn['s228k_vsdbmax_3'], 4, 0, unit='K') if comn['s228k_vsdbmax_3'] > 0 else ' ':>5} "
         f"{comn['s228k_vsdbxtme_3'].time().strftime('%H.%M.%S') if comn['s228k_vsdbmax_3'] > 0 else '        '}",
         f"{convert_bi(comn['s231k_vsdbmax_3'], 4, 0, unit='K') if comn['s231k_vsdbmax_3'] > 0 else ' ':>5} "
         f"{comn['s231k_vsdbxtme_3'].time().strftime('%H.%M.%S') if comn['s231k_vsdbmax_3'] > 0 else '        '}",
         f"{convert_bi(comn['s241k_vsdbmax_3'], 4, 0, unit='K') if comn['s241k_vsdbmax_3'] > 0 else ' ':>5} "
         f"{comn['s241k_vsdbxtme_3'].time().strftime('%H.%M.%S') if comn['s241k_vsdbmax_3'] > 0 else '        '}"],
        ["4", f"{convert_bi(comn['s227k_vsdbmax_4'], 4, 0, unit='K') if comn['s227k_vsdbmax_4'] > 0 else ' ':>5} "
              f"{comn['s227k_vsdbxtme_4'].time().strftime('%H.%M.%S') if comn['s227k_vsdbmax_4'] > 0 else '        '}",
         f"{convert_bi(comn['s228k_vsdbmax_4'], 4, 0, unit='K') if comn['s228k_vsdbmax_4'] > 0 else ' ':>5} "
         f"{comn['s228k_vsdbxtme_4'].time().strftime('%H.%M.%S') if comn['s228k_vsdbmax_4'] > 0 else '        '}",
         f"{convert_bi(comn['s231k_vsdbmax_4'], 4, 0, unit='K') if comn['s231k_vsdbmax_4'] > 0 else ' ':>5} "
         f"{comn['s231k_vsdbxtme_4'].time().strftime('%H.%M.%S') if comn['s231k_vsdbmax_4'] > 0 else '        '}",
         f"{convert_bi(comn['s241k_vsdbmax_4'], 4, 0, unit='K') if comn['s241k_vsdbmax_4'] > 0 else ' ':>5} "
         f"{comn['s241k_vsdbxtme_4'].time().strftime('%H.%M.%S') if comn['s241k_vsdbmax_4'] > 0 else '        '}"],
        ["5", f"{convert_bi(comn['s227k_vsdbmax_5'], 4, 0, unit='K') if comn['s227k_vsdbmax_5'] > 0 else ' ':>5} "
              f"{comn['s227k_vsdbxtme_5'].time().strftime('%H.%M.%S') if comn['s227k_vsdbmax_5'] > 0 else '        '}",
         f"{convert_bi(comn['s228k_vsdbmax_5'], 4, 0, unit='K') if comn['s228k_vsdbmax_5'] > 0 else ' ':>5} "
         f"{comn['s228k_vsdbxtme_5'].time().strftime('%H.%M.%S') if comn['s228k_vsdbmax_5'] > 0 else '        '}",
         f"{convert_bi(comn['s231k_vsdbmax_5'], 4, 0, unit='K') if comn['s231k_vsdbmax_5'] > 0 else ' ':>5} "
         f"{comn['s231k_vsdbxtme_5'].time().strftime('%H.%M.%S') if comn['s231k_vsdbmax_5'] > 0 else '        '}",
         f"{convert_bi(comn['s241k_vsdbmax_5'], 4, 0, unit='K') if comn['s241k_vsdbmax_5'] > 0 else ' ':>5} "
         f"{comn['s241k_vsdbxtme_5'].time().strftime('%H.%M.%S') if comn['s241k_vsdbmax_5'] > 0 else '        '}"],
        ["6", f"{convert_bi(comn['s227k_vsdbmax_6'], 4, 0, unit='K') if comn['s227k_vsdbmax_6'] > 0 else ' ':>5} "
              f"{comn['s227k_vsdbxtme_6'].time().strftime('%H.%M.%S') if comn['s227k_vsdbmax_6'] > 0 else '        '}",
         f"{convert_bi(comn['s228k_vsdbmax_6'], 4, 0, unit='K') if comn['s228k_vsdbmax_6'] > 0 else ' ':>5} "
         f"{comn['s228k_vsdbxtme_6'].time().strftime('%H.%M.%S') if comn['s228k_vsdbmax_6'] > 0 else '        '}",
         f"{convert_bi(comn['s231k_vsdbmax_6'], 4, 0, unit='K') if comn['s231k_vsdbmax_6'] > 0 else ' ':>5} "
         f"{comn['s231k_vsdbxtme_6'].time().strftime('%H.%M.%S') if comn['s231k_vsdbmax_6'] > 0 else '        '}",
         f"{convert_bi(comn['s241k_vsdbmax_6'], 4, 0, unit='K') if comn['s241k_vsdbmax_6'] > 0 else ' ':>5} "
         f"{comn['s241k_vsdbxtme_6'].time().strftime('%H.%M.%S') if comn['s241k_vsdbmax_6'] > 0 else '        '}"],
        ["7", f"{convert_bi(comn['s227k_vsdbmax_7'], 4, 0, unit='K') if comn['s227k_vsdbmax_7'] > 0 else ' ':>5} "
              f"{comn['s227k_vsdbxtme_7'].time().strftime('%H.%M.%S') if comn['s227k_vsdbmax_7'] > 0 else '        '}",
         f"{convert_bi(comn['s228k_vsdbmax_7'], 4, 0, unit='K') if comn['s228k_vsdbmax_7'] > 0 else ' ':>5} "
         f"{comn['s228k_vsdbxtme_7'].time().strftime('%H.%M.%S') if comn['s228k_vsdbmax_7'] > 0 else '        '}",
         f"{convert_bi(comn['s231k_vsdbmax_7'], 4, 0, unit='K') if comn['s231k_vsdbmax_7'] > 0 else ' ':>5} "
         f"{comn['s231k_vsdbxtme_7'].time().strftime('%H.%M.%S') if comn['s231k_vsdbmax_7'] > 0 else '        '}",
         f"{convert_bi(comn['s241k_vsdbmax_7'], 4, 0, unit='K') if comn['s241k_vsdbmax_7'] > 0 else ' ':>5} "
         f"{comn['s241k_vsdbxtme_7'].time().strftime('%H.%M.%S') if comn['s241k_vsdbmax_7'] > 0 else '        '}"],
        ["8-F", f"{convert_bi(comn['s227k_vsdbmax_8'], 4, 0, unit='K') if comn['s227k_vsdbmax_8'] > 0 else ' ':>5} "
                f"{comn['s227k_vsdbxtme_8'].time().strftime('%H.%M.%S') if comn['s227k_vsdbmax_8'] > 0 else '        '}",
         f"{convert_bi(comn['s228k_vsdbmax_8'], 4, 0, unit='K') if comn['s228k_vsdbmax_8'] > 0 else ' ':>5} "
         f"{comn['s228k_vsdbxtme_8'].time().strftime('%H.%M.%S') if comn['s228k_vsdbmax_8'] > 0 else '        '}",
         f"{convert_bi(comn['s231k_vsdbmax_8'], 4, 0, unit='K') if comn['s231k_vsdbmax_8'] > 0 else ' ':>5} "
         f"{comn['s231k_vsdbxtme_8'].time().strftime('%H.%M.%S') if comn['s231k_vsdbmax_8'] > 0 else '        '}",
         f"{convert_bi(comn['s241k_vsdbmax_8'], 4, 0, unit='K') if comn['s241k_vsdbmax_8'] > 0 else ' ':>5} "
         f"{comn['s241k_vsdbxtme_8'].time().strftime('%H.%M.%S') if comn['s241k_vsdbmax_8'] > 0 else '        '}"],
        ["All", f"{convert_bi(comn['s227k_vsdbmax_all'], 4, 0, unit='K') if comn['s227k_vsdbmax_all'] > 0 else ' ':>5} "
                f"{comn['s227k_vsdbxtme_all'].time().strftime('%H.%M.%S') if comn['s227k_vsdbmax_all'] > 0 else '        '}",
         f"{convert_bi(comn['s228k_vsdbmax_all'], 4, 0, unit='K') if comn['s228k_vsdbmax_all'] > 0 else ' ':>5} "
         f"{comn['s228k_vsdbxtme_all'].time().strftime('%H.%M.%S') if comn['s228k_vsdbmax_all'] > 0 else '        '}",
         f"{convert_bi(comn['s231k_vsdbmax_all'], 4, 0, unit='K') if comn['s231k_vsdbmax_all'] > 0 else ' ':>5} "
         f"{comn['s231k_vsdbxtme_all'].time().strftime('%H.%M.%S') if comn['s231k_vsdbmax_all'] > 0 else '        '}",
         f"{convert_bi(comn['s241k_vsdbmax_all'], 4, 0, unit='K') if comn['s241k_vsdbmax_all'] > 0 else ' ':>5} "
         f"{comn['s241k_vsdbxtme_all'].time().strftime('%H.%M.%S') if comn['s241k_vsdbmax_all'] > 0 else '        '}"],
        ["---", "--------------", "--- Average ---", "--------------", "--------------"],
        ["0",
         f"{convert_bi(comn['s227k_vsdbtotl_0'] / pro['smf78sam'], 4, 0, unit='K') if comn['s227k_vsdbtotl_0'] > 0 else ' ':>5}         ",
         f"{convert_bi(comn['s228k_vsdbtotl_0'] / pro['smf78sam'], 4, 0, unit='K') if comn['s228k_vsdbtotl_0'] > 0 else ' ':>5}         ",
         f"{convert_bi(comn['s231k_vsdbtotl_0'] / pro['smf78sam'], 4, 0, unit='K') if comn['s231k_vsdbtotl_0'] > 0 else ' ':>5}         ",
         f"{convert_bi(comn['s241k_vsdbtotl_0'] / pro['smf78sam'], 4, 0, unit='K') if comn['s241k_vsdbtotl_0'] > 0 else ' ':>5}         "],
        ["1",
         f"{convert_bi(comn['s227k_vsdbtotl_1'] / pro['smf78sam'], 4, 0, unit='K') if comn['s227k_vsdbtotl_1'] > 0 else ' ':>5}         ",
         f"{convert_bi(comn['s228k_vsdbtotl_1'] / pro['smf78sam'], 4, 0, unit='K') if comn['s228k_vsdbtotl_1'] > 0 else ' ':>5}         ",
         f"{convert_bi(comn['s231k_vsdbtotl_1'] / pro['smf78sam'], 4, 0, unit='K') if comn['s231k_vsdbtotl_1'] > 0 else ' ':>5}         ",
         f"{convert_bi(comn['s241k_vsdbtotl_1'] / pro['smf78sam'], 4, 0, unit='K') if comn['s241k_vsdbtotl_1'] > 0 else ' ':>5}         "],
        ["2",
         f"{convert_bi(comn['s227k_vsdbtotl_2'] / pro['smf78sam'], 4, 0, unit='K') if comn['s227k_vsdbtotl_2'] > 0 else ' ':>5}         ",
         f"{convert_bi(comn['s228k_vsdbtotl_2'] / pro['smf78sam'], 4, 0, unit='K') if comn['s228k_vsdbtotl_2'] > 0 else ' ':>5}         ",
         f"{convert_bi(comn['s231k_vsdbtotl_2'] / pro['smf78sam'], 4, 0, unit='K') if comn['s231k_vsdbtotl_2'] > 0 else ' ':>5}         ",
         f"{convert_bi(comn['s241k_vsdbtotl_2'] / pro['smf78sam'], 4, 0, unit='K') if comn['s241k_vsdbtotl_2'] > 0 else ' ':>5}         "],
        ["3",
         f"{convert_bi(comn['s227k_vsdbtotl_3'] / pro['smf78sam'], 4, 0, unit='K') if comn['s227k_vsdbtotl_3'] > 0 else ' ':>5}         ",
         f"{convert_bi(comn['s228k_vsdbtotl_3'] / pro['smf78sam'], 4, 0, unit='K') if comn['s228k_vsdbtotl_3'] > 0 else ' ':>5}         ",
         f"{convert_bi(comn['s231k_vsdbtotl_3'] / pro['smf78sam'], 4, 0, unit='K') if comn['s231k_vsdbtotl_3'] > 0 else ' ':>5}         ",
         f"{convert_bi(comn['s241k_vsdbtotl_3'] / pro['smf78sam'], 4, 0, unit='K') if comn['s241k_vsdbtotl_3'] > 0 else ' ':>5}         "],
        ["4",
         f"{convert_bi(comn['s227k_vsdbtotl_4'] / pro['smf78sam'], 4, 0, unit='K') if comn['s227k_vsdbtotl_4'] > 0 else ' ':>5}         ",
         f"{convert_bi(comn['s228k_vsdbtotl_4'] / pro['smf78sam'], 4, 0, unit='K') if comn['s228k_vsdbtotl_4'] > 0 else ' ':>5}         ",
         f"{convert_bi(comn['s231k_vsdbtotl_4'] / pro['smf78sam'], 4, 0, unit='K') if comn['s231k_vsdbtotl_4'] > 0 else ' ':>5}         ",
         f"{convert_bi(comn['s241k_vsdbtotl_4'] / pro['smf78sam'], 4, 0, unit='K') if comn['s241k_vsdbtotl_4'] > 0 else ' ':>5}         "],
        ["5",
         f"{convert_bi(comn['s227k_vsdbtotl_5'] / pro['smf78sam'], 4, 0, unit='K') if comn['s227k_vsdbtotl_5'] > 0 else ' ':>5}         ",
         f"{convert_bi(comn['s228k_vsdbtotl_5'] / pro['smf78sam'], 4, 0, unit='K') if comn['s228k_vsdbtotl_5'] > 0 else ' ':>5}         ",
         f"{convert_bi(comn['s231k_vsdbtotl_5'] / pro['smf78sam'], 4, 0, unit='K') if comn['s231k_vsdbtotl_5'] > 0 else ' ':>5}         ",
         f"{convert_bi(comn['s241k_vsdbtotl_5'] / pro['smf78sam'], 4, 0, unit='K') if comn['s241k_vsdbtotl_5'] > 0 else ' ':>5}         "],
        ["6",
         f"{convert_bi(comn['s227k_vsdbtotl_6'] / pro['smf78sam'], 4, 0, unit='K') if comn['s227k_vsdbtotl_6'] > 0 else ' ':>5}         ",
         f"{convert_bi(comn['s228k_vsdbtotl_6'] / pro['smf78sam'], 4, 0, unit='K') if comn['s228k_vsdbtotl_6'] > 0 else ' ':>5}         ",
         f"{convert_bi(comn['s231k_vsdbtotl_6'] / pro['smf78sam'], 4, 0, unit='K') if comn['s231k_vsdbtotl_6'] > 0 else ' ':>5}         ",
         f"{convert_bi(comn['s241k_vsdbtotl_6'] / pro['smf78sam'], 4, 0, unit='K') if comn['s241k_vsdbtotl_6'] > 0 else ' ':>5}         "],
        ["7",
         f"{convert_bi(comn['s227k_vsdbtotl_7'] / pro['smf78sam'], 4, 0, unit='K') if comn['s227k_vsdbtotl_7'] > 0 else ' ':>5}         ",
         f"{convert_bi(comn['s228k_vsdbtotl_7'] / pro['smf78sam'], 4, 0, unit='K') if comn['s228k_vsdbtotl_7'] > 0 else ' ':>5}         ",
         f"{convert_bi(comn['s231k_vsdbtotl_7'] / pro['smf78sam'], 4, 0, unit='K') if comn['s231k_vsdbtotl_7'] > 0 else ' ':>5}         ",
         f"{convert_bi(comn['s241k_vsdbtotl_7'] / pro['smf78sam'], 4, 0, unit='K') if comn['s241k_vsdbtotl_7'] > 0 else ' ':>5}         "],
        ["8-F",
         f"{convert_bi(comn['s227k_vsdbtotl_8'] / pro['smf78sam'], 4, 0, unit='K') if comn['s227k_vsdbtotl_8'] > 0 else ' ':>5}         ",
         f"{convert_bi(comn['s228k_vsdbtotl_8'] / pro['smf78sam'], 4, 0, unit='K') if comn['s228k_vsdbtotl_8'] > 0 else ' ':>5}         ",
         f"{convert_bi(comn['s231k_vsdbtotl_8'] / pro['smf78sam'], 4, 0, unit='K') if comn['s231k_vsdbtotl_8'] > 0 else ' ':>5}         ",
         f"{convert_bi(comn['s241k_vsdbtotl_8'] / pro['smf78sam'], 4, 0, unit='K') if comn['s241k_vsdbtotl_8'] > 0 else ' ':>5}         "],
        ["All",
         f"{convert_bi(comn['s227k_vsdbtotl_all'] / pro['smf78sam'], 4, 0, unit='K') if comn['s227k_vsdbtotl_all'] > 0 else ' ':>5}         ",
         f"{convert_bi(comn['s228k_vsdbtotl_all'] / pro['smf78sam'], 4, 0, unit='K') if comn['s228k_vsdbtotl_all'] > 0 else ' ':>5}         ",
         f"{convert_bi(comn['s231k_vsdbtotl_all'] / pro['smf78sam'], 4, 0, unit='K') if comn['s231k_vsdbtotl_all'] > 0 else ' ':>5}         ",
         f"{convert_bi(comn['s241k_vsdbtotl_all'] / pro['smf78sam'], 4, 0, unit='K') if comn['s241k_vsdbtotl_all'] > 0 else ' ':>5}         "]
    ]
    return (tb.tabulate(header1, tablefmt="plain") + "\n" + tb.tabulate(header2, tablefmt="plain") + "\n" +
            tb.tabulate(header3, tablefmt="plain") + '\n' +
            tb.tabulate(report_detail, tablefmt='plain',
                        headers=["   ", "   Subpool 227\n", "   Subpool 228\n", "   Subpool 231\n", "   Subpool 241\n",
                                 "\nSubpool", "\n   Min", "\n   Max", "\n   Avg"],
                        colalign=('center', 'right', 'right', 'right', 'right', 'center', 'right', 'right', 'right')))


def format_common_storage_summary(comn, pro):
    if 'date' in pro.keys() and 'datetime' in pro.keys():
        report_date = comn['date']
        report_time = comn['datetime'].time().strftime('%H.%M.%S')
        interval = format_s2min(pro['smf78int'])
    elif 'date' in pro.keys():
        report_date = comn['date']
        report_time = '00.00.00'
        interval = format_s2hr(pro['smf78int'])
    else:
        report_date = comn['smf78ist'].date()
        report_time = comn['smf78ist'].time().strftime('%H.%M.%S')
        interval = format_s2min(pro['smf78int'])
    zos_ver = 'V' + pro['smf78mvs'][2:4].lstrip('0') + 'R' + pro['smf78mvs'][4:6].lstrip('0')
    interval_x = f"{interval[:-3]}"
    whitespace = ' '
    header1 = [["                                         V I R T U A L    S T O R A G E    A C T I V I T Y"]]
    header2 = [
        [f"{whitespace:>12}", f"z/OS {zos_ver}", f"{whitespace:>13}", f"System ID {comn['smf78sid']}", f"{whitespace:>6}",
         f"Date {report_date:%m/%d/%Y}", f"{whitespace:>11}", f"Interval {interval_x}"],
        ["", "", "", f"RMF Version {pro['smf78mfv']:<5}", "", f"Time {report_time}", "", f"Cycle {pro['smf78cyc'] / 1000:5.3f} Seconds"]
    ]
    header3 = [
        ["   "],
        ["                                                        Common Storage Summary"],
        [f"Number of Samples    {pro['smf78sam']:>4}"],
        ["      Static Storage Map                                                             Allocated CSA/SQA"]
    ]
    table1 = [
        ["EPVT", f"{comn['r782epa'][:-1].lstrip('0') + comn['r782epa'][-1]:>8}",
         f"{convert_bi(comn['r782eps'], 4, 0, unit='K'):>5}"],
        ["ECSA", f"{comn['r782eca'][:-1].lstrip('0') + comn['r782eca'][-1]:>8}",
         f"{convert_bi(comn['r782ecs'], 4, 0, unit='K'):>5}"],
        ["EMLPA", f"{comn['r782emla'][:-1].lstrip('0') + comn['r782emla'][-1]:>8}",
         f"{convert_bi(comn['r782emls'], 4, 0, unit='K'):>5}"],
        ["EFLPA", f"{comn['r782efla'][:-1].lstrip('0') + comn['r782efla'][-1]:>8}",
         f"{convert_bi(comn['r782efls'], 4, 0, unit='K'):>5}"],
        ["EPLPA", f"{comn['r782elpa'][:-1].lstrip('0') + comn['r782elpa'][-1]:>8}",
         f"{convert_bi(comn['r782elps'], 4, 0, unit='K'):>5}"],
        ["ESQA", f"{comn['r782esa'][:-1].lstrip('0') + comn['r782esa'][-1]:>8}",
         f"{convert_bi(comn['r782ess'], 4, 0, unit='K'):>5}"],
        ["ENUC", f"{comn['r782ena'][:-1].lstrip('0') + comn['r782ena'][-1]:>8}",
         f"{convert_bi(comn['r782ens'], 4, 0, unit='K'):>5}"],
        ["-----", "16 Meg Boundary", "------"],
        ["NUCLEUS", f"{comn['r782na'][:-1].lstrip('0') + comn['r782na'][-1]:>8}",
         f"{convert_bi(comn['r782ns'], 4, 0, unit='K'):>5}"],
        ["SQA", f"{comn['r782sa'][:-1].lstrip('0') + comn['r782sa'][-1]:>8}",
         f"{convert_bi(comn['r782ss'], 4, 0, unit='K'):>5}"],
        ["PLPA", f"{comn['r782pla'][:-1].lstrip('0') + comn['r782pla'][-1]:>8}",
         f"{convert_bi(comn['r782pls'], 4, 0, unit='K'):>5}"],
        ["FLPA", f"{comn['r782fla'][:-1].lstrip('0') + comn['r782fla'][-1]:>8}",
         f"{convert_bi(comn['r782fls'], 4, 0, unit='K'):>5}"],
        ["MLPA", f"{comn['r782mla'][:-1].lstrip('0') + comn['r782mla'][-1]:>8}",
         f"{convert_bi(comn['r782mls'], 4, 0, unit='K'):>5}"],
        ["CSA", f"{comn['r782ca'][:-1].lstrip('0') + comn['r782ca'][-1]:>8}",
         f"{convert_bi(comn['r782cs'], 4, 0, unit='K'):>5}"],
        ["PRIVATE", f"{comn['r782pa'][:-1].lstrip('0') + comn['r782pa'][-1]:>8}",
         f"{convert_bi(comn['r782ps'], 4, 0, unit='K'):>5}"],
        ["PSA", "0", "8K"],["","",""]]
    table2 = [
        ["Min         ", "Max", " ", "Avg", "Min", " ", "Max", " ", "Avg"],
        ["SQA" f"{convert_bi(comn['sqau_vsdbmin'], 4, 0, unit='K'):>5} "
         f"{comn['sqau_vsdbntme'].time().strftime('%H.%M.%S') if pd.notna(comn['sqau_vsdbntme']) else ' '}",
         f"{convert_bi(comn['sqau_vsdbmax'], 4, 0, unit='K'):>5}",
         f"{comn['sqau_vsdbxtme'].time().strftime('%H.%M.%S') if pd.notna(comn['sqau_vsdbxtme']) else ' '}",
         f"{convert_bi(comn['sqau_vsdbtotl'] / pro['smf78sam'], 4, 0, unit='K'):>5}",
         f"{convert_bi(comn['sqau_vsdamin'], 4, 0, unit='K'):>5}",
         f"{comn['sqau_vsdantme'].time().strftime('%H.%M.%S') if pd.notna(comn['sqau_vsdantme']) else ' '}",
         f"{convert_bi(comn['sqau_vsdamax'], 4, 0, unit='K'):>5}",
         f"{comn['sqau_vsdaxtme'].time().strftime('%H.%M.%S') if pd.notna(comn['sqau_vsdaxtme']) else ' '}",
         f"{convert_bi(comn['sqau_vsdatotl'] / pro['smf78sam'], 4, 0, unit='K'):>5}"],
        ["CSA" f"{convert_bi(comn['csau_vsdbmin'], 4, 0, unit='K'):>5} "
         f"{comn['csau_vsdbntme'].time().strftime('%H.%M.%S') if pd.notna(comn['csau_vsdbntme']) else ' '}",
         f"{convert_bi(comn['csau_vsdbmax'], 4, 0, unit='K'):>5}",
         f"{comn['csau_vsdbxtme'].time().strftime('%H.%M.%S') if pd.notna(comn['csau_vsdbxtme']) else ' '}",
         f"{convert_bi(comn['csau_vsdbtotl'] / pro['smf78sam'], 4, 0, unit='K'):>5}",
         f"{convert_bi(comn['csau_vsdamin'], 4, 0, unit='K'):>5}",
         f"{comn['csau_vsdantme'].time().strftime('%H.%M.%S') if pd.notna(comn['csau_vsdantme']) else ' '}",
         f"{convert_bi(comn['csau_vsdamax'], 4, 0, unit='K'):>5}",
         f"{comn['csau_vsdaxtme'].time().strftime('%H.%M.%S') if pd.notna(comn['csau_vsdaxtme']) else ' '}",
         f"{convert_bi(comn['csau_vsdatotl'] / pro['smf78sam'], 4, 0, unit='K'):>5}"],
        [" "],
        ["Allocated CSA By Key"],
        [" 0 " f"{convert_bi(comn['csak_vsdbmin_0'], 4, 0, unit='K'):>5} "
         f"{comn['csak_vsdbntme_0'].time().strftime('%H.%M.%S') if pd.notna(comn['csak_vsdbntme_0']) else ' '}",
         f"{convert_bi(comn['csak_vsdbmax_0'], 4, 0, unit='K'):>5}",
         f"{comn['csak_vsdbxtme_0'].time().strftime('%H.%M.%S') if pd.notna(comn['csak_vsdbxtme_0']) else ' '}",
         f"{convert_bi(comn['csak_vsdbtotl_0'] / pro['smf78sam'], 4, 0, unit='K'):>5}",
         f"{convert_bi(comn['csak_vsdamin_0'], 4, 0, unit='K'):>5}",
         f"{comn['csak_vsdantme_0'].time().strftime('%H.%M.%S') if pd.notna(comn['csak_vsdantme_0']) else ' '}",
         f"{convert_bi(comn['csak_vsdamax_0'], 4, 0, unit='K'):>5}",
         f"{comn['csak_vsdaxtme_0'].time().strftime('%H.%M.%S') if pd.notna(comn['csak_vsdaxtme_0']) else ' '}",
         f"{convert_bi(comn['csak_vsdatotl_0'] / pro['smf78sam'], 4, 0, unit='K'):>5}"],
        [" 1 " f"{convert_bi(comn['csak_vsdbmin_1'], 4, 0, unit='K'):>5} "
         f"{comn['csak_vsdbntme_1'].time().strftime('%H.%M.%S') if pd.notna(comn['csak_vsdbntme_1']) else ' '}",
         f"{convert_bi(comn['csak_vsdbmax_1'], 4, 0, unit='K'):>5}",
         f"{comn['csak_vsdbxtme_1'].time().strftime('%H.%M.%S') if pd.notna(comn['csak_vsdbxtme_1']) else ' '}",
         f"{convert_bi(comn['csak_vsdbtotl_1'] / pro['smf78sam'], 4, 0, unit='K'):>5}",
         f"{convert_bi(comn['csak_vsdamin_1'], 4, 0, unit='K'):>5}",
         f"{comn['csak_vsdantme_1'].time().strftime('%H.%M.%S') if pd.notna(comn['csak_vsdantme_1']) else ' '}",
         f"{convert_bi(comn['csak_vsdamax_1'], 4, 0, unit='K'):>5}",
         f"{comn['csak_vsdaxtme_1'].time().strftime('%H.%M.%S') if pd.notna(comn['csak_vsdaxtme_1']) else ' '}",
         f"{convert_bi(comn['csak_vsdatotl_1'] / pro['smf78sam'], 4, 0, unit='K'):>5}"],
        [" 2 " f"{convert_bi(comn['csak_vsdbmin_2'], 4, 0, unit='K'):>5} "
         f"{comn['csak_vsdbntme_2'].time().strftime('%H.%M.%S') if pd.notna(comn['csak_vsdbntme_2']) else ' '}",
         f"{convert_bi(comn['csak_vsdbmax_2'], 4, 0, unit='K'):>5}",
         f"{comn['csak_vsdbxtme_2'].time().strftime('%H.%M.%S') if pd.notna(comn['csak_vsdbxtme_2']) else ' '}",
         f"{convert_bi(comn['csak_vsdbtotl_2'] / pro['smf78sam'], 4, 0, unit='K'):>5}",
         f"{convert_bi(comn['csak_vsdamin_2'], 4, 0, unit='K'):>5}",
         f"{comn['csak_vsdantme_2'].time().strftime('%H.%M.%S') if pd.notna(comn['csak_vsdantme_2']) else ' '}",
         f"{convert_bi(comn['csak_vsdamax_2'], 4, 0, unit='K'):>5}",
         f"{comn['csak_vsdaxtme_2'].time().strftime('%H.%M.%S') if pd.notna(comn['csak_vsdaxtme_2']) else ' '}",
         f"{convert_bi(comn['csak_vsdatotl_2'] / pro['smf78sam'], 4, 0, unit='K'):>5}"],
        [" 3 " f"{convert_bi(comn['csak_vsdbmin_3'], 4, 0, unit='K'):>5} "
         f"{comn['csak_vsdbntme_3'].time().strftime('%H.%M.%S') if pd.notna(comn['csak_vsdbntme_3']) else ' '}",
         f"{convert_bi(comn['csak_vsdbmax_3'], 4, 0, unit='K'):>5}",
         f"{comn['csak_vsdbxtme_3'].time().strftime('%H.%M.%S') if pd.notna(comn['csak_vsdbxtme_3']) else ' '}",
         f"{convert_bi(comn['csak_vsdbtotl_3'] / pro['smf78sam'], 4, 0, unit='K'):>5}",
         f"{convert_bi(comn['csak_vsdamin_3'], 4, 0, unit='K'):>5}",
         f"{comn['csak_vsdantme_3'].time().strftime('%H.%M.%S') if pd.notna(comn['csak_vsdantme_3']) else ' '}",
         f"{convert_bi(comn['csak_vsdamax_3'], 4, 0, unit='K'):>5}",
         f"{comn['csak_vsdaxtme_3'].time().strftime('%H.%M.%S') if pd.notna(comn['csak_vsdaxtme_3']) else ' '}",
         f"{convert_bi(comn['csak_vsdatotl_3'] / pro['smf78sam'], 4, 0, unit='K'):>5}"],
        [" 4 " f"{convert_bi(comn['csak_vsdbmin_4'], 4, 0, unit='K'):>5} "
         f"{comn['csak_vsdbntme_4'].time().strftime('%H.%M.%S') if pd.notna(comn['csak_vsdbntme_4']) else ' '}",
         f"{convert_bi(comn['csak_vsdbmax_4'], 4, 0, unit='K'):>5}",
         f"{comn['csak_vsdbxtme_0'].time().strftime('%H.%M.%S') if pd.notna(comn['csak_vsdbxtme_4']) else ' '}",
         f"{convert_bi(comn['csak_vsdbtotl_4'] / pro['smf78sam'], 4, 0, unit='K'):>5}",
         f"{convert_bi(comn['csak_vsdamin_4'], 4, 0, unit='K'):>5}",
         f"{comn['csak_vsdantme_4'].time().strftime('%H.%M.%S') if pd.notna(comn['csak_vsdantme_4']) else ' '}",
         f"{convert_bi(comn['csak_vsdamax_4'], 4, 0, unit='K'):>5}",
         f"{comn['csak_vsdaxtme_4'].time().strftime('%H.%M.%S') if pd.notna(comn['csak_vsdaxtme_4']) else ' '}",
         f"{convert_bi(comn['csak_vsdatotl_4'] / pro['smf78sam'], 4, 0, unit='K'):>5}"],
        [" 5 " f"{convert_bi(comn['csak_vsdbmin_5'], 4, 0, unit='K'):>5} "
         f"{comn['csak_vsdbntme_5'].time().strftime('%H.%M.%S') if pd.notna(comn['csak_vsdbntme_5']) else ' '}",
         f"{convert_bi(comn['csak_vsdbmax_5'], 4, 0, unit='K'):>5}",
         f"{comn['csak_vsdbxtme_5'].time().strftime('%H.%M.%S') if pd.notna(comn['csak_vsdbxtme_5']) else ' '}",
         f"{convert_bi(comn['csak_vsdbtotl_5'] / pro['smf78sam'], 4, 0, unit='K'):>5}",
         f"{convert_bi(comn['csak_vsdamin_5'], 4, 0, unit='K'):>5}",
         f"{comn['csak_vsdantme_5'].time().strftime('%H.%M.%S') if pd.notna(comn['csak_vsdantme_5']) else ' '}",
         f"{convert_bi(comn['csak_vsdamax_5'], 4, 0, unit='K'):>5}",
         f"{comn['csak_vsdaxtme_5'].time().strftime('%H.%M.%S') if pd.notna(comn['csak_vsdaxtme_5']) else ' '}",
         f"{convert_bi(comn['csak_vsdatotl_5'] / pro['smf78sam'], 4, 0, unit='K'):>5}"],
        [" 6 " f"{convert_bi(comn['csak_vsdbmin_6'], 4, 0, unit='K'):>5} "
         f"{comn['csak_vsdbntme_6'].time().strftime('%H.%M.%S') if pd.notna(comn['csak_vsdbntme_6']) else ' '}",
         f"{convert_bi(comn['csak_vsdbmax_6'], 4, 0, unit='K'):>5}",
         f"{comn['csak_vsdbxtme_6'].time().strftime('%H.%M.%S') if pd.notna(comn['csak_vsdbxtme_6']) else ' '}",
         f"{convert_bi(comn['csak_vsdbtotl_6'] / pro['smf78sam'], 4, 0, unit='K'):>5}",
         f"{convert_bi(comn['csak_vsdamin_6'], 4, 0, unit='K'):>5}",
         f"{comn['csak_vsdantme_6'].time().strftime('%H.%M.%S') if pd.notna(comn['csak_vsdantme_6']) else ' '}",
         f"{convert_bi(comn['csak_vsdamax_6'], 4, 0, unit='K'):>5}",
         f"{comn['csak_vsdaxtme_6'].time().strftime('%H.%M.%S') if pd.notna(comn['csak_vsdaxtme_6']) else ' '}",
         f"{convert_bi(comn['csak_vsdatotl_6'] / pro['smf78sam'], 4, 0, unit='K'):>5}"],
        [" 7 " f"{convert_bi(comn['csak_vsdbmin_7'], 4, 0, unit='K'):>5} "
         f"{comn['csak_vsdbntme_7'].time().strftime('%H.%M.%S') if pd.notna(comn['csak_vsdbntme_7']) else ' '}",
         f"{convert_bi(comn['csak_vsdbmax_7'], 4, 0, unit='K'):>5}",
         f"{comn['csak_vsdbxtme_7'].time().strftime('%H.%M.%S') if pd.notna(comn['csak_vsdbxtme_7']) else ' '}",
         f"{convert_bi(comn['csak_vsdbtotl_7'] / pro['smf78sam'], 4, 0, unit='K'):>5}",
         f"{convert_bi(comn['csak_vsdamin_7'], 4, 0, unit='K'):>5}",
         f"{comn['csak_vsdantme_7'].time().strftime('%H.%M.%S') if pd.notna(comn['csak_vsdantme_7']) else ' '}",
         f"{convert_bi(comn['csak_vsdamax_7'], 4, 0, unit='K'):>5}",
         f"{comn['csak_vsdaxtme_7'].time().strftime('%H.%M.%S') if pd.notna(comn['csak_vsdaxtme_7']) else ' '}",
         f"{convert_bi(comn['csak_vsdatotl_7'] / pro['smf78sam'], 4, 0, unit='K'):>5}"],
        ["8-F" f"{convert_bi(comn['csak_vsdbmin_8'], 4, 0, unit='K'):>5} "
         f"{comn['csak_vsdbntme_8'].time().strftime('%H.%M.%S') if pd.notna(comn['csak_vsdbntme_8']) else ' '}",
         f"{convert_bi(comn['csak_vsdbmax_8'], 4, 0, unit='K'):>5}",
         f"{comn['csak_vsdbxtme_8'].time().strftime('%H.%M.%S') if pd.notna(comn['csak_vsdbxtme_8']) else ' '}",
         f"{convert_bi(comn['csak_vsdbtotl_8'] / pro['smf78sam'], 4, 0, unit='K'):>5}",
         f"{convert_bi(comn['csak_vsdamin_8'], 4, 0, unit='K'):>5}",
         f"{comn['csak_vsdantme_8'].time().strftime('%H.%M.%S') if pd.notna(comn['csak_vsdantme_8']) else ' '}",
         f"{convert_bi(comn['csak_vsdamax_8'], 4, 0, unit='K'):>5}",
         f"{comn['csak_vsdaxtme_8'].time().strftime('%H.%M.%S') if pd.notna(comn['csak_vsdaxtme_8']) else ' '}",
         f"{convert_bi(comn['csak_vsdatotl_8'] / pro['smf78sam'], 4, 0, unit='K'):>5}"],
        [" "],
        ["SQA Expansion into CSA"],
        ["   " f"{convert_bi(comn['sqex_vsdbmin'], 4, 0, unit='K'):>5} "
         f"{comn['sqex_vsdbntme'].time().strftime('%H.%M.%S') if pd.notna(comn['sqex_vsdbntme']) else ' '}",
         f"{convert_bi(comn['sqex_vsdbmax'], 4, 0, unit='K'):>5}",
         f"{comn['sqex_vsdbxtme'].time().strftime('%H.%M.%S') if pd.notna(comn['sqex_vsdbxtme']) else ' '}",
         f"{convert_bi(comn['sqex_vsdbtotl'] / pro['smf78sam'], 4, 0, unit='K'):>5}",
         f"{convert_bi(comn['sqex_vsdamin'], 4, 0, unit='K'):>5}",
         f"{comn['sqex_vsdantme'].time().strftime('%H.%M.%S') if pd.notna(comn['sqex_vsdantme']) else ' '}",
         f"{convert_bi(comn['sqex_vsdamax'], 4, 0, unit='K'):>5}",
         f"{comn['sqex_vsdaxtme'].time().strftime('%H.%M.%S') if pd.notna(comn['sqex_vsdaxtme']) else ' '}",
         f"{convert_bi(comn['sqex_vsdatotl'] / pro['smf78sam'], 4, 0, unit='K'):>5}"]
    ]
    table_data = []
    for i in range(0, len(table1)):
        row = [table1[i][0], table1[i][1], table1[i][2]]
        for j in range(0, len(table2[i])):
            row += [table2[i][j]]
        table_data.append(row)
    table3 = [
        ["CSA"],
        [" Free Pages (Bytes)", f"{convert_bi(comn['csaf_vsdbmin'], 4, 0, unit='K'):>5}",
         f"{comn['csaf_vsdbntme'].time().strftime('%H.%M.%S') if pd.notna(comn['csaf_vsdbntme']) else ' '}",
         f"{convert_bi(comn['csaf_vsdbmax'], 4, 0, unit='K'):>5}",
         f"{comn['csaf_vsdbxtme'].time().strftime('%H.%M.%S') if pd.notna(comn['csaf_vsdaxtme']) else ' '}",
         f"{convert_bi(comn['csaf_vsdbtotl'] / pro['smf78sam'], 4, 0, unit='K'):>5}",
         f"{convert_bi(comn['csaf_vsdamin'], 4, 0, unit='K'):>5}",
         f"{comn['csaf_vsdantme'].time().strftime('%H.%M.%S') if pd.notna(comn['csaf_vsdantme']) else ' '}",
         f"{convert_bi(comn['csaf_vsdamax'], 4, 0, unit='K'):>5}",
         f"{comn['csaf_vsdaxtme'].time().strftime('%H.%M.%S') if pd.notna(comn['csaf_vsdaxtme']) else ' '}",
         f"{convert_bi(comn['csaf_vsdatotl'] / pro['smf78sam'], 4, 0, unit='K'):>5}"],
        [" Largest Free Block", f"{convert_bi(comn['cslf_vsdbmin'], 4, 0, unit='K'):>5}",
         f"{comn['cslf_vsdbntme'].time().strftime('%H.%M.%S') if pd.notna(comn['cslf_vsdbntme']) else ' '}",
         f"{convert_bi(comn['cslf_vsdbmax'], 4, 0, unit='K'):>5}",
         f"{comn['cslf_vsdbxtme'].time().strftime('%H.%M.%S') if pd.notna(comn['cslf_vsdbxtme']) else ' '}",
         f"{convert_bi(comn['cslf_vsdbtotl'] / pro['smf78sam'], 4, 0, unit='K'):>5}",
         f"{convert_bi(comn['cslf_vsdamin'], 4, 0, unit='K'):>5}",
         f"{comn['cslf_vsdantme'].time().strftime('%H.%M.%S') if pd.notna(comn['cslf_vsdantme']) else ' '}",
         f"{convert_bi(comn['cslf_vsdamax'], 4, 0, unit='K'):>5}",
         f"{comn['cslf_vsdaxtme'].time().strftime('%H.%M.%S') if pd.notna(comn['cslf_vsdaxtme']) else ' '}",
         f"{convert_bi(comn['cslf_vsdatotl'] / pro['smf78sam'], 4, 0, unit='K'):>5}"],
        [" Allocated Area Size", f"{convert_bi(comn['csal_vsdbmin'], 4, 0, unit='K'):>5}",
         f"{comn['csal_vsdbntme'].time().strftime('%H.%M.%S') if pd.notna(comn['csal_vsdbntme']) else ' '}",
         f"{convert_bi(comn['csal_vsdbmax'], 4, 0, unit='K'):>5}",
         f"{comn['csal_vsdbxtme'].time().strftime('%H.%M.%S') if pd.notna(comn['csal_vsdbxtme']) else ' '}",
         f"{convert_bi(comn['csal_vsdbtotl'] / pro['smf78sam'], 4, 0, unit='K'):>5}",
         f"{convert_bi(comn['csal_vsdamin'], 4, 0, unit='K'):>5}",
         f"{comn['csal_vsdantme'].time().strftime('%H.%M.%S') if pd.notna(comn['csal_vsdantme']) else ' '}",
         f"{convert_bi(comn['csal_vsdamax'], 4, 0, unit='K'):>5}",
         f"{comn['csal_vsdaxtme'].time().strftime('%H.%M.%S') if pd.notna(comn['csal_vsdaxtme']) else ' '}",
         f"{convert_bi(comn['csal_vsdatotl'] / pro['smf78sam'], 4, 0, unit='K'):>5}"],
        ["SQA"],
        [" Free Pages (Bytes)", f"{convert_bi(comn['sqaf_vsdbmin'], 4, 0, unit='K'):>5}",
         f"{comn['sqaf_vsdbntme'].time().strftime('%H.%M.%S') if pd.notna(comn['sqaf_vsdbntme']) else ' '}",
         f"{convert_bi(comn['sqaf_vsdbmax'], 4, 0, unit='K'):>5}",
         f"{comn['sqaf_vsdbxtme'].time().strftime('%H.%M.%S') if pd.notna(comn['sqaf_vsdbxtme']) else ' '}",
         f"{convert_bi(comn['sqaf_vsdbtotl'] / pro['smf78sam'], 4, 0, unit='K'):>5}",
         f"{convert_bi(comn['sqaf_vsdamin'], 4, 0, unit='K'):>5}",
         f"{comn['sqaf_vsdantme'].time().strftime('%H.%M.%S') if pd.notna(comn['sqaf_vsdantme']) else ' '}",
         f"{convert_bi(comn['sqaf_vsdamax'], 4, 0, unit='K'):>5}",
         f"{comn['sqaf_vsdaxtme'].time().strftime('%H.%M.%S') if pd.notna(comn['sqaf_vsdaxtme']) else ' '}",
         f"{convert_bi(comn['sqaf_vsdatotl'] / pro['smf78sam'], 4, 0, unit='K'):>5}"],
        [" Largest Free Block", f"{convert_bi(comn['sqlf_vsdbmin'], 4, 0, unit='K'):>5}",
         f"{comn['sqlf_vsdbntme'].time().strftime('%H.%M.%S') if pd.notna(comn['sqlf_vsdbntme']) else ' '}",
         f"{convert_bi(comn['sqlf_vsdbmax'], 4, 0, unit='K'):>5}",
         f"{comn['sqlf_vsdbxtme'].time().strftime('%H.%M.%S') if pd.notna(comn['sqlf_vsdbxtme']) else ' '}",
         f"{convert_bi(comn['sqlf_vsdbtotl'] / pro['smf78sam'], 4, 0, unit='K'):>5}",
         f"{convert_bi(comn['sqlf_vsdamin'], 4, 0, unit='K'):>5}",
         f"{comn['sqlf_vsdantme'].time().strftime('%H.%M.%S') if pd.notna(comn['sqlf_vsdantme']) else ' '}",
         f"{convert_bi(comn['sqlf_vsdamax'], 4, 0, unit='K'):>5}",
         f"{comn['sqlf_vsdaxtme'].time().strftime('%H.%M.%S') if pd.notna(comn['sqlf_vsdaxtme']) else ' '}",
         f"{convert_bi(comn['sqlf_vsdatotl'] / pro['smf78sam'], 4, 0, unit='K'):>5}"],
        [" Allocated Area Size", f"{convert_bi(comn['sqal_vsdbmin'], 4, 0, unit='K'):>5}",
         f"{comn['sqal_vsdbntme'].time().strftime('%H.%M.%S') if pd.notna(comn['sqal_vsdbntme']) else ' '}",
         f"{convert_bi(comn['sqal_vsdbmax'], 4, 0, unit='K'):>5}",
         f"{comn['sqal_vsdbxtme'].time().strftime('%H.%M.%S') if pd.notna(comn['sqal_vsdbxtme']) else ' '}",
         f"{convert_bi(comn['sqal_vsdbtotl'] / pro['smf78sam'], 4, 0, unit='K'):>5}",
         f"{convert_bi(comn['sqal_vsdamin'], 4, 0, unit='K'):>5}",
         f"{comn['sqal_vsdantme'].time().strftime('%H.%M.%S') if pd.notna(comn['sqal_vsdantme']) else ' '}",
         f"{convert_bi(comn['sqal_vsdamax'], 4, 0, unit='K'):>5}",
         f"{comn['sqal_vsdaxtme'].time().strftime('%H.%M.%S') if pd.notna(comn['sqal_vsdaxtme']) else ' '}",
         f"{convert_bi(comn['sqal_vsdatotl'] / pro['smf78sam'], 4, 0, unit='K'):>5}"],
        ["Maximum Possible User Region", "-", f"{convert_bi(comn['r782mr'], 4, 0, unit='K'):>5}",
         "Below And", f"{convert_bi(comn['r782emr'], 4, 0, unit='K'):>5}", "Above"],
        ["Defined Size Of RUCSA", "-", f"{convert_bi(comn['r782rucs'], 4, 0, unit='K') if comn['r782rucd'] else '  0M':>4}",
         "Below", "And", f"{convert_bi(comn['r782erucs'], 4, 0, unit='K') if comn['r782rucd'] else '   0M':>5}", "Above"]
    ]
    return (tb.tabulate(header1, tablefmt="plain") + "\n" + tb.tabulate(header2, tablefmt="plain") + "\n" +
            tb.tabulate(header3, tablefmt="plain") + '\n' +
            tb.tabulate(table_data, tablefmt='plain',
                        headers=["Area", "Address", "Size", "<-----------", "Below 16M", "--------",
                                 "------>", "<------", "Extended", "(Above", "16M)", "------->"],
                        colalign=('left', 'right', 'right',
                                  'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right',
                                  'right')) + '\n' +
            f"PLPA Intermodule Space              - {convert_bi(comn['r782lpai'], 4, 0, unit='K'):>5} In PLPA And {convert_bi(comn['r782elpi'], 4, 0, unit='K'):>5} In EPLPA\n"
            f"PLPA Space Redundant With MLPA/FLPA - {convert_bi(comn['r782nl'], 4, 0, unit='K'):>5} In PLPA And {convert_bi(comn['r782enl'], 4, 0, unit='K'):>5} In EPLPA\n\n" +
            tb.tabulate(table3, tablefmt='plain',
                        headers=[" ", "<------\nMin", "---Below\n", "16M --\nMax", "--------\n ", "---->\nAvg",
                                 "<------\nMin", "--------\n", "Above\nMax", "16M ---\n", "------>\nAvg"],
                        colalign=('left', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right',
                                  'right', 'right'))
            )


def format_private_storage_detail(pvt, pro, pvsps):
    if not pvt['r782actv']:
        return None

    subpool = {203: "ELSQA", 204: "ELSQA", 205: "ELSQA", 213: "ELSQA", 214: "ELSQA", 215: "ELSQA", 223: "ELSQA",
               224: "ELSQA", 225: "ELSQA",
               226: "SQA", 227: "CSA", 228: "CSA", 231: "CSA", 233: "LSQA", 234: "LSQA",
               236: "SWA", 237: "SWA", 239: "SQA", 241: "CSA", 245: "SQA", 247: "ESQA", 248: "ESQA",
               251: "Modules", 252: "Reentrant", 253: "LSQA", 254: "LSQA", 255: "LSQA"}
    if 'date' in pro.keys() and 'datetime' in pro.keys():
        # report_date = pvt['date']
        # report_time = pvt['datetime'].time().strftime('%H.%M.%S')
        start_time = pvt['datetime']
        end_time = start_time + pd.to_timedelta(pro['smf78int'], unit='s')
        interval = format_s2min(pro['smf78int'])
    elif 'date' in pro.keys():
        # report_date = pvt['date']
        # report_time = '00.00.00'
        start_time = dt.datetime.combine(pvt['date'], dt.time())
        end_time = start_time + pd.to_timedelta(pro['smf78int'], unit='s')
        interval = format_s2hr(pro['smf78int'])
    else:
        # report_date = pvt['smf78ist'].date()
        # report_time = pvt['smf78ist'].time().strftime('%H.%M.%S')
        start_time = pvt['smf78ist']
        end_time = start_time + pd.to_timedelta(pro['smf78int'], unit='s')
        interval = format_s2min(pro['smf78int'])
    zos_ver = 'V' + pro['smf78mvs'][2:4].lstrip('0') + 'R' + pro['smf78mvs'][4:6].lstrip('0')
    interval_x = f"{interval[:-3]}"
    whitespace = ' '
    header1 = [["                                         V I R T U A L    S T O R A G E    A C T I V I T Y"]]
    header2 = [
        [f"{whitespace:>12}", f"z/OS {zos_ver}", f"{whitespace:>13}", f"System ID {pvt['smf78sid']}", f"{whitespace:>6}",
         f"Start {start_time:%m/%d/%Y-%H.%M.%S}", f"{whitespace:>3}", f"Interval {interval_x}"],
        ["", "", "", f"RMF Version {pro['smf78mfv']:<5}", "", f"End   {end_time:%m/%d/%Y-%H.%M.%S}", "",
         f"Cycle {pro['smf78cyc'] / 1000:5.3f} Seconds"]
    ]
    header3 = [
        ["   "],
        ["                                                Private Area Detail"],
    ]
    header4 = [["Job Name -", f"{pvt['r782jobn']:<8}", "    ", "Memory Limit -",
                f"{convert_bi(pvt['r782meml'] * 1024 * 1024, 5, 0, unit='M'):>6}"]]
    header5 = [["Number Of Bytes Of Allocated Blocks By Area (Below 16 Meg)"]]
    subpool_data = []
    user_data = []
    for pvsp in pvsps:
        if pvsp['r782spn'] not in list(range(128)) + [251, 252]:
            subpool_data.append(
                [f"{pvsp['r782spn']:>3} {'(' if pvsp['r782spn'] in subpool.keys() else ' '}{subpool.get(pvsp['r782spn'], '') + ')' if pvsp['r782spn'] in subpool.keys() else '':<10}",
                 f"{convert_bi(pvsp['spd_vsdbmin'], 4, 0, unit='K'):>5}",
                 f"{pvsp['spd_vsdbntme'].time().strftime('%H.%M.%S') if pd.notna(pvsp['spd_vsdbntme']) else ' '}",
                 f"{convert_bi(pvsp['spd_vsdbmax'], 4, 0, unit='K'):>5}",
                 f"{pvsp['spd_vsdbxtme'].time().strftime('%H.%M.%S') if pd.notna(pvsp['spd_vsdbxtme']) else ' '}",
                 f"{convert_bi(pvsp['spd_vsdbtotl'] / pvt['r782samp'], 4, 0, unit='K'):>5}"])
        else:
            user_data.append(
                [f"{pvsp['r782spn']:>3} {'(' if pvsp['r782spn'] in subpool.keys() else ' '}{subpool.get(pvsp['r782spn'], '') + ')' if pvsp['r782spn'] in subpool.keys() else '':<10}",
                 f"{convert_bi(pvsp['spd_vsdbmin'], 4, 0, unit='K'):>5}",
                 f"{pvsp['spd_vsdbntme'].time().strftime('%H.%M.%S') if pd.notna(pvsp['spd_vsdbntme']) else ' '}",
                 f"{convert_bi(pvsp['spd_vsdbmax'], 4, 0, unit='K'):>5}",
                 f"{pvsp['spd_vsdbxtme'].time().strftime('%H.%M.%S') if pd.notna(pvsp['spd_vsdbxtme']) else ' '}",
                 f"{convert_bi(pvsp['spd_vsdbtotl'] / pvt['r782samp'], 4, 0, unit='K'):>5}"])

    subpool_data.append(['User Region'])
    subpool_data += user_data
    memory_data = [
        ["  Private", f"{convert_bi(pvt['toby_vsdgmin'], 5, 2, unit='K'):>6}",
         f"{pvt['toby_vsdgntme'].time().strftime('%H.%M.%S') if pd.notna(pvt['toby_vsdgntme']) else ' '}",
         f"{convert_bi(pvt['toby_vsdgmax'], 5, 2, unit='K'):>6}",
         f"{pvt['toby_vsdgxtme'].time().strftime('%H.%M.%S') if pd.notna(pvt['toby_vsdgxtme']) else ' '}",
         f"{convert_bi(pvt['toby_vsdgtotl'] / pvt['r782samp'], 5, 2, unit='K'):>6}",
         f"{convert_bi(pvt['toby_vsdghwm'], 5, 2, unit='K'):>6}"],
        [f"  Shared", f"{convert_bi(pvt['shby_vsdgmin'], 5, 2, unit='K') if pvt['shby_vsdgmin'] > 0 else 0 :>6}",
         f"{pvt['shby_vsdgntme'].time().strftime('%H.%M.%S') if pd.notna(pvt['shby_vsdgntme']) else ' '}",
         f"{convert_bi(pvt['shby_vsdgmax'], 5, 2, unit='K') if pvt['shby_vsdgmax'] > 0 else 0:>6}",
         f"{pvt['shby_vsdgxtme'].time().strftime('%H.%M.%S') if pd.notna(pvt['shby_vsdgxtme']) else ' '}",
         f"{convert_bi(pvt['shby_vsdgtotl'] / pvt['r782samp'], 5, 2, unit='K') if pvt['shby_vsdgtotl'] > 0 else 0:>6}",
         f"{convert_bi(pvt['shby_vsdghwm'], 5, 2, unit='K') if pvt['shby_vsdghwm'] > 0 else 0:>6}"],
        [f"  Common", f"{convert_bi(pvt['coby_vsdgmin'], 5, 2, unit='K') if pvt['coby_vsdgmin'] > 0 else 0 :>6}",
         f"{pvt['coby_vsdgntme'].time().strftime('%H.%M.%S') if pd.notna(pvt['coby_vsdgntme']) else ' '}",
         f"{convert_bi(pvt['coby_vsdgmax'], 5, 2, unit='K') if pvt['coby_vsdgmax'] > 0 else 0:>6}",
         f"{pvt['coby_vsdgxtme'].time().strftime('%H.%M.%S') if pd.notna(pvt['coby_vsdgxtme']) else ' '}",
         f"{convert_bi(pvt['coby_vsdgtotl'] / pvt['r782samp'], 5, 2, unit='K') if pvt['coby_vsdgtotl'] > 0 else 0:>6}",
         f"{convert_bi(pvt['coby_vsdghwm'], 5, 2, unit='K') if pvt['coby_vsdghwm'] > 0 else 0:>6}"],
        ["Memory Objects"],
        ["  Private", f"{pvt['tomo_vsdcmin']:>6.0f}",
         f"{pvt['tomo_vsdcntme'].time().strftime('%H.%M.%S') if pd.notna(pvt['tomo_vsdcntme']) else ' '}",
         f"{pvt['tomo_vsdcmax']:>6.0f}",
         f"{pvt['tomo_vsdcxtme'].time().strftime('%H.%M.%S') if pd.notna(pvt['tomo_vsdcxtme']) else ' '}",
         f"{pvt['tomo_vsdctotl'] / pvt['r782samp']:>6.0f}"],
        ["  Shared", f"{pvt['shmo_vsdcmin']:>6.0f}",
         f"{pvt['shmo_vsdcntme'].time().strftime('%H.%M.%S') if pd.notna(pvt['shmo_vsdcntme']) else ' '}",
         f"{pvt['shmo_vsdcmax']:>6.0f}",
         f"{pvt['shmo_vsdcxtme'].time().strftime('%H.%M.%S') if pd.notna(pvt['shmo_vsdcxtme']) else ' '}",
         f"{pvt['shmo_vsdctotl'] / pvt['r782samp']:>6.0f}"],
        ["  Common", f"{pvt['como_vsdcmin']:>6.0f}",
         f"{pvt['como_vsdcntme'].time().strftime('%H.%M.%S') if pd.notna(pvt['como_vsdcntme']) else ' '}",
         f"{pvt['como_vsdcmax']:>6.0f}",
         f"{pvt['como_vsdcxtme'].time().strftime('%H.%M.%S') if pd.notna(pvt['como_vsdcxtme']) else ' '}",
         f"{pvt['como_vsdctotl'] / pvt['r782samp']:>6.0f}"],
        ["  Fixed 1 MB", f"{pvt['lgmo_vsdcmin']:>6.0f}",
         f"{pvt['lgmo_vsdcntme'].time().strftime('%H.%M.%S') if pd.notna(pvt['lgmo_vsdcntme']) else ' '}",
         f"{pvt['lgmo_vsdcmax']:>6.0f}",
         f"{pvt['lgmo_vsdcxtme'].time().strftime('%H.%M.%S') if pd.notna(pvt['lgmo_vsdcxtme']) else ' '}",
         f"{pvt['lgmo_vsdctotl'] / pvt['r782samp']:>6.0f}"],
        ["  Fixed 2 GB", f"{pvt['gfmo_vsdcmin']:>6.0f}",
         f"{pvt['gfmo_vsdcntme'].time().strftime('%H.%M.%S') if pd.notna(pvt['gfmo_vsdcntme']) else ' '}",
         f"{pvt['gfmo_vsdcmax']:>6.0f}",
         f"{pvt['gfmo_vsdcxtme'].time().strftime('%H.%M.%S') if pd.notna(pvt['gfmo_vsdcxtme']) else ' '}",
         f"{pvt['gfmo_vsdctotl'] / pvt['r782samp']:>6.0f}"],
        ["  Shared 1 MB", f"{pvt['lsmo_vsdcmin']:>6.0f}",
         f"{pvt['lsmo_vsdcntme'].time().strftime('%H.%M.%S') if pd.notna(pvt['lsmo_vsdcntme']) else ' '}",
         f"{pvt['lsmo_vsdcmax']:>6.0f}",
         f"{pvt['lsmo_vsdcxtme'].time().strftime('%H.%M.%S') if pd.notna(pvt['lsmo_vsdcxtme']) else ' '}",
         f"{pvt['lsmo_vsdctotl'] / pvt['r782samp']:>6.0f}"],
        ["1 MB Frames"],
        ["  Fixed", f"{pvt['tofr_vsdcmin']:>6.0f}",
         f"{pvt['tofr_vsdcntme'].time().strftime('%H.%M.%S') if pd.notna(pvt['tofr_vsdcntme']) else ' '}",
         f"{pvt['tofr_vsdcmax']:>6.0f}",
         f"{pvt['tofr_vsdcxtme'].time().strftime('%H.%M.%S') if pd.notna(pvt['tofr_vsdcxtme']) else ' '}",
         f"{pvt['tofr_vsdctotl'] / pvt['r782samp']:>6.0f}"],
        ["  Pageable", f"{pvt['pafr_vsdcmin']:>6.0f}",
         f"{pvt['pafr_vsdcntme'].time().strftime('%H.%M.%S') if pd.notna(pvt['pafr_vsdcntme']) else ' '}",
         f"{pvt['pafr_vsdcmax']:>6.0f}",
         f"{pvt['pafr_vsdcxtme'].time().strftime('%H.%M.%S') if pd.notna(pvt['pafr_vsdcxtme']) else ' '}",
         f"{pvt['pafr_vsdctotl'] / pvt['r782samp']:>6.0f}"],
        ["2 GB Frames"],
        ["  Fixed", f"{pvt['gffr_vsdcmin']:>6.0f}",
         f"{pvt['gffr_vsdcntme'].time().strftime('%H.%M.%S') if pd.notna(pvt['gffr_vsdcntme']) else ' '}",
         f"{pvt['gffr_vsdcmax']:>6.0f}",
         f"{pvt['gffr_vsdcxtme'].time().strftime('%H.%M.%S') if pd.notna(pvt['gffr_vsdcxtme']) else ' '}",
         f"{pvt['gffr_vsdctotl'] / pvt['r782samp']:>6.0f}"]
    ]
    return (tb.tabulate(header1, tablefmt="plain") + "\n" + tb.tabulate(header2, tablefmt="plain") + "\n" +
            tb.tabulate(header3, tablefmt="plain") + '\n' + tb.tabulate(header4, tablefmt="plain") + '\n' +
            tb.tabulate(header5, tablefmt="plain") + '\n' +
            tb.tabulate(subpool_data,
                        headers=["Subpool (Area)", "Min", " ", "Max", " ", "Avg"],
                        colalign=('left', 'right', 'right', 'right', 'right', 'right')) + '\n' +
            "                                                High Virtual Memory Usage (Above 2GB)\n" +
            tb.tabulate(memory_data,
                        headers=["Bytes", "Min", " ", "Max", " ", "Avg", "Peak"],
                        colalign=('left', 'right', 'right', 'right', 'right', 'right', 'right')))


def format_private_storage_summary(pvt, comn, pro):
    if 'date' in pro.keys() and 'datetime' in pro.keys():
        report_date = pvt['date']
        report_time = pvt['datetime'].time().strftime('%H.%M.%S')
        interval = format_s2min(pro['smf78int'])
    elif 'date' in pro.keys():
        report_date = pvt['date']
        report_time = '00.00.00'
        interval = format_s2hr(pro['smf78int'])
    else:
        report_date = pvt['smf78ist'].date()
        report_time = pvt['smf78ist'].time().strftime('%H.%M.%S')
        interval = format_s2min(pro['smf78int'])
    zos_ver = 'V' + pro['smf78mvs'][2:4].lstrip('0') + 'R' + pro['smf78mvs'][4:6].lstrip('0')
    interval_x = f"{interval[:-3]}"
    whitespace = ' '
    header1 = [["                                         V I R T U A L    S T O R A G E    A C T I V I T Y"]]
    header2 = [
        [f"{whitespace:>12}", f"z/OS {zos_ver}", f"{whitespace:>13}", f"System ID {pvt['smf78sid']}", f"{whitespace:>6}",
         f"Date {report_date:%m/%d/%Y}", f"{whitespace:>11}", f"Interval {interval_x}"],
        ["", "", "", f"RMF Version {pro['smf78mfv']:<5}", "", f"Time {report_time}", "", f"Cycle {pro['smf78cyc'] / 1000:5.3f} Seconds"]
    ]
    header3 = [
        ["   "],
        [" ", " ", " ", "           Private Area Summary"],
        ["        ", "Job Name -", f"{pvt['r782jobn']:<8}", " ", "Region Requested",
         f"{convert_bi(pvt['r782regr'], 4, 0, unit='K'):>5}"],
        ["        ", "Step Name -", f"{pvt['r782step']:<8}", " ", "Region Assigned (Below 16M)",
         f"{convert_bi(pvt['r782rgab'], 4, 0, unit='K'):>5}"],
        ["        ", "Program Name -", f"{pvt['r782pgmn']:<8}", " ", "Region Assigned (Above 16M)",
         f"{convert_bi(pvt['r782rgaa'], 4, 0, unit='K'):>5}"],
        ["        ", "Number Of Samples -", f"{pvt['r782samp']:>5}"],
    ]
    report = (tb.tabulate(header1, tablefmt="plain") + "\n" + tb.tabulate(header2, tablefmt="plain") + "\n" +
              tb.tabulate(header3, tablefmt="plain") + '\n')
    starting_b = comn['r782ps'] + int(comn['r782pa'], 16) - 1
    b1 = starting_b - pvt['lsal_vsdbmin'] + 1  # lsqa/swa
    b2 = pvt['r782gmlb']  # getmain limit
    b4 = int(pvt['r782urab'], 16)
    # b5 = int(comn['r782pa'], 16)
    b3 = b4 + pvt['usal_vsdbmax']
    starting_a = int('0x7FFFFFFF', 0)
    a1 = starting_a - pvt['lsal_vsdamin'] + 1  # lsqa/swa
    a2 = pvt['r782gmla'] if pvt['r782gmla'] < int('0x7FFFFFFF', 0) else int('0x7FFFFFFF', 0)  # getmain limit
    a4 = int(pvt['r782uraa'], 16)
    a3 = a4 + pvt['usal_vsdamax']
    if pvt['r782actv']:
        report += (
            f"                                              Private Storage Map\n"
            f"                           Below 16M                              Extended (Above 16M)\n"
            f"                {starting_b:>6X} ________________________                 ________________________ {starting_a:>8X}\n"
            f"                       | LSQA/SWA             |                 | LSQA/SWA             |\n"
            f"                       | 229/230         {convert_bi(pvt['lsal_vsdbmin'], 4, 0, unit='K'):>5}|    Bottom Of    | 229/230"
            f"         {convert_bi(pvt['lsal_vsdamin'], 4, 0, unit='K'):>5}|\n"
            f"                {b1:>6X} |_____{pvt['lsal_vsdbntme'].time().strftime('%H.%M.%S') if pd.notna(pvt['lsal_vsdbntme']) else '        '}_________"
            f"| Allocated Area  |_____{pvt['lsal_vsdantme'].time().strftime('%H.%M.%S') if pd.notna(pvt['lsal_vsdantme']) else '        '}"
            f"_________| {a1:>8X}\n"
            f"                       | Unused          "
            f"{convert_bi(b1 - b2 - pvt['lsal_vsdbmin'], 4, 0, unit='K') if b1 - b2 - pvt['lsal_vsdbmin'] > 0 else '0K':>5}"
            f"|                 | Unused          "
            f"{convert_bi(a1 - a2 - pvt['lsal_vsdamin'], 4, 0, unit='K') if a1 - a2 - pvt['lsal_vsdamin'] > 0 else '0K':>5}|\n"
            f"                {b2:>6X} |______________________|  GETMAIN Limit  |______________________| {a2:>8X}\n"
            f"                       | Unused          "
            f"{convert_bi(b2 - b3 - pvt['lsal_vsdbmin'], 4, 0, unit='K') if b2 - b3 - pvt['lsal_vsdbmin'] > 0 else '0K':>5}|"
            f"                 | Unused          "
            f"{convert_bi(a2 - a3, 4, 0, unit='K') if a2 != int('0x7FFFFFFF', 0) and a2 - a3 > 0 else convert_bi(a2 - a3 - pvt['lsal_vsdamin'], 4, 0, unit='K') if a2 - a3 - pvt['lsal_vsdamin'] > 0 else '0K':>5}|\n"
            f"                {b3:>6X} |_____{pvt['usal_vsdbxtme'].time().strftime('%H.%M.%S') if pd.notna(pvt['usal_vsdbxtme']) else '        '}"
            f"_________|     Top Of      |_____{pvt['usal_vsdaxtme'].time().strftime('%H.%M.%S') if pd.notna(pvt['usal_vsdaxtme']) else '        '}_________| "
            f"{a3:>8X}\n"
            f"                       | User                 | Allocated Area  | User                 |\n"
            f"                       | Region          {convert_bi(pvt['usal_vsdbmax'], 4, 0, unit='K'):>5}|                 | Region               |\n"
            f"              {pvt['r782urab'][:-1].lstrip('0') + pvt['r782urab'][-1]:>8} |______________________|"
            f"                 |                 {convert_bi(pvt['usal_vsdamax'], 4, 0, unit='K'):>5}|\n"
            f"                       | System Region   {convert_bi(int(pvt['r782urab'], 16) - int(comn['r782pa'], 16), 4, 0, unit='K'):>5}|                 |                      |\n"
            f"                {comn['r782pa'][:-1].lstrip('0') + comn['r782pa'][-1]:>6} ------------------------                 ------------------------ "
            f"{pvt['r782uraa'][:-1].lstrip('0') + pvt['r782uraa'][-1]:>8}\n\n")
        # f"                     ---------- Below 16M ----------------  --------------- Above 16M -----------\n"
        # f"                       Min             Max             Avg    Min             Max             Avg\n")
        report += tb.tabulate([
            ["LSQA/SWA/229/230"],
            [" Free Pages (Bytes)", f"{convert_bi(pvt['lsfp_vsdbmin'], 4, 0, unit='K'):>5}",
             f"{pvt['lsfp_vsdbntme'].time().strftime('%H.%M.%S') if pd.notna(pvt['lsfp_vsdbntme']) else ' '}",
             f"{convert_bi(pvt['lsfp_vsdbmax'], 4, 0, unit='K'):>5}",
             f"{pvt['lsfp_vsdbxtme'].time().strftime('%H.%M.%S') if pd.notna(pvt['lsfp_vsdbxtme']) else ' '}",
             f"{convert_bi(pvt['lsfp_vsdbtotl'] / pvt['r782samp'], 4, 0, unit='K'):>5}",
             f"{convert_bi(pvt['lsfp_vsdamin'], 4, 0, unit='K'):>5}",
             f"{pvt['lsfp_vsdantme'].time().strftime('%H.%M.%S') if pd.notna(pvt['lsfp_vsdantme']) else ' '}",
             f"{convert_bi(pvt['lsfp_vsdamax'], 4, 0, unit='K'):>5}",
             f"{pvt['lsfp_vsdaxtme'].time().strftime('%H.%M.%S') if pd.notna(pvt['lsfp_vsdaxtme']) else ' '}",
             f"{convert_bi(pvt['lsfp_vsdatotl'] / pvt['r782samp'], 4, 0, unit='K'):>5}"],
            [" Largest Free Block", f"{convert_bi(pvt['lsfb_vsdbmin'], 4, 0, unit='K'):>5}",
             f"{pvt['lsfb_vsdbntme'].time().strftime('%H.%M.%S') if pd.notna(pvt['lsfb_vsdbntme']) else ' '}",
             f"{convert_bi(pvt['lsfb_vsdbmax'], 4, 0, unit='K'):>5}",
             f"{pvt['lsfb_vsdbxtme'].time().strftime('%H.%M.%S') if pd.notna(pvt['lsfb_vsdbxtme']) else ' '}",
             f"{convert_bi(pvt['lsfb_vsdbtotl'] / pvt['r782samp'], 4, 0, unit='K'):>5}",
             f"{convert_bi(pvt['lsfb_vsdamin'], 4, 0, unit='K'):>5}",
             f"{pvt['lsfb_vsdantme'].time().strftime('%H.%M.%S') if pd.notna(pvt['lsfb_vsdantme']) else ' '}",
             f"{convert_bi(pvt['lsfb_vsdamax'], 4, 0, unit='K'):>5}",
             f"{pvt['lsfb_vsdaxtme'].time().strftime('%H.%M.%S') if pd.notna(pvt['lsfb_vsdaxtme']) else ' '}",
             f"{convert_bi(pvt['lsfb_vsdatotl'] / pvt['r782samp'], 4, 0, unit='K'):>5}"],
            [" Pages Allocated"],
            ["  (in Bytes)", f"{convert_bi(pvt['lspa_vsdbmin'], 4, 0, unit='K'):>5}",
             f"{pvt['lspa_vsdbntme'].time().strftime('%H.%M.%S') if pd.notna(pvt['lspa_vsdbntme']) else ' '}",
             f"{convert_bi(pvt['lspa_vsdbmax'], 4, 0, unit='K'):>5}",
             f"{pvt['lspa_vsdbxtme'].time().strftime('%H.%M.%S') if pd.notna(pvt['lspa_vsdbxtme']) else ' '}",
             f"{convert_bi(pvt['lspa_vsdbtotl'] / pvt['r782samp'], 4, 0, unit='K'):>5}",
             f"{convert_bi(pvt['lspa_vsdamin'], 4, 0, unit='K'):>5}",
             f"{pvt['lspa_vsdantme'].time().strftime('%H.%M.%S') if pd.notna(pvt['lspa_vsdantme']) else ' '}",
             f"{convert_bi(pvt['lspa_vsdamax'], 4, 0, unit='K'):>5}",
             f"{pvt['lspa_vsdaxtme'].time().strftime('%H.%M.%S') if pd.notna(pvt['lspa_vsdaxtme']) else ' '}",
             f"{convert_bi(pvt['lspa_vsdatotl'] / pvt['r782samp'], 4, 0, unit='K'):>5}\n"],
            ["User Region"],
            [" Free Pages (Bytes)", f"{convert_bi(pvt['usfp_vsdbmin'], 4, 0, unit='K'):>5}",
             f"{pvt['usfp_vsdbntme'].time().strftime('%H.%M.%S') if pd.notna(pvt['usfp_vsdbntme']) else ' '}",
             f"{convert_bi(pvt['usfp_vsdbmax'], 4, 0, unit='K'):>5}",
             f"{pvt['usfp_vsdbxtme'].time().strftime('%H.%M.%S') if pd.notna(pvt['usfp_vsdbxtme']) else ' '}",
             f"{convert_bi(pvt['usfp_vsdbtotl'] / pvt['r782samp'], 4, 0, unit='K'):>5}",
             f"{convert_bi(pvt['usfp_vsdamin'], 4, 0, unit='K'):>5}",
             f"{pvt['usfp_vsdantme'].time().strftime('%H.%M.%S') if pd.notna(pvt['usfp_vsdantme']) else ' '}",
             f"{convert_bi(pvt['usfp_vsdamax'], 4, 0, unit='K'):>5}",
             f"{pvt['usfp_vsdaxtme'].time().strftime('%H.%M.%S') if pd.notna(pvt['usfp_vsdaxtme']) else ' '}",
             f"{convert_bi(pvt['usfp_vsdatotl'] / pvt['r782samp'], 4, 0, unit='K'):>5}"],
            [" Largest Free Block"],
            ["   in GETMAIN Limit", f"{convert_bi(pvt['usfb_vsdbmin'], 4, 0, unit='K'):>5}",
             f"{pvt['usfb_vsdbntme'].time().strftime('%H.%M.%S') if pd.notna(pvt['usfb_vsdbntme']) else ' '}",
             f"{convert_bi(pvt['usfb_vsdbmax'], 4, 0, unit='K'):>5}",
             f"{pvt['usfb_vsdbxtme'].time().strftime('%H.%M.%S') if pd.notna(pvt['usfb_vsdbxtme']) else ' '}",
             f"{convert_bi(pvt['usfb_vsdbtotl'] / pvt['r782samp'], 4, 0, unit='K'):>5}",
             f"{convert_bi(pvt['usfb_vsdamin'], 4, 0, unit='K'):>5}",
             f"{pvt['usfb_vsdantme'].time().strftime('%H.%M.%S') if pd.notna(pvt['usfb_vsdantme']) else ' '}",
             f"{convert_bi(pvt['usfb_vsdamax'], 4, 0, unit='K'):>5}",
             f"{pvt['usfb_vsdaxtme'].time().strftime('%H.%M.%S') if pd.notna(pvt['usfb_vsdaxtme']) else ' '}",
             f"{convert_bi(pvt['usfb_vsdatotl'] / pvt['r782samp'], 4, 0, unit='K'):>5}"],
            [" Pages Allocated"],
            ["   (in Bytes)", f"{convert_bi(pvt['uspa_vsdbmin'], 4, 0, unit='K'):>5}",
             f"{pvt['uspa_vsdbntme'].time().strftime('%H.%M.%S') if pd.notna(pvt['uspa_vsdbntme']) else ' '}",
             f"{convert_bi(pvt['uspa_vsdbmax'], 4, 0, unit='K'):>5}",
             f"{pvt['uspa_vsdbxtme'].time().strftime('%H.%M.%S') if pd.notna(pvt['uspa_vsdbxtme']) else ' '}",
             f"{convert_bi(pvt['uspa_vsdbtotl'] / pvt['r782samp'], 4, 0, unit='K'):>5}",
             f"{convert_bi(pvt['uspa_vsdamin'], 4, 0, unit='K'):>5}",
             f"{pvt['uspa_vsdantme'].time().strftime('%H.%M.%S') if pd.notna(pvt['uspa_vsdantme']) else ' '}",
             f"{convert_bi(pvt['uspa_vsdamax'], 4, 0, unit='K'):>5}",
             f"{pvt['uspa_vsdaxtme'].time().strftime('%H.%M.%S') if pd.notna(pvt['uspa_vsdaxtme']) else ' '}",
             f"{convert_bi(pvt['uspa_vsdatotl'] / pvt['r782samp'], 4, 0, unit='K'):>5}"]], tablefmt='plain',
            headers=[" ", "<------\nMin", "Below\n", "16M  \nMax", "--------\n", "------>\nAvg",
                     "<-----\nMin", "--------\n", "Above\nMax", "16M      \n", "------>\nAvg"],
            colalign=('left', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right'))
    else:
        report += "\n**** Job was not active at the beginning of this interval ****\n"
    return report


def hr_min_sec_milli(td):
    hours = td.seconds // 3600
    minutes = (td.seconds // 60) % 60
    seconds = td.seconds - hours * 3600 - minutes * 60
    return hours, minutes, seconds, td.microseconds // 1000


def format_policy_page(duration, policy, sid_list, rgss, rgss_wmss, rgss_wmss_scss):
    if duration == 'Hourly':
        # report_date = policy['date']
        report_time = policy['datetime'].time().strftime('%H.%M.%S')
    elif duration == 'Daily':
        # report_date = policy['date']
        report_time = '00.00.00'
    else:
        # report_date = policy['smf72ist'].date()
        report_time = policy['smf72ist'].time().strftime('%H.%M.%S')

    policy_page_table = [
        [f"Service Definition: {policy['r723midn']:<8}  {policy['r723midd']:<32}", "<Service",
         "Definition", "Coefficients", "-->", "-Norm", "Factors-"],
        [f"  Install Date: {policy['r723mtdi']:%m/%d/%Y %H.%M.%S}  Installed By: {policy['r723midu']:<8}", "IOC", "CPU",
         "SRB", "MSO", "AAP", "IIP"],
        [f"  Policy: {policy['r723mnsp']:<8}  {policy['r723mdsp']:<32}"],
        [f"  Discretionary Goal Management: {'NO' if is_bit_set(policy['r723mflg'], 8, 6) else 'YES'}",
         f"{policy['r723mioc']:>2.1f}", f"{policy['r723mcpu']:>2.1f}",
         f"{policy['r723msrb']:>2.1f}", f"{policy['r723mmso']:>5.4f}",
         f"{policy['r723nffi'] / 256:>6.4f}", f"{policy['r723nffs'] / 256:>6.4f}"],
        [f"  Dynamic Alias Management: {'YES' if is_bit_set(policy['r723mscf'], 8, 6) else 'NO'}"],
        [f"  I/O Priority Management:  {'YES' if is_bit_set(policy['r723mscf'], 8, 3) else 'NO'}"],
    ]
    policy_systems_odd = []
    policy_systems_even = []
    for sid_idx, sid_pro in enumerate(sid_list):
        sid_interval = pd.to_datetime(0) + pd.to_timedelta(sid_pro[1], unit='s')
        if sid_pro[2] and not sid_pro[3]:
            boost_type = 'S'
        elif not sid_pro[2] and sid_pro[3]:
            boost_type = 'I'
        elif sid_pro[2] and sid_pro[3]:
            boost_type = 'A'
        else:
            boost_type = 'Inactive'
        if sid_idx % 2:
            policy_systems_odd.append(
                [f"  {sid_pro[0]:<8}", f"{policy['r723mopt']:<2}",
                 f"{16000000 / policy['r723madj']:<6.1f}",
                 f"{policy['smf70cai']:>4}", f"{report_time}",
                 f"{sid_interval:%H.%M.%S}", f"{boost_type:^8}"])
        else:
            policy_systems_even.append(
                [f"  {sid_pro[0]:<8}", f"{policy['r723mopt']:<2}",
                 f"{16000000 / policy['r723madj']:<6.1f}",
                 f"{policy['smf70cai']:>4}", f"{report_time}",
                 f"{sid_interval:%H.%M.%S}", f"{boost_type:^8}"])

    policy_systems = []
    min_len = min(len(policy_systems_odd), len(policy_systems_even))
    header_col = ["Systems\n  --ID---", "\nOpt", "\nSU/Sec", "\nCap%", "\n--Time--", "\nInterval", "\n--Boost--"]
    col_align = ('left', 'right', 'right', 'right', 'left', 'left', 'left')
    float_fmt = ('', '', '.1f', '.0f', '', '', '')
    for i in range(min_len):
        policy_systems.append(policy_systems_even[i])
        policy_systems.append(policy_systems_odd[i])
    policy_systems += policy_systems_even[min_len:]
    if len(policy_systems) > 1:
        header_col += ["\n  --ID---", "\nOpt", "\nSU/Sec", "\nCap%", "\n--Time--", "\nInterval", "\n--Boost--"]
        col_align += col_align
        float_fmt += float_fmt
    policy_code = (
            f"                                                          - Service Policy Page -\n\n" +
            tb.tabulate(policy_page_table, tablefmt='plain',
                        colalign=('left', 'right', 'right', 'right', 'right', 'right', 'right'),
                        floatfmt=('', '.1f', '.1f', '.1f', '.4f', '.4f', '.4f')) + '\n\n' +
            tb.tabulate(policy_systems, tablefmt='plain',
                        headers=header_col,
                        # colalign=col_align,
                        # floatfmt=float_fmt
                        ) + '\n'
    )

    resource_table = []
    for idx, rgs in enumerate(rgss):
        rgs_wmss = rgss_wmss[idx]

        if is_bit_set(rgs['r723gglt'], 8, 5): #rgs['r723ggms']:
            defined_as = 'MSU'
        elif is_bit_set(rgs['r723gglt'], 8, 2): #rgs['r723ggpv']:
            defined_as = '% Lpar Share'
        elif is_bit_set(rgs['r723gglt'], 8, 3): #rgs['r723ggpc']:
            defined_as = 'Number of CPs'
        else:
            defined_as = 'SU/Sec'
        rgs_report_class = []
        rgs_service_class = []
        rgs_num_of_cps = 0.0
        rgs_msu_physical = 0.0
        rgs_su_sec = 0.0
        rgs_scss = []
        for idx2, rgs_wms in enumerate(rgs_wmss):
            rgs_scss = rgss_wmss_scss[idx][idx2]

            rgs_num_of_cps += rgs_wms['num_of_cps']
            rgs_msu_physical += rgs_wms['msu_physical']
            rgs_su_sec += rgs_wms['su_sec']
            if rgs_wms['is_report_class'] or is_bit_set(rgs_wms['r723mflg'], 8, 5): #rgs_wms['tenant_report_class']:
                rgs_report_class.append(rgs_wms)
            else:
                rgs_service_class.append(rgs_wms)

        resource_table.append(
            [f"{rgs['r723ggnm']:<8}", f"{'TRG' if is_bit_set(rgs['r723ggtf'],8,0) else 'RG':<3}", f"{rgs['r723ggde']}", "", "",
             f"{rgs_num_of_cps:>5.2f}", f"{rgs_msu_physical if pd.notna(rgs_msu_physical) else '':{'> 6.2f' if pd.notna(rgs_msu_physical) else '>6'}}", f"{rgs_su_sec:>9.2f}",
             f"{rgs['r723ggmn'] if is_bit_set(rgs['r723gglt'],8,1) else ' ':>8}",
             f"{rgs['r723ggmx'] if is_bit_set(rgs['r723gglt'],8,0) else ' ':>5}",
             f"{defined_as if is_bit_set(rgs['r723gglt'],8,1) or is_bit_set(rgs['r723gglt'],8,0) else ' ':<13}", "",
             f"{rgs['r723ggml'] if is_bit_set(rgs['r723gglt'],8,4) and pd.notna(rgs['r723ggml']) else '' :<5}"]
        )
        if len(rgs_scss) > 0:
            for rgs_scs in rgs_scss:
                resource_table.append(
                    ["", "", "", "", f"{rgs_scs['smf72sid']:<4}",
                     f"{rgs_scs['num_of_cps']:>5.2f}", f"{rgs_scs['msu_physical'] if pd.notna(rgs_scs['msu_physical']) else '':{'> 6.2f' if pd.notna(rgs_scs['msu_physical']) else '>6'}}", f"{rgs_scs['su_sec']:>9.2f}",
                     "", "", "", f"{convert_bi(rgs_scs['memory_usage'], 3):>5}"])

        if len(rgs_report_class) > 0:
            resource_table.append(
                ["", "", "-------Report Classes", f"{rgs_report_class[0]['r723mcnm']:<8}", "",
                 f"{rgs_report_class[0]['num_of_cps']:>5.2f}", f"{rgs_report_class[0]['msu_physical'] if pd.notna(rgs_report_class[0]['msu_physical']) else '':{'> 6.2f' if pd.notna(rgs_report_class[0]['msu_physical']) else '>6'}}",
                 f"{rgs_report_class[0]['su_sec']:>9.2f}"])

            for i in range(1, len(rgs_report_class)):
                resource_table.append(
                    ["", "", "", f"{rgs_report_class[i]['r723mcnm']:<8}", "",
                     f"{rgs_report_class[i]['num_of_cps']:>5.2f}", f"{rgs_report_class[i]['msu_physical'] if pd.notna(rgs_report_class[i]['msu_physical']) else '':{'> 6.2f' if pd.notna(rgs_report_class[i]['msu_physical']) else '>6'}}",
                     f"{rgs_report_class[i]['su_sec']:>9.2f}"])

        if len(rgs_service_class) > 0:
            resource_table.append(
                ["", "", "------Service Classes", f"{rgs_service_class[0]['r723mcnm']:<8}", "",
                 f"{rgs_service_class[0]['num_of_cps']:>5.2f}", f"{rgs_service_class[0]['msu_physical'] if pd.notna(rgs_service_class[0]['msu_physical']) else '':{'> 6.2f' if pd.notna(rgs_service_class[0]['msu_physical']) else '>6'}}",
                 f"{rgs_service_class[0]['su_sec']:>9.2f}"])

            for i in range(1, len(rgs_service_class)):
                resource_table.append(
                    ["", "", "", f"{rgs_service_class[i]['r723mcnm']:<8}", "",
                     f"{rgs_service_class[i]['num_of_cps']:>5.2f}", f"{rgs_service_class[i]['msu_physical'] if pd.notna(rgs_service_class[i]['msu_physical']) else '':{'> 6.2f' if pd.notna(rgs_service_class[i]['msu_physical']) else '>6'}}",
                     f"{rgs_service_class[i]['su_sec']:>9.2f}"])

    return policy_code + "\nResource Groups\n" + tb.tabulate(
        resource_table, tablefmt='plain',
        headers=["--Name--\n", "Type\n", "<----------Description--\n",
                 "------>\n", "System\n", "<---CPU\n#CPS", "Consumption\nMSU", "---->\nSU/Sec",
                 "<------\nMin", "CPU\nMax", "Capacity-->\nDefined As",
                 "<----\nUsage", "Memory->\nLimit"],
        # colalign=('left','left','left','left','lef','right','right','right','right','right','left','right','right'),
        floatfmt=('', '', '', '', '', '.2f', '.0f', '.0f')
    )


def format_service_class_being_served(ssss):
    # if wms.__class__.__name__ == 'Smf72WmsHr':
    #     ssss = wms.smf72_sss_hrs
    # elif wms.__class__.__name__ == 'Smf72WmsDa':
    #     ssss = wms.smf72_sss_das
    # else:  # wms.__class__.__name__ == 'Smf72_wms':
    #     ssss = wms.smf72_ssss
    if len(ssss) == 0:
        return None
    service_class_list = []
    code = \
        "-----------------------------------------------Service Classes Being Served------------------------------------------------------\n"
    for sss in ssss:
        if sss['r723scsn'] not in service_class_list:
            service_class_list.append(sss['r723scsn'])
    for service_class in service_class_list:
        code += f"{service_class}\n"
    return code


def format_state_samples_breakdown(target, wrss):
    # if target.__class__.__name__ == 'Smf72ScsHr':
    #     wrss = target.smf72_wrs_hrs
    # elif target.__class__.__name__ == 'Smf72Scs':
    #     wrss = target.smf72_wrss
    # elif target.__class__.__name__ == 'Smf72ScsDa':
    #     wrss = target.smf72_wrs_das
    # elif target.__class__.__name__ == 'Smf72SmsHr':
    #     wrss = target.smf72_wrsx_hrs
    # elif target.__class__.__name__ == 'Smf72Wms':
    #     wrss = target.smf72_wrsxs
    # else:
    #     wrss = target.smf72_wrsx_das

    if len(wrss) == 0:
        return None

    total_samples = target['r723ctet'] * target['sample_rate']
    delay_total = {'Lock': target['r723rwlo'], 'I/O': target['r723rwio'], 'Conv': target['r723rwco'],
                   'Dist': target['r723rwds'], 'Locl': target['r723rwsl'], 'Sysp': target['r723rwss'],
                   'Remt': target['r723rwsn'], 'Time': target['r723rwtm'], 'Ltch': target['r723rwnl'],
                   'Prod': target['r723rwo'], 'Misc': target['r723rwms'], 'SslT': target['r723rwst'],
                   'RegT': target['r723rwrt'], 'Work': target['r723rwwr'], 'BpMi': target['r723rbpm'],
                   'Typ1': target['r723rw01'], 'Typ2': target['r723rw02'], 'Typ3': target['r723rw03'],
                   'Typ4': target['r723rw04'], 'Typ5': target['r723rw05'], 'Typ6': target['r723rw06'],
                   'Typ7': target['r723rw07'], 'Typ8': target['r723rw08'], 'Typ9': target['r723rw09'],
                   'Ty10': target['r723rw10'], 'Ty11': target['r723rw11'], 'Ty12': target['r723rw12'],
                   'Ty13': target['r723rw13'], 'Ty14': target['r723rw14'], 'Ty15': target['r723rw15']}

    delay_tuple = sorted(delay_total.items(), key=lambda x: x[1], reverse=True)
    delay_cols = []
    for delay in delay_tuple:
        if delay[1] > 0:
            delay_cols.append(f"{delay[0]:>4}")
    state_category = ' '.join(delay_cols)
    state_table = []
    for wrs in wrss:
        if total_samples > 0:
            response_percent = wrs['r723ress'] / total_samples * 100
        else:
            response_percent = 0
        delay_vals = []
        for delay in delay_cols:
            if wrs['r723ress'] > 0:
                if delay == 'Lock':
                    delay_vals.append(f"{wrs['r723rwlo'] / wrs['r723ress'] * 100:>4.1f}")
                elif delay == ' I/O':
                    delay_vals.append(f"{wrs['r723rwio'] / wrs['r723ress'] * 100:>4.1f}")
                elif delay == 'Conv':
                    delay_vals.append(f"{wrs['r723rwco'] / wrs['r723ress'] * 100:>4.1f}")
                elif delay == 'Dist':
                    delay_vals.append(f"{wrs['r723rwds'] / wrs['r723ress'] * 100:>4.1f}")
                elif delay == 'Locl':
                    delay_vals.append(f"{wrs['r723rwsl'] / wrs['r723ress'] * 100:>4.1f}")
                elif delay == 'Sysp':
                    delay_vals.append(f"{wrs['r723rwss'] / wrs['r723ress'] * 100:>4.1f}")
                elif delay == 'Remt':
                    delay_vals.append(f"{wrs['r723rwsn'] / wrs['r723ress'] * 100:>4.1f}")
                elif delay == 'Time':
                    delay_vals.append(f"{wrs['r723rwtm'] / wrs['r723ress'] * 100:>4.1f}")
                elif delay == 'Ltch':
                    delay_vals.append(f"{wrs['r723rwnl'] / wrs['r723ress'] * 100:>4.1f}")
                elif delay == 'Prod':
                    delay_vals.append(f"{wrs['r723rwo'] / wrs['r723ress'] * 100:>4.1f}")
                elif delay == 'Misc':
                    delay_vals.append(f"{wrs['r723rwms'] / wrs['r723ress'] * 100:>4.1f}")
                elif delay == 'SslT':
                    delay_vals.append(f"{wrs['r723rwst'] / wrs['r723ress'] * 100:>4.1f}")
                elif delay == 'RegT':
                    delay_vals.append(f"{wrs['r723rwrt'] / wrs['r723ress'] * 100:>4.1f}")
                elif delay == 'Work':
                    delay_vals.append(f"{wrs['r723rwwr'] / wrs['r723ress'] * 100:>4.1f}")
                elif delay == 'BpMi':
                    delay_vals.append(f"{wrs['r723rbpm'] / wrs['r723ress'] * 100:>4.1f}")
                elif delay == 'Typ1':
                    delay_vals.append(f"{wrs['r723rw01'] / wrs['r723ress'] * 100:>4.1f}")
                elif delay == 'Typ2':
                    delay_vals.append(f"{wrs['r723rw02'] / wrs['r723ress'] * 100:>4.1f}")
                elif delay == 'Typ3':
                    delay_vals.append(f"{wrs['r723rw03'] / wrs['r723ress'] * 100:>4.1f}")
                elif delay == 'Typ4':
                    delay_vals.append(f"{wrs['r723rw04'] / wrs['r723ress'] * 100:>4.1f}")
                elif delay == 'Typ5':
                    delay_vals.append(f"{wrs['r723rw05'] / wrs['r723ress'] * 100:>4.1f}")
                elif delay == 'Typ6':
                    delay_vals.append(f"{wrs['r723rw06'] / wrs['r723ress'] * 100:>4.1f}")
                elif delay == 'Typ7':
                    delay_vals.append(f"{wrs['r723rw07'] / wrs['r723ress'] * 100:>4.1f}")
                elif delay == 'Typ8':
                    delay_vals.append(f"{wrs['r723rw08'] / wrs['r723ress'] * 100:>4.1f}")
                elif delay == 'Typ9':
                    delay_vals.append(f"{wrs['r723rw09'] / wrs['r723ress'] * 100:>4.1f}")
                elif delay == 'Ty10':
                    delay_vals.append(f"{wrs['r723rw10'] / wrs['r723ress'] * 100:>4.1f}")
                elif delay == 'Ty11':
                    delay_vals.append(f"{wrs['r723rw11'] / wrs['r723ress'] * 100:>4.1f}")
                elif delay == 'Ty12':
                    delay_vals.append(f"{wrs['r723rw12'] / wrs['r723ress'] * 100:>4.1f}")
                elif delay == 'Ty13':
                    delay_vals.append(f"{wrs['r723rw13'] / wrs['r723ress'] * 100:>4.1f}")
                elif delay == 'Ty14':
                    delay_vals.append(f"{wrs['r723rw14'] / wrs['r723ress'] * 100:>4.1f}")
                elif delay == 'Ty15':
                    delay_vals.append(f"{wrs['r723rw15'] / wrs['r723ress'] * 100:>4.1f}")
            else:
                delay_vals.append(" 0.0")
        state_value = ' '.join(delay_vals)
        state_detail = \
            [f"{wrs['r723rtyp']:<4}", f"{wrs['phase']:<3}",
             f"{response_percent:{'>8.0f' if response_percent > 999 else '>8.1f'}}",
             f"{wrs['r723ract'] / wrs['r723ress'] * 100 if wrs['r723ress'] > 0 else 0:>5.1f}",
             f"{wrs['r723rapp'] / wrs['r723ress'] * 100 if wrs['r723ress'] > 0 else 0:>5.1f}",
             f"{wrs['r723rrdy'] / wrs['r723ress'] * 100 if wrs['r723ress'] > 0 else 0:>5.1f}",
             f"{wrs['r723ridl'] / wrs['r723ress'] * 100 if wrs['r723ress'] > 0 else 0:>5.1f}",
             f"{state_value:<69}",
             f"{wrs['r723rssl'] / wrs['r723ress'] * 100 if wrs['r723ress'] > 0 else 0:>5.1f}",
             f"{wrs['r723rsss'] / wrs['r723ress'] * 100 if wrs['r723ress'] > 0 else 0:>5.1f}",
             f"{wrs['r723rssn'] / wrs['r723ress'] * 100 if wrs['r723ress'] > 0 else 0:>5.1f}"]
        state_table.append(state_detail)
    return '\n' + tb.tabulate(state_table, tablefmt='plain',
                              headers=["\nSub\nType", "\nP\n", "Resp\nTime\n(%)", "<--\n<--\nSub",
                                       "--------\nActive->\nAppl",
                                       "-----\nReady\n", "-----\nIdle\n",
                                       f"------------- State Samples Breakdown (%) -------------------------->\n-----------------------------Waiting For-----------------------------\n{state_category:<69}",
                                       "<-------\nSwitched\nLocal", "State\n\nSyspl", "----->\nSampl(%)\nRemot"],
                              floatfmt=('', '', '.1f', '.1f', '.1f', '.1f', '.1f', '', '.1f', '.1f', '.1f')) + '\n'


def format_response_time_distribution(scs, rts, policy_interval, wms_scss=None):
    if scs['is_report_class']:
        return None
    interval = format_s2hr(policy_interval)
    interval_x = f"{interval[:-3]}"
    if scs['class_goal_type'] in ('Execution Velocity', 'Percentile Resp. Time', 'Average Resp. Time'):
        if scs['r723rtdm'] > 0:
            if rts is None:
                return None
            bucket_transactions = [rts['class_rt_bucket_1'],
                                   rts['class_rt_bucket_2'],
                                   rts['class_rt_bucket_3'],
                                   rts['class_rt_bucket_4'],
                                   rts['class_rt_bucket_5'],
                                   rts['class_rt_bucket_6'],
                                   rts['class_rt_bucket_7'],
                                   rts['class_rt_bucket_8'],
                                   rts['class_rt_bucket_9'],
                                   rts['class_rt_bucket_10'],
                                   rts['class_rt_bucket_11'],
                                   rts['class_rt_bucket_12'],
                                   rts['class_rt_bucket_13'],
                                   rts['class_rt_bucket_14']]
            total_bucket_transactions = sum(bucket_transactions)
            if total_bucket_transactions > 0:
                response_time_distribution = (
                    "\n                                       -----------Response Time Distribution----------\n"
                )
                if scs['class_goal_type'] == 'Execution Velocity':
                    if wms_scss is None:
                        response_time_distribution += \
                            f"System: {scs['smf72sid']:<4} ----Interval:{interval_x}  ---MRT Changes:{scs['r723rtdc']:>3} ---\n"
                    else:
                        for scs_num, wms_scs in enumerate(wms_scss):
                            response_time_distribution += \
                                f"System: {wms_scs['smf72sid']:<4} ----Interval:{interval_x}  ---MRT Changes:{wms_scs['r723rtdc']:>3} ---     "
                            if scs_num % 2:
                                response_time_distribution += "\n"
                        if len(wms_scss) % 2:
                            response_time_distribution += "\n"
                accum_bucket_transactions = [sum(bucket_transactions[0:x]) for x in
                                             range(1, len(bucket_transactions) + 1)]

                bucket_1 = pd.to_timedelta(scs['r723rtdm'] * 0.5, unit='ms')
                bucket_2 = pd.to_timedelta(scs['r723rtdm'] * 0.6, unit='ms')
                bucket_3 = pd.to_timedelta(scs['r723rtdm'] * 0.7, unit='ms')
                bucket_4 = pd.to_timedelta(scs['r723rtdm'] * 0.8, unit='ms')
                bucket_5 = pd.to_timedelta(scs['r723rtdm'] * 0.9, unit='ms')
                bucket_6 = pd.to_timedelta(scs['r723rtdm'], unit='ms')
                bucket_7 = pd.to_timedelta(scs['r723rtdm'] * 1.1, unit='ms')
                bucket_8 = pd.to_timedelta(scs['r723rtdm'] * 1.2, unit='ms')
                bucket_9 = pd.to_timedelta(scs['r723rtdm'] * 1.3, unit='ms')
                bucket_10 = pd.to_timedelta(scs['r723rtdm'] * 1.4, unit='ms')
                bucket_11 = pd.to_timedelta(scs['r723rtdm'] * 1.5, unit='ms')
                bucket_12 = pd.to_timedelta(scs['r723rtdm'] * 2, unit='ms')
                bucket_13 = pd.to_timedelta(scs['r723rtdm'] * 4, unit='ms')
                if scs['class_goal_type'] == 'Execution Velocity':
                    response_time_distribution += tb.tabulate([
                        [f"<= {pd.to_datetime(0) + bucket_1:%H.%M.%S.%f}", f"{accum_bucket_transactions[0]:>9}",
                         f"{bucket_transactions[0]:>9}",
                         f"{accum_bucket_transactions[0] / total_bucket_transactions * 100:5.1f}",
                         f"{bucket_transactions[0] / total_bucket_transactions * 100:5.1f}"],
                        [f"<= {pd.to_datetime(0) + bucket_2:%H.%M.%S.%f}", f"{accum_bucket_transactions[1]:>9}",
                         f"{bucket_transactions[1]:>9}",
                         f"{accum_bucket_transactions[1] / total_bucket_transactions * 100:5.1f}",
                         f"{bucket_transactions[1] / total_bucket_transactions * 100:5.1f}"],
                        [f"<= {pd.to_datetime(0) + bucket_3:%H.%M.%S.%f}", f"{accum_bucket_transactions[2]:>9}",
                         f"{bucket_transactions[2]:>9}",
                         f"{accum_bucket_transactions[2] / total_bucket_transactions * 100:5.1f}",
                         f"{bucket_transactions[2] / total_bucket_transactions * 100:5.1f}"],
                        [f"<= {pd.to_datetime(0) + bucket_4:%H.%M.%S.%f}", f"{accum_bucket_transactions[3]:>9}",
                         f"{bucket_transactions[3]:>9}",
                         f"{accum_bucket_transactions[3] / total_bucket_transactions * 100:5.1f}",
                         f"{bucket_transactions[3] / total_bucket_transactions * 100:5.1f}"],
                        [f"<= {pd.to_datetime(0) + bucket_5:%H.%M.%S.%f}", f"{accum_bucket_transactions[4]:>9}",
                         f"{bucket_transactions[4]:>9}",
                         f"{accum_bucket_transactions[4] / total_bucket_transactions * 100:5.1f}",
                         f"{bucket_transactions[4] / total_bucket_transactions * 100:5.1f}"],
                        [f"<= {pd.to_datetime(0) + bucket_6:%H.%M.%S.%f}", f"{accum_bucket_transactions[5]:>9}",
                         f"{bucket_transactions[5]:>9}",
                         f"{accum_bucket_transactions[5] / total_bucket_transactions * 100:5.1f}",
                         f"{bucket_transactions[5] / total_bucket_transactions * 100:5.1f}"],
                        [f"<= {pd.to_datetime(0) + bucket_7:%H.%M.%S.%f}", f"{accum_bucket_transactions[6]:>9}",
                         f"{bucket_transactions[6]:>9}",
                         f"{accum_bucket_transactions[6] / total_bucket_transactions * 100:5.1f}",
                         f"{bucket_transactions[6] / total_bucket_transactions * 100:5.1f}"],
                        [f"<= {pd.to_datetime(0) + bucket_8:%H.%M.%S.%f}", f"{accum_bucket_transactions[7]:>9}",
                         f"{bucket_transactions[7]:>9}",
                         f"{accum_bucket_transactions[7] / total_bucket_transactions * 100:5.1f}",
                         f"{bucket_transactions[7] / total_bucket_transactions * 100:5.1f}"],
                        [f"<= {pd.to_datetime(0) + bucket_9:%H.%M.%S.%f}", f"{accum_bucket_transactions[8]:>9}",
                         f"{bucket_transactions[8]:>9}",
                         f"{accum_bucket_transactions[8] / total_bucket_transactions * 100:5.1f}",
                         f"{bucket_transactions[8] / total_bucket_transactions * 100:5.1f}"],
                        [f"<= {pd.to_datetime(0) + bucket_10:%H.%M.%S.%f}", f"{accum_bucket_transactions[9]:>9}",
                         f"{bucket_transactions[9]:>9}",
                         f"{accum_bucket_transactions[9] / total_bucket_transactions * 100:5.1f}",
                         f"{bucket_transactions[9] / total_bucket_transactions * 100:5.1f}"],
                        [f"<= {pd.to_datetime(0) + bucket_11:%H.%M.%S.%f}", f"{accum_bucket_transactions[10]:>9}",
                         f"{bucket_transactions[10]:>9}",
                         f"{accum_bucket_transactions[10] / total_bucket_transactions * 100:5.1f}",
                         f"{bucket_transactions[10] / total_bucket_transactions * 100:5.1f}"],
                        [f"<= {pd.to_datetime(0) + bucket_12:%H.%M.%S.%f}", f"{accum_bucket_transactions[11]:>9}",
                         f"{bucket_transactions[11]:>9}",
                         f"{accum_bucket_transactions[11] / total_bucket_transactions * 100:5.1f}",
                         f"{bucket_transactions[11] / total_bucket_transactions * 100:5.1f}"],
                        [f"<= {pd.to_datetime(0) + bucket_13:%H.%M.%S.%f}", f"{accum_bucket_transactions[12]:>9}",
                         f"{bucket_transactions[12]:>9}",
                         f"{accum_bucket_transactions[12] / total_bucket_transactions * 100:5.1f}",
                         f"{bucket_transactions[12] / total_bucket_transactions * 100:5.1f}"],
                        [f">  {pd.to_datetime(0) + bucket_13:%H.%M.%S.%f}", f"{accum_bucket_transactions[13]:>9}",
                         f"{bucket_transactions[13]:>9}",
                         f"{accum_bucket_transactions[13] / total_bucket_transactions * 100:5.1f}",
                         f"{bucket_transactions[13] / total_bucket_transactions * 100:5.1f}"],
                    ],
                        headers=["   -----Time------\nHH.MM.SS.FFFFFF",
                                 "<---#\n Cum Total", "Trans--->\nIn Bucket", "<---%\nCum Total",
                                 "Trans--->\nIn Bucket"],
                        colalign=('left', 'right', 'right', 'right', 'right'),
                        floatfmt=('', '.0f', '.1f', '.1f', '.1f'))
                else:
                    response_time_distribution += tb.tabulate([
                        [f"<= {pd.to_datetime(0) + bucket_1:%H.%M.%S.%f}", f"{accum_bucket_transactions[0]:>9}",
                         f"{bucket_transactions[0]:>9}",
                         f"{accum_bucket_transactions[0] / total_bucket_transactions * 100:5.1f}",
                         f"{bucket_transactions[0] / total_bucket_transactions * 100:5.1f}",
                         f"{'>' * int(bucket_transactions[0] / total_bucket_transactions * 51)}"],
                        [f"<= {pd.to_datetime(0) + bucket_2:%H.%M.%S.%f}", f"{accum_bucket_transactions[1]:>9}",
                         f"{bucket_transactions[1]:>9}",
                         f"{accum_bucket_transactions[1] / total_bucket_transactions * 100:5.1f}",
                         f"{bucket_transactions[1] / total_bucket_transactions * 100:5.1f}",
                         f"{'>' * int(bucket_transactions[1] / total_bucket_transactions * 51)}"],
                        [f"<= {pd.to_datetime(0) + bucket_3:%H.%M.%S.%f}", f"{accum_bucket_transactions[2]:>9}",
                         f"{bucket_transactions[2]:>9}",
                         f"{accum_bucket_transactions[2] / total_bucket_transactions * 100:5.1f}",
                         f"{bucket_transactions[2] / total_bucket_transactions * 100:5.1f}",
                         f"{'>' * int(bucket_transactions[2] / total_bucket_transactions * 51)}"],
                        [f"<= {pd.to_datetime(0) + bucket_4:%H.%M.%S.%f}", f"{accum_bucket_transactions[3]:>9}",
                         f"{bucket_transactions[3]:>9}",
                         f"{accum_bucket_transactions[3] / total_bucket_transactions * 100:5.1f}",
                         f"{bucket_transactions[3] / total_bucket_transactions * 100:5.1f}",
                         f"{'>' * int(bucket_transactions[3] / total_bucket_transactions * 51)}"],
                        [f"<= {pd.to_datetime(0) + bucket_5:%H.%M.%S.%f}", f"{accum_bucket_transactions[4]:>9}",
                         f"{bucket_transactions[4]:>9}",
                         f"{accum_bucket_transactions[4] / total_bucket_transactions * 100:5.1f}",
                         f"{bucket_transactions[4] / total_bucket_transactions * 100:5.1f}",
                         f"{'>' * int(bucket_transactions[4] / total_bucket_transactions * 51)}"],
                        [f"<= {pd.to_datetime(0) + bucket_6:%H.%M.%S.%f}", f"{accum_bucket_transactions[5]:>9}",
                         f"{bucket_transactions[5]:>9}",
                         f"{accum_bucket_transactions[5] / total_bucket_transactions * 100:5.1f}",
                         f"{bucket_transactions[5] / total_bucket_transactions * 100:5.1f}",
                         f"{'>' * int(bucket_transactions[5] / total_bucket_transactions * 51)}"],
                        [f"<= {pd.to_datetime(0) + bucket_7:%H.%M.%S.%f}", f"{accum_bucket_transactions[6]:>9}",
                         f"{bucket_transactions[6]:>9}",
                         f"{accum_bucket_transactions[6] / total_bucket_transactions * 100:5.1f}",
                         f"{bucket_transactions[6] / total_bucket_transactions * 100:5.1f}",
                         f"{'>' * int(bucket_transactions[6] / total_bucket_transactions * 51)}"],
                        [f"<= {pd.to_datetime(0) + bucket_8:%H.%M.%S.%f}", f"{accum_bucket_transactions[7]:>9}",
                         f"{bucket_transactions[7]:>9}",
                         f"{accum_bucket_transactions[7] / total_bucket_transactions * 100:5.1f}",
                         f"{bucket_transactions[7] / total_bucket_transactions * 100:5.1f}",
                         f"{'>' * int(bucket_transactions[7] / total_bucket_transactions * 51)}"],
                        [f"<= {pd.to_datetime(0) + bucket_9:%H.%M.%S.%f}", f"{accum_bucket_transactions[8]:>9}",
                         f"{bucket_transactions[8]:>9}",
                         f"{accum_bucket_transactions[8] / total_bucket_transactions * 100:5.1f}",
                         f"{bucket_transactions[8] / total_bucket_transactions * 100:5.1f}",
                         f"{'>' * int(bucket_transactions[8] / total_bucket_transactions * 51)}"],
                        [f"<= {pd.to_datetime(0) + bucket_10:%H.%M.%S.%f}", f"{accum_bucket_transactions[9]:>9}",
                         f"{bucket_transactions[9]:>9}",
                         f"{accum_bucket_transactions[9] / total_bucket_transactions * 100:5.1f}",
                         f"{bucket_transactions[9] / total_bucket_transactions * 100:5.1f}",
                         f"{'>' * int(bucket_transactions[9] / total_bucket_transactions * 51)}"],
                        [f"<= {pd.to_datetime(0) + bucket_11:%H.%M.%S.%f}", f"{accum_bucket_transactions[10]:>9}",
                         f"{bucket_transactions[10]:>9}",
                         f"{accum_bucket_transactions[10] / total_bucket_transactions * 100:5.1f}",
                         f"{bucket_transactions[10] / total_bucket_transactions * 100:5.1f}",
                         f"{'>' * int(bucket_transactions[10] / total_bucket_transactions * 51)}"],
                        [f"<= {pd.to_datetime(0) + bucket_12:%H.%M.%S.%f}", f"{accum_bucket_transactions[11]:>9}",
                         f"{bucket_transactions[11]:>9}",
                         f"{accum_bucket_transactions[11] / total_bucket_transactions * 100:5.1f}",
                         f"{bucket_transactions[11] / total_bucket_transactions * 100:5.1f}",
                         f"{'>' * int(bucket_transactions[11] / total_bucket_transactions * 51)}"],
                        [f"<= {pd.to_datetime(0) + bucket_13:%H.%M.%S.%f}", f"{accum_bucket_transactions[12]:>9}",
                         f"{bucket_transactions[12]:>9}",
                         f"{accum_bucket_transactions[12] / total_bucket_transactions * 100:5.1f}",
                         f"{bucket_transactions[12] / total_bucket_transactions * 100:5.1f}",
                         f"{'>' * int(bucket_transactions[12] / total_bucket_transactions * 51)}"],
                        [f">  {pd.to_datetime(0) + bucket_13:%H.%M.%S.%f}", f"{accum_bucket_transactions[13]:>9}",
                         f"{bucket_transactions[13]:>9}",
                         f"{accum_bucket_transactions[13] / total_bucket_transactions * 100:5.1f}",
                         f"{bucket_transactions[13] / total_bucket_transactions * 100:5.1f}",
                         f"{'>' * int(bucket_transactions[13] / total_bucket_transactions * 51)}"],
                    ], tablefmt='plain',
                        headers=["   -----Time------\n   HH.MM.SS.FFFFFF", "<---#\n Cum Total", "Trans--->\nIn Bucket",
                                 "<---%\nCum Total", "Trans--->\nIn Bucket",
                                 "0    10   20   30   40   50   60   70   80   90   100\n|....|....|....|....|....|....|....|....|....|....|"],
                        colalign=('left', 'right', 'right', 'right', 'right', 'left'),
                        floatfmt=('', '.0f', '.1f', '.1f', '.1f'))
                return response_time_distribution + '\n'
            return None
        return None
    return None


def format_workload_header(duration, policy):
    if duration == 'Hourly':
        report_date = policy['date']
        report_time = policy['datetime'].time().strftime('%H.%M.%S')
        interval = format_s2min(policy['smf72int'])
    elif duration == 'Daily':
        report_date = policy['date']
        report_time = '00.00.00'
        interval = format_s2min(policy['smf72int'])
    else:
        report_date = policy['smf72ist'].date()
        report_time = policy['smf72ist'].time().strftime('%H.%M.%S')
        interval = format_s2min(policy['smf72int'])
    zos_ver = 'V' + policy['smf72mvs'][2:4].lstrip('0') + 'R' + policy['smf72mvs'][4:6].lstrip('0')
    interval_x = f"{interval[:-3]}"
    mode = 'Goal'
    whitespace = ' '
    header1 = [["                                                 W O R K L O A D     A C T I V I T Y"]]
    header2 = [
        [f"{whitespace:>4}", f"z/OS {zos_ver}", f"{whitespace:>13}", f"Sysplex {policy['smf72xnm']:<8}",
         f"{whitespace:>10}",
         f"Date {report_date:%m/%d/%Y}", f"{whitespace:>6}", f"Interval {interval_x}", f" Mode = {mode}"],
        ["", "", "", f"RMF Version {policy['smf72mfv']}", "", f"Time {report_time}"]
    ]
    header3 = [
        [f"                                                Policy Activation Date/Time {policy['r723mtpa']:%m/%d/%Y %H.%M.%S}                                           "]]
    return (tb.tabulate(header1, tablefmt="plain") + "\n" + tb.tabulate(header2, tablefmt="plain") + "\n" +
            tb.tabulate(header3, tablefmt="simple") + '\n')


def format_transaction_detail(target, wms, policy, ssss):
    if wms['is_report_class']:
        transaction_detail = (
                tb.tabulate([
                    [f"Policy={target['r723mnsp']:<8}", "                       ",
                     f"Report Class={target['r723mcnm']:<8}"],
                    ["", "", f"Description ={wms['r723mcde']}"]], tablefmt='plain') + '\n'
        )
    else:
        if pd.isna(wms['r723ggnm']):
            resource_group = '*None'
        else:
            resource_group = wms['r723ggnm']
        if is_bit_set(wms['r723mscf'],8, 4) and is_bit_set(wms['r723mscf'],8, 5):  #cpu_protection'] and wms['stor_protection']:
            critical = 'Storage + CPU'
        elif is_bit_set(wms['r723mscf'],8, 4): #wms['cpu_protection']:
            critical = 'CPU'
        elif is_bit_set(wms['r723mscf'],8, 5): #wms['stor_protection']:
            critical = 'Storage'
        else:
            critical = 'None'
        transaction_detail = (
                tb.tabulate(
                    [[f"Policy={target['r723mnsp']:<8}", " ", f"Workload={target['r723mwnm']:<8}", " ",
                      f"Service Class={target['r723mcnm']:<8}", " ",
                      f"Resource Group={resource_group:<8}", " ",
                      f"Period={target['r723cper']:<1}", f"Importance={target['r723cimp']:<1}"],
                     ["", "", "", "", f"Critical     ={critical}"], "",
                     f"{'I/O Priority Group=High' if is_bit_set(policy['r723mscf'],8, 7) else ''}"],
                    tablefmt='plain'
                ) + '\n'
        )

    if target['r723csrv'] > 0 or target['r723crcp'] > 0:
        actual = (pd.to_datetime(0) + dt.timedelta(seconds=target['transaction_response_time_mean'])).strftime(
            '%H.%M.%S.%f')
        if pd.notna(target['transaction_execution_time_mean']):
            execution = (pd.to_datetime(0) + dt.timedelta(seconds=target['transaction_execution_time_mean'])).strftime(
                '%H.%M.%S.%f')
        else:
            execution = 'N/A'
        queued = (pd.to_datetime(0) + dt.timedelta(seconds=target['transaction_queue_delay_time_mean'])).strftime(
            '%H.%M.%S.%f')
        rs_affin = (pd.to_datetime(0) + dt.timedelta(seconds=target['transaction_aff_delay_time_mean'])).strftime(
            '%H.%M.%S.%f')
        ineligible = (pd.to_datetime(0) + dt.timedelta(seconds=target['transaction_inel_delay_time_mean'])).strftime(
            '%H.%M.%S.%f')
        if pd.notna(target['transaction_average_elapsed_time_std_dev']):
            std_dev = (pd.to_datetime(0) + dt.timedelta(
                seconds=target['transaction_average_elapsed_time_std_dev'])).strftime('%H.%M.%S.%f')
        else:
            std_dev = None
        jcl_time_mean = (pd.to_datetime(0) + dt.timedelta(
                seconds=target['transaction_jcl_time_mean'])).strftime('%H.%M.%S.%f')
        if target['r723ctrr'] > 0:
            storage_avg = target['r723cprs'] / target['r723ctrr']
        else:
            storage_avg = 0
        transaction_table1 = [
            ["Avg", f"{target['transaction_average_active']:>11.2f}",
             "Actual", f"{format_time(actual):>20}",
             "Total", f"{target['transaction_total_percentage_cp_time']:>7.2f}",
             f"{target['transaction_total_percentage_sp_on_cp_time']:>7.2f}",
             f"{target['transaction_total_percentage_sp_time'] if (is_bit_set(policy['smf72prf'],8,5) or is_bit_set(policy['smf72prf'],8,4)) and pd.notna(target['transaction_total_percentage_sp_time']) else 'N/A':{'> 7.2f' if (is_bit_set(policy['smf72prf'],8,5) or is_bit_set(policy['smf72prf'],8,4)) and pd.notna(target['transaction_total_percentage_sp_time']) else '>7'}}",
             "Avg Enc", f"{target['transaction_enclave_average']:>6.2f}"],
            ["MPL", f"{target['transaction_average_swapped_in']:>11.2f}",
             "Execution", f"{format_time(execution):>17}",
             "Mobile", f"{target['transaction_mobile_percentage_cp_time']:>7.2f}",
             f"{target['transaction_mobile_percentage_sp_on_cp_time']:>7.2f}",
             f"{target['transaction_mobile_percentage_sp_time'] if (is_bit_set(policy['smf72prf'],8,5) or is_bit_set(policy['smf72prf'],8,4)) and pd.notna(target['transaction_mobile_percentage_sp_time']) else 'N/A':{'> 7.2f' if (is_bit_set(policy['smf72prf'],8,5) or is_bit_set(policy['smf72prf'],8,4)) and pd.notna(target['transaction_mobile_percentage_sp_time']) else '>7'}}",
             "Rem Enc", f"{target['foreign_enclave_average']:>6.2f}"],
            ["Ended", f"{target['r723crcp']:>9}",
             "Queued", f"{format_time(queued):>20}",
             "CategoryA", f"{target['transaction_cata_percentage_cp_time']:>7.2f}",
             f"{target['transaction_cata_percentage_sp_on_cp_time']:>7.2f}",
             f"{target['transaction_cata_percentage_sp_time'] if (is_bit_set(policy['smf72prf'],8,5) or is_bit_set(policy['smf72prf'],8,4)) and pd.notna(target['transaction_cata_percentage_sp_time']) else 'N/A':{'> 7.2f' if (is_bit_set(policy['smf72prf'],8,5) or is_bit_set(policy['smf72prf'],8,4)) and pd.notna(target['transaction_cata_percentage_sp_time']) else '>7'}}",
             "MS Enc ", f"{target['export_enclave_average']:>6.2f}"],
            ["End/s", f"{target['transaction_total_per_second']:>9.2f}",
             "R/S Affin", f"{format_time(rs_affin):>17}",
             "CategoryB", f"{target['transaction_catb_percentage_cp_time']:>7.2f}",
             f"{target['transaction_catb_percentage_sp_on_cp_time']:>7.2f}",
             f"{target['transaction_catb_percentage_sp_time'] if (is_bit_set(policy['smf72prf'],8,5) or is_bit_set(policy['smf72prf'],8,4)) and pd.notna(target['transaction_catb_percentage_sp_time']) else 'N/A':{'> 7.2f' if (is_bit_set(policy['smf72prf'],8,5) or is_bit_set(policy['smf72prf'],8,4)) and pd.notna(target['transaction_catb_percentage_sp_time']) else '>7'}}"],
            ["#Swaps", f"{target['r723cswc']:>8.0f}", "Ineligible", f"{format_time(ineligible):>16}"],
            ["Exctd", f"{target['r723cncp']:>9}", "Conversion",
             f"{format_time(jcl_time_mean):>16}"],
            ["", "", "Std Dev",
             f"{format_time(std_dev) if pd.notna(target['transaction_average_elapsed_time_std_dev']) else 'N/A':>19}"]]

        transaction_table2 = [
            ["IOC", f"{target['r723cioc']:>.0f}",
             "CPU", f"{target['tcbtime_insec']:>.3f}",
             "CP", f"{target['appl_percentage_cp_time']:>.2f}",
             "Blk", f"{target['r723tpdp']:>.3f}",
             "SSCHRT", f"{target['start_subchannel_rate']:>.1f}",
             "Avg", f"{storage_avg:>.2f}",
             "Single", f"{target['single_page_in_rate']:>.1f}"],
            ["CPU", f"{target['r723ccpu']:>.0f}",
             "SRB", f"{target['srbtime_insec']:>.3f}",
             "IIPCP", f"{target['appl_percentage_iipcp_time']:>.2f}",
             "Enq", f"{target['r723ectc']:>.3f}",
             "Resp", f"{target['avg_dasd_response_time'] * 1000:>.1f}",
             "Total", f"{target['storage_total_swapped_in']:>.2f}",
             "Block", f"{target['block_page_in_rate']:>.1f}"],
            ["MSO", f"{target['r723cmso']:>.0f}",
             "RCT", f"{target['r723crct']:>.3f}",
             "IIP",
             f"{target['appl_percentage_iip_time'] if is_bit_set(policy['smf72prf'],8,5) else 'N/A':{'>.2f' if is_bit_set(policy['smf72prf'],8,5) else '>'}}",
             "CRM", f"{target['r723cpdp']:>.3f}",
             "Conn", f"{target['avg_dasd_connect_time'] * 1000:>.1f}",
             "Shared", f"{target['r723csrs'] / policy['smf72int']:>.2f}",
             "Shared", f"{target['shared_page_in_rate']:>.1f}"],
            ["SRB", f"{target['r723csrb']:>.0f}",
             "IIT", f"{target['r723ciit']:>.3f}",
             "AAPCP", f"{target['appl_percentage_aapcp_time']:>.2f}",
             "Lck", f"{target['r723lpdp']:>.3f}",
             "Disc", f"{target['avg_dasd_disconnect_time'] * 1000:>.1f}",
             "", "",
             "HSP", f"{target['hsp_page_in_rate']:>.1f}"],
            ["Tot", f"{target['r723csrv']:>.0f}",
             "HST", f"{target['r723chst']:>.3f}",
             "AAP",
             f"{target['appl_percentage_aap_time'] if is_bit_set(policy['smf72prf'],8,4) else 'N/A':{'>.2f' if is_bit_set(policy['smf72prf'],8,4) else '>'}}",
             "Sup", f"{target['r723spdp']:>.3f}",
             "Q+Pend", f"{target['avg_dasd_pending_time'] * 1000:>.1f}"],
            ["/Sec", f"{target['r723csrv'] / policy['smf72int']:>.0f}",
             "IIP", f"{target['iiptime_insec'] if is_bit_set(policy['smf72prf'],8,5) else 'N/A':{'>.3f' if is_bit_set(policy['smf72prf'],8,5) else '>'}}",
             "", "", "", "", "IOSQ", f"{target['avg_dasd_ios_queue_time'] * 1000:>.1f}"],
            ["Absrptn", f"{target['absorption_rate']:>.0f}",
             "AAP",
             f"{target['aaptime_insec'] if is_bit_set(policy['smf72prf'],8,4) else 'N/A':{'>.3f' if is_bit_set(policy['smf72prf'],8,4) else ':>'}}"],
            ["Trx Serv", f"{target['transaction_service_rate']:>.0f}"]]
        transaction_detail += \
            tb.tabulate(transaction_table1, disable_numparse=True,
                        headers=["<-", "Transactions->", "<Trans-Time", "HH.MM.SS.FFFFFF>",
                                 "<Trans Appl%", "---CP", "-IIPCP/AAPCP",
                                 "-IIP/AAP>", "<---", "Enclaves-->"],
                        colalign=('left', 'right', 'left', 'right', 'left', 'right', 'right', 'right', 'left', 'right'),
                        floatfmt=('', '.2f', '', '', '', '.2f', '.2f', '.2f', '', '.2f')) + '\n' + \
            tb.tabulate(transaction_table2,  # tablefmt='plain',
                        headers=["<-----", "Service->", "<--", "Service Time->", "<---", "Appl%->", "<---",
                                 "Promoted->",
                                 "<---", "DASD I/O->", "<---", "Storage->", "<---", "Page In Rates>"],
                        colalign=('left', 'right', 'left', 'right', 'left', 'right', 'left', 'right',
                                  'left', 'right', 'left', 'right', 'left', 'right',),
                        floatfmt=('', '.0f', '', '.3f', '', '.2f', '', '.3f', '', '.1f', '', '.2f', '', '.1f')) + '\n'

        sc_being_served = format_service_class_being_served(ssss)
        if pd.notna(sc_being_served):
            transaction_detail += sc_being_served

    else:
        transaction_detail += "  - All Data Zero - \n"

    return transaction_detail


def format_goal_and_response_lpar(scs, pro, rts):
    if scs['is_report_class']:
        return None

    response_time_sid = 'N/A'

    response_line = []
    if is_bit_set(scs['r723crs1'],8,0): #scs['is_heterogeneous']:
        response_line = ["Goal:", "N/A"]
    else:
        if scs['class_goal_type'] == 'Execution Velocity':
            if (scs['r723ccus'] + scs['r723ccde']) > 0:
                io_mgmt = scs['r723ctou'] / (scs['r723ctou'] + scs['r723ccde'])
            else:
                io_mgmt = 0
            if (scs['r723ctou'] + scs['r723ctdq']) > 0:
                init_mgmt = scs['r723ctou'] / (scs['r723ctou'] + scs['r723ctdq'])
            else:
                init_mgmt = 0
            response_line = ["Goal:", f"Execution Velocity {scs['r723cval'] / 100:>.1%}", "  ",
                             "Velocity Migration:", f"  I/O Mgnt {io_mgmt:>.1%}",
                             f"Init Mgmt {init_mgmt:>.1%}"]

        elif scs['class_goal_type'] in ('Percentile Resp. Time', 'Average Resp. Time'):

            if scs['response_time_millisec']:
                response_time = scs['r723cval'] * 0.001
            elif scs['response_time_seconds']:
                response_time = scs['r723cval']
            elif scs['response_time_minutes']:
                response_time = scs['r723cval'] * 60
            elif scs['response_time_hours']:
                response_time = scs['r723cval'] * 3600
            else:
                response_time = None
            (rtime_hr, rtime_min, rtime_sec, rtime_milli) = hr_min_sec_milli(pd.to_timedelta(response_time, unit='s'))
            if scs['class_goal_type'] == 'Percentile Resp. Time':
                response_line = ["Goal:",
                                 f"Response Time {rtime_hr:03}.{rtime_min:02}.{rtime_sec:02}.{rtime_milli:03} For {scs['r723cpct'] / 100:.0%}"]
                if scs['r723ctet'] > 0 and pd.notna(rts):
                    sid_response_time = (rts['class_rt_bucket_1'] + rts['class_rt_bucket_2'] + rts[
                        'class_rt_bucket_3'] + rts['class_rt_bucket_4'] + rts['class_rt_bucket_5'] + rts[
                                             'class_rt_bucket_6']) / scs['r723crcp'] * 100
                    response_time_sid = f"{sid_response_time:{'>6.1f' if sid_response_time < 100 else '>6.0f'}}"
                else:
                    response_time_sid = "   0.0"
            elif scs['class_goal_type'] == 'Average Resp. Time':
                if scs['r723crcp'] > 0:
                    if pd.notna(scs['r723ctetx']):
                        response_time_sid = f"{scs['r723ctetx'] / scs['r723crcp']:>6.1f}"
                    else:
                        response_time_sid = f"{scs['r723ctet'] / scs['r723crcp']:>6.1f}"
                else:
                    response_time_sid = "   0.0"
                response_line = ["Goal:", f"Response Time {rtime_hr:03}.{rtime_min:02}.{rtime_sec:02}.{rtime_milli:03}"]
        else:
            response_line = ["Goal:", f"{scs['class_goal_type']}"]
    top_cols_dict = {0: 'Delays', 1: '%', 2: '', 3: '', 4: '', 5: '', 6: '>\n\n'}
    top_scs_vals = {0: '', 1: '', 2: '', 3: '', 4: '', 5: '', 6: ''}
    aapusgp = f"{scs['r723ifau'] / scs['r723ctsa'] * 100 if scs['r723ctsa'] > 0 else 0:>4.1f}"
    iipusgp = f"{scs['r723supu'] / scs['r723ctsa'] * 100 if scs['r723ctsa'] > 0 else 0:>4.1f}"
    if scs['r723ctsa'] > 0:
        delay_list = []
        if scs['r723ccde'] / scs['r723ctsa'] * 100 >= 0.05:
            delay_list.append(('CPU', scs['r723ccde'] / scs['r723ctsa'] * 100))
        if scs['r723ifad'] / scs['r723ctsa'] * 100 >= 0.05:
            delay_list.append(('AAP', scs['r723ifad'] / scs['r723ctsa'] * 100))
        if scs['r723supd'] / scs['r723ctsa'] * 100 >= 0.05:
            delay_list.append(('IIP', scs['r723supd'] / scs['r723ctsa'] * 100))
        if scs['r723ciod'] / scs['r723ctsa'] * 100 >= 0.05:
            delay_list.append(('I/O', scs['r723ciod'] / scs['r723ctsa'] * 100))
        if scs['r723ccca'] / scs['r723ctsa'] * 100 >= 0.05:
            delay_list.append(('Cap', scs['r723ccca'] / scs['r723ctsa'] * 100))
        if scs['r723cswi'] / scs['r723ctsa'] * 100 >= 0.05:
            delay_list.append(('Sin', scs['r723cswi'] / scs['r723ctsa'] * 100))
        if scs['r723cmpl'] / scs['r723ctsa'] * 100 >= 0.05:
            delay_list.append(('Mpl', scs['r723cmpl'] / scs['r723ctsa'] * 100))
        if scs['r723cq'] / scs['r723ctsa'] * 100 >= 0.05:
            delay_list.append(('Q Mpl', scs['r723cq'] / scs['r723ctsa'] * 100))
        if scs['r723cspv'] / scs['r723ctsa'] * 100 >= 0.05:
            delay_list.append(('Srv Prv', scs['r723cspv'] / scs['r723ctsa'] * 100))
        if scs['r723csvi'] / scs['r723ctsa'] * 100 >= 0.05:
            delay_list.append(('Srv Vio', scs['r723csvi'] / scs['r723ctsa'] * 100))
        if scs['r723cshs'] / scs['r723ctsa'] * 100 >= 0.05:
            delay_list.append(('Srv Shs', scs['r723cshs'] / scs['r723ctsa'] * 100))
        if scs['r723cssw'] / scs['r723ctsa'] * 100 >= 0.05:
            delay_list.append(('Srv Sin', scs['r723cssw'] / scs['r723ctsa'] * 100))
        if scs['r723csmp'] / scs['r723ctsa'] * 100 >= 0.05:
            delay_list.append(('Srv Mpl', scs['r723csmp'] / scs['r723ctsa'] * 100))
        if scs['r723capr'] / scs['r723ctsa'] * 100 >= 0.05:
            delay_list.append(('Aux Prv', scs['r723capr'] / scs['r723ctsa'] * 100))
        if scs['r723caco'] / scs['r723ctsa'] * 100 >= 0.05:
            delay_list.append(('Aux Com', scs['r723caco'] / scs['r723ctsa'] * 100))
        if scs['r723caxm'] / scs['r723ctsa'] * 100 >= 0.05:
            delay_list.append(('Aux Xme', scs['r723caxm'] / scs['r723ctsa'] * 100))
        if scs['r723cvio'] / scs['r723ctsa'] * 100 >= 0.05:
            delay_list.append(('Aux Vio', scs['r723cvio'] / scs['r723ctsa'] * 100))
        if scs['r723chsp'] / scs['r723ctsa'] * 100 >= 0.05:
            delay_list.append(('Aux Shs', scs['r723chsp'] / scs['r723ctsa'] * 100))
        if scs['r723cchs'] / scs['r723ctsa'] * 100 >= 0.05:
            delay_list.append(('Aux Ehs', scs['r723cchs'] / scs['r723ctsa'] * 100))
        if len(delay_list) > 0:
            sorted_delay_list = sorted(delay_list, key=itemgetter(1), reverse=True)
            for delay_idx, delay in enumerate(sorted_delay_list):
                if delay_idx < 7:
                    top_scs_vals[delay_idx] = delay[1]
                    if len(delay[0]) == 7:
                        if 6 > delay_idx > 1:
                            top_cols_dict[delay_idx] = '\n' + f"{delay[0][0:3]:>4}" + '\n' + f"{delay[0][4:]:>4}"
                        elif delay_idx < 6:
                            top_cols_dict[delay_idx] += ('\n' + f"{delay[0][0:3]:>4}" + '\n' + f"{delay[0][4:]:>4}")
                        else:
                            top_cols_dict[delay_idx] = '>\n' + f"{delay[0][0:3]:>4}" + '\n' + f"{delay[0][4:]:>4}"
                    elif len(delay[0]) > 3:
                        if 6 > delay_idx > 1:
                            top_cols_dict[delay_idx] = '\n' + f"{delay[0][0]:>4}" + '\n' + f"{delay[0][2:]:>4}"
                        elif delay_idx < 6:
                            top_cols_dict[delay_idx] += ('\n' + f"{delay[0][0]:>4}" + '\n' + f"{delay[0][2:]:>4}")
                        else:
                            top_cols_dict[delay_idx] = '>\n' + f"{delay[0][0]:>4}" + '\n' + f"{delay[0][2:]:>4}"
                    else:
                        if 6 > delay_idx > 1:
                            top_cols_dict[delay_idx] = '\n\n' + f"{delay[0][0:3]:>4}"
                        elif delay_idx < 6:
                            top_cols_dict[delay_idx] += ('\n\n' + f"{delay[0][0:3]:>4}")
                        else:
                            top_cols_dict[delay_idx] = '>\n\n' + f"{delay[0][0:3]:>4}"

    response_table = [
        [f"{scs['smf72sid']:<4}", f"{response_time_sid:>7}", f"{scs['execution_velocity']:>4.1f}",
         f"{scs['performance_index'] if 0 < scs['performance_index'] <= 4 else '****' if scs['performance_index'] > 0 else ' ':{'> 4.1f' if 0 > scs['performance_index'] <= 4 else '>4'}}",
         f"{scs['transaction_address_space_percentage']:>5.1f}",
         f"{scs['r723ccus'] / scs['r723ctsa'] * 100 if scs['r723ctsa'] > 0 else 0:>4.1f}",
         f"{aapusgp if is_bit_set(pro['smf72prf'],8,4) else 'N/A':>4}", f"{iipusgp if is_bit_set(pro['smf72prf'],8,5) else 'N/A':>4}",
         f"{scs['r723ciou'] / scs['r723ctsa'] * 100 if scs['r723ctsa'] > 0 else 0:>4.1f}",
         f"{scs['r723ccde'] / scs['r723ctsa'] * 100 if scs['r723ctsa'] > 0 else 0:>4.1f}",
         f"{top_scs_vals[0]}", f"{top_scs_vals[1]}", f"{top_scs_vals[2]}",
         f"{top_scs_vals[3]}", f"{top_scs_vals[4]}", f"{top_scs_vals[5]}",
         f"{top_scs_vals[6]}",
         f"{scs['r723apu'] / scs['r723ctsa'] * 100 if scs['r723ctsa'] > 0 else 0:>4.1f}",
         f"{scs['r723rcou'] / scs['r723ctsa'] * 100 if scs['r723ctsa'] > 0 else 0:>4.1f}",
         f"{scs['r723cunk'] / scs['r723ctsa'] * 100 if scs['r723ctsa'] > 0 else 0:>4.1f}",
         f"{scs['r723cidl'] / scs['r723ctsa'] * 100 if scs['r723ctsa'] > 0 else 0:>4.1f}",
         f"{scs['r723apd'] / scs['r723ctsa'] * 100 if scs['r723ctsa'] > 0 else 0:>4.1f}",
         f"{scs['r723rcod'] / scs['r723ctsa'] * 100 if scs['r723ctsa'] > 0 else 0:>4.1f}",
         f"{scs['r723cpqu'] / scs['r723ctsa'] * 100 if scs['r723ctsa'] > 0 else 0:>4.1f}"]
    ]
    return (  # '\n' + #response_code +
            tb.tabulate([tb.SEPARATING_LINE, response_line, tb.SEPARATING_LINE], tablefmt='plain') + '\n' +
            tb.tabulate(response_table,
                        headers=["\n\nSystem",
                                 f"Response\nTime\n{'Actual%' if scs['class_goal_type'] in ('Percentile Resp. Time', 'Average Resp. Time') else ' '}",
                                 "\nEx  \nVel%", "\nPerf\nIndx", "\n Avg \nAdrsp",
                                 "\n<--\nCPU", "\nExec\nAAP", "\nUsing\nIIP", "\n%->\nI/O",
                                 "<Exec\n\nTot", top_cols_dict[0], top_cols_dict[1], top_cols_dict[2], top_cols_dict[3],
                                 top_cols_dict[4], top_cols_dict[5], top_cols_dict[6],
                                 "\n<--\nCry", "Using\n % >\nCnt",
                                 "\n<--\nUnk", "\nDelay\nIdl", "\n%  \nCry", "\n-->\nCnt", "\n%\nQui"],
                        colalign=('left', 'center', 'right', 'right', 'right', 'right', 'right', 'right', 'right',
                                  # 'left',
                                  'right', 'right', 'right', 'right', 'right', 'right', 'right'
                                                                                        'right', 'right', 'right',
                                  'right', 'right', 'right', 'right'),
                        floatfmt=('', '', '.1f', '.1f', '.1f', '.1f', '.1f', '.1f', '.1f',  # '',
                                  '.1f', '.1f', '.1f', '.1f', '.1f', '.1f', '.1f',
                                  '.1f', '.1f',
                                  '.1f', '.1f', '.1f', '.1f', '.1f')) + '\n')


def format_goal_and_response_sysplex(wms, scss, pro):
    if wms['is_report_class']:
        return None

    if wms['r723crcp'] == 0:
        return None
    # if wms.__class__.__name__ == 'Smf72WmsHr':
    #     scss = wms.smf72_scs_hrs
    # elif wms.__class__.__name__ == 'Smf72WmsDa':
    #     scss = wms.smf72_scs_das
    # else:  # wms.__class__.__name__ == 'Smf72Wms':
    #     scss = wms.smf72_scss

    response_line = []
    response_time_sid = 'N/A'
    if wms['is_heterogeneous']:
        response_line = ["Goal:", "N/A"]
    else:
        if wms['class_goal_type'] == 'Execution Velocity':
            if wms['velocity_io_delays']:  # delays used
                io_mgmt = wms['execution_velocity']
                init_mgmt = wms['execution_velocity']
            elif wms['r723ccus'] > 0:
                io_mgmt = (wms['r723ccus'] * 100) / (wms['r723ccus'] + wms['r723ccde'])
                init_mgmt = io_mgmt
            else:
                io_mgmt = 0
                init_mgmt = 0
            response_line = ["Goal:", f"Execution Velocity {wms['r723cval'] / 100:>.1%}", "  ",
                             "Velocity Migration:", f"  I/O Mgnt {io_mgmt:>.1%}",
                             f"Init Mgmt {init_mgmt:>.1%}"]
        elif wms['class_goal_type'] in ('Percentile Resp. Time', 'Average Resp. Time'):
            if wms['response_time_millisec']:
                response_time = wms['r723cval'] * 0.001
            elif wms['response_time_seconds']:
                response_time = wms['r723cval']
            elif wms['response_time_minutes']:
                response_time = wms['r723cval'] * 60
            elif wms['response_time_hours']:
                response_time = wms['r723cval'] * 3600
            else:
                response_time = None

            (rtime_hr, rtime_min, rtime_sec, rtime_milli) = hr_min_sec_milli(pd.to_timedelta(response_time, unit='s'))
            if wms['class_goal_type'] == 'Percentile Resp. Time':
                response_line = ["Goal:",
                                 f"Response Time {rtime_hr:03}.{rtime_min:02}.{rtime_sec:02}.{rtime_milli:03} For {wms['r723cpct'] / 100:.0%}"]
            elif wms['class_goal_type'] == 'Average Resp. Time':
                response_line = ["Goal:", f"Response Time {rtime_hr:03}.{rtime_min:02}.{rtime_sec:02}.{rtime_milli:03}"]
        else:
            response_line = ["Goal:", f"{wms['class_goal_type']}"]
    delay_list = []
    sorted_delay_list = []
    top_cols_dict = {0: 'Delays', 1: '%', 2: '', 3: '', 4: '', 5: '', 6: '>\n\n'}
    top_all_values = {0: '', 1: '', 2: '', 3: '', 4: '', 5: '', 6: ''}
    response_time_all = '--N/A--'
    if wms['r723ctsa'] > 0:
        if wms['r723ccde'] / wms['r723ctsa'] * 100 >= 0.05:
            delay_list.append(('CPU', wms['r723ccde'] / wms['r723ctsa'] * 100))
        if wms['r723ifad'] / wms['r723ctsa'] * 100 >= 0.05:
            delay_list.append(('AAP', wms['r723ifad'] / wms['r723ctsa'] * 100))
        if wms['r723supd'] / wms['r723ctsa'] * 100 >= 0.05:
            delay_list.append(('IIP', wms['r723supd'] / wms['r723ctsa'] * 100))
        if wms['r723ciod'] / wms['r723ctsa'] * 100 >= 0.05:
            delay_list.append(('I/O', wms['r723ciod'] / wms['r723ctsa'] * 100))
        if wms['r723ccca'] / wms['r723ctsa'] * 100 >= 0.05:
            delay_list.append(('Cap', wms['r723ccca'] / wms['r723ctsa'] * 100))
        if wms['r723cswi'] / wms['r723ctsa'] * 100 >= 0.05:
            delay_list.append(('Sin', wms['r723cswi'] / wms['r723ctsa'] * 100))
        if wms['r723cmpl'] / wms['r723ctsa'] * 100 >= 0.05:
            delay_list.append(('Mpl', wms['r723cmpl'] / wms['r723ctsa'] * 100))
        if wms['r723cq'] / wms['r723ctsa'] * 100 >= 0.05:
            delay_list.append(('Q Mpl', wms['r723cq'] / wms['r723ctsa'] * 100))
        if wms['r723cspv'] / wms['r723ctsa'] * 100 >= 0.05:
            delay_list.append(('Srv Prv', wms['r723cspv'] / wms['r723ctsa'] * 100))
        if wms['r723csvi'] / wms['r723ctsa'] * 100 >= 0.05:
            delay_list.append(('Srv Vio', wms['r723csvi'] / wms['r723ctsa'] * 100))
        if wms['r723cshs'] / wms['r723ctsa'] * 100 >= 0.05:
            delay_list.append(('Srv Shs', wms['r723cshs'] / wms['r723ctsa'] * 100))
        if wms['r723cssw'] / wms['r723ctsa'] * 100 >= 0.05:
            delay_list.append(('Srv Sin', wms['r723cssw'] / wms['r723ctsa'] * 100))
        if wms['r723csmp'] / wms['r723ctsa'] * 100 >= 0.05:
            delay_list.append(('Srv Mpl', wms['r723csmp'] / wms['r723ctsa'] * 100))
        if wms['r723capr'] / wms['r723ctsa'] * 100 >= 0.05:
            delay_list.append(('Aux Prv', wms['r723capr'] / wms['r723ctsa'] * 100))
        if wms['r723caco'] / wms['r723ctsa'] * 100 >= 0.05:
            delay_list.append(('Aux Com', wms['r723caco'] / wms['r723ctsa'] * 100))
        if wms['r723caxm'] / wms['r723ctsa'] * 100 >= 0.05:
            delay_list.append(('Aux Xme', wms['r723caxm'] / wms['r723ctsa'] * 100))
        if wms['r723cvio'] / wms['r723ctsa'] * 100 >= 0.05:
            delay_list.append(('Aux Vio', wms['r723cvio'] / wms['r723ctsa'] * 100))
        if wms['r723chsp'] / wms['r723ctsa'] * 100 >= 0.05:
            delay_list.append(('Aux Shs', wms['r723chsp'] / wms['r723ctsa'] * 100))
        if wms['r723cchs'] / wms['r723ctsa'] * 100 >= 0.05:
            delay_list.append(('Aux Ehs', wms['r723cchs'] / wms['r723ctsa'] * 100))
        if len(delay_list) > 0:
            sorted_delay_list = sorted(delay_list, key=itemgetter(1), reverse=True)
            for delay_idx, delay in enumerate(sorted_delay_list):
                top_all_values[delay_idx] = delay[1]
                if delay_idx < 7:
                    if len(delay[0]) == 7:
                        if 6 > delay_idx > 1:
                            top_cols_dict[delay_idx] = '\n' + f"{delay[0][0:3]:>4}" + '\n' + f"{delay[0][4:]:>4}"
                        elif delay_idx < 6:
                            top_cols_dict[delay_idx] += ('\n' + f"{delay[0][0:3]:>4}" + '\n' + f"{delay[0][4:]:>4}")
                        else:
                            top_cols_dict[delay_idx] = '>\n' + f"{delay[0][0:3]:>4}" + '\n' + f"{delay[0][4:]:>4}"
                    elif len(delay[0]) > 3:
                        if 6 > delay_idx > 1:
                            top_cols_dict[delay_idx] = '\n' + f"{delay[0][0]:>4}" + '\n' + f"{delay[0][2:]:>4}"
                        elif delay_idx < 6:
                            top_cols_dict[delay_idx] += ('\n' + f"{delay[0][0]:>4}" + '\n' + f"{delay[0][2:]:>4}")
                        else:
                            top_cols_dict[delay_idx] = '>\n' + f"{delay[0][0]:>4}" + '\n' + f"{delay[0][2:]:>4}"
                    else:
                        if 6 > delay_idx > 1:
                            top_cols_dict[delay_idx] = '\n\n' + f"{delay[0][0:3]:>4}"
                        elif delay_idx < 6:
                            top_cols_dict[delay_idx] += ('\n\n' + f"{delay[0][0:3]:>4}")
                        else:
                            top_cols_dict[delay_idx] = '>\n\n' + f"{delay[0][0:3]:>4}"

    if not wms['is_heterogeneous']:
        if wms['class_goal_type'] in ('Percentile Resp. Time', 'Average Resp. Time'):
            # if wms['response_time_millisec']:
            #     response_time = wms['r723cval'] * 0.001
            # elif wms['response_time_seconds']:
            #     response_time = wms['r723cval']
            # elif wms['response_time_minutes']:
            #     response_time = wms['r723cval'] * 60
            # elif wms['response_time_hours']:
            #     response_time = wms['r723cval'] * 3600
            # else:
            #     response_time = None
            # (rtime_hr, rtime_min, rtime_sec, rtime_milli) = hr_min_sec_milli(pd.to_timedelta(response_time, unit='s'))
            if wms['class_goal_type'] == 'Average Resp. Time':
                if wms['r723crcp'] > 0:
                    if pd.notna(wms['r723ctetx']):
                        response_time_all = f"{wms['r723ctetx'] / wms['r723crcp']:>6.1f}"
                    else:
                        response_time_all = f"{wms['r723ctet'] / wms['r723crcp']:>6.1f}"
                else:
                    response_time_all = "   0.0"
    interval_list = []
    zaap_inst_list = []
    ziip_inst_list = []
    response_table = []

    for scs in scss:
        # if scs.__class__.__name__ == 'Smf72ScsHr':
        #     pro = scs.smf72_pro_hr
        # elif scs.__class__.__name__ == 'Smf72ScsDa':
        #     pro = scs.smf72_pro_da
        # else:  # scs.__class__.__name__ == 'Smf72Scs':
        #     pro = scs.smf72_pro
        interval_list.append(pro['smf72int'])
        zaap_inst_list.append(is_bit_set(pro['smf72prf'],8,4))
        ziip_inst_list.append(is_bit_set(pro['smf72prf'],8,5))
        top_scs_vals = {0: '', 1: '', 2: '', 3: '', 4: '', 5: '', 6: ''}
        aapusgp = f"{scs['r723ifau'] / scs['r723ctsa'] * 100 if scs['r723ctsa'] > 0 else 0:>4.1f}"
        iipusgp = f"{scs['r723supu'] / scs['r723ctsa'] * 100 if scs['r723ctsa'] > 0 else 0:>4.1f}"
        if scs['r723ctsa'] > 0:
            if len(delay_list) > 0:
                for delay_idx, delay in enumerate(sorted_delay_list):
                    if delay[0] == 'CPU':
                        top_scs_vals[
                            delay_idx] = f"{scs['r723ccde'] / scs['r723ctsa'] * 100 if scs['r723ctsa'] > 0 else 0:>4.1f}"
                    elif delay[0] == 'AAP':
                        top_scs_vals[
                            delay_idx] = f"{scs['r723ifad'] / scs['r723ctsa'] * 100 if scs['r723ctsa'] > 0 else 0:>4.1f}"
                    elif delay[0] == 'IIP':
                        top_scs_vals[
                            delay_idx] = f"{scs['r723supd'] / scs['r723ctsa'] * 100 if scs['r723ctsa'] > 0 else 0:>4.1f}"
                    elif delay[0] == 'I/O':
                        top_scs_vals[
                            delay_idx] = f"{scs['r723ciod'] / scs['r723ctsa'] * 100 if scs['r723ctsa'] > 0 else 0:>4.1f}"
                    elif delay[0] == 'Cap':
                        top_scs_vals[
                            delay_idx] = f"{scs['r723ccca'] / scs['r723ctsa'] * 100 if scs['r723ctsa'] > 0 else 0:>4.1f}"
                    elif delay[0] == 'Sin':
                        top_scs_vals[
                            delay_idx] = f"{scs['r723cswi'] / scs['r723ctsa'] * 100 if scs['r723ctsa'] > 0 else 0:>4.1f}"
                    elif delay[0] == 'Mpl':
                        top_scs_vals[
                            delay_idx] = f"{scs['r723cmpl'] / scs['r723ctsa'] * 100 if scs['r723ctsa'] > 0 else 0:>4.1f}"
                    elif delay[0] == 'Q Mpl':
                        top_scs_vals[
                            delay_idx] = f"{scs['r723cq'] / scs['r723ctsa'] * 100 if scs['r723ctsa'] > 0 else 0:>4.1f}"
                    elif delay[0] == 'Srv Prv':
                        top_scs_vals[
                            delay_idx] = f"{scs['sample_server_prv_delay'] / scs['r723ctsa'] * 100 if scs['r723ctsa'] > 0 else 0:>4.1f}"
                    elif delay[0] == 'Srv Vio':
                        top_scs_vals[
                            delay_idx] = f"{scs['sample_server_vio_delay'] / scs['r723ctsa'] * 100 if scs['r723ctsa'] > 0 else 0:>4.1f}"
                    elif delay[0] == 'Srv Shs':
                        top_scs_vals[
                            delay_idx] = f"{scs['r723cshs'] / scs['r723ctsa'] * 100 if scs['r723ctsa'] > 0 else 0:>4.1f}"
                    elif delay[0] == 'Srv Sin':
                        top_scs_vals[
                            delay_idx] = f"{scs['r723cssw'] / scs['r723ctsa'] * 100 if scs['r723ctsa'] > 0 else 0:>4.1f}"
                    elif delay[0] == 'Srv Mpl':
                        top_scs_vals[
                            delay_idx] = f"{scs['r723csmp'] / scs['r723ctsa'] * 100 if scs['r723ctsa'] > 0 else 0:>4.1f}"
                    elif delay[0] == 'Aux Prv':
                        top_scs_vals[
                            delay_idx] = f"{scs['r723capr'] / scs['r723ctsa'] * 100 if scs['r723ctsa'] > 0 else 0:>4.1f}"
                    elif delay[0] == 'Aux Com':
                        top_scs_vals[
                            delay_idx] = f"{scs['r723caco'] / scs['r723ctsa'] * 100 if scs['r723ctsa'] > 0 else 0:>4.1f}"
                    elif delay[0] == 'Aux Xme':
                        top_scs_vals[
                            delay_idx] = f"{scs['r723caxm'] / scs['r723ctsa'] * 100 if scs['r723ctsa'] > 0 else 0:>4.1f}"
                    elif delay[0] == 'Aux Vio':
                        top_scs_vals[
                            delay_idx] = f"{scs['r723cvio'] / scs['r723ctsa'] * 100 if scs['r723ctsa'] > 0 else 0:>4.1f}"
                    elif delay[0] == 'Aux Shs':
                        top_scs_vals[
                            delay_idx] = f"{scs['r723chsp'] / scs['r723ctsa'] * 100 if scs['r723ctsa'] > 0 else 0:>4.1f}"
                    elif delay[0] == 'Aux Ehs':
                        top_scs_vals[
                            delay_idx] = f"{scs['r723cchs'] / scs['r723ctsa'] * 100 if scs['r723ctsa'] > 0 else 0:>4.1f}"

            response_time_sid = '   '
            if not scs['is_heterogeneous']:
                if scs['class_goal_type'] in ('Percentile Resp. Time', 'Average Resp. Time'):
                    # if scs['response_time_millisec']:
                    #     response_time = scs['r723cval'] * 0.001
                    # elif scs['response_time_seconds']:
                    #     response_time = scs['r723cval']
                    # elif scs['response_time_minutes']:
                    #     response_time = scs['r723cval'] * 60
                    # elif scs['response_time_hours']:
                    #     response_time = scs['r723cval'] * 3600
                    # else:
                    #     response_time = None
                    # (rtime_hr, rtime_min, rtime_sec, rtime_milli) = hr_min_sec_milli(
                    #     pd.to_timedelta(response_time, unit='s'))
                    if scs['class_goal_type'] == 'Average Resp. Time':
                        if scs['r723crcp'] > 0:
                            if pd.notna(scs['r723ctetx']):
                                response_time_sid = f"{scs['r723ctetx'] / scs['r723crcp']:>6.1f}"
                            else:
                                response_time_sid = f"{scs['r723ctet'] / scs['r723crcp']:>6.1f}"
                        else:
                            response_time_sid = "   0.0"
        response_table_line = \
            [f"{scs['smf72sid']:<4}", f"{response_time_sid:>7}", f"{scs['execution_velocity']:>4.1f}",
             f"{scs['performance_index']:>4.1f}", f"{scs['transaction_address_space_percentage']:>5.1f}",
             f"{scs['r723ccus'] / scs['r723ctsa'] * 100 if scs['r723ctsa'] > 0 else 0:>4.1f}",
             f"{aapusgp if is_bit_set(pro['smf72prf'],8,4) else 'N/A':>4}", f"{iipusgp if is_bit_set(pro['smf72prf'],8,5) else 'N/A':>4}",
             f"{scs['r723ciou'] / scs['r723ctsa'] * 100 if scs['r723ctsa'] > 0 else 0:>4.1f}",
             f"{scs['r723ctdq'] / scs['r723ctsa'] * 100 if scs['r723ctsa'] > 0 else 0:>4.1f}",  # {value_7}",
             f"{top_scs_vals[0]}", f"{top_scs_vals[1]}", f"{top_scs_vals[2]}",
             f"{top_scs_vals[3]}", f"{top_scs_vals[4]}", f"{top_scs_vals[5]}",
             f"{top_scs_vals[6]}",
             f"{scs['r723apu'] / scs['r723ctsa'] * 100 if scs['r723ctsa'] > 0 else 0:>4.1f}",
             f"{scs['r723rcou'] / scs['r723ctsa'] * 100 if scs['r723ctsa'] > 0 else 0:>4.1f}",
             f"{scs['r723cunk'] / scs['r723ctsa'] * 100 if scs['r723ctsa'] > 0 else 0:>4.1f}",
             f"{scs['r723cidl'] / scs['r723ctsa'] * 100 if scs['r723ctsa'] > 0 else 0:>4.1f}",
             f"{scs['r723apd'] / scs['r723ctsa'] * 100 if scs['r723ctsa'] > 0 else 0:>4.1f}",
             f"{scs['r723rcod'] / scs['r723ctsa'] * 100 if scs['r723ctsa'] > 0 else 0:>4.1f}",
             f"{scs['r723cpqu'] / scs['r723ctsa'] * 100 if scs['r723ctsa'] > 0 else 0:>4.1f}"]
        response_table.append(response_table_line)

    aapusgp_all = f"{wms['r723ifau'] / wms['r723ctsa'] * 100 if wms['r723ctsa'] > 0 else 0:>4.1f}"
    iipusgp_all = f"{wms['r723supu'] / wms['r723ctsa'] * 100 if wms['r723ctsa'] > 0 else 0:>4.1f}"
    response_table.append(
        ["*All", f"{response_time_all:>7}", f"{wms['execution_velocity']:>4.1f}",
         f"{wms['performance_index']:>4.1f}", f"{wms['r723csac'] / wms['r723mtv_']:>5.1f}",
         f"{wms['r723ccus'] / wms['r723ctsa'] * 100 if wms['r723ctsa'] > 0 else 0:>4.1f}",
         f"{aapusgp_all if max(zaap_inst_list) == 1 else 'N/A':>4}",
         f"{iipusgp_all if max(ziip_inst_list) == 1 else 'N/A':>4}",
         f"{wms['r723ciou'] / wms['r723ctsa'] * 100 if wms['r723ctsa'] > 0 else 0:>4.1f}",
         f"{wms['r723ctdq'] / wms['r723ctsa'] * 100 if wms['r723ctsa'] > 0 else 0:>4.1f}",  # {value_7_all}",
         f"{top_all_values[0]}", f"{top_all_values[1]}", f"{top_all_values[2]}",
         f"{top_all_values[3]}", f"{top_all_values[4]}", f"{top_all_values[5]}",
         f"{top_all_values[6]}",
         f"{wms['r723apu'] / wms['r723ctsa'] * 100 if wms['r723ctsa'] > 0 else 0:>4.1f}",
         f"{wms['r723rcou'] / wms['r723ctsa'] * 100 if wms['r723ctsa'] > 0 else 0:>4.1f}",
         f"{wms['r723cunk'] / wms['r723ctsa'] * 100 if wms['r723ctsa'] > 0 else 0:>4.1f}",
         f"{wms['r723cidl'] / wms['r723ctsa'] * 100 if wms['r723ctsa'] > 0 else 0:>4.1f}",
         f"{wms['r723apd'] / wms['r723ctsa'] * 100 if wms['r723ctsa'] > 0 else 0:>4.1f}",
         f"{wms['r723rcod'] / wms['r723ctsa'] * 100 if wms['r723ctsa'] > 0 else 0:>4.1f}",
         f"{wms['r723cpqu'] / wms['r723ctsa'] * 100 if wms['r723ctsa'] > 0 else 0:>4.1f}"]
    )
    return (tb.tabulate([tb.SEPARATING_LINE, response_line, tb.SEPARATING_LINE], tablefmt='plain') + '\n' +
            tb.tabulate(response_table,
                        headers=["\n\nSystem",
                                 f"Response\nTime\n{'Actual%' if scss[-1]['class_goal_type'] in ('Percentile Resp. Time', 'Average Resp. Time') else ' '}",
                                 "\nEx  \nVel%", "\nPerf\nIndx", "\n Avg \nAdrsp",
                                 "\n<--\nCPU", "\nExec\nAAP", "\nUsing\nIIP", "\n%->\nI/O",
                                 "<Exec\n\nTot", top_cols_dict[0], top_cols_dict[1], top_cols_dict[2], top_cols_dict[3],
                                 top_cols_dict[4], top_cols_dict[5], top_cols_dict[6],
                                 "\n<--\nCry", "Using\n % >\nCnt",
                                 "\n<--\nUnk", "\nDelay\nIdl", "\n%  \nCry", "\n-->\nCnt", "\n%\nQui"],
                        colalign=(
                            'left', 'center', 'right', 'right', 'right', 'right', 'right', 'right', 'right',
                            'right', 'right', 'right', 'right', 'right', 'right', 'right',
                            'right', 'right', 'right', 'right', 'right', 'right', 'right'),
                        floatfmt=('', '', '.1f', '.1f', '.1f', '.1f', '.1f', '.1f', '.1f',
                                  '.1f', '.1f', '.1f', '.1f', '.1f', '.1f', '.1f', '.1f',
                                  '.1f', '.1f',
                                  '.1f', '.1f', '.1f', '.1f', '.1f')) + '\n')


def format_sdelay_header(duration, sctl, pro):
    if duration == 'Hourly':
        report_date = sctl['date']
        report_time = sctl['datetime'].time().strftime('%H.%M.%S')
        interval = format_s2min(pro['smf72int'])
    elif duration == 'Daily':
        report_date = sctl['date']
        report_time = '00.00.00'
        interval = format_s2min(pro['smf72int'])
    else:
        report_date = sctl['smf72ist'].date()
        report_time = sctl['smf72ist'].time().strftime('%H.%M.%S')
        interval = format_s2min(pro['smf72int'])
    zos_ver = 'V' + pro['smf72mvs'][2:4].lstrip('0') + 'R' + pro['smf72mvs'][4:6].lstrip('0')
    interval_x = f"{interval[:-3]}"
    whitespace = ' '
    header1 = [["                                           S E R I A L I Z A T I I N     D E L A Y     R E P O R T"]]
    header2 = [
        [f"{whitespace:>12}", f"z/OS {zos_ver}", f"{whitespace:>13}", f"System ID {pro['smf72sid']}", f"{whitespace:>6}",
         f"Date {report_date:%m/%d/%Y}", f"{whitespace:>11}", f"Interval {interval_x}"],
        ["", "", "", f"RMF Version {pro['smf72mfv']:<5}", "", f"Time {report_time}", "",
         f"Cycle {pro['smf72cyc'] / 1000:5.3f} Seconds"]
    ]
    header3 = [["Serialization Delay Summary"]]
    return tb.tabulate(header1, tablefmt="plain") + "\n" + tb.tabulate(header2, tablefmt="plain") + "\n" + tb.tabulate(
        header3, tablefmt="plain") + "\n"


def cal_std_dev(time_sum_sq, count, time):
    if count > 1 and pd.notna(time_sum_sq) and pd.notna(time):
        temp = ((count * time_sum_sq) - (time ** 2)) / (count * (count - 1))
        if temp > 0:
            std_dev = math.sqrt(temp)
        else:
            std_dev = 0
    else:
        std_dev = 0
    return std_dev


def dfcal_std_dev(time_sum_sq, count, time):
    if count > 1 and not pd.isna(time_sum_sq) and not pd.isna(time):
        temp = ((count * time_sum_sq) - (time ** 2)) / (count * (count - 1))
        if temp > 0:
            std_dev = math.sqrt(temp)
        else:
            std_dev = 0
    else:
        std_dev = 0
    return std_dev


df_cal_std_dev = np.frompyfunc(dfcal_std_dev, 3, 1)


def format_cms_lock_detail(cmsss, cedss, class_, csmss):
    if len(cmsss) > 0 or len(cedss) > 0 or len(class_) > 0 or len(csmss) > 0:
        df1 = pd.DataFrame.from_records(
            [('CMS', d['r725cmas'], d['r725cmjn'], d['r725cmsn'], d['r725cmsp'], d['r725cmti'], d['r725cmti'],
              d['r725cmsu'], d['r725cmal']) for d in cmsss],
            columns=['Lock Type', 'Address\nSpace\nID', 'Job Name', 'Service\nClass\nName', 'Service\nClass\nPeriod',
                     'Total\nContention\nTime', 'Avg\nContention\nTime', 'Total\nContention\nCount',
                     'Contention\nCount with\nQLen>1']).dropna(how='all')
        df1['Total\nContention\nTime'] = df1['Total\nContention\nTime'] * 1000
        df1['Avg\nContention\nTime'] = (df1['Avg\nContention\nTime'] * 1000 / df1['Total\nContention\nCount']).where(
            df1['Total\nContention\nCount'] > 0, 0)
        df2 = pd.DataFrame.from_records(
            [('CMSEQDQ', d['r725cmas'], d['r725cmjn'], d['r725cmsn'], d['r725cmsp'], d['r725cmti'], d['r725cmti'],
              d['r725cmsu'], d['r725cmal']) for d in cedss],
            columns=['Lock Type', 'Address\nSpace\nID', 'Job Name', 'Service\nClass\nName', 'Service\nClass\nPeriod',
                     'Total\nContention\nTime', 'Avg\nContention\nTime', 'Total\nContention\nCount',
                     'Contention\nCount with\nQLen>1']).dropna(how='all')
        df2['Total\nContention\nTime'] = df2['Total\nContention\nTime'] * 1000
        df2['Avg\nContention\nTime'] = (df2['Avg\nContention\nTime'] * 1000 / df2['Total\nContention\nCount']).where(
            df2['Total\nContention\nCount'] > 0, 0)
        df3 = pd.DataFrame.from_records(
            [(
                'CMSLatch', d['r725cmas'], d['r725cmjn'], d['r725cmsn'], d['r725cmsp'], d['r725cmti'], d['r725cmti'],
                d['r725cmsu'], d['r725cmal']) for d in class_],
            columns=['Lock Type', 'Address\nSpace\nID', 'Job Name', 'Service\nClass\nName', 'Service\nClass\nPeriod',
                     'Total\nContention\nTime', 'Avg\nContention\nTime', 'Total\nContention\nCount',
                     'Contention\nCount with\nQLen>1']).dropna(how='all')
        df3['Total\nContention\nTime'] = df3['Total\nContention\nTime'] * 1000
        df3['Avg\nContention\nTime'] = (df3['Avg\nContention\nTime'] * 1000 / df3['Total\nContention\nCount']).where(
            df3['Total\nContention\nCount'] > 0, 0)
        df4 = pd.DataFrame.from_records(
            [('CMSSMF', d['r725cmas'], d['r725cmjn'], d['r725cmsn'], d['r725cmsp'], d['r725cmti'], d['r725cmti'],
              d['r725cmsu'], d['r725cmal']) for d in csmss],
            columns=['Lock Type', 'Address\nSpace\nID', 'Job Name', 'Service\nClass\nName', 'Service\nClass\nPeriod',
                     'Total\nContention\nTime', 'Avg\nContention\nTime', 'Total\nContention\nCount',
                     'Contention\nCount with\nQLen>1']).dropna(how='all')
        df4['Total\nContention\nTime'] = df4['Total\nContention\nTime'] * 1000
        df4['Avg\nContention\nTime'] = (df4['Avg\nContention\nTime'] * 1000 / df4['Total\nContention\nCount']).where(
            df4['Total\nContention\nCount'] > 0, 0)
        df = pd.concat([df1 if not df1.empty else None, df2 if not df2.empty else None, df3 if not df3.empty else None,
                        df4 if not df4.empty else None])
        piv_columns = ['Total\nContention\nTime', 'Avg\nContention\nTime', 'Total\nContention\nCount',
                       'Contention\nCount with\nQLen>1']
        df_piv = df.pivot(
            index=['Address\nSpace\nID', 'Job Name', 'Service\nClass\nName', 'Service\nClass\nPeriod'],
            columns='Lock Type', values=piv_columns).reset_index().set_index(
            ['Address\nSpace\nID', 'Job Name', 'Service\nClass\nName', 'Service\nClass\nPeriod'])
        df_piv.columns = [str(s2) + '\n' + s1 for (s1, s2) in df_piv.columns]
        df_piv = df_piv.reindex(sorted(df_piv.columns), axis=1)
        df_piv = df_piv.replace([np.nan], [None], regex=False)

        return tb.tabulate(df_piv.reset_index(), headers='keys', tablefmt='psql', showindex=False,
                           missingval='-', floatfmt='.2f')
    else:
        return None


def format_cml_lock_detail(lotds, clods, clrds):
    if len(clods) > 0 or len(lotds) > 0 or len(clrds) > 0:
        df1 = pd.DataFrame.from_records(
            [('CML Lock Owner', d['r725coas'], d['r725cojn'], d['r725cosn'], d['r725cosp'], d['r725coti'],
              d['r725coti'], d['r725cosu'], d['r725coal']) for d in clods],
            columns=['Lock Type', 'Address\nSpace\nID', 'Job Name', 'Service\nClass\nName', 'Service\nClass\nPeriod',
                     'Total\nContention\nTime', 'Avg\nContention\nTime', 'Total\nContention\nCount',
                     'Contention\nCount with\nQLen>1']).dropna(how='all')
        df1['Total\nContention\nTime'] = df1['Total\nContention\nTime'] * 1000
        df1['Avg\nContention\nTime'] = (df1['Avg\nContention\nTime'] * 1000 / df1['Total\nContention\nCount']).where(
            df1['Total\nContention\nCount'] > 0, 0)
        df2 = pd.DataFrame.from_records(
            [('Local Lock', d['r725loas'], d['r725lojn'], d['r725losn'], d['r725losp'], d['r725loti'], d['r725loti'],
              d['r725losu'], d['r725loal']) for d in lotds],
            columns=['Lock Type', 'Address\nSpace\nID', 'Job Name', 'Service\nClass\nName', 'Service\nClass\nPeriod',
                     'Total\nContention\nTime', 'Avg\nContention\nTime', 'Total\nContention\nCount',
                     'Contention\nCount with\nQLen>1']).dropna(how='all')
        df2['Total\nContention\nTime'] = df2['Total\nContention\nTime'] * 1000
        df2['Avg\nContention\nTime'] = (df2['Avg\nContention\nTime'] * 1000 / df2['Total\nContention\nCount']).where(
            df2['Total\nContention\nCount'] > 0, 0)
        df3 = pd.DataFrame.from_records(
            [('CML Lock Requestor', d['r725cras'], d['r725crjn'], d['r725crsn'], d['r725crsp'], d['r725crti'],
              d['r725crti'], d['r725crsu'], d['r725cral']) for d in clrds],
            columns=['Lock Type', 'Address\nSpace\nID', 'Job Name', 'Service\nClass\nName', 'Service\nClass\nPeriod',
                     'Total\nContention\nTime', 'Avg\nContention\nTime', 'Total\nContention\nCount',
                     'Contention\nCount with\nQLen>1']).dropna(how='all')
        df3['Total\nContention\nTime'] = df3['Total\nContention\nTime'] * 1000
        df3['Avg\nContention\nTime'] = (df3['Avg\nContention\nTime'] * 1000 / df3['Total\nContention\nCount']).where(
            df3['Total\nContention\nCount'] > 0, 0)
        df = pd.concat([df1 if not df1.empty else None, df2 if not df2.empty else None, df3 if not df3.empty else None])
        piv_columns = ['Total\nContention\nTime', 'Avg\nContention\nTime', 'Total\nContention\nCount',
                       'Contention\nCount with\nQLen>1']
        df_piv = df.pivot(
            index=['Address\nSpace\nID', 'Job Name', 'Service\nClass\nName', 'Service\nClass\nPeriod'],
            columns='Lock Type', values=piv_columns).reset_index().set_index(
            ['Address\nSpace\nID', 'Job Name', 'Service\nClass\nName', 'Service\nClass\nPeriod'])
        df_piv.columns = [str(s2) + '\n' + s1 for (s1, s2) in df_piv.columns]
        df_piv = df_piv.reindex(sorted(df_piv.columns), axis=1)
        df_piv = df_piv.replace([np.nan], [None], regex=False)
        return tb.tabulate(df_piv.reset_index(), headers='keys', tablefmt='psql', showindex=False,
                           missingval='-', floatfmt='.2f')
    else:
        return None


def format_grs_latch_detail(lascs, lares):
    if len(lascs) > 0 or len(lares) > 0:
        df1 = pd.DataFrame.from_records(
            [('Latch Set Creator', d['r725laas'], d['r725lajn'], d['r725lasn'], d['r725lasp'], d['r725lati'],
              d['r725lati'], d['r725lasq'], d['r725lasu']) for d in lascs],
            columns=['Latch Type', 'Address\nSpace\nID', 'Job Name', 'Service\nClass\nName', 'Service\nClass\nPeriod',
                     'Total\nContention\nTime', 'Avg\nContention\nTime', 'Std Dev\nContention\nTime',
                     'Total\nContention\nCount']).dropna(how='all')
        df1['Std Dev\nContention\nTime'] = df_cal_std_dev(df1['Std Dev\nContention\nTime'],
                                                          df1['Total\nContention\nCount'],
                                                          df1['Total\nContention\nTime']) * 1000
        df1['Total\nContention\nTime'] = df1['Total\nContention\nTime'] * 1000
        df1['Avg\nContention\nTime'] = (df1['Avg\nContention\nTime'] * 1000 / df1['Total\nContention\nCount']).where(
            df1['Total\nContention\nCount'] > 0, 0)
        df2 = pd.DataFrame.from_records(
            [('Latch Requestor', d['r725laas'], d['r725lajn'], d['r725lasn'], d['r725lasp'], d['r725lati'],
              d['r725lati'], d['r725lasq'], d['r725lasu']) for d in lares],
            columns=['Latch Type', 'Address\nSpace\nID', 'Job Name', 'Service\nClass\nName', 'Service\nClass\nPeriod',
                     'Total\nContention\nTime', 'Avg\nContention\nTime', 'Std Dev\nContention\nTime',
                     'Total\nContention\nCount']).dropna(how='all')
        df2['Std Dev\nContention\nTime'] = df_cal_std_dev(df2['Std Dev\nContention\nTime'],
                                                          df2['Total\nContention\nCount'],
                                                          df2['Total\nContention\nTime']) * 1000
        df2['Total\nContention\nTime'] = df2['Total\nContention\nTime'] * 1000
        df2['Avg\nContention\nTime'] = (df2['Avg\nContention\nTime'] * 1000 / df2['Total\nContention\nCount']).where(
            df2['Total\nContention\nCount'] > 0, 0)
        df = pd.concat([df1 if not df1.empty else None, df2 if not df2.empty else None])
        piv_columns = ['Total\nContention\nTime', 'Avg\nContention\nTime', 'Std Dev\nContention\nTime',
                       'Total\nContention\nCount']
        df_piv = df.pivot(
            index=['Address\nSpace\nID', 'Job Name', 'Service\nClass\nName', 'Service\nClass\nPeriod'],
            columns='Latch Type', values=piv_columns).reset_index().set_index(
            ['Address\nSpace\nID', 'Job Name', 'Service\nClass\nName', 'Service\nClass\nPeriod'])
        df_piv.columns = [str(s2) + '\n' + s1 for (s1, s2) in df_piv.columns]
        df_piv = df_piv.reindex(sorted(df_piv.columns), axis=1)
        df_piv = df_piv.replace([np.nan], [None], regex=False)
        return tb.tabulate(df_piv.reset_index(), headers='keys', tablefmt='psql',
                           showindex=False, missingval='-', floatfmt='.2f')
    else:
        return None


def format_grs_enq_detail(enses, ensys, ensss):
    if len(enses) > 0 or len(ensys) > 0 or len(ensss) > 0:
        df1 = pd.DataFrame.from_records(
            [('ENQ STEP', d['r725enas'], d['r725enjn'], d['r725ensn'], d['r725ensp'], d['r725enti'], d['r725enti'],
              d['r725ensq'], d['r725enrc'], d['r725ensu']) for d in enses],
            columns=['Enqueue Scope', 'Address\nSpace\nID', 'Job Name', 'Service\nClass\nName',
                     'Service\nClass\nPeriod',
                     'Total\nContention\nTime', 'Avg\nContention\nTime', 'Std Dev\nContention\nTime', 'Request Count',
                     'Contention\nCount']).dropna(how='all')
        df1['Std Dev\nContention\nTime'] = df_cal_std_dev(df1['Std Dev\nContention\nTime'],
                                                          df1['Contention\nCount'],
                                                          df1['Total\nContention\nTime']) * 1000
        df1['Total\nContention\nTime'] = df1['Total\nContention\nTime'] * 1000
        df1['Avg\nContention\nTime'] = (df1['Avg\nContention\nTime'] * 1000 / df1['Contention\nCount']).where(
            df1['Contention\nCount'] > 0, 0)
        df2 = pd.DataFrame.from_records(
            [('ENQ SYSTEM', d['r725enas'], d['r725enjn'], d['r725ensn'], d['r725ensp'], d['r725enti'], d['r725enti'],
              d['r725ensq'], d['r725enrc'], d['r725ensu']) for d in ensys],
            columns=['Enqueue Scope', 'Address\nSpace\nID', 'Job Name', 'Service\nClass\nName',
                     'Service\nClass\nPeriod',
                     'Total\nContention\nTime', 'Avg\nContention\nTime', 'Std Dev\nContention\nTime', 'Request Count',
                     'Contention\nCount']).dropna(how='all')
        df2['Std Dev\nContention\nTime'] = df_cal_std_dev(df2['Std Dev\nContention\nTime'],
                                                          df2['Contention\nCount'],
                                                          df2['Total\nContention\nTime']) * 1000
        df2['Total\nContention\nTime'] = df2['Total\nContention\nTime'] * 1000
        df2['Avg\nContention\nTime'] = (df2['Avg\nContention\nTime'] * 1000 / df2['Contention\nCount']).where(
            df2['Contention\nCount'] > 0, 0)
        df3 = pd.DataFrame.from_records(
            [('ENQ SYSTEMS', d['r725enas'], d['r725enjn'], d['r725ensn'], d['r725ensp'], d['r725enti'], d['r725enti'],
              d['r725ensq'], d['r725enrc'], d['r725ensu']) for d in ensss],
            columns=['Enqueue Scope', 'Address\nSpace\nID', 'Job Name', 'Service\nClass\nName',
                     'Service\nClass\nPeriod',
                     'Total\nContention\nTime', 'Avg\nContention\nTime', 'Std Dev\nContention\nTime', 'Request Count',
                     'Contention\nCount']).dropna(how='all')
        df3['Std Dev\nContention\nTime'] = df_cal_std_dev(df3['Std Dev\nContention\nTime'],
                                                          df3['Contention\nCount'],
                                                          df3['Total\nContention\nTime']) * 1000
        df3['Total\nContention\nTime'] = df3['Total\nContention\nTime'] * 1000
        df3['Avg\nContention\nTime'] = (df3['Avg\nContention\nTime'] * 1000 / df3['Contention\nCount']).where(
            df2['Contention\nCount'] > 0, 0)
        df = pd.concat([df1 if not df1.empty else None, df2 if not df2.empty else None, df3 if not df3.empty else None])
        piv_columns = ['Total\nContention\nTime', 'Avg\nContention\nTime', 'Std Dev\nContention\nTime',
                       'Request Count', 'Contention\nCount']
        df_piv = df.pivot(
            index=['Address\nSpace\nID', 'Job Name', 'Service\nClass\nName', 'Service\nClass\nPeriod'],
            columns='Enqueue Scope', values=piv_columns).reset_index().set_index(
            ['Address\nSpace\nID', 'Job Name', 'Service\nClass\nName', 'Service\nClass\nPeriod'])
        df_piv.columns = [str(s2) + '\n' + s1 for (s1, s2) in df_piv.columns]
        df_piv = df_piv.reindex(sorted(df_piv.columns), axis=1)
        df_piv = df_piv.replace([np.nan], [None], regex=False)
        return tb.tabulate(df_piv.reset_index(), headers='keys', tablefmt='psql',
                           showindex=False, missingval='-', floatfmt='.2f')
    else:
        return None


def format_delay_summary(sctl):
    if sctl['r725sgmo'] == '0x01':
        grs_mode = 'Ring'
    elif sctl['r725sgmo'] == '0x02':
        grs_mode = 'Start'
    else:
        grs_mode = 'None'

    system_lst = [
        ["CMS", f"{sctl['r725scmt'] * 1000:>15.0f}",
         f"{sctl['r725scmt'] * 1000 / sctl['r725scms'] if sctl['r725scms'] > 0 else 0:>15.2f}", f"{sctl['r725scms']:>16.0f}",
         f"{sctl['r725scma']:>16.0f}"],
        ["CMSEQDQ", f"{sctl['r725sedt'] * 1000:>15.0f}",
         f"{sctl['r725sedt'] * 1000 / sctl['r725seds'] if sctl['r725seds'] > 0 else 0:>15.2f}", f"{sctl['r725seds']:>16.0f}",
         f"{sctl['r725seda']:>16.0f}"],
        ["CMSLatch", f"{sctl['r725slat'] * 1000:>15.0f}",
         f"{sctl['r725slat'] * 1000 / sctl['r725slas'] if sctl['r725slas'] > 0 else 0:>15.2f}", f"{sctl['r725slas']:>16.0f}",
         f"{sctl['r725slaa']:>16.0f}"],
        ["CMSSMF", f"{sctl['r725ssmt'] * 1000:>15.0f}",
         f"{sctl['r725ssmt'] * 1000 / sctl['r725ssms'] if sctl['r725ssms'] > 0 else 0:>15.2f}", f"{sctl['r725ssms']:>16.0f}",
         f"{sctl['r725ssma']:>16.0f}"],
        ["Local", f"{sctl['r725slot'] * 1000:>15.0f}",
         f"{sctl['r725slot'] * 1000 / sctl['r725slos'] if sctl['r725slos'] > 0 else 0:>15.2f}", f"{sctl['r725slos']:>16.0f}",
         f"{sctl['r725sloa']:>16.0f}"],
        ["CMLOwner", f"{sctl['r725sclt'] * 1000:>15.0f}",
         f"{sctl['r725sclt'] * 1000 / sctl['r725scls'] if sctl['r725scls'] > 0 else 0:>15.2f}", f"{sctl['r725scls']:>16.0f}",
         f"{sctl['r725scla']:>16.0f}"]]
    df_system = pd.DataFrame(system_lst, columns=['Lock Type', 'Total Contention Time', 'Avg Contention Time',
                                                  'Total Contention Count', 'Contention Count with Q Len>1'])
    df_latch = pd.DataFrame([[f"{sctl['r725slrt'] * 1000:>15.0f}",
                              f"{sctl['r725slrt'] * 1000 / sctl['r725slrs'] if sctl['r725slrs'] > 0 else 0:>15.2f}",
                              f"{cal_std_dev(sctl['r725slrq'], sctl['r725slrs'], sctl['r725slrt']) * 1000:>15.2f}",
                              f"{sctl['r725slrs']:>16.0f}"]],
                            columns=['Total Contention Time', 'Avg Contention Time', 'Std Dev of Contention Time',
                                     'Total Contention Count'])
    df_grs = pd.DataFrame([
        ["Step", f"{sctl['r725sstt'] * 1000:>15.0f}",
         f"{sctl['r725sstt'] * 1000 / sctl['r725ssts'] if sctl['r725ssts'] > 0 else 0:>15.2f}",
         f"{cal_std_dev(sctl['r725sstq'], sctl['r725ssts'], sctl['r725sstt']) * 1000:>15.2f}", f"{sctl['r725sstr']:>13.0f}",
         f"{sctl['r725ssts']:>16.0f}"],
        ["System", f"{sctl['r725ssyt'] * 1000:>15.0f}",
         f"{sctl['r725ssyt'] * 1000 / sctl['r725ssys'] if sctl['r725ssys'] > 0 else 0:>15.2f}",
         f"{cal_std_dev(sctl['r725ssyq'], sctl['r725ssys'], sctl['r725ssyt']) * 1000:>15.2f}", f"{sctl['r725ssyr']:>13.0f}",
         f"{sctl['r725ssys']:>16.0f}"],
        ["Systems", f"{sctl['r725ssst'] * 1000:>15.0f}",
         f"{sctl['r725ssst'] * 1000 / sctl['r725ssss'] if sctl['r725ssss'] > 0 else 0:>15.2f}",
         f"{cal_std_dev(sctl['r725sssq'], sctl['r725ssss'], sctl['r725ssst']) * 1000:>15.2f}", f"{sctl['r725sssr']:>13.0f}",
         f"{sctl['r725ssss']:>16.0f}"]],
        columns=['Scope', 'Total Contention Time', 'Avg Contention Time', 'Std Dev of Contention Time',
                 'Total Request Count',
                 'Total Contention Count'])

    return (grs_mode,
            tb.tabulate(df_system, headers='keys', tablefmt='psql', showindex=False, missingval=' ', floatfmt='.2f'),
            tb.tabulate(df_latch, headers='keys', tablefmt='psql', showindex=False, missingval=' ', floatfmt='.2f'),
            tb.tabulate(df_grs, headers='keys', tablefmt='psql', showindex=False, missingval=' ', floatfmt='.2f'))


def format_cachsys_header(duration, target, pro, category):
    if duration == 'Hourly':
        report_date = target['date']
        report_time = target['datetime'].time().strftime('%H.%M.%S')
        interval = format_s2min(pro['smf74int'])
    elif duration == 'Daily':
        report_date = target['date']
        report_time = '00.00.00'
        interval = format_s2min(pro['smf74int'])
    else:
        report_date = target['smf74ist'].date()
        report_time = target['smf74ist'].time().strftime('%H.%M.%S')
        interval = format_s2min(pro['smf74int'])
    zos_ver = 'V' + pro['smf74mvs'][2:4].lstrip('0') + 'R' + pro['smf74mvs'][4:6].lstrip('0')
    interval_x = f"{interval[:-3]}"
    whitespace = ' '
    header1a = [["                                         C A C H E   S U B S Y S T E M   S U M M A R Y"]]
    header1b = [["                                         C A C H E   S U B S Y S T E M   A C T I V I T Y"]]
    header2 = [
        [f"{whitespace:>12}", f"z/OS {zos_ver}", f"{whitespace:>13}", f"System ID {pro['smf74sid']}", f"{whitespace:>6}",
         f"Date {report_date:%m/%d/%Y}", f"{whitespace:>11}", f"Interval {interval_x}"],
        ["", "", "", f"RMF Version {pro['smf74mfv']:<5}", "", f"Time {report_time}"]
    ]
    if category == 1:
        return tb.tabulate(header1a, tablefmt="plain") + "\n" + tb.tabulate(header2, tablefmt="plain") + "\n"
    else:
        return tb.tabulate(header1b, tablefmt="plain") + "\n" + tb.tabulate(header2, tablefmt="plain") + "\n"


def format_cachsys_overview(cache):
    report1 = [
        ["Total I/O", f"{convert_si(cache['total_io'], 7, 0)}", "", "Cache I/O", f"{convert_si(cache['cache_io'], 7, 0)}"],
        ["Total H/R", f"{convert_si(cache['total_hits'] / cache['total_io'], 7, 3) if cache['total_io'] > 0 else 'N/A'}", "",
         "Cache H/R", f"{convert_si(cache['total_hits'] / cache['cache_io'], 7, 3) if cache['cache_io'] > 0 else 'N/A'}"],
        tb.SEPARATING_LINE,
        ["Cache I/O\nRequests", "--------\nCount", "-----\nRate", "Read I/O\nHits", "Requests\nRate", "--------\nH/R",
         "--------\nCount", "--------\nRate", "Write I/O\nFast", "Requests\nRate", "--------\nHits", "-------\nRate",
         "-------\nH/R", "%\nRead"],
        # ["Requests","Count",   "Rate",  "Hits",    "Rate",    "H/R",     "Count",   "Rate",    "Fast",     "Rate",    "Hits",    "Rate",   "H/R",   "Read"],
        tb.SEPARATING_LINE,
        ["Normal",
         f"{convert_si(cache['r745drcr'], 8, 0)}",
         f"{convert_si(cache['r745drcr'] / cache['r745cint'], 7, 1)}",
         f"{convert_si(cache['r745dcrh'], 8, 0)}",
         f"{convert_si(cache['r745dcrh'] / cache['r745cint'], 7, 1)}",
         f"{convert_si(cache['r745dcrh'] / cache['r745drcr'], 6, 3) if cache['r745drcr'] > 0 else 'N/A'}",
         f"{convert_si(cache['r745dwrc'], 8, 0)}",
         f"{convert_si(cache['r745dwrc'] / cache['r745cint'], 7, 1)}",
         f"{convert_si(cache['r745dfwc'], 8, 0)}",
         f"{convert_si(cache['r745dfwc'] / cache['r745cint'], 7, 1)}",
         f"{convert_si(cache['r745dwch'], 8, 0)}",
         f"{convert_si(cache['r745dwch'] / cache['r745cint'], 6, 1)}",
         f"{convert_si(cache['r745dwch'] / cache['r745dwrc'], 6, 3) if cache['r745dwrc'] > 0 else 'N/A'}",
         f"{convert_si(cache['r745drcr'] * 100 / (cache['r745drcr'] + cache['r745dwrc']), 8, 1) if cache['r745drcr'] + cache['r745dwrc'] > 0 else 'N/A'}"],
        ["Sequential",
         f"{convert_si(cache['r745drsr'], 8, 0)}",
         f"{convert_si(cache['r745drsr'] / cache['r745cint'], 7, 1)}",
         f"{convert_si(cache['r745drsh'], 8, 0)}",
         f"{convert_si(cache['r745drsh'] / cache['r745cint'], 7, 1)}",
         f"{convert_si(cache['r745drsh'] / cache['r745drsr'], 6, 3) if cache['r745drsr'] > 0 else 'N/A'}",
         f"{convert_si(cache['r745dwsr'], 8, 0)}",
         f"{convert_si(cache['r745dwsr'] / cache['r745cint'], 7, 1)}",
         f"{convert_si(cache['r745dfws'], 8, 0)}",
         f"{convert_si(cache['r745dfws'] / cache['r745cint'], 7, 1)}",
         f"{convert_si(cache['r745dwsh'], 8, 0)}",
         f"{convert_si(cache['r745dwsh'] / cache['r745cint'], 6, 1)}",
         f"{convert_si(cache['r745dwsh'] / cache['r745dwsr'], 6, 3) if cache['r745dwsr'] > 0 else 'N/A'}",
         f"{convert_si(cache['r745drsr'] * 100 / (cache['r745drsr'] + cache['r745dwsr']), 8, 1) if cache['r745drsr'] + cache['r745dwsr'] > 0 else 'N/A'}"],
        ["CFW Data",
         f"{convert_si(cache['r745drnr'], 8, 0)}",
         f"{convert_si(cache['r745drnr'] / cache['r745cint'], 7, 1)}",
         f"{convert_si(cache['r745dnrh'], 8, 0)}",
         f"{convert_si(cache['r745dnrh'] / cache['r745cint'], 7, 1)}",
         f"{convert_si(cache['r745dnrh'] / cache['r745drnr'], 6, 3) if cache['r745drnr'] > 0 else 'N/A'}",
         f"{convert_si(cache['r745dwnr'], 8, 0)}",
         f"{convert_si(cache['r745dwnr'] / cache['r745cint'], 7, 1)}",
         f"{convert_si(cache['r745dwnr'], 8, 0)}",
         f"{convert_si(cache['r745dwnr'] / cache['r745cint'], 7, 1)}",
         f"{convert_si(cache['r745dwnh'], 8, 0)}",
         f"{convert_si(cache['r745dwnh'] / cache['r745cint'], 6, 1)}",
         f"{convert_si(cache['r745dwnh'] / cache['r745dwnr'], 6, 3) if cache['r745dwnr'] > 0 else 'N/A'}",
         f"{convert_si(cache['r745drnr'] * 100 / (cache['r745drnr'] + cache['r745dwnr']), 8, 1) if cache['r745drnr'] + cache['r745dwnr'] > 0 else 'N/A'}"],
        tb.SEPARATING_LINE,
        ["Total",
         f"{convert_si(cache['total_reads'], 8, 0)}",
         f"{convert_si((cache['total_reads']) / cache['r745cint'], 7, 1)}",
         f"{convert_si(cache['read_hits'], 8, 0)}",
         f"{convert_si((cache['read_hits']) / cache['r745cint'], 7, 1)}",
         f"{convert_si((cache['read_hits']) / (cache['total_reads']), 6, 3) if cache['total_reads'] > 0 else 'N/A'}",
         f"{convert_si(cache['total_writes'], 8, 0)}",
         f"{convert_si((cache['total_writes']) / cache['r745cint'], 7, 1)}",
         f"{convert_si(cache['fast_writes'], 8, 0)}",
         f"{convert_si((cache['fast_writes']) / cache['r745cint'], 7, 1)}",
         f"{convert_si(cache['write_hits'], 8, 0)}",
         f"{convert_si((cache['write_hits']) / cache['r745cint'], 6, 1)}",
         f"{convert_si((cache['write_hits']) / (cache['total_writes']), 6, 3) if cache['total_writes'] > 0 else 'N/A'}",
         f"{convert_si((cache['total_reads']) * 100 / (cache['total_reads'] + cache['total_writes']), 8, 1) if cache['total_reads'] + cache['total_writes'] > 0 else 'N/A'}"],
    ]
    report2 = [
        ["", "", "", "", "", "", "", "",
         "Delayed Due To NVS",
         f"{convert_si(cache['r745dfwb'], 6, 0)}",
         f"{convert_si(cache['r745dfwb'] / cache['r745cint'], 5, 1)}"],
        ["Normal",
         f"{convert_si(cache['r745drcr'] - cache['r745dcrh'], 7, 0)}",
         f"{convert_si((cache['r745drcr'] - cache['r745dcrh']) / cache['r745cint'], 6, 1)}",
         f"{convert_si(cache['r745dwrc'] - cache['r745dwch'], 6, 0)}",
         f"{convert_si((cache['r745dwrc'] - cache['r745dwch']) / cache['r745cint'], 6, 1)}",
         f"{convert_si(cache['r745dntd'], 6, 0)}",
         f"{convert_si(cache['r745dntd'] / cache['r745cint'], 6, 1)}",
         "",
         "Delayed Due To Cache",
         f"{convert_si(cache['r745dfwr'], 6, 0)}",
         f"{convert_si(cache['r745dfwr'] / cache['r745cint'], 5, 1)}"],
        ["Sequential",
         f"{convert_si(cache['r745drsr'] - cache['r745drsh'], 7, 0)}",
         f"{convert_si((cache['r745drsr'] - cache['r745drsh']) / cache['r745cint'], 6, 1)}",
         f"{convert_si(cache['r745dwsr'] - cache['r745dwsh'], 6, 0)}",
         f"{convert_si((cache['r745dwsr'] - cache['r745dwsh']) / cache['r745cint'], 6, 1)}",
         f"{convert_si(cache['r745dtc'], 6, 0)}",
         f"{convert_si(cache['r745dtc'] / cache['r745cint'], 6, 1)}",
         "",
         "DFW Inhibit",
         f"{convert_si(cache['total_writes'] - cache['fast_writes'], 7, 0)}",
         f"{convert_si((cache['total_writes'] - cache['fast_writes']) / cache['r745cint'], 6, 1)}"],
        ["CFW Data",
         f"{convert_si(cache['r745drnr'] - cache['r745dnrh'], 7, 0)}",
         f"{convert_si((cache['r745drnr'] - cache['r745dnrh']) / cache['r745cint'], 6, 1)}",
         f"{convert_si(cache['r745dwnr'] - cache['r745dwnh'], 6, 0)}",
         f"{convert_si((cache['r745dwnr'] - cache['r745dwnh']) / cache['r745cint'], 6, 1)}",
         "", "", "",
         "Async (Trks)",
         f"{convert_si(cache['r745dctd'], 6, 0)}",
         f"{convert_si(cache['r745dctd'] / cache['r745cint'], 5, 1)}"],
        tb.SEPARATING_LINE,
        ["Total",
         f"{convert_si(cache['total_reads'] + cache['total_writes'] - (cache['read_hits'] + cache['write_hits']), 7, 0)}",
         "Rate",
         f"{convert_si((cache['total_reads'] + cache['total_writes'] - (cache['read_hits'] + cache['write_hits'])) / cache['r745cint'], 6, 1)}"]
    ]
    report3 = [
        ["\nWrite",
         f"\n{convert_si(cache['r745dkdw'], 7, 0)}",
         "\nRead Misses",
         f"\n{convert_si(cache['r745dcrm'], 7, 0)}",
         "",
         "Req\n/Sec", "Hits\n/Req", "", "Bytes\n/Req", "Bytes\n/Sec", "", "Resp\nTime", "Bytes\n/Req", "Bytes\n/Sec"],
        ["Write Hits",
         f"{convert_si(cache['r745dkdh'], 7, 0)}", "Write Prom", f"{convert_si(cache['r745dcwp'], 7, 0)}",
         "Read",
         f"{convert_si(cache['r7451srr'] / cache['r745cint'], 6, 1)}",
         f"{convert_si((cache['r7451srh']) / (cache['r7451srr']), 6, 3) if cache['r7451srr'] > 0 else '0.000'}",
         "  Read     ",
         f"{convert_si(cache['r7451ct1'] * 128 * 1024 / cache['total_reads'], 5, 2) if cache['r7451unt'] == '00' and cache['total_reads'] > 0 else convert_si(cache['r7451ct1'] / cache['total_reads'], 5, 2) if cache['total_reads'] > 0 else 0}",
         f"{convert_si(cache['r7451ct1'] * 128 * 1024 / cache['r745cint'], 5, 1) if cache['r7451unt'] == '00' else convert_si(cache['r7451ct1'] / cache['r745cint'], 5, 1)}",
         " Read",
         f"{convert_si(cache['r7452prt'] * 1000 / cache['r7452pro'], 7, 3) if pd.notna(cache['r7452pro']) and cache['r7452pro'] > 0 else '0.000'}",
         f"{convert_si(cache['r7452pbr'] * 128 * 1024 / cache['r7452pro'], 5, 2) if cache['r7451unt'] == '00' and pd.notna(cache['r7452pro']) and cache['r7452pro'] > 0 else convert_si(cache['r7452pbr'] / cache['r7452pro'], 5, 2) if pd.notna(cache['r7452pro']) and cache['r7452pro'] > 0 else 0}",
         f"{convert_si(cache['r7452pbr'] * 128 * 1024 / cache['r745cint'], 5, 1) if cache['r7451unt'] == '00' and pd.notna(cache['r7452pbr']) else convert_si(cache['r7452pbr'] / cache['r745cint'], 5, 1) if pd.notna(cache['r7452pbr']) else 0}"],
        ["", "", "", "", "Write   ",
         f"{convert_si(cache['r7451swr'] / cache['r745cint'], 6, 1)}",
         f"{convert_si(cache['r7451swh'] / cache['r7451swr'], 6, 3) if cache['r7451swr'] > 0 else '0.000'}",
         "  Write",
         f"{convert_si(cache['r7451ct2'] * 128 * 1024 / cache['total_writes'], 5, 2) if cache['r7451unt'] == '00' and cache['total_writes'] > 0 else convert_si(cache['r7451ct2'] / cache['total_writes'], 5, 2) if cache['total_writes'] > 0 else 0}",
         f"{convert_si(cache['r7451ct2'] * 128 * 1024 / cache['r745cint'], 5, 1) if cache['r7451unt'] == '00' else convert_si(cache['r7451ct2'] / cache['r745cint'], 5, 1)}",
         " Write",
         f"{convert_si(cache['r7452pwt'] * 1000 / cache['r7452pwo'], 7, 3) if pd.notna(cache['r7452pwo']) and cache['r7452pwo'] > 0 else '0.000'}",
         f"{convert_si(cache['r7452pbw'] * 128 * 1024 / cache['r7452pwo'], 5, 2) if cache['r7451unt'] == '00' and pd.notna(cache['r7452pwo']) and cache['r7452pwo'] > 0 else convert_si(cache['r7452pbw'] / cache['r7452pwo'], 5, 2) if pd.notna(cache['r7452pwo']) and cache['r7452pwo'] > 0 else 0}",
         f"{convert_si(cache['r7452pbw'] * 128 * 1024 / cache['r745cint'], 5, 1) if cache['r7451unt'] == '00' and pd.notna(cache['r7452pbw']) else convert_si(cache['r7452pbw'] / cache['r745cint'], 5, 1) if pd.notna(cache['r7452pbw']) else 0}"]
    ]
    return (tb.tabulate(report1, tablefmt='plain',
                        floatfmt=('', '.0f', '.1f', '.0f', '.1f', '.3f', '.0f', '.1f', '.0f', '.1f', '.0f', '.1f',
                                  '.3f', '.1f',),
                        colalign=('left', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right',
                                  'right', 'right', 'right', 'right', 'right')) + '\n' + '\n' +
            "-----------------------Cache Misses---------------------------   -------------------Misc---------------\n" +
            tb.tabulate(report2, tablefmt='plain',
                        headers=["Requests", "Read", "Rate", "Write", "Rate", "Tracks", "Rate", "", "", "Count",
                                 "Rate"],
                        colalign=('left', 'right', 'right', 'right', 'right', 'right', 'right', '', 'left', 'right',
                                  'right'),
                        floatfmt=('', '.0f', '.1f', '.0f', '.1f', '.0f', '.1f', '', '', '.0f', '.1f')) + '\n' +
            "---CKD Statistics--- ---Record Caching---  ---Synch I/O Activity---  --Host Adapter Activity-- ---------Disk Activity-------\n" +
            tb.tabulate(report3, tablefmt='plain',
                        # headers=["---CKD Statistics","---","---Record","Caching---","---Synch","I/O","Activity---","--Host","Adapter","Activity-","---------",
                        #         "Disk","Activity","-------"],
                        colalign=('left', 'right', 'left', 'right', 'left', 'right', 'right', 'left', 'right', 'right',
                                  'left', 'right', 'right', 'right'),
                        floatfmt=('', '.0f', '', '.0f', '', '.1f', '.3f', '', '', '', '', '.3f', '.0f', '.0f'))
            )


def format_cachsys_status_and_overview(duration, cachsys, pro):
    cachsys_overview = format_cachsys_header(duration, cachsys, pro, 2)
    cachsys_overview += '\n'
    if duration == 'Hourly':
        cdate = cachsys.date
        ctime = cachsys.datetime.time().strftime('%H.%M.%S')
    elif duration == 'Daily':
        cdate = cachsys.date
        ctime = '00.00.00'
    else:
        cdate = cachsys['smf74ist'].date()
        ctime = cachsys['smf74ist'].time().strftime('%H.%M.%S')
    interval = pd.to_datetime(0) + pd.to_timedelta(cachsys['r745cint'], unit='s')
    interval_x = f"{interval:%M.%S}"
    nvs_status_list = []
    if cachsys['r745snht']:
        nvs_status_list.append('EXPLICIT HOST TERMINATION')
    if cachsys['r745snis']:
        nvs_status_list.append('INTERNAL ERROR TERMINATION')
    if cachsys['r745dfwi']:
        nvs_status_list.append('DASD FAST WRITE INHIBITED')
    if cachsys['r745snds']:
        nvs_status_list.append('DISABLED FOR MAINTENANCE')
    if cachsys['r745snpe']:
        nvs_status_list.append('PENDING DUE TO ERROR')
    if len(nvs_status_list) > 0:
        nvs_status = ','.join(nvs_status_list)
    else:
        nvs_status = 'ACTIVE'
    overview1 = [
        [f"Subsystem",
         f"{cachsys['r745ccmt_typen'].lstrip('0'):4}-{cachsys['r745cmdl']:2}", "   ",
         "CU-ID",
         f"{cachsys['r745sdev'][2:].zfill(4)}", "   ",
         f"SSID",
         f"{cachsys['r745ssid']}", "   ",
         "CDate", f"{cdate:%m/%d/%Y}", "   ", "CTime", f"{ctime}", "   ", "CINT", f"{interval_x}"],
        ["Type-Model", f"{cachsys['r745ccmt_typen'].lstrip('0'):4}-{cachsys['r745ccmt_modn']:3}", "   ", "Manuf",
         f"{cachsys['r745ccmt_manuf']:3}", "   ",
         "Plant", f"{cachsys['r745ccmt_pmanu']}", "   ", "Serial", f"{cachsys['r745ccmt_seqn']}"]]
    overview2 = [
        ["Configured", f"{convert_bi(cachsys['r745scnf'] * 1024 if cachsys['r745sft'] > 0 else cachsys['r745scnf'], 6, 1)}",
         "Configured", f"{convert_bi(cachsys['r745scnv'] * 1024 if cachsys['r745sft'] > 0 else cachsys['r745scnv'], 5, 1)}",
         "Non-Volatile Storage", f"- {nvs_status}"],
        ["Available", f"{convert_bi(cachsys['r745savl'] * 1024 if cachsys['r745sft'] > 0 else cachsys['r745savl'], 6, 1)}",
         "Pinned", f"{convert_bi(cachsys['r745spnd'] * 1024 if cachsys['r745sft'] > 0 else cachsys['r745spnd'], 5, 1)}",
         "Cache Fast Write", f"- {'DEACTIVATED' if cachsys['r745snr'] else 'ACTIVE'}"],
        ["Pinned", f"{convert_bi(cachsys['r745spin'] * 1024 if cachsys['r745sft'] > 0 else cachsys['r745spin'], 6, 1)}"],
        ["Offline", f"{convert_bi(cachsys['r745soff'] * 1024 if cachsys['r745sft'] > 0 else cachsys['r745soff'], 6, 1)}"]
    ]
    cachsys_overview1 = tb.tabulate(overview1, tablefmt='plain',
                                    colalign=('left', 'left', '', 'left', 'left', '', 'left', 'right', '', 'left',
                                              'left', '', 'left', 'right'),
                                    floatfmt='.2f')
    cachsys_overview2 = tb.tabulate(overview2, tablefmt='plain',
                                    headers=['Subsystem Storage', '', 'Non-Volatile Storage', '', 'Status', ''],
                                    colalign=('left', 'center', 'left', 'center', 'left', 'left'),
                                    floatfmt=('', '.1f', '', '.1f'))
    cachsys_overview += cachsys_overview1
    cachsys_overview += \
        "\n--------------------------------------------------------------------------------------------------------------------------------------------\n" \
        "                                                       CACHE SUBSYSTEM STATUS\n" \
        "--------------------------------------------------------------------------------------------------------------------------------------------\n\n"
    cachsys_overview += cachsys_overview2
    cachsys_overview += \
        "\n--------------------------------------------------------------------------------------------------------------------------------------------\n" \
        "                                                      CACHE SUBSYSTEM OVERVIEW\n" \
        "--------------------------------------------------------------------------------------------------------------------------------------------\n\n"
    #    )
    cachsys_overview += format_cachsys_overview(cachsys)
    return cachsys_overview


def format_cachsys_device_overview_and_raid_activity(duration, cachsys, pro, cdevs, rranks, rranks_raids,
                                                     cdevs_raid, cdevs_xpool):
    cachsys_overview = format_cachsys_header(duration, cachsys, pro, 2)
    cachsys_overview += '\n'
    if duration == 'Hourly':
        cdate = cachsys['date']
        ctime = cachsys['datetime'].time().strftime('%H.%M.%S')
    elif duration == 'Daily':
        cdate = cachsys['date']
        ctime = '00.00.00'
    else:
        cdate = cachsys['smf74ist'].date()
        ctime = cachsys['smf74ist'].time().strftime('%H.%M.%S')
    interval = pd.to_datetime(0) + pd.to_timedelta(cachsys['r745cint'], unit='s')
    interval_x = f"{interval:%M.%S}"
    cachsys_overview += tb.tabulate([
        [f"Subsystem", f"{cachsys['r745ccmt_typen'].lstrip('0'):4}-{cachsys['r745cmdl']:2}", "   ",
         "CU-ID", f"{cachsys['r745sdev'][2:].zfill(4)}", "   ",
         f"SSID", f"{cachsys['r745ssid']}", "   ",
         "CDate", f"{cdate:%m/%d/%Y}", "   ", "CTime", f"{ctime}", "   ", "CINT", f"{interval_x}"],
        ["Type-Model", f"{cachsys['r745ccmt_typen'].lstrip('0'):4}-{cachsys['r745ccmt_modn']:3}", "   ",
         "Manuf", f"{cachsys['r745ccmt_manuf']:3}", "   ",
         "Plant", f"{cachsys['r745ccmt_pmanu']}", "   ", "Serial", f"{cachsys['r745ccmt_seqn']}"]],
        tablefmt='plain',
        colalign=(
            'left', 'left', '', 'left', 'left', '', 'left', 'right', '', 'left', 'left', '', 'left', 'right'),
        floatfmt='.2f')
    overview2 = [
        ["*ALL", "", "", f"{cachsys['total_io'] / cachsys['total_io'] * 100 if cachsys['total_io'] > 0 else 0}",
         f"{convert_si(cachsys['total_io'] / cachsys['r745cint'], 6, 1)}",
         f"{convert_si((cachsys['r745dcrh'] + cachsys['r745drsh']) / cachsys['r745cint'], 6, 1)}",
         f"{convert_si((cachsys['r745dwch'] + cachsys['r745dwsh']) / cachsys['r745cint'], 5, 1)}",
         f"{convert_si((cachsys['r745dnrh'] + cachsys['r745dwnh']) / cachsys['r745cint'], 5, 1)}",
         f"{convert_si((cachsys['total_reads'] + cachsys['total_writes'] - cachsys['total_hits'] - (cachsys['total_writes'] - cachsys['fast_writes']) - cachsys['r745dfwr'] - cachsys['r745dfwb']) / cachsys['r745cint'], 6, 1)}",
         f"{convert_si(cachsys['r745dfwb'] / cachsys['r745cint'], 6, 1)}",
         f"{convert_si((cachsys['total_writes'] - cachsys['fast_writes'] + cachsys['r745dfwr']) / cachsys['r745cint'], 5, 1)}",
         f"{convert_si(cachsys['r745dctd'] / cachsys['r745cint'], 6, 1)}",
         f"{convert_si(cachsys['total_hits'] / cachsys['total_io'], 6, 3) if cachsys['total_io'] > 0 else 'N/A'}",
         f"{convert_si(cachsys['read_hits'] / cachsys['total_reads'], 6, 3) if cachsys['total_reads'] > 0 else 'N/A'}",
         f"{convert_si(cachsys['write_hits'] / cachsys['total_writes'], 6, 3) if cachsys['total_writes'] > 0 else 'N/A'}",
         f"{convert_si(cachsys['total_reads'] * 100 / (cachsys['total_reads'] + cachsys['total_writes']), 6, 1) if cachsys['total_reads'] + cachsys['total_writes'] > 0 else 'N/A'}"]
    ]
    raid_rank_detail = None
    if len(rranks) > 0:
        raid_rank_activity = (
            "\n"
            "------------------------------------------------------------------------------------------------------------------------------------\n"
            "                                                         RAID RANK ACTIVITY\n"
            "------------------------------------------------------------------------------------------------------------------------------------\n\n"
            "Id    RAID     DA   HDD    -------- Read Req -------     ------- Write Req -------   ---------- Highest Utilized Volumes ----------\n"
            "      Type                 Rate  Avg MB  MB/S  RTime     Rate  Avg MB  MB/S  RTime\n\n"
        )
        total_r7451rrq = 0
        total_r7451sr = 0
        total_r7451rrt = 0.0
        total_r7451wrq = 0
        total_r7451sw = 0
        total_r7451wrt = 0.0
        raid_rank_detail = [
            ["*ALL", "", "", "",
             f"{convert_si(total_r7451rrq / cachsys['r745cint'], 4, 0)}",
             f"{convert_si(total_r7451sr / total_r7451rrq / (1024 * 1024), 6, 3) if total_r7451rrq > 0 else 'N/A'}",
             f"{convert_si(total_r7451sr / cachsys['r745cint'] / (1024 * 1024), 4, 1)}",
             f"{convert_si(total_r7451rrt / total_r7451rrq, 5, 0) if total_r7451rrq > 0 else 'N/A'}",
             f"{convert_si(total_r7451wrq / cachsys['r745cint'], 4, 0)}",
             f"{convert_si(total_r7451sw / total_r7451wrq / (1024 * 1024), 6, 3) if total_r7451wrq > 0 else 'N/A'}",
             f"{convert_si(total_r7451sw / cachsys['r745cint'] / (1024 * 1024), 4, 1)}",
             f"{convert_si(total_r7451wrt / total_r7451wrq, 5, 0) if total_r7451wrq > 0 else 'N/A ':>6}"]
        ]
        for ix_1, rrank in enumerate(rranks):
            raid_io_list = []
            raid_volumes = ""
            vol_count = 0
            for ix_2, raid in enumerate(rranks_raids[ix_1]):
                raid_io_list.append((raid['r745dvol'], raid['r7451rrq'] + raid['r7451wrq']))
            if len(raid_io_list) > 0:
                sorted_io_list = sorted(raid_io_list, key=itemgetter(1), reverse=True)
                for volume, total_io in sorted_io_list:
                    raid_volumes += volume
                    raid_volumes += "  "
                    vol_count += 1
                    if vol_count == 6:
                        break
            total_r7451rrq += rrank['r7451rrq']
            total_r7451sr += rrank['r7451sr'] * rrank['r7451hss']
            total_r7451rrt += rrank['r7451rrt'] * 1000
            total_r7451wrq += rrank['r7451wrq']
            total_r7451sw += rrank['r7451sw'] * rrank['r7451hss']
            total_r7451wrt += rrank['r7451wrt'] * 1000
            raid_rank_detail.append(
                [f"{rrank['r7451rid']}",
                 f"{'RAID-5' if rrank['r7451rty'] == 0 else 'JBOD' if rrank['r7451rty'] == 1 else 'RAID-10' if rrank['r7451rty'] == 2 else 'UNKNOWN'}",
                 f"{int(rrank['r7451aid'], 0)}", f"{rrank['r7451hdd']}",
                 f"{convert_si(rrank['r7451rrq'] / cachsys['r745cint'], 4, 0)}",
                 f"{convert_si(rrank['r7451sr'] * rrank['r7451hss'] / rrank['r7451rrq'] / (1024 * 1024), 6, 3) if rrank['r7451rrq'] > 0 else 'N/A'}",
                 f"{convert_si(rrank['r7451sr'] * rrank['r7451hss'] / cachsys['r745cint'] / (1024 * 1024), 4, 1)}",
                 f"{convert_si(rrank['r7451rrt'] * 1000 / rrank['r7451rrq'], 5, 0) if rrank['r7451rrq'] > 0 else 'N/A'}",
                 f"{convert_si(rrank['r7451wrq'] / cachsys['r745cint'], 4, 0)}",
                 f"{convert_si(rrank['r7451sw'] * rrank['r7451hss'] / rrank['r7451wrq'] / (1024 * 1024), 6, 3) if rrank['r7451wrq'] > 0 else 'N/A'}",
                 f"{convert_si(rrank['r7451sw'] * rrank['r7451hss'] / cachsys['r745cint'] / (1024 * 1024), 4, 1)}",
                 f"{convert_si(rrank['r7451wrt'] * 1000 / rrank['r7451wrq'], 5, 0) if rrank['r7451wrq'] > 0 else 'N/A'}",
                 f"{raid_volumes}"]
            )
    else:
        raid_rank_activity = None

    for ix_1, cdev in enumerate(cdevs):
        overview2.append(
            [f"{cdev['r745dvol']}", f"{cdev['r745devn']}",
             f"{cdevs_xpool[ix_1]['r748xpid'] if pd.notna(cdevs_xpool[ix_1]) else cdevs_raid[ix_1]['r7451rid'] if pd.notna(cdevs_raid[ix_1]) else 'N/A'}",
             f"{cdev['total_io'] / cachsys['total_io'] * 100 if cachsys['total_io'] > 0 else 0}",
             f"{convert_si(cdev['total_io'] / cachsys['r745cint'], 6, 1)}",
             f"{convert_si((cdev['r745dcrh'] + cdev['r745drsh']) / cachsys['r745cint'], 6, 1)}",
             f"{convert_si((cdev['r745dwch'] + cdev['r745dwsh']) / cachsys['r745cint'], 5, 1)}",
             f"{convert_si((cdev['r745dnrh'] + cdev['r745dwnh']) / cachsys['r745cint'], 5, 1)}",
             f"{convert_si((cdev['total_reads'] + cdev['total_writes'] - cdev['total_hits'] - (cdev['total_writes'] - cdev['fast_writes']) - cdev['r745dfwr'] - cdev['r745dfwb']) / cachsys['r745cint'], 6, 1)}",
             f"{convert_si(cdev['r745dfwb'] / cachsys['r745cint'], 6, 1)}",
             f"{convert_si((cdev['total_writes'] - cdev['fast_writes'] + cdev['r745dfwr']) / cachsys['r745cint'], 5, 1)}",
             f"{convert_si(cdev['r745dctd'] / cachsys['r745cint'], 6, 1)}",
             f"{convert_si(cdev['total_hits'] / cdev['total_io'], 6, 3) if cdev['total_io'] > 0 else 'N/A'}",
             f"{convert_si(cdev['read_hits'] / cdev['total_reads'], 6, 3) if cdev['total_reads'] > 0 else 'N/A'}",
             f"{convert_si(cdev['write_hits'] / cdev['total_writes'], 6, 3) if cdev['total_writes'] > 0 else 'N/A'}",
             f"{convert_si(cdev['total_reads'] * 100 / (cdev['total_reads'] + cdev['total_writes']), 6, 1) if cdev['total_reads'] + cdev['total_writes'] > 0 else 'N/A'}\n"]
        )

    cachsys_overview += '\n'
    cachsys_overview += \
        "--------------------------------------------------------------------------------------------------------------------------------------------\n" \
        "                                                      CACHE SUBSYSTEM DEVICE OVERVIEW\n" \
        "--------------------------------------------------------------------------------------------------------------------------------------------\n"
    if any(cdevs_raid):
        cachsys_overview += tb.tabulate(overview2, tablefmt='plain',
                                        headers=["\nVolume\nSerial", "\nDev\nNum", "\nRRID", "\n%\nI/O",
                                                 "\nI/O\nRate", "\n----\nRead", " Cache \nHit Rate\nDFW",
                                                 "\n-----\nCFW", "\n----\nStage", " DASD \nI/O Rate\nDel NVS",
                                                 "\n----\nOther", "\nAsync\nRate", "\nTotal\nH/R",
                                                 "\nRead\nH/R", "\nWrite\nH/R", "\n%\nRead"],
                                        colalign=('left', 'left', 'left', 'right', 'right', 'right', 'right', 'right',
                                                  'right', 'right', 'right', 'right',
                                                  'right', 'right', 'right', 'right'),
                                        floatfmt=('', '', '', '.1f', '.1f', '.1f', '.1f', '.1f', '.1f', '.1f', '.1f',
                                                  '.1f', '.3f', '.3f', '.3f', '.1f'))
    else:
        cachsys_overview += tb.tabulate(overview2, tablefmt='plain',
                                        headers=["\nVolume\nSerial", "\nDev\nNum", "\nXtnt\nPool", "\n%\nI/O",
                                                 "\nI/O\nRate", "\n----\nRead", " Cache \nHit Rate\nDFW",
                                                 "\n-----\nCFW", "\n----\nStage", " DASD \nI/O Rate\nDel NVS",
                                                 "\n----\nOther", "\nAsync\nRate", "\nTotal\nH/R",
                                                 "\nRead\nH/R", "\nWrite\nH/R", "\n%\nRead"],
                                        colalign=('left', 'left', 'left', 'right', 'right', 'right', 'right', 'right',
                                                  'right', 'right', 'right', 'right',
                                                  'right', 'right', 'right', 'right'),
                                        floatfmt=('', '', '', '.1f', '.1f', '.1f', '.1f', '.1f', '.1f', '.1f', '.1f', '.1f',
                                                  '.3f', '.3f', '.3f', '.1f'))
    cachsys_overview += '\n'

    if raid_rank_activity is not None:
        cachsys_overview += raid_rank_activity
        cachsys_overview += tb.tabulate(raid_rank_detail, tablefmt='plain',
                                        headers=["Id", "RAID\nType", "DA", "HDD", "-----\nRate", "Read\nAvg MB",
                                                 "Req\nMB/S", "-------\nRTime",
                                                 "-----\nRate", "Write\nAvg MB", "Req\nMB/S", "-------\nRTime",
                                                 "---------- Highest Utilized Volumes ----------"],
                                        colalign=('left', 'left', 'left', 'center', 'right', 'right', 'right', 'right',
                                                  'right', 'right', 'right', 'right', 'left'),
                                        floatfmt=('', '', '', '.0f', '.0f', '.3f', '.1f', '.0f', '.0f', '.3f', '.1f',
                                                  '.0f', ''))
    return cachsys_overview


def format_top20_report(duration, cachsys, cdevs_total, cdevs_dasd, pro):
    report_cols = [
        "Volume\nSerial", "Dev\nNum", "SSID", "%\nI/O", "I/O\nRate", "---Cache\nRead", "Hit\nDFW", "Rate--\nCFW",
        "----DASD\nStage", "I/O\nDel NVS", "Rate----\nOther", "Async\nRate", "Total\nH/R", "Read\nH/R", "Write\nH/R",
        "%\nRead"]
    report_start = True
    report = None
    dasd_report = "*** Device List By DASD I/O Rate ***\n\n"
    dasd_detail = []
    for cdev in cdevs_dasd:
        if report_start:
            report = format_cachsys_header(duration, cachsys, pro, 1)
            report_start = False
        dasd_detail.append([
            f"{cdev['r745dvol']}",
            f"{cdev['r745devn']}",
            f"{cdev['r745dsid']}",
            f"{cdev['total_io'] / cachsys['total_io'] * 100 if cachsys['total_io'] > 0 else 0}",
            f"{convert_si(cdev['total_io'] / cachsys['r745cint'], 6, 1)}",
            f"{convert_si((cdev['r745dcrh'] + cdev['r745drsh']) / cachsys['r745cint'], 6, 1)}",
            f"{convert_si((cdev['r745dwch'] + cdev['r745dwsh']) / cachsys['r745cint'], 5, 1)}",
            f"{convert_si((cdev['r745dnrh'] + cdev['r745dwnh']) / cachsys['r745cint'], 5, 1)}",
            f"{convert_si((cdev['total_reads'] + cdev['total_writes'] - cdev['total_hits'] - (cdev['total_writes'] - cdev['fast_writes']) - cdev['r745dfwr'] - cdev['r745dfwb']) / cachsys['r745cint'], 6, 1):>7}",
            f"{convert_si(cdev['r745dfwb'] / cachsys['r745cint'], 6, 1)}",
            f"{convert_si((cdev['total_writes'] - cdev['fast_writes'] + cdev['r745dfwr']) / cachsys['r745cint'], 5, 1)}",
            f"{convert_si(cdev['r745dctd'] / cachsys['r745cint'], 6, 1)}",
            f"{convert_si(cdev['total_hits'] / cdev['total_io'], 6, 3) if cdev['total_io'] > 0 else 'N/A'}",
            f"{convert_si(cdev['read_hits'] / cdev['total_reads'], 6, 3) if cdev['total_reads'] > 0 else 'N/A'}",
            f"{convert_si(cdev['write_hits'] / cdev['total_writes'], 6, 3) if cdev['total_writes'] > 0 else 'N/A'}",
            f"{convert_si(cdev['total_reads'] * 100 / (cdev['total_reads'] + cdev['total_writes']), 6, 1) if cdev['total_reads'] + cdev['total_writes'] > 0 else 'N/A'}"
        ])
    dasd_report += tb.tabulate(dasd_detail, tablefmt='simple',
                               headers=report_cols,
                               colalign=('left', 'left', 'left', 'right', 'right', 'right', 'right', 'right', 'right',
                                         'right', 'right', 'right', 'right', 'right', 'right', 'right'),
                               floatfmt=('', '', '', '.1f', '.1f', '.1f', '.1f', '.1f', '.1f', '.1f', '.1f', '.1f',
                                         '.3f', '.3f', '.3f', '.1f'))
    total_report = "\n*** Device List BY Total I/O Rate ***\n\n"
    total_detail = []
    for cdev in cdevs_total:
        total_detail.append([
            f"{cdev['r745dvol']}",
            f"{cdev['r745devn']}",
            f"{cdev['r745dsid']}",
            f"{cdev['total_io'] / cachsys['total_io'] * 100 if cachsys['total_io'] > 0 else 0}",
            f"{convert_si(cdev['total_io'] / cachsys['r745cint'], 6, 1)}",
            f"{convert_si((cdev['r745dcrh'] + cdev['r745drsh']) / cachsys['r745cint'], 6, 1)}",
            f"{convert_si((cdev['r745dwch'] + cdev['r745dwsh']) / cachsys['r745cint'], 5, 1)}",
            f"{convert_si((cdev['r745dnrh'] + cdev['r745dwnh']) / cachsys['r745cint'], 5, 1)}",
            f"{convert_si((cdev['total_reads'] + cdev['total_writes'] - cdev['total_hits'] - (cdev['total_writes'] - cdev['fast_writes']) - cdev['r745dfwr'] - cdev['r745dfwb']) / cachsys['r745cint'], 6, 1)}",
            f"{convert_si(cdev['r745dfwb'] / cachsys['r745cint'], 6, 1)}",
            f"{convert_si((cdev['total_writes'] - cdev['fast_writes'] + cdev['r745dfwr']) / cachsys['r745cint'], 5, 1)}",
            f"{convert_si(cdev['r745dctd'] / cachsys['r745cint'], 6, 1)}",
            f"{convert_si(cdev['total_hits'] / cdev['total_io'], 6, 3) if cdev['total_io'] > 0 else 'N/A'}",
            f"{convert_si(cdev['read_hits'] / cdev['total_reads'], 6, 3) if cdev['total_reads'] > 0 else 'N/A'}",
            f"{convert_si(cdev['write_hits'] / cdev['total_writes'], 6, 3) if cdev['total_writes'] > 0 else 'N/A'}",
            f"{convert_si(cdev['total_reads'] * 100 / (cdev['total_reads'] + cdev['total_writes']), 6, 1) if cdev['total_reads'] + cdev['total_writes'] > 0 else 'N/A'}"
        ])
    total_report += tb.tabulate(total_detail, tablefmt='simple',
                                headers=report_cols,
                                colalign=(
                                    'left', 'left', 'left', 'right', 'right', 'right', 'right', 'right', 'right',
                                    'right', 'right', 'right', 'right', 'right', 'right', 'right'),
                                floatfmt=(
                                    '', '', '', '.1f', '.1f', '.1f', '.1f', '.1f', '.1f', '.1f', '.1f', '.1f', '.3f',
                                    '.3f', '.3f', '.1f'))
    report += dasd_report
    report += '\n\n'
    report += total_report
    return report


def format_cachsys_summary(duration, cachsyss, pro):
    first_summary = True
    summary_report = None
    report = []
    report_dict = {}
    for idx, cachsys in enumerate(cachsyss):
        if first_summary:
            summary_report = format_cachsys_header(duration, cachsys, pro, 1)
            summary_report += '\n'
            first_summary = False
        report_dict[cachsys['r745ssid']] = [
            f"{cachsys['r745sdev'][2:].zfill(4)}",
            f"{cachsys['r745ccmt_typen'].lstrip('0') if isinstance(cachsys['r745ccmt_typen'], str) else cachsys['r745ccmt_typen']:4}-{cachsys['r745ccmt_modn']:3}",
            f"{convert_si(cachsys['r745scnf'] * 1024 if cachsys['r745sft'] > 0 else cachsys['r745scnf'], 4, 1)}",
            f"{convert_bi(cachsys['r745scnv'] * 1024 if cachsys['r745sft'] > 0 else cachsys['r745scnv'], 4, 1)}",
            f"{convert_si(cachsys['total_io'] / cachsys['r745cint'], 6, 1)}",
            f"{convert_si((cachsys['r745dcrh'] + cachsys['r745drsh']) / cachsys['r745cint'], 6, 1)}",
            f"{convert_si((cachsys['r745dwch'] + cachsys['r745dwsh']) / cachsys['r745cint'], 5, 1)}",
            f"{convert_si((cachsys['r745dnrh'] + cachsys['r745dwnh']) / cachsys['r745cint'], 5, 1)}",
            f"{convert_si((cachsys['total_reads'] + cachsys['total_writes'] - cachsys['total_hits'] - (cachsys['total_writes'] - cachsys['fast_writes']) - cachsys['r745dfwr'] - cachsys['r745dfwb']) / cachsys['r745cint'], 6, 1)}",
            f"{convert_si(cachsys['r745dfwb'] / cachsys['r745cint'], 6, 1)}",
            f"{convert_si((cachsys['total_writes'] - cachsys['fast_writes'] + cachsys['r745dfwr']) / cachsys['r745cint'], 5, 1)}",
            f"{convert_si(cachsys['r745dctd'] / cachsys['r745cint'], 6, 1)}",
            f"{convert_si(cachsys['total_hits'] / cachsys['total_io'], 6, 3) if cachsys['total_io'] > 0 else 'N/A'}",
            f"{convert_si(cachsys['read_hits'] / cachsys['total_reads'], 6, 3) if cachsys['total_reads'] > 0 else 'N/A'}",
            f"{convert_si(cachsys['write_hits'] / cachsys['total_writes'], 6, 3) if cachsys['total_writes'] > 0 else 'N/A'}",
            f"{convert_si(cachsys['total_reads'] * 100 / (cachsys['total_reads'] + cachsys['total_writes']), 6, 1) if cachsys['total_reads'] + cachsys['total_writes'] > 0 else 'N/A'}"
        ]
    sorted_keys = sorted(report_dict.keys())
    for ssid in sorted_keys:
        report_line = [ssid] + report_dict[ssid]
        report.append(report_line)

    if len(report) > 0:
        return (summary_report +
                tb.tabulate(report,
                            headers=["SSID", "CU-ID", "Type", "Cache", "NVS", "I/O\nRate", "---Cache\nRead", "Hit\nDFW",
                                     "Rate---\nCFW",
                                     "---DASD\nStage", "  I/O  \nDel NVS", "Rate---\nOther", "Async\nRate",
                                     "Total\nH/R", "Read\nH/R", "Write\nH/R", "%\nRead"],
                            tablefmt='plain',
                            colalign=('left', 'left', 'left', 'right', 'right', 'right', 'right', 'right', 'right',
                                      'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right'),
                            floatfmt=('', '', '', '', '', '.1f', '.1f', '.1f', '.1f', '.1f', '.1f', '.1f', '.1f', '.3f',
                                      '.3f', '.3f', '.1f'))
                )
    return summary_report


def format_cache_device_status_and_activity(duration, cdev, cachsys, raid, xpool, pro):
    device_overview = format_cachsys_header(duration,cdev, pro, 2)
    device_overview += '\n'
    if duration == 'Hourly':
        cdate = cachsys['date']
        ctime = cachsys['datetime'].time().strftime('%H.%M.%S')
    elif duration == 'Daily':
        cdate = cachsys['date']
        ctime = '00.00.00'
    else:
        cdate = cachsys['smf74ist'].date()
        ctime = cachsys['smf74ist'].time().strftime('%H.%M.%S')

    interval = pd.to_datetime(0) + pd.to_timedelta(cachsys['r745cint'], unit='s')
    interval_x = f"{interval:%M.%S}"
    if pd.notna(xpool):
        xpool_raid = 'Extend Pool'
    elif pd.notna(raid):
        xpool_raid = 'RRID'
    else:
        xpool_raid = 'Unknown'
    device_overview += tb.tabulate([
        [f"Subsystem", f"{cachsys['r745ccmt_typen'].lstrip('0'):4}-{cachsys['r745cmdl']:2}", "   ",
         "CU-ID", f"{cachsys['r745sdev'][2:].zfill(4)}", "   ",
         f"SSID", f"{cachsys['r745ssid']}", "   ",
         "CDate", f"{cdate:%m/%d/%Y}", "   ", "CTime", f"{ctime}", "   ", "CINT", f"{interval_x}"],
        ["Type-Model", f"{cachsys['r745ccmt_typen'].lstrip('0'):4}-{cachsys['r745ccmt_modn']:3}", "   ",
         "Manuf", f"{cachsys['r745ccmt_manuf']:3}", "   ",
         "Plant", f"{cachsys['r745ccmt_pmanu']}", "   ", "Serial", f"{cachsys['r745ccmt_seqn']}"],
        ["Volser", f"{cdev['r745dvol']}", "   ", "Num", f"{cdev['r745devn']}", "   ",
         f"{xpool_raid}", f"{xpool['r748xpid'] if pd.notna(xpool) else raid['r7451rid'] if pd.notna(raid) else 'N/A'}"]],
        tablefmt='plain',
        colalign=(
            'left', 'left', '', 'left', 'left', '', 'left', 'right', '', 'left', 'left', '', 'left', 'right'),
        floatfmt='.2f')
    device_overview += \
        "\n----------------------------------------------------------------------------------------------------------------------------------------\n" \
        "                                                        CACHE DEVICE STATUS\n" \
        "----------------------------------------------------------------------------------------------------------------------------------------\n\n"
    device_overview += \
        tb.tabulate([
            ["DASD Fast Write",
             f"- {'ACTIVE' if cdev['r745dsfw'] == '00' else 'DEACTIVATED' if cdev['r745dsfw'] == '11' else 'DEACTIVATION PENDING' if cdev['r745dsfw'] == '10' else 'NOT USED'}"],
            ["Pinned Data",
             f"- {'NONE' if cdev['r745dpdt'] == '00' else 'EXISTS' if cdev['r745dpdt'] == '01' else 'NOT USED' if cdev['r745dpdt'] == '11' else 'UNKNOWN PINNED STATUS'}"]],
            tablefmt='plain', headers=["Cache Status", "  "], colalign=('left', 'left'))
    device_overview += \
        "\n----------------------------------------------------------------------------------------------------------------------------------------\n" \
        "                                                       CACHE DEVICE ACTIVITY\n" \
        "----------------------------------------------------------------------------------------------------------------------------------------\n\n"

    device_overview += format_cachsys_overview(cdev)
    return device_overview


def format_cf_header(duration, cf):
    if duration == 'Hourly':
        report_date = cf['date']
        report_time = cf['datetime'].time().strftime('%H.%M.%S')
        interval = format_s2min(cf['smf74int'])
    elif duration == 'Daily':
        report_date = cf['date']
        report_time = '00.00.00'
        interval = format_s2hr(cf['smf74int'])
    else:
        report_date = cf['smf74ist'].date()
        report_time = cf['smf74ist'].time().strftime('%H.%M.%S')
        interval = format_s2min(cf['smf74int'])
    zos_ver = 'V' + cf['smf74mvs'][2:4].lstrip('0') + 'R' + cf['smf74mvs'][4:6].lstrip('0')
    interval_x = f"{interval[:-3]}"
    whitespace = ' '
    header1 = [["                                      C O U P L I N G   F A C I L I T Y   A C T I V I T Y"]]
    header2 = [
        [f"{whitespace:>12}", f"z/OS {zos_ver}", f"{whitespace:>13}", f"Sysplex {cf['smf74xnm']:<8}", f"{whitespace:>6}",
         f"Date {report_date:%m/%d/%Y}", f"{whitespace:>11}", f"Interval {interval_x}"],
        ["", "", "", f"RMF Version {cf['smf74mfv']}", "", f"Time {report_time}", "", f"Cycle {cf['smf74cyc'] / 1000:5.3f} Seconds"]
    ]
    return tb.tabulate(header1, tablefmt="plain") + "\n" + tb.tabulate(header2, tablefmt="plain") + "\n"


def format_cf2cf_activity(duration, cf, cfrfs, peer_cfs, dupchpas):
    if len(cfrfs) == 0:
        return None

    report = format_cf_header(duration, cf)
    report += \
        f"-------------------------------------------------------------------------------------------------------------------------------------------------------\n" \
        f" Coupling Facility Name = {cf['r744fnam']:<8}\n" \
        f"-------------------------------------------------------------------------------------------------------------------------------------------------------\n" \
        f"                                                     CF TO CF ACTIVITY\n" \
        f"-------------------------------------------------------------------------------------------------------------------------------------------------------\n" \
        f"                                               -------------------- Requests -------------------    ------------------ Delayed Requests ---------------\n"
    report_detail = []
    contain_channel_path_detail = False

    channel_path_detail = []
    op_mod_dict = {"0x01": "1GBIT", "0x02": "2GBIT", "0x10": "1X  IFB  HCA2-0 LR", "0x11": "12X IFB  HCA2-0",
                   "0x20": "1X  IFB  HCA3-0 LR", "0x21": "12X IFB  HCA3-0", "0x30": "12X IFB3 HCA3-0",
                   "0x40": "8x GEN3 PCIe-0 SR", "0x50": "10GBIT CEE RoCE LR"}

    for idx_1, cfrf_list in enumerate(peer_cfs):
        receiver_paths = {}
        sender_paths = {}
        receiver_path_id = []
        sender_path_id = []
        receiver_type = {}
        sender_type = {}
        receiver_op_mod = {}
        sender_op_mod = {}
        receiver_degraded = {}
        sender_degraded = {}
        receiver_latency = {}
        sender_latency = {}
        total_reqs = 0
        total_service_time = 0.0
        total_sq_service_time = 0
        total_delay_reqs = 0
        total_delay_time = 0.0
        total_sq_delay_time = 0
        first_cfrf = True
        for idx_2, cfrf in enumerate(cfrf_list):
            # if cfrf.__class__.__name__ == 'Smf74_cfrf_hr':
            #     dupchpas = cfrf.smf74_dupchpa_hrs
            # elif cfrf.__class__.__name__ == 'Smf74_cfrf_da':
            #     dupchpas = cfrf.smf74_dupchpa_das
            # else:
            #     dupchpas = cfrf.smf74_dupchpas
            total_reqs += (cfrf['r744rhes'] + cfrf['r744rrcs'] + cfrf['r744rres'] + cfrf['r744rrsa'])
            total_delay_reqs += cfrf['r744rdsc']
            total_service_time += cfrf['r744rsse']
            total_sq_service_time += cfrf['r744rsss']
            total_delay_time += cfrf['r744rsdt']
            total_sq_delay_time += cfrf['r744rssd']
            if first_cfrf:
                for ix in range(0, 8):
                    rtap = cfrf.get('r744rtap_' + str(ix + 1))
                    if rtap != "" and rtap != "?????" and rtap not in receiver_paths.keys():
                        receiver_paths[rtap] = 1

                    elif rtap not in ("", "?????"):
                        receiver_paths[rtap] += 1

                    stap = cfrf.get('r744rsap_' + str(ix + 1))
                    if stap != "" and stap != "?????" and stap not in sender_paths.keys():
                        sender_paths[stap] = 1

                    elif stap not in ("", "?????"):
                        sender_paths[stap] += 1
                first_cfrf = False
                for chpa in dupchpas[idx_1][idx_2]:
                    if chpa['r744hsnd']:
                        if chpa['r744hcpi'] not in sender_path_id:
                            sender_path_id.append(chpa['r744hcpi'])
                            sender_latency[chpa['r744hcpi']] = 0
                            sender_type[chpa['r744hcpi']] = chpa['r744htap']
                    else:
                        if chpa['r744hcpi'] not in receiver_path_id:
                            receiver_path_id.append(chpa['r744hcpi'])
                            receiver_latency[chpa['r744hcpi']] = 0
                            receiver_type[chpa['r744hcpi']] = chpa['r744htap']
                    if chpa['r744hmov']:
                        if chpa['r744hsnd']:
                            sender_op_mod[chpa['r744hcpi']] = chpa['r744hopm']
                        else:
                            receiver_op_mod[chpa['r744hcpi']] = chpa['r744hopm']
                    if chpa['r744hdev']:
                        if chpa['r744hsnd']:
                            sender_degraded[chpa['r744hcpi']] = chpa['r744hdeg']
                        else:
                            receiver_degraded[chpa['r744hcpi']] = chpa['r744hdeg']
                    if chpa['r744hlav']:
                        if chpa['r744hsnd']:
                            sender_latency[chpa['r744hcpi']] += chpa['r744hlat']
                        else:
                            receiver_latency[chpa['r744hcpi']] += chpa['r744hlat']
        receiver_types = list(receiver_paths.keys())
        sender_types = list(sender_paths.keys())
        report_detail.append(
            [f"{cfrf_list[-1]['r744rnam']}", f"{receiver_types[0]}", f"{receiver_paths[receiver_types[0]]}",
             f"{sender_types[0]}", f"{sender_paths[sender_types[0]]}", "SYNC",
             f"{convert_si(total_reqs, 8, 0)}", f"{convert_si(total_reqs / cf['smf74int'], 6, 1)}",
             f"{convert_si((total_service_time * 1e6 / total_reqs) if total_reqs > 0 else 0, 8, 1)}",
             f"{cal_std_dev(total_reqs, total_sq_service_time, total_service_time * 1e6):>6.1f}",
             f"{convert_si(total_delay_reqs, 8, 0)}",
             f"{total_delay_reqs / (total_delay_reqs + total_reqs) * 100 if (total_delay_reqs + total_reqs) > 0 else 0:>6.1f}",
             f"{convert_si(total_delay_time * 1e6 / total_delay_reqs if total_delay_reqs > 0 else 0, 7, 1)}",
             f"{cal_std_dev(total_delay_reqs, total_sq_delay_time, total_delay_time * 1e6)}",
             f"{convert_si((total_delay_time * 1e6 / (total_reqs + total_delay_reqs)) if total_reqs + total_delay_reqs > 0 else 0, 8, 1)}"]
        )

        first_peer_cf = True
        for path_id in receiver_type.keys():
            contain_channel_path_detail = True
            sender_distance = sender_latency[path_id] * 1e6 / 10
            receiver_distance = receiver_latency[path_id] * 1e6 / 10
            if first_peer_cf:
                channel_path_detail.append(
                    [f"{cfrf_list[-1]['r744rnam'] if first_peer_cf else ''}",
                     f"{path_id:2}", f"{receiver_type[path_id]}",
                     "R",
                     f"{op_mod_dict[receiver_op_mod[path_id]] if receiver_op_mod[path_id] in op_mod_dict.keys() else 'UNKNOWN'}",
                     f"{'Y' if receiver_degraded[path_id] else 'N':1}",
                     f"{'<1' if 1 > receiver_distance > 0 else int(receiver_distance)}"
                     ]
                )
                first_peer_cf = False
            else:
                channel_path_detail.append(
                    ["", f"{path_id:2}", f"{receiver_type[path_id]}",
                     "R",
                     f"{op_mod_dict[receiver_op_mod[path_id]] if receiver_op_mod[path_id] in op_mod_dict.keys() else 'UNKNOWN'}",
                     f"{'Y' if receiver_degraded[path_id] else 'N':1}",
                     f"{'<1' if 1 > receiver_distance > 0 else int(receiver_distance)}"]
                )
            channel_path_detail.append(
                ["", f"{path_id:2}", f"{sender_type[path_id]:<5}",
                 "S",
                 f"{op_mod_dict[sender_op_mod[path_id]] if sender_op_mod[path_id] in op_mod_dict.keys() else 'UNKNOWN'}",
                 f"{'Y' if sender_degraded[path_id] else 'N':1}",
                 f"{'<1' if 1 > sender_distance > 0 else int(sender_distance)}"]
            )
    report += (tb.tabulate(report_detail, tablefmt='plain',
                           headers=["Peer\nCF", "-Receiver\nType", "---\nUse", "-Sender\nType", "---\nUse",
                                    "   ", "#\nReq", "Avg/\nSec", "-Service\nAvg", "Time(Mic)-\nStd_Dev", "#\nReq",
                                    "% of\nReq",
                                    "------\nDel", "Avg Time(Mic)\nStd_Dev", "------\n/All"],
                           colalign=('left', 'center', 'right', 'center', 'right', 'left', 'right', 'right', 'right',
                                     'right', 'right', 'right', 'right', 'right', 'right'),
                           floatfmt=('', '', '.0f', '', '.0f', '', '.0f', '.1f', '.1f', '.1f', '.0f', '.1f', '.1f',
                                     '.1f', '.1f')))
    if contain_channel_path_detail:
        report += \
            "\n------------------------------------------------------------------------------------------------------------------------------\n" \
            "                                                    CHANNEL PATH DETAILS\n" \
            "------------------------------------------------------------------------------------------------------------------------------\n"
        report += (tb.tabulate(channel_path_detail, tablefmt='plain',
                               headers=["Peer CF", "ID", "Type", "R/S", "Operation Mode", "Degraded", "Distance"],
                               colalign=('left', 'left', 'left', 'center', 'left', 'center', 'right')))

    return report


def add(*p):
    return sum(filter(None, p))


def format_subch_activity(duration, cf, lcfs, chpas):
    report = format_cf_header(duration, cf)
    report_detail = []
    subchannel_header = [
        ["----------------------------------------------------------------------------------------------------------------------------------------------------------------"],
        [f"Coupling Facility Name = {cf['r744fnam']:<8}"],
        ["----------------------------------------------------------------------------------------------------------------------------------------------------------------"],
        ["                                                                 SUBCHANNEL  ACTIVITY"],
        ["----------------------------------------------------------------------------------------------------------------------------------------------------------------"],
        ["              # Req                                   ---------------- Requests ---------------- ------------------------- Delayed Requests --------------------"],
    ]
    for lcf in lcfs:
        path_available_mask = "{0:08b}".format(int(lcf['r744fpas'], 16))
        path_installed_mask = "{0:08b}".format(int(lcf['r744fpis'], 16))
        composite_path_mask = "{0:08b}".format(int(lcf['r744fpcm'], 16))
        path_available = {}
        path_installed = {}
        path_used = {}
        for ix in range(0, 8):
            ftap = lcf.get('r744ftap_' + str(ix + 1))
            if ftap != "" and ftap not in path_available.keys():
                path_available[ftap] = 0
                path_installed[ftap] = 0
                path_used[ftap] = 0
            if int(path_available_mask[ix]):
                path_available[ftap] += 1

            if int(path_installed_mask[ix]):
                path_installed[ftap] += 1

            if int(composite_path_mask[ix]):
                path_used[ftap] += 1
        paths = list(path_available.keys())
        total_delayed_reqs = add(lcf['total_list_delayed_reqs'], lcf['total_cache_delayed_reqs'], lcf['total_lock_delayed_reqs'])
        report_detail.append(
            [f"{lcf['smf74sid']}", f"{convert_si(lcf['r744ftor'], 5, 0)}", f"{paths[0]}", f"{path_available[paths[0]]:4}",
             f"{path_used[paths[0]]:4}",
             f"{convert_si(lcf['r744fpbc'], 5, 0)}",
             f"SYNC", f"{convert_si(lcf['r744ssrc'], 6, 0)}",
             f"{lcf['r744sstm'] * 1e6 / lcf['r744ssrc'] if pd.notna(lcf['r744ssrc']) and lcf['r744ssrc'] > 0 else 0:>6.1f}",
             f"{cal_std_dev(lcf['r744ssrc'], lcf['r744sssq'], lcf['r744sstm'] * 1e6 if pd.notna(lcf['r744sstm']) else 0):>6.1f}",
             "LIST/CACHE",
             f"{convert_si(add(lcf['total_list_delayed_reqs'], lcf['total_cache_delayed_reqs']), 4, 0)}",
             f"{add(lcf['total_list_delayed_reqs'], lcf['total_cache_delayed_reqs']) / add(lcf['total_list_r744ssrc'], lcf['total_list_r744sarc'], lcf['total_cache_r744ssrc'], lcf['total_cache_r744sarc']) * 100 if add(lcf['total_list_r744ssrc'], lcf['total_list_r744sarc'], lcf['total_cache_r744ssrc'], lcf['total_cache_r744sarc']) > 0 else 0:>6.1f}",
             f"{convert_si(add(lcf['total_list_delay_time'], lcf['total_cache_delay_time']) * 1e6 / add(lcf['total_list_delayed_reqs'], lcf['total_cache_delayed_reqs']), 5, 1) if add(lcf['total_list_delayed_reqs'], lcf['total_cache_delayed_reqs']) > 0 else 0.0}",
             f"{cal_std_dev(add(lcf['total_list_delayed_reqs'], lcf['total_cache_delayed_reqs']), add(lcf['total_list_delay_sq_time'], lcf['total_cache_delay_sq_time']), add(lcf['total_list_delay_time'], lcf['total_cache_delay_time']) * 1e6):>8.1f}",
             f"{convert_si(add(lcf['total_list_delay_time'], lcf['total_cache_delay_time']) * 1e6 / add(lcf['total_list_r744ssrc'], lcf['total_list_r744sarc'], lcf['total_cache_r744ssrc'], lcf['total_cache_r744sarc']), 5, 1) if add(lcf['total_list_r744ssrc'], lcf['total_list_r744sarc'], lcf['total_cache_r744ssrc'], lcf['total_cache_r744sarc']) > 0 else 0}"]
        )
        if len(paths) == 1:
            report_detail.append(  # line 2
                ["", f"{convert_si(lcf['r744ftor'] / cf['smf74int'], 5, 1)}",
                 "SUBCH", f"{lcf['r744fscg']}", f"{lcf['r744fscu']}", "",
                 "ASYNC", f"{convert_si(lcf['r744sarc'], 6, 0)}",
                 f"{lcf['r744satm'] * 1e6 / lcf['r744sarc'] if pd.notna(lcf['r744sarc']) and lcf['r744sarc'] > 0 else 0:>6.1f}",
                 f"{cal_std_dev(lcf['r744sarc'], lcf['r744sasq'], lcf['r744satm'] * 1e6):>6.1f}", "LOCK",
                 f"{convert_si(lcf['total_lock_delayed_reqs'], 4, 0)}",
                 f"{lcf['total_lock_delayed_reqs'] / add(lcf['total_lock_r744ssrc'], lcf['total_lock_r744sarc']) * 100 if pd.notna(lcf['total_lock_delayed_reqs']) and add(lcf['total_lock_r744ssrc'], lcf['total_lock_r744sarc']) > 0 else 0:>6.1f}",
                 f"{convert_si(lcf['total_lock_delay_time'] / lcf['total_lock_delayed_reqs'] * 1e6, 5, 1) if pd.notna(lcf['total_lock_delay_time']) and lcf['total_lock_delayed_reqs'] > 0 else 0.0}",
                 f"{cal_std_dev(lcf['total_lock_delayed_reqs'], lcf['total_lock_delay_sq_time'], lcf['total_lock_delay_time'] * 1e6 if pd.notna(lcf['total_lock_delay_time']) else 0)}",
                 f"{convert_si(lcf['total_lock_delay_time'] * 1e6 / add(lcf['total_lock_r744ssrc'], lcf['total_lock_r744sarc']) if pd.notna(lcf['total_lock_delay_time']) and add(lcf['total_lock_r744ssrc'], lcf['total_lock_r744sarc']) > 0 else 0, 5, 1)}"
                 ]
            )
            report_detail.append(  # line 3
                ["", "", "", "", "", "", "CHANGED", f"{convert_si(lcf['r744ssta'], 6, 0)}", "INCLUDED", "IN ASYNC",
                 "TOTAL",
                 f"{convert_si(total_delayed_reqs, 4, 0)}", f"{total_delayed_reqs / lcf['r744ftor'] * 100:>6.1f}"]
            )
            report_detail.append(  # line 4
                ["", "", "", "", "", "", "UNSUCC", f"{convert_si(lcf['r744fail'], 6, 0)}",
                 f"{lcf['r744ftim'] * 1e6 / lcf['r744fail'] if lcf['r744fail'] > 0 else 0:>6.1f}",
                 f"{cal_std_dev(lcf['r744fail'], lcf['r744fsqu'], lcf['r744ftim'] * 1e6):>6.1f}"]
            )
        else:
            report_detail.append(  # line 2 : path > 1
                ["", f"{convert_si(lcf['r744ftor'] / cf['smf74int'], 5, 1)}",
                 f"{paths[1]}", f"{path_available[paths[1]]:4}", f"{path_used[paths[1]]:4}", "",
                 "ASYNC", f"{convert_si(lcf['r744sarc'], 6, 0)}",
                 f"{lcf['r744satm'] * 1e6 / lcf['r744sarc'] if lcf['r744sarc'] > 0 else 0:>6.1f}",
                 f"{cal_std_dev(lcf['r744sarc'], lcf['r744sasq'], lcf['r744satm'] * 1e6):>6.1f}", "LOCK",
                 f"{convert_si(lcf['total_lock_delayed_reqs'], 4, 0)}",
                 f"{lcf['total_lock_delayed_reqs'] / lcf['r744ftor'] * 100 if pd.notna(lcf['total_lock_delayed_reqs']) and lcf['r744ftor'] > 0 else 0:>6.1f}",
                 f"{convert_si(lcf['total_lock_delay_time'] / lcf['total_lock_delayed_reqs'] * 1e6, 5, 1) if pd.notna(lcf['total_lock_delay_time']) and lcf['total_lock_delayed_reqs'] > 0 else 0.0}",
                 f"{cal_std_dev(lcf['total_lock_delayed_reqs'], lcf['total_lock_delay_sq_time'], lcf['total_lock_delay_time'] * 1e6 if pd.notna(lcf['total_lock_delay_time']) else 0)}",
                 f"{convert_si(lcf['total_lock_delay_time'] / lcf['r744ftor'] if pd.notna(lcf['total_lock_delay_time']) and lcf['r744ftor'] > 0 else 0, 5, 1)}"
                 ]
            )
            if len(paths) < 3:  # line 3
                report_detail.append(
                    ["", "", "SUBCH", f"{lcf['r744fscg']}", f"{lcf['r744fscu']}", "",
                     "CHANGED", f"{convert_si(lcf['r744ssta'], 6, 0)}", "INCLUDED", "IN ASYNC", "TOTAL",
                     f"{convert_si(total_delayed_reqs, 4, 0)}", f"{total_delayed_reqs / lcf['r744ftor'] * 100:>6.1f}"]
                )
                report_detail.append(
                    ["", "", "", "", "", "",
                     "UNSUCC", f"{convert_si(lcf['r744fail'], 6, 0)}",
                     f"{lcf['r744ftim'] * 1e6 / lcf['r744fail'] if lcf['r744fail'] > 0 else 0:>6.1f}",
                     f"{cal_std_dev(lcf['r744fail'], lcf['r744fsqu'], lcf['r744ftim'] * 1e6):>6.1f}"]
                )
            else:
                report_detail.append(
                    ["", "", f"{paths[2]}", f"{path_available[paths[2]]:4}", f"{path_used[paths[2]]:4}", "",
                     "CHANGED", f"{convert_si(lcf['r744ssta'], 6, 0)}", "INCLUDED", "IN ASYNC", "TOTAL",
                     f"{convert_si(total_delayed_reqs, 4, 0)}", f"{total_delayed_reqs / lcf['r744ftor'] * 100:>6.1f}"]
                )
                if len(paths) < 4:
                    report_detail.append(
                        ["", "", "", "", "", "",
                         "UNSUCC", f"{convert_si(lcf['r744fail'], 6, 0)}",
                         f"{lcf['r744ftim'] * 1e6 / lcf['r744fail'] if lcf['r744fail'] > 0 else 0:>6.1f}",
                         f"{cal_std_dev(lcf['r744fail'], lcf['r744fsqu'], lcf['r744ftim'] * 1e6):>6.1f}"]
                    )
                else:
                    report_detail.append(
                        ["", "", f"{paths[3]}", f"{path_available[paths[3]]:4}", f"{path_used[paths[3]]:4}", "",
                         "UNSUCC", f"{convert_si(lcf['r744fail'], 6, 0)}",
                         f"{lcf['r744ftim'] * 1e6 / lcf['r744fail'] if lcf['r744fail'] > 0 else 0:>6.1f}",
                         f"{cal_std_dev(lcf['r744fail'], lcf['r744fsqu'], lcf['r744ftim'] * 1e6):>6.1f}"]
                    )
                    for i in range(4, len(paths)):
                        report_detail.append(
                            ["", "", f"{paths[i]}", f"{path_available[paths[i]]:4}", f"{path_used[paths[i]]:4}"]
                        )
                    report_detail.append(
                        ["", "", "SUBCH", f"{lcf['r744fscg']}", f"{lcf['r744fscu']}"])
    if len(report_detail) > 0:
        report += (tb.tabulate(subchannel_header, tablefmt='plain') + '\n' +
                   tb.tabulate(report_detail, tablefmt='plain',
                               headers=["System\nName", "Total\nAvg/Sec", "-- CF\nType", "Links\nGen", "--\nUse",
                                        "Path\nBusy", "   ",
                                        "#\nReq", "-Service\nAvg", "Time(Mic)-\nStd_Dev", "   ",
                                        "#\nReq", "% of\nReq", "------\nDel", "Avg Time(Mic)\nStd_Dev", "------\n/All"],
                               colalign=('left', 'right', 'left', 'right', 'right', 'right', 'left',
                                         'right', 'right', 'right', 'left',
                                         'right', 'right', 'right', 'right', 'right'),
                               floatfmt=('', '', '', '.0f', '.0f', '.0f', '',
                                         '.0f', '.1f', '.1f', '',
                                         '.0f', '.1f', '.1f', '.1f', '.1f')) + '\n')

    op_mod_dict = {"0x01": "1GBIT", "0x02": "2GBIT", "0x10": "1X  IFB  HCA2-0 LR", "0x11": "12X IFB  HCA2-0",
                   "0x20": "1X  IFB  HCA3-0 LR", "0x21": "12X IFB  HCA3-0", "0x30": "12X IFB3 HCA3-0",
                   "0x40": "8x GEN3 PCIe-0 SR", "0x50": "10GBIT CEE RoCE LR"}
    channel_path_detail = []
    previous_sid = None
    contain_channel_path_detail = False
    for chpa in chpas:
        if chpa['r744htap'] != 'ICP':
            contain_channel_path_detail = True
            distance = chpa['r744hlat'] * 1e6 / 10
            channel_path_detail.append(
                [f"{chpa['smf74sid'] if chpa['smf74sid'] != previous_sid else ' '}",
                 f"{chpa['r744hcpi']:2}", f"{chpa['r744htap']}",
                 f"{op_mod_dict[chpa['r744hopm']] if chpa['r744hopm'] in op_mod_dict.keys() else 'UNKNOWN'}",
                 f"{'Y' if chpa['r744hdev'] and chpa['r744hdeg'] else 'N':1}",
                 f"{'<1' if 1 > distance > 0 else round_(distance)}",
                 f"{chpa['r744hpcp'].lstrip('0'):>4}", f"{chpa['r744haid']:4}", f"{chpa['r744hapn']:2}",
                 f"{chpa['r744hsap_1']:2} {chpa['r744hsap_2']:2} {chpa['r744hsap_3']:2} {chpa['r744hsap_4']:2}"]
            )
            if chpa['smf74sid'] != previous_sid:
                previous_sid = chpa['smf74sid']
    if contain_channel_path_detail:
        channel_path = [
            ["---------------------------------------------------------------------------------------------------------------------------------------"],
            ["                                                                CHANNEL PATH DETAILS"],
            ["----------------------------------------------------------------------------------------------------------------------------------------"],
        ]
        report += (tb.tabulate(channel_path, tablefmt='plain') + '\n' +
                   tb.tabulate(channel_path_detail, tablefmt='plain',
                               headers=["System Name", "ID", "Type", "Operation Mode", "Degraded", "Distance", "PCHID",
                                        "AID", "Port", "------- IOP IDs -------"],
                               colalign=('left', 'left', 'left', 'left', 'center', 'right', 'center', 'right', 'right',
                                         'left')) + '\n')
    return report


def format_str_activity(duration, structure, sreqs, interval):
    # str_dict = {"0x01":"UNSERIAL", "0x02":"SERIAL", "0x03":"LOCK", "0x04":"CACHE"}
    status_2 = ''
    if structure['r744qact'] or structure['r744qrbn'] or structure['r744qrbo'] or \
            structure['r744qrbp'] or structure['r744qrbd'] or \
            structure['r744scei'] or structure['r744sadi'] or structure['r744sdas']:
        status_1 = 'Active'
        status_2 = ' '
        if structure['r744qrbn']:
            status_2 = 'Primary'
        elif structure['r744qrbo']:
            status_2 = 'Secondary'
    else:
        status_1 = 'Inactive'
        if structure['r744ssiz'] == 0:
            status_1 = 'Unallocate'
    report_header1 = ["\nSystem\nName", "# Req\nTotal\nAvg/Sec", "<----\n\n", "----\n#\nReq", "Requests\n% of\nAll",
                      "-----\n-Serv\nAvg", "--------->\nTime(Mic)-\nStd_Dev",
                      "<-----\nReason\n", "----\n#\nReq", "Delayed\n% of\nReq", "Requests\n-----Avg\nDel",
                      "---------\nTime(Mic)\nStd_Dev", "----->\n-----\nAll", "", ""]
    report_header3 = ["\nSystem\nName", "# Req\nTotal\nAvg/Sec", "<----\n\n", "----\n#\nReq", "Requests\n% of\nAll",
                      "-----\n-Serv\nAvg", "--------->\nTime(Mic)-\nStd_Dev",
                      "<-----\nReason", "----\n#\nReq", "Delayed\n% of\nReq", "Requests\n-----Avg\nDel",
                      "---------\nTime(Mic)\nStd_Dev", "----->\n-----\nAll", "\nExternal\nContentions",
                      "\nRequest\n"]
    report_detail = []
    if structure['r744styp'] in (1, 2):
        report = (
            f"Structure Name = {structure['r744qstr']:<16}  Type = LIST   Status = {status_1 + ' ' + status_2:<16}       Encrypted = {'Yes' if structure['r744senc'] else 'No':<3}\n")
    elif structure['r744styp'] == 3:
        report = (
            f"Structure Name = {structure['r744qstr']:<16}  Type = LOCK   Status = {status_1 + ' ' + status_2:<16}       Encrypted = N/A\n")
    else:
        report = (
            f"Structure Name = {structure['r744qstr']:<16}  Type = CACHE  Status = {status_1 + ' ' + status_2:<16}        Encrypted = {'Yes' if structure['r744senc'] else 'No':<3}\n")

    previous_sid = None
    for sreq in sreqs:
        report_detail.append(
            [f"{sreq['smf74sid'] if sreq['smf74sid'] != previous_sid else ' '}",
             f"{convert_si(sreq['r744ssrc'] + sreq['r744sarc'], 6, 0)}", "SYNC", f"{convert_si(sreq['r744ssrc'], 4, 0)}",
             f"{sreq['r744ssrc'] / (structure['r744ssrc'] + structure['r744sarc']) * 100 if (structure['r744ssrc'] + structure['r744sarc']) > 0 else 0:>6.1f}",
             f"{sreq['r744sstm'] * 1e6 / sreq['r744ssrc'] if sreq['r744ssrc'] > 0 else 0:>6.1f}",
             f"{cal_std_dev(sreq['r744ssrc'], sreq['r744sssq'], sreq['r744sstm'] * 1e6):>6.1f}",
             "NO SCH", f"{convert_si(sreq['r744sqrc'], 4, 0)}",
             f"{sreq['r744sqrc'] / (structure['r744ssrc'] + structure['r744sarc']) * 100 if (structure['r744ssrc'] + structure['r744sarc']) > 0 else 0:>6.1f}",
             f"{sreq['r744sqtm'] * 1e6 / sreq['r744sqrc'] if sreq['r744sqrc'] > 0 else 0:>6.1f}",
             f"{cal_std_dev(sreq['r744sqrc'], sreq['r744sqsq'], sreq['r744sqtm'] * 1e6):>6.1f}",
             f"{sreq['r744sqtm'] * 1e6 / (structure['r744ssrc'] + structure['r744sarc']) if structure['r744ssrc'] + structure['r744sarc'] > 0 else 0:>6.1f}",
             f"{'Req Total' if structure['r744styp'] == 3 else ''}",
             f"{convert_si(sreq['r744strc'], 5, 0) if structure['r744styp'] == 3 else ''}"]
        )
        if sreq['smf74sid'] != previous_sid:
            previous_sid = sreq['smf74sid']
        report_detail.append(
            ["", f"{convert_si((sreq['r744ssrc'] + sreq['r744sarc']) / interval, 6, 2)}", "ASYNC",
             f"{convert_si(sreq['r744sarc'], 4, 0)}",
             f"{sreq['r744sarc'] / (structure['r744ssrc'] + structure['r744sarc']) * 100 if (structure['r744ssrc'] + structure['r744sarc']) > 0 else 0:>6.1f}",
             f"{sreq['r744satm'] * 1e6 / sreq['r744sarc'] if sreq['r744sarc'] > 0 else 0:>6.1f}",
             f"{cal_std_dev(sreq['r744sarc'], sreq['r744sasq'], sreq['r744satm'] * 1e6):>6.1f}",
             "PR WT", f"{convert_si(sreq['r744sptc'], 4, 0)}",
             f"{sreq['r744sptc'] / (structure['r744ssrc'] + structure['r744sarc']) * 100 if (structure['r744ssrc'] + structure['r744sarc']) > 0 else 0:>6.1f}",
             f"{sreq['r744spst'] * 1e6 / sreq['r744sptc'] if sreq['r744sptc'] > 0 else 0:>6.1f}",
             f"{cal_std_dev(sreq['r744sptc'], sreq['r744spss'], sreq['r744spst'] * 1e6):>6.1f}",
             f"{sreq['r744spss'] * 1e6 / (structure['r744ssrc'] + structure['r744sarc']) if structure['r744ssrc'] + structure['r744sarc'] > 0 else 0:>6.1f}",
             f"{'Req Deferred' if structure['r744styp'] == 3 else ''}",
             f"{convert_si(sreq['r744stac'], 5, 0) if structure['r744styp'] == 3 else ''}"]
        )
        report_detail.append(
            ["", "", "CHNGD", f"{convert_si(sreq['r744ssta'], 4, 0)}",
             f"{sreq['r744ssta'] / sreq['r744strc'] * 100 if sreq['r744strc'] > 0 else 0:>6.1f}",
             "INCLUDED", "IN ASYNC", "PR CMP", f"{convert_si(sreq['r744sctc'], 4, 0)}",
             f"{sreq['r744sctc'] / (structure['r744ssrc'] + structure['r744sarc']) * 100 if (structure['r744ssrc'] + structure['r744sarc']) > 0 else 0:>6.1f}",
             f"{sreq['r744scst'] * 1e6 / sreq['r744sctc'] if sreq['r744sctc'] > 0 else 0:>6.1f}",
             f"{cal_std_dev(sreq['r744sctc'], sreq['r744scss'], sreq['r744scst'] * 1e6):>6.1f}",
             f"{sreq['r744scss'] * 1e6 / (structure['r744ssrc'] + structure['r744sarc']) if structure['r744ssrc'] + structure['r744sarc'] > 0 else 0:>6.1f}",
             f"{'-Cont' if structure['r744styp'] == 3 else ''}",
             f"{convert_si(sreq['r744scn'], 5, 0) if structure['r744styp'] == 3 else ''}"]
        )
        report_detail.append(
            ["", "", "SUPPR", f"{convert_si(sreq['r744spes'], 4, 0)}",
             f"{sreq['r744spes'] / sreq['r744strc'] * 100 if sreq['r744strc'] > 0 else 0:>6.1f}", "", "",
             f"{'DUMP' if structure['r744styp'] != 3 else ''}",
             f"{convert_si(sreq['r744sdto'], 4, 0) if structure['r744styp'] != 3 else ''}",
             f"{sreq['r744sdto'] / (structure['r744ssrc'] + structure['r744sarc']) * 100 if structure['r744styp'] != 3 and (structure['r744ssrc'] + structure['r744sarc']) > 0 else 0 if structure['r744styp'] != 3 else ''}",
             f"{sreq['r744sdtm'] * 1e6 / sreq['r744sdto'] if structure['r744styp'] != 3 and sreq['r744sdto'] > 0 else 0 if structure['r744styp'] != 3 else ''}",
             f"{cal_std_dev(sreq['r744sdto'], sreq['r744sdsq'], sreq['r744sdtm'] * 1e6) if structure['r744styp'] != 3 else ''}",
             f"{sreq['r744sdtm'] * 1e6 / (structure['r744ssrc'] + structure['r744sarc']) if structure['r744styp'] != 3 and structure['r744ssrc'] + structure['r744sarc'] > 0 else 0 if structure['r744styp'] != 3 else ''}",
             f"{'-False Cont' if structure['r744styp'] == 3 else ''}",
             f"{convert_si(sreq['r744sfcn'], 5, 0) if structure['r744styp'] == 3 else ''}"]
        )
        report_detail.append(
            ["", "", "", "", "", "", "", "MONOP", f"{convert_si(sreq['r744smrc'], 4, 0)}",
             f"{sreq['r744smrc'] / (structure['r744ssrc'] + structure['r744sarc']) * 100 if (structure['r744ssrc'] + structure['r744sarc']) > 0 else 0:>6.1f}",
             f"{sreq['r744smtm'] * 1e6 / sreq['r744smrc'] if sreq['r744smrc'] > 0 else 0:>6.1f}",
             f"{cal_std_dev(sreq['r744smrc'], sreq['r744smsq'], sreq['r744smtm'] * 1e6):>6.1f}",
             f"{sreq['r744smtm'] * 1e6 / (structure['r744ssrc'] + structure['r744sarc']) if structure['r744ssrc'] + structure['r744sarc'] > 0 else 0:>6.1f}"]
        )

    report_detail.append(tb.SEPARATING_LINE)
    report_detail.append(
        ["Total", f"{convert_si(structure['r744ssrc'] + structure['r744sarc'], 6, 0)}",
         "SYNC", f"{convert_si(structure['r744ssrc'], 4, 0)}",
         f"{structure['r744ssrc'] / (structure['r744ssrc'] + structure['r744sarc']) * 100 if (structure['r744ssrc'] + structure['r744sarc']) > 0 else 0:>6.1f}",
         f"{structure['r744sstm'] * 1e6 / structure['r744ssrc'] if structure['r744ssrc'] > 0 else 0:>6.1f}",
         f"{cal_std_dev(structure['r744ssrc'], structure['r744sssq'], structure['r744sstm'] * 1e6):>6.1f}",
         "NO SCH", f"{convert_si(structure['r744sqrc'], 4, 0)}",
         f"{structure['r744sqrc'] / (structure['r744ssrc'] + structure['r744sarc']) * 100 if (structure['r744ssrc'] + structure['r744sarc']) > 0 else 0:>6.1f}",
         f"{structure['r744sqtm'] * 1e6 / structure['r744sqrc'] if structure['r744sqrc'] > 0 else 0:>6.1f}",
         f"{cal_std_dev(structure['r744sqrc'], structure['r744sqsq'], structure['r744sqtm'] * 1e6):>6.1f}",
         f"{structure['r744sqtm'] * 1e6 / (structure['r744ssrc'] + structure['r744sarc']) if structure['r744ssrc'] + structure['r744sarc'] > 0 else 0:>6.1f}",
         f"{'Req Total' if structure['r744styp'] == 3 else '' if structure['r744styp'] in (1, 2) else '-- Data'}",
         f"{convert_si(structure['r744strc'], 5, 0) if structure['r744styp'] == 3 else '' if structure['r744styp'] in (1, 2) else 'Access ---'}"]
    )
    report_detail.append(
        ["", f"{convert_si((structure['r744ssrc'] + structure['r744sarc']) / interval, 6, 2)}",
         "ASYNC", f"{convert_si(structure['r744sarc'], 4, 0)}",
         f"{structure['r744sarc'] / (structure['r744ssrc'] + structure['r744sarc']) * 100 if (structure['r744ssrc'] + structure['r744sarc']) > 0 else 0:>6.1f}",
         f"{structure['r744satm'] * 1e6 / structure['r744sarc'] if structure['r744sarc'] > 0 else 0:>6.1f}",
         f"{cal_std_dev(structure['r744sarc'], structure['r744sasq'], structure['r744satm'] * 1e6):>6.1f}",
         "PR WT", f"{convert_si(structure['r744sptc'], 4, 0)}",
         f"{structure['r744sptc'] / (structure['r744ssrc'] + structure['r744sarc']) * 100 if (structure['r744ssrc'] + structure['r744sarc']) > 0 else 0:>6.1f}",
         f"{structure['r744spst'] * 1e6 / structure['r744sptc'] if structure['r744sptc'] > 0 else 0:>6.1f}",
         f"{cal_std_dev(structure['r744sptc'], structure['r744spss'], structure['r744spst'] * 1e6):>6.1f}",
         f"{structure['r744spss'] * 1e6 / (structure['r744ssrc'] + structure['r744sarc']) if structure['r744ssrc'] + structure['r744sarc'] > 0 else 0:>6.1f}",
         f"{'Req Deferred' if structure['r744styp'] == 3 else '' if structure['r744styp'] in (1, 2) else 'Reads'}",
         f"{convert_si(structure['r744stac'], 5, 0) if structure['r744styp'] == 3 else '' if structure['r744styp'] in (1, 2) else convert_si(structure['r744crhc'], 5, 0)}"]
    )
    report_detail.append(
        ["", "", "CHNGD", f"{convert_si(structure['r744ssta'], 4, 0)}",
         f"{structure['r744ssta'] / structure['r744strc'] * 100 if structure['r744strc'] > 0 else 0:>6.1f}", "", "",
         "PR CMP", f"{convert_si(structure['r744sctc'], 4, 0)}",
         f"{structure['r744sctc'] / (structure['r744ssrc'] + structure['r744sarc']) * 100 if (structure['r744ssrc'] + structure['r744sarc']) > 0 else 0:>6.1f}",
         f"{structure['r744scst'] * 1e6 / structure['r744sctc'] if structure['r744sctc'] > 0 else 0:>6.1f}",
         f"{cal_std_dev(structure['r744sctc'], structure['r744scss'], structure['r744scst'] * 1e6):>6.1f}",
         f"{structure['r744scss'] * 1e6 / (structure['r744ssrc'] + structure['r744sarc']) if structure['r744ssrc'] + structure['r744sarc'] > 0 else 0:>6.1f}",
         f"{'-Cont' if structure['r744styp'] == 3 else '' if structure['r744styp'] in (1, 2) else 'Writes'}",
         f"{convert_si(structure['r744scn'], 5, 0) if structure['r744styp'] == 3 else '' if structure['r744styp'] in (1, 2) else convert_si(add(structure['r744cwh0'], structure['r744cwh1']), 5, 0)}"
         ]
    )
    report_detail.append(
        ["", "", "SUPPR", f"{convert_si(structure['r744spes'], 4, 0)}",
         f"{structure['r744spes'] / structure['r744strc'] * 100 if structure['r744strc'] > 0 else 0:>6.1f}", "", "",
         f"{'DUMP' if structure['r744styp'] != 3 else ''}",
         f"{convert_si(structure['r744sdto'], 4, 0) if structure['r744styp'] != 3 else ''}",
         f"{structure['r744sdto'] / (structure['r744ssrc'] + structure['r744sarc']) * 100 if structure['r744styp'] != 3 and (structure['r744ssrc'] + structure['r744sarc']) > 0 else 0 if structure['r744styp'] != 3 else ''}",
         f"{structure['r744sdtm'] * 1e6 / structure['r744sdto'] if structure['r744styp'] != 3 and structure['r744sdto'] > 0 else 0 if structure['r744styp'] != 3 else ''}",
         f"{cal_std_dev(structure['r744sdto'], structure['r744sdsq'], structure['r744sdtm'] * 1e6) if structure['r744styp'] != 3 else ''}",
         f"{structure['r744sdtm'] * 1e6 / (structure['r744ssrc'] + structure['r744sarc']) if structure['r744styp'] != 3 and structure['r744ssrc'] + structure['r744sarc'] > 0 else 0 if structure['r744styp'] != 3 else ''}",
         f"{'-False Cont' if structure['r744styp'] == 3 else '' if structure['r744styp'] in (1, 2) else 'Castouts'}",
         f"{convert_si(structure['r744sfcn'], 5, 0) if structure['r744styp'] == 3 else '' if structure['r744styp'] in (1, 2) else convert_si(structure['r744ccoc'], 5, 0)}"
         ]
    )
    xis = "Xi's"
    report_detail.append(
        ["", "", "", "", "", "", "", "MONOP", f"{convert_si(structure['r744smrc'], 4, 0)}",
         f"{structure['r744smrc'] / (structure['r744ssrc'] + structure['r744sarc']) * 100 if (structure['r744ssrc'] + structure['r744sarc']) > 0 else 0:>6.1f}",
         f"{structure['r744smtm'] * 1e6 / structure['r744smrc'] if structure['r744smrc'] > 0 else 0:>6.1f}",
         f"{cal_std_dev(structure['r744smrc'], structure['r744smsq'], structure['r744smtm'] * 1e6):>6.1f}",
         f"{structure['r744smtm'] * 1e6 / (structure['r744ssrc'] + structure['r744sarc']) if structure['r744ssrc'] + structure['r744sarc'] > 0 else 0:>6.1f}",
         f"{xis if structure['r744styp'] == 4 else ''}",
         f"{convert_si(add(structure['r744cxci'], structure['r744cxni'], structure['r744cxfw'], structure['r744cxrl'], structure['r744cxdr']), 5, 0) if structure['r744styp'] == 4 else ''}"]
    )
    if structure['r744styp'] == 3:
        report += tb.tabulate(report_detail, tablefmt='simple',
                              headers=report_header3,
                              colalign=('left', 'left', 'left', 'right', 'right', 'right', 'right',
                                        'left', 'right', 'right', 'right', 'right', 'right', 'left', 'right'),
                              floatfmt=('', '.0f', '', '.0f', '.1f', '.1f', '.1f', '', '.0f', '.1f', '.1f', '.1f',
                                        '.1f', '', '.0f'))
    else:
        report += tb.tabulate(report_detail, tablefmt='simple',
                              headers=report_header1,
                              colalign=('left', 'left', 'left', 'right', 'right', 'right', 'right',
                                        'left', 'right', 'right', 'right', 'right', 'right', 'left', 'right'),
                              floatfmt=('', '', '', '', '.0f', '.1f', '.1f', '.1f', '', '.0f', '.1f', '.1f', '.1f',
                                        '.1f', '', '.0f'))
    report += '\n\n\n'
    return report


def format_cf_summary(duration, cf, strs, lcfs, procs, str_group_list, mscms_list, adups_list):
    # if cf.__class__.__name__ == 'Smf74_cf_hr':
    #     strs = cf.smf74_str_hrs
    #     lcfs = cf.smf74_lcf_hrs
    #     procs = cf.smf74_proc_hrs
    # elif cf.__class__.__name__ == 'Smf74_cf_da':
    #     strs = cf.smf74_str_das
    #     lcfs = cf.smf74_lcf_das
    #     procs = cf.smf74_proc_das
    # else:
    #     strs = cf.smf74_strs
    #     lcfs = cf.smf74_lcfs
    #     procs = cf.smf74_procs
    report = format_cf_header(duration, cf)
    usage_summary = [
        ["--------------------------------------------------------------------------------------------------------------------------------------------------"],
        [f"Coupling Facility Name = {cf['r744fnam']:<8}"],
        [f"Total Samples(Avg) =  {mean(i['smf74sam'] for i in lcfs):<4.0f}  (Max) =  {max(i['smf74sam'] for i in lcfs)}  (Min) =  {min(i['smf74sam'] for i in lcfs)}"],
        ["--------------------------------------------------------------------------------------------------------------------------------------------------"],
        ["                                               COUPLING  FACILITY  USAGE  SUMMARY"],
        ["--------------------------------------------------------------------------------------------------------------------------------------------------"],
    ]
    structure_summary_header = ["\n\nType", "\nStructure\nName", "\n\nStatus", "\n\nChg", "\n\nEnc", "\nAlloc\nSize",
                                "% of\nCF\nStor", "\n#\nReq", "% of\nAll\nReq",
                                "% of\nCF\nUtil", "Avg\nReq/\nSec", "Lst/Dir\nEntries\nTot/Cur",
                                "Data\nElements\nTot/Cur", "Lock\nEntries\nTot/Cur", "Dir Rec/\nDir Rec\nXi's"]
    scm_summary = [
        ["SCM Structure Summary"],
        ["------------------------------------------------------------------------------------------------------------------------------------------------------------"]
    ]
    scm_summary_header = ["\n\nType", "\nStructure\nName", "\n\nAlg", "SCM Space\nMax/\n%Used",
                          "Augmented\nEst.Max/\n%Used", "Lst Entry\nEst.Max/\nCur",
                          "Lst Elem\nEst.Max\nCur", "--- SCM\nCnt/Byte\nX'ferred", "Read ----\nAvg St/\nStd_Dev",
                          "--- SCM\nCnt/Byte\nX'ferred",
                          "Write ---\nAvg St/\nStd_Dev", "SCM Aux\nEnabled\nCmd/%all", "Delayed\nFaults\nCnt/%All"]
    adup_summary = [
        ["Asynchronous CF Dupexing Summary"],
        ["--------------------------------------------------------------------------------------------------------------------------------------------------------------"],
        ["                              ------------- Async Duplex CF Operations -------------    ----- Async Duplex Sync_Up Requests -----"],
    ]
    adup_summary_header = ["\nType", "Structure\nName", "Total", "--Transmit\n  Avg", "Time--\nStd_Dev",
                           "--Service\n   Avg", "Time--\nStd_Dev",
                           "Total", "#Suspend", "--Suspend\n   Avg", "Time--\nStd_Dev"]
    processor_summary = [
        ["Processor Summary"],
        ["--------------------------------------------------------------------------------------------------------------------------------\n"],
    ]
    general_structure_summary = [
        ["General Structure Summary"],
        ["--------------------------------------------------------------------------------------------------------------------------------------------------"]
    ]
    storage_summary = [
        ["Storage Summary"],
        ["--------------------------------------------------------------------------------------------------------------------------------"],
    ]
    processor_summary_detail = [
        ["Coupling Facility", f"{cf['r744fmod']:>6}", "Model", f"{cf['r744fver']:3}", "CFLevel", f"{cf['r744flvl']:>3}",
         "DynDisp", f"{'THIN' if cf['r744fthn'] else 'ON' if cf['r744fdyd'] else 'OFF':<4}"],
        tb.SEPARATING_LINE,
        ["Average CF Utilization", "(% Busy)", "",
         f"{cf['total_processor_busy'] / (cf['total_processor_busy'] + cf['total_processor_wait']) * 100:>4.1f}", "Logical",
         "Processors:", "Defined", f"{cf['r744fpdn']:>2}",
         "Effective", f"{(cf['total_processor_busy'] + cf['total_processor_wait']) / cf['smf74int']:>4.1f}"],
        ["", "", "", "", "", "", "Shared", f"{cf['r744fpsn']:>2}", "Avg Weight", f"{cf['avg_processor_weight']:>4.1f}"]
    ]
    if len(strs) == 0:
        usage_summary.append(["                                         No structure/storage data reportable"])
        return (report + '\n' + tb.tabulate(processor_summary, tablefmt='plain') + '\n\n' +
                tb.tabulate(processor_summary_detail, tablefmt='plain',
                            colalign=('left', 'center', 'right', 'right', 'left', 'left', 'left', 'right', 'left',
                                      'right'),
                            floatfmt=('', '.0f', '', '.1f', '', '.0f', '', '.0f', '', '.1f')) + '\n')

    report += (tb.tabulate(usage_summary, tablefmt='plain') + '\n')
    total_sync_reqs = sum([i['r744ssrc'] for i in strs if pd.notna(i['r744ssrc'])], start=0)
    total_async_reqs = sum([i['r744sarc'] for i in strs if pd.notna(i['r744sarc'])], start=0)
    total_reqs = total_sync_reqs + total_async_reqs
    total_pbsys = sum([i['r744pbsy'] for i in procs if pd.notna(i['r744pbsy'])], start=0)
    total_alloc_size = 0
    total_cf_util = 0
    str_dict = {1: "UNSERIAL", 2: "SERIAL", 3: "LOCK", 4: "CACHE"}
    # str_group_list = [list(g) for k, g in groupby(strs, attrgetter('r744styp'))]
    has_scm_data = False
    has_adup_data = False
    general_structure_detail = [tb.SEPARATING_LINE]
    scm_structure_detail = [tb.SEPARATING_LINE]
    adup_detail = [tb.SEPARATING_LINE]
    status_2 = ' '
    for idx_1, str_group in enumerate(str_group_list):
        first_mscm_type = None
        first_adup_type = None
        for ix, structure in enumerate(str_group):
            # if structure.__class__.__name__ == 'Smf74_str_hr':
            #     mscms = structure.smf74_mscm_hrs
            #     adups = structure.smf74_adup_hrs
            # elif structure.__class__.__name__ == 'Smf74_str_da':
            #     mscms = structure.smf74_mscm_das
            #     adups = structure.smf74_adup_das
            # else:
            #     mscms = structure.smf74_mscms
            #     adups = structure.smf74_adups
            if structure['r744qact'] or structure['r744qrbn'] or structure['r744qrbo'] or \
                    structure['r744qrbp'] or structure['r744qrbd'] or \
                    structure['r744scei'] or structure['r744sadi'] or structure['r744sdas']:
                status_1 = 'ACTIVE'
                status_2 = ' '
                if structure['r744qrbn']:
                    status_2 = 'PRIM'
                    if structure['r744spri']:
                        status_2 += ' A'
                elif structure['r744qrbo']:
                    status_2 = 'SEC'
                    if structure['r744ssec']:
                        status_2 += ' A'
            else:
                status_1 = 'INACT'
                if structure['r744ssiz'] == 0:
                    status_1 = 'UNALLOC'
            if structure['r744styp'] == 3:
                enc = 'N/A'
            elif structure['r744senc']:
                enc = 'Yes'
            else:
                enc = 'No'
            size = structure['r744ssiz'] * 4 * 1024  # in kilobytes
            total_alloc_size += size
            total_cf_util += structure['r744setm']
            num_of_reqs = structure['r744strc'] if structure['r744styp'] != 3 else structure['r744ssrc']
            general_structure_detail.append(
                [f"{str_dict[structure['r744styp']] if ix == 0 else '':<8}",
                 f"{structure['r744qstr']:<16}", f"{status_1:<6}",
                 f"{'X' if structure['r744qtra'] or structure['r744qhol'] else ' ':1}",
                 f"{enc:<3}", f"{convert_bi(size, 3):>4}",
                 f"{size / (cf['r744gtsd'] * 4 * 1024) * 100:>4.1f}",
                 f"{convert_si(num_of_reqs, 9, comma=True):>}",
                 f"{num_of_reqs / total_reqs * 100:>4.1f}",
                 f"{structure['r744setm'] / total_pbsys * 100:>4.1f}",
                 f"{convert_si(num_of_reqs / cf['smf74int'], 7, 2):>9}",
                 f"{convert_si(structure['r744sdec'], 4, 0) if structure['r744styp'] == 4 else convert_si(structure['r744slel'], 4, 0):>5}",
                 f"{convert_si(structure['r744sdel'], 4, 0) if structure['r744styp'] == 4 else convert_si(structure['r744smae'], 4, 0):>5}",
                 f"{convert_si(structure['r744sltl'], 4, 0) if structure['r744styp'] in (2, 3) else 'N/A':>5}",
                 f"{convert_si(structure['r744cder'], 4, 0) if structure['r744styp'] == 4 else 'N/A':>5}"])
            general_structure_detail.append(
                ["", "", f"{status_2:<6}", "", "", "", "", "", "", "", "",
                 f"{convert_si(structure['r744cdec'], 4, 0) if structure['r744styp'] == 4 else convert_si(structure['r744slem'], 4, 0):>5}",
                 f"{convert_si(structure['r744cdac'], 4, 0) if structure['r744styp'] == 4 else convert_si(structure['r744scue'], 4, 0):>5}",
                 f"{convert_si(structure['r744sltm'], 4, 0) if structure['r744styp'] in (2, 3) else 'N/A':>5}",
                 f"{convert_si(structure['r744cxdr'], 4, 0) if structure['r744styp'] == 4 else 'N/A':>5}"]
            )
            if len(mscms_list[idx_1][ix]) > 0:
                has_scm_data = True
                if first_mscm_type is None:
                    first_mscm_type = str_dict[structure['r744styp']]
                scm_structure_detail.append(
                    [f"{str_dict[structure['r744styp']] if first_mscm_type is None else '':<8}",
                     f"{structure['r744qstr']:<16}", f"{'KP1' if structure['r744malg'] == 1 else 'UNK'}",
                     f"{convert_si(structure['r744msma'], 7, 0):>8}",
                     f"{convert_si(structure['r744mema'] * 4 * 1024, 5, 0):>6}",
                     f"{convert_si(structure['r744meml'], 5, 0):>6}",
                     f"{convert_si(structure['r744meme'], 5, 0):>6}",
                     f"{convert_si(structure['r744mrfc'] + structure['r744mrpc'], 5, 0):>6}",
                     f"{convert_si(structure['r744mrst'] * 1e6 / (structure['r744mrfc'] + structure['r744mrpc']), 7, 1) if (structure['r744mrfc'] + structure['r744mrpc']) > 0 else '0 ':>8}",
                     f"{convert_si(structure['r744mswc'], 5, 0):>6}",
                     f"{convert_si(structure['r744mwst'] * 1e6 / structure['r744mswc'], 7, 1) if structure['r744mswc'] > 0 else '0 ':>8}",
                     f"{convert_si(structure['r744maec'], 5, 0):>6}", f"{convert_si(structure['r744sosa'], 5, 0):>6}"])
                scm_structure_detail.append(
                    ["", "", "",
                     f"{structure['r744mius'] * 100 / structure['r744msma'] if structure['r744msma'] > 0 else 0:>5.1f}",
                     f"{structure['r744miua'] * 100 / structure['r744mema'] if structure['r744mema'] > 0 else 0:>5.1f}",
                     f"{convert_si(structure['r744menl'], 5, 0):>6}", f"{convert_si(structure['r744mene'], 5, 0):>6}",
                     f"{convert_bi(structure['r744mrbt'], 5):>6}",
                     f"{cal_std_dev(structure['r744mrfc'] + structure['r744mrpc'], structure['r744mrsq'], structure['r744mrst'] * 1e6):>6.1f}",
                     f"{convert_bi(structure['r744mwbt'], 5):>6}",
                     f"{cal_std_dev(structure['r744mswc'], structure['r744mwsq'], structure['r744mwst'] * 1e6):>6.1f}",
                     f"{structure['r744maec'] / (structure['r744ssrc'] + structure['r744sarc']) * 100 if structure['r744ssrc'] + structure['r744sarc'] > 0 else 0:>6.1f}",
                     f"{structure['r744sosa'] / (structure['r744ssrc'] + structure['r744sarc']) * 100 if structure['r744ssrc'] + structure['r744sarc'] > 0 else 0:>6.1f}"])

            if len(adups_list[idx_1][ix]) > 0:
                has_adup_data = True
                if first_adup_type is None:
                    first_adup_type = str_dict[structure['r744styp']]
                adup_detail.append(
                    [f"{str_dict[structure['r744styp']] if first_adup_type is None else '':<8}",
                     f"{structure['r744qstr']:<16}", f"{convert_si(structure['r744alco'], 6, 0):>7}",
                     f"{structure['r744aott'] * 1e6 / structure['r744atpoc'] if structure['r744atpoc'] > 0 else 0:>6.1f}",
                     f"{cal_std_dev(structure['r744atpoc'], structure['r744aotq'], structure['r744aott'] * 1e6):>6.1f}",
                     f"{structure['r744astt'] * 1e6 / structure['r744alco'] if structure['r744alco'] > 0 else 0:>6.1f}",
                     f"{cal_std_dev(structure['r744alco'], structure['r744astq'], structure['r744astt'] * 1e6):>6.1f}",
                     f"{convert_si(structure['r744sixc'], 5, 0):>6}", f"{convert_si(structure['r744sxsc'], 5, 0):>6}",
                     f"{structure['r744sxst'] * 1e6 / structure['r744sxsc'] if structure['r744sxsc'] > 0 else 0:>6.1f}",
                     f"{cal_std_dev(structure['r744sxsc'], structure['r744sxsq'], structure['r744sxst'] * 1e6):>6.1f}"]
                )

    general_structure_detail.append(
        ["", "", "", "", "", "----", "----", "-------", "----", "----", "-------"])
    general_structure_detail.append(
        [f"", "Structure Totals", "", "", "",
         f"{convert_bi(total_alloc_size, 3):>4}", f"{total_alloc_size / (cf['r744gtsd'] * 4 * 1024) * 100:>4.1f}",
         f"{convert_si(total_reqs, 6, comma=True):>8}", f"{total_reqs / total_reqs * 100:>4.0f}",
         f"{total_cf_util / total_pbsys * 100:>4.1f}",
         f"{convert_si(total_reqs / cf['smf74int'], 7, 2):>9}"]
    )
    # attach General Structure Summary to the report
    report += (tb.tabulate(general_structure_summary, tablefmt='plain') + '\n' +
               tb.tabulate(general_structure_detail, tablefmt='plain',
                           headers=structure_summary_header,
                           colalign=('left', 'left', 'center', 'left', 'right', 'right', 'right', 'right', 'right',
                                     'right', 'right', 'right', 'right', 'right'),
                           floatfmt=('', '', '', '', '.0f', '.1f', '.0f', '.1f', '.1f', '.2f', '.0f', '.0f', '.0f',
                                     '.0f')) + '\n\n')
    # attach SCM Structure Summary
    if has_scm_data:
        report += (tb.tabulate(scm_summary, tablefmt='plain') + '\n' +
                   tb.tabulate(scm_structure_detail, tablefmt='plain',
                               headers=scm_summary_header,
                               colalign=('left', 'left', 'left', 'right', 'right', 'right', 'right', 'right', 'right',
                                         'right', 'right', 'right', 'right'),
                               floatfmt=('', '', '', '.1f', '.1f', '.0f', '.0f', '.0f', '.1f', '.0f', '.1f', '.1f',
                                         '.1f')) + '\n')
    else:
        scm_summary.append(["                                No storage class memorty data available"])
        report += (tb.tabulate(scm_summary, tablefmt='plain') + '\n\n')
    # attach Asynchronous CF Duplexing Summary
    if has_adup_data:
        report += (tb.tabulate(adup_summary, tablefmt='plain') + '\n' +
                   tb.tabulate(adup_detail, tablefmt='plain',
                               headers=adup_summary_header,
                               colalign=('left', 'left', 'right', 'right', 'right', 'right', 'right', 'right', 'right',
                                         'right', 'right'),
                               floatfmt=('', '', '.0f', '.1f', '.1f', '.1f', '.1f', '.0f', '.0f', '.1f',
                                         '.1f')) + '\n\n')
    else:
        adup_summary.append(["                                No asynchronous CF duplexing data available"])
        report += (tb.tabulate(adup_summary, tablefmt='plain') + '\n\n')
    # attach Storage Summary
    report += (tb.tabulate(storage_summary, tablefmt='plain') + '\n' +
               tb.tabulate([
                   ["Total CF Storage Used By Structures", f"{convert_bi(cf['total_str_alloc'] * 4 * 1024, 5):>6}",
                    f"{cf['total_str_alloc'] / cf['r744gtsd'] * 100:>4.1f}"],
                   ["Total CF Dump Storage", f"{convert_bi(cf['r744gdsa'] * 4 * 1024, 5):>6}",
                    f"{cf['r744gdsa'] / cf['r744gtsd'] * 100:>4.1f}",
                    f"{(cf['r744gdsa'] * 4 * 1024 - cf['r744gdsf'] * 4 * 1024) / (cf['r744gdsa'] * 4 * 1024) * 100:>4.1f}",
                    f"{cf['r744gdsr'] / cf['r744gdsa'] * 100:>4.1f}"],
                   ["Total CF Augmented Space",
                    f"{convert_bi(cf['total_augmented_alloc'] * 4 * 1024, 5) if pd.notna(cf['total_augmented_alloc']) else '0K':>6}",
                    f"{cf['total_augmented_alloc'] / cf['r744gtsd'] * 100 if pd.notna(cf['total_augmented_alloc']) else 0:>4.1f}"],
                   ["Total CF Storage Available", f"{convert_bi(cf['r744gcsf'] * 4 * 1024, 5):>6}",
                    f"{cf['r744gcsf'] / cf['r744gtsd'] * 100:>4.1f}"],
                   ["", "-------"],
                   ["Total CF Storage Size", f"{convert_bi(cf['r744gtsd'] * 4 * 1024, 6):>7}"],
                   tb.SEPARATING_LINE,
                   ["", "Alloc\nSize", "% Allocated"],
                   ["Total Control Storage Defined", f"{convert_bi(cf['r744gcsd'] * 4 * 1024, 6):>7}",
                    f"{(cf['r744gcsd'] - cf['r744gcsf']) / cf['r744gcsd'] * 100:>4.1f}"],
                   ["Total Data Storage Defined", f"{convert_bi((cf['r744gtsd'] - cf['r744gcsd']) * 4 * 1024, 6):>7}",
                    f"{(cf['r744gtsd'] - cf['r744gcsd']) / cf['r744gcsd'] * 100:>4.1f}"],
                   tb.SEPARATING_LINE,
                   ["", "Assigned", "% In Use", "Sum Max SCM"],
                   ["Total CF Storage Class Memory", f"{convert_bi(cf['r744gtsc'] * 4 * 1024, 6):>7}",
                    f"{(cf['r744gtsc'] - cf['r744gfsc']) / cf['r744gtsc'] * 100 if cf['r744gtsc'] > 0 else 0:>4.1f}",
                    f"{convert_bi(cf['total_max_scm'] * 4 * 1024, 6) if pd.notna(cf['total_max_scm']) else '0K':>7}"]],
                   tablefmt='plain',
                   headers=["  ", "Alloc\nSize", "% of CF\nStorage", "----- Dump\n% In Use",
                            "Space ---------\nMax % Requested"],
                   colalign=('left', 'right', 'right', 'center', 'right'),
                   floatfmt=('', '.0f', '.1f', '.1f', '.1f')) + '\n')
    # attach processor summary
    return (report + '\n' + tb.tabulate(processor_summary, tablefmt='plain') + '\n' +
            tb.tabulate(processor_summary_detail, tablefmt='plain',
                        colalign=('left', 'center', 'right', 'right', 'left', 'left', 'left', 'right', 'left', 'right'),
                        floatfmt=('', '.0f', '', '.1f', '', '.0f', '', '.0f', '', '.1f')))


def format_cf_activity_report(duration, cf, strs, report_type, lcfs, procs, cfrfs, str_group_list,
                              chpas, sreqs, peer_cfs, dupchpas,
                              mscms_list, adups_list, str_type_list=None):
    # "CF Usage Summary", "Subchannel Activity", "CF to CF Activity", "CF Structure Activity"
    cf_structure_activity = [
        ["------------------------------------------------------------------------------------------------------------------------------"],
        [f" Coupling Facility Name = {cf['r744fnam']:<8}"],
        ["------------------------------------------------------------------------------------------------------------------------------"],
        ["                                           COUPLING  FACILITY  STRUCTURE  ACTIVITY"],
        ["------------------------------------------------------------------------------------------------------------------------------"],
    ]
    subchannel_header = [
        ["----------------------------------------------------------------------------------------------------------------------------------------------------------------"],
        [f"Coupling Facility Name = {cf['r744fnam']:<8}"],
        ["----------------------------------------------------------------------------------------------------------------------------------------------------------------"],
        ["                                                                 SUBCHANNEL  ACTIVITY"],
        ["----------------------------------------------------------------------------------------------------------------------------------------------------------------"],
        ["                                         No structure/storage data reportable"],
    ]
    report_detail = ""
    if report_type == "CF Usage Summary":
        return format_cf_summary(duration, cf, strs, lcfs, procs, str_group_list, mscms_list, adups_list)
    elif report_type == 'Subchannel Activity':
        if len(strs) == 0:
            return format_cf_header(duration, cf) + '\n' + tb.tabulate(subchannel_header, tablefmt='plain') + '\n'
        return format_subch_activity(duration, cf, lcfs, chpas)
    elif report_type == "CF to CF Activity":
        return format_cf2cf_activity(duration, cf, cfrfs, peer_cfs, dupchpas)
    else:
        contain_cf_structure_data = False
        report = format_cf_header(duration, cf)

        # str_group_list = [list(g) for k, g in groupby(strs, attrgetter('r744styp'))]
        for idx_1, str_group in enumerate(str_group_list):
            if len(str_type_list) > 0:
                if str_group[0]['r744styp'] not in str_type_list:
                    continue

            for idx_2, structure in enumerate(str_group):
                contain_cf_structure_data = True
                report_detail += format_str_activity(duration, structure, sreqs[idx_1][idx_2], cf['smf74int'])
        if not contain_cf_structure_data:
            cf_structure_activity.append(
                ["                                         No structure/storage data reportable"])
            return report + '\n' + tb.tabulate(cf_structure_activity, tablefmt='plain') + '\n'
        return report + '\n' + tb.tabulate(cf_structure_activity, tablefmt='plain') + '\n' + report_detail


def format_device_header(duration, dctl, pro, sync_io=None):
    if duration == 'Hourly':
        report_date = dctl['date']
        report_time = dctl['datetime'].time().strftime('%H.%M.%S')
        interval = format_s2min(pro['smf74int'])
    elif duration == 'Daily':
        report_date = dctl['date']
        report_time = '00.00.00'
        interval = format_s2hr(pro['smf74int'])
    else:
        report_date = dctl['smf74ist'].date()
        report_time = dctl['smf74ist'].time().strftime('%H.%M.%S')
        interval = format_s2min(pro['smf74int'])
    zos_ver = 'V' + pro['smf74mvs'][2:4].lstrip('0') + 'R' + pro['smf74mvs'][4:6].lstrip('0')
    interval_x = f"{interval[:-3]}"
    if dctl['smf74sub'] == "0020":
        if sync_io is None:
            title = 'D I R E C T   A C C E S S   D E V I C E   A C T I V I T Y'
        else:
            title = 'S Y N C H R O N O U S   I / O   D E V I C E   A C T I V I T Y'
    elif dctl['smf74sub'] == "0010":
        title = 'G R A P H I C S    D E V I C E   A C T I V I T Y'
    elif dctl['smf74sub'] == "0040":
        title = '          C O M M U N I C A T I O N   E Q U I P M E N T   A C T I V I T Y\n'
    elif dctl['smf74sub'] == "0080":
        title = '      M A G N E T I C   T A P E   D E V I C E   A C T I V I T Y\n'
    else:
        return None
    whitespace = ' '
    header1 = [[f"{title}"]]
    header2 = [
        [f"{whitespace:>12}", f"z/OS {zos_ver}", f"{whitespace:>13}", f"System ID {dctl['smf74sid']}", f"{whitespace:>6}",
         f"Date {report_date:%m/%d/%Y}", f"{whitespace:>11}", f"Interval {interval_x}"],
        ["", "", "", f"RMF Version {pro['smf74mfv']:<5}", "", f"Time {report_time}", "", f"Cycle {pro['smf74cyc'] / 1000:5.3f} Seconds"]
    ]
    header3 = [["Total Samples =", f"{pro['smf74sam']:,}", " ",
                "IODF =", f"{dctl['smf74tsf']:2}", " ",
                "Cr-Date:", f"{dctl['smf74tdt'].date():%m/%d/%Y}", " ",
                "Cr-Time:", f"{dctl['smf74tdt'].time():%H.%M.%S}", "  ",
                "Act:", f"{'Activate' if dctl['config_changed_since_ipl'] else 'POR'}"]]
    return (tb.tabulate(header1, tablefmt="plain") + "\n\n" +
            tb.tabulate(header2, tablefmt="plain") + "\n" +
            tb.tabulate(header3, tablefmt="plain") + "\n")


def format_device_detail(devs, interval, total_number_of_samples, sub):
    device_activity_rate_dict = {}
    sync_device_read_activity_rate_dict = {}
    sync_device_write_activity_rate_dict = {}
    avg_resp_time_atv_dict = {}
    avg_resp_time_mec_dict = {}
    avg_resp_time_que_dict = {}
    avg_resp_time_ssc_dict = {}
    sync_avg_read_resp_time_spr_dict = {}
    sync_avg_read_resp_time_sqr_dict = {}
    sync_avg_write_resp_time_spw_dict = {}
    sync_avg_write_resp_time_sqw_dict = {}
    sync_read_xfer_rate_dict = {}
    sync_write_xfer_rate_dict = {}
    sync_req_success_dict = {}
    sync_total_req_dict = {}
    sync_link_busy_dict = {}
    sync_cache_miss_dict = {}
    sync_timeout_dict = {}
    sync_rej_read_dict = {}
    sync_rej_write_dict = {}
    avg_iosq_time_ios_dict = {}
    avg_cmr_dly_cmr_dict = {}
    avg_db_dly_dvb_dict = {}
    avg_int_dly_idt_dict = {}
    avg_pend_time_pen_dict = {}
    avg_disc_time_dis_dict = {}
    avg_conn_time_cnn_dict = {}
    dev_conn_percent_dict = {}
    dev_util_percent_dict = {}
    dev_resv_percent_dict = {}
    avg_numbr_alloc_nda_dict = {}
    any_alloc_percent_dict = {}
    num_of_mts_dict = {}
    mt_pend_percent_dict = {}
    not_ready_percent_dict = {}
    avg_mt_time_mtp_dict = {}
    avg_mt_time_mtc_dict = {}
    time_dev_alloc_dict = {}
    dev_count_dict = {}
    total_number_of_samples_dict = {}
    sync_io = None
    if len(devs) == 0:
        return None, None
    detail = []
    sync_detail = []
    for dev in devs:
        if dev['smf74lcu'] not in dev_count_dict:
            dev_count_dict[dev['smf74lcu']] = 0
            total_number_of_samples_dict[dev['smf74lcu']] = 0
            sync_device_read_activity_rate_dict[dev['smf74lcu']] = 0
            sync_device_write_activity_rate_dict[dev['smf74lcu']] = 0
            sync_avg_read_resp_time_spr_dict[dev['smf74lcu']] = 0
            sync_avg_read_resp_time_sqr_dict[dev['smf74lcu']] = 0
            sync_avg_write_resp_time_spw_dict[dev['smf74lcu']] = 0
            sync_avg_write_resp_time_sqw_dict[dev['smf74lcu']] = 0
            sync_read_xfer_rate_dict[dev['smf74lcu']] = 0
            sync_write_xfer_rate_dict[dev['smf74lcu']] = 0
            sync_req_success_dict[dev['smf74lcu']] = 0
            sync_link_busy_dict[dev['smf74lcu']] = 0
            sync_cache_miss_dict[dev['smf74lcu']] = 0
            sync_timeout_dict[dev['smf74lcu']] = 0
            sync_rej_read_dict[dev['smf74lcu']] = 0
            sync_rej_write_dict[dev['smf74lcu']] = 0
            sync_total_req_dict[dev['smf74lcu']] = 0
            device_activity_rate_dict[dev['smf74lcu']] = 0
            avg_resp_time_atv_dict[dev['smf74lcu']] = 0
            avg_resp_time_mec_dict[dev['smf74lcu']] = 0
            avg_resp_time_que_dict[dev['smf74lcu']] = 0
            avg_resp_time_ssc_dict[dev['smf74lcu']] = 0
            avg_iosq_time_ios_dict[dev['smf74lcu']] = 0
            avg_cmr_dly_cmr_dict[dev['smf74lcu']] = 0
            avg_db_dly_dvb_dict[dev['smf74lcu']] = 0
            avg_int_dly_idt_dict[dev['smf74lcu']] = 0
            avg_pend_time_pen_dict[dev['smf74lcu']] = 0
            avg_disc_time_dis_dict[dev['smf74lcu']] = 0
            avg_conn_time_cnn_dict[dev['smf74lcu']] = 0
            dev_conn_percent_dict[dev['smf74lcu']] = 0
            dev_util_percent_dict[dev['smf74lcu']] = 0
            dev_resv_percent_dict[dev['smf74lcu']] = 0
            avg_numbr_alloc_nda_dict[dev['smf74lcu']] = 0
            any_alloc_percent_dict[dev['smf74lcu']] = 0
            mt_pend_percent_dict[dev['smf74lcu']] = 0
            not_ready_percent_dict[dev['smf74lcu']] = 0
            num_of_mts_dict[dev['smf74lcu']] = 0
            avg_mt_time_mtp_dict[dev['smf74lcu']] = 0
            avg_mt_time_mtc_dict[dev['smf74lcu']] = 0
            time_dev_alloc_dict[dev['smf74lcu']] = 0
        pav = dev['smf74nux'] if not dev['hpv'] else dev['smf74nux'] / dev['smf74psm']
        if dev['sta']:
            if dev['sir'] or dev['siw']:
                sync_io = True
                sync_device_read_activity_rate_dict[dev['smf74lcu']] += dev['sync_device_read_activity_rate']
                sync_device_write_activity_rate_dict[dev['smf74lcu']] += dev['sync_device_write_activity_rate']
                sync_avg_read_resp_time_spr_dict[dev['smf74lcu']] += dev['smf74spr']
                sync_avg_read_resp_time_sqr_dict[dev['smf74lcu']] += dev['smf74sqr']
                sync_avg_write_resp_time_spw_dict[dev['smf74lcu']] += dev['smf74spw']
                sync_avg_write_resp_time_sqw_dict[dev['smf74lcu']] += dev['smf74sqw']
                sync_read_xfer_rate_dict[dev['smf74lcu']] += dev['sync_read_xfer_rate']
                sync_write_xfer_rate_dict[dev['smf74lcu']] += dev['sync_write_xfer_rate']
                sync_req_success_dict[dev['smf74lcu']] += dev['sync_req_success']
                sync_link_busy_dict[dev['smf74lcu']] += dev['sync_link_busy']
                sync_cache_miss_dict[dev['smf74lcu']] += dev['sync_cache_miss']
                sync_timeout_dict[dev['smf74lcu']] += dev['sync_timeout']
                sync_rej_read_dict[dev['smf74lcu']] += dev['sync_rej_read']
                sync_rej_write_dict[dev['smf74lcu']] += dev['sync_rej_write']
                sync_total_req_dict[dev['smf74lcu']] += dev['sync_total_req']
            dev_count_dict[dev['smf74lcu']] += 1
            total_number_of_samples_dict[dev['smf74lcu']] += total_number_of_samples
            device_activity_rate_dict[dev['smf74lcu']] += dev['device_activity_rate']
            avg_resp_time_atv_dict[dev['smf74lcu']] += dev['smf74atv']
            avg_resp_time_mec_dict[dev['smf74lcu']] += dev['smf74mec']
            avg_resp_time_que_dict[dev['smf74lcu']] += dev['smf74que']
            avg_resp_time_ssc_dict[dev['smf74lcu']] += dev['smf74ssc']
            avg_iosq_time_ios_dict[dev['smf74lcu']] += dev['smf74ios']
            avg_cmr_dly_cmr_dict[dev['smf74lcu']] += dev['smf74cmr']
            avg_db_dly_dvb_dict[dev['smf74lcu']] += dev['smf74dvb']
            avg_int_dly_idt_dict[dev['smf74lcu']] += dev['smf74idt']
            avg_pend_time_pen_dict[dev['smf74lcu']] += dev['smf74pen']
            avg_disc_time_dis_dict[dev['smf74lcu']] += dev['smf74dis']
            avg_conn_time_cnn_dict[dev['smf74lcu']] += dev['smf74cnn']
            dev_conn_percent_dict[dev['smf74lcu']] += dev['dev_conn_percent']
            dev_util_percent_dict[dev['smf74lcu']] += dev['dev_util_percent']
            dev_resv_percent_dict[dev['smf74lcu']] += dev['dev_resv_percent']
            avg_numbr_alloc_nda_dict[dev['smf74lcu']] += dev['smf74nda']
            any_alloc_percent_dict[dev['smf74lcu']] += dev['any_alloc_percent']
            mt_pend_percent_dict[dev['smf74lcu']] += dev['mt_pend_percent']
            not_ready_percent_dict[dev['smf74lcu']] += dev['not_ready_percent']
            num_of_mts_dict[dev['smf74lcu']] += dev['smf74mtc']
            avg_mt_time_mtp_dict[
                dev['smf74lcu']] += dev['smf74mtp']  # * interval/total_number_of_samples/dev.mtc if dev.mtc > 0 else 0)
            avg_mt_time_mtc_dict[dev['smf74lcu']] += dev['smf74mtc']
            time_dev_alloc_dict[dev['smf74lcu']] += dev['time_dev_alloc']
        if sub == "0020":
            if dev['sta']:
                avg_resp_time = dev['avg_pend_time'] + dev['avg_disc_time'] + dev['avg_conn_time'] + dev['avg_iosq_time']
                detail.append(
                    [f"{dev['smf74sgn']:>8}",
                     f"{dev['smf74scs']:1}{dev['smf74num']:>4}",
                     f"{dev['smf74dev']:<8}",
                     f"{dev['smf74cap']:>6}",
                     f"{dev['smf74ser']:<7}",
                     f"{pav:>4.1f}{'H' if dev['hpv'] else ' ':1}",
                     f"{dev['smf74lcu']:4}",
                     f"{convert_si(dev['device_activity_rate'], 6, 3):>7}{'S' if dev['sir'] or dev['siw'] else ' '}",
                     f"{convert_si(avg_resp_time * 1000, 5, 3) if pd.notna(avg_resp_time) else '-':>5}",
                     f"{convert_si(dev['avg_iosq_time'] * 1000, 5, 3):>5}",
                     f"{convert_si(dev['avg_cmr_dly'] * 1000, 5, 3):>5}",
                     f"{convert_si(dev['avg_db_dly'] * 1000, 5, 3):>5}",
                     f"{convert_si(dev['avg_int_dly'] * 1000, 5, 3):>5}",
                     f"{convert_si(dev['avg_pend_time'] * 1000, 6, 3):>6}",
                     f"{convert_si(dev['avg_disc_time'] * 1000, 5, 3):>5}",
                     f"{convert_si(dev['avg_conn_time'] * 1000, 5, 3):>5}",
                     f"{dev['dev_conn_percent']:>6.2f}",
                     f"{dev['dev_util_percent']:>6.2f}",
                     f"{dev['dev_resv_percent']:>5.2f}",
                     f"{dev['avg_numbr_alloc']:{'>6.2f' if dev['avg_numbr_alloc'] < 100 else '>6.0f'}}",
                     f"{dev['any_alloc_percent']:>6.2f}"
                     ])
                if dev['sir'] or dev['siw']:
                    sync_detail.append(
                        [f"{dev['smf74sgn']:>8}",
                         f"{dev['smf74scs']:1}{dev['']:>4}",
                         f"{dev['smf74dev']:<8}",
                         f"{dev['smf74ser']:<7}",
                         f"{dev['smf74lcu']:4}",
                         f"{dev['sync_device_read_activity_rate']:{'>7.3f' if dev['sync_device_read_activity_rate'] < 1000 else '>7.2f'}}",
                         f"{dev['sync_device_write_activity_rate']:{'>7.3f' if dev['sync_device_write_activity_rate'] < 1000 else '>7.2f'}}",
                         f"{dev['device_activity_rate']:{'>8.3f' if dev['device_activity_rate'] < 1000 else '>8.2f'}}",
                         f"{dev['sync_avg_read_resp_time'] * 1000:>6.3f},{dev['sync_avg_write_resp_time'] * 1000:>6.3f}",
                         f"{dev['avg_resp_time'] * 1000 if pd.notna(dev['avg_resp_time']) else 0:>6.3f}",
                         f"{dev['sync_read_xfer_rate']:>6.3f},{dev['sync_write_xfer_rate']:>7.3f}",
                         f"{dev['sync_req_success'] / dev['sync_total_req'] * 100 if dev['sync_total_req'] > 0 else 0:>6.2f}",
                         f"{dev['sync_link_busy'] / dev['sync_total_req'] * 100 if dev['sync_total_req'] > 0 else 0:>6.2f}",
                         f"{dev['sync_cache_miss'] / dev['sync_total_req'] * 100 if dev['sync_total_req'] > 0 else 0:>6.2f}",
                         f"{dev['sync_rej_read'] / dev['sync_total_req'] * 100 if dev['sync_total_req'] > 0 else 0:>6.2f}",
                         f"{dev['sync_rej_write'] / dev['sync_total_req'] * 100 if dev['sync_total_req'] > 0 else 0:>6.2f}"
                         ])
            else:
                detail.append(
                    [f"{dev['smf74sgn']:>8}",
                     f"{dev['smf74scs']:1}{dev['smf74num']:>4}",
                     f"{dev['smf74dev']:<8}", f"{dev['smf74cap']:>6}",
                     f"{dev['smf74ser']:<7}",
                     f"{pav:>4.1f}{'H' if dev['hpv'] else ' ':1}",
                     f"{dev['smf74lcu']:4}",
                     "Offline"
                     ])
                if dev['sir'] or dev['siw']:
                    sync_detail.append(
                        [f"{dev['smf74sgn']:>8}",
                         f"{dev['smf74scs']:1}{dev['smf74num']:>4}",
                         f"{dev['smf74dev']:<8}",
                         f"{dev['smf74ser']:<7}",
                         f"{dev['smf74lcu']:4}",
                         "Offline"
                         ])

        elif sub == "0010":
            if dev['sta']:
                detail.append(
                    [f"{dev['smf74scs']:1}{dev['smf74num']:>4}",
                     f"{dev['smf74dev']:<8}", f"{dev['smf74ser']:<7}",
                     f"{dev['smf74lcu']:4}",
                     f"{convert_si(dev['device_activity_rate'], 6, 3):>7}",
                     f"{convert_si(dev['avg_resp_time'] * 1000 if pd.notna(dev['avg_resp_time']) else 0, 5, 3):>5}",
                     f"{convert_si(dev['avg_iosq_time'] * 1000, 5, 3):>5}",
                     f"{convert_si(dev['avg_cmr_dly'] * 1000, 5, 3):>5}",
                     f"{convert_si(dev['avg_db_dly'] * 1000, 5, 3):>5}",
                     f"{convert_si(dev['avg_int_dly'] * 1000, 5, 3):>5}",
                     f"{convert_si(dev['avg_pend_time'] * 1000, 6, 3):>6}",
                     f"{convert_si(dev['avg_disc_time'] * 1000, 5, 3):>5}",
                     f"{convert_si(dev['avg_conn_time'] * 1000, 5, 3):>5}",
                     f"{dev['dev_conn_percent']:>6.2f}",
                     f"{dev['dev_util_percent']:>6.2f}",
                     f"{dev['dev_resv_percent']:>5.2f}",
                     f"{dev['any_alloc_percent']:>6.2f}",
                     f"{dev['not_ready_percent']:{'>6.2f' if dev['not_ready_percent'] > 0 else '>6.0f'}}"
                     ])
            else:
                detail.append(
                    [f"{dev['smf74scs']:1}{dev['smf74num']:>4}",
                     f"{dev['smf74dev']:<8}",
                     f"{dev['smf74ser']:<7}{dev['smf74lcu']:4}",
                     "Offline"])
        elif sub == "0040":
            if dev['sta']:
                detail.append(
                    ["", f"{dev['smf74scs']:1}{dev['smf74num']:>4}", "", "",
                     f"{dev['smf74lcu']:4}",
                     f"{convert_si(dev['device_activity_rate'], 6, 3):>7}",
                     f"{convert_si(dev['avg_resp_time'] * 1000 if pd.notna(dev['avg_resp_time']) else 0, 5, 3):>5}",
                     f"{convert_si(dev['avg_iosq_time'] * 1000, 5, 3):>5}",
                     f"{convert_si(dev['avg_cmr_dly'] * 1000, 5, 3):>5}",
                     f"{convert_si(dev['avg_db_dly'] * 1000, 5, 3):>5}",
                     f"{convert_si(dev['avg_int_dly'] * 1000, 5, 3):>5}",
                     f"{convert_si(dev['avg_pend_time'] * 1000, 6, 3):>6}",
                     f"{convert_si(dev['avg_disc_time'] * 1000, 5, 3):>5}",
                     f"{convert_si(dev['avg_conn_time'] * 1000, 5, 3):>5}",
                     f"{dev['dev_conn_percent']:>6.2f}",
                     f"{dev['dev_util_percent']:>6.2f}", f"{dev['dev_resv_percent']:>5.2f}",
                     f"{dev['any_alloc_percent']:>6.2f}",
                     f"{dev['not_ready_percent']:{'>6.2f' if dev['not_ready_percent'] > 0 else '>6.0f'}}"
                     ])
            else:
                detail.append(
                    ["", f"{dev['smf74scs']:1}{dev['smf74num']:>4}",
                     "", "",
                     f"{dev['smf74lcu']:4}",
                     "Offline"])
        elif sub == "0080":
            if dev['sta']:
                avg_mt_time = pd.to_datetime(0) + pd.to_timedelta(dev['avg_mt_time'], unit='s')
                time_dev_alloc = pd.to_datetime(0) + pd.to_timedelta(dev['time_dev_alloc'], unit='s')
                detail.append(
                    ["", f"{dev['smf74scs']:1}{dev['smf74num']:>4}",
                     f"{dev['smf74dev']:<8}",
                     f"{dev['smf74ser']:<7}",
                     f"{dev['smf74lcu']:4}",
                     f"{convert_si(dev['device_activity_rate'], 6, 3):>7}",
                     f"{convert_si(dev['avg_resp_time'] * 1000 if pd.notna(dev['avg_resp_time']) else 0, 5, 3):>5}",
                     f"{convert_si(dev['avg_iosq_time'] * 1000, 5, 3):>5}",
                     f"{convert_si(dev['avg_cmr_dly'] * 1000, 5, 3):>5}",
                     f"{convert_si(dev['avg_db_dly'] * 1000, 5, 3):>5}",
                     f"{convert_si(dev['avg_int_dly'] * 1000, 5, 3):>5}",
                     f"{convert_si(dev['avg_pend_time'] * 1000, 6, 3):>6}",
                     f"{convert_si(dev['avg_disc_time'] * 1000, 5, 3):>5}",
                     f"{convert_si(dev['avg_conn_time'] * 1000, 5, 3):>5}",
                     f"{dev['dev_conn_percent']:>6.2f}",
                     f"{dev['dev_util_percent']:>6.2f}",
                     f"{dev['dev_resv_percent']:>5.2f}",
                     f"{dev['num_of_mts']:>6.0f}",
                     f"{avg_mt_time:%H:%M:%S}",
                     f"{time_dev_alloc:%H:%M:%S}"
                     ])
            else:
                detail.append(
                    ["", f"{dev['smf74scs']:1}{dev['smf74num']:>4}",
                     f"{dev['smf74dev']:<8}",
                     f"{dev['smf74ser']:<7}",
                     f"{dev['smf74lcu']:4}",
                     "Offline"])
        else:
            break
    sync_avg_read_resp_time = (sync_avg_read_resp_time_spr_dict[devs[-1]['smf74lcu']] /
                               (sync_avg_read_resp_time_sqr_dict[devs[-1]['smf74lcu']] * 2000) if
                               sync_avg_read_resp_time_sqr_dict[devs[-1]['smf74lcu']] > 0 else 0)
    sync_avg_write_resp_time = (sync_avg_write_resp_time_spw_dict[devs[-1]['smf74lcu']] /
                                (sync_avg_write_resp_time_sqw_dict[devs[-1]['smf74lcu']] * 2000) if
                                sync_avg_write_resp_time_sqw_dict[devs[-1]['smf74lcu']] > 0 else 0)
    device_active_time = avg_resp_time_atv_dict[devs[-1]['smf74lcu']] / avg_resp_time_mec_dict[devs[-1]['smf74lcu']] if \
    avg_resp_time_mec_dict[devs[-1]['smf74lcu']] > 0 else 0
    if devs[-1]['smf74sub'] != '0080':
        iosq_time = avg_resp_time_que_dict[devs[-1]['smf74lcu']] / total_number_of_samples_dict[devs[-1]['smf74lcu']] / (
                (avg_resp_time_ssc_dict[devs[-1]['smf74lcu']] / interval) / dev_count_dict[devs[-1]['smf74lcu']]) if \
        avg_resp_time_ssc_dict[devs[-1]['smf74lcu']] > 0 else 0
    else:
        iosq_time = avg_iosq_time_ios_dict[devs[-1]['smf74lcu']] / avg_resp_time_ssc_dict[devs[-1]['smf74lcu']] if \
        avg_resp_time_ssc_dict[devs[-1]['smf74lcu']] > 0 else 0
    avg_resp_time = (device_active_time + iosq_time) * 1000
    avg_iosq_time = (
        avg_iosq_time_ios_dict[devs[-1]['smf74lcu']] / avg_resp_time_ssc_dict[devs[-1]['smf74lcu']] * 1000 if
        avg_resp_time_ssc_dict[devs[-1]['smf74lcu']] > 0 else 0)
    avg_cmr_dly = (
        avg_cmr_dly_cmr_dict[devs[-1]['smf74lcu']] / avg_resp_time_mec_dict[devs[-1]['smf74lcu']] * 1000 if
        avg_resp_time_mec_dict[devs[-1]['smf74lcu']] > 0 else 0)
    avg_db_dly = (
        avg_db_dly_dvb_dict[devs[-1]['smf74lcu']] / avg_resp_time_mec_dict[devs[-1]['smf74lcu']] * 1000 if
        avg_resp_time_mec_dict[devs[-1]['smf74lcu']] > 0 else 0)
    avg_int_dly = (
        avg_int_dly_idt_dict[devs[-1]['smf74lcu']] / avg_resp_time_mec_dict[devs[-1]['smf74lcu']] * 1000 if
        avg_resp_time_mec_dict[devs[-1]['smf74lcu']] > 0 else 0)
    avg_pend_time = (
        avg_pend_time_pen_dict[devs[-1]['smf74lcu']] / avg_resp_time_mec_dict[devs[-1]['smf74lcu']] * 1000 if
        avg_resp_time_mec_dict[devs[-1]['smf74lcu']] > 0 else 0)
    avg_disc_time = (
        avg_disc_time_dis_dict[devs[-1]['smf74lcu']] / avg_resp_time_mec_dict[devs[-1]['smf74lcu']] * 1000 if
        avg_resp_time_mec_dict[devs[-1]['smf74lcu']] > 0 else 0)
    avg_conn_time = (
        avg_conn_time_cnn_dict[devs[-1]['smf74lcu']] / avg_resp_time_mec_dict[devs[-1]['smf74lcu']] * 1000 if
        avg_resp_time_mec_dict[devs[-1]['smf74lcu']] > 0 else 0)
    avg_numbr_alloc = (avg_numbr_alloc_nda_dict[devs[-1]['smf74lcu']] / total_number_of_samples)
    avg_mt_time = (
        avg_mt_time_mtp_dict[devs[-1]['smf74lcu']] * interval / total_number_of_samples / avg_mt_time_mtc_dict[devs[-1]['smf74lcu']] if
        avg_mt_time_mtc_dict[devs[-1]['smf74lcu']] > 0 else 0)
    if sub == "0020":
        detail.append(tb.SEPARATING_LINE)
        detail.append(
            ["", "", "", "", " LCU ", "",
             f"{devs[-1]['smf74lcu']:4}",
             f"{convert_si(device_activity_rate_dict[devs[-1]['smf74lcu']], 6, 3):>7}",
             f"{convert_si(avg_resp_time, 5, 3):>5}",
             f"{convert_si(avg_iosq_time, 5, 3):>5}",
             f"{convert_si(avg_cmr_dly, 5, 3):>5}",
             f"{convert_si(avg_db_dly, 5, 3):>5}",
             f"{convert_si(avg_int_dly, 5, 3):>5}",
             f"{convert_si(avg_pend_time, 6, 3):>6}",
             f"{convert_si(avg_disc_time, 5, 3):>5}",
             f"{convert_si(avg_conn_time, 5, 3):>5}",
             f"{dev_conn_percent_dict[devs[-1]['smf74lcu']] / dev_count_dict[devs[-1]['smf74lcu']] if dev_count_dict[devs[-1]['smf74lcu']] > 0 else '----':{'>6.2f' if dev_count_dict[devs[-1]['smf74lcu']] > 0 else '>6'}}",
             f"{dev_util_percent_dict[devs[-1]['smf74lcu']] / dev_count_dict[devs[-1]['smf74lcu']] if dev_count_dict[devs[-1]['smf74lcu']] > 0 else '----':{'>6.2f' if dev_count_dict[devs[-1]['smf74lcu']] > 0 else '>6'}}",
             f"{dev_resv_percent_dict[devs[-1]['smf74lcu']] / dev_count_dict[devs[-1]['smf74lcu']] if dev_count_dict[devs[-1]['smf74lcu']] > 0 else '----':{'>5.2f' if dev_count_dict[devs[-1]['smf74lcu']] > 0 else '>5'}}",
             f"{avg_numbr_alloc:{'>6.2f' if avg_numbr_alloc < 100 else '>6.0f'}}",
             f"{any_alloc_percent_dict[devs[-1]['smf74lcu']] / dev_count_dict[devs[-1]['smf74lcu']] if dev_count_dict[devs[-1]['smf74lcu']] > 0 else '----':{'>6.2f' if dev_count_dict[devs[-1]['smf74lcu']] > 0 else '>6'}}"
             ])
        detail.append(tb.SEPARATING_LINE)
        if sync_io:
            sync_detail.append(
                ["", "", "", " LCU ",
                 f"{devs[-1]['smf74lcu']:4}",
                 f"{convert_si(sync_device_read_activity_rate_dict[devs[-1]['smf74lcu']], 6, 3):>7}",
                 f"{convert_si(sync_device_write_activity_rate_dict[devs[-1]['smf74lcu']], 6, 3):>7}",
                 f"{convert_si(device_activity_rate_dict[devs[-1]['smf74lcu']], 7, 3):>8}",
                 f"{convert_si(sync_avg_read_resp_time, 6, 3):>6}",
                 f"{convert_si(sync_avg_write_resp_time, 6, 3):>6}",
                 f"{convert_si(avg_resp_time, 6, 3):>6}",
                 f"{convert_si(sync_read_xfer_rate_dict[devs[-1]['smf74lcu']], 6, 3):>6}",
                 f"{convert_si(sync_write_xfer_rate_dict[devs[-1]['smf74lcu']], 6, 3):>7}",
                 f"{sync_req_success_dict[devs[-1]['smf74lcu']] / sync_total_req_dict[devs[-1]['smf74lcu']] * 100 if sync_total_req_dict[devs[-1]['smf74lcu']] > 0 else 0:>6.2f}",
                 f"{sync_link_busy_dict[devs[-1]['smf74lcu']] / sync_total_req_dict[devs[-1]['smf74lcu']] * 100 if sync_total_req_dict[devs[-1]['smf74lcu']] > 0 else 0:>6.2f}",
                 f"{sync_cache_miss_dict[devs[-1]['smf74lcu']] / sync_total_req_dict[devs[-1]['smf74lcu']] * 100 if sync_total_req_dict[devs[-1]['smf74lcu']] > 0 else 0:>6.2f}",
                 f"{sync_rej_read_dict[devs[-1]['smf74lcu']] / sync_total_req_dict[devs[-1]['smf74lcu']] * 100 if sync_total_req_dict[devs[-1]['smf74lcu']] > 0 else 0:>6.2f}",
                 f"{sync_rej_write_dict[devs[-1]['smf74lcu']] / sync_total_req_dict[devs[-1]['smf74lcu']] * 100 if sync_total_req_dict[devs[-1]['smf74lcu']] > 0 else 0:>6.2f}"
                 ])
            detail.append(tb.SEPARATING_LINE)
            return (tb.tabulate(detail, tablefmt="plain",
                                floatfmt=(
                                    "", "", "", "", "", "", "", ".3f", ".3f", ".3f", ".3f", ".3f", ".3f", ".3f", ".3f",
                                    ".3f", ".2f", ".2f",
                                    ".2f", ".2f", ".2f"),
                                headers=[" \nStorage\nGroup", " \nDev\nNum", " \nDevice\nType", " \nNumber\nOf Cyl",
                                         " \nVolume\nSerieal",
                                         " \nPav", " \nLCU",
                                         "Device\nActivity\nRate", "Avg\nResp\nTime", "Avg\nIOSQ\nTime",
                                         "Avg\nCMR\nDly", "Avg\nDb\nDly",
                                         "Avg\nInt\nDly", "Avg\nPend\nTime", "Avg\nDisc\nTime", "Avg\nConn\nTime",
                                         "%\nDev\nConn",
                                         "%\nDev\nUtil", "%\nDev\nResv", "Avg\nNmbr\nAlloc", "%\nAny\nAlloc"]),
                    tb.tabulate(sync_detail, tablefmt="plain", numalign="right",
                                floatfmt=(
                                    "", "", "", "", "", ".3f", ".3f", ".3f", ".3f", ".3f", ".3f", ".3f", ".3f", ".2f",
                                    ".2f", ".2f",
                                    ".2f", ".2f"),
                                headers=[" \nStorage\nGroup", " \nDev\nNum", " \nDevice\nType",
                                         " \nVolumne\nSerial", " \nLCU",
                                         "-DEVICE\n-- Sync\nRead", "ACTIVITY\nI/O --\nWrite", "RATE -\nAsynch\nI/O",
                                         "--AVG\n-Synch\nRead", "RESP\nI/O -\nWrite", "TIME --\nAsynch\nI/O",
                                         "AVG SYNCH\nTransfer\nRead", " I/O\nRate\nWrite",
                                         "%\nReq\nSuccess", "%\nLink\nBusy", "%\nCache\nMiss", "%\n--Rej\nRead",
                                         "ects--\nWrite"]))
        return (tb.tabulate(detail, tablefmt="plain", numalign="right",
                            floatfmt=(
                                "", "", "", "", "", "", "", ".3f", ".3f", ".3f", ".3f", ".3f", ".3f", ".3f", ".3f",
                                ".3f", ".2f", ".2f",
                                ".2f", ".2f", ".2f"),
                            headers=[" \nStorage\nGroup", " \nDev\nNum", " \nDevice\nType", " \nNumber\nOf Cyl",
                                     " \nVolume\nSerieal",
                                     " \nPav", " \nLCU",
                                     "Device\nActivity\nRate", "Avg\nResp\nTime", "Avg\nIOSQ\nTime",
                                     "Avg\nCMR\nDly", "Avg\nDb\nDly",
                                     "Avg\nInt\nDly", "Avg\nPend\nTime", "Avg\nDisc\nTime", "Avg\nConn\nTime",
                                     "%\nDev\nConn",
                                     "%\nDev\nUtil", "%\nDev\nResv", "Avg\nNmbr\nAlloc", "%\nAny\nAlloc"]),
                None)
    elif sub == "0010":
        detail.append(tb.SEPARATING_LINE)
        detail.append(
            ["", "", " LCU ",
             f"{devs[-1]['smf74lcu']:4}",
             f"{convert_si(device_activity_rate_dict[devs[-1]['smf74lcu']], 6, 3):>7}",
             f"{convert_si(avg_resp_time, 5, 3):>5}",
             f"{convert_si(avg_iosq_time, 5, 3):>5}",
             f"{convert_si(avg_cmr_dly, 5, 3):>5}",
             f"{convert_si(avg_db_dly, 5, 3):>5}",
             f"{convert_si(avg_int_dly, 5, 3):>5}",
             f"{convert_si(avg_pend_time, 5, 3):>6}",
             f"{convert_si(avg_disc_time, 5, 3):>5}",
             f"{convert_si(avg_conn_time, 5, 3):>5}",
             f"{dev_conn_percent_dict[devs[-1]['smf74lcu']] / dev_count_dict[devs[-1]['smf74lcu']] if dev_count_dict[devs[-1]['smf74lcu']] > 0 else '----':{'>6.2f' if dev_count_dict[devs[-1]['smf74lcu']] > 0 else '>6'}}",
             f"{dev_util_percent_dict[devs[-1]['smf74lcu']] / dev_count_dict[devs[-1]['smf74lcu']] if dev_count_dict[devs[-1]['smf74lcu']] > 0 else '----':{'>6.2f' if dev_count_dict[devs[-1]['smf74lcu']] > 0 else '>6'}}",
             f"{dev_resv_percent_dict[devs[-1]['smf74lcu']] / dev_count_dict[devs[-1]['smf74lcu']] if dev_count_dict[devs[-1]['smf74lcu']] > 0 else '----':{'>5.2f' if dev_count_dict[devs[-1]['smf74lcu']] > 0 else '>5'}}",
             f"{any_alloc_percent_dict[devs[-1]['smf74lcu']] / dev_count_dict[devs[-1]['smf74lcu']] if dev_count_dict[devs[-1]['smf74lcu']] > 0 else '----':{'>6.2f' if dev_count_dict[devs[-1]['smf74lcu']] > 0 else '>6'}}",
             f"{not_ready_percent_dict[devs[-1]['smf74lcu']] / dev_count_dict[devs[-1]['smf74lcu']] if dev_count_dict[devs[-1]['smf74lcu']] > 0 else '----':{'>6.2f' if dev_count_dict[devs[-1]['smf74lcu']] > 0 else '>6'}}"
             ])
        detail.append(tb.SEPARATING_LINE)
        return (tb.tabulate(detail, tablefmt="plain", numalign="right",
                            floatfmt=(
                                "", "", "", "", ".3f", ".3f", ".3f", ".3f", ".3f", ".3f", ".3f", ".3f", ".3f", ".2f",
                                ".2f",
                                ".2f", ".2f", ".2f"),
                            headers=[" \nDev\nNum", " \nDevice\nType", " \nVolume\nSerieal", " \nLCU",
                                     "Device\nActivity\nRate", "Avg\nResp\nTime", "Avg\nIOSQ\nTime",
                                     "Avg\nCMR\nDly", "Avg\nDb\nDly",
                                     "Avg\nInt\nDly", "Avg\nPend\nTime", "Avg\nDisc\nTime", "Avg\nConn\nTime",
                                     "%\nDev\nConn",
                                     "%\nDev\nUtil", "%\nDev\nResv", "Avg\nNmbr\nAlloc", "%\nAny\nAlloc",
                                     "%\nMount\nPend", "%\nNot\nReady"]),
                None)
    elif sub == "0040":
        detail.append(tb.SEPARATING_LINE)
        detail.append(
            ["", "", "", " LCU ",
             f"{devs[-1]['smf74lcu']:4}",
             f"{convert_si(device_activity_rate_dict[devs[-1]['smf74lcu']], 6, 3):>7}",
             f"{convert_si(avg_resp_time, 5, 3):>5}",
             f"{convert_si(avg_iosq_time, 5, 3):>5}",
             f"{convert_si(avg_cmr_dly, 5, 3):>5}",
             f"{convert_si(avg_db_dly, 5, 3):>5}",
             f"{convert_si(avg_int_dly, 5, 3):>5}",
             f"{convert_si(avg_pend_time, 5, 3):>6}",
             f"{convert_si(avg_disc_time, 5, 3):>5}",
             f"{convert_si(avg_conn_time, 5, 3):>5}",
             f"{dev_conn_percent_dict[devs[-1]['smf74lcu']] / dev_count_dict[devs[-1]['smf74lcu']] if dev_count_dict[devs[-1]['smf74lcu']] > 0 else '----':{'>6.2f' if dev_count_dict[devs[-1]['smf74lcu']] > 0 else '>6'}}",
             f"{dev_util_percent_dict[devs[-1]['smf74lcu']] / dev_count_dict[devs[-1]['smf74lcu']] if dev_count_dict[devs[-1]['smf74lcu']] > 0 else '----':{'>6.2f' if dev_count_dict[devs[-1]['smf74lcu']] > 0 else '>6'}}",
             f"{dev_resv_percent_dict[devs[-1]['smf74lcu']] / dev_count_dict[devs[-1]['smf74lcu']] if dev_count_dict[devs[-1]['smf74lcu']] > 0 else '----':{'>5.2f' if dev_count_dict[devs[-1]['smf74lcu']] > 0 else '>5'}}",
             f"{any_alloc_percent_dict[devs[-1]['smf74lcu']] / dev_count_dict[devs[-1]['smf74lcu']] if dev_count_dict[devs[-1]['smf74lcu']] > 0 else '----':{'>6.2f' if dev_count_dict[devs[-1]['smf74lcu']] > 0 else '>6'}}",
             f"{not_ready_percent_dict[devs[-1]['smf74lcu']] / dev_count_dict[devs[-1]['smf74lcu']] if dev_count_dict[devs[-1]['smf74lcu']] > 0 else '----':{'>6.2f' if dev_count_dict[devs[-1]['smf74lcu']] > 0 else '>6'}}"
             ])
        detail.append(tb.SEPARATING_LINE)
        return (tb.tabulate(detail, tablefmt="plain", numalign="right",
                            floatfmt=(
                                "", "", "", "", ".3f", ".3f", ".3f", ".3f", ".3f", ".3f", ".3f", ".3f", ".3f", ".2f",
                                ".2f",
                                ".2f", ".2f", ".2f", ".2f", ".2f"),
                            headers=[" \nDev\nNum", " \nDevice\nType", " \nVolume\nSerieal", " \nLCU",
                                     "Device\nActivity\nRate", "Avg\nResp\nTime", "Avg\nIOSQ\nTime",
                                     "Avg\nCMR\nDly", "Avg\nDb\nDly",
                                     "Avg\nInt\nDly", "Avg\nPend\nTime", "Avg\nDisc\nTime", "Avg\nConn\nTime",
                                     "%\nDev\nConn",
                                     "%\nDev\nUtil", "%\nDev\nResv", "Avg\nNmbr\nAlloc", "%\nAny\nAlloc",
                                     "%\nMT\nPend", "%\nNot\nRdy"]),
                None)
    elif sub == "0080":
        avg_mt_time = pd.to_datetime(0) + pd.to_timedelta(avg_mt_time, unit='s')
        time_dev_alloc_sec = time_dev_alloc_dict[devs[-1]['smf74lcu']] / dev_count_dict[devs[-1]['smf74lcu']] if dev_count_dict[devs[
            -1]['smf74lcu']] > 0 else 0
        time_dev_alloc = pd.to_datetime(0) + pd.to_timedelta(time_dev_alloc_sec, unit='s')
        detail.append(tb.SEPARATING_LINE)
        detail.append(
            ["", "", "", "LCU",
             f"{devs[-1]['smf74lcu']:4}",
             f"{convert_si(device_activity_rate_dict[devs[-1]['smf74lcu']], 6, 3):>7}",
             f"{convert_si(avg_resp_time, 5, 3):>5}",
             f"{convert_si(avg_iosq_time, 5, 3):>5}",
             f"{convert_si(avg_cmr_dly, 5, 3):>5}",
             f"{convert_si(avg_db_dly, 5, 3):>5}",
             f"{convert_si(avg_int_dly, 5, 3):>5}",
             f"{convert_si(avg_pend_time, 5, 3):>6}",
             f"{convert_si(avg_disc_time, 5, 3):>5}",
             f"{convert_si(avg_conn_time, 5, 3):>5}",
             f"{dev_conn_percent_dict[devs[-1]['smf74lcu']] / dev_count_dict[devs[-1]['smf74lcu']] if dev_count_dict[devs[-1]['smf74lcu']] > 0 else '----':{'>6.2f' if dev_count_dict[devs[-1]['smf74lcu']] > 0 else '>6'}}",
             f"{dev_util_percent_dict[devs[-1]['smf74lcu']] / dev_count_dict[devs[-1]['smf74lcu']] if dev_count_dict[devs[-1]['smf74lcu']] > 0 else '----':{'>6.2f' if dev_count_dict[devs[-1]['smf74lcu']] > 0 else '>6'}}",
             f"{dev_resv_percent_dict[devs[-1]['smf74lcu']] / dev_count_dict[devs[-1]['smf74lcu']] if dev_count_dict[devs[-1]['smf74lcu']] > 0 else '----':{'>5.2f' if dev_count_dict[devs[-1]['smf74lcu']] > 0 else '>5'}}",
             f"{num_of_mts_dict[devs[-1]['smf74lcu']]:>6.0f}",
             f"{avg_mt_time:%H:%M:%S}",
             f"{time_dev_alloc:%H:%M:%S}"
             ])
        detail.append(tb.SEPARATING_LINE)
        return (tb.tabulate(detail, tablefmt="plain", numalign="right",
                            floatfmt=(
                                "", "", "", "", ".3f", ".3f", ".3f", ".3f", ".3f", ".3f", ".3f", ".3f", ".3f", ".2f",
                                ".2f",
                                ".2f", ".2f", ".2f", ".0f", ".2f", ".2f"),
                            headers=[" \nDev\nNum", " \nDevice\nType", " \nVolume\nSerieal", " \nLCU",
                                     "Device\nActivity\nRate", "Avg\nResp\nTime", "Avg\nIOSQ\nTime",
                                     "Avg\nCMR\nDly", "Avg\nDb\nDly",
                                     "Avg\nInt\nDly", "Avg\nPend\nTime", "Avg\nDisc\nTime", "Avg\nConn\nTime",
                                     "%\nDev\nConn",
                                     "%\nDev\nUtil", "%\nDev\nResv", "Number\nof\nMounts", "Avg\nMount\nTime",
                                     "Time\nDevice\nAlloc"]), None)
    return None, None


def format_device_activity_report(duration, dctl, devs, pro, device_list):
    # device_list = [list(g) for k, g in groupby(devs, attrgetter('lcu'))]
    if len(device_list) == 0:
        return None

    report = format_device_header(duration, dctl, pro)
    report_2 = None
    for dlist in device_list:
        (report_detail, sync_detail) = format_device_detail(dlist, pro['smf74int'], pro['smf74sam'], dctl['smf74sub'])
        if report_detail is not None:
            report += '\n'
            report += report_detail
        if dctl['smf74sub'] == '0020' and sync_detail is not None:
            if report_2 is None:
                report_2 = format_device_header(duration, dctl, pro, True)
            report_2 += '\n'
            report_2 += sync_detail
    if report_2 is None:
        return report
    else:
        report += '\n'
        report += report_2
        return report

def format_ess_header(duration, cntl, pros, report_type):
    if duration == 'Hourly':
        report_date = cntl['date']
        report_time = cntl['datetime'].time().strftime('%H.%M.%S')
        interval = format_s2min(pros[0]['smf74int'])
    elif duration == 'Daily':
        report_date = cntl['date']
        report_time = '00.00.00'
        interval = format_s2hr(pros[0]['smf74int'])
    else:
        report_date = cntl['smf74ist'].date()
        report_time = cntl['smf74ist'].time().strftime('%H.%M.%S')
        interval = format_s2min(pros[0]['smf74int'])
    zos_ver = 'V' + pros[-1]['smf74mvs'][2:4].lstrip('0') + 'R' + pros[-1]['smf74mvs'][4:6].lstrip('0')
    interval_x = f"{interval[:-3]}"
    whitespace = ' '
    header1a = [["                                                  E S S  L I N K  S T A T I S T I C S"]]
    header1b = [["                                 E S S  S Y N C H R O N O U S  I / O  L I N K  S T A T I S T I C S"]]
    header1c = [["                                       E S S   E X T E N T  P O O L  S T A T I S T I C S"]]
    header1d = [["                                                  E S S  R A N K  S T A T I S T I C S"]]
    header2 = [
        [f"{whitespace:>12}", f"z/OS {zos_ver}", f"{whitespace:>13}", f"System ID {pros[-1]['smf74sid']}", f"{whitespace:>6}",
         f"Date {report_date:%m/%d/%Y}", f"{whitespace:>11}", f"Interval {interval_x}"],
        ["", "", "", f"RMF Version {pros[-1]['smf74mfv']:<5}", "", f"Time {report_time}", "", f"Cycle {pros[-1]['smf74cyc'] / 1000:5.3f} Seconds"]
    ]
    header3 = [
        ["Serial Number",f"{cntl['r748cser']:<10}"," ","Type-Model",f"{cntl['r748ctyp']:6}-{cntl['r748cmdl']:3}"," ",
         "CDate",f"{report_date:%m/%d/%Y}"," ","CTime",f"{report_time}"," ","CInt",f"{interval_x[:-4]}"],
        tb.SEPARATING_LINE
    ]
    header4b = [
        ["                                 -------Cache Read Operations--------  ------Cache Write Operations-----  -------NVS Write Operations------"],
    ]
    header4c = [["--Extent Pool--   -------------- Real --------------     ------------ Virtual -------------"]]
    header4d = [["                                    -------- Read Operations --------  -------- Write Operations -------"]]
    if report_type == 'Link':
        return (tb.tabulate(header1a, tablefmt="plain") + "\n" + tb.tabulate(header2, tablefmt="plain") + "\n" +
                tb.tabulate(header3, tablefmt="plain") + "\n") # + tb.tabulate(header4a, tablefmt="plain") + "\n")
    elif report_type == 'SyncIO':
        return (tb.tabulate(header1b, tablefmt="plain") + "\n" + tb.tabulate(header2, tablefmt="plain") + "\n" +
                tb.tabulate(header3, tablefmt="plain") + "\n" + tb.tabulate(header4b, tablefmt="plain") + "\n")
    elif report_type == 'ExtentPool':
        return (tb.tabulate(header1c, tablefmt="plain") + "\n" + tb.tabulate(header2, tablefmt="plain") + "\n" +
                tb.tabulate(header3, tablefmt="plain") + "\n" + tb.tabulate(header4c, tablefmt="plain") + "\n")
    elif report_type == 'RankStat':
        return (tb.tabulate(header1d, tablefmt="plain") + "\n" + tb.tabulate(header2, tablefmt="plain") + "\n" +
                tb.tabulate(header3, tablefmt="plain") + "\n" + tb.tabulate(header4d, tablefmt="plain") + "\n")
    else:
        header = None
    return header

def format_link_statistics(duration, cntl, lsss, pros):
    link_type = {1:'ESCON', 2:'Fibre 1Gb', 3:'Fibre 2Gb', 4:'Fibre 4Gb',
                 5:'Fibre 8Gb', 6:'Fibre 16Gb', 7:'Fibre 32Gb', 10:'Ethernet 10Gb', 11:'Ethernet 40Gb'}
    if len(lsss) == 0:
        return None
    report = format_ess_header(duration, cntl, pros, 'Link')
    report_detail = []
    for lss in lsss:
        if lss['r748lerb'] > 0 or lss['r748lewb'] > 0:
            line_detail = [
                f"{lss['r748laid']:<4}",f"{link_type.get(lss['r748ltyp'], 'Undefined'):<15}","ECKD READ",
                f"{convert_si(lss['r748lerb'] * 128 * 1024 / cntl['r748cint'], 5, 1):>7}",
                f"{convert_si(lss['r748lerb'] * 128 * 1024 / lss['r748lero'], 5, 1) if lss['r748lero'] > 0 else '0.0':>7}",
                f"{convert_si(lss['r748lero'] / cntl['r748cint'], 5, 1):>7}",
                f"{convert_si(lss['r748lert'] * 1000 / lss['r748lero'], 6, 3) if lss['r748lero'] > 0 else '0.000':>7}",
                f"{convert_si(lss['r748lert'] * 1000 / cntl['r748cint'], 5, 1):>7}"]
            report_detail.append(line_detail)
            line_detail = [
                "","","ECKD WRITE",
                f"{convert_si(lss['r748lewb'] * 128 * 1024 / cntl['r748cint'], 5, 1):>7}",
                f"{convert_si(lss['r748lewb'] * 128 * 1024 / lss['r748lewo'], 5, 1) if lss['r748lewo'] > 0 else '0.0':>7}",
                f"{convert_si(lss['r748lewo'] / cntl['r748cint'], 5, 1):>7}",
                f"{convert_si(lss['r748lewt'] * 1000 / lss['r748lewo'], 6, 3) if lss['r748lewo'] > 0 else '0.000':>7}",
                f"{convert_si(lss['r748lewt'] * 1000 / cntl['r748cint'], 5, 1):>7}"]
            report_detail.append(line_detail)
            report_detail.append(tb.SEPARATING_LINE)
            line_detail = [
                "","","","","","","",f"{convert_si((lss['r748lert'] + lss['r748lewt']) * 1000 / cntl['r748cint'], 5, 1):>7}"
            ]
            report_detail.append(line_detail)
        elif lss['r748lpsb'] > 0 or lss['r748lprb'] > 0:
            line_detail = [
                f"{lss['r748laid']:<4}",f"{link_type.get(lss['r748ltyp'], 'Undefined'):<15}","PPRC SEND",
                f"{convert_si(lss['r748lpsb'] * 128 * 1024 / cntl['r748cint'], 5, 1):>7}",
                f"{convert_si(lss['r748lpsb'] * 128 * 1024 / lss['r748lpso'], 5, 1) if lss['r748lpso'] > 0 else '0.0':>7}",
                f"{convert_si(lss['r748lpso'] / cntl['r748cint'], 5, 1):>7}",
                f"{convert_si(lss['r748lpst'] * 1000 / lss['r748lpso'], 6, 3) if lss['r748lpso'] > 0 else '0.000':>7}",
                f"{convert_si(lss['r748lpst'] * 1000 / cntl['r748cint'], 5, 1):>7}"]
            report_detail.append(line_detail)
            line_detail = [
                "","","PPRC RECEIVE",
                f"{convert_si(lss['r748lprb'] * 128 * 1024 / cntl['r748cint'], 5, 1):>7}",
                f"{convert_si(lss['r748lprb'] * 128 * 1024 / lss['r748lpro'], 5, 1) if lss['r748lpro'] > 0 else '0.0':>7}",
                f"{convert_si(lss['r748lpro'] / cntl['r748cint'], 5, 1):>7}",
                f"{convert_si(lss['r748lprt'] * 1000 / lss['r748lpro'], 6, 3) if lss['r748lpro'] > 0 else '0.000':>7}",
                f"{convert_si(lss['r748lprt'] * 1000 / cntl['r748cint'], 5, 1):>7}"]
            report_detail.append(line_detail)
            report_detail.append(tb.SEPARATING_LINE)
            line_detail = [
                "", "", "", "", "", "","",f"{convert_si((lss['r748lprt']+lss['r748lpst'])*1000/cntl['r748cint'],5,1):>7}"
            ]
            report_detail.append(line_detail)
            line_detail = [" ", " ", " ", " ", " ", ""] # blank line
            report_detail.append(line_detail)
        elif lss['r748lsrb'] > 0 or lss['r748lswb'] > 0:
            line_detail = [
                f"{lss['r748laid']:<4}",f"{link_type.get(lss['r748ltyp'], 'Undefined'):<15}","SCSI READ",
                f"{convert_si(lss['r748lsrb'] * 128 * 1024 / cntl['r748cint'], 5, 1):>7}",
                f"{convert_si(lss['r748lsrb'] * 128 * 1024 / lss['r748lsro'], 5, 1) if lss['r748lsro'] > 0 else '0.0':>7}",
                f"{convert_si(lss['r748lsro'] / cntl['r748cint'], 5, 1):>7}",
                f"{convert_si(lss['r748lsrt'] * 1000 / lss['r748lsro'], 6, 3) if lss['r748lsro'] > 0 else '0.000':>7}",
                f"{convert_si(lss['r748lsrt'] * 1000 / cntl['r748cint'], 5, 1):>7}"]
            report_detail.append(line_detail)
            line_detail = [
                "", "", "SCSI WRITE",
                f"{convert_si(lss['r748lswb']*128*1024/cntl['r748cint'],5,1):>7}",
                f"{convert_si(lss['r748lswb']*128*1024/lss['r748lswo'],5,1) if lss['r748lswo'] > 0 else '0.0':>7}",
                f"{convert_si(lss['r748lswo']/cntl['r748cint'],5,1):>7}",
                f"{convert_si(lss['r748lswt']*1000/lss['r748lswo'],6,3) if lss['r748lswo'] > 0 else '0.000':>7}",
                f"{convert_si(lss['r748lswt']*1000/cntl['r748cint'],5,1):>7}"]
            report_detail.append(line_detail)
            report_detail.append(tb.SEPARATING_LINE)
            line_detail = [
                "", "", "", "", "", "", "", f"{convert_si((lss['r748lsrt']+lss['r748lswt'])*1000/cntl['r748cint'],5,1):>7}"
            ]
            report_detail.append(line_detail)
            line_detail = [" ", " ", " ", " ", " ", ""] # blank line
            report_detail.append(line_detail)
        else:
            line_detail = [f"{lss['r748laid']:<4}",f"{link_type.get(lss['r748ltyp'], 'Undefined'):<15}","NO DATA TO REPORT OR ZERO"]
            report_detail.append(line_detail)
            line_detail = [" "," "," "," "," ",""] # blank line
            report_detail.append(line_detail)

    if len(report_detail) > 0:
        return report + tb.tabulate(report_detail,
                                 headers=["------\nSAID","Adapter------\nType","--Link Type--\n","Bytes\n/Sec",
                                          "Bytes\n/Operation","Operations\n/Sec","Resp Time\n/Operation","I/O\nIntensity"],
                                 colalign=('left','left','left','right','right','right','right','right'),
                                 floatfmt=('','','','.1f','.1f','.1f','.03f','.1f')
                                 )
    return report

def format_sync_io_statistics(duration, cntl, siols, pros):
    link_speed = {'01':'GEN1', '02':'GEN2', '03':'GEN3', '04':'GEN4'}
    if len(siols) == 0:
        return None
    report = format_ess_header(duration, cntl, pros, 'SyncIO')
    report_detail = []
    for siol in siols:
        if siol['r748scbr'] > 0 or siol['r748scbw'] > 0 or siol['r748snbw'] > 0:
            line_detail = \
                [f"{siol['r748siid']:4}",
                 f"{'Optical PCIe' if siol['r748styp']=='01' else 'Unknown':<12}  {link_speed.get(siol['r748sspd'], 'UNKN'):<4} {siol['r748swdh']:>2}",
                 f"{convert_si(siol['r748scro']/cntl['r748cint'],5,1):>7}",
                 f"{convert_bi(siol['r748scbr']*128*1024/siol['r748scro'],4,1) if siol['r748scro'] > 0 else 'N/A':>6}",
                 f"{convert_si(siol['r748scrt']*1000/siol['r748scro'],5,1) if siol['r748scro'] > 0 else 'N/A':>7}",
                 f"{siol['r748scrs']*100/siol['r748scro'] if siol['r748scro'] > 0 else 'N/A':{'>5.1f' if siol['r748scro'] > 0 else '>5'}}",
                 f"{convert_si(siol['r748scwo']/cntl['r748cint'],5,1):>7}",
                 f"{convert_bi(siol['r748scbw']*128*1024/siol['r748scwo'],4,1) if siol['r748scwo'] > 0 else 'N/A':>6}",
                 f"{convert_si(siol['r748scwt']*1000/siol['r748scwo'],5,1) if siol['r748scwo'] > 0 else 'N/A':>7}",
                 f"{siol['r748scws']*100/siol['r748scwo'] if siol['r748scwo'] > 0 else 'N/A':{'>5.1f' if siol['r748scwo'] > 0 else '>5'}}",
                 f"{convert_si(siol['r748snwo']/cntl['r748cint'],5,1):>7}",
                 f"{convert_bi(siol['r748snbw']*128*1024/siol['r748snwo'],4,1) if siol['r748snwo'] > 0 else 'N/A':>6}",
                 f"{convert_si(siol['r748snwt']*1000/siol['r748snwo'],5,1) if siol['r748snwo'] > 0 else 'N/A':>7}",
                 f"{siol['r748snws']*100/siol['r748snwo'] if siol['r748snwo'] > 0 else 'N/A':{'>5.1f' if siol['r748snwo'] > 0 else '>5'}}"]
            report_detail.append(line_detail)
        else:
            line_detail = [f"{siol['r748siid']:4}",
                           f"{'Optical PCIe' if siol['r748styp']=='01' else 'Unknown':<12}  {link_speed.get(siol['r748sspd'], 'UNKN'):<4} {siol['r748swdh']:>2}",
                           "NO DATA","TO REPORT","OR ZERO"]
            report_detail.append(line_detail)
    return report + tb.tabulate(report_detail,
                                headers=["\nSIID","\n------Link Type------","OPS\n/Sec","Bytes\n/OP","RTime\n/OP","%Succ\n",
                                         "OPS\n/Sec","Bytes\n/OP","RTime\n/OP","%Succ\n","OPS\n/Sec","Bytes\n/OP",
                                         "RTime\n/OP","%Succ\n"],
                                colalign=('left','left','right','right','right','right','right','right','right','right',
                                          'right','right','right','right'),
                                floatfmt=('','','.1f','.1f','.1f','.1f','.1f','.1f','.1f','.1f','.1f','.1f','.1f','.1f'))

def format_extent_pool_statistics(duration, cntl, extps, pros):
    extent_type = {4:'FIBRE 1Gb', 132:'CKD 1Gb'}
    if len(extps) == 0:
        return None
    report = format_ess_header(duration, cntl, pros, 'ExtentPool')
    report_detail = []
    for extp in extps:
        detail_line = [
            f"{extp['r748xpid']}",f"{extent_type.get(extp['r748xplt'], 'Unknown'):<9}",
            f"{extp['r748xrcp']:>8}",f"{extp['r748xrns']:>8}",f"{extp['r748xrsc']:>8}",
            f"{extp['r748xvcp']:>8}",f"{extp['r748xvns']:>8}",f"{extp['r748xvsc']:>8}"]
        report_detail.append(detail_line)
    return report + tb.tabulate(report_detail,
                                headers=["ID","Type","Capacity","Extents","Conversions","Capacity","Extents","Conversions"],
                                colalign=('left','left','right','right','right','right','right','right'),
                                floatfmt=())


def format_rank_statistics(duration, cntl, extps, ranks_list, ranks_arrys_list, pros):
    extent_type = {4:'FIBRE 1Gb', 132:'CKD 1Gb'}
    array_type = {1: 'RAID 5', 2: 'RAID 10', 3: 'RAID 6'}
    if len(extps) == 0:
        return None
    report = format_ess_header(duration, cntl, pros, 'RankStat')
    report_detail = []
    for idx_1, extp in enumerate(extps):
        if len(ranks_list[idx_1]) == 0:
            continue
        prev_extpid = None
        for idx_2, rank in enumerate(ranks_list[idx_1]):
            detail_line = [
                f"{rank['r748rpnm'] if rank['r748rpnm'] != prev_extpid else ' ':<4} {extent_type.get(extp['r748xplt'], 'Unknown') if rank['r748rpnm'] != prev_extpid else ' ':<10}",
                f"{rank['r748rrid']:<4}",f"{rank['r748rai']:<4}",f"{convert_si(rank['r748rrop'] / cntl['r748cint'], 5, 1):>7}",
                f"{convert_si(rank['r748rbyr'] * 128 * 1024 / rank['r748rrop'], 4, 1) if rank['r748rrop'] > 0 else '0.0':>6}",
                f"{convert_si(rank['r748rbyr'] * 128 * 1024 / cntl['r748cint'], 4, 1):>6}",
                f"{convert_si(rank['r748rkrt'] * 1000 / rank['r748rrop'], 5, 1) if rank['r748rrop'] > 0 else '0.0':>7}",
                f"{convert_si(rank['r748rwop'] / cntl['r748cint'], 6, 3):>7}",
                f"{convert_si(rank['r748rbyw'] * 128 * 1024 / rank['r748rwop'], 4, 1) if rank['r748rwop'] > 0 else '0.0':>6}",
                f"{convert_si(rank['r748rbyw'] * 128 * 1024 / cntl['r748cint'], 4, 1):>6}",
                f"{convert_si(rank['r748rkwt'] * 1000 / rank['r748rwop'], 6, 3) if rank['r748rwop'] > 0 else '0.000':>7}",
                f"{'Y' if ranks_arrys_list[idx_1][idx_2][-1]['r748adc'] == '11' else ' ':1}",f"{rank['r748rcnt']:>3}",f"{ranks_arrys_list[idx_1][idx_2][-1]['r748aawd']:>3}",
                f"{'N/A' if ranks_arrys_list[idx_1][idx_2][-1]['r748adc'] == '11' else str(ranks_arrys_list[idx_1][idx_2][-1]['r748aasp']) + ' ' if len(str(ranks_arrys_list[idx_1][idx_2][-1]['r748aasp'])) < 3 else ranks_arrys_list[idx_1][idx_2][-1]['r748aasp']:>3}",
                f"{rank['rank_cap']:>6}G",f"{array_type.get(ranks_arrys_list[idx_1][idx_2][-1]['r748atyp'], 'Unknown'):<8}"
            ]
            report_detail.append(detail_line)
            if rank['r748rpnm'] != prev_extpid:
                prev_extpid = rank['r748rpnm']
        if len(ranks_list[idx_1]) > 1:
            report_detail.append(tb.SEPARATING_LINE)
            detail_line = [
                "","POOL","",f"{convert_si(extp['r748rrop'] / cntl['r748cint'], 5, 1):>7}",
                f"{convert_si(extp['r748rbyr'] * 128 * 1024 / extp['r748rrop'], 4, 1) if extp['r748rrop'] > 0 else '0.0':>6}",
                f"{convert_si(extp['r748rbyr'] * 128 * 1024 / cntl['r748cint'], 4, 1):>6}",
                f"{convert_si(extp['r748rkrt'] * 1000 / extp['r748rrop'], 5, 1) if extp['r748rrop'] > 0 else '0.0':>7}",
                f"{convert_si(extp['r748rwop'] / cntl['r748cint'], 6, 3):>7}",
                f"{convert_si(extp['r748rbyw'] * 128 * 1024 / extp['r748rwop'], 4, 1) if extp['r748rwop'] > 0 else '0.0':>6}",
                f"{convert_si(extp['r748rbyw'] * 128 * 1024 / cntl['r748cint'], 4, 1):>6}",
                f"{convert_si(extp['r748rkwt'] * 1000 / extp['r748rwop'], 5, 3) if extp['r748rwop'] > 0 else '0.000':>7}",
                f"{'Y' if extp['r748adc'] == '11' else ' ':1}",f"{extp['r748rcnt']:>3}",f"{extp['r748aawd']:>4}",
                f"{'0 ' if extp['r748adc'] == '11' else str(extp['r748aasp']) + ' ' if len(str(extp['r748aasp'])) < 3 else extp['r748aasp']:>3}",
                f"{extp['rank_cap']:>6}G",f"{extp['r748aebc']:<8}"
            ]
            report_detail.append(detail_line)
            report_detail.append([" "," "])
    return report + tb.tabulate(report_detail,
                                headers=["--Extent Pool--\n ID  Type","\nRRID","Adapt\nID","OPS\n/Sec","Bytes\n/OP","Bytes\n/Sec",
                                         "RTime\n/OP","OPS\n/Sec","Bytes\n/OP","Bytes\n/Sec","RTime\n/OP","-----\nSSD","Array\nNum",
                                         "----\nWidth","Min\nRpm","Rank\nCap","Raid\nType"],
                                colalign=('left','left','right','right','right','right','right','right','right','right',
                                          'right','right','right','right','right','right'),
                                floatfmt=('','','','.1f','.1f','.1f','.1f','.03f','.1f','.1f','.03f',))


def format_fcd_header(duration, fcd, pros):
    if duration == 'Hourly':
        report_date = fcd['date']
        report_time = fcd['datetime'].time().strftime('%H.%M.%S')
        interval = format_s2min(pros[-1]['smf74int'])
    elif duration == 'Daily':
        report_date = fcd['date']
        report_time = '00.00.00'
        interval = format_s2hr(pros[-1]['smf74int'])
    else:
        report_date = fcd['smf74ist'].date()
        report_time = fcd['smf74ist'].time().strftime('%H.%M.%S')
        interval = format_s2min(pros[-1]['smf74int'])
    zos_ver = 'V' + pros[-1]['smf74mvs'][2:4].lstrip('0') + 'R' + pros[-1]['smf74mvs'][4:6].lstrip('0')
    interval_x = f"{interval[:-3]}"
    whitespace = ' '
    header1 = [["                                            F I C O N  D I R E C T O R  A C T I V I T Y"]]
    header2 = [
        [f"{whitespace:>12}", f"z/OS {zos_ver}", f"{whitespace:>13}", f"System ID {pros[-1]['smf74sid']}", f"{whitespace:>6}",
         f"Date {report_date:%m/%d/%Y}", f"{whitespace:>11}", f"Interval {interval_x}"],
        ["", "", "", f"RMF Version {pros[-1]['smf74mfv']:<5}", "", f"Time {report_time}", "",
         f"Cycle {pros[-1]['smf74cyc'] / 1000:5.3f} Seconds"]
    ]

    return tb.tabulate(header1, tablefmt="plain") + "\n" + tb.tabulate(header2, tablefmt="plain") + "\n"


def format_switch_activity(duration, switch, ports, fcd, pros, connectors_list):
    if len(ports) == 0:
        return None
    interval = pros[-1]['smf74int']
    header3 = [
        tb.SEPARATING_LINE,
        ["IODF =", f"{fcd['r747gisf']:2}", "  ",
         "Cr-Date:", f"{fcd['r747gict'].date():%m/%d/%Y}", "  ",
         "Cr-Time:", f"{fcd['r747gict'].time().strftime('%H.%M.%S'):8}", "  ",
         "Act:", f"{'Activate' if fcd['r747giac'] else 'POR':<8}"]
    ]
    header4 = [
        tb.SEPARATING_LINE,
        ["Switch Device:", f"{switch['r747sdev']:4}", "", "Switch ID:",
         f"{'**' if switch['r747sfcs'] else switch['r747slsn']:2}", "",
         "Type:", f"{switch['ndetype']:6}", "", "Model:", f"{switch['ndemodel']:3}", "",
         "Man:", f"{switch['ndemfg']:3}", "", "Plant:", f"{switch['ndeplant']:2}", "", "Serial:", f"{switch['ndesequence']:12}"],
        tb.SEPARATING_LINE
    ]
    report = (format_fcd_header(duration, fcd, pros) + tb.tabulate(header3, tablefmt='plain')
              + '\n' + tb.tabulate(header4, tablefmt='plain') + '\n')
    prev_port = None
    report_detail = []
    for idx_1, port in enumerate(ports):
        if port['r747padr'] != prev_port:
            port_adr = port['r747padr']
            prev_port = port['r747padr']
        else:
            port_adr = " "
        if not port['r747poff'] and not port['r747plf'] and not port['r747pnti'] and \
                (len(connectors_list[idx_1]) > 0 and not connectors_list[idx_1][0]['r747crem']):
            detail_line = [f"{port_adr:<2}"]
            if len(connectors_list[idx_1]) > 0:
                detail_line += [
                    f"{'CU' if connectors_list[idx_1][0]['r747cscu'] or connectors_list[idx_1][0]['r747cmcu'] else 'CHP-H' if connectors_list[idx_1][0]['r747cchp'] and connectors_list[idx_1][0]['r747cosy'] else 'SWITCH' if connectors_list[idx_1][0]['r747csw'] else 'CHP' if connectors_list[idx_1][0]['r747cchp'] else ' ':<6} "
                    f"{'----' if connectors_list[idx_1][0]['r747ctnu'] or connectors_list[idx_1][0]['r747csw'] else connectors_list[idx_1][0]['r747ccu'].lstrip('0') if connectors_list[idx_1][0]['r747cchp'] else ' ' if connectors_list[idx_1][0]['r747ccu'] == '0000' else connectors_list[idx_1][0]['r747ccu']:>4}   {port['ndesequence']:12}",
                ]
            else:
                detail_line += ["", "----"]
            detail_line += [
                f"{port['r747pfpt'] * 1e6 / port['r747pnft'] if port['r747pnft'] > 0 else 0:{'>10.1f' if port['r747pfpt'] > 0 else '>10.0f'}}",
                f"{convert_si(port['r747pnwr'] * 4 / port['r747pnfr'], 6, 0) if port['r747pnfr'] > 0 else 0:>7}",
                f"{convert_si(port['r747pnwt'] * 4 / port['r747pnft'], 6, 0) if port['r747pnft'] > 0 else 0:>7}",
                f"{port['r747pnwr'] / (250 * 1000) / interval:>11.2f}",
                f"{port['r747pnwt'] / (250 * 1000) / interval:>11.2f}",
                f"{port['r747pner']:>7.0f}\n"
            ]
            report_detail.append(detail_line)
        elif port['r747poff']:
            detail_line = [f"{port_adr:<2}", "----  ----         P O R T", "O F F L I N E"]
            report_detail.append(detail_line)
        elif port['r747plf']:
            detail_line = [f"{port_adr:<2}", "----  ----         L I N K", "F A I L U R E"]
            report_detail.append(detail_line)
        elif port['r747pnti']:
            detail_line = [f"{port_adr:<2}", "----  ----         P O R T", "N O T", "I N S T A L L E D"]
            report_detail.append(detail_line)
        # elif len(connectors_list[idx_1]) > 0 and connectors_list[idx_1][0]['r747cnmd:
        #    detail_line = [
        #        f"{port_adr:<2}",
        #        f"{'CU' if connectors_list[idx_1][0]['r747cscu'] or connectors_list[idx_1][0]['r747cmcu'] else 'CHP-H' if connectors_list[idx_1][0]['r747cchp'] and connectors_list[idx_1][0]['r747cosy'] else 'SWITCH' if connectors_list[idx_1][0]['r747csw'] else 'CHP' if connectors_list[idx_1][0]['r747cchp'] else ' ':<6}"
        #        f"  {'----' if connectors_list[idx_1][0]['r747ctnu'] else connectors_list[idx_1][0]['r747ccu'].lstrip('0') if connectors_list[idx_1][0]['r747cchp'] else ' ' if connectors_list[idx_1][0]['r747ccu'] == '0000' else connectors_list[idx_1][0]['r747ccu']:>4}   {port['ndesequence']:12}",
        #        " N O  D A T A"
        #    ]
        #    report_detail.append(detail_line)
        elif len(connectors_list[idx_1]) > 0 and connectors_list[idx_1][0]['r747crem']:
            detail_line = [f"{port_adr:<2}", "----  ----         P O R T", "R E M O V E D"]
            report_detail.append(detail_line)
        if len(connectors_list[idx_1]) > 1:
            for i in range(1, len(connectors_list[idx_1])):
                report_detail.append(["",
                                      f"{'CU' if connectors_list[idx_1][i]['r747cscu'] or connectors_list[idx_1][i]['r747cmcu'] else 'CHP-H' if connectors_list[idx_1][i]['r747cchp'] and connectors_list[idx_1][i]['r747cosy'] else 'SWITCH' if connectors_list[idx_1][i]['r747csw'] else 'CHP' if connectors_list[idx_1][i]['r747cchp'] else ' ':<6} {connectors_list[idx_1][i]['r747ccu']}"])
    return report + tb.tabulate(report_detail,
                                headers=["Port\nAddr", "---------Connection--------\nUnit      ID  Serial Number",
                                         "Avg Frame\nPacing", "Avg Frame\nRead", "Size\nWrite",
                                         "Port Bandwidth\n-- Read --", "(MB/Sec)\n-- Write --", "Error\nCount"],
                                colalign=('center', 'left', 'right', 'right', 'right', 'right', 'right', 'right'),
                                floatfmt=('', '', '.0f', '.0f', '.0f', '.2f', '.2f', '.0f'))

def format_hfs_header(duration, hfs, pro, report_type):
    title_dict = {1:'                                              H F S  G L O B A L  S T A T I S T I C S',
                  2:'                                        H F S   F I L E   S Y S T E M   S T A T I S T I C S'}
    if duration == 'Hourly':
        report_date = hfs['date']
        report_time = hfs['datetime'].time().strftime('%H.%M.%S')
        interval = format_s2min(pro['smf74int'])
    elif duration == 'Daily':
        report_date = hfs['date']
        report_time = '00.00.00'
        interval = format_s2hr(pro['smf74int'])
    else:
        report_date = hfs['smf74ist'].date()
        report_time = hfs['smf74ist'].time().strftime('%H.%M.%S')
        interval = format_s2min(pro['smf74int'])
    zos_ver = 'V' + pro['smf74mvs'][2:4].lstrip('0') + 'R' + pro['smf74mvs'][4:6].lstrip('0')
    interval_x = f"{interval[:-3]}"
    whitespace = ' '
    header1 = [[f"{title_dict[report_type]}"]]
    header2 = [
        [f"{whitespace:>12}", f"z/OS {zos_ver}", f"{whitespace:>13}", f"System ID {hfs['smf74sid']}", f"{whitespace:>6}",
         f"Date {report_date:%m/%d/%Y}", f"{whitespace:>11}", f"Interval {interval_x}"],
        ["", "", "", f"RMF Version {pro['smf74mfv']:<5}", "", f"Time {report_time}", "", f"Cycle {pro['smf74cyc'] / 1000:5.3f} Seconds"]
    ]
    return tb.tabulate(header1, tablefmt="plain") + "\n" + tb.tabulate(header2, tablefmt="plain") + "\n"

def format_hfs_global_statistics(duration, hfs, pro, gbufs):
    report = format_hfs_header(duration, hfs, pro, 1)
    message = ""
    if hfs['r746gonr']:
        message += 'OMVS kernel not ready.\n'
    if hfs['r746gnbl']:
        message += f"Buffer limit data is not available. BPX1PCT RC={hfs['r746glrc'][3:]:<4}, RS={hfs['r746glrs'][3:]:<4}.\n"
    if hfs['r746gngd']:
        message += f"Global HFS data is not available. BPX1PCT RC={hfs['r746gsrc'][3:]:<4}, RS={hfs['r746gsrs'][3:]:<4}.\n"
    if hfs['r746gpgd']:
        message += 'Global HFS data is partially available.\n'
    if message != "":
        hfs = None
    report_detail = []
    report_detail1 = []
    if pd.notna(hfs):
        report_detail1 = [
            ["","Virtual","Max",f"{hfs['r746gmxv'] if pd.notna(hfs) else ' ':{'>7.3f' if pd.notna(hfs) else '>7'}}"],
            ["","","Use",f"{hfs['r746gusv']*4096/(1024*1024) if pd.notna(hfs) else ' ':{'>7.3f' if pd.notna(hfs) else '>7'}}",
             " ","Cache",f"{hfs['r746g1c'] if pd.notna(hfs) else ' ':>7}",
             f"{hfs['r746g1c']/pro['smf74int'] if pd.notna(hfs) else ' ':{'>8.3f' if pd.notna(hfs) else '>8'}}",
             f"{hfs['r746gmc'] if pd.notna(hfs) else ' ':>7}",
             f"{hfs['r746gmc']/pro['smf74int'] if pd.notna(hfs) else ' ':{'>8.3f' if pd.notna(hfs) else '>8'}}"],
            ["","Fixed","Min",f"{hfs['r746gmnf'] if pd.notna(hfs) else ' ':{'>7.3f' if pd.notna(hfs) else '>7'}}",
             " ","DASD",f"{hfs['r746g1nc'] if pd.notna(hfs) else ' ':>7}",
             f"{hfs['r746g1nc']/pro['smf74int'] if pd.notna(hfs) else ' ':{'>8.3f' if pd.notna(hfs) else '>8'}}",
             f"{hfs['r746gmnc'] if pd.notna(hfs) else ' ':>7}",
             f"{hfs['r746gmnc']/pro['smf74int'] if pd.notna(hfs) else ' ':{'>8.3f' if pd.notna(hfs) else '>8'}}"],
            ["","","Use",f"{hfs['r746gusf']*4096/(1024*1024) if pd.notna(hfs) else ' ':{'>7.3f' if pd.notna(hfs) else '>7'}}",
             " ","Hit Ratio",f"{round_(hfs['r746g1c']*100/(hfs['r746g1c']+hfs['r746g1nc']),2) if pd.notna(hfs) and (hfs['r746g1c']+hfs['r746g1nc']) >0 else 0 if pd.notna(hfs) else ' ':{'>6.2f' if pd.notna(hfs) else '>6'}}",
             "",f"{round_(hfs['r746gmc']*100/(hfs['r746gmc']+hfs['r746gmnc']),2) if pd.notna(hfs) and (hfs['r746gmc']+hfs['r746gmnc']) >0 else 0 if pd.notna(hfs) else ' ':{'>6.2f' if pd.notna(hfs) else '>6'}}"],
            tb.SEPARATING_LINE
        ]

    if pd.notna(hfs):
        for gbuf in gbufs:
            detail_line = [
                f"{gbuf['pool_number']:1}",f"{gbuf['r746gsbp']:>8}",f"{gbuf['r746gsb']:>8}",f"{gbuf['r746gsbp']:>8}",
                f"{convert_bi(gbuf['r746gsbp'] * 4096, 8, 0):>9}",
                f"{gbuf['r746gsbf'] * 100 / gbuf['r746gsbp'] if gbuf['r746gsbp'] > 0 else 0:4.1f}",f"{gbuf['r746gnds']:>4}",
                f"{convert_si(gbuf['r746gbf'] + gbuf['r746gbnf'], 8, 0):>8}",
                f"{convert_si(gbuf['r746gbf'], 8, 0):>8}",
                f"{convert_si(gbuf['r746gbf'] * 100 / (gbuf['r746gbf'] + gbuf['r746gbnf']), 8, 0) if (gbuf['r746gbf'] + gbuf['r746gbnf']) > 0 else 0:>8}"
            ]
            report_detail.append(detail_line)
    else:
        report += message
    if len(report_detail) > 0:
        return (report +
                tb.tabulate(report_detail1,tablefmt='plain',
                            headers=["       ","--- Storage","Limits (MB)","------","  ","      ","---- File\nCount ",
                                     "I/O ----\nRate ","--- Metadata\nCount ","I/O ---\nRate "],
                            colalign=('','left','center','right','left','right','right','right','right'),
                            floatfmt=('','','','.3f','','','.2f','.3f','.2f','.3f')
                            ) +
                '\n----------------------------------------------- Buffer Pool Statistics -----------------------------------------------\n' +
                tb.tabulate(report_detail,
                            headers=["Pool\nNumber","Number\nBuffers","Buffer\nSize","--------\nPages   ","Pool Size\nBytes   ",
                                     "--------\n%Fixed","Data\nSpaces","----------\nTotal","I/O Activity\nFixed    ","---------\n%Fixed"],
                            colalign=('right','right','right','right','right','right','right','right','right'),
                            floatfmt=('.0f','.0f','.0f','.0f','.0f','.0f','.0f','.0f','.0f')
                            ))
    else:
        return report

def format_hfs_file_system_statistics(duration, hfs, pro, fsyss):
    if len(fsyss) == 0:
        return None
    report = format_hfs_header(duration, hfs, pro, 2)
    report += (
        "--- Allocation (MB) --      ----- File I/O ----- -- Metadata I/O --  -- Index I/O --   ---- Index Events ---\n"
        "                  Size           Count     Rate    Count      Rate   Count      Rate                   Count\n\n"
        )
    for fsys in fsyss:
        if fsys['r746fnhs']:
            report += (
                f"File System Name: {fsys['r746fsnm']:<44}\n\n"
                f"File system data is not available, EPX1PCT RC={fsys['r746fsrc'][3:]:<4}, RS={fsys['r746fsrs'][3:]:<4}\n\n"
                )
        elif fsys['r746fmtc']:
            report += (
                f"File System Name: {fsys['r746fsnm']:<44}\n\n"
                f"Mount time changed during interval\n\n"
                )
        elif fsys['r746ffsm']:
            report += (
                f"File System Name: {fsys['r746fsnm']:<44}\n\n"
                f"File system now mounted\n\n"
                )
        else:
            report += (
                f"File System Name: {fsys['r746fsnm']:<44}\n"
                f"Mount Date: {fsys['r746fmtm'].date():%m/%d/%Y}   TIME: {fsys['r746fmtm'].time().strftime('%H.%M.%S'):>8}\n")
            report_detail = [
                tb.SEPARATING_LINE,
                ["System",f"{round_(fsys['r746fsf'] * 4 / 1024, 3):{'>11.0f' if fsys['r746fsf'] * 4 / 1024 >= 10 else '>11.3f'}}",
                 "Cache",f"{fsys['r746f1c']:>11.0f}",f"{round_(fsys['r746f1c'] / pro['smf74int'], 3):{'>8.0f' if fsys['r746f1c'] / pro['smf74int'] >= 10 else '>8.3f'}}",
                 f"{fsys['r746fmc']:>11.0f}",f"{round_(fsys['r746fmc'] / pro['smf74int'], 3):{'>8.0f' if fsys['r746fmc'] / pro['smf74int'] >= 10 else '>8.3f'}}",
                 f"{fsys['r746firh'] + fsys['r746fiwh']:>11.0f}",
                 f"{round_((fsys['r746firh'] + fsys['r746fiwh']) / pro['smf74int'], 3):{'>8.0f' if (fsys['r746firh'] + fsys['r746fiwh']) / pro['smf74int'] >= 10 else '>8.3f'}}",
                 "New Level",f"{fsys['r746fint']:>11.0f}"],
                ["Data",f"{round_(fsys['r746fpf'] * 4 / 1024, 3):{'>11.0f' if fsys['r746fpf'] * 4 / 1024 >= 10 else '>11.3f'}}",
                 "DASD",f"{fsys['r746f1nc']:>11.0f}",f"{round_(fsys['r746f1nc'] / pro['smf74int'], 3):{'>8.0f' if fsys['r746f1nc'] / pro['smf74int'] >= 10 else '>8.3f'}}",
                 f"{fsys['r746fmnc']:>11.0f}",f"{round_(fsys['r746fmnc'] / pro['smf74int'], 3):{'>8.0f' if fsys['r746fmnc'] / pro['smf74int'] >= 10 else '>8.3f'}}",
                 f"{fsys['r746firm'] + fsys['r746fiwm']:>11.0f}",f"{round_((fsys['r746firm'] + fsys['r746fiwm']) / pro['smf74int'], 3):{'>8.0f' if (fsys['r746firm'] + fsys['r746fiwm']) / pro['smf74int'] >= 10 else '>8.3f'}}",
                 "Splits",f"{fsys['r746fis']:>11.0f}"],
                ["Attr. Dir",f"{round_(fsys['r746fpd'] * 4 / 1024, 3):{'>11.0f' if fsys['r746fpd'] * 4 / 1024 >= 10 else '>11.3f'}}",
                 "Hit Ratio",f"{round_(fsys['r746f1c'] * 100 / (fsys['r746f1c'] + fsys['r746f1nc']), 2) if (fsys['r746f1c'] + fsys['r746f1nc']) > 0 else 0:>6.2f}","",
                 f"{round_(fsys['r746fmc'] * 100 / (fsys['r746fmc'] + fsys['r746fmnc']), 2) if (fsys['r746fmc'] + fsys['r746fmnc']) > 0 else 0:>6.2f}","",
                 f"{round_((fsys['r746firh'] + fsys['r746fiwh']) * 100 / (fsys['r746firh'] + fsys['r746fiwh'] + fsys['r746firm'] + fsys['r746fiwm']), 2) if (fsys['r746firh'] + fsys['r746fiwh'] + fsys['r746firm'] + fsys['r746fiwm']) > 0 else 0:>6.2f}",
                 "","Joins",f"{fsys['r746fij']:>11.0f}"],
                ["","","Sequential",f"{fsys['r746fsfi']:>11.0f}",f"{round_(fsys['r746fsfi'] / pro['smf74int'], 3):{'>8.0f' if fsys['r746fsfi'] / pro['smf74int'] >= 10 else '>8.3f'}}"],
                ["Cached",f"{round_(fsys['r746fpc'] * 4 / 1024, 3):{'>11.0f' if fsys['r746fpc'] * 4 / 1024 >= 10 else '>11.3f'}}",
                 "Random",f"{fsys['r746frfi']:>11.0f}",f"{round_(fsys['r746frfi'] / pro['smf74int'], 3):{'>8.0f' if fsys['r746frfi'] / pro['smf74int'] >= 10 else '>8.3f'}}"]
            ]
            report += tb.tabulate(report_detail, tablefmt='plain',
                                  colalign=('left','right','left','right','right','right','right','right','right','left','right'),
                                  floatfmt=('','','','.0f','.3f','.2f','.3f','.2f','.3f','','.0f'))
            report += '\n\n'

    return report


def format_omvs_activity_report(duration, omvs, pro):
    if duration == 'Hourly':
        report_date = omvs['date']
        report_time = omvs['datetime'].time().strftime('%H.%M.%S')
        interval = format_s2min(pro['smf74int'])
    elif duration == 'Daily':
        report_date = omvs['date']
        report_time = '00.00.00'
        interval = format_s2hr(pro['smf74int'])
    else:
        report_date = omvs['smf74ist'].date()
        report_time = omvs['smf74ist'].time().strftime('%H.%M.%S')
        interval = format_s2min(pro['smf74int'])
    zos_ver = 'V' + pro['smf74mvs'][2:4].lstrip('0') + 'R' + pro['smf74mvs'][4:6].lstrip('0')
    interval_x = f"{interval[:-3]}"
    whitespace = ' '
    header1 = [["                                              O M V S   K E R N E L   A C T I V I T Y"]]
    header2 = [
        [f"{whitespace:>12}", f"z/OS {zos_ver}", f"{whitespace:>13}", f"System ID {omvs['smf74sid']}", f"{whitespace:>6}",
         f"Date {report_date:%m/%d/%Y}", f"{whitespace:>11}", f"Interval {interval_x}"],
        ["", "", "", f"RMF Version {pro['smf74mfv']:<5}", "", f"Time {report_time}", "", f"Cycle {pro['smf74cyc'] / 1000:5.3f} Seconds"]
    ]
    header3 = [
        [f"Total Samples = {pro['smf74sam']:<4,}"],
        ["                                                    OMVS SYSTEM CALL ACTIVITY"],
        ["-----------------------------------------------------------------------------------------------------------------------------------------------------------------"],
        ]
    report = (tb.tabulate(header1, tablefmt="plain") + "\n" + tb.tabulate(header2, tablefmt="plain") + "\n" +
              tb.tabulate(header3, tablefmt="plain") + "\n")
    report += \
        (tb.tabulate([
            [f"SYScalls (N/S)",f"{convert_si(omvs['r743scmn']/omvs['r743cyct']*1000,5,3):>6}",
             f"{convert_si(omvs['r743sysc']/omvs['r743cyct']*1000,5,3):>6}{'*' if omvs['r743ter'] else ' '}",
             f"{convert_si(omvs['r743scmx']/omvs['r743cyct']*1000,5,3):>6}"],
            ["CPU Time (H/S)",f"{convert_si((omvs['r743ctmn']/100)/omvs['r743cyct']*1000,5,3):>6}",
             f"{convert_si((omvs['r743cpu']/100)/omvs['r743cyct']*1000,5,3):>6}{'*' if omvs['r743ter'] else ' '}",
             f"{convert_si((omvs['r743ctmx']/100)/omvs['r743cyct']*1000,5,3):>6}"]
        ],headers=[' ','Minimum','Average','Maximum'],
            colalign=('left','right','right','right'),
            floatfmt=('','.03f','.03f','.03f')) + '\n' +
         f"                                                      OMVS PROCESS ACTIVITY\n"
         f"-----------------------------------------------------------------------------------------------------------------------------------------------------------------\n"
         + tb.tabulate([
                    ["Maximum  (Tot)",'       ',
                     f"{convert_si(omvs['r743maxp'],5,0) if not omvs['r743chpr'] else '****':>6}",
                     "                        ",
                     f"{convert_si(omvs['r743maxu'],5,0) if not omvs['r743chus'] else '****':>6}",
                     "                     ",
                     f"{convert_si(omvs['r743mxpu'],5,0) if not omvs['r743chpu'] else '****':>6}"]],tablefmt='plain',
                headers=[' ','        ','Processes','              ','Users','            ','Processes Per User'],
                colalign=('left','left','center','right','right','right','center')) + '\n' +
         "-----------------------------------------------------------------------------------------------------------------------------------------------------------------\n"
         + tb.tabulate([
                    ["Current  (Tot)",f"{convert_si(omvs['r743cpmn'],5,0):>6}",
                     f"{convert_si(float(omvs['r743curp']/pro['smf74int']),5,2):>6}",
                     f"{convert_si(omvs['r743cpmx'],5,0):>6}"," ",
                     f"{convert_si(omvs['r743cumn'],5,0):>6}",
                     f"{convert_si(omvs['r743curu']/pro['smf74int'],5,3):>6}",
                     f"{convert_si(omvs['r743cumx'],5,0):>6}"],
                    ["Overruns (N/S)",f"{convert_si(omvs['r743opmn']/omvs['r743cyct']*1000,5,3):>6}",
                     f"{convert_si(omvs['r743opr']/omvs['r743cyct']*1000,5,3):>6}{'*' if omvs['r743ter'] else ' '}",
                     f"{convert_si(omvs['r743opmx']/omvs['r743cyct']*1000,5,3):>6}"," ",
                     f"{convert_si(omvs['r743oumn']/omvs['r743cyct']*1000,5,3):>6}",
                     f"{convert_si(omvs['r743ous']/omvs['r743cyct']*1000,5,3):>6}{'*' if omvs['r743ter'] else ' '}",
                     f"{convert_si(omvs['r743oumx']/omvs['r743cyct']*1000,5,3):>6}"," ",
                     f"{convert_si(omvs['r743ormn']/omvs['r743cyct']*1000,5,3):>6}",
                     f"{convert_si(omvs['r743opru']/omvs['r743cyct']*1000,5,3):>6}{'*' if omvs['r743ter'] else ' '}",
                     f"{convert_si(omvs['r743ormx']/omvs['r743cyct']*1000,5,3):>6}"]
                ],headers=[' ','Minimum','Average','Maximum',' ','Minimum','Average','Maximum',' ','Minimum','Average','Maximum'],
                colalign=('left','right','right','right','left','right','right','right','left','right','right','right'),
                floatfmt=('','.03f','.03f','.03f','','.03f','.03f','.03f','','.03f','.03f','.03f')) +
         "\n                                                  OMVS INTER-PROCESS COMMUNICATION\n"
         "-----------------------------------------------------------------------------------------------------------------------------------------------------------------\n" +
         tb.tabulate([
             ["Maximum  (Tot)","    ",
              f"{convert_si(omvs['r743mmsg'],5,0):>6}","                 ",
              f"{convert_si(omvs['r743msem'],5,0):>6}","                 ",
              f"{convert_si(omvs['r743mshm'],5,0):>6}","              ",
              f"{convert_si(omvs['r743mspg'],6,0):>7}"]],tablefmt='plain',
            headers=[' ',' ','Message Queue IDs',' ','Semaphore IDs',' ','Shared Memory IDs',' ','Shared Memory Pages'],
            colalign=('left','center','center','center','center','center','center','center','center')) +
         "\n-----------------------------------------------------------------------------------------------------------------------------------------------------------------\n" +
         tb.tabulate([
             ["Current  (Tot)",f"{convert_si(omvs['r743cmmn'],5,0):>6}",f"{convert_si(omvs['r743cmsg']/pro['smf74int'],5,0):>6}",
              f"{convert_si(omvs['r743cmmx'],5,0):>6}",' ',
              f"{convert_si(omvs['r743csmn'],5,0):>6}",f"{convert_si(omvs['r743csem']/pro['smf74int'],5,0):>6}",
              f"{convert_si(omvs['r743csmx'],5,0):>6}",' ',
              f"{convert_si(omvs['r743chmn'],5,0):>6}",f"{convert_si(omvs['r743cshm']/pro['smf74int'],5,0):>6}",
              f"{convert_si(omvs['r743chmx'],5,0):>6}",' ',
              f"{convert_si(omvs['r743cgmn'],5,0):>6}",f"{convert_si(omvs['r743cspg']/pro['smf74int'],5,0):>6}",
              f"{convert_si(omvs['r743cgmx'],5,0):>6}"],
             ["Overruns (N/S)",f"{convert_si(omvs['r743ommn']/omvs['r743cyct']*1000,5,3):>6}",
              f"{convert_si(omvs['r743omsg']/omvs['r743cyct']*1000,5,3):>6}{'*' if omvs['r743ter'] else ' '}",
              f"{convert_si(omvs['r743ommx']/omvs['r743cyct']*1000,5,3):>6}",' ',
              f"{convert_si(omvs['r743osmn']/omvs['r743cyct']*1000,5,3):>6}",
              f"{convert_si(omvs['r743osem']/omvs['r743cyct']*1000,5,3):>6}{'*' if omvs['r743ter'] else ' '}",
              f"{convert_si(omvs['r743osmx']/omvs['r743cyct']*1000,5,3):>6}",' ',
              f"{convert_si(omvs['r743ohmn']/omvs['r743cyct']*1000,5,3):>6}",
              f"{convert_si(omvs['r743oshm']/omvs['r743cyct']*1000,5,3):>6}{'*' if omvs['r743ter'] else ' '}",
              f"{convert_si(omvs['r743ohmx']/omvs['r743cyct']*1000,5,3):>6}",' ',
              f"{convert_si(omvs['r743ogmn']/omvs['r743cyct']*1000,5,3):>6}",
              f"{convert_si(omvs['r743ospg']/omvs['r743cyct']*1000,5,3):>6}{'*' if omvs['r743ter'] else ' '}",
              f"{convert_si(omvs['r743ogmx']/omvs['r743cyct']*1000,5,3):>6}"]],
         headers=[' ','Minimum','Average','Maximum',' ','Minimum','Average','Maximum',' ','Minimum','Average','Maximum',
                  ' ','Minimum','Average','Maximum'],
         colalign=('left','right','right','right','right','right','right','right','right','right','right','right','right',
                   'right','right','right'),
         floatfmt=('','.03f','.03f','.03f','.03f','.03f','.03f','.03f','.03f','.03f','.03f','.03f','.03f','.03f','.03f','.03f')) +
         "\n                                          OMVS Memory Map                                         Shared Lib Region                        Queued Signals\n"
         f"-----------------------------------------------------------------------------------------------------------------------------------------------------------------\n" +
         tb.tabulate([
             ["Maximum  (Tot)",f"{convert_si(omvs['r743mmap'],5,0):>6}"," ",
              f"{convert_si(omvs['r743mpag'],5,0):>6}"," ",
              f"{convert_bi(omvs['r743mslr']*1024*1024,4):>6}"," ",
              f"{convert_si(omvs['r743mqds'],5,0):>6}"]],tablefmt='plain',
         headers=[' ','    Memory Map Storage Pages    ',' ','  Shared Storage Pages  ',' ',
                  '   Max Shared Library Region  ',' ','    Maximum Queued Signals   '],
         colalign=('left','center','center','center','center','center','center','center')) +
         "\n-----------------------------------------------------------------------------------------------------------------------------------------------------------------\n" +
         tb.tabulate([
             ["Current  (Tot)",f"{convert_si(omvs['r743camn'],5,0):>6}",
              f"{convert_si(omvs['r743cmap']/pro['smf74int'],5,0):>6}",
              f"{convert_si(omvs['r743camx'],5,0):>6}"," ",
              f"{convert_si(omvs['r743cxmn'],5,0):>6}",
              f"{convert_si(omvs['r743cpag']/pro['smf74int'],5,0):>6}",
              f"{convert_si(omvs['r743cxmx'],5,0):>6}"," ",
              f"{convert_bi(omvs['r743clmn']*1024*1024,4):>6}",f"{convert_bi(omvs['r743cslr']*1024*1024/pro['smf74int'],4):>6}",
              f"{convert_bi(omvs['r743clmx']*1024*1024,4):>6}"],
             ["Overruns (N/S)",f"{convert_si(omvs['r743oamn']/omvs['r743cyct']*1000,5,3):>6}",
              f"{convert_si(omvs['r743omap']/omvs['r743cyct']*1000,5,3):>6}",
              f"{convert_si(omvs['r743oamx']/omvs['r743cyct']*1000,5,3):>6}"," ",
              f"{convert_si(omvs['r743oxmn']/omvs['r743cyct']*1000,5,3):>6}",
              f"{convert_si(omvs['r743opag']/omvs['r743cyct']*1000,5,3):>6}",
              f"{convert_si(omvs['r743oxmx']/omvs['r743cyct']*1000,5,3):>6}"," ",
              f"{convert_si(omvs['r743olmn']/omvs['r743cyct']*1000,5,3):>6}",
              f"{convert_si(omvs['r743oslr']/omvs['r743cyct']*1000,5,3):>6}",
              f"{convert_si(omvs['r743olmx']/omvs['r743cyct']*1000,5,3):>6}"," ",
              f"{convert_si(omvs['r743oqmn']/omvs['r743cyct']*1000,5,3):>6}",
              f"{convert_si(omvs['r743oqds']/omvs['r743cyct']*1000,5,3):>6}",
              f"{convert_si(omvs['r743oqmx']/omvs['r743cyct']*1000,5,3):>6}"]],
         headers=[' ','Minimum','Average','Maximum',' ','Minimum','Average','Maximum',' ',
                  'Minimum','Average','Maximum',' ','Minimum','Average','Maximum'],
         colalign=('left','right','right','right','right','right','right','right','right',
                   'right','right','right','right','right','right','right'),
         floatfmt=('','.03f','.03f','.03f','','.03f','.03f','.03f','','.03f','.03f','.03f','','.03f','.03f','.03f')) +
         "\n\nUnits:   (Tot) = Total Value, (N/S) = Number per Second, (H/S) = Hundredth of seconds per Second\n"
         )
    return report

def format_xcf_header(duration, pro):
    if duration == 'Hourly':
        report_date = pro['date']
        report_time = pro['datetime'].time().strftime('%H.%M.%S')
        interval = format_s2min(pro['smf74int'])
    elif duration == 'Daily':
        report_date = pro['date']
        report_time = '00.00.00'
        interval = format_s2hr(pro['smf74int'])
    else:
        report_date = pro['smf74ist'].date()
        report_time = pro['smf74ist'].time().strftime('%H.%M.%S')
        interval = format_s2min(pro['smf74int'])
    zos_ver = 'V' + pro['smf74mvs'][2:4].lstrip('0') + 'R' + pro['smf74mvs'][4:6].lstrip('0')
    interval_x = f"{interval[:-3]}"
    whitespace = ' '
    header1 = [["                                                       X C F  A C T I V I T Y"]]
    header2 = [
        [f"{whitespace:>12}", f"z/OS {zos_ver}", f"{whitespace:>13}", f"System ID {pro['smf74sid']}", f"{whitespace:>6}",
         f"Date {report_date:%m/%d/%Y}", f"{whitespace:>11}", f"Interval {interval_x}"],
        ["", "", "", f"RMF Version {pro['smf74mfv']:<5}", "", f"Time {report_time}", "", f"Cycle {pro['smf74cyc'] / 1000:5.3f} Seconds"]
    ]
    return tb.tabulate(header1, tablefmt="plain") + "\n" + tb.tabulate(header2, tablefmt="plain") + "\n"

def format_xcf_sys_detail(syss, mbrs_list, pro):
    if len(syss) == 0:
        return None
    header = [
        [f"                                                        XCF Usage By System\n"],
        [f"--------------------------------------------------------------------------------------------------------------------------------------------------------------------\n"],
        [f"                                            Remote Systems                                                          Local\n"],
        [f"---------------------------------------------------------------------------------------------------------------------------------------- -----------------------\n"],
        [f"                          Outbound From {pro['smf74sid']}                                                             Inbound To {pro['smf74sid']}                      {pro['smf74sid']}\n"],
        [f"---------------------------------------------------------------------------------------------------  ----------------------------------- -----------------------\n"],
    ]
    report_out_dict = {}
    report_in_dict = {}
    report_local = []
    total_outbound_req_out = 0
    total_inbound_req_in = 0
    for idx_1, sys in enumerate(syss):
        if sys['r742sdir'] == 'OUT':
            if sys['r742snme'] not in report_out_dict.keys():
                report_out_dict[sys['r742snme']] = []
                detail_line = [sys['r742snme']]
            else:
                detail_line = [""]
            outbound_req_out = sys['r742sbig'] + sys['r742sfit'] + sys['r742ssml']
            total_outbound_req_out += outbound_req_out
            detail_line += \
                [f"{sys['r742stcn']:<8}", f"{sys['r742stcl']:>9,}", f"{outbound_req_out:>11,}",
                 f"{sys['r742ssml'] / outbound_req_out * 100 if outbound_req_out > 0 else 0:>3.0f}",
                 f"{sys['r742sfit'] / outbound_req_out * 100 if outbound_req_out > 0 else 0:>3.0f}",
                 f"{sys['r742sbig'] / outbound_req_out * 100 if outbound_req_out > 0 else 0:>3.0f}",
                 f"{sys['r742sovr'] / sys['r742sbig'] * 100 if sys['r742sbig'] > 0 else 0:>3.0f}",
                 f"{sys['r742snop']:>9,}", f"{sys['r742sbsy'] + sys['r742snop']:>8,}"]
            report_out_dict[sys['r742snme']].append(detail_line)

        elif sys['r742sdir'] == 'IN':
            total_sent = 0
            if len(mbrs_list[idx_1]) > 0:
                for mbr in mbrs_list[idx_1]:
                    total_sent += mbr['r742msnt']
            if sys['r742snme'] not in report_in_dict.keys():
                report_in_dict[sys['r742snme']] = []
                detail_line2 = [sys['r742snme']]
            else:
                detail_line2 = [""]
            inbound_req_rej = sys['r742sbsy'] + sys['r742snop']
            total_inbound_req_in += total_sent
            detail_line2 += [f"{total_sent:>15,}", f"{inbound_req_rej:>8,}"]
            report_in_dict[sys['r742snme']].append(detail_line2)
        else:
            total_local_req_rej = sys['r742sbsy']
            report_local.append([f"{sys['r742stcn']:<8}", f"{total_local_req_rej:>9,}"])
    report_table = []
    j = 0
    for system in report_out_dict.keys():
        for i in range(0, len(report_out_dict[system])):
            row = report_out_dict[system][i].copy()
            if i == 0 and system in report_in_dict.keys():
                row += report_in_dict[system][0]
            else:
                row += ["", "", ""]
            if j < len(report_local):
                row += report_local[j]
                j += 1
            report_table.append(row)
    report_table.append(tb.SEPARATING_LINE)
    report_table.append(
        ['Total', '', '', f"{total_outbound_req_out:>,}", '', '', '', '', '', '', 'Total', f"{total_inbound_req_in:>,}"])
    return (tb.tabulate(header, tablefmt="plain") + "\n" +
            tb.tabulate(report_table,
                        headers=["\nTo\nSystem","\nTransport\nClass","\nBuffer\nLength","\nReq\nOut",
                                 "<---\n% \nSml","Buffer\n% \nFit","\n% \nBig","--->\n% \nOvr",
                                 "All\nPaths\nUnavail","\nReq\nReject",
                                 "\nFrom\nSystem","\nReq\nIn","\nReq\nReject",
                                 "\nTransport\nClass","\nReq\nReject"],
                        colalign=('left','left','right','right','right','right','right','right','right','right',
                                  'left','right','right','left','right'),
                        ) + '\n')

def format_xcf_path_detail(paths, paths_group_list, pro):
    if len(paths) == 0:
        return None
    header1 = [
        [f"Total Samples = {pro['smf74sam']:<4}                             XCF Path Statistics                                        "],
        [f"                             Outbound From {pro['smf74sid']}"],
        tb.SEPARATING_LINE,
    ]
    header2 = [
        [f"                                                Inbound To {pro['smf74sid']}                                                               "],
    ]
    # paths_group_list = [list(g) for k, g in groupby(paths, attrgetter('r742pdir'))]
    outbound_dict = {}
    inbound_dict = {}
    in_report_table = []
    out_report_table = []
    total_req_out = 0
    total_req_in = 0
    for paths_list in paths_group_list:
        for path in paths_list:
            if path['r742pdir'] == 'OUT':
                if path['r742pona'] not in outbound_dict.keys():
                    outbound_dict[path['r742pona']] = []
                total_req_out += path['r742psig']
                outbound_dict[path['r742pona']].append(
                    [f"{'C' if path['r742ptyp'] == '0x01' else 'S':1}", f"{path['r742pstr']:<16}", f"{path['r742ptcn']:<8}",
                     f"{path['r742psig']:>,}", f"{path['r742pqln'] / pro['smf74sam']:>8.2f}", f"{path['r742psus']:>8,}", f"{path['r742papp']:>8,}",
                     f"{path['r742prst']:>8,}"])
            else:  # inbound
                if path['r742pona'] not in inbound_dict.keys():
                    inbound_dict[path['r742pona']] = []
                total_req_in += path['r742psig']
                inbound_dict[path['r742pona']] += [
                    [f"{'C' if path['r742ptyp'] == '0x01' else 'S':1}", f"{path['r742pstr']:<16}",
                     f"{path['r742psig']:>7,}", f"{path['r742pibr']:>8,}",
                     f"{path['r742piot'] * 1000:>9,.3f}",
                     f"{path['r742pnib_timesum'] * 1000:>9,.3f}", f"{path['r742pnib_timenum']:>8,}",
                     f"{path['r742pusg_percent_1']:>3}", f"{path['r742pusg_timesum_1'] * 1000:>9,.3f}",
                     f"{path['r742pusg_timenum_1']:8,}", f"{path['r742pusg_sigcnt_1']:>10,}"],
                    ["", "", "", "", "", "", "", f"{path['r742pusg_percent_2']:>3}",
                     f"{path['r742pusg_timesum_2'] * 1000:>9,.3f}", f"{path['r742pusg_timenum_2']:8,}",
                     f"{path['r742pusg_sigcnt_2']:>10,}"],
                    ["", "", "", "", "", "", "", f"{path['r742pusg_percent_3']:>3}",
                     f"{path['r742pusg_timesum_3'] * 1000:>9,.3f}", f"{path['r742pusg_timenum_3']:8,}",
                     f"{path['r742pusg_sigcnt_3']:>10,}"],
                    ["", "", "", "", "", "", "", f"{path['r742pusg_percent_4']:>3}",
                     f"{path['r742pusg_timesum_4'] * 1000:>9,.3f}", f"{path['r742pusg_timenum_4']:8,}",
                     f"{path['r742pusg_sigcnt_4']:>10,}"]]
    for pona in outbound_dict.keys():
        for i in range(0, len(outbound_dict[pona])):
            if i == 0:
                row = [pona]
            else:
                row = [""]
            row += outbound_dict[pona][i]
            out_report_table.append(row)
    if len(outbound_dict.keys()) > 0:
        total_row = ["Total", "", "", "", f"{total_req_out:>,}"]
        out_report_table.append(tb.SEPARATING_LINE)
        out_report_table.append(total_row)
    for pona in inbound_dict.keys():
        for i in range(0, len(inbound_dict[pona])):
            if i == 0:
                row = [pona]
            else:
                row = [""]
            row += inbound_dict[pona][i]
            in_report_table.append(row)
    if len(inbound_dict.keys()) > 0:
        total_row = ["Total", "", "", f"{total_req_in:>,}"]
        in_report_table.append(tb.SEPARATING_LINE)
        in_report_table.append(total_row)
    return (tb.tabulate(header1, headers="firstrow") + '\n' +
            tb.tabulate(out_report_table,
                        headers=["\nTo\nSystem","T\nY\nP","From/To\nDevice, Or\nStructure",
                                 "\nTransport\nClass","\nReq\nOut","\nAvg Q\nLngth","\n\nAvail",
                                 "\n\nBusy","\n\nRetry"],
                        colalign=('left','center','left','left','right','right','right','right','right'),
                        floatfmt=('','','','','.0f','.2f','.0f','.0f','.0f')) + '\n\n' +
            tb.tabulate(header2, headers="firstrow") + '\n' +
            tb.tabulate(in_report_table,
                        headers=["\nFrom\nSystem","T\nY\nP","From/To\nDevice, Or\nStructure","\nReq\nIn","\nBuffers\nUnavail",
                                 "\nTransfer\nTime","\nNo Buf\nTime","\n\nNo Buf","<----\n\nUtil%"," Usage \nIn Use\nTime",
                                 "------\n\nIn Use","------>\n\nSignals"],
                        colalign=('left','center','left','right','right','right','right','right','right','right',
                                  'right','right'),
                        floatfmt=('','','','.0f','.0f','.3f','.3f','.0f','.0f','.3f','.0f','.0f')))

def format_xcf_mbr_detail(mbrs, mbr_group_list, pro):
    if len(mbrs) == 0:
        return None
    header = [
        ["                                          XCF Usage By Member                                       "],
        [f"Members Communicating With {pro['smf74sid']}                                           Members On {pro['smf74sid']}"],
        ["-----------------------------------------------       ------------------------------------------------"]
    ]
    # mbr_group_list = [list(g) for k, g in groupby(mbrs, attrgetter('r742mgrp'))]
    mbr_comm_dict = {}
    mbr_on_dict = {}
    report_table = []
    for mbr_list in mbr_group_list:
        for mbr in mbr_list:
            if mbr['r742msys'] != pro['smf74sid']:
                if mbr['r742mgrp'] not in mbr_comm_dict.keys():
                    mbr_comm_dict[mbr['r742mgrp']] = []
                mbr_comm_dict[mbr['r742mgrp']].append([mbr['r742mmem'], mbr['r742msys'], mbr['r742mrcv'], mbr['r742msnt']])
            else:
                if mbr['r742mgrp'] not in mbr_on_dict.keys():
                    mbr_on_dict[mbr['r742mgrp']] = []
                mbr_on_dict[mbr['r742mgrp']].append([mbr['r742mmem'], mbr['r742msnt'], mbr['r742mrcv']])
    mgrp_list = sorted(list(set(list(mbr_comm_dict.keys()) + list(mbr_on_dict.keys()))))
    for mgrp in mgrp_list:
        total_gp_comm_req_fr = 0
        total_gp_comm_req_to = 0
        total_gp_on_req_out = 0
        total_gp_on_req_in = 0
        if mgrp in mbr_comm_dict.keys():
            for i in range(0, len(mbr_comm_dict[mgrp])):
                if i == 0:
                    row = [mgrp]
                else:
                    row = [""]
                row += [mbr_comm_dict[mgrp][i][0],mbr_comm_dict[mgrp][i][1],
                        f"{mbr_comm_dict[mgrp][i][2]:>,}", f"{mbr_comm_dict[mgrp][i][3]:>,}", ""]
                total_gp_comm_req_fr += mbr_comm_dict[mgrp][i][2]
                total_gp_comm_req_to += mbr_comm_dict[mgrp][i][3]
                if mgrp in mbr_on_dict.keys():
                    if i == 0:
                        row += [mgrp]
                    else:
                        row += [""]
                    if i < len(mbr_on_dict[mgrp]):
                        total_gp_on_req_out += mbr_on_dict[mgrp][i][1]
                        total_gp_on_req_in += mbr_on_dict[mgrp][i][2]
                        row += [mbr_on_dict[mgrp][i][0],
                                f"{mbr_on_dict[mgrp][i][1]:>,}", f"{mbr_on_dict[mgrp][i][2]:>,}"]
                report_table.append(row)
            total_row = ["Total", "", "", f"{total_gp_comm_req_fr:>,}", f"{total_gp_comm_req_to:>,}", ""]
            if mgrp in mbr_on_dict.keys():
                total_row += ["Total", "", f"{total_gp_on_req_out:>,}", f"{total_gp_on_req_in:>,}"]
            report_table.append(tb.SEPARATING_LINE)
            report_table.append(total_row)
            report_table.append([" "])
        else:
            total_row = ["", "", "", "", "", ""]
            for i in range(0, len(mbr_on_dict[mgrp])):
                row = ["", "", "", "", "", ""]
                if i == 0:
                    row += [mgrp]
                else:
                    row += [""]
                total_gp_on_req_out += mbr_on_dict[mgrp][i][1]
                total_gp_on_req_in += mbr_on_dict[mgrp][i][2]
                row += [mbr_on_dict[mgrp][i][0],
                        f"{mbr_on_dict[mgrp][i][1]:>,}", f"{mbr_on_dict[mgrp][i][2]:>,}"]
                report_table.append(row)
            total_row += ["Total", "", f"{total_gp_on_req_out:>,}", f"{total_gp_on_req_in:>,}"]
            report_table.append(tb.SEPARATING_LINE)
            report_table.append(total_row)
            report_table.append([" "])
    return (tb.tabulate(header, headers="firstrow") + "\n" +
            tb.tabulate(report_table,
                        headers=["\n\nGroup","\n\nMember","\n\nSystem",f"Req\nFrom\n{pro['smf74sid']}",
                                 f"Req\nTo\n{pro['smf74sid']}","      ","\n\nGroup","\n\nMember","\nReq\nOut","\nReq\nIn"],
                        colalign=('left','left','left','right','right','left',
                                  'left','left','right','right')) + '\n')

def format_xcf_activity_report(duration, ctl, pro, syss, mbrs, paths, mbrs_list, mbrs_group_list, paths_group_list):
    page_detail = ''
    if duration == 'Hourly':
        report_time = ctl['datetime']
    elif duration == 'Daily':
        report_time = ctl['date']
    else:
        report_time = ctl['smf74ist']
    if len(syss) == 0 or len(mbrs) == 0:
        return None
    xcf_object_list = []
    report = format_xcf_header(duration, pro)
    report_detail_1 = format_xcf_sys_detail(syss, mbrs_list, pro)
    report_detail_2 = format_xcf_mbr_detail(mbrs, mbrs_group_list, pro)
    report_detail_3 = format_xcf_path_detail(paths, paths_group_list, pro)
    if report_detail_1 is not None:
        page_detail += (report + report_detail_1)
        xcf_object_list.append({"id":f"XCF Usage by System {report_time}","content": report + report_detail_1})
    if report_detail_2 is not None:
        page_detail += (report + report_detail_2)
        xcf_object_list.append({"id":f"XCF Usage by Member {report_time}","content": report + report_detail_2})
    if report_detail_3 is not None:
        page_detail += (report + report_detail_3)
        xcf_object_list.append({"id":f"XCF Path Statistics {report_time}","content": report + report_detail_3})
    return xcf_object_list, page_detail