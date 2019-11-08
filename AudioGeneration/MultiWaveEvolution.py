# Author
# William Lucca

import wave
from AudioGeneration.SineWave import SineWave

# Standard audio quality: 16-bit, 44.1kHz

# Audio file parameters
BIT_DEPTH = 16  # How many bits in one audio sample for one channel
SAMP_FREQ = 44.1  # In kHz
NUM_CHANNELS = 1  # Mono or stereo
DURATION = 3  # In seconds

MAX_VOLUME = 256 ** (BIT_DEPTH // 8) - 1


def main():
    """Initializes an audio file with some parameters and writes a sine wave
    """
    
    with wave.open('output.wav', 'wb') as out:
        # Setup audio file parameters
        sampwidth = BIT_DEPTH * NUM_CHANNELS // 8
        framerate = int(SAMP_FREQ * 1000)
        numframes = int(DURATION * SAMP_FREQ * 1000)
        out.setsampwidth(sampwidth)
        out.setframerate(framerate)
        out.setnchannels(NUM_CHANNELS)
        out.setnframes(numframes)
        print(sampwidth, framerate, numframes)
        
        # Write some data
        sine = SineWave(100, 32000, 32500)
        out.writeframes(sine.getsamples(numframes, sampwidth, framerate))


if __name__ == '__main__':
    main()
