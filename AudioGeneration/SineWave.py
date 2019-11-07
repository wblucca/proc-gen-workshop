# Author
# William Lucca


class SineWave:
    
    def __init__(self, amplitude, freq, offset=0):
        self.amplitude = amplitude
        self.freq = freq
        self.offset = offset
    
    def getsamples(self, numsamples, bitdepth=16, sampfreq=44100, numchannels=1) -> bytes:
        """Get audio samples from this mathematically defined sine wave
        
        :param numsamples: The number of samples to generate
        :param bitdepth: The bit-depth of one sample
        :param sampfreq: The sample frequency (in Hz)
        :param numchannels: The number of channels to generate audio for
        :return: The audio samples as bytes objects
        :rtype: bytes
        """
        
        return b''
