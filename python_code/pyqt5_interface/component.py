from PyQt5.QtCore import Qt, QTimer, QObjectCleanupHandler
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import *

from panel import *

import objects as obj 

class ComponentFeature(QFrame):
    def __init__(self, parent, panel=None):
        super(ComponentFeature,self).__init__()
        self.setFrameShape(QFrame.Box)
        self.setFrameShadow(QFrame.Sunken)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.parent = parent
        self.panel = panel
        self.featureType = None
        self.mainLayout = QHBoxLayout(self)
        self.setLayout(self.mainLayout)
        self.mainLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        # add button to delete feature
        self.delButton = QPushButton('-')
        self.delButton.setFixedWidth(22)
        self.delButton.clicked.connect(self.delete)
        self.mainLayout.addWidget(self.delButton)
        # add combobox to select type of feature
        self.featureTypes = ['']+sorted(['Betriebsspannung','Inhalt',
                         'Druck','Temperatur','Durchmesser','Herstellungsdatum',
                         'Leistung','Länge','Volumen','Treibstoff'])
        self.featureMenu = QComboBox()
        self.featureMenu.setFixedWidth(150)
        for f in self.featureTypes:
            self.featureMenu.addItem(f)
        self.featureMenu.activated.connect(self.addPanels)
        self.widgetStack = QStackedWidget()
        self.widgetStack.setFixedWidth(150)
        self.widgetStack.setFixedHeight(20)
        self.widgetStack.addWidget(self.featureMenu)
        self.fixedLabel = QLabel()
        self.widgetStack.addWidget(self.fixedLabel)
        self.mainLayout.addWidget(self.widgetStack)

    def fixFeatureType(self):
        l = self.featureMenu.currentText()
        self.fixedLabel.setText(l)
        self.widgetStack.setCurrentWidget(self.fixedLabel)


    def delete(self):
        print('deleted feature')
        self.deleteLater()
        idx = self.parent.parent.features.index(self)
        del self.parent.parent.features[idx]
        del self

    def clearOldPanels(self):
        if not self.panel is None:
            self.panel.delete()


    def addPanels(self):
        self.clearOldPanels()
        t = self.featureMenu.currentText()
        self.featureType = t
        print(t)
        self.panel = Panel()
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


        self.mainLayout.addWidget(self.panel)


class ComponentConfiguration(QWidget):
    def __init__(self,parent):
        super(ComponentConfiguration,self).__init__()
        self.parent = parent
        self.setGeometry(600,100,800,300)
        self.setWindowTitle(parent.componentType)
        self.mainLayout = QVBoxLayout(self)
        self.setLayout(self.mainLayout)
        self.mainLayout.setAlignment(Qt.AlignTop|Qt.AlignLeft)
        self.show()
        '''
        Top Part Layout
            buttons to add feature and to accept configuration
        '''
        self.topLayout = QHBoxLayout()
        self.topLayout.setAlignment(Qt.AlignRight | Qt.AlignTop)
        # button to add a feature to component
        self.addFeatureButton = QPushButton('Eigenschaft Hinzufügen')
        self.addFeatureButton.clicked.connect(self.addFeature)
        self.topLayout.addWidget(self.addFeatureButton)
        # button to accept configuration and close window
        self.acceptButton = QPushButton('abschicken')
        self.acceptButton.clicked.connect(self.accepted)
        self.topLayout.addWidget(self.acceptButton)
        self.mainLayout.addLayout(self.topLayout)
        '''
        Bottom Part Layout
            contains list of features (in graphical sense)
        '''
        self.bottomLayout = QVBoxLayout()
        self.bottomLayout.setAlignment(Qt.AlignTop)
        self.mainLayout.addLayout(self.bottomLayout)


    def accepted(self):
        print('accepted')
        self.hide()

    def addFeature(self):
        print('add feature')
        f = ComponentFeature(self)
        self.parent.features.append(f)
        self.bottomLayout.addWidget(f)

    def addKnownFeature(self, featureType = 'Betriebsspannung'):
        print('add feature')
        f = ComponentFeature(self)
        self.parent.features.append(f)
        self.bottomLayout.addWidget(f)
        f.featureMenu.setCurrentText(featureType)
        f.fixFeatureType()
        return f


class Component(QFrame):
    def __init__(self, parent):
        super(Component,self).__init__()
        self.setFrameShape(QFrame.Box)
        self.setFrameShadow(QFrame.Sunken)
        self.features = []
        self.parent = parent 
        self.componentType = None
        self.configuration = None
        self.mainLayout = QHBoxLayout(self)
        self.setLayout(self.mainLayout)
        self.mainLayout.setAlignment(Qt.AlignTop)
        # add button to delete component
        self.delButton = QPushButton('-')
        self.delButton.setFixedWidth(22)
        self.delButton.clicked.connect(self.delete)
        self.mainLayout.addWidget(self.delButton)
        # add combobox to select from list of components
        self.componentsList = ['-']+sorted(obj.loadCSV('csv/confirmed_komponenten.csv'))
        self.selectionMenu = QComboBox()
        for c in self.componentsList:
            self.selectionMenu.addItem(c)
        self.selectionMenu.activated.connect(self.componentSelected)
        self.mainLayout.addWidget(self.selectionMenu)

        self.operationLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.operationLayout)
        self.operationLabel = QLabel('Komponente ist durch Beschäftigte zu bedienen oder zu überwachen?')
        self.operationLabel.setWordWrap(True)
        self.operationLabel.setFixedWidth(190)
        self.operationLabel.setFixedHeight(55)
        self.operationLabel.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.operationLayout.addWidget(self.operationLabel)
        self.operationCheckbox = QCheckBox()
        self.operationCheckbox.setChecked(False)
        self.operationCheckbox.clicked.connect(self.setMachineOperation)
        self.operationLayout.addWidget(self.operationCheckbox)
        self.operationLayout.addStretch()

        self.mainLayout.addStretch()



    def setMachineOperation(self):
        print('implement "setMachineOperation" in "Component"')


    def delete(self):
        print('delete component')
        self.deleteLater()
        idx = self.parent.machine.components.index(self)
        del self.parent.machine.components[idx]
        del self 

    def componentSelected(self):
        ct = self.selectionMenu.currentText()
        if ct == '-':
            return 
        print('component type selected: {0}'.format(ct))
        self.componentType = ct
        self.selectionMenu.clear()
        self.componentsList = sorted(obj.loadCSV('csv/confirmed_komponenten.csv'))
        for c in self.componentsList:
            self.selectionMenu.addItem(c)
        self.selectionMenu.setCurrentText(ct)
        if not hasattr(self, 'confButton'):
            # add button to configure component
            self.confButton = QPushButton('konfigurieren')
            self.confButton.clicked.connect(self.configure)
            self.mainLayout.addWidget(self.confButton)
        else:
            self.configuration = None
        self.configure()


    def configure(self):
        print('configure component')
        if self.configuration is None:
            self.configuration = ComponentConfiguration(self)
            selection = self.selectionMenu.currentText()
            #
            if selection == 'Elektromotor':
                names = ['Betriebsspannung',
                         'Leistung']
                for n in names:
                    f = self.configuration.addKnownFeature(n)
                    f.addPanels()
            #
            elif selection == 'Verbennungsmotor':
                names = ['Treibstoff',
                         'Leistung']
                for n in names:
                    f = self.configuration.addKnownFeature(n)
                    f.addPanels()
            #
            elif selection == 'Druckrohr':
                names = ['Länge',
                         'Durchmesser',
                         'Druck',
                         'Temperatur',
                         'Inhalt']
                for n in names:
                    f = self.configuration.addKnownFeature(n)
                    f.addPanels()
            #
            elif selection == 'Behälter':
                names = ['Druck',
                         'Temperatur',
                         'Volumen',
                         'Inhalt']
                for n in names:
                    f = self.configuration.addKnownFeature(n)
                    f.addPanels()
            #
            elif selection == 'Rohrleitung':
                names = ['Druck',
                         'Temperatur',
                         'Durchmesser',
                         'Länge',
                         'Inhalt']
                for n in names:
                    f = self.configuration.addKnownFeature(n)
                    f.addPanels()
            #
            elif selection == 'Dampferzeuger (Kessel)':
                names = ['Betriebsspannung',
                         'Leistung',
                         'Volumen',
                         'Druck',
                         'Inhalt',
                         'Herstellungsdatum']
                for n in names:
                    f = self.configuration.addKnownFeature(n)
                    f.addPanels()

        else:
            self.configuration.show()



