# Uno flag station

Firmware for Arduino Uno flag stations: boards that serve `DSU{...}` flags over UART. The station source and the protocols to obtain each flag are intentional and public.

Organizers flash this firmware onto flag stations. Participants connect their own Uno with jumper wires, write firmware that speaks the flag protocols, and collect flags.

Station logic lives in [`src/main.cpp`](src/main.cpp). Host-side reference clients that speak the same bytes are in [`poc/`](poc/).

## Wiring

Connect the participant Uno to the flag station with jumper wires on the hardware UART pins (and ground):

| Flag station | Participant |
|--------------|-------------|
| TX (pin 1)   | RX (pin 0)  |
| RX (pin 0)   | TX (pin 1)  |
| GND          | GND         |

Baud rate: 9600.

```mermaid
flowchart LR
  Part[participant Uno] -->|"TX pin 1 → RX pin 0"| Station[flag station]
  Station -->|"TX pin 1 → RX pin 0"| Part
  Part ---|GND| Station
```

Pins 0 and 1 are shared with the USB-serial chip. Use USB to flash and power boards. While collecting flags, talk over the jumpers from the participant board—avoid a second host driving the same UART at the same time.

## Architecture

| Item | Detail |
|------|--------|
| Board | Arduino Uno |
| UART | Pins 0 (RX), 1 (TX), GND |
| Baud | 9600 |
| LED | `LED_BUILTIN` |

```mermaid
flowchart LR
  Part[participant Uno] -->|"flag number + protocol"| Station[flag station]
  Station -->|"DSU flag string"| Part
```

## Build and flash

Flags 1–4 are not committed. Put them in a project-root `.env` (gitignored). Placeholders in [`include/flags.h`](include/flags.h) are used if a key is missing. Flag 0 is the exception: its string is written in [`src/main.cpp`](src/main.cpp) on purpose.

```env
BLINKS=<count>
FLAG1="DSU{...}"
FLAG2="DSU{...}"
FLAG3="DSU{...}"
FLAG4="DSU{...}"
```

At build time, [`scripts/env_flags.py`](scripts/env_flags.py) reads `.env` and injects the values as compiler defines:

```mermaid
flowchart LR
  Env[".env"] --> Script[env_flags.py]
  Script --> Defines[compiler defines]
  Defines --> Firmware[firmware]
```

```bash
pio run
pio run -t upload
pio device monitor -b 9600
```

## Obtaining flags

Send a flag number (`0`–`4`) followed by a newline, then complete that flag’s protocol. On success the station prints a `DSU{...}` line.

| Flag | Idea |
|------|------|
| 0 | In the source |
| 1 | Request only |
| 2 | Password |
| 3 | Handshake |
| 4 | Handshake, LED blinks, count |

### Handshake

A handshake confirms that both ends are present, listening, and speaking the same protocol before anything important is exchanged. Real networks use the same idea (for example TCP’s three-way handshake): each side sends a short signal and waits for a matching reply so neither starts mid-stream or talks past a board that is not ready.

Here the exchange is a tiny syn/ack-style dialog over UART—tokens `S`, `A`, and `SA`—implemented as `server_handshake()` and `client_handshake()` in [`src/main.cpp`](src/main.cpp).

```mermaid
sequenceDiagram
  participant P as participant
  participant S as flag station
  rect rgba(70, 130, 180, 0.12)
    Note over P,S: server handshake
    P->>S: S
    S->>P: A
    P->>S: SA
  end
```

When the station acts as server, the participant is the client (diagram above). When the station acts as client, roles reverse: station sends `S`, participant replies `A`, station sends `SA`.

### Flag 0

Send `0`, then `A`. The station replies `B`. Send `C` and it prints the flag. That string is the literal in `flag0()` in [`src/main.cpp`](src/main.cpp). It is part of the firmware source, not a value from `.env`.

```mermaid
sequenceDiagram
  participant P as participant
  participant S as flag station
  P->>S: 0
  P->>S: A
  S->>P: B
  P->>S: C
  S->>P: FLAG0
```

### Flag 1

Request the flag; no further exchange.

```mermaid
sequenceDiagram
  participant P as participant
  participant S as flag station
  P->>S: 1
  S->>P: FLAG1
```

### Flag 2

Send `2`, then the password line. The station compares it to `hello, world` and prints the flag on a match.

```mermaid
sequenceDiagram
  participant P as participant
  participant S as flag station
  P->>S: 2
  P->>S: hello, world
  S->>P: FLAG2
```

### Flag 3

Send `3`, then complete one server-side handshake (participant as client). Success unlocks the flag.

```mermaid
sequenceDiagram
  participant P as participant
  participant S as flag station
  P->>S: 3
  rect rgba(70, 130, 180, 0.12)
    Note over P,S: server handshake
    P->>S: S
    S->>P: A
    P->>S: SA
  end
  S->>P: FLAG3
```

### Flag 4

Send `4`, complete a server handshake, watch `LED_BUILTIN` blink, complete a client handshake, send the blink count as an integer, complete another server handshake, then receive the flag or an error. Organizers set the blink count with `BLINKS` in `.env`.

```mermaid
sequenceDiagram
  participant P as participant
  participant S as flag station
  P->>S: 4
  rect rgba(70, 130, 180, 0.12)
    Note over P,S: server handshake
    P->>S: S
    S->>P: A
    P->>S: SA
  end
  Note over S: blink LED_BUILTIN BLINKS times
  rect rgba(70, 130, 180, 0.12)
    Note over P,S: client handshake
    S->>P: S
    P->>S: A
    S->>P: SA
  end
  P->>S: blink count as integer
  rect rgba(70, 130, 180, 0.12)
    Note over P,S: server handshake
    P->>S: S
    S->>P: A
    P->>S: SA
  end
  alt count correct
    S->>P: FLAG4
  else wrong
    S->>P: Incorrect.
  end
```

## Reference clients

POC scripts in [`poc/`](poc/) speak the same protocols over USB serial (default `/dev/ttyACM0` at 9600). Useful for organizers and debugging. The participant path is jumpered Unos; the scripts show the exact byte sequences.

## Repository layout

| Path | Role |
|------|------|
| `src/main.cpp` | Flag station firmware |
| `include/flags.h` | `FLAG*` / `BLINKS` placeholders |
| `scripts/env_flags.py` | Injects `.env` into the build |
| `poc/` | Reference serial clients |
| `platformio.ini` | Uno / PlatformIO config |
