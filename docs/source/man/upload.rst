upload
======

Synopsis
--------

**db upload** <smf_type> <jsonfile> ... [*OPTIONS*] ...

Description
-----------

:program:`db upload` is an interactive command line tool that asks some questions
about your credentials and then upload the JSON files to Postgres database
which should be set up in another tool `initdb` in advance.

*smf_typ* is the SMF type of the JSON files supported by this program to be uploaded.
Currently, only 30, 70 - 75, 77, 78, 110_1, 110_2, 123 are supported.

*jsonfile* is the path to one or more JSON files containing the output of
`SMF2JSON <https://cbttape.org/ftp/cbt/CBT1064.zip>`__.

Options
-------

.. program:: db upload

.. option:: --config_file=CONFIG_FILE_PATH

   It is the absolute or relative config file path of the config file. The file extension must be ``.yaml``.

.. option:: -U USERNAME, --db_user=USERNAME

   This USERNAME will be used to connect to the database.

.. option:: -W PASSWORD, --password=PASSWORD

   It is used to connect to the database.

.. option:: --ssh_user=USERNAME

   This USERNAME will be used to connect to the SSH Server if ssh is used.

.. option:: --ssh_password=PASSWORD

   It is used to connect to the SSH Server if ssh is used.

.. option:: -i INTERVAL, --interval=INTERVAL

   This option is only available for smf type ``30``. It denotes the smf interval of the records which is advised
   to be specified, otherwise, the program may calculate it incorrectly from the JSON data.
   Default to ``30`` minutes.

.. option:: -h, --help

   Display usage summary.

