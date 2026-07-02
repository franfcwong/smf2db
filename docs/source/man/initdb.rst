initdb
======

Synopsis
--------

**db initdb** <smf_type> ... [*OPTIONS*] ...

Description
-----------

:program:`db initdb` is an interactive command line tool that asks some questions
about further options if required and then create the schema, databases and tables in the smf type specified.

*smf_typ* is the SMF type to be initialized by this program.
Currently, only 30, 70 - 75, 77, 78, 110_1, 110_2, 123 are supported.

Options
-------

.. program:: db initdb

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
