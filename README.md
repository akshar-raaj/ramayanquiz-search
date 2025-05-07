This service has to perform two broad functions:
- Ingest the data into a suitable data store, that's optimized for search.
- Provide ability to search and provide results.

## Architecture

We want to keep this search service decoupled from the core. Simultaneously we want to have an asynchronous architecture for maximum scalability.

This service has a consumer that listens on a particular queue. The consumer is provided with a question_id. It then retrieves this question from the database and ingests it into the search backend. The search backend is Elasticsearch.
