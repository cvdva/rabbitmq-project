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
                last_id = int(ids[-1])
                self.sourceID = last_id + 1
                self.write_to_file("sourcelog.csv", "{}, {}".format(name, self.sourceID))
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
        names = []
        ids = []
        with open(file_name, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                name = row[0]
                id = row[1]
                names.append(name)
                ids.append(id)
        print(names, ids)
        return names, ids

    def write_to_file(self, file_name, data):
        with open(file_name, 'a') as f:
            f.write("\n")
            f.write(data)


if __name__ == "__main__":
    one = Message("Test1")
    print(one.get_sourceID())
    two = Message("Test3")
    print(two.get_sourceID())