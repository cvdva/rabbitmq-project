import json
from src import send

if __name__ == "__main__":
    # name = input("Your institution name: \n")
    # person = input("Your name: \n")
    # app = input("Application and version: \n")
    # sourceID = input("Your source ID if known (Enter if unknown): \n")
    # form = input("Current format of your data: \n")
    # private = input("Would you like this data only sent to one group? (True/False): \n")
    # date = input("Enter date of data creation (MM/DD/YY): \n")
    # size = input("Data size (in MB): \n")

    name = "CNU"
    person = "Cassie"
    dataID = '010'
    form = 'A'

    data = {}
    data['name'] = name
    data['person'] = person
    data['dataID'] = dataID
    data['format'] = form
    json_data = json.dumps(data)
    send.main(json_data, 'request')
