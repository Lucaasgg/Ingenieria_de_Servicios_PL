import sys
import socket

# Creación del socket de escucha
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Permitir reutilizar la dirección tras cerrar el socket
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Obtener puerto de línea de comandos o usar 9999 por defecto
if len(sys.argv) > 1:
    try:
        puerto = int(sys.argv[1])
    except ValueError:
        print("Uso: {} [puerto]".format(sys.argv[0]))
        sys.exit(1)
else:
    puerto = 9999

def recvall(sock, n):
    buf = bytearray()
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:  # conexión cerrada o sin más datos
            break
        buf.extend(chunk)
    return buf.decode("ascii", errors="replace")

# Asignarle puerto
s.bind(("", puerto))

# Ponerlo en modo pasivo
s.listen(5)  # Máximo de clientes en la cola de espera al accept()

# Bucle principal de espera por clientes
while True:
    print("Esperando un cliente")
    sd, origen = s.accept()
    print("Nuevo cliente conectado desde %s, %d" % origen)
    continuar = True
    # Bucle de atención al cliente conectado
    while continuar:
        datos = recvall(sd, 5)  # Usar recvall para leer 5 bytes exactamente
        if datos == "":  # Si no se reciben datos, es que el cliente cerró el socket
            print("Conexión cerrada de forma inesperada por el cliente")
            sd.close()
            continuar = False
        elif datos == "FINAL":
            print("Recibido mensaje de finalización")
            sd.close()
            continuar = False
        else:
            print("Recibido mensaje: %s" % datos)
            
            
            
            
            