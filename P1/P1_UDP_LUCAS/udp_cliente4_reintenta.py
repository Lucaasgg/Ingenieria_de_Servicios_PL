import sys
import socket

host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
port = int(sys.argv[2]) if len(sys.argv) > 2 else 9999

addr = (host, port)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

numero = 1

while True:
    linea = input()
    if linea == "FIN":
        break

    data = f"{numero}: {linea}".encode()
    timeout = 0.5

    while timeout <= 2.0:
        sock.settimeout(timeout)
        sock.sendto(data, addr)
        try:
            sock.recvfrom(4096)
            numero += 1
            break
        except socket.timeout:
            timeout *= 2
    else:
        print("Servidor no responde. Adiós muy buenas.")
        break

sock.close()