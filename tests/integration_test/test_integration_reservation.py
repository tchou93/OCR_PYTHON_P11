import pytest
from http import HTTPStatus
import random
from tests.global_var import ENDPOINT_PURCHASE_PLACES
from tests.global_var import MAX_PURCHASE

@pytest.fixture
def valid_reservation_mocker(mocker):
    mocker.patch('server.valid_reservation', return_value=(True, "Valid message"))


@pytest.fixture
def invalid_reservation_mocker(mocker):
    mocker.patch('server.valid_reservation', return_value=(False, "Invalid message"))


class TestReservation:

    def test_good_purchase(self, client, valid_reservation_mocker, data_base_mocker, clubs_test,
                                  competitions_test):
        data = {
            'competition': (competitions_test[0])['name'],
            'club': (clubs_test[0])['name'],
            'places': random.randint(1, MAX_PURCHASE),
        }
        club_points_before_purchase = (clubs_test[0])['points']
        competitions_places_before_purchase = (competitions_test[0])['numberOfPlaces']
        result = client.post(ENDPOINT_PURCHASE_PLACES, data=data)

        assert result.status_code == HTTPStatus.OK
        assert "Valid message" in result.data.decode()
        assert int(club_points_before_purchase) - data['places'] == int((clubs_test[0])['points'])
        assert int(competitions_places_before_purchase) - data['places'] == \
               int((competitions_test[0])['numberOfPlaces'])

    def test_bad_purchase(self, client, invalid_reservation_mocker, data_base_mocker, clubs_test,
                                  competitions_test):
        data = {
            'competition': (competitions_test[0])['name'],
            'club': (clubs_test[0])['name'],
            'places': 0,
        }
        club_points_before_purchase = (clubs_test[0])['points']
        competitions_places_before_purchase = (competitions_test[0])['numberOfPlaces']
        result = client.post(ENDPOINT_PURCHASE_PLACES, data=data)

        assert result.status_code == HTTPStatus.BAD_REQUEST
        assert "Invalid message" in result.data.decode()
        assert int(club_points_before_purchase) == int((clubs_test[0])['points'])
        assert int(competitions_places_before_purchase) == int((competitions_test[0])['numberOfPlaces'])