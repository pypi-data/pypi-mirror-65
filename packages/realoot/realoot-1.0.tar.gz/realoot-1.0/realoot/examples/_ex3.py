# This example computes transfer on a grid of orbits.
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import realoot as lt
from realoot.utils import deg2rad
import numpy as np
from numpy import asarray
from numpy import savez

def run_example3():	
    problemContext = LtProblemContext()
    problemContext.performOptimisation = True
    problemContext.setInitialGuess(0.584294, -0.007173, -0.004140, 0, 0,-0.063167, 0.1)
    problemContext.initguess_duration = 0.06
    problemContext.verbose = True
    problemContext.rtol=1e-8
    problemContext.max_iter=100
    problemContext.verbose=0
    problemContext.reportFilename=""    
    problemContext.initGuessMultiStart = False
    problemContext.initGuessMultiStartMaxAttempts = 0

    problemDefinition = LtProblemDefinition()
    problemDefinition.mu = 3.9860064e+14
    problemDefinition.cj2 = 0.00108263
    problemDefinition.radius = 6378136.
    problemDefinition.constraintType = TerminalConstraintType.C_SMA_ECC_INC
    problemDefinition.spacecraft = SpacecraftData("SC", ThrusterData(0.012, 9.80665 * 1200), 150)
	
    problemDefinition.state0 = State()
    problemDefinition.state0.setSma(6378136 + 500 * 1e3);
    problemDefinition.state0.setInclination(deg2rad(77.5));
    problemDefinition.state0.setEccentricity(0.001);
    problemDefinition.state0.setArgumentOfPericenter(deg2rad(90));
    problemDefinition.state0.setRightAscensionOfAscendingNode(0);
    problemDefinition.state0.setMass(150);

    # FIXME: RAAN and AoP are not updated with epoch
    problemDefinition.statef = State()
    problemDefinition.statef.setSma(6378136 + 1200 * 1e3);
    problemDefinition.statef.setInclination(deg2rad(78));
    problemDefinition.statef.setEccentricity(0.0012);
    problemDefinition.statef.setArgumentOfPericenter(deg2rad(90));
    problemDefinition.statef.setRightAscensionOfAscendingNode(0);

    problemSolution = LtProblemSolution()

    sma_0_grid = np.arange(500, 1000, 5)
    sma_f_grid = np.arange(500, 1000, 5)
    grid_v = [[0 for _ in sma_f_grid] for _ in sma_0_grid]
    grid_t = [[0 for _ in sma_f_grid] for _ in sma_0_grid]
    i = 0
    ncv = 0
    for sma_0 in sma_0_grid:
        problemDefinition.state0.setSma(6378136 + sma_0 * 1e3);
        j = 0
        for sma_f in sma_f_grid:
            problemDefinition.statef.setSma(6378136 + sma_f * 1e3);
            res = lt.solve(problemDefinition, problemContext, problemSolution, False)
            if res == 0:
                grid_v[i][j] = problemSolution.dvcost
                grid_t[i][j] = problemSolution.duration
            else:
                #grid_v[i][j] = np.nan
                #grid_t[i][j] = np.nan
                ncv = ncv + 1

            #problemContext.setInitialGuess(problemSolution.initguess)
            problemContext.initguess_duration = problemSolution.initguess_duration

            j = j + 1
        i = i + 1

    print('Convergence ratio: ', 100 * (1 - ncv / len(sma_f_grid) / len(sma_0_grid)))

    # save numpy array as npy file
    grid_v = asarray(grid_v)
    grid_t = asarray(grid_t)
    savez('data_out.npy', x=asarray(sma_0_grid), y=asarray(sma_f_grid), v=asarray(grid_v), t=asarray(grid_t))

    X, Y = np.meshgrid(sma_0_grid, sma_f_grid)
    
    # plot transfer duration and transfer cost 
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    surf = ax.plot_surface(X, Y, grid_v, cmap='winter')
    ax.grid(c='k', ls='-', alpha=0.3)
    plt.xlabel("sma_0, km")
    plt.ylabel("sma_f, km")    
    ax.set_zlabel("transfer cost, m/s")  
    plt.title("Transfer costs in minimum time")
    fig.colorbar(surf)
    plt.savefig('ex3_surf_dv.png', dpi=240, format='png', bbox_inches='tight')
        
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    surf = ax.plot_surface(X, Y, grid_t, cmap='winter')
    ax.grid(c='k', ls='-', alpha=0.3)
    plt.xlabel("sma_0, km")
    plt.ylabel("sma_f, km")    
    ax.set_zlabel("transfer duration, day") 
    plt.title("Transfer durations in minimum time")
    fig.colorbar(surf)

    plt.savefig('ex3_surf_dt.png', dpi=240, format='png', bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    run_example3()


