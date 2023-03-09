import json  # python library to read json files into dictionaries
import random


def read_from_jason(path):
    reading = open(path_to_json)  # open json object for reading
    json_data = json.load(reading)  # read the json data into the json_data dictionary
    flight_time = json_data["time"]  # first key of dict is a time signature
    flight_list = json_data["states"]  # second key of dict is list of lists with all flight info

    return flight_list  # return the flight list


def sort_flight_list(flight_list):
    sorted_flight_list = flight_list.copy()  # Need copy function here otherwise we will sort original list in place
    sorted_flight_list.sort(key=lambda x: x[2])  # Sort the list of lists by the 3rd index, which is the country name

    return [sorted_flight_list, flight_list]  # return the sorted flight list and original flight list


def create_security_key(flight_list_item):
    security_key = [None] * len(flight_list_item)  # creates a security key list for the data of one flight
    for i in range(len(security_key)):
        security_key[i] = random.randint(1, 4)  # dummy function to create random security levels, will replace this
    return security_key  # return the created security key


path_to_json = r"C:\Users\mmkdu\Documents\json for lab 4\opensky1.json"  # change this to the path to json file
flight_list = read_from_jason(path_to_json)
sorted_flight_list = sort_flight_list(flight_list)[0]
security_key = create_security_key(flight_list[0])

print("Unsorted flight list: ")
print(flight_list)  # print original list of lists for flights
print(" ")
print("First Flight Data with Security Levels: ")  # print sorted data for first flight with security levels
for x in range(len(sorted_flight_list[0])):
    print(str(sorted_flight_list[0][x]) + ", " + "Level " + str(security_key[x]))
