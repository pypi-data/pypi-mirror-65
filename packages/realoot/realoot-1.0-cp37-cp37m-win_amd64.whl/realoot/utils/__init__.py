# We import all symbols in the core namespace (also the ones we do not use
# in this file, but we still want in the namespace core)

import math


def deg2rad(value_deg):
    """" Conversion degrees -> radians """
    return value_deg * math.pi / 180.


def rad2deg(value_rad):
    """" Conversion radians -> degrees """
    return value_rad * 180. / math.pi


def calc_ra(sma, ecc):
    """ Compute the radius of apoapsis from semi-major axis and eccentricity """
    return sma * (1. + ecc)


def calc_rp(sma, ecc):
    """ Compute the radius of periapsis from semi-major axis and eccentricity """
    return sma * (1. - ecc)


def calc_rarp(sma, ecc):
    """ Compute the radius of apoapsis and periapsis from semi-major axis and eccentricity """
    return calc_ra(sma, ecc), calc_rp(sma, ecc)


def calc_sma(ha, hp, radius):
    """ Compute the semi-major axis from altitude of apoapsis and periapsis """
    return radius + (ha + hp) / 2.


def calc_orbital_energy(sma, mu):
    """ Compute orbital energy from semi-major axis """
    return -mu / (2. * sma)


def calc_eccentricity_vector(ecc, aop, raan):
    """ Compute the eccentricity vector from eccentricity, argument of pericenter and right ascension of ascending node 
        Angles are in radians.
    """
    ex = ecc * math.cos(aop + raan)
    ey = ecc * math.sin(aop + raan)
    return [ex, ey]


def calc_eccentricity_vector(ecc, aop, raan):
    """ Compute inclination vector from eccentricity and right ascension of ascending node
        Angles are in radians
    """
    hx = math.tan(inc/2.) * math.cos(raan)
    hy = math.tan(inc/2.) * math.sin(raan)
    return [hx, hy]



