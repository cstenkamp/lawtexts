#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os
#from pprint import pprint as print
from _machine import Machine

sys.path.insert(0, os.path.join(os.getcwd(),'logic/saveLoad/'))
from configurator import Configurator
from jsonParser import PARSER as jPARSER

sys.path.insert(0, os.path.join(os.getcwd(),'logic/logic/'))
from baseLogic import BaseLogic
from atexLogic import AtexLogic
from mrlLogic import MrlLogic
from nsrLogic import NsrLogic
from dgrLogic import DgrLogic
from atexTree import Questions

sys.path.insert(0, os.path.join(os.getcwd(),'logic/html_parser/'))
from directiveParser import PARSER as dPARSER

sys.path.insert(0, os.path.join(os.getcwd(),'logic/dict_parser/'))
from dictParser import PARSER as dictPARSER

from PyQt5.QtWidgets import QApplication


sys.path.insert(0, os.path.join(os.getcwd(),'logic/views/'))
from roleView import RoleView
from atexView import AtexView
from dgrView import DgrView
from mrlView import MrlView
from nsrView import NsrView
from basicView import QuestionInterface, ResultView

class ResultBuffer():
    def __init__(self,str):
        self.str=str
    def append(self,str):
        self.str+=str

class MainLogic():
    def __init__(self, machineData=None, filePath=None):

        """
        load json
        """
        self.machineData = machineData

        self.filePath = filePath

        self.fileHandle = open(self.filePath,'w')

        self.jparser = jPARSER()
        self.jsonPartsPath = os.path.join(os.path.split(os.getcwd())[0],'jsons/parts.json')
        self.partsData = self.jparser.parse(self.jsonPartsPath)

        """
        parse directives
        """
        self.dParser = dPARSER()

        """
        add parsed directive articles and appendices to 
        a dictionairy parser
        """
        self.dictParser = dictPARSER(self.dParser.appendices,
                                     self.dParser.articles)


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
        self.dgrLogic = DgrLogic(self.Product, self.dictParser)

        childLogics = {'ATEX':self.atexLogic,
                       'MRL':self.mrlLogic,
                       'NSR':self.nsrLogic,
                       'DGR':self.dgrLogic}

        self.baseLogic = BaseLogic(self.Product, self.dictParser, 'name', childLogics=childLogics)

        res = self.baseLogic.checkParts(overwrite=False)
        # MRL should be asked always:
        self.mrlLogic.state = True
        self.baseLogic.state = True


    def loadViews(self):
        self.result_buffer = ResultBuffer('')

        '''
        self.resultView = DgrView(self.Product, self.dgrLogic, 
                                 childView = None,
                                 childLogic=self.baseLogic,
                                 buffer=self.result_buffer,
                                 parentLogic=self)
        '''
        self.resultView = ResultView()
        self.atexView = AtexView(self.Product, self.atexLogic, 
                                 childView = self.resultView,
                                 childLogic=self.baseLogic,
                                 buffer=self.result_buffer,
                                 parentLogic=self)

        self.nsrView  = NsrView( self.Product, self.nsrLogic,  
                                 childView = self.atexView,
                                 childLogic=self.atexLogic,
                                 buffer=self.result_buffer)

        self.mrlView  = MrlView( self.Product, self.mrlLogic,  
                                 childView = self.nsrView,
                                 childLogic=self.nsrLogic,
                                 buffer=self.result_buffer)

        self.roleView = RoleView(self.Product, self.baseLogic,           
                                 childView = self.mrlView,
                                 childLogic=self.mrlLogic,
                                 buffer=self.result_buffer)



    def atexTest(self):
        self.atexView.startYesNoQuestions(self.atexLogic.QA)


    def mrlTest(self):
        self.mrlView.startYesNoQuestions(self.mrlLogic.QA)


    def nsrTest(self):
        self.nsrView.startYesNoQuestions(self.nsrLogic.QA)

    def start(self):
        self.loadLogicEngines()
        self.loadViews()
        self.getUserRole()


if __name__ == '__main__':
    jparser = jPARSER()
    data=jparser.parse('/home/me/Dropbox/Alles_fuer_die_Uni/Master/0_Study-Project/git/lawtexts/MAIN/machines/machinestestM.json')
    m = MainLogic(machineData=data, 
                filePath='/home/me/Dropbox/Alles_fuer_die_Uni/Master/0_Study-Project/git/lawtexts/MAIN/machines/testM.html')
    m.start()