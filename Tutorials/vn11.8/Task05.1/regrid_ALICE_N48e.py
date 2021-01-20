#!/usr/bin/env python

# This file is part of the UKCA Tutorials:
#  http://www.ukca.ac.uk/wiki/index.php/UKCA_Chemistry_and_Aerosol_Tutorials_at_vn11.8

# Copyright (C) 2021  University of Cambridge

# This is free software: you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.

# It is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

# You find a copy of the GNU Lesser General Public License at <http://www.gnu.org/licenses/>.

# Written by N. Luke Abraham 2021-01-04 <nla27@cam.ac.uk> 

# To use this script on a personal VM you should first
#    install-iris
# and then open a new terminal with the correct PATHs set using the command
#    conda
# If you have been provided a VM, please use the command
#    pyterm
# followed by
#    pylab
# once you have done this, you can run the script (through ipython) using
#    %run "/path/to/regrid_ALICE_N48e.py"

# preamble
import iris
import numpy
# pre-Iris v1.10, use iris.unit instead of cf_units
import cf_units

# --- CHANGE THINGS BELOW THIS LINE TO WORK WITH YOUR FILES ETC. ---

# name of file containing an ENDGame grid, e.g. your model output
# NOTE: all the fields in the file should be on the same horizontal
#       grid, as the field used MAY NOT be the first in order of STASH
grid_file='/umshared/Tutorials/vn11.8/sample_output/Base/atmosa.pa19810901_00'
# name of emissions file
emissions_file='/umshared/Tutorials/vn11.8/Task05.1/Emissions_of_ALICE.nc'

# --- BELOW THIS LINE, NOTHING SHOULD NEED TO BE CHANGED ---

species_name='ALICE'

# this is the grid we want to regrid to, e.g. N48 ENDGame
grd=iris.load_cube(grid_file,iris.AttributeConstraint(STASH='m01s34i001'))
grd.coord(axis='x').guess_bounds()
grd.coord(axis='y').guess_bounds()

# This is the original data
ems=iris.load_cube(emissions_file)
# make intersection between 0 and 360 longitude to ensure that 
# the data is regridded correctly
nems = ems.intersection(longitude=(0, 360))

# make sure that we use the same coordinate system, otherwise regrid won't work
nems.coord(axis='x').coord_system=grd.coord_system()
nems.coord(axis='y').coord_system=grd.coord_system()

# now guess the bounds of the new grid prior to regridding
nems.coord(axis='x').guess_bounds()
nems.coord(axis='y').guess_bounds()

# now regrid
ocube=nems.regrid(grd,iris.analysis.AreaWeighted())

# now add correct attributes and names to netCDF file
ocube.var_name='emissions_'+str.strip(species_name)
ocube.long_name=str.strip(species_name)+' surf emissions'
ocube.units=cf_units.Unit('kg m-2 s-1')
ocube.attributes['vertical_scaling']='surface'
ocube.attributes['tracer_name']=str.strip(species_name)
# global attributes, so don't set in local_keys
# NOTE: all these should be strings, including the numbers! This will change at a later UM version.
# basic emissions type
ocube.attributes['emission_type']='2' # periodic
ocube.attributes['update_type']='2'   # same as above
ocube.attributes['update_freq_in_hours']='120' # i.e. 5 days
ocube.attributes['source']='UKCA Tutorial Task 5.1 - creating netCDF emissions'

# rename and set time coord - set to be 0000/01/16:00:00-0000/12/16:00:00
# this bit is annoyingly fiddly
ocube.coord(axis='t').var_name='time'
ocube.coord(axis='t').standard_name='time'
ocube.coords(axis='t')[0].units=cf_units.Unit('hours since 1970-01-01', calendar='360_day')
ocube.coord(axis='t').points=numpy.array([-17020440, -17019720, -17019000, -17018280,
                                          -17017560, -17016840, -17016120, -17015400, 
                                          -17014680, -17013960, -17013240, -17012520]) 
# make z-direction.
zdims=iris.coords.DimCoord(numpy.array([0]),standard_name = 'model_level_number',
                           units='1',attributes={'positive':'up'})
ocube.add_aux_coord(zdims)
ocube=iris.util.new_axis(ocube, zdims)
# now transpose cube to put Z 2nd
ocube.transpose([1,0,2,3])

# make coordinates 64-bit
ocube.coord(axis='x').points=ocube.coord(axis='x').points.astype(dtype='float64')
ocube.coord(axis='y').points=ocube.coord(axis='y').points.astype(dtype='float64')
#ocube.coord(axis='z').points=ocube.coord(axis='z').points.astype(dtype='float64') # integer
ocube.coord(axis='t').points=ocube.coord(axis='t').points.astype(dtype='float64')
# for some reason, longitude_bounds are double, but latitude_bounds are float
ocube.coord('latitude').bounds=ocube.coord('latitude').bounds.astype(dtype='float64')


# add forecast_period & forecast_reference_time
# forecast_reference_time
frt=numpy.array([-17020080, -17019360, -17018640, -17017920, 
                 -17017200, -17016480, -17015760, -17015040, 
                 -17014320, -17013600, -17012880, -17012160],dtype='float64')
frt_dims=iris.coords.AuxCoord(frt,standard_name = 'forecast_reference_time',
                           units=cf_units.Unit('hours since 1970-01-01', calendar='360_day'))
ocube.add_aux_coord(frt_dims,data_dims=0)
ocube.coord('forecast_reference_time').guess_bounds()
# forecast_period
fp=numpy.array([-360],dtype='float64')
fp_dims=iris.coords.AuxCoord(fp,standard_name = 'forecast_period',
                           units=cf_units.Unit('hours'),bounds=numpy.array([-720,0],dtype='float64'))
ocube.add_aux_coord(fp_dims,data_dims=None)

# add-in cell_methods
ocube.cell_methods = [iris.coords.CellMethod('mean', 'time')]
# set _FillValue
fillval=1e+20
ocube.data = numpy.ma.array(data=ocube.data, fill_value=fillval, dtype='float32')

# output file name, based on species
outpath='ukca_emiss_'+species_name+'.nc'
# don't want time to be cattable, as is a periodic emissions file
iris.FUTURE.netcdf_no_unlimited=True
# annoying hack to set a missing_value attribute as well as a _FillValue attribute
dict.__setitem__(ocube.attributes, 'missing_value', fillval)
# now write-out to netCDF
saver = iris.fileformats.netcdf.Saver(filename=outpath, netcdf_format='NETCDF3_CLASSIC')
saver.update_global_attributes(Conventions=iris.fileformats.netcdf.CF_CONVENTIONS_VERSION)
saver.write(ocube, local_keys=['vertical_scaling', 'missing_value','um_stash_source','tracer_name'])

# end of script

# Why we are messing around with metadata?
#-----------------------------------------
#
# We need to adapt the metadata of the emissions data to 
# match what UKCA is expecting. 
#  e.g. the metadata of the 'Emissions_of_ALICE.nc file is:
#
#    netcdf Emissions_of_ALICE {
#    dimensions:
#            lon = 720 ;
#            lat = 360 ;
#            date = UNLIMITED ; // (12 currently)
#    variables:
#            float lon(lon) ;
#                    lon:long_name = "Longitude" ;
#                    lon:standard_name = "longitude" ;
#                    lon:units = "degrees_east" ;
#                    lon:point_spacing = "even" ;
#                    lon:modulo = " " ;
#            float lat(lat) ;
#                    lat:long_name = "Latitude" ;
#                    lat:standard_name = "latitude" ;
#                    lat:units = "degrees_north" ;
#                    lat:point_spacing = "even" ;
#            float date(date) ;
#                    date:long_name = "Time" ;
#                    date:units = "days since 1960-01-01" ;
#                    date:time_origin = "01-JAN-1960:00:00:00" ;
#            float ALICE(date, lat, lon) ;
#                    ALICE:source = " " ;
#                    ALICE:name = "ALICE" ;
#                    ALICE:title = "Emissions of ALICE in kg/m^2/s" ;
#                    ALICE:date = "01/01/60" ;
#                    ALICE:time = "00:00" ;
#                    ALICE:long_name = "Emissions of ALICE in kg/m^2/s" ;
#                    ALICE:standard_name = "tendency_of_atmosphere_mass_content_of_ALICE_due_to_emission" ;
#                    ALICE:units = "kg/m2/s" ;
#                    ALICE:missing_value = 2.e+20f ;
#                    ALICE:_FillValue = 2.e+20f ;
#                    ALICE:valid_min = 0.f ;
#                    ALICE:valid_max = 2.60646e-08f ;
#    
#    // global attributes:
#                    :history = "Tue Jun 18 14:32:42 BST 2013 - XCONV V1.92 16-February-2006" ;
#    }
#
#  whereas, the metadata of the 
#  /home/vagrant/umdir/ancil/atmos/n48e/ukca_emiss/cmip5/2000/v1/ukca_emiss_CO.nc
#  file is, e.g.:
#
#    netcdf ukca_emiss_CO {
#    dimensions:
#            time = UNLIMITED ; // (12 currently)
#            model_level_number = 1 ;
#            latitude = 72 ;
#            longitude = 96 ;
#            bnds = 2 ;
#    variables:
#            double emissions_CO(time, model_level_number, latitude, longitude) ;
#                    emissions_CO:long_name = "CO surf emissions" ;
#                    emissions_CO:units = "kg m-2 s-1" ;
#                    emissions_CO:um_stash_source = "m01s00i303" ;
#                    emissions_CO:tracer_name = "CO" ;
#                    emissions_CO:vertical_scaling = "surface" ;
#                    emissions_CO:cell_methods = "time: mean" ;
#                    emissions_CO:grid_mapping = "latitude_longitude" ;
#                    emissions_CO:coordinates = "forecast_period forecast_reference_time" ;
#            int latitude_longitude ;
#                    latitude_longitude:grid_mapping_name = "latitude_longitude" ;
#                    latitude_longitude:longitude_of_prime_meridian = 0. ;
#                    latitude_longitude:earth_radius = 6371229. ;
#            double time(time) ;
#                    time:axis = "T" ;
#                    time:bounds = "time_bnds" ;
#                    time:units = "hours since 1970-01-01 00:00:00" ;
#                    time:standard_name = "time" ;
#                    time:calendar = "360_day" ;
#            double time_bnds(time, bnds) ;
#            int model_level_number(model_level_number) ;
#                    model_level_number:axis = "Z" ;
#                    model_level_number:units = "metre" ;
#                    model_level_number:standard_name = "model_level_number" ;
#                    model_level_number:long_name = "height at theta layer midpoint" ;
#                    model_level_number:positive = "up" ;
#            float latitude(latitude) ;
#                    latitude:axis = "Y" ;
#                    latitude:bounds = "latitude_bnds" ;
#                    latitude:units = "degrees_north" ;
#                    latitude:standard_name = "latitude" ;
#            float latitude_bnds(latitude, bnds) ;
#            float longitude(longitude) ;
#                    longitude:axis = "X" ;
#                    longitude:bounds = "longitude_bnds" ;
#                    longitude:units = "degrees_east" ;
#                    longitude:standard_name = "longitude" ;
#            double longitude_bnds(longitude, bnds) ;
#            double forecast_period ;
#                    forecast_period:bounds = "forecast_period_bnds" ;
#                    forecast_period:units = "hours" ;
#                    forecast_period:standard_name = "forecast_period" ;
#            double forecast_period_bnds(bnds) ;
#            double forecast_reference_time(time) ;
#                    forecast_reference_time:units = "hours since 1970-01-01 00:00:00" ;
#                    forecast_reference_time:standard_name = "forecast_reference_time" ;
#                    forecast_reference_time:calendar = "360_day" ;
#    
#    // global attributes:
#                    :emission_type = "2" ;
#                    :source = "Data from Met Office Unified Model" ;
#                    :um_version = "7.3" ;
#                    :update_freq_in_hours = "120" ;
#                    :update_type = "2" ;
#                    :Conventions = "CF-1.5" ;
#    }
#
#  so the metadata of our new emissions file needs to be edited to be what UKCA
#  expects.
#
#  After using this script, the resultant netCDF file should look like:
#
#    netcdf ukca_emiss_ALICE {
#    dimensions:
#            time = 12 ;
#            model_level_number = 1 ;
#            latitude = 72 ;
#            longitude = 96 ;
#            bnds = 2 ;
#    variables:
#            float emissions_ALICE(time, model_level_number, latitude, longitude) ;
#                    emissions_ALICE:_FillValue = 1.e+20f ;
#                    emissions_ALICE:long_name = "ALICE surf emissions" ;
#                    emissions_ALICE:units = "kg m-2 s-1" ;
#                    emissions_ALICE:missing_value = 1.e+20 ;
#                    emissions_ALICE:tracer_name = "ALICE" ;
#                    emissions_ALICE:vertical_scaling = "surface" ;
#                    emissions_ALICE:cell_methods = "time: mean" ;
#                    emissions_ALICE:grid_mapping = "latitude_longitude" ;
#                    emissions_ALICE:coordinates = "forecast_period forecast_reference_time" ;
#            int latitude_longitude ;
#                    latitude_longitude:grid_mapping_name = "latitude_longitude" ;
#                    latitude_longitude:longitude_of_prime_meridian = 0. ;
#                    latitude_longitude:earth_radius = 6371229. ;
#            double time(time) ;
#                    time:axis = "T" ;
#                    time:units = "hours since 1970-01-01" ;
#                    time:standard_name = "time" ;
#                    time:long_name = "Time" ;
#                    time:calendar = "360_day" ;
#                    time:time_origin = "01-JAN-1960:00:00:00" ;
#            int model_level_number(model_level_number) ;
#                    model_level_number:axis = "Z" ;
#                    model_level_number:units = "1" ;
#                    model_level_number:standard_name = "model_level_number" ;
#                    model_level_number:positive = "up" ;
#            double latitude(latitude) ;
#                    latitude:axis = "Y" ;
#                    latitude:bounds = "latitude_bnds" ;
#                    latitude:units = "degrees_north" ;
#                    latitude:standard_name = "latitude" ;
#            double latitude_bnds(latitude, bnds) ;
#            double longitude(longitude) ;
#                    longitude:axis = "X" ;
#                    longitude:bounds = "longitude_bnds" ;
#                    longitude:units = "degrees_east" ;
#                    longitude:standard_name = "longitude" ;
#            double longitude_bnds(longitude, bnds) ;
#            double forecast_period ;
#                    forecast_period:bounds = "forecast_period_bnds" ;
#                    forecast_period:units = "hours" ;
#                    forecast_period:standard_name = "forecast_period" ;
#            double forecast_period_bnds(bnds) ;
#            double forecast_reference_time(time) ;
#                    forecast_reference_time:bounds = "forecast_reference_time_bnds" ;
#                    forecast_reference_time:units = "hours since 1970-01-01" ;
#                    forecast_reference_time:standard_name = "forecast_reference_time" ;
#                    forecast_reference_time:calendar = "360_day" ;
#            double forecast_reference_time_bnds(time, bnds) ;
#    
#    // global attributes:
#                    :Conventions = "CF-1.5" ;
#                    :date = "01/01/60" ;
#                    :emission_type = "2" ;
#                    :history = "Tue Jun 18 14:32:42 BST 2013 - XCONV V1.92 16-February-2006" ;
#                    :invalid_standard_name = "tendency_of_atmosphere_mass_content_of_ALICE_due_to_emission" ;
#                    :name = "ALICE" ;
#                    :source = "UKCA Tutorial Task 5.1 - creating netCDF emissions" ;
#                    :time = "00:00" ;
#                    :title = "Emissions of ALICE in kg/m^2/s" ;
#                    :update_freq_in_hours = "120" ;
#                    :update_type = "2" ;
#                    :valid_max = 2.60646e-08f ;
#                    :valid_min = 0.f ;
#    }
