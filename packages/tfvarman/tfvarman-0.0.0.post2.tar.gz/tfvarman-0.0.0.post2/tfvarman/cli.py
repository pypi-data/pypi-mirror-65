"""tfvarman cli

Usage:
  tfvarman sync <varfile>
  tfvarman show <varfile>

  tfvarman (-h | --help)
  tfvarman --version

Options:
  -h --help     Show this screen.
  --version     Show version.
"""
from tfvarman import TFVarMan
from docopt import docopt
from tabulate import tabulate
import sys
import json
import yaml

def main():
  arguments = docopt(__doc__, version='tfvarman 0.0.0-post1')
  # print(arguments)
  data = {}

  try:
    tf = TFVarMan(arguments)
    if arguments['sync']:
      tf.sync()
    
    if arguments['show']:
      tf.show()
  except Exception as err:
    print("ERROR: %s" % (str(err)))
    sys.exit(1)