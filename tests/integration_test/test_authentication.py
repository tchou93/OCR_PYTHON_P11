import pytest
from http import HTTPStatus
from tests.global_var import ENDPOINT_SHOWSUMMARY


class TestAuthentication:
    @pytest.mark.parametrize("email, status_code", [
        ({'email': 'john@simplylift.com'}, HTTPStatus.OK),
        ({'email': 'clubtest@gmail.com'}, HTTPStatus.OK),
        ({'email': 'kate@shelifts.co.uk'}, HTTPStatus.OK),
    ])
    def test_good_email(self, email, status_code, client, databasemocker):
        result = client.post(ENDPOINT_SHOWSUMMARY, data=email)
        message = f"Welcome, {email['email']}"

        assert result.status_code == status_code
        assert message in result.data.decode()

    @pytest.mark.parametrize("email, status_code", [
        ({'email': 'test@gmail.com'}, HTTPStatus.NOT_FOUND),
        ({'email': ''}, HTTPStatus.NOT_FOUND),
    ])
    def test_bad_email(self, email, status_code, client, databasemocker):
        result = client.post(ENDPOINT_SHOWSUMMARY, data=email)

        assert result.status_code == HTTPStatus.UNAUTHORIZED
        assert "Sorry, that email was not found." in result.data.decode()
