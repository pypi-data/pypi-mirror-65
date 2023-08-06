""" datatypes.py: data wrappers and loaders
"""

__version__ = "0.2"
__status__ = "beta"

import librosa
import os
from typing import List
import numpy
from itertools import cycle

class Waveform(object):
    """Class holding a Waveform object.
    
    Constructors:
        Waveform(x:array, fs:int)
        Waveform.load(path:str)                # load recording from 'path.wav'
        
    Data Model Operators:
        wave = Wave(...)
        len(wave)             # returns length of the Waveform.x attribute
        wave[:10000]          # returns sliced Waveform
    
    Data Augmentation Functions:
        wave = Wave(...)
        other = Wave(...)
        wave.append(other)    # appending another wave to self
        .
        """
    
    def __init__(self, x, fs):
        self.x = x
        self.fs = fs
    
    # factory methods
    @classmethod
    def load(cls, path:str):
        x, fs = librosa.load(path)
        return cls(x, fs)    # basic data model attributes 
    
    # basic datamodel attributes
    def __len__(self):
        return len(self.x)
    
    def __repr__(self):
        return f"{type(self).__name__}({abbreviate(self.x)}, {self.fs})"
    
    def __getitem__(self, key):
        """"""
        assert(isinstance(key, slice) and key.step is None), "please only slice Waveform, integer indexing and stepwise slicing are not supported"
        return Waveform(x=self.x.__getitem__(key), fs=self.fs)
    
    # read-only properties
    @property
    def duration(self):
        """Duration of Waveform in seconds, read only."""
        return self.__len__()/self.fs
    
    # data augmentation functionality
    def append(self, other):
        """Appends other Waveform to self if sample rates match."""
        assert(isinstance(other, Waveform))
        assert(self.fs == other.fs), "can only append if sample rates match"
        self.x = numpy.hstack([self.x, other.x])
        
    def mix_with(self, other, factor:float=0.5):
        """Mixes other Waveform into self, with the other making up factor*100 % of the resulting signal. Will repeat other Waveform to match length of existing.
        """
        assert(0 <= factor <= 1), "please mix with factors in [0, 1]"
        assert(self.fs == other.fs), "need equal samplerates for mixing"
        for i, (x1, x2) in enumerate(zip(self.x, cycle(other.x))):
            self.x[i] = (1 - factor)*x1 + factor*x2

        
def load(path):
    x, fs = librosa.load(path)
    return Waveform(x, fs)

class Take:
    """Class representing a part of an Recording that can be asigned attributes of interest (is this part of a Recording active, valid, etc.)
    
    Constructor:
        Take(name:str, waveform:Waveform, **kwargs)  
        Take(..., active=True, valid=False, color='green') # can take any attributes via **kwargs 
    
    Is used to asign attributes (such as active or valid)on the run:
        take = Take(...)
        take.active = True
        take.valid = True
        take.color = 'green'
    .
    """
    def __init__(self, name:str, waveform:Waveform, **kwargs):
        self.name = name
        self.waveform = waveform
        for key, value in kwargs.items():
            self.__dict__[key] = value
        
        
    # basic data model attributes 
    def __repr__(self):
        attributes = ', '.join(f'{key}={value!r}' for key, value in self.__dict__.items())
        return f'{type(self).__name__}({attributes})'
    
class Recording:
    """Class to hold all the takes from a single subject.
    
    Constructors:
        Recording(file_name:str, waveform:Waveform)
        Recording.from_file(file_name:str)
    
    Data Model Operators:
        recording = Recording(...)
        
        for take in recording:      # Iteration over Recording.takes 
            isinstance(take, Take)  # True
            take.processed = True   # Adding features to Takes 
            
        recording[10]               # Indexing into Recording.takes
        recording[1:5]
        
        
    Properties (read-only):
        .active_takes      # -> List[Takes]
        .silent_takes      # -> List[Takes]
        .valid_takes       # -> List[Takes]
        .invalid_takes     # -> List[Takes]
        .proportion_active # -> float
        .proportion_valid  # -> float
        
    Workflows:
    1. Working on the whole recording and CHANGING the number of Takes, e.g. cutting Recording into Takes at the begginning or end
        recording = Recording(...)            # instanciate Recording
        wave = recording.waveform
        take_1 = Take(..., wave[:10000])      # generate Takes that fullfill condition
        take_1.at_beginning = True            # set condition as Take.attribute
        take_2 = Take(..., wave[10000:])
        take_2.at_beginning = False
        recording.takes = [take_1, take_2]    # reset Recording.takes attribute (in order to change the number of takes)
    
    2. Working on the Takes of a recording and NOT CHANGING the number of Takes, e.g. classifying Takes into valid and invalid
        recording = Recording(...)            # instanciate Recording
        for take in recording:                # iterate over takes
            if take.attribute == value:       # decide whether take fulfills condition
                take.valid == True            # add an attribute inplace
            else:
                take.valid == False
                                             # no resetting of Recording.takes attribute (in order to keep the number of takes)
    .
    """
    
    def __init__(self, file_name:str, waveform:Waveform):
        self.file_name = add_wav(file_name)
        self.id = os.path.splitext(file_name)[0]
        self.id = os.path.split(self.id)[1]
        self.waveform = waveform
        self.takes:List[Take] = [Take(name=self.id, waveform=self.waveform)]

    # factory methods
    @classmethod
    def from_file(cls, file_name:str):
        file_name = add_wav(file_name)
        wave = Waveform.load(file_name)
        return cls(file_name=file_name, waveform=wave)
    
    # basic data model attributes 
    def __repr__(self):
        return f"{type(self).__name__}(file_name={self.file_name!r}, waveform={self.waveform!r})"
        
    def __iter__(self):
        """Allows iteration over all self.takes."""
        assert(len(set(id(take) for take in self.takes)) == len(self.takes)), "please use different object's for each take"
        return iter(self.takes)

    def __getitem__(self, key):
        """returns Take(s) at self.takes[key]"""
        return self.takes.__getitem__(key)
    
    # read-only properties
    @property
    def active_takes(self) -> List[Take]:
        """returns all Takes that have take.active = True"""
        return [take for take in self.__iter__() if hasattr(take, 'active') and take.active]
    
    @property
    def silent_takes(self) -> List[Take]:
        """returns all Takes that have take.active = False"""
        return [take for take in self.__iter__() if hasattr(take, 'active') and not take.active]
    
    @property
    def valid_takes(self) -> List[Take]:
        """returns all Takes that have take.valid = True"""
        return [take for take in self.__iter__() if hasattr(take, 'valid') and take.valid]
    
    @property
    def invalid_takes(self) -> List[Take]:
        """returns all Takes that have take.valid = False"""
        return [take for take in self.__iter__() if hasattr(take, 'valid') and not take.valid]
    
    @property
    def proportion_active(self) -> float:
        """returns the proportion of silent takes to active takes"""
        return len(self.active_takes)/len(self.takes) if len(self.takes) > 0 else 0

    @property
    def proportion_valid(self) -> float:
        """returns the proportion of valid takes to invalid takes, excluding silent takes"""
        return len(self.valid_takes)/len(self.active_takes) if len(self.active_takes) > 0 else 0
    


    

# helper functions, mainly for handling strings in __repr__ and file_name
def add_wav(name:str) -> str:
    """adds '.wav' to filename if not already present. Raises Error if other extension would be overridden"""
    
    assert(os.path.splitext(name)[1] in ['', '.wav']), f"was expecting '.wav' or no extension, got {os.path.splitext(name)[1]}"
    if os.path.splitext(name)[1] == '':
        name += '.wav'
    return name

def abbreviate(listy_obj) -> str:
    """returns amn abbreviated version of repr(listy_obj)"""
    if len(listy_obj) <= 3:
        return repr(listy_obj)
    return f'{type(listy_obj).__name__}([{listy_obj[0]}, ..., {listy_obj[-1]}])'
