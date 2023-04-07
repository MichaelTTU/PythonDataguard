LoginDict = {"Superuser":'Superpassword'} # Master dictionary that holds all login-password pairs
ClearanceDict = {"Superuser":4} # Master dictionary that holds all clearance levels 

def options(username, LoginDict, ClearanceDict): # General options function, acts as "main"
  print("1) Add a user")
  print("2) Logout")
  print("3) Add a document")
  print("4) View a document")
  choice = input("choose from the listed options: ")
  if choice == "1" and ClearanceDict[username] == 4: # Checks for highest clearance level before allowing to add a user
    add_user()
    options(username, LoginDict, ClearanceDict)
  if choice == "2":
    login(LoginDict, ClearanceDict)
  else:
    print("option unavailable.")
    options(username, LoginDict, ClearanceDict)

def add_user(): # Function to add a user, only avaiable to clearance level 4
  login_pair = ["username", "password"]
  login_pair[0] = input("Enter a username: ")
  login_pair[1] = input("Enter a password: ")
  LoginDict[login_pair[0]] = login_pair[1] # Adds the username and password pair to master dict
  ClearanceDict[login_pair[0]] = 1
  

def login(LoginDict, ClearanceDict): # Login function
  attempted_login = [" "," "]
  attempted_login[0] = input("Enter your username: ")
  attempted_login[1] = input("Enter your password: ")
  if LoginDict[attempted_login[0]] == attempted_login[1]: # Checks if the user and password pair exist in LoginDict
    print("Login credentials accepted.")
    options(attempted_login[0], LoginDict, ClearanceDict) # Returns to options screen once the login credentials are accepted
  else:
    print("Invalid username or password. ") # Returns to the login screen if the login credentials are not accepted
    login(LoginDict, ClearanceDict)
    
login(LoginDict, ClearanceDict) # Login must be called once at the start of the program for the initial user
