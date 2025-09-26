import socket
import sys
import random as r

if len(sys.argv) > 1:
    print("Error: solo se acepta un parámetro, el puerto", file=sys.stderr)
    quit
elif len(sys.argv) == 1:
    port = 9999
else:
    port = int(sys.argv[1])


#Creamos el socket UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("Socket creado: ", s)
#Asignamos el socket al puerto que se pase por línea de comandos

dirección = "0.0.0.0"
s.bind((dirección, port))
print("Socket asignado al puerto ", port)

while True:
    datagrama, origen = s.recvfrom(1024)
    n = r.randint(1,4)
    if n > 2:
        print("Simulando que he perdido el paquete")
        continue
    print("Datagrama recibido: ")
    print(datagrama.decode("utf-8"))
    print("Ha llegado desde ", origen)
