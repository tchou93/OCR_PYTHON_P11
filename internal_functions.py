from flask import json


def loadClubs() -> object:
    with open('D:\Tan\Travail\developpement\python\projetOC\projet11\clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('D:\Tan\Travail\developpement\python\projetOC\projet11\competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions
