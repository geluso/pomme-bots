#!/usr/local/bin/python

import argparse
import time
import sys
import os
import random

from bestcards import *
from pomme_api import *
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

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
      message = "%s received kill order" % username
      logging.info(message)
      sys.exit()
  except IOError:
    sys.exit()

if __name__ == "__main__":
  args = get_args()
  username = args.username
  password = args.password
  session = args.session
  room = args.room

  if not session:
    message = "Logging in as %s with password %s" % (username, password)
    logging.info(message)
    login = api_login(username, password)
    if "error" in login:
      message = "%s %s" % (username, login["error"])
      logging.info(message)
      sys.exit()
    session = login["session"]
  else:
    logging.info("using existing session.")
  logging.info(session)

  game = api_join(session, room)
  room = game["path"]
  cards = game["cards"]

  logging.info("Robot: %s" % username)
  logging.info("Joined: %s" % room)
  logging.info("Hand: %s", cards)

  while (True):
    if not args.ignorecommands:
      check_commands(room)

    time.sleep(1)
    poll = api_poll(session, room)

    state = poll["state"]
    bets = poll["bets"]

    message = "%s %s %s" % (username, state, STATES[state])
    logging.info(message)
    if state == STATE_BET:
      countdown = poll["countdown"]
      if countdown > args.submitdelay:
        message = "%s waiting to submit bet" % countdown
        logging.info(message)
      else:
        card = best_card(cards)
        if card is None:
          card = random.choice(cards)
        logging.info("betting: %s" % card)
        bet = api_bet(session, room, card)
        logging.info(bet)
        if len(bet) > 0:
          new_card = bet["card"]
          logging.info("adding: %s" % card)
          cards.remove(card)
          cards.append(new_card)
          logging.info("new hand:", cards)
    elif state == STATE_PICKED:
      logging.info("Waiting for players to submit.")
    elif state == STATE_JUDGE:
      countdown = poll["countdown"]
      if countdown > args.judgedelay:
        logging.info("%s waiting to submit judgement." % countdown)
      else:
        card = best_card(bets)
        logging.info("bets:", bets)
        logging.info("betting: %s" % card)
        api_judge(session, room, card)
