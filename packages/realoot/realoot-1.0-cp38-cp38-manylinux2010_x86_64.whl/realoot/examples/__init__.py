"""
Set of examples.
 - (1) example with problem described in Python.
 - (2) example with problem described with an input file.
 - (3) example performing batch computations.


To run an example:
realoot.examples.run_example1()

"""
from realoot import __extensions__

# Basic example 
from ._ex1 import run_example1

# example 2 read an XML file. Xerces is required.
if __extensions__['xerces']:
	from ._ex2 import run_example2

#
if __extensions__['matplotlib']:
	from ._ex3 import run_example3
