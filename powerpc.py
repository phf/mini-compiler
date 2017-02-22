# $Id: powerpc.py 655 2005-05-11 07:10:45Z phf $
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
  Code generator for PowerPC and Mac OS X.

  TODO
  """

  def __init__( self, name ):
    # name of output file
    self.name = name
    # counter for generating labels
    self.labels = -1
    # counter for generating variables
    self.vars = 0
    # buffer for data segment (variables)
    self.data = B.Buffer( ":", ";" )
    # buffer for text segment (code)
    self.text = B.Buffer( ":", ";" )

  def format( self, op="", operands="", comment="" ):
    self.text.append( "", op, operands, comment )

  def declare( self, name ):
    self.data.append( "", ".set", "V%s, %d" % (name, self.vars*4) )
    self.vars += 1

  def next( self ):
    self.labels += 1
    return self.labels

  def label( self, label ):
    self.text.append( "L%s" % label )

  def load( self, name ):
    self.format( "lwz", "r14, V%s(r13)" % name, "load from variable" )

  def store( self, name ):
    self.format( "stw", "r14, V%s(r13)" % name, "store into variable" )

  def constant( self, value ):
    if -32768 <= value <= 32767:
      # 16 bit or less, one instruction needed
      self.format( "li", "r14, %s" % value )
    else:
      # more than 16 bit, two instructions needed
      self.format( "addis", "r14, 0, hi16(%s)" % value )
      self.format( "ori", "r14, r14, lo16(%s)" % value )

  def move( self ):
    self.format( "addi", "r15, r14, 0", "copy" )

  def add( self ):
    self.format( "add", "r14, r14, r15", "add" )

  def negate( self ):
    self.format( "neg", "r14, r14", "negate" )

  def test( self ):
    self.format( "cmpi", "cr0, r14, 0", "test" )

  def branch( self, label ):
    self.format( "ble", "cr0, L%s" % label, "branch if <= 0" )

  def jump( self, label ):
    self.format( "b", "L%s" % label, "branch always" )

  def write( self ):
    self.format( "addi", "r3, r14, 0", "set up parameter" )
    self.format( "bl", "puti", "write integer" )
    self.format( "bl", "putn", "write newline" )

  def commit( self ):
    src = B.Buffer( ":", ";" )
    #
    src.format( ".data" )
    src.label( "vars" )
    src.format( ".space", "%s, 0" % (self.vars*4) )
    # largest integer is 4294967296 (10 digits)
    src.append( "iostr", ".space", "16,0", "16 byte string buffer" )
    src.append( "iochr", ".byte", "0,0", "2 byte char buffer" )
    src.append( "ionew", ".byte", "10,0", "2 byte newline buffer" )
    # TODO: split into constants and variables?
    self.data.freeze()
    src.insert( self.data )
    #
    src.append( "", ".text" )
    src.append( "", ".globl", "_main" )
    #####
    src.label( "putn" )
    #
    src.format( "mflr", "r0", "get link register" )
    src.format( "addi", "r1, r1, -4", "adjust stack" )
    src.format( "stw", "r0, 0(r1)", "save link register" )
    #
    src.format( "li", "r0, 4", "write() call" )
    src.format( "li", "r3, 1", "stdout" )
    src.format( "addis", "r4, 0, hi16(ionew)", "high address of buffer" )
    src.format( "ori", "r4, r4, lo16(ionew)", "low address of buffer" )
    src.format( "li", "r5, 1", "length" )
    src.format( "sc", "", "syscall" )
    src.format( "nop" )
    src.format( "nop" )
    #
    src.format( "lwz", "r0, 0(r1)", "restore link register" )
    src.format( "addi", "r1, r1, 4", "adjust stack" )
    src.format( "mtlr", "r0", "set link register" )
    src.format( "blr" )
    #####
    src.append( "putc", "", "", "character = r3" )
    #
    src.format( "mflr", "r0", "get link register" )
    src.format( "addi", "r1, r1, -8", "adjust stack" )
    src.format( "stw", "r0, 0(r1)", "save link register" )
    src.format( "stw", "r5, 4(r1)", "save r5 for puti" )
    #
    src.format( "addis", "r4, 0, hi16(iochr)", "high address of buffer" )
    src.format( "ori", "r4, r4, lo16(iochr)", "low address of buffer" )
    #
    src.format( "stb", "r3, 0(r4)", "store character" )
    #
    src.format( "li", "r0, 4", "write() call" )
    src.format( "li", "r3, 1", "stdout" )
    src.format( "li", "r5, 1", "length" )
    src.format( "sc", "", "syscall" )
    src.format( "nop" )
    src.format( "nop" )
    #
    src.format( "lwz", "r5, 4(r1)", "restore r5 for puti" )
    src.format( "lwz", "r0, 0(r1)", "restore link register" )
    src.format( "addi", "r1, r1, 8", "adjust stack" )
    src.format( "mtlr", "r0", "set link register" )
    src.format( "blr" )
    #####
    src.append( "puti", "", "", "integer = r3" )
    #
    src.format( "mflr", "r0", "get link register" )
    src.format( "addi", "r1, r1, -4", "adjust stack" )
    src.format( "stw", "r0, 0(r1)", "save link register" )
    #
    src.format( "cmpi", "cr2, r3, 0", "negative? note use of cr2!" )
    src.format( "bge", "cr2, pi_notneg", "skip negation" )
    src.format( "neg", "r3, r3", "negate" )
    src.label( "pi_notneg" )
    src.format( "li", "r5, 0", "?" )
    src.format( "addis", "r7, 0, hi16(iostr)", "?" )
    src.format( "ori", "r7, r7, lo16(iostr)", "?" )
    #
    src.format( "li", "r0, 10", "?" )
    src.label( "pi_loop" )
    src.format( "divwu", "r2, r3, r0", "r2 = quotient" )
    src.format( "mullw", "r4, r2, r0", "r4 = remainder (step 1)" )
    src.format( "subf", "r4, r4, r3", "r4 = remainder (step 2)" )
    #
    src.format( "addi", "r4, r4, 0x30", "convert to ASCII" )
    src.format( "stb", "r4, 0(r7)", "store character" )
    src.format( "addi", "r7, r7, 1", "?" )
    src.format( "addi", "r5, r5, 1", "?" )
    #
    src.format( "addi", "r3, r2, 0", "copy quotient to r3" )
    src.format( "cmpi", "cr0, r3, 0", "test" )
    src.format( "bne", "cr0, pi_loop", "?" )
    #
    src.format( "bge", "cr2, pi_skip", "skip - sign" )
    src.format( "li", "r3, 45", "set up parameter '-'" )
    src.format( "bl", "putc", "write character" )
    #
    src.label( "pi_skip" )
    src.format( "addi", "r7, r7, -1", "?" )
    src.format( "lbz", "r3, 0(r7)", "?" )
    src.format( "bl", "putc", "write character" )
    src.format( "addi", "r5, r5, -1", "?" )
    src.format( "cmpi", "cr0, r5, 0", "test" )
    src.format( "bne", "cr0, pi_skip", "?" )
    #
    src.format( "lwz", "r0, 0(r1)", "restore link register" )
    src.format( "addi", "r1, r1, 4", "adjust stack" )
    src.format( "mtlr", "r0", "set link register" )
    src.format( "blr" )
    #
    # code for Mini program
    src.append( "_main" )
    #
    src.format( "mflr", "r0" )
    src.format( "addi", "r1, r1, -4" )
    src.format( "stw", "r0, 0(r1)" )
    #
    src.format( "addis", "r13, 0, hi16(vars)", "save base address of vars" )
    src.format( "ori", "r13, r13, lo16(vars)", "lo bits" )
    #
    self.text.freeze()
    src.insert( self.text )
    #
    src.label( "exit" )
    src.format( "lwz", "r0, 0(r1)", "restore saved r0" )
    src.format( "addi", "r1, r1, 4", "adjust stack" )
    src.format( "mtlr", "r0", "restore link register" )
    src.format( "li", "r3, 0", "set return code" )
    src.format( "blr", "", "branch back where we came from" )

    src.freeze()

    file = open( self.name, "w" )
    file.write( src.content() )
    file.close()

    return src.content()

if __name__ == "__main__":
  generator = Generator( "ttt.s" )
  print generator.commit()

