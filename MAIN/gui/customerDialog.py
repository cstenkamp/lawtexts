import sys
import os
from jsonHandler import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import functools

class CustomerDialog(QDialog):

    def __init__(self):
        super(CustomerDialog, self).__init__()
        self.createFormGroupBox()
        self.role = "Betreiber"
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonBox.accepted.connect(self.accept)
        cancel = QPushButton("abbrechen")
        cancel.setIcon(QIcon(ICON_PATH+"cancel.png"))
        buttonBox.addButton(cancel, QDialogButtonBox.RejectRole)
        buttonBox.rejected.connect(self.reject)
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)
        self.setWindowTitle("Prüfung der Richtlinien")
        self.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)

    def createFormGroupBox(self):
        self.formGroupBox = QGroupBox("Zuständigkeit:")
        layout = QFormLayout()
        self.combBox = QComboBox()
        self.combBox.addItems(["Betreiber", "Bevollmächtigter", "Händler", "Hersteller"])
        layout.addRow(QLabel("Zuständig als"), self.combBox)
        self.formGroupBox.setLayout(layout)

    def newAccept(self):
        self.role = self.combBox.currentText()
        self.accept()

    def getRole(self):
        return self.role
