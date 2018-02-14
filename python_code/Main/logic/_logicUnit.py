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
	def __init__(self, Product, articles, appendices,directiveNames=['MRL','NSR']):
		self.Product = Product
		self.appendices = appendices
		self.articles = articles

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
		self.directiveStates = {}
		for n in directiveNames:
			self.directiveStates[n] = True


	def checkInfo(self,dName,texts,results,text_output,B):
		# append to results
		results[dName] = B
		# append to text outputs
		if not dName in text_output:
			text_output[dName] = []				
		for t in texts:
			text_output[dName].append(t)
		return results, text_output


	def checkFirstLevel(self,kind='Verwendungszwecke',directive='MRL'):
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
		ac,dc = self.features['features']['Spannung']
		k,v = list(values.items())[0]
		if k == ac:
			if  NSR_ac_low<float(v)<NSR_ac_high:
				return True
			else:
				r = Q['Ressource']
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

	def flushDict(self,D):
		HTML = ''
		# srt everything alphabetically
		keys = sorted(D.keys())
		if keys[-1]=='_':
			keys = ['_']+keys[:-1]
		#iterate over keys
		for K in keys:
			# see, if current value is dict
			if type(D[K]) is dict:
				# call yourself
				HTML += self.flushDict(D[K])
			else:
				t = '\n'.join(D[K])
				HTML += t
		return HTML


	def labelToHtml(self,label,dName,append_base=False):
		HTML = ''
		label = label.lower()
		k = label.split('_')[0]
		label = label.split('_')[1:]
		if k == 'anhang':
			D = self.appendices
		elif k == 'artikel':
			D = self.articles


		D = D[dName]
		d = D.copy()

		for ix,l in enumerate(label):
			# if there is a base case under the current label, append it
			if ("_" in d) and (ix>0) and append_base:
				t = '\n'.join(d["_"])
				HTML += t
			#
			if ix==len(label)-1:
				if type(d[l]) == dict:
					t = self.flushDict(d[l])
				else:
					t = '\n'.join(d[l])
				HTML+= t
			#
			# check, if current index is last index, if so, append everything downwards
			# else overwrite dictionairy with new one one level deeper
			if not ix==len(label)-1:
				d = d[l].copy()
		return HTML



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


	def fullMRLcheck(self):
		article_buffer = {}
		procedure_buffer = []
		current_state = False
		# first see if any component activates MRL
		parts_check = self.checkParts()
		for part, res in parts_check.items():
			if not "MRL" in res:
				continue
			# if anything activates directive, this becomes True
			current_state += res['MRL']
		# we now know if this directive is activated by ANY part

		# next we check if the directive gets deactivated by purpose/site
		result_purpose = self.checkFirstLevel(kind='Verwendungszwecke',directive="MRL")
		# if purpose is deactivating, we have no questions
		if 'MRL' in r_purpose:
			if r_purpose['MRL']==False:
				HTML = '<h0>MRL trifft aufgrund von Verwendungszweck nicht zu.</h0>'
				return HTML, False
		# if directive is not activated by any part, return
		if not current_state:
			HTML = '<h0>MRL trifft auf keine der Komponenten zu.</h0>'
			return HTML, False


		# add regular information regarding Konformitätsbewertungsverfahren
		procedure_buffer.append(self.articles['MRL']['12']['_'])
		procedure_buffer.append(self.articles['MRL']['12']['1)'])
		procedure_buffer.append(self.articles['MRL']['12']['2)'])

		# ask question if product is listed under Anhang IV
		q = '<h2>Ist das Produkt hier aufgelistet?</h2>'
		q_text = self.labelToHtml('anhang_iv','MRL')
		T = '{0}\n{1}\n "y"/"n"\n'.format(q,q_text)
		answer=''
		while not answer in ['y','n']:
			answer = input(T)
		
		if answer == 'n':
			procedure_buffer.append(['<h1>Produkt ist nicht in Anhang IV gelistet</h1>'])
			article_buffer['anhang_viii'] = self.labelToHtml('anhang_viii','MRL')
			article_buffer['anhang_vii'] = self.labelToHtml('anhang_vii','MRL')
		else:
			procedure_buffer.append(['<h1>Produkt ist in Anhang IV gelistet</h1>'])
			procedure_buffer.append(self.articles['MRL']['12']['3)'])
			procedure_buffer.append(self.articles['MRL']['12']['4)'])
			article_buffer['artikel_7_2'] = self.labelToHtml('artikel_7_2)','MRL')
			article_buffer['anhang_viii'] = self.labelToHtml('anhang_viii','MRL')
			article_buffer['anhang_vii']  = self.labelToHtml('anhang_vii','MRL')
			article_buffer['anhang_ix']   = self.labelToHtml('anhang_ix','MRL')
			article_buffer['anhang_x']    = self.labelToHtml('anhang_x','MRL')
			article_buffer['anhang_iv']   = self.labelToHtml('anhang_iv','MRL')
		# append other information based on purpose
		for res in t_purpose['MRL']:
			article_buffer[res.lower()] = self.labelToHtml(res,'MRL')

		# append stuff, that applies in any case
		t = '\n'.join(self.appendices['MRL']['i']['_'])
		article_buffer['anhang_i_'] = t

		t = '\n'.join(self.appendices['MRL']['i']['1.']['1.']['2.'])
		article_buffer['anhang_i_1.1.2'] = t

		t = '\n'.join(self.appendices['MRL']['i']['1.']['7.']['3.'])
		article_buffer['anhang_i_1.7.3'] = t

		t = '\n'.join(self.appendices['MRL']['i']['1.']['7.']['4.'])
		article_buffer['anhang_i_1.7.4'] = t


		return article_buffer, procedure_buffer

