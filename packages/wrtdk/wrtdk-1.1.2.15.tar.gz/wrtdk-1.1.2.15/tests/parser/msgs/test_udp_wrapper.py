'''
Created on Dec 5, 2019

@author: Reynolds
'''
import unittest
from wrtdk.parser.msg.wrtmsg import udp_wrapper


class Test(unittest.TestCase):


    def setUp(self):
        self.wrapper = udp_wrapper()

    def test_hasErrored(self):
        msg = b'$SYSTM\x00\x00\xfbs\x00\x00\x13\x03L1[{\x1e\xcd\x00\x00\x00o\x00\x00\x00\x00\x00\x00\x00\x9c\x00\x00)\x1e'
        self.wrapper.parse(msg)
        
        self.assertFalse(self.wrapper.hasErrored())
        
    def test_get_parse(self):
        mtype = '$SYSTM'
        sen_id = 1001
        sys_id = 1234
        fid = 101
        status = 'AG'
        t_s = 10
        t_ms = 123
        mlen=42
        m = self.wrapper.get(mtype=mtype,sen_id=sen_id,sys_id=sys_id,
                             fid=fid,status=status,t_s=t_s, t_ms=t_ms,
                             mlen=mlen)
        
        self.wrapper.parse(m)
        
        self.assertFalse(self.wrapper.hasErrored())
        
        self.assertEqual(mtype,self.wrapper.getType())
        self.assertEqual(sen_id,self.wrapper.getSensorID())
        self.assertEqual(sys_id,self.wrapper.getSystemID())
        self.assertEqual(fid,self.wrapper.getFiducial())
        self.assertEqual(status,self.wrapper.getStatus())
        self.assertEqual(t_s+t_ms*1e-3,self.wrapper.getMCU())
        self.assertEqual(mlen,self.wrapper.getLength())

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()