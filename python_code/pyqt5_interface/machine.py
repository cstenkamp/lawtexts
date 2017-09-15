from PyQt5.QtCore import Qt, QTimer, QObjectCleanupHandler
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import *

import sys

from panel import *


class Machine():
    def __init__(self, purpose=None, site=None, category=None, components=[], humanOperation=False):
        self.purpose = purpose
        self.site = site
        self.category = category
        self.components = components
        self.humanOperation = humanOperation


    def newComponent(self):
        c = Component()
        self.addComponent(c)


    def addComponent(self,component):
        self.components.append(component)


    def removeComponent(self,component):
        if self.components.count(component) < 0:
            del self.components[self.components.index(component)]
        else:
            print("component not in machine's component list")




class Component():
    def __init__(self, name=None):
        self.name = name
        self.features = []

    def setName(self,name):
        self.name = name

    def newFeature(self):
        f = Feature()
        self.addFeature(f)

    def addFeature(self,feature):
        self.features.append(feature)


    def removeFeature(self,feature):
        if self.features.count(feature) < 0:
            del self.features[self.features.index(feature)]
        else:
            print("feature not in component's feature list")



class Feature():
    def __init__(self,name=None, values={}):
        self.name = name
        self.values = values

    def setName(self,name):
        self.name = name

    def addValue(self,name,value):
        self.values[name] = value

    def clearVals(self):
        self.values = {}

'''




class MachineGui(QFrame):
    def __init__(self,machine, parent=None):
        super(MachineGui,self).__init__(parent=parent)
        self.machine = machine
        self.componentGuis = []



        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.mainLayout.setAlignment(Qt.AlignTop|Qt.AlignLeft)

        self.topLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.topLayout)

        self.topLeftLayout = QVBoxLayout()
        self.topLayout.addLayout(self.topLeftLayout)
        self.topLayout.addStretch()
        self.topRightLayout = QVBoxLayout()
        self.topLayout.addLayout(self.topRightLayout)

        self.addComponentButton = QPushButton('Komponente hinzufügen')
        self.addComponentButton.clicked.connect(self.addComponent)
        self.topRightLayout.addWidget(self.addComponentButton)

        self.bottomLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.bottomLayout)


        self.show()


    def addComponent(self):
        CG = ComponentGui(parent=self)
        self.componentGuis.append(CG)
        self.bottomLayout.addWidget(CG)







if __name__ == '__main__':
    app = QApplication(sys.argv)
    M = Machine()
    mg = MachineGui(M)

'''