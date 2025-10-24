import telnetlib
import time

HOST = "localhost"  # Cambia esto si el servidor está en otra máquina
USER = "uo295421"  # Sustituye por tu nombre de usuario en la máquina remota
PASSWORD = "IngServ"  # Sustituye por tu contraseña

# Conexión Telnet
tn = telnetlib.Telnet(HOST)

# Autenticación
tn.read_until(b"login: ")
tn.write(USER.encode('ascii') + b"\n")
tn.read_until(b"Password: ")
tn.write(PASSWORD.encode('ascii') + b"\n")

# Esperar al prompt del shell
tn.read_until(b"$")

# Comprobar si el servidor ya está en ejecución
tn.write(b"ps -ef\n")
output = tn.read_until(b"$").decode('ascii')

if "udp_servidor3_con_ok.py" in output:
    print("El servidor ya está en ejecución")
else:
    print("Servidor no encontrado, lanzando...")
    tn.write(b"nohup python3 udp_servidor3_con_ok.py &\n")
    time.sleep(1)
    tn.write(b"exit\n")
    print(tn.read_all().decode('ascii'))
