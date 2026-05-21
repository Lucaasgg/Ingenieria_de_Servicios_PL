import telnetlib
import time

HOST = "localhost"
PORT = 23
user = "uo293747"
password = "Samuel-12"

tn = telnetlib.Telnet(HOST, PORT)

tn.read_until(b"login: ")
tn.write(user.encode('utf-8') + b"\n")
tn.read_until(b"Password: ")
tn.write(password.encode('utf-8') + b"\n")

# Discard welcome message
tn.read_until(b"$ ")

tn.write(b"ps -ef\n")
respuesta = tn.read_until(b"$ ")

server = b"udp_servidor3_con_ok.py"  # bytes to match respuesta
if server in respuesta:
    print("\nEl servidor ya está en ejecución")
else:
    tn.write(b"nohup python3 udp_servidor3_con_ok.py &\n")
    time.sleep(1)
    tn.write(b"exit\n")
    respuesta = tn.read_all().decode('utf-8', errors='replace')
    print(respuesta)
