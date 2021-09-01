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
        index.add_documents(docs)

    fn()
    stats = index.get_stats()
    assert stats["numberOfDocuments"] == expected_indexed

    out, _ = capfd.readouterr()

    fail_text = "'status': 'failed'"

    if expected_fail:
        assert fail_text in out
    else:
        assert fail_text not in out


@pytest.mark.parametrize(
    "docs, expected_fail, expected_indexed, expected_messages",
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
            0,
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
            2,
        ),
    ],
)
def test_status_check_batches(
    docs, expected_fail, expected_indexed, expected_messages, index, capfd
):
    @status_check(index=index)
    def fn():
        index.add_documents_in_batches(docs, 1)

    fn()
    stats = index.get_stats()
    assert stats["numberOfDocuments"] == expected_indexed

    out, _ = capfd.readouterr()

    fail_text = "'status': 'failed'"

    if expected_fail:
        assert out.count(fail_text) == expected_messages
    else:
        assert fail_text not in out
