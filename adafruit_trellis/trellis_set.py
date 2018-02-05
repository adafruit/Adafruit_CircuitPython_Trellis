#  This is a library for the Adafruit Trellis w/HT16K33
#
#  Designed specifically to work with the Adafruit Trellis
#  ----> https://www.adafruit.com/products/1616
#  ----> https://www.adafruit.com/products/1611
#
#  These displays use I2C to communicate, 2 pins are required to
#  interface
#  Adafruit invests time and resources providing this open source code,
#  please support Adafruit and open-source hardware by purchasing
#  products from Adafruit!
#
#  Written by Limor Fried/Ladyada for Adafruit Industries.
#  MIT license, all text above must be included in any redistribution
#
#  Also utilized functions from the following two libraries:
#  - CircuitPython HT16K33 library written by Radomir Dopieralski &
#    Tony DiCola for Adafruit Industries
#    https://github.com/adafruit/Adafruit_CircuitPython_HT16K33
#
#  - Python Trellis library written by Tony DiCola
#    https://github.com/tdicola/Adafruit_Trellis_Python
#
#  CircuitPython Library Author: Michael Schroeder(sommersoft). No
#  affiliation to Adafruit is implied.
"""
`adafruit_trellis.tellis_set` - Adafruit Trellis Monochrome 4x4 LED Backlit Keypad
===================================================================================

CircuitPython library to support Adafruit's Trellis Keypad.

* Author(s): Limor Fried, Radomir Dopieralski, Tony DiCola,
             and Michael Schroeder

Implementation Notes
--------------------

**Hardware:**

* Adafruit `Trellis Monochrome 4x4 LED Backlit Keypad
  <https://www.adafruit.com/product/1616>`_ (Product ID: 1616)

**Software and Dependencies:**

* Adafruit CircuitPython firmware (2.2.0+) for the ESP8622 and M0-based boards:
  https://github.com/adafruit/circuitpython/releases
* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
* Adafruit_CircuitPython_Trellis base library (trellis.py)
"""

__version__ = "1.0.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_Trellis.git"


class MATRIX(object):
    """
    Driver base for a matrix of Trellis Boards (up to 8)
    See Trellis product guide for using different/multiple I2C addresses.
    https://learn.adafruit.com/adafruit-trellis-diy-open-source-led-keypad

    :param ~trellis.TRELLIS object: A list of `trellis.TRELLIS` objects to
                                    use in the matrix. Each object needs its
                                    own I2C address.

    Example:

    .. code-block:: python

        import time
        import busio
        from board import SCL, SDA
        from adafruit_trellis import trellis
        from adafruit_trellis import trellis_set

        i2c = busio.I2C(SCL, SDA)
        matrix1 = trellis.TRELLIS(i2c) #omitting the address defaults to 0x70
        matrix2 = trellis.TRELLIS(i2c, 0x72)
        trelly = trellis_set.MATRIX(matrix1, matrix2)

        while True:
            try:
                if trelly.read_buttons():
                    for i in range(32):
                        if trelly.just_pressed(i):
                            print('Button', i + 1, 'was just pressed!')
                            trelly.led_on(i)
                            trelly.show()
                    for i in range(32):
                        if trelly.just_released(i):
                            print('Button', i + 1, 'was just released!')
                            trelly.led_off(i)
                            trelly.show()
            except KeyboardInterrupt:
                break
            time.sleep(.1)
    """

    def __init__(self, *matrices):
        self._matrices = []
        if not matrices:
            raise ValueError('You must include at least one Trellis object.')
        elif len(matrices) > 8:
            raise ValueError('A maximum of 8 Trellis objects can be used. You',
                             'have attempted to use:', len(matrices))

        for matrix in matrices:
            if matrix.__qualname__ != 'TRELLIS':
                raise ValueError('Only Trellis objects can be used with a MATRIX.',
                                 matrix, 'is not a Trellis object.')
            if matrix not in self._matrices:
                self._matrices.append(matrix)
            else:
                print(matrix, 'already added to matrices. Moving to next.')

    def _get_matrix(self, position):
        """
        Get the matrix for the associated global LED/key position.
        Returns a tuple with matrix, and local position inside that matrix.
        If position is not within the range of possible values, returns None.
        """
        if position > (16 * len(self._matrices)) or position < 0:
            # pylint: disable=multiple-statements
            return None, None
            # pylint: enable=multiple-statements
        matrix = int(position / 16)
        offset = position % 16
        return self._matrices[matrix], offset

    def blink_rate(self, rate, *matrices):
        """
        Set the blink rate.

        :param int brightness: Range 0-3.
        :param ~trellis.TRELLIS object(s): list of `trellis.TRELLIS` objects
                                           you wish to change the blink rate
                                           of. Only required if you don't want
                                           to update ALL `trellis_set.MATRIX`
                                           objects.

        """
        if not matrices:
            for matrix in self._matrices:
                matrix.blink_rate(rate)

        for matrix in matrices:
            matrix.blink_rate(rate)

    def brightness(self, brightness, *matrices):
        """
        Set the brightness.

        :param int brightness: Range 0-15.
        :param ~trellis.TRELLIS object(s): list of `trellis.TRELLIS` objects
                                           you wish to change the brightness
                                           of. Only required if you don't want
                                           to update ALL `trellis_set.MATRIX`
                                           objects.
        """
        if not matrices:
            for matrix in self._matrices:
                matrix.brightness(brightness)

        for matrix in matrices:
            matrix.brightness(brightness)

    def show(self, *matrices):
        """
        Refresh the matrix and show the changes.

        :param ~trellis.TRELLIS *matrices: List of `trellis.TRELLIS` objects
                                           you wish refresh.
                                           Only required if you want to turn
                                           on an LED on a specific Trellis
                                           board.
        """
        if not matrices:
            for matrix in self._matrices:
                matrix.show()

        for matrix in matrices:
            matrix.show()

    def led_on(self, x, *matrices):
        """
        Turn on the specified LED in the display buffer. Must call
        `[trellis].show()` afterwards to update the matrix.

        :param int x: Number of LED you wish to turn on. When not including
                      specific `trellis.TRELLIS` objects (`*matrices` param),
                      the range of `x` is 0 to the maximum number of LEDs you
                      have (4 Trellis boards: 0-63). When using `*matrices`,
                      the range of `x` is 0-15 for the LED on each Trellis.

        :param ~trellis.TRELLIS *matrices: List of `trellis.TRELLIS` objects
                                           you wish to turn on the LED `x`.
                                           Only required if you want to turn
                                           on an LED on a specific Trellis
                                           board.
        """
        if not matrices:
            # pylint: disable=multiple-statements
            matrix, led = self._get_matrix(x)
            # pylint: enable=multiple-statements
            if matrix is None:
                return False
            return matrix.led_on(led)

        for matrix in matrices:
            return matrix.led_on(x)

    def led_off(self, x, *matrices):
        """
        Turn off the specified LED in the display buffer. Must call
        `[trellis].show()` afterwards to update the matrix.

        :param int x: Number of LED you wish to turn off. When not including
                      specific `trellis.TRELLIS` objects (`*matrices` param),
                      the range of `x` is 0 to the maximum number of LEDs you
                      have (4 Trellis boards: 0-63). When using `*matrices`,
                      the range of `x` is 0-15 for the LED on each Trellis.

        :param ~trellis.TRELLIS *matrices: List of `trellis.TRELLIS` objects
                                           you wish to turn off the LED `x`.
                                           Only required if you want to turn
                                           off an LED on a specific Trellis
                                           board.
        """
        if not matrices:
            # pylint: disable=multiple-statements
            matrix, led = self._get_matrix(x)
            # pylint: enable=multiple-statements
            if matrix is None:
                return False
            return matrix.led_off(led)

        for matrix in matrices:
            return matrix.led_off(x)

    def led_status(self, x, *matrices):
        """
        Gives the current status of an LED: True == ON, False == OFF

        :param int x: Number of LED you wish to check. When not including
                      specific `trellis.TRELLIS` objects (`*matrices` param),
                      the range of `x` is 0 to the maximum number of LEDs you
                      have (4 Trellis boards: 0-63). When using `*matrices`,
                      the range of `x` is 0-15 for the LED on each Trellis.

        :param ~trellis.TRELLIS *matrices: List of `trellis.TRELLIS` objects
                                           you wish to check the LED `x`.
                                           Only required if you want to check
                                           an LED on a specific Trellis board.
        """
        if not matrices:
            # pylint: disable=multiple-statements
            matrix, led = self._get_matrix(x)
            # pylint: enable=multiple-statements
            if matrix is None:
                return False
            return matrix.led_status(led)

        for matrix in matrices:
            return matrix.led_status(x)

    def fill(self, color, *matrices):
        """
        Fill the whole board/matrix with the given color.

        :param int color: 0 == OFF, > 0 == ON

        :param ~trellis.TRELLIS *matrices: List of `trellis.TRELLIS` objects
                                           you wish to fill with the given color.
                                           Only required if you want to fill
                                           the color on a specific Trellis board.
        """
        if not matrices:
            for matrix in self._matrices:
                matrix.fill(color)

        for matrix in matrices:
            matrix.fill(color)

    def read_buttons(self, *matrices):
        """
        Read the button matrix register on the Trellis.

        :param ~trellis.TRELLIS *matrices: List of `trellis.TRELLIS` object(s)
                                           you wish to read the button matrix of.
                                           Only required if you want to read the
                                           the buttons on a specific Trellis board.
        """
        read_results = False
        if not matrices:
            for matrix in self._matrices:
                read_results |= matrix.read_buttons()
        else:
            for matrix in matrices:
                read_results |= matrix.read_buttons()

        return read_results

    def just_pressed(self, button, *matrices):
        """
        Checks if a button was/is depressed. If return value is above zero then
        the button was/is depressed. Returns zero otherwise.

        :param int button: Number of the button you wish to check.
                           When not including specific `trellis.TRELLIS` objects
                           (`*matrices` param), the range of `x` is 0 to the
                           maximum number of buttons available (4 boards: 0-63).
                           When using `*matrices`, the range of `button` is 0-15
                           for the button on each Trellis.

        :param ~trellis.TRELLIS *matrices: List of `trellis.TRELLIS` object you
                                           wish to check the button on.
                                           Only required if you want to read the
                                           the buttons on a specific Trellis board.
        """
        if not matrices:
            # pylint: disable=multiple-statements
            matrix, key = self._get_matrix(button)
            # pylint: enable=multiple-statements
            if matrix is None:
                return False
            return matrix.just_pressed(key)

        if len(matrices) > 1:
            raise ValueError('Only one matrix key can be checked at a time.')
        else:
            for matrix in matrices:
                return matrix.just_pressed(button)

    def just_released(self, button, *matrices):
        """
        Checks if a button was/is released. If return value is above zero then
        the button was/is released. Returns zero otherwise.

        :param int button: Number of the button you wish to check.
                           When not including specific `trellis.TRELLIS` objects
                           (`*matrices` param), the range of `x` is 0 to the
                           maximum number of buttons available (4 boards: 0-63).
                           When using `*matrices`, the range of `button` is 0-15
                           for the button on each Trellis.

        :param ~trellis.TRELLIS *matrices: List of `trellis.TRELLIS` object you
                                           wish to check the button on.
                                           Only required if you want to read the
                                           the buttons on a specific Trellis board.
        """
        if not matrices:
            # pylint: disable=multiple-statements
            matrix, key = self._get_matrix(button)
            # pylint: enable=multiple-statements
            if matrix is None:
                return False
            return matrix.just_released(key)

        if len(matrices) > 1:
            raise ValueError('Only one matrix key can be checked at a time.')
        else:
            for matrix in matrices:
                return matrix.just_released(button)
