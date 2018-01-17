import json

purposesPath = 'json/_purposes.json'
sitesPath = 'json/_sites.json'


NSR_ac_high = 1000
NSR_ac_low  = 50

NSR_dc_high = 1000
NSR_dc_low  = 50



class LOGIC():
	def __init__(self, Product):
		self.Product = Product
		self.kBase = {'Verwendungszwecke':{},
					  'Verwendungsorte':{}}

		self.HTML_Results = {'MRL':[],'NSR':[]}

		self.loadPurposes()
		self.loadSites()

	def loadPurposes(self):
		with open(purposesPath) as f:
			self.kBase['Verwendungszwecke'] = json.load(f)

	def loadSites(self):
		with open(sitesPath) as f:
			self.kBase['Verwendungsorte'] = json.load(f)

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


		









