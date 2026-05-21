import paramiko
import time
import base64
client = paramiko.SSHClient()
key = paramiko.Ed25519Key(data=base64.b64decode(b'AAAAC3NzaC1lZDI1NTE5AAAAIFyhi2jjPeBJAhyDxJwfmRoCnFfVMzvci3sksj+cSEgB'))
client.get_host_keys().add('localhost', 'ssh-ed25519', key)
client.connect('localhost', username='uo293747', password='Samuel-12')
print("Conectado!!")

stdin, stdout, stderr = client.exec_command('ls')

for line in stdout:
    print(line.rstrip())
time.sleep(1)
client.close()
