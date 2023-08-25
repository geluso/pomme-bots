from __future__ import print_function

LOGGING = False

def log(*args):
  if LOGGING:
    print(*args)
