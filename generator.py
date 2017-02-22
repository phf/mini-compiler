# $Id: generator.py 622 2005-05-06 00:30:26Z phf $

class Generator:
  """
  Interface for code generators.

  The central idea for our code generators is to use
  an accumulator (register) and a scratch (register)
  to perform all arithmetic. It helps that Mini only
  supports "+" and "-": We don't have to worry about
  precedence at all. It also helps that we write out
  assembly source, not object files. In fact most of
  Mini's error handling is "outsourced" this way.

  The methods below generate code that performs the
  following operations:

    load:     A = variable
    store:    variable = A
    constant: A = natural number

    move:     S = A
    add:      A = A + S
    negate:   A = -A

    test:
    branch:
    jump:

    declare:
    next:
    label:

    write:    print A

    commit:

  Here "A" is the accumulator and "S" is the scratch.
  """

  def __init__( self, name ):
    """Create a code generator writing to file name."""
    pass

  def declare( self, name ):
    """Declare a variable."""
    pass

  def next( self ):
    """Get next label number."""
    pass

  def label( self, label ):
    """Emit a label."""
    pass

  def load( self, name ):
    """Load a variable into accumulator."""
    pass

  def store( self, name ):
    """Store accumulator to a variable."""
    pass

  def constant( self, value ):
    """Load a constant into accumulator."""
    pass

  def move( self ):
    """Copy accumulator to scratch."""
    pass

  def add( self ):
    """Add scratch to accumulator."""
    pass

  def negate( self ):
    """Negate accumulator."""
    pass

  def test( self ):
    """Test accumulator for 0."""
    pass

  def branch( self, label ):
    """Branch if accumulator <= 0."""
    pass

  def jump( self, label ):
    """Branch always."""
    pass

  def write( self ):
    """Print accumulator."""
    pass

  def commit( self ):
    """Done with code generation."""
    pass

