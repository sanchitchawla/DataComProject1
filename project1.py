#! /usr/bin/python

import socket as soc
from urlparse import urlparse
import argparse 
import sys

urr = "http://www.muic.mahidol.ac.th/eng/wp-content/uploads/2016/10/TEA-banner-960x330-resized-1.jpg"
PORT=80 

def downloadrqt(host,path,GETHEAD):
	if GETHEAD:
		getorhead = "GET "
	else : getorhead = "HEAD "
	return getorhead + path + " HTTP/1.1\r\n" + "Host: " + host + "\r\n\r\n"

def getlength(HOST,PORT,PATH):
	clientSocket = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
	clientSocket.connect((HOST,PORT))
	print "connected"
	header = downloadrqt(HOST,PATH,False)
	clientSocket.send(header)
	text = ""
	res = clientSocket.recv(1024)
	cont_len=""
	while len(res) != 0:
		text += res
		res = clientSocket.recv(1024)
		for i in text[text.find("Content-Length") + 16:]:
			if i =="\r":
				break
			cont_len+=i
	cont_len=int(cont_len)
	clientSocket.close()
	return cont_len

def downloadpls(HOST,PORT,PATH):
	clientSocket = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
	clientSocket.connect((HOST,PORT))
	print "connected again"
	header = downloadrqt(HOST,PATH,True)
	clientSocket.send(header)
	text = ""
	res = clientSocket.recv(1024)
	cont_len=""
	while len(res) != 0:
		text += res
		res = clientSocket.recv(1024)
	lis= text.split("\r\n\r\n")
	return lis[1]

if len(sys.argv) ==4 and sys.argv[1]== "-o" or len(sys.argv) == 6 and sys.argv[-3]== "-c":
	parseSTR = urlparse(sys.argv[-1])
	fileName=sys.argv[2]
	netloc = parseSTR.hostname
	if "https" in netloc:
		print "Sorry we don't support https :/"	
		sys.exit
	path = parseSTR.path
	length=getlength(netloc, PORT, path)
	text=downloadpls(netloc,PORT,path)
	with open("/home/sanchit/Desktop/"+ fileName, "wb+") as file:
		file.write(text)
	
