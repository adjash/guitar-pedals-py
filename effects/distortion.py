import numpy as np
from .base import Effect
from config import DIST_GAIN

class Distortion(Effect):
    @property
    def name(self):
        return "Distortion"
    
    def process(self, audio, frames):
        boosted = audio * DIST_GAIN
        return np.tanh(boosted)