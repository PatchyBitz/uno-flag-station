import time

import serial

with serial.Serial(port="/dev/ttyACM0", baudrate=9600, timeout=10) as uno:
    time.sleep(2)
    uno.reset_input_buffer()

    uno.write(b"3\n")
    uno.write(b"S\n")

    f = uno.readline().strip()
    if f == b"A":
        uno.write(b"SA\n")

    flag = uno.readline().decode().strip()
    print(flag)
