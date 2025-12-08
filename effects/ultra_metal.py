import numpy as np
from .base import Effect

class UltraMetal(Effect):
    def __init__(self, sample_rate):
        super().__init__(sample_rate)
        
        # --- GAIN STAGE PARAMETERS ---
        self.pre_gain = 80.0      # Increased input boost for max saturation
        self.drive = 0.6          # Increased clipping intensity
        self.post_level = 0.6     
        
        # --- NEW PRE-CLIPPING EQ (Pinch Harmonic Focus) ---
        self.pre_mid_freq = 2500  # Critical frequency where harmonic energy sits
        self.pre_mid_boost = 3.5  # Focused boost
        self.pre_mid_q = 8.0      # Very high Q for a narrow, piercing emphasis
        
        # --- POST-CLIPPING EQ (Metal V-Scoop) ---
        
        # Low-End (Bass)
        self.bass_freq = 100
        self.bass_gain = 0.5      
        
        # Mid-Scoop (The Metal V)
        self.mid_freq = 750       
        self.mid_gain = 0.25      
        self.mid_q = 1.0          
        
        # High-End (Presence/Treble)
        self.high_freq = 4000     # Pushed higher for more sizzle
        self.high_gain = 5.0      # Even more aggressive boost
        self.high_q = 2.0         # Sharper Q
        
    def reset(self):
        # Filter states for Pre-Mid
        self.pre_mid_x1, self.pre_mid_x2, self.pre_mid_y1, self.pre_mid_y2 = 0.0, 0.0, 0.0, 0.0
        # Filter states for Post-EQ (Bass, Mid, High)
        self.bass_x1, self.bass_x2, self.bass_y1, self.bass_y2 = 0.0, 0.0, 0.0, 0.0
        self.mid_x1, self.mid_x2, self.mid_y1, self.mid_y2 = 0.0, 0.0, 0.0, 0.0
        self.high_x1, self.high_x2, self.high_y1, self.high_y2 = 0.0, 0.0, 0.0, 0.0
    
    @property
    def name(self):
        return "Ultra Metal V3"
    
    def _peaking_eq(self, x, x1, x2, y1, y2, freq, gain, q):
        """Biquad Peaking EQ filter (Formula Unchanged)"""
        w0 = 2 * np.pi * freq / self.sample_rate
        A = np.sqrt(gain)
        alpha = np.sin(w0) / (2 * q)
        
        b0 = 1 + alpha * A
        b1 = -2 * np.cos(w0)
        b2 = 1 - alpha * A
        a0 = 1 + alpha / A
        a1 = -2 * np.cos(w0)
        a2 = 1 - alpha / A
        
        # Normalize by a0
        b0_norm, b1_norm, b2_norm = b0 / a0, b1 / a0, b2 / a0
        a1_norm, a2_norm = a1 / a0, a2 / a0
        
        y = b0_norm * x + b1_norm * x1 + b2_norm * x2 - a1_norm * y1 - a2_norm * y2
        
        return y, x, x1, y, y1
        
    def _harsh_sigmoid_clip(self, x, drive):
        """NEW: Increased harshness for high-order harmonics."""
        
        # Increase the exponent of the drive to force harder clipping at the edges
        z = np.tanh(x * (1.0 + 2 * drive))
        
        # INCREASED power term: This term significantly boosts high-order harmonics,
        # which are the "scream" of the pinch harmonic.
        return z + 0.5 * np.power(z, 5) 

    def process(self, audio, frames):
        out = np.empty_like(audio)
        
        for i in range(frames):
            sample = audio[i]
            
            # 1. Pre-Gain Stage
            sample *= self.pre_gain
            
            # 2. NEW PRE-CLIPPING EQ: Focus the pinch harmonic frequencies
            # This aggressive, narrow boost ensures the harmonic partials saturate first.
            sample, self.pre_mid_x2, self.pre_mid_x1, self.pre_mid_y2, self.pre_mid_y1 = self._peaking_eq(
                sample, self.pre_mid_x1, self.pre_mid_x2, self.pre_mid_y1, self.pre_mid_y2,
                self.pre_mid_freq, self.pre_mid_boost, self.pre_mid_q
            )
            
            # 3. Clipping/Saturation: Use the harsher clipper
            sample = self._harsh_sigmoid_clip(sample, self.drive)
            
            # --- POST-CLIPPING EQ ---
            
            # 4. Bass EQ: Tighten the low end
            sample, self.bass_x2, self.bass_x1, self.bass_y2, self.bass_y1 = self._peaking_eq(
                sample, self.bass_x1, self.bass_x2, self.bass_y1, self.bass_y2,
                self.bass_freq, self.bass_gain, 1.0
            )

            # 5. Mid EQ: The classic mid-scoop
            sample, self.mid_x2, self.mid_x1, self.mid_y2, self.mid_y1 = self._peaking_eq(
                sample, self.mid_x1, self.mid_x2, self.mid_y1, self.mid_y2,
                self.mid_freq, self.mid_gain, self.mid_q
            )
            
            # 6. High EQ: Final aggressive high-end boost
            sample, self.high_x2, self.high_x1, self.high_y2, self.high_y1 = self._peaking_eq(
                sample, self.high_x1, self.high_x2, self.high_y1, self.high_y2,
                self.high_freq, self.high_gain, self.high_q
            )
            
            # 7. Output Level control
            out[i] = sample * self.post_level
        
        return out