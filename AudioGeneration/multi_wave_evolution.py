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
DURATION = 1.8  # In seconds

MAX_VOLUME = (256 ** (BIT_DEPTH // 8)) / 2 - 1

# Store all the generated wave sounds
generatedsounds = []


def main():
    """Initializes an audio file with some parameters and writes an audio wave
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
        
        # Create pool of worker processes for generating digital audio samples
        pool = multiprocessing.Pool(4)
        
        # Make some audio wave objects
        notes = ['A3', 'C#4', 'E4', 'A4']
        waves = []
        for n in notes:
            waves.append(Wave(Note(n).freq, -MAX_VOLUME, MAX_VOLUME))
        
        # Get their digital audio samples (expensive!)
        results = []
        for w in waves:
            results.append(pool.apply_async(
                    w.sinesamples,
                    args=(DURATION, sampwidth, framerate, 0.1, 0.1)
            ))
        
        # Retrieve samples from pool's results objects
        for r in results:
            audio = r.get()
            generatedsounds.append(audio)
        
        # Mix all of the generated waves
        mixed = mixsamples(sampwidth, generatedsounds)
        
        # Clean up pool processes
        pool.close()
        pool.join()
        
        # Write to wav file
        outwav.writeframes(mixed)
        outwav.close()


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
