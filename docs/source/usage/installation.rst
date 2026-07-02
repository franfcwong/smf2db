.. _installation:

Installing smf2db
=================

This is a CLI application that does upload SMF JSON files to database,
summarization and printing reports on the fly without loading to database management system (DBMS).
This section covers how to install it.

.. _installing_requirements:

Requirements for Installing smf2db
----------------------------------

This section describes the steps to follow before installing smf2db.

* Ensure you can run Python from the command line

    Before you go any further, make sure you have Python and that the expected
    version is available from your command line. You can check this by running:

    .. tab-set::

        .. tab-item:: z/OS

            .. code-block:: console

                python3 --version

        .. tab-item:: Unix/macOS

            .. code-block:: console

                python3 --version

        .. tab-item:: Windows

            .. code-block:: console

                py --version


    You should get some output like ``Python 3.13.0``. If you do not have Python,
    please refer to :doc:`installing-python-on-zos`
    to download and install on z/OS platform. For other platforms,
    please install the latest 3.x version from `python.org`_.


* Creating Virtual Environments

    It is recommended smf2db to be installed in a virtual environment, rather than being installed
    globally. This section discusses the basic of how to create and activate a virtual environment using
    the standard library's virtual environment tool ``venv`` and install pre-requisite packages and smf2db.
    You can use other virtual environment tools if you prefer.

    To create a virtual environment, go to your project's directory and run the
    following command. This will create a new virtual environment in a local folder
    named ``myvenv``:

    .. tab-set::

        .. tab-item:: z/OS

            .. code-block:: console

                python3 -m venv myvenv

        .. tab-item:: Unix/macOS

            .. code-block:: console

                python3 -m venv myvenv

        .. tab-item:: Windows

            .. code-block:: console

                py -m venv myvenv


    The second argument is the location to create the virtual environment. Generally, you
    can just create this in your project and call it ``myvenv``.

    ``venv`` will create a virtual Python installation in the ``myvenv`` folder.

* Activate a virtual environment

    Before you can start installing or using packages in your virtual environment you'll
    need to ``activate`` it. Activating a virtual environment will put the
    virtual environment-specific ``python`` and ``pip`` executables into your
    shell's ``PATH``.

    .. tab-set::

        .. tab-item:: z/OS

            .. code-block:: console

                source myenv/bin/activate

        .. tab-item:: Unix/macOS

            .. code-block:: console

                source myvenv/bin/activate

        .. tab-item:: Windows

            .. code-block:: console

                myvenv\Scripts\activate


    While a virtual environment is activated, pip will install packages into that
    specific environment. This enables you to use packages in this Python application.

    * Deactivate a virtual environment

        If you want to switch projects or leave your virtual environment,
        ``deactivate`` the environment:

        .. code-block:: console

            deactivate

        .. note::
            Closing your shell will deactivate the virtual environment. If
            you open a new shell window and want to use the virtual environment,
            reactivate it.

    * Reactivate a virtual environment

        If you want to reactivate an existing virtual environment, follow the same
        instructions about activating a virtual environment. There's no need to create
        a new virtual environment.


Prepare pip
~~~~~~~~~~~

``pip`` is the reference Python package manager.
It's used to install and update packages into a virtual environment.

.. tab-set::

    .. tab-item:: z/OS

        The Python libraries for z/OS should include pip. You can check the pip version
        by running:

        .. code-block:: console

            python -m pip --version

    .. tab-item:: Unix/macOS

        The Python installers for macOS include pip. On Linux, you may have to install
        an additional package such as ``python3-pip``. You can make sure that pip is
        up-to-date by running:

        .. code-block:: console

            python3 -m pip install --upgrade pip
            python3 -m pip --version

    .. tab-item:: Windows

        The Python installers for Windows include pip. You can make sure that pip is
        up-to-date by running:

        .. code-block:: bat

            py -m pip install --upgrade pip
            py -m pip --version


Use pip for Installing smf2db
-----------------------------

``pip`` is the recommended installer.  smf2db currently is published on `PyPI <https://pypi.org/project/smf2db>`_,
which included source archive file format and pre-built wheel format. Below, we'll cover the most common usage scenarios.

If you install ``smf2db`` on z/OS, it is required to install the pre-requisite packages before installing smf2db.

Following the instructions below to install the pre-requistie packages:

.. tab-set::

    .. tab-item:: z/OS

        The following packages are required to follow :doc:`install-python-ai-toolkit-for-zos` to install to
        your z/OS environment::

            click
            numpy
            pandas
            SQLALchemy
            packaging
            jsonschema
            pyyaml

        For the other packages as shown below, you can download the .whl (wheel) files published on the
        `Python Package Index`_ (PyPI) to your local machine and upload the wheel files
        to z/OS::

            rich >= 14.3.2
            tabulate == 0.9.0

        Then, you run the following comand

        .. code-block:: console

            pip install <some-package.whl>

        Or if you can access the `Python Package Index`_ (PyPI) directly on z/OS, you can create another
        :file:`requirements2.txt` and run the following command::

            pip install -r requirements2.txt

    .. tab-item:: Unix/macOS

        The dependencies listed below will be automatically pulled from `Python Package Index`_ (PyPI) or your
        corporate site::

            click >= 8.1.3
            numpy >= 1.23.4
            pandas >= 1.5.1
            SQLALchemy >= 2.0.12
            packaging >= 25.0
            jsonschema >= 4.17.3
            pyyaml >= 6.0.3
            rich >= 14.3.2
            tabulate == 0.9.0

        Otherwise, you can download the .whl (wheel) files using a machine which has access to PyPI and transfer
        the files to your local machine and run the following command one by one for each .whl file:

        .. code-block:: console

            pip install <some-package.whl>

    .. tab-item:: Windows

        The dependencies listed below will be automatically pulled from `Python Package Index`_ (PyPI) or your
        corporate site::

            click >= 8.1.3
            numpy >= 1.23.4
            pandas >= 1.5.1
            SQLALchemy >= 2.0.12
            packaging >= 25.0
            jsonschema >= 4.17.3
            pyyaml >= 6.0.3
            rich >= 14.3.2
            tabulate == 0.9.0

        Otherwise, you can download the .whl (wheel) files using a machine which has access to PyPI and transfer
        the files to your local machine and run the following command one by one for each .whl file:

        .. code-block:: console

            pip install <some-package.whl>

After installation of pre-requiste python packages, smf2db can be installed in one of the ways described
below:

.. _install-wheel:

Installation from wheel
~~~~~~~~~~~~~~~~~~~~~~~

Following the instructions below to install the smf2db in wheel format:

.. tab-set::

    .. tab-item:: z/OS

        Upload the wheel files to z/OS and run the following comand

        .. code-block:: console

            pip install <smf2db.whl>

    .. tab-item:: Unix/macOS

        Run the following command:

        .. code-block:: console

            pip install <smf2db.whl>

    .. tab-item:: Windows

        Run the following command:

        .. code-block:: console

            pip install <smf2db.whl>


.. _install-pypi:

Installing from PyPI
~~~~~~~~~~~~~~~~~~~~

In the future, smf2db package will be published on the `Python Package Index`_
(PyPI).  The preferred tool for installing packages from PyPI is :command:`pip`,
which is included in all modern versions of Python.

Run the following command if your machine can access PyPI directly::

   $ pip install -U smf2db


Installation from local archives
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install source archive file downloaded from PyPI.

.. tab-set::

    .. tab-item:: z/OS

        Upload the archive file to target virtual environment on z/OS and run the following comand

        .. code-block:: console

            python3 -m pip install install <smf2db-0.1.0.tar.gz>

    .. tab-item:: Unix/macOS

        .. code-block:: bash

            python3 -m pip install <smf2db-0.1.0.tar.gz>

    .. tab-item:: Windows

        .. code-block:: bat

            py -m pip install <smf2db-0.1.0.tar.gz>



After installation, you can check that smf2db is available by running ::

   $ smf2db --version

This should print out the smf2db version number.



.. _python.org: https://www.python.org
.. _Python Package Index: https://pypi.org