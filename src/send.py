#!/usr/bin/env python
import pika
import json
import sys
import os


def main(message, que):
    url = os.environ.get('CLOUDAMQP_URL',
                         "amqps://hgaxqhai:BZL-fO3G7Pkuo-3V2manFRbqI4Z7LnK7@toad.rmq.cloudamqp.com/hgaxqhai")
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue=que,
                          durable=True)
    channel.basic_publish(exchange='',
                          routing_key=que,
                          body=message)
    print(" [x] Sent message")
    connection.close()


def encode_json(json_name):
    """
    Converts a json at a given location to bytes
    :param json_path: name of the json file
    :return: json as string
    """

    name = json_name + ".json"
    with open(name) as f:
        d = json.load(f)
        d = json.dumps(d)
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
