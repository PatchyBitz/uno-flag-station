import serial

with serial.Serial(port="/dev/ttyACM0", baudrate=9600, timeout=10) as uno:
    uno.reset_input_buffer()

    uno.write(b"3\n")
    uno.write(b"S\n")

    while True:
        f = uno.readline().strip()
        if f == b"A":
            uno.write(b"SA\n")
            break

    flag = uno.readline().decode().strip()
    print(flag)
