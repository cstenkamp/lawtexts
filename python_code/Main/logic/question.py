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