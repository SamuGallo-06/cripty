from PyQt5.QtCore import QThread
import bcrypt
import configparser
from Crypto.Random import get_random_bytes
import base64
import os
import secrets

class SetupThread(QThread):
    
    def __init__(self, progressbar, vaultName, password, keyType, securityKeyPath):
        super().__init__()
        self.progressbar = progressbar
        self.keyType = keyType
        self.securityKeyPath = securityKeyPath
        self.TOTAL_OPERATIONS = 6
        self.HOME = os.path.expanduser("~")
        self.CRIPTY_DIR = self.HOME + "/.cripty"
        self.password = password
        self.vaultName = vaultName
        self.cfg = configparser.ConfigParser()
        
    def run(self):
        self.progressbar.setValue(0)
        self.HashPassword()
        self.progressbar.setValue(int((1 / self.TOTAL_OPERATIONS) * 100))
        self.GenerateVaultkey()
        self.progressbar.setValue(int((2 / self.TOTAL_OPERATIONS) * 100))
        self.SaveSecurityKey()
        self.progressbar.setValue(int((3 / self.TOTAL_OPERATIONS) * 100))
        self.CreateVault()
        self.progressbar.setValue(int((4 / self.TOTAL_OPERATIONS) * 100))
        self.WritePasswordFile()
        self.progressbar.setValue(int((5 / self.TOTAL_OPERATIONS) * 100))
        self.WriteSettings()
        self.progressbar.setValue(int((6 / self.TOTAL_OPERATIONS) * 100))
        
    def HashPassword(self):
        salt = bcrypt.gensalt()
        self.hashedPassword = bcrypt.hashpw(self.password.encode("utf-8"), salt)
        
    def GenerateVaultkey(self):
        if(self.keyType == "16 Byte"):
            self.key = get_random_bytes(16)
        elif(self.keyType == "24 Byte"):
            self.key = get_random_bytes(24)
        elif(self.keyType == "32 Byte"):
            self.key = get_random_bytes(32)
            
        self.key = base64.b64encode(self.key).decode("utf-8")
        
    def WriteSettings(self):
        with open(".config", "a") as file:
            self.cfg.add_section(self.vaultName)
            self.cfg.set(self.vaultName, "vault-name", str(self.vaultName))
            self.cfg.set(self.vaultName, "key-type", str(self.keyType))
            self.cfg.set(self.vaultName, "vault-key", str(self.key))
            self.cfg.set(self.vaultName, "security-key", self.securityKey)
            self.cfg.write(file)
            
    def WritePasswordFile(self):
        with open((self.CRIPTY_DIR + "/" + self.vaultName + "/.psswd"), "wb") as psswdFile:
            psswdFile.write(self.hashedPassword)
            
    def CreateVault(self):
        
        if(not(os.path.exists(self.CRIPTY_DIR))):
            os.mkdir(self.CRIPTY_DIR)
            
        if(not os.path.exists(self.CRIPTY_DIR + "/" + self.vaultName)):
            os.mkdir(self.CRIPTY_DIR + "/" + self.vaultName)
        
        with open(self.CRIPTY_DIR + "/" + self.vaultName + "/encrypted_files.cfg", "w"):
            pass
        
    def SaveSecurityKey(self):
        self.securityKey = secrets.token_hex(16)
        with open(self.securityKeyPath, "w") as keyFile:
            keyFile.write(self.securityKey)