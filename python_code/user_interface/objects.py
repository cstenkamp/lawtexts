import numpy as np 
import csv
from pprint import pprint as print


class Directive():
	def __init__(self, name):
		self.name = name

class Machine():
	def __init__(self, title, purpose, siteOfOperation, properties, valuedProperties):
		self.title = title
		self.purpose = purpose
		self.siteOfOperation = siteOfOperation
		self.properties = {}
		for prop in properties:
			self.properties[prop.title] = prop 
		self.valuedProperties = {}
		for prop in valuedProperties:
			self.valuedProperties[prop.title] = prop


class Property():
	def __init__(self, title, listOfDirectivesIncluded, listOfDirectivesExcluded):
		self.title = title
		self.including_directives = {}
		for directive in listOfDirectivesIncluded:
			self.including_directives[directive] = Directive(directive)
		self.excluding_directives = {}
		for directive in listOfDirectivesExcluded:
			self.excluding_directives[directive] = Directive(directive)

class ValuedProperty(Property):
	def __init__(self, title, listOfDirectivesIncluded, listOfDirectivesExcluded):
		super(ValuedProperty, self).__init__(title, listOfDirectivesIncluded, listOfDirectivesExcluded)
		self.value = value 

class Purpose(Property):
	def __init__(self, title, listOfDirectivesIncluded, listOfDirectivesExcluded):
		super(Purpose, self).__init__(title, listOfDirectivesIncluded, listOfDirectivesExcluded)

class SiteOfOperation(Property):
	def __init__(self, title, listOfDirectivesIncluded, listOfDirectivesExcluded):
		super(SiteOfOperation, self).__init__(title, listOfDirectivesIncluded, listOfDirectivesExcluded)

def loadCSV(f_name = 'verwendungsorte.csv'):
	sites = {}
	reader = open(f_name)
	for row in reader:
		if row == []:
			return sites
		row = row.strip().split(',')
		row = [r.strip() for r in row]
		siteTitle = row[0]
		directives = row[1:]
		directives = [d.strip() for d in directives if not d == '']
		listOfDirectivesIncluded = []
		listOfDirectivesExcluded = []
		for d in directives:
			flag = d[0]
			directiveCode = d[1:].strip()
			if flag == '+':
				listOfDirectivesIncluded.append(directiveCode)
			elif flag == '-':
				listOfDirectivesExcluded.append(directiveCode)
		sites[siteTitle] = SiteOfOperation(siteTitle, listOfDirectivesIncluded, listOfDirectivesExcluded)
	return sites




if __name__ == '__main__':
	f_name = 'verwendungszwecke.csv'
	purposes = loadCSV(f_name)
	f_name = 'verwendungsorte.csv'
	sites = loadCSV(f_name)