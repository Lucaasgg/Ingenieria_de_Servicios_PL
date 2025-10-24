# tcp_cliente3_oche_envia_seguido.py
import sys
import socket

def recibe_mensaje(sock):
   
    buf = bytearray()
    while True:
        try:
            b = sock.recv(1)
        except socket.timeout:
            # Propagar para que el llamador lo maneje igual que antes
            raise
        except Exception:
            # Propagar cualquier otro error también
            raise

        if not b:
            # socket cerrado por el otro extremo
            if buf:
                # devolver lo acumulado (sin CRLF porque no lo recibimos)
                return buf.decode(errors='replace')
            return None

        buf += b
        if buf.endswith(b'\r\n'):
            # quitar CRLF y devolver la línea
            return buf[:-2].decode(errors='replace')


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
            respuesta = recibe_mensaje(s)
        except socket.timeout:
            print(f"Timeout esperando respuesta {i+1}")
            continue
        except Exception as e:
            print(f"Error al recibir respuesta {i+1}: {e}")
            break

        if respuesta is None:
            respuesta = ''
            print(repr(respuesta))
            print("Conexión cerrada por el servidor")
            break

        print(repr(respuesta))

except Exception as e:
    print(f"No se pudo conectar/enviar: {e}")
finally:
    s.close()