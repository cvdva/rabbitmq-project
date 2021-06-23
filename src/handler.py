import csv

class Message:
    def __init__(self, name='', sourceID=0, format=None, private=False, rec=None, size=0, Type=None):
        self.name = name
        names, ids = self.open_file("sourcelog.csv")
        if sourceID == 0:
            if self.name in names:
                name_index = names.index(name)
                id = ids[name_index]
                self.sourceID = id
            else:
                last_id = ids[-1]
                self.sourceID = last_id + 1
                "TODO: Write the new name and ID to the csv file"
        else:
            self.sourceID = sourceID
        self.format = format
        self.private = private
        self.recipient = rec
        self.size = size
        self.type = Type

    def get_name(self):
        return self.name

    def get_sourceID(self):
        return self.sourceID

    def get_format(self):
        return self.format

    def get_private(self):
        return self.private

    def get_recipient(self):
        return self.recipient

    def get_size(self):
        return self.size

    def get_type(self):
        return self.type

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
        names = list[0]
        ids = list[1]
        return names, ids