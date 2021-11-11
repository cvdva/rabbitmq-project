#!/usr/bin/env python
import pika
import json
import sys
import os

url = os.environ.get('CLOUDAMQP_URL',
                         "amqps://hgaxqhai:BZL-fO3G7Pkuo-3V2manFRbqI4Z7LnK7@toad.rmq.cloudamqp.com/hgaxqhai")
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='hello', durable=True)
message = json.load(example_json.json)
message = bytearray(message)
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=message,
                      properties=pika.BasicProperties(
                          delivery_mode=2,
                      ))
print(" [x] Sent %r" % message)
connection.close()