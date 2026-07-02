.. _getting started:

Getting started
===============

This section covers basic tutorials of smf2db including:

* `Installation`_.
* `Printing the report`_.
* `Configuring database`_.
* `Initializing database`_.
* `Uploading data to DB`_.
* `Initializing sumup database`_.
* `Summing up database`_.

Installation
------------

If you already know how to install python packages, then you can simply create a Python virtual environment and
install the package like this:

.. code-block:: console

    pip install smf2db

.. seealso::

   Refer to the :doc:`installation` for more detail instructions.

Printing the report
-------------------

Assuming that you have had some SMF JSON files, (if not, please following the instructions on
`CBTTape <https://cbttape.org/ftp/cbt/CBT1064.zip>`__ to get ready of some SMF JSON files,)
let's print the reports to have an overview of your data. It is started with the :program:`report` program:

.. code-block:: console

   smf2db report <smf type> <jsonfiles> -o <outfile>

where *smf type* is the ``SMF type`` (e.g. 30, 70, 123, etc) and *jsonfiles* is the
JSON files in which you want to print the report.
The ``-o <outfile>`` option outputs the report to a file *outfile*.

|

.. collapse:: The following table is a reference of the corresponding reports supported:

    ============ =========== ===================================
    **SMF Type** **Subtype** **Report**
    ------------ ----------- -----------------------------------
         30      1,2,3,4,5,6 Address Space Activity
         70           1      CPU Activity
         ''           2      Cryptographic Hardware Activity
         71           1      Paging Activity
         72           3      Workload Activty
         ''           5      Serialization Delay
         73           1      Channel Path Activity
         74           1      Device Activity
         ''           2      XCF Activity
         ''           3      OMVS Activity
         ''           4      CF Activity
         ''           5      Cache Subsystem Activity
         ''           6      HFS Statistics
         ''           7      FCD Activity
         ''           8      ESS Activity
         ''           9      PCIE Activity
         ''          10      EADM Activity
         75           1      Page Data Set Activity
         77           1      Enqueue Activity
         78           2      Virtual Storage Activity
         ''           3      I/O Queuing Activity
        110           1      CICS Performance Summary
         ''           2      CICS Statistics Summary
        123           1      z/OS Connect EE Requeust Overview
    ============ =========== ===================================

.. seealso::

   Refer to the :doc:`smf2db man page </man/report>`
   for all options that :program:`report` supports.

Usage Examples
~~~~~~~~~~~~~~

|

Print smf 70 CPU Activity report
""""""""""""""""""""""""""""""""

By running the following command on the terminal or by JCL on z/OS:

.. tab-set::

    .. tab-item:: terminal

        .. code-block:: console

            smf2db report 70 smf70.json -t 'CPU Activity Report' -l S0W1

        .. tip::

           To avoid issues of report is too wide or too long,
           it is advisable to output the report to a file like this::

            smf2pgdb report 70 smf70.json -t 'CPU Activity Report' -l S0W1 -o cpu_report.txt

    .. tab-item:: JCL

        For z/OS platform, you can also run a batch job to output the report in USS
        using a JCL like this:

           .. code-block:: text

              //PYJOB    EXEC PGM=BPXBATCH,REGION=0M
              //SYSPRINT DD SYSOUT=*
              //STDERR   DD SYSOUT=*
              //STDOUT   DD SYSOUT=*
              //STDPARM  DD *
              sh
              <smf2db path>
              report
              70
              <json files full path>
              -r "CPU Activity Report"
              -l <lpar name>
              -o <output file full path>
              /*

        where *smf2db path* is the absoulte path where **smf2db** installed, say, /u/myuser/.venv/bin/smf2db and
        *json files full path* is the JSON files in which you want to print the report. The *lpar name* is the
        target lpar name of this report and finally, the *output file full path* is the full path of output report.

.. collapse:: You will see the following content on your screen or in your output file:

    .. code-block:: text

                                                                 C P U  A C T I V I T Y

                      z/OS V2R4                 System ID S0W1             Date 07/27/2021               Interval 29:59.996
                                                RMF Version 796            Time 10.00.00                 Cycle 1.000 Seconds
        CPU        1090       CPC Capacity     0       Sequence Code 000000000000ABCD
        Model      306                                 Hiperdispatch=Yes
        H/W Model  L06        Change Reason=N/A        Boost Type=None    Boost Class=None
          ---CPU---       ---------------- Time % ----------------     Log Proc          --I/O Interrupts--
        Num    Type       Online      Lpar Busy    MVS Busy  Parked    Share %            Rate    % Via TPI
         0      CP        100.00           4.24        3.49    0.00     -----             5.71         0.25
         1      CP        100.00           2.55        1.87    0.00     -----             2.11         0.18
         2      CP        100.00           5.91        4.70    0.00     -----             1.28         0.39
        Total  /Average:                   4.23        3.35             -----             9.1          0.83
         3     IIP        100.00           6.85        5.70    0.00     -----
         4     IIP        100.00           1.36        0.69    0.00     -----
         5     IIP        100.00           0.89        0.21    0.00     -----
        Total  /Average:                   3.03        2.20             -----

                                                                  C P U  A C T I V I T Y

                      z/OS V2R4                 System ID S0W1             Date 07/27/2021               Interval 29:59.996
                                                RMF Version 796            Time 10.00.00                 Cycle 1.000 Seconds
        System Address Space And Work Unit Analysis
        ---------Number of Address Spaces-----------      -----------------------Distribution of In-Ready Work Unit Queue--------------
        Queue Types                 Min    Max    Avg  Number of       (%)  0    10   20   30   40   50   60   70   80   90   100
                                                       Work Units           !....!....!....!....!....!....!....!....!....!....!
        IN                           54     56   54.2
        IN READY                      0      3    0.2  <=  N           100  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                                                        =  N +  1        0
        OUT READY                     0      0    0.0   =  N +  2        0
        OUT WAIT                      0      0    0.0   =  N +  3        0
                                                       <=  N +  5        0
        LOGICAL OUT RDY               0      0    0.0  <=  N + 10        0
        LOGICAL OUT WAIT             14     16   15.8  <=  N + 15        0
                                                       <=  N + 20        0
        Address Space Types                            <=  N + 30        0
                                                       <=  N + 40        0
        BATCH                         0      0    0.0  <=  N + 60        0
        STC                          68     68   68.0  <=  N + 80        0
        TSO                           0      0    0.0  <=  N + 100       0
        ASCH                          0      0    0.0  <=  N + 120       0
        OMVS                          2      2    2.0  <=  N + 150       0
                                                       >   N + 150       0

        ---------Number of Work Units-------------
        CPU Types      Min        Max        Avg  N = Number of processors online unparked ( 6.0 on avg)
        CP               0          5        0.1
        IIP              0          3        0.1

        Blocked Workload Analysis
        OPT Parameters: BLWLTRPCT (%)  0.5  Promote Rate:  Defined  1  Waiters for Promote:  Avg  0
                            BLWLINTHD   20                Used (%)  0                       Peak  0

                                                      P A R T I T I O N  D A T A  R E P O R T

                      z/OS V2R4                 System ID S0W1             Date 07/27/2021               Interval 29:59.996
                                                RMF Version 796            Time 10.00.00                 Cycle 1.000 Seconds
        MVS Partition Name               SYSPLEX     Phys Proc Num  6         Group Name  DEFAULT         Initial Cap   YES
        Image Capacity                        18                CP  6         Limit         0             Lpar HW Cap   NO
        Number of Configured Partitions        1                              Available     0             HW Group Cap  NO
        Wait Completion                       NO                                                          ABS MSU Cap   NO
        Dispatch Interval                Dynamic
        --------------------- Partition Data ---------------------  ---- Logical Partition Processor Data ---  ------ Average Processor Utilization Percentages ------
                                       ----MSU----    --Capping---  --Processor--  ----Dispatch Time Data----    Logical Processors  ------ Physical Processors ------
        Name         S    BT      Wgt    Def    Act   Def     WLM%    Num   Type    Effective       Total        Effective    Total    Lpar Mgmt    Effective    Total
        SYSPLEX      A    N       950      0      0  Y N N     0.0      3    CP    00.03.37.095  00.03.48.521         4.02     4.23         0.11         2.01     2.12
        *PHYSICAL*                                                                               00.00.07.843                               0.07                  0.07
                               ------                                              ------------  ------------                              -----       ------    -----
        Total                     950                                              00.03.37.095  00.03.56.364                               0.18         2.01     2.19

        SYSPLEX      A    N       950                Y N N              3   IIP    00.02.35.461  00.02.43.643         2.88     3.03         0.00         0.00     0.00
                               ------                                              ------------  ------------                              -----       ------    -----
        Total                     950                                              00.02.35.461  00.02.43.643                               0.00         0.00     0.00


        Printing smf70 report was completed.


.. _Configuring database:

Configuring Database
--------------------

This section is for those who would like to use the :program:`upload` function. (It will not
cover how to `install and use PostgreSQL <https://www.postgresql.org/docs/current/tutorial-install.html>`_.)

**smf2db** comes with a script called :program:`initcfg` that create a yaml file, say, :file:`config.yaml` in
your preferred config directory, which you can configure all aspects of databases which will be used later for
uploading to the database . The configuration values are set from a few queustions it asks you. Currently, only
three db drivers are supported: ``sqlite``, ``pg8000`` and ``psycopg2`` and it depends on whether it is supported
on your platform. In addition, you can choose which partition scheme for your database according to
your data volume: ``no partition``, ``weekday``, ``day of month`` and ``week number``. Here is how to run this:

.. tab-set::

    .. tab-item:: terminal

        .. code-block:: console

           smf2db db initcfg --config_file <config file path>

    .. tab-item:: JCL

        For z/OS platform, you can run a batch job to create the config yaml file using a JCL like this:

           .. code-block:: text

              //PYJOB    EXEC PGM=BPXBATCH,REGION=0M
              //SYSPRINT DD SYSOUT=*
              //STDERR   DD SYSOUT=*
              //STDOUT   DD SYSOUT=*
              //STDPARM  DD *
              sh
              <smf2db path>
              db
              initcfg
              --config_fle <config file path>
              --db_driver <db driver>
              --sqlite_path <sqlite db path>
              --partitions "<partition scheme>"
              --db_prefix "<database name prefix>"

where *config file path* is the target config file in full path or relative path with extension ``yaml`` and
it will be overrided if exist.

.. seealso::

   Refer to the :doc:`smf2db man page </man/initcfg>`
   for all options that :program:`initcfg` supports.


.. _Initializing database:

Initializing database
---------------------

After creating the config yaml file using :ref:`Configuring database`, you will need to run :program:`initdb`.
It will create the corresponding schemas, databases and tables in your chosen DBMS. You can initialize multiple smf types
in one go. To do this, run:

.. tab-set::

    .. tab-item:: terminal

        .. code-block:: console

           smf2db db initdb <smf type> --config_file <config file>

        .. warning::
           This script will drop and recreate the tables if they are exist in your database with
           the same names.

    .. tab-item:: JCL

        For z/OS platform, you can run a batch job to initialize the databases using a JCL like this:

           .. code-block:: text

              //PYJOB    EXEC PGM=BPXBATCH,REGION=0M
              //SYSPRINT DD SYSOUT=*
              //STDERR   DD SYSOUT=*
              //STDOUT   DD SYSOUT=*
              //STDPARM  DD *
              sh
              echo y |
              <smf2db path>
              db
              initdb
              <smf type list>
              --config_fle <config file path>

where *smf type* is the ``SMF type`` (e.g. 30, 70, 123, etc) and *config file* is the target config file in
full path or relative path with extension ``yaml`` which must be exist before running.

.. seealso::

   Refer to the :doc:`smf2db man page </man/initdb>`
   for all options that :program:`initdb` supports.


.. _Uploading data to DB:

Uploading data to DB
--------------------

Assuming that you have had some SMF JSON files, (if not, please following the instructions on
`CBTTape <https://cbttape.org/ftp/cbt/CBT1064.zip>`__ to get ready of some SMF JSON files,) and you have
run the :ref:`Initializing database`, you can now upload the data to your chosen DBMS based on the :file:`config.yaml`.
It is started with the :program:`upload` program which is an interactive script which will prompt you for user ID
and password to connect to the database if you are using PostgreSQL and you does not provide it on the command like this:

.. tab-set::

    .. tab-item:: terminal

        .. code-block:: console

           smf2db db upload <smf type> <jsonfiles> --config_file <config file>

    .. tab-item:: JCL

        For z/OS platform, you can run a batch job to upload data to database using a JCL like this:

           .. code-block:: text

              //PYJOB    EXEC PGM=BPXBATCH,REGION=0M
              //SYSPRINT DD SYSOUT=*
              //STDERR   DD SYSOUT=*
              //STDOUT   DD SYSOUT=*
              //STDPARM  DD *
              sh
              <smf2db path>
              db
              upload
              <smf type>
              <json files>
              --config_fle <config file path>

where *smf type* is the ``SMF type`` (e.g. 30, 70, 123, etc), *jsonfiles* is the
JSON files in which you want to upload and *config file* is the target config file in full path or relative path
with extension ``yaml`` which must be exist before running.

.. seealso::

   Refer to the :doc:`smf2db man page </man/upload>`
   for all options that :program:`upload` supports.

Usage Examples
~~~~~~~~~~~~~~

Upload smf 70
"""""""""""""

By running the following command or submiting the JCL:

.. tab-set::

    .. tab-item:: terminal

        .. code-block:: console

            smf2db db upload 70 smf70_1.json smf70_2.json --config_file configs/config.yaml

    .. tab-item:: JCL

        .. code-block:: text

              //PYJOB    EXEC PGM=BPXBATCH,REGION=0M
              //SYSPRINT DD SYSOUT=*
              //STDERR   DD SYSOUT=*
              //STDOUT   DD SYSOUT=*
              //STDPARM  DD *
              sh
              /u/myuser/.venv/bin/smf2db
              db
              upload
              70
              /u/myuser/data/smf70_1.json
              /u/myuser/data/smf70_2.json
              --config_fle /u/myuser/configs/config.yaml

You will see something like the following content on your screen or job output, which is, the ``Execution time`` for
each of the JSON file and the total number of records added to each of the tables after the process will be shown.

.. code-block:: text

   Execution time (/u/myuser/data/smf70_1.json): 0.043489535649617515 minutes
   Execution time (/u/myuser/data/smf70_2.json): 0.012916600704193116 minutes
   Upload Result (table name: row count): {'smf70_pro': 204, 'smf70_ctl': 102, 'smf70_cpu': 372, 'smf70_aid': 102, 'smf70_bct': 1212, 'smf70_bct_cpu': 1266, 'smf70_bpd': 4008, 'smf70_trg': 0, 'smf70_ccf': 102, 'smf70_typ3': 96, 'smf70_typ4': 96, 'smf70_typ5': 0}

.. note::

   smf70 data is the pre-requsite of smf30 and other smf7x data. If you prepare to upload these data to
   database, you are required to upload smf70 data first.

.. _Initializing sumup database:

Initializing sumup database
---------------------------

After creating the config yaml file by running :ref:`Configuring database` and loading interval data to database from
:ref:`Uploading data to DB`, you can sum up the interval data in database by running :program:`initsum` to initialize
the sumup database. It will create the corresponding schemas, databases and tables in your chosen DBMS. There are three
summary levels you can choose: 15-minute, hourly and daily although only some smf-types support 15-minute.
To use this, run:

.. tab-set::

    .. tab-item:: terminal

        .. code-block:: console

           smf2db db initsum <smf type> <summary level> --config_file <config file>

    .. tab-item:: JCL

        For z/OS platform, you can also run a batch job to initialize summary database using a JCL like this:

           .. code-block:: text

              //PYJOB    EXEC PGM=BPXBATCH,REGION=0M
              //SYSPRINT DD SYSOUT=*
              //STDERR   DD SYSOUT=*
              //STDOUT   DD SYSOUT=*
              //STDPARM  DD *
              sh
              echo y |
              <smf2db path>
              db
              initsum
              <smf type>
              <summary level>
              --config_fle <config file path>

where *smf type* is the ``SMF type`` (e.g. 30, 70, 123, etc), *summary level* is either 15-min, hourly or daily
depends on what you want to sumup and *config file* is the target config file in full path or relative path
with extension ``yaml`` which must be exist before running.

.. warning::
   This script will drop and recreate the summary tables if they are exist in your database with
   the same names.

.. seealso::

   Refer to the :doc:`smf2db man page </man/initsum>`
   for all options that :program:`initsum` supports.

.. _Summing up database:

Summing up database
-------------------

Assuming that you have uploaded some SMF JSON files to database, (if not, please following the instructions on
:ref:`Uploading data to DB` to get ready of the interval databases,) and you have run the :ref:`Initializing sumup database`
to initialize the database, you can now sum up the database to a specified summary level. It is started with the
:program:`sumup` program which is an interactive script and will prompt you for user ID and password to connect to
the database if you are using PostgreSQL and does not provide it on the command like this:

.. tab-set::

    .. tab-item:: terminal

        .. code-block:: console

           smf2db db sumup <smf type> --summary_levl <summary level> --config_file <config file>

    .. tab-item:: JCL

        For z/OS platform, you can also run a batch job to summarize the database in different supported summary
        level using a JCL like this:

           .. code-block:: text

              //PYJOB    EXEC PGM=BPXBATCH,REGION=0M
              //SYSPRINT DD SYSOUT=*
              //STDERR   DD SYSOUT=*
              //STDOUT   DD SYSOUT=*
              //STDPARM  DD *
              sh
              <smf2db path>
              db
              sumup
              <smf type>
              --summary_lvel <summary level>
              --config_fle <config file path>

where *smf type* is the ``SMF type`` (e.g. 30, 70, 123, etc), *summary level* is either 15-min, hourly or daily
depends on what summary level you want to sumup and *config file* is the target config file in full path or relative path
with extension ``yaml`` which must be exist before running.

.. seealso::

   Refer to the :doc:`smf2db man page </man/sumup>`
   for all options that :program:`sumup` supports.