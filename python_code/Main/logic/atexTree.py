
class Question():
	def __init__(self, text, effect=None):
		self.text = text
		self.posChild = None
		self.negChild = None
		self.effect = effect 

	def next(self,answer):
		if answer == 'y':
			return self.posChild
		else:
			return self.negChild

class Result():
	def __init__(self, text, bool, switch=None):
		self.text = text
		self.bool = bool 
		self.switch = switch 


class Test():
	def __init__(self):
		self.effects = []

	def start(self,Q1):
		result = self.iter(Q1)
		return result 

	def iter(self, question):
		while (not type(question) is Result) and (not question is None):
			print(question.text)
			a = None
			while not a in ['y','n']:
				a = input('y/n \n')
			self.effects.append((question.effect[a],question.text,a))
			question = question.next(a)
		return self.effects



class Questions():
	def __init__(self):

		self.QD = Question('Produkt wird unter eigenem Namen oder unter eigener Handelsmarke in Verkehr gebracht, oder Produkt wird vor in Verkehr bringen so verändert, dass die Konformität mit dieser Richtlinie beeinträchtigt wird?',
					  effect={'y':'extra',
					  		  'n':'None'})

		self.Q0 = Question('Handelt es sich bei dem Produkt um ein Schutzsystem?',
					  effect={'y':'Schutzsystem',
					  		  'n':'None'})


		self.Q1 = Question('Gerät ist zur Verwendung in untertägigen Bergwerken sowie deren Übertageanlagen bestimmt, die durch Grubengas und/oder brennbare Stäbe gefährded wird?',
					  effect={'y':'Gerätegruppe I',
					  		  'n':'Gerätegruppe II'})
		self.Q0.negChild = self.Q1

		self.Q1y = Question('Beinhalten die Geräte zusätzliche Schutzmaßnahmen und sollen selbst in explosionsfähiger Atmosphäre weiter betrieben werden?',
					   effect={'y':'Gerätekategorie M 1',
					   		   'n':'Gerätekategorie M 2'})
		self.Q1.posChild = self.Q1y


		self.Q1n = Question('Ist damit zu rechnen, dass die Atmosphäre, in der das Gerät betrieben werden soll, explosionsfähig wird?',
					   effect={'y':'None',
					   		   'n':'Gerätekategorie 3'})
		self.Q1.negChild = self.Q1n


		self.Q2 = Question('Ist eine explosionsfähige Atmosphäre ständig oder häufig vorhanden?',
					   effect={'y':'Gerätekategorie 1',
					   		   'n':'Gerätekategorie 2'})

		self.Q1n.posChild = self.Q2


		self.Q3 = Question('Handelt es sich um ein Gerät mit Motor mit innerer Verbrennung oder um ein elektrisches Gerät?',
					   effect={'y':'motor',
					   		   'n':'noMotor'})
		self.Q1y.negChild = self.Q3
		#self.Q2.posChild = self.Q3
		self.Q2.negChild = self.Q3

