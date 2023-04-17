
# import socket programming library
import socket
 
# import thread module
# from _thread import *
import threading
 
print_lock = threading.Lock()
 
# thread function
def threaded(test_message):
    
    host = "10.171.227.118"
    port = 12345
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to port", port)
 
    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")
    
    #while True:
    c, addr = s.accept()
    print_lock.acquire()
        #if addr[0]:
            #print("Connection established")
            #break
    
            
    print('Connected to :', addr[0], ':', addr[1])

    while True:
 
        # data received from client
        data = c.recv(1024)
        print("Received from client: " + str(data.decode('ascii')))
        if not data:
            print('Bye')
             
            # lock released on exit
            print_lock.release()
            break
 
        # reverse the given string from client
        data = data[::-1]
 
        # send back reversed string to client
        #c.send(data)
        c.send(test_message.encode('ascii'))
 
    # connection closed
    c.close()
    s.close()
 
 
def Main():
    test_message = "poop"
    host = "10.171.227.118"
 
    # reserve a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = 12345
    t1 = threading.Thread(target=threaded, args=(test_message,))
    t1.start()
    t1.join()
    
 
 
if __name__ == '__main__':
    Main()

