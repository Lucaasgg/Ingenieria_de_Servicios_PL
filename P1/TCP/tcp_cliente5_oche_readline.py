import socket
import sys

def recibe_mensaje(sock):
    buf = bytearray()
    while True:
        f = sock.makefile(encoding="utf8", newline="\r\n")
        mensaje = f.readline()
        return mensaje

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
