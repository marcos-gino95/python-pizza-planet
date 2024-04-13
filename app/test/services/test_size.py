from unittest.mock import patch

import pytest

from app.controllers.size import SizeController


@pytest.mark.asyncio
def test_get_sizes_services(client, create_sizes, size_uri):
    response = client.get(size_uri)
    assert response.status_code == 200
    returned_sizes = {size["_id"]: size for size in response.json}
    for size in create_sizes:
        assert size["_id"] in returned_sizes


@pytest.mark.asyncio
def test_get_sizes_empty_response(client, size_uri):
    response = client.get(size_uri)
    assert response.json == []


@pytest.mark.asyncio
def test_get_sizes_with_bad_request(client, size_uri):
    with patch.object(
        SizeController, "get_all", return_value=(None, "Error retrieving sizes")
    ):
        response = client.get(size_uri)
    assert response.status_code == 400
