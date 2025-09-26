#Escribe un servidor UDP que escuche en el puerto que se le pase por línea de comandos, o en el 9999 por defecto.
# El servidor estará en un bucle infinito en el que, para cada datagrama que llegue, imprimirá en pantalla el contenido del datagrama y la dirección de la cual proviene.
# Guárdalo como udp_servidor1.py

import socket
import sys
import random

s= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# parsear puerto desde la línea de comandos (por defecto 9999)
port = 9999
if len(sys.argv) > 1:
    try:
        port = int(sys.argv[1])
    except ValueError:
        print("Puerto inválido: ", sys.argv[1])
        sys.exit(1)

# enlazar socket UDP a todas las interfaces en el puerto indicado
s.bind(("", port))
print("Escuchando en UDP puerto " , port)

try:
    while True:
        data, addr = s.recvfrom(4096)  # tamaño máximo del datagrama
        # mostrar contenido y dirección de origen
        texto = data.decode('utf-8', errors='replace')
        nrand= random.randint(1,2)
        if nrand==1:
            print(f"Recibido de", addr, ":", texto)
        else:
            print(f"Simulando paquete perdido")
            
except KeyboardInterrupt:
    print("Servidor interrumpido por el usuario.")
finally:
    s.close()

