#!/usr/local/bin/python

import argparse
import time
import sys
import os
import random

from bestcards import *
from pomme_api import *
import logging
from logging import *

def get_args():
  parser = argparse.ArgumentParser(description="Creates a Pomme bot that joins a room and automatically plays the game.")
  parser.add_argument("username", type=str, help="The bot account username.")
  parser.add_argument("--password", type=str, nargs="?", default="secretpomme", help="The bot account password.")
  parser.add_argument("--session", type=str, nargs="?", default="", help="Providing a session will skip login and mimic a current session.")
  parser.add_argument("--room", type=str, nargs="?", default="bigapple", help="Which room to join.")
  parser.add_argument("--submitdelay", type=int, default=15, help="The bot will wait until the countdown is below this number to submit bets.")
  parser.add_argument("--judgedelay", type=int, default=7, help="The bot will wait until the countdown is below this number to submit judgements.")
  parser.add_argument("--verbose", type=bool, default=False, help="Print things if True.")
  parser.add_argument("--ignorecommands", type=bool, default=False, help="Run without reading the commands control file.")
  return parser.parse_args()

BOTS = [
  "polol",
  "Cowboy",
  "cabbageman",
  #"formulaD",
  #"puget",
  #"Wubbles",
  #"manky",
  #"Rickter",
  #"quaid",
  #"Bernadette",
  #"Pheobe",
  #"Butterfly",
  #"Moon_child",
  #"Suzzzy",
  #"Mars_girl",
  #"Seatbelt"
]

def check_commands(room):
  try:
    command = open("commands/" + room).read().strip()
    if command == "leave" or os.path.isfile("commands/kill"):
      log(username, "received kill order")
      sys.exit()
  except IOError:
    sys.exit()

if __name__ == "__main__":
  args = get_args()
  username = args.username
  password = args.password
  session = args.session
  room = args.room

  if args.verbose:
    logging.LOGGING = True

  if not session:
    log("Logging in as", username, "with password:", password)
    login = api_login(username, password)
    if "error" in login:
      log(username, login["error"])
      sys.exit()
    session = login["session"]
  else:
    log("using existing session.")
  log(session)

  game = api_join(session, room)
  room = game["path"]
  cards = game["cards"]

  log("Robot:", username)
  log("Joined:", room)
  log("Hand:", cards)

  while (True):
    if not args.ignorecommands:
      check_commands(room)

    time.sleep(1)
    poll = api_poll(session, room)

    state = poll["state"]
    bets = poll["bets"]

    log(username, state, STATES[state])
    if state == STATE_BET:
      countdown = poll["countdown"]
      if countdown > args.submitdelay:
        log(countdown, "waiting to submit bet.")
      else:
        card = best_card(cards)
        if card is None:
          card = random.choice(cards)
        log("betting:", card)
        bet = api_bet(session, room, card)
        log(bet)
        if len(bet) > 0:
          new_card = bet["card"]
          log("adding:", card)
          cards.remove(card)
          cards.append(new_card)
          log("new hand:", cards)
    elif state == STATE_PICKED:
      log("Waiting for players to submit.")
    elif state == STATE_JUDGE:
      countdown = poll["countdown"]
      if countdown > args.judgedelay:
        log(countdown, "waiting to submit judgement.")
      else:
        card = best_card(bets)
        log("bets:", bets)
        log("betting:", card)
        api_judge(session, room, card)
