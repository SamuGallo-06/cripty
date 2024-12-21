from PyQt5.QtWidgets import (
    QWizard, QLineEdit, QMessageBox, QComboBox, QLabel, QFileDialog, QPushButton
)
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
import configparser, os
from threads.deleteVaultThread import DeleteVaultThread

class CriptyRemoveVaultWizard(QWizard):
    
    def __init__(self):
        super().__init__()
        self.cfg = configparser.ConfigParser()
        self.cfg.read(".config")
        self.HOME = os.path.expanduser("~")
        loadUi("ui/removeVaultWizard.ui", self)
        self.SetupUi()
        
    def SetupUi(self):
        self.vaultsComboBox = self.findChild(QComboBox, "vaultsComboBox")
        self.securityKeyInput = self.findChild(QLineEdit, "securityKeyInput")
        self.logLabel = self.findChild(QLabel, "logLabel")
        self.browseKeyButton = self.findChild(QPushButton, "browseKeyButton")
        self.browseKeyButton.clicked.connect(self.BrowseSecurityKey)
        #self.currentIdChanged.connect(self.OnPageChanged)

        self.setWindowIcon(QIcon("resources/icon.png"))

    def validateCurrentPage(self):
        pageId = self.currentId()
        if(pageId == 1):
            self.vaultName = self.vaultsComboBox.currentText()
        if(pageId == 2):
            if(not(os.path.exists(self.securityKeyInput.text()))):
                QMessageBox.critical(
                    self,
                    "Fatal Error",
                    "Security Key not found in specified path"
                ) 
                return False
            else:
                result = self.CheckSecurityKey()
                return result
        return True
    
    def initializePage(self, id):
        super().initializePage(id)
        if(id == 1):
            self.vaultsComboBox.addItems(self.cfg.sections())
        elif(id == 3):
            self.removeThread = DeleteVaultThread(self.progressBar, self.vaultName, self.logLabel)
            self.removeThread.start()
        self.setupComplete = False
            
    def OnSetupComplete(self):
        self.setupComplete = True
        
    def BrowseSecurityKey(self):
        print("browseKeyButton clicked")
        self.securityKeyPath = QFileDialog.getOpenFileName(self, "Select security Key", self.HOME, "Cripty Security Key(.key)")[0]
        self.securityKeyInput.setText(self.securityKeyPath)
        
    def CheckSecurityKey(self):
        self.securityKeyPath = self.securityKeyInput.text()
        realSecurityKey = self.cfg.get(self.vaultName, "security-key")
        
        with open(self.securityKeyPath, "r") as file:
            securityKey = file.read()
            return (securityKey == realSecurityKey)
                
                