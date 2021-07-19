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
import iris.analysis
import numpy as np

fname='/home/ubuntu/Tutorials/vn11.8/sample_output/Task10.1/atmosa.pa19810901_00'

# constraint on time to get 2nd radiation timestep
tconstr=iris.Constraint(time=lambda cell: cell.point.hour == 2)

# load orography to enable correct calculation of level heights
orog=iris.load_cube(
     '/home/vagrant/umdir/ancil/atmos/n48e/orography/globe30/v2/qrparm.orog',
     iris.AttributeConstraint(STASH='m01s00i033'))

# load all extinction components at 0.55 micron
ukca=iris.load_cube(fname,[
    iris.Constraint(pseudo_level=3) & iris.AttributeConstraint(STASH='m01s02i530') & tconstr])
classic=iris.load_cube(fname,[
    iris.Constraint(pseudo_level=3) & iris.AttributeConstraint(STASH='m01s02i540') & tconstr])

# Calculate the correct height of each cell
# add the orography as an auxillary coordinate
auxcoord=iris.coords.AuxCoord(orog.data,standard_name=str(orog.standard_name),long_name="orography",var_name="orog",units=orog.units)
# added in to lat/lon (ht=0,lat=1,lon=2)
ukca.add_aux_coord(auxcoord,(1,2,))
# now calculate the correct altitude above sea-level
factory=iris.aux_factory.HybridHeightFactory(delta=ukca.coord("level_height"),sigma=ukca.coord("sigma"),orography=ukca.coord("surface_altitude"))
# now create the 'altitude' derrived coordinate
ukca.add_aux_factory(factory)
# now calculate the height from the bounds
bounds = ukca.coord('altitude').bounds[:,:,:,1] - ukca.coord('altitude').bounds[:,:,:,0]
    
# mutliply by the height of each cell 
ukca.data = ukca.data * bounds
classic.data = classic.data * bounds

# now sum up the column
ukca_int=ukca.collapsed('model_level_number',iris.analysis.SUM)
classic_int=classic.collapsed('model_level_number',iris.analysis.SUM)

# add together
aod=ukca_int.copy()
aod.data = ukca_int.data + classic_int.data
# rename
aod.rename('atmosphere_optical_thickness_due_to_aerosol')

# output to netCDF
iris.save(aod,'Task105_AOD.nc',netcdf_format='NETCDF3_CLASSIC')
