import pika, sys, os
import time
import src.handler
import json


def main():
    url = os.environ.get('CLOUDAMQP_URL',
                         "amqps://hgaxqhai:BZL-fO3G7Pkuo-3V2manFRbqI4Z7LnK7@toad.rmq.cloudamqp.com/hgaxqhai")
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    # connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    # channel = connection.channel()
    channel.queue_declare(queue='hello', durable=True)

    def on_request(ch, method, properties, body):
        print(" [x] Received on hello queue % r" % body.decode())
        messagej = json.loads(body)
        dataID = src.handler.receive(messagej)
        time.sleep(body.count(b'.'))
        ch.basic_publish(exchange='',
                         routing_key=properties.reply_to,
                         properties=pika.BasicProperties(correlation_id=properties.correlation_id),
                         body=str(dataID))
        print(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='hello', on_message_callback=on_request)
    print(' [*] Waiting for hello messages. To exit press CTRL+C')
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


# def main():
#     # url = os.environ.get('CLOUDAMQP_URL',
#     #                      "amqps://hgaxqhai:BZL-fO3G7Pkuo-3V2manFRbqI4Z7LnK7@toad.rmq.cloudamqp.com/hgaxqhai")
#     # params = pika.URLParameters(url)
#     # connection = pika.BlockingConnection(params)
#     # channel = connection.channel()
#     connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
#     channel = connection.channel()
#
#     channel.queue_declare(queue='hello', durable=True)
#     print(' [*] Waiting for hello messages. To exit press CTRL+C')
#
#
#     def callback(ch, method, properties, body):
#         print(" [x] Received on hello queue % r" % body.decode())
#         messagej = json.loads(body)
#         src.handler.receive(messagej)
#         time.sleep(body.count(b'.'))
#         print(" [x] Done")
#         ch.basic_ack(delivery_tag=method.delivery_tag)
#
#
#     channel.basic_qos(prefetch_count=1)
#     channel.basic_consume(queue='hello', on_message_callback=callback)
#     channel.start_consuming()
#
#
# if __name__ == '__main__':
#     try:
#         main()
#     except KeyboardInterrupt:
#         print('Interrupted')
#         try:
#             sys.exit(0)
#         except SystemExit:
#             os._exit(0)
