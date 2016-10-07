#!/usr/bin/env python

import socket as s
from urlparse import urlparse
import argparse 
import sys

def network():
	text = ""
	res = connection.recv(1024)
	while len(res) != 0:
		text += res
		res = connection.recv(1024)
	return text

def connect(HOST,PORT):
	try:
		clientSocket = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
		clientSocket.connect((HOST, PORT))
		connection = clientSocket
		return connection
	except Exception, e:
		"Something is wrong, Windows Style"
	else:
		print "Can't connect"


def hostpath(url):
	work = urlparse(url)
	ls = []
	ls.append(work.host) # at index 0 we append the host
	path= work.path
	if work.query!="":
		path = path + "?" + query
	ls.append(path) # at index 1 we append the path + query if there is one
	return ls  #return a list of [host,path]

def getPort(url):
	work = urlparse(url)
	return work.port # well, gets the port number

def downloadrqt(host,path,GETHEAD):
	if GET:
		getorhead = "GET"
	else : getorhead = "HEAD"
	return getorhead + path + " HTTP/1.1\r\n" + "Host: " + host + "\r\n\r\n"

def continuerqt(host,path,date,lastStop):
	return "GET " + path + " HTTP/1.1\r\n" + "Host: " + host + "\r\n" + "If-Range: " + date + "Range: " + "bytes=" + lastStop + "-" + "\r\n\r\n"


connection=connect(HOST,PORT)
with open(fileName, "wb") as file:
	file.write(content)
	
if len(sys.argv) ==4:
	URL = sys.argv[-1]
	HOST,PATH = hostpath(URL)
	fileName = sys.argv[2]
	PORT= getPort(URL)
	connection = connect()
	header = downloadrqt(HOST,PATH,True)
	connection.send(header)
	buffer=network()
	content = buffer.split('\r\n\r\n')

	with open(outDirectory +  fileName, "wb") as file:
		file.write(content)
	
	socket.close()
