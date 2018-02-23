
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
		pass


