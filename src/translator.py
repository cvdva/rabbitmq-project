import pika, sys, os
import time
import json


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='announce', durable=True)
    print(' [*] Waiting for translator messages. To exit press CTRL+C')


    def callback(ch, method, properties, body):
        print(" [x] Received % r" % body.decode())
        messagej = json.loads(body)
        #TODO: insert function to check if the data can be translated
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
