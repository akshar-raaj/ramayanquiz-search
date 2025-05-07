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
    connection = get_database_connection()
    cursor = connection.cursor()
    cursor.execute(query, (question_id,))
    row = cursor.fetchone()
    if row is None:
        return row
    columns = [col.name for col in cursor.description]
    return {k: v for k, v in zip(columns, row)}
