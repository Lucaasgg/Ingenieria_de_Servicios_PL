import socket
import sys

def RecvReply(sock, code):
    respuesta = sock.recv(1024)
    print("Respuesta del servidor:", respuesta.decode())
    if respuesta[:3] != code:
        print(f"Error: se esperaba el código {code.decode()}, pero se recibió {respuesta[:3].decode()}")
        sys.exit()


server = "relay.uniovi.es"
port = 25
fromaddr = "uo295421@uniovi.es" 
toaddr = "uo295421@uniovi.es"
subject = "Prueba desde email_envia_crudo.py"
data = "Este es un mensaje de prueba enviado usando comandos SMTP crudos."


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((server, port))


RecvReply(sock, b'220')
sock.send(b"HELO uniovi.es\r\n")
RecvReply(sock, b'250')

sock.send(f"MAIL FROM:<{fromaddr}>\r\n".encode())
RecvReply(sock, b'250')

sock.send(f"RCPT TO:<{toaddr}>\r\n".encode())
RecvReply(sock, b'250')

sock.send(b"DATA\r\n")
RecvReply(sock, b'354')


message = """To: %s
From: %s
Subject: %s\r\n\r\n
%s
\r\n.\r\n""" % (toaddr, fromaddr, subject, data)

sock.send(message.encode())
RecvReply(sock, b'250')


sock.send(b"QUIT\r\n")
RecvReply(sock, b'221')

sock.close()