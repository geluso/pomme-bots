import ssl
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import json
import hashlib

BASE_URL = "https://pomme.us:32123"
LOGIN = BASE_URL + "/user/login"
LOGOUT = BASE_URL + "/user/logout"
GAME_LIST = BASE_URL + "/game/list"
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

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

def post(url, data):
  data = urllib.parse.urlencode(data)
  data = data.encode("utf-8")
  return urllib.request.urlopen(url, data, context=CTX).read()

def is_json(func):
  def func_wrapper(*args):
    response = func(*args)
    try:
      jj = json.loads(response)
      if "error" in jj:
        #log(jj["error"])
        pass
      return jj
    except ValueError:
      #import pdb; pdb.set_trace()
      pass
  return func_wrapper

@is_json
def api_login(name, password=""):
  if password:
    password = "pomme" + password
    password = hashlib.md5(bytes(password, "utf-8")).hexdigest()
  data={"name": name, "password":password}
  return post(LOGIN, data)

@is_json
def api_list(session):
  data={"session": session}
  return post(GAME_LIST, data)

@is_json
def api_join(session, game="bigapple", last=0):
  data={"session": session, "game": game, "last": last}
  return post(GAME_JOIN, data)

@is_json
def api_poll(session, game, last=0):
  data={"session": session, "game": game, "last": last}
  return post(GAME_POLL, data)

@is_json
def api_bet(session, game, card, deck="player"):
  data={"session": session, "game": game, "card": card, "deck": deck}
  return post(GAME_BET, data)

@is_json
def api_judge(session, game, card, deck="player"):
  data={"session": session, "game": game, "card": card, "deck": "player"}
  return post(GAME_JUDGE, data)

@is_json
def api_logout(game, name):
  data={"session": session, "game": game, "name": name}
  return post(LOGOUT, data)

