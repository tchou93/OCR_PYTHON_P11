import pytest

from external_functions import valid_reservation
from tests.global_var import MAX_PURCHASE

@pytest.mark.parametrize("clubs_purchase, places_required, clubpoint,nb_place_competition, expected_value, messages",
                         [(0, MAX_PURCHASE+1, 20, 50, False, ["The places required should not be more than 12"]),
                          (0, MAX_PURCHASE, 20, 50, True, ["Great-booking complete!"]),
                          (0, MAX_PURCHASE-1, 20, 50, True, ["Great-booking complete!"]),
                          (0, MAX_PURCHASE-1, 20, 10, False, ["The places required is more than the number of places "
                                                              "of the competition."]),
                          (0, MAX_PURCHASE-2, 20, 10, True, ["Great-booking complete!"]),
                          (0, MAX_PURCHASE-3, 20, 10, True, ["Great-booking complete!"]),
                          (0, MAX_PURCHASE-1, 10, 20, False, ["The places required is more than the number of places "
                                                              "of the club"]),
                          (0, MAX_PURCHASE-2, 10, 20, True, ["Great-booking complete!"]),
                          (0, MAX_PURCHASE-3, 10, 20, True, ["Great-booking complete!"]),
                          (0, MAX_PURCHASE+1, 30, 12, False, ["The places required should not be more than 12",
                                               "The places required is more than the number of places of the "
                                               "competition"]),
                          (0, MAX_PURCHASE+1, 12, 12, False, ["The places required should not be more than 12",
                                               "The places required is more than the number of places of the "
                                               "competition",
                                               "The places required is more than the number of places of the club"]),
                          (0, -1, 20, 50, False, ["The places required should be more than 0"]),
                          (0, 0, 20, 50, False, ["The places required should be more than 0"]),
                          (1, MAX_PURCHASE, 20, 10, False, ["The total of the place for this competition is more than 12"]),
                          (1, MAX_PURCHASE -1, 20, 20, True, ["Great-booking complete!"]),
                          ])
def test_sut_validreservation(clubs_purchase,
                              places_required,
                              clubpoint,
                              nb_place_competition,
                              expected_value,
                              messages):
    assert (valid_reservation(clubs_purchase, places_required, clubpoint, nb_place_competition))[0] == expected_value
    for message in messages:
        assert message in (valid_reservation(clubs_purchase,places_required, clubpoint, nb_place_competition))[1]
