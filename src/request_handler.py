import csv
import json
from src import announce


class Request:
    def __init__(self, name='', person='', dataID=0, format=None):
        self.name = name
        self.person = person
        data_list = self.open_file("datalog.csv")
        sids = []
        dids = []
        form = []
        for row in data_list:
            sids.append(row[0])
            dids.append(row[1])
            form.append(row[2])
        if dataID in dids:
            self.dataID = dataID
        else:
            # TODO: respond to sender that the data ID is invalid
            pass
        self.format = format


    def get_name(self):
        return self.name

    def get_person(self):
        return self.person

    def get_dataID(self):
        return self.dataID

    def get_format(self):
        return self.format

    def open_file(self, file_name):
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

    def write_to_file(self, file_name, data):
        with open(file_name, 'a') as f:
            f.write("\n")
            f.write(data)


def receive(body):
    name = body['name']
    person = body['person']
    dataID = body['dataID']
    form = body['format']
    obj = Request(name, person, dataID, form)
    print('created object')


#if __name__ == "__main__":
