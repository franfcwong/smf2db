initsum
=======

Synopsis
--------

**db initsum** <smf_type> <summary> ... [*OPTIONS*] ...

Description
-----------

:program:`db initsum` is an interactive command line tool that asks some questions
about further options if required and then initialize the summary databases for the smf type and summary level specified.

*smf_typ* is the SMF type to be initialized by this program.
Currently, only 30, 70 - 75, 77, 78, 110_1, 110_2, 123 are supported.

*summary* is the summary level to be initialized for the specified smf type.
Currently, only 15min, hourly and daily are supported. For 15min, only smf type 110_1 and 123 are supported.

Options
-------

.. program:: db initsum

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

.. option:: -h, --help

   Display usage summary.