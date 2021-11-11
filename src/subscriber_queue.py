#!/usr/bin/env python
import pika, sys, os
import src.handler
import json

def main():
    url = os.environ.get('CLOUDAMQP_URL',
                         "amqps://hgaxqhai:BZL-fO3G7Pkuo-3V2manFRbqI4Z7LnK7@toad.rmq.cloudamqp.com/hgaxqhai")
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue='subscribe', durable=True)

    def on_request(ch, method, properties, body):
        print(" [x] Received on subscribe queue % r" % body.decode())
        body = json.loads(body)
        name = body['name']
        person = body['person']
        sourceID = body['sourceID']
        if sourceID == '':
            ob = src.handler.Producer(name, person)
        else:
            ob = src.handler.Producer(name, person, sourceID)
        new_id = ob.get_sourceID()
        ch.basic_publish(exchange='',
                         routing_key=properties.reply_to,
                         properties=pika.BasicProperties(correlation_id= \
                                                             properties.correlation_id),
                         body=str(new_id))
        print(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='subscribe', on_message_callback=on_request)
    print(' [*] Waiting for subscribe messages. To exit press CTRL+C')
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
