## A wrapper around the python low-level socket api, made by Tyler Clarke, April 5, 2020.
## Feel free to use and distribute under the terms of any freeware license you care to mention

## When using, just extend the ServerListenable class and define the handle_post and handle_get functions (each with the arguments self, data, and connection).
## And the handle_aux function, if you want to.

## The webserver can be run by creating an object of your extended class, and calling the run function on it.

## Enjoy!

import socket
import json
class ServerListenable:
    def __init__(self,host,port):
        self.sckt=socket.socket()
        self.sckt.bind((host,port))
        self.inittasks(host,port)
    def run(self):
        self.sckt.listen(5)
        while True:
            self.connection, (client_host, client_port) = self.sckt.accept()
            recieved=self.connection.recv(1024)
            try:
                ppt=self.parseRequest(recieved)
                if ppt["reqtype"]=="POST":
                    self.handle_post(ppt,self.connection)
                elif ppt["reqtype"]=="GET":
                    self.handle_get(ppt,self.connection)
                else:
                    raise Exception
            except Exception as e:
                self.handle_aux(recieved,self.connection)
            self.connection.close()
    def inittasks(self,host,port):
        pass
    def handle_post(self,data,connection):
        pass
    def handle_get(self,data,connection):
        pass
    def handle_aux(self,req,connection):
        pass
    def send_file_headers(self, connection, typ):
        connection.send("HTTP/1.0 200 OK\n".encode())
        bork = "Content-Type: " + typ + "\n"
        connection.send(bork.encode())
        connection.send("\n".encode())
    def parseRequest(self,data):
        toreturn={}
        copy=data.decode()
        copy=copy.replace("\r","")
        toreturn["rawrequesttext"]=str(copy)
        copy=copy.split("\n\n")
        toreturn["content"]=str(copy[1])
        toreturn["rawheaders"]=str(copy[0])
        cop=copy[0].split("\n")
        for x in cop[1:]:
            p=x.split(": ")
            toreturn[p[0]]=p[1]
        top=cop[0].split(" ")
        toreturn["reqtype"]=top[0]
        toreturn["reqlocation"]=top[1]
        toreturn["reqhttpversion"]=top[2]
        return toreturn
