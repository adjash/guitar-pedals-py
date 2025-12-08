import numpy as np

class Effect:
    """Base class for all effects"""
    
    def __init__(self, sample_rate):
        self.sample_rate = sample_rate
        self.reset()
    
    def reset(self):
        """Reset effect state"""
        pass
    
    def process(self, audio, frames):
        """Process audio buffer and return output"""
        raise NotImplementedError
    
    @property
    def name(self):
        """Effect name for display"""
        return self.__class__.__name__