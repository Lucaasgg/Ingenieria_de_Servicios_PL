import socket
import sys


PORT = 12345
BUF_SIZE = 4096

def main(port=PORT):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Permite realizar broadcast 
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    s.bind(('', port))
    print(f"Servidor UDP 'HOLA' escuchando en puerto {port} (broadcast activado). Ctrl-C para salir.")

    try:
        while True:
            try:
                data, addr = s.recvfrom(BUF_SIZE)
            except InterruptedError:
                continue
            if not data:
                continue

            text = data.decode(errors='ignore').strip()
            client_ip, client_port = addr[0], addr[1]
            print(f"Recibido de {client_ip}:{client_port}: {repr(text)}")

            if text == "BUSCANDO HOLA":
                resp = "IMPLEMENTO HOLA"
                s.sendto(resp.encode(), addr)
                print(f" -> Enviado a {client_ip}:{client_port}: {resp}")
            elif text == "HOLA":
                resp = f"HOLA: {client_ip}"
                s.sendto(resp.encode(), addr)
                print(f" -> Enviado a {client_ip}:{client_port}: {resp}")
            else:
                # Mensaje no reconocido: se ignora (podría ampliarse)
                print(" -> Mensaje no reconocido. Ignorado.")
    except KeyboardInterrupt:
        print("\nServidor detenido por usuario.")
    finally:
        s.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            PORT = int(sys.argv[1])
        except ValueError:
            print("Puerto inválido, usando 12345.")
    main(PORT)