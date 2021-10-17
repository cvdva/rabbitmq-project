#!/usr/bin/env python
import pika, sys, os
import time
import src.handler
import json


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='register', durable=True)

    def on_request(ch, method, properties, body):
        print(" [x] Received on register queue % r" % body.decode())
        body = json.loads(body)
        answer = src.handler.receive_producer(body)
        print("Listen with queue tag: {}".format(answer))
        ch.basic_publish(exchange='',
                         routing_key=properties.reply_to,
                         properties=pika.BasicProperties(correlation_id= \
                                                             properties.correlation_id),
                         body=str(answer))
        print(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='register', on_message_callback=on_request)
    print(' [*] Waiting for register messages. To exit press CTRL+C')
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
