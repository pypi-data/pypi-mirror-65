'''
Created on Aug 17, 2018

@author: reynolds
'''

from wrtdk.comms.comms import SerialPort

def set_auto(port,baud=9600,close=True,verb=True):
    if type(port) == type(str): port = SerialPort(port,baud)
    elif type(port) != type(SerialPort()):
        print('Please make sure that the port entry is a str or SerialPort object')
        return
    else:
        print('Please make sure that the port entry is a str or SerialPort object')
        return
    
    # write commands to fluxgate
    port.write(b'0L\r')
    if verb: print(port.readLine())
    port.write(b'0wc01b5A\r')
    if verb: print(port.readLine())
    port.write(b'0L\r')
    if verb: print(port.readLine())
    port.write(b'0wc08b10\r')
    if verb: print(port.readLine())
    
    # close the port
    if close: port.close()
    
def set_poll(port,baud=9600,close=True,verb=True):
    if type(port) == type(str): port = SerialPort(port,baud)
    elif type(port) != type(SerialPort()):
        print('Please make sure that the port entry is a str or SerialPort object')
        return
    else:
        print('Please make sure that the port entry is a str or SerialPort object')
        return
    
    # write commands to fluxgate
    port.write(b'0l\r')
    if verb: print(port.readLine())
    port.write(b'0wv1\r')
    if verb: print(port.readLine())
    port.write(b'0L\r')
    if verb: print(port.readLine())
    port.write(b'0wc01b00\r')
    if verb: print(port.readLine())
    
    #close the port
    if close: port.close()
    
def poll(port,baud=9600,close=True,verb=True):
    if type(port) == type(str): port = SerialPort(port,baud)
    elif type(port) != type(SerialPort()):
        print('Please make sure that the port entry is a str or SerialPort object')
        return
    else:
        print('Please make sure that the port entry is a str or SerialPort object')
        return
    
    # write commands to fluxgate
    port.write(b'0SD')
    print(port.readLine())
    
    #close the port
    if close: port.close()

class ap1540(object):
    ''' a parser for the ap150 fluxgate '''

    def __init__(self):
        ''' Constructor '''
        super().__init__()
        
        # initialzie properties
        self.reset()
        
        # define constants
        self.COUNT_2_NT = 1000/75
        
    def reset(self):
        ''' resets the properties '''
        self._bx = self._nan()
        self._by = self._nan()
        self._bx = self._nan()
        
    def parse(self,msg):
        ''' parses the ap1540 message '''
        print(msg)