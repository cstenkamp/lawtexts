from tkinter import *
from configurationWindow import *
from classes import *
from directives import *
from interfaces import *

from tkinter.ttk import Separator, Style
import objects as obj 

class ComponentFrame(Frame):
    '''
    The ComponentFrame class adds a row in the main window where the user can
    add a part to the machine. 
    It offers a button to dele the row and to call another interface to further
    specify the part. 
    Specifications are stored in  'self.properties'. They are added in the 
    'ConfigurationWindow' class.
    '''
    def __init__(self, parent):
        super(ComponentFrame, self).__init__(parent)
        self.parent = parent
        self.properties = []

        self.directives = []
        self.grid(row = len(parent.COMPONENTS)+3, columnspan = 3, sticky = W)
        # add label to frame 
        self.label = Label(self, text = 'Komponente: {0}'.format(len(self.parent.COMPONENTS)))
        self.label.grid(row = 0, column = 0, sticky = W)
        # add options menu to frame
        self.componentName = StringVar()
        self.componentName.set('')
        self.componentName.trace('w', lambda *args: self.optionSet())
        options = ['--andere--']+sorted(list(parent.components.keys()))
        self.menu = OptionMenu(self, self.componentName, *options)
        self.menu.grid(row = 0, column = 1, sticky = W)
        # add configuration button
        self.confButton = Button(self, text = 'konfigurieren', command = self.configure)        
        self.confButton.grid(row = 0, column = 2, sticky = W)
        # add minus sign button to delete frame
        self.deleteButton = Button(self, text = '-', command = self.delete)
        self.deleteButton.grid(row = 0, column = 3, sticky = W)
        # add whole frame to parent
        self.parent.COMPONENTS.append(self)


    def delete(self):
        del self.parent.COMPONENTS[self.parent.COMPONENTS.index(self)]
        self.destroy()


    def configure(self):
        self.componentConfiguration = ConfigurationWindow(self,title=self.componentName.get(), componentType=self.componentName.get())


    def optionSet(self):
        self.configure()

class main(Tk):
    def __init__(self):
        super(main, self).__init__()
        '''
        Load directives.
        The directive classes have dictionairies containing key-value pairs
        of machine parts, lists of possible operation sites, contents for
        tanks, etc. and directive id strings (e.g. 26/96/EG) with an additional
        '+' or '-' symbol indicating, whether the e.g. machine part activates
        or deactivates a directive.
        Further directives implement methods to check their applicability to
        a certain component specified by the user.
        '''
        self.lvd = LowVoltageDirective(parent=self)
        self.emc = ElectromagneticCompatibilityDirective(parent=self)
        self.mrl = MachineryDirective(parent=self)
        self.atex = ATEXDirective(parent=self)

        '''
        Load lists of purposes, sites etc.
        '''
        self.cur_row = 3
        self.purposes = obj.loadCSV('csv/verwendungszwecke.csv')
        self.sites = obj.loadCSV('csv/verwendungsorte.csv')
        self.products = obj.loadCSV('csv/Erzeugnisse.csv')
        self.components = obj.loadCSV('csv/confirmed_komponenten.csv')
        self.deviceCategories = obj.loadCSV('csv/Kategorien.csv')

        self.DIRECTIVES = []

        # components of the machine will be stored in here.
        # Components are of type 'ComponentFrame' (see above class)
        self.COMPONENTS = []


        self.root = Tk()
        self.root.title('test')
        self.frame = Canvas(self.root, height = 1200, width = 800)
        #self.frame.create_line(0,167,600,167, width=2)
        self.frame.grid(row = 0, column = 0, pady = (10,10), ipadx = 100)

        Label(self.frame, text = 'Art des Erzeugnisses:').grid(row = 0,sticky = W, padx = (10,10))
        self.productVar = StringVar()
        self.productVar.set('')
        self.productVar.trace('w', lambda *args: [self.mrl.openProductDialog(), self.atex.openProductDialog()])
        options = ['--andere--'] + sorted(list(self.products.keys()))
        self.productOption = OptionMenu(self.frame, self.productVar, *options)
        self.productOption.grid(row = 0, column  = 1,sticky = W, columnspan = 2, pady = (10,10))

        Label(self.frame, text = 'Verwendungsort:').grid(row = 1,sticky = W, padx = (10,10))
        self.siteVar = StringVar()
        self.siteVar.set('')
        options = ['--andere--'] + list(np.sort(list(self.sites.keys())))
        self.siteOption = OptionMenu(self.frame, self.siteVar, *options)
        self.siteOption.grid(row = 1, column  = 1,sticky = W, columnspan = 2, pady = (10,10))

        Label(self.frame, text = 'Verwendungszweck:').grid(row = 2,sticky = W, padx = (10,10))
        self.purposeVar = StringVar()
        self.purposeVar.set('')
        options = ['--andere--'] + list(np.sort(list(self.purposes.keys())))
        self.purposeOption = OptionMenu(self.frame, self.purposeVar, *options)
        self.purposeOption.grid(row = 2, column  = 1,sticky = W, columnspan = 2, pady = (10, 10))

        Label(self.frame, text = 'Anlage ist durch Beschäftigte zu bedienen oder überwachen? ').grid(row = 3,sticky = W, padx = (10,10))
        self.operationalSafetyVar = StringVar()
        self.operationalSafetyVar.set('')
        options = ['ja','nein']
        self.purposeOption = OptionMenu(self.frame, self.operationalSafetyVar, *options)
        self.purposeOption.grid(row = 3, column  = 1,sticky = W, columnspan = 2, pady = (10, 10))


        button = Button(self.root, text = 'Komponente hinzufügen', command = lambda: [ComponentFrame(self)])
        button.grid(row = 0, column = 5,sticky = W+S)

        button2 = Button(self.root, text = 'abschicken', command = lambda: self.finalize())
        button2.grid(row = 0, column = 6,sticky = W+S)
        self.mainloop()


    def finalize(self):
        print('-='*5)
        print('FINAL VERDICT: ')
        if hasattr(self, 'MachineryInterfaceVars'):
            self.mrl.checkApplicabilityOnProduct()
        if hasattr(self, 'ATEXInterfaceVars'):
            self.atex.checkApplicabilityOnProduct()
        self.lvd.check(self.siteVar.get(), self.purposeVar.get(), self.COMPONENTS)
        self.emc.check(self.siteVar.get(), self.purposeVar.get(), self.COMPONENTS)
        self.mrl.check(self.siteVar.get(), self.purposeVar.get(), self.COMPONENTS)
        self.atex.check(self.siteVar.get(), self.purposeVar.get(), self.COMPONENTS)

        '''
        if self.lvd.active:
            LowVoltageInterface(self)
            if any(self.LowVoltageInterfaceVars):
                self.lvd.active = False
        if self.emc.active:
            ElectromagneticCompatibilityInterface(self)
            if any(self.ElectromagneticCompatibilityInterfaceVars):
                self.emc.active = False
        '''




        for component in self.COMPONENTS:
            print('')
            print('     {0}:'.format(component.componentName.get()))
            for directive in component.directives:
                print('         {0}'.format(directive))
            print('-'*10)



    
    


t = main()

