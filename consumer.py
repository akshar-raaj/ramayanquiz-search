"""
RabbitMQ consumer.
"""
import json
import logging

from constants import INGEST_QUEUE
from connection import get_connection_channel
from ingest import insert_question


logging.basicConfig(level=logging.INFO)


logger = logging.getLogger(__name__)


def on_message_callback(ch, method, properties, body):
    logger.info("Message received")
    try:
        body = body.decode('utf-8')
        logger.info(f"Decoded message: {body}")
        body = json.loads(body)
        question_id = body['question_id']
    except Exception as exc:
        logger.error(f"Exception while decoding: {body}. Exception is {exc}")
        # Need to acknowledge this even in case of exceptions to ensure this gets dequeued.
        # Else it can choke the queue.
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return
    try:
        insert_question(question_id)
    except Exception as exc:
        # This is like the interface for the client.
        # Hence we should have exception handling here.
        # Similar to how we never allow an API to fail and gracefully return 500 Internal Server Error if all else fails.
        logger.error(f"Exception while inserting question {question_id}: {exc}")
    logger.info("Message processed")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def consume(queue_name):
    channel = get_connection_channel()
    # Highly likely that the queue already exists.
    # The publisher would have already pushed to the queue.
    # A safe measure, in case consumer started before the publisher
    logger.info(f"Declaring queue {queue_name}")
    channel.queue_declare(queue_name, durable=True)
    # Disable automatic acknowledgement, enable manual acknowledgement
    channel.basic_consume(queue_name, on_message_callback=on_message_callback, auto_ack=False)
    logger.info("Starting to consume")
    channel.start_consuming()


if __name__ == '__main__':
    consume(INGEST_QUEUE)
