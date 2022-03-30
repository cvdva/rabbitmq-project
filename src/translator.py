import csv
import json
import src.send
import src.handler
import src.init_queue
import src.send_reply
import src.final_queue
import src.need_data_queue
import src.send_need_data
import src.send_final_data
import src.announce_queue_translator
from multiprocessing import Process


def write_to_file(file_name, data):
    with open(file_name, 'a') as f:
        f.write("\n")
        f.write(data)


def open_file(file_name):
    list = []
    with open(file_name, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            list.append(row)
    return list


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
    dataID = body['dataID']
    source = body['sourceID']
    lines = open_file("translator_data.csv")
    dids = []
    ndids = []
    forms = []
    for line in lines:
        dids.append(line[1])
        ndids.append(line[0])
        forms.append(line[2])
    translations = []
    translation_list = [('txt', 'csv'), ('txt', 'word'), ('word', 'txt')]
    for line in translation_list:
        if form == line[0]:
            new_form = line[1]
            if source == '99':
                pass
            else:
                if dataID in dids:
                    index = dids.index(dataID)
                    if forms[index] == new_form:
                        pass
                    else:
                        translations.append(line[1])
                else:
                    translations.append(line[1])
    return translations


def announce_sub(body):
    translations = check_translate(body)
    for t in translations:
        announce_listen(t, body)
        # json_data = json.dumps(body)
        # src.send.main(json_data, 'announce')


def announce_listen(new_format, body):
    old_dataID = body['dataID']
    source = body['sourceID']
    body['format'] = new_format
    body['sourceID'] = '99'
    body['private'] = 'False'
    print(body)
    bodyj = json.dumps(body)
    queue = src.send_reply.RPCSender('hello')
    new_dataID = queue.call(bodyj)
    new_dataID = new_dataID.decode('utf-8')
    new_dataID = str(new_dataID)
    write_to_file("translator_data.csv", "{}, {}, {}, {}".format(new_dataID, old_dataID, new_format, source))
    # p = Process(target=listen)
    # p.start()
    listen()


def listen():
    src.need_data_queue.main('1')


def pull_translation(dataID):
    trans = open_file("translator_data.csv")
    new_dataIDs = []
    old_dataIDs = []
    new_format = []
    source = []
    for line in trans:
        new_dataIDs.append(line[0])
        old_dataIDs.append(line[1])
        new_format.append(line[2])
        source.append(line[3])
    index = new_dataIDs.index(dataID)
    original = old_dataIDs[index]
    source = source[index]
    ex_format = new_format[index]
    message = {}
    message['dataID'] = original
    data = json.dumps(message)
    # p = Process(target=src.send_need_data.main, args=(data, source))
    # p.start()
    src.send_need_data.main(data, source.strip())
    src.final_queue.main(original.strip())




if __name__ == "__main__":
    listen()
