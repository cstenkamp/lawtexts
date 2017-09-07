from tkinter import *


class Interface(Toplevel):
	def __init__(self, parent = None, file = None):
		if parent is None:
			self.parent = Tk()
		else:
			self.parent = parent
		super(Interface, self).__init__(self.parent)
		self.readFile(file)
		self.leftCanvas = Canvas(self,
								 width=128,
								 height=128)
		self.leftCanvas.grid(row = 0, column = 0, sticky = W)
		self.explanation = Label(self.leftCanvas, 
								 text = self.text, 
								 justify = LEFT,  
								 relief = GROOVE,
								 wraplength = 500)
		self.explanation.grid(row=0,column=0,sticky=W, pady=(10,10), padx=(10,10))
		# slap canvas in middle to separate checkbuttons and ok button
		self.middleCanvas = Canvas(self, width=50)
		self.middleCanvas.grid(row=0,column = 1)
		self.vars = []
		for option in self.options:
			var = IntVar()
			var.set(0)
			b = Checkbutton(self.leftCanvas, text = option, 
							variable = var, 
							relief = GROOVE,
							wraplength = 500, 
							justify = LEFT, 
							anchor = N)
			b.grid(sticky = W,
				   pady = (10,10),
				   padx = (10,10))
			self.vars.append(var)
		self.rightCanvas = Canvas(self, relief = GROOVE, 
								  width=50,
								  height=128)
		self.rightCanvas.grid(row = 0, column = 2, sticky = E)
		self.button = Button(self.rightCanvas, text = 'ok', command = self.accept)
		self.button.grid()

	def readFile(self, f_name):
		f = open(f_name)
		# read file as a whole
		text = f.read()
		# split into parts
		self.text = text.split('$')[0]
		text = text.split('$')[1]
		self.options = text.split('%')
		self.options = [o.strip() for o in self.options if not o.strip() == ''] 
		f.close()

	def accept(self):
		# save variables in parent
		vars = [v.get() for v in self.vars]
		s = self.__class__.__name__
		setattr(self.parent, s+'Vars', vars)
		# save options in parent
		setattr(self.parent, s+'Options', self.options)
		self.destroy()

	def check(self):
		pass





class ElectromagneticCompatibilityInterface(Interface):
	def __init__(self, parent = None):
		self.parent = parent
		super(ElectromagneticCompatibilityInterface, self).__init__(self.parent, file = 'txt/EMV_interface.txt')
		self.title('Elektromagnetische Verträglichkeit Interface')




class LowVoltageInterface(Interface):
	def __init__(self, parent = None):
		self.parent = parent
		super(LowVoltageInterface, self).__init__(self.parent, file = 'txt/NSR_interface.txt')
		self.title('Niederspannungsrichtlinien Interface')

		

class MachineryInterface(Interface):
	def __init__(self, file_name, parent = None):
		super(MachineryInterface, self).__init__(parent, file = file_name)
		self.title('Maschinenrichtlinien Interface')

class ATEXInterface(Interface):
	def __init__(self, file_name, parent = None):
		super(ATEXInterface, self).__init__(parent, file = file_name)
		self.title('ATEX Interface')



