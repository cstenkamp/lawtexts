#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt, QTimer, QObjectCleanupHandler
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import *
#from PyQt5.QtWebEngineWidgets import QWebEngineView
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
from atexLogic import AtexLogic
from question import Question 

from basicView import QuestionInterface



class RoleView(QuestionInterface):
    def __init__(self,Product, logic):
        super(RoleView,self).__init__(Product, logic)

        
        if not logic is None:
            self.logic = logic
        else:
            self.logic = self

        self.role = None

        self.logic.QD = Question('Produkt wird unter eigenem Namen oder unter eigener Handelsmarke in Verkehr gebracht, oder Produkt wird vor in Verkehr bringen so verändert, dass die Konformität mit einer oder mehreren der EU-Richtlinien beeinträchtigt werden könnte?',
                      effect={'y':'extra',
                              'n':'None'})

    def next(self,B):
        self.close()
        if B == 'y':
            self.Product.extraDuties = True 
        else:
            self.Product.extraDuties = False 


    def getUserRole(self):
        self.show()
        self.roleLayout = QVBoxLayout()
        self.roleLayout.setAlignment(Qt.AlignCenter)
        self.topLayout.addLayout(self.roleLayout)

        self.label = QLabel('Bitte bestimmen sie ihre Rolle als Wirtschaftsakteur.')
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



    def setUserRole(self, role):
        self.role = role
        self.Product.role = role 
        if (self.role == 'Händler') or (self.role == 'Einführer'):
            self.getExtraDuties()
        else:
            self.close()


    def getExtraDuties(self):
        self.startYesNoQuestions(self.logic.QD)