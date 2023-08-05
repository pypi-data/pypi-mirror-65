'''
Created on Nov 19, 2019

@author: reynolds
'''

import os, sys, struct

from wrtdk.parser.parser import parser

class confv3(parser):
    '''
    classdocs
    '''
    
    LENGTH = 24
    VERSION = 3
    
    PREAMBLE = b'CONF'

    def __init__(self):
        '''
        Constructor
        '''
        super().__init__()
        self.reset()
        
    def reset(self):
        self._fid = self._minus1()
        self._svn = self._minus1()
        self._hdr = self._minus1()
        self._glb = self._minus1()
        self._tot = self._minus1()
        self._txs = self._minus1()
        self._sys = self._minus1()
        self._tme = self._minus1()
        self._cnt = self._minus1()
        self._hld = self._minus1()
        self._rxs = self._minus1()
        self._axs = self._minus1()
        self._bns = self._minus1()
        
    def get_bins(self):
        return self._bns
        
    def parse(self,msg):
        self.reset()
        
        try:
            m = struct.unpack('>4sHHBBBBHHxxHBBBB',msg[0:self.LENGTH])
            if m[0] != self.PREAMBLE: 
                raise('CONFFormatException',
                      'This is not an em configuration message')
            
            self._fid = m[1]
            self._svn = m[2]
            self._hdr = m[3]
            if self._hdr != self.VERSION: 
                raise Exception('CONFVersionException',
                                'This is not the proper version.')
            self._glb = m[4]
            self._tot = m[5]
            self._txs = m[6]
            self._sys = m[7]
            self._tme = m[8]
            self._cnt = m[9]
            self._hld = m[10]
            self._rxs = m[11]
            self._axs = m[12]
            self._bns = m[13]
        except Exception as e:
            self._error = True
            exc_type, _, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('%s:%s in %s at %d. MSG:%s'%(exc_type.__name__,str(e), fname, exc_tb.tb_lineno,msg))  
        
    def getData(self):
        ''' returns the data from the conf message
        0) FID
        1) SVN Revision
        2) Version Number
        3) Globals
        4) Duty States Total
        5) Duty States Tx
        6) System Timer
        7) Sample Timer
        8) Total Sample Count
        9) Holdoff
        10) Cube Count
        11) Axis Count
        12) Bin Count
        '''
        return [self._fid,self._svn,self._hdr,self._glb,
                self._tot,self._txs,self._sys,self._tme,
                self._cnt,self._hld,self._rxs,self._axs,
                self._bns]
class confv5(parser):
    '''
    classdocs
    '''
    
    LENGTH = 27
    VERSION = 5
    
    PREAMBLE = b'CONF'

    def __init__(self):
        '''
        Constructor
        '''
        super().__init__()
        self.reset()
        
    def reset(self):
        self._fid = -1
        self._svn = -1
        self._hdr = -1
        self._glb = -1
        self._tot = -1
        self._txs = -1
        self._sys = -1
        self._tme = -1
        self._cnt = -1
        self._hld = -1
        self._rxs = -1
        self._axs = -1
        self._bns = -1
        
    def get_bins(self):
        return self.bin_count
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
            #unpack up through the bins
            m = struct.unpack('>4sBBBHHBBBBBHHBHBBBB',msg[0:self.LENGTH])
            if m[0] != self.PREAMBLE: 
                raise('CONFFormatException',
                      "Did not begin with CONF")
            self.read_checksum = m[1]
            self.conf_version = m[2]
            if self.conf_version != self.VERSION: 
                raise Exception('CONFVersionException','CONF version %d instead of CONF version %d'%(self.conf_version,self.VERSION))
            #check sum version
            self.checksum_version = m[3]
            self.system_id = m[4]
            self.fiducial = m[5]
            self.svn_version = m[6]
            self.conf_flags1 = m[7]
            self.conf_flags2 = m[8]
            use_checksum=((self.conf_flags2 & 4)==4)
            
            self.state_max = m[9]
            self.conf_txon_count = m[10]
            self.system_timer = m[11]
            self.sample_timer = m[12]
            self.conf_flags3 = m[13]
            self.sample_count = m[14]
            self.timer_holdoff = m[15]
            self.cube_count = m[16]
            self.cube_axes = m[17]
            self.bin_count = m[18]
            if(use_checksum):
                #add checksum versions here
                self.calc_checksum=self.checksum(msg[5:self.LENGTH+2*self.bin_count])
                if self.read_checksum!=self.calc_checksum: #might need +1 for \n
                    raise Exception('CONFVersionException','Checksum did not match: %d vs %d'%(self.read_checksum,self.calc_checksum))
            frmt='>%dH'%(self.bin_count)
            self.bin_values= struct.unpack(frmt,msg[self.LENGTH:self.LENGTH+2*self.bin_count])
            
        except Exception as e:
            self._error = True
            exc_type, _, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('%s:%s in %s at %d. MSG:%s'%(exc_type.__name__,str(e), fname, exc_tb.tb_lineno,msg))  
        
    def getData(self):
        ''' returns the data from the conf message
        0) FID
        1) SVN Revision
        2) Version Number
        3) Globals
        4) Duty States Total
        5) Duty States Tx
        6) System Timer
        7) Sample Timer
        8) Total Sample Count
        9) Holdoff
        10) Cube Count
        11) Axis Count
        12) Bin Count
        '''
        return [self._fid,self._svn,self._hdr,self._glb,
                self._tot,self._txs,self._sys,self._tme,
                self._cnt,self._hld,self._rxs,self._axs,
                self._bns]