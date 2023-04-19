# Import socket module
# client code
import socket
import threading

def test_func():
    print("this is from the test function")

def verify_input_choice(socket_conn, input_type):
    incorrect_string = "13112"
    
    socket_conn.sendall(input_type.encode('ascii')) # Send type of expected input to server
    data = socket_conn.recv(2048)
    decoded_data = data.decode('ascii')
    print(str(decoded_data))
    
    input_choice = input(input_type + " (type number):")
    socket_conn.sendall(str(input_choice).encode('ascii')) # Send choice of key to server
    data = socket_conn.recv(2048)
    decoded_data = data.decode('ascii')
    verifying = True
    while verifying:
        print("in while loop")
        
        if str(decoded_data) == incorrect_string:
            print("Invalid Choice. Please choose a valid option from the list")
            input_choice = input(input_type + " (type number):")
            socket_conn.sendall(str(input_choice).encode('ascii'))
            data = socket_conn.recv(2048)
            decoded_data = data.decode('ascii')
        else:
            verifying = False
    
    return decoded_data


def threaded(test_message, LoginDict):
    
    host = "10.175.226.40"
    port = 12345
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((host,port))
    
    pick_previous_api_call = "pick previous api call"
    username_password = "username password"
    make_api_call = "make api call"
    
    
    ThreadDict = LoginDict
    message = test_message
    message2 = "length received"
    message_length = -1
    keys_from_dict = []
    info_from_dict = []

    while True:
        
        #verify_input(s)
        test_func()
        s.sendall(message.encode('ascii'))
        data = s.recv(2048)
        decoded_data = data.decode('ascii')
        #length: 123
        print('Received from the server :',str(decoded_data))
        if decoded_data[0:6] == "length":  # if received message is a length message
            message_length = decoded_data.split(":", -1)[1] 
            ans = input("Receive message of length " + str(message_length) + "? (y/n)")
            print(" ")
            if ans == 'y':
                s.sendall(message2.encode('ascii'))
                for x in range(int(message_length)):  # receive all series of message of specified length
                    data = s.recv(2048)
                    decoded_data = data.decode('ascii')
                    keys_from_dict = keys_from_dict + [decoded_data]
                    s.sendall(message2.encode('ascii'))
                    print(str(x) + ": " + str(decoded_data))
                
                decoded_data = verify_input_choice(s, pick_previous_api_call)

                message_length = decoded_data.split(":", -1)[1]
                print(str(decoded_data))
                print("length " + message_length)
                s.sendall(message2.encode('ascii'))
                for x in range(int(message_length)):
                    data = s.recv(2048)
                    decoded_data = data.decode('ascii')
                    info_from_dict = info_from_dict + [decoded_data]
                    s.sendall(message2.encode('ascii'))
                    print(str(decoded_data), end='\n')
                print("received all")
                #print(decoded_data)
            else:
                failmsg="fail"
                print("Wrong input from client",end='\n')
                s.sendall(failmsg.encode('ascii'))
                pass
                
                
        # ask the client whether he wants to continue
        ans = input('\nDo you want to continue communication(y/n) :')
        print(" ")
        if ans == 'y':
            continue
        else:
            break
    # close the connection
    s.close()
    
 
def Main():
    LoginDict = {"Superuser":'Superpassword'} # Master dictionary that holds all login-password pairs
    ClearanceDict = {"Superuser":4} # Master dictionary that holds all clearance levels 
    

    
    test_message = "poop from client"
    thread1 = threading.Thread(target=threaded, args=(test_message, LoginDict))
    thread1.start()
    thread1.join()
    print("done!")

 
if __name__ == '__main__':
    Main()
