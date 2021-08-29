# MeiliSearch Status Check Decorator

[![Tests Status](https://github.com/sanders41/meilisearch-status-check-decorator/workflows/Testing/badge.svg?branch=main&event=push)](https://github.com/sanders41/meilisearch-status-check-decorator/actions?query=workflow%3ATesting+branch%3Amain+event%3Apush)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/sanders41/meilisearch-status-check-decorator/main.svg)](https://results.pre-commit.ci/latest/github/sanders41/meilisearch-status-check-decorator/main)
[![Coverage](https://codecov.io/github/sanders41/meilisearch-status-check-decorator/coverage.svg?branch=main)](https://codecov.io/gh/sanders41/meilisearch-status-check-decorator)
[![PyPI version](https://badge.fury.io/py/meilisearch-status-check-decorator.svg)](https://badge.fury.io/py/meilisearch-status-check-decorator)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/meilisearch-status-check-decorator?color=5cc141)](https://github.com/sanders41/meilisearch-status-check-decorator)

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

## Contributing

Contributions to this project are welcome. If you are interesting in contributing please see our [contributing guide](CONTRIBUTING.md)
