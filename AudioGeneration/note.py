# Author
# William Lucca

import re


class Note:
    """A musical note
    """
    
    def __init__(self, name):
        """Creates a Note object
        
        :param name: The name of the note (e.g. 'A4', 'C#6', 'Bb2')
        """
        
        self.pianonum = getpianonum(name)
        self.freq = getfreq(self.pianonum)


def getpianonum(name):
    """Get the numerical position of this note on a piano (1 is A0)
    
    :param name: The name of the note as a string (e.g. 'A4', 'C#6', 'Bb2')
    :return: The number of the note on a piano
    :rtype: int
    """
    
    # Different offsets depending on the chars in the name string
    letter = 0
    semitone = 0
    
    # Parse letter
    if 'A' in name:
        letter = 1
    elif 'B' in name:
        letter = 3
    elif 'C' in name:
        letter = 4
    elif 'D' in name:
        letter = 6
    elif 'E' in name:
        letter = 8
    elif 'F' in name:
        letter = 9
    elif 'G' in name:
        letter = 11
    
    # Parse semitone
    if '#' in name:
        semitone = 1
    elif 'b' in name:
        semitone = -1
    
    # Parse octave
    octavenum = re.search('\\d+', name)
    octave = 12 * int(octavenum.group(0))
    
    return letter + semitone + octave


def getfreq(pianonum):
    """Calculates the frequency of a given note on a standard piano
    
    :param pianonum: The number of the note's position on a piano
    :return: The frequency of the note
    :rtype: float
    """
    
    return