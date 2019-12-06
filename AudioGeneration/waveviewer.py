# Author
# William Lucca

import wave
import matplotlib.pyplot as plt

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
    plt.title(title)
    
    # Show the plot
    plt.show()


def plotwav(wavfile, color):
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
        
        # Declare x and y values for this plot
        x = [0 for i in range(numframes)]
        y = [0 for i in range(numframes)]
        
        for i in range(numframes):
            # TODO get the actual data points
            x[i] = 0
        
        plt.plot(x, y, color)
