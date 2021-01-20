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

# Written by N. Luke Abraham 2021-01-15 <nla27@cam.ac.uk> 

# preamble
import iris
import iris.time

fname='/umshared/Tutorials/vn11.8/sample_output/Task10.6/atmosa.pa19810901_00'

# constraint on time to get 2nd radiation timestep
tconstr=iris.Constraint(time=lambda cell: cell.point.hour == 2)

# load all AOD & AAOD components at 0.55 micron
# must use this way of loading to account for constraint on time
with iris.FUTURE.context(cell_datetime_objects=True):
    aod=iris.load(fname,[
        iris.Constraint(pseudo_level=3) & iris.AttributeConstraint(STASH='m01s02i285') & tconstr,
	iris.Constraint(pseudo_level=3) & iris.AttributeConstraint(STASH='m01s02i300') & tconstr,
	iris.Constraint(pseudo_level=3) & iris.AttributeConstraint(STASH='m01s02i301') & tconstr,
	iris.Constraint(pseudo_level=3) & iris.AttributeConstraint(STASH='m01s02i302') & tconstr,
	iris.Constraint(pseudo_level=3) & iris.AttributeConstraint(STASH='m01s02i303') & tconstr,
	iris.Constraint(pseudo_level=3) & iris.AttributeConstraint(STASH='m01s02i304') & tconstr,
	iris.Constraint(pseudo_level=3) & iris.AttributeConstraint(STASH='m01s02i305') & tconstr])
    aaod=iris.load(fname,[
         iris.Constraint(pseudo_level=3) & iris.AttributeConstraint(STASH='m01s02i585') & tconstr,
	 iris.Constraint(pseudo_level=3) & iris.AttributeConstraint(STASH='m01s02i240') & tconstr,
	 iris.Constraint(pseudo_level=3) & iris.AttributeConstraint(STASH='m01s02i241') & tconstr,
	 iris.Constraint(pseudo_level=3) & iris.AttributeConstraint(STASH='m01s02i242') & tconstr,
	 iris.Constraint(pseudo_level=3) & iris.AttributeConstraint(STASH='m01s02i243') & tconstr,
	 iris.Constraint(pseudo_level=3) & iris.AttributeConstraint(STASH='m01s02i244') & tconstr,
	 iris.Constraint(pseudo_level=3) & iris.AttributeConstraint(STASH='m01s02i245') & tconstr])

# make cube to store total AOD
aodsum=aod[0].copy()
# add-up components
aodsum.data=aod[0].data+aod[1].data+aod[2].data+aod[3].data+aod[4].data+aod[5].data+aod[6].data

# make cube to store total AAOD
aaodsum=aaod[0].copy()
# add-up components
aaodsum.data=aaod[0].data+aaod[1].data+aaod[2].data+aaod[3].data+aaod[4].data+aaod[5].data+aaod[6].data

# calculate single-scattering albedo
ssa=aodsum.copy()
ssa.data = 1.0 - (aaodsum.data/aodsum.data)

# rename
ssa.rename('single_scattering_albedo_in_air_due_to_ambient_aerosol_particles')

# remove unlimited dimension when writing to netCDF
iris.FUTURE.netcdf_no_unlimited=True

# output to netCDF
iris.save(ssa,'Task106_SSA.nc',netcdf_format='NETCDF3_CLASSIC')
