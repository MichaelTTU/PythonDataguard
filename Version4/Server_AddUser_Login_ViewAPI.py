# Import socket module
# client code
import socket
import threading

def clearance_level_check():
	pass


def login(socket_conn):
    attempted_login = ["username", "password"]
    attempted_login[0] = input("Enter your username: ")
    if attempted_login[0] == "":
        blank = True
        while(blank):
            attempted_login[0] = input("No username was entered. Please enter your username: ")
            if attempted_login[0] != "":
                blank = False
    attempted_login[1] = input("Enter your password: ")
    if attempted_login[1] == "":
        blank = True
        while(blank):
            attempted_login[1] = input("No password was entered. Please enter your password: ")
            if attempted_login[1] != "":
                blank = False
    
    socket_conn.sendall(attempted_login[0].encode('ascii')) # sending username
    data = socket_conn.recv(2048)
    decoded_data = data.decode('ascii')
    print(str(decoded_data))
    
    socket_conn.sendall(attempted_login[1].encode('ascii')) # sending password
    data = socket_conn.recv(2048)
    decoded_data = data.decode('ascii')
    print(str(decoded_data))
    
    socket_conn.sendall("was login successful".encode('ascii'))
    data = socket_conn.recv(2048)
    decoded_data = data.decode('ascii')
    print(str(decoded_data))
    
    if str(decoded_data) == "626": # successful login
        print("Login Successful")
        options(socket_conn)
        pass
    else:
        print("Invalid username or password")
        login(socket_conn)
   

def view_api_calls(socket_conn, pick_previous_api_call):

    message = "message"
    message2 = "length received"
    message_length = -1
    keys_from_dict = []
    info_from_dict = []
    
    while True:

        test_func()
        socket_conn.sendall(message.encode('ascii'))  # for the very first communication, client is the sender
        data = socket_conn.recv(2048)
        decoded_data = data.decode('ascii')
        #length: 123
        print('Received from the server :',str(decoded_data))
        if decoded_data[0:6] == "length":  # if received message is a length message
            message_length = decoded_data.split(":", -1)[1] 
            ans = input("Receive message of length " + str(message_length) + "? (y/n)")
            print(" ")
            if ans == 'y':
                socket_conn.sendall(message2.encode('ascii'))
                for x in range(int(message_length)):  # receive all series of message of specified length
                    data = socket_conn.recv(2048)
                    decoded_data = data.decode('ascii')
                    keys_from_dict = keys_from_dict + [decoded_data]
                    socket_conn.sendall(message2.encode('ascii'))
                    print(str(x) + ": " + str(decoded_data))
                
                decoded_data = verify_input_choice(socket_conn, pick_previous_api_call)

                message_length = decoded_data.split(":", -1)[1]
                print(str(decoded_data))
                print("length " + message_length)
                socket_conn.sendall(message2.encode('ascii'))
                for x in range(int(message_length)):
                    data = socket_conn.recv(2048)
                    decoded_data = data.decode('ascii')
                    info_from_dict = info_from_dict + [decoded_data]
                    socket_conn.sendall(message2.encode('ascii'))
                    print(str(decoded_data), end='\n')
                    
                data = socket_conn.recv(2048)
                decoded_data = data.decode('ascii')
                print(str(decoded_data))
                print("received all")
                #print(decoded_data)
            else:
                failmsg="fail"
                print("Wrong input from client",end='\n')
                socket_conn.sendall(failmsg.encode('ascii'))
                data = socket_conn.recv(2048)
                decoded_data = data.decode('ascii')
                print(str(decoded_data))
                pass
                
                
        # ask the client whether he wants to continue
        ans = input('\nContinue viewing previous api calls? (y/n) :')
        print(" ")
        if ans == 'y':
            socket_conn.sendall("continue".encode('ascii'))
            data = socket_conn.recv(2048)
            continue
        else:
            socket_conn.sendall("end".encode('ascii'))
            data = socket_conn.recv(2048)
            break
            
    options(socket_conn)
    


def request_api_call():
	pass

def options(socket_conn):
    
    print(" ")
    print("1) Add a user")
    print("2) Logout")
    print("3) Make API call")
    print("4) View previous API calls")
    
    choice = input("choose from the listed options: ")
    
    if choice == "1":
        # ADD A USER
        print("checking user security level")
        socket_conn.sendall(choice.encode('ascii'))
        data = socket_conn.recv(2048)
        decoded_data = data.decode('ascii')
        
        
        if str(decoded_data) == "1001":
            print("Current user is not authorized to add a new user")
            options(socket_conn)
            # return back to option select
        else:
            login_pair = ["username", "password"]
            login_pair[0] = input("Enter a username for the new user: ")
            if login_pair[0] == "":
                blank = True
                while(blank):
                    login_pair[0] = input("No username was entered. Please enter a username: ")
                    if login_pair[0] != "":
                        blank = False

            login_pair[1] = input("Enter a password for the new user: ")
            if login_pair[1] == "":
                blank = True
                while(blank):
                    login_pair[1] = input("No password was entered. Please enter a password: ")
                    if login_pair[1] != "":
                        blank = False            
            
            socket_conn.sendall(login_pair[0].encode('ascii'))
            data = socket_conn.recv(2048)
            decoded_data = data.decode('ascii')
            print(str(decoded_data))
            
            socket_conn.sendall(login_pair[1].encode('ascii'))
            data = socket_conn.recv(2048)
            decoded_data = data.decode('ascii')
            print(str(decoded_data))
            if str(decoded_data) == "A User with this username already exists":
                print(str(decoded_data) + ". Returning to options select screen")
                options(socket_conn)
            
            clearance_level = input("Choose a clearance level for the new user (between 3 and 0): ")
            if clearance_level.isdigit() and int(clearance_level) >= 0 and int(clearance_level) <= 3:
                socket_conn.sendall(str(int(clearance_level)).encode('ascii'))
                data = socket_conn.recv(2048)
                decoded_data = data.decode('ascii')
                print(str(decoded_data))
                options(socket_conn)
                
                pass
            else:
                checking = True
                while(checking):
                    print("Unacceptable clearance level chosen. Choose a clearance level for the new user (between 3 and 0): ")
                    clearance_level = input("Choose a clearance level for the new user (between 3 and 0): ")
                    
                    if clearance_level.isdigit() and int(clearance_level) >= 0 and int(clearance_level) <= 3:
                        socket_conn.sendall(str(int(clearance_level)).encode('ascii'))
                        data = socket_conn.recv(2048)
                        decoded_data = data.decode('ascii')
                        print(str(decoded_data))
                        checking = False
                options(socket_conn)
                        
                    
    if choice == "2":
        socket_conn.sendall(choice.encode('ascii'))
        login(socket_conn)
        pass
        
    if choice == "3":
        socket_conn.sendall(choice.encode('ascii'))
        pass
        
    if choice == "4":
        socket_conn.sendall(choice.encode('ascii'))
        view_api_calls(socket_conn, "pick previous api call")
        pass
        
    else:
        socket_conn.sendall(choice.encode('ascii'))
        pass

def test_func():
    print("this is from the test function")

def verify_input_choice(socket_conn, input_type):
    incorrect_string = "13112"
    
    socket_conn.sendall(input_type.encode('ascii')) # Send type of expected input to server
    data = socket_conn.recv(2048)
    decoded_data = data.decode('ascii')
    print(str(decoded_data))
    
    input_choice = input(input_type + " (type number):")
    if input_choice == "":
        blank = True
        while(blank):
            input_choice = input("No input was entered. Please enter an input: ")
            if input_choice != "":
                blank = False
                
    socket_conn.sendall(str(input_choice).encode('ascii')) # Send choice of key to server
    data = socket_conn.recv(2048)
    decoded_data = data.decode('ascii')
    verifying = True
    while verifying:
        print("in while loop")
        
        if str(decoded_data) == incorrect_string:
            print("Invalid Choice. Please choose a valid option from the list")
            input_choice = input(input_type + " (type number):")
            if input_choice == "":
                blank = True
                while(blank):
                    input_choice = input("No input was entered. Please enter an input: ")
                    if input_choice != "":
                        blank = False
                        
            socket_conn.sendall(str(input_choice).encode('ascii'))
            data = socket_conn.recv(2048)
            decoded_data = data.decode('ascii')
        else:
            verifying = False
    
    return decoded_data


def threaded(test_message, LoginDict):   # for the very first communication, client is the sender
    
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
    
    login(s)    # login is attempted, need this uncommented on both client and server when you want to run it
    #options(s)
    #view_api_calls(s, "pick previous api call")

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
