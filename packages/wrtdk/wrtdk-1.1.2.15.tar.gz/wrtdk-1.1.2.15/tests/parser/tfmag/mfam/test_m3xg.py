'''
Created on Jan 20, 2020

@author: Reynolds
'''
import unittest
from wrtdk.parser.tfmag.mfam import mx3g

class Test(unittest.TestCase):

    def setUp(self):
        self.msg = b'\xea\x7f\x00\x04CA)<\x00\x04\x00\x04C\xf2\x99\xa8\x1c\r\x00\x009%\x00\x00\x00\x00\x00\x00'
        self.m = mx3g()

    def test_parse(self):
        self.m.parse(self.msg)
        
        self.assertFalse(self.m.hasErrored())
        
        data = self.m.getData()
        
        msg = self.m.get(m1=data[0],
                        m2=data[1],
                        v1=data[13],
                        v2=data[14],
                        s1=data[6],
                        s2=data[7],
                        count=data[9],
                        failed=data[12],
                        synch=data[11],
                        pps=data[10],
                        a0=data[15],
                        a1=data[16],
                        a2=data[17],
                        adc0=data[2],
                        adc1=data[3],
                        adc2=data[4],
                        temp=data[5])
        
        self.m.parse(msg)
        
        self.assertFalse(self.m.hasErrored())
        
        d = self.m.getData()
        
        #print(data)
        #print(d)
        
        self.assertEqual(data,d)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()