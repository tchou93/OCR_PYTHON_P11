import pytest
from http import HTTPStatus

from tests.global_var import ENDPOINT_SHOWSUMMARY, ENDPOINT_BOOK, simu_clubs, simu_competitions, \
    ENDPOINT_RECAP_CLUB_POINTS


class TestDisplay:

    def test_display_new_competition(self, client, data_base_mocker, only_new_competitions_mocker):
        result = client.post(ENDPOINT_SHOWSUMMARY, data={'email': (simu_clubs[0])["email"]})
        message = "Book Places"

        assert result.status_code == HTTPStatus.OK
        assert result.data.decode().count(message) == 1
        assert (simu_competitions[2])["name"] in result.data.decode()

    def test_display_old_competition(self, client, data_base_mocker, only_old_competitions_mocker):
        result = client.post(ENDPOINT_SHOWSUMMARY, data={'email': (simu_clubs[0])["email"]})
        message = "Book Places"

        assert result.status_code == HTTPStatus.OK
        assert result.data.decode().count(message) == 0
        assert (simu_competitions[0])["name"] in result.data.decode()
        assert (simu_competitions[1])["name"] in result.data.decode()

    def test_display_new_old_competition(self, client, data_base_mocker, new_old_competitions_mocker):
        result = client.post(ENDPOINT_SHOWSUMMARY, data={'email': (simu_clubs[0])["email"]})
        message = "Book Places"

        assert result.status_code == HTTPStatus.OK
        assert result.data.decode().count(message) == 1
        assert (simu_competitions[0])["name"] in result.data.decode()
        assert (simu_competitions[1])["name"] in result.data.decode()
        assert (simu_competitions[2])["name"] in result.data.decode()

    @pytest.mark.parametrize("endpoint, message, status_code", [
        (f"{ENDPOINT_BOOK}/{(simu_competitions[2])['name'].replace(' ', '%20')}/"
         f"{(simu_clubs[0])['name'].replace(' ', '%20')}",
         "Booking for",
         HTTPStatus.OK),
        (f"{ENDPOINT_BOOK}/{(simu_competitions[2])['name'].replace(' ', '%20')}/badclub",
         "Something went wrong-please try again",
         HTTPStatus.NOT_FOUND),
        (f"{ENDPOINT_BOOK}/badcompetition/{(simu_clubs[0])['name'].replace(' ', '%20')}",
         "Something went wrong-please try again",
         HTTPStatus.NOT_FOUND),
        (f"{ENDPOINT_BOOK}/{(simu_competitions[1])['name'].replace(' ', '%20')}/"
         f"{(simu_clubs[0])['name'].replace(' ', '%20')}",
         "This is a old competition-please try again",
         HTTPStatus.BAD_REQUEST)
    ])
    def test_display_book_validity_path(self, client, data_base_mocker, new_old_competitions_mocker,
                                        endpoint, message, status_code):
        result = client.get(endpoint)

        assert result.status_code == status_code
        assert message in result.data.decode()

    def test_display_recap_club_points(self, client, data_base_mocker):
        data = {
            'clubs': simu_clubs,
        }
        result = client.get(ENDPOINT_RECAP_CLUB_POINTS, data=data)
        assert result.status_code == HTTPStatus.OK
        for club in simu_clubs:
            assert club["name"] in result.data.decode()
            assert club["points"] in result.data.decode()
