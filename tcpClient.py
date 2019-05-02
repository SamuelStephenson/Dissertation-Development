import socket

def Main():
    turn = None
    #host = raw_input ("Please enter the IP address of the server you wish to connect to")
    host = '192.168.150.45'# this is the server IP
    port = 5000#this is the port on the server

    #------Note that we do not need to specify Client IP and port ------#

    s = socket.socket()#create a new socket
    s.connect((host, port))#create a socket with the server details
   
    go = s.recv(1024)# recieve ID from server
    print go
    if go in ["1"]:
        turn= True
        them = "2"
    elif go in ["2"]:
        turn = False
        them="1"

    print"You are connected to the server, and you are player " + go

    while True:
        
        if turn == True:
            message = raw_input("\n Please enter a message-> ")
            if message in ["quit","Q","q"]:
                s.close()
                break
            s.send(message)
            turn = False

        #------now we get data back from the server------#
        
        elif turn == False:
            print "\nwaiting for the other guy\n"
            data = s.recv(1024)
            print " person " + them + " says ----> " + data
            turn = True


if __name__ == '__main__':#run main
    Main()

    
        
