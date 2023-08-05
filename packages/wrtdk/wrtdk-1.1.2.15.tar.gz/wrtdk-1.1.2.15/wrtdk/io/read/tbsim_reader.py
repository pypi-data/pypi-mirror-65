'''
Created on Dec 17, 2019

@author: Reynolds
'''

import numpy as np

from wrtdk.io.read.file_reader import file_reader
from wrtdk.io.sim.sim_simulator import sim_simulator
from wrtdk.parser.msg.wrtmsg import udp_wrapper
from wrtdk.parser.imu.microstrain import lord3dm_cv5
from wrtdk.parser.nmea.nmea import gpgga
from wrtdk.parser.tfmag.qmag import qmag
from wrtdk.parser.tfmag.mfam import mx3g
from wrtdk.parser.vmag.pni import pni
from wrtdk.parser.alt.hcsr04 import hcsr04
from wrtdk.parser.alt.lidar_lite_v3 import lidar_lite_v3

class tbsim0_reader(file_reader):
    '''
    classdocs
    '''
    
    GGA_PATTERN = r'$G.GGA'
    TALKER_ID_LEN = len(GGA_PATTERN)
    GPS = (b'$GPS' + bytes([0,0])).decode()
    WRAPPER_COLS = 4

    def __init__(self):
        '''
        Constructor
        '''
        super().__init__()
        
    def _read(self,filename):
        ''' reads the file and returns the data in a dictionary '''
        
        # intialize all parsers
        msgparser = sim_simulator()# get individual messages 
        wrapper = udp_wrapper()# udp wrapper parser
        imu = lord3dm_cv5()# Lord microstrain imu parser
        gga = gpgga()# nmea gga parser
        q = qmag()# qmag parser
        mfam = mx3g()
        vmag = pni()# pni parser
        sonar = hcsr04()# acoustic range finder parser
        lidar = lidar_lite_v3()# lidar parser
        
        # read the file 
        msgparser.read(filename)# read
        
        # cycle through all messages and count message types and system ids
        _len = msgparser.length()# get number of messages
        k = 0# counter for the messages
        msgs,data={},{}# intialize dictionaries to hold sensor count/length and data
        while k < _len:
            msg,_ = msgparser.getNext()# get the next message
            wrapper.parse(msg[0:wrapper.LENGTH])# parse the wrapper
            if not wrapper.hasErrored():# check to make sure no errors occurred
                s = str(wrapper.getSystemID())# get the system id key
                if s not in msgs.keys(): msgs[s] = {}# add dict to key is new msg type
                if wrapper.getType() == self.GPS:
                    if not self._gga(msg[wrapper.getMsgStart():wrapper.getMsgStart()+self.TALKER_ID_LEN]):
                        k += 1
                        continue
                if wrapper.getType() not in msgs[s].keys():# new sensor msg if new
                    msgs[s][wrapper.getType()] = {'count':0,'length':0}# count for filling array and length
                msgs[s][wrapper.getType()]['length'] += 1# increment the row number
            k += 1# increment the msg number
            
        #print(msgs)# uncomment to see how the messages count
        
        # initialze the output data array
        for system in msgs.keys():# cycle through all keys
            data[system] = {}# intialze key as a dict
            for sensor in msgs[system]:# cycel through all sensors
                # get the number of columsn depending on sensor type
                if sensor == '$SYSTM': cols = self.WRAPPER_COLS
                elif sensor == '$LIDAR': cols = self.WRAPPER_COLS+2
                elif sensor == '$TFMAG': cols = self.WRAPPER_COLS+2
                elif sensor == '$IMUX1': cols = self.WRAPPER_COLS+3
                elif sensor == '$VCMAG': cols = self.WRAPPER_COLS+4
                elif sensor == '$SONAR': cols = self.WRAPPER_COLS+2
                elif sensor == '$MFAM1': cols = self.WRAPPER_COLS+4
                elif sensor == '$MFAM2': cols = self.WRAPPER_COLS+4
                elif sensor == self.GPS: cols = self.WRAPPER_COLS+11
                else: cols = self.WRAPPER_COLS# default for unknown message
                
                # initialze numpy array to proper length and width
                data[system][sensor] = np.zeros([msgs[system][sensor]['length'],cols])
        
        # fill the arrays with sensor data
        k,row = 0,0
        while k < _len:# cycle through all messages
            msg,_ = msgparser.getNext()# get the next message
            wrapper.parse(msg[0:wrapper.LENGTH])# parse the header
            skey = str(wrapper.getSystemID())# find the system id key
            row = msgs[skey][wrapper.getType()]['count']# get the row number
            if row >= msgs[skey][wrapper.getType()]['length']: 
                k += 1
                print(msg)
                continue# skip if out of range
            
            # parse all the messages based on the sensor types
            if wrapper.getType() == '$TFMAG':# QMAG messages
                q.parse(msg[wrapper.getMsgStart():wrapper.getMsgEnd()])
                if not q.hasErrored():
                    d =  q.getData()
                    data[skey][wrapper.getType()][row,:] = self._hdr(wrapper) + [d[0][0],d[1][0]]
            elif wrapper.getType() == '$MFAM1':
                mfam.parse(msg[wrapper.getMsgStart():wrapper.getMsgEnd()])
                if not mfam.hasErrored():
                    d = mfam.getData()
                    data[skey][wrapper.getType()][row,:] = self._hdr(wrapper) + [d[0],d[6],d[1],d[7]]
            elif wrapper.getType() == '$MFAM2':
                mfam.parse(msg[wrapper.getMsgStart():wrapper.getMsgEnd()])
                if not mfam.hasErrored():
                    d = mfam.getData()
                    data[skey][wrapper.getType()][row,:] = self._hdr(wrapper) + [d[0],d[6],d[1],d[7]]
            elif wrapper.getType() == '$IMUX1':# Lord IMU
                imu.parse(msg[wrapper.getMsgStart():wrapper.getMsgEnd()])
                if not imu.hasErrored():
                    data[skey][wrapper.getType()][row,:] = self._hdr(wrapper) + imu.getData()[0:3]
            elif wrapper.getType() == '$VCMAG':# PNI vector mag
                vmag.parse(msg[wrapper.getMsgStart():wrapper.getMsgEnd()])
                if not vmag.hasErrored():
                    data[skey][wrapper.getType()][row,:] = self._hdr(wrapper) + vmag.getData()
            elif wrapper.getType() == '$SONAR':# acoustic range finder
                sonar.parse(msg[wrapper.getMsgStart():wrapper.getMsgEnd()])
                if not sonar.hasErrored():
                    data[skey][wrapper.getType()][row,:] = self._hdr(wrapper) + sonar.getData()
            elif wrapper.getType() == '$LIDAR':# lidar lite v3
                lidar.parse(msg[wrapper.getMsgStart():wrapper.getMsgEnd()])
                if not lidar.hasErrored():
                    data[skey][wrapper.getType()][row,:] = self._hdr(wrapper) + lidar.getData()[6::]
            elif wrapper.getType() == self.GPS:# all gps messages
                m = msg[wrapper.getMsgStart():wrapper.getMsgEnd()]
                if self._gga(m[0:self.TALKER_ID_LEN]):# all gpgga messages
                    gga.parse(m)
                    if not gga.hasErrored():
                        d = gga.getData()
                        data[skey][wrapper.getType()][row,:] = self._hdr(wrapper) + [d[0],
                                                                                     d[2],
                                                                                     d[3],
                                                                                     d[5],
                                                                                     d[6],
                                                                                     d[7],
                                                                                     d[8],
                                                                                     d[9],
                                                                                     ord(d[10]),
                                                                                     d[11],
                                                                                     d[12]]
                else:
                    k += 1
                    continue
            
            msgs[skey][wrapper.getType()]['count'] += 1# incremenent the row number
            k += 1# increment the msg number
            
        # reorder time to be chronological
        for skey in data.keys():# for each system id
            for hkey in data[skey].keys():# for each sensor 
                order = np.argsort(data[skey][hkey][:,0])# get order
                data[skey][hkey] = data[skey][hkey][order,:]# rearrange
        
        # return the data dict
        return data
        
    def _hdr(self,w):
        ''' gets the header info into a list '''
        return [w.getMCU(),w.getSensorID(),w.getFiducial(),self._status(w.getStatus())]
    
    def _gga(self,string):
        return string == b'$GPGGA' or string == b'$GNGGA'
            
    def _status(self,status):
        ''' correlates and integer with a status '''
        if status == 'AG': return 1
        elif status == 'ND': return 0
        elif status == 'MA': return 2
        elif status == 'ES': return 3
        elif status == 'L0': return 4
        elif status == 'L1': return 5
        elif status == 'L2': return 6
        elif status == 'L3': return 7
        elif status == 'L4': return 8
        elif status == 'L5': return 9
        elif status == 'L6': return 10
        elif status == 'L7': return 11
        elif status == 'L8': return 12
        elif status== 'l9': return 13
        else: return -1
            
        
if __name__ == '__main__':
    r = tbsim0_reader()
    data = r.read(r'C:\Users\reynolds\Documents\1704_madunit\data\20190308_enfield01\log00001.log')
    print(data)
    for skey in data.keys():
        print(skey)
        for hkey in data[skey].keys():
            print(hkey,data['4001']['$GPS\x00\x00'][:,0])
    
            