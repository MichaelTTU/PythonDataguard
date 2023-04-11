# PythonDataguard
Pieces of program that will need to be consolidated, then split between the two Pis

Client Pi will have the Login and Security Verification + Option Select screen code, and Viewing / Sorting code for API calls

Server Pi will have the API Call data storage code + security dict for each previous API call

------------------------------------------------------------------------
# WIP ideas:


Active Connection Process:  
-Pis connect, both active threads are now the connection threads  
-Server Pi passes the API Dict to the connection thread  
-Leave connection thead open in the manner that we are currently doing (with prompt from Client Pi to keep going)  
-Client Pi can pick options to create a custom API request string that is sent to Server  
-Server opens new API Call thread (and passes the API Dict) from the connection thread, acquires the flight data  
-Flight data is added to API Dict, API Call thread closes  
-Active thread is now connection thread, where it sends the flight data to the Client Pi  
-Connection waits for another prompt from Client Pi for a new API Call, or for list of previous API calls  
-Request for a list of previous API calls would result in Server Pi sending all keys in API Dict  
