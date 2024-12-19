from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QFileDialog, QMessageBox
)

from Crypto.Cipher import AES
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
import configparser
import os
import base64

class CriptyMainWindow(QMainWindow):
    
    def __init__(self, vaultName):
        super().__init__()
        loadUi("ui/main.ui", self)
        self.vaultName = vaultName
        self.SetupEnv()
        self.SetupVault()
        self.SetupUi()
        self.cfg = configparser.ConfigParser()
        self.cfg.read(".config")
        self.show()
        
    def SetupEnv(self):
        self.currentFiles = []
        self.HOME = os.path.expanduser("~")
        self.CRIPTY_DIR = self.HOME + "/.cripty"
        self.VAULT_PATH = self.CRIPTY_DIR + "/" + self.vaultName
        self.vaultData = configparser.ConfigParser()
        self.vaultData.read(self.VAULT_PATH + "/files.ini")
        
    def SetupUi(self):
        self.setWindowIcon(QIcon("resources/icon.png"))
        vaultNameText = "<html><head/><body><p><span style=\" font-size:12pt; font-weight:700;\">" + self.vaultName + "</span></p></body></html>"
        self.vaultNameLabel.setText(vaultNameText)
        self.addFileButton.clicked.connect(self.AddFile)
        self.decryptFileButton.clicked.connect(self.DecryptFile)
        self.deleteFileButton.clicked.connect(self.OnRemoveFileClicked)
        self.currentFilesComboBox.clear()
        self.currentFilesComboBox.addItems(self.currentFiles)
        self.statusbar.showMessage("Ready!")
        
    def SetupVault(self):
        encryptedFilesPath = self.VAULT_PATH + "/encrypted_files.cfg"
        
        self.currentFiles = []

        try:
            with open(encryptedFilesPath, 'r') as f:
                for line in f:
                    original_file = line.strip().split(',')[0]
                    self.currentFiles.append(original_file)
        except FileNotFoundError:
            QMessageBox.critical(
                self,
                "Fatal Error",
                "Unable to find vault configuration file"
            )   
        except ValueError:
            QMessageBox.critical(
                self,
                "Fatal Error",
                "Configuration file is corrupted"
            ) 
        self.currentFilesComboBox.clear()
        self.currentFilesComboBox.addItems(self.currentFiles)
        
    def AddFile(self):
        self.newFilePath = QFileDialog.getOpenFileName(
            self,
            "Select file to add", 
            self.HOME, 
            "All Files(*)"
        )[0]
        
        self.vaultKey = self.cfg.get(self.vaultName, "vault-key")
        self.vaultKey = base64.b64decode(self.vaultKey)
        
        self.encryptFile(self.newFilePath, self.vaultKey)
        self.vaultKey = None
        
    def DecryptFile(self):
        selectedFile = self.currentFilesComboBox.currentText()

        encryptedFilesPath = self.VAULT_PATH + "/encrypted_files.cfg"

        associatedEncFile = None
        try:
            with open(encryptedFilesPath, 'r') as f:
                for line in f:
                    originalFile, encryptedFile = line.strip().split(',')
                    if originalFile == selectedFile:
                        associatedEncFile = encryptedFile
                        break
                        
        except FileNotFoundError:
            QMessageBox.critical(
                self,
                "Fatal Error",
                "Unable to find vault configuration file"
            )
            return
        except ValueError:
            QMessageBox.critical(
                self,
                "Fatal Error",
                "Configuration file is corrupted"
            ) 
            return

        if not associatedEncFile:
            self.statusbar.showMessage(f"No associated encrypted file found for {associatedEncFile}.")
            return

        exportPath = QFileDialog.getSaveFileName(
            self,
            "Save decrypted file",
            self.HOME
        )[0]
        if not exportPath:
            self.statusbar.showMessage("Decryption cancelled.")
            return

        self.vaultKey = self.cfg.get(self.vaultName, "vault-key")
        self.vaultKey = base64.b64decode(self.vaultKey)
        self.decrypt_file(self.vaultKey, associatedEncFile, exportPath)
        self.vaultKey = None
        self.statusbar.showMessage(f"Decrypted file saved to {exportPath}.")

        
    def encryptFile(self, filePath, key):
        cipher = AES.new(key, AES.MODE_EAX)
        with open(filePath, 'rb') as file:
            data = file.read()
        
        ciphertext, tag = cipher.encrypt_and_digest(data)

        filename = os.path.basename(filePath)
        encrypted_file_path = self.VAULT_PATH + "/" + os.path.splitext(filename)[0] + ".enc"
        with open(encrypted_file_path, 'wb') as encrypted_file:
            [encrypted_file.write(x) for x in (cipher.nonce, tag, ciphertext)]
        
        #Update elements list in GUI
        self.currentFiles.append(filePath)
        self.currentFilesComboBox.clear()
        self.currentFilesComboBox.addItems(self.currentFiles)
        self.statusbar.showMessage("Encrypted " + filePath + " and added to the vault")

        self.save_pair_text(self.VAULT_PATH + "/encrypted_files.cfg", filePath, encrypted_file_path)
        
    def decrypt_file(self, key, filePath, exportPath):
        with open(filePath, 'rb') as file:
            nonce, tag, ciphertext = [file.read(x) for x in (16, 16, -1)]

        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        data = cipher.decrypt_and_verify(ciphertext, tag)

        decryptedFilePath = exportPath
        print(decryptedFilePath)
        with open(decryptedFilePath, 'wb') as decryptedFile:
            decryptedFile.write(data)
        
        print(f"File decriptato: {decryptedFilePath}")
        
    def remove_pair_from_text(self, file_path, original_file):
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()

            with open(file_path, 'w') as f:
                for line in lines:
                    if not line.startswith(original_file + ","):
                        f.write(line)

        except FileNotFoundError:
            QMessageBox.critical(
                self,
                "Error",
                "Unable to remove the file from vault: file not found"
            ) 


    def OnRemoveFileClicked(self):
        #Warning
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Warning")
        msg.setText("Are you sure you want to delete this file?\nThe action is irreversible")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        result = msg.exec_()

        if result == QMessageBox.Yes:
            selected_file = self.currentFilesComboBox.currentText()
            print("removing", selected_file)

            encrypted_files_path = self.VAULT_PATH + "/encrypted_files.cfg"
            try:
                with open(encrypted_files_path, 'r') as f:
                    lines = f.readlines()
                for line in lines:
                    original_file, encrypted_file = line.strip().split(',')
                    if original_file == selected_file:
                        os.remove(encrypted_file)
                        break
            except FileNotFoundError:
                QMessageBox.critical(
                    self,
                    "Fatal Error",
                    "Unable to find vault configuration file"
                )
                
            self.remove_pair_from_text(encrypted_files_path, selected_file)

            self.currentFiles = []
            try:
                with open(encrypted_files_path, 'r') as f:
                    for line in f:
                        original_file, _ = line.strip().split(',')
                        self.currentFiles.append(original_file)
            except FileNotFoundError:
                QMessageBox.critical(
                    self,
                    "Fatal Error",
                    "encrypted_files.cfg is empty or doesn't exists"
                ) 
            self.currentFilesComboBox.clear()
            self.currentFilesComboBox.addItems(self.currentFiles)
            self.statusbar.showMessage(f"Removed {selected_file} from the vault.")
    
    def save_pair_text(self, file_path, original_file, encrypted_file):
        with open(file_path, 'a') as f:
            f.write(f"{original_file},{encrypted_file}\n")