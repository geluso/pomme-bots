#!/usr/local/bin/python

import argparse
import json
import random
import requests
import time

from bestcards import CARD_RANKINGS

parser = argparse.ArgumentParser(description="Creates a Pomme bot that joins a room and automatically plays the game.")
parser.add_argument("username", type=str, help="The bot account username.")
parser.add_argument("--password", type=str, nargs="?", default="", help="The bot account password.")
parser.add_argument("--session", type=str, nargs="?", default="", help="Providing a session will skip login and mimic a current session.")
parser.add_argument("--room", type=str, nargs="?", default="bigapple", help="Which room to join.")
parser.add_argument("--submit-delay", type=int, default=15, help="The bot will wait until the countdown is below this number to submit bets.")
parser.add_argument("--judge-delay", type=int, default=7, help="The bot will wait until the countdown is below this number to submit judgements.")

BASE_URL = "http://pomme.us:32123"
LOGIN = BASE_URL + "/user/login"
LOGOUT = BASE_URL + "/user/logout"
GAME_JOIN = BASE_URL + "/game/join"
GAME_POLL = BASE_URL + "/game/poll"
GAME_BET = BASE_URL + "/game/bet"
GAME_JUDGE = BASE_URL + "/game/judge"

STATE_IDLE = 0
STATE_SETUP = 1
STATE_BET = 2
STATE_PICKED = 3
STATE_JUDGE = 4
STATE_VOTE = 5
STATE_WIN = 6
STATE_GAMEOVER = 7

STATES = {
  0: "waiting for other players.",
  1: "setup",
  2: "bet",
  3: "picked",
  4: "judge",
  5: "vote",
  6: "someone won round.",
  7: "someone won game."
}

def is_json(func):
  def func_wrapper(*args):
    return json.loads(func(*args).text)
  return func_wrapper

@is_json
def api_login(name, password=""):
  req = requests.post(LOGIN, data={"name": name, "password":password})
  return req

@is_json
def api_join(session, game="bigapple", last=0):
  req = requests.post(GAME_JOIN, data={"session": session, "game": game, "last": last})
  return req

@is_json
def api_poll(session, game, last=0):
  req = requests.post(GAME_POLL, data={"session": session, "game": game, "last": last})
  return req

@is_json
def api_bet(session, game, card, deck="player"):
  req = requests.post(GAME_BET, data={"session": session, "game": game, "card": card, "deck": deck})
  return req

@is_json
def api_judge(session, game, card, deck="player"):
  req = requests.post(GAME_JUDGE, data={"session": session, "game": game, "card": card, "deck": "player"})
  return req

@is_json
def api_logout(game, name):
  req = requests.post(LOGOUT, data={"session": session, "game": game, "name": name})
  return req

def best_card(cards):
  best_score = 0
  best_card = None
  for card in cards:
    try:
      ranking = CARD_RANKINGS[card]
      if ranking > best_score:
        best_score = ranking
        best_card = card
    except KeyError:
      ranking = 0
    print "%04d %s" % (ranking, card)
  return best_card

args = parser.parse_args()
username = args.username
password = args.password
session = args.session
room = args.room

if not session:
  print "Logging in as", username
  login = api_login(username, password)
  session = login["session"]
else:
  print "using existing session."
print session

game = api_join(session, room)
room = game["path"]
cards = game["cards"]

print "Robot:", username
print "Joined:", room
print "Hand:", cards

while (True):
  time.sleep(1)
  poll = api_poll(session, room)

  state = poll["state"]
  bets = poll["bets"]

  print state, STATES[state]
  if state == STATE_BET:
    countdown = poll["countdown"]
    if countdown > 7:
      print countdown, "waiting to submit bet."
    else:
      card = best_card(cards)
      print "betting:", card
      bet = api_bet(session, room, card)
      print bet
      if len(bet) > 0:
        card = bet["card"]
        print "adding:", card
        cards.append(card)
        print "new hand:", cards
  elif state == STATE_PICKED:
    print "Waiting for players to submit."
  elif state == STATE_JUDGE:
    countdown = poll["countdown"]
    if countdown > 5:
      print countdown, "waiting to submit judgement."
    else:
      card = best_card(bets)
      print "bets:", bets
      print "betting:", card
      api_judge(session, room, card)
  else:
    pass
