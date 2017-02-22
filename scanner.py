# $Id: scanner.py 510 2005-04-22 03:17:24Z phf $

import string as S

class Token:
  def __init__( self, kind, value=None ):
    self.kind = kind
    self.value = value
  def __str__( self ):
    if self.kind in ["identifier","constant"]:
      return "%s<%s>" % (self.kind, self.value)
    else:
      return self.kind

class Scanner:
  def __init__( self, name ):
    file = open( name )
    self.src = file.read()
    file.close()
    self.len = len( self.src )
    self.pos = 0
    self.eof = Token( "eof" )

  def valid( self ):
    return self.pos < self.len
  def char( self ):
    if self.valid():
      return self.src[self.pos]
  def tick( self ):
    if self.valid():
      self.pos += 1

  def next( self ):
    token = self.eof

    # Skip whitespace.
    while self.valid() and self.char() in S.whitespace:
      self.tick()

    # Anything left to scan?
    if self.valid():
      if self.char() in S.letters:
        id = ""
        while self.valid() and self.char() in S.letters:
          id += self.char()
          self.tick()
        if id in ["PROGRAM","VAR","BEGIN","END","WHILE","DO","PRINT"]:
          token = Token( id )
        else:
          token = Token( "identifier", id )
      elif self.char() in S.digits:
        int = 0
        while self.valid() and self.char() in S.digits:
          int = 10*int + ord( self.char() ) - ord( "0" )
          self.tick()
        token = Token( "constant", int )
      elif self.char() in "=,+-":
        token = Token( self.char() )
        self.tick()
      else:
        raise "Unexpected character!"

    # Return the token.
    return token

if __name__ == "__main__":
  scanner = Scanner( "prime.mini" )
  token = scanner.next()
  while token.kind != "eof":
    print token
    token = scanner.next()
