from PyQt5.QtWidgets import (
    QWidget, QMessageBox, QLineEdit
)
from windows.mainWindow import CriptyMainWindow
from windows.setupWizard import CriptySetupWizard
from PyQt5.uic import loadUi
import configparser, bcrypt, os

class CriptyLoginWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        loadUi("ui/login.ui", self)
        self.cfg = configparser.ConfigParser()
        self.cfg.read(".config")
        self.HOME = os.path.expanduser("~")
        self.CRIPTY_DIR = self.HOME + "/.cripty"
        self.SetupUi()
        self.show()
        self.main_window = None
        self.setupWizard = None
        
    def SetupUi(self):
        self.loginButton.clicked.connect(self.OnLoginButtonClicked)
        self.vaultNameInput.addItems(self.cfg.sections())
        self.newVaultButton.clicked.connect(self.OnNewVaultClicked)
        self.vaultPasswordInput.setEchoMode(QLineEdit.Password)
    
    def OnLoginButtonClicked(self):
        self.password = self.vaultPasswordInput.text().encode("utf-8")
        self.vaultName = self.vaultNameInput.currentText()
        self.VAULT_PATH = self.CRIPTY_DIR + "/" + self.vaultName
        
        if self.cfg.has_section(self.vaultName):
            with open(self.VAULT_PATH + "/.psswd", "rb") as file:
                self.realPassword = file.read()
                
            if bcrypt.checkpw(self.password, self.realPassword):
                print("Login permitted")
                self.main_window = CriptyMainWindow(self.vaultName)
                self.main_window.show()
                self.close()
            else:
                QMessageBox.critical(
                    self,
                    "Login Error",
                    "Incorrect password"
                )            
        else:
            QMessageBox.critical(
                self,
                "Login Error",
                "Vault not found"
            )
    
    def OnNewVaultClicked(self):
        self.setupWizard = CriptySetupWizard()
        self.setupWizard.show()
        self.close()