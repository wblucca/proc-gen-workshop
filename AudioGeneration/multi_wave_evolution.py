# Author
# William Lucca

import wave
import multiprocessing
from AudioGeneration.audiowave import *
from AudioGeneration.note import *

# Standard audio quality: 16-bit, 44.1kHz

# Audio file parameters
BIT_DEPTH = 16  # How many bits in one audio sample for one channel
SAMP_FREQ = 44.1  # In kHz
NUM_CHANNELS = 1  # Mono or stereo

DURATION = 10  # Duration of whole audio file (seconds)
FADE = 0.06  # Duration of fade (seconds)

SAMP_WIDTH = BIT_DEPTH * NUM_CHANNELS // 8
FRAMERATE = int(SAMP_FREQ * 1000)
NUM_FRAMES = int(DURATION * SAMP_FREQ * 1000)
MAX_VOLUME = (256 ** (BIT_DEPTH // 8)) / 2 - 1


def main():
    """Initializes an audio file with some parameters and writes an audio wave
    """
    
    with wave.open('output.wav', 'wb') as outwav:
        # Setup audio file parameters
        outwav.setsampwidth(SAMP_WIDTH)
        outwav.setframerate(FRAMERATE)
        outwav.setnchannels(NUM_CHANNELS)
        outwav.setnframes(NUM_FRAMES)

        # Write some chords
        chords = [
            ['A2', 'C3', 'A3'],
            ['B2', 'D3', 'B3'],
            ['C3', 'E3', 'C4'],
            ['B2', 'D3', 'B3'],
            ['A2', 'C3', 'A3'],
            ['B2', 'D3', 'B3'],
            ['C3', 'E3', 'C4']
        ]
        for c in chords:
            writechord(outwav, c, DURATION / len(chords))
        
        outwav.close()


def writechord(outwav, notes, duration):
    # Create pool of worker processes for generating digital audio samples
    pool = multiprocessing.Pool(4)
    
    # Make some audio wave objects
    waves = []
    for n in notes:
        waves.append(Wave(Note(n).freq, -MAX_VOLUME, MAX_VOLUME))
    
    # Get their digital audio samples (expensive!)
    results = []
    for w in waves:
        results.append(pool.apply_async(
                w.sinesamples,
                args=(duration, SAMP_WIDTH, FRAMERATE, FADE, FADE)
        ))
    
    # Retrieve samples from pool's results objects
    generatedsounds = []
    for r in results:
        audio = r.get()
        generatedsounds.append(audio)
    
    # Mix all of the generated waves
    mixed = mixsamples(SAMP_WIDTH, generatedsounds)
    
    # Clean up pool processes
    pool.close()
    pool.join()
    
    # Write to wav file
    outwav.writeframes(mixed)


def mixsamples(bytespersamp, waves):
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
    
    finalsamples = bytearray(shortestlen)
    numwaves = len(waves)
    
    # Index in finalsamples bytearray
    s = 0
    
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
            finalsamples[s] = byte
            s += 1
    
    return bytes(finalsamples)


if __name__ == '__main__':
    main()
