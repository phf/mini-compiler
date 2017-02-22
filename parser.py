# $Id: parser.py 654 2005-05-11 07:03:23Z phf $
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

class Parser:
  """
  TODO
  """

  def __init__( self, scanner, generator ):
    self.lex = scanner
    self.obj = generator
    self.next()

  def next( self ):
    self.tok = self.lex.next()

  def match( self, kind ):
    if self.tok.kind == kind:
      t = self.tok
      self.next()
      return t
    else:
      raise "Expected %s but got %s!" % (kind, self.tok)

  def Program( self ):
    self.match( "PROGRAM" )
    if self.tok.kind == "VAR":
      self.VarDeclaration()
    self.match( "BEGIN" )
    while self.tok.kind != "END":
      self.Statement()
    self.match( "END" )
    # original compiler allows junk, we don't... :-/
    self.match( "eof" )

  def VarDeclaration( self ):
    self.next()
    t = self.match( "identifier" )
    self.obj.declare( t.value )
    while self.tok.kind == ",":
      self.match( "," )
      t = self.match( "identifier" )
      self.obj.declare( t.value )

  def Statement( self ):
    if self.tok.kind == "identifier":
      name = self.tok.value
      self.next()
      self.match( "=" )
      self.Expression()
      self.obj.store( name )
    elif self.tok.kind == "WHILE":
      self.next()
      start = self.obj.next()
      end = self.obj.next()
      self.obj.label( start )
      self.Expression()
      self.match( "DO" )
      self.obj.test()
      self.obj.branch( end )
      while self.tok.kind != "END":
        self.Statement()
      self.match( "END" )
      self.obj.jump( start )
      self.obj.label( end )
    elif self.tok.kind == "PRINT":
      self.next()
      self.Expression()
      self.obj.write()
    else:
      raise "Statement expected!"

  def Expression( self ):
    neg = False
    if self.tok.kind in ["+", "-"]:
      neg = self.tok.kind == "-"
      self.next()
    self.Factor()
    if neg:
      self.obj.negate()
    while self.tok.kind in ["+", "-"]:
      neg = self.tok.kind == "-"
      self.next()
      self.obj.move()
      self.Factor()
      if neg:
        self.obj.negate()
      self.obj.add()

  def Factor( self ):
    if self.tok.kind == "identifier":
      self.obj.load( self.tok.value )
      self.next()
    elif self.tok.kind == "constant":
      self.obj.constant( self.tok.value )
      self.next()
    else:
      raise "Factor expected!"

if __name__ == "__main__":
  import scanner as S
  import generator as G
  scanner = S.Scanner( "4711.mini" )
  generator = G.Generator( "4711.s" )
  parser = Parser( scanner, generator )
  parser.Program()
  generator.commit()
  print generator.src

