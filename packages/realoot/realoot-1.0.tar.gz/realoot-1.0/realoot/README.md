README
=========

## Preambule

The application solves the averaged optimal minimum time orbit transfer problem. It is initially inspired by [MIPELEC] that uses the averaged optimal control formulation.
This application however includes important upgrade, such as:
  * different terminal conditions
  * inclusion of zonal gravitational field perturbation to model secular evolution of node and apoapsis lines, around an oblate body.  

IMPORTANT WARNINGS
1. The optimal control is the solution of the averaged optimal control problem. 
	* It cannot be used as such for high fidelity propagation, 
	* It cannot currently be used for rendezvous problems (e.g. interplanetary)
2. The solution starts diverging from the non-averaged optimal control problem solution for very large thrust accelerations.


## Running under python

### Installation from repository
`pip install realoot`

The module works with Python 3.

### Installation from sources 
Please follow the instructions in COMPILE.


### Example Usage
Import
```
	import realoot.main as lt
```

Then either, as for the application, open a script file with
```
	problemDefinition, problemContext = lt.readXml("examples/ex2.xml")
	lt.solve(problemDefinition, problemContext, problemSolution, True)
```
	
Or define manually your problem filling the structure
```
	problemContext = lt.LtProblemContext()
	problemDefinition = lt.LtProblemDefinition()
```
Then call
```
	lt.solve(problemDefinition, problemContext, problemSolution, True)
```

Please see the examples for details.

You will need `matplotlib` to run the examples.


	
## Credits
  * [MIPELEC]: (https://logiciels.cnes.fr/fr/content/mipelec)
  * [An averaging optimal control tool for low thrust minimum-time transfers](https://logiciels.cnes.fr/sites/default/files/attached_doc/An%20averaging%20optimal%20control%20tool%20for%20low%20thrust%20minimum-time%20transfers.pdf)
  
  
