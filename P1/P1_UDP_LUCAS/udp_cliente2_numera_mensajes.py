import sys
import socket

# Cliente UDP que envía líneas al servidor hasta que se escribe "FIN"

def main():
    host = "localhost"
    port = 9999
    numero_mensaje = 1
    # Parseo sencillo de parámetros: [host] [port]
    if len(sys.argv) >= 2:
        host = sys.argv[1]
    if len(sys.argv) >= 3:
        try:
            port = int(sys.argv[2])
        except ValueError:
            print("Puerto no válido. Usando 9999.")
            port = 9999

    addr = (host, port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        while True:
            try:
                linea = input().rstrip("\n")
            except EOFError:
                # Fin de entrada estándar -> salir
                break

            if linea == "FIN":
                break

            data = f"{numero_mensaje}: {linea}".encode("utf-8")
            try:
                sock.sendto(data, addr)
                numero_mensaje += 1
            except OSError as e:
                print(f"Error al enviar: {e}")
                break
    except KeyboardInterrupt:
        pass
    finally:
        sock.close()

if __name__ == "__main__":
    main()