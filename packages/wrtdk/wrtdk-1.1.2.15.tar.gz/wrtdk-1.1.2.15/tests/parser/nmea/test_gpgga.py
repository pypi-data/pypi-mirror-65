'''
Created on Nov 20, 2019

@author: reynolds
'''
import unittest
from wrtdk.parser.nmea.nmea import gpgga


class test_gga(unittest.TestCase):


    def setUp(self):
        self.gpgga = b'$GPGGA,123519.00,4807.0380000,N,01131.0000000,E,1,08,0.9,545.4,M,46.9,M,,*69'
        self.gngga = b'$GNGGA,123519.00,4807.0380000,N,01131.0000000,E,1,08,0.9,545.4,M,46.9,M,,*77'
        self.gga = gpgga()

    def test_gpgga_parse(self):
        self.gga.parse(self.gpgga)
        self.assertFalse(self.gga.hasErrored())
        
        d =  self.gga.getData()
        
        gpgga = self.gga.get(time=d[0],latitude=d[2],longitude=d[3],fix=d[5],nsat=d[4],dop=d[6],altitude=d[11],geoid=d[12])
        
        self.assertEqual(self.gpgga,gpgga)
        
    def test_gngga_parser(self):
        self.gga.parse(self.gngga)
        self.assertFalse(self.gga.hasErrored())
        
        d =  self.gga.getData()
        
        gngga = self.gga.get(talker_id='$GNGGA',time=d[0],latitude=d[2],longitude=d[3],fix=d[5],nsat=d[4],dop=d[6],altitude=d[11],geoid=d[12])
        
        self.assertEqual(self.gngga,gngga)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()