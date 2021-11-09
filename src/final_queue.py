import pika
import sys
import os
import json


def main(binding):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='final', exchange_type='direct')

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='final', queue=queue_name, routing_key=binding)
    print(' [*] Waiting for final messages on {}'.format(binding))

    def callback(ch, method, properties, body):
        print(' [x] Received {} from {} on final queue'.format(body.decode(), method.routing_key))

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