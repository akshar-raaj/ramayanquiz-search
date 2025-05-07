"""
The glue between RabbitMQ , Postgres and Elasticsearch.

This is invoked by the RabbitMQ consumer when it receives a message.
This glue retrieves the question from the database and ingests it into Elasticsearch.
"""
import logging

from database import select_question
from elastic import insert_document


logger = logging.getLogger(__name__)


def insert_question(question_id):
    """
    Insert a document with question details into the Elasticsearch index.
    """
    logger.info(f"Inserting question {question_id}")
    # No exception handling here
    # In case something goes wrong, we want the exception to bubble up.
    # Exceptions should be handled in cases where there is a reasonable way to recover from them
    # or take meaningful action, but here we cannot, hence let them bubble up.
    question = select_question(question_id)
    if question is None:
        logger.warning(f"Question {question_id} does not exist.")
        return
    # Elastic by default has an _id field. We do not want to make it confusing.
    # Hence be extra explicit, and call it question_id.
    question['question_id'] = question['id']
    del question['id']
    # No exception handling here
    # In case something goes wrong, we want the exception to bubble up.
    # Exceptions should be handled in cases where there is a reasonable way to recover from them.
    insert_document(question)
    logger.info(f"Inserted question {question_id} into Elasticsearch")
