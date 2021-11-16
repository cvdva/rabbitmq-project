import pika, sys, os
import threading
import json
import src.send
import src.init_queue
import src.send_reply
import src.need_data_queue
import src.announce_queue_translator


def init_translator():
    queue = src.send_reply.RPCSender('register')
    data = {}
    data['name'] = 'translator'
    data['institution'] = 'CNU'
    data['sourceID'] = '99'
    message = json.dumps(data)
    reply = queue.call(message)
    decoded = reply.decode('utf-8')
    if decoded == '1':
        src.need_data_queue.main(reply)
    else:
        return "Error connecting to server"


def check_translate(body):
    form = body['format']
    translations = []
    translation_list = [('txt', 'csv'), ('txt', 'word'), ('word', 'txt')]
    for line in translation_list:
        if form == line[0]:
            translations.append(line[1])
    return translations


def announce_sub(body):
    translations = check_translate(body)
    if len(translations) >= 1:
        for i in range(len(translations)):
            x = threading.Thread(target=announce_listen(translations[i], body), daemon=True)
            x.start()
    else:
        pass


def announce_listen(new_format, body):
    body['format'] = new_format
    body['sourceID'] = '99'
    bodyj = json.dumps(body)
    queue = src.send_reply.RPCSender('hello')
    dataID = queue.call(bodyj)




if __name__ == "__main__":
    translation_list = [('txt', 'csv'), ('txt', 'word'), ('word', 'txt')]
    json_path = '/Users/cassie/Documents/School Stuff/CNU/Thesis Monster/PyCharm Projects/RabbitMQ/src/example_json'
    name = json_path + ".json"
    with open(name) as f:
        d = json.load(f)
    # queue1 = src.send_reply.RPCSender('hello')
    # dataID = queue1.call(file)
    announce_sub(d)