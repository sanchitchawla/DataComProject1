#!/usr/bin/env python

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

def network(HOST,PORT,PATH):
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
	print cont_len
	clientSocket.close()

	return text


def getPort(url):
	work = urlparse(url)
	return work.port # well, gets the port number


#if len(sys.argv) ==4 and sys.argv[1]== "-o" or len(sys.argv) == 4 and sys.argv[-3]== "-c":

parseSTR = urlparse(urr)
netloc = parseSTR.netloc
if "https" in netloc:
	print "Sorry we don't support https :/"	
path = parseSTR.path
text=network(netloc, PORT, path)
with open("/home/sanchit/Desktop"+ "sanchit.jpg", "wb") as file:
	file.write(text)
	
