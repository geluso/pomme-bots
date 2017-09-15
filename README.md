# Pomme Bots, bots for pomme
Ignore the index.php. That's a failed attempt to create a web interface for these bots.

Create one bot by running

```bash
python bot.py [botname] --password [password] --game [room]
```

Log in to the web interface then use the Chrome Javascript console to find
document.cookie and get the session your user has. Copy and paste that
session string and run a bot that will submit bets and judge for you
while you use the web interface to see what it's doing.

```bash
python bot.py [username] --session [session string]
```

Run observe.py to see how many humans and bots are in each rooom.
Running this script will only print info out and won't spawn bots unless
the --control True flag is set.

```bash
python control.py
```

or 

```bash
ptyhon control.py --control True
```

Read the source to see more about what options are available,
and good luck!

```python
def get_args():
  parser = argparse.ArgumentParser(description="Creates a Pomme bot that joins a room and automatically plays the game.")
  parser.add_argument("username", type=str, help="The bot account username.")
  parser.add_argument("--password", type=str, nargs="?", default="secretpomme", help="The bot account password.")
  parser.add_argument("--session", type=str, nargs="?", default="", help="Providing a session will skip login and mimic a current session.")
  parser.add_argument("--room", type=str, nargs="?", default="bigapple", help="Which room to join.")
  parser.add_argument("--submitdelay", type=int, default=15, help="The bot will wait until the countdown is below this number to submit bets.")
  parser.add_argument("--judgedelay", type=int, default=7, help="The bot will wait until the countdown is below this number to submit judgements.")
  parser.add_argument("--verbose", type=bool, default=False, help="Print things if True.")
  return parser.parse_args()
```

Watch out for errors if anything refers to my local filesystem.
