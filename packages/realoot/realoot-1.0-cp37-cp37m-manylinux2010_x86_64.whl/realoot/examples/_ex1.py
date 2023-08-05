# This example describes how to manually set the transfer problem
from realoot.main import LtProblemContext, LtProblemDefinition, LtProblemSolution, SpacecraftData, ThrusterData, State, TerminalConstraintType
from realoot.main import solve
import realoot.main as constants

def run_example1():
    #import matplotlib.pyplot as plt

    problemContext = LtProblemContext()
    problemContext.performOptimisation = True
    problemContext.setInitialGuess(0.584294, -0.007173, -0.004140, 0, 0,-0.063167, 0.1)
    problemContext.initguess_duration = 0.06
    problemContext.verbose = True
    problemContext.rtol=1e-8
    problemContext.max_iter=100
    problemContext.verbose=2
    problemContext.reportFilename="ex1_report.xml"
    problemContext.initGuessMultiStart = True
    problemContext.initGuessMultiStartMaxAttempts = 5
    
    problemDefinition = LtProblemDefinition()
    problemDefinition.mu = 3.9860064e+14
    problemDefinition.cj2 = 0.00108263
    problemDefinition.radius = 6378136.
    problemDefinition.constraintType = TerminalConstraintType.C_SMA_ECC_INC
    problemDefinition.spacecraft = SpacecraftData("SC", ThrusterData(0.012, 9.80665 * 1200), 150)

    problemDefinition.state0 = State()
    problemDefinition.state0.setSma(6378136 + 500 * 1e3);
    problemDefinition.state0.setInclination(78 * constants.DEG2RAD);
    problemDefinition.state0.setEccentricity(0.001);
    problemDefinition.state0.setArgumentOfPericenter(90 * constants.DEG2RAD);
    problemDefinition.state0.setRightAscensionOfAscendingNode(0);
    problemDefinition.state0.setMass(150);

    # FIXME: RAAN and AoP are not updated with epoch
    problemDefinition.statef = State()
    problemDefinition.statef.setSma(6378136 + 1200 * 1e3);
    problemDefinition.statef.setInclination(78 * constants.DEG2RAD);
    problemDefinition.statef.setEccentricity(0.0012);
    problemDefinition.statef.setArgumentOfPericenter(90 * constants.DEG2RAD);
    problemDefinition.statef.setRightAscensionOfAscendingNode(0);

    problemSolution = LtProblemSolution()

    solve(problemDefinition, problemContext, problemSolution, True)
    print("dV=", problemSolution.dvcost)
    print("duration=", problemSolution.duration)
    print("nb revolutions=", problemSolution.nbRevolutions)

if __name__ == "__main__":
	run_example1()
