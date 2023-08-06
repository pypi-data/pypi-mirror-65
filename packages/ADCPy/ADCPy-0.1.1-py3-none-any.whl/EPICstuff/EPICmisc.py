# -*- coding: utf-8 -*-
"""
Conatiner for misc utilities
Created on Fri Oct 20 13:27:04 2017

catEPIC - concatenate like EPIC convention netCDF files, handle CF or EPIC time
        - files must be presented in the proper chronological order, this
          function will simply stick the data together in the order it is found

@author: mmartini USGS Woods Hole
"""

from netCDF4 import Dataset
from netCDF4 import num2date
import datetime as dt
import numpy as np
import math
import os
import sys
# this is important in order to import my package which is not on the python path
sys.path.append('c:\projects\python\ADCPy')
#from TRDIpd0tonetcdf import julian
#from TRDIpd0tonetcdf import ajd
#from ADCPcdf2ncEPIC import EPICtime2datetime

def s2hms(secs):
    hour = math.floor(secs/3600)
    mn = math.floor((secs % 3600)/60)
    sec = secs % 60
    return hour, mn, sec

def jdn(dto):
    # Given datetime object returns Julian Day Number
    year = dto.year
    month = dto.month
    day = dto.day

    not_march = month < 3
    if not_march:
        year -= 1
        month += 12

    fr_y = math.floor(year / 100)
    reform = 2 - fr_y + math.floor(fr_y / 4)
    jjs = day + (
        math.floor(365.25 * (year + 4716)) + math.floor(30.6001 * (month + 1)) + reform - 1524)

    return jjs

def ajd(dto):
    #Given datetime object returns Astronomical Julian Day.
    #Day is from midnight 00:00:00+00:00 with day fractional
    #value added.
    jdd = jdn(dto)
    day_fraction = dto.hour / 24.0 + dto.minute / 1440.0 + dto.second / 86400.0
    return jdd + day_fraction - 0.5

def cftime2EPICtime(timecount, timeunits):
    # take a CF time variable and convert to EPIC time and time2
    # timecountis the integer count of minutes (for instance) since the time stamp
    # given in timeunits
    buf = timeunits.split()
    t0 = dt.datetime.strptime(buf[2]+' '+buf[3], '%Y-%m-%d %H:%M:%S.%f')
    t0j = ajd(t0)
    # julian day for EPIC is the beginning of the day e.g. midnight
    t0j = t0j+0.5 # add 0.5 because ajd() subtracts 0.5 
    
    if buf[0] == 'hours':
        tj = timecount/(24)
    elif buf[0] == 'minutes':
        tj = timecount/(24*60)
    elif buf[0] == 'seconds':
        tj = timecount/(24*60*60)
    elif buf[0] == 'milliseconds':
        tj = timecount/(24*60*60*1000)
    elif buf[0] == 'microseconds':
        tj = timecount/(24*60*60*1000*1000)
        
    tj = t0j+tj
    
    time = math.floor(tj)
    time2 = math.floor((tj-time)*(24*3600*1000))
    
    return time, time2

def EPICtime2datetime(time,time2):
    # EPICtime2datetime(time,time2)
    # convert EPIC time and time2 to python datetime object
    
    # TODO - there is a rollover problem with this algorithm
    
    dtos = []
    gtime = []
    for idx in range(len(time)):
        # time and time2 are the julian day and milliseconds 
        # in the day as per PMEL EPIC convention for netcdf
        jd = time[idx]+(time2[idx]/(24*3600*1000))
        secs = (jd % 1)*(24*3600)
        
        j = math.floor(jd) - 1721119
        in1 = 4*j-1
        y = math.floor(in1/146097)
        j = in1 - 146097*y
        in1 = math.floor(j/4)
        in1 = 4*in1 +3
        j = math.floor(in1/1461)
        d = math.floor(((in1 - 1461*j) +4)/4)
        in1 = 5*d -3
        m = math.floor(in1/153)
        d = math.floor(((in1 - 153*m) +5)/5)
        y = y*100 +j
        mo=m-9
        yr=y+1
        if m<10:
            mo = m+3
            yr = y
        hour, mn, sec = s2hms(secs)
        ss = math.floor(sec)
        
        hund = math.floor((sec-ss)*100)

        gtime.append([yr, mo, d, hour, mn, ss, hund])

        # centiseconds * 10000 = microseconds
        dto = dt.datetime(yr, mo, d, hour, mn, ss, int(hund*10000))
        
        dtos.append(dto)

    return gtime, dtos

def resample_cleanup(datafiles):

    for filenum in range(len(datafiles)):
        
        pydata = datafiles[filenum]
        print('Working on file %s\n' % pydata)
        
        # re-open the dataset for numerical operations such as min and max
        # we have to make attribute changes, etc. so need to open with the netCDF package
        pyd = Dataset(pydata, mode="r+", format='NETCDF4')
        
        dkeys = pyd.dimensions.keys()
        
        # add minimum and maximum attributes and replace NaNs with _FillValue
        for key in pyd.variables.keys():
            if (key not in dkeys) & (key not in {'time','EPIC_time','EPIC_time2'}):
                data = pyd[key][:]
                nanidx = np.isnan(pyd[key][:])
                mn = np.min(data[~nanidx])
                mx = np.max(data[~nanidx])
                print('%s min = %f, max = %f' % (key, mn, mx))
                pyd[key].minimum = mn
                pyd[key].maximum = mx
                fill = pyd.variables[key].getncattr('_FillValue')
                data[nanidx] = fill
                pyd[key][:] = data
               
        # Add back EPIC time
        timecount = pyd['time']
        timeunits = pyd['time'].units
        #timecal = pyd['time'].calendar
        
        #time, time2 = cf2EPICtime(timecount,timeunits,'proleptic_gregorian')
        time, time2 = cftime2EPICtime(timecount,timeunits)
        print('first time = %7d and %8d' % (time[0],time2[0]))
        
        try:
            varobj = pyd.createVariable('EPIC_time','u4',('time'))
        except:
            print('EPIC_time exists, updating.')
            varobj = pyd['EPIC_time'] 
            
        varobj.units = "True Julian Day"
        varobj.epic_code = 624
        varobj.datum = "Time (UTC) in True Julian Days: 2440000 = 0000 h on May 23, 1968"
        varobj.NOTE = "Decimal Julian day [days] = time [days] + ( time2 [msec] / 86400000 [msec/day] )"  
        varobj[:] = time[:]
        
        try:
            varobj = pyd.createVariable('EPIC_time2','u4',('time'))
        except:
            print('EPIC_time2 exists, updating.')
            varobj = pyd['EPIC_time2']
                
        varobj.units = "msec since 0:00 GMT"
        varobj.epic_code = 624
        varobj.datum = "Time (UTC) in True Julian Days: 2440000 = 0000 h on May 23, 1968"
        varobj.NOTE = "Decimal Julian day [days] = time [days] + ( time2 [msec] / 86400000 [msec/day] )"   
        varobj[:] = time2[:]
        
        # re-compute DELTA_T in seconds
        dtime = np.diff(pyd['time'][:])
        dtm = dtime.mean().astype('float').round()
        u = timeunits.split()
        if u[0] == 'minutes':
            dtm = dtm*60
        elif u[0] == 'hours':
            dtm = dtm*60*60
        elif u[0] == 'milliseconds':
            dtm = dtm/1000
        elif u[0] == 'microseconds':
            dtm = dtm/1000000
        
        DELTA_T = '%d' % int(dtm)
            
        pyd.DELTA_T = DELTA_T
        print(DELTA_T)
        
        # check start and stop time
        pyd.start_time = '%s' % num2date(pyd['time'][0],pyd['time'].units)
        pyd.stop_time = '%s' % num2date(pyd['time'][-1],pyd['time'].units)
        print('cf start time %s' % pyd.start_time)
        print('cf stop time %s' % pyd.stop_time)
        
        # add the variable descriptions
        vardesc = ''
        for key in pyd.variables.keys():
            if key not in dkeys:
                vardesc = vardesc+':'+key
        
        vardesc = vardesc[1:]
        print(vardesc)
        pyd.VAR_DESC = vardesc
            
        pyd.close()    
        
        

def catEPIC(datafiles, outfile):
    
    nfiles = len(datafiles)
    
    # use the first file to establish some information
    nc0 = Dataset(datafiles[0], mode = 'r', format = 'NETCDF4')
    varnames = nc0.variables.keys()
    if 'time2' not in varnames: 
        CFtime = True
        if 'calendar' not in nc0['time'].__dict__:
            print('No calendar specified, using gregorian')
            nccalendar = 'gregorian'
        else:
            nccalendar = nc0['time'].calendar
    else:
        CFtime = False
    
    nc0.close()
           
    # now glean time information from all the files
    alldt = np.array([])
    timelens = []
    for ifile in range(nfiles):
        print(datafiles[ifile])
        nc = Dataset(datafiles[ifile], mode = 'r', format = 'NETCDF4')
        timelens.append(nc.dimensions['time'].size)
        if CFtime: 
            tobj = num2date(nc['time'][:],nc['time'].units,calendar=nccalendar)
            alldt = np.concatenate((alldt,tobj))
        else:
            tobj = EPICtime2datetime(nc['time'][:],nc['time2'][:])
            alldt = np.concatenate((alldt,tobj))
        
        print('file %d is %s to %s' % (ifile, tobj[0], tobj[-1]))
        print('   first time object nc[''time''][0] is %f' % nc['time'][0])
        print('   time units are %s' % nc['time'].units)
        #if 'corvert' in nc.variables.keys():
        #    print('   there is a corvert')
        nc.close()
        
    # it was the case in the MATLAB version that the schema technique
    # would reorder the variables - not sure python does this
    # reordering the variables might not be a problem here since they are 
    # iterated by name
    
    # dimensions
    ncid_out = Dataset(outfile, "w", clobber=True, format="NETCDF4")
    ncid_in = Dataset(datafiles[0], mode = 'r', format = 'NETCDF4')
    for dimname in ncid_in.dimensions.keys():
        if 'time' in dimname:
            ncid_out.createDimension('time',len(alldt))
        else:
            ncid_out.createDimension(dimname,ncid_in.dimensions[dimname].size)
    
    # global attributes
    for attname in ncid_in.__dict__:
        ncid_out.setncattr(attname,ncid_in.getncattr(attname))
    
    # variables with their attributes
    for varname in ncid_in.variables.keys():
        print('Creating %s as %s' % (varname, ncid_in[varname].datatype))
        ncid_out.createVariable(varname, ncid_in[varname].datatype, 
                            dimensions = ncid_in[varname].dimensions)
        for attname in ncid_in[varname].__dict__:
            ncid_out[varname].setncattr(attname, ncid_in[varname].getncattr(attname))
            
    ncid_out.close()
    ncid_in.close()
        
    # load the data
    ncid_out = Dataset(outfile, mode='r+', format="NETCDF4")
    print(timelens)
    for ifile in range(nfiles):
        if ifile == 0: 
            outidx_start = 0
            outidx_end = outidx_start+timelens[ifile]
        else:
            outidx_start = outidx_end
            outidx_end = outidx_start+timelens[ifile]
        print('getting data from file %s and writing %d to %d (pythonic indeces)' % (datafiles[ifile],outidx_start,outidx_end))
        ncid_in = Dataset(datafiles[ifile], mode="r", format="NETCDF4")
        # TODO - check for the variable int he outfile
        for varname in ncid_in.variables.keys():
            dimnames = ncid_in[varname].dimensions
            if 'time' in dimnames:
                s = outidx_start
                e = outidx_end
            else:
                s = 0
                e = len(ncid_in[varname])
            ndims = len(ncid_in[varname].dimensions)
            #print('%s, %d' % (varname, ndims))
            #print(len(ncid_in[varname]))
            if ndims == 1:
                ncid_out[varname][s:e] = ncid_in[varname][:]
            elif ndims == 2:
                ncid_out[varname][s:e,:] = ncid_in[varname][:,:]
            elif ndims == 3:
                ncid_out[varname][s:e,:,:] = ncid_in[varname][:,:,:]
            elif ndims == 4:
                ncid_out[varname][s:e,:,:,:] = ncid_in[varname][:,:,:,:]                        
        ncid_in.close()
    
    # finally, put the correct time span in th output file
    units = "seconds since %d-%d-%d %d:%d:%f" % (alldt[0].year, 
        alldt[0].month,alldt[0].day,alldt[0].hour,alldt[0].minute,
        alldt[0].second+alldt[0].microsecond/1000000)
    # the 0:00 here was causing problems for xarray
    units = "seconds since %d-%d-%d %d:%d:%f +0:00" % (alldt[0].year, 
        alldt[0].month,alldt[0].day,alldt[0].hour,alldt[0].minute,
        alldt[0].second+alldt[0].microsecond/1000000)
    elapsed = alldt-alldt[0] # output is a numpy array of timedeltas
    # have to iterate to get at the timedelta objects in the numpy container
    # seems crazy, someone please show me a better trick!
    elapsed_sec = []
    for e in elapsed:  elapsed_sec.append(e.total_seconds())
    t = np.zeros((len(alldt),1))
    t2 = np.zeros((len(alldt),1))
    for i in range(len(alldt)): 
        jd = ajd(alldt[i])
        t[i] = int(math.floor(jd))
        t2[i] = int((jd - math.floor(jd))*(24*3600*1000))
    if CFtime:
        ncid_out['time'][:] = elapsed_sec[:]
        ncid_out['time'].units = units
        ncid_out['EPIC_time'][:] = t[:]
        ncid_out['EPIC_time2'][:] = t2[:]
    else:
        ncid_out['CFtime'][:] = elapsed_sec[:]
        ncid_out['CFtime'].units = units
        ncid_out['time'][:] = int(math.floor(jd))
        ncid_out['time2'][:] = int((jd - math.floor(jd))*(24*3600*1000))
    
    # recompute start_time and end_time
    ncid_out.start_time = '%s' % num2date(ncid_out['time'][0],ncid_out['time'].units)
    print(ncid_out.start_time)
    ncid_out.stop_time = '%s' % num2date(ncid_out['time'][-1],ncid_out['time'].units)
    print(ncid_out.stop_time)
    
    # TODO update history
    
    ncid_out.close()
	
def check_FillValue_encoding(ds):
    # restore encoding to what it needs to be for EPIC and CF compliance
    # input
    # ds = xarray Dataset whose variables' encoding will be examined for the correct _FillValue
    # output 
    # ds = Dataset with corrected encoding
    # encoding_dict = encoding that can be used with to_netcdf
    encoding_dict = {}
    
    for var in ds.variables.items():
        encoding_dict[var[0]] = ds[var[0]].encoding
        
        # is it a coordinate?
        if var[0] in ds.coords:
            # coordinates do not have a _FillValue
            if '_FillValue' in var[1].encoding:
                encoding_dict[var[0]]['_FillValue'] = False
        else:
            # _FillValue cannot be NaN and must match the data type
            # so just make sure it matches the data type.
            # xarray changes ints to floats, not sure why yet
            if ('_FillValue' in var[1].encoding):
                if np.isnan(var[1].encoding['_FillValue']):
                    print('NaN found in _FillValue, correcting')
                    
                if var[1].encoding['dtype'] in {'float32','float64'}:
                    var[1].encoding['_FillValue'] = 1E35
                    encoding_dict[var[0]]['_FillValue'] = 1E35
                elif var[1].encoding['dtype'] in {'int32','int64'}:
                    var[1].encoding['_FillValue'] = 32768
                    encoding_dict[var[0]]['_FillValue'] = 32768
            
    return ds, encoding_dict
            
    
def __main():
    print('%s running on python %s' % (sys.argv[0], sys.version))
	
    if len(sys.argv) < 2:
        print("%s useage:" % sys.argv[0])
        print("catEPIC file_list outfile\n" )
        sys.exit(1)
        
    try:
        datafiles = sys.argv[1]
    except:
        print('error - input file list missing')
        sys.exit(1)
        
    try:
        outfile = sys.argv[2]
    except:
        print('error - output file name missing')
        sys.exit(1)
        
    # some input testing
    if ~os.path.isfile(datafiles[0]):
        print('error - input file not found')
        sys.exit(1)
        
    if ~os.path.isfile(outfile):
        print('%s will be overwritten' % outfile)
    
    print('Start concatination at ',dt.datetime.now())
    
    catEPIC(datafiles, outfile)
    
    print('Finished file concatination at ',dt.datetime.now())
 
if __name__ == "__main__":
    __main()        
    