from PyQt5.QtCore import Qt
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
        self.titleBottomLayout.addWidget(self.messageLabel)

    def delete(self):
        self.deleteLater()

class ResultWindow(QFrame):
    def __init__(self):
        super(ResultWindow,self).__init__()
        self.setGeometry(300,300,400,100)
        self.setWindowTitle('Ergebnisse')
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





class MachineryDirectiveInterface(Interface):
    def __init__(self,machine):
        super(MachineryDirectiveInterface,self).__init__('Maschinen Richtlinie')
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






class ATEXInterface(Interface):
    def __init__(self,machine):
        super(ATEXInterface,self).__init__(title='ATEX',id_string='2014/34/EU')
        self.category = None
        self.group = None
        self.machine = machine
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
        self.L2 = QLabel('Gerätekategorie: {0}'.format(self.group))
        self.lB.addWidget(self.L2)


    def writeMessages(self):
        self.initResultWindow()

        message = Message(self.title, self.id_string, self.verdict)
        panel = self.categoryGroupPanel()
        message.titleTopLayout.addLayout(panel)

        self.addMessageToResultWindow(message)


    def printVerdict(self):
        self.verdict = ''
        print('\n')
        print('Gerätegruppe: {0}'.format(self.group))
        print('Gerätekategorie: {0}'.format(self.category))
        if self.category == 'M 1':
            self.verdict = '        Die Geräte dieser Kategorie müssen die weitergehenden Anforderungen des Anhangs II Nummer 2.0.1 erfüllen'
        elif self.category == 'M 2':
            self.verdict = '        Die Geräte dieser Kategorie müssen die weitergehenden Anforderungen des Anhangs II Nummer 2.0.2 erfüllen.'
        elif self.category == '1':
            self.verdict = '        Die Geräte dieser Kategorie müssen die weitergehenden Anforderungen des Anhangs II Nummer 2.1 erfüllen.'
        elif self.category == '2':
            self.verdict = '        Die Geräte dieser Kategorie müssen die weitergehenden Anforderungen des Anhangs II Nummer 2.2 erfüllen.'
        elif self.category == '3':
            self.verdict = '        Die Geräte dieser Kategorie müssen die weitergehenden Anforderungen des Anhangs II Nummer 2.3 erfüllen.'
        else:
            self.verdict = '        Gerät nicht zulassig nach ATEX'

        if not self.verdict == '        Gerät nicht zulassig nach ATEX':
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
        self.category = ''
        self.group = ''
        if self.Q1.yes.isChecked():
            self.group = 'I'
            if self.Q2_1_1.yes.isChecked() or self.Q2_1_2.yes.isChecked():
                self.category = 'M 1'
            elif self.Q2_2_1.yes.isChecked():
                self.category = 'M 2'
            else:
                self.category = ''
        else:
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

