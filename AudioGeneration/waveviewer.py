# Author
# William Lucca

import wave


def plotwav(*files):
    for file in files:
        with wave.open(file, 'rb') as wavfile:
            pass
