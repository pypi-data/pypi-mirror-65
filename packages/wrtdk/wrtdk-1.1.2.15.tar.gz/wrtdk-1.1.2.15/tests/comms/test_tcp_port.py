'''
Created on Nov 13, 2019

@author: reynolds
'''
import unittest

from wrtdk.comms.comms import tcp_port

ADDR = 'localhost'
PORT = 10011

class Test(unittest.TestCase):
    
    def test(self):
        s = tcp_port(connect=False)
        
        _open = s.open(ADDR,PORT,1)
        self.assertTrue(_open)
        
        msg,addr = s.read(1000)
        print(addr,msg)
        self.assertNotEqual(msg,None)
        
        _close = s.close()
        self.assertTrue(_close)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_open']
    unittest.main()