INGEST_QUEUE = 'search-ingest'               # RabbitMQ queue where publisher publishes the question_id, that needs to be indexed.
QUESTION_INDEX = 'questions'                 # Elasticsearch index where document, i.e question details, need to be inserted.
RABBITMQ_HOST = 'host.docker.internal'
ELASTIC_HOST = 'http://host.docker.internal:9200'       # Elastic host
ELASTIC_AUTH = ('elastic', 'abc')
# Read it from environment variable. Use python-dotenv
# PostgreSQL connection string
DATABASE_CONNECTION_STRING = "host=host.docker.internal port=5432 user=postgres password=abc dbname=ramayanquiz application_name=search-service"
