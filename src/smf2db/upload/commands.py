import datetime as dt
import importlib.util
import os
import platform
import sqlite3
from collections.abc import Callable
from pathlib import Path

import click
import jsonschema
import sqlalchemy
from packaging import version
from rich.progress import Progress, SpinnerColumn, TextColumn
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.ext.horizontal_shard import ShardedSession
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import Insert
from sqlalchemy.sql import operators
from sqlalchemy.sql import visitors

from smf2db import ERRORS, DB_WRITE_ERROR, SUCCESS, DB_CONNECTION_ERROR, DEFAULT_DB_HOST
from smf2db.api.api_1101db import upload_1101db
from smf2db.api.api_1102db import upload_1102db
from smf2db.api.api_123db import upload_123db
from smf2db.api.api_30db import upload_30db
from smf2db.api.api_70db import upload_70db
from smf2db.api.api_71db import upload_71db
from smf2db.api.api_72db import upload_72db
from smf2db.api.api_73db import upload_73db
from smf2db.api.api_74db import upload_74db
from smf2db.api.api_75db import upload_75db
from smf2db.api.api_77db import upload_77db
from smf2db.api.api_78db import upload_78db
from smf2db.config import ConfigManager
from smf2db.db_models.smf1101_model import Base1101
from smf2db.db_models.smf1102_model import Base1102
from smf2db.db_models.smf123_model import Base123
from smf2db.db_models.smf30_model import Base30
from smf2db.db_models.smf70_model import Base70
from smf2db.db_models.smf71_model import Base71
from smf2db.db_models.smf72_model import Base72
from smf2db.db_models.smf73_model import Base73
from smf2db.db_models.smf74_model import Base74
from smf2db.db_models.smf75_model import Base75
from smf2db.db_models.smf77_model import Base77
from smf2db.db_models.smf78_model import Base78
from smf2db.db_models.smf7x_model import Base7x, SmfCpc, SmfLpar
from smf2db.schemas.schema import schema

sqlite_execution_options = {"schema_translate_map": {"smf30": None, "smf70": None, "smf71": None, "smf72": None,
                                                     "smf73": None, "smf74": None, "smf75": None, "smf77": None,
                                                     "smf78": None, "smf110": None, "smf110_1": None,
                                                     "smf123": None, "smf": None}}
db_base = {
    '30': Base30,
    '70': Base70,
    '71': Base71,
    '72': Base72,
    '73': Base73,
    '74': Base74,
    '75': Base75,
    '77': Base77,
    '78': Base78,
    '110_1': Base1101,
    '110_2': Base1102,
    '123': Base123,
    'smf': Base7x,
}


def supports_sqlite():
    return version.parse(sqlite3.sqlite_version) >= version.parse("3.32.0")

def supports_psycopg2():
    module_name = 'psycopg2'
    spec = importlib.util.find_spec(module_name)
    if spec:
        return True
    else:
        return False

def supports_pg8000():
    module_name = 'pg8000'
    spec = importlib.util.find_spec(module_name)
    if spec:
        return True
    else:
        return False

def supports_sshtunnel():
    module_name = 'sshtunnel'
    spec = importlib.util.find_spec(module_name)
    if spec:
        return True
    else:
        return False


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
            elif smf['type'] == 'smf':
                if config_mgr.get('database.driver') != 'sqlite':
                    engines[f"{smf['type']}.0"] = create_engine(
                        f"{config_mgr.get('database.driver')}://{user}:{password}@{config_mgr.get('database.host')}:{port}/{smf['dbname']}",
                        isolation_level="AUTOCOMMIT",
                    )
                else:
                    full_path = os.path.join(config_mgr.get('database.sqlite_path'), f"{smf['dbname']}.db")
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


def init_database(smf_type, config_file: Path, db_user: str, db_password: str, ssh_user: str,
                  ssh_password: str) -> int:
    """Create the database for a specific smf_type."""

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

        if use_ssh and not supports_sshtunnel(): #SSH_TUNNEL_SUPPORT:
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
                        result = create_pg_databases(smf_type, config_mgr, engine, db_user, db_password, db_port)
                    else:
                        click.secho(
                            "Unable to establish SSH tunnel.",
                            err=True,
                            fg="red")
                        return DB_CONNECTION_ERROR
            except Exception as e:
                click.secho(
                    f"Unable to establish SSH tunnel: {e}",
                    err=True,
                    fg="red")
                return DB_CONNECTION_ERROR
        elif db_driver != 'sqlite':
            db_url = get_database_url(config_mgr, db_user, db_password, db_port, 'postgres')
            engine = create_engine(db_url, isolation_level="AUTOCOMMIT")
            result = create_pg_databases(smf_type, config_mgr, engine, db_user, db_password, db_port)
        else:
            result = create_sqlite_databases(smf_type, config_mgr)
    return result


def create_pg_databases(smf_type, config_mgr: ConfigManager, engine, db_user, db_password, db_port):
    """Create databases and tables for target smf_type if not exists"""
    partitions_scheme = config_mgr.get('database.partition_scheme')
    if partitions_scheme == 'weekday':
        partitions = range(1, 8)
        other_partitions = range(8, 53)
    elif partitions_scheme == 'day':
        partitions = range(1, 32)
        other_partitions = range(32, 53)
    elif partitions_scheme == 'week':
        partitions = range(1, 53)
        other_partitions = []
    else:
        partitions = range(1, 2)
        other_partitions = range(2, 53)
    # creating the database
    print(f"Creating databases for {smf_type} with partitions_scheme: {partitions_scheme}")
    try:
        with engine.connect() as conn:
            for smf in config_mgr.get('smf'):
                if smf_type == '70' and smf['type'] == 'smf':
                    cursor = conn.execute(
                        text(f"SELECT 1 FROM pg_database WHERE datname = '{smf['dbname']}'"))
                    if not cursor.fetchone():
                        conn.execute(text(f"CREATE DATABASE {smf['dbname']}"))
                        print(f"Database {smf['dbname']} created successfully.")
                    else:
                        print(f"Database {smf['dbname']} already exists")
                        # Check for active connections
                        cursor = conn.execute(
                            text(f"SELECT * from pg_stat_activity where datname = '{smf['dbname']}'"))
                        active_connections = cursor.fetchall()
                        if not active_connections:
                            # Drop the database
                            conn.execute(text(f"DROP DATABASE {smf['dbname']}"))
                            print(f"Database {smf['dbname']} dropped successfully.")
                        else:
                            click.secho(f"Cannot drop {smf['type']} database; active connectionss exist.",
                                        err=True,
                                        fg="red",)
                            raise SystemExit(1)
                        conn.execute(text(f"CREATE DATABASE {smf['dbname']}"))
                        print(f"Database {smf['dbname']} created successfully.")
                elif smf['type'] == smf_type and smf['enabled']:
                    for part in partitions:
                        cursor = conn.execute(
                            text(f"SELECT 1 FROM pg_database WHERE datname = '{smf['dbname']}_{part}'"))
                        if not cursor.fetchone():
                            conn.execute(text(f"CREATE DATABASE {smf['dbname']}_{part}"))
                            print(f"Database {smf['dbname']}_{part} created successfully.")
                        else: # drop and recreate the database
                            print(f"Database {smf['dbname']}_{part} already exists")
                            # Check for active connections
                            cursor = conn.execute(
                                text(f"SELECT * from pg_stat_activity where datname = '{smf['dbname']}_{part}'"))
                            active_connections = cursor.fetchall()
                            if not active_connections:
                                # Drop the database
                                conn.execute(text(f"DROP DATABASE {smf['dbname']}_{part}"))
                                print(f"Database {smf['dbname']}_{part} dropped successfully.")
                            else:
                                click.secho(f"Cannot drop {smf['dbname']}_{part} database; active connectionss exist.",
                                            err=True,
                                            fg="red", )
                                raise SystemExit(1)

                            conn.execute(text(f"CREATE DATABASE {smf['dbname']}_{part}"))
                            print(f"Database {smf['dbname']}_{part} created successfully.")
                    for part in other_partitions: # clear the other partitions if exist
                        cursor = conn.execute(
                            text(f"SELECT 1 FROM pg_database WHERE datname = '{smf['dbname']}_{part}'"))
                        if cursor.fetchone():
                            # Check for active connections
                            cursor = conn.execute(
                                text(f"SELECT * from pg_stat_activity where datname = '{smf['dbname']}_{part}'"))
                            active_connections = cursor.fetchall()
                            if not active_connections:
                                # Drop the database
                                conn.execute(text(f"DROP DATABASE {smf['dbname']}_{part}"))
                                print(f"Database {smf['dbname']}_{part} dropped successfully.")
                            else:
                                click.secho(f"Cannot drop {smf['dbname']}_{part} database; active connectionss exist.",
                                            err=True,
                                            fg="red", )
                                raise SystemExit(1)
    except Exception as e:
        print(f"Exception occurred: {e}")
        return DB_CONNECTION_ERROR

    try:
        for smf in config_mgr.get('smf'):
            if smf['type'] == smf_type and smf['enabled']:
                for part in partitions:
                    connectable = create_engine(get_database_url(config_mgr, db_user, db_password, db_port, f"{smf['dbname']}_{part}"))

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
                        get_database_url(config_mgr, db_user, db_password, db_port, f"{smf['dbname']}_{part}"))
                    # db_base[smf['type']].metadata.drop_all(db_engine)
                    db_base[smf['type']].metadata.create_all(db_engine)
            elif smf_type == '70' and smf['type'] == 'smf':
                connectable = create_engine(
                    get_database_url(config_mgr, db_user, db_password, db_port, f"{smf['dbname']}"))

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
                    get_database_url(config_mgr, db_user, db_password, db_port, f"{smf['dbname']}"))
                db_base[smf['type']].metadata.create_all(db_engine)

        return SUCCESS
    except OSError as e:
        print(f"OS Exception occurred: {e}")
        return DB_WRITE_ERROR
    except Exception as e:
        print(f"Exception occurred: {e}")
        return DB_CONNECTION_ERROR

def create_sqlite_databases(smf_type, config_mgr: ConfigManager):
    """Create sqlite databases and tables if not exists"""
    partitions_scheme = config_mgr.get('database.partition_scheme')
    if partitions_scheme == 'weekday':
        partitions = range(1, 8)
        other_partitions = range(8, 53)
    elif partitions_scheme == 'day':
        partitions = range(1, 32)
        other_partitions = range(32, 53)
    elif partitions_scheme == 'week':
        partitions = range(1, 53)
        other_partitions = []
    else:
        partitions = [1]
        other_partitions = range(2, 53)
    try:
        print(f"Creating databases for {smf_type} with partitions_scheme: {partitions_scheme}")
        for smf in config_mgr.get('smf'):
            if smf['type'] == smf_type and smf['enabled']:
                for part in partitions:
                    full_path = os.path.join(config_mgr.get('database.sqlite_path'), f"{smf['dbname']}_{part}.db")
                    sqlite_path = f"sqlite:///{full_path}"
                    if Path(full_path).exists():
                        os.remove(full_path)
                        print(f"Database {smf['dbname']}_{part} dropped successfully.")
                    db_engine = create_engine(sqlite_path, execution_options=sqlite_execution_options)
                    db_base[smf['type']].metadata.create_all(db_engine)
                    print(f"Database {smf['dbname']}_{part} created successfully.")
                for part in other_partitions:
                    full_path = os.path.join(config_mgr.get('database.sqlite_path'), f"{smf['dbname']}_{part}.db")
                    if Path(full_path).exists():
                        os.remove(full_path)
                        print(f"Database {smf['dbname']}_{part} dropped successfully.")
            elif smf_type == '70' and smf['type'] == 'smf':
                full_path = os.path.join(config_mgr.get('database.sqlite_path'), f"{smf['dbname']}.db")
                sqlite_path = f"sqlite:///{full_path}"
                if Path(full_path).exists():
                    os.remove(full_path)
                    print(f"Database {smf['dbname']} dropped successfully.")
                db_engine = create_engine(sqlite_path, execution_options=sqlite_execution_options)
                db_base[smf['type']].metadata.create_all(db_engine)
                print(f"Database {smf['dbname']} created successfully.")
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
                    dbname = f"{smf['dbname']}_{part}"  # Get the partition db name
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
                            f"\nDatabase {db} not found. Please run `smf2db db initdb` to create it first.")
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
                        f"\nDatabase {db} not found. Please run `smf2db db initdb` to create it first.")
                    raise SystemExit(1)
        return True
    else:
        return False


def process_upload_command(config_file: Path, smf_type: str, upload_func: Callable, jsonfiles, db_user,
                           db_password, ssh_user, ssh_password, *args):
    """Upload data to smf2db database."""

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

        # Check database has been initialized
        for smf_feature in config_mgr.get('smf'):
            if smf_feature['type'] == smf_type:
                if not smf_feature['enabled']:
                    click.echo(
                        f"\nDatabase for {smf_type} has not been initialized. Please run `smf2db db initdb` to create it first.")
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
                            progress.add_task(description=f"Uploading {smf_type}...{jsonfiles}", total=None)
                            session, engines = with_sql_session(config_mgr, smf_type, db_user, db_password,
                                                                tunnel.local_bind_port, use_ssh=True)
                            try:
                                with session as s:
                                    insert_result = upload_func(engines, s, jsonfiles, partitions_scheme, db_driver)

                            except OSError as e:
                                click.echo(f"Loading JSON failed with '{ERRORS[DB_WRITE_ERROR]}': {str(e)}")
                                raise SystemExit(1)
                            except Exception as e:
                                click.echo(f"Loading JSON failed with '{ERRORS[DB_WRITE_ERROR]}': {str(e)}")
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
                progress.add_task(description=f"Uploading {smf_type}...{jsonfiles}", total=None)
                session, engines = with_sql_session(config_mgr, smf_type, db_user, db_password, db_port, use_ssh=False)
                try:
                    with session as s:
                        insert_result = upload_func(engines, s, jsonfiles, partitions_scheme, db_driver)
                except OSError as e:
                    click.echo(f"Loading JSON failed with '{ERRORS[DB_WRITE_ERROR]}': {str(e)}")
                    raise SystemExit(1)
                except Exception as e:
                    click.echo(f"Loading JSON failed with '{ERRORS[DB_WRITE_ERROR]}': {str(e)}")
                    raise SystemExit(1)
        return insert_result
    else:
        click.secho(
            'Cannot open config file. '
            "Please run `smf2db db initcfg` to create the config file first before you initialize the database.",
            err=True,
            fg="red",
        )
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

def validate_config_file(ctx, param, config_file):
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
        raise click.BadParameter(
            f"Invalid config file: {ex} "
            "Please run `smf2db db initcfg` to create the config file first."
        )
    return config_file

def process_upload_result(upload_result):
    insert_dict_list = upload_result.insert_dict_list
    if len(insert_dict_list) > 0:
        insert_dict = insert_dict_list[0]
        if len(insert_dict_list) > 1:
            for i_dict in insert_dict_list[1:]:
                for key, value in i_dict.items():
                    insert_dict[key] += value
        click.echo(f"Upload Result (table name: row count): {insert_dict}")
    else:
        click.echo("No records were inserted.")


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
@click.option("--config_file", required=True, type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True), callback=validate_config_file)
@click.option("-U", "--db_user", prompt="Username", cls=OptionPromptNull, help="Database userid.")
@click.option("-W", "--password", prompt="Password", cls=OptionPromptNull, hide_input=True)
@click.option("-i", "--interval", type=click.INT, required=True, default=30,
              help="SMF Interval in seconds.")
@click.option('--ssh_user', prompt="SSH Username", cls=OptionPromptSsh, help="SSH connect userid.")
@click.option('--ssh_password', prompt="SSH User Password", cls=OptionPromptSsh, hide_input=True)
def upload_30(jsonfiles, config_file, db_user, password, interval, ssh_user=None, ssh_password=None) -> None:
    """Upload smf30 jsonfile(s) to database."""
    upload_result = process_upload_command(config_file, '30', upload_30db, jsonfiles, db_user, password,
                                           ssh_user, ssh_password, interval)
    process_upload_result(upload_result)

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
@click.option("--config_file", required=True, type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True), callback=validate_config_file)
@click.option("-U", "--db_user", prompt="Username", cls=OptionPromptNull, help="Database userid.")
@click.option("-W", "--password", prompt="Password", cls=OptionPromptNull, hide_input=True)
@click.option('--ssh_user', prompt="SSH Username", cls=OptionPromptSsh, help="SSH connect userid.")
@click.option('--ssh_password', prompt="SSH User Password", cls=OptionPromptSsh, hide_input=True)
def upload_70(jsonfiles, config_file, db_user, password, ssh_user=None, ssh_password=None) -> None:
    """Upload smf70 jsonfile(s) to database."""
    upload_result = process_upload_command(config_file, '70', upload_70db, jsonfiles,
                                           db_user, password, ssh_user, ssh_password)
    process_upload_result(upload_result)

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
@click.option("--config_file", required=True, type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True), callback=validate_config_file)
@click.option("-U", "--db_user", prompt="Username", cls=OptionPromptNull, help="Database userid.")
@click.option("-W", "--password", prompt="Password", cls=OptionPromptNull, hide_input=True)
@click.option('--ssh_user', prompt="SSH Username", cls=OptionPromptSsh, help="SSH connect userid.")
@click.option('--ssh_password', prompt="SSH User Password", cls=OptionPromptSsh, hide_input=True)
def upload_71(jsonfiles, config_file, db_user, password, ssh_user=None, ssh_password=None) -> None:
    """Upload smf71 jsonfile(s) to database."""
    upload_result = process_upload_command(config_file, '71', upload_71db, jsonfiles, db_user,
                                           password, ssh_user, ssh_password)
    process_upload_result(upload_result)

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
@click.option("--config_file", required=True, type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True), callback=validate_config_file)
@click.option("-U", "--db_user", prompt="Username", cls=OptionPromptNull, help="Database userid.")
@click.option("-W", "--password", prompt="Password", cls=OptionPromptNull, hide_input=True)
@click.option('--ssh_user', prompt="SSH Username", cls=OptionPromptSsh, help="SSH connect userid.")
@click.option('--ssh_password', prompt="SSH User Password", cls=OptionPromptSsh, hide_input=True)
def upload_72(jsonfiles, config_file, db_user, password, ssh_user=None, ssh_password=None) -> None:
    """Upload smf72 jsonfile(s) to database."""
    upload_result = process_upload_command(config_file, '72', upload_72db, jsonfiles, db_user,
                                           password, ssh_user, ssh_password)
    process_upload_result(upload_result)

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
@click.option("--config_file", required=True, type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True), callback=validate_config_file)
@click.option("-U", "--db_user", prompt="Username", cls=OptionPromptNull, help="Database userid.")
@click.option("-W", "--password", prompt="Password", cls=OptionPromptNull, hide_input=True)
@click.option('--ssh_user', prompt="SSH Username", cls=OptionPromptSsh, help="SSH connect userid.")
@click.option('--ssh_password', prompt="SSH User Password", cls=OptionPromptSsh, hide_input=True)
def upload_73(jsonfiles, config_file, db_user, password, ssh_user=None, ssh_password=None) -> None:
    """Upload smf73 jsonfile(s) to database."""
    upload_result = process_upload_command(config_file, '73', upload_73db, jsonfiles, db_user,
                                           password, ssh_user, ssh_password)
    process_upload_result(upload_result)

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
@click.option("--config_file", required=True, type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True), callback=validate_config_file)
@click.option("-U", "--db_user", prompt="Username", cls=OptionPromptNull, help="Database userid.")
@click.option("-W", "--password", prompt="Password", cls=OptionPromptNull, hide_input=True)
@click.option('--ssh_user', prompt="SSH Username", cls=OptionPromptSsh, help="SSH connect userid.")
@click.option('--ssh_password', prompt="SSH User Password", cls=OptionPromptSsh, hide_input=True)
def upload_74(jsonfiles, config_file, db_user, password, ssh_user=None, ssh_password=None) -> None:
    """Upload smf74 jsonfile(s) to database."""
    upload_result = process_upload_command(config_file, '74', upload_74db, jsonfiles, db_user,
                                           password, ssh_user, ssh_password)
    process_upload_result(upload_result)

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
@click.option("--config_file", required=True, type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True), callback=validate_config_file)
@click.option("-U", "--db_user", prompt="Username", cls=OptionPromptNull, help="Database userid.")
@click.option("-W", "--password", prompt="Password", cls=OptionPromptNull, hide_input=True)
@click.option('--ssh_user', prompt="SSH Username", cls=OptionPromptSsh, help="SSH connect userid.")
@click.option('--ssh_password', prompt="SSH User Password", cls=OptionPromptSsh, hide_input=True)
def upload_75(jsonfiles, config_file, db_user, password, ssh_user=None, ssh_password=None) -> None:
    """Upload smf75 jsonfile(s) to database."""
    upload_result = process_upload_command(config_file, '75', upload_75db, jsonfiles, db_user,
                                           password, ssh_user, ssh_password)
    process_upload_result(upload_result)

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
@click.option("--config_file", required=True, type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True), callback=validate_config_file)
@click.option("-U", "--db_user", prompt="Username", cls=OptionPromptNull, help="Database userid.")
@click.option("-W", "--password", prompt="Password", cls=OptionPromptNull, hide_input=True)
@click.option('--ssh_user', prompt="SSH Username", cls=OptionPromptSsh, help="SSH connect userid.")
@click.option('--ssh_password', prompt="SSH User Password", cls=OptionPromptSsh, hide_input=True)
def upload_77(jsonfiles, config_file, db_user, password, ssh_user=None, ssh_password=None) -> None:
    """Upload smf77 jsonfile(s) to database."""
    upload_result = process_upload_command(config_file, '77', upload_77db, jsonfiles, db_user,
                                           password, ssh_user, ssh_password)
    process_upload_result(upload_result)

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
@click.option("--config_file", required=True, type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True), callback=validate_config_file)
@click.option("-U", "--db_user", prompt="Username", cls=OptionPromptNull, help="Database userid.")
@click.option("-W", "--password", prompt="Password", cls=OptionPromptNull, hide_input=True)
@click.option('--ssh_user', prompt="SSH Username", cls=OptionPromptSsh, help="SSH connect userid.")
@click.option('--ssh_password', prompt="SSH User Password", cls=OptionPromptSsh, hide_input=True)
def upload_78(jsonfiles, config_file, db_user, password, ssh_user=None, ssh_password=None) -> None:
    """Upload smf78 jsonfile(s) to database."""
    upload_result = process_upload_command(config_file, '78', upload_78db, jsonfiles, db_user,
                                           password, ssh_user, ssh_password)
    process_upload_result(upload_result)

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
@click.option("--config_file", required=True, type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True), callback=validate_config_file)
@click.option("-U", "--db_user", prompt="Username", cls=OptionPromptNull, help="Database userid.")
@click.option("-W", "--password", prompt="Password", cls=OptionPromptNull, hide_input=True)
@click.option('--ssh_user', prompt="SSH Username", cls=OptionPromptSsh, help="SSH connect userid.")
@click.option('--ssh_password', prompt="SSH User Password", cls=OptionPromptSsh, hide_input=True)
def upload_123(jsonfiles, config_file, db_user, password, ssh_user=None, ssh_password=None) -> None:
    """Upload smf123 jsonfile(s) to database."""
    upload_result = process_upload_command(config_file, '123', upload_123db, jsonfiles, db_user,
                                           password, ssh_user, ssh_password)
    process_upload_result(upload_result)

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
@click.option("--config_file", required=True, type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True), callback=validate_config_file)
@click.option("-U", "--db_user", prompt="Username", cls=OptionPromptNull, help="Database userid.")
@click.option("-W", "--password", prompt="Password", cls=OptionPromptNull, hide_input=True)
@click.option('--ssh_user', prompt="SSH Username", cls=OptionPromptSsh, help="SSH connect userid.")
@click.option('--ssh_password', prompt="SSH User Password", cls=OptionPromptSsh, hide_input=True)
def upload_110_1(jsonfiles, config_file, db_user, password, ssh_user=None, ssh_password=None) -> None:
    """Upload smf110 Subtype 1 jsonfile(s) to database."""
    upload_result = process_upload_command(config_file, '110_1', upload_1101db, jsonfiles, db_user,
                                           password, ssh_user, ssh_password)
    process_upload_result(upload_result)

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
@click.option("--config_file", required=True, type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True), callback=validate_config_file)
@click.option("-U", "--db_user", prompt="Username", cls=OptionPromptNull, help="Database userid.")
@click.option("-W", "--password", prompt="Password", cls=OptionPromptNull, hide_input=True)
@click.option('--ssh_user', prompt="SSH Username", cls=OptionPromptSsh, help="SSH connect userid.")
@click.option('--ssh_password', prompt="SSH User Password", cls=OptionPromptSsh, hide_input=True)
def upload_110_2(jsonfiles, config_file, db_user, password, ssh_user=None, ssh_password=None) -> None:
    """Upload smf110 Subtype 2 jsonfile(s) to database."""
    upload_result = process_upload_command(config_file, '110_2', upload_1102db, jsonfiles, db_user,
                                           password, ssh_user, ssh_password)
    process_upload_result(upload_result)

