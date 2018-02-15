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

        #
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setAlignment(Qt.AlignTop)
        #
        self.setLayout(self.mainLayout)
        self.show()

        self.topLayout = QHBoxLayout()
        self.topLayout.setAlignment(Qt.AlignTop)
        self.mainLayout.addLayout(self.topLayout)


        self.bottomLayout = QHBoxLayout()
        self.bottomLayout.setAlignment(Qt.AlignTop)
        self.mainLayout.addLayout(self.bottomLayout)


        self.htmlView = QWebEngineView()
        self.topLayout.addWidget(self.htmlView)

        self.buttonYes = QPushButton('ja')
        self.buttonYes.setFixedWidth(80)
        self.buttonYes.clicked.connect(self.yes)
        self.bottomLayout.addWidget(self.buttonYes)

        self.buttonNo = QPushButton('nein')
        self.buttonNo.setFixedWidth(80)
        self.buttonNo.clicked.connect(self.no)
        self.bottomLayout.addWidget(self.buttonNo)

        self.Q = questions.Q0
        self.updateView(self.Q.text)


    def yes(self):
        self.Q = self.Q.posChild
        self.updateView(self.Q.text)

    def no(self):
        self.Q = self.Q.negChild
        self.updateView(self.Q.text)



    def updateView(self,html):
    	self.htmlView.setHtml(html)




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


    dictParser = dictPARSER(atexAppendice,atexArticle)



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