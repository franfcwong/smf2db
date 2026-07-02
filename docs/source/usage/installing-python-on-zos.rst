.. _install_python_on_zos:

Install Python on z/OS
======================

This guide covers basic tutorial of how to install and configure the pax format of
IBM Open Enterprise SDK for Python. For detail instructions, please refer IBM website.

Prepare the environment
-----------------------

250MB is required to download the PAX archive file and minimum 660 MB is required to
extract and install Python. You may consider to create a zFS file to store the python
libraries and mount the file to your USS directory. The following JCL is for your reference:

.. code-block:: console

    //CREATZFS EXEC PGM=IDCAMS,REGION=1M
    //SYSPRINT DD SYSOUT=*
    //SYSUDUMP DD SYSOUT=*
    //AMSDUMP DD SYSOUT=*
    //SYSIN DD *
    DEFINE CLUSTER(NAME(<your zFS filename>) -
    CYLINDER(500 50) -
    LINEAR -
    SHAREOPTIONS(3,3) -
    VOLUME(<your vol-ser to store the zFS file>))
    /*
    //***********************************************************
    //* FORMAT — zFS FILE
    //***********************************************************
    //FORMAT EXEC PGM=IOEAGFMT,REGION=0M,
    // PARM=(‘-aggregate <your zFS filename> -compat’)
    //SYSPRINT DD SYSOUT=*
    //SYSUDUMP DD SYSOUT=*
    //STDOUT DD SYSOUT=*
    //STDERR DD SYSOUT=*
    //*
    //***********************************************************
    //* MOUNT — zFS FILE
    //***********************************************************
    //MOUNT EXEC PGM=IKJEFT01,REGION=0M
    //SYSTSPRT DD SYSOUT=*
    //SYSTSOUT DD SYSOUT=*
    //SYSTSIN DD *
    MOUNT FILESYSTEM(‘<your zFS filename>’) +
    MOUNTPOINT(‘<path to install dir>’) +
    TYPE(ZFS) MODE(RDWR) +
    PARM(‘AGGRGROW’) UNMOUNT
    /*
    //

Install the pax archive file
----------------------------

* Follow the instruction to download the python pax file
  from `IBM <https://www.ibm.com/products/open-enterprise-python-zos>`_. IBM-id
  is required to download the file and the file should be named like this
  'HAMB3xx.nonsmpe.pax.Z'.
* Create a directory <path to install dir> to hold the extracted pax file.
* Using whatever ways to upload the file to the z/OS USS file system.
* Unpax the downloaded file with the following command:

.. code-block:: console

  $ cd <path to install dir>
  $ pax -r -ppAx -f <path to downloaded paxfile>

Environment variables setup
---------------------------

Configure the PATH and LIBPATH environment variables to include the Python bin
directories with following commands:

.. code-block:: console

  export PATH=<path to install dir>/bin:$PATH
  export LIBPATH=<path to install dir>/lib:$LIBPATH
  export _BPXK_AUTOCVT='ON'
  export _CEE_RUNOPTS='FILETAG(AUTOCVT,AUTOTAG) POSIX(ON)'

.. Note:: Every time you logout and log back in you will need to set these path
   and other variables. To avoid this, you can add or update these export commands
   to .profile file in your USS home directory.

Validating Python installation
------------------------------

To confirm the Python installation has been successfully installed, run the
following command. You should be able to see the Python version as 3.x.x.

.. code-block:: console

  python --version




