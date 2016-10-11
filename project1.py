#! /usr/bin/python

import socket as soc
from urlparse import urlparse
import sys

def downloadrqt(host,path):
	return "GET " + path + " HTTP/1.1\r\n" + "Host: " + host + "\r\n\r\n"

def isRedirect(HOST,PORT,PATH):
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
	ol= lis[0].split("\r\n")
	if "301" in ol[0] or "302" in ol[0]:
		idc,head=ol[3].split(": ")
		url = urlparse(head)
		HOST = url.hostname
		if url.port== None: PORT=80
		else: PORT=80
		PATH = url.path
		if PATH=="" or PATH== None:
			PATH="/"
	clientSocket.close()
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
	print lis[0]
	cont_len= lis[0].split("\r\n")
	final= cont_len[-3].split(": ")
	return lis[1], final[1]

# def downloadpls(HOST,PORT,PATH):
# 	clientSocket = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
# 	clientSocket.connect((HOST,PORT))
# 	header = downloadrqt(HOST,PATH)
# 	clientSocket.send(header)
# 	text = "" 
# 	res = clientSocket.recv(8096)
# 	cont_len=[]
# 	while len(res) != 0:
# 		text += res
# 		res = clientSocket.recv(8096)
# 	lis= text.split("\r\n\r\n")
# 	cont_len= lis[0].split("\r\n")
# 	final= cont_len[-3].split(": ")
# 	return lis[1], final[1]

if len(sys.argv) ==4 and sys.argv[1]== "-o":
	if "https" in sys.argv[-1]:
		print "Sorry we don't support https :/"	
		sys.exit(2)
	parseSTR = urlparse(sys.argv[-1])
	if parseSTR.port == None: PORT = 80
	else: PORT = parseSTR.port
	fileName=sys.argv[2]
	HOST = parseSTR.hostname
	PATH = parseSTR.path
	if PATH=="" or PATH== None:
		PATH="/"
	#isRedirect(HOST,PORT,PATH)
	text,length=isRedirect(HOST,PORT,PATH)
	if type(length)!= int:
		print "Cannot fetch Content- Length"
	with open("/home/sanchit/Desktop/"+ fileName, "wb+") as file:
		file.write(text)
	
