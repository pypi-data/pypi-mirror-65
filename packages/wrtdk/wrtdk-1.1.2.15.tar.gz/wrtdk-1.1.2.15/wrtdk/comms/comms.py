'''
Created on Aug 17, 2018

@author: reynolds
'''

import sys, glob, serial, socket, time, select

class CommsPort(object):
    '''
    a super class for a communication port
    '''
    def __init__(self,port=''):
        ''' constructor '''
        self.set_name(port)
        self.port = None
        
    def set_name(self,name):
        self.name = name

    def open(self):
        ''' opens the port '''
        print('Opening ' + self.name + ' ... ',end='')
        pass

    def available(self):
        ''' checks to see if anything is available '''
        pass
    
    def read(self,n):
        pass
    
    def send(self,message):
        pass

    def close(self):
        ''' closes the port ''' 
        print('Closing ' + self.name + ' ... ',end='')
        try:
            self.port.close()
            print('Done')
            return True
        except Exception as e:
            print('Error. %s'%str(e))
            return False

    ''' reads a single line of ascii data '''
    def readLine(self):
        pass

    ''' checks to see if anything is open '''
    def isOpen(self):
        pass

class SerialPort(CommsPort):
    '''
    a serial data communication port
    '''
    def __init__(self,port=[],baud=9600,timeout=1):
        ''' Constructor '''
        super().__init__(port + '@' + str(baud))
        self.open(port,baud,timeout=timeout)

    def open(self,port,baud,timeout=0):
        self.set_name('%s@%d with %d s timeout'%(port,baud,timeout))
        ''' opens the serial port'''
        super().open()
        try:
            self.port = serial.Serial(port,baud,timeout=timeout)
            print('Done')
        except (OSError, serial.SerialException):
            print('Error. SerialException')

    def available(self):
        ''' checks to see if data is available '''
        super().available()
        return self.port.in_waiting
    
    def read(self,n=None):
        if n == None: n = self.port.inWaiting()
        return self.port.read(n), (self.port.name,self.port.baudrate)
        
    def readLast(self):
        ''' reads data until a full new message is read '''
        buffer = ''# initialize the buffer
        while True:
            buffer = buffer + self.port.read(self.port.inWaiting()).decode()# concat the buffer
            if '\n' in buffer: # check to see if there are any full messages
                lines = buffer.split('\n')# split on the line feed
                #print(lines)# uncomment to debug
                # return the most recent message
                if lines[-1].endswith('\r'):
                    return lines[-1][:-1].encode(),(self.port.name,self.port.baudrate)# received a full message last
                else:
                    return lines[-2].encode(),(self.port.name,self.port.baudrate)# return last full message
        
    def write(self,msg):
        ''' writes a message '''
        #if isinstance(msg,typing.ByteString):
        #    print('Writing %s' % msg.decode() )
        try:
            self.port.write(msg)
        except Exception as e:
            print('Error',str(e))

    def readLine(self):
        ''' reads one line of data '''
        super().readLine()
        try:
            return self.port.readline(), (self.port.name,self.port.baudrate)
        except (OSError, serial.SerialException):
            return None, None

    def isOpen(self):
        ''' Checks if the port is open'''
        if self.port != []:
            return self.port.isOpen()
        else:
            return False
        
class tcp_port(CommsPort):
    
    def __init__(self,address='127.0.0.1',port=4444,timeout=1000,connect=True,debug=False,filename=''):
        super().__init__(address+'@'+str(port))
        self.debug=debug
        self.filename=filename
        self.address=address
        self.port=port
        self.timeout=timeout
        self.size=float('inf')
        self.is_open=False
        if connect: 
            self.is_open=self.open(address,port,timeout)
        
    def open(self,address,port,timeout=0):
        if(self.debug):
            
            try:
                self.set_name(self.filename)
                super().open()
                self.port=open(self.filename, mode='rb')
                print('Done')
                self.is_open=True
                return True
            except Exception as e:
                print('Error. ',str(e))
                return False
                
        
        else:
            self.set_name('%s@%d with %d s timeout'%(address,port,timeout))
            super().open()
            try:
                self.port = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                if timeout != 0: self.port.settimeout(timeout)
                self.port.connect((address,port))
                print('Done')
                self.is_open=True
                return True
            except Exception as e:
                self.port = None
                print('Error. ',str(e))
                return False
        
    def send(self,message,address,port):
        ''' send a message to the port '''
        self.port.sendto(message,(address,port))
        
    def read(self,n):
        ''' reads a message of n bytes from the port '''
        if self.debug:
            try:
                msg=self.port.read(n)
                return msg,None
            except Exception as e:
                print(str(e))
                return None, str(e)
        try:
            read_socket,_,_=select.select([self.port],[],[],60)
            if(len(read_socket)!=0):
                message = self.port.recv(n)
                return message,None
            else:
                return None,None
        except Exception as e:
            print(str(e))
            return None, str(e)
    def readLine(self):
        ''' reads one line of data '''
        super().readLine()
        try:
            return self.port.readline(), (self.port.name,self.port.baudrate)
        except (OSError, serial.SerialException):
            return None, None
    def get_size(self):
        return float('inf')
class UDPServerPort(CommsPort):
    '''  a class for a udp server port '''
    def __init__(self,address='',port=0,timeout=1000,connect=True):
        ''' constructor '''
        super().__init__(address+'@'+str(port))
        if connect: self.open(address,port,timeout)
        
    def open(self,address,port,timeout=0):
        ''' opens the port '''
        self.set_name('%s@%d with %d s timeout'%(address,port,timeout))
        super().open()
        
        try:
            self.port = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            self.port.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            self.port.bind((address,port))
            if timeout != 0:
                self.port.settimeout(timeout)
                print('Done')
        except Exception as e:
            self.port = None
            print('Error. ',str(e))
        
    def send(self,message,address,port):
        ''' send a message to the port '''
        self.port.sendto(message,(address,port))
        
    def read(self,n):
        ''' reads a message of n bytes from the port '''
        message, address  = self.port.recvfrom(n)
        return message, address

class PortFinder(object):
    '''
    an abstract class for finding available ports
    '''
    def __init__(self):
        ''' constructor '''
        pass

    def update(self):
        ''' updates the list of available ports '''
        pass

class SerialPortFinder(object):
    '''
    This class is designed to find all available ports to the user.
    '''
    def __init__(self):
        ''' Constructor '''
        self.ports = []
        if sys.platform.startswith('win'):
            self.ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            self.ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            self.ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')
        self.update()

    def update(self):
        ''' Updates the ports available to the user '''
        self.result = []
        for port in self.ports:
            try:
                s = serial.Serial(port)
                s.close()
                self.result.append(port)
            except (OSError, serial.SerialException):
                pass
            
def testUDPServerClass():
    ''' tests the udpserver receive functionality'''
    port = UDPServerPort('',8000)
    message,address = port.read(1024)
    print(str(address),message,len(message))
    port.close()
    
def testUDPPortReader():
    port = UDPServerPort('',8112,1)
    
    i = 0
    while i < 500:
        message,address = port.read(1024)
        print(str(address),message)
        i += 1
            
    port.close()
    #reader.stopLog()
    
def testUDPPortWriter():
    print('Starting')
    port = UDPServerPort('',7654)
    
    for i in range(10):
        msg = 'message'
        print('Sending message',i,'... ',end='')
        port.send(bytes(msg,'utf-8'),'10.1.10.58',7654)
        print('Done')
        time.sleep(1)
        
    port.close()
        
    print('Done')
    
def testSerialReadLine():
    ser = SerialPort('COM8',9600,timeout=0.5)
    
    for i in range(10):
        line,addr = ser.readLine()
        print(i,addr,line.decode().strip())
    
    ser.close()

def testSerialReadLast():
    ser = SerialPort('COM8',9600,timeout=0)
    
    for i in range(10):
        line = ser.readLast()
        print(i,line.decode().strip())
    
    ser.close()

if __name__ == '__main__':
    #send0SD()
    #set1540Poll()
    testUDPServerClass()
    #testUDPPortReader()
    #testUDPPortWriter()
    #testSerialReadLast()
    #testSerialReadLine()
    
    