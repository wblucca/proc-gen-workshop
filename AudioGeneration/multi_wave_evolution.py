# Author
# William Lucca

import wave
from AudioGeneration.audiowave import *

# Standard audio quality: 16-bit, 44.1kHz

# Audio file parameters
BIT_DEPTH = 16  # How many bits in one audio sample for one channel
SAMP_FREQ = 44.1  # In kHz
NUM_CHANNELS = 1  # Mono or stereo
DURATION = 3  # In seconds

MAX_VOLUME = (256 ** (BIT_DEPTH // 8)) / 2 - 1


def main():
    """Initializes an audio file with some parameters and writes a sine wave
    """
    
    with wave.open('output.wav', 'wb') as outwav:
        # Setup audio file parameters
        sampwidth = BIT_DEPTH * NUM_CHANNELS // 8
        framerate = int(SAMP_FREQ * 1000)
        numframes = int(DURATION * SAMP_FREQ * 1000)
        outwav.setsampwidth(sampwidth)
        outwav.setframerate(framerate)
        outwav.setnchannels(NUM_CHANNELS)
        outwav.setnframes(numframes)
        
        # Write some data
        sine = Wave(440, -MAX_VOLUME, MAX_VOLUME)
        frames = sine.sinesamples(DURATION, sampwidth, framerate, 0.2, 0.2)
        outwav.writeframes(frames)


def mixsamples(bytespersamp, *waves):
    """Mixes multiple waves together to produce a composite wave
    
    :param bytespersamp: The depth of one sample in bytes
    :param waves: All of the sample bytes objects
    :return: The mixed audio samples as a bytes object
    :rtype: bytes
    """
    
    # Get length of shortest audio sample list
    shortestlen = -1
    for w in waves:
        if len(waves) > shortestlen:
            shortestlen = len(waves) / bytespersamp
    
    finalsamples = []
    numwaves = len(waves)
    
    # Average the individual samples of each wave one at a time
    for i in range(shortestlen, step=bytespersamp):
        # Cumulative sum for this wave
        sum = 0
        for w in waves:
            # Get signed integer value of sample and add to sum
            sum += twoscompint(w[i: i + bytespersamp], bytespersamp)
        
        # Convert average into two's complement
        average = sum // numwaves
        average = twoscompbytes(average, bytespersamp)
        
        # Push average onto finalsamples
        finalsamples.append(average)
    
    return finalsamples


if __name__ == '__main__':
    main()
