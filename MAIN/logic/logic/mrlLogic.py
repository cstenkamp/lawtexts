#!/usr/bin/env python
# -*- coding: utf-8 -*-
from baseLogic import BaseLogic
from question import Question 


class MrlLogic(BaseLogic):
    def __init__(self, Product, dictParser, name='MRL'):
        super(MrlLogic,self).__init__(Product, dictParser, name)


    def setRole(self,role):
        self.Product.role = role 

    def setState(self,B):
        self.state=B

    def setType(self,B):
        self.type=B

    def setHarmonized(self,B):
        self.Product.harmonized=B


    def getRoleDuties(self):
        if self.Product.role == 'Hersteller':
            self.roleDuties = '<h2> In ihrer Rolle als {0} obliegen ihnen folgende Pflichten: </h2>'.format(self.Product.role)
            self.roleDuties += self.dictParser.labelToHtml('artikel_5',self.name)
        elif self.Product.extraDuties:
            self.roleDuties = '''<h2>Dadurch, dass Sie das Produkt unter 
                                     eigenem Namen oder unter eigener Handelsmarke 
                                     in Verkehr bringen, oder das Produkt so verändern,
                                     dass die Konformität mit dieser Richtlinie 
                                     beeinträchtigt wird, obliegen ihnen in ihrer Rolle als {0} folgende Pflichten</h2>'''.format(self.Product.role)
            self.roleDuties += self.dictParser.labelToHtml('artikel_5',self.name)
        else:
            self.roleDuties = '<h2> In ihrer Rolle als {0} obliegen ihnen keine weiteren Pflichten.</h2>'.format(self.Product.role)



    def getTypeDuties(self):
        if self.type == 'unvollst':
            self.Product.typeDuties = self.dictParser.labelToHtml('artikel_13',self.name)
        elif self.type == 'vollst':
            self.Product.typeDuties = self.dictParser.labelToHtml('artikel_12',self.name)


    def getHarmDuties(self):
        if self.Product.harmonized:
            self.harmDuties = '<h2> Da die Maschine nach einer harmonisierten Norm hergestellt wurde </h2>'
            self.harmDuties += self.dictParser.labelToHtml('artikel_7',self.name)

    def finalize(self):
        if self.state:
            self.html = '<h1>MRL</h1>'       
            if not self.Product.harmonized:
                if (self.Product.role == 'Hersteller') or (self.Product.extraDuties):
                    self.getRoleDuties()    
                    self.html += self.roleDuties
                    self.getTypeDuties()
                    self.html += self.Product.typeDuties
                else:
                    self.getRoleDuties()    
                    self.html += self.roleDuties
            else:
                self.getHarmDuties()
                self.html = '<h1>MRL</h1>'       
                self.html += self.harmDuties
        else:
            self.html = '<h1>MRL trifft nicht zu!</h1>'
        return self.html 


    def initQuestions(self):
        tmp = self.dictParser.labelToHtml('artikel_1_1)',self.name)
        tmp = tmp[tmp.index(':</p>')+5:]
        tmp = '<h2>Finden Sie das Produkt in dieser Liste wieder?</h2>\n'+tmp
        self.QA = Question(tmp,
                           effect={'y':True,
                                   'n':False})

        tmp = self.dictParser.labelToHtml('artikel_1_2)',self.name)
        tmp = tmp[tmp.index(':</p>')+5:]
        tmp = '<h2>Finden Sie das Produkt in dieser Liste wieder?</h2>\n'+tmp
        self.QB = Question(tmp,
                           effect={'y':False,
                                   'n':True})

        self.QA.posChild = self.QB 


        self.QC = Question('<h2>Handel es sich bei dem Produkt um eine unvollständige Maschine?</h2>',
                           effect={'y':'unvollst',
                                   'n':'vollst'})


        self.QB.negChild = self.QC 


        self.QD = Question('<h2>Wurde die Maschine nach einer harmonisierten Norm hergestellt?</h2>',
                           effect={'y':'harm',
                                   'n':'nichtHarm'})


        self.QC.negChild = self.QD 
        self.QC.posChild = self.QD 

