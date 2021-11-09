import pika
import sys


def main(message, queue):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='final', exchange_type='direct')

    channel.basic_publish(exchange='final', routing_key=queue, body=message)
    print(' [x] sent {} to queue {}'.format(message, queue))
    connection.close()

if __name__ == '__main__':
    b = str.encode('I need data')
    main(b, '1001')
