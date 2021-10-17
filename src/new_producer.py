import json
import src.send_reply
import src.need_data_queue

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
    input('Reply received. Start listening? (Enter or ctl + c to exit)\n')
    src.need_data_queue.main(reply)

