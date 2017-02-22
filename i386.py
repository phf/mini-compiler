# $Id: i386.py 655 2005-05-11 07:10:45Z phf $
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
  Code generator for Intel 80386 and better.

  TODO
  """

  def __init__( self, name ):
    # name of output file
    self.name = name
    # counter for generating labels
    self.labels = -1
    # buffer for data segment (variables)
    self.data = B.Buffer( ":",  "#" )
    # buffer for text segment (code)
    self.text = B.Buffer( ":",  "#" )

  def format( self, op="", operands="", comment="" ):
    self.text.append( "", op, operands, comment )

  def declare( self, name ):
    self.data.append( "V%s" % name, ".long", "0" )

  def next( self ):
    self.labels += 1
    return self.labels

  def label( self, label ):
    self.text.append( "L%s" % label )

  def load( self, name ):
    self.format( "movl", "V%s, %%eax" % name, "load from variable" )

  def store( self, name ):
    self.format( "movl", "%%eax, V%s" % name, "store into variable" )

  def constant( self, value ):
    self.format( "movl", "$%d, %%eax" % value, "load constant" )

  def move( self ):
    self.format( "movl", "%eax, %ebx", "copy" )

  def add( self ):
    self.format( "addl", "%ebx, %eax", "add" )

  def negate( self ):
    self.format( "negl", "%eax", "negate" )

  def test( self ):
    self.format( "cmpl", "$0, %eax", "test" )

  def branch( self, label ):
    self.format( "jle", "L%s" % label, "branch if <= 0" )

  def jump( self, label ):
    self.format( "jmp", "L%s" % label, "branch always" )

  def write( self ):
    self.format( "call", "puti", "write integer" )
    self.format( "call", "putn", "write newline" )

  def commit( self ):
    src = B.Buffer( ":",  "#" )
    src.format( ".data", "", "?" )
    # largest integer is 4294967296 (10 digits)
    src.append( "iostr", ".space", "16,0", "16 byte string buffer" )
    src.append( "iochr", ".byte", "0,0", "2 byte char buffer" )
    src.append( "ionew", ".byte", "10,0", "2 byte newline buffer" )
    #
    self.data.freeze()
    src.insert( self.data )
    #
    src.format( ".text", "", "?" )
    src.format( ".global", "_start", "?" )
    #
    src.label( "putn" )
    src.format( "pushl", "%eax", "save accumulator" ) # needed?
    src.format( "movl", "$1, %edx", "string length" )
    src.format( "movl", "$ionew, %ecx", "string buffer" )
    src.format( "movl", "$1, %ebx", "stdout" )
    src.format( "movl", "$4, %eax", "sys_write" )
    src.format( "int", "$0x80", "system call" )
    src.format( "popl", "%eax", "restore accumulator" ) # needed?
    src.format( "ret", "", "return" )
    #
    src.label( "putc" )
    src.format( "pushl", "%eax", "?" )
    src.format( "pushl", "%ebx", "?" )
    src.format( "pushl", "%ecx", "?" )
    src.format( "pushl", "%edx", "?" )
    src.format( "movl", "$iochr, %ecx", "string buffer" )
    src.format( "mov", "%al, 0(%ecx)", "set character" )
    src.format( "movl", "$1, %edx", "string length" )
    src.format( "movl", "$1, %ebx", "stdout" )
    src.format( "movl", "$4, %eax", "sys_write" )
    src.format( "int", "$0x80", "system call" )
    src.format( "popl", "%edx", "?" )
    src.format( "popl", "%ecx", "?" )
    src.format( "popl", "%ebx", "?" )
    src.format( "popl", "%eax", "?" )
    src.format( "ret", "", "return" )
    #
    src.label( "puti" )
    src.format( "pushl", "%eax", "?" )
    src.format( "pushl", "%ebx", "?" )

    # had to use ecx since edx collides with div instruction, argh
    src.format( "cmpl", "$0, %eax", "less than 0?" )
    src.format( "jge", "pi_nonneg", "no! skip ahead" )
    src.format( "movl", "%eax, %ecx", "save number to ecx" )
    src.format( "movl", "'-', %eax", "put - into parameter" )
    src.format( "call", "putc", "write - sign" )
    src.format( "negl", "%ecx", "negate number" )
    src.format( "movl", "%ecx, %eax", "restore number from ecx" )

    src.label( "pi_nonneg" )
    src.format( "movl", "$iostr, %ebx", "load buffer pointer" )
    src.format( "movl", "$10, %ecx", "load divisor 10" )

    src.label( "pi_fill" )
    src.format( "xorl", "%edx, %edx", "clear edx" )
    src.format( "div", "%ecx", "divide by 10, eax=quotient, edx=remainder" )
    src.format( "addl", "$0x30, %edx", "convert remainder to ASCII" )
    src.format( "mov", "%dl, 0(%ebx)", "store in buffer" )
    src.format( "addl", "$1, %ebx", "increment buffer pointer" )
    src.format( "cmpl", "$0, %eax", "zero already?" )
    src.format( "jne", "pi_fill", "no! another round!" )

    src.label( "pi_put" )
    src.format( "subl", "$1, %ebx", "decrement buffer pointer" )
    src.format( "xorl", "%eax, %eax", "clear eax" ) # needed?
    src.format( "mov", "0(%ebx), %al", "load from buffer" )
    src.format( "call", "putc", "write character" )
    src.format( "cmpl", "$iostr, %ebx", "first character?" )
    src.format( "jne", "pi_put", "no! another round!" )

    src.format( "popl", "%ebx", "?" )
    src.format( "popl", "%eax", "?" )
    src.format( "ret", "", "return" )
    #
    # code for Mini program
    #
    src.label( "_start" )
    #
    self.text.freeze()
    src.insert( self.text )
    #
    src.format( "movl", "$0, %ebx", "exit code" )
    src.format( "movl", "$1, %eax", "sys_exit" )
    src.format( "int", "$0x80", "system call" )
    #
    src.freeze()

    file = open( self.name, "w" )
    file.write( src.content() )
    file.close()

    return src.content()

if __name__ == "__main__":
  generator = Generator( "ttt.s" )
  print generator.commit()

