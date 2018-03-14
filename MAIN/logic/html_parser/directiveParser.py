#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import numpy as np 
import os, sys


class PARSER():

	def __init__(self):

		self.primariesArt = ['class="ti-art">']
		self.primaryExtractorArt = '[\d]+</p>'
		self.pStartArt = 0
		self.pEndArt = -4

		self.secondariesArt = ['<p class="normal">\([\d]+\)']
		self.secondaryExtractorArt = '\([\d]+\)'
		self.sStartArt = 1
		self.sEndArt = None

		
		self.primaries = ['<p class="doc-ti" id="d1e3']
		self.primaryExtractor = '>.+</p>'
		self.pStart = 8
		self.pEnd = -4

		self.secondaries = ['<p class="ti-grseq-1".+>\d\.[ ]']
		self.secondaryExtractor = '>((\d\.){1,1}|[A-Z]\.)[ ]'
		self.sStart = 1
		self.sEnd = 3

		self.tertiaries = ['<p class="ti-grseq-1".+>((\d\.){2,2}|[A-Z]\.)[ ]+']
		self.tertiaryExtractor = '((\d\.){2,2}  |">[A-Z]\.)[ ]'
		self.tStart = 2
		self.tEnd = 4

		self.quaternaries = ['<p class="ti-grseq-1".+>(\d\.){3,3}[ ]+']
		self.quaternaryExtractor = '>(\d\.){3,3}[ ]'
		self.qStart = 5
		self.qEnd = 7

		self.path = os.path.join(os.path.split(os.getcwd())[0],'logic/html_resources/directives')

		self.parse()



	def getHtml(self,p='html_resources/directives/mrl.html'):
		with open(p) as f:
			text = list(map(lambda x: x.strip(), f.readlines()))
		return text

	def _split(self, textList, splitAlong, extractKeys, stringStart, stringEnd):
		D = {}
		buffer = []
		key = '_'
		# go line by line
		for line in textList:
			for p in splitAlong:
				m = re.search(p,line)
			if not m is None:
				D[key] = buffer
				buffer = []
				key = re.search(extractKeys,line).group(0)[stringStart:stringEnd].lower()
			buffer.append(line)
		D[key] = buffer
		return D

	def parseArticles(self, textList):

		D = {}
		primarySplit = self._split(textList,
								   self.primariesArt,
								   self.primaryExtractorArt, 
								   self.pStartArt, 
								   self.pEndArt)

		for item in primarySplit.items():
			pKey = item[0]
			pContent = item[1]
			D[pKey] = {}
			if pKey == '_':
				D[pKey] = pContent
			else:
				secondarySplit = self._split(pContent,
											 self.secondariesArt,
											 self.secondaryExtractorArt,
											 self.sStartArt, 
											 self.sEndArt)
				D[pKey] = secondarySplit
		return D


	def parseAppendices(self, textList):

		D = {}
		primarySplit = self._split(textList,
								   self.primaries,
								   self.primaryExtractor, 
								   self.pStart, 
								   self.pEnd)

		for item in primarySplit.items():
			pKey = item[0]
			pContent = item[1]
			D[pKey] = {}
			if pKey == '_':
				D[pKey] = pContent
			else:
				secondarySplit = self._split(pContent,
											 self.secondaries,
											 self.secondaryExtractor,
											 self.sStart, 
											 self.sEnd)

				for stem in secondarySplit.items():
					sKey = stem[0]
					sContent = stem[1]
					D[pKey][sKey] = {}
					if sKey == '_':
						D[pKey][sKey] = sContent
					else:
						tertiarySplit = self._split(sContent,
													 self.tertiaries,
													 self.tertiaryExtractor,
													 self.tStart, 
													 self.tEnd)

						for ttem in tertiarySplit.items():
							tKey = ttem[0]
							tContent = ttem[1]
							D[pKey][sKey][tKey] = {}
							if tKey == '_':
								D[pKey][sKey][tKey] = tContent
							else:
								quaternarySplit = self._split(tContent,
															 self.quaternaries,
															 self.quaternaryExtractor,
															 self.qStart, 
															 self.qEnd)
								D[pKey][sKey][tKey] = quaternarySplit
		return D

	def parse(self):
		self.parseMRL()
		self.parseNSR()
		self.parseATEX()


		self.articles = {'MRL':self.mrlArticle,
				   	'NSR':self.nsrArticle,
				   	'ATEX':self.atexArticle
				   }
		self.appendices = {'MRL':self.mrlAppendices,
					  'NSR':self.nsrAppendices,
					  'ATEX':self.atexAppendices
					 }

					 

	def parseMRL(self):
		# parse MRL into articles and appendices
		p = os.path.join(self.path,'mrl.html')
		text = self.getHtml(p=p)
		self.mrlArticle = self.parseArticles(text)
		self.mrlAppendices = self.parseAppendices(text)

	def parseNSR(self):
		# parse MRL into articles and appendices
		p = os.path.join(self.path,'nsr.html')
		text = self.getHtml(p=p)
		self.nsrArticle = self.parseArticles(text)
		self.nsrAppendices = self.parseAppendices(text)

	def parseATEX(self):
		self.secondaries = ['<p class="ti-grseq-1".+>\d\.[^\d]']
		self.secondaryExtractor = '>((\d\.){1,1}|[A-Z]\.)'

		self.tertiaries = ['<p class="ti-grseq-1".+>(\d\.){2,2}[^\d].*<spa']
		self.tertiaryExtractor = '((\d\.){2,2})'

		self.quaternaries = ['<p class="ti-grseq-1".+>(\d\.){3,3}[^\d].*<spa']
		self.quaternaryExtractor = '((\d\.){3,3})'

		self.qStart = 4
		self.qEnd = 6

		p = os.path.join(self.path,'atex.html')
		text = self.getHtml(p=p)
		self.atexArticle = self.parseArticles(text)
		self.atexAppendices = self.parseAppendices(text)