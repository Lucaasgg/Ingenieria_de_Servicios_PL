import socket
import sys

debug = False

if len(sys.argv) > 2:
    print("USO: python3 %s [puerto] [debug]", file=sys.stderr)
    quit
elif len(sys.argv) == 1:
    port = 9999
else:
    port = int(sys.argv[1])
    if sys.argv[2] == "debug":
        debug = True

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", port))

if debug:
    print(s)
print("Socket creado en el puerto ", port)

s.listen(5)
while True:

    print("Esperando un cliente")
    sd, origen = s.accept()

    if debug:
        print(sd)
        print(origen)

    print("Nuevo cliente conectado desde %s, %d" % origen)

    continuar = True
    while continuar:
        datos = sd.recv(1024)
        if debug:
            print(datos)

        datos = datos.decode("ascii")
        if datos=="":
            print("Conexión cerrada de forma inesperada por el cliente")
            sd.close()
            continuar = False
        elif datos=="FINAL":
            print("Recibido mensaje de finalización")
            sd.close()
            continuar = False
        else:
            print("Recibido mensaje: %s" % datos)
