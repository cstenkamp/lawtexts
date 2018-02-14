import webbrowser, os 

P = os.path.join(os.getcwd(),'html_resources/snippets/')

htmlOutPath = os.path.abspath('temp.html')
url = 'file://' + htmlOutPath

class Machine():
	'''
	HTML:
		Anhang I
			Allg. Grundsaetze
			1.1.2
			1.7.3
			1.7.4
	'''
	def __init__(self):

		self.activated_by_purpose = []
		self.deactivated_by_purpose = []

		self.unvollst = False
		self.nichtIV = False
		self.lastAufnM = False
		self.ivA = False
		self.ivB = False


	def setUnvollst():
		self.unvollst = True

	def setNichtIV():
		self.nichtIV = True

	def setLastAufnM():
		self.lastAufnM = True

	def setIVA():
		self.ivA = True

	def setIVB():
		self.ivB = True