# tcp_cliente3_oche_envia_seguido.py
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

    # Enviar tres mensajes seguidos
    for m in messages[:3]:
        payload = (m + "\r\n").encode()
        try:
            s.sendall(payload)
        except Exception as e:
            print(f"No se pudo enviar '{m}': {e}")
            break

    # Leer tres respuestas y mostrarlas con repr()
    for i in range(3):
        try:
            resp = s.recv(4096)
        except socket.timeout:
            print(f"Timeout esperando respuesta {i+1}")
            continue
        except Exception as e:
            print(f"Error al recibir respuesta {i+1}: {e}")
            break

        if not resp:
            respuesta = ''
            print(repr(respuesta))
            print("Conexión cerrada por el servidor")
            break

        respuesta = resp.decode(errors='replace')
        print(repr(respuesta))

except Exception as e:
    print(f"No se pudo conectar/enviar: {e}")
finally:
    s.close()