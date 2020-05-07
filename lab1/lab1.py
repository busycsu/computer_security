import socket
import struct
from message_pb2 import Message

HOST = 'cs177.seclab.cs.ucsb.edu'
PORT = 12690

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print ("socket created")

except socket.error as err:
	print ("Failed with error %s" %(err))


try: 
	host_ip = socket.gethostbyname(HOST) 
except socket.gaierror: 
  
	# this means could not resolve the host 
	print ("there was an error resolving the host")
	sys.exit() 
  
# connecting to the server 
s.connect((host_ip, PORT)) 
  
print ("the socket has successfully connected to cs177 on port == %s" %(host_ip)) 

# m_len = 1
# s.send(struct.pack("H",m_len))
# s.send(m_len)
msg = Message()
msg.type = 0


m_len = len(msg.SerializeToString())

# s.send(str(m_len).encode("utf-8"))
s.send(struct.pack('>H', m_len))
s.send(msg.SerializeToString())
# print("send: ",str(m_len).encode("utf-8"))
print("send: ",struct.pack('>H', m_len))
print("send: ",msg.SerializeToString())
print("m_len: ",m_len)

print("*************recv state***********")
mlen = s.recv(m_len)
print("mlen: ",mlen)
m_len = int.from_bytes(mlen, byteorder='big', signed=False)
print("after m_len:", m_len)
data = s.recv(m_len)
print("data: ",data)


print("*************response state***********")
msg.type = 7
msg.keyorcount = 0
m_len = len(msg.SerializeToString())
s.send(struct.pack('>H', m_len))
print("send: ",struct.pack('>H', m_len))
s.send(msg.SerializeToString())
print("send: ",msg.SerializeToString())
print("finish send")


print("*************ask state***********")
msg = Message()
msg.type = 0
m_len = len(msg.SerializeToString())
s.send(struct.pack('>H', m_len))
s.send(msg.SerializeToString())
# print("send: ",str(m_len).encode("utf-8"))
print("send: ",struct.pack('>H', m_len))
print("send: ",msg.SerializeToString())
print("m_len: ",m_len)

print("*************recv state***********")
print("m_len: ", m_len)
mlen = s.recv(m_len)
print("mlen: ",mlen)
m_len = int.from_bytes(mlen, byteorder='big', signed=False)
print("after m_len:", m_len)
data1 = s.recv(m_len)
print("data: ",data1)
msg = Message()
msg.ParseFromString(data1)
print("type: ", str(msg.type))
print("number: ", str(msg.keyorcount) )
print("value: ",msg.msg)





# while True:
# 	print("before m_len: ",m_len)
# 	mlen = s.recv(m_len)
# 	m_len = int.from_bytes(mlen, byteorder='big', signed=False)
# 	print("mlen: ",mlen)
# 	data = s.recv(m_len)
# 	print("after m_len:", m_len)
# 	print("data: ",data)
# 	msg.ParseFromString(data)
# 	if msg.type==6:
# 		print("rec: ", msg.type)
# 		msg.type = 7
# 		msg.keyorcount = 0
# 		m_len = len(msg.SerializeToString())
# 		s.send(struct.pack('>H', m_len))
# 		print("send: ",struct.pack('>H', m_len))
# 		s.send(msg.SerializeToString())
# 		print("send: ",msg.SerializeToString())
# 		print("finish send")

	

#  # Look for the response
# amount_received = 0
# amount_expected = 20
    
# while amount_received < amount_expected:
# 	data = s.recv(1024)
# 	amount_received += len(data)
# 	print("data: ",data)
# 	msg.ParseFromString(data)
# 	print("rec: ",msg.type)
# 	print("rec: ",msg.msg)


