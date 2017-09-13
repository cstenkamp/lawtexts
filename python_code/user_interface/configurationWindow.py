import numpy as np
from tkinter import *
from tkinter.ttk import Separator, Style
import objects as obj 
from classes import *

class ConfigurationWindow(Toplevel):
    '''
    The 'ConfigurationWindow' class is a dialogue window in which users can
    specify a certain machine part. 
    Specifications are stored in the 'properties' list of the parent class
    (e.g. a 'ComponentFrame'). 
    If a known 'componentType' (machine part name as a string) is passed 
    to this class it will configure the dialogue window in a way, so that
    fields to fill out with neccessary information will be presented to
    the user. 
    If no known name string is passed the dialogue will only contain buttons
    to either confirm the input ('abschicken'), or add different properties
    (predefined in 'addPropertyFixedLabel'). 
    For each Property a 'panel' will be added to the window. Inside the panel 
    OptionMenus, Checkbuttons, and Entries can be implemented to obtain relevant
    information from the users.
    '''
    def __init__(self, parent=None, title=None, componentType=None):
        if parent == None:  
            self = Tk()
        else:
            self.parent = parent
        super(ConfigurationWindow, self).__init__(parent)
        self.geometry('{0}x{1}'.format(900,400))

        if not title is None:
            self.title(title)

        self.directives = []

        self.componentType = componentType

        # create left an right panels
        self.bottom = Canvas(self, width=500, height=100)
        self.bottom.grid(row=0, column=0, sticky=NW)

        self.top = Canvas(self, width=500, height=100, relief=GROOVE)
        self.top.grid(row=1, column=0, sticky=NW, pady=(10,10),padx=(10,10))

        # add spacer label
        spacerLabel = Label(self.top, text='', width=80)
        spacerLabel.grid(row=0, column=0, sticky=NW)

        # add plus botton to right canvas
        self.addButton = Button(self.top, text = 'Eigenschaft hinzufügen', command = lambda: self.addPropertyFixedLabel())
        self.addButton.grid(row=0, column=1,sticky=NE)

        # add ok botton to right canvas
        self.okButton = Button(self.top, text = 'abschicken', command = lambda: self.confirm())
        self.okButton.grid(row=0, column=2,sticky=NE)

        # add spacer panel to left frame
        s = Canvas(self.bottom, width = 600, height = 20)
        s.grid(row=0, column=0)

        self.openKnownComponentConfiguration()

    def deleteRow(self, row):
        del self.parent.properties[self.parent.properties.index(row)]
        row.destroy()

    def confirm(self):
        for property in self.parent.properties:
            if hasattr(property, 'propertyValue'):
                value = property.propertyValue.get()
                property.propertyValue = value

            if hasattr(property, 'propertyValueUnit'):
                unit = property.propertyValueUnit.get()
                property.propertyUnit = unit
                if not hasattr(property, 'propertyValue'):
                    property.propertyValue = property.propertyValueUnit.get()

            if hasattr(property, 'propertyValueLabel'):
                label = property.propertyValueLabel.cget('text')
                property.propertyValueLabel = label

            if hasattr(property, 'checkVar'):
                checks = property.checkVar.get()
                property.checkVar = checks

            if hasattr(property, 'options'):
                options = property.options
                property.options = options

        self.destroy()

    '''
    Panels are defined here. 
    Please make sure you use the correct type of widget (OptionMenu, Entry,...)
    for the type of input. 
    propertyValueUnit -> ['volt a/c','d/c'] or lists of fuel types etc. Need to be 
        StringVars. Use their 'trace' function to observe value changes made by user
    propertyValue -> Only Entries (i.e. text input from user)
    '''
    def addVoltagePanel(self, row):
        #row.part = Voltage()
        row.title = 'Betriebsspannung'
        # add entry to fill in volatge:
        row.propertyValue = Entry(row, text='', width=5)
        row.propertyValue.grid(row=0, column=3)
        # add label
        row.propertyValueUnit = StringVar()
        row.propertyValueUnit.set('')
        row.options = ['Volt a/c','Volt d/c']
        row.propertyValueMenu = OptionMenu(row, row.propertyValueUnit, *row.options)
        row.propertyValueMenu.grid(row=0, column=4, sticky=W, columnspan=2)
        # add checkbox for elektromagnetic interference
        row.checkVar = IntVar()
        row.checkVar.set(0)
        row.checkButton = Checkbutton(row, var=row.checkVar, 
                                text='Kann prinzipiell elektromagnetische Störungen Verursachen.',
                                justify=LEFT)
        row.checkButton.grid(row=1,column=2, columnspan=7, sticky=W)

    def addFuelPanel(self, row):
        #row.part = Voltage()
        row.title = 'Treibstoff'
        # add entry to fill in volatge:
        row.propertyValue = Entry(row, text='', width=5)
        row.propertyValue.grid(row=0, column=3)
        # add label
        row.propertyValueUnit = StringVar()
        row.propertyValueUnit.set('')
        row.options = obj.loadCSV('csv/Treibstoffe.csv')
        row.propertyValueMenu = OptionMenu(row, row.propertyValueUnit, *row.options)
        row.propertyValueMenu.grid(row=0, column=4, sticky=W, columnspan=2)
        # add checkbox for elektromagnetic interference
        row.checkVar = IntVar()
        row.checkVar.set(0)
        row.checkButton = Checkbutton(row, var=row.checkVar, 
                                text='Kann prinzipiell elektromagnetische Störungen Verursachen.',
                                justify=LEFT)
        row.checkButton.grid(row=1,column=2, columnspan=7, sticky=W)

    def addPressurePanel(self, row):
        #row.part = Pressure()
        row.title = 'Druck'
        # add entry to fill in volatge:
        row.propertyValue = Entry(row, text='', width=5)
        row.propertyValue.grid(row=0, column=3)
        # add label
        row.propertyValueUnit = StringVar()
        row.propertyValueUnit.set('bar')
        row.propertyValueLabel = Label(row, text=row.propertyValueUnit.get())
        row.propertyValueLabel.grid(row=0, column=4, sticky=W)

    def addMaxPressurePanel(self, row):
        # row.part = Pressure()
        row.title = 'Maximal zulässiger Druck'
        # add entry to fill in volatge:
        row.propertyValue = Entry(row, text='', width=5)
        row.propertyValue.grid(row=0, column=3)
        # add label
        row.propertyValueUnit = StringVar()
        row.propertyValueUnit.set('bar')
        row.propertyValueLabel = Label(row, text=row.propertyValueUnit.get())
        row.propertyValueLabel.grid(row=0, column=4, sticky=W)

    def addPressureAtMaxTemperaturePanel(self, row):
        # row.part = Pressure()
        row.title = 'Dampfdruck bei maximal zulässiger Temperatur'
        # add entry to fill in volatge:
        row.propertyValue = Entry(row, text='', width=5)
        row.propertyValue.grid(row=0, column=3)
        # add label
        row.propertyValueUnit = StringVar()
        row.propertyValueUnit.set('bar')
        row.propertyValueLabel = Label(row, text=row.propertyValueUnit.get())
        row.propertyValueLabel.grid(row=0, column=4, sticky=W)

    def addPowerPanel(self, row):
        #row.part = Wattage()
        row.title = 'Leistung'
        # add entry to fill in volatge:
        row.propertyValue = Entry(row, text='', width=5)
        row.propertyValue.grid(row=0, column=3)
        row.propertyValueUnit = StringVar()
        row.propertyValueUnit.set('')
        row.options = ['ps','watt']
        # add label
        row.propertyValueMenu = OptionMenu(row, row.propertyValueUnit, *row.options)
        row.propertyValueMenu.grid(row=0, column=4, sticky=W, columnspan=2)

    def addVolumePanel(self, row):
        #row.part = Volume()
        row.title = 'Volumen'
        # add entry to fill in volatge:
        row.propertyValue = Entry(row, text='', width=5)
        row.propertyValue.grid(row=0, column=3)
        # add label
        row.propertyValueUnit = StringVar()
        row.propertyValueUnit.set('m^3')
        row.propertyValueLabel = Label(row, text=row.propertyValueUnit.get())
        row.propertyValueLabel.grid(row=0, column=4, sticky=W)

    def addPipeLengthPanel(self, row):
        #row.part = Volume()
        row.title = 'Länge'
        # add entry to fill in volatge:
        row.propertyValue = Entry(row, text='', width=5)
        row.propertyValue.grid(row=0, column=3)
        # add label
        row.propertyValueUnit = StringVar()
        row.propertyValueUnit.set('m')
        row.propertyValueLabel = Label(row, text=row.propertyValueUnit.get())
        row.propertyValueLabel.grid(row=0, column=4, sticky=W)

    def addPipeDiameterPanel(self, row):
        #row.part = Volume()
        row.title = 'Durchmesser'
        # add entry to fill in volatge:
        row.propertyValue = Entry(row, text='', width=5)
        row.propertyValue.grid(row=0, column=3)
        # add label
        row.propertyValueUnit = StringVar()
        row.propertyValueUnit.set('cm')
        row.propertyValueLabel = Label(row, text=row.propertyValueUnit.get())
        row.propertyValueLabel.grid(row=0, column=4, sticky=W)

    def addContentPanel(self, row):
        #row.part = Content()
        row.title = 'Inhalt'
        # add entry to fill in volatge:
        row.propertyValue = StringVar()
        row.propertyValue.set('Inhalt')
        row.propertyValueUnit = StringVar()
        row.propertyValueUnit.set('')
        row.options = obj.loadCSV('csv/Materialien.csv')
        row.propertyValueUnit.trace('w', lambda *args: self.specifyContentPanel(row))
        # add label
        #row.label = Label(row, text='Inhalt: ')
        #row.label.grid(row=0, column=3)
        row.propertyValueMenu = OptionMenu(row, row.propertyValueUnit, *['--andere--']+sorted(list(row.options.keys())))
        row.propertyValueMenu.grid(row=0, column=3, sticky=W, columnspan=8)
        row.contentState = StringVar()
        row.contentState.set('')
        ts = ['fest', 'flüssig', 'gas förmig']
        vs = ts
        for ix in range(len(ts)):
            radiobutton = Radiobutton(row, text=ts[ix], value=vs[ix], variable=row.contentState)
            radiobutton.grid(row=1, column = 3+ix, sticky=W, columnspan=1)

    # If a unknown content is added it can be further specified (flammable, toxic...) here

    def specifyContentPanel(self, row):
        if row.propertyValueUnit.get() == '--andere--':
            row.contentSpecifier = StringVar()
            row.contentSpecifier.set('')
            row.specifier = obj.loadCSV('csv/Eigenschaften.csv')
            options = ['--andere--']+sorted(list(row.specifier.keys()))
            row.contentSpecifierMenu = OptionMenu(row, row.contentSpecifier, *options)
            row.contentSpecifierMenu.grid(row=2, column=4, sticky=W, columnspan=3)
            row.label2 = Label(row, text='Eigenschaft: ')
            row.label2.grid(row=2, column=3, sticky=W)


    def addTemperaturePanel(self, row):
        #row.part = Temperature()
        row.title = 'Temperatur'
        # add entry to fill in volatge:
        row.propertyValue = Entry(row, text='', width=5)
        row.propertyValue.grid(row=0, column=3)
        # add label
        row.propertyValueUnit = StringVar()
        row.propertyValueUnit.set('grad celsius')
        row.propertyValueLabel = Label(row, text=row.propertyValueUnit.get())
        row.propertyValueLabel.grid(row=0, column=4, sticky=W)


    def addConditionalVoltagePanel(self, row):
        if row.checkVar1.get() == 1 and row.checkVar2.get() == 1 and row.checkVar3.get() == 1:
            # row.part = Voltage()
            Label(row, text='Betriebsspannung').grid(row = 4,column=2)
            row.title = 'Betriebsspannung'
            # add entry to fill in volatge:
            row.propertyValue = Entry(row, text='', width=5)
            row.propertyValue.grid(row=4, column=3)
            # add label
            row.propertyValueUnit = StringVar()
            row.propertyValueUnit.set('')
            row.options = ['Volt a/c', 'Volt d/c']
            row.propertyValueMenu = OptionMenu(row, row.propertyValueUnit, *row.options)
            row.propertyValueMenu.grid(row=4, column=4, sticky=W, columnspan=2)
            # add checkbox for elektromagnetic interference
            row.checkVar = IntVar()
            row.checkVar.set(0)
            row.checkButton = Checkbutton(row, var=row.checkVar,
                                          text='Kann prinzipiell elektromagnetische Störungen Verursachen.',
                                          justify=LEFT)
            row.checkButton.grid(row=8, column=2, columnspan=7, sticky=W)

    def addMachinePanel(self, row):
        #row.part = Temperature()
        row.title = 'MRL'        
        row.checkVar1 = IntVar()
        row.checkVar1.set(0)
        row.checkVar1.trace('w',lambda *args: self.addConditionalVoltagePanel(row))
        row.checkButton1 = Checkbutton(row, var=row.checkVar1, 
                                text='Betseht aus miteinander verbundenen Teilen mit mindestens einem beweglichen Teil',
                                justify=LEFT)
        row.checkButton1.grid(row=0,column=2, columnspan=7, sticky=W)

        row.checkVar2 = IntVar()
        row.checkVar2.set(0)
        row.checkButton2 = Checkbutton(row, var=row.checkVar2, 
                                text='Kann für sich genommen die bestimmte Anwendung erfüllen',
                                justify=LEFT)
        row.checkButton2.grid(row=1,column=2, columnspan=7, sticky=W)

        row.checkVar3 = IntVar()
        row.checkVar3.set(0)
        row.checkVar3.trace('w',lambda *args: self.addConditionalVoltagePanel(row))
        row.checkButton3 = Checkbutton(row, var=row.checkVar3,

                                text='Ist eine mit einem anderen Antriebssystem als der unimttelbar eingestetzen menschlichen oder tierischen Kraft ausgestattet',
                                justify=LEFT)
        row.checkButton3.grid(row=2,column=2, columnspan=7, sticky=W)



    def valueChosen(self, row):
        if hasattr(row, 'propertyValue'):
            if isinstance(row.propertyValue, StringVar):
                del row.propertyValue
            else:
                row.propertyValue.destroy()
        if hasattr(row, 'propertyValueUnit'):
            del row.propertyValueUnit
        if hasattr(row, 'propertyValueMenu'):
            row.propertyValueMenu.destroy()
        if hasattr(row, 'options'):
            del row.options
        if hasattr(row, 'checkVar'):
            del row.checkVar
            row.checkButton.destroy()
        if hasattr(row, 'propertyValueLabel'):
            row.propertyValueLabel.destroy()
        '''
        for each possible property define what kind of panel to open here
        '''
        if row.propertyName.get() == 'Betriebsspannung':
            self.addVoltagePanel(row)
        if row.propertyName.get() == 'Druck':
            self.addPressurePanel(row)
        if row.propertyName.get() == 'Maximal zulässiger Druck':
            self.addMaxPressurePanel(row)
        if row.propertyName.get() == 'Dampfdruck bei maximal zulässiger Temperatur':
            self.addPressurePanel(row)
        if row.propertyName.get() == 'Temperatur':
            self.addTemperaturePanel(row)
        if row.propertyName.get() == 'Inhalt':
            self.addContentPanel(row)
        if row.propertyName.get() == 'Volumen':
            self.addVolumePanel(row)
        if row.propertyName.get() == 'Leistung':
            self.addPowerPanel(row)
        if row.propertyName.get() == 'Durchmesser':
            self.addPipeDiameterPanel(row)
        if row.propertyName.get() == 'Länge':
            self.addPipeLengthPanel(row)


    def addPropertyFixedLabel(self, label=None):
        row = Frame(self.bottom, relief=GROOVE)
        self.parent.properties.append(row)
        row.grid(row=self.bottom.grid_size()[1], column=0, pady=10, padx=10, sticky=NW)

        # empty spacer label
        for r in range(0,11):
            if r==2:
                spacerLabel = Label(row, text='', width=20)
            else:
                spacerLabel = Label(row, text='', width=5)
            spacerLabel.grid(row=0, column=r)

        if label is None or label is '--andere--':
            row.label = Label(row, text='Eigenschaft: ', width=11)
            row.label.grid(row=0, column=0, sticky = W)
            options = sorted(list(['Inhalt','Volumen', 'Leistung', 'Temperatur','Druck', 'Betriebsspannung', 'Durchmesser', 'Länge']))
            row.propertyName = StringVar()
            row.propertyName.set('')
            row.propertyName.trace('w', lambda    *args: self.valueChosen(row))
            row.om = OptionMenu(row, row.propertyName, *options)
            row.om.grid(row=0, column=2, sticky=W)
        else:
            spacerLabel = Label(row, text='', width=11)
            spacerLabel.grid(row=0, column=1, sticky = W)
            # label
            row.propertyLabel = Label(row, text=label, width = 20, justify=LEFT, anchor=W)
            row.propertyLabel.grid(row=0, column=2, sticky = W)
            # create more empty spacer labels:
        # create another spacer panel
        c2 = Canvas(row, width=60, height=5)
        c2.grid(row=0, column=3, sticky=E)
        c3 = Canvas(row, width=70, height=5)
        c3.grid(row=0, column=4, sticky=E)
        # create button to delete row
        row.button = Button(row, text = '-', command = lambda: self.deleteRow(row))
        row.button.grid(row=0, column=11, sticky=E, padx = (50,0))
        return row 

    '''
    Defines a list of panels that need to be added for any given known machine part
    (name string)
    '''
    def openKnownComponentConfiguration(self):
        # if component type is 
        if self.componentType == 'Elektromotor':
            initRows = ['Betriebsspannung','Leistung']

        elif self.componentType == 'Verbrennungsmotor':
            initRows = ['Treibstoff','Leistung']

        elif self.componentType == 'Behälter':
            initRows = ['Inhalt','Volumen','Maschine']

        elif self.componentType == 'Verdichter':
            initRows = ['Inhalt','Volumen']

        elif self.componentType == 'Dampferzeuger (Kessel)':
            initRows = ['Maschine','Inhalt','Maximal zulässiger Druck','Dampfdruck bei maximal zulässiger Temperatur']


        elif self.componentType == 'Rührwerk':
            initRows = ['Inhalt','Volumen','Betriebsspannung','Leistung']

        elif self.componentType == 'Rohrleitung':
            initRows = ['Durchmesser','Länge','Druck','Temperatur','Inhalt']

        elif self.componentType == 'Druckrohr':
            initRows = ['Inhalt','Druck','Länge','Durchmesser']
        else:
            initRows = []


        for init in initRows:
            row = self.addPropertyFixedLabel(label=init)
            if init == 'Inhalt':
                self.addContentPanel(row)
            if init == 'Leistung':
                self.addPowerPanel(row)
            if init == 'Druck':
                self.addPressurePanel(row)
            if init == 'Durchmesser':
                self.addPipeDiameterPanel(row)
            if init == 'Länge':
                self.addPipeLengthPanel(row)
            if init == 'Betriebsspannung':
                self.addVoltagePanel(row)
            if init == 'Temperatur':
                self.addTemperaturePanel(row)
            if init == 'Volumen':
                self.addVolumePanel(row)
            if init == 'Maschine':
                self.addMachinePanel(row)








'''
root = Tk()
c1 = ConfigurationWindow(parent = root, title = 'Motor', componentType = 'Motor')
c2 = ConfigurationWindow(parent = root, title = 'Behälter', componentType = 'Behälter')
c2 = ConfigurationWindow(parent = root, title = 'Kessel', componentType = 'Kessel')
'''