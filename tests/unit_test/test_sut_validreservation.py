import pytest

from server import valid_reservation


@pytest.mark.parametrize("places_required, clubpoint,nb_place_competition, expected_value, messages",
                         [(13, 20, 50, False, ["The places required should not be more than 12"]),
                          (12, 20, 50, True, ["Great-booking complete!"]),
                          (11, 20, 50, True, ["Great-booking complete!"]),
                          (11, 20, 10, False, ["The places required is more than the number of places of the "
                                               "competition."]),
                          (10, 20, 10, True, ["Great-booking complete!"]),
                          (9, 20, 10, True, ["Great-booking complete!"]),
                          (11, 10, 20, False, ["The places required is more than the number of places of the club"]),
                          (10, 10, 20, True, ["Great-booking complete!"]),
                          (9, 10, 20, True, ["Great-booking complete!"]),
                          (13, 30, 12, False, ["The places required should not be more than 12",
                                               "The places required is more than the number of places of the "
                                               "competition"]),
                          (13, 12, 12, False, ["The places required should not be more than 12",
                                               "The places required is more than the number of places of the "
                                               "competition",
                                               "The places required is more than the number of places of the club"])])
def test_sut_validreservation(places_required, clubpoint, nb_place_competition, expected_value, messages):
    assert (valid_reservation(places_required, clubpoint, nb_place_competition))[0] == expected_value
    for message in messages:
        assert message in (valid_reservation(places_required, clubpoint, nb_place_competition))[1]
