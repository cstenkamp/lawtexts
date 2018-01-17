class Configurator():

	def __init__(self, machine=None):
		if machine is None:
			self.Product = Machine()
		else:
			self.Product = machine

	def configure(self, data):
		self.Product.json = data 




