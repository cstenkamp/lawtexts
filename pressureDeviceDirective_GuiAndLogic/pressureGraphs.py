import numpy as np
import matplotlib.pyplot as plt 

def loadGraphImage(path):
	im=plt.imread(path)
	yshift=583
	xshift=81

	x1000 = 590

	x = np.log(desiredX)/(np.log(1000)/(x1000-xshift))+xshift

	return im

def graph1(volume,pressure):
	# IV
	if (pressure>=1000) or (pressure*volume >+ 1000):
		return "IV"
	# III
	elif ((volume <= 1) and (200<=pressure<=1000)) or \
		 ((volume >= 1) and (200<=pressure*volume<=1000)):
		 return "III"
	# II
	elif ((volume >= 1) and (50<=pressure*volume<=200)):
		 return "II"
	# I
	elif ((volume >= 1) and (25<pressure*volume<=50)):
		 return "I"
	else:
		return "Artikel 4, Absatz 3"


def graph2(volume,pressure):
	if (pressure>=3000) or ((pressure*volume>=3000) and volume<=750) or (volume>=750 and pressure>=4):
		return "IV"
	elif ((1000<=pressure<=3000) and volume <= 1) \
		or ((1000<=pressure*volume<=3000) and (1<=volume)) \
		or ((pressure <= 4) and (1000<=pressure*volume)):
		return "III"
	elif ((volume>=1) and (200<=pressure*volume<=1000)):
		return "II"
	elif ((volume>=1) and (50<=pressure*volume<=200)):
		return "I"
	else:
		return "Artikel 4, Absatz 3"

def graph3(volume,pressure):
	if (1 <= volume) and (500 <= pressure):
		return "III"
	elif ((volume <= 1) and (500<=pressure)) \
		or ((10 <= pressure <= 500) and ((200<=pressure*volume) and (1<=volume))):
		return "II"
	elif (pressure<=10) and (200 <= pressure*volume):
		return "I"
	else:
		return "Artikel 4, Absatz 3"


def graph4(volume,pressure):
	if (10<=volume) and (10000<=volume*pressure) and (500<=pressure):
		return "II"
	elif ((volume<=10) and (1000<=pressure)) \
		or ((10<=pressure<=500) and 10000<=pressure*volume):
		return "I"
	else:
		return "Artikel 4, Absatz 3"

def graph5(volume,pressure):
	if ((2<=volume) and (32<=pressure)) \
		or ((32<=pressure) and (3000<=pressure*volume)) \
		or 1000<=volume:
		return "IV"
	elif (pressure<=32) and (200<=pressure*volume<=3000) and (volume<=1000):
		return "III"
	elif (pressure<=32) and (50<=pressure*volume<=200) and (2<=volume):
		return "II"
	elif (2<=volume) and (pressure*volume<=50):
		return "I"
	else:
		return "Artikel 4, Absatz 3"

def graph6(DN,pressure):
	if ((100<=DN) and (3500<=pressure*DN)) or 350<=DN:
		return "III"
	elif ((25<=DN) and (1000<=pressure*DN)) or 100<=DN:
		return "II"
	elif (25<=DN):
		return "I"
	else:
		return "Artikel 4, Absatz 3"


def graph7(DN,pressure):
	if (250<=DN) and (5000<=pressure*DN):
		return "III"
	elif (100<=DN) and (3500<=pressure*DN):
		return "II"
	elif (32<=DN) and (1000<=pressure*DN):
		return "II"
	else:
		return "Artikel 4, Absatz 3"

def graph8(DN,pressure):
	if (25<=DN) and (500<=pressure):
		return "III"
	elif (25<=DN) and (10<=pressure) and (2000<=pressure*DN):
		return "II"
	elif (2000<=pressure*DN):
		return "I"
	else:
		return "Artikel 4, Absatz 3"


def graph9(DN,pressure):
	if (200<=DN) and (500<=pressure):
		return "II"
	elif (200<=DN) and (10<=pressure) and (5000<=pressure*DN):
		return "I"
	else:
		return "Artikel 4, Absatz 3"

pressureGraphs = [graph1,graph2,graph3,graph4,graph5,graph6,graph7,graph8,graph9]