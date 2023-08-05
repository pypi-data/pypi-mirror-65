'''
Created on Nov 20, 2019

@author: reynolds
'''
import unittest
from wrtdk.parser.em.em3d.em.em import emv1


class test_emv1(unittest.TestCase):


    def setUp(self):
        self.msg = b't\xd5L\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\n'
        self.emv1 = emv1()
        
    def tearDown(self):
        pass

    def test_parse(self):
        self.emv1.parse(self.msg)
        self.assertTrue(self.emv1.hasErrored())
        
        self.emv1.set_bins(16)
        
        self.emv1.parse(self.msg)
        
        self.assertFalse(self.emv1.hasErrored())
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()