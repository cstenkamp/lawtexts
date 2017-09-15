from PyQt5.QtCore import Qt, QTimer, QObjectCleanupHandler
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import *

from panel import *
#from component import *
from machine import *
from directives import *
from interfaces import *

import objects as obj 

import sys 



class FeatureGui(QFrame):
    def __init__(self, parent):
        super(FeatureGui,self).__init__()
        self.parent = parent
        self.panel = None
        self.feature = Feature()
        self.parent.parent.component.features.append(self.feature)

        self.setFrameShape(QFrame.Box)
        self.setFrameShadow(QFrame.Sunken)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.mainLayout = QHBoxLayout(self)
        self.mainLayout.setAlignment(Qt.AlignLeft)


        self.selectionMenu = QComboBox()
        options = ['Betriebsspannung','Inhalt',
                         'Druck','Temperatur','Durchmesser','Herstellungsdatum',
                         'Leistung','Länge','Volumen','Treibstoff']
        for o in options:
            self.selectionMenu.addItem(o)
        self.selectionMenu.setCurrentIndex(-1)
        self.selectionMenu.activated.connect(self.updatePanel)
        self.mainLayout.addWidget(self.selectionMenu)

        self.middleLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.middleLayout)


        self.mainLayout.addStretch()

        self.removeButton = QPushButton('-')
        self.removeButton.clicked.connect(self.remove)
        self.mainLayout.addWidget(self.removeButton)


    def remove(self):
        self.deleteLater() 
        self.parent.featureGuis.remove(self)
        self.parent.parent.component.features.remove(self.feature)

    def updatePanel(self):
        t = self.selectionMenu.currentText()

        # if panel, delte and create new
        if not self.panel is None:
            self.panel.delete()
        self.panel = Panel(self)

        self.feature.setName(t)
        self.feature.clearVals()

        if t == 'Inhalt':
            self.panel.addContentPanel()
            #
        elif t == 'Betriebsspannung':
            self.panel.addVoltagePanel()
            #
        elif t == 'Druck':
            self.panel.addPressurePanel()
            #
        elif t == 'Leistung':
            self.panel.addPowerPanel()
            #
        elif t == 'Länge':
            self.panel.addLengthPanel()
            #
        elif t == 'Treibstoff':
            self.panel.addFuelPanel()
            #
        elif t == 'Volumen':
            self.panel.addVolumePanel()
            #
        elif t == 'Durchmesser':
            self.panel.addDiameterPanel()
            #
        elif t == 'Herstellungsdatum':
            self.panel.addDatePanel()
            #
        elif t == 'Temperatur':
            self.panel.addTemperaturePanel()
            #

        self.middleLayout.addWidget(self.panel)




class ConfigGui(QFrame):
    def __init__(self, parent):
        super(ConfigGui,self).__init__()
        self.setGeometry(600,100,800,300)
        self.parent = parent
        self.featureGuis = []

        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setAlignment(Qt.AlignTop|Qt.AlignLeft)

        self.topLayout = QHBoxLayout()
        self.topLayout.setAlignment(Qt.AlignTop|Qt.AlignLeft)        
        self.mainLayout.addLayout(self.topLayout)

        self.topLayout.addStretch()

        self.addFeatureButton = QPushButton('Eigenschaft hinzufügen')
        self.addFeatureButton.clicked.connect(self.addFeature)
        self.topLayout.addWidget(self.addFeatureButton)

        self.sendButton = QPushButton('abschicken')
        self.sendButton.clicked.connect(self.send)
        self.topLayout.addWidget(self.sendButton)

        self.bottomLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.bottomLayout)


    def addFeature(self):
        f = FeatureGui(self)
        self.bottomLayout.addWidget(f)
        self.featureGuis.append(f)

    def send(self):
        self.hide()


class ComponentGui(QFrame):
    def __init__(self, parent):
        super(ComponentGui,self).__init__()
        self.parent = parent
        self.component = Component()
        self.config = None

        self.parent.machine.addComponent(self.component)

        self.setFrameShape(QFrame.Box)
        self.setFrameShadow(QFrame.Sunken)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.mainLayout = QHBoxLayout(self)
        self.mainLayout.setAlignment(Qt.AlignTop|Qt.AlignLeft)

        self.selectionMenu = QComboBox()
        self.componentsList = sorted(obj.loadCSV('csv/confirmed_komponenten.csv'))
        self.selectionMenu = QComboBox()
        for c in self.componentsList:
            self.selectionMenu.addItem(c)
        self.selectionMenu.setCurrentIndex(-1)
        self.selectionMenu.activated.connect(self.newConfig)
        self.mainLayout.addWidget(self.selectionMenu)


        self.mainLayout.addStretch()

        self.configButton = QPushButton('konfigurieren')
        self.configButton.clicked.connect(self.configure)
        self.configButton.hide()

        self.mainLayout.addWidget(self.configButton)

        self.removeButton = QPushButton('-')
        self.removeButton.clicked.connect(self.remove)
        self.mainLayout.addWidget(self.removeButton)


    def remove(self):
        self.deleteLater() 
        self.parent.machine.components.remove(self.component)

    def configure(self):
        if self.config is None:
            self.config = ConfigGui(self)
            self.config.setWindowTitle(self.selectionMenu.currentText())
            self.config.show()
        else:
            self.config.hide()
            self.config.show()

    def newConfig(self):
        t = self.selectionMenu.currentText()
        self.configButton.show()
        self.config = ConfigGui(self)
        self.config.setWindowTitle(t)
        self.config.show()
        self.component.setName(t)


    def setName(self,name):
        self.component.setName(name)

    def setValue(self,value):
        self.component.setValue(value)

    def newFeature(self):
        self.component.newFeature()

    def addFeature(self,feature):
        self.component.addFeature(feature)

    def removeFeature(self,feature):
        self.component.removeFeature(feature)


class MachineGui(QWidget):
    def __init__(self, machine):
        super(MachineGui,self).__init__()
        self.setGeometry(100,100,850,300)
        #
        self.machine = machine
        self.componentGuis = []
        #
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setAlignment(Qt.AlignTop)
        #
        self.setLayout(self.mainLayout)
        self.show()

        self.topLayout = QHBoxLayout()
        self.topLayout.setAlignment(Qt.AlignTop)
        self.mainLayout.addLayout(self.topLayout)

        self.MDI = None
        '''
        Top Part Layout (left side)
        '''
        self.topLayoutLeft = QVBoxLayout()
        self.topLayoutLeft.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.topLayout.addLayout(self.topLayoutLeft)
        # select site of operation of machine
        self.siteLayout = QHBoxLayout()
        self.topLayoutLeft.addLayout(self.siteLayout)
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
        self.topLayoutLeft.addLayout(self.purposeLayout)
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
        self.topLayoutLeft.addLayout(self.operationLayout)
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
        '''
        Top Part Layout (right side)
        - button to classify thing after 2006/42/EG
        '''
        self.topLayout.addStretch()
        self.topLayoutRight = QVBoxLayout()
        self.topLayoutLeft.setAlignment(Qt.AlignTop | Qt.AlignRight)
        self.topLayout.addLayout(self.topLayoutRight)

        self.mdeButton = QPushButton('MRL')
        self.mdeButton.setFixedWidth(80)
        self.mdeButton.clicked.connect(self.startMDI)
        self.topLayoutRight.addWidget(self.mdeButton)

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

    def startMDI(self):
        if self.MDI is None:
            self.MDI = MachineryDirectiveInterface(self.machine)
            self.MDI.applicabilityPilot()
        else:
            self.MDI.show()


    def addComponent(self):
        CG = ComponentGui(parent=self)
        self.componentGuis.append(CG)
        self.bottomLayout.addWidget(CG)

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
    MG = MachineGui(M)

    #sys.exit(app.exec_())