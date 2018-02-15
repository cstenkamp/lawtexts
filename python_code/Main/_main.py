import sys, os, webbrowser
from pprint import pprint as print
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

sys.path.insert(0, os.path.join(os.getcwd(),'dict_parser/'))
from dictParser import PARSER as dictPARSER

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


dictParser = dictPARSER(APPENDICES,ARTICLES)

Product = Machine()

"""
add machineData to Product
"""

configurator = Configurator(Product)
configurator.configure(machineData)



Logic = LOGIC(Product, dictParser)

'''
LINUS: 
'''
# first check first level features, such as purpose and site:
result_purpose, result_sites = Logic.checkFirstLevel()

# proceed checking by asking questions to user. skip, if directive is already deactivated
for D,v in result_purpose.items():
	if Logic.directiveStates[D]:
		q = v['user_questions']
		if q == {}:
			continue
		else:
			for p,l in q:
				# display questions and collect answers
				purpose = p 
				for head,label in l:
					body = Logic.labelToHtml(label,D)
				# head = e.g. Finden sie ihr Produkt in dieser Liste wieder?
				# body = e.g. text of appendix 7
				pass

# proceed by checking applicability of directive to every single part
parts_results = Logic.checkParts()

# if parts deactivate directive, but directive is already deactivated by purpose
# deactivate directive in part
# if there is no verdict for a directive (None), set it to verdict of part
for part, res in parts_results.items():
	for D,state in res.items():
		if Logic.directiveStates[D] is False:
			state = False
		elif Logic.directiveStates[D] is None:
			Logic.directiveStates[D] = state
			Logic.stateExplanation[D].append(part)


'''
questions that need to be asked if a directive is activated
'''
if Logic.directiveStates['MRL']:
	# get questions regarding MRL
	q_head, q_body, procedures, headers = Logic.getMRLProcedure()
	# get user answer
	answer = 'yes'#/'no'
	# set question results
	header, procedure = Logic.setMRLProcedure(answer, headers, procedures)

if Logic.directiveStates['NSR']:
	pass

if Logic.directiveStates['DGN']:
	pass

