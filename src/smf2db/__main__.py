# smf2db/__main__.py

"""This module provides the Smf2db CLI."""
import os
import re
from pathlib import Path

import click
import jsonschema

from smf2db import (
    __version__, ERRORS, SUCCESS, DEFAULT_DB_HOST, DEFAULT_DB_PORT, DEFAULT_DB_USER
)
from smf2db.config import ConfigManager
from smf2db.print import commands as print_commands
from smf2db.schemas.schema import schema
from smf2db.sumup import commands as sumup_commands
from smf2db.sumup.commands import init_summary
from smf2db.upload import commands as upload_commands
from smf2db.upload.commands import init_database, validate_config_file, supports_psycopg2, supports_sqlite, \
    supports_sshtunnel, supports_pg8000


@click.group()
@click.version_option(version=__version__)
@click.pass_context
def cli(ctx):
    """A CLI application that upload data to database or print the reports using the JSON files."""
    pass

@cli.group("db")
def db():
    """A CLI application that uploads data to database."""
    pass

@cli.group("report")
def report():
    """Print report from JSON files"""

@db.group("upload")
def upload():
    """Upload JSON files to database"""


@db.group("sumup")
def sumup():
    """Summing up database to 15min, hourly or daily database"""

def required_with_initcfg(ctx, param, db_driver):
    if db_driver == 'psycopg2' and not supports_psycopg2(): #PSYCOPG2_SUPPORT:
        click.secho(
            'Cannot import psycopg2, "psycopg2" package was not found. '
            "Please install smf2db with `pip install smf2db[psycopg2]` if you want psycopg2 support and ensure psycopg2 is supported on this platform.",
            err=True,
            fg="red",
        )
        raise SystemExit(1)
    if db_driver == 'pg8000' and not supports_pg8000(): #PSYCOPG2_SUPPORT:
        click.secho(
            'Cannot import pg8000, "pg8000" package was not found. '
            "Please install smf2db with `pip install smf2db[pg8000]` if you want pg8000 support.",
            err=True,
            fg="red",
        )
        raise SystemExit(1)
    if db_driver == 'sqlite' and not supports_sqlite(): #SQLITE_SUPPORT:
        click.secho(
            'SQLite version need to be above 3.32 to continue the database operation.',
            err=True,
            fg="red",
        )
        raise SystemExit(1)
    if db_driver in ['psycopg2', 'pg8000']:
        host = ctx.params.get("host")
        if not host:
            # ctx.params['host'] = click.prompt('Host address of the database', default=DEFAULT_DB_HOST)
            host_value = click.prompt('Host address of the database', default=DEFAULT_DB_HOST)
            ctx.params["host"] = validate_hostname(ctx, param, host_value)

        port = ctx.params.get("port")
        if not port:
            # ctx.params['port'] = click.prompt('Port number at which the database instance is listening', default=DEFAULT_DB_PORT)
            port_value = click.prompt('Port number at which the database instance is listening',
                                      default=DEFAULT_DB_PORT)
            ctx.params["port"] = validate_port(ctx, param, port_value)

    elif db_driver == 'sqlite':
        sqlite_path = ctx.params.get('sqlite_path')
        if not sqlite_path:
            ctx.params['sqlite_path'] = click.prompt('Sqlite filepath',
                                                         type=click.Path(exists=True, file_okay=False, readable=True))
    return db_driver

def required_with_initdb(ctx, param, smf):
    config_file_path = ctx.params.get('config_file')
    if not config_file_path:
        ctx.params['config_file'] = click.prompt('Config file name', type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True))
        config_file_path = ctx.params.get('config_file')

    config_mgr = ConfigManager(config_file_path)
    cfg = config_mgr.load_config()
    if isinstance(cfg, tuple):
        click.secho(
            'Cannot open config file. '
            "Please run `smf2db db initcfg` to create the config file first before you initialize the database.",
            err=True,
            fg="red",
        )
        raise SystemExit(1)

    # Validate config file
    try:
        jsonschema.validate(cfg, schema=schema)
    except jsonschema.exceptions.ValidationError as ex:
        click.secho(
            f'Invalid config file: {ex} '
            "Please run `smf2db db initcfg` to create the config file first.",
            err=True,
            fg="red",
        )
        raise SystemExit(1)

    db_driver = config_mgr.get('database.driver')
    ssh_host = config_mgr.get('database.ssh_host')
    if ssh_host:
        use_ssh = True
    else:
        use_ssh = False

    if db_driver == 'psycopg2' and not supports_psycopg2():  # PSYCOPG2_SUPPORT:
        click.secho(
            'Cannot import psycopg2, "psycopg2" package was not found. '
            "Please install smf2db with `pip install smf2db[psycopg2]` if you want psycopg2 support and ensure psycopg2 is supported on this platform.",
            err=True,
            fg="red",
        )
        raise SystemExit(1)
    if db_driver == 'pg8000' and not supports_pg8000():  # PSYCOPG2_SUPPORT:
        click.secho(
            'Cannot import pg8000, "pg8000" package was not found. '
            "Please install smf2db with `pip install smf2db[pg8000]` if you want pg8000 support.",
            err=True,
            fg="red",
        )
        raise SystemExit(1)
    if db_driver == 'sqlite' and not supports_sqlite():
        click.secho(
            'SQLite version need to be above 3.32 to continue the database operation.',
            err=True,
            fg="red",
        )
        raise SystemExit(1)
    if use_ssh and not supports_sshtunnel():
        click.secho(
            'Cannot open SSH tunnel, "sshtunnel" package was not found. '
            "Please install smf2db with `pip install smf2db[sshtunnel]` if you want SSH tunnel support and SSH tunnel is supported on this platform.",
            err=True,
            fg="red",
        )
        raise SystemExit(1)

    if 'psycopg2' in db_driver or 'pg8000' in db_driver:
        user = ctx.params.get('username')
        if not user:
            ctx.params['username'] = click.prompt('Username to connect to the database.', default=DEFAULT_DB_USER)

        password = ctx.params.get('password')
        if not password:
            ctx.params['password'] = click.prompt('Password to connect to the database', hide_input=True,)

    if ('psycopg2' in db_driver or 'pg8000' in db_driver) and use_ssh:
        user = ctx.params.get('ssh_user')
        if not user:
            ctx.params["ssh_user"] = click.prompt('SSH User')

        password = ctx.params.get('ssh_password')
        if not password:
            ctx.params["ssh_password"] = click.prompt('SSH Password', hide_input=True)

    return smf

def prompt_ssh_with_initcfg(ctx, param, ssh):
    if ssh and not supports_sshtunnel(): #SSH_TUNNEL_SUPPORT:
        click.secho(
            'Cannot open SSH tunnel, "sshtunnel" package was not found. '
            "Please install smf2db with `pip install smf2db[sshtunnel]` if you want SSH tunnel support and SSH tunnel is supported on this platform.",
            err=True,
            fg="red",
        )
        raise SystemExit(1)

    if ctx.params.get("db_driver") != 'sqlite' and ssh:
        host = ctx.params.get("ssh_host")
        if not host:
            # ctx.params["ssh_host"] = click.prompt("SSH Host")
            ssh_host_value = click.prompt("SSH Host")
            ctx.params["ssh_host"] = validate_hostname(ctx, param, ssh_host_value)

        port = ctx.params.get("ssh_port")
        if not port:
            # ctx.params["ssh_port"] = click.prompt("SSH Port", default="")
            ctx.params["ssh_port"] = None

    elif ctx.params.get("db_driver") == 'sqlite' and ssh:
        raise click.BadParameter("--ssh is not supported using sqlite.")

    return ssh


def validate_hostname(ctx, param, value):
    """
    Validate hostname according to RFC 1035
    - Maximum length: 255 characters
    - Labels separated by dots
    - Each label: 1-63 characters
    - Labels can contain letters, digits, hyphens
    - Labels cannot start or end with hyphen
    """
    if value:
        if len(value) > 255:
            raise click.BadParameter("Host name too long.")

        # Remove trailing dot if present
        if value[-1] == ".":
            value = value[:-1]

        # Check each label
        allowed = re.compile(r"(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
        result = all(allowed.match(x) for x in value.split("."))
        if not result:
            raise click.BadParameter("Host name invalid.")
        else:
            return value
    else:
        return value


def validate_port(ctx, param, value):
    if value:
        if isinstance(value, int) and 0 < value <= 65535:
            return value
        try:
            if value[:2].lower() == "0x":
                return int(value[2:], 16)
            elif value[:1] == "0":
                return int(value, 8)
            return int(value, 10)
        except ValueError:
            raise click.BadParameter("Port number invalid.")
    return value

def validate_filename(ctx, param, value: os.PathLike):
    # Define a regular expression pattern to match forbidden characters
    if Path(value).suffix != '.yaml':
        raise click.BadParameter("Filename must be a YAML file.")
    filename = Path(value).stem
    ILLEGAL_NTFS_CHARS = r'[<>:/\\|?*\"]|[\0-\31]'
    # Define a list of forbidden names
    FORBIDDEN_NAMES = ['CON', 'PRN', 'AUX', 'NUL',
                       'COM1', 'COM2', 'COM3', 'COM4', 'COM5',
                       'COM6', 'COM7', 'COM8', 'COM9',
                       'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5',
                       'LPT6', 'LPT7', 'LPT8', 'LPT9']
    # Check for forbidden characters
    match = re.search(ILLEGAL_NTFS_CHARS, filename)
    if match:
        raise click.BadParameter(
            f"Invalid character '{match[0]}' for filename {filename}.")
    # Check for forbidden names
    if filename.upper() in FORBIDDEN_NAMES:
        click.BadParameter(f"{filename} is a reserved folder name.")
    # Check for empty name (disallowed in Windows)
    if filename.strip() == "":
        raise click.BadParameter("Empty file name not allowed.")
    # Check for names starting or ending with dot or space
    match = re.match(r'^[. ]|.*[. ]$', filename)
    if match:
        raise click.BadParameter(
            f"Invalid start or end character ('{match[0]}')"
            f" in file name {filename}"
        )
    return value

def validate_dbname(ctx, param, value):
    if value:
        if len(value) > 50:
            raise click.BadParameter("Db prefix cannot be longer than 50 characters.")

        result = re.fullmatch(r"[A-Za-z0-9_]+", value) is not None
        if not result:
            raise click.BadParameter("Invalid character(s). Only alphanumeric characters and underscore are allowed.")
        else:
            return value
    else:
        return value

@db.command()
@click.option("--config_file", prompt="Configuration file name", required=True, prompt_required=False,
              type=click.Path(file_okay=True, dir_okay=False, readable=True), callback=validate_filename)
@click.option("--db_driver", default="sqlite", prompt="Database driver", help="Database driver",
              required=True, prompt_required=False, type=click.Choice(["sqlite", "psycopg2", "pg8000"]),
              callback=required_with_initcfg)
@click.option("-x", "--db_prefix", default="", prompt="Database prefix", required=True, prompt_required=False,
              help="Database prefix(e.g. db_ will create database db_smf30)", callback=validate_dbname)
@click.option("--partitions", default="no partition", prompt="Database partition scheme", required=True, prompt_required=False,
              help="Database partition scheme", type=click.Choice(["no partition", "weekday", "day of month", "week number"]))
@click.option("-h", "--host", is_eager=True, default=None, help="Host address of the database.", callback=validate_hostname)
@click.option("-p", "--port", is_eager=True, default=None, callback=validate_port,
              help="Port number at which the database instance is listening.")
@click.option('--ssh', is_flag=True, default=False, callback=prompt_ssh_with_initcfg,
              help="Use SSH connection.")
@click.option("--sqlite_path", is_eager=True, type=click.Path(exists=True, file_okay=False, readable=True),
              default=None, help="Path to sqlite file")
@click.option('--ssh_host', is_eager=True, default=None, help="SSH host", callback=validate_hostname)
@click.option('--ssh_port', is_eager=True, default=None, required=False, callback=validate_port,
              help="SSH port")
def initcfg(config_file: os.PathLike, host: str, port: str, db_prefix: str, ssh: bool, ssh_host: str = None,
            ssh_port: str = None, db_driver: str = 'sqlite', partitions: str = 'weekday', sqlite_path: str = '') -> int:
    """Initialize the configuration file."""
    predefined_smf_list = ['smf', '30', '70', '71', '72', '73', '74', '75', '77', '78', '110_1', '110_2', '123']
    partitions_scheme_dict = {'no partition': 'single', 'weekday': 'weekday', 'day of month': 'day',
                              'week number': 'week'}
    partition_scheme = partitions_scheme_dict[partitions]

    config_mgr = ConfigManager(config_file)
    cfg = config_mgr.load_config()
    if not isinstance(cfg, tuple):
        click.confirm(
            'This config file is already exist and it will be overwritten. If there is any inconsistent databases exist. they may be deleted. Do you want to continue?',
            abort=True)

    smf_feature_list = []

    for smf_type in predefined_smf_list:
        if smf_type != 'smf':
            if smf_type in ['110_1', '110_2']:
                schema = 'smf110'
            else:
                schema = f'smf{smf_type}'
            smf = {'type': smf_type,
                   'enabled': False,
                   'dbname': f'{db_prefix}smf{smf_type}',
                   'schema': schema,
                   'summary': {'15min': False, 'hourly': False, 'daily': False}
                   }
        else:
            smf = {'type': smf_type,
                   'enabled': True,
                   'dbname': f'{db_prefix}{smf_type}',
                   'schema': f'{smf_type}',
                   'summary': {'15min': False, 'hourly': False, 'daily': False}
                   }
        smf_feature_list.append(smf)
    if db_driver != 'sqlite':
        db_driver = f'postgresql+{db_driver}'

    app_config = {
        'database': {
            'host': host,
            'port': port,
            'ssh_host': ssh_host,
            'ssh_port': ssh_port,
            'driver': db_driver,
            'partition_scheme': partition_scheme,
            'sqlite_path': sqlite_path
            },
        'smf': smf_feature_list
    }

    # Write to file
    config_mgr.save_config(app_config)
    return SUCCESS


@db.command()
@click.argument("smf",
                callback=required_with_initdb,
                nargs=-1,
                required=True,
                type=click.Choice(['30', '70', '71', '72', '73', '74', '75', '77', '78', '110_1', '110_2', '123']))
@click.option("--config_file", required=True, type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True), callback=validate_config_file)
@click.option("-U", "--username", is_eager=True, default=None, help="Username to connect to the database.")
@click.option("-W", "--password", is_eager=True, default=None, help="Force password prompt.")
@click.option('--ssh_user', is_eager=True, default=None, help="SSH user")
@click.option('--ssh_password', is_eager=True, default=None, help="SSH password")
def initdb(smf: list, config_file: Path, username: str, password: str,
           ssh_user=None, ssh_password=None) -> None:
    """Initialize the smf2db database."""
    config_mgr = ConfigManager(config_file)
    cfg = config_mgr.load_config()

    smf_feature_list = cfg['smf']
    smf_70_feature = {}
    for smf_feature in smf_feature_list:
        if smf_feature['type'] == '70':
            smf_70_feature = smf_feature
            break

    if '70' not in smf and not smf_70_feature['enabled']:
        for smf_type in smf:
            if smf_type.startswith('7') or smf_type.startswith('3'):
                click.secho(
                    '70 is the prerequisite of all other 7x and 30 smf types. '
                    "Please initialize 70 first by running `smf2db db initdb 70` before you initialize other 7x or 30 databases.",
                    err=True,
                    fg="red",
                )
                raise SystemExit(1)

    if config_mgr.get('database.driver') == 'sqlite':
        # Valid its path is a valid path
        if not Path(config_mgr.get('database.sqlite_path')).exists():
            click.secho(f"The database path {config_mgr.get('database.sqlite_path')} does not exist. Please create it.", err=True, fg="red")
            raise SystemExit(1)


    db_list = []
    partitions_scheme = config_mgr.get('database.partition_scheme')
    if partitions_scheme == 'weekday':
        partitions = range(1, 8)
    elif partitions_scheme == 'day':
        partitions = range(1, 32)
    elif partitions_scheme == 'week':
        partitions = range(1, 53)
    else:
        partitions = range(1, 2)

    for smf_feature in smf_feature_list:
        if smf_feature['type'] in smf:
            original_status = smf_feature['enabled']
            smf_feature['enabled'] = True
            dbname_prefix = smf_feature['dbname']
            for part in partitions:
                db_list.append(f"{smf_feature['dbname']}_{part}")
            if original_status:
                click.confirm(f"This smf {smf_feature['type']} is already enabled. The database(s) with prefix {dbname_prefix} will be dropped if exist and recreated. Do you want to continue?", abort=True)


    if len(db_list) > 0:
        click.confirm(f'The following databases will be created:\n {", ".join(db_list)}.\n Do you want to continue?', abort=True)

        cfg['smf'] = smf_feature_list
        # Write to file
        config_mgr.save_config(cfg)

        for smf_type in smf:
            db_init_error = init_database(smf_type, config_file, username, password, ssh_user, ssh_password)
            if db_init_error:
                print('Database initialization failed.')
                click.echo(f'Creating database for {smf_type} failed with "{ERRORS[db_init_error]}"')
                raise SystemExit(1)
            else:
                click.echo(f"The required databases for {smf_type} have been created")
    else:
        click.echo('No databases were created.')

@db.command()
@click.argument("smf", callback=required_with_initdb,
              type=click.Choice(['30', '70', '71', '72', '73', '74', '75', '77', '78', '110_1', '110_2', '123']))
@click.argument(
    "summary",
    type=click.Choice(['15min', 'hourly', 'daily']),
    nargs=-1,
    required=True,
)
@click.option("--config_file", required=True, type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True), callback=validate_config_file)
@click.option("-U", "--username", is_eager=True, default=None, help="Username to connect to the database.")
@click.option("-W", "--password", is_eager=True, default=None, help="Force password prompt.")
@click.option('--ssh_user', is_eager=True, default=None, help="SSH user")
@click.option('--ssh_password', is_eager=True, default=None, help="SSH password")
def initsum(smf: str, config_file: Path, summary: list, username: str, password: str,
           ssh_user=None, ssh_password=None) -> None:
    """Initialize the smf2db database for summarization."""
    config_mgr = ConfigManager(config_file)
    cfg = config_mgr.load_config()
    if isinstance(cfg, tuple):
        click.secho(
            'Cannot open config file. '
            "Please run `smf2db db initcfg` to create the config file first before you initialize the database.",
            err=True,
            fg="red",
        )
        raise SystemExit(1)
    if config_mgr.get('database.driver') == 'sqlite':
        # Valid its path is a valid path
        if not Path(config_mgr.get('database.sqlite_path')).exists():
            click.secho(f"The database path {config_mgr.get('database.sqlite_path')} does not exist. Please create it.", err=True, fg="red")
            raise SystemExit(1)

    smf_feature_list = cfg['smf']
    target_feature = None
    summary_db = {'15min': '15m', 'hourly': 'hr', 'daily': 'da'}
    for smf_feature in smf_feature_list:
        if smf_feature['type'] == smf:
            target_feature = smf_feature
            break

    if not target_feature['enabled']:
        click.secho(
            'This smf type is not enabled. '
            "Please initialize the db first by running `smf2db db initdb` before enable the summary databases.",
            err=True,
            fg="red",
        )
        raise SystemExit(1)

    if smf.startswith('7') or smf.startswith('3'):
        if '15min' in summary:
            click.secho(
                '15min summary level is not supported for all 7x and 30 databases. Please try again without 15min summary level.',
                err=True,
                fg="red",
            )
            raise SystemExit(1)
    db_list = []
    db_name_prefix = target_feature['dbname']
    confirmed = False
    for smf_feature in smf_feature_list:
        if smf_feature['type'] == smf:
            for summary_level in smf_feature['summary']:
                if summary_level in summary:
                    db_list.append(f"{db_name_prefix}_{summary_db[summary_level]}")
                    if smf_feature['summary'][summary_level]:
                        confirmed = True
                        click.confirm(
                            f'The summary level `{summary_level}` for this smf type is already enabled. The database {db_name_prefix}_{summary_db[summary_level]} will be dropped if exist and recreated. Do you want to continue?',
                            abort=True)
                    smf_feature['summary'][summary_level] = True
            break
    if not confirmed:
        click.confirm(
            f'The following database(s) will be dropped if exist and recreated:\n {", ".join(db_list)}.\n Do you want to continue?',
            abort=True)

    cfg['smf'] = smf_feature_list
    # Write to file
    config_mgr.save_config(cfg)

    db_init_error = init_summary(smf, config_file, summary, username, password, ssh_user, ssh_password)
    if db_init_error:
        click.echo(f'Creating summary database for {smf} failed with "{ERRORS[db_init_error]}"')
        raise SystemExit(1)
    else:
        click.echo(f"The required summary databases for {smf} have been created")

upload.add_command(upload_commands.upload_30)
upload.add_command(upload_commands.upload_70)
upload.add_command(upload_commands.upload_71)
upload.add_command(upload_commands.upload_72)
upload.add_command(upload_commands.upload_73)
upload.add_command(upload_commands.upload_74)
upload.add_command(upload_commands.upload_75)
upload.add_command(upload_commands.upload_77)
upload.add_command(upload_commands.upload_78)
upload.add_command(upload_commands.upload_123)
upload.add_command(upload_commands.upload_110_1)
upload.add_command(upload_commands.upload_110_2)

report.add_command(print_commands.print_30)
report.add_command(print_commands.print_70)
report.add_command(print_commands.print_71)
report.add_command(print_commands.print_72)
report.add_command(print_commands.print_73)
report.add_command(print_commands.print_74)
report.add_command(print_commands.print_75)
report.add_command(print_commands.print_77)
report.add_command(print_commands.print_78)
report.add_command(print_commands.print_123)
report.add_command(print_commands.print_110_1)
report.add_command(print_commands.print_110_2)

sumup.add_command(sumup_commands.sum_30)
sumup.add_command(sumup_commands.sum_70)
sumup.add_command(sumup_commands.sum_71)
sumup.add_command(sumup_commands.sum_72)
sumup.add_command(sumup_commands.sum_73)
sumup.add_command(sumup_commands.sum_74)
sumup.add_command(sumup_commands.sum_75)
sumup.add_command(sumup_commands.sum_77)
sumup.add_command(sumup_commands.sum_78)
sumup.add_command(sumup_commands.sum_123)
sumup.add_command(sumup_commands.sum_110_1)
sumup.add_command(sumup_commands.sum_110_2)
