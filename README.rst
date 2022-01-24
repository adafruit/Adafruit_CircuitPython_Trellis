Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-trellis/badge/?version=latest
    :target: https://docs.circuitpython.org/projects/trellis/en/latest/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_Trellis/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_Trellis/actions/
    :alt: Build Status

This library will allow you to control the LEDs and read button presses on the `Adafruit Trellis
Board <https://www.adafruit.com/product/1616>`_. It will work with a single Trellis board, or
with a matrix of up to 8 Trellis boards.

For more details, see the `Adafruit Trellis Learn Guide <https://learn.adafruit.com/adafruit-trellis-diy-open-source-led-keypad>`_.

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython 2.0.0+ <https://github.com/adafruit/circuitpython>`_
* `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Installing from PyPI
====================

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-trellis/>`_. To install for current user:

.. code-block:: shell

    pip3 install adafruit-circuitpython-trellis

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install adafruit-circuitpython-trellis

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install adafruit-circuitpython-trellis

Usage Example
=============
See `examples/trellis_simpletest.py <https://github.com/adafruit/Adafruit_CircuitPython_Trellis/examples/trellis_simpletest.py>`_ for full
usage example.

.. code:: python

    import time
    import busio
    from board import SCL, SDA
    from adafruit_trellis import Trellis

    # Create the I2C interface
    i2c = busio.I2C(SCL, SDA)

    # Create a Trellis object for each board
    trellis = Trellis(i2c) # 0x70 when no I2C address is supplied

    # Turn on every LED
    print('Turning all LEDs on...')
    trellis.led.fill(True)
    time.sleep(2)

    # Turn off every LED
    print('Turning all LEDs off...')
    trellis.led.fill(False)
    time.sleep(2)

Documentation
=============

API documentation for this library can be found on `Read the Docs <https://docs.circuitpython.org/projects/trellis/en/latest/>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/adafruit_CircuitPython_Trellis/blob/main/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Documentation
=============

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.
