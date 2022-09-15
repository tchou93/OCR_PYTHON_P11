from flask import Flask, render_template, request, redirect, flash, url_for, json
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

########### Create app ###########
app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadcompetitions()
clubs = loadclubs()

########### Endpoints ###########
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showsummary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template('welcome.html', club=club, competitions=competitions)

    except IndexError:
        flash("Sorry, that email was not found.")
        return render_template('index.html'), HTTPStatus.UNAUTHORIZED


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundclub = [c for c in clubs if c['name'] == club][0]
    foundcompetition = [c for c in competitions if c['name'] == competition][0]
    if foundclub and foundcompetition:
        return render_template('booking.html', club=foundclub, competition=foundcompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


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
        return render_template('welcome.html', club=club, competitions=competitions)
    else:
        flash(message)
        return render_template('booking.html', club=club, competition=competition),HTTPStatus.BAD_REQUEST


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
