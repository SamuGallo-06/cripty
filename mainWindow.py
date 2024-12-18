from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QFileDialog
)

from Crypto.Cipher import AES
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
import configparser
import os

class CriptyMainWindow(QMainWindow):
    
    def __init__(self, vaultName):
        super().__init__()
        loadUi("ui/main.ui", self)
        self.SetupUi()
        self.cfg = configparser.ConfigParser()
        self.cfg.read(".config")
        self.vaultName = vaultName
        self.HOME = os.path.expanduser("~")
        self.CRIPTY_DIR = self.HOME + "/.cripty"
        self.VAULT_PATH = self.CRIPTY_DIR + "/" + self.vaultName
        self.show()
        
    def SetupUi(self):
        self.setWindowIcon(QIcon("resources/icon.png"))
        self.addFileButton.clicked.connect(self.AddFile)
        
    def AddFile(self):
        self.newFilePath = QFileDialog.getOpenFileName(
            self,
            "Select file to add", 
            self.HOME, 
            "All Files(*)"
        )[0]
        
        self.encryptFile(self.newFilePath) #add key
        
    def encryptFile(self, filePath, key):
        cipher = AES.new(key, AES.MODE_EAX)
        with open(filePath, 'rb') as file:
            data = file.read()
            
        ciphertext, tag = cipher.encrypt_and_digest(data)
        
        filename = os.path.splitext(os.path.basename(filePath))[0]
        encrypted_file_path = self.VAULT_PATH + filename + ".enc"
        print("Saved" + encrypted_file_path)
        with open(encrypted_file_path, 'wb') as encrypted_file:
            [encrypted_file.write(x) for x in (cipher.nonce, tag, ciphertext)]
        