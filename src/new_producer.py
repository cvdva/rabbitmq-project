import json
import src.send_reply
import src.need_data_queue
import src.send
import src.send_final_data


def write_to_file(file_name, data):
    with open(file_name, 'a') as f:
        f.write("\n")
        f.write(data)


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
    path = '/Users/cassie/Desktop/hi.txt'
    with open(path, 'rb') as f:
        contents = f.read()
    json_path = '/Users/cassie/Documents/School Stuff/CNU/Thesis Monster/PyCharm Projects/RabbitMQ/src/example_json'
    file = src.send.encode_json(json_path)

    queue = src.send_reply.RPCSender('hello')
    dataID = queue.call(file)
    write_to_file("datum.csv", "{}, {}".format(dataID, path))
    src.need_data_queue.main(reply)
    # print("Data id is {}".format(dataID))
    # dataID = str(dataID)
    # src.send_final_data.main(contents, dataID)


