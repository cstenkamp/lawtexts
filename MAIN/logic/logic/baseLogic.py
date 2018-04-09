import os, sys, json, re

from jsonParser import PARSER 

import numpy as np 

sys.path.insert(0, os.path.join(os.getcwd(),'logic/html_resources'))
from header import getHtmlHeader


class BaseLogic():
    def __init__(self,Product, dictParser, name, childLogics=None):
        self.path = os.path.split(os.getcwd())[0]

        self.purposesPath = os.path.join(self.path,'jsons/_purposes.json')
        self.sitesPath = os.path.join(self.path,'jsons/_sites.json')
        self.partsPath = os.path.join(self.path,'jsons/parts.json')
        self.featuresPath = os.path.join(self.path,'jsons/features.json')
        self.contentsPath = os.path.join(self.path,'jsons/contents.json')

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
        self.contents = jParser.parse(self.contentsPath)


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
        # for every site the machine should be used at:
        for site in self.Product.json['Verwendungsorte']:
            if site in self.sites:
                info = list(self.sites[site]['aktiviert'].keys())
                for dir in info:
                    self.childLogics[dir].state = True
                info = list(self.sites[site]['deaktiviert'].keys())
                for dir in info:
                    self.childLogics[dir].state = False
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
        f = {'m':1,'cm':.1,'mm':.01,'L':0.001,'m³':1}
        print(partName)
        print(entry)

        val = list(entry['Druck'].values())[0]
        content = list(entry['Inhalt'].values())[0]
        c_state = list(entry['Inhalt'].keys())[0]
        if 'Volumen' in entry:
            vol = list(entry['Volumen'].values())[0]
            vol_type = list(entry['Volumen'].keys())[0]
            # transform to meters
            vol = vol * f[vol_type]
            vol_type = 'm^3'
        else:
            l = list(entry['Länge'].values())[0]
            l_type = list(entry['Länge'].keys())[0]
            dn = list(entry['Durchmesser'].values())[0]
            dn_type = list(entry['Durchmesser'].keys())[0]

        temp = list(entry['Temperatur'].values())[0]
        temp_type = list(entry['Temperatur'].keys())[0]
        #  Diese Richtlinie gilt für die Auslegung, Fertigung und Konformitätsbewertung von 
        # Druckgeräten und Baugruppen mit einem maximal zulässigen Druck (PS) von über 0,5 bar.
        if val < 0.5:
            return False
        hidden_features = self.getHiddenFeatures(partName)
        # Dampfdruck bei der zulässigen maximalen Temperatur um mehr als 0,5 bar über dem normalen Atmosphärendruck
        steam_pressure_high = True
        content_state_i = c_state in ["gasförmig","verflüssigtes Gas","unter Druck gelöstes Gas"]
        if not content_state_i:
            content_state_i = (c_state=='flüssig') and steam_pressure_high
        content_state_ii = not content_state_i 

        fluid_features = list(entry['Inhalt']['Eigenschaften'])
        fluid_type_1 = np.any([ff in self.contents for ff in fluid_features])

        if 'DRG_a' in hidden_features:
            if (temp > 110 ) and (vol > 0.002) and (content == 'Wasser'):
                return 'Anhang II, Diagramm 5'
            else:
                if content_state_i:
                    A = ((vol > 0.001) and (val * vol > 25*val*vol*f[vol_type])) or val > 200.
                    B = ((vol > 0.001) and (val * vol > 50*val*vol*f[vol_type])) or val > 1000.
                    if A and fluid_type_1:
                        return 'Anhang II, Diagramm 1'
                    elif B and (not fluid_type_1):
                        return 'Anhang II, Diagramm 2'
                    else:
                        return 'phuck_i_a'

                if content_state_ii:
                    A = ((vol > 0.001) and (val * vol > 200*val*vol*f[vol_type])) or val > 500.
                    B = ((vol > 0.001) and (val * vol > 50*val*vol*f[vol_type])) or val > 1000.
                    if A and fluid_type_1:
                        return 'Anhang II, Diagramm 1'
                    elif B and (not fluid_type_1):
                        return 'Anhang II, Diagramm 2'
                    else:
                        return 'phuck_ii_a'


        if 'DRG_c' in hidden_features:
            if (temp > 110 ) and (vol > 0.002) and (content == 'Wasser'):
                return 'Anhang II, Diagramm 5'
            else:
                if content_state_i:
                    if (dn > 25) and fluid_type_1: 
                        return 'Anhang II, Diagramm 6'
                    elif (dn > 25) and (val*dn > 1000) and (not fluid_type_1): 
                        return 'Anhang II, Diagramm 7'
                    else:
                        return 'phuck_i_c'

                if content_state_ii:
                    if (dn > 25) (val*dn > 2000) and fluid_type_1: 
                        return 'Anhang II, Diagramm 8'
                    elif (val > 10) and (dn > 200) and (val*dn > 5000) and (not fluid_type_1): 
                        return 'Anhang II, Diagramm 9'
                    else:
                        return 'phuck_ii_c'






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
                continue
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