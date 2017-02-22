# $Id: lc3.py 622 2005-05-06 00:30:26Z phf $

import generator as G
import buffer as B
import version as V

class Generator(G.Generator):
  """
  Code generator for LC-3.

  TODO: Numbers greater than 16 bit are silently accepted,
  even by the lc3as assembler. Go figure. That's why some
  of the examples don't work right.
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
    self.data = B.Buffer( ":",  ";" )
    # buffer for text segment (code)
    self.text = B.Buffer( ":",  ";" )

  def format( self, op="", operands="", comment="" ):
    self.text.append( "", op, operands, comment )

  def declare( self, name ):
    self.data.append( "V%s" % name, ".FILL", "0" )

  def next( self ):
    self.labels += 1
    return self.labels

  def label( self, label ):
    self.text.append( "L%s" % label )

  def load( self, name ):
    self.format( "LD", "R0, V%s" % name, "load variable to R0" )

  def store( self, name ):
    self.format( "ST", "R0, V%s" % name, "store R0 to variable" )

  def constant( self, value ):
    # needed since there's no immediate mode for load on the LC-3
    if value not in self.pool.keys():
      self.data.append( "C%s" % self.consts, ".FILL", "%d" % value )
      self.pool[value] = self.consts
      self.consts += 1
    self.format( "LD", "R0, C%s" % self.pool[value], "load constant to R0" )

  def move( self ):
    self.format( "ADD", "R1, R0, 0", "copy R0 to R1" )

  def add( self ):
    self.format( "ADD", "R0, R0, R1", "add R1 to R0" )

  def negate( self ):
    self.format( "NOT", "R0, R0", "negate R0 (step 1)" )
    self.format( "ADD", "R0, R0, 1", "negate R0 (step 2)" )

  def test( self ):
    # not necessary for LC-3? seems that even LD sets condition codes...
    pass

  def branch( self, label ):
    self.format( "BRnz", "L%s" % label, "branch if R0 <= 0" )

  def jump( self, label ):
    self.format( "BR", "L%s" % label, "branch always" )

  def write( self ):
    self.format( "TRAP", "xFC", "write integer in R0" )

  def commit( self ):
    src = B.Buffer( ":",  ";" )
    src.append( "", ".ORIG", "x3000" )
    self.text.freeze()
    src.insert( self.text )
    src.append( "", "HALT" )
    self.data.freeze()
    src.insert( self.data )
    src.append( "", ".END" )
    src.freeze()

    file = open( self.name, "w" )
    file.write( src.content() )
    file.close()

    return src.content()

if __name__ == "__main__":
  generator = Generator( "ttt.s" )
  print generator.commit()

