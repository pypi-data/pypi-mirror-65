'''
Created on Oct 31, 2019

@author: reynolds
'''

import os, sys

from wrtdk.io.streamer.streamer import LoggingStreamer
from PyQt5.QtCore import pyqtSignal
from wrtdk.data.buffer.buffer import byte_buffer
from wrtdk.parser.nmea.nmea import gpgga
from wrtdk.parser.em.em3d.em.em import emv1,emv2
from wrtdk.parser.em.em3d.conf.conf import confv3,confv5

class em_streamer(LoggingStreamer):
    '''
    classdocs
    '''
    
    EM_SOL = 116
    GGA_SOL = 36
    CONF_SOL = 67
    EOL = bytes([10])
    SOL = bytes([EM_SOL,CONF_SOL,GGA_SOL])
    EM = 0
    CONF = 1
    GGA = 2
    RAW = 3
    
    new_timeout = pyqtSignal()# timeout signal
    new_em = pyqtSignal(int,int,list)#type,list length,data
    new_conf = pyqtSignal(int,int,list)#type, list length,data
    new_gga = pyqtSignal(int,int,list)#type, list length, data
    new_raw = pyqtSignal(int,int,bytes)#type, list length, data

    def __init__(self,port=None,debug=False,filename=None,dt=0.1,version=1):
        '''
        Constructor
        '''
        super().__init__(debug=debug,port=port,dt=dt)
        
        self._buffer = byte_buffer()
        
        # define parsers
        self.gga = gpgga()
        self._version(version)
        if self._debug and os.path.join(filename):
            print('Simulation is currently not functional - rwr 10/31/19')
            self.filename=filename
        else:self.filename=None
        
    def _version(self,version):
        ''' sets the version of the parser to be used '''
        if version == 2:# second version
            self.em = emv2()
            self.conf = confv5()
        else:# assume first version
            self.em = emv1()
            self.conf = confv3()
            
    def run(self):
        self.set_mode()
        
        i = 0
        
        while self._running:
            try:
                msg,_ = self.port.read(2000)
            except Exception as e:
                exc_type, _, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print('%s:%s in %s at %d'%(exc_type.__name__,str(e), fname, exc_tb.tb_lineno))
                self.new_timeout.emit()
                continue
            
            if msg is None: return
            
            i += 1
            
            if self.isLogging(): self.writer.write(msg)
            
            self._buffer.append(msg)
            
            m = self.parse()
            
            while m is not None:
                self.send(m)
                m = self.parse()
                
            
        self.port.close()           
            
    def parse(self):
        if self._buffer.is_empty(): return
        
        # find a start byte
        try:
            b = bytes([self._buffer.get()])
        except Exception as e:
            print('error',str(e),self._buffer)
            return
        while not self.is_sol(b) and not self._buffer.is_empty(): 
            b = bytes([self._buffer.get()])
        
        buff = bytes()
        
        while not self._buffer.is_empty():
            buff = buff + b
            
            # check if the message is full
            if self.is_eol(b) and self.is_sol(self._buffer.view()):
                self._buffer.remove_head()
                return buff
            
            # get the next byte
            b = bytes([self._buffer.get()])
        
        self._buffer.reset_position()
        
        if self._buffer.get_length() > 2000: self._buffer.clear()
            
        return None
    
    def send(self,b):
        self.new_raw.emit(self.RAW,len(b),b)
        
        if self.is_em(b[0]):
            if not self.em.is_set(): return
            self.em.parse(b)
            if not self.em.hasErrored():
                data = self.em.getData()
                self.new_em.emit(self.EM,
                                 len(data),
                                 data)
        elif self.is_conf(b[0]):
            self.conf.parse(b)
            if not self.conf.hasErrored():
                if not self.em.is_set():
                    self.em.set_bins(self.conf.get_bins())
                data = self.conf.getData()
                self.new_conf.emit(self.CONF,
                                   len(data),
                                   data)
        elif self.is_gga(b[0]):
            self.gga.parse(b)
            if not self.gga.hasErrored():
                data = self.gga.getData()
                self.new_gga.emit(self.GGA,
                                  len(data),
                                  data)
    
    def is_conf(self,b):
        return b == self.SOL[1]
    
    def is_em(self,b):
        return b == self.SOL[0]
    
    def is_gga(self,b):
        return b == self.SOL[2]
        
    def is_sol(self,b):
        return b in self.SOL
    
    def is_eol(self,b):
        return b in self.EOL