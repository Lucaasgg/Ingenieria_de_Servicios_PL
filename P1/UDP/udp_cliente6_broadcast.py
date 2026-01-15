import socket
import sys

BROADCAST = sys.argv[1] if len(sys.argv) > 1 else "255.255.255.255"
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 12345
WAIT = float(sys.argv[3]) if len(sys.argv) > 3 else 2.0

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.bind(("", 0))

sock.sendto(b"BUSCANDO HOLA", (BROADCAST, PORT))
print(f"Broadcast enviado a {BROADCAST}:{PORT}")

sock.settimeout(WAIT)
servidores = []

while True:
    try:
        data, addr = sock.recvfrom(4096)
        ip = addr[0]
        print(f"Servidor encontrado: {ip} -> {data.decode(errors='ignore')}")
        servidores.append(ip)
    except socket.timeout:
        break

if servidores:
    ip = servidores[0]
    print(f"\nProbando HOLA con {ip}")
    sock.sendto(b"HOLA", (ip, PORT))
    try:
        data, _ = sock.recvfrom(4096)
        print("Respuesta:", data.decode(errors="ignore"))
    except socket.timeout:
        print("Sin respuesta al HOLA")
else:
    print("No se encontró ningún servidor")

sock.close()