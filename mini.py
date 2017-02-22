# $Id: mini.py 515 2005-04-22 06:38:31Z phf $

import scanner as S
import parser as P
import spim as G
import version as V

import optparse as O

def command_line():
  """
  Parse command line, optparse style.
  """
  parser = O.OptionParser( usage="%prog", \
    version="%prog " + "%s" % V.__version__ )

#  parser.add_option( "-b", "--blame", action = "store_true", \
#    help = "perform blame analysis (pretty expensive)" )

  return parser.parse_args()

def main():
  """
  Read the source, Luke!
  """
  (options, arguments) = command_line()

  if len( arguments ) > 0:
    for name in arguments:
      s = S.Scanner( name + ".mini" )
      g = G.Generator( name + ".s" )
      p = P.Parser( s, g )
      p.Program()
      g.commit()
  else:
    print "error: No files to compile!"

