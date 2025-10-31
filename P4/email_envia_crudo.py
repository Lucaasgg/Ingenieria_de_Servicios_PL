import sys
import socket

def RecvReply(sc, codigo):
    datos = sc.recv(1024)
    caracteres = datos[:3]
    if codigo != int(caracteres):
        print("El código proporcionado no coincide con el recibido", file=sys.stderr)
        sys.exit()

    print(datos.decode('utf-8'))
server = "relay.uniovi.es"
port = 25
toaddr = "uo293747@uniovi.es"
fromaddr = "uo293747@uniovi.es"
subject = "Práctica"
data = "Estoy haciendo la práctica"
message = """To: %s
From: %s
Subject: %s\r\n\r\n
%s
\r\n.\r\n""" % (toaddr, fromaddr, subject, data)
s = socket.socket()

s.connect((server, port))
RecvReply(s, 220)

command1 = "HELO %s\r\n" % server
print("Comando a enviar: %s" % command1)
s.sendall(command1.encode('utf-8'))
RecvReply(s, 250)

command2 = "MAIL FROM:<%s>\r\n" % fromaddr
print("Comando a enviar: %s" % command2)
s.sendall(command2.encode('utf-8'))
RecvReply(s, 250)

command3 = "RCPT TO:<%s>\r\n" % toaddr
print("Comando a enviar: %s" % command3)
s.sendall(command3.encode('utf-8'))
RecvReply(s, 250)

s.sendall("DATA\r\n".encode('utf-8'))
RecvReply(s, 354)

s.sendall(message.encode('utf-8'))
RecvReply(s, 250)

s.sendall("QUIT\r\n".encode('utf-8'))
RecvReply(s, 221)
