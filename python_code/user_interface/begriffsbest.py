#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np 
import csv 

class Directive():
	def __init__(self, name, key):
		self.name = name
		self.key = key


class Definition():
	def __init__(self, name, key, definition, directive, synonyms = None):
		self.name = name
		self.key = key 
		self.definition = definition
		self.directive = directive
		self.synonyms = synonyms


class Purpose():
	def __init__(self, purpose_text, directive, tag = '+'):
		self.purpose_text = purpose_text
		self. directive = directive
		self.tag = tag



def getBegriffe():	
	f_name = 'begriffsklaerung.csv'
	f = open(f_name)

	reader = csv.reader(f)


	begriffe = dict()

	directives = {}
	directives['9. ProdSV'] =  Directive('Maschinenverordnung','9. ProdSV')
	directives['2009/104/EG'] =  Directive('Betriebssicherheitsverordnung','2009/104/EG')
	directives['94/9/EG'] =    Directive('ATEX','94/9/EG')
	directives['2014/68/EU'] = Directive('Druckgeräte Norm','2014/68/EU')
	directives['2014/35/EU'] = Directive('Niederspannungsrichtlinie','2014/35/EU')
	directives['2014/30/EU'] = Directive('Elektromagnetische Verträglichkeit','2014/30/EU')

	for ix,row in enumerate(reader):
		#row = [r.encode('latin-1') for r in row]
		if ix == 0:
			continue
		name_string = '{0} ({1})'.format(row[0].strip(),row[3].strip())
		begriffe[name_string] =  Definition(row[0],row[0],row[1],directives[row[3].strip()])

	return begriffe