import telnetlib

HOST = "localhost"
PORT = 9999
user = "uo293747"
password = "Samuel-12"

tn = telnetlib.Telnet(HOST, PORT)

tn.read_until(b"$")
tn.write(b"ps -ef\n")
respuesta = tn.read_until(b"$")

print(respuesta)
