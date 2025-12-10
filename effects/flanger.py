import numpy as np
from .base import Effect

class Flanger(Effect):
    """
    Flanger: Short delay with LFO-modulated delay time
    
    Key Concepts:
    - Circular delay buffer (ring buffer)
    - Fractional delay (interpolation)
    - Feedback for resonance
    - Comb filtering creates the "jet plane" sound
    """
    
    def __init__(self, sample_rate):
        # Set parameters BEFORE calling super().__init__()
        # Flanger parameters
        self.rate = 0.5           # LFO speed in Hz
        self.depth = 0.002        # Delay modulation depth in seconds (2ms)
        self.feedback = 0.5       # Amount of output fed back (0-0.95)
        self.mix = 0.5            # Dry/wet mix (0=dry, 1=wet)
        
        # Delay line specs
        self.min_delay = 0.001    # Minimum delay: 1ms
        self.max_delay = 0.005    # Maximum delay: 5ms
        
        super().__init__(sample_rate)
        
    def reset(self):
        # Calculate buffer size needed
        # Must be large enough to hold max_delay samples
        max_delay_samples = int(self.max_delay * self.sample_rate)
        self.buffer_size = max_delay_samples + 1
        
        # Circular delay buffer
        # This is a ring buffer - when we reach the end, we wrap to the beginning
        self.buffer = np.zeros(self.buffer_size, dtype='float32')
        
        # Write position in buffer
        self.write_pos = 0
        
        # LFO phase
        self.phase = 0.0
    
    @property
    def name(self):
        return "Flanger"
    
    def _linear_interpolate(self, buffer, position):
        """
        Linear interpolation for fractional delay
        
        WHY INTERPOLATION?
        The LFO creates delay times like 2.347ms, but we can only read
        integer sample positions. Interpolation lets us read "between samples"
        
        Example: position = 10.7
        - Read samples at index 10 and 11
        - Return 30% of sample[10] + 70% of sample[11]
        """
        # Split position into integer and fractional parts
        index = int(position) % self.buffer_size
        next_index = (index + 1) % self.buffer_size
        frac = position - int(position)
        
        # Linear interpolation between two samples
        # This is the simplest form - more advanced: cubic, Hermite
        return buffer[index] * (1 - frac) + buffer[next_index] * frac
    
    def process(self, audio, frames):
        """
        Process with modulated delay line
        
        Signal flow:
        Input → [+] → Delay → [+] → Output
                ↑             ↓
                └── Feedback ─┘
        """
        out = np.empty_like(audio)
        
        # LFO phase increment
        phase_increment = 2 * np.pi * self.rate / self.sample_rate
        
        for i in range(frames):
            # Generate LFO (-1 to +1)
            lfo = np.sin(self.phase)
            
            # Convert LFO to delay time in samples
            # LFO modulates between min_delay and max_delay
            min_delay_samples = self.min_delay * self.sample_rate
            max_delay_samples = self.max_delay * self.sample_rate
            delay_range = max_delay_samples - min_delay_samples
            
            # Map LFO to delay time
            # lfo=-1 → min_delay, lfo=+1 → max_delay
            current_delay = min_delay_samples + (lfo + 1) * 0.5 * delay_range
            
            # Calculate read position (fractional!)
            # Read from "delay samples ago"
            read_pos = self.write_pos - current_delay
            if read_pos < 0:
                read_pos += self.buffer_size
            
            # Read delayed sample with interpolation
            # This is the KEY technique for smooth modulation
            delayed_sample = self._linear_interpolate(self.buffer, read_pos)
            
            # Input signal
            input_sample = audio[i]
            
            # Write to buffer: input + feedback
            # The feedback creates resonance peaks (the "swoosh")
            self.buffer[self.write_pos] = input_sample + delayed_sample * self.feedback
            
            # Mix dry and wet signals
            # Mixing delayed with undelayed creates COMB FILTERING
            # This is what makes the flanger sound!
            output_sample = input_sample * (1 - self.mix) + delayed_sample * self.mix
            
            out[i] = output_sample
            
            # Advance pointers
            self.write_pos = (self.write_pos + 1) % self.buffer_size
            self.phase += phase_increment
            if self.phase >= 2 * np.pi:
                self.phase -= 2 * np.pi
        
        return out