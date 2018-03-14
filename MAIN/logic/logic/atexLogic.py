#!/usr/bin/env python
# -*- coding: utf-8 -*-
from baseLogic import BaseLogic
from question import Question 


class AtexLogic(BaseLogic):
    def __init__(self, Product, dictParser, name='ATEX'):
        super(AtexLogic,self).__init__(Product, dictParser, name)
        self.initQuestions()

        self.effects = []
        self.gcEffects = {'all':[],
                          'one':[],
                          'or':[]}

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



    def finalize(self):
        self.getRoleDuties()
        if not self.state:
            self.html = '<h1>ATEX trifft nicht zu!</h1>'
            return self.html

        if self.effects == None:
            return False

        cat = None
        group = None
        motor = None
        for e in self.effects:
            if e[0].startswith('Gerätekategorie'):
                cat = e[0]
            if e[0].startswith('Gerätegruppe'):
                group = e[0]
            if e[0].startswith('motor'):
                motor = 'mit'
            if e[0].startswith('noMotor'):
                motor = 'ohne'

        self.html = '<h3>Konformitätsbewertungsverfahren</h3>'
        for e in self.effects:
            if e[0] == 'Schutzsystem':
                self.html += '<h4>Bei dem Produkt handelt es sich um ein Schutzsystem</h4>'
                self.html += 'Für Schutzsysteme ist die Konformitätsbewertung nach dem in Artikel 13 Absatz 1 Buchstabe a oder d genannten Verfahren durchzuführen.'
                
            elif (e[0] == 'Gerätekategorie M 1') or (e[0] == 'Gerätekategorie 1'):
                self.html += '<h4>Bei dem Produkt handelt es sich um ein Gerät der {0} und {1} </h4>'.format(group,cat)
                self.html += 'Für Gerätegruppen I und II, Gerätekategorie M 1 und 1 ist die EU-Baumusterprüfung gemäß Anhang III anzuwenden, und zwar in Verbindung mit einem von Folgendem:<br />    — Konformität mit dem Baumuster auf der Grundlage einer Qualitätssicherung bezogen auf den Produktionsprozess gemäß Anhang IV,<br />    —Konformität mit dem Baumuster auf der Grundlage einer Prüfung der Produkte gemäß Anhang V;'
            
            elif (e[0] == 'motor'):
                self.html += '<h4>Bei dem Produkt handelt es sich um ein Gerät der {0} und {1}, ausgestattet mit einem Verbrennungsmotor oder elektrisch betrieben.</h4>'.format(group,cat)
                self.html += 'Für Motoren mit innerer Verbrennung und für elektrische Geräte dieser Gruppen und Kategorien ist die EU-Baumusterprüfung gemäß Anhang III anzuwenden, und zwar in Verbindung mit einem von Folgendem:<br />   — Konformität mit dem Baumuster auf der Grundlage einer internen Fertigungskontrolle mit überwachten Produktprüfungen gemäß Anhang VI,<br />    — Konformität mit dem Baumuster auf der Grundlage der Qualitätssicherung bezogen auf das Produkt gemäß Anhang VII'
            
            elif (e[0] == 'noMotor'):
                self.html += '<h4>Bei dem Produkt handelt es sich um ein Gerät der {0} und {1}</h4>'.format(group,cat)
                self.html += 'für Geräte dieser Gruppen und Kategorien ist die interne Fertigungskontrolle gemäß Anhang VIII anzuwenden, und die technischen Unterlagen gemäß Anhang VIII Nummer 2 sind einer notifizierten Stelle zu übermitteln, die den Erhalt dieser Unterlagen unverzüglich bestätigt und sie aufbewahrt;'

            elif (e[0] == 'Gerätekategorie 3'):
                self.html += '<h4>Bei dem Produkt handelt es sich um ein Gerät der {0} und {1}</h4>'.format(group,cat)
                self.html += 'für Gerätegruppe II, Gerätekategorie 3 ist die interne Fertigungskontrolle gemäß Anhang VIII anzuwenden;'

        header  = '<h1>ATEX</h1>'
        self.html = header+self.roleDuties+self.html
        self.html += '<h4>Komponenten</h4>'
        self.html += 'Die oben genannten Verfahren finden Anwendung bei Komponenten mit Ausnahme der Anbringung der CE-Kennzeichnung und der Ausstellung der EU-Konformitätserklärung. Der Hersteller muss eine schriftliche Konformitätsbescheinigung ausstellen, durch die die Konformität der Komponenten mit den anwendbaren Bestimmungen dieser Richtlinie erklärt wird und aus der die Merkmale dieser Komponenten sowie die Bedingungen für ihren Einbau in Geräte und Schutzsysteme zu ersehen sind, die dazu beitragen, dass die für fertiggestellte Geräte und Schutzsysteme geltenden wesentlichen Gesundheits- und Sicherheitsanforderungen gemäß Anhang II erfüllt werden.<br \>'
        self.html += 'In Bezug auf die in Anhang II Nummer 1.2.7 genannten Sicherheitsaspekte kann zusätzlich zu den oben genannten Konformitätsbewertungsverfahren das Verfahren gemäß Anhang VIII ebenfalls angewendet werden.<br \>'
        self.html += 'Die zuständigen Behörden können auf hinreichend begründeten Antrag das Inverkehrbringen und die Inbetriebnahme von Produkten, die keine Komponenten sind, auf dem Hoheitsgebiet des betroffenen Mitgliedstaats genehmigen, auf die die oben genannten Verfahren nicht angewandt worden sind und deren Verwendung im Interesse des Schutzes geboten ist.<br \>'
        self.html += 'Die Unterlagen und der Schriftwechsel betreffend die Konformitätsbewertungsverfahren werden in einer von dem betreffenden Mitgliedstaat festgelegten Sprache abgefasst.<br \>'
        return self.html


    def initQuestions(self):

        self.QD = Question('Produkt wird unter eigenem Namen oder unter eigener Handelsmarke in Verkehr gebracht, oder Produkt wird vor in Verkehr bringen so verändert, dass die Konformität mit dieser Richtlinie beeinträchtigt wird?',
                      effect={'y':'extra',
                              'n':'None'})


        tmp = self.dictParser.labelToHtml('artikel_1_1)','ATEX')
        tmp = tmp[tmp.index('/p>')+3:]
        tmp = '<h2>Finden Sie das Produkt in dieser Liste wieder?</h2>\n'+tmp
        self.QA = Question(tmp,
                      effect={'y':'None',
                              'n':'False'})

        tmp = self.dictParser.labelToHtml('artikel_1_2)','ATEX')
        tmp = tmp[tmp.index('/p>')+3:]
        tmp = '<h2>Finden Sie das Produkt in dieser Liste wieder?</h2>\n'+tmp
        self.QB = Question(tmp,
                      effect={'y':'False',
                              'n':'True'})

        self.QA.posChild = self.QB



        self.Q0 = Question('Handelt es sich bei dem Produkt um ein Schutzsystem?',
                      effect={'y':'Schutzsystem',
                              'n':'None'})

        self.QB.negChild = self.Q0

        self.Q1 = Question('Gerät ist zur Verwendung in untertägigen Bergwerken sowie deren Übertageanlagen bestimmt, die durch Grubengas und/oder brennbare Stäbe gefährded wird?',
                      effect={'y':'Gerätegruppe I',
                              'n':'Gerätegruppe II'})
        self.Q0.negChild = self.Q1

        self.Q1y = Question('Beinhalten die Geräte zusätzliche Schutzmaßnahmen und sollen selbst in explosionsfähiger Atmosphäre weiter betrieben werden?',
                       effect={'y':'Gerätekategorie M 1',
                               'n':'Gerätekategorie M 2'})
        self.Q1.posChild = self.Q1y


        self.Q1n = Question('Ist damit zu rechnen, dass die Atmosphäre, in der das Gerät betrieben werden soll, explosionsfähig wird?',
                       effect={'y':'None',
                               'n':'Gerätekategorie 3'})
        self.Q1.negChild = self.Q1n


        self.Q2 = Question('Ist eine explosionsfähige Atmosphäre ständig oder häufig vorhanden?',
                       effect={'y':'Gerätekategorie 1',
                               'n':'Gerätekategorie 2'})

        self.Q1n.posChild = self.Q2


        self.Q3 = Question('Handelt es sich um ein Gerät mit Motor mit innerer Verbrennung oder um ein elektrisches Gerät?',
                       effect={'y':'motor',
                               'n':'noMotor'})
        self.Q1y.negChild = self.Q3
        #self.Q2.posChild = self.Q3
        self.Q2.negChild = self.Q3