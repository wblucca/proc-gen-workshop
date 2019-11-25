# Author
# William Lucca

import wave
import random
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
        sineA1 = Wave(440, -MAX_VOLUME, MAX_VOLUME)
        sineA2 = Wave(444, -MAX_VOLUME, MAX_VOLUME)
        framesA1 = sineA1.sinesamples(DURATION, sampwidth, framerate, 0.2, 0.2)
        framesA2 = sineA2.sinesamples(DURATION, sampwidth, framerate, 0.2, 0.2)
        
        mixed = mixsamples(sampwidth, framesA1, framesA2)
        outwav.writeframes(mixed)


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
        if len(w) > shortestlen:
            shortestlen = len(w)
    
    finalsamples = bytearray()
    numwaves = len(waves)
    
    # Average the individual samples of each wave one at a time
    for i in range(0, shortestlen, bytespersamp):
        # Cumulative sum for this wave
        total = 0
        for w in waves:
            # Get signed integer value of sample and add to sum
            sample = w[i: i + bytespersamp]
            total += twoscompint(sample, bytespersamp)
        
        # Convert average into two's complement
        average = total // numwaves
        average = twoscompbytes(average, bytespersamp)
        
        # Push average onto finalsamples
        for byte in average:
            finalsamples.append(byte)

    return bytes(finalsamples)


if __name__ == '__main__':
    main()
