from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

import objects as obj 

class Panel(QWidget):
    def __init__(self,parent):
        super(Panel,self).__init__()
        self.parent = parent
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
        self.selectionMenu.activated.connect(lambda: self.setVal('content',self.selectionMenu.currentText()))
        #self.selectionMenu.activated.connect(self.specifyContent)
        self.row1.addWidget(self.selectionMenu)
        self.selectionMenu.setCurrentIndex(-1)
        self.specifyContent()
        # state to select from (gas/liquid/solid)
        self.gasButton = QRadioButton('Gas förmig')
        self.gasButton.clicked.connect(lambda: self.setVal('stateOfMatter','gas'))
        self.row2.addWidget(self.gasButton)
        #
        self.liquidGasButton = QRadioButton('verflüssigtes Gas')
        self.liquidGasButton.clicked.connect(lambda: self.setVal('stateOfMatter','liquified_gas'))
        self.row2.addWidget(self.liquidGasButton)
        #
        self.fluidButton = QRadioButton('flüssig')
        self.fluidButton.clicked.connect(lambda: self.setVal('stateOfMatter','liquid'))
        self.row2.addWidget(self.fluidButton)
        #
        self.solidButton = QRadioButton('fest')
        self.solidButton.clicked.connect(lambda: self.setVal('stateOfMatter','solid'))
        self.row2.addWidget(self.solidButton)

        self.solidButton.setAutoExclusive(False)
        self.solidButton.setChecked(False)
        self.solidButton.setAutoExclusive(True)

        self.buttons = [self.gasButton,self.liquidGasButton,self.fluidButton,self.solidButton]
        #
    def specifyContent(self):
        #if self.selectionMenu.currentText() == '--andere--':
        self.specifiers = obj.loadCSV('csv/Eigenschaften.csv')
        self.specificationMenu = QMenu()
        for s in self.specifiers:
            a = self.specificationMenu.addAction(s)
            a.triggered.connect(self.prepareSpecifications)
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
        self.selectionMenu.activated.connect(lambda: self.setVal('Fuel',self.selectionMenu.currentText()))
        self.row1.addWidget(self.selectionMenu)
        self.selectionMenu.setCurrentIndex(-1)

    def addVoltagePanel(self):
        self.lineEdit = QLineEdit()
        self.lineEdit.setFixedWidth(100)
        self.lineEdit.editingFinished.connect(lambda: self.setVal('value',self.lineEdit.text()))
        self.row1.addWidget(self.lineEdit)
        self.selectionMenu = QComboBox()
        self.selectionMenu.addItem('Volt AC')
        self.selectionMenu.addItem('Volt DC')
        self.selectionMenu.activated.connect(lambda: self.setVal('unit',self.selectionMenu.currentText()))
        self.selectionMenu.setFixedWidth(80)
        self.row1.addWidget(self.selectionMenu)
        self.selectionMenu.setCurrentIndex(-1)

    def addPowerPanel(self):
        self.lineEdit = QLineEdit()
        self.lineEdit.setFixedWidth(100)
        self.lineEdit.editingFinished.connect(lambda: self.setVal('value',self.lineEdit.text()))
        self.row1.addWidget(self.lineEdit)
        self.selectionMenu = QComboBox()
        self.selectionMenu.addItem('PS')
        self.selectionMenu.addItem('Watt')
        self.selectionMenu.activated.connect(lambda: self.setVal('unit',self.selectionMenu.currentText()))
        self.selectionMenu.setFixedWidth(80)
        self.row1.addWidget(self.selectionMenu)
        self.selectionMenu.setCurrentIndex(-1)

    def addDiameterPanel(self):
        self.lineEdit = QLineEdit()
        self.lineEdit.setFixedWidth(100)
        self.lineEdit.editingFinished.connect(lambda: self.setVal('value',self.lineEdit.text()))
        self.row1.addWidget(self.lineEdit)
        self.label = QLabel('cm')
        self.row1.addWidget(self.label)

    def addTemperaturePanel(self):
        self.lineEdit = QLineEdit()
        self.lineEdit.setFixedWidth(100)
        self.lineEdit.editingFinished.connect(lambda: self.setVal('value',self.lineEdit.text()))
        self.row1.addWidget(self.lineEdit)
        self.label = QLabel('Grad Celsius')
        self.row1.addWidget(self.label)

    def addLengthPanel(self):
        self.lineEdit = QLineEdit()
        self.lineEdit.setFixedWidth(100)
        self.lineEdit.editingFinished.connect(lambda: self.setVal('value',self.lineEdit.text()))
        self.row1.addWidget(self.lineEdit)
        self.label = QLabel('m')
        self.row1.addWidget(self.label)

    def addVolumePanel(self):
        self.lineEdit = QLineEdit()
        self.lineEdit.setFixedWidth(100)
        self.lineEdit.editingFinished.connect(lambda: self.setVal('value',self.lineEdit.text()))
        self.row1.addWidget(self.lineEdit)
        self.label = QLabel('m^3')
        self.row1.addWidget(self.label)

    def addPressurePanel(self):
        self.lineEdit = QLineEdit()
        self.lineEdit.setFixedWidth(100)
        self.lineEdit.editingFinished.connect(lambda: self.setVal('value',self.lineEdit.text()))
        self.row1.addWidget(self.lineEdit)
        self.selectionMenu = QComboBox()
        units = sorted(['bar','at','atm','psi','Torr','Pa'])
        for u in units:
            self.selectionMenu.addItem(u)
        self.selectionMenu.activated.connect(lambda: self.setVal('unit',self.selectionMenu.currentText()))
        self.selectionMenu.setFixedWidth(80)
        self.row1.addWidget(self.selectionMenu)
        self.selectionMenu.setCurrentIndex(-1)


    def addDatePanel(self):
        self.lineEdit = QLineEdit()
        self.label = QLabel('vor dem 01.01.2003 in Verkehr gebracht?')
        self.row1.addWidget(self.label)
        self.checkBox = QCheckBox()
        self.checkBox.setChecked(False)
        self.checkBox.clicked.connect(lambda: self.setVal('date',self.checkBox.isChecked()))
        self.row1.addWidget(self.checkBox)

    def setVal(self,name, val):
        if val is None:
            return 
        self.parent.feature.addValue(name, val)

    def prepareSpecifications(self):
        specs = []
        for a in self.specificationMenu.actions():
            if a.isChecked():
                specs.append(a.text())
        print(specs)
        self.setVal('specifications',specs)



