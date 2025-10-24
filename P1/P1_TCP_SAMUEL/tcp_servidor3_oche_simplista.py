import socket
import sys
import time

if len(sys.argv) > 2:
    print("USO: python3 %s [puerto] [debug]", file=sys.stderr)
    quit
elif len(sys.argv) == 1:
    port = 9999
else:
    port = int(sys.argv[1])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", port))

print("Socket creado en el puerto ", port)

s.listen(80)
while True:

    print("Esperando un cliente")
    sd, origen = s.accept()
    print("Nuevo cliente conectado desde %s, %d" % origen)

    time.sleep(1)
    while True:
        datos = sd.recv(80)

        datos = str(datos, "utf-8")
        print(datos)
        if datos=="":
            print("Conexión cerrada de forma inesperada por el cliente")
            sd.close()
            break

        línea = datos[:-2]
        línea = línea[::-1]
        print(línea)
        sd.sendall(bytes(línea+"\r\n", "utf-8"))
