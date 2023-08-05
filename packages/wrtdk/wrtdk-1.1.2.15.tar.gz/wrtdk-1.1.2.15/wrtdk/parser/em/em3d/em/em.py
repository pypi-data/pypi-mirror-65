'''
Created on Nov 19, 2019

@author: reynolds
'''
import os, sys, struct
from wrtdk.parser.parser import parser
import numpy as np
class emv1(parser):
    '''
    classdocs
    '''
    
    TX_MASK = 0b11100000
    RX_MASK = 0b00011100
    AX_MASK = 0b00000011
    COUNT_TO_MV = .1562
    PREAMBLE = b't'

    def __init__(self):
        '''
        Constructor
        '''
        super().__init__()
        self._len = self._minus1()
        self._bins = self._minus1()
        self._set = False
        self._fmt = ''
        
    def is_set(self):
        return self._set
        
    def reset(self):
        self._tx = self._minus1()
        self._rx = self._minus1()
        self._ax = self._minus1()
        self._ct = self._minus1()
        if self.is_set():
            for i in range(len(self._tg)):
                self._tg[i] = self._nan()
                self._mv[i] = self._nan()
            
    def set_bins(self,bins):
        self._bins = bins
        self._len = 1+1+1+self._bins*2
        self._tg = self._arr(self._bins)
        self._mv = self._arr(self._bins)
        self._set = True
        self._fmt = '>cBB%dhx'%self._bins
        
    def get_length(self):
        return self._len
        
    def get_bins(self):
        return self._bins
        
    def parse(self,msg):
        self.reset()
        
        try:
            if not self.is_set(): raise Exception('EMFormatException','Bin length is not set yet')
            m = struct.unpack(self._fmt,msg)
            
            if m[0] != self.PREAMBLE: raise Exception('EMFormatException','Message is not the proper format')
            
            self._tx = (m[1] & self.TX_MASK) >> 5
            self._rx = (m[1] & self.RX_MASK) >> 2
            self._ax = m[1] & self.AX_MASK
            self._ct = m[2]
            
            for i in range(self._bins):
                self._tg[i] = m[3+i]
                self._mv[i] = m[3+i] * self.COUNT_TO_MV
                
        except Exception as e:
            self._error = True
            exc_type, _, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('%s:%s in %s at %d. MSG:%s'%(exc_type.__name__,str(e), fname, exc_tb.tb_lineno,msg))    
        
    def getData(self):
        ''' returns the data from the em message if set
        0) Tx
        1) Rx
        2) Ax
        3) Count
        4-end) millivolt bin data 
        '''
        if not self.is_set(): return None
        return [self._tx,self._rx,self._ax,self._ct]+self._mv
class emv2(parser):
    '''
    Identical to emv1 except with a checksum byte
    '''
    
    TX_MASK = 0b11100000
    RX_MASK = 0b00011100
    AX_MASK = 0b00000011
    COUNT_TO_MV = .1562
    PREAMBLE = b't'

    def __init__(self):
        '''
        Constructor
        '''
        super().__init__()
        self._len = -1
        self._bins = -1
        self._set = False
        self._fmt = ''
        
    def is_set(self):
        return self._set
        
    def reset(self):
        self._tx = -1
        self._rx = -1
        self._ax = -1
        self._ct = -1
        if self.is_set():
            for i in range(len(self._tg)):
                self._tg[i] = np.nan
                self._mv[i] = np.nan
            
    def set_bins(self,bins):
        self._bins = bins
        self._len = 1+1+1+self._bins*2
        self._tg = self._arr(self._bins)
        self._mv = self._arr(self._bins)
        self._set = True
        self._fmt = '>cBBB%dhx'%self._bins
        
    def get_length(self):
        return self._len
        
    def get_bins(self):
        return self._bins
    def checksum(self,byte_values):
        '''
        calculate a checksum value of a section of bytes
        '''
        total=0
        i=0
        for b in byte_values:
            total+=b
            i+=1
#         print(total)
        return total & 255
    def parse(self,msg):
        self.reset()
        
        try:
            if not self.is_set(): raise Exception('EMFormatException','Bin length is not set yet')
#             print(len(msg))
            m = struct.unpack(self._fmt,msg)
            
            if m[0] != self.PREAMBLE: raise Exception('EMFormatException','Message is not the proper format')
            #checksum
            read_checksum=int(m[1])
            calc_checksum=self.checksum(msg[2:4+(2*self._bins)])
#             for i in range(len(msg)):
#                 for j in range(i,len(msg)):
#                     if read_checksum==self.checksum(msg[i:j]):
#                         print("SUCCESS:",i,j,self._bins)
            if(read_checksum!=calc_checksum): 
                print(m[1],m[2],m[3])
                raise Exception('CONFVersionException','Checksum did not match: %d vs %d'%(read_checksum,calc_checksum))
            #cubestate
            self._tx = (m[2] & self.TX_MASK) >> 5
            #cube number
            self._rx = (m[2] & self.RX_MASK) >> 2
            #cube axes
            self._ax = m[2] & self.AX_MASK
            #fiducial
            self._ct = m[3]
            
            for i in range(self._bins):
                self._tg[i] = m[4+i]
                self._mv[i] = m[4+i] * self.COUNT_TO_MV
                
        except Exception as e:
            self._error = True
            exc_type, _, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('%s:%s in %s at %d. MSG:%s'%(exc_type.__name__,str(e), fname, exc_tb.tb_lineno,msg))    
        
    def getData(self):
        ''' returns the data from the em message if set
        0) Tx
        1) Rx
        2) Ax
        3) Count
        4-end) millivolt bin data 
        '''
        if not self.is_set(): return None
        return [self._tx,self._rx,self._ax,self._ct]+self._mv