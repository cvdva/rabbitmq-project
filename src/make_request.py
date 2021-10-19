import json
import src.send_reply

if __name__ == "__main__":

    name = "CNU"
    person = "Cassie"
    dataID = '1005'
    form = 'CSV'

    data = {}
    data['name'] = name
    data['person'] = person
    data['dataID'] = dataID
    data['format'] = form
    json_data = json.dumps(data)
    queue = src.send_reply.RPCSender('request')
    reply = queue.call(json_data)
    print("Reply: {}".format(reply))
