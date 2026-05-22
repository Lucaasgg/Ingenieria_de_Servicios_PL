import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('localhost', username='alumno', password='alumno')

sftp = client.open_sftp()
listado = sftp.listdir()
for nombre in listado:
    print(nombre)
