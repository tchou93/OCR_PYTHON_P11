import pytest
from http import HTTPStatus
import random
from tests.global_var import ENDPOINT_PURCHASE_PLACES, MAX_PURCHASE, simu_clubs, simu_competitions


@pytest.fixture
def valid_reservation_mocker(mocker):
    mocker.patch('server.valid_reservation', return_value=(True, "Valid message"))


@pytest.fixture
def invalid_reservation_mocker(mocker):
    mocker.patch('server.valid_reservation', return_value=(False, "Invalid message"))


class TestReservation:

    def test_good_purchase(self, client, valid_reservation_mocker, data_base_mocker, clubs_test,
                           competitions_test, new_old_competitions_mocker):
        competition = competitions_test[2]
        club = clubs_test[0]
        data = {
            'competition': competition['name'],
            'club': club['name'],
            'places': random.randint(1, MAX_PURCHASE),
        }
        club_points_before_purchase = club['points']
        competitions_places_before_purchase = competition['numberOfPlaces']
        result = client.post(ENDPOINT_PURCHASE_PLACES, data=data)

        assert result.status_code == HTTPStatus.OK
        assert "Valid message" in result.data.decode()
        assert str(competition['numberOfPlaces']) in result.data.decode()
        assert int(club_points_before_purchase) - data['places'] == int(club['points'])
        assert int(competitions_places_before_purchase) - data['places'] == \
               int(competition['numberOfPlaces'])

    def test_bad_purchase(self, client, invalid_reservation_mocker, data_base_mocker, clubs_test,
                          competitions_test, new_old_competitions_mocker):
        club = clubs_test[0]
        data = {
            'competition': (competitions_test[0])['name'],
            'club': club['name'],
            'places': MAX_PURCHASE + 1,
        }
        club_points_before_purchase = club['points']
        competitions_places_before_purchase = (competitions_test[0])['numberOfPlaces']
        result = client.post(ENDPOINT_PURCHASE_PLACES, data=data)

        assert result.status_code == HTTPStatus.BAD_REQUEST
        assert "Invalid message" in result.data.decode()
        assert str((competitions_test[0])['numberOfPlaces']) in result.data.decode()
        assert int(club_points_before_purchase) == int(club['points'])
        assert int(competitions_places_before_purchase) == int((competitions_test[0])['numberOfPlaces'])

    def test_purchase_indexerror_1(self, client, valid_reservation_mocker, data_base_mocker, clubs_test,
                           competitions_test, new_old_competitions_mocker):

        club = clubs_test[0]
        data = {
            'competition': "bad competition",
            'club': club['name'],
            'places': MAX_PURCHASE + 1,
        }
        result = client.post(ENDPOINT_PURCHASE_PLACES, data=data)
        assert result.status_code == HTTPStatus.NOT_FOUND
        assert "Something went wrong-please try again" in result.data.decode()

    def test_purchase_indexerror_2(self, client, valid_reservation_mocker, data_base_mocker, clubs_test,
                           competitions_test, new_old_competitions_mocker):

        club = clubs_test[0]
        data = {
            'competition': (competitions_test[0])['name'],
            'club': "bad club",
            'places': MAX_PURCHASE + 1,
        }
        result = client.post(ENDPOINT_PURCHASE_PLACES, data=data)
        assert result.status_code == HTTPStatus.NOT_FOUND
        assert "Something went wrong-please try again" in result.data.decode()

    def test_purchase_value_error(self, client, valid_reservation_mocker, data_base_mocker, clubs_test,
                           competitions_test, new_old_competitions_mocker):

        club = clubs_test[0]
        data = {
            'competition': (competitions_test[0])['name'],
            'club': club['name'],
            'places': "bad caracters",
        }
        result = client.post(ENDPOINT_PURCHASE_PLACES, data=data)
        assert result.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assert "The entry must be an number between 1 and 12" in result.data.decode()