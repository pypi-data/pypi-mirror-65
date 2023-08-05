# This example illustrates the use of an input script file to configure the problem
import realoot.main as lt
import pkg_resources

def run_example2():
    resource_package = "realoot.examples"
    filename = pkg_resources.resource_filename(resource_package, "ex2.xml")
    problemDefinition, problemContext = lt.readXml(filename)	
    problemSolution = lt.LtProblemSolution()
    lt.solve(problemDefinition, problemContext, problemSolution, True)


if __name__ == "__main__":
    run_example2()