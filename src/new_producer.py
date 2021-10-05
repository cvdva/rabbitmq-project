import json
from src import send_reply

if __name__ == "__main__":

    name = "Cassie"
    sourceID = '100'
    institution = "CNU"

    data = {}
    data['name'] = name
    data['sourceID'] = sourceID
    data['institution'] = institution
    json_data = json.dumps(data)
    queue = send_reply.RPCSender('register')
    reply = queue.call(json_data)
    print(reply)
