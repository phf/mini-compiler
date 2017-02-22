# $Id: mmix.py 655 2005-05-11 07:10:45Z phf $
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
  Code generator for Donald Knuth's MMIX.

  The conventions used by mmixal are *very* weird if you know
  only old-school assemblers. It took me quite a while to find
  out how to use those base registers: Simple declare them at
  certain spots where they can be used by mmixal to automatically
  set up the details. :-)

  Every program gets split into a bunch of segments now, each
  with it's own GREG directive for addressing. Eventually we
  may have to "regularly" emit GREG directives if the segments
  grow to large, but that's to be resolved still.

  The register stack took me a while to figure out as well, but
  it's a pretty nifty feature:

  You have N local registers $0..$N-1.
  You want to call a function that expects M parameters.
  Set aside $N (I guess that's the "hole" Knuth talks about?).
  Fill parameters into $N+1..$N+M.
  Do PUSHJ $N,function.
  Inside the function the old $N+1..$N+M will be $0..$M-1.
  """

  def __init__( self, name ):
    # name of output file
    self.name = name
    # counter for generating labels
    self.labels = -1
    # counter for generating constants
    self.consts = 0
    # pool of constants we created: value -> number of constant
    self.pool = {}
    # buffer for data segment (variables)
    self.data = B.Buffer( "",  "%" )
    # buffer for text segment (code)
    self.text = B.Buffer( "",  "%" )

  def format( self, op="", operands="", comment="" ):
    self.text.append( "", op, operands, comment )

  def declare( self, name ):
    self.data.append( "V%s" % name, "OCTA", "0" )

  def next( self ):
    self.labels += 1
    return self.labels

  def label( self, label ):
    self.text.append( "L%s" % label, "SWYM" )

  def load( self, name ):
    self.format( "LDO", "accu,V%s" % name, "load from variable" )

  def store( self, name ):
    self.format( "STO", "accu,V%s" % name, "store into variable" )

  def constant( self, value ):
    # needed since immediate mode is limited to 8-bit values on MMIX
    if value not in self.pool.keys():
      self.data.append( "C%s" % self.consts, "OCTA", "%d" % value )
      self.pool[value] = self.consts
      self.consts += 1
    self.format( "LDO", "accu,C%s" % self.pool[value], "load from constant" )

  def move( self ):
    self.format( "SET", "temp,accu", "copy" )

  def add( self ):
    self.format( "ADD", "accu,accu,temp", "add" )

  def negate( self ):
    self.format( "NEG", "accu,0,accu", "negate" )

  def test( self ):
    self.format( "CMP", "t,accu,0", "test" )

  def branch( self, label ):
    self.format( "BNP", "t,L%s" % label, "branch if <= 0" )

  def jump( self, label ):
    self.format( "JMP", "L%s" % label, "branch always" )

  def write( self ):
    self.format( "SET", "$5,accu", "set up parameter" )
    self.format( "PUSHJ", "$4,puti", "write integer" )
    self.format( "PUSHJ", "$4,putn", "write newline" )

  def commit( self ):
    src = B.Buffer( "",  "%" )
    # global definitions that are useful later...
    src.append( "t", "IS", "$255", "temporary register for MMIX" )
    src.append( "accu", "IS", "$3", "accumulator register" )
    src.append( "temp", "IS", "$2", "scratch register" )
    #
    src.append( "", "LOC", "Data_Segment", "data" )
    src.append( "", "GREG", "@", "implicit base register" )
    # largest integer is 18446744073709551616 (20 digits)
    src.append( "iostr", "OCTA", "0,0,0", "24 byte string buffer" )
    src.append( "iochr", "BYTE", "0,0", "2 byte char buffer" )
    src.append( "ionew", "BYTE", "10,0", "2 byte newline buffer" )
    # TODO: split into constants and variables?
    self.data.freeze()
    src.insert( self.data )
    # code for the IO functions
    src.append( "", "LOC", "#1000", "code for IO functions" )
    src.append( "", "GREG", "@", "implicit base register" )
    #
    src.append( "putn", "LDA", "t,ionew", "address of newline" )
    src.format( "TRAP", "0,Fputs,StdOut", "trap to puts" )
    src.format( "POP", "0,0", "return, no results" )
    #
    src.append( "putc", "STBU", "$0,iochr", "store char into buffer" )
    src.format( "LDA", "t,iochr", "address of buffer" )
    src.format( "TRAP", "0,Fputs,StdOut", "trap to puts" )
    src.format( "POP", "0,0", "return, no results" )
    #
    src.append( "puti", "ADDU", "$1,$0,0", "?" )
    src.format( "CMP", "$3,$0,0", "set $3 to -1/0/+1" )
    src.format( "BNN", "$3,0F", "skip negation" )
    src.format( "NEG", "$1,0,$1", "negate" )
    src.append( "0H", "GET", "$0,rJ", "?" )
    src.format( "SET", "$5,0", "?" )
    src.format( "LDA", "$7,iostr", "?" )
    src.append( "1H", "DIVU", "$1,$1,10", "?" )
    src.format( "GET", "$2,rR", "?" )
    src.format( "ADDU", "$2,$2,#30", "?" )
    src.format( "STBU", "$2,$7", "?" )
    src.format( "ADDU", "$7,$7,1", "?" )
    src.format( "ADDU", "$5,$5,1", "?" )
    src.format( "BNZ", "$1,1B", "?" )
    src.format( "BNN", "$3,2F", "skip - sign" )
    src.format( "SET", "$10,'-'", "put - sign into parameter" )
    src.format( "PUSHJ", "$9,putc", "print" )
    src.append( "2H", "SUBU", "$7,$7,1", "?" )
    src.format( "LDBU", "$10,$7", "?" )
    src.format( "PUSHJ", "$9,putc", "?" )
    src.format( "SUBU", "$5,$5,1", "?" )
    src.format( "BNZ", "$5,2B", "?" )
    src.format( "PUT", "rJ,$0", "?" )
    src.format( "POP", "0,0", "?" )
    # code for Mini program
    src.append( "", "LOC", "#2000", "code for Mini program" )
    src.append( "", "GREG", "@", "implicit base register" )
    src.append( "Main", "SWYM" )
    self.text.freeze()
    src.insert( self.text )
    src.append( "", "TRAP", "0,Halt,0" )

    src.freeze()

    file = open( self.name, "w" )
    file.write( src.content() )
    file.close()

    return src.content()

if __name__ == "__main__":
  generator = Generator( "ttt.s" )
  print generator.commit()

