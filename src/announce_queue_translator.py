#!/usr/bin/env python
import pika, sys, os
import json
import src.translator


# class NonBlocking():
#     def __init__(self):
#         self.url = os.environ.get('CLOUDAMQP_URL',
#                              "amqps://xpzuyovc:wa4RwiAHOv4G4LCFvoYb5vaXwvZ__o2v@beaver.rmq.cloudamqp.com/xpzuyovc")
#         self.params = pika.URLParameters(self.url)
#         self.connection = pika.BlockingConnection(self.params)
#         self.channel = self.connection.channel()
#         self.channel.queue_declare(queue='announce', durable=True)
#
#     def consume(self, callback):
#         result = self.channel.queue_declare('', exclusive=True)
#         queue_name = result.method.queue
#         self.channel.basic_consume(queue=queue_name, on_message)


def main():
    url = os.environ.get('CLOUDAMQP_URL',
                         "amqps://xpzuyovc:wa4RwiAHOv4G4LCFvoYb5vaXwvZ__o2v@beaver.rmq.cloudamqp.com/xpzuyovc")
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.queue_declare(queue='announce', durable=True)
    print(' [*] Waiting for announce messages. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        print(" [x] Received on announce queue % r" % body.decode())
        message = json.loads(body)
        src.translator.announce_sub(message)
        print(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='announce', on_message_callback=callback)
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
