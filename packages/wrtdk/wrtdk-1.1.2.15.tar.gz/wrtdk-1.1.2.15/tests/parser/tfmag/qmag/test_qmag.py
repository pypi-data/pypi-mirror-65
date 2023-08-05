'''
Created on Dec 4, 2019

@author: Reynolds
'''
import unittest
from wrtdk.parser.tfmag.qmag import qmag


class Test(unittest.TestCase):


    def setUp(self):
        self.tf = 50e3
        self.strength = 10
        self.qmag = qmag()

    def test_get(self):
        b = self.qmag.get(self.tf,self.strength)
        self.qmag.parse(b)
        self.assertFalse(self.qmag.hasErrored())
        d = self.qmag.getData()
        self.assertAlmostEqual(self.tf,d[0][0],1)
        self.assertEqual(self.strength,d[1][0])
        
    def test_parse(self):
        msg = b'!326611627@77'
        matlab_ans = 54350.6458794415521
        self.qmag.parse(msg)
        self.assertFalse(self.qmag.hasErrored())
        d = self.qmag.getData()
        
        self.assertAlmostEqual(matlab_ans,d[0][0],10)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()