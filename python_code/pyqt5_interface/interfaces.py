from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import *

from interfaceHelper import *

class Message(QFrame):
    def __init__(self, directive_name, directive_id, message):
        super(Message,self).__init__()
        self.setFrameShape(QFrame.Box)
        self.setFrameShadow(QFrame.Sunken)
        self.directive_name = directive_name
        self.directive_id = directive_id
        self.message = message

        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setAlignment(Qt.AlignTop|Qt.AlignLeft)
        self.setLayout(self.mainLayout)
        
        self.titleLayout = QVBoxLayout()
        self.titleLayout.setAlignment(Qt.AlignTop|Qt.AlignLeft)
        self.mainLayout.addLayout(self.titleLayout)

        self.titleTopLayout = QHBoxLayout()
        self.titleLayout.addLayout(self.titleTopLayout)

        self.titleBottomLayout = QHBoxLayout()
        self.titleLayout.addLayout(self.titleBottomLayout)

        self.bottomLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.bottomLayout)

        self.titleLabel = QLabel('Auswertung nach: {0} ({1})'.format(self.directive_id,directive_name))
        self.titleTopLayout.addWidget(self.titleLabel)

        self.messageLabel = QLabel(message)
        self.bottomLayout.addWidget(self.messageLabel)

    def delete(self):
        self.deleteLater()

class ResultWindow(QFrame):
    def __init__(self, title = 'Ergebnisse'):
        super(ResultWindow,self).__init__()
        self.setGeometry(300,300,400,100)
        self.setWindowTitle(title)
        self.show()
        #
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setAlignment(Qt.AlignTop|Qt.AlignLeft)
        self.setLayout(self.mainLayout)
        #
        self.topLayout = QHBoxLayout()
        self.topLayout.setAlignment(Qt.AlignRight|Qt.AlignTop)
        self.mainLayout.addLayout(self.topLayout)
        #
        self.bottomLayout = QVBoxLayout()
        self.bottomLayout.setAlignment(Qt.AlignRight|Qt.AlignTop)
        self.mainLayout.addLayout(self.bottomLayout)
        #
        self.closeButton = QPushButton('schließen')
        self.closeButton.clicked.connect(self.hide)
        self.topLayout.addWidget(self.closeButton)


class Interface(QWidget):
    def __init__(self, title=None, id_string=None):
        super(Interface,self).__init__()
        self.setGeometry(300,300,400,100)
        self.setWindowTitle(title)
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setAlignment(Qt.AlignTop)
        self.title = title
        self.id_string = id_string
        self.setLayout(self.mainLayout)
        self.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.MinimumExpanding)
        self.show()
        #
        self.questions = []
        self.resultWindow = None
        self.message_frames = []
        self.spacer = QSpacerItem(10, 0, QSizePolicy.Maximum, QSizePolicy.Minimum)
        self.mainLayout.addItem(self.spacer)

    def addRadioQuestion(self,text=None, question=None, parent=None, antagonists=[]):
        if question is None:
            question = RadioQuestion(text, parent=parent,antagonists=antagonists)
        self.mainLayout.addWidget(question)
        self.questions.append(question)
        return question

    def addSingleCheckQuestion(self,text=None, question=None, parent=None, antagonists=[]):
        if question is None:
            question = SingleCheckQuestion(text, parent=parent,antagonists=antagonists)
        self.topLayout.addWidget(question)
        self.questions.append(question)
        return question

    def addAnswer(self,text=None, question=None, parent=None, antagonists=[]):
        if question is None:
            question = Answer(text, parent=parent,antagonists=antagonists)
        self.mainLayout.addWidget(question)
        self.questions.append(question)
        return question

    def addMessageToResultWindow(self, message_frame):
        self.resultWindow.bottomLayout.addWidget(message_frame)
        self.message_frames.append(message_frame)

    def removeMessageToResultWindow(self, message_frame):
        self.message_frames.remove(message_frame)
        message_frame.delete()

    def openResultWindow(self):
        if self.resultWindow is None:
            self.resultWindow = self.initResultWindow()
        else:
            self.resultWindow.show()

    def delete(self):
        self.deleteLater()


    def initResultWindow(self):
        self.resultWindow = ResultWindow()





class MachineryDirectiveApplicabilityInterface(Interface):
    def __init__(self,machine):
        super(MachineryDirectiveApplicabilityInterface,self).__init__('Maschinen Richtlinie')
        self.machine = machine



    def applicabilityPilot(self):
        # top layout
        self.topLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.topLayout)
        # label explaining what to do
        self.label = QLabel('In diesem Interface können Sie die Anwendbarkeit der 2006/42/EG auf Ihr Produkt prüfen.')
        self.label.setFrameShadow(QFrame.Sunken)
        self.label.setFrameStyle(QFrame.Box)
        self.topLayout.addWidget(self.label)
        # finalize button
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addStretch()
        self.button = QPushButton('abschicken')
        self.buttonLayout.addWidget(self.button)
        self.topLayout.addLayout(self.buttonLayout)
        self.button.clicked.connect(self.close)
        self.show()




        '''
        Part II
        '''
        text = 'Besteht das Produkt aus miteinander verbundenen Teilen (evtl. zwecks Transport getrennt), von denen mindestens eins beweglich ist?'
        self.Q = self.addRadioQuestion(text)

        text = 'Kann für sich genommen die bestimmte Anwendung/Funktion erfüllen?'
        self.QY = self.addRadioQuestion(text,parent=self.Q)
        self.QY.hide()

        text = 'Produkt ist mit einem Antriebssystem ausgestattet?'
        self.QYY = self.addRadioQuestion(text,parent=self.QY)
        self.QYY.hide()

        text = 'Antriebssystem ist unmittelbar eingesetzte menschliche Kraft?'
        self.QYYY = self.addRadioQuestion(text,parent=self.QYY)
        self.QYYY.hide()

        text = 'Antriebssystem ist unmittelbar eingesetzte menschliche Kraft?'
        self.QYYYY = self.addRadioQuestion(text,parent=self.QYYY)
        self.QYYYY.hide()

        text = 'Produkt ist für Hebevorgänge?'
        self.QYYYYY = self.addRadioQuestion(text,parent=self.QYYYY)
        self.QYYYYY.hide()
        '''
        text = 'Maschine nach Artikel 1(1)a'
        self.QYYYYYY = self.addAnswer(text,parent=self.QYYYYY)
        self.QYYYYYY.hide()

        text = 'Kein Produkt nach Artikel 1(1)a-g'
        self.QYYYYYN = self.addAnswer(text,parent=self.QYYYYY)
        self.QYYYYYN.hide()
        '''

        self.Q.yes.clicked.connect(lambda:[
                                self.QY.showw(),
                                self.updateLabels(),
                                ])
        self.Q.no.clicked.connect(lambda:[
                                self.QY.hidee(),
                                self.updateLabels(),
                                ])


        self.QY.yes.clicked.connect(lambda:[
                                self.QYY.showw(),
                                self.updateLabels(),
                                ])
        self.QY.no.clicked.connect(lambda:[
                                self.QYY.hidee(),
                                self.updateLabels(),
                                ])

        self.QYY.yes.clicked.connect(lambda:[
                                self.QYYY.showw(),
                                self.updateLabels(),
                                ])
        self.QYY.no.clicked.connect(lambda:[
                                self.QYYY.hidee(),
                                self.updateLabels(),
                                ])

        self.QYYY.yes.clicked.connect(lambda:[
                                self.QYYYY.showw(),
                                self.updateLabels(),
                                ])
        self.QYYY.no.clicked.connect(lambda:[
                                self.QYYYY.hidee(),
                                self.updateLabels(),
                                ])

        self.QYYYY.yes.clicked.connect(lambda:[
                                self.QYYYYY.showw(),
                                self.updateLabels(),
                                ])
        self.QYYYY.no.clicked.connect(lambda:[
                                self.QYYYYY.hidee(),
                                self.updateLabels(),
                                ])
        '''
        self.QYYYYY.yes.clicked.connect(lambda:[
                                self.QYYYYYY.showw(),
                                self.QYYYYYN.hidee(),
                                self.updateLabels(),
                                ])
        self.QYYYYY.no.clicked.connect(lambda:[
                                self.QYYYYYY.hidee(),
                                self.QYYYYYN.showw(),
                                self.updateLabels(),
                                ])
        '''



    def close(self):
        self.hide()



    def updateLabels(self):
        self.category = None
        print(self.category)



class MachineryDirectiveAppendixIVInterface(Interface):
    def __init__(self,machine):
        super(MachineryDirectiveAppendixIVInterface,self).__init__('Test auf Anwendbarkeit von Anhang IV')
        self.machine = machine

    def applicabilityPilot(self):
        # top layout
        self.show()

        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        


        self.topLayoutWidget = QWidget(self.scrollArea)
        self.topLayout = QVBoxLayout(self.topLayoutWidget)
        self.topLayout.setAlignment(Qt.AlignTop)

        self.scrollArea.setWidget(self.topLayoutWidget)
        self.mainLayout.addWidget(self.scrollArea)
        

        text = '(1) Einblatt- und Mehrblatt-Kreissäge zum Bearbeiten von Holz und von Werkstoffen mit ähnlichen physikalischen Eigenschaften oder zum Bearbeiten von Fleisch und von Stoffen mit ähnlichen physikalischen Eigenschaften:'
        self.k1 = self.addSingleCheckQuestion(text)

        text = '(1.1) Sägemaschine mit während des Arbeitsvorgangs feststehendem Sägeblatt, mit feststehendem Arbeitstisch oder Werkstückhalter, mit Vorschub des Sägeguts von Hand oder durch einen abnehmbaren Vorschubapparat;'
        self.k1_1 = self.addSingleCheckQuestion(text,parent = self.k1)
        self.k1_1.hide()

        text = '(1.2) Sägemaschine mit während des Arbeitsvorgangs feststehendem Sägeblatt, mit manuell betätigtem Pendelbock oder -schlitten;'
        self.k1_2 = self.addSingleCheckQuestion(text,parent = self.k1)
        self.k1_2.hide()

        text = '(1.3) Sägemaschine mit während des Arbeitsvorgangs feststehendem Sägeblatt, mit eingebauter mechanischer Vorschubeinrichtung für das Sägegut und Handbeschickung und/oder Handentnahme;'
        self.k1_3 = self.addSingleCheckQuestion(text,parent = self.k1)
        self.k1_3.hide()

        text = '(1.4) Sägemaschine mit während des Arbeitsvorgangs beweglichem Sägeblatt, mit eingebauter mechanischer Vorschubeinrichtung für das Sägeblatt und Handbeschickung und/oder Handentnahme.'
        self.k1_4 = self.addSingleCheckQuestion(text,parent = self.k1)
        self.k1_4.hide()

        text = '(2) Abrichthobelmaschine mit Handvorschub für die Holzbearbeitung.'
        self.k2 = self.addSingleCheckQuestion(text)
        
        text = '(3) Hobelmaschine für einseitige Bearbeitung von Holz, mit eingebauter maschineller Vorschubeinrichtung und Handbeschickung und/oder Handentnahme.'
        self.k3 = self.addSingleCheckQuestion(text)
        
        text = '(4) Bandsäge mit Handbeschickung und/oder Handentnahme zur Bearbeitung von Holz und von Werkstoffen mit ähnlichen physikalischen Eigenschaften oder von Fleisch und von Stoffen mit ähnlichen physikalischen Eigenschaften:'
        self.k4 = self.addSingleCheckQuestion(text)

        text = '(4.1) Sägemaschine mit während des Arbeitsvorgangs feststehendem Sägeblatt und feststehendem oder hin- und her beweglichem Arbeitstisch oder Werkstückhalter;'
        self.k4_1 = self.addSingleCheckQuestion(text)

        text = '(4.2) Sägemaschine, deren Sägeblatt auf einem hin- und her beweglichen Schlitten montiert ist'
        self.k4_2 = self.addSingleCheckQuestion(text)
        
        text = '(5) Kombination der in den Nummern 1 bis 4 und in Nummer 7 genannten Maschinen für die Bearbeitung von Holz und von Werkstoffen mit ähnlichen physikalischen Eigenschaften.'
        self.k5 = self.addSingleCheckQuestion(text)
        
        
        text = '(6) Mehrspindel-Zapfenfräsmaschine mit Handvorschub für die Holzbearbeitung.'
        self.k6 = self.addSingleCheckQuestion(text)
        
        
        text = '(7) Senkrechte Tischfräsmaschine mit Handvorschub für die Bearbeitung von Holz und von Werkstoffen mit ähnlichen physikalischen Eigenschaften.'
        self.k7 = self.addSingleCheckQuestion(text)
        
        
        text = '(8) Handkettensäge für die Holzbearbeitung.'
        self.k8 = self.addSingleCheckQuestion(text)
        
        
        text = '(9) Presse, einschließlich Biegepressen, für die Kaltbearbeitung von Metall mit Handbeschickung und/oder Handentnahme, deren beim Arbeitsvorgang bewegliche Teile einen Hub von mehr als 6 mm und eine Geschwindigkeit von mehr als 30 mm/s haben können.'
        self.k9 = self.addSingleCheckQuestion(text)
        
        
        text = '(10) Kunststoffspritzgieß- und -formpressmaschine mit Handbeschickung oder Handentnahme'
        self.k10 = self.addSingleCheckQuestion(text)
        
        
        text = '(11) Gummispritzgieß- und -formpressmaschine mit Handbeschickung oder Handentnahme.'
        self.k11 = self.addSingleCheckQuestion(text)
        
        
        text = '(12) Maschinenart für den Einsatz unter Tage:'
        self.k12 = self.addSingleCheckQuestion(text)
        
        
        text = '(12.1) Lokomotive oder Bremswage;'
        self.k12_1 = self.addSingleCheckQuestion(text,parent=self.k12)
        

        text = '(12.2) hydraulischer Schreitausbau'
        self.k12_2 = self.addSingleCheckQuestion(text,parent=self.k12)

        
        text = '(13) Hausmüllsammelwagen für manuelle Beschickung mit Pressvorrichtung.'
        self.k13 = self.addSingleCheckQuestion(text)
        
        
        text = '(14) Abnehmbare Gelenkwellen einschließlich ihrer Schutzeinrichtungen.'
        self.k14 = self.addSingleCheckQuestion(text)
        
        
        text = '(15) Schutzeinrichtungen für abnehmbare Gelenkwellen.'
        self.k15 = self.addSingleCheckQuestion(text)
        
        
        text = '(16) Hebebühnen für Fahrzeuge.'
        self.k16 = self.addSingleCheckQuestion(text)
        
        
        text = '(17) Maschinen zum Heben von Personen oder von Personen und Gütern, bei denen die Gefährdung eines Absturzes aus einer Höhe von mehr als 3 m besteht.'
        self.k17 = self.addSingleCheckQuestion(text)
        
        
        text = '(18) Tragbare Befestigungsgeräte mit Treibladung und andere Schussgeräte.'
        self.k18 = self.addSingleCheckQuestion(text)
        
        
        text = '(19) Schutzeinrichtungen zur Personendetektion.'
        self.k19 = self.addSingleCheckQuestion(text)
        
        
        text = '(20) Kraftbetriebene, bewegliche trennende Schutzeinrichtungen mit Verriegelung für die in den Nummern 9, 10 und 11 genannten Maschinen.'
        self.k20 = self.addSingleCheckQuestion(text)
        
        
        text = '(21) Logikeinheiten für Sicherheitsfunktionen.'
        self.k21 = self.addSingleCheckQuestion(text)
        
        
        text = '(22) Überrollschutzaufbau (ROPS).'
        self.k22 = self.addSingleCheckQuestion(text)
        
        
        text = '(23) Schutzaufbau gegen herabfallende Gegenstände (FOPS).'
        self.k23 = self.addSingleCheckQuestion(text)


        self.k1.yes.stateChanged.connect(self.k1.toggleChildren)
        self.k4.yes.stateChanged.connect(self.k4.toggleChildren)
        self.k12.yes.stateChanged.connect(self.k12.toggleChildren)

        self.k1_1.yes.stateChanged.connect(self.initConfirmationDialogue)
        self.k1_2.yes.stateChanged.connect(self.initConfirmationDialogue)
        self.k1_3.yes.stateChanged.connect(self.initConfirmationDialogue)
        self.k1_4.yes.stateChanged.connect(self.initConfirmationDialogue)
        self.k2.yes.stateChanged.connect(self.initConfirmationDialogue)
        self.k3.yes.stateChanged.connect(self.initConfirmationDialogue)
        self.k4_1.yes.stateChanged.connect(self.initConfirmationDialogue)
        self.k4_2.yes.stateChanged.connect(self.initConfirmationDialogue)
        self.k5.yes.stateChanged.connect(self.initConfirmationDialogue)
        self.k6.yes.stateChanged.connect(self.initConfirmationDialogue)
        self.k7.yes.stateChanged.connect(self.initConfirmationDialogue)
        self.k8.yes.stateChanged.connect(self.initConfirmationDialogue)
        self.k9.yes.stateChanged.connect(self.initConfirmationDialogue)
        self.k10.yes.stateChanged.connect(self.initConfirmationDialogue)
        self.k11.yes.stateChanged.connect(self.initConfirmationDialogue)
        self.k12_1.yes.stateChanged.connect(self.initConfirmationDialogue)
        self.k12_2.yes.stateChanged.connect(self.initConfirmationDialogue)
        self.k13.yes.stateChanged.connect(self.initConfirmationDialogue)
        self.k14.yes.stateChanged.connect(self.initConfirmationDialogue)
        self.k15.yes.stateChanged.connect(self.initConfirmationDialogue)
        self.k16.yes.stateChanged.connect(self.initConfirmationDialogue)
        self.k17.yes.stateChanged.connect(self.initConfirmationDialogue)
        self.k18.yes.stateChanged.connect(self.initConfirmationDialogue)
        self.k19.yes.stateChanged.connect(self.initConfirmationDialogue)
        self.k20.yes.stateChanged.connect(self.initConfirmationDialogue)
        self.k21.yes.stateChanged.connect(self.initConfirmationDialogue)
        self.k22.yes.stateChanged.connect(self.initConfirmationDialogue)
        self.k23.yes.stateChanged.connect(self.initConfirmationDialogue)


    def initConfirmationDialogue(self):
        for question in self.questions:
            if question in [self.k1,self.k4,self.k12]:
                print('ding')
                continue 
            else:
                if question.yes.isChecked():
                    self.rw = ResultWindow(title='Ergebniss des Tests auf Anwendbarkeit von Anhang IV ')
                    if not question.parent is None:
                        l = QLabel(question.parent.label.text())
                        self.rw.bottomLayout.addWidget(l)
                    l = QLabel(question.label.text())
                    self.rw.bottomLayout.addWidget(l)



class ATEXInterface(Interface):
    def __init__(self,machine,parent):
        super(ATEXInterface,self).__init__(title='ATEX',id_string='2014/34/EU')
        self.category = None
        self.group = None
        self.machine = machine
        self.parent = parent
        # finalize button
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addStretch()
        self.button = QPushButton('abschicken')
        self.buttonLayout.addWidget(self.button)
        self.mainLayout.addLayout(self.buttonLayout)
        self.button.clicked.connect(self.printVerdict)

    def categoryGroupPanel(self):
        self.cgpLayout = QVBoxLayout()

        self.lT = QHBoxLayout()
        self.cgpLayout.addLayout(self.lT)
        self.lB = QHBoxLayout()
        self.cgpLayout.addLayout(self.lB)

        self.L1 = QLabel('Gerätegruppe: {0}'.format(self.group))
        self.lT.addWidget(self.L1)
        self.L2 = QLabel('Gerätekategorie: {0}'.format(self.category))
        self.lB.addWidget(self.L2)


    def writeMessages(self):
        self.initResultWindow()

        message = Message(self.title, self.id_string, self.verdict)
        self.categoryGroupPanel()
        message.titleBottomLayout.addLayout(self.cgpLayout)

        self.addMessageToResultWindow(message)


    def printVerdict(self):
        self.verdict = ''
        print('\n')
        print('Gerätegruppe: {0}'.format(self.group))
        print('Gerätekategorie: {0}'.format(self.category))
        if self.category == 'M 1':
            self.verdict = 'Die Geräte dieser Kategorie müssen die weitergehenden Anforderungen des Anhangs II Nummer 2.0.1 erfüllen'
        elif self.category == 'M 2':
            self.verdict = 'Die Geräte dieser Kategorie müssen die weitergehenden Anforderungen des Anhangs II Nummer 2.0.2 erfüllen.'
        elif self.category == '1':
            self.verdict = 'Die Geräte dieser Kategorie müssen die weitergehenden Anforderungen des Anhangs II Nummer 2.1 erfüllen.'
        elif self.category == '2':
            self.verdict = 'Die Geräte dieser Kategorie müssen die weitergehenden Anforderungen des Anhangs II Nummer 2.2 erfüllen.'
        elif self.category == '3':
            self.verdict = 'Die Geräte dieser Kategorie müssen die weitergehenden Anforderungen des Anhangs II Nummer 2.3 erfüllen.'
        else:
            self.verdict = 'Gerät nicht zulassig nach ATEX'

        if not self.verdict == 'Gerät nicht zulassig nach ATEX':
            self.hide()

        self.writeMessages()
        print(self.verdict)

    def setGroup(self, group):
        self.group = group
        self.updateLabels()

    def setCategory(self, category):
        self.category = category
        self.updateLabels()

    def updateLabels(self):
        self.category = 'ungültig'
        self.group = 'ungültig'
        if self.Q1.yes.isChecked():
            #self.parent.
            self.group = 'I'
            if self.Q2_1_1.yes.isChecked() or self.Q2_1_2.yes.isChecked():
                self.category = 'M 1'
                # TODO: set label siteSelectionMenu in parent (MachineGui) to appropriate item 
            elif self.Q2_2_1.yes.isChecked():
                self.category = 'M 2'
            else:
                self.category = ''
        elif self.Q1.no.isChecked():
            self.group = 'II'
            if self.Q2_1_1.yes.isChecked() or self.Q2_1_2.yes.isChecked():
                self.category = '1'
            if self.Q2_2_1.yes.isChecked():
                self.category = '2'
            if self.Q3.yes.isChecked():
                self.category = '3'
        self.categoryLabel.setText('Gerätekategorie: {0}'.format(self.category))
        self.groupLabel.setText('Gerätegruppe: {0}'.format(self.group))

    def categoryMask(self):
        self.topRow = QHBoxLayout()
        self.topRow.addStretch()
        self.categoryLabel = QLabel('Gerätekategorie: ')
        self.topRow.addWidget(self.categoryLabel)
        self.groupLabel = QLabel('Gerätegruppe: ')
        self.topRow.addWidget(self.groupLabel)
        self.mainLayout.addLayout(self.topRow)

        text = 'ENTSCHEIDUNGSKRITERIEN FÜR DIE EINTEILUNG DER GERÄTEGRUPPEN IN KATEGORIEN'
        self.label = QLabel(text)
        self.mainLayout.addWidget(self.label)
        text = 'Gerät ist zur Verwendung in untertägigen Bergwerken sowie deren Übertageanlagen bestimmt?'
        self.Q1 = self.addRadioQuestion(text=text)


        text = 'Gerät muss selbst bei seltenen Gerätestörungen in vorhandener explosionsfähiger Atmosphäre weiterbetrieben werden?'
        self.Q2_1 = self.addRadioQuestion(text=text)
        self.Q2_1.hide()

        text = 'Beim Versagen einer apparativen Schutzmaßnahme ist mindestens eine zweite unabhängige apparative Schutzmaßnahme vorhanden, die die erforderliche Sicherheit gewährleistet?'
        self.Q2_1_1 = self.addRadioQuestion(text=text, parent=self.Q2_1)
        self.Q2_1_1.hide()

        text = 'Beim Auftreten von zwei unabhängigen Fehlern wird die erforderliche Sicherheit gewährleistet?'
        self.Q2_1_2 = self.addRadioQuestion(text=text, parent=self.Q2_1)
        self.Q2_1_2.hide()

        text = 'Gerät ist dazu bestimmt, beim Auftreten einer explosionsfähigen Atmosphäre abgeschaltet zu werden?'
        self.Q2_2 = self.addRadioQuestion(text=text)
        self.Q2_2.hide()

        #self.Q2_2.addAntagonists(self.Q2_1)
        #self.Q2_1.addAntagonists(self.Q2_2)

        text = 'Die apparativen Explosionsschutzmaßnahmen gewährleisten das erforderliche Maß an Sicherheit bei normalem Betrieb, auch unter schweren Betriebsbedingungen und insbesondere bei rauer Behandlung und wechselnden Umgebungseinflüssen?'
        self.Q2_2_1 = self.addRadioQuestion(text=text, parent=self.Q2_2)
        self.Q2_2_1.hide()

        text = 'Gerät ist zur Verwendung in Bereichen bestimmt, in denen nicht damit zu rechnen ist, dass eine explosionsfähige Atmosphäre durch Gase, Dämpfe, Nebel oder aufgewirbelten Staub auftritt, aber wenn sie dennoch auftritt, dann aller Wahrscheinlichkeit nach nur selten und während eines kurzen Zeitraums?'
        self.Q3 = self.addRadioQuestion(text=text)
        self.Q3.hide()

        if self.machine.site in ['in untertägigen Bergwerken oder deren Übertageanlagen']:
            self.Q1.yes.setChecked(True)
            self.setGroup('I')
        else:
            self.setGroup('II')
            self.Q3.show()

        self.Q2_1.show()
        self.Q2_2.show()
        self.updateLabels()

        """
        Q1
        """
        self.Q1.yes.clicked.connect(lambda: [self.Q1.showChildren(),
                                            self.Q3.hide(),
                                            self.Q3.no.setChecked(False),
                                            self.updateLabels()])


        self.Q1.no.clicked.connect(lambda: [self.Q1.hideChildren(),
                                            self.Q3.show(),
                                            self.updateLabels()])

        """
        Q2_1
        """
        #
        self.Q2_1.yes.clicked.connect(lambda: [self.Q2_1.showChildren(),
                                               self.Q2_2.resetAntagonists(),
                                               self.updateLabels()])
        #
        self.Q2_1.no.clicked.connect(lambda: [self.Q2_1.hideChildren(),
                                              self.updateLabels()])
        #
        self.Q2_1_1.yes.clicked.connect(lambda: [self.updateLabels()])
        self.Q2_1_1.no.clicked.connect(lambda: [self.updateLabels()])
        #
        self.Q2_1_2.yes.clicked.connect(lambda: [self.updateLabels()])
        self.Q2_1_2.no.clicked.connect(lambda: [self.updateLabels()])

        """
        Q2_2
        """
        #
        self.Q2_2.yes.clicked.connect(lambda: [self.Q2_2.showChildren(),
                                               self.Q2_1.resetAntagonists(),
                                               self.updateLabels()])
        self.Q2_2.no.clicked.connect(lambda: [self.Q2_2.hideChildren(),
                                              self.updateLabels()])
        #
        self.Q2_2_1.yes.clicked.connect(lambda: [self.updateLabels()])
        self.Q2_2_1.no.clicked.connect(lambda: [self.Q2_2_1.hideChildren(),
                                                self.updateLabels()])
        #
        self.Q3.yes.clicked.connect(lambda: [self.updateLabels()])
        self.Q3.no.clicked.connect(lambda: [self.Q3.hideChildren(),
                                                self.updateLabels()])

