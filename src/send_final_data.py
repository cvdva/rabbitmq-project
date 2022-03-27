import pika
import sys
import os


def main(message, queue):
    url = os.environ.get('CLOUDAMQP_URL',
                         "amqps://xpzuyovc:wa4RwiAHOv4G4LCFvoYb5vaXwvZ__o2v@beaver.rmq.cloudamqp.com/xpzuyovc")
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.exchange_declare(exchange='final', exchange_type='direct')

    channel.basic_publish(exchange='final', routing_key=queue, body=message)
    print(' [x] sent {} to queue {}'.format(message, queue))
    connection.close()

if __name__ == '__main__':
    b = str.encode('I need data')
    main(b, '1001')
