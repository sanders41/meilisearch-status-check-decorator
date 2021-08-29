# MeiliSearch Status Check Decorator

This package provides a decorator for the [MeiliSearch Python](https://github.com/meilisearch/meilisearch-python)
client that will check for a failed status when adding documents.

## Instillation

```sh
pip install meilisearch-status-check-decorator
```

## Useage

### Add documents with no errors

In this example there will be no errors so the documents will be added and the decorator will not
print anything.

```py
from meilisearch import Client
from meilisearch_status_check_decorator import status_check

index = Client("http://localhost:7700", "masterKey").index("test")


@status_check(index=index)
def good_insert():
    documents = [
      {
        "id": 1,
        "name": "test 1",
      },
      {
        "id": 2,
        "name": "test 2",
      }
    ]
    index.add_documents(documents)
```

### Add documents with errors

In this example an error will be returned because a primary key cannot be inferred

```py
from meilisearch import Client
from meilisearch_status_check_decorator import status_check

index = Client("http://localhost:7700", "masterKey").index("test")


@status_check(index=index)
def bad_insert():
    documents = [
      {
        "name": "test 1",
      },
      {
        "name": "test 2",
      }
    ]
    index.add_documents(documents)
```

This will result in an error similar to the following being printed:

```sh
FAILED: {'status': 'failed', 'updateId': 0, 'type': {'name': 'DocumentsAddition'}, 'message': 'missing primary key', 'errorCode': 'missing_primary_key', 'errorType': 'invalid_request_error', 'errorLink': 'https://docs.meilisearch.com/errors#missing_primary_key', 'duration': 0.025, 'enqueuedAt': '2021-08-29T17:06:59.877177189Z', 'processedAt': '2021-08-29T17:06:59.906190045Z'}
```
