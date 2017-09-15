from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

class Question(QFrame):
    def __init__(self,text,parent=None,antagonists=[]):
        super(Question,self).__init__()
        if parent is None:
            self.indent = 0
        else:
            self.indent = parent.indent + 100
            parent.addChild(self)
        self.antagonists = antagonists
        self.setFrameShape(QFrame.Box)
        self.setFrameShadow(QFrame.Sunken)
        self.mainLayout = QHBoxLayout(self)
        self.setLayout(self.mainLayout)
        self.mainLayout.setAlignment(Qt.AlignLeft)
        #self.setFixedHeight(80)
        #
        self.spacer = QSpacerItem(self.indent, 100, QSizePolicy.Minimum, QSizePolicy.Maximum)
        self.mainLayout.addItem(self.spacer)
        #
        self.label = QLabel(text)
        self.label.setWordWrap(True)
        self.label.setMinimumWidth(400)
        self.label.setContentsMargins(2,10,2,10)
        self.label.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Fixed)
        self.mainLayout.addWidget(self.label)
        #
        self.children = []

    def addChild(self,child):
        self.children.append(child)

    def removeChild(self,child):
        print(child)
        print('implement me')

    def addAntagonists(self,antagonist):
        self.antagonists.append(antagonist)

    def resetAntagonists(self):
        pass
        #print('phyx me')
        '''
        for antagonist in self.antagonists:
            if self.yes.isChecked():
                antagonist.no.setChecked(True)
                antagonist.yes.setChecked(False)
                antagonist.hideChildren()
            elif self.no.isChecked():
                antagonist.yes.setChecked(True)
                antagonist.no.setChecked(False)
                antagonist.showChildren()
        '''


    def iterHide(self):
        for child in self.children:
            child.iterHide()
            if isinstance(child, RadioQuestion):
                child.no.setChecked(True)
                self.no.setAutoExclusive(False)
                child.no.setChecked(False)
                self.no.setAutoExclusive(True)
                child.hidee()
            else:
                child.hide()

    def hideChildren(self):
        for child in self.children:
            self.iterHide()

    def showChildren(self):
        for child in self.children:
            child.show()
            if isinstance(child, RadioQuestion):
                child.no.setChecked(True)
                self.no.setAutoExclusive(False)
                child.no.setChecked(False)
                self.no.setAutoExclusive(True)
                child.showw()
            else:
                child.hidee()


class Answer(Question):
    def __init__(self):
        super(Answer,self).__init__(text,parent=parent,antagonists=[])




class RadioQuestion(Question):
    def __init__(self,text, parent=None,antagonists=[]):
        super(RadioQuestion,self).__init__(text,parent=parent,antagonists=antagonists)
        #
        self.yes = QRadioButton('ja')
        self.no = QRadioButton('nein')
        self.no.setChecked(False)
        self.yes.setChecked(False)
        self.mainLayout.addWidget(self.yes)
        self.mainLayout.addWidget(self.no)


    def showw(self):
        self.show()
        self.no.setChecked(True)
        self.no.setAutoExclusive(False)
        self.no.setChecked(False)
        self.no.setAutoExclusive(True)

    def hidee(self):
        self.hide()
        self.no.setChecked(True)
        self.no.setAutoExclusive(False)
        self.no.setChecked(False)
        self.no.setAutoExclusive(True)



