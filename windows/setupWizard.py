from PyQt5.QtWidgets import (
    QWizard, QLineEdit, QMessageBox, QComboBox, QLabel, QFileDialog
)
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt

from threads.setupThread import *

class CriptySetupWizard(QWizard):
    
    def __init__(self):
        super().__init__()
        loadUi("ui/setup.ui", self)
        self.SetupEnv()
        self.SetupUi()
        
    def SetupUi(self):
        self.passwordInput = self.findChild(QLineEdit, "passwordInput")
        self.passwordConfirm = self.findChild(QLineEdit, "passwordConfirm")
        self.passwordInput.setEchoMode(QLineEdit.Password)
        self.passwordConfirm.setEchoMode(QLineEdit.Password)
        self.nextButton = self.button(QWizard.NextButton)
        self.keyTypeBox = self.findChild(QComboBox, "keyTypeBox")
        self.secKeyPathInput = self.findChild(QLineEdit, "secKeyPathInput")
        
        self.imageLabel = self.findChild(QLabel, "imageLabel")
        self.imageLabel.setPixmap(QPixmap("resources/icon.png"))
        self.browsekeyButton.clicked.connect(self.BrowseKey)

        self.setWindowIcon(QIcon("resources/icon.png"))
        
    def SetupEnv(self):
        self.HOME = os.path.expanduser("~")
        self.CRIPTY_DIR = self.HOME + "/.cripty"

    def validateCurrentPage(self):
        pageId = self.currentId()
        self.vaultName = self.vaultNameInput.text()
        cfg = configparser.ConfigParser()
        cfg.read(".config")
        if(pageId == 1):
            if(len(self.vaultName) == 0):
                QMessageBox.critical(
                        self,
                        "Error",
                        "Vault name can't be empty"
                    )
                return False
            elif(cfg.has_section(self.vaultName)):
                QMessageBox.critical(
                        self,
                        "Error",
                        "A Vault with this name already exists.\nPlease choose a different name."
                    )
                return False
            else:
                return True
        elif(pageId == 2):
            if(self.passwordInput.text() == self.passwordConfirm.text()):
                self.password = self.passwordInput.text()
                if(len(self.passwordInput.text()) < 8):
                    QMessageBox.critical(
                        self,
                        "Error",
                        "Password must be at least 8 characters long"
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
            self.securityKeyPath = self.secKeyPathInput.text()
            if(len(self.securityKeyPath) > 0):
                return True
            else:
                QMessageBox.critical(
                    self,
                    "Error",
                    "Security key path cannot be empty"
                )
                return False
                
        elif(pageId == 5):
            return self.setupComplete
    
        return True
    
    def initializePage(self, id):
        super().initializePage(id)
        self.setupComplete = False
        if(id == 5):
            self.setupThread = SetupThread(self.progressBar,self.vaultName, self.password, self.keyType, self.securityKeyPath)
            self.setupThread.finished.connect(self.OnSetupComplete)
            self.setupThread.start()
            
    def OnSetupComplete(self):
        self.setupComplete = True
        
    def BrowseKey(self):
        self.securityKeyPath = QFileDialog.getSaveFileName(self, "Select security Key", self.HOME, "Cripty Security Key(.key)")[0]
        self.secKeyPathInput.setText(self.securityKeyPath)