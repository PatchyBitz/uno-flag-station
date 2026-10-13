import serial


def client_handshake() -> bool:
    uno.write(b"S\n")
    f = uno.readline().strip()
    if f == b"A":
        uno.write(b"SA\n")
        return True
    return False


def server_handshake() -> bool:
    f = uno.readline().strip()
    if f == b"S":
        uno.write(b"A\n")
    f = uno.readline().strip()
    return f == b"SA"


with serial.Serial(port="/dev/ttyACM0", baudrate=9600, timeout=10) as uno:
    uno.reset_input_buffer()

    uno.write(b"4\n")
    client_handshake()
    if server_handshake():
        num = input("Blinks? ")
        uno.write(num.encode())
    if client_handshake():
        flag = uno.readline().decode().strip()
        print(flag)
