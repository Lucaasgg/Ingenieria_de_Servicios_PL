import socket
import sys


if len(sys.argv) > 4:
    print("USO: python3 %s [IP] [puerto] [debug]" % sys.argv[0], file=sys.stderr)
    quit
elif len(sys.argv) == 1:
    IP = "127.0.0.1"
    port = 9999
else:
    IP = sys.argv[1]
    port = int(sys.argv[2])

s = socket.socket()
s.connect((IP,port))

for i in range(5):
    s.send("ABCDE\n".encode("utf-8"))

s.send("FINAL".encode("utf-8"))
s.close()
