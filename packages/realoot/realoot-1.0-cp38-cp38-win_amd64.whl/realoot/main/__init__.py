# We import all symbols in the core namespace (also the ones we do not use
# in this file, but we still want in the namespace core)

from ._main import solve, propagate, readXml
from ._main import LtProblemContext, LtProblemDefinition, LtProblemSolution
from ._main import State, SpacecraftData, ThrusterData
from ._main import TerminalConstraintType, OrbitRepresentation


# We import the protected symbols we use in this file
from ._constants import *
from ._constants import _get_AU, _get_DAY2SEC, _get_DAY2YEAR, _get_DEG2RAD, _get_EARTH_J2, _get_EARTH_RADIUS, _get_EARTH_MU, _get_G0, _get_SUN_MU, _get_RAD2DEG, _get_SEC2DAY

# We import all symbols in the core namespace (also the ones we do not use
# in this file, but we still want in the namespace core)


"""Constants defined in SpaceMechanicsConstants.hpp"""
AU = _get_AU()
DAY2SEC = _get_DAY2SEC()
DAY2YEAR = _get_DAY2YEAR()
DEG2RAD = _get_DEG2RAD()
RAD2DEG = _get_RAD2DEG()
SEC2DAY = _get_SEC2DAY()

EARTH_J2 = _get_EARTH_J2()
EARTH_RADIUS = _get_EARTH_RADIUS()
MU_EARTH = _get_EARTH_MU()
MU_SUN = _get_SUN_MU()
G0 = _get_G0()
