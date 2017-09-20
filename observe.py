#!/usr/local/bin/python

import argparse
import random
import os
import sys
import time

from pomme_api import *
from bot import BOTS
from subprocess import Popen

parser = argparse.ArgumentParser(description="Spawns and destroys bots in given rooms.")
parser.add_argument("--control", type=bool, default=False, help="The script will only spawn bots if this is True.")
parser.add_argument("--stat", type=bool, default=False, help="If True only checks rooms once.")
parser.add_argument("--join", type=str, help="Name of the room for bots to join")
parser.add_argument("--kill", type=str, help="Name of the room for bots to evac.")

ENOUGH_HUMANS = 7
MAX_BOTS = 3

username = "botcontrol"
password = "secretpomme"

def kill_bots(room):
  #print "killing", room
  commands = open("commands/" + room, "w")
  commands.write("leave")
  commands.close()

def spawn_bots(room):
  # only send bots to bigapple for now.
  # keep all other rooms human so bots aren't spammy
  room = "bigapple"
  commands = open("commands/" + room, "w")
  commands.write("join")
  commands.close()

  bots = random.sample(BOTS, MAX_BOTS)
  for bot in bots:
    #print "spawning %s in %s" % (bot, room)
    cwd = os.getcwd()
    cmd = ["python", cwd + "/bot.py", bot, "--room", room, "--password", "secretpomme"]
    devnull = open(os.devnull, 'wb')
    Popen(cmd)
    #Popen(cmd, stdout=devnull, stderr=devnull)

def get_info():
  login = api_login(username, password)
  if "error" in login:
    #print login["error"]
    sys.exit()
  session = login["session"]

  info = api_list(session)
  games = info["games"]
  for room in games:
    if room != "lobbychat":
      # go over all the players in the room and sort between humans and bots.
      players = games[room]["players"]
      humans, bots = [], []
      for player in players:
        if player["name"] in BOTS:
          bots.append(player)
        else:
          humans.append(player)

      # show human/robot room info.
      #print "%d humans, %d bots in %s" % (len(humans), len(bots), room)

      if args.control:
        if len(humans) >= ENOUGH_HUMANS:
          kill_bots(room)
        elif len(humans) > 0 and len(bots) < MAX_BOTS:
          spawn_bots(room)

args = parser.parse_args()
if args.join:
  spawn_bots(args.join)
  sys.exit()

if args.kill:
  kill_bots(args.join)
  sys.exit()

if __name__ == "__main__":
  while(True):
    get_info()
    if args.stat:
      sys.exit()
    time.sleep(60)
