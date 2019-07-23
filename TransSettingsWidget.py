from PyQt4.QtGui import *
import os
import sys

class TransmissionSettings(QDialog):
    """This class provides a settings window for the transmitter application"""
    
    def __init__(self):
        super(TransmissionSettings, self).__init__()
        #get the local directory
        if getattr(sys, 'frozen', False):
            # The application is frozen
            self.localDir = os.path.dirname(sys.executable)
        else:
            # The application is not frozen
            self.localDir = os.path.dirname(os.path.realpath(__file__))    
        
        self.setWindowTitle("Transmission Settings")                
        self.setWindowIcon(QIcon(self.localDir + "/images/FaceReqRFIcon.png")) 
        
        #Create Radio Button group and radio buttons
        self.radio_button_group = QButtonGroup()
        self.radio_button_0 = QRadioButton("Local Area Network")
        self.radio_button_1 = QRadioButton("HackRF One - IQ Modulation")
        self.radio_button_2 = QRadioButton("HackRF One - Pal Modulation")
        #connect each radio button to a fuction
        self.radio_button_0.clicked.connect(self.clicked_LAN)
        self.radio_button_1.clicked.connect(self.clicked_RF)
        self.radio_button_2.clicked.connect(self.clicked_PAL)
        #create layout and add the buttons
        self.radio_button_layout = QVBoxLayout()
        self.radio_button_layout.addWidget(self.radio_button_0)
        self.radio_button_layout.addWidget(self.radio_button_1)
        self.radio_button_layout.addWidget(self.radio_button_2)
        #add buttons to button group
        self.radio_button_group.addButton(self.radio_button_0)
        self.radio_button_group.addButton(self.radio_button_1) 
        self.radio_button_group.addButton(self.radio_button_2) 
        #set button IDs      
        self.radio_button_group.setId(self.radio_button_0, 0)
        self.radio_button_group.setId(self.radio_button_1, 1)   
        self.radio_button_group.setId(self.radio_button_2, 2)               
        #create the labels and textboxes
        self.label1 = QLabel("Adress: ")
        self.label2 = QLabel("Port: ")
        self.label3 = QLabel("Buffer: ")
        self.label4 = QLabel("Frequency: ")
        self.label5 = QLabel("Sample Rate: ")
        self.label6 = QLabel("Bandwidth: ")
        self.label9 = QLabel("Flip Image: ")
        self.label7 = QLabel("Camera Port: ")
        self.label8 = QLabel("Image resize: ")
        self.label10 = QLabel("Frames to Skip: ")
        self.textBox1 = QLineEdit()
        self.textBox2 = QLineEdit()
        self.textBox3 = QLineEdit()
        self.textBox4 = QLineEdit()
        self.textBox5 = QLineEdit()
        self.textBox6 = QLineEdit()
        self.textBox7 = QLineEdit()
        self.textBox8 = QLineEdit()
        self.textBox9 = QLineEdit()
        self.checkBox1 = QCheckBox()
        #create submit button and connect it to function
        self.SettingsSubmitButton = QPushButton("Submit")  
        self.SettingsSubmitButton.clicked.connect(self.close)
        #create layouts
        self.LAN_setting_form_layout = QGridLayout()
        self.RF_setting_form_layout = QGridLayout()
        self.Other_setting_form_layout = QGridLayout()
        self.setting_total_layout = QVBoxLayout()
        #add lable widgets to the grid layout
        self.LAN_setting_form_layout.addWidget(self.label1,0,0)
        self.LAN_setting_form_layout.addWidget(self.label2,1,0)
        self.LAN_setting_form_layout.addWidget(self.label3,2,0)
        self.RF_setting_form_layout.addWidget(self.label4,0,0)
        self.RF_setting_form_layout.addWidget(self.label5,1,0)
        self.RF_setting_form_layout.addWidget(self.label6,2,0)
        self.RF_setting_form_layout.addWidget(self.label9,3,0)
        self.Other_setting_form_layout.addWidget(self.label7,0,0)
        self.Other_setting_form_layout.addWidget(self.label8,1,0)
        self.Other_setting_form_layout.addWidget(self.label10,2,0)
        #add line edit widgets to the grid layout
        self.LAN_setting_form_layout.addWidget(self.textBox1,0,1)
        self.LAN_setting_form_layout.addWidget(self.textBox2,1,1)
        self.LAN_setting_form_layout.addWidget(self.textBox3,2,1)
        self.RF_setting_form_layout.addWidget(self.textBox4,0,1)
        self.RF_setting_form_layout.addWidget(self.textBox5,1,1)
        self.RF_setting_form_layout.addWidget(self.textBox6,2,1)
        self.RF_setting_form_layout.addWidget(self.checkBox1,3,1)
        self.Other_setting_form_layout.addWidget(self.textBox7,0,1)
        self.Other_setting_form_layout.addWidget(self.textBox8,1,1)
        self.Other_setting_form_layout.addWidget(self.textBox9,2,1)
        #create group boxes for each part of the window
        self.radio_group_box = QGroupBox("Please select a transmission method:") 
        self.Other_group_box = QGroupBox("General Settings:") 
        self.LAN_group_box = QGroupBox("Lan Settings:") 
        self.RF_group_box = QGroupBox("RF Settings:") 
        #add QWidget layouts to group boxes
        self.radio_group_box.setLayout(self.radio_button_layout)
        self.Other_group_box.setLayout(self.Other_setting_form_layout)
        self.LAN_group_box.setLayout(self.LAN_setting_form_layout)
        self.RF_group_box.setLayout(self.RF_setting_form_layout)
        #add the group boxes and button widget to layout 
        self.setting_total_layout.addWidget(self.radio_group_box)
        self.setting_total_layout.addWidget(self.Other_group_box)
        self.setting_total_layout.addWidget(self.LAN_group_box)
        self.setting_total_layout.addWidget(self.RF_group_box)
        self.setting_total_layout.addWidget(self.SettingsSubmitButton)
        #set the widget layout as the total layout
        self.setLayout(self.setting_total_layout)
        
    #function to set the textbox default values
    def setValues(self, transMethod, gottenAddress, gottenPort, gottenBuffer, gottenFrequency, gottenSampRate, gottenBandwidth, gottenCamPort, gottenFlip, gottenResize, gottenSkipValue):
        print "Current LAN Values are: ", transMethod, gottenAddress, gottenPort, gottenBuffer
        print "Current RF Values are: ", gottenFrequency, gottenSampRate, gottenBandwidth, gottenFlip
        print "Current Camera port: ", gottenCamPort, " - Resize value: ", gottenResize, " - Skipping ", gottenSkipValue, " - Frames."
        if transMethod == 0:
            self.radio_button_0.setChecked(True)
            self.LAN_group_box.show()
            self.RF_group_box.hide()
        elif transMethod == 1:
            self.radio_button_1.setChecked(True)
            self.LAN_group_box.hide()
            self.RF_group_box.show()
            self.label5.show()
            self.label6.show()
            self.label9.show()
            self.textBox5.show()
            self.textBox6.show()
            self.checkBox1.show()
        elif transMethod == 2:
            self.radio_button_2.setChecked(True)
            self.LAN_group_box.hide()
            self.RF_group_box.show()
            self.label5.hide()
            self.label6.hide()
            self.label9.hide()
            self.textBox5.hide()
            self.textBox6.hide()
            self.checkBox1.hide()
        self.textBox1.setText(str(gottenAddress))
        self.textBox2.setText(str(gottenPort))
        self.textBox3.setText(str(gottenBuffer))
        self.textBox4.setText(str(gottenFrequency))
        self.textBox5.setText(str(gottenSampRate))
        self.textBox6.setText(str(gottenBandwidth))
        self.textBox7.setText(str(gottenCamPort))
        self.textBox8.setText(str(gottenResize))
        self.textBox9.setText(str(gottenSkipValue))
        if gottenFlip == 0:
            self.checkBox1.setChecked(0)
        elif gottenFlip == 1:
            self.checkBox1.setChecked(1)
        
    #function to return the new entered values
    def getValues(self):
        print "New LAN values are: ", self.radio_button_group.checkedId() , self.textBox1.text(), int(self.textBox2.text()), int(self.textBox3.text())
        print "New RF values are: ", int(self.textBox4.text()), int(self.textBox5.text()), int(self.textBox6.text()), int(self.checkBox1.isChecked())
        print "New Camera port is: ", int(self.textBox7.text()), " - Resize value: ", int(self.textBox8.text()), " - Skipping ", int(self.textBox9.text()), " Frames."
        return self.radio_button_group.checkedId() , self.textBox1.text(), int(self.textBox2.text()), int(self.textBox3.text()), int(self.textBox4.text()), int(self.textBox5.text()), int(self.textBox6.text()),  int(self.textBox7.text()), int(self.checkBox1.isChecked()), int(self.textBox8.text()), int(self.textBox9.text())
        
    #functions to control which settings are enabled or disabled
    def clicked_LAN(self):
        self.RF_group_box.hide()
        self.LAN_group_box.show()
    def clicked_RF(self):
        self.RF_group_box.setTitle("IQ modulation settings:")
        self.LAN_group_box.hide()
        self.RF_group_box.show()
        self.label5.show()
        self.label6.show()
        self.label9.show()
        self.textBox5.show()
        self.textBox6.show()
        self.checkBox1.show()
    def clicked_PAL(self):
        self.RF_group_box.setTitle("Pal settings:")
        self.LAN_group_box.hide()
        self.RF_group_box.show()
        self.label5.hide()
        self.label6.hide()
        self.label9.hide()
        self.textBox5.hide()
        self.textBox6.hide()
        self.checkBox1.hide()