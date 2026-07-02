report
======

Synopsis
--------

**report** <smf_type> <jsonfile> ... [*OPTIONS*] ...

Description
-----------

:program:`report` is an command line tool that asks some questions
about further options if required and then print the report based on the JSON files.

*smf_typ* is the SMF type of the JSON files supported by this program to be uploaded.
Currently, only 30, 70 - 75, 77, 78, 110_1, 110_2, 123 are supported.

*jsonfile* is the path to one or more JSON files containing the output of
`SMF2JSON <https://cbttape.org/ftp/cbt/CBT1064.zip>`__.

Generic Options for all SMF types
---------------------------------

.. program:: report

.. option:: -s START-TIME, --start_time=START-TIME

   If specified, the program will filter the JSON files data starting from this time. Defaults to ``2000-01-01 00:00``.

.. option:: -e END-TIME, --end_time=END-TIME

   If specified, the program will filter the JSON files data before this time. Defaults to ``current time``.

.. option:: -h, --help

   Display usage summary.

.. option:: -o OUTPUT-FILE, --out=OUTPUT-FILE

   If specified, the report will be output to the file specified instead.

Options for 30
--------------

.. option:: -i INTERVAL, --interval=INTERVAL

   SMF Interval in minutes will be set if it cannot be determined from the data. Defaults to ``30``.

.. option:: -t SUBTYPE, --subtype=SUBTYPE

   SUBTYPE must be between 1 to 6. If specified, only the corresponding subtype will be displayed.
   Defaults to ``None``, that means all the subtypes will be displayed.

.. option:: -j JOBNAME, --jobname=JOBNAME

   If specified, only records with this JOBNAME will be displayed. Defaults to ``None``.

.. option:: -x EXCLUDE, --exclude_job_starts=EXCLDUE

   If specified, all job names start with this EXCLUDE will not be displayed. Defaults to ``None``.

Options for 70
--------------

.. option:: -r REPORT-NAME, --report_type=REPORT-NAME

   This option is required. Currently, only two reports are supported, either ``'CPU Activity Report'`` or
   ``'Crypto Hardware Activity Report'``.

.. option:: -l LPAR, --lpar=LPAR

   This option is required. The report for the LPAR will be displayed.

Options for 71
--------------

.. option:: -l LPAR, --lpar=LPAR

   This option is required. The report for the LPAR will be displayed.

Options for 72
--------------

.. option:: -r REPORT-NAME, --report_type=REPORT-NAME

   This option is required. Currently, only two reports are supported:

   * ``'Workload Activity Report'``
   * ``'Serialization Delay Report'``

.. option:: -l LPAR, --lpar=LPAR

   This option is required. The report for the LPAR will be displayed.

Options for 72 (Workload Activity Report)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. option:: -c CATEGORY, --category=CATEGORY

   This option is required. It can be one of the following:

   * ``'Workload Group'``
   * ``'Service Class'``
   * ``'Report Class'``

.. option:: -x LPAR/SYSPLEX, --lpar_sysplex=LPAR/SYSPLEX

   This option is required. It can either be ``'Lpar'`` or ``'Sysplex'``. That means the report is in Lpar level or
   Sysplex level.

.. option:: -X SYSPLEX, --sysplex_name=SYSPLEX

   This option is required only if LPAR/SYSPLEX is ``'Sysplex'``. This indicates the report is for this SYSPLEX.

.. option:: -w WLM, --wlm_selected=WLM

   This option means a targeted Workload Group, Service Class or Report Class will be selected for the report.
   Defaults to ``None``, that means all will be selected.

.. option:: -z VERSION, --zos_version=VERSION

   This option is check whether its z/OS version is later than 2.2.0. Either ``'Y'`` or ``'N'`` can be specified.

.. option:: -a CPA_ACTUAL, --cpa_actual=CPA_ACTUAL

   This option is only required when z/OS version is earlier than 2.2.0. It is the physical CPU adjustment factor value.

Options for 73
--------------

.. option:: -l LPAR, --lpar=LPAR

   This option is required. The report for the LPAR will be displayed.

Options for 74
--------------

.. option:: -r REPORT-NAME, --report_type=REPORT-NAME

   This option is required. The following reports are valid:

   * ``'Cache Subsystem Activity'``,
   * ``'CF Activity'``,
   * ``'OMVS Activity'``,
   * ``'Device Activity'``,
   * ``'EADM Activity'``,
   * ``'ESS Activity'``,
   * ``'FCD Activity'``,
   * ``'HFS Statistics'``,
   * ``'PCIE Activity'``,
   * ``'XCF Activity'``

.. option:: -l LPAR, --lpar=LPAR

   This option is required. The report for the LPAR will be displayed.

.. option:: -S SSID, --ssid=SSID

   It is the target Cache Subsystem ID. This option is required if the report type is ``'Cache Subsystem Activity'`` and
   sub-report type is either ``'Cache Subsystem Status and Overview'`` or ``'Cache Device Status and Activity'``.
   Defaults to ``None``, that means all the Cache Subsystems will be reported.

.. option:: -d DEVICE, --device=DEVICE

   It is the target device type. This option is required if the report type is ``'Device Activity'``. The device can
   be the following:

   * ``'DASD'``,
   * ``'Tape'``,
   * ``'Communication Device'``,
   * ``'Graphic Device'``

.. option:: -C CF, --cf=CF

   CF is the Coupling Facility name. This option is required if the report type is ``'CF Activity'``.
   Defaults to ``None``, that means all the Coupling Facility names will be included in the report.

.. option:: -R CACHE-REPORT, --cache_report_type=CACHE-REPORT

   This option is required if the REPORT-NAME is ``'Cache Subsystem Activity'`` and the following values are valid:

   * ``'Cache Subsystem Summary'``,
   * ``'Cache Subsystem Status and Overview'``,
   * ``'Cache Device Status and Activity'``

.. option:: -H HFS-REPORT, --hfs_report_type=HFS-REPORT

   This option is required if the REPORT-NAME is ``'HFS Statistics'`` and the following values are valid:

   * ``'HFS Global Statistics'``,
   * ``'HFS File System Statistics'``

.. option:: -F SWITCH, --switch=SWITCH

   SWITCH is the FICON Directory switch name. This option is required if the report type is ``'FCD Activity'``.
   Defaults to ``None``, that means all the switch names will be included in the report.

.. option:: -E ESS-REPORT, --ess_report_type=ESS-REPORT

   This option is required if the REPORT-NAME is ``'HFS Statistics'`` and the following values are valid:

   * ``'Link Statistics'``,
   * ``'Synchronous I/O Link Statistics'``,
   * ``'Extent Pool Statistics'``,
   * ``'Rank Statistics'``

.. option:: -U CU, --cu=CU

   CU is the control unit name. This option is required if the report type is ``'ESS Activity'``.
   Defaults to ``None``, that means all the control units will be included in the report.

Options for 75
--------------

.. option:: -l LPAR, --lpar=LPAR

   This option is required. The report for the LPAR will be displayed.

Options for 77
--------------

.. option:: -l LPAR, --lpar=LPAR

   This option is required. The report for the LPAR will be displayed.

Options for 78
--------------

.. option:: -r REPORT-NAME, --report_type=REPORT-NAME

   This option is required. The following reports are valid:

   * ``'I/O Queuing Activity Report'``,
   * ``'Virtual Storage Activity Report'``

.. option:: -l LPAR, --lpar=LPAR

   This option is required. The report for the LPAR will be displayed.

.. option:: -L LCU, --lcu=LCU

   The target LCU is required if the REPORT-NAME is ``'I/O Queuing Activity Report'``. Defaults to ``None``, 
   that means all the LCUs will be included.

.. option:: -R SUB-REPORT, --sub_report_type=SUB-REPORT

   This option is required if the REPORT-NAME is ``'Virtual Storage Activity Report'`` and the following values are valid:

   * ``'Common Storage'``,
   * ``'Private Area'``

Options for 110 Subtype 1 (110_1)
---------------------------------

.. option:: -A APPLID, --applid=APPLID

   If specified, the report will display the data for this specific APPLID only. Defaults to ``'None'``.

.. option:: -x EXCLUDE-TRANS, --exclude_trans_starts=EXCLUDE-TRANS

   If specified, all the trans ID starts with EXCLUDE-TRANS will be ignored in the report. Defaults to ``'None'``.

Options for 110 Subtype 2 (110_2)
---------------------------------

.. option:: -A APPLID, --applid=APPLID

   If specified, the report will display the data for this specific APPLID only. Defaults to ``'None'``.
