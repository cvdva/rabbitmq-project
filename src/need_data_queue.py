import pika
import sys
import os
import json


def main(binding):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='need_data', exchange_type='direct')

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='need_data', queue=queue_name, routing_key=binding)
    print(' [*] Waiting for need data messages')

    def callback(ch, method, properties, body):
        body = json.loads(body)
        dataID = body['dataID']
        print(' [x] Received {} from {} on need data queue'.format(dataID, method.routing_key))
        connection.close()


    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()


if __name__ == '__main__':
    try:
        main('1')
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)