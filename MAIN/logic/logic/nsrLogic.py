#!/usr/bin/env python
# -*- coding: utf-8 -*-
from baseLogic import BaseLogic
from question import Question 


class NsrLogic(BaseLogic):
    def __init__(self, Product, dictParser, name='NSR'):
        super(NsrLogic,self).__init__(Product, dictParser, name)
        self.initQuestions()

        self.ac_high = 1000
        self.ac_low  = 50

        self.dc_high = 1000
        self.dc_low  = 50


    def checkVoltage(self, val, type):
        type = type.lower()
        if type == 'ac':
            if self.ac_low < val < self.ac_high:
                return True
            else:
                return False
        elif type == 'dc':
            if self.dc_low < val < self.dc_high:
                return True
            else:
                return False
        else:
            print('wrong voltage type. Must either be "ac" or "dc"')



    def getRoleDuties(self):
        self.roleDuties = '<h2> Durch ihre Rolle als {0} obliegen ihnen folgende Pflichten: </h2>'.format(self.Product.role)
        if self.Product.role == 'Hersteller':
            self.roleDuties += self.dictParser.labelToHtml('artikel_6',self.name)
        if self.Product.role == 'Bevollmächtigter':
            self.roleDuties += self.dictParser.labelToHtml('artikel_7',self.name)
        if self.Product.role == 'Einführer':
            self.roleDuties += self.dictParser.labelToHtml('artikel_8',self.name)
        if self.Product.role == 'Händler':
            self.roleDuties += self.dictParser.labelToHtml('artikel_9',self.name)
        if self.Product.extraDuties:
            self.roleDuties = '''<h3>Dadurch, dass Sie das Produkt unter 
                                     eigenem Namen oder unter eigener Handelsmarke 
                                     in Verkehr bringen, oder das Produkt so verändern,
                                     dass die Konformität mit dieser Richtlinie 
                                     beeinträchtigt wird</h3>'''
            self.roleDuties += self.dictParser.labelToHtml('artikel_6',self.name)
        return self.roleDuties


    def initQuestions(self):
        tmp = self.dictParser.labelToHtml('anhang_ii',self.name)
        tmp = tmp[tmp.index('"normal">')+9:]
        tmp = '<h2>Finden Sie das Produkt in dieser Liste wieder?</h2>\n'+tmp
        self.QA = Question(tmp,
                      effect={'y':False,
                              'n':True})
