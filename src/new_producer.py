import json
import src.send_reply
import src.need_data_queue
import src.send

if __name__ == "__main__":

    print('Welcome to the messaging system.')
    name = input('Please input your name: \n')
    institution = input('Input your institution \n')

    data = {}
    data['name'] = name
    data['institution'] = institution
    data['sourceID'] = 0
    json_data = json.dumps(data)
    queue = src.send_reply.RPCSender('register')
    print('Sent request server. Waiting on reply')
    reply = queue.call(json_data)
    path = input('Reply received. Enter path of file\n')
    json_path = input("Input JSON file path \n")
    file = src.send.encode_json(json_path)

    src.send.main(file, 'hello')
    src.need_data_queue.main(reply)

