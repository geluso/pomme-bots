#!/usr/local/bin/python

import argparse
import time

from bestcards import *
from pomme_api import *

parser = argparse.ArgumentParser(description="Creates a Pomme bot that joins a room and automatically plays the game.")
parser.add_argument("username", type=str, help="The bot account username.")
parser.add_argument("--password", type=str, nargs="?", default="", help="The bot account password.")
parser.add_argument("--session", type=str, nargs="?", default="", help="Providing a session will skip login and mimic a current session.")
parser.add_argument("--room", type=str, nargs="?", default="bigapple", help="Which room to join.")
parser.add_argument("--submitdelay", type=int, default=15, help="The bot will wait until the countdown is below this number to submit bets.")
parser.add_argument("--judgedelay", type=int, default=7, help="The bot will wait until the countdown is below this number to submit judgements.")

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
    if countdown > args.submitdelay:
      print countdown, "waiting to submit bet."
    else:
      card = best_card(cards)
      print "betting:", card
      bet = api_bet(session, room, card)
      print bet
      if len(bet) > 0:
        new_card = bet["card"]
        print "adding:", card
        cards.remove(card)
        cards.append(new_card)
        print "new hand:", cards
  elif state == STATE_PICKED:
    print "Waiting for players to submit."
  elif state == STATE_JUDGE:
    countdown = poll["countdown"]
    if countdown > args.judgedelay:
      print countdown, "waiting to submit judgement."
    else:
      card = best_card(bets)
      print "bets:", bets
      print "betting:", card
      api_judge(session, room, card)
  else:
    pass
