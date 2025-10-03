import socket
import sys

def recvall(sock, num_bytes):

    #Array para guardar los datos
    data = bytearray()

    #Bucle para recibir los datos
    while len(data) < num_bytes:
        try:
            packet = sock.recv(num_bytes - len(data))
        except socket.error as e:
            print(f"Socket error: {e}", file=sys.stderr)
            break

        if not packet:
            break

        data.extend(packet)

    return data.decode("utf-8")


if len(sys.argv) > 2:
    print("USO: python3 %s [puerto]" % sys.argv[0], file=sys.stderr)
    sys.exit()
elif len(sys.argv) == 1:
    port = 9999
else:
    port = int(sys.argv[1])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", port))


s.listen(5)
while True:

    print("Esperando un cliente")
    sd, origen = s.accept()

    print("Nuevo cliente conectado desde %s, %d" % origen)

    continuar = True
    while continuar:
        datos = recvall(sd,5)

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
