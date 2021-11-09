import json
import src.send_reply
import src.need_data_queue
import src.send
import src.send_final_data

if __name__ == "__main__":

    # print('Welcome to the messaging system.')
    # name = input('Please input your name: \n')
    # institution = input('Input your institution \n')
    name = 'Cassie'
    institution = 'CNU'

    data = {}
    data['name'] = name
    data['institution'] = institution
    data['sourceID'] = 0
    json_data = json.dumps(data)
    queue = src.send_reply.RPCSender('register')
    print('Sent request server. Waiting on reply')
    reply = queue.call(json_data)
    # path = input('Reply received. Enter path of file\n')
    # json_path = input("Input JSON file path \n")
    path = 'https://drive.google.com/file/d/11n9T0tAIlXkz7AVjTSmgKDsLY0HLohCn/view?usp=sharing'
    byte_path = str.encode(path)
    json_path = '/Users/cassie/Documents/School Stuff/CNU/Thesis Monster/PyCharm Projects/RabbitMQ/src/example_json'
    file = src.send.encode_json(json_path)

    src.send.main(file, 'hello')
    dataID = src.need_data_queue.main(reply)
    print("Data id is {}".format(dataID))
    dataID = str(dataID)
    src.send_final_data.main(byte_path, dataID)


