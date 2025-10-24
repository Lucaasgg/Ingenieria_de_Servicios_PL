import socket
import argparse
import sys


def main():
        ap = argparse.ArgumentParser(description="Cliente UDP que descubre servidores HOLA por broadcast.")
        ap.add_argument("--broadcast", "-b", default="255.255.255.255",
                                        help="Dirección de broadcast (por defecto: 255.255.255.255)")
        ap.add_argument("--port", "-p", type=int, default=12345, help="Puerto de servicio (por defecto: 12345)")
        ap.add_argument("--wait", "-w", type=float, default=2.0, help="Timeout en segundos para recibir respuestas")
        args = ap.parse_args()

        msg_buscar = b"BUSCANDO HOLA"
        msg_hola = b"HOLA"

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
                # permitir broadcast y recibir respuestas
                s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

                # ligar a un puerto efímero para recibir respuestas en él
                s.bind(("", 0))

                # enviar broadcast
                try:
                        s.sendto(msg_buscar, (args.broadcast, args.port))
                        print(f"Enviado broadcast '{msg_buscar.decode()}' a {args.broadcast}:{args.port}")
                except OSError as e:
                        print("Error enviando broadcast:", e, file=sys.stderr)
                        return

                # recibir respuestas hasta que timeout ocurra
                s.settimeout(args.wait)
                servidores = []
                primero = None

                print("Esperando respuestas de servidores...")
                while True:
                        try:
                                data, addr = s.recvfrom(4096)
                        except socket.timeout:
                                # asumimos que no habrá más servidores
                                break
                        except KeyboardInterrupt:
                                break

                        ip, puerto = addr[0], addr[1]
                        texto = data.decode(errors="replace")
                        print(f"Respuesta de {ip}:{puerto} -> {texto}")
                        servidores.append((ip, puerto, texto))
                        if primero is None:
                                primero = ip

                if not servidores:
                        print("No se han encontrado servidores.")
                        return

                # probar servicio con el primer servidor encontrado
                servidor_ip = primero
                print(f"\nProbando servicio HOLA con el primer servidor encontrado: {servidor_ip}:{args.port}")
                try:
                        s.sendto(msg_hola, (servidor_ip, args.port))
                except OSError as e:
                        print("Error enviando HOLA al servidor:", e, file=sys.stderr)
                        return

                # esperar respuesta del servidor al HOLA
                s.settimeout(args.wait)
                try:
                        data, addr = s.recvfrom(4096)
                        print("Respuesta final:", data.decode(errors="replace"), "desde", addr[0])
                except socket.timeout:
                        print("No se recibió respuesta al mensaje HOLA (timeout).")
        finally:
                s.close()

if __name__ == "__main__":
        main()