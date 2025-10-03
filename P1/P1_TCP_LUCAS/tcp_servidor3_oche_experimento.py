import socket
import sys
import time

# Creación del socket de escucha
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if len(sys.argv) > 1:
    try:
        puerto = int(sys.argv[1])
    except ValueError:
        print("Uso: {} [puerto]".format(sys.argv[0]))
        sys.exit(1)
else:
    puerto = 9999

s.bind(('0.0.0.0', puerto))
s.listen(5)
print("Escuchando en el puerto", puerto)

try:
    while True:
        conn, addr = s.accept()
        time.sleep(1)
        print("Conexión desde", addr)
        try:
            # Para cada cliente, repetir hasta que recv() devuelva b'' (cliente cerró)
            while True:
                mensaje_bytes = conn.recv(80)  # Nunca enviará más de 80 bytes, aunque tal vez sí menos
                if not mensaje_bytes:
                    # Cliente cerró la conexión
                    break
                mensaje = mensaje_bytes.decode('utf8')  # Convertir los bytes a caracteres

                # Quitar el "fin de línea" que son sus 2 últimos caracteres
                linea = mensaje[:-2]  # slice desde el principio hasta el final -2

                # Darle la vuelta
                linea = linea[::-1]

                # Enviar la respuesta con un fin de línea añadido
                conn.sendall(linea.encode('utf8') + b"\r\n")
        finally:
            conn.close()
            print("Conexión con", addr, "cerrada")
except KeyboardInterrupt:
    print("\nServidor interrumpido por usuario")
finally:
    s.close()
    
    
    
    
    