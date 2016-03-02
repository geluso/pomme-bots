#!/usr/local/bin/python

import argparse
import random
import os
import sys

from pomme_api import *
from bot import BOTS
from subprocess import Popen

parser = argparse.ArgumentParser(description="Spawns and destroys bots in given rooms.")
parser.add_argument("--control", type=bool, default=False, help="The script will only spawn bots if this is True.")
parser.add_argument("--join", type=str, help="Name of the room for bots to join")
parser.add_argument("--kill", type=str, help="Name of the room for bots to evac.")

ENOUGH_HUMANS = 7
MAX_BOTS = 3

username = "asdfus"
password = ""

def kill_bots(room):
  print "killing", room
  commands = open("commands/" + room, "w")
  commands.write("leave")
  commands.close()

def spawn_bots(room):
  commands = open("commands/" + room, "w")
  commands.write("join")
  commands.close()

  bots = random.sample(BOTS, MAX_BOTS)
  for bot in bots:
    print "spawning %s in %s" % (bot, room)
    cmd = ["nohup", "python", "/Users/moonmayor/Code/pomme-bots/bot.py", bot, "--room", room, "--password", "secretpomme"]
    devnull = open(os.devnull, 'wb')
    Popen(cmd)
    #Popen(cmd, stdout=devnull, stderr=devnull)

args = parser.parse_args()
if args.join:
  spawn_bots(args.join)
  sys.exit()

if args.kill:
  kill_bots(args.join)
  sys.exit()

login = api_login(username, password)
session = login["session"]

info = api_list(session)
games = info["games"]
for room in games:
  if room != "lobbychat":
    # go over all the players in the room and sort between humans and bots.
    players = games[room]["players"]
    humans, bots = [], []
    for player in players:
      if player["name"] in KNOWN_BOTS:
        bots.append(player)
      else:
        humans.append(player)

    # show human/robot room info.
    print "%d humans, %d bots in %s" % (len(humans), len(bots), room)

    if args.control:
      if len(humans) >= ENOUGH_HUMANS:
        kill_bots(room)
      elif len(humans) > 0 and len(bots) < MAX_BOTS:
        spawn_bots(room)
      print
