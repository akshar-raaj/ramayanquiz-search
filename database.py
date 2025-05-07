"""
All interactions with the PostgreSQL database.
"""
import psycopg2

from constants import DATABASE_CONNECTION_STRING


database_connection = None


def get_database_connection(force=False):
    global database_connection
    if database_connection is None or force is True:
        database_connection = psycopg2.connect(DATABASE_CONNECTION_STRING)
    return database_connection


def select_question(question_id: int):
    query = "select id, question, tags from questions where id=%s"
    # Don't need context manager for connection as no insert happening.
    # Hence, don't have to worry about commit or rollback.
    connection = get_database_connection()
    # Client side cursor, hence don't need to worry about context manager or closing the cursor.
    cursor = connection.cursor()
    cursor.execute(query, (question_id,))
    row = cursor.fetchone()
    if row is None:
        return row
    columns = [col.name for col in cursor.description]
    return {k: v for k, v in zip(columns, row)}
