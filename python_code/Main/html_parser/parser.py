import re
from pprint import pprint as print 
import numpy as np 

class PARSER():
	"""
	#parses html directives into hierarchical dictionairies, so that:

	listOfTextLines = getHtml(path_to_mrl_directive_as_html)

	# the parse function is only capable of splitting the text
	# at text matching certain regular expressions. At those positions
	# a dictionairy key is produced from the text (section/subsection name)
	# and the text is saved at the corresponding level in the dictionairy.

	# parsing the 'artikel' into dictionairies:
	reg1 = 'ti-art">Artikel [\d]+</p>'
	reg2 = 'ti-art">Artikel [\d]+</p>'
	s_start = 8
	s_end = 4
	articles = parse(text, reg1, reg2,s_start,s_end)

	art2 = articles['artikel 2']['a']

	# the dictionairy can then be transformed into a list
	as_list = printDict(art2)

	# and then be written to a file
	"""

	def __init__(self):
		pass

	def getHtml(self, p):
		with open(p) as f:
			text = list(map(lambda x: x.strip(), f.readlines()))
		return text

	def parse(self,textList,reg1,reg2,s_start, s_end, name='none'):
		D = {}
		idx = [ix for ix in range(len(textList)) if not re.search(reg1,textList[ix]) is None] 
		keys = [re.search(reg2,textList[ix]) for ix in idx]
		idx = [i for ix,i in enumerate(idx) if not keys[ix] is None]
		keys = [k.group(0)[s_start:-s_end] for k in keys if not k is None]
		keys = [k.lower() for k in keys if not k is None]
		tmp = list(map(lambda x: re.search('[[\d]+[\.]*]*',x), keys))
		if all([not t is None for t in tmp]):
			keys = [t.group(0) for t in tmp]
		if keys == []:
			D[name] = textList
			return D
		ix=-1
		for ix in range(len(idx)-1):
			k = keys[ix]
			d = textList[idx[ix]:idx[ix+1]]
			D[k] = d
		k = keys[ix+1]
		d = textList[idx[ix+1]:]
		D[k] = d
		return D


	def printDict(self,d):
		if type(d) is list:
			return ''.join(d)
		if all([type(d) is list for d in d.values()]):
			return '\n'.join([item for sublist in d.values() for item in sublist])
		else:
			return '\n'.join([printDict(d) for d in d.values()])
"""
if __name__ == '__main__':
	main()
	text = getHtml()

	reg1 = 'ti-art">Artikel [\d]+</p>'
	reg2 = 'ti-art">Artikel [\d]+</p>'
	s_start = 8
	s_end = 4

	articles = parse(text, reg1, reg2,s_start,s_end)

	reg1 = '<p class="normal">[\w]*\)'
	reg2 = '>[a-z]*\)'

	ARTICLES = {}
	for k in articles.keys():
		subArticles = parse(articles[k], reg1, reg2, s_start=1, s_end=1)
		if 'none' in subArticles:
			ARTICLES[k] = list(subArticles.values())
		else:
			ARTICLES[k] = subArticles



	reg1 = reg2 = '>ANHANG [IXV]+</p>'
	s_start = 1
	s_end = 4

	appendices = parse(text, reg1, reg2,s_start,s_end)




	reg1 = '<p class="ti-grseq-1" id=".+">[\d]\.'
	reg2 = '>\d\.[ ]+[<span class="italic">]+[\w -]*'
	s_start = 1
	s_end = 1

	APPENDICES = {}
	for k in appendices.keys():
		subArticles = parse(appendices[k], reg1, reg2, s_start=s_start, s_end=s_end)
		if 'none' in subArticles:
			APPENDICES[k] = list(subArticles.values())
		else:
			APPENDICES[k] = subArticles





	# open some file and print anhang i . 6 and artikel 2
	art2 = ARTICLES['2']
	app = APPENDICES['anhang i']['6.']

	ar = printDict(art2)
	ap = printDict(app)

	with open('tmp.html','w') as f:
		f.write(ar)
		f.write(ap)

"""