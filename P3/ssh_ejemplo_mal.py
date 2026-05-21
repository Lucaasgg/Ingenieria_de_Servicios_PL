import paramiko
import time
client = paramiko.SSHClient()
client.connect('localhost', username='alumno', password='clave-mal')
print("Conectado!!")

stdin, stdout, stderr = client.exec_command('ls')

for line in stdout:
    print(line.rstrip())
time.sleep(1)
client.close()
