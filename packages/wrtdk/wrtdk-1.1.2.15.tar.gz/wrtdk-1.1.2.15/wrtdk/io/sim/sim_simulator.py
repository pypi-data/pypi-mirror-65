'''
Created on Feb 20, 2019

@author: reynolds
'''

from wrtdk.io.sim.simulator import simulator
from wrtdk.parser.msg.wrtmsg import udp_wrapper

class sim_simulator(simulator):
    ''' classdocs '''

    def __init__(self):
        ''' Constructor '''
        super().__init__()    
        
    def read(self,filename,filt=None):
        simulator.read(self, filename)
        
        if not self.didError():
            # initialize the message parser and variable to store the bytes
            h = udp_wrapper()
            b = None
            pos = 0
            t = 0
            
            # open the file
            with open(filename,'rb') as f:
                b = f.read()# read in the bytes
                blen = len(b)# get the length of the buffer
                
                while pos < blen:
                    h.parse(b[pos:pos+h.LENGTH])
                    if h.hasErrored():
                        pos += 1
                        print('Error reading header:',h.hasErrored())
                        continue
                    
                    if filt is not None:
                        if h.getType() in filt:
                            self._msgs.append(b[pos:h.getMsgEnd(pos)])
                            self._dt.append(min(0.01,abs(h.getMCU()-t)))
                            t = h.getMCU()
                            
                        pos += h.getMsgEnd()
                    else:
                        self._msgs.append(b[pos:h.getMsgEnd(pos)])
                        self._dt.append(min(0.01,abs(h.getMCU()-t)))
                        t = h.getMCU()
                        pos += h.getMsgEnd()
                
                # re-adjust the change in time
                self._dt = self._dt[1::] + [4]
                
            if b is not None:
                print('Done')
                self._len = len(self._msgs)
                return True
            else:
                print('Error')
                return False
        return False
        
def test():
    ''' tests the simulator '''
    #port = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s = sim_simulator()
    s.read(r'C:\Users\reynolds\Documents\1704_madunit\data\20190227_imu-vmag_compare\imu_vcmag_test_1.dat')
    
if __name__ == '__main__':
    test()