import json
import re
import sys

from jsonParser import PARSER 

purposesPath = 'json/_purposes.json'
sitesPath = 'json/_sites.json'
partsPath = 'json/parts.json'
featuresPath = 'json/features.json'


NSR_ac_high = 1000
NSR_ac_low  = 50

NSR_dc_high = 1000
NSR_dc_low  = 50



class LOGIC():
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

		'''
		keep this dict to check if a directive is still theoretically applicable 
		or not. (If directives are deactivated by some product purpose or site,
		it is noted here. )
		'''
		self.directiveStates = {'MRL':None,
								'NSR':None,
								'ATEX':None,
								'DGN':None}

		self.stateExplanation = {'MRL':[],
								'NSR':[],
								'ATEX':[],
								'DGN':[]}


	def checkInfo(self,dName,texts,results,text_output,B):
		# append to results
		results[dName] = B
		# append to text outputs
		if not dName in text_output:
			text_output[dName] = []				
		for t in texts:
			text_output[dName].append(t)
		return results, text_output

	def checkFirstLevel(self):
		result_purposes = {}
		for D in ['MRL','NSR']:
			t = self._checkFirstLevel(kind='Verwendungszwecke',directive=D)
			result_purposes[D] = t

		result_sites = {}
		for D in ['MRL','NSR']:
			t = self._checkFirstLevel(kind='Verwendungsorte',directive=D)
			result_sites[D] = t

		for D,v in result_purposes.items():
			if not v['deactivating'] == {}:
				self.directiveStates[D] = False
				self.stateExplanation[D] = list(v['deactivating'].keys())

		for D,v in result_sites.items():
			if not v['deactivating'] == {}:
				self.directiveStates[D] = False
				self.stateExplanation[D] = list(v['deactivating'].keys())

		return result_purposes, result_sites


	def _checkFirstLevel(self,kind='Verwendungszwecke',directive='MRL'):
		if kind == 'Verwendungszwecke':
			kBase = self.purposes
		elif kind == 'Verwendungsorte':
			kBase = self.sites 
		"""
		checks, if product is affected by directive due to purpose/site
		"""
		result = {'activating':{},
				  'deactivating':{},
				  'user_questions':{},
				  'directive_texts':{}}
		# iterate over purposes/sites
		for firstLevelFeature in self.Product.json[kind]:
			# get information about site/purpose 
			if directive in kBase[firstLevelFeature]['aktiviert']:
				activating = kBase[firstLevelFeature]['aktiviert'][directive]
				result['activating'][firstLevelFeature] = activating

			if directive in kBase[firstLevelFeature]['deaktiviert']:
				deactivating = kBase[firstLevelFeature]['deaktiviert'][directive]
				result['deactivating'][firstLevelFeature] = deactivating

			if directive in kBase[firstLevelFeature]['betrifft vielleicht']:
				user_question = kBase[firstLevelFeature]['betrifft vielleicht'][directive]
				tmp = []
				for U in user_question:
					tmp.append((U['Frage'],U['Ressource']))
				result['user_questions'][firstLevelFeature] = tmp

			if directive in kBase[firstLevelFeature]['benötigt Text']:
				directiveTexts = kBase[firstLevelFeature]['benötigt Text'][directive]
				result['directive_texts'][firstLevelFeature] = directiveTexts
		return result



	def checkNSR(self,values):
		# names of current types
		ac,dc = self.features['Features']['Spannung']
		k,v = list(values.items())[0]
		if k == ac:
			if  NSR_ac_low<float(v)<NSR_ac_high:
				return True
			else:
				return False
		elif k == dc:
			if  NSR_dc_low<float(v)<NSR_dc_high:
				return True
			else:
				return False

	def checkFeatures(self,part):
		results = {}
		# get features of part of product
		featDict = self.Product.json['Komponenten'][part]
		if 'Spannung' in featDict:
			B = self.checkNSR(featDict['Spannung'])
			if B:
				results['NSR'] = B
		return results

	def checkHiddenFeatures(self,part):
		results = {}
		_feat = self.getHiddenFeatures(part)
		if _feat is None:
			return 
		for f in _feat:
			if f.startswith('+'):
				results[f[1:]] = True
			if f.startswith('-'):
				results[f[1:]] = False
			return results


	def getHiddenFeatures(self,part):
		if part in self.parts:
			return self.parts[part]['_Eigenschaften']


	def checkParts(self):
		results = {}
		# for every part in the machine
		for part in self.Product.json['Komponenten']:
			# see if you find information in your knowledge base
			_f_res = {}
			if part in self.parts:
				# check possible hidden features
				_f_res = self.checkHiddenFeatures(part)
			# check each of the features
			f_res = self.checkFeatures(part)
			# overwrite results of feature check with check of hidden features
			if not _f_res is None:
				for _f,_v in _f_res.items():
					f_res[_f] = _v
			results[part] = f_res 
		return results


	def check(self):
		HTML_out = ''
		# first level check, we assume first level is dominant over others
		res_f0, text_out_f0, user_qu_f0 = self.checkFirstLevel()
		# get results for each part
		parts_results = self.checkParts()
		# iterate over results and collect result per directive (True overwrites False)
		c = {"MRL":False,"NSR":False}
		for p,D in parts_results.items():
			for k,d in D.items():
				c[k]+=d
		# negate via res_fo
		for d,b in res_f0.items():
			if not d in c:
				continue
			c[d] *= b 
		# now c contains activations from the parts, and deactivations from first level

	def getMRLProcedure(self):
		q_head = 'Finden sie ihr Produkt in dieser Liste wieder?'
		q_body = self.dictParser.labelToHtml('anhang_iv','MRL')
		# depending on the user's response different things need to 
		# be included in final output text
		header_yes = '<h1>Produkt ist nicht in Anhang IV gelistet</h1>'
		procedure_yes = {}
		procedure_yes['artikel_7_'] = self.dictParser.labelToHtml('artikel_7_','MRL')	
		procedure_yes['artikel_7_2'] = self.dictParser.labelToHtml('artikel_7_2)','MRL')		
		procedure_yes['anhang_viii'] = self.dictParser.labelToHtml('anhang_viii','MRL')
		procedure_yes['anhang_vii']  = self.dictParser.labelToHtml('anhang_vii','MRL')
		procedure_yes['anhang_ix']   = self.dictParser.labelToHtml('anhang_ix','MRL')
		procedure_yes['anhang_x']    = self.dictParser.labelToHtml('anhang_x','MRL')
		procedure_yes['anhang_iv']   = self.dictParser.labelToHtml('anhang_iv','MRL')

		header_no = '<h1>Produkt ist in Anhang IV gelistet</h1>'
		procedure_no = {}
		procedure_no['anhang_viii'] = self.dictParser.labelToHtml('anhang_viii','MRL')
		procedure_no['anhang_vii'] = self.dictParser.labelToHtml('anhang_vii','MRL')

		procedure = {}

		procedure['anhang_i_'] = self.dictParser.labelToHtml('anhang_i_','MRL')
		procedure['anhang_i_1._1._2.'] = self.dictParser.labelToHtml('anhang_i_1._1._2.','MRL')
		procedure['anhang_i_1._7._3.'] = self.dictParser.labelToHtml('anhang_i_1._7._3.','MRL')
		procedure['anhang_i_1._7._4.'] = self.dictParser.labelToHtml('anhang_i_1._7._4.','MRL')


		procedures = {'yes':procedure_yes,
				      'no':procedure_no,
				      'always':procedure}

		headers = {'yes':header_yes,
				   'no' :header_no}



		return q_head, q_body, procedures, headers

	def setMRLProcedure(self, answer, headers, procedures):
		procedure = procedures[answer]
		procedure.update(procedures['always'])
		answer = headers[answer]

		header = [self.dictParser.labelToHtml('artikel_12_','MRL'),
			 	  self.dictParser.labelToHtml('artikel_12_1)','MRL'),
			 	  self.dictParser.labelToHtml('artikel_12_2)','MRL'),
				  answer,
			 	  self.dictParser.labelToHtml('artikel_12_3)','MRL'),
			 	  self.dictParser.labelToHtml('artikel_12_4)','MRL'),]

		return header, procedure 


	