'''
Created on Dec 26, 2019

@author: Reynolds
'''
import unittest
from wrtdk.parser.vmag.pni import pni


class Test(unittest.TestCase):


    def setUp(self):
        self.msg = b'\xff\xff\xfb5\xff\xff\xff\x0f\x00\x00\r\xf6:96\x00'
        self.vmag = pni()

    def test_parse(self):
        self.vmag.parse(self.msg)
        self.assertFalse(self.vmag.hasErrored())
        d = self.vmag.getData()
        
        msg = self.vmag.get(bx=d[0], by=d[1], bz=d[2])
        
        self.assertEqual(msg[:-4],self.msg[:-4])


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()