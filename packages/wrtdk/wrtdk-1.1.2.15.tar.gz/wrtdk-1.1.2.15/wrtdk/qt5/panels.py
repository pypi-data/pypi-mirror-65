'''
Created on Aug 17, 2018

@author: reynolds
'''

from serial import Serial
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QGridLayout, QFrame, QWidget,QApplication, QPushButton, QLabel, QComboBox,\
    QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.Qt import QLineEdit, QTimer
from wrtdk.data.state.state import state
from wrtdk.qt5.animations import CubeWidget
from wrtdk.qt5.plots import PlotParameters, Plot2DWidget, Plot3DWidget

import sys, random, os
import numpy as np
from wrtdk.qt5.widgets import SoftwareLED, wrt_widget, FHLabelledInputWidget

class HealthWidget(wrt_widget):
    ''' a widget for displaying the health status of the sensor '''
    
    def __init__(self,parent=None,row=None,col=None,timeout=5000):
        ''' constructor '''
        super().__init__(parent)
        
        if row is None: row = range(1,10)
        if col is None: col = [0 for _ in range(10)]
        
        self.timeout = timeout
        
        # initialize widgets
        self.sys = self._getQLineEdit()
        self.syst = QTimer()
        self.syss = state()
        self.syst.timeout.connect(lambda: self.setSystemState('NC'))
        self.gpgga = self._getQLineEdit()
        self.gpggat = QTimer()
        self.gpggas = state()
        self.gpggat.timeout.connect(lambda: self.setGPGGAState('NC'))
        self.gpvtg = self._getQLineEdit()
        self.gpvtgt = QTimer()
        self.gpvtgs = state()
        self.gpvtgt.timeout.connect(lambda: self.setGPVTGState('NC'))
        self.gprmc = self._getQLineEdit()
        self.gprmct = QTimer()
        self.gprmcs = state()
        self.gprmct.timeout.connect(lambda: self.setGPRMCState('NC'))
        self.gphdt = self._getQLineEdit()
        self.gphdtt = QTimer()
        self.gphdts = state()  
        self.gphdtt.timeout.connect(lambda: self.setGPHDTState('NC'))
        self.gpvhw = self._getQLineEdit()
        self.gpvhwt = QTimer()
        self.gpvhws = state()
        self.gpvhwt.timeout.connect(lambda: self.setGPVHWState('NC'))
        self.vmag = self._getQLineEdit()
        self.vmagt = QTimer()
        self.vmags = state()
        self.vmagt.timeout.connect(lambda: self.setVMAGState('NC'))
        self.imu = self._getQLineEdit()
        self.imut = QTimer()
        self.imus = state()
        self.imut.timeout.connect(lambda: self.setIMUState('NC',0,0,0,0))
        self.sonar = self._getQLineEdit()
        self.sonart = QTimer()
        self.sonars = state()
        self.sonart.timeout.connect(lambda: self.setSonarState("NC"))
        self.lidar = self._getQLineEdit()
        self.lidart = QTimer()
        self.lidars = state()
        self.lidart.timeout.connect(lambda: self.setLidarState("NC"))
        self.pltfm = self._getQLineEdit()
        self.pltfms = state()
        self.gprip = self._getQLineEdit()
        self.gpript = QTimer()
        self.gprips = state()
        self.gpript.timeout.connect(lambda: self.setGPRIPState("NC"))
        
        # layout widget
        l = QGridLayout()
        #Always by itself top left.
        l.addWidget(self._getLabel('System Health',10,Qt.AlignCenter),0,0,1,4)
        #Always by itself top left.
        l.addWidget(self._getLabel('SYS:'),0,4,1,1)
        l.addWidget(self.sys,0,5,1,1)
        if(row[0]!=-1):
            l.addWidget(self._getLabel('PLTFM:'),row[0],2*col[0],1,1)
            l.addWidget(self.pltfm,row[0],2*col[0]+1,1,1)
        #row[0]
        #adding -1 for DO NOT INCLUDES
        if(row[1]!=-1):
            l.addWidget(self._getLabel('VMAG:'),row[1],2*col[1],1,1)
            l.addWidget(self.vmag,row[1],2*col[1]+1,1,1)
        if(row[2]!=-1):
            l.addWidget(self._getLabel('GPGGA:'),row[2],2*col[2],1,1)
            l.addWidget(self.gpgga,row[2],2*col[2]+1,1,1)
        if(row[3]!=-1):
            l.addWidget(self._getLabel('GPRMC:'),row[3],2*col[3],1,1)
            l.addWidget(self.gprmc,row[3],2*col[3]+1,1,1)
        if(row[4]!=-1):
            l.addWidget(self._getLabel('GPVTG:'),row[4],2*col[4],1,1)
            l.addWidget(self.gpvtg,row[4],2*col[4]+1,1,1)
        if(row[5]!=-1):
            l.addWidget(self._getLabel('GPVHW:'),row[5],2*col[5],1,1)
            l.addWidget(self.gpvhw,row[5],2*col[5]+1,1,1)
        if(row[6]!=-1):
            l.addWidget(self._getLabel('GPHDT:'),row[6],2*col[6],1,1)
            l.addWidget(self.gphdt,row[6],2*col[6]+1,1,1)
        if(row[7]!=-1):
            l.addWidget(self._getLabel('IMU:'),row[7],2*col[7],1,1)
            l.addWidget(self.imu,row[7],2*col[7]+1,1,1)
        if(row[8]!=-1):
            l.addWidget(self._getLabel('SONAR:'),row[8],2*col[8],1,1)
            l.addWidget(self.sonar,row[8],2*col[8]+1,1,1)
        if(row[9]!=-1):
            l.addWidget(self._getLabel('LIDAR:'),row[9],2*col[9],1,1)
            l.addWidget(self.lidar,row[9],2*col[9]+1,1,1)
        if(row[11]!=-1):
            l.addWidget(self._getLabel('GPRIP:'),row[11],2*col[11],1,1)
            l.addWidget(self.gprip,row[11],2*col[11]+1,1,1)
        l.addItem(QSpacerItem(10,10,QSizePolicy.Expanding,QSizePolicy.Expanding),max(row)+1,0,1,col[-1])
        #l.setVerticalSpacing(10)
        self.setLayout(l)
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        
    def _getLabel(self,text='',size=8,align=Qt.AlignRight|Qt.AlignVCenter):
        ''' sets the label font and size '''
        lbl = QLabel(text)
        lbl.setFont(QtGui.QFont('Times',size,QtGui.QFont.Bold))
        lbl.setAlignment(align)
        return lbl
        
    def _getQLineEdit(self,text='',readonly=True):
        ''' sets the line edit '''
        txt = QLineEdit()
        txt.setReadOnly(readonly)
        return txt
    
    def setStarted(self):
        ''' starts the widge '''
        self.syst.start(self.timeout)
        self.gpggat.start(self.timeout)
        self.gprmct.start(self.timeout)
        self.gpvtgt.start(self.timeout)
        self.gphdtt.start(self.timeout)
        self.gpvhwt.start(self.timeout)
        self.vmagt.start(self.timeout)
        self.imut.start(self.timeout)
        self.lidart.start(self.timeout)
        self.sonart.start(self.timeout)
        self.gpript.start(self.timeout)
    
    def setPlatformStarted(self):
        ''' sets the started platform state '''
        self.setPlatformState('AG')
        
    def setPlatformStopped(self):
        ''' sets the stoped platform state '''
        self._reset(self.pltfm)
        self.pltfms.reset()
        
    def setStopped(self):
        ''' resets the entire widget '''
        self.syst.stop()
        self._reset(self.sys)
        self.syss.reset()
        self.gpggat.stop() 
        self._reset(self.gpgga)
        self.gpggas.reset()
        self.gprmct.stop()
        self._reset(self.gprmc)
        self.gprmcs.reset()
        self.gpvtgt.stop()
        self._reset(self.gpvtg)
        self.gpvtgs.reset()
        self.gphdtt.stop()
        self._reset(self.gphdt)
        self.gphdts.reset()
        self.gpvhwt.stop()
        self._reset(self.gpvhw)
        self.gpvhws.reset()
        self.vmagt.stop()
        self._reset(self.vmag)
        self.vmags.reset()
        self.imut.stop()
        self._reset(self.imu)
        self.imus.reset()
        self.lidart.stop()
        self._reset(self.lidar)
        self.lidars.reset()
        self.sonart.stop()
        self._reset(self.sonar)
        self.sonars.reset()
        self._reset(self.gprip)
        self.gprips.reset()
        
    def _reset(self,widget):
        ''' resets the widget '''
        widget.setText('')
        widget.setStyleSheet('')
    
    def _resett(self,timer):
        ''' resets the timer '''
        #timer.stop()
        timer.start(self.timeout)
    
    def setVMAGState(self,state=''):
        ''' sets the state of the vector mag '''
        self._resett(self.vmagt)
        if not self.vmags.isDifferent(state): return
        self._setState(self.vmag,state)
        
    def setGPGGAState(self,state):
        ''' sets the state of the gpgga '''
        self._resett(self.gpggat)
        if not self.gpggas.isDifferent(state): return
        self._setState(self.gpgga, state)
        
    def setGPRMCState(self,state):
        ''' sets the state of the gprmc '''
        self._resett(self.gprmct)
        if not self.gprmcs.isDifferent(state): return
        self._setState(self.gprmc, state)
        
    def setGPVTGState(self,state):
        ''' sets the state of the gpvtg '''
        self._resett(self.gpvtgt)
        if not self.gpvtgs.isDifferent(state): return
        self._setState(self.gpvtg, state)
        
    def setGPHDTState(self,state):
        ''' sets the state of the gphdt '''
        self._resett(self.gphdtt)
        if not self.gphdts.isDifferent(state): return
        self._setState(self.gphdt, state)
        
    def setGPVHWState(self,state):
        ''' sets the state of the gpvhw '''
        self._resett(self.gpvhwt)
        if not self.gpvhws.isDifferent(state): return
        self._setState(self.gpvhw, state)
        
    def setSystemState(self,state):
        ''' sets the state of the system '''
        self._resett(self.syst)
        if not self.syss.isDifferent(state): return
        self._setState(self.sys, state)
        
    def setSonarState(self,state):
        ''' sets the state of the sonar sensor '''
        self._resett(self.sonart)
        if not self.sonars.isDifferent(state): return
        self._setState(self.sonar, state)
        
    def setLidarState(self,state):
        ''' sets the state of the lidar sensor '''
        self._resett(self.lidart)
        if not self.lidars.isDifferent(state): return
        self._setState(self.lidar, state)
        
    def setIMUState(self,state,imu=0,acc=0,gyr=0,mag=0):
        ''' sets the state of the Microstrain IMU '''
        self._resett(self.imut)
        if not self.imus.isDifferent(state): return
        self._setState(self.imu, state)
        #self.imu.setText('%s %d%d%d%d'%(self.imu.text(),imu,acc,gyr,mag))# uncomment for BNO055 IMU
        
    def setPlatformState(self,state):
        ''' sets the platform state '''
        # there is no timer for  this software led
        if not self.pltfms.isDifferent(state): return
        self._setState(self.pltfm, state)
        
    def setGPRIPState(self,state):
        ''' sets the state of the gprip message '''
        self._resett(self.gpript)
        if not self.gprips.isDifferent(state): return
        self._setState(self.gprip, state)
class altQualWidget(QFrame):
    def __init__(self, parent=None):
        QFrame.__init__(self,parent=None)
        self.n=1
        self.sensors={}
        
        self.l=QGridLayout()
        lab=QLabel('ID:')
        alt=QLabel('Altitude:')
        quality=QLabel('Quality:')
        self.l.addWidget(lab,0,0,1,1)
        self.l.addWidget(alt,1,0,1,1)
        self.l.addWidget(quality,2,0,1,1)
        self.setLayout(self.l)
    def addSensor(self,ID,alt,quality='NA'):
        self.sensors[ID]=QLabel(str(round(alt,2))),QLabel(str(quality))
        self.l.addWidget(QLabel(ID),         0,self.n,1,1)
        self.l.addWidget(self.sensors[ID][0],1,self.n,1,1)
        self.l.addWidget(self.sensors[ID][1],2,self.n,1,1)
        self.n+=1
    def setAlt(self,ID,alt):
        self.sensors[ID][0].setText(str(round(alt,2)))
    def setQuality(self,ID,quality):
        self.sensors[ID][1].setText(str(quality))
                                   
class MapWidget(QFrame):
    ''' for multiple sensors '''
    
    def __init__(self,parent=None,lsize=10,tsize=16):
        ''' constructor '''
        QFrame.__init__(self,parent)
        self.alts=altQualWidget()
        self.syms=['o','^','s','*']
        self.sensors=[]
        self.num=0
        self.plot = Plot2DWidget(parameters = 
                                 PlotParameters('UTM Map',
                                    'Easting (m)',
                                    'Northing (m)',
                                    lsize=lsize,
                                    tsize=tsize),
                                    lines=0)
        self.plot.set_aspect()
        self.leg=[]
        self.track=1;
        self.bxsize=10;
#         self.plot.add_line([], [],'ko-')#black line
#         self.plot.add_line([],[],'go')  #green dot
#         self.plot.set_legend(['Path','Current','Track'])
        self.targets=0
        l = QGridLayout()
        l.addWidget(self.alts,0,0)
        l.addWidget(self.plot,1,0)
        
        self.setLayout(l)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
    def setupTargets(self,x,y,IDs):
        self.targets=1
        self.plot.add_line([],[],'ro')
        self.leg.append('Targets')
        for i in range(len(IDs)):
            self.plot.append(x,y,line=0,autoscale=False)
            
    def addsensor(self,name):
        self.sensors.append(str(name))
        self.plot.add_line([],[],'k'+self.syms[self.num]+'-')
        self.plot.add_line([],[],'g'+self.syms[self.num])
        self.leg.append('Sensor '+str(self.sensors[self.num])+' path')
        self.leg.append('Sensor '+str(self.sensors[self.num])+' current')
        self.plot.set_legend(self.leg)
        self.num+=1
    def appendPath(self,name,x,y,z):
        for i in range(len(self.sensors)):
            if self.sensors[i]==name:
                self.plot.append(x,y,line=2*i+self.targets,autoscale=True)
                self.plot.set_data(x,y,2*i+self.targets+1,autoscale=True)
                
    def setTrack(self,sensor,bxsize=10):
        for i in range(len(self.sensors)):
            if self.sensors[i]==sensor:
                self.track=i
        self.bxsize=bxsize
                
    def clear(self):
        ''' clears all the plots, text boxes and software LEDs '''
        print("CLEARING MAP")
        for i in range(self.plot.line_total()-1,3,-1):
            self.plot.remove_line(i)
        for i in range(self.num):
            self.plot.clear_line(i)
        self.num=0
        self.plot.clear()

class SystemWidget(QFrame):
    ''' 
    a class for connecting and logging data form a system
    '''
    
    def __init__(self,parent=None):
        ''' constructor '''
        QFrame.__init__(self,parent)
        
        # define widgets
        font = QtGui.QFont('Times',12,QtGui.QFont.Bold)
        self.connect = QPushButton('Connect')
        self.connect.setStyleSheet('background-color: green')
        self.connect.setFont(font)
        self.output = LogWidget(self)
        self.output.setEnabled(False)
        self.timestamp = FHLabelledInputWidget(self,'MCU Time:','',0)
        self.timestamp.setFont(QtGui.QFont('Times',8,QtGui.QFont.Bold))
        self.timestamp.widget.setReadOnly(True)
        
        # layout grid
        l = QGridLayout()
        l.addWidget(self.connect,0,0,1,1)
        l.addWidget(self.timestamp,0,1,1,2)
        l.addWidget(self.output,1,0,1,2)
        l.setSpacing(0)
        l.setColumnStretch(0,1)
        l.setColumnStretch(1,3)
        self.setContentsMargins(0, 0, 0, 0)
        self.setLayout(l)
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        
        # define stat variables
        self._connected = False
        
    def isConnected(self):
        ''' returns whether the system is connected '''
        return self._connected
        
    def setConnected(self):
        ''' sets the widget in a connected state '''
        self.connect.setStyleSheet("background-color: red")
        self.connect.setText("Disconnect")
        self.output.setEnabled(True)
        self._connected = True
            
    def setDisconnected(self):
        ''' sets the widget in a disconnected state '''
        self.connect.setStyleSheet("background-color: green")
        self.connect.setText("Connect")
        self.output.setEnabled(False)
        self._connected = False

class LogWidget(QWidget):
    ''' a widget for logging collected data '''
    
    def __init__(self,parent=None,default='',lfnt=None,tfnt=None,align=None,
                 start_color='green',stop_color='red'):
        ''' constructor '''
        QWidget.__init__(self,parent)
        
        # define var
        self._line = 1
        self._startc = start_color
        self._stopc = stop_color
        
        # define widgets
        self.txt = self._get_qlineedit('',tfnt,align)
        self.line = self._get_qlineedit('%d'%self._line,lfnt, align)
        self.line.setReadOnly(True)
        self.log = self._get_qpushbutton('LOG',lfnt,align)
        self.pause = self._get_qpushbutton('PAUSE',lfnt,align)
        self.pause.setEnabled(False)
        self.pause.setStyleSheet('')
        plus = self._get_qpushbutton('+',lfnt,align)
        plus.clicked.connect(self._plus)
        minus = self._get_qpushbutton('-',lfnt,align)
        minus.clicked.connect(self._minus)
        self.log.setStyleSheet('background-color: %s'%self._startc)
        
        # layout widgets
        l = QGridLayout()
        l.addWidget(self.txt,0,0,1,3)
        l.addWidget(minus,1,0,1,1)
        l.addWidget(plus,1,1,1,1)
        l.addWidget(self.line,1,2,1,1)
        l.addWidget(self.log,0,3,1,1)
        l.addWidget(self.pause,1,3,1,1)
        l.setColumnStretch(0,1)
        l.setColumnStretch(1,1)
        l.setColumnStretch(2,1)
        l.setColumnStretch(3,1)
        self.setLayout(l)
        
        # define state variables
        self._log = False
        self._pause = False
        
    def _get_qlineedit(self,txt='',fnt=None,align=None):
        ''' creates the qlabels '''
        l = QLineEdit(txt)
        if fnt is not None: l.setFont(fnt)
        if align is not None: l.setAlignment(align)
        return l
        
    def _get_qpushbutton(self,txt='',fnt=None,align=None):
        ''' creates a qpush button '''
        b = QPushButton(txt)
        if fnt is not None: b.setFont(fnt)
        if align is not None: b.setAlignment(align)
        return b
        
    def setEnabled(self,enabled=False):
        ''' sets the enabled state of the logger '''
        self.log.setEnabled(enabled)
        self.txt.setReadOnly(not enabled)
        
    def isLogging(self):
        ''' returns whether the widget is in log mode or not '''
        return self._log

    def isPaused(self):
        return self._pause
    
    def setStarted(self):
        ''' sets the widget in logging mode '''
        self.log.setStyleSheet('background-color: %s'%self._stopc)
        self.log.setText('STOP')
        self._log = True
        #self.pause.setStyleSheet('background-color: %s'%self._stopc)

    def setStopped(self):
        ''' sets the widget in not logging mode '''
        self.log.setStyleSheet('background-color: %s'%self._startc)
        self.log.setText('LOG')
        self._log = False
        self._plus()
        self.pause.setEnabled(False)
        self.pause.setStyleSheet('')
        if self._pause: self.setResumed()
        
    def setPaused(self):
        self.log.setStyleSheet('background-color: red')
        self.log.setText('RESUME')
        
    def setResumed(self):
        self.log.setStyleSheet('background-color: green')
        self.log.setText('PAUSE')

    def _plus(self):
        self._line += 1
        self.line.setText('%d' % self._line)
    
    def _minus(self):
        if self._line > 1: self._line -= 1
        self.line.setText('%d' % self._line)
    
    def getFilename(self):
        ''' returns the current filename '''
        return '%s_%d' % (self.txt.text(),self._line)

class GPGGAWidget(QFrame):
    ''' a widget for displaying the GPGGA information '''
    def __init__(self,parent=None,rtk=False,lfnt=None,
                 tfnt=None,align=None,frame=QFrame.StyledPanel | QFrame.Plain):
        ''' constructor '''
        QFrame.__init__(self,parent)
        
        # create the widgets
        self._time = self._get_qlineedit(tfnt,align)
        self._lat = self._get_qlineedit(tfnt,align)
        self._lon = self._get_qlineedit(tfnt,align)
        self._fix = self._get_qlineedit(tfnt,align)
        self._n = self._get_qlineedit(tfnt,align)
        self._dop = self._get_qlineedit(tfnt,align)
        
        #setup the ui
        l = QGridLayout()
        l.addWidget(self._get_qlabel('UTC Time',lfnt,align),0,0,1,1)
        l.addWidget(self._get_qlabel('Latitude',lfnt,align),0,1,1,1)
        l.addWidget(self._get_qlabel('Longitude',lfnt,align),0,2,1,1)
        l.addWidget(self._get_qlabel('N Sats',lfnt,align),0,3,1,1)
        l.addWidget(self._get_qlabel('Quality',lfnt,align),0,4,1,1)
        l.addWidget(self._get_qlabel('DOP',lfnt,align),0,5,1,1)
        l.addWidget(self._time,1,0,1,1)
        l.addWidget(self._lat,1,1,1,1)
        l.addWidget(self._lon,1,2,1,1)
        l.addWidget(self._fix,1,3,1,1)
        l.addWidget(self._n,1,4,1,1)
        l.addWidget(self._dop,1,5,1,1)
        l.setSpacing(2)
        self.setLayout(l)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFrameStyle(frame)
        
        # initialize state variables
        self._dop_state = state()
        self._fix_state = state()
        self._rtk = rtk
        
    def set_data(self,time='',lat=360,lon=360,n=0,fix=0,dop=np.NaN):
        ''' sets the data on the plot and appends to the map '''
        self._time.setText(time)
        self._lat.setText('%.6f'%lat)
        self._lon.setText('%.6f'%lon)
        self._n.setText('%d'%n)
        self._set_fix(fix)
        self._set_dop(dop)
        
    def clear(self):
        ''' reset all the text boxes '''
        self._time.setText('')
        self._lat.setText('')
        self._lon.setText('')
        self._n.setText('')
        self._fix.setText('')
        self._fix.setStyleSheet('')
        self._dop.setText('')
        self._dop.setStyleSheet('')
        
    def _set_fix(self,fix=1):
        ''' sets the fix of the gnss receiver '''
        
        if not self._fix_state.isDifferent(fix): return
        
        self._fix.setText('%d'%fix)# update the text
        if self._rtk:
            if fix == 4: self._fix.setStyleSheet('background-color: green')
            else: self._fix.setStyleSheet('background-color: red')
            
    def _set_dop(self,dop=100):
        ''' sets the dop text and warning '''
        if not self._dop_state.isDifferent(dop): return
        
        self._dop.setText('%.2f' % dop)# update the text
        if not self._rtk:
            if dop >= 2: self._dop.setStyleSheet('background-color: red')
            else: self._dop.setStyleSheet('background-color: green')
        
    def _get_qlabel(self,text,fnt,algn):
        ''' creates the labels '''
        l = QLabel(text)
        if fnt is not None: l.setFont(fnt)
        if algn is not None: l.setAlignment(algn)
        return l
        
    def _get_qlineedit(self,fnt,algn):
        ''' creates the line edits '''
        le = QLineEdit()
        le.setReadOnly(True)
        if fnt is not None: le.setFont(fnt)
        if algn is not None: le.setAlignment(algn)
        return le

class IMUVisualWidget(QFrame):
    
    def __init__(self,parent=None,px=.2,py=.2,pz=.2,tfnt=None):
        QFrame.__init__(self,parent)
        self.roll = self._get_txt('Roll:',tfnt)
        self.pitch = self._get_txt('Pitch:',tfnt)
        self.yaw = self._get_txt('Yaw:',tfnt)
        self.imu = CubeWidget(self,px=px,py=py,pz=pz)
        
        l = QGridLayout()
        l.addWidget(self.imu,0,0,1,3)
        l.addWidget(self.roll,1,0,1,1)
        l.addWidget(self.pitch,1,1,1,1)
        l.addWidget(self.yaw,1,2,1,1)
        
        self.setLayout(l)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        
    def _get_txt(self,text='',fnt=None):
        txt = QLineEdit(text)
        txt.setReadOnly(True)
        if fnt is not None: txt.setFont(fnt)
        return txt
    
    def setEuler(self,roll,pitch,yaw):
        self.roll.setText('Roll: %.2f' % roll)
        self.pitch.setText('Pitch: %.2f' % pitch)
        self.yaw.setText('Yaw: %.2f' % yaw)
        self.imu.update(roll,pitch,yaw)
        
    def clear(self):
        ''' clears the IMU widget '''
        self.setEuler(0,0,0)
        
class GCSMapWidget(QFrame):
    ''' a class for a GCS map '''
    
    def __init__(self,parent=None,lines=1,leg=['Path'],lsize=10,tsize=16):
        ''' constructor '''
        QFrame.__init__(self,parent)
        
        # setup the plot
        self.plot = Plot2DWidget(self,
                                 parameters=PlotParameters('GCS Map',
                                                           'Longitude (deg)',
                                                           'Latitude (deg)',
                                                           lsize=lsize,
                                                           tsize=tsize),
                                 lines=lines)
        self.plot.axes.set_aspect('equal')
        self.plot.set_linestyle(line=0,style='None')
        self.plot.set_marker(line=0,marker='s')
        self.plot.set_legend(leg)
        
        #layout the map
        l = QGridLayout()
        l.setSpacing(0)
        l.addWidget(self.plot)
        self.setLayout(l)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.setStyleSheet('background-color: white')
        
    def append(self,x=0,y=0,line=0):
        ''' appends to the plot data '''
        self.plot.append(x,
                         y,
                         line,
                         autoscale=True)

class UTMMapWidget(QFrame):
    ''' a class for a UTM map '''
    
    def __init__(self,parent=None,lines=1,leg=['Path'],lsize=10,tsize=16,xref=0,yref=0):
        ''' constructor '''
        QFrame.__init__(self,parent)
        
        # setup the reference coordinates
        self._x_ref = xref
        self._y_ref = yref
        
        # setup the plot
        parameters = PlotParameters('UTM Map',
                                    'Easting - %.2f (m)' % self._x_ref,
                                    'Northing - %.2f (m)' % self._y_ref,
                                    lsize=lsize,
                                    tsize=tsize)
        self.plot = Plot2DWidget(parent=self,parameters=parameters,lines=lines)
        self.plot.axes.set_aspect('equal')
        self.plot.set_linestyle(line=0,style='None')
        self.plot.set_marker(line=0,marker='s')
        self.plot.set_legend(leg)
        
        #layout the map
        l = QGridLayout()
        l.setSpacing(0)
        l.addWidget(self.plot)
        self.setLayout(l)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.setStyleSheet('background-color: white')
        
    def setReference(self,x=0,y=0):
        ''' sets the reference coordinates '''
        self._x_ref = x
        self._y_ref = y
        self.plot.axes.set_xlabel('Easting - %.2f (m)' % self._x_ref)
        self.plot.axes.set_xlabel('Northing - %.2f (m)' % self._y_ref)
        
    def append(self,x=0,y=0,line=0):
        ''' appends to the plot '''
        self.plot.append(x-self._x_ref,
                         y-self._x_ref,
                         line,
                         autoscale=True)

class GPGGAVisualWidget(QFrame):
    ''' a class for visually displaying the NMEA string '''
    
    def __init__(self,parent=None,rtk=False,lfnt=None,tfnt=None,align=None,
                 lsize=10,tsize=16):
        ''' constructor '''
        QFrame.__init__(self,parent)
        
        # create the widgets
        self._gga = GPGGAWidget(self,rtk=rtk,
                                tfnt=tfnt,lfnt=lfnt,
                                align=align,frame=QFrame.Plain)
        self._map = GCSMapWidget(self,lsize=lsize,tsize=tsize)# map widget
        
        #setup the ui
        l = QGridLayout()
        l.addWidget(self._gga)
        l.addWidget(self._map,2,0,6,6)
        l.setSpacing(2)
        self.setLayout(l)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        
        # initialize state variables
        self._dop_state = state()
        self._fix_state = state()
        self._rtk = rtk
        
    def set_data(self,time='',lat=360,lon=360,n=0,fix=0,dop=np.NaN,append=True):
        ''' sets the data on the plot and appends to the map '''
        self._gga.set_data(time, lat, lon, n, fix, dop)
        if append: self._map.append(lon,lat)
    
class RTMag3DWidget(QFrame):
    ''' a 3d display of the real time inversion '''
    
    def __init__(self,parent=None,lsize=10,tsize=16):
        ''' constructor '''
        QFrame.__init__(self,parent)
        
        self.det = SoftwareLED(self,'DETECTION')
        _curr_m = self._get_qlabel(txt='Moment',align=Qt.AlignCenter)
        self.curr_m = self._get_qlineedit(readonly=True,align=Qt.AlignCenter)
        _track_m = self._get_qlabel(txt='Track Moment',align=Qt.AlignCenter)
        self.track_m = self._get_qlineedit(readonly=True,align=Qt.AlignCenter)
        _source_n = self._get_qlabel(txt='Sources',align=Qt.AlignCenter)
        self.source_n = self._get_qlineedit(readonly=True,align=Qt.AlignCenter)
        _state = self._get_qlabel(txt='State',align=Qt.AlignCenter)
        self.state = self._get_qlineedit(readonly=True,align=Qt.AlignCenter)
        _alt = self._get_qlabel('Altitude (m)',align=Qt.AlignCenter)
        self.altitude = self._get_qlineedit(readonly=True,align=Qt.AlignCenter)
        
        self.plot = Plot3DWidget(parameters=
                                 PlotParameters(xlabel='x(m)',
                                                ylabel='y(m)',
                                                zlabel='z(m)',
                                                lsize=lsize,
                                                tsize=tsize),
                                 lines=0)
        self.plot.add_line([], [], [],'ko-')
        self.plot.add_line([],[],[],'go')
        self.plot.add_line([],[],[],'bx',markersize=14,markeredgewidth=8)
        self.plot.add_line([], [], [],'mo-')
        self.plot.set_legend(['Path','Current','Track','Source'])
        
        l = QGridLayout()
        l.addWidget(self.det,0,0,2,1)
        l.addWidget(_curr_m,0,1,1,1)
        l.addWidget(self.curr_m,1,1,1,1)
        l.addWidget(_source_n,0,2,1,1)
        l.addWidget(self.source_n,1,2,1,1)
        l.addWidget(_track_m,0,3,1,1)
        l.addWidget(self.track_m,1,3,1,1)
        l.addWidget(_state,0,4,1,1)
        l.addWidget(self.state,1,4,1,1)
        l.addWidget(_alt,0,5,1,1)
        l.addWidget(self.altitude,1,5,1,1)
        l.addWidget(self.plot,2,0,1,9)
        l.setRowStretch(0,1)
        l.setRowStretch(1,1)
        l.setRowStretch(2,10)
        
        l.setSpacing(2)
        self.setLayout(l)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        
    def _get_qlabel(self,txt='',font=None,align=None):
        ''' creates the qlabels '''
        l = QLabel(txt)
        if font is not None: l.setFont(font)
        if align is not None: l.setAlignment(align)
        return l
        
    def _get_qlineedit(self,txt='',font=None,align=None,readonly=False):
        ''' creates the qlabels '''
        l = QLineEdit(txt)
        if font is not None: l.setFont(font)
        if align is not None: l.setAlignment(align)
        l.setReadOnly(readonly)
        return l
    
    def clear(self):
        ''' clears all the plots, text boxes and software LEDs '''
        for i in range(self.plot.line_total()-1,3,-1): self.plot.remove_line(i)
        self.plot.clear_line(0)
        self.plot.clear_line(1)
        self.plot.clear_line(2)
        self.curr_m.setText('')
        self.source_n.setText('')
        self.track_m.setText('')
        self.altitude.setText('')
        self.det.reset()
    
    def appendPath(self,x,y,z):
        ''' appends to the path line '''
        self.plot.append(x,y,z,line=0,autoscale=True)
        self.plot.set_data(x,y,z,line=1,autoscale=True)
        self.altitude.setText('%.2f' % z)
        
    def appendTrack(self,x,y,z):
        ''' appends to the mean inversion locations '''
        self.plot.append(x,y,z,line=2,autoscale=True)
        
    def addSource(self,x,y,z):
        ''' adds an inversion line '''
        self.plot.add_line(x,y,z,'mo-')
        
    def setTrackMoment(self,m=-1):
        ''' sets the track moment '''
        self.track_m.setText('%.2f' % m)
        
    def setCurrentMoment(self,m=-1):
        ''' sets the current moment '''
        self.curr_m.setText('%.2f' % m)
        
    def setTotalSources(self,n=-1):
        self.source_n.setText('%d' % n)
        
    def setDetection(self,detection=False):
        ''' sets the detection state '''
        if detection: self.det.setBad()
        else: self.det.reset()
        
    def setState(self,string=''):
        ''' relays the state of the sim board '''
        self.state.setText(string)
        
class RTMag2DWidget(QFrame):
    ''' a 2d representation of the inversion '''
    
    def __init__(self,parent=None,lsize=10,tsize=16):
        ''' constructor '''
        QFrame.__init__(self,parent)
        
        self.det = SoftwareLED(self,'DETECTION')
        _curr_m = self._get_qlabel(txt='Current Moment',align=Qt.AlignCenter)
        self.curr_m = self._get_qlineedit(readonly=True,align=Qt.AlignCenter)
        _track_m = self._get_qlabel(txt='Track Moment',align=Qt.AlignCenter)
        self.track_m = self._get_qlineedit(readonly=True,align=Qt.AlignCenter)
        _source_n = self._get_qlabel(txt='Sources',align=Qt.AlignCenter)
        self.source_n = self._get_qlineedit(readonly=True,align=Qt.AlignCenter)
        _state = self._get_qlabel(txt='State',align=Qt.AlignCenter)
        self.state = self._get_qlineedit(readonly=True,align=Qt.AlignCenter)
        _alt = self._get_qlabel('Altitude (m)',align=Qt.AlignCenter)
        self.altitude = self._get_qlineedit(readonly=True,align=Qt.AlignCenter)
        
        self.plot = Plot2DWidget(parameters = 
                                 PlotParameters('UTM Map',
                                    'Easting (m)',
                                    'Northing (m)',
                                    lsize=lsize,
                                    tsize=tsize),
                                    lines=0)
        self.plot.set_aspect()
        self.plot.add_line([], [],'ko-')
        self.plot.add_line([],[],'go')
        self.plot.add_line([],[],'bx',markersize=14,markeredgewidth=8)
        self.plot.add_line([], [],'mo-')
        self.plot.set_legend(['Path','Current','Track','Source'])
        
        l = QGridLayout()
        l.addWidget(self.det,0,0,2,1)
        l.addWidget(_curr_m,0,1,1,1)
        l.addWidget(self.curr_m,1,1,1,1)
        l.addWidget(_source_n,0,2,1,1)
        l.addWidget(self.source_n,1,2,1,1)
        l.addWidget(_track_m,0,3,1,1)
        l.addWidget(self.track_m,1,3,1,1)
        l.addWidget(_state,0,4,1,1)
        l.addWidget(self.state,1,4,1,1)
        l.addWidget(_alt,0,5,1,1)
        l.addWidget(self.altitude,1,5,1,1)
        l.addWidget(self.plot,2,0,1,9)
        l.setRowStretch(0,1)
        l.setRowStretch(1,1)
        l.setRowStretch(2,10)
        
        l.setSpacing(2)
        self.setLayout(l)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        
    def _get_qlabel(self,txt='',font=None,align=None):
        ''' creates the qlabels '''
        l = QLabel(txt)
        if font is not None: l.setFont(font)
        if align is not None: l.setAlignment(align)
        return l
        
    def _get_qlineedit(self,txt='',font=None,align=None,readonly=False):
        ''' creates the qlabels '''
        l = QLineEdit(txt)
        if font is not None: l.setFont(font)
        if align is not None: l.setAlignment(align)
        l.setReadOnly(readonly)
        return l
    
    def clear(self):
        ''' clears all the plots, text boxes and software LEDs '''
        for i in range(self.plot.line_total()-1,3,-1):self.plot.remove_line(i)
        self.plot.clear_line(0)
        self.plot.clear_line(1)
        self.plot.clear_line(2)
        self.curr_m.setText('')
        self.source_n.setText('')
        self.track_m.setText('')
        self.altitude.setText('')
        self.det.reset()
    
    def appendPath(self,x,y,z):
        ''' appends to the path line '''
        self.plot.append(x,y,line=0,autoscale=True)
        self.plot.set_data(x,y, line=1, autoscale=True)
        self.altitude.setText('%.2f' % z)
        
    def appendTrack(self,x,y,z):
        ''' appends to the mean inversion locations '''
        self.plot.append(x,y,line=2,autoscale=True)
        
    def addSource(self,x,y,z):
        ''' adds an inversion line '''
        self.plot.add_line(x,y,'mo-')
        
    def setTrackMoment(self,m=-1):
        ''' sets the track moment '''
        self.track_m.setText('%.2f' % m)
        
    def setCurrentMoment(self,m=-1):
        ''' sets the current moment '''
        self.curr_m.setText('%.2f' % m)
        
    def setTotalSources(self,n=-1):
        self.source_n.setText('%d' % n)
        
    def setDetection(self,detection=False):
        ''' sets the detection state '''
        if detection: self.det.setBad()
        else: self.det.reset()
        
    def setState(self,string=''):
        ''' displays the state of the sim board '''
        self.state.setText(string)

class dataport_widget(RTMag3DWidget):
    
    def __init__(self,parent=None,lfnt=None,tfnt=None,title=''):
        QFrame.__init__(self,parent)
        
        self.address = self._get_qlineedit(font=lfnt)
        self.port = self._get_qlineedit(font=lfnt)
        self.baud = QComboBox()
        self.baud.addItems(list(map(str,Serial.BAUDRATES)))
        self.baud.setCurrentText('9600')
        self.type = QComboBox()
        self.type.currentTextChanged.connect(self._new_commstyle)
        self.type.addItems(['UDP','TCP','Serial'])
        
        # layout the widget
        l = QGridLayout()
        l.addWidget(self._get_qlabel(title,font=tfnt,align=Qt.AlignCenter),0,0,1,2)
        l.addWidget(self._get_qlabel('Type:',font=lfnt,align=Qt.AlignRight),1,0,1,1)
        l.addWidget(self.type,1,1,1,1)
        l.addWidget(self._get_qlabel('Address:',font=lfnt,align=Qt.AlignRight),2,0,1,1)
        l.addWidget(self.address,2,1,1,1)
        l.addWidget(self._get_qlabel('Port:',font=lfnt,align=Qt.AlignRight),3,0,1,1)
        l.addWidget(self.port,3,1,1,1)
        l.addWidget(self._get_qlabel('Baudrate:',font=lfnt,align=Qt.AlignRight),4,0,1,1)
        l.addWidget(self.baud,4,1,1,1)
        l.addItem(QSpacerItem(20,40,QSizePolicy.Expanding,QSizePolicy.Expanding),5,0,1,2)
        
        self.setLayout(l)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        
    def get_port(self):
        ''' returns the port type, address and port or baud '''
        txt = self.type.currentText()
        if txt == 'UDP' or txt == 'TCP':
            try:
                return (txt,self.address.text(),int(self.port.text()))
            except Exception as e:
                exc_type, _, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print('%s:%s in %s at %d'%(exc_type.__name__,str(e), fname, exc_tb.tb_lineno))
                return None
        elif txt == 'Serial':
            return (txt,self.port.text(),int(self.baud.currentText()))
        else: return None
        
    def _serial_enabled(self,enabled=False):
        ''' sets the serial model enabled or not '''
        self.address.setReadOnly(enabled)
        self.port.setReadOnly(False)
        self.baud.setEnabled(enabled)
            
    def _new_commstyle(self,value):
        ''' handles a change in the type combobox '''
        if value == 'UDP' or value == 'TCP': self._serial_enabled(False)
        elif value == 'Serial': self._serial_enabled(True)
        
    def _get_qlabel(self,txt='',font=None,align=None):
        ''' creates the qlabels '''
        l = QLabel(txt)
        if font is not None: l.setFont(font)
        if align is not None: l.setAlignment(align)
        return l
        
    def _get_qlineedit(self,txt='',font=None,align=None,readonly=False):
        ''' creates the qlabels '''
        l = QLineEdit(txt)
        if font is not None: l.setFont(font)
        if align is not None: l.setAlignment(align)
        l.setReadOnly(readonly)
        return l

class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.w = LogWidget(self)
        clear = QPushButton('CLEAR')
        clear.clicked.connect(self._clear)
        self.nmea = GPGGAWidget(self)
        #self.imu = IMUVisualWidget(self)
        self.map = GPGGAVisualWidget(self,
                                     rtk=True,
                                     align=QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter,
                                     lsize=10,
                                     tsize=16)
        self.utm = UTMMapWidget(self,lsize=10,tsize=16)
        self.gcs = GCSMapWidget(self,lsize=10,tsize=16)
        self.rtmag = RTMag3DWidget(self)
        self.port = dataport_widget(self,title='Communication Port')
        self.rtmag2d = RTMag2DWidget(self)
        layout = QGridLayout()
        layout.addWidget(self.w,0,0,1,2)
        layout.addWidget(clear,0,2,1,1)
        layout.addWidget(self.nmea,1,0,1,3)
        layout.addWidget(self.port,2,0,1,1)
        layout.addWidget(self.map,2,1,1,1)
        layout.addWidget(self.utm,2,2,1,1)
        layout.addWidget(self.gcs,3,0,1,1)
        layout.addWidget(self.rtmag2d,3,1,1,1)
        layout.addWidget(self.rtmag,3,2,1,1)
        for i in range(layout.columnCount()):
            layout.setColumnStretch(i,1)
        self.setLayout(layout)
        
        self.w.log.clicked.connect(self.onClick)
        
        self._det = False
        
    def _clear(self):
        ''' clears the real time plot '''
        self.rtmag.clear()
        self.rtmag2d.clear()
        
    def onClick(self):
        if self.w.isLogging(): 
            self.w.setStopped()
        else:
            print('filename: %s.dat'%self.w.getFilename())
            self.w.setStarted()
            
        #print('port:',self.port.get_port())
        
        self.map.set_data('1234',43.0,127.4,3,12,100)
        self.nmea.set_data('1234',43.0,127.4,3,8,100)
        
        #test utm
        self.utm.plot.set_data([1,2,3,4],[1,1,1,1],autoscale=True)
        self.utm.plot.append(5,3,autoscale=True)
        
        # test gcs
        self.gcs.append(0,2,line=0)
        self.gcs.append(1,2,line=0)
        
        self.rtmag2d.appendPath([random.random()],
                                    [random.random()],
                                    [random.random()])
        self.rtmag2d.appendTrack([random.random()],
                                    [random.random()],
                                    [random.random()])
        self.rtmag2d.addSource([random.random()],
                                    [random.random()],
                                    [random.random()])
        self.rtmag2d.setTrackMoment(random.random())
        self.rtmag2d.setCurrentMoment(random.random())
        self.rtmag2d.setTotalSources(random.randint(0,100))
        
        self.rtmag.appendPath([random.random()],
                                    [random.random()],
                                    [random.random()])
        
        self.rtmag.appendTrack([random.random()],
                                    [random.random()],
                                    [random.random()])
        
        self.rtmag.addSource([0,random.random()],
                                    [0,random.random()],
                                    [0,random.random()])
        
        self.rtmag.setTrackMoment(random.random())
        self.rtmag.setCurrentMoment(random.random())
        self.rtmag.setTotalSources(random.randint(0,100))
        
        self.rtmag.setDetection(self._det)
        self._det = not self._det

if __name__.startswith('__main__'):
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Color Picker Demo")
    window.show()
    app.exec_()