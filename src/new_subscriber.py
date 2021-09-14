import json
from src import send_reply

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
    sourceID = ""

    data = {}
    data['name'] = name
    data['sourceID'] = sourceID
    data['person'] = person
    json_data = json.dumps(data)
    queue = send_reply.RPCSender('subscribe')
    reply = queue.call(json_data)
    print("Reply: {}".format(reply))
