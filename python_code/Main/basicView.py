from PyQt5.QtCore import Qt, QTimer, QObjectCleanupHandler
from PyQt5.QtGui import QPainter, QStandardItemModel
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys, os 

from _machine import Machine

sys.path.insert(0, os.path.join(os.getcwd(),'html_parser/'))
from directiveParser import PARSER as directivePARSER

sys.path.insert(0, os.path.join(os.getcwd(),'dict_parser/'))
from dictParser import PARSER as dictPARSER

sys.path.insert(0, os.path.join(os.getcwd(),'saveLoad/'))
from configurator import Configurator
from jsonParser import PARSER as jPARSER

sys.path.insert(0, os.path.join(os.getcwd(),'logic/'))
from question import Question 


class CheckableComboBox(QComboBox):
    def __init__(self):
        super(CheckableComboBox, self).__init__()
        self.view().pressed.connect(self.handleItemPressed)
        self.setModel(QStandardItemModel(self))
        self.hide()

    def handleItemPressed(self, index):
        item = self.model().itemFromIndex(index)
        if item.checkState() == Qt.Checked:
            item.setCheckState(Qt.Unchecked)
        else:
            item.setCheckState(Qt.Checked)

class QuestionInterface(QWidget):
    def __init__(self, Product, logic):
        super(QuestionInterface,self).__init__()

        self.setGeometry(100,100,850,300)
        self.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Expanding)


        #
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setAlignment(Qt.AlignCenter)
        #
        self.setLayout(self.mainLayout)
        self.show()

        self.topLayout = QHBoxLayout()
        self.topLayout.setAlignment(Qt.AlignTop)
        self.mainLayout.addLayout(self.topLayout)

        self.bottomLayout = QHBoxLayout()
        self.bottomLayout.setAlignment(Qt.AlignTop)
        self.mainLayout.addLayout(self.bottomLayout)

        self.Product = Product
        self.logic = logic
        
        self.hide()

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())


    def updateView(self,html):
        self.htmlView.setHtml(html)


    def startYesNoQuestions(self, firstQuestion):
        self.show()
        self.yesNoLayout()
        self.logic.Q = firstQuestion
        self.updateView(self.logic.Q.text)

    def yesNoLayout(self):
        self.clearLayout(self.topLayout)
        self.clearLayout(self.bottomLayout)
        self.htmlView = QWebEngineView()
        self.topLayout.addWidget(self.htmlView)

        self.buttonYes = QPushButton('ja')
        self.buttonYes.setFixedWidth(80)
        self.buttonYes.clicked.connect(lambda: [self.next('y')])
        self.bottomLayout.addWidget(self.buttonYes)

        self.buttonNo = QPushButton('nein')
        self.buttonNo.setFixedWidth(80)
        self.buttonNo.clicked.connect(lambda: [self.next('n')])
        self.bottomLayout.addWidget(self.buttonNo)


    def next(self,B):
        pass

    def dropDownLayout(self):

        self.ddLayout = QVBoxLayout()
        self.ddLayout.setAlignment(Qt.AlignTop)
        self.mainLayout.addLayout(self.ddLayout)

        self.specifiers = ['a','b','c']
        self.toolbutton = QToolButton(self)
        self.toolbutton.setText('Select Categories ')
        self.toolmenu = QMenu(self)
        for i in range(3):
            action = self.toolmenu.addAction("Category " + str(i))
            action.setCheckable(True)
        self.toolbutton.setMenu(self.toolmenu)
        self.toolbutton.setPopupMode(QToolButton.InstantPopup)

        self.ddLayout.addWidget(self.toolbutton)
        self.ddLayout.addWidget(self.toolmenu)