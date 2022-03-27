#!/usr/bin/env python
import pika, sys, os
import time


def main():
    url = os.environ.get('CLOUDAMQP_URL',
                         "amqps://xpzuyovc:wa4RwiAHOv4G4LCFvoYb5vaXwvZ__o2v@beaver.rmq.cloudamqp.com/xpzuyovc")
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.exchange_declare(exchange='announce', exchange_type='fanout')
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='announce', queue=queue_name)

    # channel.queue_declare(queue='announce', durable=True)
    print(' [*] Waiting for announce messages. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        print(" [x] Received on announce queue % r" % body.decode())
        time.sleep(body.count(b'.'))
        print(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)
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
