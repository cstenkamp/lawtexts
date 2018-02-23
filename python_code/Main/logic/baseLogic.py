import json
import re
import sys

from jsonParser import PARSER 

class BaseLogic():
    def __init__(self,Product, dictParser, name):
        self.purposesPath = 'json/_purposes.json'
        self.sitesPath = 'json/_sites.json'
        self.partsPath = 'json/parts.json'
        self.featuresPath = 'json/features.json'

        self.Product = Product
        self.dictParser = dictParser
        self.name = name
        self.state = None
        self.roleDuties = None
        self.Q = None


        '''
        load json files
        '''
        jParser = PARSER()
        self.features = jParser.parse('json/features.json')
        self.parts = jParser.parse('json/parts.json')
        self.sites = jParser.parse('json/_sites.json')
        self.purposes = jParser.parse('json/_purposes.json')



    def setState(self,B):
        self.state = B


    def checkParts(self):
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
            results[part] = f_res 
        return results


    def checkFeatures(self,part):
        results = {}
        # get features of part of product
        featDict = self.Product.json['Komponenten'][part]
        if 'Spannung' in featDict:
            B = self.checkNSR(featDict['Spannung'])
            if B:
                results['NSR'] = B
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