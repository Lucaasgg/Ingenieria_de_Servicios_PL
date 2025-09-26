#Escribe un servidor UDP que escuche en el puerto que se le pase por línea de comandos, o en el 9999 por defecto.
# El servidor estará en un bucle infinito en el que, para cada datagrama que llegue, imprimirá en pantalla el contenido del datagrama y la dirección de la cual proviene.
# Guárdalo como udp_servidor1.py

import socket
import sys

