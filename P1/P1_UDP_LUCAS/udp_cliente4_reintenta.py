import sys
import socket

# Cliente UDP que reintenta enviando y duplica el timeout hasta superar 2 s.


def main():
    host = "localhost"
    port = 9999
    numero_mensaje = 1

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
                break

            if linea == "FIN":
                break

            data = f"{numero_mensaje}: {linea}".encode("utf-8")

            # esquema de reintentos: timeout inicial y duplicar hasta superar 2.0 s
            initial_timeout = 0.5
            timeout_actual = initial_timeout

            # Guardar timeout anterior para restaurarlo al final
            old_timeout = s.gettimeout()

            enviado = False
            try:
                while True:
                    try:
                        s.sendto(data, addr)
                    except OSError as e:
                        print(f"Error al enviar: {e}")
                        raise  # salir del bucle externo

                    s.settimeout(timeout_actual)
                    try:
                        
                        resp, servidor = s.recvfrom(4096)
                        try:
                            texto = resp.decode("utf-8", errors="replace")
                        except Exception:
                            texto = repr(resp)
                        print(f"Confirmación recibida de {servidor}: {texto}")
                        # considerar OK (ignoring surrounding whitespace) como éxito
                        if texto.strip() == "OK":
                            enviado = True
                            break
                        else:
                            # Si se recibe cualquier otra confirmación, también se toma como éxito
                            # (evita reintentos infinitos por respuestas no-OK).
                            enviado = True
                            break
                    except socket.timeout:
                        # no llegó respuesta dentro de timeout_actual: duplicar timeout y reintentar
                        timeout_actual *= 2
                        if timeout_actual > 2.0:
                            print("Puede que el servidor esté caído. Inténtelo más tarde")
                            return
                        # seguir reintentando (mismo numero_mensaje, mismo data)
                    except OSError as e:
                        print(f"Error al recibir confirmación: {e}")
                        raise
            finally:
                s.settimeout(old_timeout)

            if enviado:
                numero_mensaje += 1

    except KeyboardInterrupt:
        pass
    finally:
        s.close()

if __name__ == "__main__":
    main()