'''
Created on Aug 17, 2018

@author: reynolds
'''

import os, sys, struct, math
from wrtdk.parser.parser import parser

class pni(parser):
    ''' a class for parsing the pni vector
    magnetometer binary message '''

    def __init__(self):
        ''' Constructor '''
        super().__init__()# inherit superclass
        
        # define constants
        self.NT_2_COUNT = 75/1000
        self.COUNT_2_NT = 1000/75
        self.MSG_LEN = 12
        
        # initialize properties
        self.reset()
        
    def reset(self):
        ''' resets the properties '''
        self._bx = self._nan()
        self._by = self._nan()
        self._bz = self._nan()
        
    def get(self,bx=0,by=0,bz=0):
        ''' returns a pni vector mag message '''
        return struct.pack('>iii4s',
                    int(bx*self.NT_2_COUNT),
                    int(by*self.NT_2_COUNT),
                    int(bz*self.NT_2_COUNT),
                    b':00\x00')
        
    def parse(self,msg):
        ''' parses the pni messages '''
        self.reset()
        
        try:
            self._bx,self._by,self._bz = struct.unpack('>iii',msg[:-4])
            self._bx *= self.COUNT_2_NT
            self._by *= self.COUNT_2_NT
            self._bz *= self.COUNT_2_NT
        except Exception as e:
            self._error = True
            exc_type, _, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('%s:%s in %s at %d. MSG:%s'%(exc_type.__name__,str(e), fname, exc_tb.tb_lineno,msg))
            
    def _total(self):
        ''' returns the total field value '''
        return math.sqrt(self._bx ** 2 + self._by ** 2 + self._bz ** 2)
            
    def getData(self):
        ''' returns all the data 
        0) bx in n
        1) by in nT
        2) bz in nT
        3) bTotal in nT '''
        return [self._bx,self._by,self._bz,
                self._total()]