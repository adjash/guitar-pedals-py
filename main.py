import sounddevice as sd
import time
from config import SAMPLE_RATE, BUFFER_SIZE, INPUT_DEVICE, OUTPUT_DEVICE
from effects import Clean, GainBoost, LowPassFilter, Distortion, Echo, WahWah, UltraMetal, EffectChain, Looper, Tremolo, Flanger, Reverb, PitchBend, LearningEffects
from cli import Menu

class GuitarFX:
    def __init__(self):
        self.running = True
        print(sd.query_devices())
        # Initialize individual effects
        self.effects = [
            Clean(SAMPLE_RATE),
            GainBoost(SAMPLE_RATE),
            LowPassFilter(SAMPLE_RATE),
            Distortion(SAMPLE_RATE),
            Echo(SAMPLE_RATE),
            WahWah(SAMPLE_RATE),
            UltraMetal(SAMPLE_RATE),
            Tremolo(SAMPLE_RATE),
            Flanger(SAMPLE_RATE),
            Reverb(SAMPLE_RATE),
            PitchBend(SAMPLE_RATE),
            LearningEffects(SAMPLE_RATE)
        ]
        
        # Initialize effect chain with all effects
        self.effect_chain = EffectChain(SAMPLE_RATE)
        for effect in self.effects:
            self.effect_chain.add_effect(effect, active=False)
        
        # Initialize looper (always active, runs after effects)
        self.looper = Looper(SAMPLE_RATE)
        
        # Initialize menu
        self.menu = Menu(self.effects, self.effect_chain, self.looper, self.stop)
    
    def audio_callback(self, indata, outdata, frames, time_data, status):
        audio = indata[:, 0]
        
        # Process through selected effect(s)
        current_effect = self.menu.get_current_effect()
        out = current_effect.process(audio, frames)
        
        # Always process through looper last
        out = self.looper.process(out, frames)
        
        outdata[:] = out.reshape(-1, 1)
    
    def stop(self):
        self.running = False
    
    def run(self):
        print("Starting real-time guitar FX…")
        
        # Start menu in separate thread
        self.menu.start_thread()
        
        try:
            with sd.Stream(
                samplerate=SAMPLE_RATE,
                blocksize=BUFFER_SIZE,
                dtype="float32",
                channels=1,
                callback=self.audio_callback,
                device=(INPUT_DEVICE, OUTPUT_DEVICE),
                latency="low",
            ):
                while self.running:
                    time.sleep(0.1)
        except KeyboardInterrupt:
            self.running = False
        
        print("\nStopped.")

if __name__ == "__main__":
    app = GuitarFX()
    app.run()