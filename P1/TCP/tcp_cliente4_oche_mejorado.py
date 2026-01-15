import socket
import sys

def recibe_mensaje(sock):
    buf = bytearray()
    while True:
        b = sock.recv(1)
        if not b:
            return buf.decode(errors="replace") if buf else None
        buf += b
        if buf.endswith(b"\r\n"):
            return buf[:-2].decode(errors="replace")

host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
port = int(sys.argv[2]) if len(sys.argv) > 2 else 9999

messages = ["Hola servidor", "Línea de prueba 1", "Línea de prueba 2"]

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(5)
sock.connect((host, port))

for m in messages:
    sock.sendall((m + "\r\n").encode())

for _ in messages:
    print(repr(recibe_mensaje(sock)))

sock.close()