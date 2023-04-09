# Import socket module
# client code
import socket
import threading

def threaded(test_message):
    # local host IP '127.0.0.1'
    host = '10.171.227.118'
 
    # Define the port on which you want to connect
    port = 12345
 
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
 
    # connect to server on local computer
    s.connect((host,port))
 
    # message you send to server
    message = test_message

    while True:
 
        # message sent to server
        s.send(message.encode('ascii'))
 
        # message received from server
        data = s.recv(1024)
 
        # print the received message
        # here it would be a reverse of sent message
        print('Received from the server :',str(data.decode('ascii')))
 
        # ask the client whether he wants to continue
        ans = input('\nDo you want to continue(y/n) :')
        if ans == 'y':
            continue
        else:
            break
    # close the connection
    s.close()
    
 
 
def Main():
    test_message = "poop from client"
    thread1 = threading.Thread(target=threaded, args=(test_message,))
    thread1.start()
    thread1.join()
    print("done!")

 
if __name__ == '__main__':
    Main()
