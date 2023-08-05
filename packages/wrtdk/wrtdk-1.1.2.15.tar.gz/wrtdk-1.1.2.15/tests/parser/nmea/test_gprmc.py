'''
Created on Nov 20, 2019

@author: reynolds
'''
import unittest
from wrtdk.parser.nmea.nmea import gprmc

class test_rmc(unittest.TestCase):


    def setUp(self):
        self.gprmc = b'$GPRMC,081836,A,3751.65,S,14507.36,E,000.0,360.0,130998,011.3,E*62'
        self.gnrmc = b'$GNRMC,081836,A,3751.65,S,14507.36,E,000.0,360.0,130998,011.3,E*62'
        self.rmc = gprmc()

    def tearDown(self):
        pass


    def test_gprmc_parse(self):
        self.rmc.parse(self.gprmc)
        self.assertFalse(self.rmc.hasErrored())
        
    def test_gnrmc_parse(self):
        self.rmc.parse(self.gnrmc)
        self.assertFalse(self.rmc.hasErrored())

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()