'''
Created on Dec 26, 2019

@author: Reynolds
'''
import unittest
from wrtdk.parser.alt.hcsr04 import hcsr04


class Test(unittest.TestCase):


    def setUp(self):
        self.msg = b'\x00\x00:\xec\x00\r\x89\xe8'
        self.sonar = hcsr04()


    def test_hcsr04(self):
        self.sonar.parse(self.msg)
        
        self.assertFalse(self.sonar.hasErrored())
        
        d = self.sonar.getData()
        
        msg = self.sonar.get(d=d[0],t_ns=d[1])
        
        self.assertEqual(msg,self.msg)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()