'''
Created on Aug 17, 2018

@author: reynolds
'''

import numpy as np

class searcher(object):
    '''
    A class for searching a bytes buffer for a specific bytes
    '''
    
    def __init__(self,mid='!',w=1):
        ''' Constructor '''
        self.setID(mid)
        self.setMessageWidth(w)
        
    def search(self,buffer=b''):
        ''' searches the buffer for the byte id with the given width '''
        locs = []
        pos = 0
        
        # search the entire buffer
        while True:
            val = buffer.find(self._id,pos)
            
            # check to make sure the byte is there
            if val > -1:
                pos = val + 1
                if not locs:
                    # the list is empty
                    locs.append(val)
                else:
                    # list is not empty so check the message width
                    if val - locs[-1] > self._width:
                        locs.append(val)
            else:
                # if the value is negative then break. there are no more messages
                break
            
        return locs
        
    def setID(self,mid = '!'):
        ''' sets the id to look for '''
        self._id = mid
        
    def setMessageWidth(self,w=1):
        ''' sets the message width '''
        self._width = w

class data_buffer(object):
    ''' a class for buffering data for plotting or anaysis '''
    
    def __init__(self,ch=1,length=100,window=15,time=10):
        ''' constructor '''
        self._n = ch
        self._len = length
        self._time = time
        self.clear()
        self._window = window
        
    def get_length(self):
        ''' returns the length of the buffer '''
        return self._len
    
    def get_channels(self):
        '''returns the number of channels in the buffer '''
        return self._n
        
    def clear(self):
        '''  clears the buffer  '''
        self.data = self._init_data(self._len,self._n)# clear the data variable
        self.x = self._init_x(self._len,self._time)#clear the x variable
        self._counter = [0] * self._n# intialize the counter
        
    def _init_data(self,m,n):
        ''' initializes the data array '''
        data = []
        for _ in range(n):
            d = np.empty([m])
            d[:] = np.NaN
            data.append(d)
        return data
    
    def _init_x(self,m,t):
        ''' initializes the x data '''
        return np.linspace(0,t,m)
    
    def append(self,col=0,d=0):
        ''' appends data to the buffer'''
        self.data[col][0:-1] = self.data[col][1:]
        self.data[col][-1] = d
        self._counter[col] += 1
        
    def doUdpate(self,col=0):
        ''' tells the user when to update the plot '''
        if self._counter[col] > self._window:
            self._counter[col] = 0
            return True
        else: return False
        
class ring_buffer(object):
    
    def __init__(self,n=100):
        self.set_length(n)
        
    def set_length(self,n=100):
        self._len = n
        self._data = [None] * self._len
        self._head = 0
        self._tail = 0
        self._n = 0
        
    def get_length(self):
        return self._len
    
    def get_count(self):
        return self._n
    
    def is_full(self):
        return self._n == self._len
    
    def is_empty(self):
        return self._n == 0
    
    def has_space(self,n=1):
        return self._len - self._n >= n
    
    def view(self):
        return self._data[self._tail]
    
    def remove(self):
        b = self._data[self._tail]
        self._tail = (self._tail + 1) % self._len
        self._n -= 1
        return self._data[self._tail]
    
    def __str__(self, *args, **kwargs):
        return '%s[len:%d,tail:%d,head:%d,count:%d]' % (self.__class__,self._len,self._tail,self._head,self._n) 
    
    def get(self,n=1):
        if self.is_empty(): raise Exception('RingBufferEmpty','There is no data in the ring buffer yet')
        _start = min(self._tail+n,self._len-self._tail)
        _stop = max(0,self._tail+n-self._len)
        x = self._data[self._tail:self._tail+_start] + self._data[0:_stop]
        print('x:',x,'data[%d:%d]+data[%d:%d]'%(self._tail,self._tail+_start,
                                                0,_stop),_start,_stop,n)
        self._n -= n
        self._tail = (self._tail+n) % self._len
        return x
    
    def append(self,x=[]):
        _len = len(x)
        
        if self.is_full(): 
            print('Why am i here')
            raise Exception('RingBufferFull','Adding %d and %d exceeds the buffer length %d' %(_len,self._n,self._len))
        if not self.has_space(_len):
            print('here')
            raise Exception('RingBufferFull','Adding %d and %d exceeds the buffer length %d' %(_len,self._n,self._len))
        
        _start = min(_len,self._len-self._head)
        self._copy(_start,x,0)
        
        _stop = _len - _start
        self._copy(_stop,x,_start)
        
        self._n += _len# not full
        
    def _copy(self,n,src,start):
        self._data[self._head:self._head+n] = src[start:start+n]
        self._head = (self._head + n) % self._len
        
class byte_buffer(object):
    
    def __init__(self,b=[]):
        self.buffer = bytes(b)
        self.reset_position()
        
    def append(self,b):
        self.buffer = self.buffer + b
        self._calc()
        
    def _calc(self):
        self.len = len(self.buffer)
        self._rem()
        
    def _rem(self):
        self.rem = self.len - self.pos
        
    def prepend(self,b):
        self.buffer = b + self.buffer
        self._calc()
        
    def set_buffer(self,b):
        self.buffer = b
        self.reset_position()
        
    def clear(self):
        self.set_buffer(bytes())
        
    def get(self):
        try:
            b = self.buffer[self.pos]
            self.increment()
            return b
        except Exception as e:
            print(self,str(e),self.buffer)
    
    def view(self):
        return self.buffer[self.pos]
    
    def remove_head(self):
        self.buffer = self.buffer[self.pos::]
        self._calc()
        self.reset_position()
    
    def increment(self):
        self.pos += 1
        self._rem()
        
    def set_position(self,i):
        self.pos = i
        self._rem()
        
    def reset_position(self):
        self.pos = 0
        self.len = len(self.buffer)
        self._rem()
        
    def get_length(self):
        return self.len
    
    def is_empty(self):
        return self.rem == 0
    
    def __str__(self, *args, **kwargs):
        return '%s[len:%d,pos:%d,rem:%d]' % (self.__class__.__name__,
                                             self.len,
                                             self.pos,
                                             self.rem)