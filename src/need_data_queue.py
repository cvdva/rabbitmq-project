import pika
import sys
import os
import json
import src.send_final_data
import csv
import src.translator
from multiprocessing import Process


def main(binding):
    url = os.environ.get('CLOUDAMQP_URL',
                         "amqps://xpzuyovc:wa4RwiAHOv4G4LCFvoYb5vaXwvZ__o2v@beaver.rmq.cloudamqp.com/xpzuyovc")
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    binding = binding.strip()

    channel.exchange_declare(exchange='need_data', exchange_type='direct')

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='need_data', queue=queue_name, routing_key=binding)

    print(' [*] Waiting for need data messages')

    def callback(ch, method, properties, body):
        body = json.loads(body)
        dataID = body['dataID']
        print(' [x] Received {} from {} on need data queue'.format(dataID, method.routing_key))
        if binding == '1':
            p = Process(target=translate, args=(dataID, ))
            p.start()
            translate(dataID)
        else:
            no_translate(dataID)

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()


def translate(dataID):
    message = src.translator.pull_translation(dataID)
    if message:
        message = message.encode('utf-8')
        src.send_final_data.main(message, dataID)


def no_translate(dataID):
    datum = open_file("datum.csv")
    dids = []
    paths = []
    for line in datum:
        dids.append(line[0].strip())
        paths.append(line[1].strip())
    i = dids.index(dataID.strip())
    path = paths[i]
    with open(path, 'rb') as f:
        contents = f.read()
    src.send_final_data.main(contents, dataID)


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


if __name__ == '__main__':
    try:
        main('100')
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)