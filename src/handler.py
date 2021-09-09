import csv
import json
from src import announce


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
            insts.append(row[0])
            names.append(row[1])
            ids.append(row[2])
            queues.append(row[3])
        if sourceID == 0:
            if self.inst in names and self.person :
                name_index = names.index(institution)
                id = ids[name_index]
                self.sourceID = id
                self.queue = queues[name_index]
            else:
                last_id = int(ids[-1])
                self.sourceID = last_id + 1
                last_queue = int(queues[-1])
                self.queue = last_queue + 1
                write_to_file("sourcelog.csv", "{}, {}, {}, {}".format(institution, person, self.sourceID, self.queue))

    def get_inst(self):
        return self.inst

    def get_name(self):
        return self.person

    def get_sourceID(self):
        return self.sourceID

    def get_queue(self):
        return self.queue


class Message:
    def __init__(self, name='', sourceID=0, person='', app='', format=None, private=False, date=None,
                 size=0, dataID=0):
        self.name = name
        full_list = open_file("sourcelog.csv")
        names = []
        ids = []
        for row in full_list:
            names.append(row[0])
            ids.append(row[1])
        if sourceID == 0:
            if self.name in names:
                name_index = names.index(name)
                id = ids[name_index]
                self.sourceID = id
            else:
                last_id = int(ids[-1])
                self.sourceID = last_id + 1
                write_to_file("sourcelog.csv", "{}, {}".format(name, self.sourceID))
        else:
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
        write_to_file("datalog.csv", "{}, {}, {}".format(self.sourceID, self.dataID, self.format))

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
        announce.main((json_data))


def receive(body):
    name = body['name']
    sourceid = body['sourceID']
    person = body['person']
    app = body['app']
    form = body['format']
    private = body['private']
    date = body['date']
    size = body['size']
    obj = Message(name, sourceid, person, app, form, private, date, size)
    print('created object')
    if obj.get_private() == "False":
        obj.create_announcement()


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
    one = Producer("CNU", "Cassie")
    print(one.get_queue())