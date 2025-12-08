import numpy as np
from .base import Effect

class UltraMetal(Effect):
    def __init__(self, sample_rate):
        super().__init__(sample_rate)
        # Pre-gain stage
        self.pre_gain = 40.0  # Heavy pre-distortion boost
        
        # Multi-stage clipping
        self.clip_stages = 3
        
        # Mid-range boost (helps pinch harmonics cut through)
        self.mid_freq = 2000  # Hz - where pinch harmonics live
        self.mid_boost = 4.0
        self.mid_q = 3.0
        
        # High-pass to tighten low end
        self.hp_freq = 100
        
        # Presence boost (high-mid emphasis)
        self.presence_freq = 4000
        self.presence_boost = 2.5
        self.presence_q = 2.0
        
    def reset(self):
        # Biquad filter states for mid boost
        self.mid_x1 = 0.0
        self.mid_x2 = 0.0
        self.mid_y1 = 0.0
        self.mid_y2 = 0.0
        
        # High-pass filter state
        self.hp_x1 = 0.0
        self.hp_y1 = 0.0
        
        # Presence boost filter states
        self.pres_x1 = 0.0
        self.pres_x2 = 0.0
        self.pres_y1 = 0.0
        self.pres_y2 = 0.0
    
    @property
    def name(self):
        return "Ultra Metal"
    
    def _peaking_eq(self, x, x1, x2, y1, y2, freq, gain, q):
        """Peaking EQ biquad filter"""
        w0 = 2 * np.pi * freq / self.sample_rate
        A = np.sqrt(gain)
        alpha = np.sin(w0) / (2 * q)
        
        b0 = 1 + alpha * A
        b1 = -2 * np.cos(w0)
        b2 = 1 - alpha * A
        a0 = 1 + alpha / A
        a1 = -2 * np.cos(w0)
        a2 = 1 - alpha / A
        
        # Normalize
        b0 /= a0
        b1 /= a0
        b2 /= a0
        a1 /= a0
        a2 /= a0
        
        # Apply filter
        y = b0 * x + b1 * x1 + b2 * x2 - a1 * y1 - a2 * y2
        
        return y, x, x1, y, y1
    
    def _highpass(self, x, x1, y1):
        """Simple one-pole high-pass filter"""
        alpha = 1.0 / (1.0 + self.sample_rate / (2 * np.pi * self.hp_freq))
        y = alpha * (y1 + x - x1)
        return y, x, y
    
    def _asymmetric_clip(self, x):
        """Asymmetric clipping for more harmonics"""
        if x > 0:
            return np.tanh(x * 1.2)
        else:
            return np.tanh(x * 0.8)
    
    def process(self, audio, frames):
        out = np.empty_like(audio)
        
        for i in range(frames):
            sample = audio[i]
            
            # Stage 1: High-pass filter (tighten bass)
            sample, self.hp_x1, self.hp_y1 = self._highpass(
                sample, self.hp_x1, self.hp_y1
            )
            
            # Stage 2: Mid-range boost (pinch harmonic emphasis)
            sample, self.mid_x2, self.mid_x1, self.mid_y2, self.mid_y1 = self._peaking_eq(
                sample, self.mid_x1, self.mid_x2, self.mid_y1, self.mid_y2,
                self.mid_freq, self.mid_boost, self.mid_q
            )
            
            # Stage 3: Heavy pre-gain
            sample *= self.pre_gain
            
            # Stage 4: Multi-stage asymmetric clipping
            for _ in range(self.clip_stages):
                sample = self._asymmetric_clip(sample)
            
            # Stage 5: Presence boost (sparkle and cut)
            sample, self.pres_x2, self.pres_x1, self.pres_y2, self.pres_y1 = self._peaking_eq(
                sample, self.pres_x1, self.pres_x2, self.pres_y1, self.pres_y2,
                self.presence_freq, self.presence_boost, self.presence_q
            )
            
            # Stage 6: Final soft clipping to control peaks
            sample = np.tanh(sample * 0.7)
            
            out[i] = sample
        
        return out  # Output scaling