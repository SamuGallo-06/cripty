from PyQt5.QtWidgets import(
    QApplication, QMainWindow
)
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
import os, sys

from setupWizard import CriptySetupWizard
from login import CriptyLoginWindow

    
if __name__ == "__main__":
    #Setup Application
    app = QApplication(sys.argv)
    if(os.path.exists(".config")):
        window = CriptyLoginWindow()
    else:
        window = CriptySetupWizard()
        window.show()
    app.exec_()