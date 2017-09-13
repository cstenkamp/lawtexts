from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from interfaceHelper import *

class Interface(QWidget):
    def __init__(self, title=None):
        super(Interface,self).__init__()
        self.setGeometry(300,300,400,100)
        self.setWindowTitle(title)
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setAlignment(Qt.AlignTop)
        self.setLayout(self.mainLayout)
        self.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.MinimumExpanding)
        self.show()
        #
        self.questions = []
        # finalize button
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addStretch()
        self.button = QPushButton('abschicken')
        self.buttonLayout.addWidget(self.button)
        self.mainLayout.addLayout(self.buttonLayout)
        self.spacer = QSpacerItem(10, 0, QSizePolicy.Maximum, QSizePolicy.Minimum)
        self.mainLayout.addItem(self.spacer)

    def addRadioQuestion(self,text=None, question=None, parent=None, antagonists=[]):
        if question is None:
            question = RadioQuestion(text, parent=parent,antagonists=antagonists)
        self.mainLayout.addWidget(question)
        self.questions.append(question)
        return question



class ATEXInterface(Interface):
    def __init__(self,machine):
        super(ATEXInterface,self).__init__('ATEX')
        self.category = None
        self.group = None
        self.machine = machine
        self.button.clicked.connect(self.printVerdict)

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

