###########################################################
# We check what extensions are available
###########################################################
__extensions__ = {'matplotlib': False, 'mplot3d': False, 'xerces' : False}
# matplotlib
try:
    from matplotlib import __version__ as matplotlib_ver
    __extensions__['matplotlib'] = True

    # We detect the version and if more than 1.1.0 mplot3d is there
    mver = matplotlib_ver.split('.')
    mver = int(mver[0]) * 100 + int(mver[1]) * 10
    if mver >= 110:
        __extensions__['mplot3d'] = True
    del mver
except ImportError:
    pass

__extensions__['xerces'] = True

###########################################################
# Import the modules
###########################################################

from . import utils, main
from . import examples

###########################################################
# Define ltavgopt package
###########################################################
version = '1.0'
__doc__ = 'Solve the averaged low-thrust optimal control transfer problem'
__all__ = ['utils', 'main', 'examples']
__version__ = {'major': int(version.split('.')[0]), 'minor': int(version.split('.')[1])}
__all__ += [name for name in dir(main) if not name.startswith('_')]
__all__ += [name for name in dir(utils) if not name.startswith('_')]
__all__ += [name for name in dir(examples) if not name.startswith('_')]
