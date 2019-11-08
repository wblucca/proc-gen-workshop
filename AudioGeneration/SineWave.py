# Author
# William Lucca

from math import sin, pi


class SineWave:
    
    def __init__(self, freq, minvolume, maxvolume, offset=0):
        """Creates a SineWave object
        
        :param freq: The frequency of the sound wave
        :param minvolume: The maximum volume of the sound wave
        :param maxvolume: The minimum volume of the sound wave
        :param offset: The start point for the sound wave (in seconds)
        """
        
        # Store sine wave parameters
        self.freq = freq
        self.minvolume = minvolume
        self.maxvolume = maxvolume
        self.amplitude = maxvolume - minvolume
        self.offset = offset
    
    def getsamples(self, numsamp, bytespersamp=2, sampfreq=44100) -> bytes:
        """Get audio samples from this mathematically defined sine wave
        
        Default parameters use standard audio quality.
        :param numsamp: The number of samples to generate
        :param bytespersamp: The bit-depth of one sample
        :param sampfreq: The sample frequency (in Hz)
        :return: The audio samples as bytes objects
        :rtype: bytes
        """
        
        # x-coordinate for stepping through the sine wave function for samples
        x = 0
        
        # Initialize return samples as a bytes object
        samples = b''
        
        for i in range(numsamp):
            # Value of sine function [0, 1]
            sinevalue = sin(2 * pi * self.freq * (x - self.offset)) / 2 + 0.5
            
            # Map to sample volume and push to samples
            sampvolume = int(self.minvolume + (self.amplitude * sinevalue))
            samples += sampvolume.to_bytes(bytespersamp, 'little')
            
            # Step x-coordinate
            x += 1 / sampfreq
        
        return samples
