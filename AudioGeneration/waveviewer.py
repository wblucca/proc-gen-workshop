# Author
# William Lucca

import wave
import matplotlib.pyplot as plt
from AudioGeneration.audiowave import twoscompint

MAX_TITLE_LEN = 30


def readwav(*files):
    # Plot title
    title = ''
    
    numfiles = len(files)
    for i in range(numfiles):
        with wave.open(files[i], 'rb') as wavfile:
            # Plot file
            plotwav(wavfile, 'C' + str(i))
            
            # Update title
            if i < numfiles - 1:
                title += files[i] + ', '
            else:
                title += 'and ' + files[i]

    # Name the x axis
    plt.xlabel('Seconds')

    # Give title to plot
    if len(title) > MAX_TITLE_LEN:
        title = str(numfiles) + ' Files'
    if numfiles == 1:
        title = files[0]
    plt.title(title)
    
    # Show the plot
    plt.show()


def plotwav(wavfile, color):
    # Get wav file parameters
    sampwidth = wavfile.getsampwidth()
    framerate = wavfile.getframerate()
    numchannels = wavfile.getnchannels()
    numframes = wavfile.getnframes()
    
    print(sampwidth)
    print(framerate)
    print(numchannels)
    print(numframes)
    
    for channel in range(numchannels):
        # Setup this channel's plot
        plt.subplot(numchannels, 1, channel + 1)
        
        # Declare x and y values for this plot
        x = [0 for i in range(numframes // sampwidth)]
        y = [0 for i in range(numframes // sampwidth)]
        
        wavfile.setpos(0)
        
        for i in range(numframes // sampwidth):
            # X-position in seconds
            x[i] = i * sampwidth / framerate
            
            # Get a sample and extract just this channel
            audiosample = wavfile.readframes(sampwidth)
            start = (channel // numchannels) * sampwidth
            end = ((channel + 1) // numchannels) * sampwidth
            channelsample = audiosample[start: end]
            
            # Y-value is signed int, not bytes
            y[i] = twoscompint(channelsample, sampwidth // numchannels)
        
        plt.plot(x, y, color)
        for i in range(len(x)):
            print(x[i], y[i])
