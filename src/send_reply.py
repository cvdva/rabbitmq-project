import pika
import sys, os
import uuid


class RPCSender(object):

    def __init__(self, queue_name):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(queue="", exclusive=True)
        self.callback_queue = result.method.queue
        self.queue_name = queue_name

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )

    def on_response(self, ch, method, properties, body):
        if self.corr_id == properties.correlation_id:
            self.response = body


    def call(self, message):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue_name,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(message))
        print("Sent: {}".format(message))
        while self.response is None:
            self.connection.process_data_events()
        return self.response


#attempt = RPCSender()

