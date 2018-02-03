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
#  Also utilized functions from the CircuitPython HT16K33 library
#  written by Radomir Dopieralski & Tony DiCola for Adafruit Industries
#  https://github.com/adafruit/Adafruit_CircuitPython_HT16K33
#
#  CircuitPython Library Author: Michael Schroeder(sommersoft). No
#  affiliation to Adafruit is implied.
"""
`adafruit_trellis` - Adafruit Trellis Monochrome 4x4 LED Backlit Keypad
========================================================================

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
"""

__version__ = "1.0.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_Trellis.git"

from micropython import const
from adafruit_bus_device import i2c_device

# HT16K33 Command Contstants
# pylint: disable=bad-whitespace, invalid-name
_HT16K33_OSCILATOR_ON       = const(0x21)
_HT16K33_BLINK_CMD          = const(0x80)
_HT16K33_BLINK_DISPLAYON    = const(0x01)
_HT16K33_CMD_BRIGHTNESS     = const(0xE0)
_HT16K33_KEY_READ_CMD       = const(0x40)

# LED Lookup Table
ledLUT = (0x3A, 0x37, 0x35, 0x34,
          0x28, 0x29, 0x23, 0x24,
          0x16, 0x1B, 0x11, 0x10,
          0x0E, 0x0D, 0x0C, 0x02)

# Button Loookup Table
buttonLUT = (0x07, 0x04, 0x02, 0x22,
             0x05, 0x06, 0x00, 0x01,
             0x03, 0x10, 0x30, 0x21,
             0x13, 0x12, 0x11, 0x31)
# pylint: enable=bad-whitespace, invalid-name

class TRELLIS:
    """
    Driver base for a single Trellis Board

    :param ~busio.I2C i2c: The `busio.I2C` object to use. This is the only required parameter
                           when using a single Trellis board.
    :param int address: The I2C address of the Trellis board you're using. Defaults to `0x70`
                        which is the default address for Trellis boards. See Trellis product
                        guide for using different/multiple I2C addresses.
                        https://learn.adafruit.com/adafruit-trellis-diy-open-source-led-keypad

    Example:

    .. code-block:: python

        import time
        import busio
        import board
        from adafruit_trellis import trellis

        i2c = busio.I2C(board.SCL, board.SDA)
        trellis = trellis.TRELLIS(i2c)
        print('Starting button sensory loop...')
        while True:
            try:
                if trellis.read_buttons():
                    for i in range(16):
                        if trellis.just_pressed(i):
                            print('Button', i + 1, 'was just pressed!')
                            trellis.led_on(i)
                            trellis.show()
                    for i in range(16):
                        if trellis.just_released(i):
                            print('Button', i + 1, 'was just released!')
                            trellis.led_off(i)
                            trellis.show()
            except KeyboardInterrupt:
                break
            time.sleep(.1)
    """
    def __init__(self, i2c, address=0x70):
        self.i2c_device = i2c_device.I2CDevice(i2c, address)
        self._temp = bytearray(1)
        self._led_buffer = bytearray(17)
        self._buttons_buffer = bytearray(6)
        self._last_buttons = bytearray(6)
        self._blink_rate = None
        self._brightness = None

        self.fill(0)
        self._write_cmd(_HT16K33_OSCILATOR_ON)
        self.blink_rate(0)
        self.brightness(15)

    def _write_cmd(self, byte):
        self._temp[0] = byte
        with self.i2c_device:
            self.i2c_device.write(self._temp)

    def blink_rate(self, rate=None):
        """
        Get or set the blink rate.

        :param int rate: (Optional) Range 0-3. If no parameter is given, current
                          blink rate is returned.

        """
        if rate is None:
            return self._blink_rate
        rate = rate & 0x03
        self._blink_rate = rate
        self._write_cmd(_HT16K33_BLINK_CMD |
                        _HT16K33_BLINK_DISPLAYON | rate << 1)
        return None

    def brightness(self, brightness):
        """
        Get or set the brightness.

        :param int brightness: (Optional) Range 0-15. If no parameter is given, current
                               brightness is returned.

        """
        if brightness is None:
            return self._brightness
        brightness = brightness & 0x0F
        self._brightness = brightness
        self._write_cmd(_HT16K33_CMD_BRIGHTNESS | brightness)
        return None

    def show(self):
        """Refresh the LED buffer and show the changes."""
        with self.i2c_device:
            # Byte 0 is 0x00, address of LED data register. The remaining 16
            # bytes are the display register data to set.
            self.i2c_device.write(self._led_buffer)

    def led_on(self, x):
        """
        Turns an LED on. Must call `[trellis].show()` afterwards to update the matrix.

        :param int x: LED number (1-16) to turn on.
        """
        if 0 < x > 15:
            raise ValueError('LED number must be between 0-15 (pyhsical LED - 1)')
        led = ledLUT[x] >> 4
        mask = 1 << (ledLUT[x] & 0x0f)
        self._led_buffer[(led * 2) + 1] |= mask
        self._led_buffer[(led * 2) + 2] |= mask >> 8

    def led_off(self, x):
        """
        Turns an LED off. Must call `[trellis].show()` to update the matrix.

        :param int x: LED number (0-15) to turn off.
        """
        if 0 < x > 15:
            raise ValueError('LED number must be between 0-15 (pyhsical LED - 1)')
        led = ledLUT[x] >> 4
        mask = 1 << (ledLUT[x] & 0x0f)
        self._led_buffer[(led * 2) + 1] &= ~mask
        self._led_buffer[(led * 2) + 2] &= ~mask >> 8

    def led_status(self, x):
        """
        Gives the current status of an LED: True == ON, False == OFF.

        :param int x: LED number (0-15) to check.
        """
        if 1 < x > 16:
            raise ValueError('LED number must be between 0-15 (pyhsical LED - 1)')
        led = ledLUT[x] >> 4
        mask = 1 << (ledLUT[x] & 0x0f)
        return bool(((self._led_buffer[(led * 2) + 1] | \
                     self._led_buffer[(led * 2) + 2] << 8) & mask) > 0)

    def fill(self, color):
        """
        Fill the whole board with the given color.

        :param int color: 0 == OFF, > 0 == ON

        """
        fill = 0xff if color else 0x00
        for i in range(16):
            self._led_buffer[i+1] = fill

    def read_buttons(self):
        """Read the button matrix register on the Trellis"""
        self._last_buttons[:] = self._buttons_buffer[:]
        self._write_cmd(_HT16K33_KEY_READ_CMD)
        with self.i2c_device:
            self.i2c_device.readinto(self._buttons_buffer)
        return bool(self._last_buttons != self._buttons_buffer)

    def _is_pressed(self, button):
        if button > 15:
            return None
        mask = 1 << (buttonLUT[button] & 0x0f)
        return self._buttons_buffer[(buttonLUT[button] >> 4)] & mask

    def _was_pressed(self, button):
        if button > 15:
            return None
        mask = 1 << (buttonLUT[button] & 0x0f)
        return self._last_buttons[(buttonLUT[button] >> 4)] & mask

    def just_pressed(self, button):
        """
        Checks if a button was/is depressed. If return value is above zero then
        the button was/is depressed. Returns zero otherwise.

        :param int x: Button number (0-15) to check.
        """
        if button > 15:
            raise ValueError('Button must be between 0-15 (pyhsical button - 1)')
        # pylint: disable=invalid-unary-operand-type
        return self._is_pressed(button) & ~self._was_pressed(button)
        # pylint: enable=invalid-unary-operand-type

    def just_released(self, button):
        """
        Checks if a button was/is released. If return value is above zero then
        the button was/is released. Returns zero otherwise.

        :param int x: Button number (0-15) to check.
        """
        if button > 15:
            raise ValueError('Button must be between 0-15 (pyhsical button - 1)')
        # pylint: disable=invalid-unary-operand-type
        return ~self._is_pressed(button) & self._was_pressed(button)
        # pylint: enable=invalid-unary-operand-type
