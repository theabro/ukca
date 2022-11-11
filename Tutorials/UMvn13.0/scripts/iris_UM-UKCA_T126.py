#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import iris
import iris.quickplot as qplt
import numpy as np
import matplotlib.pyplot as plt


# In[ ]:


# read-in fields including Sec_Org product
aod_122=iris.load_cube('/home/vagrant/iris_Task122_AOD.nc','atmosphere_optical_thickness_due_to_aerosol')
ssa_123=iris.load_cube('/home/vagrant/iris_Task123_SSA.nc','single_scattering_albedo_in_air_due_to_ambient_aerosol_particles')
toa_124=iris.load_cube('/home/vagrant/iris_Task124_TOA.nc','toa_net_downward_radiative_flux')


# In[ ]:


# read-in fields without Sec_Org product
aod_126=iris.load_cube('/home/vagrant/iris_Task126_AOD.nc','atmosphere_optical_thickness_due_to_aerosol')
ssa_126=iris.load_cube('/home/vagrant/iris_Task126_SSA.nc','single_scattering_albedo_in_air_due_to_ambient_aerosol_particles')
toa_126=iris.load_cube('/home/vagrant/iris_Task126_TOA.nc','toa_net_downward_radiative_flux')


# In[ ]:


# difference the respective fields
aoddiff=aod_126.copy()
aoddiff.data=np.zeros(aoddiff.data.shape)
aoddiff.data=aod_126.data-aod_122.data

ssadiff=ssa_126.copy()
ssadiff.data=np.zeros(ssadiff.data.shape)
ssadiff.data=ssa_126.data-ssa_123.data

toadiff=toa_126.copy()
toadiff.data=np.zeros(toadiff.data.shape)
toadiff.data=toa_126.data-toa_124.data


# In[ ]:


# save the differences for viewing later
iris.save(aoddiff, '/home/vagrant/iris_Task126_AOD_diff.nc', netcdf_format='NETCDF4')
iris.save(ssadiff, '/home/vagrant/iris_Task126_SSA_diff.nc', netcdf_format='NETCDF4')
iris.save(toadiff, '/home/vagrant/iris_Task126_TOA_diff.nc', netcdf_format='NETCDF4')


# In[ ]:


# plot the AOD
qplt.pcolormesh(aoddiff)
plt.gca().coastlines()


# In[ ]:


# plot the SSA
qplt.pcolormesh(ssadiff)
plt.gca().coastlines()


# In[ ]:


# plot the TOA
qplt.pcolormesh(toadiff)
plt.gca().coastlines()


# In[ ]:




