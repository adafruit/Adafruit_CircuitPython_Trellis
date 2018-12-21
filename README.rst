Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-trellis/badge/?version=latest
    :target: https://circuitpython.readthedocs.io/projects/trellis/en/latest/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://discord.gg/nBQh6qu
    :alt: Discord

.. image:: https://travis-ci.com/adafruit/Adafruit_CircuitPython_Trellis.svg?branch=master
    :target: https://travis-ci.com/adafruit/Adafruit_CircuitPython_Trellis
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

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/adafruit_CircuitPython_Trellis/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Building locally
================

Zip release files
-----------------

To build this library locally you'll need to install the
`circuitpython-build-tools <https://github.com/adafruit/circuitpython-build-tools>`_ package.

.. code-block:: shell

    python3 -m venv .env
    source .env/bin/activate
    pip install circuitpython-build-tools

Once installed, make sure you are in the virtual environment:

.. code-block:: shell

    source .env/bin/activate

Then run the build:

.. code-block:: shell

    circuitpython-build-bundles --filename_prefix adafruit-circuitpython-trellis --library_location .

Sphinx documentation
-----------------------

Sphinx is used to build the documentation based on rST files and comments in the code. First,
install dependencies (feel free to reuse the virtual environment from above):

.. code-block:: shell

    python3 -m venv .env
    source .env/bin/activate
    pip install Sphinx sphinx-rtd-theme

Now, once you have the virtual environment activated:

.. code-block:: shell

    cd docs
    sphinx-build -E -W -b html . _build/html

This will output the documentation to ``docs/_build/html``. Open the index.html in your browser to
view them. It will also (due to -W) error out on any warning like Travis will. This is a good way to
locally verify it will pass.
