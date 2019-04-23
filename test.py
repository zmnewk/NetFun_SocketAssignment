import socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostname = socket.gethostname()
serverPort = 6000
print hostname
serverSocket.bind((socket.gethostname(), serverPort))    