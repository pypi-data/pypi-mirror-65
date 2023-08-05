'''
Created on Aug 17, 2018

@author: reynolds
'''

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QComboBox, QWidget, QLabel, QPushButton, QLineEdit, QGridLayout, QFrame,\
    QListView
from PyQt5.QtGui import QFont
from PyQt5.Qt import Qt


class wrt_widget(QFrame):
    ''' allows for widgets to use commonly used WRT widget functions '''
    
    def __init__(self,parent=None):
        QFrame.__init__(self,parent)
        ''' constructor '''
    
    def _setState(self,widget,state):
        ''' sets the state of the qmag for the MAD Unit because
        John-Mike decided to change the firmware to something
        stupid at the last minute '''
        if state == '' or state == None:
            # if the state is nothing or the state is the same then return
            return
        elif state =='AG' or state == b'\x00\x00'.decode():
            # set the all good state
            widget.setStyleSheet('background-color: green')
        elif state == 'TO':
            # set the state to Timed Out
            widget.setStyleSheet('background-color: orange')
        elif state == 'NC':
            widget.setStyleSheet('background-color: yellow')
        else:
            # set everything else as bad
            widget.setStyleSheet('background-color: red')
        # set the text
        widget.setText(state)

class gpr_widget(wrt_widget):
    '''
    a class for plotting the gpr data
    '''
    
    LINES = 1
    
    def __init__(self,parent=None,timeout=2000):
        ''' constructor '''
        super().__init__(parent)
        self.timeout = timeout
        self.plot = WaterfallWidget(self,
                                    parameters=PlotParameters('A Scan','Amplitude','Time'),
                                    lines=1)
        self.count = self._getQLineEdit('',True)
        self.status = self._getQLineEdit('',readonly=True)
        
        l = QGridLayout()
        l.addWidget(self._getLabel('GPR',16,Qt.AlignCenter),0,0,1,4)
        l.addWidget(self._getLabel('Count:',10),1,0,1,1)
        l.addWidget(self.count,1,1,1,1)
        l.addWidget(self._getLabel('Status:',10,Qt.AlignCenter),1,2,1,1)
        l.addWidget(self.status)
        l.addWidget(self.plot,2,0,1,4)
        
        self.setLayout(l)
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        
        self.state = state()
        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.setStatus('NC'))
        
    def setStarted(self):
        ''' sets the display started '''
        self.timer.start(self.timeout)
    
    def setStopped(self):
        ''' resets the display '''
        self.timer.stop()
        self.count.setText('')
        self.status.setText('')
        self.status.setStyleSheet('')
        
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
    
    def setCount(self,count=0):
        ''' sets the count '''
        self.count.setText('%.0f' % count)
    
    def setStatus(self,status):
        ''' do nothing '''
        self.timer.stop()
        self.timer.start(self.timeout)
        if self.state.isDifferent(status):
            self._setState(self.status,status)
    
    def setStrength(self,strength=0):
        ''' sets the strength '''
        return

class IMUWidget(QFrame):
    '''
    a class for displaying IMU euler angles
    '''
    
    def __init__(self,parent=None):
        ''' constructor '''
        QFrame.__init__(self,parent)
        
        # create the widgets
        self.roll = self._getQLineEdit()
        self.pitch = self._getQLineEdit()
        self.yaw = self._getQLineEdit()
        self.temperature = self._getQLineEdit()
        
        # layout the grid
        l = QGridLayout()
        l.addWidget(self._getLabel('IMU',10,Qt.AlignCenter),0,0,1,2)
        l.addWidget(self._getLabel('Roll:'),1,0)
        l.addWidget(self.roll,1,1)
        l.addWidget(self._getLabel('Pitch:'),2,0)
        l.addWidget(self.pitch,2,1)
        l.addWidget(self._getLabel('Yaw:'),3,0)
        l.addWidget(self.yaw,3,1)
        l.addWidget(self._getLabel('T (C):'),4,0)
        l.addWidget(self.temperature,4,1)
        l.addItem(QSpacerItem(10,10,QSizePolicy.Expanding,QSizePolicy.Expanding),5,0,1,2)
        l.setSpacing(10)
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

class OutgoingWidget(QFrame):
    ''' allows the user to send commands to the sensor '''
    
    def __init__(self,parent=None):
        ''' constructor '''
        QFrame.__init__(self,parent)
        
        # create widgets
        font = QtGui.QFont('Times',12,QtGui.QFont.Bold)
        self.send = FHButtonInputWidget(self,'SEND','',spacing=10)
        self.send.setFont(font)
        self.startLog = QPushButton('SD LOG')
        #self.startLog.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.stopLog = QPushButton('STOP')
        #self.stopLog.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.startStream = QPushButton('STREAM')
        #self.startStream.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.stopStream = QPushButton('END')
        #self.stopStream.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        btns = QWidget(self)
        lb = QGridLayout()
        lb.addWidget(self.startLog,0,0,1,1)
        lb.addWidget(self.startStream,1,0,1,1)
        lb.addWidget(self.stopLog,0,1,1,1)
        lb.addWidget(self.stopStream,1,1,1,1)
        lb.setSpacing(0)
        btns.setLayout(lb)
        btns.setContentsMargins(0, 0, 0, 0)
        
        # layout widget
        l = QGridLayout()
        l.addWidget(btns,0,0,1,1)
        l.addWidget(self.send,0,1,1,1)
        l.setSpacing(10)
        self.setLayout(l)
        self.setContentsMargins(0, 0, 0, 0)
        self.setEnabled(False)
        
    def setEnabled(self,enabled=False):
        ''' sets the enabled state of the widget '''
        self.startLog.setEnabled(enabled)
        self.stopLog.setEnabled(enabled)
        self.startStream.setEnabled(enabled)
        self.stopStream.setEnabled(enabled)
        self.send.setEnabled(enabled)
        
class SoftwareLED(QWidget):
    ''' a class for a software LED '''
    
    def __init__(self,parent=None,text='',font=QFont('Times',12),align=Qt.AlignCenter):
        ''' constructor '''
        QWidget.__init__(self,parent)
        self.label = QLabel(text)
        self.label.setFrameShape(QFrame.Panel)
        self.label.setFrameShadow(QFrame.Raised)
        self.label.setLineWidth(2)
        self.label.setFont(font)
        self.label.setAlignment(align)
        l = QGridLayout()
        l.addWidget(self.label)
        self.setLayout(l)
        
    def setGood(self):
        ''' sets a good status '''
        self.label.setStyleSheet('background-color:green')
        
    def setWarning(self):
        ''' sets a warning status '''
        self.label.setStyleSheet('background-color:orange')
        
    def setBad(self):
        ''' sets a bad status '''
        self.label.setStyleSheet('background-color:red')

    def setState(self,state=''):
        self.label.setStyleSheet(state)
        
    def reset(self):
        ''' resets the led to the original state of transparent '''
        self.label.setStyleSheet('')

class CheckableComboBox(QComboBox):
    def __init__(self, parent = None):
        super(CheckableComboBox, self).__init__(parent)
        self.setView(QListView(self))
        self.view().pressed.connect(self.handleItemPressed)
        self.setModel(QtGui.QStandardItemModel(self))
        self._changed = False

    def handleItemPressed(self, index):
        item = self.model().itemFromIndex(index)
        if item.checkState() == QtCore.Qt.Checked and len(self.getCheckedItems())!=1:
            item.setCheckState(QtCore.Qt.Unchecked)
        else:
            item.setCheckState(QtCore.Qt.Checked)
        self._changed = True
            
    def getItems(self):
        return [self.itemText(i) for i in range(self.count())]
    
    def setIndexChecked(self,index,checked=True):
        item = self.model().item(index,self.modelColumn())
        if checked: item.setCheckState(QtCore.Qt.Checked)
        else: item.setCheckState(QtCore.Qt.Unchecked)
        
    def hidePopup(self):
        if not self._changed:
            super(CheckableComboBox, self).hidePopup()
        self._changed = False
        
    def itemChecked(self, index):
        item = self.model().item(index, self.modelColumn())
        return item.checkState() == QtCore.Qt.Checke    

    def getCheckedItems(self):
        checkedItems = []
        for index in range(self.count()):
            item = self.model().item(index,self.modelColumn())
            if item.checkState() == QtCore.Qt.Checked:
                checkedItems.append(item.text())
        return checkedItems
class InputWidget(QWidget):
    ''' generic input widget with a label '''
    
    def __init__(self,parent=None,text=[],widget=[],spacing=10,row=[0,0],col=[0,1]):
        ''' constructor default layout is horizontal '''
        QWidget.__init__(self,parent)

        # set the text and input widgets
        self.text = text
        #self.text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.widget = widget
        #self.widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # layout the widget
        l = QGridLayout()
        l.setSpacing(spacing)
        l.addWidget(self.text,row[0],row[0],1,1)
        l.addWidget(self.widget,row[1],col[1],1,1)
        self.setLayout(l)
    
    def setLabelAlignment(self,alignment):
        ''' sets the label alignment '''
        self.text.setAlignment(alignment)
        
    def setWidgetAlignment(self,alignment):
        ''' sets the widget alignment '''
        self.widget.setAlignment(alignment)
        
    def setLabelFont(self,font):
        ''' sets the label font '''
        self.text.setFont(font)
        
    def setWidgetFont(self,font):
        ''' sets the widget font '''
        self.widget.setFont(font)
        
    def setAlignment(self,alignment):
        ''' sets the alignment '''
        self.setLabelAlignment(alignment)
        self.setLabelAlignment(alignment)
        
    def setFont(self,font):
        ''' sets the label font '''
        self.setLabelFont(font)
        self.setWidgetFont(font)
    
    def setEnabled(self,enabled=False):
        ''' sets the ui input enabled state '''
        self.widget.setEnabled(enabled)
        
    def setReadOnly(self,readOnly):
        ''' sets read only '''
        self.widget.setReadOnly(readOnly)

class LabelledInputWidget(InputWidget):
    ''' labelled input widget. Abstract '''
    
    def __init__(self,parent=None,label='',default='',spacing=10,row=[0,0],col=[0,1]):
        ''' constructor '''
        l = QLabel(label)
        t = QLineEdit(default)
        super().__init__(parent,l,t,spacing,row,col)

    
    def getLabel(self):
        ''' returns the labelled text '''
        pass
    
    def setLabel(self,label=''):
        ''' sets the label text '''
        pass

    def getText(self):
        ''' returns the line edit text '''
        return self.widget.text()

    def setText(self,text=''):
        ''' sets the line edit text '''
        self.widget.setText(text)
        
    def setInputColor(self,color='white'):
        ''' sets the color of the widget '''
        self.widget.setStyleSheet('background-color: ' + color)
        
    def setStyleSheet(self,style):
        ''' sets the style of the widget '''
        self.text.setStyleSheet(style)
        self.widget.setStyleSheet(style)
        
    def setReadOnly(self,readonly):
        ''' sets the read only status of the widget '''
        self.widget.setReadOnly(readonly)

class LabelledComboWidget(InputWidget):
    ''' Labelled combo widget '''
    
    def __init__(self,parent=None,label='',items=[],spacing=10,row=[0,0],col=[0,1]):
        ''' constructor '''
        c = QComboBox()
        c.addItems(items)
        l = QLabel(label)
        super().__init__(parent,l,c,spacing,row,col)

    def setItems(self,items=[]):
        ''' sets the items '''
        for s in items:
            self.widget.addItem(s)

    def getSelected(self):
        ''' returns the selected items '''
        return str(self.widget.currentText())

class ButtonInputWidget(InputWidget):
    ''' button input widget '''
    
    def __init__(self,parent=None,label='',default='',spacing=10,row=[0,0],col=[0,1]):
        ''' constructor '''
        b = QPushButton(label)
        t = QLineEdit(default)
        super().__init__(parent,t,b,spacing,row,col)

    def getText(self):
        ''' returns the text from the line edit '''
        return self.text.text()

    def setButtonColor(self,color):
        ''' sets the button color '''
        self.widget.setStyleSheet("background-color: " + color)

    def setButtonText(self,text=''):
        ''' sets the text of the button '''
        self.widget.setText(text)
        
    def setReadOnly(self,readonly):
        ''' sets the line edit read only status '''
        self.text.setReadOnly(readonly)

class FHLabelledInputWidget(LabelledInputWidget):
    ''' Forward horizontal input widget '''
    
    def __init__(self,parent=None,label='',default='',spacing=10):
        ''' constructor '''
        super().__init__(parent,label,default,spacing,[0,0],[0,1])

class RHLabelledInputWidget(LabelledInputWidget):
    ''' reverse horizontal labelled input widget '''
    
    def __init__(self,parent=None,label='',default='',spacing=10):
        ''' constructor '''
        super().__init__(parent,label,default,spacing,[0,0],[1,0])

class FVLabelledInputWidget(LabelledInputWidget):
    ''' Forward versitcal labelled input widget '''
    
    def __init__(self,parent=None,label='',default='',spacing=10):
        ''' constructor '''
        super().__init__(parent,label,default,spacing,[0,1],[0,0])

class RVLabelledInputWidget(LabelledInputWidget):
    ''' Reverse vertical labelled input widget '''
    
    def __init__(self,parent=None,label='',default='',spacing=10):
        ''' constructor '''
        super().__init__(parent,label,default,spacing,[1,0],[0,0])

class FHButtonInputWidget(ButtonInputWidget):
    ''' Forward horizontal button input widget '''
    
    def __init__(self,parent=None,label='',default='',spacing=10):
        ''' constructor '''
        super().__init__(parent,label,default,spacing,[0,0],[0,1])

class RHButtonInputWidget(ButtonInputWidget):
    ''' Reverse horizontal button input widget '''
    
    def __init__(self,parent=None,label='',default='',spacing=10):
        ''' constructor '''
        super().__init__(parent,label,default,spacing,[0,0],[1,0])

class FVButtonInputWidget(ButtonInputWidget):
    ''' Fowrard horizontal button input widget '''
    
    def __init__(self,parent=None,label='',default='',spacing=10):
        ''' constructor '''
        super().__init__(parent,label,default,spacing,[0,1],[0,0])

class RVButtonInputWidget(ButtonInputWidget):
    ''' Reverse vertical input widget '''
    
    def __init__(self,parent=None,label='',default='',spacing=10):
        ''' constructor '''
        super().__init__(parent,label,default,spacing,[1,0],[0,0])

class FHLabelledComboWidget(LabelledComboWidget):
    ''' Forward horizontal labelled combo widget '''
    
    def __init__(self,parent=None,label='',items=[],spacing=10):
        ''' constructor '''
        super().__init__(parent,label,items,spacing,[0,0],[0,1])

class RHLabelledComboWidget(LabelledComboWidget):
    '''Reverse horizontal labelled combo widget '''
    
    def __init__(self,parent=None,label='',items=[],spacing=10):
        ''' constructor '''
        super().__init__(parent,label,items,spacing,[0,0],[1,0])

class FVLabelledComboWidget(LabelledComboWidget):
    ''' Forward vertical labelled combo widget '''
    
    def __init__(self,parent=None,label='',items=[],spacing=10):
        ''' constructor '''
        super().__init__(parent,label,items,spacing,[0,1],[0,0])

class RVLabelledComboWidget(LabelledComboWidget):
    ''' a rear vertical combo widget '''
    
    def __init__(self,parent=None,label='',items=[],spacing=10):
        ''' constructor '''
        super().__init__(parent,label,items,spacing,[1,0],[0,0])
        
class TwoStateTextWidget(QWidget):
    ''' A text box that indicates state by color '''
    
    def __init__(self,parent=None,gstate=None,text='',readonly=True):
        ''' constructs the state box'''
        QWidget.__init__(self,parent)
        
        self._text = QLineEdit(text)
        self._text.setReadOnly(readonly)
        self._good = gstate
        self._state = False
        
    def update(self,state):
        ''' updates the state of the box '''
        if state == self._state: return
        if state == self._good:
            self._text.setStyleSheet("background-color: green")
            self._text.setText(str(state))
        else:
            self._text.setStyleSheet("background-color: red")
            self._text.setText(str(state))
        self._state = state == self._good