import csv
import json
import src.announce
import src.send_need_data


class Producer:
    def __init__(self, institution, person, sourceID=0):
        self.inst = institution
        self.person = person
        full_list = open_file("sourcelog.csv")
        insts = []
        names = []
        ids = []
        queues = []
        for row in full_list:
            insts.append(row[0].strip())
            names.append(row[1].strip())
            ids.append(row[2].strip())
            queues.append(row[3].strip())
        if sourceID == 0:
            if self.inst in insts and self.person in names:
                name_index = insts.index(institution)
                id = ids[name_index]
                self.sourceID = id
                self.queue = queues[name_index]
            else:
                last_id = int(ids[-1])
                self.sourceID = last_id + 1
                last_queue = int(queues[-1])
                self.queue = last_queue + 1
                write_to_file("sourcelog.csv", "{}, {}, {}, {}".format(institution, person, self.sourceID, self.queue))
        else:
            index = ids.index(sourceID)
            self.queue = queues[index]

    def get_inst(self):
        return self.inst

    def get_name(self):
        return self.person

    def get_sourceID(self):
        return self.sourceID

    def get_queue(self):
        return self.queue



class Message:
    def __init__(self, name, person, sourceID, app='', format=None, private=False, date=None, size=0, dataID=0):
        self.name = name
        self.sourceID = sourceID
        self.person = person
        self.app = app
        self.format = format
        self.private = private
        self.date = date
        self.size = size
        data_list = open_file("datalog.csv")
        sids = []
        dids = []
        form = []
        for row in data_list:
            sids.append(row[0])
            dids.append(row[1])
            form.append(row[2])
        if dataID == 0:
            self.dataID = int(dids[-1]) + 1
        else:
            self.dataID = dataID
        write_to_file("datalog.csv", "{}, {}, {}, {}, {}, {}, {}".format(self.sourceID, self.dataID, self.format,
                                                                     self.name, self.person, self.app, self.date))

    def get_name(self):
        return self.name

    def get_sourceID(self):
        return self.sourceID

    def get_person(self):
        return self.person

    def get_app(self):
        return self.app

    def get_format(self):
        return self.format

    def get_private(self):
        return self.private

    def get_date(self):
        return self.date

    def get_size(self):
        return self.size

    def get_dataID(self):
        return self.dataID

    def create_announcement(self):
        data = {}
        data['name'] = self.name
        data['souceID'] = self.sourceID
        data['person'] = self.person
        data['app'] = self.app
        data['format'] = self.format
        data['date'] = self.date
        data['size'] = self.size
        data['dataID'] = self.dataID
        json_data = json.dumps(data)
        src.announce.main((json_data))


class DataRequest:
    def __init__(self, ex, prop, key, dataID, sourceID):
        self.ex = ex
        self.prop = prop
        self.key = key
        self.dataID = dataID
        data_list = open_file("datalog.csv")
        sids = []
        dids = []
        for row in data_list:
            sids.append(row[0].strip())
            dids.append(row[1].strip())
        index = dids.index(self.dataID)
        sid = sids[index]
        if sourceID == sid:
            self.sourceID = sourceID
        else:
            self.sourceID = None

    def get_ex(self):
        return self.ex

    def get_prop(self):
        return self.prop

    def get_key(self):
        return self.key

    def get_dataID(self):
        return self.dataID

    def get_sourceID(self):
        return self.sourceID

    def send_request(self):
        src.send_need_data.main((self.ex, self.prop, self.key, self.dataID), self.sourceID)


def receive(body):
    name = body['name']
    sourceid = body['sourceID']
    person = body['person']
    app = body['app']
    form = body['format']
    private = body['private']
    date = body['date']
    size = body['size']
    obj = Message(name, person, sourceid, app, form, private, date, size)
    if obj.get_private() == "False":
        obj.create_announcement()
    return obj.get_dataID()


def receive_producer(body):
    institution = body['institution']
    name = body['name']
    sourceID = body['sourceID']
    if sourceID == '':
        obj = Producer(institution, name)
    else:
        obj = Producer(institution, name, sourceID)
    return obj.get_queue()


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


def write_to_file(file_name, data):
    with open(file_name, 'a') as f:
        f.write("\n")
        f.write(data)


if __name__ == "__main__":
    one = Producer("CNU", "Villarreal")
    print(one.get_queue())