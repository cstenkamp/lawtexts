from PyQt5.QtCore import Qt, QTimer, QObjectCleanupHandler
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import *

from panel import *
from component import *
from machine import *
from directives import *
from interfaces import *

import objects as obj 

import sys 


class MainWindow(QWidget):
    def __init__(self, machine):
        super(MainWindow,self).__init__()
        self.setGeometry(100,100,700,300)
        #
        self.machine = machine
        #
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setAlignment(Qt.AlignTop)
        #
        self.setLayout(self.mainLayout)
        self.show()
        '''
        Top Part Layout
        '''
        self.topLayout = QVBoxLayout()
        self.topLayout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.mainLayout.addLayout(self.topLayout)
        # select site of operation of machine
        self.siteLayout = QHBoxLayout()
        self.topLayout.addLayout(self.siteLayout)
        self.siteLabel = QLabel('Verwendungsort: ')
        self.siteLabel.setFixedWidth(180)
        self.siteLayout.addWidget(self.siteLabel)
        sites = ['--andere--']+sorted(obj.loadCSV('csv/Verwendungsorte.csv'))
        self.siteSelectionMenu = QComboBox()
        for s in sites:
            self.siteSelectionMenu.addItem(s)
        self.siteSelectionMenu.activated.connect(self.setMachineSite)
        self.siteLayout.addWidget(self.siteSelectionMenu)
        # purpose of machine
        self.purposeLayout = QHBoxLayout()
        self.topLayout.addLayout(self.purposeLayout)
        self.purposeLabel = QLabel('Verwendungszweck: ')
        self.purposeLabel.setFixedWidth(180)
        self.purposeLayout.addWidget(self.purposeLabel)
        purposes = ['--andere--']+sorted(obj.loadCSV('csv/Verwendungszwecke.csv'))
        self.purposeSelectionMenu = QComboBox()
        for s in purposes:
            self.purposeSelectionMenu.addItem(s)
        self.purposeSelectionMenu.activated.connect(self.setMachinePurpose)
        self.purposeLayout.addWidget(self.purposeSelectionMenu)
        # do people have to operate the machine
        # purpose of machine
        self.operationLayout = QHBoxLayout()
        self.topLayout.addLayout(self.operationLayout)
        self.operationLabel = QLabel('Anlage ist durch Beschäftigte zu bedienen oder zu überwachen?')
        self.operationLabel.setWordWrap(True)
        self.operationLabel.setFixedWidth(180)
        self.operationLabel.setFixedHeight(55)
        self.operationLabel.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.operationLayout.addWidget(self.operationLabel)
        self.operationCheckbox = QCheckBox()
        self.operationCheckbox.setChecked(False)
        self.operationCheckbox.clicked.connect(self.setMachineOperation)
        self.operationLayout.addWidget(self.operationCheckbox)

        #
        '''
        Middle part of layout with 'add' and 'send' buttons
        '''
        self.middleLayout = QHBoxLayout()
        self.middleLayout.setAlignment(Qt.AlignRight)
        # buttons to add component to machine
        self.addComponentButton = QPushButton('Komponente Hinzufügen')
        self.addComponentButton.clicked.connect(self.addComponent)
        self.middleLayout.addWidget(self.addComponentButton)
        # buttons to confirm input and evaluate machine
        self.acceptButton = QPushButton('abschicken')
        self.acceptButton.clicked.connect(self.checkMachine)
        self.middleLayout.addWidget(self.acceptButton)
        # add layout to main layout
        self.mainLayout.addLayout(self.middleLayout)
        '''
        Bottom part of layout. Components will be listed here
        '''
        self.bottomLayout = QVBoxLayout()
        self.bottomLayout.setAlignment(Qt.AlignTop)
        self.bottomLayout.addWidget(self.HLine())
        self.mainLayout.addLayout(self.bottomLayout)


    def addComponent(self):
        print('added component')
        c = Component(self)
        self.machine.components.append(c)
        self.bottomLayout.addWidget(c)

    def setMachineSite(self):
        self.machine.site = self.siteSelectionMenu.currentText()

    def setMachinePurpose(self):
        self.machine.purpose = self.purposeSelectionMenu.currentText()

    def setMachineOperation(self):
        self.machine.humanOperation = self.operationCheckbox.isChecked()

    def HLine(self):
        toto = QFrame()
        toto.setFrameShape(QFrame.HLine)
        toto.setFrameShadow(QFrame.Sunken)
        return toto

    def checkMachine(self):
        self.LVD = LowVoltageDirective()
        self.LVD.checkMachine(self.machine)

        self.PED = PressureEquipmentDirective()
        self.PED.checkMachine(self.machine)
        
        self.ATEX = ATEXDirective()

        #
        self.LVD.checkApplicabilityOnSite(self.machine.site)
        self.LVD.checkApplicabilityOnPurpose(self.machine.purpose)
        #
        self.ATEX.checkApplicabilityOnSite(self.machine.site)
        self.ATEX.checkApplicabilityOnPurpose(self.machine.purpose)
        #
        if self.ATEX.active:
            self.ATEXInterface = ATEXInterface(self.machine)
            self.ATEXInterface.categoryMask()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    M = Machine()
    mw = MainWindow(M)