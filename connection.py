"""
Deals with RabbitMQ connection.
"""
import pika

from constants import RABBITMQ_HOST, RABBITMQ_USER, RABBITMQ_PASSWORD



connection = None


def get_connection_channel(force=False):
    global connection
    if connection is None or force is True:
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
        parameters = pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        connection._channel = channel
    return connection._channel
