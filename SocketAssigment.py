#import socket module
from socket import *
import sys # In order to terminate the program
import threading

# function to use for the multithreading
def respond(connectionSocket):
	try:
        #Take data recieved from client and store in variable message
        message = connectionSocket.recv(1024)
        print('message recieved')
        #filename is the 2nd item in HTTP header
        filename = message.split()[1]                 
        
        # Exclude "/" from filename and open file with that name
        f = open(filename[1:])                        
        
        #Put data from the read file into variable outputdata
        outputdata = f.read()                 
        #Send one HTTP header line into socket
        connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
                       
        #Send the content of the requested file to the client
        for i in range(0, len(outputdata)):           
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())
        print('file sent')
        #Close client socket
        connectionSocket.close()
        
    except IOError:
        #Send response message for file not found
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())
        print('404 sent')
        
        #Close client socket
        connectionSocket.close()

#Create a socket with family and type as default
serverSocket = socket(AF_INET, SOCK_STREAM)
#Prepare a sever socket

#Sets the serverPort integer variable to a suitable port
serverPort = 6787

#Bind Socket to an address. Format determined by family(AF_INET above)
serverSocket.bind(("", serverPort)) 

#Tell socket to listen to up to 1 connection at a time
serverSocket.listen(1)

while True:
    #Establish the connection
    print('Ready to serve...')
    
    #Set up a new connection from the client
    connectionSocket, addr = serverSocket.accept()          
	
	# create a new thread, using the respond function, and passing in the socket for the client
	t = threading.Thread(target = respond, args = (connectionSocket))
	
	# mark the thread as a daemon ->  a computer program that runs as a background process, rather than being under the direct control of an interactive user. 
	t.daemon = True
	
	# start the thread
	t.start()

serverSocket.close()
sys.exit()#Terminate the program after sending the corresponding data                                    
