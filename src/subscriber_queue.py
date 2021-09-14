#!/usr/bin/env python
import pika, sys, os
import time
from src import request_handler
from src import handler
import json

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='subscribe', durable=True)

    def on_request(ch, method, properties, body):
        print(" [x] Received % r" % body.decode())
        body = json.loads(body)
        name = body['name']
        person = body['person']
        sourceID = body['sourceID']
        if sourceID == '':
            ob = handler.Producer(name, person)
        else:
            ob = handler.Producer(name, person, sourceID)
        new_id = ob.get_sourceID()
        ch.basic_publish(exchange='',
                         routing_key=properties.reply_to,
                         properties=pika.BasicProperties(correlation_id= \
                                                             properties.correlation_id),
                         body=str(new_id))
        print(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='subscribe', on_message_callback=on_request)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
