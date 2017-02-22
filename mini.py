# $Id: mini.py 653 2005-05-11 06:55:27Z phf $
#
# Copyright (c) 2005 by Peter H. Froehlich <phf@acm.org>.
# All rights reserved.
#
# This file is part of Mini.
#
# Mini is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published
# by the Free Software Foundation; either version 2 of the License,
# or (at your option) any later version.
#
# Mini is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mini; if not, write to the Free Software Foundation,
# Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301, USA.

import scanner as S
import parser as P
import version as V

import optparse as O

def command_line():
  """
  Parse command line, optparse style.
  """
  parser = O.OptionParser( usage="%prog", \
    version="%prog " + "%s" % V.__version__ )

  parser.add_option( "-l", "--lc3", action = "store_true", \
    help = "generate code for the LC-3" )

  parser.add_option( "-i", "--i386", action = "store_true", \
    help = "generate code for the Intel 80386" )

  parser.add_option( "-p", "--powerpc", action = "store_true", \
    help = "generate code for the Motorola PowerPC" )

  parser.add_option( "-m", "--m68000", action = "store_true", \
    help = "generate code for the Motorola 68000 (broken)" )

  parser.add_option( "-9", "--m6809", action = "store_true", \
    help = "generate code for the Motorola 6809 (broken)" )

  parser.add_option( "-x", "--mmix", action = "store_true", \
    help = "generate code for Knuth's MMIX" )

  parser.add_option( "-b", "--big", action = "store_true", \
    help = "generate code for 32-bit arithmetic (for LC-3, 6809; broken)" )

  return parser.parse_args()

def main():
  """
  Read the source, Luke!
  """
  (options, arguments) = command_line()
  extension = ".s"

  # what a hack... :-/
  if options.m68000:
    import m68k as G
  elif options.powerpc:
    import powerpc as G
  elif options.i386:
    import i386  as G
  elif options.lc3:
    if options.big:
      import lc3long as G
    else:
      import lc3 as G
    extension = ".asm"
  elif options.m6809:
    if options.big:
      import m6809long as G
    else:
      import m6809 as G
    extension = ".asm"
  elif options.mmix:
    import mmix as G
    extension = ".mms"
  else:
    import spim as G

  if len( arguments ) > 0:
    for name in arguments:
      s = S.Scanner( name + ".mini" )
      g = G.Generator( name + extension )
      p = P.Parser( s, g )
      p.Program()
      g.commit()
  else:
    print "error: No files to compile!"

