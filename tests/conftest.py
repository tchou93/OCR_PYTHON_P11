import pytest

import server
from server import app


def get_clubs_tests():
    clubs = [
        {
            "name": "Simply Lift",
            "email": "john@simplylift.com",
            "points": "13"
        },
        {
            "name": "Iron Temple",
            "email": "admin@irontemple.com",
            "points": "4"
        },
        {
            "name": "She Lifts",
            "email": "kate@shelifts.co.uk",
            "points": "12"
        },
        {
            "name": "Club Test",
            "email": "clubtest@gmail.com",
            "points": "50"
        },
    ]
    return clubs


def get_competitions_tests():
    competitions = [
        {
            "name": "Spring Festival",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25"
        },
        {
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13"
        },
        {
            "name": "Competition Test",
            "date": "2022-10-22 13:30:00",
            "numberOfPlaces": "50"
        },
    ]
    return competitions


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture
def databasemocker(mocker):
    mocker.patch.object(server, "clubs", get_clubs_tests())
    mocker.patch.object(server, "competitions", get_competitions_tests())
