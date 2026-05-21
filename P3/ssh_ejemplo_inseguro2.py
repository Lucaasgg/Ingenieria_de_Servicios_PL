import paramiko
import time
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.WarningPolicy())
client.connect('localhost', username='uo293747', password='Samuel-12')
print("Conectado!!")

stdin, stdout, stderr = client.exec_command('ls')

for line in stdout:
    print(line.rstrip())
time.sleep(1)
client.close()
