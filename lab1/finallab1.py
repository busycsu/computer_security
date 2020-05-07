import socket
import struct
from message_pb2 import Message
from message_pb2 import Message4
from message_pb2 import Message5

HOST = 'cs177.seclab.cs.ucsb.edu'
PORT = 12690
prev = -1

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
print("")

def request(x):
	print("****requesting*****")
	msg = Message()
	msg.type = x
	m_len = len(msg.SerializeToString())
	s.send(struct.pack('>H', m_len))
	s.send(msg.SerializeToString())
	print("send: ",struct.pack('>H', m_len))
	print("send: ",msg.SerializeToString())
	print("")

def receive():
	print("****receiving*****")
	mlen = s.recv(1)
	print("mlen: ",mlen)
	m_len = int.from_bytes(mlen, byteorder='big', signed=False)

	if m_len == 0:
		mlen =s.recv(1)
		print("mlen: ",mlen)
		m_len = int.from_bytes(mlen, byteorder='big', signed=False)

	print("after m_len:", m_len)
	data = s.recv(m_len)
	print("data: ",data)
	tmp = len(data)
	print("len: ", tmp)
	while tmp != m_len:
		print("incomplete")
		data+=s.recv(m_len-tmp)
		print("data: ", data)
		tmp = len(data)
		print("new tmp: ", tmp)
	msg = Message()
	msg.ParseFromString(data)
	if msg.type == 9:
		msg = Message4()
		msg.ParseFromString(data)
	print("")
	return msg

list = []


def response(rec):
	print("****response*****")
	x = rec.type


	if x == 1:
		print("type is 1")

		key = rec.keyorcount
		value = rec.msg
		prev = rec.msg
		exist = False
		for e in list:
			if e[0] == key:
				e[1] = value
				exist = True;
			
		if not exist:
			list.append([key,value])
		#ack success
		msg = Message()
		msg.type = 2
		m_len = len(msg.SerializeToString())
		s.send(struct.pack('>H', m_len))
		print("send: ",struct.pack('>H', m_len))
		s.send(msg.SerializeToString())
		print("send: ",msg.SerializeToString())
		print("finish send")
		print("")

		return
	if x == 3:
		print("type is 3")

		key = rec.keyorcount

		for e in list:
			if e[0] == key:
				msg = Message4()
				msg.type = 4
				msg.value = e[1]
				m_len = len(msg.SerializeToString())
				s.send(struct.pack('>H', m_len))
				print("send: ",struct.pack('>H', m_len))
				s.send(msg.SerializeToString())
				print("send: ",msg.SerializeToString())
				print("type 4 is sent")
				return
			
		# for e in list:
		# 	if e[0] == key:
		# 		msg = Message4()
		# 		msg.type = 4
		# 		print("e: ",e)
		# 		msg.value = e[1]
		# 		m_len = len(msg.SerializeToString())
		# 		s.send(struct.pack('>H', m_len))
		# 		print("send: ",struct.pack('>H', m_len))
		# 		s.send(msg.SerializeToString())
		# 		print("send: ",msg.SerializeToString())
		# 		print("type 4 is sent")
		# 		return

		msg = Message5()
		msg.type = 5
		m_len = len(msg.SerializeToString())
		s.send(struct.pack('>H', m_len))
		print("send: ",struct.pack('>H', m_len))
		s.send(msg.SerializeToString())
		print("type 5 is sent")

		return

	if x == 6:
		print("type is 6")

		msg = Message()
		msg.type = 7
		msg.keyorcount = len(list)
		m_len = len(msg.SerializeToString())
		s.send(struct.pack('>H', m_len))
		print("send: ",struct.pack('>H', m_len))
		s.send(msg.SerializeToString())
		print("send: ",msg.SerializeToString())
		print("finish send")
		print("")

		return

	if x == 8:
		print("type is 8")
		print("")
		return
	if x == 9:
		print("bingo")
		return

r = 0
while r!=8 and r!=9:
	request(0)
	temp = receive()
	response(temp)
	r = temp.type
	if r == 9:
		print(temp.value)
	print(list)
















