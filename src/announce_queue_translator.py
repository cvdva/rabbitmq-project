#!/usr/bin/env python
import pika, sys, os
import time
import src.translator


def main():
    url = os.environ.get('CLOUDAMQP_URL',
                         "amqps://hgaxqhai:BZL-fO3G7Pkuo-3V2manFRbqI4Z7LnK7@toad.rmq.cloudamqp.com/hgaxqhai")
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.queue_declare(queue='announce', durable=True)
    print(' [*] Waiting for announce messages. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        print(" [x] Received on announce queue % r" % body.decode())
        time.sleep(body.count(b'.'))
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