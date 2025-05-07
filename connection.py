"""
Deals with RabbitMQ connection.
"""
import pika



connection = None


def get_connection_channel(force=False):
    global connection
    if connection is None or force is True:
        connection = pika.BlockingConnection()
        channel = connection.channel()
        connection._channel = channel
    return connection._channel
