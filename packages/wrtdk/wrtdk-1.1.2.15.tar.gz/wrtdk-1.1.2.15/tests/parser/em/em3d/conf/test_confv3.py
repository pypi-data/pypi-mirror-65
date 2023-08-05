'''
Created on Nov 20, 2019

@author: reynolds
'''
import unittest
from wrtdk.parser.em.em3d.conf.conf import confv3


class test_confv3(unittest.TestCase):


    def setUp(self):
        self.msg = b'CONF0\x0f\x02S\x03\x00\n\x01\x06\x86\x00\n\x00\x00\x03\xe8\n\x06\x03\x10\x00\x07\x00\x15\x00+\x00H\x00l\x00\x98\x00\xcb\x01\x05\x01G\x01\x90\x01\xe0\x028\x02\x97\x02\xfd\x03k\x03\xe8\n'
        self.msg = b'CONF\x04\x81\x02S\x03\x00\n\x01\x06\x86\x00\n\x00\x00\x03\xe8\n\x06\x03\x10\x00\x07\x00\x15\x00+\x00H\x00l\x00\x98\x00\xcb\x01\x05\x01G\x01\x90\x01\xe0\x028\x02\x97\x02\xfd\x03k\x03\xe8\n'
        self.conf = confv3()

    def tearDown(self):
        pass

    def test_confv1(self):
        self.conf.parse(b'msg')
        self.assertTrue(self.conf.hasErrored())
        
        self.conf.parse(self.msg)
        self.assertFalse(self.conf.hasErrored())

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()