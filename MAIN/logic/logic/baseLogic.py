import os, sys, json, re

from jsonParser import PARSER 

sys.path.insert(0, os.path.join(os.getcwd(),'logic/html_resources'))
from header import getHtmlHeader


class BaseLogic():
    def __init__(self,Product, dictParser, name, childLogics=None):
        self.path = os.path.split(os.getcwd())[0]

        self.purposesPath = os.path.join(self.path,'jsons/_purposes.json')
        self.sitesPath = os.path.join(self.path,'jsons/_sites.json')
        self.partsPath = os.path.join(self.path,'jsons/parts.json')
        self.featuresPath = os.path.join(self.path,'jsons/features.json')

        self.Product = Product
        self.dictParser = dictParser
        self.name = name
        self.state = None
        self.roleDuties = None
        self.Q = None
        self.childLogics = childLogics


        '''
        load json files
        '''
        jParser = PARSER()
        self.features = jParser.parse(self.featuresPath)
        self.parts = jParser.parse(self.partsPath)
        self.sites = jParser.parse(self.sitesPath)
        self.purposes = jParser.parse(self.purposesPath)

        self.ac_high = 1000
        self.ac_low  = 50

        self.dc_high = 1000
        self.dc_low  = 50


        self.headerString = getHtmlHeader()
        self.componentString = '<h3>{0}</h3>'
        self.componentResultString = '<p class = "tab"><b> {0}: </b> {1} </p>'


    def setRole(self,role):
        self.Product.role = role 

    def setState(self,B):
        self.state=B

    def checkSites(self):
        results = {}

    def checkParts(self,overwrite=True):
        results = {}
        # for every part in the machine
        for part in self.Product.json['Komponenten']:
            # see if you find information in your knowledge base
            _f_res = {}
            if part in self.parts:
                # check possible hidden features
                _f_res = self.checkHiddenFeatures(part)
            # check each of the features
            f_res = self.checkFeatures(part)
            # overwrite results of feature check with check of hidden features
            if not _f_res is None:
                for _f,_v in _f_res.items():
                    f_res[_f] = _v
            if overwrite:
                # see, if directive is already deactivated by purpose,site etc.
                for d,s in f_res.items():
                    dState = self.childLogics[d].state
                    if (not dState) and (s):
                        f_res[d] = False
            else:           
                # see if part activates directive     
                for d,s in f_res.items():
                    if s:
                        self.childLogics[d].state = True
            results[part] = f_res 
        return results

    def checkVoltage(self,val,type):
        type = type.lower()
        type = type.split(' ')[1]
        if type == 'ac':
            if self.ac_low < val < self.ac_high:
                return True
            else:
                return False
        elif type == 'dc':
            if self.dc_low < val < self.dc_high:
                return True
            else:
                return False
        else:
            print('unknown voltage type. Must either be "ac" or "dc"')


    def checkPressure(self,entry,partName):
        val = list(entry['Druck'].values())[0]
        content = list(entry['Inhalt'].values())[0]
        c_state = list(entry['Inhalt'].keys())[0]
        vol = list(entry['Volumen'].values())[0]
        vol_type = list(entry['Volumen'].keys())[0]
        temp = list(entry['Temperatur'].values())[0]
        temp_type = list(entry['Temperatur'].keys())[0]

        if val < 0.5:
            return True
        else:
            return False


    def resultsToHtml(self,results):
        html = self.headerString
        for part, dRes in results.items():
            a = self.componentString.format(part)
            for directive, res in dRes.items():
                if res:
                    res = 'trifft zu'
                else:
                    res = 'trifft nicht zu'
                b = self.componentResultString.format(directive,res)
                a += b
            html += a
        return html 


    def checkFeatures(self,part):
        results = {}
        # get features of part of product
        featDict = self.Product.json['Komponenten'][part]
        for entry in featDict:
            if 'Spannung' in entry:
                t = list(entry['Spannung'].keys())[0]
                val = list(entry['Spannung'].values())[0]
                B = self.checkVoltage(val,t)
                if B:
                    results['NSR'] = B
            if 'Druck' in entry:
                B = self.checkPressure(entry,part)
                if B:
                    results['DGR'] = B
        #html = self.resultsToHtml(results)
        return results



    def checkHiddenFeatures(self,part):
        results = {}
        _feat = self.getHiddenFeatures(part)
        if _feat is None:
            return 
        for f in _feat:
            if f.startswith('+'):
                results[f[1:]] = True
            if f.startswith('-'):
                results[f[1:]] = False
            return results


    def getHiddenFeatures(self,part):
        if part in self.parts:
            return self.parts[part]['_Eigenschaften']

    def finalize(self):
        return ''