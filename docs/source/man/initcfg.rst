initcfg
=======

Synopsis
--------

**db initcfg** [*OPTIONS*] ...

Description
-----------

:program:`db initcfg` is an interactive command line tool that asks some questions
about further options if required and then create a yaml configuration file in the specified file location.

Options
-------

.. program:: db initcfg

.. option:: --config_file=CONFIG_FILE_PATH

   It is the absolute or relative config file path of the config file. The file extension must be ``.yaml``.

.. option:: --db_driver=<sqlite|pg8000|psycopg2>

   It is the db python driver to be used. Defaults to ``sqlite``.
   If ``psycopg2`` or ``pg8000`` is specified, user is required to install this
   python package on your own.

.. option:: -x PREFIX, --db_prefix=PREFIX

   The prefix added to the database names. Defaults to ``None``, i.e. no prefix.

.. option:: --partitions=<no partition|weekday|day of month|week number>

    The partition scheme to be used for the interval databases. Defaults to ``no partition``, that
    means, only one single database will be created. If it is ``weekday``, it means 7 databases will
    be created, 1 for Monday, 2 for Tuseday, etc. For ``day of month``, 31 databases will be created as
    named by day of the month and for ``week number``, 52 databases will be created.

.. option:: -h HOST, --host=HOST

   The PG database server IP address or domain name. Defaults to ``None``.

.. option:: -p PORT, --port=PORT

   The port number of the PG database server. Defaults to ``None``.

.. option:: --ssh=USE

   USE can either ``True`` or ``False``.  Defaults to ``False``. If specified, it means SSH connection
   will be used to coonect to the database.

.. option:: --sqlite_path=PATH

   The path to sqlite db file and it must be exist and accessible.

.. option:: --ssh_host=HOST

   The SSH server IP address or domain name. Defaults to ``None``.

.. option:: --ssh_port=PORT

   The port number of the SSH server. Defaults to ``None``.

.. option:: -h, --help

   Display usage summary.
