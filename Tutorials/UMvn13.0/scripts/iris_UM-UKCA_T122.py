#!/usr/bin/env python
# coding: utf-8

# In[1]:


import iris
import iris.quickplot as qplt
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


# change to your suite-id to pick up the required file
runid='cq988'
datafile='/home/vagrant/cylc-run/u-'+runid+'/work/1/atmos/atmosa.pa19810901_00'


# In[3]:


# constraint on time to get 2nd radiation timestep
tconstr=iris.Constraint(time=lambda cell: cell.point.hour == 2)


# In[4]:


# load all AOD components at 0.55 micron
aod=iris.load(datafile,[
    iris.Constraint(pseudo_level=3) & iris.AttributeConstraint(STASH='m01s02i285') & tconstr,
    iris.Constraint(pseudo_level=3) & iris.AttributeConstraint(STASH='m01s02i300') & tconstr,
    iris.Constraint(pseudo_level=3) & iris.AttributeConstraint(STASH='m01s02i301') & tconstr,
    iris.Constraint(pseudo_level=3) & iris.AttributeConstraint(STASH='m01s02i302') & tconstr,
    iris.Constraint(pseudo_level=3) & iris.AttributeConstraint(STASH='m01s02i303') & tconstr,
    iris.Constraint(pseudo_level=3) & iris.AttributeConstraint(STASH='m01s02i304') & tconstr,
    iris.Constraint(pseudo_level=3) & iris.AttributeConstraint(STASH='m01s02i305') & tconstr])


# In[5]:


# make cube to store total AOD
aodsum=aod[0].copy()
aodsum.data=np.zeros(aodsum.data.shape)

# add-up components
aodsum.data=aod[0].data+aod[1].data+aod[2].data+aod[3].data+aod[4].data+aod[5].data+aod[6].data

# rename
aodsum.rename('atmosphere_optical_thickness_due_to_aerosol')


# In[6]:


qplt.pcolormesh(aodsum)
plt.gca().coastlines(color='w')


# In[7]:


# output to netCDF
iris.save(aodsum,'/home/vagrant/iris_Task122_AOD.nc',netcdf_format='NETCDF4')


# In[ ]:




