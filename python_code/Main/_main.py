import sys, os, webbrowser
#from pprint import pprint as print
from _machine import Machine

sys.path.insert(0, os.path.join(os.getcwd(),'QATree/'))
from questions_MRL import *

sys.path.insert(0, os.path.join(os.getcwd(),'Definitions/'))
from definitions import Definitions 

sys.path.insert(0, os.path.join(os.getcwd(),'saveLoad/'))
from configurator import Configurator
from jsonParser import PARSER as jPARSER

sys.path.insert(0, os.path.join(os.getcwd(),'logic/'))
from _logicUnit import LOGIC

sys.path.insert(0, os.path.join(os.getcwd(),'html_parser/'))
from directiveParser import PARSER as dPARSER

from _printer import Printer


#TODO: anwendbar auf/von 
#sys.path.insert(0, os.path.join(os.getcwd(),'productClasses/'))

"""
Create A Machine, called Product for clarity reasons
	Machine will contain all information about:
		Parts
		Directives that apply
"""

"""
load json
"""
jsonPath = 'json/__exampleMachine.json'
jparser = jPARSER()
machineData = jparser.parse(jsonPath)

jsonPath = 'json/parts.json'
partsData = jparser.parse(jsonPath)



"""
load html directives
"""
dParser = dPARSER()
# parse MRL into articles and appendices
text = dParser.getHtml(p='html_resources/directives/mrl.html')
mrlArticle = dParser.parseArticles(text)
mrlAppendices = dParser.parseAppendices(text)

text = dParser.getHtml(p='html_resources/directives/nsr.html')
nsrArticle = dParser.parseArticles(text)
nsrAppendices = dParser.parseAppendices(text)

ARTICLES = {'MRL':mrlArticle,
		   	'NSR':nsrArticle
		   }
APPENDICES = {'MRL':mrlAppendices,
			  'NSR':nsrAppendices
			 }

Product = Machine()

"""
add machineData to Product
"""

configurator = Configurator(Product)
configurator.configure(machineData)



Logic = LOGIC(Product, ARTICLES, APPENDICES, directiveNames=['MRL','NSR'])

articles_mrl, procedure_mrl = Logic.fullMRLcheck()

# print procedure to text
T = '\n'.join(['\n'.join(T) for T in procedure_mrl])
# append articles and so on
keys = sorted(articles_mrl.keys())
for k in keys:
	t = articles_mrl[k]
	T += t

# print to file and open in browser
fN = 'tmp.html'
with open(fN,'w') as f:
	f.writelines(T)

webbrowser.open(fN)