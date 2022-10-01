import pytest
from http import HTTPStatus

from tests.global_var import ENDPOINT_INDEX, ENDPOINT_LOGOUT


class TestEndpoints:

    def test_index(self, client, data_base_mocker):
        result = client.get(ENDPOINT_INDEX)

        assert result.status_code == HTTPStatus.OK

    def test_logout(self, client, data_base_mocker):
        result = client.get(ENDPOINT_LOGOUT)

        assert result.status_code == HTTPStatus.FOUND