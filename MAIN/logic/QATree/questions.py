
class Question():
	def __init__(self, text):
		self.text = text
		self.posChild = None
		self.negChild = None

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
		pass

	def start(self,Q1):
		result = self.iter(Q1)
		return result 

	def iter(self, question):
		while not type(question) is Result:
			print(question.text)
			a = None
			while not a in ['y','n']:
				a = input('y/n \n')
			question = question.next(a)
		# question is now an answer
		print(question.text)
		return question