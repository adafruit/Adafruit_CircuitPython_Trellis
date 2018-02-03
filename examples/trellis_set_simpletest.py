# Basic example of turning on LEDs and handling Keypad
# button activity.

# Import all board pins
import time
import busio
from board import SCL, SDA
from adafruit_trellis import trellis
from adafruit_trellis import trellis_set

# Create the I2C interface
i2c = busio.I2C(SCL, SDA)

# Create a Trellis object for each board
matrix1 = trellis.TRELLIS(i2c, 0x72)
matrix2 = trellis.TRELLIS(i2c) # 0x70 when no I2C address is supplied

# Create the Trellis matrix using the board
# objects
trellis = trellis_set.MATRIX(matrix1, matrix2)

# Turn on every LED
print('Turning all LEDs on...')
trellis.fill(1)
trellis.show()
time.sleep(2)

# Turn off every LED
print('Turning all LEDs off...')
trellis.fill(0)
trellis.show()
time.sleep(2)

# Turn on every LED, one at a time
print('Turning on each LED, one at a time...')
for i in range(32):
    trellis.led_on(i)
    trellis.show()
    time.sleep(.1)

# Turn off every LED, one at a time
print('Turning off each LED, one at a time...')
for i in range(31,0,-1):
    trellis.led_off(i)
    trellis.show()
    time.sleep(.1)

# Now start reading button activity
# When a button is depressed (trellis.just_pressed),
# the LED for that button will turn on.
# When the button is relased (trellis.just_released),
# the LED will turn off.
print('Starting button sensory loop...')
while True:
    # Make sure to take a break during each trellis.read_buttons
    # cycle. This allows for debouncing, and for the trellis driver
    # to write and read the buffer.
    time.sleep(.1)

    try:
        if trellis.read_buttons():
            for i in range(32):
                if trellis.just_pressed(i):
                    print('Button', i + 1, 'was just pressed!')
                    trellis.led_on(i)
                    trellis.show()
            for i in range(32):
                if trellis.just_released(i):
                    print('Button', i + 1, 'was just released!')
                    trellis.led_off(i)
                    trellis.show()

    # This allows the program to stop running when Ctrl+C is
    # pressed in the REPL
    except KeyboardInterrupt:
        break
