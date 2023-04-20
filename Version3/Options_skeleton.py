def options(socket_conn):
	
	print("1) Add a user")
	print("2) Logout")
	print("3) Make API call")
	print("4) View previous API calls")
	
	choice = input("choose from the listed options: ")
	
	if choice == "1":
		print("checking user security level")
        socket_conn.sendall(choice)
        
		#check security level of user with server
		
	if choice == "2":
		print("returning to login function")
		#login function runs
	
	if choice == "3":
		print("Requesting API call")
		#make api call function runs
	
	if choice == "4":
		print("Requesting list of previous API calls")
		#existing code to show previous API calls runs, need to wrap into function
    else:
        print("Invalid option. Please select an option from the list")
