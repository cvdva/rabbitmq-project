import csv
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
        body['format'] = t
        body['sourceID'] = 99
        body['dataID'] += 1
        json_data = json.dumps(body)
        src.send.main(json_data, 'announce')


def announce_listen(new_format, body):
    old_dataID = body['dataID']
    source = body['sourceID']
    body['format'] = new_format
    body['sourceID'] = '99'
    body['private'] = 'False'
    bodyj = json.dumps(body)
    queue = src.send_reply.RPCSender('announce')
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

    # name = "CNU"
    # sourceID = '100'
    # person = "Cassie"
    # app = "Civ v.3.1"
    # form = 'txt'
    # private = 'False'
    # date = '05/27/2021'
    # size = '35'
    #
    # data = {}
    # data['name'] = name
    # data['sourceID'] = sourceID
    # data['dataID'] = 1000
    # data['person'] = person
    # data['app'] = app
    # data['format'] = form
    # data['private'] = private
    # data['date'] = date
    # data['size'] = size
    # announce_sub(data)
