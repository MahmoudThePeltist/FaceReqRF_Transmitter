from PyQt4.QtGui import *
import os

class helpMenu(QDialog):
    """This class will display a dialog that contains help info"""
    
    def __init__(self):
        super(helpMenu,self).__init__()        
        #get the local directory
        if getattr(sys, 'frozen', False):
            # The application is frozen
            self.localDir = os.path.dirname(sys.executable)
        else:
            # The application is not frozen
            self.localDir = os.path.dirname(os.path.realpath(__file__))    
        #set the window title and icon
        self.setWindowTitle("Help")
        self.setWindowIcon(QIcon(self.localDir + "/images/FaceReqRFIcon.png"))
        self.setGeometry(25,50,500,500)
        #add labels and buttons
        self.title1 = QLabel("What is this app?")
        self.title2 = QLabel("\nWhat can it do?")
        self.title3 = QLabel("\nHow do I use it?")
        self.text1 = QTextEdit()
        self.text2 = QTextEdit()
        self.text3 = QTextEdit()
        self.doneButton = QPushButton("done")
        #set the font options.
        font_A = QFont('Helvetica',15)
        font_B = QFont('Helvetica',12)
        self.title1.setFont(font_A)
        self.title2.setFont(font_A)
        self.title3.setFont(font_A)
        self.text1.setFont(font_B)
        self.text2.setFont(font_B)
        self.text3.setFont(font_B)
        #set the textboxes to be read only
        self.text1.setReadOnly(True)
        self.text2.setReadOnly(True)
        self.text3.setReadOnly(True)
        #add content to textboxes
        self.text1.setHtml("This is the transmitter portion of FaceReqRF, which is a security application "\
                            "that utilizes facial recognition, created by Mahmoud Aburas and Soliman Shaloof.")
        self.text2.setHtml("It can be used to transmit Image data either over a local network or using a HackRF"\
                            " One SDR periphral.")
        self.text3.setHtml("1 - First make sure that a camera (a webcam) is connected to the device you are using."\
                            "<br><br>2 - Select the camera port and transmition method you want to use from the settings menu."\
                            "<br><br>3 - If you choose LAN, make sure you enter the address of the receiver device"\
                            ", you can find it in the receiver application's 'reception settings' menu."\
                            "<br><br>4 - If you choose HackRF transmission, set the frequency to a suitable and legal"\
                            " value, you may change the 'Sampling Rate' and 'Bandwidth' settings if the received image"\
                            " is deformed, you may lower the 'Image Resize' to improve performance at the cost of"\
                            " quality if using a low RAM device."
                            "<br><br>5 - After you decide on a suitable transmission method, click '<< Start Transmission>>'"\
                            " to begin sending the image data being captured by the webcam.")
        #create and setup layouts
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.title1)
        self.mainLayout.addWidget(self.text1)
        self.mainLayout.addWidget(self.title2)
        self.mainLayout.addWidget(self.text2)
        self.mainLayout.addWidget(self.title3)
        self.mainLayout.addWidget(self.text3)
        #set the layout for the dialog box
        self.setLayout(self.mainLayout)