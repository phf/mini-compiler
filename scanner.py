# $Id: scanner.py 639 2005-05-10 20:27:02Z phf $
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

import string as S

keywords = ["PROGRAM", "VAR", "BEGIN", "END", "WHILE", "DO", "PRINT"]
symbols = ["=", ",", "+", "-"]

class Token:
  """
  A simple class representing tokens.

  Aside from keywords and special symbols, there are three more
  kinds of tokens, encoded as strings as well:

    "eof" = end of file = nothing left to do, dang it!
    "identifier" = value is the identifier itself (as a string)
    "constant" = value is the constant itself (as an integer)

  TODO
  """
  def __init__( self, kind, value=None ):
    self.kind = kind
    self.value = value
  def __str__( self ):
    if self.kind in ["identifier","constant"]:
      return "%s<%s>" % (self.kind, self.value)
    else:
      return self.kind

class Scanner:
  """
  A simple scanner for Mini.

  Efficiency my behind. This is hand-coded for readability, not
  because it's faster than using regular expressions.
  """
  def __init__( self, name ):
    """
    Create a new scanner for file "name".
    """
    file = open( name )
    self.src = file.read()
    file.close()
    self.len = len( self.src )
    self.pos = 0
    self.eof = Token( "eof" )

  def valid( self ):
    """
    Valid position in the source file?
    """
    return self.pos < self.len

  def char( self ):
    """
    Current character in the source file?
    """
    if self.valid():
      return self.src[self.pos]

  def tick( self ):
    """
    Advance one character in the source file.
    """
    if self.valid():
      self.pos += 1

  def next( self ):
    """
    Return the next token.

    If an illegal character is found we raise an exception to
    that effect.

    Once we are done with the source file, we keep returning
    the "eof" token.
    """
    token = self.eof

    # Skip whitespace.
    while self.valid() and self.char() in S.whitespace:
      self.tick()

    # Anything left to scan?
    if self.valid():
      if self.char() in S.letters:
        # Assemble the identifier...
        id = ""
        while self.valid() and self.char() in S.letters:
          id += self.char()
          self.tick()
        # Keyword in disguise?
        if id in keywords:
          token = Token( id )
        else:
          token = Token( "identifier", id )
      elif self.char() in S.digits:
        # Assemble the constant...
        int = 0
        while self.valid() and self.char() in S.digits:
          int = 10*int + ord( self.char() ) - ord( "0" )
          self.tick()
        token = Token( "constant", int )
      elif self.char() in symbols:
        # Just a symbol...
        token = Token( self.char() )
        self.tick()
      else:
        # Something we can't deal with!
        raise "Unexpected character!"

    # Return the token.
    return token

if __name__ == "__main__":
  scanner = Scanner( "examples/prime.mini" )
  token = scanner.next()
  while token.kind != "eof":
    print token
    token = scanner.next()

