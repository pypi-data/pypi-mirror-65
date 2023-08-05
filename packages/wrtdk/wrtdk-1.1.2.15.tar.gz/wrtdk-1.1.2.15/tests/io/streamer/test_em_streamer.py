'''
Created on Nov 13, 2019

@author: reynolds
'''
import unittest, sys
from wrtdk.io.streamer.em_streamer import em_streamer
from wrtdk.comms.comms import tcp_port
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication

class main_window(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        s = tcp_port('169.254.10.100',10011,1)
        self.t = em_streamer(port=s)
        self.t.new_timeout.connect(self._new_timeout)
        self.t.new_em.connect(self._new_em)
        self.t.new_conf.connect(self._new_conf)
        self.t.new_gga.connect(self._new_gga)
        self.t.start()
        
        self.recv = [False] * 4
        
    def check(self):
        check = True
        for r in self.recv[1::]: check = check and r
        if check:
            self.t.stop()
            self.t.wait()
            self.close()
        
    @pyqtSlot()
    def _new_timeout(self):
        print('timeout')
        self.recv[0] = True
        self.check()
    
    @pyqtSlot(int,int,list)
    def _new_em(self,mtype,mlen,data):
        print(mtype,mlen,data)
        self.recv[1] = True
        self.check()
    
    @pyqtSlot(int,int,list)
    def _new_conf(self,mtype,mlen,data):
        print(mtype,mlen,data)
        self.recv[2] = True
        self.check()
    
    @pyqtSlot(int,int,list)
    def _new_gga(self,mtype,mlen,data):
        print(mtype,mlen,data)
        self.recv[3] = True
        self.check()

class Test(unittest.TestCase):
    
    def setUp(self):
        app = QApplication(sys.argv)
        self.widget = main_window()
        self.widget.show()
        app.exec_()

    def test_thread_running(self):
        self.assertTrue(self.widget.t.isRunning())
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()