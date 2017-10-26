from objects import *
from pressureDecisionTrees import pressureMainTree


class Directive():
    def __init__(self, title, id_string, parent=None):
        self.title = title
        self.id_string = id_string
        self.active = False
        self.parent = parent

        f_name = 'csv/Verwendungszwecke.csv'
        purposes = loadCSV(f_name)
        f_name = 'csv/Verwendungsorte.csv'
        sites = loadCSV(f_name)

        self.includingPurposes, self.excludingPurposes = self.getInExcludingX(purposes)
        self.includingSites, self.excludingSites = self.getInExcludingX(sites)

    def getInExcludingX(self, X):
        Excluding = []
        Including = []
        for x in X.keys():
            v = X[x]
            excluding = v.excluding_directives.keys()
            including = v.including_directives.keys()

            if self.id_string in excluding:
                Excluding.append(x)
            if self.id_string in including:
                Including.append(x)
        return Including, Excluding

    def checkApplicabilityOnPurpose(self, purpose):
        if purpose in self.excludingPurposes:
            self.active = False
            print('{0} trifft nicht auf Verwendungszweck zu'.format(self.title))
        if purpose in self.includingPurposes:
            self.active = True
            print('{0} trifft auf Verwendungszweck zu'.format(self.title))
        if purpose in self.includingPurposes and purpose in self.excludingPurposes:
            print('ERROR')

    def checkApplicabilityOnSite(self, site):
        if site in self.excludingSites:
            self.active = False
            print('{0} trifft nicht auf Verwendungsort zu'.format(self.title))
        if site in self.includingSites:
            self.active = True
            print('{0} trifft auf Verwendungsort zu'.format(self.title))
        if site in self.includingSites and site in self.excludingSites:
            print('ERROR')





class LowVoltageDirective(Directive):
    def __init__(self):
        super(LowVoltageDirective,self).__init__('Niederspannungsrichtlinie','2014/35/EU')
        self.acRange = [50,1000]
        self.dcRange = [75,1500]

    def checkMachine(self, machine):
        self.machine = machine
        for ix,component in enumerate(self.machine.components):
            print('')
            print('+---------------------------------------------------------+')
            print('Niederspannungsrichtlinie ')
            print('Überprüfe Komponente: {0}'.format(component.name))
            self.checkComponent(component)
            print('+---------------------------------------------------------+')
            print('')


    def checkComponent(self, component):
        for ix,feature in enumerate(component.features):
            if feature.name == 'Betriebsspannung':
                current_type = feature.values['unit']
                voltage = float(feature.values['value'])
                if current_type == 'Volt AC':
                    if self.acRange[0] < voltage < self.acRange[1]:
                        self.active = True
                        print('     NSR aktiviert durch Eigenschaft {0}'.format(feature.name))
                elif current_type == 'Volt DC':
                    if self.dcRange[0] < voltage < self.dcRange[1]:
                        self.active = True
                        print('     NSR aktiviert durch Eigenschaft {0}'.format(feature.name))



class PressureEquipmentDirective(Directive):
    def __init__(self):
        super(PressureEquipmentDirective,self).__init__('Druckgeräte-Norm','2014/68/EU')
        self.category = None
        self.group = None

    def checkMachine(self,machine):
        self.machine = machine
        print('')
        print('+---------------------------------------------------------+')
        print('Druckgeräte-Norm ')
        for ix,component in enumerate(self.machine.components):
            print('Überprüfe Komponente: {0}'.format(component.name))
            pressure_device_type, group, result, message = self.decideComponentCategory(component)
            if group is None:
                print(result)
                print(message)
                print('+---------------------------------------------------------+')
                print('')
                continue
            print('         Art des Gerätes: {0}'.format(pressure_device_type)) 
            print('         Geräte Gruppe: {0}'.format(group))
            print('         Nachricht: {0}'.format(message))
            print('         siehe: {0}'.format(result))
            print('+---------------------------------------------------------+')
            print('')



    def convertToBar(self,unit,value):
        if unit == 'bar':
            return value 
        if unit == 'Pa':
            return value * 10**(-5)
        if unit == 'at':
            return value * (9.8067 * 10**-1)
        if unit == 'atm':
            return value * (1.0133 * 10**0)
        if unit == 'Torr':
            return value * (1.3332 * 10**-3)
        if unit == 'psi':
            return value * (6.8948 * 10**-2)


    def decideComponentCategory(self,machineComponent):
        skip = True
        for feature in machineComponent.features:
            if feature.name == 'Druck':
                skip = False
        if skip:
            print('Druckgeräte-Norm trifft nicht zu')
            return None, None, None, None

        pressure_device_type = None

        badFeatures = ['entzündbar','instabil/explosiv','selbstzersetzlich','pyropher',
        'oxidierend','akut_toxisch','organisches_Peroxid','ätzend']

        componentName = machineComponent.name

        pressure = None
        volume = None
        diameter = None
        temperature = None
        content = None
        contentFeatures = None
        stateOfMatter = None

        result = 'none'
        message = 'none'

        group = None

        for feature in machineComponent.features:
            if feature.name == 'Druck':
                pressure = float(feature.values['value'])
                unit = feature.values['unit']
                pressure = self.convertToBar(unit, pressure)
            #
            if feature.name == 'Volumen':
                volume = float(feature.values['value'])
            #
            if feature.name == 'Durchmesser':
                diameter = float(feature.values['value'])
            #
            if feature.name == 'Temperatur':
                temperature = float(feature.values['value'])
            #
            if feature.name == 'Inhalt':
                content = feature.values['content']
                contentFeatures = feature.values['specifications']
                stateOfMatter = feature.values['stateOfMatter']



        if not diameter is None:
            result = "Druckbehälter"
            message = "Anlage fällt unter'Druckbehälter nach 2014/68/EU'" 

        if not volume is None:
            if pressure <= 30 and (volume*pressure) <= 10000:
                pressure_device_type = "Einfacher Druckbehälter"
                message = "Einfacher Druckbehälter nach 2014/29/EU"  
            elif pressure > 30 and volume*pressure <= 10000:
                pressure_device_type = "Druckbehälter"
                message ="Der maximal zulässige Druck ist größer als 30 bar. Daher fällt die Anlage unter 'Druckbehälter nach 2014/68/EU'"
            elif volume*pressure > 10000 and pressure <= 30:
                pressure_device_type = "Druckbehälter"
                message ="PS * V ist größer als 10.000. Daher fällt die Anlage unter 'Druckbehälter nach 2014/68/EU'" 
            elif volume*pressure > 10000 and pressure >30:
                pressure_device_type = "Druckbehälter"
                message = "Der maximal zulässige Druck ist größer als 30 bar und PS * V ist größer als 10.000. Daher fällt die Anlage unter 'Druckbehälter nach 2014/68/EU'"
        

        if not diameter is None:
            print('Komponente ist/hat eine Rohrleitung')
            if temperature is None:
                print('bitte Temperatur angeben')
            elif temperature > 110:
                message = 'Anlage fällt unter "Druckbehälter nach 2014/68/EU"'
            else:
                message = 'Die maximale Dampftemperatur liegt nicht über 110°C. Somit fällt die Anlage nicht unter die Druckgeräterichtlinie, Artikel 3.'
                return pressure_device_type,group,result,message
        

        tmp = [(cf in badFeatures) for cf in contentFeatures]
        if any(tmp):
            group = 1
        else:
            group = 2


        if diameter is None and not volume is None:
            result = pressureMainTree(componentName,stateOfMatter,group,pressure,volume)
        if volume is None and not diameter is None:
            result = pressureMainTree(componentName,stateOfMatter,group,pressure,diameter)

        return pressure_device_type,group,result,message




class ATEXDirective(Directive):
    def __init__(self):
        super(ATEXDirective,self).__init__('Atex','2014/34/EU')
