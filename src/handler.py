import csv
from src import announce


class Message:
    def __init__(self, name='', sourceID=0, format=None, private=False, date=None, size=0, dataID=0):
        self.name = name
        full_list = self.open_file("sourcelog.csv")
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
                self.write_to_file("sourcelog.csv", "{}, {}".format(name, self.sourceID))
        else:
            self.sourceID = sourceID
        self.format = format
        self.private = private
        self.date = date
        self.size = size
        data_list = self.open_file("datalog.csv")
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
        self.write_to_file("datalog.csv", "{}, {}, {}".format(self.sourceID, self.dataID, self.format))

    def get_name(self):
        return self.name

    def get_sourceID(self):
        return self.sourceID

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

    def create_announcement(self):
        name = self.name
        form = self.format
        date = self.date
        message = "Data from {} created on {} in format {} is available".format(name, date, form)
        announce.main(message)


if __name__ == "__main__":
    one = Message("Test1", 100, "A", False, None, 0, None)
    one.create_announcement()