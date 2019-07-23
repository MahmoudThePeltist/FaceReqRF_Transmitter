import cv2
import sys
import os

from PyQt4 import QtCore
from PyQt4 import QtGui

from TransSettingsWidget import *
from TransDisplayMethods import *

class mainWindow(QtGui.QMainWindow):
    def __init__(self):
        #call super user constructor
        super(mainWindow,self).__init__()
        #get local directory        
        self.localDir = os.path.dirname(os.path.realpath(__file__))
        #set window title
        self.setWindowTitle("FaceReqRF - Transmission")
        self.setWindowIcon(QIcon(self.localDir + "/images/FaceReqRFIcon.png"))
        #stylesheet
        self.setStyleSheet("QPushButton {background-color: #7a92ba; height:30%; border: none; color:white; font-size:16px;} QPushButton:hover{background-color: #5370a0}")
        #call the function to create the window
        self.create_menu_layout()
        #select the central widget to display the layout
        self.central_widget = QtGui.QWidget()
        self.central_widget.setLayout(self.total_layout)
        self.setCentralWidget(self.central_widget)
        #falgs
        self.tranFlag = False
        
    def create_menu_layout(self):
        #Video classes:
        self.thread = QtCore.QThread()
        self.thread.start()
        self.vid = ShowVideo()
        self.vid.moveToThread(self.thread)
        self.image_viewer = ImageViewer()
        #Buttons:
        self.transmit_button = QtGui.QPushButton('<< Start Transmition >>')
        self.settings_button = QtGui.QPushButton('Transmission Settings')
        self.quit_button = QtGui.QPushButton('Quit')
        #Connections:    
        self.transmit_button.clicked.connect(self.startVideo)
        self.settings_button.clicked.connect(self.modifySettings)
        self.quit_button.clicked.connect(self.quitProgram)
        self.vid.video_signal.connect(self.image_viewer.setImage)
        #next is a button designed to do nothing but start transmission, this is to "fix" the 
        #error that happens when self.vid.startVideo() is called ouside of a button click
        self.invisible_start_btn = QPushButton("you should not be seeing this")
        self.invisible_start_btn.clicked.connect(self.vid.startVideo)
        #Layouts:
        self.total_layout = QtGui.QVBoxLayout()
        self.button_layout_B = QtGui.QHBoxLayout()
        #add Widgets to their layouts
        self.button_layout_B.addWidget(self.settings_button)
        self.button_layout_B.addWidget(self.quit_button)
        self.total_layout.addWidget(self.image_viewer)
        self.total_layout.addWidget(self.transmit_button)
        self.total_layout.addLayout(self.button_layout_B)
        #create widget to display this layout
        self.layout_widget = QtGui.QWidget()
        self.layout_widget.setLayout(self.total_layout)
        self.vid.run_video = False
        
    def startVideo(self):
        #if we are transmitting pause and if we are paused start transmitting
        if self.tranFlag == False:
            #call self.video.startVideo() func with this click() see func where btn is defined for more info
            self.invisible_start_btn.click()
            self.tranFlag = True #set local flag            
            print "Starting transmission..."
            self.transmit_button.setText(">> Pause Transmission <<") #change the text written on the btn
        elif self.tranFlag == True:
            print "Pausing reception..."
            self.vid.run_video = False #set the startVideo function flag off, so we pause
            self.tranFlag = False #set local flag
            self.transmit_button.setText("<< Start Transmission >>")  #change the text written on the btn
            

    def modifySettings(self):
        #pause stream
        if self.tranFlag == True:
            self.startVideo()
        #instantiate the dialog box
        self.settings_dialog = TransmissionSettings()
        #set values
        self.settings_dialog.setValues(self.vid.transMeth,self.vid.host,self.vid.port,self.vid.buf,self.vid.transFreq,self.vid.transSamp,self.vid.transBand,self.vid.cameraPort, self.vid.flipFrame, self.vid.frameX, self.vid.frameY, self.vid.skipValue)
        print "Running dialog box."
        self.settings_dialog.exec_()
        print "Getting setting values."
        self.vid.transMeth,self.vid.host,self.vid.port,self.vid.buf,self.vid.transFreq,self.vid.transSamp,self.vid.transBand, newCamPort, self.vid.flipFrame, self.vid.frameX, self.vid.frameY, self.vid.skipValue = self.settings_dialog.getValues()
        if self.vid.cameraPort != newCamPort:
            self.vid.cameraPort == newCamPort            
            self.vid.camera = cv2.VideoCapture(self.vid.cameraPort)    
        
    def quitProgram(self):
        print "Quiting..."
        self.close()
 
def main():
    application = QtGui.QApplication(sys.argv) #create new application
    main_window = mainWindow() #Create new instance of main window
    main_window.setGeometry(25,50,600,580)
    main_window.show() #make instance visible
    main_window.raise_() #raise window to the top of window stack
    application.exec_() #monitor application for events
    sys.exit(application.exec_())
    sys.exit(main_window.vid.pauseVideo)
    
    
if __name__ == "__main__":
    main()
