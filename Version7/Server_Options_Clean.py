
import socket
import random
import threading
from opensky_api import OpenSkyApi
from datetime import datetime
 
print_lock = threading.Lock()

def add_user(socket_conn, Login_Dict, Clearance_Dict, current_user, API_States_Dict):
    
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


def API_request_get_states(API_States_Dict, current_user, socket_conn, Login_Dict, Clearance_Dict):
    socket_conn.sendall("Specify an origin country for new states data if you would like (formatting example: United States): ".encode('ascii'))
    data = socket_conn.recv(2048)
    decoded_data = data.decode('ascii')
    
    flight_search_string = "Searching for a flight with states data from " + str(decoded_data)
    socket_conn.sendall(flight_search_string.encode('ascii'))
    returned_list = API_get_states(API_States_Dict, current_user, socket_conn, Login_Dict, Clearance_Dict, str(decoded_data))
    
    API_States_Dict = returned_list[0]
    data = socket_conn.recv(2048)
    socket_conn.sendall(returned_list[1].encode('ascii'))
    
    return API_States_Dict
    

def censor_info(socket_conn, Login_Dict, Clearance_Dict, current_user, API_States_Dict, current_line):
    if Clearance_Dict[current_user] == 4:
        pass
    else:
        random_int = random.randint(1, Clearance_Dict[current_user])
        if random_int == 1:
            current_line_list = current_line.split(":")
            current_line = str(current_line_list[0]) + ": ********"
    
    return current_line
    

def datetime_formatter(num_days, num_hours): # returns a timestamp of num_days before the current time
    now = datetime.now()
    split_now_string = str(now).split("-")
    split_now_string_day = split_now_string[2].split(" ")
    print(split_now_string)
    print(split_now_string_day)
    if int(split_now_string_day[0]) == 0:
        datetime_result = datetime(int(split_now_string[0]), int(split_now_string[1]), int(split_now_string_day[0]), 0, 0, 0)
    else:
        datetime_result = datetime(int(split_now_string[0]), int(split_now_string[1]), int(split_now_string_day[0]) - num_days, 0, 0, 0)
        
    return datetime_result


def options(socket_conn, Login_Dict, Clearance_Dict, current_user, API_States_Dict):
    
    print("current user: " + str(current_user))
    airport_code = "KAUS" # example airport, austin bergstrom international
    data = socket_conn.recv(2048)   #  receive choice from client
    decoded_data = data.decode('ascii')
    choice = str(decoded_data)
    
    if choice == "1": # ADD A USER
        add_user(socket_conn, Login_Dict, Clearance_Dict, current_user, API_States_Dict)
        
    if choice == "2": # LOGOUT
        current_user = "NoUser"
        print("current user: " + current_user)
        login(socket_conn, Login_Dict, Clearance_Dict, current_user, API_States_Dict)
    
    if choice == "3": # REQUEST API CALL
        API_get_arrivals_by_airport(API_States_Dict, current_user, airport_code, socket_conn, Login_Dict, Clearance_Dict)
        
    if choice == "4": # VIEW API CALLS
        view_api_calls(socket_conn, API_States_Dict, current_user, Login_Dict, Clearance_Dict)
        
    if choice == "5": #REQUEST GET STATES
        API_States_Dict = API_request_get_states(API_States_Dict, current_user, socket_conn, Login_Dict, Clearance_Dict)
        options(socket_conn, Login_Dict, Clearance_Dict, current_user, API_States_Dict)


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
 
        data = socket_conn.recv(2048)   # for the very first communcation, server is the receiver
        incoming_message = str(data.decode('ascii'))
        print("Received from client: " + incoming_message)
        if not data:
            print('Bye')
             
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
                key_choices = key_choices + [x]
                data = socket_conn.recv(2048)
                
            print("sent all keys in dict")
            decoded_data = verify_input_choice(socket_conn, API_States_Dict)
            
            print("Client key choice: " + str(decoded_data))
            AccessStringChoice = API_States_Dict.keys()[int(decoded_data)]
            lengthline = "Length:" + str(len(API_States_Dict[AccessStringChoice][0].keys()))
            socket_conn.sendall(lengthline.encode('ascii'))  # Send length
            data = socket_conn.recv(2048)
            print(lengthline)  # print lengthline
            
            for x in API_States_Dict[AccessStringChoice][0].keys(): # sending api call info
                sendline = str(x) + ": " + str(API_States_Dict[AccessStringChoice][0][x])
                sendline = censor_info(socket_conn, Login_Dict, Clearance_Dict, current_user, API_States_Dict, sendline)
                socket_conn.sendall(sendline.encode('ascii'))
                data = socket_conn.recv(2048)
                print(sendline)
                
            send_complete_string = "sent all info in " + AccessStringChoice
            print(send_complete_string)
            socket_conn.sendall(send_complete_string.encode('ascii'))
        else: 
            if decoded_data == 'fail':
                print("wrong input from client")
                socket_conn.sendall("wrong input from client".encode('ascii'))
                
        data = socket_conn.recv(2048)
        decoded_data = data.decode('ascii')
        if str(decoded_data) == "continue":
            socket_conn.sendall("continuing api call viewing".encode('ascii'))
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
                
                if ((int(str(decoded_data)) >= 0) and int(str(decoded_data)) < len(API_States_Dict.keys())):
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
        # could make this in the future if developers want to redifine the username password requirements
    
    if input_type == "make api call":
        print("if statement for " + input_type)
        # could make this in the future if developers want to adjust the api call inputs
    
    return decoded_data


def API_get_states(API_States_Dict, current_user, socket_conn, Login_Dict, Clearance_Dict, custom_option):
    api = OpenSkyApi()
    s = api.get_states()
    AccessTimestamp = datetime.now()
    converted_dict = {}
    flight_choice = 1
    call_security_level = 3

    for x in s.states:
        if x.origin_country == custom_option:
            print("found a flight in "+custom_option)
            flight_choice = x # flight_choice is a FlightData object if a country with the specified name is found. Otherwise it is an int.
            break
    if isinstance(flight_choice, int):
        print("option is int")
        for x in vars(s.states[flight_choice]):
            converted_dict[x] = str(vars(s.states[flight_choice])[x])
            print(x)
            print(str(vars(s.states[flight_choice])[x]))
        print(str(converted_dict["origin_country"]))
        flight_search_result = "No flights from specified origin country found. Returning get_states call with a flight from "+ str(converted_dict["origin_country"]) + " instead."
    else:
        print("option is object")
        for y in vars(flight_choice):
            converted_dict[y] = str(vars(flight_choice)[y])
            print(y)
            print(str(vars(flight_choice)[y]))
        flight_search_result = "Flight from "+ custom_option +" found. Returning get_states call for most recent flight from " + custom_option + "."

    Access_Info_String = current_user + "---" + str(AccessTimestamp) + "---" +"States"+"---"+ "OriginCountry_" + str(converted_dict["origin_country"]) + "---Callsign_"+str(converted_dict["callsign"])
    print(flight_search_result)
    print(Access_Info_String)
    API_States_Dict[Access_Info_String] = [converted_dict, call_security_level]

    return [API_States_Dict, flight_search_result]
    
    
def API_get_arrivals_by_airport(API_States_Dict, current_user, airport_code, socket_conn, Login_Dict, Clearance_Dict):
    api = OpenSkyApi()
    day_count = 5
    five_day = datetime_formatter(day_count,0)
    unix_timestamp_now = (datetime.now() - datetime(1970,1,1, 0, 0)).total_seconds()
    unix_timestamp_five_day = (five_day - datetime(1970,1,1)).total_seconds()
    unix_timestamp_two_day = (datetime_formatter(2,0) - datetime(1970,1,1)).total_seconds()

    AccessTimestamp = datetime.now()
    converted_dict = {}
    
    socket_conn.sendall("Please provide an airport code".encode('ascii'))
    data = socket_conn.recv(2048)
    decoded_data = data.decode('ascii')
    airport_code = str(decoded_data)
    
    arrivals = api.get_arrivals_by_airport(airport_code, int(unix_timestamp_two_day), int(unix_timestamp_now))
    NoneType = type(None)
    if type(arrivals) == NoneType:
        print("Arrivals API call failed. Invalid airport code or no flights in time window.")
        socket_conn.sendall("Arrivals API call failed. Invalid airport code or no flights in time window.".encode('ascii'))
    else:
        socket_conn.sendall("airport exists".encode('ascii'))
        data = socket_conn.recv(2048) # receive day count
        decoded_data = data.decode('ascii')
        
        day_count = int(decoded_data)
        unix_timestamp_day_count = (datetime_formatter(day_count,0) - datetime(1970,1,1)).total_seconds()
        print("unix timestamp")
        print(str(int(unix_timestamp_day_count)))
        
        arrivals = api.get_arrivals_by_airport(airport_code, int(unix_timestamp_day_count), int(unix_timestamp_now))
        arrivals_info = str(len(arrivals)) + " arrivals at airport " + airport_code + " in the past " + str(day_count) + " days."
        print(arrivals_info)
        socket_conn.sendall(arrivals_info.encode('ascii')) # sending arrivals info
        data = socket_conn.recv(2048) # receiving confirmation 
        
        socket_conn.sendall(str(arrivals[0].callsign).encode('ascii')) # sending example callsign
        
        callsign_print_count = 10
        print("printing some callsigns")
        if callsign_print_count < len(arrivals):
            for x in range (callsign_print_count):
                print(str(arrivals[x].callsign))
        
        data = socket_conn.recv(2048) # receive callsign choice
        decoded_data = data.decode('ascii')
        print(type(arrivals[0].callsign))
        print(type(decoded_data))
        print(str(arrivals[0].callsign))
        print(str(decoded_data))
        
        callsign_index = 0
        for x in range(len(arrivals)):
            if str(arrivals[x].callsign).strip() == str(decoded_data).strip():
                print("callsign found")
                callsign_index = x
                StringToSend = "Arrival from aircraft with callsign " + str(decoded_data) + " found"
                socket_conn.sendall(StringToSend.encode('ascii')) # sending callsign found
                data = socket_conn.recv(2048)
                
                for x in vars(arrivals[callsign_index]):
                    converted_dict[x] = str(vars(arrivals[callsign_index])[x])
                
                Access_Info_String = current_user + "---" + str(AccessTimestamp) + "---" +"Arrival---AirportCode_"+str(airport_code) + "---Callsign_"+str(decoded_data) 
                print(Access_Info_String)
                API_States_Dict[Access_Info_String] = [converted_dict, 3]
                
                send_string = "Arrival at airport "+ airport_code + " with access string: " + Access_Info_String
                socket_conn.sendall(send_string.encode('ascii'))
                data = socket_conn.recv(2048)
                
                socket_conn.sendall("API Request added to database".encode('ascii'))
                print(converted_dict)
                options(socket_conn, Login_Dict, Clearance_Dict, current_user, API_States_Dict)
                
        socket_conn.sendall("callsign not found".encode('ascii')) # sending callsign not found
        print("callsign not found")
                
    options(socket_conn, Login_Dict, Clearance_Dict, current_user, API_States_Dict)


def threaded(test_message, test_list, test_dict, current_user, API_States_Dict, Login_Dict, Clearance_Dict):   # for the very first communcation, server is the receiver
    
    host = "10.175.226.40"
    port = 12345
    test_dict["FromThread"] = 2
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to port", port)
 
    s.listen(5)
    print("socket is listening")
    
    c, addr = s.accept()
    print_lock.acquire()
    print('Connected to :', addr[0], ':', addr[1])
    
    API_States_Dict = API_get_states(API_States_Dict, current_user, c, Login_Dict, Clearance_Dict, 0)[0]
    current_user = login(c, Login_Dict, Clearance_Dict, current_user, API_States_Dict) # Call login function which will call the option select function

    c.close()
    s.close()
 
 
def Main():
    test_list = [1,2,3,4]
    Clearance_Dict = {"Superuser" : 4, "Babyuser" : 1}
    current_user = "Superuser"
    Login_Dict = {"Superuser" : "Super", "Babyuser" : "Baby"}
    
    test_dict = {"Placeholder": 1}
    API_States_Dict = {"DefaultCall" : [test_dict, 1]}
    test_message = "testing"

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

