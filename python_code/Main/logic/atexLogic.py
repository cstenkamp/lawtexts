import json
import re
import sys

from jsonParser import PARSER 

from atexTree import Test, Questions

purposesPath = 'json/_purposes.json'
sitesPath = 'json/_sites.json'
partsPath = 'json/parts.json'
featuresPath = 'json/features.json'



class ATEX():
	def __init__(self, Product, dictParser):
		self.Product = Product
		self.dictParser = dictParser

		'''
		load json files
		'''
		jParser = PARSER()
		self.features = jParser.parse('json/features.json')
		self.parts = jParser.parse('json/parts.json')
		self.sites = jParser.parse('json/_sites.json')
		self.purposes = jParser.parse('json/_purposes.json')

		self.role = None 
		self.roleDuties = None

		self.tree = Test()
		self.questions = Questions()
		self.effects = None
		self.gcEffects = {'all':[],
						  'one':[],
						  'or':[],
						  'special':[]}


	def setUserRole(self,role,extraDuties=False):
		'''
		Interface asks user to identify their status/role
		'''
		self.role = role 
		self.roleDuties = '<h2> Durch ihre Rolle als {0} obliegen ihnen folgende Pflichten: </h2>'.format(role)
		if role == 'Hersteller':
			self.roleDuties += self.dictParser.labelToHtml('artikel_6','ATEX')
		if role == 'Bevollmächtigter':
			self.roleDuties += self.dictParser.labelToHtml('artikel_7','ATEX')
		if role == 'Einführer':
			self.roleDuties += self.dictParser.labelToHtml('artikel_8','ATEX')
		if role == 'Händler':
			self.roleDuties += self.dictParser.labelToHtml('artikel_9','ATEX')
		if extraDuties:
			self.roleDuties += '<h2> In diesem Falle zusätzlich: </h2>'.format(role)
			self.roleDuties += self.dictParser.labelToHtml('artikel_6','ATEX')


	def getGroupAndCategory(self, effects=None):
		if effects is None:
			self.effects = self.tree.start(self.questions.Q0)
		else:
			self.effects = effects

		for E in self.effects:
			if E[0] == 'Schutzsystem':
				self.gcEffects['all'].append(self.dictParser.labelToHtml('Anhang_III','ATEX'))
				self.gcEffects['one'].append([self.dictParser.labelToHtml('Anhang_vi','ATEX'),
											  self.dictParser.labelToHtml('Anhang_vii','ATEX')])
				self.gcEffects['or'] = self.dictParser.labelToHtml('Anhang_IX','ATEX')
				break

			if E[0].startswith('Gerätegruppe'):
				self.gcEffects['or'] = self.dictParser.labelToHtml('Anhang_IX','ATEX')

			if (E[0] == 'Gerätekategorie M 1') or (E[0] == 'Gerätekategorie 1'):
				self.gcEffects['all'].append(self.dictParser.labelToHtml('Anhang_III','ATEX'))
				self.gcEffects['one'].append([self.dictParser.labelToHtml('Anhang_vi','ATEX'),
											  self.dictParser.labelToHtml('Anhang_vii','ATEX')])

			if E[0] == 'motor':
				self.gcEffects['one'].append([self.dictParser.labelToHtml('Anhang_vi','ATEX'),
											  self.dictParser.labelToHtml('Anhang_vii','ATEX')])
				self.gcEffects['all'].append(self.dictParser.labelToHtml('Anhang_iii','ATEX'))

			if E[0] == 'noMotor':
				self.gcEffects['all'].append( '<h4>Die technischen Unterlagen gemäß Anhang VIII Nummer 2 sind einer notifizierten Stelle zu übermitteln, die den Erhalt dieser Unterlagen unverzüglich bestätigt und sie aufbewahrt;<\h4>\n'+
											  self.dictParser.labelToHtml('Anhang_viii','ATEX'))
				


			if E[0] == 'Gerätekategorie M 1':
				self.gcEffects['special'].append(self.dictParser.labelToHtml('Anhang_II_2._0._1.','ATEX'))

			if E[0] == 'Gerätekategorie M 2':
				self.gcEffects['special'].append(self.dictParser.labelToHtml('Anhang_II_2._0._2.','ATEX'))

			if E[0] == 'Gerätekategorie 1':
				self.gcEffects['special'].append(self.dictParser.labelToHtml('Anhang_II_2._1.','ATEX'))

			if E[0] == 'Gerätekategorie 2':
				self.gcEffects['special'].append(self.dictParser.labelToHtml('Anhang_II_2._2.','ATEX'))

			if E[0] == 'Gerätekategorie 3':
				self.gcEffects['all'].append(self.dictParser.labelToHtml('Anhang_III','ATEX'))
				self.gcEffects['special'].append(self.dictParser.labelToHtml('Anhang_II_2._3.','ATEX'))
		
		return self.effects


	def formatOutput(self):
		html = '<h1>ATEX</h1>'
		html += self.roleDuties
		if (self.role == 'Hersteller') or self.extraDuties:
			html += '<h1> Pflichten der Hersteller</h1>'
			html += '<h2> und unter bestimmten Umständen der Einführer und Händler</h2>'
			if not self.gcEffects['all'] == []:
				html += '<h2>Diese Regelungen müssen unbedingt eingehalten werden: </h2>\n'
			for item in self.gcEffects['all']:
				html += item

			for item in self.gcEffects['one']:
				html += '<h2>Eines der Folgenden Verfahren muss gewählt werden</h2>\n'
				for subItem in item:
					html += subItem

			if not self.gcEffects['or'] == []:
				html += '<h2>Die oben genannten Verfahren können allerdings auch durch folgendes ersetzt werden: </h2>\n'
			for item in self.gcEffects['or']:
				html += item

			if not self.gcEffects['special'] == []:
				html += '<h2>Desweiteren gelten folgende spezielle Regelungen für das Produkt: </h2>\n'
			for item in self.gcEffects['special']:
				html += item

			html += '<h2>Komponenten</h2>'
			html += 'Die oben genannten Verfahren finden Anwendung bei Komponenten mit Ausnahme der Anbringung der CE-Kennzeichnung und der Ausstellung der EU-Konformitätserklärung. Der Hersteller muss eine schriftliche Konformitätsbescheinigung ausstellen, durch die die Konformität der Komponenten mit den anwendbaren Bestimmungen dieser Richtlinie erklärt wird und aus der die Merkmale dieser Komponenten sowie die Bedingungen für ihren Einbau in Geräte und Schutzsysteme zu ersehen sind, die dazu beitragen, dass die für fertiggestellte Geräte und Schutzsysteme geltenden wesentlichen Gesundheits- und Sicherheitsanforderungen gemäß Anhang II erfüllt werden.\n'
			html += 'In Bezug auf die in Anhang II Nummer 1.2.7 genannten Sicherheitsaspekte kann zusätzlich zu den oben genannten Konformitätsbewertungsverfahren das Verfahren gemäß Anhang VIII ebenfalls angewendet werden.\n'
			html += 'Die zuständigen Behörden können auf hinreichend begründeten Antrag das Inverkehrbringen und die Inbetriebnahme von Produkten, die keine Komponenten sind, auf dem Hoheitsgebiet des betroffenen Mitgliedstaats genehmigen, auf die die oben genannten Verfahren nicht angewandt worden sind und deren Verwendung im Interesse des Schutzes geboten ist.'
			html += 'Die Unterlagen und der Schriftwechsel betreffend die Konformitätsbewertungsverfahren werden in einer von dem betreffenden Mitgliedstaat festgelegten Sprache abgefasst.'
		return html 



	def formatOutput2(self):
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

		html = '<h3>Konformitätsbewertungsverfahren</h3>'
		for e in self.effects:
			if e[0] == 'Schutzsystem':
				html += '<h4>Bei dem Produkt handelt es sich um ein Schutzsystem</h4>'
				html += 'Für Schutzsysteme ist die Konformitätsbewertung nach dem in Artikel 13 Absatz 1 Buchstabe a oder d genannten Verfahren durchzuführen.'
				
			elif (e[0] == 'Gerätekategorie M 1') or (e[0] == 'Gerätekategorie 1'):
				html += '<h4>Bei dem Produkt handelt es sich um ein Gerät der {0} und {1} </h4>'.format(group,cat)
				html += 'Für Gerätegruppen I und II, Gerätekategorie M 1 und 1 ist die EU-Baumusterprüfung gemäß Anhang III anzuwenden, und zwar in Verbindung mit einem von Folgendem:<br />    — Konformität mit dem Baumuster auf der Grundlage einer Qualitätssicherung bezogen auf den Produktionsprozess gemäß Anhang IV,<br />    —Konformität mit dem Baumuster auf der Grundlage einer Prüfung der Produkte gemäß Anhang V;'
			
			elif (e[0] == 'motor'):
				html += '<h4>Bei dem Produkt handelt es sich um ein Gerät der {0} und {1}, ausgestattet mit einem Verbrennungsmotor oder elektrisch betrieben.</h4>'.format(group,cat)
				html += 'Für Motoren mit innerer Verbrennung und für elektrische Geräte dieser Gruppen und Kategorien ist die EU-Baumusterprüfung gemäß Anhang III anzuwenden, und zwar in Verbindung mit einem von Folgendem:<br />   — Konformität mit dem Baumuster auf der Grundlage einer internen Fertigungskontrolle mit überwachten Produktprüfungen gemäß Anhang VI,<br />    — Konformität mit dem Baumuster auf der Grundlage der Qualitätssicherung bezogen auf das Produkt gemäß Anhang VII'
			
			elif (e[0] == 'noMotor'):
				html += '<h4>Bei dem Produkt handelt es sich um ein Gerät der {0} und {1}</h4>'.format(group,cat)
				html += 'für Geräte dieser Gruppen und Kategorien ist die interne Fertigungskontrolle gemäß Anhang VIII anzuwenden, und die technischen Unterlagen gemäß Anhang VIII Nummer 2 sind einer notifizierten Stelle zu übermitteln, die den Erhalt dieser Unterlagen unverzüglich bestätigt und sie aufbewahrt;'

			elif (e[0] == 'Gerätekategorie 3'):
				html += '<h4>Bei dem Produkt handelt es sich um ein Gerät der {0} und {1}</h4>'.format(group,cat)
				html += 'für Gerätegruppe II, Gerätekategorie 3 ist die interne Fertigungskontrolle gemäß Anhang VIII anzuwenden;'

		header  = '<h1>ATEX</h1>'
		html = header+self.roleDuties+html
		html += '<h4>Komponenten</h4>'
		html += 'Die oben genannten Verfahren finden Anwendung bei Komponenten mit Ausnahme der Anbringung der CE-Kennzeichnung und der Ausstellung der EU-Konformitätserklärung. Der Hersteller muss eine schriftliche Konformitätsbescheinigung ausstellen, durch die die Konformität der Komponenten mit den anwendbaren Bestimmungen dieser Richtlinie erklärt wird und aus der die Merkmale dieser Komponenten sowie die Bedingungen für ihren Einbau in Geräte und Schutzsysteme zu ersehen sind, die dazu beitragen, dass die für fertiggestellte Geräte und Schutzsysteme geltenden wesentlichen Gesundheits- und Sicherheitsanforderungen gemäß Anhang II erfüllt werden.<br \>'
		html += 'In Bezug auf die in Anhang II Nummer 1.2.7 genannten Sicherheitsaspekte kann zusätzlich zu den oben genannten Konformitätsbewertungsverfahren das Verfahren gemäß Anhang VIII ebenfalls angewendet werden.<br \>'
		html += 'Die zuständigen Behörden können auf hinreichend begründeten Antrag das Inverkehrbringen und die Inbetriebnahme von Produkten, die keine Komponenten sind, auf dem Hoheitsgebiet des betroffenen Mitgliedstaats genehmigen, auf die die oben genannten Verfahren nicht angewandt worden sind und deren Verwendung im Interesse des Schutzes geboten ist.<br \>'
		html += 'Die Unterlagen und der Schriftwechsel betreffend die Konformitätsbewertungsverfahren werden in einer von dem betreffenden Mitgliedstaat festgelegten Sprache abgefasst.<br \>'
		return html