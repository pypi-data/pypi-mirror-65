'''
Created on Jan 31, 2019

@author: reynolds
'''

from wrtdk.parser.parser import parser
import sys, os, re, utm
import numpy as np

class gcs(object):
    ''' handles gcs coordinates '''
    
    def dm2dd(self,dm,direction):
        '''  Converts a geographic coordiante given in "degres/minutes" dddmm.mmmm
        format (ie, "12319.943281" = 123 degrees, 19.953281 minutes) to a signed
        decimal (python float) format '''
        # '12319.943281'
        if not dm or dm == '0': return 0.
        d, m = re.match(r'^(\d+)(\d\d\.\d+)$', dm).groups()
        value = float(d) + float(m) / 60
        
        if direction == 'N' or direction == 'E': return value
        elif direction == 'S' or direction == 'W': return -value
        else: return np.NaN
        
    def dd2dm(self,dd=0,direction='latitude'):
        d,m = divmod(abs(dd),1)
        m *= 60
        
        if direction is 'latitude':
            if dd >= 0: return (d,m,'N')
            else: return (d,m,'S')
        else:
            if dd >= 0: return (d,m,'E')
            else: return (d,m,'W')
            
class utc_time(object):
    
    def s2dms(self,s=0):
        d,m = divmod(s,3600)
        m,s = divmod(m,60)
        return (d,m,s)
        
    def dms2s(self,dms):
        return float(dms[0:2])*3600 + float(dms[2:4])*60 + float(dms[4:])
    
class nmea_parser(parser):
    
    def __init__(self):
        super().__init__()
        
    def checksum(self,msg=b''):
        _sum = 0
        for b in msg: _sum ^=b
        return (hex(_sum).split('x')[-1].upper().encode(),_sum)

class gpgga(nmea_parser):
    ''' $GPGGA sentence parser '''
    
    BYTES = type(bytes())
    
    def __init__(self):
        ''' Constructor '''
        super().__init__()
        self.reset()
        self._gcs = gcs()
        self._utc = utc_time()
    
    def reset(self):
        ''' resets the parser '''
        self._time = self._nan()
        self._timestamp = '00:00:00.00'
        self._lat = self._nan()
        self._lon = self._nan()
        self._fix = self._minus1()
        self._n = self._minus1()
        self._easting = self._nan()
        self._northing = self._nan()
        self._region = self._minus1()
        self._zone = ''
        self._dop = self._nan()
        self._alt = self._nan()
        self._geoid = self._nan()
        
    def get(self,talker_id=b'$GPGGA',time=0,latitude=0,longitude=0,
            fix=0,nsat=0,dop=100,altitude=0,geoid=0,t_dgps=None):
        
        msg = b''
        
        if type(talker_id) != self.BYTES: talker_id = talker_id.encode()
        msg += talker_id
        
        utc_d,utc_m,utc_s = self._utc.s2dms(time)
        msg += b',%02d%02d%02.2f'%(utc_d,utc_m,utc_s)
        
        lat_d,lat_m,lat_dir = self._gcs.dd2dm(latitude,'latitude')
        msg += b',%02d%010.7f,%s' % (lat_d,lat_m,lat_dir.encode())
        
        lon_d,lon_m,lon_dir = self._gcs.dd2dm(longitude,'longitude')
        msg += b',%03d%010.7f,%s'%(lon_d,lon_m,lon_dir.encode())
        
        msg += b',%d,%02d,%.1f,%.1f,M,%.1f,M,'%(fix,nsat,dop,
                                                altitude,geoid)
        
        if t_dgps is None: msg += b',*'
        else: msg += b'%.2f,*'
        
        return msg + self.checksum(msg[1:-1])[0]
        #b'$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47'
        
    def parse(self,msg):
        ''' parses the message in ascii or binary '''
        try:
            if type(msg) == self.BYTES: msg = msg.decode()
            if (not msg.startswith('$GPGGA') and 
                not msg.startswith('$GNGGA') and 
                not msg.startswith('$GLGGA')):
                print('ImproperGPGGAMessageError.')     
            string = msg.split(',')
            self._timestamp = '%s:%s:%s' % (string[1][0:2],
                                            string[1][2:4],
                                            string[1][4:])
            self._time = float(string[1][0:2])*3600 + float(string[1][2:4])*60 + float(string[1][4:])
            self._lat = self._gcs.dm2dd(string[2],string[3])
            self._lon = self._gcs.dm2dd(string[4],string[5])
            [self._easting,self._northing,self._region,self._zone] = utm.from_latlon(self._lat,
                                                                                     self._lon)
            self._fix = int(string[6])
            self._n = int(string[7])
            self._dop = float(string[8])
            self._alt = float(string[9])
            self._geoid = float(string[11])
        except Exception as e:
            self._error = True
            exc_type, _, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('%s:%s in %s at %d. MSG:%s'%(exc_type.__name__,str(e), fname, exc_tb.tb_lineno,msg))
            
    def getData(self):
        ''' returns the data 
        0) time in seconds
        1) timestamp in HH:MM:SS.ss
        2) latitude in decimal degrees
        3) longitude in decimal degrees
        4) number of satellites
        5) GPS fix quality
        6) Dilution of precision
        7) UTM easting in m
        8) UTM northing in m
        9) UTM Region
        10) UTM zone
        11) Height above sea level in m
        12) Height above geoid in m'''
        return [self._time,self._timestamp,
                self._lat,self._lon,
                self._n,self._fix,self._dop,
                self._easting,self._northing,self._region,self._zone,
                self._alt,self._geoid]
        
class gprmc(parser):
    ''' parses the gprms nmea messages '''
    
    BYTES = type(bytes())
    
    def __init__(self):
        ''' constructor '''
        super().__init__()
        self.reset()
        self._gcs = gcs()
        
    def reset(self):
        ''' resets the parser '''
        self._time = self._nan()
        self._timestamp = '00:00:00.00'
        self._lat = self._nan()
        self._lon = self._nan()
        self._easting = self._nan()
        self._northing = self._nan()
        self._region = self._minus1()
        self._zone = ''
        self._warn = ''
        self._s = self._nan()
        self._c = self._nan()
        self._date = ''
        self._var = self._nan()
        self._var_dir = ''
        
    def parse(self,msg):
        ''' parses the message '''
        try:
            if type(msg) == self.BYTES: msg = msg.decode()
            if (not msg.startswith('$GPRMC') and 
                not msg.startswith('$GNRMC') and 
                not msg.startswith('$GLRMC')):
                print('ImproperGPRMCMessageError.')     
            string = msg.split(',')
            self._timestamp = '%s:%s:%s' % (string[1][0:2],
                                            string[1][2:4],
                                            string[1][4:])
            self._time = float(string[1][0:2])*3600 + float(string[1][2:4])*60 + float(string[1][4:])
            self._warn = string[2]
            self._lat = self._gcs.dm2dd(string[3],string[4])
            self._lon = self._gcs.dm2dd(string[5],string[6])
            self._s = float(string[7])
            self._c = string[8]
            self._date = string[9]
            self._var = string[10]
            self._var_dir = string[11]
            
            [self._easting,self._northing,self._region,self._zone] = utm.from_latlon(self._lat,
                                                                                     self._lon)
        except Exception as e:
            self._error = True
            exc_type, _, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('%s:%s in %s at %d. MSG:%s'%(exc_type.__name__,str(e), fname, exc_tb.tb_lineno,msg))
        
    def getData(self):
        ''' returns the data 
        0) time in seconds
        1) timestamp
        2) waring A=OK, V=warning
        3) latitude in decimal degrees
        4) longitude in decimal degrees
        5) utm easting in m
        6) utm northing in m
        7) utm region
        8) utm zone
        9) speed in knots
        10) true course
        11) date stamp
        12) variation
        13) east/west '''
        return [self._time,self._timestamp,self._warn,
                self._lat,self._lon,
                self._easting,self._northing,self._region,self._zone,
                self._s,self._c,self._date,self._var,self._var_dir]    