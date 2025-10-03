# tcp_cliente3_oche.py
import sys
import socket

host = 'localhost'
port = 9999
if len(sys.argv) >= 2:
    host = sys.argv[1]
if len(sys.argv) >= 3:
    try:
        port = int(sys.argv[2])
    except ValueError:
        print("Puerto inválido. Usando 9999.")

messages = ["Hola servidor", "Línea de prueba 1", "Línea de prueba 2", "FINAL"]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(5)
try:
    s.connect((host, port))
    for m in messages:
        payload = (m + "\r\n").encode()
        s.sendall(payload)
        try:
            resp = s.recv(4096)
            if not resp:
                print("Conexión cerrada por el servidor")
                break
            print("Respuesta:", resp.decode(errors='replace').rstrip("\r\n"))
        except socket.timeout:
            print("Timeout esperando respuesta para:", m)
except Exception as e:
    print(f"No se pudo conectar/enviar: {e}")
finally:
    s.close()