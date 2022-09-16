import pytest

from server import valid_reservation
from tests.global_var import ENDPOINT_SHOWSUMMARY,MAX_PURCHASE

@pytest.mark.parametrize("places_required, clubpoint,nb_place_competition, expected_value, messages",
                         [(MAX_PURCHASE+1, 20, 50, False, ["The places required should not be more than 12"]),
                          (MAX_PURCHASE, 20, 50, True, ["Great-booking complete!"]),
                          (MAX_PURCHASE-1, 20, 50, True, ["Great-booking complete!"]),
                          (MAX_PURCHASE-1, 20, 10, False, ["The places required is more than the number of places of the "
                                               "competition."]),
                          (MAX_PURCHASE-2, 20, 10, True, ["Great-booking complete!"]),
                          (MAX_PURCHASE-3, 20, 10, True, ["Great-booking complete!"]),
                          (MAX_PURCHASE-1, 10, 20, False, ["The places required is more than the number of places of the club"]),
                          (MAX_PURCHASE-2, 10, 20, True, ["Great-booking complete!"]),
                          (MAX_PURCHASE-3, 10, 20, True, ["Great-booking complete!"]),
                          (MAX_PURCHASE+1, 30, 12, False, ["The places required should not be more than 12",
                                               "The places required is more than the number of places of the "
                                               "competition"]),
                          (MAX_PURCHASE+1, 12, 12, False, ["The places required should not be more than 12",
                                               "The places required is more than the number of places of the "
                                               "competition",
                                               "The places required is more than the number of places of the club"]),
                          (-1, 20, 50, False, ["The places required should be more than 0"]),
                          (0, 20, 50, False, ["The places required should be more than 0"]),
                          ])
def test_sut_validreservation(places_required, clubpoint, nb_place_competition, expected_value, messages):
    assert (valid_reservation(places_required, clubpoint, nb_place_competition))[0] == expected_value
    for message in messages:
        assert message in (valid_reservation(places_required, clubpoint, nb_place_competition))[1]
