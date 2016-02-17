import requests
import json

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
