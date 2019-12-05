# Author
# William Lucca

import wave
import matplotlib.pyplot as plt


def readwav(*files):
    for file in files:
        with wave.open(file, 'rb') as wavfile:
            plotwav(wavfile)


def plotwav(wavfile):
    # Get wav file parameters
    sampwidth = wavfile.getsampwidth()
    framerate = wavfile.getframerate()
    numchannels = wavfile.getnchannels()
    numframes = wavfile.getnframes()
    
    # Get the width of a single sample for a single channel
    sampwidth //= numchannels
    
    for channel in range(numchannels):
        # Setup this channel's plot
        plt.subplot(3, 1, channel)
        
        # Define x and y values for this plot
        x, y = [], []
        
        for i in range(numframes):
            # TODO get the actual data points
            pass
        
        plt.plot(x, y, 'C' + str(channel))
        
        
        
    

# x axis values
x = [1, 2, 3]
# corresponding y axis values
y = [2, 4, 1]

# plotting the points
plt.plot(x, y)

# naming the x axis
plt.xlabel('x - axis')
# naming the y axis
plt.ylabel('y - axis')

# giving a title to my graph
plt.title('My first graph!')

# function to show the plot
plt.show()
