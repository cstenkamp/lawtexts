import json
import re

purposesPath = 'json/_purposes.json'
sitesPath = 'json/_sites.json'
partsPath = 'json/parts.json'


NSR_ac_high = 1000
NSR_ac_low  = 50

NSR_dc_high = 1000
NSR_dc_low  = 50



class LOGIC():
	def __init__(self, Product, articles, appendices):
		self.Product = Product
		self.kBase = {'Verwendungszwecke':{},
					  'Verwendungsorte':{}}

		self.HTML_Results = {'MRL':[],'NSR':[]}

		self.loadPurposes()
		self.loadSites()
		self.loadParts()

		self.articles = articles
		self.appendices = appendices

	def loadPurposes(self):
		with open(purposesPath) as f:
			self.kBase['Verwendungszwecke'] = json.load(f)

	def loadSites(self):
		with open(sitesPath) as f:
			self.kBase['Verwendungsorte'] = json.load(f)

	def loadParts(self):
		with open(sitesPath) as f:
			self.kBase['Komponenten'] = json.load(f)

	def checkMachineFirstLevel(self):
		P = self.Product
		subject = ['Verwendungszwecke','Verwendungsorte']
		for sj in subject:
			for feature in P.json[sj]:
				if feature in self.kBase[sj]:
					info = self.kBase[sj][feature]
					# check if any directive is directly deactivated by the machines feature
					for dN in ['NSR','MRL']:
						if dN in info['deaktiviert']:
							if ((P.states[dN]['state'] == True) 
								 and (P.states[dN]['rigid_state'] == True)):
								continue
							P.states[dN]['state'] = False
							P.states[dN]['rigid_state'] = True
							P.states[dN]['deactivators'][sj].append(feature)
					# check if any directive is directly activated by the machines feature
					for dN in ['NSR','MRL']:
						if dN in info['aktiviert']:
							if ((P.states[dN]['state'] == False) 
								 and (P.states[dN]['rigid_state'] == True)):
								continue
							P.states[dN]['state'] = True
							P.states[dN]['rigid_state'] = True
							P.states[dN]['activators'][sj].append(feature)

	def checkMachineComponents(self):
		P = self.Product
		for C in P.json['Komponenten'].items():
			for featureName in C[1]:
				if featureName == 'aktiviert Richtlinie':
					for directive in C[1][featureName]:
						P.states[directive]['state'] = True
						P.states[directive]['rigid_state'] = True
						P.states[directive]['activators']['Komponenten'].append(
								[C[0]])


				if featureName == 'Spannung':
					res = self.NSRsingleCheck(C[1][featureName])
					if res:
						# if NSR is activated, but is already hard set false
						if (P.states['NSR']['state'] == False 
								and P.states['NSR']['rigid_state']):
							continue
						else:
							P.states['NSR']['state'] = True
							P.states['NSR']['activators']['Komponenten'].append(
									[C[0],
									 featureName,
									 C[1][featureName]])


	def NSRsingleCheck(self, feature):
		k = list(feature.keys())[0]
		v = list(feature.values())[0]
		if (k == 'Volt AC') and (NSR_ac_low<float(v)<NSR_ac_high):
			return True
		elif (k == 'Volt DC') and (NSR_dc_low<float(v)<NSR_dc_high):
			return True
		else:
			return False




	def finalize(self):
		P = self.Product
		for dName in P.states:
			if not P.states[dName]['state']:
				self.HTML_Results[dName] = {'trifft nicht zu':P.states[dName]['deactivators']}
			else:
				self.HTML_Results[dName] = {'trifft zu':P.states[dName]['activators']}
	
	def snippetsToHtml(self):
		out = []
		for directive in self.snippets:
			# put directive name in header
			out.append('<h1>{0}</h1>'.format(directive))
			for section in self.snippets[directive]:
				# put section name in smaller header
				sName = list(section.keys())[0]
				out.append('<h2>{0}</h2>'.format(sName))
				out.extend(section[sName])

		return out

	def writeToFile(self, textList, fName = 'tmp.html'):
		with open(fName,'w') as f:
			f.write(''.join(textList))





	def getHtmlResponse(self):
		self.snippets = {}

		P = self.Product
		for dName in P.states:
			if not P.states[dName]['state']:
				self.HTML_Results[dName] = {'trifft nicht zu':P.states[dName]['deactivators']}
			else:
				self.HTML_Results[dName] = {'trifft zu':P.states[dName]['activators']}
		"""
		check if purpose relating to activated directive is given,
		return part of html directive regarding that purpose.
		"""
		for purpose in P.json['Verwendungszwecke']:
			if purpose in self.kBase['Verwendungszwecke']:
				p = self.kBase['Verwendungszwecke'][purpose]
				for directive in p['benötigt Text']:
					if P.states[directive]['state']:
						texts = p['benötigt Text'][directive]['text']
						for text in texts:
							text = text.lower()
							if 'anhang' in text:
								D = self.appendices[directive]
								# first key:
								idx = re.search('_[ivx]+',text).span()[1]
								fk = text[:idx].replace('_',' ')
								if idx == len(text):
									sk = None
								else:	
									sk = text[idx+1:]
									# todo: add third level
									if '.' in sk:
										idx = sk.index('.')
										sk = sk[:idx+1]
							else:
								D = self.articles[directive]
								text = text.replace('artikel_','')
								if '_' in text:
									fk = text.split('_')[0]
									sk = text.split('_')[1]

							# find corresponding text in dictionairy
							if not sk is None:
								snippet = D[fk][sk]
							else:
								snippet = D[fk]

							if not directive in self.snippets:
								self.snippets[directive] = []

							if not sk is None:
								self.snippets[directive].append({' '.join([fk,sk]):snippet})
							else:
								self.snippets[directive].append({fk:snippet})
		return self.snippets
















		









