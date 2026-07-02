import sys
from pathlib import Path
import click
from collections.abc import Callable

from rich.progress import Progress, SpinnerColumn, TextColumn
from datetime import datetime
from smf2db import JSON_ERROR, ERRORS
from smf2db.api.api_1101 import print_cics_performance_report
from smf2db.api.api_1102 import print_cics_statistics_report
from smf2db.api.api_123 import print_zcee_request_report
from smf2db.api.api_30 import print_addr_space_activity_report
from smf2db.api.api_70 import print_cpu_activity_report, print_crypto_activity_report
from smf2db.api.api_71 import print_paging_activity_report
from smf2db.api.api_72 import print_serialization_delay, print_workload_activity_report
from smf2db.api.api_73 import print_channel_activity_report
from smf2db.api.api_74 import print_cache_subsystem_activity, print_device_activity, print_cf_activity, \
    print_hfs_statistics, print_fcd_activity, print_ess_activity, print_eadm_activity, print_pcie_activity, \
    print_xcf_activity, print_omvs_activity
from smf2db.api.api_75 import print_psd_activity_report
from smf2db.api.api_77 import print_enq_activity_report
from smf2db.api.api_78 import print_ioq_activity, print_vstor_activity
from smf2db.sumup.commands import check_date_range


def process_print_command(smf_type: str, out, print_func: Callable, jsonfiles, *args):
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description=f"Printing {smf_type}...{jsonfiles}", total=None)
        try:
            report = print_func(jsonfiles, *args)
            click.echo("\n")
            if not 'No data found' in report and not 'Invalid JSON file.' in report:
                if report != "":
                    click.echo(report, file=out)
                else:
                    click.echo("No data found.")
            else:
                click.echo(report)
                # click.echo("No data found.")
            click.echo(f"Printing {smf_type} report was completed.")
        except OSError:
            click.echo(f"Printing report failed with '{ERRORS[JSON_ERROR]}'")
            raise SystemExit(1)
    # click.echo(f"Printing {smf_type} report was completed.")

@click.command("30")
@click.argument(
    'jsonfiles',
    type=click.Path(
        exists=True,
        file_okay=True,
        readable=True,
        path_type=Path,
    ),
    required=True,
    nargs=-1)
@click.option("-s", "--start_time",type=click.DateTime(formats=["%Y-%m-%d %H:%M"]),default="2000-01-01 00:00",help="Start time (YYYY-MM-DD HH:MM)")
@click.option("-e", "--end_time", type=click.DateTime(formats=["%Y-%m-%d %H:%M"]), default=str(datetime.now())[:16], help="End time (YYYY-MM-DD HH:MM)", callback=check_date_range)
@click.option("-i", "--interval", type=click.INT, required=True, default=30,
              help="SMF Interval in seconds.")
@click.option("-t", "--subtype", type=click.IntRange(min=1,max=6), default=None)
@click.option("-j", "--jobname", type=str, default=None, help="Job name.")
@click.option("-x", "--exclude_job_starts", type=str, default=None, help="Exclude job starts with.")
@click.option("-o", "--out", type=click.File('at'), help="File to write the Output to, omit to display on screen.", default=sys.stdout)
def print_30(jsonfiles, start_time, end_time, interval, subtype, jobname, exclude_job_starts, out) -> None:
    """Print smf30 address space activity report from jsonfile(s)."""
    process_print_command('smf30', out, print_addr_space_activity_report, jsonfiles,
                          start_time, end_time, interval, subtype, jobname, exclude_job_starts)

@click.command("70")
@click.argument(
    'jsonfiles',
    type=click.Path(
        exists=True,
        file_okay=True,
        readable=True,
        path_type=Path,
    ),
    required=True,
    nargs=-1)
@click.option("-r", "--report_type", required=True, type=click.Choice(['CPU Activity Report', 'Crypto Hardware Activity Report']))
@click.option("-l", "--lpar", required=True, type=str, help="Target LPAR")
@click.option("-s", "--start_time",type=click.DateTime(formats=["%Y-%m-%d %H:%M"]),default="2000-01-01 00:00",help="Start time (YYYY-MM-DD HH:MM)")
@click.option("-e", "--end_time", type=click.DateTime(formats=["%Y-%m-%d %H:%M"]), default=str(datetime.now())[:16], help="End time (YYYY-MM-DD HH:MM)", callback=check_date_range)
@click.option("-o", "--out", type=click.File('at'), help="File to write the Output to, omit to display on screen.", default=sys.stdout)
def print_70(jsonfiles, report_type, lpar, start_time, end_time, out) -> None:
    """Print smf70 RMF reports from jsonfile(s)."""
    if report_type == 'CPU Activity Report':
        process_print_command('smf70', out, print_cpu_activity_report, jsonfiles, lpar, start_time, end_time)
    else:
        process_print_command('smf70', out, print_crypto_activity_report, jsonfiles, lpar, start_time, end_time)

@click.command("71")
@click.argument(
    'jsonfiles',
    type=click.Path(
        exists=True,
        file_okay=True,
        readable=True,
        path_type=Path,
    ),
    required=True,
    nargs=-1)
@click.option("-l", "--lpar", required=True, type=str, help="Target LPAR")
@click.option("-s", "--start_time",type=click.DateTime(formats=["%Y-%m-%d %H:%M"]),default="2000-01-01 00:00",help="Start time (YYYY-MM-DD HH:MM)")
@click.option("-e", "--end_time", type=click.DateTime(formats=["%Y-%m-%d %H:%M"]), default=str(datetime.now())[:16], help="End time (YYYY-MM-DD HH:MM)", callback=check_date_range)
@click.option("-o", "--out", type=click.File('at'), help="File to write the Output to, omit to display on screen.", default=sys.stdout)
def print_71(jsonfiles, lpar, start_time, end_time, out) -> None:
    """Print smf71 RMF reports from jsonfile(s)."""
    process_print_command('smf71', out, print_paging_activity_report, jsonfiles, lpar, start_time, end_time)

@click.command("72")
@click.argument(
    'jsonfiles',
    type=click.Path(
        exists=True,
        file_okay=True,
        readable=True,
        path_type=Path,
    ),
    required=True,
    nargs=-1)
@click.option("-r", "--report_type", required=True, type=click.Choice(['Workload Activity Report', 'Serialization Delay Report']))
@click.option("-l", "--lpar", required=True, type=str, help="Target LPAR")
@click.option("-s", "--start_time",type=click.DateTime(formats=["%Y-%m-%d %H:%M"]),default="2000-01-01 00:00",help="Start time (YYYY-MM-DD HH:MM)")
@click.option("-e", "--end_time", type=click.DateTime(formats=["%Y-%m-%d %H:%M"]), default=str(datetime.now())[:16], help="End time (YYYY-MM-DD HH:MM)", callback=check_date_range)
@click.option("-o", "--out", type=click.File('at'), help="File to write the Output to, omit to display on screen.", default=sys.stdout)
@click.option("-c", "--category", type=click.Choice(['Workload Group', 'Service Class', 'Report Class', None]), default=None)
@click.option("-x", "--lpar_sysplex", type=click.Choice(['Lpar', 'Sysplex', None]), default=None)
@click.option("-X", "--sysplex_name", type=str, help="Target Lpar/Sysplex name", default=None)
@click.option("-w", "--wlm_selected", type=str, help="Target workload/Service/Report name", default=None)
@click.option("-z", "--zos_version", type=click.Choice(['Y', 'N']), help="z/OS version > 2.2.0", default=None)
@click.option("-a", "--cpa_actual", type=click.INT, default=None, help="Physical CPU adustment factor.")
def print_72(jsonfiles, report_type, lpar, start_time, end_time, out,
             category=None, lpar_sysplex=None, sysplex_name=None, wlm_selected=None,
             zos_version=None, cpa_actual=None) -> None:
    """Print smf72 RMF reports from jsonfile(s)."""
    if report_type == 'Serialization Delay Report':
        process_print_command('smf72', out, print_serialization_delay, jsonfiles, lpar, start_time, end_time)
    else:
        if category is None:
            category = click.prompt("Enter the type of report",
                                    type=click.Choice(['Workload Group', 'Service Class', 'Report Class']), default='Service Class')
        if lpar_sysplex is None:
            lpar_sysplex = click.prompt("By Sysplex or Lpar", type=click.Choice(['Lpar', 'Sysplex']), default='Lpar')
        if lpar_sysplex == 'Sysplex':
            if sysplex_name is None:
                lpar_sysplex_name = click.prompt("Sysplex name", type=str)
            else:
                lpar_sysplex_name = sysplex_name
        else:
            lpar_sysplex_name = lpar
        if wlm_selected is None:
            if category == 'Workload Group':
                wlm_selected = click.prompt("Target Workload Group", default='All', type=str)
            elif category == 'Service Class':
                wlm_selected = click.prompt("Target Service Class", default='All', type=str)
            else:
                wlm_selected = click.prompt("Target Report Class", default='All', type=str)
        if wlm_selected == 'All':
            wlm_selected = None
        if zos_version is None:
            zos_version = click.prompt("z/OS version > 2.2.0", type=click.Choice(['Y', 'N']), default='Y')
            if zos_version == 'N':
                cpa_actual = click.prompt("Enter Physical CPU adustment factor if known", type=int, default=None)
            else:
                cpa_actual = None
        process_print_command('smf72', out, print_workload_activity_report, jsonfiles, lpar, start_time, end_time,
                              category, lpar_sysplex, lpar_sysplex_name, wlm_selected, cpa_actual)

@click.command("73")
@click.argument(
    'jsonfiles',
    type=click.Path(
        exists=True,
        file_okay=True,
        readable=True,
        path_type=Path,
    ),
    required=True,
    nargs=-1)
@click.option("-l", "--lpar", required=True, type=str, help="Target LPAR")
@click.option("-s", "--start_time",type=click.DateTime(formats=["%Y-%m-%d %H:%M"]),default="2000-01-01 00:00",help="Start time (YYYY-MM-DD HH:MM)")
@click.option("-e", "--end_time", type=click.DateTime(formats=["%Y-%m-%d %H:%M"]), default=str(datetime.now())[:16], help="End time (YYYY-MM-DD HH:MM)", callback=check_date_range)
@click.option("-o", "--out", type=click.File('at'), help="File to write the Output to, omit to display on screen.", default=sys.stdout)
def print_73(jsonfiles, lpar, start_time, end_time, out) -> None:
    """Print smf73 RMF reports from jsonfile(s)."""
    process_print_command('smf73', out, print_channel_activity_report, jsonfiles, lpar, start_time, end_time)

@click.command("74")
@click.argument(
    'jsonfiles',
    type=click.Path(
        exists=True,
        file_okay=True,
        readable=True,
        path_type=Path,
    ),
    required=True,
    nargs=-1)
@click.option("-r", "--report_type", required=True, type=click.Choice(
    ["Cache Subsystem Activity", "CF Activity", "OMVS Activity", 'Device Activity',
     "EADM Activity", "ESS Activity", "FCD Activity", "HFS Statistics",
     "PCIE Activity", "XCF Activity"]))
@click.option("-l", "--lpar", required=True, type=str, help="Target LPAR")
@click.option("-s", "--start_time",type=click.DateTime(formats=["%Y-%m-%d %H:%M"]),default="2000-01-01 00:00",help="Start time (YYYY-MM-DD HH:MM)")
@click.option("-e", "--end_time", type=click.DateTime(formats=["%Y-%m-%d %H:%M"]), default=str(datetime.now())[:16], help="End time (YYYY-MM-DD HH:MM)", callback=check_date_range)
@click.option("-o", "--out", type=click.File('at'), help="File to write the Output to, omit to display on screen.", default=sys.stdout)
@click.option("-S", "--ssid", type=str, help="Target SSID", default=None)
@click.option("-d", "--device", type=click.Choice(
    ['DASD', 'Tape', 'Communication Device', 'Graphic Device', None]), help="Target device type", default=None)
@click.option("-C", "--cf", type=str, help="Target Coupling Facility name", default=None)
@click.option("-R", "--cache_report_type", type=click.Choice(
    ["Cache Subsystem Summary", "Cache Subsystem Status and Overview", "Cache Device Status and Activity", None]),
              help="Target sub report type for Cache Subsystem Activity", default=None)
@click.option("-H", "--hfs_report_type", type=click.Choice(
    ["HFS Global Statistics", "HFS File System Statistics", None]),
              help="Target sub report type for HFS Statistics", default=None)
@click.option("-F", "--switch", type=str, help="Target Switch", default=None)
@click.option("-E", "--ess_report_type", type=click.Choice(
    ["Link Statistics", "Synchronous I/O Link Statistics", "Extent Pool Statistics", "Rank Statistics", None]),
              help="Target sub report type for ESS Activity", default=None)
@click.option("-U", "--cu", type=str, help="Target Control Unit Serial Number", default=None)
def print_74(jsonfiles, report_type, lpar, start_time, end_time, out,
             ssid=None, device=None, cf=None, cache_report_type=None, hfs_report_type=None, switch=None,
             ess_report_type=None, cu=None) -> None:
    """Print smf74 RMF reports from jsonfile(s)."""
    if report_type == 'Cache Subsystem Activity':
        if cache_report_type is None:
            cache_report_type = click.prompt("Enter the report type", type=click.Choice(
                ["Cache Subsystem Summary", "Cache Subsystem Status and Overview", "Cache Device Status and Activity"]))
        if ssid == 'All':
            ssid = None
        process_print_command('smf74', out, print_cache_subsystem_activity, jsonfiles, lpar, start_time, end_time, cache_report_type, ssid)
    elif report_type == 'Device Activity':
        if device is None:
            target_device_type = click.prompt("Enter the target device type",
                                              type=click.Choice(['DASD', 'Tape', 'Communication Device', 'Graphic Device']))
        else:
            target_device_type = device
        process_print_command('smf74', out, print_device_activity, jsonfiles, lpar, start_time, end_time, target_device_type)
    elif report_type == 'CF Activity':
        process_print_command('smf74', out, print_cf_activity, jsonfiles, lpar, start_time, end_time, cf)
    elif report_type == 'OMVS Activity':
        process_print_command('smf74', out, print_omvs_activity, jsonfiles, lpar, start_time, end_time)
    elif report_type == 'HFS Statistics':
        process_print_command('smf74', out, print_hfs_statistics, jsonfiles, lpar, start_time, end_time, hfs_report_type)
    elif report_type == 'FCD Activity':
        process_print_command('smf74', out, print_fcd_activity, jsonfiles, start_time, end_time, switch)
    elif report_type == 'ESS Activity':
        process_print_command('smf74', out, print_ess_activity, jsonfiles, start_time, end_time, cu, ess_report_type)
    elif report_type == 'EADM Activity':
        process_print_command('smf74', out, print_eadm_activity, jsonfiles, lpar, start_time, end_time)
    elif report_type == 'PCIE Activity':
        process_print_command('smf74', out, print_pcie_activity, jsonfiles, start_time, end_time)
    elif report_type == 'XCF Activity':
        process_print_command('smf74', out, print_xcf_activity, jsonfiles, lpar, start_time, end_time)


@click.command("75")
@click.argument(
    'jsonfiles',
    type=click.Path(
        exists=True,
        file_okay=True,
        readable=True,
        path_type=Path,
    ),
    required=True,
    nargs=-1)
@click.option("-l", "--lpar", required=True, type=str, help="Target LPAR")
@click.option("-s", "--start_time",type=click.DateTime(formats=["%Y-%m-%d %H:%M"]),default="2000-01-01 00:00",help="Start time (YYYY-MM-DD HH:MM)")
@click.option("-e", "--end_time", type=click.DateTime(formats=["%Y-%m-%d %H:%M"]), default=str(datetime.now())[:16], help="End time (YYYY-MM-DD HH:MM)", callback=check_date_range)
@click.option("-o", "--out", type=click.File('at'), help="File to write the Output to, omit to display on screen.", default=sys.stdout)
def print_75(jsonfiles, lpar, start_time, end_time, out) -> None:
    """Print smf75 RMF reports from jsonfile(s)."""
    process_print_command('smf75', out, print_psd_activity_report, jsonfiles, lpar, start_time, end_time)

@click.command("77")
@click.argument(
    'jsonfiles',
    type=click.Path(
        exists=True,
        file_okay=True,
        readable=True,
        path_type=Path,
    ),
    required=True,
    nargs=-1)
@click.option("-l", "--lpar", required=True, type=str, help="Target LPAR")
@click.option("-s", "--start_time",type=click.DateTime(formats=["%Y-%m-%d %H:%M"]),default="2000-01-01 00:00",help="Start time (YYYY-MM-DD HH:MM)")
@click.option("-e", "--end_time", type=click.DateTime(formats=["%Y-%m-%d %H:%M"]), default=str(datetime.now())[:16], help="End time (YYYY-MM-DD HH:MM)", callback=check_date_range)
@click.option("-o", "--out", type=click.File('at'), help="File to write the Output to, omit to display on screen.", default=sys.stdout)
def print_77(jsonfiles, lpar, start_time, end_time, out) -> None:
    """Print smf77 RMF reports from jsonfile(s)."""
    process_print_command('smf77', out, print_enq_activity_report, jsonfiles, lpar, start_time, end_time)

@click.command("78")
@click.argument(
    'jsonfiles',
    type=click.Path(
        exists=True,
        file_okay=True,
        readable=True,
        path_type=Path,
    ),
    required=True,
    nargs=-1)
@click.option("-r", "--report_type", required=True, type=click.Choice(["I/O Queuing Activity Report", "Virtual Storage Activity Report"]))
@click.option("-l", "--lpar", required=True, type=str, help="Target LPAR")
@click.option("-s", "--start_time",type=click.DateTime(formats=["%Y-%m-%d %H:%M"]),default="2000-01-01 00:00",help="Start time (YYYY-MM-DD HH:MM)")
@click.option("-e", "--end_time", type=click.DateTime(formats=["%Y-%m-%d %H:%M"]), default=str(datetime.now())[:16], help="End time (YYYY-MM-DD HH:MM)", callback=check_date_range)
@click.option("-o", "--out", type=click.File('at'), help="File to write the Output to, omit to display on screen.", default=sys.stdout)
@click.option("-L", "--lcu", type=str, help="Target LCU", default=None)
@click.option("-R", "--sub_report_type", type=click.Choice(["Common Storage", "Private Area"]), default="Common Storage")
def print_78(jsonfiles, report_type, lpar, start_time, end_time, out, sub_report_type, lcu=None) -> None:
    """Print smf78 RMF reports from jsonfile(s)."""
    if report_type == 'I/O Queuing Activity Report':
        process_print_command('smf78', out, print_ioq_activity, jsonfiles, lpar, start_time, end_time, lcu)
    elif report_type == 'Virtual Storage Activity Report':
        process_print_command('smf78', out, print_vstor_activity, jsonfiles, lpar, start_time, end_time, sub_report_type)

@click.command("123")
@click.argument(
    'jsonfiles',
    type=click.Path(
        exists=True,
        file_okay=True,
        readable=True,
        path_type=Path,
    ),
    required=True,
    nargs=-1)
@click.option("-s", "--start_time",type=click.DateTime(formats=["%Y-%m-%d %H:%M"]),default="2000-01-01 00:00",help="Start time (YYYY-MM-DD HH:MM)")
@click.option("-e", "--end_time", type=click.DateTime(formats=["%Y-%m-%d %H:%M"]), default=str(datetime.now())[:16], help="End time (YYYY-MM-DD HH:MM)", callback=check_date_range)
@click.option("-o", "--out", type=click.File('at'), help="File to write the Output to, omit to display on screen.", default=sys.stdout)
def print_123(jsonfiles, start_time, end_time, out) -> None:
    """Print smf123 ZCEE request report from jsonfile(s)."""
    process_print_command('smf123', out, print_zcee_request_report, jsonfiles, start_time, end_time)

@click.command("110_1")
@click.argument(
    'jsonfiles',
    type=click.Path(
        exists=True,
        file_okay=True,
        readable=True,
        path_type=Path,
    ),
    required=True,
    nargs=-1)
@click.option("-s", "--start_time",type=click.DateTime(formats=["%Y-%m-%d %H:%M"]),default="2000-01-01 00:00",help="Start time (YYYY-MM-DD HH:MM)")
@click.option("-e", "--end_time", type=click.DateTime(formats=["%Y-%m-%d %H:%M"]), default=str(datetime.now())[:16], help="End time (YYYY-MM-DD HH:MM)", callback=check_date_range)
@click.option("-A", "--applid", type=str, default=None, help="Specific applid to print.")
@click.option("-x", "--exclude_trans_starts", type=str, default=None, help="Exclude tran id starts with.")
@click.option("-o", "--out", type=click.File('at'), help="File to write the Output to, omit to display on screen.", default=sys.stdout)
def print_110_1(jsonfiles, start_time, end_time, applid, exclude_trans_starts, out) -> None:
    """Print smf110 subtype 1 CICS performance summary report from jsonfile(s)."""
    process_print_command('smf110', out, print_cics_performance_report, jsonfiles, start_time, end_time, applid, exclude_trans_starts)

@click.command("110_2")
@click.argument(
    'jsonfiles',
    type=click.Path(
        exists=True,
        file_okay=True,
        readable=True,
        path_type=Path,
    ),
    required=True,
    nargs=-1)
@click.option("-o", "--out", type=click.File('at'), help="File to write the Output to.", required =True)
@click.option("-s", "--start_time",type=click.DateTime(formats=["%Y-%m-%d %H:%M"]),default="2000-01-01 00:00",help="Start time (YYYY-MM-DD HH:MM)")
@click.option("-e", "--end_time", type=click.DateTime(formats=["%Y-%m-%d %H:%M"]), default=str(datetime.now())[:16], help="End time (YYYY-MM-DD HH:MM)", callback=check_date_range)
@click.option("-A", "--applid", type=str, default=None, help="Specific applid to print.")
def print_110_2(jsonfiles, out, start_time, end_time, applid) -> None:
    """Print smf110 subtype 2 CICS statistics summary report from jsonfile(s)."""
    process_print_command('smf110', out, print_cics_statistics_report, jsonfiles, start_time, end_time, applid)