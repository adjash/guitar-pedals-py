import numpy as np
from .base import Effect

class PitchBend(Effect):
    @property
    def name(self):
        return "PitchBend"
    
    def __init__(self, sample_rate):
      self.pitch_ratio = 1.5  # 1.5 = up 7 semitones, 0.5 = down 12 semitones
      super().__init__(sample_rate)
    
    def reset(self):
        self.buffer = np.zeros(1000, dtype='float32')
        self.read_pos = 0.0

    def process(self, audio, frames):
        # print()
        out = np.zeros_like(audio)
        
        for i in range(frames):
            # Store input
            self.buffer[i % len(self.buffer)] = audio[i]
            
            # Read at different speed
            read_idx = int(self.read_pos) % len(self.buffer)
            out[i] = self.buffer[read_idx]
            
            # Advance read position at different rate
            self.read_pos += self.pitch_ratio
            if self.read_pos >= len(self.buffer):
                self.read_pos -= len(self.buffer)
        
        return out