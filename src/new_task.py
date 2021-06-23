#!/usr/bin/env python
import pika
import json
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
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