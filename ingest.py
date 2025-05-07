"""
The glue between RabbitMQ , Postgres and Elasticsearch.

This is invoked by the RabbitMQ consumer when it receives a message.
This glue retrieves the question from the database and ingests it into Elasticsearch.
"""
import logging

from constants import QUESTION_INDEX

from database import select_question
from elastic import insert_document


logger = logging.getLogger(__name__)


def insert_question(question_id):
    """
    Insert a document with question details into the Elasticsearch index.
    """
    logger.info(f"Inserting question {question_id}")
    question = select_question(question_id)
    if question is None:
        logger.info(f"Question {question_id} does not exist.")
        return
    # Elastic by default has an _id field. We do not want to make it confusing.
    # Hence be extra explicit, and call it question_id.
    question['question_id'] = question['id']
    del question['id']
    insert_document(QUESTION_INDEX, question)
    logger.info(f"Inserted question {question_id}")
