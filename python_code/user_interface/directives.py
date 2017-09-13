from objects import *
from tkinter import *
from interfaces import *

class Directive():
	def __init__(self, title, id_string, parent = None):
		self.title = title
		self.id_string = id_string
		self.active = False
		if parent is None:
			parent = Tk()
		self.parent = parent

		f_name = 'csv/verwendungszwecke.csv'
		purposes = loadCSV(f_name)
		f_name = 'csv/verwendungsorte.csv'
		sites = loadCSV(f_name)

		self.includingPurposes, self.excludingPurposes = self.getInExcludingX(purposes)
		self.includingSites, self.excludingSites = self.getInExcludingX(sites)

	def getInExcludingX(self, X):
		Excluding = []
		Including = []
		for x in X.keys():
			v = X[x]
			excluding = v.excluding_directives.keys()
			including = v.including_directives.keys()

			if self.id_string in excluding:
				Excluding.append(x)
			if self.id_string in including:
				Including.append(x)
		return Including, Excluding


	def checkApplicabilityOnPurpose(self, purpose):
		if purpose in self.excludingPurposes:
			self.active = False
		if purpose in self.includingPurposes:
			self.active = True
		if purpose in self.includingPurposes and purpose in self.excludingPurposes:
			print('ERROR')

	def checkApplicabilityOnSite(self, site):
		if site in self.excludingSites:
			self.active = False
		if site in self.includingSites:
			self.active = True
		if site in self.includingSites and site in self.excludingSites:
			print('ERROR')




'''
Elektromagnetische Vertraeglichkeit
'''
class ElectromagneticCompatibilityDirective(Directive):
	def __init__(self, parent = None):
		super(ElectromagneticCompatibilityDirective, self).__init__('Elektromagnetische Veträglichkeit', '2014/30/EU', parent = parent)

	def checkApplicabilityOnComponent(self, componentFrame):
		properties = componentFrame.properties
		units = [property.propertyUnit for property in properties]
		values = [property.propertyValue for property in properties]
		if 'Betriebsspannung' in units:
			property = properties[units.index('Betriebsspannung')]
			if property.checkVar == 1:
				self.active = True
				componentFrame.directives.append(self.id_string)


	def check(self, site, purpose, componentFrames):
		
		# first check applicability on each single component
		[self.checkApplicabilityOnComponent(componentFrame) for componentFrame in componentFrames]
		# then check applicability on site and purpose
		# since they can overwrite earlier decisions
		self.checkApplicabilityOnSite(site)
		self.checkApplicabilityOnPurpose(purpose)





'''
Niederspannungs Richtlinie
'''
class LowVoltageDirective(Directive):
	def __init__(self, parent = None):
		super(LowVoltageDirective, self).__init__('Niederspannungs-Richtlinie', '2014/35/EU', parent = parent)
		self.ac_limits = [50,1000]
		self.dc_limits = [75,1500]

	def checkApplicabiliyOnComponent(self, componentFrame):
		properties = componentFrame.properties
		units = [property.propertyUnit for property in properties]
		values = [property.propertyValue for property in properties]
		titles = [property.title for property in properties]

		if 'Betriebsspannung' in titles:
			print(titles)
			property = properties[titles.index('Betriebsspannung')]
			if property.propertyUnit == 'Volt a/c':
				if self.ac_limits[0] < float(property.propertyValue) < self.ac_limits[1]:
					self.active = True
					componentFrame.directives.append(self.id_string)
				else:
					self.active = False
			elif property.propertyUnit == 'Volt d/c':
				if self.dc_limits[0] < float(property.propertyValue) < self.dc_limits[1]:
					self.active = True
					componentFrame.directives.append(self.id_string)
				else:
					self.active = False


	def check(self, site, purpose, componentFrames):
		# first check applicability on each single component
		[self.checkApplicabiliyOnComponent(componentFrame) for componentFrame in componentFrames]
		# then check applicability on site and purpose
		# since they can overwrite earlier decisions
		self.checkApplicabilityOnSite(site)
		self.checkApplicabilityOnPurpose(purpose)


class MachineryDirective(Directive):
	def __init__(self, parent = None):
		super(MachineryDirective, self).__init__('Maschinenrichtlinie', '2006/42/EG', parent = parent)

		
	def openProductDialog(self):
		if not self.parent.productVar.get() in self.parent.products.keys():
			return
		# check if product is included in directive:
		variable = self.parent.productVar.get()
		including_directives = self.parent.products[variable].including_directives.keys()

		if self.id_string in including_directives:
			if variable == 'Fahrzeug':
				file_name = 'txt/MRL_interface_Fahrzeuge.txt'
				MachineryInterface(file_name, parent = self.parent)
			if variable == 'Sicherheitsbauteile':
				file_name = 'txt/MRL_interface_Sicherheitsbauteile.txt'
				MachineryInterface(file_name, parent = self.parent)


	def checkApplicabiliyOnComponent(self, componentFrame):
		for component in componentFrame:
			# check if something is interesting for machine directive
			for property in component.properties:
				if hasattr(property,'checkVar3'):
							if property.checkVar3.get() == 1:
								print('stuff')
								self.active = False
								
		print('"checkApplicabiliyOnComponent" in "directives.py" needs to be implemented')


	def checkApplicabilityOnProduct(self):
		if any(self.parent.MachineryInterfaceVars[:-1]):
			self.active = False
		elif self.parent.MachineryInterfaceVars[-1] == 1:
			self.active = True


	def check(self, site, purpose, componentFrames):
		# first check applicability on each single component
		[self.checkApplicabiliyOnComponent(componentFrame) for componentFrame in componentFrames]
		# then check applicability on site and purpose
		# since they can overwrite earlier decisions
		self.checkApplicabilityOnSite(site)
		self.checkApplicabilityOnPurpose(purpose)

		

class ATEXDirective(Directive):
	def __init__(self, parent = None):
		super(ATEXDirective, self).__init__('ATEX', '2014/34/EU', parent = parent)


	def checkApplicabiliyOnComponent(self, componentFrame):
		properties = componentFrame.properties
		units = [property.propertyUnit for property in properties]
		values = [property.propertyValue for property in properties]
		if 'Inhalt' in values:
			property = properties[values.index('Inhalt')]
			if property.propertyUnit == '--andere--':
				contentProperty = property.contentSpecifier.get()
				incl_directives = property.specifier[contentProperty].including_directives
				excl_directives = property.specifier[contentProperty].excluding_directives
			if property.propertyUnit in property.options:
				incl_directives = property.options[property.propertyUnit].including_directives
				excl_directives = property.options[property.propertyUnit].excluding_directives
			if self.id_string in incl_directives:
					self.active = True
					componentFrame.directives.append(self.id_string)
			if self.id_string in excl_directives:
					self.active = False
			if self.id_string in excl_directives and self.id_string in  incl_directives:
				print('Error in ATEXDirective')
				print('both in and excluded in same part')
		



	def openProductDialog(self):
		if not self.parent.productVar.get() in self.parent.products.keys():
			return
		# check if product is included in directive:
		variable = self.parent.productVar.get()
		including_directives = self.parent.products[variable].including_directives.keys()

		if self.id_string in including_directives:
			if variable == 'Sicherheitsbauteile':
				file_name = 'txt/ATEX_interface_Sicherheitsbauteile.txt'
				ATEXInterface(file_name, parent = self.parent)


	def check(self, site, purpose, componentFrames):
		# first check applicability on each single component
		[self.checkApplicabiliyOnComponent(componentFrame) for componentFrame in componentFrames]
		# then check applicability on site and purpose
		# since they can overwrite earlier decisions
		self.checkApplicabilityOnSite(site)
		self.checkApplicabilityOnPurpose(purpose)


	def checkApplicabilityOnProduct(self):
		if any(self.parent.ATEXInterfaceVars[:-1]):
			self.active = False
		elif self.parent.ATEXInterfaceVars[-1] == 1:
			self.active = True


'''
Betriebssicherheitsverordnung
'''
class OperationalSafetyDirective(Directive):
	def __init__(self, parent = None):
		super(OperationalSafetyDirective, self).__init__('Betriebssicherheitsverordnung', 'BetrSichV', parent = parent)
		



