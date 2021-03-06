# Author
# William Lucca

from math import sin, pi


class Wave:
    """A wave form that can be made into digital audio samples
    """
    
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
        self.axis = (self.minvolume + self.maxvolume) / 2
        self.offset = offset
    
    def sinesamples(self, numsecs, bytespersamp=2, sampfreq=44100,
                    fadein=0, fadeout=0) -> bytes:
        """Get audio samples from the wave's attributes using a sine function
        
        Default parameters use standard audio quality. Only supports mono.
        :param numsecs: The number of seconds to generate
        :param bytespersamp: The depth of one sample in bytes
        :param sampfreq: The sample frequency (in Hz)
        :param fadein: How many seconds to fade in for
        :param fadeout: How many seconds to fade out for
        :return: The audio samples as a bytes object
        :rtype: bytes
        """
        
        # Initialize return samples as a bytes object
        numsamps = int(numsecs * sampfreq)
        samples = bytearray(numsamps * bytespersamp)
        
        # Index in samples bytearray
        s = 0
        
        for i in range(numsamps):
            # Get x-value (seconds)
            x = i / sampfreq
            
            fademult = 1.0
            # Fade in
            if x < fadein:
                # [0.0, 1.0] over the course of fade in time
                fademult = x / fadein
            
            # Fade out
            if (numsecs - x) < fadeout:
                # [1.0, 0.0] over the course of fade out time
                fademult = (numsecs - x) / fadeout
            
            # Value of sine function [0, 1]
            b = 2 * pi * self.freq
            sinevalue = fademult * sin(b * (x - self.offset)) / 2 + 0.5
            
            # Map to [-minvolume, maxvolume] and push to samples
            sampvolume = int(self.minvolume + self.amplitude * sinevalue)
            samplebytes = twoscompbytes(sampvolume, bytespersamp)
            for byte in samplebytes:
                samples[s] = byte
                s += 1
        
        return bytes(samples)
    
    def squaresamples(self, numsecs, bytespersamp=2, sampfreq=44100,
                      fadein=0, fadeout=0) -> bytes:
        """Get audio samples from the wave's attributes using a sine function
        
        Default parameters use standard audio quality.
        :param numsecs: The number of seconds to generate
        :param bytespersamp: The bit-depth of one sample
        :param sampfreq: The sample frequency (in Hz)
        :param fadein: How many seconds to fade in for
        :param fadeout: How many seconds to fade out for
        :return: The audio samples as a bytes object
        :rtype: bytes
        """
        
        # Wave period
        period = 1 / self.freq
        
        # Initialize return samples as a bytes object
        numsamps = int(numsecs * sampfreq)
        samples = bytearray(numsamps * bytespersamp)
        
        # Index in samples bytearray
        s = 0
        
        for i in range(numsamps):
            # Get x-value
            x = i / sampfreq
            
            fademult = 1.0
            # Fade in
            if x < fadein:
                # [0.0, 1.0] over the course of fade in time
                fademult = x / fadein
            
            # Fade out
            if (numsecs - x) < fadeout:
                # [1.0, 0.0] over the course of fade out time
                fademult = (numsecs - x) / fadeout
            
            # Value of square wave function [minvolume, maxvolume]
            pos_in_period = (x + self.offset) / period
            if pos_in_period % 1 < 0.5:
                # [0, 0.5) in period length
                squarevalue = int(self.axis - 0.5 * self.amplitude * fademult)
            else:
                # [0.5, 1) in period length
                squarevalue = int(self.axis + 0.5 * self.amplitude * fademult)
            
            # Push to samples
            samplebytes = twoscompbytes(squarevalue, bytespersamp)
            for byte in samplebytes:
                samples[s] = byte
                s += 1
        
        return bytes(samples)


def twoscompbytes(x, numbytes):
    """Gets the two's complement representation of a signed int as bytes
    
    :param x: Signed integer to convert
    :param numbytes: How many bytes to use in binary representation
    :return: Two's complement representation of the number as bytes
    :rtype: bytes
    """
    
    # Check if negative
    if x < 0:
        # Set positive, subtract 1, and flip the bits
        complementbits = 2 ** (8 * numbytes) - 1
        x = (abs(x) - 1) ^ complementbits
    
    # Convert to bytes
    return x.to_bytes(numbytes, 'little')


def twoscompint(bytevalue, numbytes):
    """Gets the signed int shown by the given two's complement byte(s)

    :param bytevalue: Bytes object integer to convert to integer
    :param numbytes: Number of bytes used in the two's complement number
    :return: Integer represented by the two's complement format bytes
    :rtype: int
    """
    
    # Convert from bytes
    x = int.from_bytes(bytevalue, 'little')
    
    # Check if negative
    if x >> (8 * numbytes - 1) == 0b1:
        # Flip bits, add one, and set negative
        complementbits = 2 ** (8 * numbytes) - 1
        x = (x ^ complementbits) + 1
        x *= -1
    
    return x
