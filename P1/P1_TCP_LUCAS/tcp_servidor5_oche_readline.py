# tcp_servidor_readline.py
import socket
import sys

HOST = '0.0.0.0'
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(5)
print("Escuchando en el puerto", PORT)

try:
    while True:
        conn, addr = s.accept()
        print("Conexión desde", addr)
        # usamos makefile() para poder usar readline()
        r = conn.makefile('r', encoding='utf8', newline='\r\n')  # text mode reader
        try:
            while True:
                linea = r.readline()          # devuelve '' si EOF
                if linea == '':
                    break
                linea = linea.rstrip('\r\n')      # quitar CRLF
                linea_rev = linea[::-1]
                conn.sendall((linea_rev + "\r\n").encode('utf8'))
        finally:
            r.close()
            conn.close()
            print("Conexión con", addr, "cerrada")
except KeyboardInterrupt:
    print("\nServidor interrumpido por usuario")
finally:
    s.close()
