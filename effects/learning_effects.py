import numpy as np
from .base import Effect

class LearningEffects(Effect):
    """
    Educational effect to understand audio manipulation
    Each method demonstrates a different concept
    """
    
    def __init__(self, sample_rate):
        self.mode = 'simple_echo'  # Change this to try different effects
        super().__init__(sample_rate)
    
    @property
    def name(self):
        return f"Learning: {self.mode}"
    
    def process(self, audio, frames):
        """
        Uncomment different sections to hear what they do
        """
        
        # ===== AMPLITUDE EFFECTS =====
        # These change the LOUDNESS by multiplying values
        
        if self.mode == 'amplitude':
            # Make it louder: multiply by >1
            return audio * 2.0
            # Make it quieter: multiply by <1
            # return audio * 0.5
        
        # ===== WAVESHAPING / DISTORTION =====
        # These change the SHAPE of the waveform
        
        elif self.mode == 'hard_clip':
            # Hard clipping: cut off peaks above threshold
            # This creates harsh, digital distortion
            out = np.clip(audio, -0.3, 0.3)  # Limit to ±0.3
            return out
        
        elif self.mode == 'soft_clip':
            # Soft clipping: gradually compress peaks
            # tanh() smoothly squashes values as they get bigger
            # This is what you're doing in your PitchBend!
            return np.tanh(audio * 10)
            # Try different gains: 2, 5, 20, 50 to hear the difference
        
        elif self.mode == 'sine_fold':
            # Sine folding: creates metallic, bell-like tones
            # Wraps the waveform around using sine function
            return np.sin(audio * 10)
        
        # ===== TIME-BASED EFFECTS =====
        # These use PREVIOUS samples to affect current ones
        
        elif self.mode == 'simple_echo':
            # Echo: repeat signal from the past
            # This is simplified - see your Echo effect for full version
            out = np.zeros_like(audio)
            delay_samples = int(0.3 * self.sample_rate)  # 300ms delay
            
            for i in range(frames):
                if i >= delay_samples:
                    # Current sample + sample from 300ms ago
                    out[i] = audio[i] + audio[i - delay_samples] * 0.5
                else:
                    out[i] = audio[i]
            return out
        
        elif self.mode == 'reverse':
            # Reverse: play backwards!
            return np.flip(audio)
        
        # ===== FREQUENCY EFFECTS =====
        # These change which FREQUENCIES are present
        
        elif self.mode == 'dc_offset':
            # DC offset: shift entire signal up/down
            # This moves the "center" of the waveform
            return audio + 0.3  # Shift up by 0.3
        
        elif self.mode == 'rectify':
            # Full-wave rectification: flip negative values positive
            # Creates octave-up effect and harsh harmonics
            return np.abs(audio)
        
        elif self.mode == 'half_rectify':
            # Half-wave rectification: remove negative values
            # Creates different harmonics than full-wave
            return np.maximum(audio, 0)
        
        # ===== ANALYSIS MODE =====
        # Print out values to see what's happening
        
        elif self.mode == 'analyze':
            # Print statistics about the audio
            if frames > 0:
                print(f"Min: {np.min(audio):.3f}, Max: {np.max(audio):.3f}, "
                      f"Mean: {np.mean(audio):.3f}, RMS: {np.sqrt(np.mean(audio**2)):.3f}")
            return audio
        
        else:
            return audio