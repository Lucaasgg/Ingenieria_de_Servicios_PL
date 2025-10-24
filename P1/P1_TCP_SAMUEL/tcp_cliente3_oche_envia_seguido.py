import socket
import sys

if len(sys.argv) == 2:
    print("He recibido un puerto")
    port = int(sys.argv[1])
elif len(sys.argv) == 1:
    port = 9999
else:
    print("USO: python3 %s [puerto]" % sys.argv[0], file=sys.stderr)
    sys.exit(1)

s = socket.socket()
s.connect(("", port))

TEXTO = "ABCDE\r\n".encode("utf-8")

for _ in range(3):
    s.sendall(TEXTO)

for _ in range(3):
    datos = s.recv(7)
    print(repr(datos.decode("utf-8")))

s.close()

