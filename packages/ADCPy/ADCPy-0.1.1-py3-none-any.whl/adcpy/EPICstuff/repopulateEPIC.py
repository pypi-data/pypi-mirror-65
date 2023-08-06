# -*- coding: utf-8 -*-
"""
repopulateEPIC
==============
Distribute burst data output from reshapeEPIC along the sample dimension

a burst shaped file output from reshapeEPIC will have two issues that need
to be addressed before the data can be used with xarray::

    -- reshape time to be one dimension
    -- make sure the samples within each burst are index according to their
    time stamps.  Within burst time stamps will not be preserved

Usage:
    python repopulateEPIC.py shaped_file new_file sample_rate [start='left'] [drop = None]

    :param str shaped_file: output from reshapeEPIC, the expected shape of the data is one of::
        [time, sample]
        [time, sample, depth]
        [time, sample, depth, lat, lon]

    :param str new_file: a new file with the adjusted time, this file, if it exists, will be overwritten
    :param int sample_rate: the sample rate the instrument was intended to use during each burst, in seconds
    :param str start: what the time stamp should be for each burst::
        left = beginning of the burst based on the first sample time
        center = middle of the burst based on first sample and last sample times
        right = end of the burst based on the last sample time
    :param list drop: variable names to omit from the output file


Created on Wed Oct  3 15:21:53 2018
@author: mmartini
"""

# 10/15/2018 MM was using np.nan to pre-fill arrays and this was causing
# NaNs in final output, a problem for CF.  Replace np.nan with _FillValue

import os
import sys
import datetime as dt
import netCDF4 as nc
import numpy as np


def repopulateEPIC(*args, **kwargs):
    # the argument passing here works fine
    print('%s running on python %s' % (sys.argv[0], sys.version))
    print('Start file conversion at ', dt.datetime.now())

    shaped_file = args[0]
    new_file = args[1]
    sample_rate = args[2]        
    if 'start' in kwargs.keys():  
        start = kwargs['start']    
    else:
        start = 'left'
    if 'drop' in kwargs.keys():  
        drop = kwargs['drop']  
    else:
        drop = {}

    for key, value in kwargs.items():
        print('{} = {}'.format(key, value))

    print('Start file conversion at ', dt.datetime.now())
    
    # check for the output file's existence before we try to delete it.
    try:
        os.remove(new_file)
        print('{} removed'.format(new_file))
    except FileNotFoundError:
        pass    

    shapedcdf = nc.Dataset(shaped_file, format="NETCDF4")
    
    ndims = len(shapedcdf.dimensions)
    print(ndims)
    nvars = len(shapedcdf.variables)
    print(nvars)
    # shapedcdf.getncattr('sensor_type')
    ngatts = len(shapedcdf.ncattrs())
    print(ngatts)    
    
    newcdf = nc.Dataset(new_file, mode="w", clobber=True, format='NETCDF4')
    
    newcdf.set_fill_off()
    
    # copy the global attributes
    # first get a dict of them so that we can iterate
    gatts = {}
    for attr in shapedcdf.ncattrs():
        gatts[attr] = getattr(shapedcdf, attr)
            
    gatts['history'] = getattr(shapedcdf, 'history')+'; distributing time using redistributeSamples.py'
    
    newcdf.setncatts(gatts)
    
    for item in shapedcdf.dimensions.items():
        print('Defining dimension {} which is {} long'.format(item[0], len(item[1])))
        newcdf.createDimension(item[0], len(item[1]))

    # this is the dimension along which we will redistribute the burst samples
    # this is also the dimension we will drop from 'time'
    dim = 'sample' 
    for var in shapedcdf.variables.items():
        varobj = var[1]
        try:
            fill_value = varobj.getncattr('_FillValue')
        except AttributeError:
            fill_value = False  # do not use None here!!!
            
        print('{} is data type {} with fill {}'.format(varobj.name, varobj.dtype,
              fill_value))
        
        if varobj.name not in drop:  # are we copying this variable?
            if varobj.name == 'time':  # is this time which we need to drop a dimension?
                vdims_shaped = varobj.dimensions
                vdims_new = []
                for d in vdims_shaped:
                    if d == dim:
                        print('\tskipping sample in {}'.format(varobj.name))
                    else:
                        vdims_new.append(d)
                        
                newvarobj = newcdf.createVariable(varobj.name, varobj.dtype, tuple(vdims_new), fill_value=fill_value)
            else:
                # for a normal copy, no dimension drop
                newvarobj = newcdf.createVariable(varobj.name, varobj.dtype, varobj.dimensions, fill_value=fill_value)
                
            print('\t{} to {}'.format(varobj.dimensions, newvarobj.dimensions))
                
            # copy the variable attributes
            # first get a dict of them so that we can iterate
            vatts = {}
            for attr in varobj.ncattrs():
                vatts[attr] = getattr(varobj, attr)
    
            try:
                newvarobj.setncatts(vatts)
            except AttributeError:
                print('Unable to copy atts for {}'.format(varobj.name))    

    # --------------- populate the data

    # time is special, take care of it after time is populated
    # we know because we are doing this that it is [time, sample]
    if start == 'right':
        print('copying time, using the last time stamp in each burst')
        newcdf['time'][:] = shapedcdf['time'][:, -1]
    # TODO -- bring into the loop and implement
    # elif start == 'center':
    #    print('copying time, using the middle in each burst')
    #    #t = 
    #    i = int(np.floor(len(shapedcdf['time'][0,:]/2)))
    #    newcdf['time'][:] = shapedcdf['time'][:,-1]    
    else:
        print('copying time, using the first time stamp in each burst')
        newcdf['time'][:] = shapedcdf['time'][:, 0]

    drop = {'time'}  # we have already done time
    nbursts = len(newcdf['time'])
    
    # Note we are dependent on the shape [time, sample, depth, lat, lon]
    for svar in shapedcdf.variables.items():
        varname = svar[1].name
        print('{} is data type {}'.format(svar[0], svar[1].dtype))
        if varname not in drop:        
            ndims = len(svar[1].dimensions)
            print('\t{} dims to {} dims'.format(shapedcdf[varname].shape, newcdf[varname].shape))
            
            if ('time' in svar[1].dimensions) and ('sample' in svar[1].dimensions):
                print('\tdistributing samples, iterating through bursts')
                
                try:
                    fill_value = svar[1].getncattr('_FillValue')
                except AttributeError:
                    fill_value = None
                    
                for iburst in range(nbursts):
    
                    # get the data
                    if ndims == 2:
                        data = shapedcdf[varname][iburst, :]
                    elif ndims == 3:
                        data = shapedcdf[varname][iburst, :, :]
                    elif ndims == 4:
                        data = shapedcdf[varname][iburst, :, :, :]
                    elif ndims == 5:
                        data = shapedcdf[varname][iburst, :, :, :, :]
                    else:
                        data = None
                        if iburst == 0:
                            print('{} dims found - too many'.format(ndims))
                            # TODO:  what do we do when this fails?
    
                    if iburst == 0 and data is not None:
                        print('\t data is {}'.format(data.shape))

                    # do not need to iterate over depth if shapes are correct!
                    # set up the index using the time stamps
                    t = shapedcdf['time'][iburst, :]
                    tidx = np.array(t-t[0])*sample_rate
                    # incoming data is represented as NaN, how we find them
                    tidxgood = ~np.isnan(tidx)
    
                    # reset the new container, same shape as old data
                    # new_data = np.full(data.shape,np.nan) # don't use NaN!
                    new_data = np.full(data.shape, fill_value)
                    
                    # need an integer representation of the indices
                    # to make this assignment work:  new_data[idxasint] = data[tidxgood]
                    idxasint = tidx[tidxgood].astype(int)
    
                    # different index types because these are different values
                    if iburst == 0:
                        print('\tnumber of dimensions = {}'.format(ndims))
    
                    if ndims == 2:
                        new_data[idxasint] = data[tidxgood]
                        newcdf[varname][iburst, :] = new_data
                    elif ndims == 3:
                        new_data[idxasint, :] = data[tidxgood, :]
                        newcdf[varname][iburst, :, :] = new_data
                    elif ndims == 4:
                        new_data[idxasint, :, :] = data[tidxgood, :, :]
                        newcdf[varname][iburst, :, :, :] = new_data
                    elif ndims == 5:
                        new_data[idxasint, :, :, :] = data[tidxgood, :, :, :]
                        newcdf[varname][iburst, :, :, :, :] = new_data
            # no need to redistribute time
            else:  # if 'time' not in svar[1].dimensions:
                print('\tno time and sample combination found, simple copy')
                if ndims == 1:
                    newcdf[varname][:] = shapedcdf[varname][:]
                elif ndims == 2:
                    newcdf[varname][:, :] = shapedcdf[varname][:, :]
                elif ndims == 3:
                    newcdf[varname][:, :, :] = shapedcdf[varname][:, :, :]
                elif ndims == 4:
                    newcdf[varname][:, :, :, :] = shapedcdf[varname][:, :, :, :]
                elif ndims == 5:
                    newcdf[varname][:, :, :, :, :] = shapedcdf[varname][:, :, :, :, :]
                else:
                    print('Not coded for more than 5 dimensions')
                
            print('\n')
                
    shapedcdf.close()
    newcdf.close()
    
    print('Finished writing new file {}'.format(new_file))
    

def __main():

    print('%s running on python %s' % (sys.argv[0], sys.version))
    if len(sys.argv) < 3:
        print(__doc__)
        return

    try:
        shaped_file = sys.argv[1]
    except:
        print('error - shaped netCDF input file name missing')
        sys.exit(1)

    try:
        new_file = sys.argv[2]
    except:
        print('error - output file name missing')
        sys.exit(1)

    try:
        sample_rate = sys.argv[3]
    except:
        print('error - sample_rate missing')
        sys.exit(1)

    print('repopulating {} to {} with {} sample_rate'.format(shaped_file, new_file, sample_rate))

    repopulateEPIC(shaped_file, new_file, sample_rate, sys.argv[4:])


if __name__ == "__main__":
    __main()
