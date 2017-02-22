# $Id: spim.py 528 2005-04-23 03:42:20Z phf $

class Generator:
  """
  Interface for code generators.
  """

  def __init__( self, name ):
    """Create a code generator."""
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

