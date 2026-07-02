sumup
=====

Synopsis
--------

**db sumup** <smf_type> [*OPTIONS*] ...

Description
-----------

:program:`sumup` is an interactive command line tool that asks some questions
about further options if required and then summarize the databases of the smf type specified and
the chosen summary level.

*smf_typ* is the SMF type to be summarized by this program.
Currently, only 30, 70 - 75, 77, 78, 110_1, 110_2, 123 are supported.

Options
-------

.. program:: db sumup

.. option:: --summary_level=<15min|hourly|daily>

   This is the summary level to be summarized. Currently, only smf type ``110_1`` and ``123`` allow summary
   level ``15min`` while all smf types will support ``hourly`` and ``daily`` summary level.

.. option:: -U USERNAME, --username=USERNAME

   This USERNAME will be used to connect to the database.

.. option:: -W PASSWORD, --password=PASSWORD

   It is used to connect to the database.

.. option:: --ssh_user=USERNAME

   This USERNAME will be used to connect to the SSH Server if ssh is used.

.. option:: --ssh_password=PASSWORD

   It is used to connect to the SSH Server if ssh is used.

.. option:: --config_file=CONFIG_FILE_PATH

   It is the absolute or relative config file path of the config file. The file extension must be ``.yaml``.

.. option:: -s START-TIME, --start_time=START-TIME

   If specified, the program will summarize the records in databases starting from this time. Defaults to ``2000-01-01 00:00``.

.. option:: -e END-TIME, --end_time=END-TIME

   If specified, the program will summarize the records in databases before this time. Defaults to ``current time``.

.. option:: -h, --help

   Display usage summary.