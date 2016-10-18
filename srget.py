#! /usr/bin/python

import socket as soc
from urlparse import urlparse
import sys
import os

def downloadrqt(host,path):
	return "GET " + path + " HTTP/1.1\r\n" + "Host: " + host + "\r\n\r\n"

def HEADrqt(host,path):
	return "HEAD " + path + " HTTP/1.1\r\n" + "Host: " + host + "\r\n\r\n"

def conteenew(host,path,my):
	return "GET " + path + " HTTP/1.1\r\n" + "Host: " + host + "\r\n" +\
	"Connection: close" + "\r\n"+ "Range: bytes=" + str(my) + "-" "\r\n\r\n"
 		
def myreceive(h,file, sock,MSGLEN,name,bytes_recd):
	chunks = []
	while bytes_recd < MSGLEN:
		chunk = sock.recv(min(MSGLEN - bytes_recd, 2048))
		bytes_recd += len(chunk)
		file.write(chunk)
		h.write(str(bytes_recd)+ "\r\n")

def myreceiveresume(file, sock,MSGLEN,bytes_recd):
	chunks = []
	while bytes_recd < MSGLEN:
		chunk = sock.recv(min(MSGLEN - bytes_recd, 2048))
		bytes_recd += len(chunk)
		file.write(chunk)


def getmeeverything(text,h):
	mydic={}
	i=text.find("\r\n\r\n")
	header = text[:i]
	h.write(str(len(header))+"\r\n")
	body=text[i+4:]
	eachhead=header.split("\r\n")
	lenofhead= len(header)
	if not "200" in eachhead[0]:
		print "Sorry! We caught an error!"
		sys.exit(2)

	for each in eachhead[1:]:
		hm=each.split(": ")
		if "Content-Length" in each or "Last-Modified" in each or "ETag" in each :
			h.write(each+"\r\n")
		mydic[hm[0]]= hm[1]
	return mydic,body,lenofhead

def getmeeverythingforresume(text):
	mydic={}
	i=text.find("\r\n\r\n")
	header = text[:i]
	body=text[i+4:]
	lenofnewhead= len(header)
	eachhead=header.split("\r\n")

	if not "200" in eachhead[0]:
		print "Sorry! We caught an error!"
		sys.exit(2)

	for each in eachhead[1:]:
		hm=each.split(": ")
		mydic[hm[0]]= hm[1]
	return mydic,body,lenofnewhead,header

def downloadpls(HOST,PORT,PATH,name):
	fname,extension= name.split(".")
	with open(fname+ "sanchit","ab+") as file:
		with open("meta.txt","wb+") as h:
			clientSocket = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
			clientSocket.connect((HOST,PORT))
			header = downloadrqt(HOST,PATH)
			clientSocket.send(header)
			text = "" 
			while True:
				print "not resume"
				res = clientSocket.recv(1024)	
				text += res
				if "\r\n\r\n" in text:
					mydic ,body,lenofhead= getmeeverything(text,h)
					file.write(body)
					h.write(str(lenofhead))
					h.write(str(len(text))+ "\r\n")
					length= int(mydic["Content-Length"])
					myreceive(h,file, clientSocket, long(length), name, long(len(body)))
					clientSocket.close()
					break	
			os.rename(fname+"sanchit", fname + "." + extension)
			os.remove("meta.txt")
	

def resumedownload(HOST,PORT,PATH,name):
	fname,extension= name.split(".")
	clientSocket = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
	clientSocket.connect((HOST,PORT))
	header = HEADrqt(HOST,PATH)	
	clientSocket.send(header)
	text=""
	oldFile = fname+"sanchit"
	while True:
		res = clientSocket.recv(1024)	
		text += res
		if "\r\n\r\n" in text:
			mydic ,body,bs,bs2= getmeeverythingforresume(text)
			try:
				Etag= mydic["ETag"]
				Last= mydic["Last-Modified"]
			except Exception as e:
				print "Server Doesn't support resuming, sorry."
				sys.exit()
			length= int(mydic["Content-Length"])
			clientSocket.close()
			break

	if os.path.isfile(oldFile):
		lst = []
        string = oldFile
        lst = string.split("\r\n")
        with open("meta.txt","r") as fffile:
			byte = fffile.readlines()

			hm,prevEtag= byte[3].split(": ")
			hmmmm,prevLast= byte[2].split(": ")
			hmmm,prevLength = byte[1].split(": ")
			headerlen=byte[0].strip()
			sizz= byte[-1].strip()

	
	clientSocket = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
	clientSocket.connect((HOST,PORT))
	host = soc.gethostbyname(HOST)
	filesize=os.path.getsize(oldFile)  
	sendin=int(filesize) # - int(headerlen)
	header = conteenew(host,PATH,sendin)
	clientSocket.send(header)
	with open(fname+"sanchit","ab+") as writeout:
		if prevLast.strip()== Etag.strip() or Etag.strip()==prevEtag.strip():
			print "in the if"
			try:
				while True:
					res = clientSocket.recv(1024)	
					text += res
					if "\r\n\r\n" in text:
						mydic ,sechead,lenofnewhead,header= getmeeverythingforresume(text)
						meh,mehreal= sechead.split("\r\n\r\n") 
						writeout.write(mehreal)
						myreceiveresume(writeout, clientSocket, long(length),hehe+len(mehreal))
						clientSocket.close()
						break	
				os.rename(fname+"sanchit", name)
				os.remove("meta.txt")
			except KeyboardInterrupt  as e:
				sys.exit()
		else:
			downloadpls(HOST,PORT,PATH,name)


if len(sys.argv) ==4 and sys.argv[1]== "-o":
	if "https" in sys.argv[-1]:
		print "Sorry we don't support https"	
		sys.exit(2)
	parseSTR = urlparse(sys.argv[-1])
	if parseSTR.port == None: PORT = 80
	else: PORT = parseSTR.port
	fileName=sys.argv[2]
	fname,extension= fileName.split(".")
	HOST = parseSTR.hostname
	PATH = parseSTR.path
	if PATH=="" or PATH== None:
		PATH="/"
	if os.path.isfile(fname+"sanchit"):
		resumedownload(HOST,PORT,PATH,fileName)
	else:
		downloadpls(HOST,PORT,PATH,fileName)
	
# class Downloader(object):
# 	"""Trying to replicate my work in class form"""
# 	def __init__(self,HOST,PORT,PATH,fileName):
		
# 		super(ClassName, self).__init__()
# 		self.HOST= HOST
# 		self.PORT = PORT
# 		self.PATH = PATH
# 		self.fname,self.extension= fileName.split(".")
# 		self.name = fileName


# 	def downloadpls(self):
# 		with open(fname+ "sanchit","wb+") as file:
# 			with open("meta.txt","wb+") as h:
# 				clientSocket = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
# 				clientSocket.connect((HOST,PORT))
# 				header = downloadrqt(HOST,PATH)
# 				clientSocket.send(header)
# 				text = "" 
# 				while True:
# 					res = clientSocket.recv(1024)	
# 					text += res
# 					if "\r\n\r\n" in text:
# 						mydic ,body= getmeeverything(text,h)
# 						file.write(body)
# 						h.write(str(len(text))+ "\r\n")
# 						length= int(mydic["Content-Length"])
# 						myreceive(h,file, clientSocket, long(length), name, long(len(body)))
# 						clientSocket.close()
# 						break	
# 				os.rename(fname+"sanchit", fname + "." + extension)
# 				os.remove("meta.txt")