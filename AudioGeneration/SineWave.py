# Author
# William Lucca


class SineWave:
    
    def __init__(self, amplitude, freq, offset=0):
        self.amplitude = amplitude
        self.freq = freq
        self.offset = offset
    
    def getsamples(self, numsamples, bytespersamp=2, sampfreq=44100) -> bytes:
        """Get audio samples from this mathematically defined sine wave
        
        Default parameters use standard audio quality.
        :param numsamples: The number of samples to generate
        :param bytespersamp: The bit-depth of one sample
        :param sampfreq: The sample frequency (in Hz)
        :return: The audio samples as bytes objects
        :rtype: bytes
        """
        
        # Get max audio volume for this bit-depth
        maxvol = 256 ** bytespersamp - 1
        
        return b''
