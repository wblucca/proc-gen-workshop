# Author
# William Lucca

import wave
from random import random

import matplotlib.pyplot as plt
from AudioGeneration.audiowave import twoscompint

MAX_TITLE_LEN = 45

# List of axes for plotting on
axes = []


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
                title += files[i]
    
    # Name the x axis
    plt.xlabel('Seconds')
    
    # Switch back to top subplot
    if len(axes) > 0:
        plt.sca(axes[0])
    
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
    
    for channel in range(numchannels):
        # Setup this channel's plot (if it doesn't exist)
        if channel > len(axes) - 1:
            axes.insert(channel, plt.subplot(numchannels, 1, channel + 1))
        
        # Declare x and y values for this plot
        x = [0 for i in range(numframes // sampwidth)]
        y = [0 for i in range(numframes // sampwidth)]
        
        wavfile.setpos(0)
        
        for i in range(numframes // sampwidth):
            # X-position in seconds
            x[i] = i * sampwidth / framerate
            
            # Get a sample and extract just this channel
            audiosample = wavfile.readframes(sampwidth)
            start = channel * sampwidth // numchannels
            end = (channel + 1) * sampwidth // numchannels
            channelsample = audiosample[start: end]
            
            # Y-value is signed int, not bytes
            y[i] = twoscompint(channelsample, sampwidth // numchannels)
        
        axes[channel].plot(x, y, color)
