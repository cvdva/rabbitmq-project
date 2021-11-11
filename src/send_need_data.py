import pika
import sys
import os


def main(message, queue):
    url = os.environ.get('CLOUDAMQP_URL',
                         "amqps://hgaxqhai:BZL-fO3G7Pkuo-3V2manFRbqI4Z7LnK7@toad.rmq.cloudamqp.com/hgaxqhai")
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.exchange_declare(exchange='need_data', exchange_type='direct')

    channel.basic_publish(exchange='need_data', routing_key=queue, body=message)
    print(' [x] sent {} to queue {}'.format(message, queue))
    connection.close()

if __name__ == '__main__':
    main('I need data', '1')
