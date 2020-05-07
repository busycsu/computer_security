from scapy.all import *
ip_layer = IP(dst="www.google.com")
icmp_layer = ICMP(type=8, code =0)

ip_layer.show()
icmp_layer.show()

pkt = ip_layer / icmp_layer
pkt.show()

response = sr1(ip_layer / icmp_layer)