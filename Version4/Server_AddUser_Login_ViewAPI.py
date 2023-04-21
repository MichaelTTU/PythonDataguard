
# import socket programming library
import socket

from opensky_api import OpenSkyApi
 
# import thread module
# from _thread import *
import threading
import datetime
 
print_lock = threading.Lock()
#test_list = [1,2,3,4]

def options(socket_conn, Login_Dict, Clearance_Dict, current_user, API_States_Dict):
    
    print("current user: " + str(current_user))
    data = socket_conn.recv(2048)   #  receive choice from client
    decoded_data = data.decode('ascii')
    choice = str(decoded_data)
    
    if choice == "1":
        print("checking user security level")
        
        if Clearance_Dict[current_user] < 4:
            print(str(current_user) + " is not authorized to add a new user")
            socket_conn.sendall("1001".encode('ascii'))
            current_user = options(socket_conn, Login_Dict, Clearance_Dict, current_user, API_States_Dict)
            # return back to option select
        else:
            new_user = ["",""]
            socket_conn.sendall("authorized".encode('ascii'))
            
            data = socket_conn.recv(2048)
            decoded_data = data.decode('ascii')
            socket_conn.sendall("received".encode('ascii'))
            new_user[0] = str(decoded_data)
            
            data = socket_conn.recv(2048)
            decoded_data = data.decode('ascii')
            new_user[1] = str(decoded_data)
            
            if new_user[0] in Login_Dict.keys():
                socket_conn.sendall("A User with this username already exists".encode('ascii'))
                print("A User with this username already exists")
                options(socket_conn, Login_Dict, Clearance_Dict, current_user, API_States_Dict)
            else:
                socket_conn.sendall("Username is unique".encode('ascii'))
                Login_Dict[new_user[0]] = new_user[1]
                print(Login_Dict)
            
                data = socket_conn.recv(2048)
                decoded_data = data.decode('ascii')
                Clearance_Dict[new_user[0]] = int(str(decoded_data))
                receipt_string = "User " + str(new_user[0]) + " created with clearance level " + str(decoded_data)
                socket_conn.sendall(receipt_string.encode('ascii'))
                options(socket_conn, Login_Dict, Clearance_Dict, current_user, API_States_Dict)
            
        
    if choice == "2": # LOGOUT
        current_user = "NoUser"
        print("current user: " + current_user)
        login(socket_conn, Login_Dict, Clearance_Dict, current_user, API_States_Dict)
        pass
    
    if choice == "3":
        pass
        
    if choice == "4":
        view_api_calls(socket_conn, API_States_Dict, current_user, Login_Dict, Clearance_Dict)
        pass


    #receive option choice
    #if tree
    #return to options depending on tree


def login(socket_conn, Login_Dict, Clearance_Dict, current_user, API_States_Dict):
    attempted_login = ["username", "password"]
    
    data = socket_conn.recv(2048)
    decoded_data = data.decode('ascii')
    attempted_login[0] = str(decoded_data)
    return_msg = "received "+ str(decoded_data)
    print("attempted login with username: "+ str(decoded_data))
    socket_conn.sendall(return_msg) 

    data = socket_conn.recv(2048)
    decoded_data = data.decode('ascii')
    if str(decoded_data) == "":
        print("aint shit here")
    attempted_login[1] = str(decoded_data)
    return_msg = "received "+ str(decoded_data)
    print("attempted login with password: "+ str(decoded_data))
    socket_conn.sendall(return_msg)
    
    data = socket_conn.recv(2048)
    
    if attempted_login[0] in Login_Dict.keys():
        print("username exists")
        
        if Login_Dict[attempted_login[0]] == attempted_login[1]: # successful login
            print("login successful")
            socket_conn.sendall("626".encode('ascii'))
            options(socket_conn, Login_Dict, Clearance_Dict, attempted_login[0], API_States_Dict) # change current user on successful login
        else:
            print("invalid username or password")  # failed login
            socket_conn.sendall("8008".encode('ascii'))
            login(socket_conn, Login_Dict, Clearance_Dict, current_user, API_States_Dict)
    else:
        print("invalid username or password")  # failed login
        socket_conn.sendall("8008".encode('ascii'))
        login(socket_conn, Login_Dict, Clearance_Dict, current_user, API_States_Dict)
    
    return attempted_login[0]
            

def view_api_calls(socket_conn, API_States_Dict, current_user, Login_Dict, Clearance_Dict):

    print("current user: " + str(current_user))

    while True:
 
        # data received from client
        data = socket_conn.recv(2048)   # for the very first communcation, server is the receiver
        incoming_message = str(data.decode('ascii'))
        print("Received from client: " + incoming_message)
        if not data:
            print('Bye')
             
            # lock released on exit
            print_lock.release()
            break
 
        blank_line = " "
        length_message = "length:" + str(len(API_States_Dict.keys()))
        socket_conn.sendall(length_message.encode('ascii'))  # sending length of API Dict
        data = socket_conn.recv(2048)
        decoded_data = data.decode('ascii')
        if decoded_data == "length received":
            incoming_message = str(data.decode('ascii'))
            key_choices = []
            
            print("Received from client: " + incoming_message)  # Receive confirmation of length from Client
            for x in API_States_Dict.keys():  # Send each key from the API Dict
                socket_conn.sendall(x.encode('ascii'))
                #c.sendall(blank_line.encode('ascii'))
                key_choices = key_choices + [x]
                data = socket_conn.recv(2048)
                
            print("sent all keys in dict")
            ##extra stuff here
            decoded_data = verify_input_choice(socket_conn, API_States_Dict)
                
            #if (1 <= x && x <= 100)
            
            #=IF(COUNTIF(data,E5)>0,"Yes","No")
            
            print("Client key choice: " + str(decoded_data))
            AccessStringChoice = API_States_Dict.keys()[int(decoded_data)]
            lengthline = "Length:" + str(len(API_States_Dict[AccessStringChoice][0].keys()))
            socket_conn.sendall(lengthline.encode('ascii'))  # Send length
            data = socket_conn.recv(2048)
            print(lengthline)  # print lengthline
            
            for x in API_States_Dict[AccessStringChoice][0].keys():
                sendline = str(x) + ": " + str(API_States_Dict[AccessStringChoice][0][x])
                socket_conn.sendall(sendline.encode('ascii'))
                data = socket_conn.recv(2048)
                print(sendline)
                
            send_complete_string = "sent all info in " + AccessStringChoice
            print(send_complete_string)
            socket_conn.sendall(send_complete_string.encode('ascii'))
        else: 
            #data = c.recv(2048)
            #print"
            #decoded_data = data.decode('ascii')
            if decoded_data == 'fail':
                print("wrong input from client")
                socket_conn.sendall("wrong input from client".encode('ascii'))
                pass
                
        data = socket_conn.recv(2048)
        decoded_data = data.decode('ascii')
        if str(decoded_data) == "continue":
            socket_conn.sendall("continuing api call viewing".encode('ascii'))
            pass
        else:
            socket_conn.sendall("ending api call viewing".encode('ascii'))
            break
            
    options(socket_conn, Login_Dict, Clearance_Dict, current_user, API_States_Dict)
    
    
    

def verify_input_choice(socket_conn, API_States_Dict):
    
    invalid_string = "Invalid Choice. Please choose a valid option from the list"
    
    data = socket_conn.recv(2048) ##
    decoded_data = data.decode('ascii') # Receive the type of input expected
    input_type = str(decoded_data)
    input_message = "input type of " + input_type + " received"
    socket_conn.sendall(input_message.encode('ascii'))

    data = socket_conn.recv(2048)##
    decoded_data = data.decode('ascii') # Receive the choice of key from Client
    print("type of data received: " + str(type(decoded_data)))
    
    if input_type == "pick previous api call":
        print("if statement for " + input_type)
    
        verifying = True
        while verifying:
            print("in while loop")
            if str(decoded_data).isdigit():
                
                if ((int(str(decoded_data)) >= 0) and int(str(decoded_data)) <= len(API_States_Dict.keys())):
                    verifying = False
                    print("valid input received")
                else:
                    print("input fails in-range check")
                    socket_conn.sendall("13112".encode('ascii'))
                    print("send invalid input key")
                    data = socket_conn.recv(2048)
                    decoded_data = data.decode('ascii')
            else:
                print("input fails isdigit() check")
                socket_conn.sendall("13112".encode('ascii'))
                print("sent invalid input key")
                data = socket_conn.recv(2048)
                decoded_data = data.decode('ascii')
        
    if input_type == "username password":
        print("if statement for " + input_type)
        pass
    
    if input_type == "make api call":
        print("if statement for " + input_type)
        pass
    
    return decoded_data


def convert_message():
    print("make this")

def API_get_states(API_States_Dict, current_user):
    api = OpenSkyApi()
    s = api.get_states()
    AccessTimestamp = datetime.datetime.now()
    converted_dict = {}
    
    for x in vars(s.states[0]):
        converted_dict[x] = str(vars(s.states[0])[x])
    
    Access_Info_String = current_user + "---" + str(AccessTimestamp) + "---" + str(converted_dict["origin_country"])
    print(Access_Info_String)
    API_States_Dict[Access_Info_String] = [converted_dict, 3]
    
    for x in vars(s.states[0]):
        message = x + ": " + str(vars(s.states[0])[x])
        encoded_message_line = message.encode('ascii')
        #encoded_message_list = message_list + [message_line]

    return API_States_Dict

 
# thread function
def threaded(test_message, test_list, test_dict, current_user, API_States_Dict, Login_Dict, Clearance_Dict):   # for the very first communcation, server is the receiver
    
    host = "10.175.226.40"
    port = 12345
    test_list[0] = test_list[0] + 5
    test_dict["FromThread"] = 2
    #API_Dict[Access_Info_String] = [sorted_flight_info, SecurityLevel]
    API_States_Dict = API_get_states(API_States_Dict, current_user)
    
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
    #encoded_message_list = message_list
    
    current_user = login(c, Login_Dict, Clearance_Dict, current_user, API_States_Dict) #login is attempted, need this uncommented on both client and server when you want to run it
    #options(c, Login_Dict, Clearance_Dict, current_user)
    #view_api_calls(c, API_States_Dict, current_user)

    # connection closed
    c.close()
    s.close()
 
 
def Main():
    test_list = [1,2,3,4]
    Clearance_Dict = {"Superuser" : 4, "Babyuser" : 1}
    current_user = "Superuser"
    #current_user = "Babyuser"
    Login_Dict = {"Superuser" : "Super", "Babyuser" : "Baby"}
    
    #API_Dict[Access_Info_String] = [sorted_flight_info, SecurityLevel]
    test_dict = {"Placeholder": 1}
    API_States_Dict = {"DefaultCall" : [test_dict, 1]}
    test_message = "poop"
    #host = "10.175.226.40"
 
    # reserve a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = 12345
    print("Current API dict: ")
    print(API_States_Dict)
    t1 = threading.Thread(target=threaded, args=(test_message, test_list, test_dict, current_user, API_States_Dict, Login_Dict, Clearance_Dict))
    t1.start()
    t1.join()
    print("Resulting API dict: ")
    print(API_States_Dict)
 
 
if __name__ == '__main__':
    Main()

