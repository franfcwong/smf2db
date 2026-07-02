Install Packages from IBM Python AI Toolkit for z/OS
====================================================

This guide covers basic tutorial of how to acquire Python packages from
IBM Python AI Toolkit for z/OS to your z/OS environment. For detail instructions,
please refer IBM website.

Configure a user pip.conf
-------------------------

Create a file $HOME/.config/pip/pip.conf that has these contents:

.. code-block:: console

  [global]
  index = https://downloads.pyaitoolkit.ibm.net:443/repository/python_ai_toolkit_zos/
  index-url = https://downloads.pyaitoolkit.ibm.net:443/repository/python_ai_toolkit_zos/simple
  trusted-host = downloads.pyaitoolkit.ibm.net

This will provide defaults that prevent you from unintentionally referencing the
default python package repository at pypi.org. If you you can't access IBM website using this, your site's firewall
might be blocking it. If it is so, get your network team's advice for the proxy server setting and
try the following pip.conf instead:

.. code-block:: console

  [global]
  index = https://downloads.pyaitoolkit.ibm.net:443/repository/python_ai_toolkit_zos/
  index-url = https://downloads.pyaitoolkit.ibm.net:443/repository/python_ai_toolkit_zos/simple
  trusted-host = downloads.pyaitoolkit.ibm.net
  proxy = <your proxy server IP>:<your proxy server port number>

Install the required packages
-----------------------------

Packages included in this AI Toolkit is available at
`IBM Python AI Toolkit Web Interface`_. The
packages required by Smf2pgdb from IBM Python AI Tookkit are shown below.

.. code-block:: console

  click
  numpy
  pandas
  SQLALchemy
  typing_extensions
  python_dateutil
  pytz
  packaging


You can follow the advice in IBM website to create the requirements.txt as shown below
with the ``hash=SHA`` setting::

  touch requirements.txt
  chtag -tc iso8859-1 requirements.txt

After copying the packages shown above into the requirements.txt with the hash information, run
the following comand to install it::

  pip install -r requirements.txt

Or simply install the packages one by one using the following command::

  pip install <package>


.. _IBM Python AI Toolkit Web Interface: https://ibm-z-oss-oda.github.io/python_ai_toolkit_zos