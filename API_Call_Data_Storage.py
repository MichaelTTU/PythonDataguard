import datetime

LoginDict = {"SuperUser" : "Superpassword"} 
ClearanceDict = {"SuperUser" : 4}
API_Dict = {"DefaultCall" : [flight_info, 1]} # Dict containing all past API calls
CurrentUser = " " # Dict containing current user's username, it is populated by the login() 
                  # function and returned to blank by the logout() function

if ClearanceDict[CurrentUser] => 3:
    SecurityLevel = input("Enter Security Level for this API call")
else:
    SecurityLevel = 3
    
AccessTimestamp = datetime.datetime.now()
Access_Info_String = CurrentUser + "---" + AccessTimestamp + str(sorted_flight_info[0])
# Example Access_info_String = Michael1---2022-06-20 16:06:13.176788---Bermuda
# Can add takeoff location in addtion to the destination location to the Access Info Access_info_String

API_Dict[Access_Info_String] = [sorted_flight_info, SecurityLevel]
# Adds an entry to API_Dict with the Access Info String as the key, and a list as the value
# The list has the flight info at [0] and the security level at [1]
