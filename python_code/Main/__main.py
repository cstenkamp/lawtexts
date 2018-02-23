#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os, webbrowser
from pprint import pprint as print
from _machine import Machine


sys.path.insert(0, os.path.join(os.getcwd(),'saveLoad/'))
from configurator import Configurator
from jsonParser import PARSER as jPARSER

sys.path.insert(0, os.path.join(os.getcwd(),'logic/'))
from _logicUnit import LOGIC
from atexLogic import AtexLogic
from mrlLogic import MrlLogic
from nsrLogic import NsrLogic
from atexTree import Questions

sys.path.insert(0, os.path.join(os.getcwd(),'html_parser/'))
from directiveParser import PARSER as directivePARSER

sys.path.insert(0, os.path.join(os.getcwd(),'dict_parser/'))
from dictParser import PARSER as dictPARSER

from PyQt5.QtWidgets import QApplication
from roleView import RoleView
from atexView import AtexView
from mrlView import MrlView
from nsrView import NsrView
from basicView import QuestionInterface



class Main():
    def __init__(self, machineJsonPath='json/__exampleMachine.json'):

        """
        load json
        """
        self.jsonPath = machineJsonPath
        self.jparser = jPARSER()
        self.machineData = self.jparser.parse(self.jsonPath)

        self.jsonPath = 'json/parts.json'
        self.partsData = self.jparser.parse(self.jsonPath)


        """
        parse directives
        """
        self.directiveParser = directivePARSER()

        """
        add parsed directive articles and appendices to 
        a dictionairy parser
        """
        self.dictParser = dictPARSER(self.directiveParser.appendices,
                                     self.directiveParser.articles)


        """
        load a product
        """
        self.Product = Machine()
        self.configurator = Configurator(self.Product)
        self.configurator.configure(self.machineData)


    def getUserRole(self):
        """
        open an interface window
        """

        # general question concerning the user's role (hersteller, beauftragter...)
        self.roleView.getUserRole()


    def loadLogicEngines(self):
        """
        load logic engines
        """
        self.atexLogic = AtexLogic(self.Product, self.dictParser)
        self.mrlLogic = MrlLogic(self.Product, self.dictParser)
        self.nsrLogic = NsrLogic(self.Product, self.dictParser)


    def loadViews(self):
        self.app = QApplication(sys.argv)
        self.roleView = RoleView(self.Product, None)
        self.atexView = AtexView(self.Product, self.atexLogic)
        self.mrlView = MrlView(self.Product, self.mrlLogic)
        self.nsrView = NsrView(self.Product, self.nsrLogic)

    def atexTest(self):
        self.atexView.startYesNoQuestions(self.atexLogic.QA)


    def mrlTest(self):
        self.mrlView.startYesNoQuestions(self.mrlLogic.QA)


    def nsrTest(self):
        self.nsrView.startYesNoQuestions(self.nsrLogic.QA)

if __name__ == '__main__':
    m = Main(machineJsonPath='json/__exampleMachine.json',
             )
    self = m 
    m.loadLogicEngines()
    m.loadViews()
    m.getUserRole()