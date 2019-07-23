import cv2
import os
from moviepy.editor import ImageSequenceClip
from socket import *
from PyQt4 import QtCore
from PyQt4 import QtGui
from Image2IQFile import *
     
class ShowVideo(QtCore.QObject):
    def __init__(self, parent = None):
        super(ShowVideo, self).__init__(parent)
        #set the pause screen image
        self.localDir = os.path.dirname(os.path.realpath(__file__))
        self.pause_image = QtGui.QImage(self.localDir  + '/images/FaceRecRFWait.png')
        #General variables
        self.counter = 0
        self.skipValue = 10
        self.cameraPort = 1
        self.frame = 1
        #LAN variables
        self.transMeth = 0
        self.host = "127.0.0.1"
        self.port = 4096
        self.buf = 1024
        #HackRF variables
        self.outputFile = self.localDir +  "/frames/frameSmallG.iqhackrf"
        self.sourceFile = self.localDir +  "/frames/frameSmallG.jpg"
        self.transFreq = 440000000
        self.transBand = 1750000
        self.transSamp = 1000000
        self.lineTime = 0.005
        self.flipFrame = 0
        
    camera = cv2.VideoCapture(1)
    video_signal = QtCore.pyqtSignal(QtGui.QImage, name = 'vidSig')

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
                print "Capturing Frame: ", self.counter
                #resize and save the frame as a jpeg image locally
                frame2resize = cv2.resize(frame,(0,0),fx=self.frame,fy=self.frame)
                cv2.imwrite(self.localDir + "/frames/frame.jpg", frame2resize)
                ###Based on the chosen transmission method the images are either sent over LAN or via HACKRF
                if(self.counter >= self.skipValue):  
                    # # # if we are transmitting over LAN
                    if self.transMeth == 0:                                               
                            print "sending image: ", self.counter , " over LAN"
                            self.sendFile(self.localDir + "/frames/frame.jpg")
                            
                    # # # if we are tranmsitting over HACKRF with IQ modulation
                    elif self.transMeth == 1:   
                        print "Encoding frame: ", self.counter
                        #frame can be flipped depending on receiving waterfall                        
                        if self.flipFrame == True:
                            frame_toSend = cv2.flip(frame2resize, 0)
                        else:
                            frame_toSend = frame2resize
                        cv2.imwrite(self.localDir + "/frames/frameSmallG.jpg", frame_toSend)
                        #use the IQstream converter to convert the image into a hackrf tranmsission file
                        tran = Image2IQFile(self.transSamp,self.lineTime,self.outputFile,self.sourceFile)
                        tran.convert()
                        print "Transmiting frame: "
                        #transmit the saved image using the hackRF
                        os.system("hackrf_transfer -t " + self.localDir +  "/frames/frameSmallG.iqhackrf -f " + str(self.transFreq) + " -b " + str(self.transBand) + " -s " + str(self.transSamp) + " -x 20 -a 1")
                    # # # if we are transmitting over HACKRF with PAL modulation
                    elif self.transMeth == 2:
                        print "Encoding Video with ", self.counter, " images."
                        clip = ImageSequenceClip("recording", 10)
                        print "Writing file..."
                        clip.write_videofile(self.localDir + "/toSend.mp4",codec = "libx264")
                        os.system("hacktv -f "+str(self.transFreq)+" -m i -g 47 "+self.localDir+"/toSend.mp4")
                    #finally reset the counter
                    self.counter = 0 
                #if we are using PAL transmission save a number of images
                if self.transMeth == 2:
                    cv2.imwrite(self.localDir + "/recording/" + str(self.counter) + ".jpg", frame2resize)
                else:
                    print "skipping Frame: ", self.counter
                self.counter = self.counter + 1
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
        #set the default screen image
        self.localDir = os.path.dirname(os.path.realpath(__file__))
        self.default_image = self.localDir + '/images/FaceRecMenuImage.png'
        self.image = QtGui.QImage(self.default_image,"PNG")
        self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent)
 
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0,0, self.image)
        self.image = QtGui.QImage()
 
    @QtCore.pyqtSlot(QtGui.QImage)
    def setImage(self, image):
        if image.isNull():
            print("Viewer Dropped frame!")
        self.image = image
        if image.size() != self.size():
            self.setFixedSize(image.size())
        self.update()
