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

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((host, port))
except Exception as e:
    print(f"No se pudo conectar a {host}:{port} -> {e}")
    s.close()
    sys.exit(1)

try:
    # Enviar 5 veces exactamente 5 bytes "ABCDE"
    for _ in range(5):
        s.send(b"ABCDE")
    # Envío final
    s.send(b"FINAL")
except Exception as e:
    print(f"Error enviando datos: {e}")
finally:
    s.close()