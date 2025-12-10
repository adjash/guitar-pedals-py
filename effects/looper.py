import numpy as np
from .base import Effect

class Looper(Effect):
    def __init__(self, sample_rate):
        self.max_loop_seconds = 30.0  # Maximum loop length
        self.max_loop_samples = int(self.max_loop_seconds * sample_rate)
        
        super().__init__(sample_rate)
        
    def reset(self):
        # Loop buffer
        self.loop_buffer = np.zeros(self.max_loop_samples, dtype='float32')
        self.loop_length = 0
        self.loop_position = 0
        
        # States
        self.is_recording = False
        self.is_playing = False
        self.record_position = 0
        
    @property
    def name(self):
        return "Looper"
    
    def start_recording(self):
        """Start recording a new loop"""
        self.reset()  # Clear previous loop
        self.is_recording = True
        self.is_playing = False
        self.record_position = 0
        return "Recording..."
    
    def stop_recording(self):
        """Stop recording and start playback"""
        if self.is_recording and self.record_position > 0:
            self.loop_length = self.record_position
            self.is_recording = False
            self.is_playing = True
            self.loop_position = 0
            duration = self.loop_length / self.sample_rate
            return f"Loop saved ({duration:.1f}s) - Playing back"
        return "No loop recorded"
    
    def stop_playback(self):
        """Stop loop playback"""
        self.is_playing = False
        return "Loop stopped"
    
    def toggle_playback(self):
        """Toggle playback on/off (keep loop in memory)"""
        if self.loop_length > 0:
            self.is_playing = not self.is_playing
            return "Playing" if self.is_playing else "Paused"
        return "No loop to play"
    
    def clear_loop(self):
        """Clear the current loop"""
        self.reset()
        return "Loop cleared"
    
    def get_status(self):
        """Get current looper status"""
        if self.is_recording:
            duration = self.record_position / self.sample_rate
            return f"REC [{duration:.1f}s]"
        elif self.is_playing and self.loop_length > 0:
            duration = self.loop_length / self.sample_rate
            position = self.loop_position / self.sample_rate
            return f"PLAY [{position:.1f}/{duration:.1f}s]"
        elif self.loop_length > 0:
            duration = self.loop_length / self.sample_rate
            return f"PAUSED [{duration:.1f}s]"
        else:
            return "EMPTY"
    
    def process(self, audio, frames):
        out = np.zeros_like(audio)
        
        for i in range(frames):
            input_sample = audio[i]
            output_sample = input_sample
            
            if self.is_recording:
                # Record input into buffer
                if self.record_position < self.max_loop_samples:
                    self.loop_buffer[self.record_position] = input_sample
                    self.record_position += 1
                else:
                    # Auto-stop if max length reached
                    self.stop_recording()
                
                output_sample = input_sample  # Pass through while recording
            
            if self.is_playing and self.loop_length > 0:
                # Play back loop
                loop_sample = self.loop_buffer[self.loop_position]
                output_sample = input_sample + loop_sample  # Mix input with loop
                
                # Advance loop position
                self.loop_position = (self.loop_position + 1) % self.loop_length
            
            out[i] = output_sample
        
        return out