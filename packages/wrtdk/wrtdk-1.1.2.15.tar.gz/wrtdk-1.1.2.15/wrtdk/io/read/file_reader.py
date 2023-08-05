'''
Created on Dec 17, 2019

@author: Reynolds
'''

import os

class file_reader(object):
    '''
    classdocs
    '''
    
    def read(self,filename):
        if not os.path.exists(filename):
            print('%s does not exist'%filename)
            return {}
        
        return self._read(filename)
        
    def _read(self,filename):
        pass