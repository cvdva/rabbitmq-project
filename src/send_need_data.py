import pika
import sys


def main(message, queue):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='need_data', exchange_type='direct')

    channel.basic_publish(exchange='need_data', routing_key=queue, body=message)
    print(' [x] sent {} to queue {}'.format(message, queue))
    connection.close()

if __name__ == '__main__':
    main('I need data', '1')
