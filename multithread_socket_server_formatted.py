import socket
import threading

API_Dict = {"DefaultCall": ["flight_info", 1]}  # Dict containing all past API calls
CurrentUser = " "  # Dict containing current user's username, it is populated by the login()
# function and returned to blank by the logout() function
print_lock = threading.Lock()

# thread function
def threaded(test_message):
    host = "10.171.227.118"  # static IP of server pi
    port = 12345  # chosen TCP port, can be any open port

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))  # bind the specified host and port to a socket object s
    print("socket binded to port", port)

    s.listen(5)  # listening state where socket object is waiting for a client connection
    print("socket is listening")

    c, addr = s.accept()  # accept function returns connection object c
    print_lock.acquire()
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
        # c.send(data)
        c.send(test_message.encode('ascii'))

    # close connections
    c.close()
    s.close()

def Main():
    test_message = "poop"

    t1 = threading.Thread(target=threaded, args=(test_message,))
    t1.start()
    t1.join()


if __name__ == '__main__':
    Main()
