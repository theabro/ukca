#!/usr/bin/env python

# This file is part of the UKCA Tutorials:
#  http://www.ukca.ac.uk/wiki/index.php/UKCA_Chemistry_and_Aerosol_Tutorials_at_vn11.8

# Copyright (C) 2021  University of Cambridge

# This is free software: you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.

# It is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.

# You find a copy of the GNU Lesser General Public License at <http://www.gnu.org/licenses/>.

# Written by N. Luke Abraham 2021-01-18 <nla27@cam.ac.uk> 

# preamble
import iris
import iris.time

fname='/umshared/Tutorials/vn11.8/sample_output/Task10.1/atmosa.pa19810901_00'

# constraint on time to get 2nd radiation timestep
tconstr=iris.Constraint(time=lambda cell: cell.point.hour == 2)

# load all TOA components at 0.55 micron
# must use this way of loading to account for constraint on time
with iris.FUTURE.context(cell_datetime_objects=True):
    isw=iris.load_cube(fname,[iris.AttributeConstraint(STASH='m01s01i207') & tconstr])
    osw=iris.load_cube(fname,[iris.AttributeConstraint(STASH='m01s01i208') & tconstr])
    olw=iris.load_cube(fname,[iris.AttributeConstraint(STASH='m01s02i205') & tconstr])

# make cube to store net downward TOA flux
toa=isw.copy()
# add-up components
toa.data=isw.data - (osw.data + olw.data)

toa.rename('toa_net_downward_radiative_flux')

# remove unlimited dimension when writing to netCDF
iris.FUTURE.netcdf_no_unlimited=True

# output to netCDF
iris.save(toa,'Task104_TOA.nc',netcdf_format='NETCDF3_CLASSIC')
