# IP ping

![PyPI](https://img.shields.io/pypi/v/ipping)
![PyPI - Status](https://img.shields.io/pypi/status/ipping)

A [`ping(8)`](https://linux.die.net/man/8/ping) like network utility allowing use of TCP and UDP packets to measure round-trip and packet loss statistics.

Implemented in minimal-dependency pure Python 3.6+ using [asyncio-protocol](https://docs.python.org/3/library/asyncio-protocol.html).

## Installation

Get it from [pypi](https://pypi.org/project/ipping)

```sh
pip install --upgrade ipping
```

## Usage

### UDP

Sends UDP packets to a running UDP echo server.

Echo server must be running on the machine we want to ping.

Using [`socat(1)`](https://linux.die.net/man/1/socat):

```sh
socat PIPE UDP-RECVFROM:5554,fork
```

Run ping test:

```sh
$ ipping udp 192.168.20.2 5554 -i 0.5 -s 8176 -c 4
PING 192.168.20.2:5554: 8176 data bytes
8192 bytes from 192.168.20.2:5554: time=7.476 ms
8192 bytes from 192.168.20.2:5554: time=7.687 ms
8192 bytes from 192.168.20.2:5554: time=13.941 ms
8192 bytes from 192.168.20.2:5554: time=8.448 ms

--- 192.168.20.2:5554 ping statistics ---
4 packets transmitted, 4 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 7.476/9.388/13.941/3.064 ms
```
