import cv2
import sys
import os
from socket import *

from PyQt4 import QtCore
from PyQt4 import QtGui

from ServerSettingsWidget import *

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
        
    def create_menu_layout(self):
        #Video classes:
        thread = QtCore.QThread()
        thread.start()
        self.vid = ShowVideo()
        self.vid.moveToThread(thread)
        self.image_viewer = ImageViewer()
        #Buttons:
        self.start_button = QtGui.QPushButton('<< Start Transmition >>')
        self.pause_button = QtGui.QPushButton('<< Pause Transmition >>')
        self.settings_button = QtGui.QPushButton('Transmission Settings')
        self.quit_button = QtGui.QPushButton('Quit')
        #Connections:    
        self.start_button.clicked.connect(self.vid.startVideo)
        self.pause_button.clicked.connect(self.pauseVideo)
        self.settings_button.clicked.connect(self.modifySettings)
        self.quit_button.clicked.connect(self.quitProgram)
        self.vid.video_signal.connect(self.image_viewer.setImage)
        #Layouts:
        self.total_layout = QtGui.QVBoxLayout()
        self.button_layout_A = QtGui.QHBoxLayout()
        self.button_layout_B = QtGui.QHBoxLayout()
        #add Widgets to their layouts
        self.button_layout_A.addWidget(self.start_button)
        self.button_layout_A.addWidget(self.pause_button)
        self.button_layout_B.addWidget(self.settings_button)
        self.button_layout_B.addWidget(self.quit_button)
        self.total_layout.addWidget(self.image_viewer)
        self.total_layout.addLayout(self.button_layout_A)
        self.total_layout.addLayout(self.button_layout_B)
        #create widget to display this layout
        self.layout_widget = QtGui.QWidget()
        self.layout_widget.setLayout(self.total_layout)
        self.vid.run_video = False
        
    def pauseVideo(self):
        print "Pausing Video..."
        self.vid.run_video = False

    def modifySettings(self):
        #instantiate the dialog box
        self.settings_dialog = TransmissionSettings()
        #set values
        self.settings_dialog.setValues(self.vid.transMeth,self.vid.host,self.vid.port,self.vid.buf)
        print "Running dialog box."
        self.settings_dialog.exec_()
        print "Getting setting values."
        self.vid.transMeth,self.vid.host,self.vid.port,self.vid.buf = self.settings_dialog.getValues()
        
    def quitProgram(self):
        print "Quiting..."
        self.close()
        
class ShowVideo(QtCore.QObject):
    def __init__(self, parent = None):
        super(ShowVideo, self).__init__(parent)
        #set the pause screen image
        self.localDir = os.path.dirname(os.path.realpath(__file__))
        self.pause_image = QtGui.QImage(self.localDir  + '/images/FaceRecRFWait.png')
        self.counter = 0
        self.transMeth = 0
        self.host = "127.0.0.1"
        self.port = 4096
        self.buf = 1024
    
    camera_port = 0
    camera = cv2.VideoCapture(camera_port)
        
    video_signal = QtCore.pyqtSignal(QtGui.QImage)

    def sendFile(self, fName):
        #open socket to transmit data
        s = socket()
        s.connect((self.host, self.port))
        f = open(fName, "rb") #open file to be transmited
        print 'Sending ', fName, ' to ', self.host, self.port
        data = f.read(self.buf)
        while data:
            s.send(data)
            data = f.read(self.buf)
        f.close()#close file after transmission
        print "done sending"
        s.shutdown(SHUT_WR)
        print s.recv(self.buf)
        s.close()#close socket after transmission
        
    @QtCore.pyqtSlot()
    def startVideo(self): 
        print "Starting Video..."
        self.run_video = True
        while self.run_video:
            ret,frame = self.camera.read()
            if ret == True:
                #get frames from CNT class
                self.counter = self.counter + 1
                print "Creating Frame: ", self.counter
                #save the frame as a jpeg image locally
                cv2.imwrite(self.localDir + "/frames/frame%d.jpg" % self.counter, frame)
                ###Based on the chosen transmission method the images are either sent over LAN or via HACKRF
                if self.transMeth == 0:
                    if(self.counter == 3):                            
                            print "sending image: ", self.counter , " over LAN"
                            self.sendFile(self.localDir + "/frames/frame%d.jpg" % self.counter)
                    else:
                        print "skipping image: ", self.counter
                
                elif self.transMeth == 1:   
                    if(self.counter == 3):               
                        print "Encoding an resizing frame: ", self.counter
                        frame_small = cv2.resize(frame,(0,0),fx=0.90,fy=0.90)
                        frame_fliped = cv2.flip(frame_small, 0)
                        cv2.imwrite(self.localDir + "/frames/frameSmallG.jpg", frame_fliped)
                        os.system("python " + self.localDir +  "/spectrum_painter/img2iqstream.py -s 1000000 -l 0.004 -o " + self.localDir +  "/frames/frameSmallG.iqhackrf --format hackrf " + self.localDir +  "/frames/frameSmallG.jpg")
                        print "Transmiting frame: 3"
                        #transmit the saved image using the hackRF
                        os.system("hackrf_transfer -t /home/pi/ProjectFiles/Server/frames/frameSmallG.iqhackrf -f 440000000 -b 1750000 -s 100000 -x 20 -a 1")
                    else:
                        print "skipping image: ", self.counter
                
                #reset the counter so that the stored images don't go over 100
                if self.counter > 3:
                    self.counter = 0
                #do operations to make cv2 video compatible with PyQt4
                color_swapped_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)             
                height, width, _ = color_swapped_image.shape                
                qt_image = QtGui.QImage(color_swapped_image.data,
                                        width,
                                        height,
                                        color_swapped_image.strides[0],
                                        QtGui.QImage.Format_RGB888)
                self.video_signal.emit(qt_image)#emit the QImage
        #set the default image and transmit it
        self.emitted_signal = self.video_signal.emit(self.pause_image)
        

 
class ImageViewer(QtGui.QWidget):
    def __init__(self, parent = None):
        super(ImageViewer, self).__init__(parent)
        self.image = QtGui.QImage()
        #set the default screen image
        self.localDir = os.path.dirname(os.path.realpath(__file__))
        self.default_image = self.localDir + '/images/FaceRecMenuImage.png'
        self.image = QtGui.QImage(self.default_image,"PNG")
        self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent)
 
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0,0, self.image)
        self.image = QtGui.QImage()
 
    def initUI(self):
        self.setWindowTitle('Test')
 
    @QtCore.pyqtSlot(QtGui.QImage)
    def setImage(self, image):
        if image.isNull():
            print("Viewer Dropped frame!")
 
        self.image = image
        if image.size() != self.size():
            self.setFixedSize(image.size())
        self.update()
 
 
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