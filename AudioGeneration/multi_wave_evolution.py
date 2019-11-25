# Author
# William Lucca

import wave
from AudioGeneration.audiowave import Wave

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

def mixsamples(numsecs, bytespersamp, sampfreq, *waves):
    """Mixes multiple waves together to produce a composite wave
    
    :param numsecs: The number of seconds to generate
    :param bytespersamp: The depth of one sample in bytes
    :param sampfreq: The sample frequency (in Hz)
    :param waves: All of the waves to mix together
    :return: The mixed audio samples as a bytes object
    :rtype: bytes
    """
    
    pass


if __name__ == '__main__':
    main()
