# tcp_servidor5_oche_readline.py
import socket
import time

def recibe_mensaje(sock):
    buf = bytearray()
    while True:
        try:
            b = sock.recv(1)
        except Exception:
            # Propagar el error al llamador
            raise

        if not b:
            # socket cerrado por el otro extremo
            if buf:
                return buf.decode(errors='replace')
            return None

        buf += b
        if buf.endswith(b'\r\n'):
            return buf[:-2].decode(errors='replace')


HOST = 'localhost'
PORT = 9999

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"Escuchando en {HOST}:{PORT}...")

    while True:
        conn, addr = s.accept()
        print(f"Conexión desde {addr}")
        with conn:
           
            while True:
                try:
                    linea = recibe_mensaje(conn)
                except Exception as e:
                    print(f"Error al recibir: {e}")
                    break

                if linea is None:
                    print("Conexión cerrada por el cliente")
                    break

                print("Recibido:", repr(linea))

                # Simular procesamiento lento
                time.sleep(1)

                respuesta = f"OK {linea}\r\n".encode()
                try:
                    conn.sendall(respuesta)
                except Exception as e:
                    print(f"Error al enviar: {e}")
                    break

                if linea == "FINAL":
                    print("Final recibido; cerrando conexión")
                    break

        print("Cliente desconectado, esperando otro cliente...")
