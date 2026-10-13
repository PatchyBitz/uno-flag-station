import serial

with serial.Serial(port="/dev/ttyACM0", baudrate=9600, timeout=10) as uno:
    uno.reset_input_buffer()

    uno.write(b"1\n")
    flag = uno.readline().decode().strip()
    print(flag)
