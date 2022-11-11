#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cf
import cfplot as cfp
import numpy as np


# In[2]:


# read-in fields including Sec_Org product
aod_122=cf.read('/home/vagrant/Task122_AOD.nc',select='atmosphere_optical_thickness_due_to_aerosol')[0]
ssa_123=cf.read('/home/vagrant/Task123_SSA.nc',select='single_scattering_albedo_in_air_due_to_ambient_aerosol_particles')[0]
toa_124=cf.read('/home/vagrant/Task124_TOA.nc',select='toa_net_downward_radiative_flux')[0]


# In[3]:


# read-in fields without Sec_Org product
aod_126=cf.read('/home/vagrant/Task126_AOD.nc',select='atmosphere_optical_thickness_due_to_aerosol')[0]
ssa_126=cf.read('/home/vagrant/Task126_SSA.nc',select='single_scattering_albedo_in_air_due_to_ambient_aerosol_particles')[0]
toa_126=cf.read('/home/vagrant/Task126_TOA.nc',select='toa_net_downward_radiative_flux')[0]


# In[4]:


# difference the respective fields
aoddiff=aod_126-aod_122
ssadiff=ssa_126-ssa_123
toadiff=toa_126-toa_124


# In[5]:


# save the differences for viewing later
cf.write(aoddiff, '/home/vagrant/Task126_AOD_diff.nc', fmt='NETCDF4')
cf.write(ssadiff, '/home/vagrant/Task126_SSA_diff.nc', fmt='NETCDF4')
cf.write(toadiff, '/home/vagrant/Task126_TOA_diff.nc', fmt='NETCDF4')


# In[6]:


# plot the AOD
cfp.con(aoddiff, blockfill_fast=True, lines=False, title='Difference in Aerosol Optical Depth at 550nm')


# In[7]:


# plot the SSA
cfp.con(ssadiff, blockfill_fast=True, lines=False, title='Difference in Single Scattering Albedo at 550nm')


# In[8]:


# plot the TOA
cfp.con(toadiff, blockfill_fast=True, lines=False, title='Difference in Top of Atmosphere Net Downward Radiative Flux')


# In[ ]:




