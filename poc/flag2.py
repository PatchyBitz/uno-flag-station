import time

import serial

with serial.Serial(port="/dev/ttyACM0", baudrate=9600, timeout=10) as uno:
    time.sleep(2)
    uno.reset_input_buffer()

    uno.write(b"2\n")
    uno.write(b"hello, world\n")
    flag = uno.readline().decode().strip()
    print(flag)
