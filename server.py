from flask import Flask, render_template, request, redirect, flash, url_for
from http import HTTPStatus
from external_functions import loadcompetitions, loadclubs, init_dict_club_purchase, get_old_new_competitions, \
    get_possibility_to_book, \
    valid_reservation, update_club_purchase

# Create app
app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadcompetitions()
competitions_old, competitions_new = get_old_new_competitions(competitions)
clubs = loadclubs()
dict_clubs_purchase = init_dict_club_purchase(clubs, competitions)


# Endpoints
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showsummary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        books_ko, books_ok = get_possibility_to_book(club, competitions_new, dict_clubs_purchase)
        return render_template('welcome.html',
                               club=club,
                               competitions_no_book=competitions_old + books_ko,
                               competitions_book=books_ok,
                               already_book=dict_clubs_purchase
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
            books_ko, books_ok = get_possibility_to_book(foundclub, competitions_new, dict_clubs_purchase)
            return render_template('welcome.html',
                                   club=foundclub,
                                   competitions_no_book=competitions_old + books_ko,
                                   competitions_book=books_ok,
                                   already_book=dict_clubs_purchase
                                   ), HTTPStatus.BAD_REQUEST
    except IndexError:
        return render_template('error.html'), HTTPStatus.NOT_FOUND


@app.route('/purchasePlaces', methods=['POST'])
def purchaseplaces():
    try:
        competition = [c for c in competitions if c['name'] == request.form['competition']][0]
        club = [c for c in clubs if c['name'] == request.form['club']][0]
    except IndexError:
        return render_template('error.html'), HTTPStatus.NOT_FOUND

    try:
        placesrequired = int(request.form['places'])
        statut, message = valid_reservation((dict_clubs_purchase[club["name"]])[competition["name"]],
                                            placesrequired,
                                            int(club["points"]),
                                            int(competition['numberOfPlaces']))
        if statut:
            update_club_purchase(dict_clubs_purchase, club["name"], competition["name"], placesrequired)
            competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesrequired
            club['points'] = int(club['points']) - placesrequired
            flash(message)
            books_ko, books_ok = get_possibility_to_book(club, competitions_new, dict_clubs_purchase)
            return render_template('welcome.html',
                                   club=club,
                                   competitions_no_book=competitions_old + books_ko,
                                   competitions_book=books_ok,
                                   already_book=dict_clubs_purchase
                                   )
        else:
            flash(message)
            return render_template('booking.html', club=club, competition=competition), HTTPStatus.BAD_REQUEST
    except ValueError:
        flash('The entry must be an number between 1 and 12.')
        return render_template('booking.html', club=club, competition=competition), HTTPStatus.INTERNAL_SERVER_ERROR


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


@app.route('/pointsDisplay')
def pointsdisplay():
    clubs_sort_by_points = sorted(clubs, key=lambda c: int(c['points']))
    return render_template('recap_club_points.html', clubs=clubs_sort_by_points)
