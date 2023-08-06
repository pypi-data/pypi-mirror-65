--------------

Amazon CloudWatch Rule Manager
==============================

--------------

Summary
-------

Python 3 cli utility for managing CloudWatch rules via the AWS API's.
Configure:

::

    * Enable/ Disable Rules
    * Set trigger times

**Version**: 0.1.11

--------------

Contents
--------

-  `**Dependencies** <#dependencies>`__

-  `**Installation** <#installation>`__

-  `**Options** <#options>`__

-  `**Use** <#use>`__

-  `**Author & Copyright** <#author--copyright>`__

-  `**License** <#license>`__

-  `**Disclaimer** <#disclaimer>`__

--

`back to the top <#markdown-header-amazon-cloudwatch-rule-manager>`__

--------------

Dependencies
------------

Python 3 libraries
~~~~~~~~~~~~~~~~~~

-  `Python 3.6+ <https://docs.python.org/3/>`__
-  `Boto3
   SDK <https://boto3.amazonaws.com/v1/documentation/api/latest/index.html>`__
-  `awscli <https://docs.aws.amazon.com/cli/latest/reference>`__
-  `Libtools <https://github.com/fstab50/libtools>`__ General utilities
   library

Runtime Environment
~~~~~~~~~~~~~~~~~~~

-  Bash completion requires *at a minimum* Read-only permissions for the
   `'default' awscli profile
   name <https://docs.aws.amazon.com/cli/latest/topic/config-vars.html?highlight=profile%20name>`__.

--

`back to the top <#markdown-header-amazon-cloudwatch-rule-manager>`__

--------------

Installation
------------

**rulemanager** may be installed on Linux via `pip, python package
installer <https://pypi.org/project/pip>`__ in one of 3 slightly
different ways:

1. Global install **rulemanager** for a single user:

   ::

       $  pip3 install rulemanager --user

2. Global install **rulemanager** for all users (Linux):

   ::

       $  sudo -H pip3 install rulemanager

3. Installation for only 1 project (virtual environment install):

   ::

       $ cd  <project root>
       $ . p3_venv/bin/activate     # virtual env = p3_venv
       $  pip install rulemanager

Methods 1 and 2, one installation of **rulemanager** will work for all
local python 3 projects. For method 3, each python 3 project requires
its own installation of **rulemanager**.

`back to the top <#markdown-header-amazon-cloudwatch-rule-manager>`__

--------------

Options
-------

.. code:: bash

    $ rulemanager --help

|help|

--

`back to the top <#markdown-header-amazon-cloudwatch-rule-manager>`__

--------------

Use
---

**rulemanager** automatically extracts the current project name from
either DESCRIPTION.rst or MANIFEST.ln artifacts. Before issuing any of
the following commands, cd to the project root directory (top level).

1. Display all CloudWatch rules in the default AWS region:

   .. code:: bash

       $ rulemanager --view

   |all rules|

2. Display only specific CloudWatch rules matching a keyword in the
   default region:

   .. code:: bash

       $ rulemanager  --view --keyword spot

   |spec rules|

3. Display all CloudWatch rules in an alternative region:

   .. code:: bash

       $ rulemanager  --view --region us-east-1

   |alt region|

--

`back to the top <#markdown-header-amazon-cloudwatch-rule-manager>`__

--------------

Author & Copyright
------------------

All works contained herein copyrighted via below author unless work is
explicitly noted by an alternate author.

-  Copyright Blake Huber, All Rights Reserved.

`back to the top <#markdown-header-amazon-cloudwatch-rule-manager>`__

--------------

License
-------

-  Software contained in this repo is licensed under the `license
   agreement <./LICENSE.md>`__. You may display the license and
   copyright information by issuing the following command:

::

    $ rulemanager --version

.. raw:: html

   <p align="center">

::

    <a href="http://images.awspros.world/rulemanager/version-copyright.png" target="_blank"><img src="./assets/version-copyright.png">

.. raw:: html

   </p>

`back to the top <#markdown-header-amazon-cloudwatch-rule-manager>`__

--------------

Disclaimer
----------

*Code is provided "as is". No liability is assumed by either the code's
originating author nor this repo's owner for their use at AWS or any
other facility. Furthermore, running function code at AWS may incur
monetary charges; in some cases, charges may be substantial. Charges are
the sole responsibility of the account holder executing code obtained
from this library.*

Additional terms may be found in the complete `license
agreement <./LICENSE.md>`__.

`back to the top <#markdown-header-amazon-cloudwatch-rule-manager>`__

--------------

.. |help| image:: ./assets/help-menu.png
   :target: http://images.awspros.world/rulemanager/help-menu.png
.. |all rules| image:: ./assets/rules-table-all.png
   :target: http://images.awspros.world/rulemanager/rules-table-all.png
.. |spec rules| image:: ./assets/rules-table-keyword.png
   :target: http://images.awspros.world/rulemanager/rules-table-keyword.png
.. |alt region| image:: ./assets/rules-table-region.png
   :target: http://images.awspros.world/rulemanager/rules-table-region.png
