#!/usr/bin/env python

# This file is part of the UKCA Tutorials:
#  http://www.ukca.ac.uk/wiki/index.php/UKCA_Chemistry_and_Aerosol_Tutorials_at_vn10.9

# Copyright (C) 2017  University of Cambridge

# This is free software: you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.

# It is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.

# You find a copy of the GNU Lesser General Public License at <http://www.gnu.org/licenses/>.

# Written by N. Luke Abraham 2017-12-11 <nla27@cam.ac.uk> 

# preamble
import iris

cname='./Task104_TOA.nc'
ename='./Task106_TOA.nc'

cntl=iris.load_cube(cname)
expt=iris.load_cube(ename)

# difference the fields
expt.data=expt.data - cntl.data

# output to netCDF
iris.save(expt,'Task106_TOA_diff.nc',netcdf_format='NETCDF3_CLASSIC')
