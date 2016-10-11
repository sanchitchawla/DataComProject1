#! /usr/bin/python

import socket as soc
from urlparse import urlparse
import sys

def downloadrqt(host,path):
	return "GET " + path + " HTTP/1.1\r\n" + "Host: " + host + "\r\n\r\n"

def myreceive(sock,MSGLEN):
        chunks = []
        bytes_recd = 0
        count=0
        while bytes_recd < MSGLEN:
            chunk = sock.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == '':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd +=len(chunk)
            print (bytes_recd/float(MSGLEN))*100
            print bytes_recd,MSGLEN
        return ''.join(chunks)

def downloadpls(HOST,PORT,PATH):
	clientSocket = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
	clientSocket.connect((HOST,PORT))
	header = downloadrqt(HOST,PATH)
	clientSocket.send(header)
	text = "" 
	cont_len=[]
	got=False
	mydic={}
	headbyte=0
	while True:
		res = clientSocket.recv(1024)
		text += res
		if "\r\n\r\n" in text:
			header,body=text.split("\r\n\r\n")
			eachhead=header.split("\r\n")
			for each in eachhead[1:]:
				hm=each.split(": ")
				mydic[hm[0]]= hm[1]
			length= int(mydic["Content-Length"])
			print length
			body+= myreceive(clientSocket,long(length)- long(len(body)))
			print "done!"
			clientSocket.close()
			break
	print "Download Completed"
	return body

if len(sys.argv) ==4 and sys.argv[1]== "-o":
	if "https" in sys.argv[-1]:
		print "Sorry we don't support https"	
		sys.exit(2)
	parseSTR = urlparse(sys.argv[-1])
	if parseSTR.port == None: PORT = 80
	else: PORT = parseSTR.port
	fileName=sys.argv[2]
	HOST = parseSTR.hostname
	PATH = parseSTR.path
	if PATH=="" or PATH== None:
		PATH="/"
	text=downloadpls(HOST,PORT,PATH)
	with open("/home/sanchit/Desktop/"+ fileName, "wb+") as file:
		file.write(text)
	