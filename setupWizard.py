from PyQt5.QtWidgets import (
    QWizard, QLineEdit, QMessageBox, QComboBox, QLabel
)
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt

from setupThread import *

class CriptySetupWizard(QWizard):
    
    def __init__(self):
        super().__init__()
        loadUi("ui/setup.ui", self)
        
    def SetupUi(self):
        self.passwordInput = self.findChild(QLineEdit, "passwordInput")
        self.passwordConfirm = self.findChild(QLineEdit, "passwordConfirm")
        self.passwordInput.setEchoMode(QLineEdit.Password)
        self.passwordConfirm.setEchoMode(QLineEdit.Password)
        self.nextButton = self.button(QWizard.NextButton)
        self.currentIdChanged.connect(self.OnPageChanged)
        self.keyTypeBox = self.findChild(QComboBox, "keyTypeBox")
        
        self.imageLabel = self.findChild(QLabel, "imageLabel")
        self.imageLabel.setPixmap(QPixmap("resources/icon.png"))

        self.setWindowIcon(QIcon("resources/icon.png"))

    def validateCurrentPage(self):
        pageId = self.currentId()
        self.vaultName = self.vaultNameInput.text()
        if(pageId == 1):
            if(len(self.vaultName) == 0):
                QMessageBox.warning(
                        self,
                        "Error",
                        "Vault name can't be empty"
                    )
                return False
            else:
                return True
        elif(pageId == 2):
            if(self.passwordInput.text() == self.passwordConfirm.text()):
                self.password = self.passwordInput.text()
                if(len(self.passwordInput.text()) <= 15):
                    QMessageBox.warning(
                        self,
                        "Error",
                        "Password must be at least 16 characters long"
                    )
                    return False
                else:
                    return True
                
            else:
                QMessageBox.warning(
                    self,
                    "Error",
                    "Password do not match"
                )
                return False
        elif(pageId == 3):
            self.keyType = self.keyTypeBox.currentText()
            return True
        elif(pageId == 4):
            return self.setupComplete
    
        return True
    
    def initializePage(self, id):
        super().initializePage(id)
        self.setupComplete = False
        if(id == 4):
            self.setupThread = SetupThread(self.progressBar,self.vaultName, self.password, self.keyType)
            self.setupThread.finished.connect(self.OnSetupComplete)
            self.setupThread.start()
            
    def OnSetupComplete(self):
        self.setupComplete = True