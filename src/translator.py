import pika, sys, os
import json
import src.init_queue
import src.send_reply
import src.need_data_queue


def init_translator():
    queue = src.send_reply.RPCSender('register')
    data = {}
    data['name'] = 'translator'
    data['institution'] = 'CNU'
    data['sourceID'] = '99'
    message = json.dumps(data)
    reply = queue.call(message)
    decoded = reply.decode('utf-8')
    if decoded == '0':
        src.need_data_queue.main(reply)
    else:
        return "Error connecting to server"


def check_translate(body):
    form = body['format']
    translations = []
    for line in translation_list:
        if form == line[0]:
            translations.append(line[1])
    return translations


def announce_listen(new_format, body):
    body['format'] = new_format



if __name__ == "__main__":
    translation_list = [('txt', 'csv'), ('txt', 'word'), ('word', 'txt')]
    print(init_translator())