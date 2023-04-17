
# import socket programming library
import socket

from opensky_api import OpenSkyApi
 
# import thread module
# from _thread import *
import threading
import datetime
 
print_lock = threading.Lock()
#test_list = [1,2,3,4]

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
def threaded(test_message, test_list, test_dict, current_user, API_States_Dict):
    
    host = "10.171.227.118"
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

    while True:
 
        # data received from client
        data = c.recv(2048)
        incoming_message = str(data.decode('ascii'))
        print("Received from client: " + incoming_message)
        if not data:
            print('Bye')
             
            # lock released on exit
            print_lock.release()
            break
 
        blank_line = " "
        length_message = "length:" + str(len(API_States_Dict.keys()))
        c.sendall(length_message.encode('ascii'))  # sending length of API Dict
        data = c.recv(2048)
        decoded_data = data.decode('ascii')
        if decoded_data == "length received":
            incoming_message = str(data.decode('ascii'))
            key_choices = []
            
            print("Received from client: " + incoming_message)  # Receive confirmation of length from Client
            for x in API_States_Dict.keys():  # Send each key from the API Dict
                c.sendall(x.encode('ascii'))
                #c.sendall(blank_line.encode('ascii'))
                key_choices = key_choices + [x]
                data = c.recv(2048)
                
            print("sent all keys in dict")
            data = c.recv(2048)
            decoded_data = data.decode('ascii') # Receive the choice of key from Client
            print("type of data received: " + str(type(decoded_data)))
            #print("int cast: " + str(int(decoded_data)))
            invalid_string = "Invalid Choice. Please choose a valid option from the list"
            verifying = True 
            while verifying:
                print("in while loop")
                if str(decoded_data).isdigit():
                    pass
                else:
                    print("invalid choice for is digit")
                    c.sendall("13112".encode('ascii'))
                    print("sending invalid string")
                    data = c.recv(2048)
                    decoded_data = data.decode('ascii')
                    continue
                
                if ((int(str(decoded_data)) >= 0) and int(str(decoded_data)) <= len(API_States_Dict.keys())):
                    verifying = False
                else:
                    print("invalid choice for in range")
                    c.sendall("13112".encode('ascii'))
                    print("sending invalid string")
                    data = c.recv(2048)
                    decoded_data = data.decode('ascii')
                    continue
                #verifying = True
                
            #if (1 <= x && x <= 100)
            
            #=IF(COUNTIF(data,E5)>0,"Yes","No")
            
            print("Client key choice: " + str(decoded_data))
            AccessStringChoice = API_States_Dict.keys()[int(decoded_data)]
            lengthline = "Length:" + str(len(API_States_Dict[AccessStringChoice][0].keys()))
            c.sendall(lengthline.encode('ascii'))  # Send length
            data = c.recv(2048)
            print(lengthline)  # print lengthline
            
            for x in API_States_Dict[AccessStringChoice][0].keys():
                sendline = str(x) + ": " + str(API_States_Dict[AccessStringChoice][0][x])
                c.sendall(sendline.encode('ascii'))
                data = c.recv(2048)
                print(sendline)
                
            print("sent all info in " + AccessStringChoice)
        else: 
            #data = c.recv(2048)
            #print"
            #decoded_data = data.decode('ascii')
            if decoded_data == 'fail':
                print("wrong input from client")
                pass
        
            

 
    # connection closed
    c.close()
    s.close()
 
 
def Main():
    test_list = [1,2,3,4]
    ClearanceDict = {"SuperUser" : 4}
    current_user = "SuperUser"
    
    #API_Dict[Access_Info_String] = [sorted_flight_info, SecurityLevel]
    test_dict = {"Placeholder": 1}
    API_States_Dict = {"DefaultCall" : [test_dict, 1]}
    test_message = "poop"
    host = "10.171.227.118"
 
    # reserve a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = 12345
    print("Current API dict: ")
    print(API_States_Dict)
    t1 = threading.Thread(target=threaded, args=(test_message, test_list, test_dict, current_user, API_States_Dict))
    t1.start()
    t1.join()
    print("Resulting API dict: ")
    print(API_States_Dict)
    
 
 
if __name__ == '__main__':
    Main()

