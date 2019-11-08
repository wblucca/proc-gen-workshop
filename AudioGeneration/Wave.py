# Author
# William Lucca

from math import sin, pi


class Wave:
    
    def __init__(self, freq, minvolume, maxvolume, offset=0):
        """Creates a SineWave object
        
        :param freq: The frequency of the sound wave
        :param minvolume: The maximum volume of the sound wave
        :param maxvolume: The minimum volume of the sound wave
        :param offset: The start point for the sound wave (in seconds)
        """
        
        # Store sine wave parameters
        self.freq = freq
        self.minvolume = int(minvolume)
        self.maxvolume = int(maxvolume)
        self.amplitude = self.maxvolume - self.minvolume
        self.offset = offset
    
    def sinesamples(self, numsamp, bytespersamp=2, sampfreq=44100) -> bytes:
        """Get audio samples from the wave's attributes using a sine function
        
        Default parameters use standard audio quality.
        :param numsamp: The number of samples to generate
        :param bytespersamp: The bit-depth of one sample
        :param sampfreq: The sample frequency (in Hz)
        :return: The audio samples as bytes objects
        :rtype: bytes
        """
        
        # Initialize return samples as a bytes object
        samples = b''
        
        for i in range(numsamp):
            # Get x-value
            x = i / sampfreq
            
            # Value of sine function [0, 1]
            sinevalue = sin(2 * pi * self.freq * (x - self.offset)) / 2 + 0.5
            
            # Map to sample volume and push to samples
            sampvolume = int(self.minvolume + (self.amplitude * sinevalue))
            samples += sampvolume.to_bytes(bytespersamp, 'little')
        
        return samples
    
    def squaresamples(self, numsamp, bytespersamp=2, sampfreq=44100) -> bytes:
        """Get audio samples from the wave's attributes using a sine function
        
        Default parameters use standard audio quality.
        :param numsamp: The number of samples to generate
        :param bytespersamp: The bit-depth of one sample
        :param sampfreq: The sample frequency (in Hz)
        :return: The audio samples as bytes objects
        :rtype: bytes
        """
        
        # Wave period
        period = 1 / self.freq
        
        # Initialize return samples as a bytes object
        samples = b''
        
        for i in range(numsamp):
            # Get x-value
            x = i / sampfreq
            
            # Value of square wave function [0, 1]
            pos_in_period = (x + self.offset) / period
            if pos_in_period % 1 < 0.5:
                squarevalue = self.minvolume
            else:
                squarevalue = self.maxvolume
            
            # Push to samples
            samples += squarevalue.to_bytes(bytespersamp, 'little')
        
        return samples
