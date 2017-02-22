# $Id: buffer.py 634 2005-05-10 05:39:56Z phf $
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

class Buffer:
  """
  An output buffer for assembly-like text.

  This class encapsulates some ugly and volatile formatting code
  that I just can't get a good handle on. Maybe the code has to
  be ugly to produce a nice format? Any hints on improving this
  would be *very* welcome.
  """

  def __init__( self, label=":", comment="#", newline="\n" ):
    """
    Create a new buffer.

    The character labels must end with is "label", the character
    comments must start with is "comment", and the character to
    create a new line in the output is "newline".

    TODO: There a probably many more useful configuration options
    that are currently hard-coded. Mea culpa. :-)

    Buffers start out empty and mutable.
    """
    self._frozen = False
    self._buffer = ""
    self._label = label
    self._comment = comment
    self._newline = newline

  def empty( self ):
    """
    Is this buffer empty?
    """
    return len( self._buffer ) > 0

  def frozen( self ):
    """
    Is this buffer frozen (i.e. *not* mutable)?
    """
    return self._frozen

  def insert( self, other ):
    """
    Insert another buffer.

    Insert is only possible for mutable buffers; the other buffer
    must be frozen (i.e. *not* mutable).
    """
    assert not self._frozen
    assert other._frozen
    self._buffer += other._buffer

  def append( self, label="", operator="", operands="", comment="" ):
    """
    Append a line of output.

    Appending is only possible for mutable buffers.
    """
    assert not self._frozen

    # complete fields if necessary
    if len( comment ) > 0:
      comment = self._comment + " " + comment
    if len( label ) > 0:
      label += self._label

    # determine proper format string
    if len( comment ) > 0:
      format = "%-8s %-8s %-20s %s" + self._newline
    elif len( operands ) > 0:
      format = "%-8s %-8s %s%s" + self._newline
    elif len( operator ) > 0:
      format = "%-8s %s%s%s" + self._newline
    elif len( label ) > 0:
      format = "%s%s%s%s" + self._newline
    else:
      raise "Empty lines can't be appended!"

    line = format % (label, operator, operands, comment)
    self._buffer += line
    return line

  def label( self, label ):
    """
    Append a label.

    Convenience function calling append() in turn.
    """
    self.append( label )

  def format( self, operator, operand="", comment="" ):
    """
    Append an instruction.

    Convenience function calling append() in turn.
    """
    self.append( "", operator, operand, comment )

  def comment( self, comment="" ):
    """
    Append a comment by itself, taking up the whole line.

    Convenience function.
    """
    self._buffer += self._comment + " " + comment + self._newline

  def freeze( self ):
    """
    Freeze this buffer.
    """
    assert not self._frozen
    self._frozen = True

  def content( self ):
    """
    Get the contents of this buffer.

    Content is only accessible for frozen buffers.   
    """
    assert self._frozen
    return self._buffer

if __name__ == "__main__":
  b = Buffer( "$", ";", "\r\n" )
  b.append( "one", "two", "three", "infinity" )
  b.append( "", "two", "three", "infinity" )
  b.label( "label" )
  b.append( "", "two", "three", "" )
  b.comment( "Hmmm, how did I get here?" )
  b.append( "", "two", "", "" )
  b.format( "inst", "oper", "comm" )
  b.append( "one", "", "", "" )
  b.freeze()
  print b.content()

