import uuid
import socket

mac = uuid.getnode()
ip = socket.gethostbyname(socket.gethostname())

print("Mac address: ", mac)
print("As hex     : ", hex(mac))
print("IP address : ", ip)


