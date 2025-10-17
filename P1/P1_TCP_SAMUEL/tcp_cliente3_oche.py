import socket
import sys

if len(sys.argv) == 2:
    print("He recibido un puerto")
    port = int(sys.argv[1])
elif len(sys.argv) == 1:
    port = 9999

s = socket.socket()
s.connect(("",port))
for i in range(5):
    s.sendall("ABCDE\r\n".encode("utf-8"))
    datos = s.recv(7)
    print(datos.decode("utf-8"))

s.close()
