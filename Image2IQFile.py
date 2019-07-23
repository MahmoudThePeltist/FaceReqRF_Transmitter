import numpy as np
import cv2

class SpectrumPainter(object):
    """This class transmforms and image into a signal"""    
    
    def __init__(self, Fs=1000000, T_line=0.005):
        self.NFFT = 4096
        self.Fs = Fs
        self.T_line = T_line

    @property
    def repetitions(self):
        return int(np.ceil(self.T_line * self.Fs / self.NFFT))

    def convert_image(self, filename):
        #read image and store it as an array of values from 0 to 255
        pic = cv2.imread(filename)
        
        # Set FFT size to be double the image size so that the edge of the spectrum stays clear
        # preventing some bandfilter artifacts
        self.NFFT = 2*pic.shape[1]

        # Repeat image lines until each one comes often enough to reach the desired line time
        ffts = (np.flipud(np.repeat(pic[:, :, 0], self.repetitions, axis=0) / 16.)**2.) / 256. #total image

        # Embed image in center bins of the FFT
        fftall = np.zeros((ffts.shape[0], self.NFFT))#total fft
        startbin = int(self.NFFT/4)#start point of the actual image
        fftall[:, startbin:(startbin+pic.shape[1])] = ffts#setting the relevent part of the total fft to be = to the image

        # Generate random phase vectors for the FFT bins, this is important to prevent high peaks in the output
        # The phases won't be visible in the spectrum
        phases = 2*np.pi*np.random.rand(*fftall.shape)
        rffts = fftall * np.exp(1j*phases)

        # Perform the FFT per image line, then concatenate them to form the final signal
        timedata = np.fft.ifft(np.fft.ifftshift(rffts, axes=1), axis=1) / np.sqrt(float(self.NFFT))
        linear = timedata.flatten()
        linear = linear / np.max(np.abs(linear))
        return linear

class Image2IQFile(object):
    """This class creates a hackrf file to tranmsit"""
    
    def __init__(self,sampleRate = 1000000,lineTime = 0.005,outputFile = "image.iqhackrf",sourceFile = "image.jpg"):
        self.sampleRate = sampleRate #Samplerate of the radio
        self.lineTime = lineTime #Time for each line to show
        self.outputFile = outputFile #File to write to
        self.sourceFile = sourceFile #file to write from
        
    def interleave(self, complex_iq):
        # Interleave I and Q
        intlv = np.zeros(2*complex_iq.size, dtype=np.float32)
        intlv[0::2] = np.real(complex_iq)
        intlv[1::2] = np.imag(complex_iq)
        return intlv

    def clip(self, complex_iq, limit=1.0):
        # Clips amplitude to level
        clipped_samples = np.abs(complex_iq) > limit
        if np.any(clipped_samples):
            clipped = complex_iq
            clipped[clipped_samples] = complex_iq[clipped_samples] / np.abs(complex_iq[clipped_samples])
        else:
            clipped = complex_iq
        return clipped

    def convert(self):
        painter = SpectrumPainter(Fs=self.sampleRate, T_line=self.lineTime)
        self.IQSamples = painter.convert_image(self.sourceFile)
        #convert the IQ samples into hackRF format
        intlv = self.interleave(self.IQSamples)
        clipped = self.clip(intlv)
        converted = 127. * clipped
        #cast the converted data into bytes
        hackRF_out = converted.astype(np.int8) 
        # open/create a file and write the converted data to it
        f = open(self.outputFile,"w+")
        f.write(hackRF_out)