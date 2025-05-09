"""
Deals with RabbitMQ connection.
"""
import pika

from constants import RABBITMQ_HOST



connection = None


def get_connection_channel(force=False):
    global connection
    if connection is None or force is True:
        parameters = pika.ConnectionParameters(host=RABBITMQ_HOST)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        connection._channel = channel
    return connection._channel
