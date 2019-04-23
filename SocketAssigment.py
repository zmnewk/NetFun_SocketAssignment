#import socket module
from socket import *
import sys # In order to terminate the program

#Create a socket with family and type as default
serverSocket = socket(AF_INET, SOCK_STREAM)
#Prepare a sever socket

#Sets the serverPort integer variable to a suitable port
serverPort = 6000

#Bind Socket to an address. Format determined by family(AF_INET above)
serverSocket.bind(('49.195.49.211', serverPort)) 

#Tell socket to listen to up to 1 connection at a time
serverSocket.listen(1)

while True:
    #Establish the connection
    print('Ready to serve...')
    
    #Set up a new connection from the client
    connectionSocket, addr = serverSocket.accept()          
    try:
        #Take data recieved from client and store in variable message
        message = connectionSocket.recv(1024)  #Fill in start                        
        #filename is the 2nd item in HTTP header
        filename = message.split()[1]                 
        
        # Exclude "/" from filename and open file with that name
        f = open(filename[1:])                        
        
        #Put data from the read file into variable outputdata
        outputdata = f.read                 
        #Send one HTTP header line into socket
        connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
                       
        #Send the content of the requested file to the client
        for i in range(0, len(outputdata)):           
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())
        
        #Close client socket
        connectionSocket.close()
        
    except IOError:
        #Send response message for file not found
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode)
        connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())

        
        #Close client socket
        connectionSocket.close()
        
        
        
serverSocket.close()
sys.exit()#Terminate the program after sending the corresponding data                                    
