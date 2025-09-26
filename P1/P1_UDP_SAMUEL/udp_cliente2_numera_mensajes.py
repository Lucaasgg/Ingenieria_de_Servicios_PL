import socket
import sys

#Voy a asumir que o recibe ambos argumentos o ninguno
num_argumentos = len(sys.argv)

if num_argumentos > 3:
    print("Error: solo dos argumentos, la IP y el puerto", file=sys.stderr)
    quit
elif num_argumentos == 3:
    ip = sys.argv[1]
    print("IP recibida: ", ip)
    puerto = int(sys.argv[2])
    print("Puerto: ", puerto)
elif num_argumentos == 1:
    ip = "localhost"
    puerto =  9999
    print("No se han recibido argumentos, por lo que la ip es %s y el puerto es %d" % (ip, puerto))
else:
    print("Error: o me das todos los argumentos o ninguno", file=sys.stderr)

#Creamos el socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Lo asignamos a la dirección y puerto deseados
s.bind((ip, puerto-1))

contador = 0
while True:
    contador+=1
    texto = input()
    if texto == "FIN":
        break
    texto_a_enviar = f"{contador}: {texto}"
    s.sendto(texto_a_enviar.encode("utf-8"), (ip, puerto))

s.close()
