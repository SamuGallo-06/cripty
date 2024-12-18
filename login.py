from PyQt5.QtWidgets import (
    QWidget, QMessageBox
)
from mainWindow import CriptyMainWindow
from PyQt5.uic import loadUi
import configparser, bcrypt

class CriptyLoginWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        loadUi("ui/login.ui", self)
        self.SetupUi()
        self.show()
        self.cfg = configparser.ConfigParser()
        self.cfg.read(".config")
        self.main_window = None
        
    def SetupUi(self):
        self.loginButton.clicked.connect(self.OnLoginButtonClicked)
    
    def OnLoginButtonClicked(self):
        self.password = self.vaultPasswordInput.text().encode("utf-8")
        self.vaultName = self.vaultNameInput.text()
        
        if self.cfg.has_section(self.vaultName):
            with open(".psswd", "rb") as file:
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