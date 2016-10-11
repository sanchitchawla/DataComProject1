#! /usr/bin/python

import socket as soc
from urlparse import urlparse
import sys

def downloadrqt(host,path):
	return "GET " + path + " HTTP/1.1\r\n" + "Host: " + host + "\r\n\r\n"

def downloadpls(HOST,PORT,PATH):
	clientSocket = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
	clientSocket.connect((HOST,PORT))
	header = downloadrqt(HOST,PATH)
	clientSocket.send(header)
	text = "" 
	res = clientSocket.recv(8096)
	cont_len=[]
	while len(res) != 0:
		text += res
		res = clientSocket.recv(8096)

	lis= text.split("\r\n\r\n")
	cont_len= lis[0].split("\r\n")
	final= cont_len[-3].split(": ")
	return lis[1], final[1]

if len(sys.argv) ==4 and sys.argv[1]== "-o":
	if "https" in sys.argv[-1]:
		print "Sorry we don't support https :/"	
		sys.exit(2)
	elif "http" not in sys.argv[-1]:
		print "is your http correct?"
		sys.exit(2)
	parseSTR = urlparse(sys.argv[-1])
	if parseSTR.port == None: PORT = 80
	else: PORT = parseSTR.port
	fileName=sys.argv[2]
	netloc = parseSTR.hostname
	path = parseSTR.path
	text,length=downloadpls(netloc,PORT,path)
	with open("/home/sanchit/Desktop/"+ fileName, "wb+") as file:
		file.write(text)
	
