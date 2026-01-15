import socket
import sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 12345
BUF_SIZE = 4096

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.bind(("", PORT))

print(f"Servidor UDP escuchando en {PORT}")

while True:
    data, addr = sock.recvfrom(BUF_SIZE)
    text = data.decode(errors="ignore").strip()
    ip, port = addr

    print(f"{ip}:{port} -> {text!r}")

    if text == "BUSCANDO HOLA":
        sock.sendto(b"IMPLEMENTO HOLA", addr)
    elif text == "HOLA":
        sock.sendto(f"HOLA: {ip}".encode(), addr)