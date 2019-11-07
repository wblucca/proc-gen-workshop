# Author
# William Lucca

import wave

# Standard audio quality: 16-bit, 44.1kHz

# Audio file parameters
NUM_CHANNELS = 1  # Mono or stereo
BIT_DEPTH = 16  # How many bits in one audio sample
SAMP_FREQ = 44.1  # In kHz
DURATION = 3  # In seconds


def main():
    """Initializes an audio file with some parameters and writes a sine wave"""
    
    with wave.open('output.wav', 'w') as out:
        # Setup audio file parameters
        out.setnchannels(NUM_CHANNELS)
        out.setsampwidth(int(BIT_DEPTH * NUM_CHANNELS // 8))
        out.setframerate(int(SAMP_FREQ * 1000))
        out.setnframes(int(DURATION * SAMP_FREQ * 1000))
        
        # Write some data
        pass


if __name__ == '__main__':
    main()
