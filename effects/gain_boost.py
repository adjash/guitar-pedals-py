from .base import Effect
from config import GAIN_BOOST

class GainBoost(Effect):
    @property
    def name(self):
        return "Gain Boost"
    
    def process(self, audio, frames):
        return audio * GAIN_BOOST