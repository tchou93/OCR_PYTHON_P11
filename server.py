from flask import Flask, render_template, request, redirect, flash, url_for, json
import copy
import time
from datetime import datetime
from http import HTTPStatus


########### Internal function ###########
def loadclubs() -> object:
    with open(r'D:\Tan\Travail\developpement\python\projetOC\projet11\clubs.json') as c:
        listofclubs = json.load(c)['clubs']
        return listofclubs


def loadcompetitions():
    with open(r'D:\Tan\Travail\developpement\python\projetOC\projet11\competitions.json') as comps:
        listofcompetitions = json.load(comps)['competitions']
        return listofcompetitions


def valid_reservation(places_required, clubpoint, nb_place_competition):
    message = ""
    if places_required > 12:
        message += "The places required should not be more than 12. "

    if places_required > nb_place_competition:
        message += "The places required is more than the number of places of the competition. "

    if places_required > clubpoint:
        message += "The places required is more than the number of places of the club."

    if message == "":
        message += "Great-booking complete!"
        return True, message
    else:
        return False, message


def getOldNewCompetitions(comp):
    comp_tmp = copy.deepcopy(comp)
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


########### Create app ###########
app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadcompetitions()
competitions_old, competitions_new = getOldNewCompetitions(competitions)
clubs = loadclubs()


########### Endpoints ###########
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showsummary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template('welcome.html',
                               club=club,
                               competitions_old=competitions_old,
                               competitions_new=competitions_new
                               )

    except IndexError:
        flash("Sorry, that email was not found.")
        return render_template('index.html'), HTTPStatus.UNAUTHORIZED


@app.route('/book/<competition>/<club>')
def book(competition, club):
    try:
        foundclub = [c for c in clubs if c['name'] == club][0]
        foundcompetition = [c for c in competitions if c['name'] == competition][0]
        if foundclub and foundcompetition in competitions_new:
            return render_template('booking.html', club=foundclub, competition=foundcompetition)
        else:
            flash("This is a old competition-please try again")
            return render_template('welcome.html',
                                   club=club,
                                   competitions_old=competitions_old,
                                   competitions_new=competitions_new), HTTPStatus.BAD_REQUEST
    except IndexError:
        flash("Something went wrong-please try again", 'error')
        return render_template('welcome.html',
                               club=club,
                               competitions_old=competitions_old,
                               competitions_new=competitions_new), HTTPStatus.NOT_FOUND


@app.route('/purchasePlaces', methods=['POST'])
def purchaseplaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesrequired = int(request.form['places'])

    statut, message = valid_reservation(placesrequired, int(club["points"]), int(competition['numberOfPlaces']))
    if statut:
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesrequired
        club['points'] = int(club['points']) - placesrequired
        flash(message)
        return render_template('welcome.html',
                               club=club,
                               competitions_old=competitions_old,
                               competitions_new=competitions_new
                               )
    else:
        flash(message)
        return render_template('booking.html', club=club, competition=competition), HTTPStatus.BAD_REQUEST


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


@app.route('/pointsDisplay')
def pointsdisplay():
    clubs_sort_by_points = sorted(clubs, key=lambda club: int(club['points']))
    return render_template('recap_club_points.html', clubs=clubs_sort_by_points)
