import numpy as np
from .base import Effect
from config import LPF_COEFF

class LowPassFilter(Effect):
    def reset(self):
        self.prev_lpf = 0.0
    
    @property
    def name(self):
        return "Low-Pass Filter"
    
    def process(self, audio, frames):
        alpha = LPF_COEFF
        out = np.empty_like(audio)
        
        self.prev_lpf = self.prev_lpf + alpha * (audio[0] - self.prev_lpf)
        out[0] = self.prev_lpf
        
        for i in range(1, len(audio)):
            self.prev_lpf = self.prev_lpf + alpha * (audio[i] - self.prev_lpf)
            out[i] = self.prev_lpf
        
        return out