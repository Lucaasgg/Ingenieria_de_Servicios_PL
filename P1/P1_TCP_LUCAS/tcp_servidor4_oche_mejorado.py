import socket
import sys


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
        print("Conexión desde", addr)
        try:
            # Para cada cliente, repetir hasta que recibe None (cliente cerró)
            while True:
                linea = recibe_mensaje(conn)
                if linea is None:
                    # Cliente cerró la conexión
                    break

                # Darle la vuelta
                linea_rev = linea[::-1]

                # Enviar la respuesta con un fin de línea añadido
                conn.sendall(linea_rev.encode('utf8') + b"\r\n")
        finally:
            conn.close()
            print("Conexión con", addr, "cerrada")
except KeyboardInterrupt:
    print("\nServidor interrumpido por usuario")
finally:
    s.close()


def recibe_mensaje(conn):
    buf = bytearray()
    while True:
        b = conn.recv(1)
        if not b:
            if not buf:
                return None
            # si hay datos acumulados, devolverlos (sin CRLF si existiera)
            if buf.endswith(b'\r\n'):
                return buf[:-2].decode('utf8')
            return buf.decode('utf8')
        buf += b
        if len(buf) >= 2 and buf[-2:] == b'\r\n':
            return buf[:-2].decode('utf8')

