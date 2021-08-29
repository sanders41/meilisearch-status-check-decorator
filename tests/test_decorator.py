import pytest
from meilisearch import Client

from meilisearch_status_check_decorator import status_check


@pytest.fixture
def index():
    index = Client("http://localhost:7700", "masterKey").index("test")
    yield index
    index.delete()


@pytest.mark.parametrize(
    "docs, expected_fail, expected_indexed",
    [
        (
            [
                {
                    "id": 1,
                    "name": "test 1",
                },
                {
                    "id": 2,
                    "name": "test 2",
                },
            ],
            False,
            2,
        ),
        (
            [
                {
                    "name": "test 1",
                },
                {
                    "name": "test 2",
                },
            ],
            True,
            0,
        ),
    ],
)
def test_status_check(docs, expected_fail, expected_indexed, index, capfd):
    @status_check(index=index)
    def fn():
        response = index.add_documents(docs)
        index.wait_for_pending_update(response["updateId"])

    fn()
    stats = index.get_stats()
    assert stats["numberOfDocuments"] == expected_indexed

    out, _ = capfd.readouterr()

    fail_text = "'status': 'failed'"

    if expected_fail:
        assert fail_text in out
    else:
        assert fail_text not in out
