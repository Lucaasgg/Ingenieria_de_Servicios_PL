import getpass
import telnetlib

HOST = "localhost"
user = input("Enter your remote account: ")
password = getpass.getpass()

tn = telnetlib.Telnet(HOST)

tn.read_until(b"login: ")
tn.write(user.encode('ascii') + b"\n")
if password:
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")

# Wait for the prompt before sending ls
tn.read_until(b"$ ")
tn.write(b"ls\n")

# Read until the next prompt, which captures ls output
output = tn.read_until(b"$ ")
print(output.decode('utf-8', errors='replace'))

tn.write(b"exit\n")
