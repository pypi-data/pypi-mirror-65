'''
Created on Dec 26, 2019

@author: Reynolds
'''
import unittest
from wrtdk.parser.alt.lidar_lite_v3 import lidar_lite_v3


class Test(unittest.TestCase):

    def setUp(self):
        self.msg = b'\x9a\x9a\x00S'
        self.lidar = lidar_lite_v3()

    def test_lidar_lite_v3(self):
        self.lidar.parse(self.msg)
        self.assertFalse(self.lidar.hasErrored())
        d1 = self.lidar.getData()
        
        msg = self.lidar.get(health=d1[0],
                             reg=d1[1],
                             roverflow=d1[3],
                             soverflow=d1[4],
                             dpeak=d1[2],
                             busy=d1[5],
                             strength=d1[6],
                             d=d1[-1])
        
        self.lidar.parse(msg)
        self.assertFalse(self.lidar.hasErrored())
        
        d2 = self.lidar.getData()
        
        self.assertEqual(d1,d2)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()