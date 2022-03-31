import pika
import sys
import os
import json
import csv
import src.send_final_data


def main(binding):
    url = os.environ.get('CLOUDAMQP_URL',
                         "amqps://xpzuyovc:wa4RwiAHOv4G4LCFvoYb5vaXwvZ__o2v@beaver.rmq.cloudamqp.com/xpzuyovc")
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    binding = binding.strip()

    channel.exchange_declare(exchange='final', exchange_type='direct')

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='final', queue=queue_name, routing_key=binding)
    print(' [*] Waiting for final messages on {}'.format(binding))

    def callback(ch, method, properties, body):
        print(' [x] Received {} from {} on final queue'.format(body.decode(), method.routing_key))
        connection.close()
        trans = open_file("translator_data.csv")
        new_dataIDs = []
        old_dataIDs = []
        new_format = []
        source = []
        for line in trans:
            new_dataIDs.append(line[0].strip())
            old_dataIDs.append(line[1].strip())
            new_format.append(line[2])
            source.append(line[3])
        index = old_dataIDs.index(method.routing_key)
        new_format = new_format[index]
        new_dataID = new_dataIDs[index]
        print(new_format)
        src.send_final_data.main(body, new_dataID.strip())


    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()


def open_file(file_name):
    list = []
    with open(file_name, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            list.append(row)
    return list


if __name__ == '__main__':
    try:
        main('1')
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)