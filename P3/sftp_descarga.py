import paramiko
from stat import S_ISDIR

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('localhost', username='alumno', password='alumno')

sftp = client.open_sftp()
sftp.chdir("ISPL")
list = sftp.listdir()
for f in list:
    if not S_ISDIR(sftp.stat(f).st_mode):
        print("Descargando " + f)
        sftp.get(f, f + "-d")
