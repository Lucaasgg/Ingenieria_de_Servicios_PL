import socket
import sys

def recibe_mensaje(conn):
    buf = bytearray()
    while True:
        b = conn.recv(1)
        if not b:
            return buf.decode() if buf else None
        buf += b
        if buf.endswith(b"\r\n"):
            return buf[:-2].decode()

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("0.0.0.0", PORT))
sock.listen(5)

print("Escuchando en", PORT)

while True:
    conn, addr = sock.accept()
    print("Conexión desde", addr)

    while True:
        linea = recibe_mensaje(conn)
        if linea is None:
            break
        conn.sendall(linea[::-1].encode() + b"\r\n")

    conn.close()
    print("Conexión cerrada", addr)
