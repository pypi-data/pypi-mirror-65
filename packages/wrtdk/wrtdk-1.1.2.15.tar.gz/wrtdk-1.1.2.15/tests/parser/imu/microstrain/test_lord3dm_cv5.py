'''
Created on Dec 5, 2019

@author: Reynolds
'''
import unittest
from wrtdk.parser.imu.microstrain import lord3dm_cv5


class Test(unittest.TestCase):


    def setUp(self):
        self.imu = lord3dm_cv5()


    def test_hasErrored(self):
        msg = b'ue\x80J\x0e\x0c\xc0\x1f\x0c0\xbfK\xcb\xaf\xbf\x80nq\x12\n=\xac="\xbfS>z>\x9e\xc31\xbe\xed\xe1\xf1\x0e\x04\xbf7\xa63>\xd9\xc8,?\r\x13{\x0e\x05;j\r\xbe\xbab\x9bG;~\x05\xbe\x0e\x06>\xe7\xbaI\xbe\xa3:4\xbd\x9b\xddibU'
        self.imu.parse(msg)
        
        self.assertFalse(self.imu.hasErrored())
        
    def test_get_parse(self):
        roll,pitch,yaw = 10,20,30
        
        m = self.imu.get(roll,pitch,yaw)
        
        self.imu.parse(m)
        
        self.assertFalse(self.imu.hasErrored())
        
        d = self.imu.getData()
        
        self.assertAlmostEqual(d[0],roll,1)
        self.assertAlmostEqual(d[1],pitch,1)
        self.assertAlmostEqual(d[2],yaw,1)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()