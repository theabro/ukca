#!/usr/bin/env python
# coding: utf-8

# ## Plot comparisons of total column ozone for specific months
# 
# Plots from the CCMI simulations.

# In[1]:


import cf
import cfplot as cfp
import numpy as np


# In[2]:


# define the locations of the various datasets
# CCMI2022 refD1 ensemble
ensdata='/home/ubuntu/Tutorials/UMvn13.0/data/toz_Amon_UKESM1-StratTrop_refD1_r?i1p1f2_gn_19600101-20190101.nc'
# CCMI1 refC1
ccmidata='/home/ubuntu/Tutorials/UMvn13.0/data/toz_monthly_UMUKCA-UCAM_refC1_r1i1p1_*.nc'
# UKCA model data from ACSIS project, nudged to ERA5
ukcadata='/home/ubuntu/Tutorials/UMvn13.0/data/u-*/apm.pp/*.pp'
# Bodeker Scientific TCO dataset - https://www.bodekerscientific.com/data/total-column-ozone
# this has been preprocessed into a single file using ncks, ncatted, and ncrcat
# for i in `ls *.nc`; do echo $i; ncks -O --mk_rec_dmn time $i $i; done
# for i in `ls *.nc`; do echo $i; ncatted -O -a created,global,d,, $i; done
# for i in `ls *.nc`; do echo $i; ncatted -O -a units,longitude,o,c,degrees_east $i; done
# for i in `ls *.nc`; do echo $i; ncatted -O -a units,latitude,o,c,degrees_north $i; done
# ncrcat BSFilledTCO_V3.4.1_????_Monthly.nc ../BSFilledTCO_V3.4.1_Monthly.nc
obsdata='/home/ubuntu/Tutorials/UMvn13.0/data/Bodeker_3.4.1/*.nc'
# We would like to thank Bodeker Scientific, funded by the New Zealand Deep South National 
# Science Challenge, for providing the combined NIWA-BS total column ozone database.


# In[3]:


# read-in the data
# 3x ensemble members for CCMI2022
inens=cf.read(ensdata, select='equivalent_thickness_at_stp_of_atmosphere_ozone_content')

# 10-year files for CCMI1
ccmi=cf.read(ccmidata, select='equivalent_thickness_at_stp_of_atmosphere_ozone_content')[0]


# In[4]:


# want to look at the 1995-2005 range, and produce a monthly climatology
ccmi_2000 = ccmi.collapse('T: mean within years T: mean over years', within_years=cf.M(), over_years=cf.year(cf.wi(1995, 2005)))


# In[5]:


# CCMI2022 data is in units of m rather than Dobson units, so will need to convert
duconv=1.0e5
# ensemble from CCMI2022
ens=cf.FieldList()
for f in inens:
    # delete auxillary coordinates as these might cause problems with some operations
    f.del_construct('forecast_period')
    f.del_construct('forecast_reference_time')
    # convert to DU for this set of data
    f.data=f.data/duconv
    f.override_units('DU', inplace=True)
    # produce the climatology
    g=f.collapse('T: mean within years T: mean over years', within_years=cf.M(), over_years=cf.year(cf.wi(1995, 2005)))
    # append to new field list
    ens.append(g)


# In[6]:


# calculate ensemble mean
s=list(ens[0].data.shape)
s.append(len(ens))
arr=np.zeros(s)
for i in range(len(ens)):
    arr[:,:,:,i]=ens[i].array[:,:,:]
darr=np.mean(arr,axis=3)
ensmean=ens[0].copy()
ensmean.data=darr


# In[7]:


# choose a month to plot, e.g. March=2, September=8 (python counts from 0)
imonth=2


# In[8]:


# set the levels to use
cfp.levs(min=180, max=440, step=20)


# In[9]:


cfp.gopen()
cfp.mapset(proj='npstere', boundinglat=30, lon_0=0)
# can only do titles for NH plots currently
cfp.con(ccmi_2000[imonth,:,:], lines=False, title='CCMI1 Y2000 Climatological Total Column Ozone (DU)')
cfp.gclose()


# In[10]:


cfp.gopen()
cfp.mapset(proj='npstere', boundinglat=30, lon_0=0)
# can only do titles for NH plots currently
cfp.con(ensmean[imonth,:,:], lines=False, title='CCMI2022 Y2000 Ensemble Mean Climatological Total Column Ozone (DU)')
cfp.gclose()


# In[11]:


# calculate differences for CCMI2022 ensemble members
ens_abs=cf.FieldList()
ens_pc=cf.FieldList()
for f in ens:
    # absolute
    diff_abs=f.copy()
    diff_abs.data=f.data - ensmean.data
    ens_abs.append(diff_abs)
    # percentage
    diff_pc=f.copy()
    diff_pc.data=100.0*((f.data - ensmean.data)/f.data)
    diff_pc.override_units('%', inplace=True)
    ens_pc.append(diff_pc)


# In[12]:


# reset levels
cfp.levs()


# In[13]:


for f in ens_abs:
    cfp.cscale(scale='BlWhRe')
    cfp.mapset(proj='npstere', boundinglat=30, lon_0=0)
    cfp.con(f[imonth,:,:], lines=False)


# In[14]:


for f in ens_pc:
    cfp.cscale(scale='BlWhRe')
    cfp.mapset(proj='npstere', boundinglat=30, lon_0=0)
    cfp.con(f[imonth,:,:], lines=False)


# In[ ]:




