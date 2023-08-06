"""test datatypes.py: tests for datatypes.py
"""


import unittest
import datatypes
import numpy

class WaveformTestCase(unittest.TestCase):
    def setUp(self):
        self.wave = datatypes.Waveform(x=numpy.random.uniform(-1, 1, 80000), fs=22000)
        self.other = datatypes.Waveform(x=numpy.random.uniform(-1, 1, 80000), fs=22000)
    
    def test_append(self):
        duration_self = self.wave.duration
        duration_other = self.other.duration
        self.wave.append(self.other)
        self.assertEqual(self.wave.duration, duration_self + duration_other)
        self.assertEqual(self.other.duration, duration_other)
        
        with self.assertRaises(AssertionError):
            self.wave.append([1,2,3])    # need other Waveform
            self.other.fs += 1000
            self.wave.append(self.other) # need equal sample-rates
            
    def test_mix_with(self):
        factor = 0.2
        theoretical = (1-factor) * self.wave.x + factor * self.other.x 
        self.wave.mix_with(self.other, factor=factor)
        new = self.wave.x
        self.assertTrue(all(new == theoretical))
        
        
    
class TakeTestCase(unittest.TestCase):
    def setUp(self):
        wave = datatypes.Waveform(x=numpy.random.uniform(-1, 1, 80000), fs=22000)
        self.take = datatypes.Take(name="name", waveform=wave)
        
    def test_runs(self):
        pass
    
class RecordingTestCase(unittest.TestCase):
    def setUp(self):
        wave = datatypes.Waveform(x=numpy.random.uniform(-1, 1, 80000), fs=22000)
        self.recording = datatypes.Recording(file_name="test.wav", waveform=wave)
        
    def test_runs(self):
        pass
    
        
if __name__ == "__main__":
    unittest.main()
    