# -*- coding: utf-8 -*-
#
#   pycheops - Tools for the analysis of data from the ESA CHEOPS mission
#
#   Copyright (C) 2018  Dr Pierre Maxted, Keele University
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
"""
funcs
=====

 Functions related to observable properties of stars and exoplanets

Parameters
----------
Functions are defined in terms of the following parameters. [1]_

* a          - orbital semi-major axis in solar radii = a_1 + a_2 
* P          - orbital period in mean solar days
* Mass       - total system mass in solar masses, Mass = m_1 + m_2
* ecc        - orbital eccentricity
* omdeg      - longitude of periastron of star's orbit, omega, in _degrees_
* sini       - sine of the orbital inclination 
* K          - 2.pi.a.sini/(P.sqrt(1-e^2)) = K_1 + K_2
* K_1, K_2   - orbital semi-amplitudes in km/s
* q          - mass ratio = m_2/m_1 = K_1/K_2 = a_1/a_2
* f_m        - mass function = m_2^3.sini^3/(m_1+m_2)^2 in solar masses 
                             = K_1^3.P/(2.pi.G).(1-e^2)^(3/2)
* r_1        - radius of star 1 in units of the semi-major axis, r_1 = R_*/a
* rhostar    - mean stellar density = 3.pi/(GP^2(1+q)r_1^3)
* rstar      - host star radius/semi-major axis, rstar = R_*/a
* k          - planet/star radius ratio, k = R_planet/R_star
* tzero      - time of mid-transit (minimum on-sky star-planet separation). 
* b          - impact parameter, b = a.cos(i)/R_star
  
.. rubric References
.. [1] Hilditch, R.W., An Introduction to Close Binary Stars, CUP 2001.


Functions 
---------

"""

from __future__ import (absolute_import, division, print_function,
                                unicode_literals)
from .constants import *
from numpy import roots, imag, real, isscalar, isfinite, array, empty_like
from numpy import arcsin, sqrt, pi, sin, cos, tan, arctan, nan, hypot, finfo
from scipy.optimize import brent
from numba import vectorize


__all__ = [ 'a_rsun','f_m','m1sin3i','m2sin3i','asini','rhostar',
        'K_kms','m_comp','transit_width','esolve','t2z',
        'tzero2tperi', 'vrad', 'xyz_planet']

_arsun   = (GM_SunN*mean_solar_day**2/(4*pi**2))**(1/3.)/R_SunN
_f_m     = mean_solar_day*1e9/(2*pi)/GM_SunN
_asini   = mean_solar_day*1e3/2/pi/R_SunN
_rhostar = 3*pi*V_SunN/(GM_SunN*mean_solar_day**2)

def a_rsun(P, Mass):
    """
    Semi-major axis in solar radii

    :param P: orbital period in mean solar days
    :param Mass: total mass in solar masses, M

    :returns: a = (G.M.P^2/(4.pi^2))^(1/3) in solar radii
    
    """

    return _arsun * P**(2/3.) * Mass**(1/3.)

def f_m(P, K, ecc=0):
    """
    Mass function in solar masses

    :param P: orbital period in mean solar days
    :param K: semi-amplitude of the spectroscopic orbit in km/s
    :param ecc: orbital eccentricity

    :returns: f_m =  m_2^3.sini^3/(m_1+m_2)^2  in solar masses
    """
    return _f_m * K**3 * P * (1 - ecc**2)**1.5

def m1sin3i(P, K_1, K_2, ecc=0):
    """
     Reduced mass of star 1 in solar masses

     :param K_1: semi-amplitude of star 1 in km/s
     :param K_2: semi-amplitude of star 2 in km/s
     :param P: orbital period in mean solar days
     :param ecc:  orbital eccentricity

     :returns: m_1.sini^3 in solar masses 
    """
    return _f_m * K_2 * (K_1 + K_2)**2 * P * (1 - ecc**2)**1.5

def m2sin3i(P, K_1, K_2, ecc=0):
    """
     Reduced mass of star 2 in solar masses

     :param K_1:  semi-amplitude of star 1 in km/s
     :param K_2:  semi-amplitude of star 2 in km/s
     :param P:   orbital period in mean solar days
     :param ecc:   orbital eccentricity

     :returns: m_2.sini^3 in solar masses 
    """
    return _f_m * K_1 * (K_1 + K_2)**2 * P * (1 - ecc**2)**1.5

def asini(K, P, ecc=0):
    """
     a.sini in solar radii

     :param K: semi-amplitude of the spectroscopic orbit in km/s
     :param P: orbital period in mean solar days

     :returns: a.sin(i) in solar radii

    """
    return _asini * K * P *sqrt(1-ecc**2)

def r_star(rho, P, q=0):
    """ 
    Scaled stellar radius R_*/a from mean stellar density 

    :param rho: Mean stellar density in solar units
    :param P: orbital period in mean solar days
    :param q: mass ratio, m_2/m_1

    :returns: radius of star in units of the semi-major axis, R_*/a

    """
    return (_rhostar/(rho*P**2/(1+q)))**(1/3.)

def rhostar(r_1, P, q=0):
    """ 
    Mean stellar density from scaled stellar radius.

    :param r_1: radius of star in units of the semi-major axis, r_1 = R_*/a
    :param P: orbital period in mean solar days
    :param q: mass ratio, m_2/m_1

    :returns: Mean stellar density in solar units

    """
    return _rhostar/(P**2*(1+q)*r_1**3)

def K_kms(m_1, m_2, P, sini, ecc):
    """
    Semi-amplitudes of the spectroscopic orbits in km/s
     - K = 2.pi.a.sini/(P.sqrt(1-ecc^2))
     - K_1 = K * m_2/(m_1+m_2)
     - K_2 = K * m_1/(m_1+m_2)

    :param m_1:  mass of star 1 in solar masses
    :param m_2:  mass of star 2 in solar masses
    :param P:  orbital period in mean solar days
    :param sini:  sine of the orbital inclination
    :param ecc:  orbital eccentrcity

    :returns: K_1, K_2 -- semi-amplitudes in km/s
    """
    M = m_1 + m_2
    a = a_rsun(P, M)
    K = 2*pi*a*R_SunN*sini/(P*mean_solar_day*sqrt(1-ecc**2))/1000
    K_1 = K * m_2/M
    K_2 = K * m_1/M
    return K_1, K_2

#---------------

def m_comp(f_m, m_1, sini):
    """
    Companion mass in solar masses given mass function and stellar mass

    :param f_m: = K_1^3.P/(2.pi.G).(1-ecc^2)^(3/2) in solar masses
    :param m_1: mass of star 1 in solar masses
    :param sini: sine of orbital inclination

    :returns: m_2 = mass of companion to star 1 in solar masses

    """

    def _m_comp_scalar(f_m, m_1, sini):
        if not isfinite(f_m*m_1*sini):
            return nan
        for r in roots([sini**3, -f_m,-2*f_m*m_1, -f_m*m_1**2]):
            if imag(r) == 0:
                return real(r)
        raise ValueError("No finite companion mass for input values.")

#    _m_comp_vector = vectorize(_m_comp_scalar )

    if isscalar(f_m) & isscalar(m_1) & isscalar(sini):
        return float(_m_comp_scalar(f_m, m_1, sini))
    else:
        return np.array([m for m in map(_m_comp_scalar,f_m, m_1, sini)])

#---------------

def transit_width(r, k, b, P=1):
    """
    Total transit duration for a circular orbit.

    See equation (3) from Seager and Malen-Ornelas, 2003ApJ...585.1038S.

    :param r: R_star/a
    :param k: R_planet/R_star
    :param b: impact parameter = a.cos(i)/R_star
    :param P: orbital period (optional, default P=1)

    :returns: Total transit duration in the same units as P.

    """

    return P*arcsin(r*sqrt( ((1+k)**2-b**2) / (1-b**2*r**2) ))/pi

#---------------

@vectorize(nopython=True)
def esolve(M, ecc):
    """
    Solve Kepler's equation M = E - ecc.sin(E) 

    :param M: mean anomaly (scalar or array)
    :param ecc: eccentricity (scalar or array)

    :returns: eccentric anomaly, E

    Algorithm is from Markley 1995, CeMDA, 63, 101 via pyAstronomy class
    keplerOrbit.py

    :Example:

    Test precision using random values::
    
     >>> from pycheops.funcs import esolve
     >>> from numpy import pi, sin, abs, max
     >>> from numpy.random import uniform
     >>> ecc = uniform(0,1,1000)
     >>> M = uniform(-2*pi,4*pi,1000)
     >>> E = esolve(M, ecc)
     >>> maxerr = max(abs(E - ecc*sin(E) - (M % (2*pi)) ))
     >>> print("Maximum error = {:0.2e}".format(maxerr))
     Maximum error = 8.88e-16

    """
    M = M % (2*pi)
    if ecc == 0:
        return M
    if M > pi:
        M = 2*pi - M
        flip = True
    else:
        flip = False
    alpha = (3*pi + 1.6*(pi-abs(M))/(1+ecc) )/(pi - 6/pi)
    d = 3*(1 - ecc) + alpha*ecc
    r = 3*alpha*d * (d-1+ecc)*M + M**3
    q = 2*alpha*d*(1-ecc) - M**2
    w = (abs(r) + sqrt(q**3 + r**2))**(2/3)
    E = (2*r*w/(w**2 + w*q + q**2) + M) / d
    f_0 = E - ecc*sin(E) - M
    f_1 = 1 - ecc*cos(E)
    f_2 = ecc*sin(E)
    f_3 = 1-f_1
    d_3 = -f_0/(f_1 - 0.5*f_0*f_2/f_1)
    d_4 = -f_0/(f_1 + 0.5*d_3*f_2 + (d_3**2)*f_3/6)
    E = E -f_0/(f_1 + 0.5*d_4*f_2 + d_4**2*f_3/6 - d_4**3*f_2/24)
    if flip:
        E =  2*pi - E
    return E

#---------------

def t2z(t, tzero, P, sini, rstar, ecc=0, omdeg=90, returnMask=False):
    """
    Calculate star-planet separation relative to scaled stellar radius, z

    Optionally, return a flag/mask to indicate cases where the planet is
    further from the observer than the star, i.e., whether phases with z<1 are
    transits (mask==True) or eclipses (mask==False)

    :param t: time of observation (scalar or array)
    :param tzero: time of inferior conjunction, i.e., mid-transit
    :param P: orbital period
    :param sini: sine of orbital inclination
    :param rstar: scaled stellar radius, R_star/a
    :param ecc: eccentricity (optional, default=0)
    :param omdeg: longitude of periastron in degrees (optional, default=90)
    :param returnFlag: return a flag to distinguish transits from eclipses.

    N.B. omdeg is the longitude of periastron for the star's orbit

    :returns: z [, mask]

    :Example:
    
    >>> from pycheops.funcs import t2z
    >>> from numpy import linspace
    >>> import matplotlib.pyplot as plt
    >>> t = linspace(0,1,1000)
    >>> sini = 0.999
    >>> rstar = 0.1
    >>> plt.plot(t, t2z(t,0,1,sini,rstar))
    >>> plt.xlim(0,1)
    >>> plt.ylim(0,12)
    >>> ecc = 0.1
    >>> for omdeg in (0, 90, 180, 270):
    >>>     plt.plot(t, t2z(t,0,1,sini,rstar,ecc,omdeg))
    >>> plt.show()
        
    """
    if ecc == 0:
        nu = 2*pi*(t-tzero)/P
        omrad = 0.5*pi
        z = sqrt(1 - cos(nu)**2*sini**2)/rstar
    else:
        tp = tzero2tperi(tzero,P,sini,ecc,omdeg)
        M = 2*pi*(t-tp)/P
        E = esolve(M,ecc)
        nu = 2*arctan(sqrt((1+ecc)/(1-ecc))*tan(E/2))
        omrad = pi*omdeg/180
        # Equation (5.63) from Hilditch
        z = ((1-ecc**2)/(1+ecc*cos(nu))*sqrt(1-sin(omrad+nu)**2*sini**2))/rstar
    if returnMask:
        return z, sin(nu + omrad)*sini < 0
    else:
        return z

#---------

def tzero2tperi(tzero,P,sini,ecc,omdeg):
    """
    Calculate time of periastron from time of mid-transit

    Uses the method by Lacy, 1992AJ....104.2213L

    :param tzero: times of mid-transit
    :param P: orbital period
    :param sini: sine of orbital inclination 
    :param ecc: eccentricity 
    :param omdeg: longitude of periastron in degrees

    :returns: time of periastron prior to tzero

    :Example:
     >>> from pycheops.funcs import tzero2tperi
     >>> tzero = 54321.6789
     >>> P = 1.23456
     >>> sini = 0.987
     >>> ecc = 0.123
     >>> omdeg = 89.01
     >>> print(tzero2tperi(tzero,P,sini,ecc,omdeg))
     54321.6762764

    """
    def _delta(th, sin2i, omrad, ecc):
        # Equation (4.9) from Hilditch
        return (1-ecc**2)*sqrt(1-sin2i*sin(th+omrad)**2)/(1+ecc*cos(th))

    omrad = omdeg*pi/180
    theta = 0.5*pi-omrad
    if (1-sini**2) > finfo(0.).eps :
        fa = _delta(theta-0.25*pi, sini**2, omrad, ecc)
        fb = _delta(theta        , sini**2, omrad, ecc)
        fc = _delta(theta+0.25*pi, sini**2, omrad, ecc)
        if ((fb>fa)|(fb>fc)):
            print (theta-0.25*pi,theta,theta+0.25*pi)
            print (fa,fb,fc)

        theta = brent(_delta, args = (sini**2, omrad, ecc),
                brack = (theta-0.25*pi,theta,theta+0.25*pi))
    if theta == pi:
        E = pi 
    else:
        E = 2*arctan(sqrt((1-ecc)/(1+ecc))*tan(theta/2))
    return tzero - (E - ecc*sin(E))*P/(2*pi)

#---------------

def nu_max(Teff, logg):
    """
    Peak frequency in micro-Hz for solar-like oscillations.

    From equation (17) of Campante et al., (2016)[2]_.

    :param logg: log of the surface gravity in cgs units.
    :param Teff: effective temperature in K

    :returns: nu_max in micro-Hz

    .. rubric References
    .. [2] Campante, 2016, ApJ 830, 138.

    """
    return 3090 * 10**(logg-4.438)/sqrt(Teff/5777)


#---------------

def vrad(t,tzero,P,K,ecc=0,omdeg=90,sini=1, primary=True):
    """
    Calculate radial velocity, V_r, for body in a Keplerian orbit

    :param t: array of input times 
    :param tzero: time of inferior conjunction, i.e., mid-transit
    :param P: orbital period
    :param K: radial velocity semi-amplitude 
    :param ecc: eccentricity (optional, default=0)
    :param omdeg: longitude of periastron in degrees (optional, default=90)
    :param sini: sine of orbital inclination (to convert tzero to t_peri)
    :param primary: if false calculate V_r for companion

    :returns: V_r in same units as K relative to the barycentre of the binary

    """
    tp = tzero2tperi(tzero,P,sini,ecc,omdeg)
    M = 2*pi*(t-tp)/P
    E = esolve(M,ecc)
    nu = 2*arctan(sqrt((1+ecc)/(1-ecc))*tan(E/2))
    omrad = pi*omdeg/180
    if not primary:
        omrad = omrad + pi
    return K*(cos(nu+omrad)+ecc*cos(omrad))

#---------------

def xyz_planet(t, tzero, P, sini, ecc=0, omdeg=90):
    """
    Position of the planet in Cartesian coordinates.

    The position of the ascending node is taken to be Omega=0 and the
    semi-major axis is taken to be a=1.

    :param t: time of observation (scalar or array)
    :param tzero: time of inferior conjunction, i.e., mid-transit
    :param P: orbital period
    :param sini: sine of orbital inclination
    :param ecc: eccentricity (optional, default=0)
    :param omdeg: longitude of periastron in degrees (optional, default=90)

    N.B. omdeg is the longitude of periastron for the star's orbit

    :returns: (x, y, z)

    :Example:
    
    >>> from pycheops.funcs import phase_angle
    >>> from numpy import linspace
    >>> import matplotlib.pyplot as plt
    >>> t = linspace(0,1,1000)
    >>> sini = 0.9
    >>> ecc = 0.1
    >>> omdeg = 90
    >>> x, y, z = xyz_planet(t, 0, 1, sini, ecc, omdeg)
    >>> plt.plot(x, y)
    >>> plt.plot(x, z)
    >>> plt.show()
        
    """
    if ecc == 0:
        nu = 2*pi*(t-tzero)/P
        r = 1
        cosw = 0
        sinw = -1
    else:
        tp = tzero2tperi(tzero,P,sini,ecc,omdeg)
        M = 2*pi*(t-tp)/P
        E = esolve(M,ecc)
        nu = 2*arctan(sqrt((1+ecc)/(1-ecc))*tan(E/2))
        r = (1-ecc**2)/(1+ecc*cos(nu))
        omrad = pi*omdeg/180
        # negative here since om_planet = om_star + pi
        cosw = -cos(omrad)
        sinw = -sin(omrad)
    sinv = sin(nu) 
    cosv = cos(nu)
    cosi = sqrt(1-sini**2)
    x = r*(-sinv*sinw + cosv*cosw)
    y = r*cosi*(cosv*sinw + sinv*cosw)
    z = -r*sini*(cosw*sinv + cosv*sinw)
    return x, y, z

