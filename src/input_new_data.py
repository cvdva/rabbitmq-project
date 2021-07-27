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
    sourceID = ''
    person = "Cassie"
    app = "Civ v.3.1"
    form = 'A'
    private = 'False'
    date = '05/27/2021'
    size = '35'

    data = {}
    data['name'] = name
    data['sourceID'] = sourceID
    data['person'] = person
    data['app'] = app
    data['format'] = form
    data['private'] = private
    data['date'] = date
    data['size'] = size
    json_data = json.dumps(data)
    send.main(json_data)
