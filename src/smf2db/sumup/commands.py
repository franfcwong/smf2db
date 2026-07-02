import datetime as dt
import os
import platform
from collections.abc import Callable
from pathlib import Path

import click
import jsonschema
import sqlalchemy
from rich.progress import Progress, SpinnerColumn, TextColumn
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.ext.horizontal_shard import ShardedSession
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import Insert
from sqlalchemy.sql import operators
from sqlalchemy.sql import visitors

from smf2db import ERRORS, DB_WRITE_ERROR, SUCCESS, DB_CONNECTION_ERROR, DEFAULT_DB_HOST
from smf2db.api.api_1101db_sum import sum_1101db
from smf2db.api.api_1102db_sum import sum_1102db
from smf2db.api.api_123db_sum import sum_123db
from smf2db.api.api_30db_sum import sum_30db
from smf2db.api.api_70db_sum import sum_70db
from smf2db.api.api_71db_sum import sum_71db
from smf2db.api.api_72db_sum import sum_72db
from smf2db.api.api_73db_sum import sum_73db
from smf2db.api.api_74db_sum import sum_74db
from smf2db.api.api_75db_sum import sum_75db
from smf2db.api.api_77db_sum import sum_77db
from smf2db.api.api_78db_sum import sum_78db
from smf2db.config import ConfigManager
from smf2db.db_models.smf1101_base import Base110115m, Base1101Hr, Base1101Da
from smf2db.db_models.smf123_base import Base12315m, Base123Hr, Base123Da
from smf2db.db_models.smf1102_base import Base1102Hr, Base1102Da
from smf2db.db_models.smf30_base import Base30Hr, Base30Da
from smf2db.db_models.smf70_base import Base70Hr, Base70Da
from smf2db.db_models.smf71_base import Base71Hr, Base71Da
from smf2db.db_models.smf72_base import Base72Hr, Base72Da
from smf2db.db_models.smf73_base import Base73Hr, Base73Da
from smf2db.db_models.smf74_base import Base74Hr, Base74Da
from smf2db.db_models.smf75_base import Base75Hr, Base75Da
from smf2db.db_models.smf77_base import Base77Hr, Base77Da
from smf2db.db_models.smf78_base import Base78Hr, Base78Da
from smf2db.db_models.smf7x_model import SmfCpc, SmfLpar
from smf2db.schemas.schema import schema
from smf2db.upload.commands import validate_config_file, sqlite_execution_options, supports_sshtunnel

summary_db = {'15min': '15m', 'hourly': 'hr', 'daily': 'da'}
summary_base = {
    '15min': {
        '110_1': Base110115m,
        '123': Base12315m
    },
    'hourly': {
        '30': Base30Hr,
        '70': Base70Hr,
        '71': Base71Hr,
        '72': Base72Hr,
        '73': Base73Hr,
        '74': Base74Hr,
        '75': Base75Hr,
        '77': Base77Hr,
        '78': Base78Hr,
        '110_1': Base1101Hr,
        '110_2': Base1102Hr,
        '123': Base123Hr,
    },
    'daily': {
        '30': Base30Da,
        '70': Base70Da,
        '71': Base71Da,
        '72': Base72Da,
        '73': Base73Da,
        '74': Base74Da,
        '75': Base75Da,
        '77': Base77Da,
        '78': Base78Da,
        '110_1': Base1101Da,
        '110_2': Base1102Da,
        '123': Base123Da,
    }

}

def get_engines_for_port(config_mgr: ConfigManager, user, password, port, use_ssh):
    engines = {}

    partitions_scheme = config_mgr.get('database.partition_scheme')
    if partitions_scheme == 'weekday':
        partitions = range(1, 8)
    elif partitions_scheme == 'day':
        partitions = range(1, 32)
    elif partitions_scheme == 'week':
        partitions = range(1, 53)
    else:
        partitions = range(1, 2)

    if not use_ssh:
        for smf in config_mgr.get('smf'):
            if smf['type'] != 'smf' and smf['enabled']:
                for part in partitions:
                    if config_mgr.get('database.driver') != 'sqlite':
                        engines[f"{smf['type']}.{part}"] = create_engine(
                            f"{config_mgr.get('database.driver')}://{user}:{password}@{config_mgr.get('database.host')}:{port}/{smf['dbname']}_{part}",
                            isolation_level="AUTOCOMMIT",
                        )
                    else:
                        full_path = os.path.join(config_mgr.get('database.sqlite_path'), f"{smf['dbname']}_{part}.db")
                        sqlite_path = f"sqlite:///{full_path}"

                        engines[f"{smf['type']}.{part}"] = create_engine(sqlite_path, execution_options=sqlite_execution_options)
                for summary_level in smf['summary']:
                    if summary_level:
                        if config_mgr.get('database.driver') != 'sqlite':
                            engines[f"{smf['type']}.{summary_level}"] = create_engine(
                                f"{config_mgr.get('database.driver')}://{user}:{password}@{config_mgr.get('database.host')}:{port}/{smf['dbname']}_{summary_db[summary_level]}",
                                isolation_level="AUTOCOMMIT",
                            )
                        else:
                            full_path = os.path.join(config_mgr.get('database.sqlite_path'),
                                                     f"{smf['dbname']}_{summary_db[summary_level]}.db")
                            sqlite_path = f"sqlite:///{full_path}"
                            engines[f"{smf['type']}.{summary_level}"] = create_engine(
                                sqlite_path, execution_options=sqlite_execution_options)

            elif smf['type'] == 'smf':
                if config_mgr.get('database.driver') != 'sqlite':
                    engines[f"{smf['type']}.0"] = create_engine(
                        f"{config_mgr.get('database.driver')}://{user}:{password}@{config_mgr.get('database.host')}:{port}/{smf['dbname']}",
                        isolation_level="AUTOCOMMIT",
                    )
                else:
                    full_path = os.path.join(config_mgr.get('database.sqlite_path'),
                                             f"{smf['dbname']}.db")
                    sqlite_path = f"sqlite:///{full_path}"
                    engines[f"{smf['type']}.0"] = create_engine(sqlite_path, execution_options=sqlite_execution_options)
    else: # Not sqlite
        for smf in config_mgr.get('smf'):
            if smf['type'] != 'smf' and smf['enabled']:
                engines[smf['type']] = {}
                for part in partitions:
                    engines[f"{smf['type']}.{part}"] = create_engine(
                        f"{config_mgr.get('database.driver')}://{user}:{password}@{DEFAULT_DB_HOST}:{port}/{smf['dbname']}_{part}",
                        isolation_level="AUTOCOMMIT",
                    )
                for summary_level in smf['summary']:
                    if summary_level:
                        engines[f"{smf['type']}.{summary_level}"] = create_engine(
                            f"{config_mgr.get('database.driver')}://{user}:{password}@{DEFAULT_DB_HOST}:{port}/{smf['dbname']}_{summary_db[summary_level]}",
                            isolation_level="AUTOCOMMIT",
                        )
            elif smf['type'] == 'smf':
                engines[f"{smf['type']}.0"] = create_engine(
                    f"{config_mgr.get('database.driver')}://{user}:{password}@{DEFAULT_DB_HOST}:{port}/{smf['dbname']}",
                    isolation_level="AUTOCOMMIT",
                )
    return engines

def with_sql_session(config_mgr: ConfigManager, smf_type, user, password, port, use_ssh=False):
    # inner function
    def shard_lookup(target_date: dt.date) -> str:
        if config_mgr.get('database.partition_scheme') == 'weekday':
            return f"{smf_type}.{target_date.isoweekday()}"
        elif config_mgr.get('database.partition_scheme') == 'day':
            return f"{smf_type}.{target_date.day}"
        elif config_mgr.get('database.partition_scheme') == 'week':
            return f"{smf_type}.{target_date.isocalendar().week}"
        elif config_mgr.get('database.partition_scheme') == 'single':
            return f"{smf_type}.1"
        else:
            return 'smf.0'

    def shard_chooser(mapper, instance, clause=None):
        if isinstance(instance, (SmfCpc, SmfLpar)):
            return 'smf.0'
        elif hasattr(instance, 'datetime'):
            return shard_lookup(instance.datetime.date())
        elif hasattr(instance, 'date'):
            return shard_lookup(instance.date)
        elif hasattr(instance, 'start_interval'):
            return shard_lookup(instance.start_interval.date())
        else:
            print('Unrecognized instance: ', instance)
            return 'smf.0'

    def identity_chooser(mapper, primary_key, *, lazy_loaded_from, **kw):
        if lazy_loaded_from:
            return [lazy_loaded_from.identity_token]
        else:
            target_key = next((v for i, v in enumerate(primary_key) if isinstance(v, dt.datetime)), None)
            if target_key:
                if config_mgr.get('database.partition_scheme') == 'weekday':
                    return [f'{smf_type}.{target_key.isoweekday()}']
                elif config_mgr.get('database.partition_scheme') == 'day':
                    return [f'{smf_type}.{target_key.day}']
                elif config_mgr.get('database.partition_scheme') == 'week':
                    return [f'{smf_type}.{target_key.isocalendar().week}']
                elif config_mgr.get('database.partition_scheme') == 'single':
                    return [f'{smf_type}.1']
                else:
                    return ['smf.0']
            else:
                return ['smf.0']

    def execute_chooser(context):
        ids = []
        if config_mgr.get('database.partition_scheme') == 'weekday':
            partitions_range = range(1, 8)
        elif config_mgr.get('database.partition_scheme') == 'day':
            partitions_range = range(1, 32)
        elif config_mgr.get('database.partition_scheme') == 'week':
            partitions_range = range(1, 53)
        else:
            partitions_range = range(1, 2)
        for column, operator, value in _get_select_comparisons(context.statement):
            if isinstance(column, dt.datetime):
                if operator == operators.eq:
                    ids.append(shard_lookup(value.date()))
                elif operator == operators.in_op:
                    ids.extend(shard_lookup(v.date()) for v in value)

        if len(ids) == 0:
            return [f'{smf_type}.{part}' for part in partitions_range]
            # return list(partitions_range)
        else:
            return ids

    def _get_select_comparisons(statement):
        binds = {}
        clauses = set()
        comparisons = []
        def visit_bindparam(bind):
            value = bind.effective_value
            binds[bind] = value

        def visit_column(column):
            clauses.add(column)

        def visit_binary(binary):
            if binary.left in clauses and binary.right in binds:
                comparisons.append(
                    (binary.left, binary.operator, binds[binary.right])
                )

            elif binary.left in binds and binary.right in clauses:
                comparisons.append(
                    (binary.right, binary.operator, binds[binary.left])
                )

        if not isinstance(statement, Insert) and statement.whereclause is not None:
            visitors.traverse(
                statement.whereclause,
                {},
                {
                    "bindparam": visit_bindparam,
                    "binary": visit_binary,
                    "column": visit_column,
                },
            )
        return comparisons

    partitions_scheme = config_mgr.get('database.partition_scheme')
    if partitions_scheme == 'weekday':
        partitions = range(1, 8)
    elif partitions_scheme == 'day':
        partitions = range(1, 32)
    elif partitions_scheme == 'week':
        partitions = range(1, 53)
    else:
        partitions = range(1, 2)

    engines = get_engines_for_port(config_mgr, user, password, port, use_ssh)
    session = scoped_session(sessionmaker(class_=ShardedSession,
                                          shards=engines,))

    session.configure(
        shard_chooser=shard_chooser,
        identity_chooser=identity_chooser,
        execute_chooser=execute_chooser,)
    return session(), engines


def get_database_url(config_mgr: ConfigManager, db_user: str, db_password: str, db_port: str, dbname: str) -> str:
    """Return the current path to the smf2db database."""
    if platform.system() != "OS/390" and config_mgr.get('database.ssh_host') is not None:
        return f"{config_mgr.get('database.driver')}://{db_user}:{db_password}@{DEFAULT_DB_HOST}:{db_port}/{dbname}"
    else:
        return f"{config_mgr.get('database.driver')}://{db_user}:{db_password}@{config_mgr.get('database.host')}:{config_mgr.get('database.port')}/{dbname}"


def init_summary(smf_type, config_file: Path, summary_list: list, db_user: str, db_password: str,
                 ssh_user: str, ssh_password: str) -> int:
    """Create the summary database for a specific smf_type."""

    config_mgr = ConfigManager(config_file)
    result = config_mgr.load_config()
    if not isinstance(result, tuple):
        db_host = config_mgr.get('database.host')
        db_port = config_mgr.get('database.port')
        db_driver = config_mgr.get('database.driver')
        ssh_host = config_mgr.get('database.ssh_host')
        ssh_port = config_mgr.get('database.ssh_port')
        if ssh_host is not None:
            use_ssh = True
        else:
            use_ssh = False

        if use_ssh and not supports_sshtunnel():
            click.secho(
                'Cannot open SSH tunnel, "sshtunnel" package was not found. '
                "Please install smf2db with `pip install smf2db[sshtunnel]` if you want SSH tunnel support and SSH tunnel is supported on this platform.",
                err=True,
                fg="red",
            )
            raise SystemExit(1)

        if db_driver != 'sqlite' and use_ssh and ssh_host is not None:
            if ssh_port is None:
                ssh_address_or_host = (ssh_host)
            else:
                ssh_address_or_host = (ssh_host, ssh_port)
            try:
                import sshtunnel
                with sshtunnel.SSHTunnelForwarder(
                        ssh_address_or_host=ssh_address_or_host,
                        ssh_username=ssh_user,
                        ssh_password=ssh_password,
                        # ssh_pkey=ssh_private_key_path,
                        # ssh_private_key_password=ssh_private_key_password,
                        remote_bind_address=(db_host, db_port),
                ) as tunnel:
                    if tunnel is not None:
                        tunnel.start()
                        print(f"TunnelIsUp: {tunnel.tunnel_is_up} | {tunnel.local_bind_address}")
                        db_port = tunnel.local_bind_port
                        db_url = get_database_url(config_mgr, db_user, db_password, db_port, 'postgres')
                        engine = create_engine(db_url, isolation_level="AUTOCOMMIT")
                        result = create_pg_summary(smf_type, config_mgr, summary_list, engine, db_user, db_password, db_port)
                    else:
                        click.secho(
                            f"Unable to establish SSH tunnel. Please verify your SSH setting and userid/password are correct.",
                            err=True,
                            fg="red")
                        return DB_CONNECTION_ERROR
            except Exception as e:
                click.secho(
                    f"Unable to establish SSH tunnel. Please verify your SSH setting and userid/password are correct: {e}",
                    err=True,
                    fg="red")
                raise DB_CONNECTION_ERROR
        elif db_driver != 'sqlite':
            db_url = get_database_url(config_mgr, db_user, db_password, db_port, 'postgres')
            engine = create_engine(db_url, isolation_level="AUTOCOMMIT")
            result = create_pg_summary(smf_type, config_mgr, summary_list, engine, db_user, db_password, db_port)
        else:
            result = create_sqlite_summary(smf_type, config_mgr, summary_list)
    return result

def create_pg_summary(smf_type, config_mgr: ConfigManager, summary_list, engine, db_user, db_password, db_port):
    """Create summary databases and tables for target smf_type if not exists"""
    try:
        with engine.connect() as conn:
            for smf in config_mgr.get('smf'):
                if smf['type'] == smf_type and smf['enabled']:
                    for summary_level in smf['summary']:
                        if summary_level in summary_list:
                            if smf['summary'][summary_level]:
                                print(f"Creating databases for {smf_type} with summary level: {summary_level}")
                                cursor = conn.execute(
                                    text(f"SELECT 1 FROM pg_database WHERE datname = '{smf['dbname']}_{summary_db[summary_level]}'"))
                                if not cursor.fetchone():
                                    conn.execute(text(f"CREATE DATABASE {smf['dbname']}_{summary_db[summary_level]}"))
                                    print(f"'Database {smf['dbname']}_{summary_db[summary_level]} created successfully.'")
                                else: # drop and recreate the database
                                    print(f"Database {smf['dbname']}_{summary_db[summary_level]} already exists")
                                    # Check for active connections
                                    cursor = conn.execute(
                                        text(f"SELECT * from pg_stat_activity where datname = '{smf['dbname']}_{summary_db[summary_level]}'"))
                                    active_connections = cursor.fetchall()
                                    if not active_connections:
                                        # Drop the database
                                        conn.execute(text(f"DROP DATABASE {smf['dbname']}_{summary_db[summary_level]}"))
                                        print(f"Database {smf['dbname']}_{summary_db[summary_level]} dropped successfully.")
                                    else:
                                        click.secho(f"Cannot drop {smf['dbname']}_{summary_db[summary_level]} database; active connectionss exist.",
                                                    err=True,
                                                    fg="red", )
                                        raise SystemExit(1)
                                    conn.execute(text(f"CREATE DATABASE {smf['dbname']}_{summary_db[summary_level]}"))
                                    print(f"Database {smf['dbname']}_{summary_db[summary_level]} created successfully.")
                    break
    except Exception as e:
        print(f"Exception occurred: {e}")
        return DB_CONNECTION_ERROR

    try:
        for smf in config_mgr.get('smf'):
            if smf['type'] == smf_type and smf['enabled']:
                for summary_level in smf['summary']:
                    if summary_level in summary_list:
                        if smf['summary'][summary_level]:
                            connectable = create_engine(get_database_url(config_mgr, db_user, db_password, db_port, f"{smf['dbname']}_{summary_db[summary_level]}"))

                            with connectable.connect() as connection:
                                if not isinstance(smf['schema'], list):
                                    if not inspect(connection).has_schema(smf['schema']):
                                        connection.execute(sqlalchemy.schema.CreateSchema(smf['schema']))
                                        connection.commit()
                                else:
                                    for schema in smf['schema']:
                                        if not inspect(connection).has_schema(schema):
                                            connection.execute(sqlalchemy.schema.CreateSchema(schema))
                                            connection.commit()
                            db_engine = create_engine(
                                get_database_url(config_mgr, db_user, db_password, db_port, f"{smf['dbname']}_{summary_db[summary_level]}"))
                            summary_base[summary_level][smf['type']].metadata.drop_all(db_engine)
                            summary_base[summary_level][smf['type']].metadata.create_all(db_engine)

        return SUCCESS
    except OSError as e:
        print(f"OS Exception occurred: {e}")
        return DB_WRITE_ERROR
    except Exception as e:
        print(f"Exception occurred: {e}")
        return DB_CONNECTION_ERROR

def create_sqlite_summary(smf_type, config_mgr: ConfigManager, summary_list):
    """Create sqlite summary databases and tables if not exists"""
    try:
        for smf in config_mgr.get('smf'):
            if smf['type'] == smf_type and smf['enabled']:
                for summary_level in smf['summary']:
                    if summary_level in summary_list:
                        if smf['summary'][summary_level]:
                            print(f"Creating databases for {smf_type} with summary level: {summary_level}")
                            full_path = os.path.join(config_mgr.get('database.sqlite_path'),
                                                     f"{smf['dbname']}_{summary_db[summary_level]}.db")
                            sqlite_path = f"sqlite:///{full_path}"
                            if Path(full_path).exists():
                                os.remove(full_path)
                                print(f"Database {smf['dbname']}_{summary_db[summary_level]} dropped successfully.")
                            db_engine = create_engine(sqlite_path, execution_options=sqlite_execution_options)
                            # summary_base[summary_level][smf['type']].metadata.drop_all(db_engine)
                            summary_base[summary_level][smf['type']].metadata.create_all(db_engine)
                            print(f"Database {smf['dbname']}_{summary_db[summary_level]} created successfully.")

        return SUCCESS
    except OSError as e:
        print(f"OS Exception occurred: {e}")
        return DB_WRITE_ERROR


def check_database_existence(config_mgr: ConfigManager, smf_type, db_user, db_password, db_port) -> bool:
    db_found = False
    dbname = ""
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

    for smf in config_mgr.get('smf'):
        if smf['type'] == smf_type:
            if smf_type != 'smf':
                for part in partitions:
                    dbname = f"{smf['dbname']}_{part}" # Get the partition db name
                    db_list.append(dbname)
                for summary_level in smf['summary']:
                    if smf['summary'][summary_level]:
                        dbname = f"{smf['dbname']}_{summary_db[summary_level]}"
                        db_list.append(dbname)
            else:
                dbname = f"{smf['dbname']}"
                db_list.append(dbname)
            db_found = True
            break
    if db_found:
        if config_mgr.get('database.driver') != 'sqlite':
            db_url = get_database_url(config_mgr, db_user, db_password, db_port, 'postgres')
            engine = create_engine(db_url)
            try:
                conn = engine.connect()
                for db in db_list:
                    query = f"SELECT datname FROM pg_catalog.pg_database WHERE datname = '{db}'"
                    rows = conn.execute(text(query))
                    data = rows.fetchall()
                    if len(data) == 0:
                        click.echo(
                            f"\nDatabase {db} not found. Please run `smf2db db initdb` or `smf2db db initsum` to create it first.")
                        raise SystemExit(1)
            except Exception as error:
                click.echo(
                    f"\nDatabase connection error: {error}.")
                raise SystemExit(1)

        else:
            for db in db_list:
                sqlite_path = Path(os.path.join(config_mgr.get('database.sqlite_path'), f"{db}.db"))
                if not sqlite_path.exists():
                    click.echo(
                        f"\nDatabase {db} not found. Please run `smf2db db initdb` or `smf2db db initsum` to create it first.")
                    raise SystemExit(1)
        return True
    else:
        return False


def process_sum_command(config_file: Path, smf_type: str, sum_func: Callable, summary_level: str,
                        start_time: str, end_time: str, db_user: str, db_password: str,
                        ssh_user: str, ssh_password: str, *args):
    """Summing up from interval database to 15min, hourly and daily databases."""

    config_mgr = ConfigManager(config_file)
    result = config_mgr.load_config()
    if not isinstance(result, tuple):
        db_host = config_mgr.get('database.host')
        db_port = config_mgr.get('database.port')
        db_driver = config_mgr.get('database.driver')
        ssh_host = config_mgr.get('database.ssh_host')
        ssh_port = config_mgr.get('database.ssh_port')
        partitions_scheme = config_mgr.get('database.partition_scheme')
        if ssh_host is not None:
            use_ssh = True
        else:
            use_ssh = False

        if use_ssh and not supports_sshtunnel(): #SSH_TUNNEL_SUPPORT:
            click.secho(
                'Cannot open SSH tunnel, "sshtunnel" package was not found. '
                "Please install smf2db with `pip install smf2db[sshtunnel]` if you want SSH tunnel support and SSH tunnel is supported on this platform.",
                err=True,
                fg="red",
            )
            raise SystemExit(1)

        for smf in config_mgr.get('smf'):
            if smf['type'] == smf_type:
                if not smf['enabled']:
                    click.echo(f"\nDatabase for {smf_type} has not been initialized. Please, run `smf2db db initdb` to create it first.")
                    raise SystemExit(1)
                if not smf['summary'][summary_level]:
                    click.echo(f"\nThe summary level `{summary_level}` for this smf type is not enabled. Please, run `smf2db db initsum` to enable it.")
                    raise SystemExit(1)
                break

        if db_driver != 'sqlite' and use_ssh and ssh_host is not None:
            if ssh_port is None:
                ssh_address_or_host = (ssh_host)
            else:
                ssh_address_or_host = (ssh_host, ssh_port)
            try:
                import sshtunnel
                with sshtunnel.SSHTunnelForwarder(
                        ssh_address_or_host=ssh_address_or_host,
                        ssh_username=ssh_user,
                        ssh_password=ssh_password,
                        # ssh_pkey=ssh_private_key_path,
                        # ssh_private_key_password=ssh_private_key_password,
                        remote_bind_address=(db_host, db_port),
                ) as tunnel:
                    if tunnel is not None:
                        tunnel.start()
                        print(f"TunnelIsUp: {tunnel.tunnel_is_up} | {tunnel.local_bind_address}")
                        db_port = tunnel.local_bind_port
                        # check database existence
                        check_database_existence(config_mgr, smf_type, db_user, db_password, db_port)

                        with Progress(
                                SpinnerColumn(),
                                TextColumn("[progress.description]{task.description}"),
                                transient=True,
                        ) as progress:
                            progress.add_task(description=f"Summing up {smf_type}...{summary_level}", total=None)
                            session, engines = with_sql_session(config_mgr, smf_type, db_user, db_password,
                                                                tunnel.local_bind_port, use_ssh=True)
                            try:
                                with session as s:
                                    sumup_result = sum_func(engines, s, summary_level, start_time, end_time,
                                                            partitions_scheme, db_driver)
                            except Exception as e:
                                click.secho(
                                    f"Summing up failed with '{ERRORS[DB_WRITE_ERROR]}': {str(e)}",
                                    err=True,
                                    fg="red")
                                raise SystemExit(1)
                    else:
                        click.secho(
                            "Unable to establish SSH tunnel.",
                            err=True,
                            fg="red")
                        return DB_CONNECTION_ERROR
            except Exception as e:
                click.secho(
                    f"Unable to establish SSH tunnel: {str(e)}",
                    err=True,
                    fg="red")
                return DB_CONNECTION_ERROR
        else:
            # check database existence
            check_database_existence(config_mgr, smf_type, db_user, db_password, db_port)
            with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    transient=True,
            ) as progress:
                progress.add_task(description=f"Summing up {smf_type}...{summary_level}", total=None)
                session, engines = with_sql_session(config_mgr, smf_type, db_user, db_password, db_port,
                                                    use_ssh=False)
                try:
                    with session as s:
                        sumup_result = sum_func(engines, s, summary_level, start_time, end_time,
                                                partitions_scheme, db_driver)
                except Exception as e:
                    click.echo(f"Summing up database failed with '{ERRORS[DB_WRITE_ERROR]}': {str(e)}")
                    raise SystemExit(1)

        return sumup_result
    else:
        click.echo('\nConfig file not found. Please, run `smf2db db initcfg`')
        raise SystemExit(1)


class OptionPromptNull(click.Option):

    def prompt_for_value(self, ctx):
        default = None
        config_file = ctx.params.get('config_file')
        config_mgr = ConfigManager(config_file)
        cfg = config_mgr.load_config()
        if isinstance(cfg, tuple):
            click.secho(
                'Cannot open config file. '
                f"Please run `smf2db db initcfg` to create the config file first before you initialize the database.{cfg}",
                err=True,
                fg="red",
            )
            raise SystemExit(1)

        # Validate config file
        try:
            jsonschema.validate(cfg, schema=schema)
        except jsonschema.exceptions.ValidationError as ex:
            click.secho(
                f"Invalid config file: {ex} "
                "Please run `smf2db db initcfg` to create the config file first.",
                err=True,
                fg="red",
            )
            raise SystemExit(1)

        db_driver = config_mgr.get('database.driver')

        # only prompt if the db_driver is not sqlite
        if db_driver != 'sqlite':
            return super(OptionPromptNull, self).prompt_for_value(ctx)

        return default


class OptionPromptSsh(click.Option):

    def prompt_for_value(self, ctx):
        default = None
        config_file = ctx.params.get('config_file')
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
        # Validate config file
        try:
            jsonschema.validate(cfg, schema=schema)
        except jsonschema.exceptions.ValidationError as ex:
            click.secho(
                f"Invalid config file: {ex} "
                "Please run `smf2db db initcfg` to create the config file first.",
                err=True,
                fg="red",
            )
            raise SystemExit(1)

        ssh_host = config_mgr.get('database.ssh_host')

        # only prompt if the ssh_host is not None
        if ssh_host is not None:
            return super(OptionPromptSsh, self).prompt_for_value(ctx)

        return default

def check_date_range(ctx, param, end_time):
    start_time = ctx.params.get('start_time')
    if end_time < start_time:
        raise click.BadParameter(
            f"Invalid start time or end time: end time must be greater than start time.",
        )
    return end_time


def process_sumup_result(sumup_result):
    insert_dict_list = sumup_result.insert_dict_list
    if len(insert_dict_list) > 0:
        insert_dict = insert_dict_list[0]
        click.echo(f"Sumup Result (table name: row count): {insert_dict}")
    else:
        click.echo("No records were inserted.")

@click.command("30")
@click.option("--config_file", required=True, type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True), callback=validate_config_file)
@click.option("-U", "--db_user", prompt="Username", cls=OptionPromptNull, help="Database userid.")
@click.option("-W", "--password", prompt="Password", cls=OptionPromptNull, hide_input=True)
@click.option('--ssh_user', prompt="SSH Username", cls=OptionPromptSsh, help="SSH connect userid.")
@click.option('--ssh_password', prompt="SSH User Password", cls=OptionPromptSsh, hide_input=True)
@click.option("--summary_level", prompt="Summary Level", required=True,
              type=click.Choice(["hourly", "daily"]))
@click.option("-s", "--start_time",type=click.DateTime(formats=["%Y-%m-%d %H:%M"]),default="2000-01-01 00:00",help="Start time (YYYY-MM-DD HH:MM)")
@click.option("-e", "--end_time", type=click.DateTime(formats=["%Y-%m-%d %H:%M"]), default=str(dt.datetime.now())[:16], help="End time (YYYY-MM-DD HH:MM)", callback=check_date_range)
def sum_30(config_file, summary_level, start_time, end_time,
           db_user, password, ssh_user=None, ssh_password=None) -> None:
    """Summing up Smf30 database from interval to hourly or daily databases."""
    sumup_result = process_sum_command(config_file, '30', sum_30db, summary_level,
                                       start_time, end_time, db_user, password, ssh_user, ssh_password)
    process_sumup_result(sumup_result)


@click.command("70")
@click.option("--config_file", required=True, type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True), callback=validate_config_file)
@click.option("-U", "--db_user", prompt="Username", cls=OptionPromptNull, help="Database userid.")
@click.option("-W", "--password", prompt="Password", cls=OptionPromptNull, hide_input=True)
@click.option('--ssh_user', prompt="SSH Username", cls=OptionPromptSsh, help="SSH connect userid.")
@click.option('--ssh_password', prompt="SSH User Password", cls=OptionPromptSsh, hide_input=True)
@click.option("--summary_level", prompt="Summary Level", required=True,
              type=click.Choice(["hourly", "daily"]))
@click.option("-s", "--start_time",type=click.DateTime(formats=["%Y-%m-%d %H:%M"]),default="2000-01-01 00:00",help="Start time (YYYY-MM-DD HH:MM)")
@click.option("-e", "--end_time", type=click.DateTime(formats=["%Y-%m-%d %H:%M"]), default=str(dt.datetime.now())[:16], help="End time (YYYY-MM-DD HH:MM)", callback=check_date_range)
def sum_70(config_file, summary_level, start_time, end_time,
           db_user, password, ssh_user=None, ssh_password=None) -> None:
    """Summing up Smf70 database from interval to hourly or daily databases."""
    sumup_result = process_sum_command(config_file, '70', sum_70db, summary_level, start_time, end_time,
                                       db_user, password, ssh_user, ssh_password)
    process_sumup_result(sumup_result)


@click.command("71")
@click.option("--config_file", required=True, type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True), callback=validate_config_file)
@click.option("-U", "--db_user", prompt="Username", cls=OptionPromptNull, help="Database userid.")
@click.option("-W", "--password", prompt="Password", cls=OptionPromptNull, hide_input=True)
@click.option('--ssh_user', prompt="SSH Username", cls=OptionPromptSsh, help="SSH connect userid.")
@click.option('--ssh_password', prompt="SSH User Password", cls=OptionPromptSsh, hide_input=True)
@click.option("--summary_level", prompt="Summary Level", required=True,
              type=click.Choice(["hourly", "daily"]))
@click.option("-s", "--start_time",type=click.DateTime(formats=["%Y-%m-%d %H:%M"]),default="2000-01-01 00:00",help="Start time (YYYY-MM-DD HH:MM)")
@click.option("-e", "--end_time", type=click.DateTime(formats=["%Y-%m-%d %H:%M"]), default=str(dt.datetime.now())[:16], help="End time (YYYY-MM-DD HH:MM)", callback=check_date_range)
def sum_71(config_file, summary_level, start_time, end_time,
           db_user, password, ssh_user=None, ssh_password=None) -> None:
    """Summing up Smf71 database from interval to hourly or daily databases."""
    sumup_result = process_sum_command(config_file, '71', sum_71db, summary_level, start_time, end_time,
                                       db_user, password, ssh_user, ssh_password)
    process_sumup_result(sumup_result)


@click.command("72")
@click.option("--config_file", required=True, type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True), callback=validate_config_file)
@click.option("-U", "--db_user", prompt="Username", cls=OptionPromptNull, help="Database userid.")
@click.option("-W", "--password", prompt="Password", cls=OptionPromptNull, hide_input=True)
@click.option('--ssh_user', prompt="SSH Username", cls=OptionPromptSsh, help="SSH connect userid.")
@click.option('--ssh_password', prompt="SSH User Password", cls=OptionPromptSsh, hide_input=True)
@click.option("--summary_level", prompt="Summary Level", required=True,
              type=click.Choice(["hourly", "daily"]))
@click.option("-s", "--start_time",type=click.DateTime(formats=["%Y-%m-%d %H:%M"]),default="2000-01-01 00:00",help="Start time (YYYY-MM-DD HH:MM)")
@click.option("-e", "--end_time", type=click.DateTime(formats=["%Y-%m-%d %H:%M"]), default=str(dt.datetime.now())[:16], help="End time (YYYY-MM-DD HH:MM)", callback=check_date_range)
def sum_72(config_file, summary_level, start_time, end_time,
           db_user, password, ssh_user=None, ssh_password=None) -> None:
    """Summing up Smf72 database from interval to hourly or daily databases."""
    sumup_result = process_sum_command(config_file, '72', sum_72db, summary_level, start_time, end_time,
                                       db_user, password, ssh_user, ssh_password)
    process_sumup_result(sumup_result)

@click.command("73")
@click.option("--config_file", required=True, type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True), callback=validate_config_file)
@click.option("-U", "--db_user", prompt="Username", cls=OptionPromptNull, help="Database userid.")
@click.option("-W", "--password", prompt="Password", cls=OptionPromptNull, hide_input=True)
@click.option('--ssh_user', prompt="SSH Username", cls=OptionPromptSsh, help="SSH connect userid.")
@click.option('--ssh_password', prompt="SSH User Password", cls=OptionPromptSsh, hide_input=True)
@click.option("--summary_level", prompt="Summary Level", required=True,
              type=click.Choice(["hourly", "daily"]))
@click.option("-s", "--start_time",type=click.DateTime(formats=["%Y-%m-%d %H:%M"]),default="2000-01-01 00:00",help="Start time (YYYY-MM-DD HH:MM)")
@click.option("-e", "--end_time", type=click.DateTime(formats=["%Y-%m-%d %H:%M"]), default=str(dt.datetime.now())[:16], help="End time (YYYY-MM-DD HH:MM)", callback=check_date_range)
def sum_73(config_file, summary_level, start_time, end_time,
           db_user, password, ssh_user=None, ssh_password=None) -> None:
    """Summing up Smf73 database from interval to hourly or daily databases."""
    sumup_result = process_sum_command(config_file, '73', sum_73db, summary_level, start_time, end_time,
                                       db_user, password, ssh_user, ssh_password)
    process_sumup_result(sumup_result)


@click.command("74")
@click.option("--config_file", required=True, type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True), callback=validate_config_file)
@click.option("-U", "--db_user", prompt="Username", cls=OptionPromptNull, help="Database userid.")
@click.option("-W", "--password", prompt="Password", cls=OptionPromptNull, hide_input=True)
@click.option('--ssh_user', prompt="SSH Username", cls=OptionPromptSsh, help="SSH connect userid.")
@click.option('--ssh_password', prompt="SSH User Password", cls=OptionPromptSsh, hide_input=True)
@click.option("--summary_level", prompt="Summary Level", required=True,
              type=click.Choice(["hourly", "daily"]))
@click.option("-s", "--start_time",type=click.DateTime(formats=["%Y-%m-%d %H:%M"]),default="2000-01-01 00:00",help="Start time (YYYY-MM-DD HH:MM)")
@click.option("-e", "--end_time", type=click.DateTime(formats=["%Y-%m-%d %H:%M"]), default=str(dt.datetime.now())[:16], help="End time (YYYY-MM-DD HH:MM)", callback=check_date_range)
def sum_74(config_file, summary_level, start_time, end_time,
           db_user, password, ssh_user=None, ssh_password=None) -> None:
    """Summing up Smf74 database from interval to hourly or daily databases."""
    sumup_result = process_sum_command(config_file, '74', sum_74db, summary_level, start_time, end_time,
                                       db_user, password, ssh_user, ssh_password)
    process_sumup_result(sumup_result)


@click.command("75")
@click.option("--config_file", required=True, type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True), callback=validate_config_file)
@click.option("-U", "--db_user", prompt="Username", cls=OptionPromptNull, help="Database userid.")
@click.option("-W", "--password", prompt="Password", cls=OptionPromptNull, hide_input=True)
@click.option('--ssh_user', prompt="SSH Username", cls=OptionPromptSsh, help="SSH connect userid.")
@click.option('--ssh_password', prompt="SSH User Password", cls=OptionPromptSsh, hide_input=True)
@click.option("--summary_level", prompt="Summary Level", required=True,
              type=click.Choice(["hourly", "daily"]))
@click.option("-s", "--start_time",type=click.DateTime(formats=["%Y-%m-%d %H:%M"]),default="2000-01-01 00:00",help="Start time (YYYY-MM-DD HH:MM)")
@click.option("-e", "--end_time", type=click.DateTime(formats=["%Y-%m-%d %H:%M"]), default=str(dt.datetime.now())[:16], help="End time (YYYY-MM-DD HH:MM)", callback=check_date_range)
def sum_75(config_file, summary_level, start_time, end_time,
           db_user, password, ssh_user=None, ssh_password=None) -> None:
    """Summing up Smf75 database from interval to hourly or daily databases."""
    sumup_result = process_sum_command(config_file, '75', sum_75db, summary_level, start_time, end_time,
                                       db_user, password, ssh_user, ssh_password)
    process_sumup_result(sumup_result)


@click.command("77")
@click.option("--config_file", required=True, type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True), callback=validate_config_file)
@click.option("-U", "--db_user", prompt="Username", cls=OptionPromptNull, help="Database userid.")
@click.option("-W", "--password", prompt="Password", cls=OptionPromptNull, hide_input=True)
@click.option('--ssh_user', prompt="SSH Username", cls=OptionPromptSsh, help="SSH connect userid.")
@click.option('--ssh_password', prompt="SSH User Password", cls=OptionPromptSsh, hide_input=True)
@click.option("--summary_level", prompt="Summary Level", required=True,
              type=click.Choice(["hourly", "daily"]))
@click.option("-s", "--start_time",type=click.DateTime(formats=["%Y-%m-%d %H:%M"]),default="2000-01-01 00:00",help="Start time (YYYY-MM-DD HH:MM)")
@click.option("-e", "--end_time", type=click.DateTime(formats=["%Y-%m-%d %H:%M"]), default=str(dt.datetime.now())[:16], help="End time (YYYY-MM-DD HH:MM)", callback=check_date_range)
def sum_77(config_file, summary_level, start_time, end_time,
           db_user, password, ssh_user=None, ssh_password=None) -> None:
    """Summing up Smf77 database from interval to hourly or daily databases."""
    sumup_result = process_sum_command(config_file, '77', sum_77db, summary_level, start_time, end_time,
                                       db_user, password, ssh_user, ssh_password)
    process_sumup_result(sumup_result)


@click.command("78")
@click.option("--config_file", required=True, type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True), callback=validate_config_file)
@click.option("-U", "--db_user", prompt="Username", cls=OptionPromptNull, help="Database userid.")
@click.option("-W", "--password", prompt="Password", cls=OptionPromptNull, hide_input=True)
@click.option('--ssh_user', prompt="SSH Username", cls=OptionPromptSsh, help="SSH connect userid.")
@click.option('--ssh_password', prompt="SSH User Password", cls=OptionPromptSsh, hide_input=True)
@click.option("--summary_level", prompt="Summary Level", required=True,
              type=click.Choice(["hourly", "daily"]))
@click.option("-s", "--start_time",type=click.DateTime(formats=["%Y-%m-%d %H:%M"]),default="2000-01-01 00:00",help="Start time (YYYY-MM-DD HH:MM)")
@click.option("-e", "--end_time", type=click.DateTime(formats=["%Y-%m-%d %H:%M"]), default=str(dt.datetime.now())[:16], help="End time (YYYY-MM-DD HH:MM)", callback=check_date_range)
def sum_78(config_file, summary_level, start_time, end_time,
           db_user, password, ssh_user=None, ssh_password=None) -> None:
    """Summing up Smf78 database from interval to hourly or daily databases."""
    sumup_result = process_sum_command(config_file, '78', sum_78db, summary_level, start_time, end_time,
                                       db_user, password, ssh_user, ssh_password)
    process_sumup_result(sumup_result)


@click.command("123")
@click.option("--config_file", required=True, type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True), callback=validate_config_file)
@click.option("-U", "--db_user", prompt="Username", cls=OptionPromptNull, help="Database userid.")
@click.option("-W", "--password", prompt="Password", cls=OptionPromptNull, hide_input=True)
@click.option('--ssh_user', prompt="SSH Username", cls=OptionPromptSsh, help="SSH connect userid.")
@click.option('--ssh_password', prompt="SSH User Password", cls=OptionPromptSsh, hide_input=True)
@click.option("--summary_level", prompt="Summary Level", required=True,
              type=click.Choice(["15min", "hourly", "daily"]))
@click.option("-s", "--start_time",type=click.DateTime(formats=["%Y-%m-%d %H:%M"]),default="2000-01-01 00:00",help="Start time (YYYY-MM-DD HH:MM)")
@click.option("-e", "--end_time", type=click.DateTime(formats=["%Y-%m-%d %H:%M"]), default=str(dt.datetime.now())[:16], help="End time (YYYY-MM-DD HH:MM)", callback=check_date_range)
def sum_123(config_file, summary_level, start_time, end_time,
           db_user, password, ssh_user=None, ssh_password=None) -> None:
    """Summing up Smf123 database from interval to 15min, hourly or daily databases."""
    sumup_result = process_sum_command(config_file, '123', sum_123db, summary_level, start_time, end_time,
                                       db_user, password, ssh_user, ssh_password)
    process_sumup_result(sumup_result)


@click.command("110_1")
@click.option("--config_file", required=True, type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True), callback=validate_config_file)
@click.option("-U", "--db_user", prompt="Username", cls=OptionPromptNull, help="Database userid.")
@click.option("-W", "--password", prompt="Password", cls=OptionPromptNull, hide_input=True)
@click.option('--ssh_user', prompt="SSH Username", cls=OptionPromptSsh, help="SSH connect userid.")
@click.option('--ssh_password', prompt="SSH User Password", cls=OptionPromptSsh, hide_input=True)
@click.option("--summary_level", prompt="Summary Level", required=True,
              type=click.Choice(["15min", "hourly", "daily"]))
@click.option("-s", "--start_time",type=click.DateTime(formats=["%Y-%m-%d %H:%M"]),default="2000-01-01 00:00",help="Start time (YYYY-MM-DD HH:MM)")
@click.option("-e", "--end_time", type=click.DateTime(formats=["%Y-%m-%d %H:%M"]), default=str(dt.datetime.now())[:16], help="End time (YYYY-MM-DD HH:MM)", callback=check_date_range)
def sum_110_1(config_file, summary_level, start_time, end_time,
           db_user, password, ssh_user=None, ssh_password=None) -> None:
    """Summing up Smf110 subtype 1 database from interval to 15min, hourly or daily databases."""
    sumup_result = process_sum_command(config_file, '110_1', sum_1101db, summary_level, start_time, end_time,
                                       db_user, password, ssh_user, ssh_password)
    process_sumup_result(sumup_result)


@click.command("110_2")
@click.option("--config_file", required=True, type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True), callback=validate_config_file)
@click.option("-U", "--db_user", prompt="Username", cls=OptionPromptNull, help="Database userid.")
@click.option("-W", "--password", prompt="Password", cls=OptionPromptNull, hide_input=True)
@click.option('--ssh_user', prompt="SSH Username", cls=OptionPromptSsh, help="SSH connect userid.")
@click.option('--ssh_password', prompt="SSH User Password", cls=OptionPromptSsh, hide_input=True)
@click.option("--summary_level", prompt="Summary Level", required=True,
              type=click.Choice(["hourly", "daily"]))
@click.option("-s", "--start_time",type=click.DateTime(formats=["%Y-%m-%d %H:%M"]),default="2000-01-01 00:00",help="Start time (YYYY-MM-DD HH:MM)")
@click.option("-e", "--end_time", type=click.DateTime(formats=["%Y-%m-%d %H:%M"]), default=str(dt.datetime.now())[:16], help="End time (YYYY-MM-DD HH:MM)", callback=check_date_range)
def sum_110_2(config_file, summary_level, start_time, end_time,
           db_user, password, ssh_user=None, ssh_password=None) -> None:
    """Summing up Smf110 subtype 2 database from interval to hourly or daily databases."""
    sumup_result = process_sum_command(config_file, '110_2', sum_1102db, summary_level, start_time, end_time,
                                       db_user, password, ssh_user, ssh_password)
    process_sumup_result(sumup_result)

