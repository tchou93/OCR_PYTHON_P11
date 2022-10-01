import datetime

from external_functions import get_old_new_competitions


def datetime_format_to_str(date):
    return date.strftime("%Y-%m-%d %H:%M:%S")


def test_sut_get_old_new_competitions():
    actual_date = datetime_format_to_str(datetime.datetime.now())
    actual_date_plus_one_day = datetime_format_to_str(datetime.datetime.now() + datetime.timedelta(days=1))
    actual_date_minus_one_day = datetime_format_to_str(datetime.datetime.now() - datetime.timedelta(days=1))
    print(str(actual_date))
    competitions = [
        {"name": "Competition test1", "date": actual_date, "numberOfPlaces": "25"},
        {"name": "Competition test2", "date": actual_date_plus_one_day, "numberOfPlaces": "25"},
        {"name": "Competition test3", "date": actual_date_minus_one_day, "numberOfPlaces": "25"},
        {"name": "Competition test4", "date": "2020-03-27 10:00:00", "numberOfPlaces": "25"},
        {"name": "Competition test5", "date": "2021-03-27 10:00:00", "numberOfPlaces": "25"},
    ]

    old_competitions = [
        {"name": "Competition test3", "date": actual_date_minus_one_day, "numberOfPlaces": "25"},
        {"name": "Competition test4", "date": "2020-03-27 10:00:00", "numberOfPlaces": "25"},
        {"name": "Competition test5", "date": "2021-03-27 10:00:00", "numberOfPlaces": "25"},
    ]

    new_competitions = [
        {"name": "Competition test1", "date": actual_date, "numberOfPlaces": "25"},
        {"name": "Competition test2", "date": actual_date_plus_one_day, "numberOfPlaces": "25"},
    ]
    assert (get_old_new_competitions(competitions))[0] == old_competitions
    assert (get_old_new_competitions(competitions))[1] == new_competitions
