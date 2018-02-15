import re
from pprint import pprint as print 
import numpy as np 


class PARSER():

	def __init__(self):
		pass

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
		primaries = ['class="ti-art">']
		primaryExtractor = '[\d]+</p>'
		pStart = 0
		pEnd = -4

		secondaries = ['<p class="normal">\([\d]+\)']
		secondaryExtractor = '\([\d]+\)'
		sStart = 1
		sEnd = None

		D = {}
		primarySplit = self._split(textList,
								   primaries,
								   primaryExtractor, 
								   pStart, 
								   pEnd)

		for item in primarySplit.items():
			pKey = item[0]
			pContent = item[1]
			D[pKey] = {}
			if pKey == '_':
				D[pKey] = pContent
			else:
				secondarySplit = self._split(pContent,
											 secondaries,
											 secondaryExtractor,
											 sStart, 
											 sEnd)
				D[pKey] = secondarySplit
		return D


	def parseAppendices(self, textList):
		primaries = ['<p class="doc-ti" id="d1e3']
		primaryExtractor = '>.+</p>'
		pStart = 8
		pEnd = -4

		secondaries = ['<p class="ti-grseq-1".+>\d\.[ ]']
		secondaryExtractor = '>((\d\.){1,1}|[A-Z]\.)[ ]'
		sStart = 1
		sEnd = 3

		tertiaries = ['<p class="ti-grseq-1".+>((\d\.){2,2}|[A-Z]\.)[ ]+']
		tertiaryExtractor = '((\d\.){2,2}  |">[A-Z]\.)[ ]'
		tStart = 2
		tEnd = 4

		quaternaries = ['<p class="ti-grseq-1".+>(\d\.){3,3}[ ]+']
		quaternaryExtractor = '>(\d\.){3,3}[ ]'
		qStart = 5
		qEnd = 7

		D = {}
		primarySplit = self._split(textList,
								   primaries,
								   primaryExtractor, 
								   pStart, 
								   pEnd)

		for item in primarySplit.items():
			pKey = item[0]
			pContent = item[1]
			D[pKey] = {}
			if pKey == '_':
				D[pKey] = pContent
			else:
				secondarySplit = self._split(pContent,
											 secondaries,
											 secondaryExtractor,
											 sStart, 
											 sEnd)

				for stem in secondarySplit.items():
					sKey = stem[0]
					sContent = stem[1]
					D[pKey][sKey] = {}
					if sKey == '_':
						D[pKey][sKey] = sContent
					else:
						tertiarySplit = self._split(sContent,
													 tertiaries,
													 tertiaryExtractor,
													 tStart, 
													 tEnd)

						for ttem in tertiarySplit.items():
							tKey = ttem[0]
							tContent = ttem[1]
							D[pKey][sKey][tKey] = {}
							if tKey == '_':
								D[pKey][sKey][tKey] = tContent
							else:
								quaternarySplit = self._split(tContent,
															 quaternaries,
															 quaternaryExtractor,
															 qStart, 
															 qEnd)
								D[pKey][sKey][tKey] = quaternarySplit
		return D
