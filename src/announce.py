import pika, sys, os, json
import time


def main(message):
    url = os.environ.get('CLOUDAMQP_URL',
                         "amqps://xpzuyovc:wa4RwiAHOv4G4LCFvoYb5vaXwvZ__o2v@beaver.rmq.cloudamqp.com/xpzuyovc")
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.exchange_declare(exchange='announce', exchange_type='fanout')
    channel.basic_publish(exchange='announce', routing_key='', body=message)
    print(" [x] Sent message")
    connection.close()


# def encode_json(json_name):
#     """
#     Converts a json at a given location to bytes
#     :param json_path: name of the json file
#     :return: json as bytes
#     """
#
#     name = json_name + ".json"
#     with open(name) as f:
#         d = json.load(f)
#         print(d)
#         print(type(d))
#     d = str(d)
#     return d


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
