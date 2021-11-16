import csv
import threading
import json
import src.send
import src.init_queue
import src.send_reply
import src.need_data_queue
import src.announce_queue_translator


def write_to_file(file_name, data):
    with open(file_name, 'a') as f:
        f.write("\n")
        f.write(data)


def open_file(file_name):
    '''
    Opens the csv file under the name given
    :param file_name: The name of the file to be open
    :return: Raw list from the csv
    '''
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
    if len(translations) >= 1:
        for i in range(len(translations)):
            x = threading.Thread(target=announce_listen(translations[i], body), daemon=True)
            x.start()
    else:
        pass


def announce_listen(new_format, body):
    old_dataID = body['dataID']
    source = body['sourceID']
    body['format'] = new_format
    body['sourceID'] = '99'
    body['private'] = 'False'
    bodyj = json.dumps(body)
    queue = src.send_reply.RPCSender('hello')
    new_dataID = queue.call(bodyj)
    new_dataID = new_dataID.decode('utf-8')
    new_dataID = str(new_dataID)
    write_to_file("translator_data.csv", "{}, {}, {}".format(new_dataID, old_dataID, new_format, source))




if __name__ == "__main__":
    translation_list = [('txt', 'csv'), ('txt', 'word'), ('word', 'txt')]
    json_path = '/Users/cassie/Documents/School Stuff/CNU/Thesis Monster/PyCharm Projects/RabbitMQ/src/example_json'
    name = json_path + ".json"
    with open(name) as f:
        d = json.load(f)
        d = json.dumps(d)
    queue1 = src.send_reply.RPCSender('hello')
    dataID = queue1.call(d)
