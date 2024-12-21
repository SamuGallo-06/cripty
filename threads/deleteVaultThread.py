from PyQt5.QtCore import QThread
import os
import configparser
import time

class DeleteVaultThread(QThread):
    
    def __init__(self, progressbar, vaultName, logLabel):
        super().__init__()
        self.progressbar = progressbar
        self.progressbar.setValue(0)
        self.vaultName = vaultName
        self.logLabel = logLabel
        
    def run(self):
        self.TOTAL_OPERATIONS = 2
        self.progress = 0
        self.HOME = os.path.expanduser("~")
        self.CRIPTY_DIR = self.HOME + "/.cripty"
        self.cfg = configparser.ConfigParser()
        self.cfg.read(".config")
        self.RemoveVaultDirectory()
        self.UpdateConfigurationFile()
        self.logLabel.setText("Done")
        
    def RemoveVaultDirectory(self):
        self.logLabel.setText("Removing vault")
        self.TOTAL_OPERATIONS += len(os.listdir(self.CRIPTY_DIR + "/" + self.vaultName))
        print("Total operations: " + str(self.TOTAL_OPERATIONS))
        
        #remove all files in the vault directory
        for file in os.listdir(self.CRIPTY_DIR + "/" + self.vaultName):
            print("Removing " + file + " from vault")
            os.remove(self.CRIPTY_DIR + "/" + self.vaultName + "/" + file)
            self.progress += 1
            self.progressbar.setValue(int((self.progress / self.TOTAL_OPERATIONS) * 100))
            time.sleep(0.1)
        
        #and then remove the directory.
        os.rmdir(self.CRIPTY_DIR + "/" + self.vaultName)
        time.sleep(0.2)
        
        self.progress += 1
        self.progressbar.setValue(int((self.progress / self.TOTAL_OPERATIONS) * 100))
        
    def UpdateConfigurationFile(self):
        self.logLabel.setText("Updating Configuration file")
        with open(".config", "w") as cfgFile:
            self.cfg.remove_section(self.vaultName)
            self.cfg.write(cfgFile)
        time.sleep(0.2)
        self.progress += 1
        self.progressbar.setValue(int((self.progress / self.TOTAL_OPERATIONS) * 100))