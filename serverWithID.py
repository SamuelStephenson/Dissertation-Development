import socket, select
ID=1

#function to broadcast chat messages to all connected clients
def broadcast_data (sock, message):
        
        #Do not send the message to master socket and the client who has send us teh message
        for socket in CONNECTION_LIST:
            if socket != server_socket and socket != sock:
                try :
                    socket.send(message)
                except :
                        #broken socket connection may be, chat client pressed crtl+c for example
                        socket.close()
                        CONNECTION_LIST.remove(socket)
if __name__ == "__main__":
         
        #List to keep track of socket descriptors
        CONNECTION_LIST = []
        RECV_BUFFER = 4096 #Advisable to keep is as an expoent of 2
        PORT = 5000

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #this has no effect, why?
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(("0.0.0.0", PORT))
        server_socket.setblocking(0)
        server_socket.listen(10)

        #add server socket to the list of readable connections
        CONNECTION_LIST.append(server_socket)

        print "Chat server started on port" + str(PORT)
        
        while 1:
                #get the list sockets which are ready to be read through select
                read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
                for sock in read_sockets:
                        #mew connection
                        if sock == server_socket:
                                #Handle the case in which there is a new connection recived thorugh server_socket
                                sockfd, addr = server_socket.accept()

                                CONNECTION_LIST.append(sockfd)
                                print "Client (%s, %s) is online" % addr
                                print ID
                                turn= str(ID)
                                ID = ID +1
                                sockfd.send(turn)
                                #broadcast_data(sockfd, "The other player is turn " + turn)
                                

                        #some incoming message from a client
                        else:
                                try:
                                        #in windows, sometimes when a tcp ptogram claoses abruptly
                                        #a "connection reset by peer" execption will be thrown
                                        data = sock.recv(RECV_BUFFER)
                                        
                                        if data:
                                                #broadcast_data(sock, "\r" + '<' + str(sock.getpeername()) + '>' + data)
                                                broadcast_data(sock, data)

                                except:
                                        broadcast_data(sock, "client (%s, %s) is offline" % addr)
                                        print "Client (%s, %s) is offline" % addr
                                        sock.close()
                                        CONNECTION_LIST.remove(sock)
                                        continue
                        
        server_socket.close()                    
                                
