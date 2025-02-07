########## Min/Max uvdist (in lambda) from MS data ########
# Written by Ramij Raja.
# Date: 06th Feb 2025
######################################
# RUN within CASA
######################################

import numpy as np
import scipy.constants as const

vis = raw_input("Enter MS name: ")
vis = vis.rstrip('/')

# Load data from MS
ms.open(vis)
datadict = ms.getdata(['UVW', 'FLAG'])
ax = ms.getdata(["axis_info"])
ms.close()

# Extract individual data columns
uvw = datadict['uvw'].squeeze()

flags = datadict['flag'].squeeze()

# Channel frequencies
cf = ax["axis_info"]["freq_axis"]["chan_freq"].squeeze()

# 1 over lambda (m^-1)
lambda_inv = cf/const.c

# Now multiply the lambda_inv to u, v data to convert in units of lambda
u = uvw[0]
v = uvw[1]

ul = np.outer(lambda_inv, u)
vl = np.outer(lambda_inv, v)

# Nan the flag u, v data points
ul[flags] = np.nan
vl[flags] = np.nan

# Calculate uvdist in lambda
uvd = np.sqrt(ul**2 + vl**2)

print('Min uv-lambda: {0:4.1f} (lambda), Max uv-lambda: {1:4.1f} (kilo-lambda)'.format(np.nanmin(uvd), np.nanmax(uvd)/1000.))


# The End!




