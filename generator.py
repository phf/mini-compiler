# $Id: generator.py 654 2005-05-11 07:03:23Z phf $
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

import version as V

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

