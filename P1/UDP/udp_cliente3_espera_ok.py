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

#Ponemos el timeout a 2 segundos
s.settimeout(2)

#Inicializamos el contador para los mensajes
contador = 0

#Comenzamos el bucle para enviar los mensajes al servidor
while True:
    contador+=1
    texto = input()
    if texto == "FIN":
        break
    texto_a_enviar = f"{contador}: {texto}"
    s.sendto(texto_a_enviar.encode("utf-8"), (ip, puerto))
    #Una vez mandado el mensaje, esperamos la respuesta del servidor
    try:
        datagrama, origen = s.recvfrom(1024)
        datagrama = datagrama.decode("utf-8")
        if datagrama == "OK":
            print("Confirmación recibida\r")
        else:
            print("No he recibido lo que pensaba %s\r" % datagrama)
    except socket.timeout:
        print("Error: no ha llegado la confirmación de llegada del servidor", file=sys.stderr)

s.close()
