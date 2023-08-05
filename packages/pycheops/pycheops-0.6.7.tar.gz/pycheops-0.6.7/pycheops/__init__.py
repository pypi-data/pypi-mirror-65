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
 ********
 pycheops
 ********
 This package provides tools for the analysis of light curves from the ESA
 CHEOPS mission <http://cheops.unibe.ch/>.

"""

from os import path
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'VERSION')) as version_file:
    __version__ = version_file.read().strip()

"""
 Create pickle files for interpolation within various data tables
"""
from scipy.interpolate import interp1d, NearestNDInterpolator
from photutils import CircularAperture, aperture_photometry
import numpy as np
import pickle
from astropy.table import Table
from .core import load_config
try:
    config = load_config()
except ValueError:
    print(' ** Run pycheops.core.setup_config **')
    raise ValueError

data_path = path.join(here,'data','instrument')
cache_path = config['DEFAULT']['data_cache_path']
# Photometric aperture contamation calculation from PSF for make_xml_files
pfile = path.join(cache_path,'Contamination_33arcsec_aperture.p')
if not path.isfile(pfile):
    radius = 33  # Aperture radius in pixels
    psffile = path.join(data_path, 'CHEOPS_IT_PSFwhite_20180720AO1v1.0.txt')
    with open(psffile) as fp:
        data = [[float(digit) for digit in line.split()] for line in fp]
    position0 = [(99.5,99.5)]
    aperture0 = CircularAperture(position0, r=radius)
    photTable0 = aperture_photometry(data, aperture0)
    target_flux = photTable0['aperture_sum'][0]
    rad = np.linspace(0.0,125,25,endpoint=True)
    contam = np.zeros_like(rad)
    contam[0] = 1.0
    for i,r in enumerate(rad[1:]):
        nthe = max(4, round(r/5).astype(int))
        the = np.linspace(0,2*np.pi,nthe)
        pos= np.array((100+np.array(r*np.cos(the)),
                    100+np.array(r*np.sin(the)))).T
        apertures = CircularAperture(pos, r=radius)
        photTable = aperture_photometry(data, apertures)
        contam[i+1] = max(photTable['aperture_sum'])/target_flux
    contam = np.array(contam)  # convert to numpy array else sphinx complains
    I = interp1d(rad, contam,fill_value=min(contam),bounds_error=False)
    with open(pfile,'wb') as fp:
        pickle.dump(I,fp)

# Visibility calculator for instrument.py and make_xml_files
pfile = path.join(cache_path,'visibility_interpolator.p')
if not path.isfile(pfile):
    vfile = path.join(data_path,'VisibilityTable.csv')
    visTable = Table.read(vfile)
    ra_ = visTable['RA']*180/np.pi
    dec_ = visTable['Dec']*180/np.pi
    vis = visTable['Efficiency']
    I = NearestNDInterpolator((np.array([ra_,dec_])).T,vis)
    with open(pfile,'wb') as fp:
        pickle.dump(I,fp)

# T_eff v. G_BP-G_RP colour from 
# http://www.pas.rochester.edu/~emamajek/EEM_dwarf_UBVIJHK_colors_Teff.txt
# Version 2019.3.22
pfile = path.join(cache_path,'Teff_BP_RP_interpolator.p')
if not path.isfile(pfile):
    fT = path.join(here,'data','EEM_dwarf_UBVIJHK_colors_Teff',
            'EEM_dwarf_UBVIJHK_colors_Teff.txt')
    T = Table.read(fT,format='ascii',header_start=-1,
            fill_values=('...',np.nan))
    b_p = np.array(T['Bp-Rp']) # convert to numpy array else sphinx complains
    Teff = np.array(T['Teff'])  # convert to numpy array else sphinx complains
    I = interp1d(b_p,Teff,bounds_error=False,
            fill_value='extrapolate')
    with open(pfile,'wb') as fp:
        pickle.dump(I,fp)

# CHEOPS magnitude - Gaia G magnitude v. T_eff
# From ImageETCc1.4 exposure time calculator spreadsheet
pfile = path.join(cache_path,'C_G_Teff_interpolator.p')
if not path.isfile(pfile):
    fT = path.join(here,'data','instrument', 'C_G_Teff.csv')
    T = Table.read(fT,format='csv')
    Teff = np.array(T['Teff'])  # convert to numpy array else sphinx complains
    C_G = np.array(T['C-G']) # convert to numpy array else sphinx complains
    I = interp1d(Teff,C_G,bounds_error=False, fill_value='extrapolate')
    with open(pfile,'wb') as fp:
        pickle.dump(I,fp)

from .dataset import Dataset
from .starproperties import StarProperties

