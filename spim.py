# $Id: spim.py 654 2005-05-11 07:03:23Z phf $
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

import generator as G
import buffer as B

class Generator(G.Generator):
  """
  Code generator for MIPS as implemented by SPIM.

  TODO: Turning this into a native version, e.g. for NetBSD,
  should be straightforward. Only the stuff for PRINT would
  need some reworking.
  """

  def __init__( self, name ):
    # name of output file
    self.name = name
    # counter for generating labels
    self.counter = -1
    # buffer for data segment (variables)
    self.data = B.Buffer()
    # buffer for text segment (code)
    self.text = B.Buffer()

  def format( self, op="", operands="", comment="" ):
    self.text.append( "", op, operands, comment )

  def declare( self, name ):
    self.data.append( "V%s" % name, ".word", "0" )

  def next( self ):
    self.counter += 1
    return self.counter

  def label( self, label ):
    self.text.append( "L%s" % label )

  def load( self, name ):
    self.format( "lw", "$s0, V%s" % name, "load variable to $s0" )

  def store( self, name ):
    self.format( "sw", "$s0, V%s" % name, "store $s0 to variable" )

  def constant( self, value ):
    self.format( "li", "$s0, %d" % value, "load constant to $s0" )

  def move( self ):
    self.format( "move", "$s1, $s0", "copy $s0 to $s1" )

  def add( self ):
    self.format( "addu", "$s0, $s0, $s1", "add $s1 to $s0" )

  def negate( self ):
    self.format( "sub", "$s0, $0, $s0", "negate $s0" )

  def test( self ):
    # not necessary for MIPS
    pass

  def branch( self, label ):
    self.format( "blez", "$s0, L%s" % label, "branch if $s0 <= 0" )

  def jump( self, label ):
    self.format( "b", "L%s" % label, "branch always" )

  def write( self ):
    self.format( "li", "$v0, 1", "1 = write integer" )
    self.format( "move", "$a0, $s0", "copy value to $a0" )
    self.format( "syscall" )
    self.format( "li", "$v0, 4", "4 = write string" )
    self.format( "la", "$a0, crlf", "copy address to $a0" )
    self.format( "syscall" )

  def commit( self ):
    src = B.Buffer()
    src.append( "", ".data" )
    self.data.freeze()
    src.insert( self.data )
    src.append( "crlf", ".asciiz", "\"\\n\"" )
    src.append( "", ".text" )
    src.append( "", ".globl", "main" )
    src.append( "main" )
    self.text.freeze()
    src.insert( self.text )
    src.append( "", "jr", "$ra" )
    src.append( "", ".end" )
    src.freeze()

    file = open( self.name, "w" )
    file.write( src.content() )
    file.close()

    return src.content()

if __name__ == "__main__":
  generator = Generator( "ttt.s" )
  print generator.commit()

