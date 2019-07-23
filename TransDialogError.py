import os
import sys
#pyqt import
from PyQt4.QtGui import *
from PyQt4.QtCore import *


class errorBox(QDialog):
    """This class will display a dialog that contains exception info"""  
    
    def __init__(self,errorText = "Error box Error"):
        super(errorBox,self).__init__()
        #get local directory
        if getattr(sys, 'frozen', False):
            # The application is frozen
            self.localDir = os.path.dirname(sys.executable)
        else:
            # The application is not frozen
            self.localDir = os.path.dirname(os.path.realpath(__file__))    
        #set the window title and icon
        self.setWindowTitle("Error")
        self.setWindowIcon(QIcon(self.localDir + "/images/FaceReqRFIcon.png"))
        #add buttons label and textbox
        self.errorLabel = QLabel(errorText)
        self.okBtn = QPushButton("Ok")
        #add connection
        self.okBtn.clicked.connect(self.close)
        #setup layouts
        self.popupLayout = QVBoxLayout()        
        self.popupLayout.addWidget(self.errorLabel)        
        self.popupLayout.addWidget(self.okBtn)        
        self.setLayout(self.popupLayout)
        self.exec_()