from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

import objects as obj 

class Panel(QWidget):
    def __init__(self):
        super(Panel,self).__init__()
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.setLayout(self.mainLayout)
        # first row is always there
        self.row1 = QHBoxLayout()
        self.row1.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.mainLayout.addLayout(self.row1)

    def delete(self):
        print('delete panel')
        self.deleteLater()
        del self 

    def addContentPanel(self):
        self.row2 = QHBoxLayout()
        self.row2.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.mainLayout.addLayout(self.row2)
        # materials to select from
        contents = ['--andere--']+sorted(obj.loadCSV('csv/Materialien.csv'))
        self.selectionMenu = QComboBox()
        for c in contents:
            self.selectionMenu.addItem(c)
        #self.selectionMenu.activated.connect(self.specifyContent)
        self.row1.addWidget(self.selectionMenu)
        self.specifyContent()
        # state to select from (gas/liquid/solid)
        self.gasButton = QRadioButton('Gas förmig')
        self.row2.addWidget(self.gasButton)
        #
        self.liquidGasButton = QRadioButton('verflüssigtes Gas')
        self.row2.addWidget(self.liquidGasButton)
        #
        self.fluidButton = QRadioButton('flüssig')
        self.row2.addWidget(self.fluidButton)
        self.fluidButton.setChecked(True)
        #
        self.solidButton = QRadioButton('fest')
        self.row2.addWidget(self.solidButton)
        self.buttons = [self.gasButton,self.liquidGasButton,self.fluidButton,self.solidButton]
        #
    def specifyContent(self):
        #if self.selectionMenu.currentText() == '--andere--':
        self.specifiers = obj.loadCSV('csv/Eigenschaften.csv')
        self.specificationMenu = QMenu()
        for s in self.specifiers:
            a = self.specificationMenu.addAction(s)
            a.setCheckable(True)
        self.specificationMenuButton = QPushButton('Eigenschaften')
        self.specificationMenuButton.setMenu(self.specificationMenu)
        self.row1.addWidget(self.specificationMenuButton)
        #elif hasattr(self, 'specificationMenu'):
        #    self.specificationMenu.deleteLater()

    def addFuelPanel(self):
        self.selectionMenu = QComboBox()
        fuels = obj.loadCSV('csv/Treibstoffe.csv')
        for f in fuels:
            self.selectionMenu.addItem(f)
        self.row1.addWidget(self.selectionMenu)

    def addVoltagePanel(self):
        self.lineEdit = QLineEdit()
        self.lineEdit.setFixedWidth(100)
        self.row1.addWidget(self.lineEdit)
        self.selectionMenu = QComboBox()
        self.selectionMenu.addItem('Volt AC')
        self.selectionMenu.addItem('Volt DC')
        self.selectionMenu.setFixedWidth(80)
        self.row1.addWidget(self.selectionMenu)

    def addPowerPanel(self):
        self.lineEdit = QLineEdit()
        self.lineEdit.setFixedWidth(100)
        self.row1.addWidget(self.lineEdit)
        self.selectionMenu = QComboBox()
        self.selectionMenu.addItem('PS')
        self.selectionMenu.addItem('Watt')
        self.selectionMenu.setFixedWidth(80)
        self.row1.addWidget(self.selectionMenu)

    def addDiameterPanel(self):
        self.lineEdit = QLineEdit()
        self.lineEdit.setFixedWidth(100)
        self.row1.addWidget(self.lineEdit)
        self.label = QLabel('cm')
        self.row1.addWidget(self.label)

    def addTemperaturePanel(self):
        self.lineEdit = QLineEdit()
        self.lineEdit.setFixedWidth(100)
        self.row1.addWidget(self.lineEdit)
        self.label = QLabel('Grad Celsius')
        self.row1.addWidget(self.label)

    def addLengthPanel(self):
        self.lineEdit = QLineEdit()
        self.lineEdit.setFixedWidth(100)
        self.row1.addWidget(self.lineEdit)
        self.label = QLabel('m')
        self.row1.addWidget(self.label)

    def addVolumePanel(self):
        self.lineEdit = QLineEdit()
        self.lineEdit.setFixedWidth(100)
        self.row1.addWidget(self.lineEdit)
        self.label = QLabel('m^3')
        self.row1.addWidget(self.label)

    def addPressurePanel(self):
        self.lineEdit = QLineEdit()
        self.lineEdit.setFixedWidth(100)
        self.row1.addWidget(self.lineEdit)
        self.selectionMenu = QComboBox()
        units = sorted(['bar','at','atm','psi','Torr','Pa'])
        for u in units:
            self.selectionMenu.addItem(u)
        self.selectionMenu.setFixedWidth(80)
        self.row1.addWidget(self.selectionMenu)


    def addDatePanel(self):
        self.lineEdit = QLineEdit()
        self.label = QLabel('vor dem 01.01.2003 in Verkehr gebracht?')
        self.row1.addWidget(self.label)
        self.checkBox = QCheckBox()
        self.checkBox.setChecked(False)
        self.row1.addWidget(self.checkBox)


