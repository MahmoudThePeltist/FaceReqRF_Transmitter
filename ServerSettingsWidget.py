from PyQt4.QtGui import *
import os

class TransmissionSettings(QDialog):
    """This class provides a settings window for the server"""
    
    def __init__(self):
        super(TransmissionSettings, self).__init__()

        self.localDir = os.path.dirname(os.path.realpath(__file__))        
        self.setWindowTitle("Transmission Settings")                
        self.setWindowIcon(QIcon(self.localDir + "/images/FaceReqRFIcon.png"))        
        #Add Radio Buttons
        self.radio_group_box = QGroupBox("Please select a transmission method:") 
        self.radio_button_group = QButtonGroup()
        
        self.radio_button_0 = QRadioButton("Local Area Network")
        self.radio_button_1 = QRadioButton("HackRF One")
        
        self.radio_button_layout = QVBoxLayout()
        self.radio_button_layout.addWidget(self.radio_button_0)
        self.radio_button_layout.addWidget(self.radio_button_1)
        
        self.radio_button_group.addButton(self.radio_button_0)
        self.radio_button_group.addButton(self.radio_button_1)       
        self.radio_button_group.setId(self.radio_button_0, 0)
        self.radio_button_group.setId(self.radio_button_1, 1)
        
        self.radio_group_box.setLayout(self.radio_button_layout)
        #Add Texboxes and their labels
        self.label1 = QLabel("Adress: ")
        self.label2 = QLabel("Port: ")
        self.label3 = QLabel("Buffer: ")
        self.textBox1 = QLineEdit()
        self.textBox2 = QLineEdit()
        self.textBox3 = QLineEdit()
        self.SettingsSubmitButton = QPushButton("Submit")
        
        #create layouts
        self.setting_form_grid = QGridLayout()
        self.setting_total_layout = QVBoxLayout()
        #add lable widgets to the grid layout
        self.setting_form_grid.addWidget(self.label1,0,0)
        self.setting_form_grid.addWidget(self.label2,1,0)
        self.setting_form_grid.addWidget(self.label3,2,0)
        #add line edit widgets to the grid layout
        self.setting_form_grid.addWidget(self.textBox1,0,1)
        self.setting_form_grid.addWidget(self.textBox2,1,1)
        self.setting_form_grid.addWidget(self.textBox3,2,1)
        
        self.setting_total_layout.addWidget(self.radio_group_box)
        self.setting_total_layout.addLayout(self.setting_form_grid)
        self.setting_total_layout.addWidget(self.SettingsSubmitButton)
        
        self.setLayout(self.setting_total_layout)

        self.SettingsSubmitButton.clicked.connect(self.close)
        
        #function to set the textbox default values
    def setValues(self, transMethod, gottenAddress, gottenPort, gottenBuffer):
        print "Current Values are: ", transMethod, gottenAddress, gottenPort, gottenBuffer
        if transMethod == 0:
            self.radio_button_0.setChecked(True)
        elif transMethod == 1:
            self.radio_button_1.setChecked(True)
        self.textBox1.setText(str(gottenAddress))
        self.textBox2.setText(str(gottenPort))
        self.textBox3.setText(str(gottenBuffer))
        
        #function to return the new entered values
    def getValues(self):
        print "New values are: ", self.radio_button_group.checkedId() , self.textBox1.text(), int(self.textBox2.text()), int (self.textBox3.text())
        return self.radio_button_group.checkedId() , self.textBox1.text(), int(self.textBox2.text()), int (self.textBox3.text())