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
		self.parts = {}

		self.html_pages = []
		self.html_names = []

		self.description = None
		self.procedures = None 
		self.applicability = None

		self.HTML_description = {}
		self.HTML_Results = {'MRL':[],'NSR':[]}
		self.HTML_Procedures = {} 

		self.comments = []

		self.states = {'MRL':{'state':None,
							  'activators':{
							  		'Verwendungszwecke':[],
							  		'Verwendungsorte':[],
							  		'Komponenten':[]
							  },
							  'deactivators':{
							  		'Verwendungszwecke':[],
							  		'Verwendungsorte':[],
							  		'Komponenten':[]
							  },
							  'rigid_state':False
					   	     },
				       'NSR':{'state':None,
							  'activators':{
							  		'Verwendungszwecke':[],
							  		'Verwendungsorte':[],
							  		'Komponenten':[]
							  },
							  'deactivators':{
							  		'Verwendungszwecke':[],
							  		'Verwendungsorte':[],
							  		'Komponenten':[]
							  },
							  'rigid_state':False
				       		 }				       
				       }
