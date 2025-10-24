import sys
import socket

# Cliente UDP que envía líneas al servidor hasta que se escribe "FIN"
# Tras cada datagrama enviado espera UNA confirmación (solo 1 intento), con tiempo límite.

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
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

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
                s.sendto(data, addr)
            except OSError as e:
                print(f"Error al enviar: {e}")
                break

            # Esperar UNA confirmación con tiempo límite (no reintenta)
            timeout_segundos = 2.0  # tiempo de espera limitado
            old_timeout = s.gettimeout()
            s.settimeout(timeout_segundos)
            try:
                resp, servidor = s.recvfrom(4096)
                try:
                    texto = resp.decode("utf-8", errors="replace")
                except Exception:
                    texto = repr(resp)
                print(f"Confirmación recibida de {servidor}: {texto}")
            except socket.timeout:
                print(f"No se recibió confirmación en {timeout_segundos} s.")
            except OSError as e:
                print(f"Error al recibir confirmación: {e}")
            finally:
                # restaurar modo bloqueante si era así
                s.settimeout(old_timeout)

            numero_mensaje += 1

    except KeyboardInterrupt:
        pass
    finally:
        s.close()

if __name__ == "__main__":
    main()