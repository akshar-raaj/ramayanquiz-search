"""
All interactions with Elasticsearch should happen from here.
Currently we are using the `requests` library. Later we will shift to elasticsearch-py
"""
import requests
import json

from constants import ELASTIC_HOST, QUESTION_INDEX


elastic_connection = None


def get_connection(force=False):
    global elastic_connection
    if elastic_connection is None or force:
        pass
    return elastic_connection


def create_index(index_name):
    """
    This operation is idempotent.
    Multiple calls to create_index will not do anything extra. It would ensure that the index exists.
    """
    url = f'{ELASTIC_HOST}/{index_name}'
    response = requests.put(url)
    # Idempotency
    if response.status_code == 400:
        response_json = response.json()
        if response_json['error']['type'] == 'resource_already_exists_exception':
            return True, ''
        return False
    if response.ok:
        return True, ''
    else:
        response_json = response.json()
        return False, response_json['error']['reason']


def delete_index(index_name):
    url = f'{ELASTIC_HOST}/{index_name}'
    response = requests.delete(url)
    if response.ok:
        return True, ''
    else:
        response_json = response.json()
        return False, response_json['error']['reason']


def insert_document(document, index_name=QUESTION_INDEX):
    url = f'{ELASTIC_HOST}/{index_name}/_doc'
    response = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(document))
    response_json = response.json()
    if response.status_code == 201:
        return True, ''
    else:
        return False, response_json['error']


def search_document(index_name, term):
    url = f'{ELASTIC_HOST}/{index_name}/_search'
    response = requests.get(url)
    response_json = response.json()
    if response.status_code == 200:
        return response_json, ''
    else:
        return False, response_json['error']
