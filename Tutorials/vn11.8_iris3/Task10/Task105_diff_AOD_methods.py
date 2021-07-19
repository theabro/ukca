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

dname='./Task102_AOD.nc'
cname='./Task105_AOD.nc'

diag=iris.load_cube(dname)
# need to constrain on name due to using load_cube
calc=iris.load_cube(cname,'atmosphere_optical_thickness_due_to_aerosol')

# difference the fields
calc.data=calc.data - diag.data

# output to netCDF
iris.save(calc,'Task105_AOD_diff.nc',netcdf_format='NETCDF3_CLASSIC')
