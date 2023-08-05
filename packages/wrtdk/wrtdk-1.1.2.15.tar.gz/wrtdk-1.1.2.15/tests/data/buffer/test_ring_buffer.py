'''
Created on Nov 5, 2019

@author: reynolds
'''

import unittest
from wrtdk.data.buffer.buffer import ring_buffer

class test_ring_buffer(unittest.TestCase):
    '''
    classdocs
    '''
    
    def test_length(self):
        length = 100
        b = ring_buffer(length)
        self.assertEqual(b.get_length(),length)
        
    def test_set_length(self):
        length = 10
        b = ring_buffer()
        b.set_length(length)
        self.assertEqual(b.get_length(),length)
        
    def test_is_full(self):
        length = 1
        b = ring_buffer(length)
        before = b.is_full()
        b.append([0])
        self.assertNotEqual(before,b.is_full())
        
    def test_is_empty(self):
        b = ring_buffer(10)
        empty = b.is_empty()
        b.append([1])
        not_empty = b.is_empty()
        self.assertNotEqual(empty,not_empty)
        
    def test_get_count(self):
        app = [1]
        b = ring_buffer(10)
        b.append([1])
        self.assertEqual(b.get_count(),len(app))
        
    def test_has_space(self):
        b = ring_buffer(10)
        under,over = b.has_space(b.get_length()-1),b.has_space(b.get_length()+1)
        self.assertNotEqual(under,over)
    
    def test_append_get(self):
        b = ring_buffer(10)
        x = list(range(0,b.get_length()))
        b.append(x)
        x0 = b.get(1)
        self.assertEqual(x[0:1],x0)
        n = [100]
        b.append(n)
        xn = b.get(b.get_length())
        self.assertEqual(x[1::] + n,xn)
        
if __name__ == '__main__':
    unittest.main()
        