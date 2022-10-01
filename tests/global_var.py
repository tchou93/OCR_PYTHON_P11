ENDPOINT_SHOWSUMMARY = "/showSummary"
ENDPOINT_PURCHASE_PLACES = "/purchasePlaces"
ENDPOINT_BOOK = "/book"
ENDPOINT_RECAP_CLUB_POINTS = "/pointsDisplay"
MAX_PURCHASE = 12

simu_clubs = [
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

simu_competitions = [
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

simu_dict_clubs_purchase = {
    'Simply Lift': {'Spring Festival': 0, 'Fall Classic': 0, 'Competition Test': 0},
    'Iron Temple': {'Spring Festival': 0, 'Fall Classic': 0, 'Competition Test': 0},
    'She Lifts': {'Spring Festival': 0, 'Fall Classic': 0, 'Competition Test': 0},
    'Club Test': {'Spring Festival': 0, 'Fall Classic': 0, 'Competition Test': 0}
}
