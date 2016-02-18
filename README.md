Ignore the index.php. That's a failed attempt to create a web interface for these bots.

Create one bot by running

python bot.py [botname] --password [password] --game [room]

Log in to the web interface then use the Chrome Javascript console to find
document.cookie and get the session your user has. Copy and paste that
session string and run a bot that will submit bets and judge for you
while you use the web interface to see what it's doing.

python bot.py [username] --session [session string]

Run observe.py to see how many humans and bots are in each rooom.
Running this script will only print info out and won't spawn bots unless
the --control True flag is set.

python control.py

or 

ptyhon control.py --control True

Read the source to see more about what options are available,
and good luck!

Watch out for errors if anything refers to my local filesystem.
