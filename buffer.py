# $Id: buffer.py 606 2005-05-02 07:36:56Z phf $

class Buffer:
  """
  An output buffer for assembly-like text.

  This class encapsulates some ugly and volatile formatting code
  that I just can't get a good handle on. Maybe the code has to
  be ugly to produce a nice format? Any hints on improving this
  would be *very* welcome.
  """

  def __init__( self, label=":", comment="#" ):
    """
    Create a new buffer.

    Buffers start out empty and mutable.
    """
    self._frozen = False
    self._buffer = ""
    self._label = label
    self._comment = comment

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
      format = "%-8s %-8s %-20s %s\n"
    elif len( operands ) > 0:
      format = "%-8s %-8s %s%s\n"
    elif len( operator ) > 0:
      format = "%-8s %s%s%s\n"
    elif len( label ) > 0:
      format = "%s%s%s%s\n"
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
  b = Buffer( "", ";" )
  b.append( "one", "two", "three", "infinity" )
  b.append( "", "two", "three", "infinity" )
  b.append( "", "two", "three", "" )
  b.append( "", "two", "", "" )
  b.append( "one", "", "", "" )
  b.freeze()
  print b.content()

