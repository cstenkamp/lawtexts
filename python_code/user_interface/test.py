import numpy as np
from tkinter import *
from tkinter.ttk import Separator, Style
import objects as obj 
from classes import *

class ConfigurationWindow(Toplevel):
    def __init__(self, parent=None):
        if parent == None:  
            self.parent = Tk()
        else:
            self.parent = parent

        super(ConfigurationWindow, self).__init__(parent)
        self.geometry('{0}x{1}'.format(800,400))

        self.rows = []

        # create left an right panels
        self.left = Canvas(self, width=500, height=100)
        self.left.grid(row=0, column=0, sticky=NW)

        self.right = Canvas(self, width=200, height=100)
        self.right.grid(row=0, column=1, sticky=NW)

        # add plus botton to right canvas
        self.addButton = Button(self.right, text = '+', command = lambda: self.addRow())
        self.addButton.grid(row=0, column=0,sticky=NE)

        # add ok botton to right canvas
        self.okButton = Button(self.right, text = 'abschicken', command = lambda: self.confirm())
        self.okButton.grid(row=0, column=1,sticky=NE)

        # add spacer panel to left frame
        s = Canvas(self.left, width = 600, height = 20)
        s.grid(row=0, column=0)

        self.addRow()

    def addRow(self):
        row = Frame(self.left, relief=GROOVE)
        self.rows.append(row)
        row.grid(row=self.left.grid_size()[1], column=0, pady=10, padx=10, sticky=NW)
        # label
        row.label = Label(row, text='Eigenschaft: ')
        row.label.grid(row=0, column=0, sticky = W)
        # create spacer panel
        c1 = Canvas(row, width=300, height=0,)
        c1.grid(row=0, column=1, sticky=W)
        # create optionmenu
        options = sorted(list(['Inhalt','Volumen', 'Leistung', 'Temperatur','Druck', 'Betriebsspannung']))
        row.propertyName = StringVar()
        row.propertyName.set('')
        row.propertyName.trace('w', lambda    *args: self.valueChosen(row))
        row.om = OptionMenu(row, row.propertyName, *options)
        row.om.grid(row=0, column=1, sticky=W)
        # create another spacer panel
        c2 = Canvas(row, width=60, height=5)
        c2.grid(row=0, column=3, sticky=E)
        c3 = Canvas(row, width=70, height=5)
        c3.grid(row=0, column=4, sticky=E)
        # create button to delete row
        row.button = Button(row, text = '-', command = lambda: self.deleteRow(row))
        row.button.grid(row=0, column=5, sticky=E, padx = (50,0))
        return row 

    def deleteRow(self, row):
        del self.rows[self.rows.index(row)]
        row.destroy()

    def confirm(self):
        self.destroy()

    def addVoltagePanel(self, row):
        row.part = Voltage()
        # add entry to fill in volatge:
        row.propertyValue = Entry(row, text='', width=5)
        row.propertyValue.grid(row=0, column=3)
        # add label
        row.propertyValueLabel = Label(row, text='Volt')
        row.propertyValueLabel.grid(row=0, column=4, sticky=W)
        # add checkbox for elektromagnetic interference
        row.checkVar = IntVar()
        row.checkVar.set(0)
        row.checkButton = Checkbutton(row, var=row.checkVar, 
                                text='Kann prinzipiell elektromagnetische Störungen Verursachen.',
                                justify=LEFT)
        row.checkButton.grid(row=1,column=0, columnspan=4, sticky=W)

    def addPressurePanel(self, row):
        row.part = Pressure()
        # add entry to fill in volatge:
        row.propertyValue = Entry(row, text='', width=5)
        row.propertyValue.grid(row=0, column=3)
        # add label
        row.propertyValueLabel = Label(row, text='bar')
        row.propertyValueLabel.grid(row=0, column=4, sticky=W)

    def addPowerPanel(self, row):
        row.part = Wattage()
        # add entry to fill in volatge:
        row.propertyValue = Entry(row, text='', width=5)
        row.propertyValue.grid(row=0, column=3)
        row.propertyValueUnit = StringVar()
        row.propertyValueUnit.set('')
        row.options = ['ps','watt']
        # add label
        row.propertyValueLabel = OptionMenu(row, row.propertyValueUnit, *row.options)
        row.propertyValueLabel.grid(row=0, column=4, sticky=W, columnspan=2)

    def addVolumePanel(self, row):
        row.part = Volume()
        # add entry to fill in volatge:
        row.propertyValue = Entry(row, text='', width=5)
        row.propertyValue.grid(row=0, column=3)
        # add label
        row.propertyValueLabel = Label(row, text='m^3')
        row.propertyValueLabel.grid(row=0, column=4, sticky=W)

    def addContentPanel(self, row):
        row.part = Content()
        # add entry to fill in volatge:
        row.propertyValue = StringVar()
        row.propertyValue.set('')
        row.options = sorted(list(obj.loadCSV('csv/Materialien.csv').keys()))
        # add label
        row.propertyValueLabel = OptionMenu(row, row.propertyValue, *row.options)
        row.propertyValueLabel.grid(row=0, column=3, sticky=W, columnspan=3)

    def addTemperaturePanel(self, row):
        row.part = Content()
        # add entry to fill in volatge:
        row.propertyValue = Entry(row, text='', width=5)
        row.propertyValue.grid(row=0, column=3)
        # add label
        row.propertyValueLabel = Label(row, text='grad celsius')
        row.propertyValueLabel.grid(row=0, column=4, sticky=W)



    def valueChosen(self, row):
        if hasattr(row, 'propertyValue'):
            row.propertyValue.destroy()
            row.propertyValueLabel.destroy()
        if row.propertyName.get() == 'Betriebsspannung':
            self.addVoltagePanel(row)
        if row.propertyName.get() == 'Druck':
            self.addPressurePanel(row)
        if row.propertyName.get() == 'Temperatur':
            self.addTemperaturePanel(row)
        if row.propertyName.get() == 'Inhalt':
            self.addContentPanel(row)
        if row.propertyName.get() == 'Volumen':
            self.addVolumePanel(row)
        if row.propertyName.get() == 'Leistung':
            self.addPowerPanel(row)
