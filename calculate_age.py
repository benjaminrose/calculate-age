"""calculate_age.py -- Calculate the age for a set of SFH parameters.
"""
__version__ = '0.1'
__author__ = 'Benjamin Rose'

import matplotlib.pyplot as plt

import numpy as np
from scipy import integrate
# import astropy.units as u
from astropy.cosmology import FlatLambdaCDM

#TODO make this a class so users can change the cosmology
cosmo = FlatLambdaCDM(H0=70, Om0=0.27)


# TODO update all functions to be vectorized
def age(tau: float, sf_start_t: float, sf_trans_percent: float, phi: float, redshift: float) -> float:
    """Calculates the mass weighted age.

    This is for a given set of parameters from the 4-parameter delayed tau SFH model.

    Parameters
    ----------
        tau: float
            In 1/Gyr.
        sf_start_t: float
            In Gyr.
        sf_trans_percent: float
        phi: float
        redshift: 

    Returns
    -------
        float
            The mass weighted age, in Gyr.

    """

    tau = np.asarray(tau)
    sf_start_t = np.asarray(sf_start_t)
    sf_trans_percent = np.asarray(sf_trans_percent)
    phi = np.asarray(phi)

    # Get correct variables to match Gupta 2011 eqn 6 definitions
    age_of_universe = cosmo.age(redshift).to('Gyr').value
    length_of_sf = age_of_universe - sf_start_t     # Gupta's A value
    sf_trans_since_sf_start = length_of_sf*sf_trans_percent    # transition time, since start of SF
    sf_slope = np.tan(phi)

    # If tau can equal 0.1 and we are over 14 Gyr max, that is 140 e-folding times
    # We can sample that with >1400 samples, previously I used 8193. IDK why.
    # Needs to be an odd number of samples to use Simpson Rule
    time_since_start = np.linspace(0, length_of_sf, 2001)

    # Calculate numerator and denominator for each SFH
    star_formation = []
    for t in time_since_start:
        star_formation.append(four_param_tau(t, tau, sf_trans_since_sf_start, sf_slope))
    star_formation = np.array(star_formation)

    # print(star_formation.shape, time_since_start.shape)
    numerator = integrate.simps(time_since_start*star_formation, time_since_start)
    denominator = integrate.simps(star_formation, time_since_start)

    # This is from Gupta 2011 Equation 3 but with a change in t_0. He used t_0
    # = start of star formation, I use t_0 = big bang. Explained in FIndings 
    # on 2017-05-10 & updated on 2017-05-15
    # return age_of_universe.to('Gyr').value - sf_start_t + numerator/denominator

    # return a function that integrates over Gupta's variables.
    return length_of_sf - numerator/denominator

def ramp(x: float) -> float:
    """A ramp function.

    Simha 2014's Delta-function in eqn 6
    """

    return x if x >= 0 else 0


def four_param_tau(time_since_start: float, tau: float, sf_trans_since_sf_start: float,
                   sf_slope: float) -> float:
    """Calculate star formation rate for the 4-parameter tau model at 1 time.

    This follows the variable convention found in Gupta et al 2011 eq 3, but
    uses the 4 parameter delayed tau model (sometimes called linear-exponent)
    instead Defined piecewise around `sf_trans_since_sf_start` time.  no
    variables can be arrays! ALso must return a float!"""

    # Do vectorized piece wise.
    # Build a boolian array defining when a step is first and second parts of piecewise
    # Multiply first function by boolian array.
    # Multiply second function by logical not of boolian array.
    # Since the parts outside the appropate piecewise regions will be zero, add the two
    # arrays to get the final function output.
    if time_since_start <= sf_trans_since_sf_start:
        sf = time_since_start*np.e**(-time_since_start/tau)
    else:
        sf = (four_param_tau(sf_trans_since_sf_start, tau, sf_trans_since_sf_start, sf_slope) +
              sf_slope*ramp(time_since_start - sf_trans_since_sf_start))

    # Only return a positive star formation.
    if sf <= 0:
        return 0
    else:
        return sf
