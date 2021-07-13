#!/usr/bin/env python
import pika
import json
import sys
import os

def main(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='hello',
                          durable=True)
    channel.basic_publish(exchange='',
                          routing_key='hello',
                          body=message)
    print(" [x] Sent message")
    connection.close()


def encode_json(json_name):
    """
    Converts a json at a given location to bytes
    :param json_path: name of the json file
    :return: json as bytes
    """

    name = json_name + ".json"
    with open(name) as f:
        d = json.load(f)
        print(d)
        print(type(d))
    d = str(d)
    return d


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
