# Copyright (c) 2018 Andreas Kvas
# See LICENSE for copyright/license details.

"""
Isotropic harmonic integral kernels.
"""

import numpy as np
import pkg_resources
import abc
import l3py.utilities


def get_kernel(kernel_name, nmax):
    """
    Return kernel coefficients.

    Parameters
    ----------
    kernel_name : string
        name of kernel, currently implemented: water height ('ewh', 'water_height'),
        ocean bottom pressure ('obp', 'ocean_bottom_pressure')
    nmax : int
        maximum degree of kernel coefficients

    Returns
    -------
    kernel : Kernel subclass instance
        kernel associated with kernel_name

    Raises
    ------
    ValueError
        if an unrecognized kernel name is passed

    """

    if kernel_name.lower() in ['ewh', 'water_height']:
        inverse_coefficients = l3py.kernel.WaterHeight(nmax)

    elif kernel_name.lower() in ['obp', 'ocean_bottom_pressure']:
        inverse_coefficients = l3py.kernel.OceanBottomPressure(nmax)

    elif kernel_name.lower() in ['potential']:
        inverse_coefficients = l3py.kernel.Potential()

    elif kernel_name.lower() in ['geoid', 'geoid_height']:
        inverse_coefficients = l3py.kernel.GeoidHeight()

    else:
        raise ValueError("Unrecognized kernel '{0:s}'.".format(kernel_name))

    return inverse_coefficients


class Kernel(metaclass=abc.ABCMeta):
    """
    Base interface for spherical harmonic kernels.

    Subclasses must implement a method `kn` which depends on degree radius and co-latitude and returns kernel
    coefficients.
    """

    @abc.abstractmethod
    def kn(self, r, colat):
        pass


class WaterHeight(Kernel):
    """
    Implementation of the water height kernel. Applied to a sequence of potential coefficients, the result is
    equivalent water height in meters when propagated to space domain.

    Parameters
    ----------
    nmax : int
        maximum spherical harmonic degree
    rho : float
        density of water in [kg/m**3]
    """

    def __init__(self, nmax, rho=1025):

        file_name = pkg_resources.resource_filename('l3py', 'data/loadLoveNumbers_Gegout97.txt')
        love_numbers = np.loadtxt(file_name)[0:nmax+1]

        self.__kn = (2*np.arange(0, nmax+1)+1)/(1+love_numbers[0:nmax+1])/(4*np.pi*6.673e-11*rho)

    def kn(self, n, r=6378136.6, colat=0):
        """
        Kernel coefficient for degree n.

        Parameters
        ----------
        n : int
            coefficient degree
        r : float, array_like shape (m,)
            radius of evaluation points
        colat : float, array_like shape (m,)
            co-latitude of evaluation points in radians

        Returns
        -------
        kn : float, array_like shape (m,)
            kernel coefficients for degree n for all evaluation points
        """
        return self.__kn[n]/r


class OceanBottomPressure(Kernel):
    """
    Implementation of the ocean bottom pressure kernel. Applied to a sequence of potential coefficients, the result
    is ocean bottom pressure in Pascal when propagated to space domain.

    Parameters
    ----------
    nmax : int
        maximum spherical harmonic degree
    """
    def __init__(self, nmax):
        file_name = pkg_resources.resource_filename('l3py', 'data/loadLoveNumbers_Gegout97.txt')
        love_numbers = np.loadtxt(file_name)[0:nmax+1]

        self.__kn = (2 * np.arange(0, nmax + 1) + 1) / (1 + love_numbers[0:nmax + 1]) / (4 * np.pi * 6.673e-11)

    def kn(self, n, r=6378136.6, colat=0):
        """
        Kernel coefficient for degree n.

        Parameters
        ----------
        n : int
            coefficient degree
        r : float, array_like shape (m,)
            radius of evaluation points
        colat : float, array_like shape (m,)
            co-latitude of evaluation points in radians

        Returns
        -------
        kn : float, array_like shape (m,)
            kernel coefficients for degree n for all evaluation points
        """

        return self.__kn[n]/r*l3py.utilities.normal_gravity(r, colat)


class Potential(Kernel):
    """
    Implementation of the Poisson kernel (disturbing potential).
    """
    def __init__(self):
        pass

    def kn(self, n, r=6378136.6, colat=0):
        """
        Kernel coefficient for degree n.

        Parameters
        ----------
        n : int
            coefficient degree
        r : float, array_like shape (m,)
            radius of evaluation points
        colat : float, array_like shape (m,)
            co-latitude of evaluation points in radians

        Returns
        -------
        kn : float, array_like shape (m,)
            kernel coefficients for degree n for all evaluation points
        """

        count = max(np.asarray(r).size, np.asarray(colat).size)

        return np.ones(count)


class GeoidHeight(Kernel):
    """
    Implementation of the geoid height kernel (disturbing potential divided by normal gravity).
    """
    def __init__(self):
        pass

    def kn(self, n, r=6378136.6, colat=0):
        """
        Kernel coefficient for degree n.

        Parameters
        ----------
        n : int
            coefficient degree
        r : float, array_like shape (m,)
            radius of evaluation points
        colat : float, array_like shape (m,)
            co-latitude of evaluation points in radians

        Returns
        -------
        kn : float, array_like shape (m,)
            kernel coefficients for degree n for all evaluation points
        """

        return l3py.utilities.normal_gravity(r, colat)**-1

