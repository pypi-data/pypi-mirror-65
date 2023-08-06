Pyux - Python ux tools to ease tracking scripts
===============================================

Pyux is a set of functions and classes that help with keeping
track of what is happening during a script execution. It contains simple
but helpful classes.
`Contributions <https://pyux.readthedocs.io/en/stable/contributing.html>`__ *to the package are welcomed !*

Three modules are available :

- ``console`` provide tools to print stuff to console while a script is executing
- ``time`` provide tools in relation with time, which is measuring it or waiting for it
- ``logging`` contains a wrapper around a logger from ``logging`` module to spare you configuring one.

Installation
------------

You can download ``pyux`` from PyPi. There is only one requirement which
is package `colorama`_, which will be automatically installed with
``pyux``.

.. code:: bash

   pip install pyux-track

Demonstration script
--------------------

Once installed, the package comes with a demonstration script that you
can use to see how the available classes behave. The demo is exhaustive
and interactive so you can skip some sections if you want, or quit it
if you get bored. Launch the demo by typing in a terminal :

.. code:: bash

   python -m pyux

Please note that the demo does not provide any information on how to
use the classes : you will find detailed explanations in the 
`documentation <https://pyux.readthedocs.io/en/stable/index.html>`__.

.. _colorama: https://pypi.org/project/colorama
