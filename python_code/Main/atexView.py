from PyQt5.QtCore import Qt, QTimer, QObjectCleanupHandler
from PyQt5.QtGui import QPainter
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
from atexLogic import ATEX
from atexTree import Questions


# QWebEngineView.setHtml(html)
html = '''<html>
<head>
<title>A Sample Page</title>
</head>
<body>
<h1>Hello, World!</h1>
<hr />
I have nothing to say.
</body>
</html>'''
class AtexView(QWidget):
    def __init__(self,atex,questions):
        super(AtexView,self).__init__()
        self.setGeometry(100,100,850,300)
        self.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Expanding)

        self.effects = []
        self.atex = atex
        self.questions = questions

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



        self.getUserRole()

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

    def changeLayout(self):

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



    def setUserRole(self,role):
        self.role = role 
        self.atex.setUserRole(role)
        self.clearLayout(self.roleLayout)
        self.changeLayout()
        if (self.role == 'Händler') or (self.role =='Einführer'):
            self.Q = self.questions.QD
            self.updateView(self.questions.QD.text)
        else:
            self.startQuestions()





    def getUserRole(self):

        self.roleLayout = QVBoxLayout()
        self.roleLayout.setAlignment(Qt.AlignCenter)
        self.topLayout.addLayout(self.roleLayout)

        self.label = QLabel('Bitte bestimmen sie ihre Rolle als wirtschaftsakteur.')
        self.label.setAlignment(Qt.AlignVCenter)
        self.label.setFixedWidth(300)
        self.roleLayout.addWidget(self.label)

        self.buttonH = QPushButton('Hersteller')
        self.buttonH.setFixedWidth(100)
        self.buttonH.clicked.connect(lambda: [self.setUserRole('Hersteller')])
        self.roleLayout.addWidget(self.buttonH)

        self.buttonE = QPushButton('Einführer')
        self.buttonE.setFixedWidth(100)
        self.buttonE.clicked.connect(lambda: [self.setUserRole('Einführer')])
        self.roleLayout.addWidget(self.buttonE)

        self.buttonD = QPushButton('Händler')
        self.buttonD.setFixedWidth(100)
        self.buttonD.clicked.connect(lambda: [self.setUserRole('Händler')])
        self.roleLayout.addWidget(self.buttonD)

        self.buttonB = QPushButton('(Bevollmächtigter)')
        self.buttonB.setFixedWidth(100)
        self.buttonB.clicked.connect(lambda: [self.setUserRole('Bevollmächtigter')])
        self.roleLayout.addWidget(self.buttonB)


    def startQuestions(self):
        self.Q = self.questions.Q0
        self.updateView(self.Q.text)



    def next(self,b):
        if self.Q.effect[b]=='extra':
            self.atex.setUserRole(self.role, extraDuties=True)
            self.startQuestions()
        else:
            self.effects.append([self.Q.effect[b]])
            if b == 'y':
                self.Q = self.Q.posChild
            elif b == 'n':
                self.Q = self.Q.negChild
            if self.Q is None:
                self.finalize()
            else:
                self.updateView(self.Q.text)

    def updateView(self,html):
    	self.htmlView.setHtml(html)

    def finalize(self):
        self.clearLayout(self.bottomLayout)
        self.buttonClose = QPushButton('Schließen')
        self.buttonClose.clicked.connect(self.close)
        self.bottomLayout.addWidget(self.buttonClose)
        self.atex.getGroupAndCategory(effects=self.effects)
        html = self.atex.formatOutput2()
        self.updateView(html)




if __name__ == '__main__':


    directiveParser = directivePARSER()
    directiveParser.secondaries = ['<p class="ti-grseq-1".+>\d\.[^\d]']
    directiveParser.secondaryExtractor = '>((\d\.){1,1}|[A-Z]\.)'

    directiveParser.tertiaries = ['<p class="ti-grseq-1".+>(\d\.){2,2}[^\d].*<spa']
    directiveParser.tertiaryExtractor = '((\d\.){2,2})'

    directiveParser.quaternaries = ['<p class="ti-grseq-1".+>(\d\.){3,3}[^\d].*<spa']
    directiveParser.quaternaryExtractor = '((\d\.){3,3})'

    directiveParser.qStart = 4
    directiveParser.qEnd = 6

    text = directiveParser.getHtml(p='html_resources/directives/atex.html')
    atexArticle = directiveParser.parseArticles(text)
    atexAppendice = directiveParser.parseAppendices(text)

    ARTICLES = {'ATEX':atexArticle
               }
    APPENDICES = {'ATEX':atexAppendice
                 }


    dictParser = dictPARSER(APPENDICES,ARTICLES)



    jsonPath = 'json/__exampleMachine.json'

    jparser = jPARSER()
    machineData = jparser.parse(jsonPath)
    Product = Machine()

    configurator = Configurator(Product)
    configurator.configure(machineData)

    atex = ATEX(Product, dictParser)
    questions = Questions()

    app = QApplication(sys.argv)
    MG = AtexView(atex,questions)