from flask import json
import time
from datetime import datetime

MAXIMUM_PURCHASE = 12

FILE_CLUBS_PATH = "clubs.json"
FILE_COMPETITIONS_PATH = "competitions.json"


def loadclubs() -> object:
    with open(FILE_CLUBS_PATH) as c:
        listofclubs = json.load(c)['clubs']
        return listofclubs


def loadcompetitions():
    with open(FILE_COMPETITIONS_PATH) as comps:
        listofcompetitions = json.load(comps)['competitions']
        return listofcompetitions


def valid_reservation(clubs_purchase, places_required, clubpoint, nb_place_competition):
    message = ""
    if places_required > MAXIMUM_PURCHASE:
        message += "The places required should not be more than 12. "

    if (clubs_purchase + places_required) > MAXIMUM_PURCHASE:
        message += f"The total of the place for this competition is more than 12"

    if places_required > nb_place_competition:
        message += "The places required is more than the number of places of the competition. "

    if places_required > clubpoint:
        message += "The places required is more than the number of places of the club."

    if places_required <= 0:
        message += "The places required should be more than 0."

    if message == "":
        message += "Great-booking complete!"
        return True, message
    else:
        return False, message


def get_old_new_competitions(comp):
    comp_tmp = comp.copy()
    comp_old = []
    comp_new = []
    actual_date = datetime.now()
    actual_date = actual_date.strftime("%Y-%m-%d %H:%M:%S")
    formatted_actual_date = time.strptime(actual_date, "%Y-%m-%d %H:%M:%S")

    while comp_tmp:
        formatted_competition_date = time.strptime((comp_tmp[0])["date"], "%Y-%m-%d %H:%M:%S")
        if formatted_actual_date > formatted_competition_date:
            comp_old.append(comp_tmp.pop(0))
        else:
            comp_new.append(comp_tmp.pop(0))
    return comp_old, comp_new


def init_dict_club_purchase(_clubs, _competitions):
    _dict_clubs_purchase = {}
    i = 0
    for _club in _clubs:
        globals()[f"dict_competitions_purchase_{i}"] = {}
        for _competition in _competitions:
            (globals()[f"dict_competitions_purchase_{i}"])[_competition["name"]] = 0
        _dict_clubs_purchase[_club["name"]] = globals()[f"dict_competitions_purchase_{i}"]
        i += 1
    return _dict_clubs_purchase


def get_possibility_to_book(_club, _new_competitions, _dict_clubs_purchase):
    if _club["points"] == 0:
        books_ko = _new_competitions.copy()
        books_ok = []
    else:
        books_ok = _new_competitions.copy()
        books_ko = []
        for _competition in _new_competitions:
            if ((_dict_clubs_purchase[_club["name"]])[_competition["name"]] >= MAXIMUM_PURCHASE) \
                    or (_competition["numberOfPlaces"] == 0):
                books_ko.append(_competition)
                books_ok.remove(_competition)

    return books_ko, books_ok


def update_club_purchase(_dict_clubs_purchase, _clubs_name, _competitions_name, place):
    dict_club = _dict_clubs_purchase[_clubs_name]
    dict_club[_competitions_name] = dict_club[_competitions_name] + place
