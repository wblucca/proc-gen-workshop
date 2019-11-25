# Author
# William Lucca

from math import sin, pi


class Wave:
    
    def __init__(self, freq, minvolume, maxvolume, offset=0):
        """Creates a SineWave object
        
        :param freq: The frequency of the sound wave
        :param minvolume: The maximum volume of the sound wave
        :param maxvolume: The minimum volume of the sound wave
        :param offset: The start point (x=0) for the sound wave (in seconds)
        """
        
        # Store sine wave parameters
        self.freq = freq
        self.minvolume = int(minvolume)
        self.maxvolume = int(maxvolume)
        self.amplitude = self.maxvolume - self.minvolume
        self.offset = offset
    
    def sinesamples(self, numsamp, bytespersamp=2, sampfreq=44100) -> bytes:
        """Get audio samples from the wave's attributes using a sine function
        
        Default parameters use standard audio quality. Only supports mono.
        :param numsamp: The number of samples to generate
        :param bytespersamp: The depth of one sample in bytes
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
            
            # Map to [-minvolume, maxvolume] and push to samples
            sampvolume = int(self.minvolume + (self.amplitude * sinevalue))
            samples += twoscompbytes(sampvolume, bytespersamp)
            
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
            
            # Get value of square wave function, either minvolume or maxvolume
            pos_in_period = (x + self.offset) / period
            if pos_in_period % 1 < 0.5:
                # [0, 0.5) in period length
                squarevalue = self.minvolume
            else:
                # [0.5, 1) in period length
                squarevalue = self.maxvolume
            
            # Push to samples
            samples += twoscompbytes(squarevalue, bytespersamp)
        
        return samples


def twoscompbytes(x, numbytes):
    """Gets the two's complement representation of a signed int as bytes
    
    :param x: Signed integer to convert
    :param numbytes: How many bytes to use in binary representation
    :return: Two's complement representation of the number as bytes
    :rtype: bytes
    """
    
    if x < 0:
        complementbits = 2 ** (8 * numbytes) - 1
        x = (abs(x) - 1) ^ complementbits
    
    return x.to_bytes(numbytes, 'little')
