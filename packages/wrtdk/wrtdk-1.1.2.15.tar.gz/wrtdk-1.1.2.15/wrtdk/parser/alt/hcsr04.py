'''
Created on Jan 29, 2019

@author: reynolds
'''

import sys, os, struct
from wrtdk.parser.parser import parser

class hcsr04(parser):
    ''' A class for parsing the HCSR04 messages'''

    def __init__(self):
        ''' Constructor '''
        super().__init__()# inherit superclass
        
        # initialize properties
        self.reset()
        
        # define constants
        self.M_2_LSB = 1e4
        self.NS_2_LSB = 0.1
        self.LSB_2_M = 100 * 1e-6
        self.LSB_2_NS = 10
        
    def reset(self):
        ''' resets the parser properties '''
        self._ns = []
        self._alt = []
        
    def get(self,d=0,t_ns=0):
        return struct.pack('>iI',
                           int(d*self.M_2_LSB),
                           int(t_ns*self.NS_2_LSB))
        
    def parse(self,msg):
        ''' parses the wrt hcsr04 acoustic sensor message '''
        try:
            self._alt,self._ns = struct.unpack('>iI',msg)
            self._alt *= self.LSB_2_M
            self._ns *= self.LSB_2_NS
        except Exception as e:
            self._error = True
            exc_type, _, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('%s:%s in %s at %d. MSG:%s'%(exc_type.__name__,str(e), fname, exc_tb.tb_lineno,msg))
    
    def getData(self):
        ''' returns the data
        altitude in m
        time in nanoseconds'''
        return [self._alt,self._ns]