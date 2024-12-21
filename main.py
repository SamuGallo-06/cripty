from PyQt5.QtWidgets import(
    QApplication, QMainWindow
)
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
import os, sys, configparser

from windows.setupWizard import CriptySetupWizard
from windows.login import CriptyLoginWindow

    
if __name__ == "__main__":
    #Setup Application
    app = QApplication(sys.argv)
    
    #check configuration file
    if(os.path.exists(".config")):
        cfg = configparser.ConfigParser()
        cfg.read(".config")
        if(cfg.sections()):
            window = CriptyLoginWindow()
        else:
            window = CriptySetupWizard()
    else:
        window = CriptySetupWizard()
    
    window.show()
    app.exec_()