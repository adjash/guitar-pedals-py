from .base import Effect

class EffectChain(Effect):
    """Manages multiple effects in series"""
    
    def __init__(self, sample_rate):
        self.effects = []
        self.active_states = []
        super().__init__(sample_rate)
    
    @property
    def name(self):
        return "Effect Chain"
    
    def add_effect(self, effect, active=True):
        """Add an effect to the chain"""
        self.effects.append(effect)
        self.active_states.append(active)
    
    def toggle_effect(self, index):
        """Toggle an effect on/off"""
        if 0 <= index < len(self.effects):
            self.active_states[index] = not self.active_states[index]
            return True
        return False
    
    def is_active(self, index):
        """Check if an effect is active"""
        if 0 <= index < len(self.effects):
            return self.active_states[index]
        return False
    
    def get_status_display(self):
        """Get visual status of all effects"""
        lines = []
        for i, (effect, active) in enumerate(zip(self.effects, self.active_states)):
            status = "●" if active else "○"
            lines.append(f"  {i+1}. [{status}] {effect.name}")
        return "\n".join(lines)
    
    def reset(self):
        """Reset all effects in the chain"""
        for effect in self.effects:
            effect.reset()
    
    def process(self, audio, frames):
        """Process audio through active effects in series"""
        out = audio.copy()
        
        for effect, active in zip(self.effects, self.active_states):
            if active:
                out = effect.process(out, frames)
        
        return out