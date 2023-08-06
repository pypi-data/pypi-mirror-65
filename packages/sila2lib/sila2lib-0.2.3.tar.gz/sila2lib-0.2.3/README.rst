SiLA2 Library - a Python3 library to develop SiLA 2 Server/Clients
==================================================================

-  SiLA2 gRPC server
-  SiLA2 gRPC base class
-  SiLA2 Feature Definition Language (FDL) parsing
-  ErrorHandling
-  SiLAService Feature
-  simulation-/real mode switching by SimulationController Feature
-  zeroconfig Device Detection (not completely implemented yet)

Installation
------------

The easiest installation can be done via pip :

::

    pip install --user sila2lib  # --user option installs sila2lib for current user only

alternatively one could use the setup.py script, like:

.. code:: bash

    cd [sila_library folder containing setup.py]
    pip3 install --user -r requirements_base.txt
    python3 setup.py install

Installation on Raspberry Pi
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    pip install sila2lib

Testing the library with unittests
----------------------------------

.. code:: bash

    cd [sila_library folder containing setup.py]
    python3 setup.py test

sila2lib package Content
------------------------

std\_features
~~~~~~~~~~~~~

SiLA standard features


tests
~~~~~

unittests
