# AMPLITUDE - How loud

audio = [0.1, 0.2, 0.3] # Quiet sound
audio = [0.5, 0.7, 0.9] # Loud sound
audio = [1.0, 1.0, 1.0] # Maximum loudness (clipping!)

# FREQUENCY - How fast values change

audio = [0.1, 0.2, 0.3, 0.2, 0.1, 0.0, -0.1, -0.2] # Low frequency (bass)
audio = [0.1, -0.1, 0.1, -0.1, 0.1, -0.1] # High frequency (treble)

# WAVEFORMS - The pattern of numbers

# Sine wave: smooth, pure tone

sine = np.sin(np.linspace(0, 2\*np.pi, 100))

# Square wave: harsh, buzzy tone

square = np.sign(np.sin(np.linspace(0, 2\*np.pi, 100)))

# Triangle wave: somewhere in between

triangle = 2 _ np.abs(2 _ (np.linspace(0, 1, 100) - 0.5)) - 1

1. Multiplication (Amplitude)
   audio _ 2.0 # Louder
   audio _ 0.5 # Quieter
   audio _ 0.0 # Silence
   audio _ -1.0 # Inverted (phase flip - sounds the same!)
2. Addition (DC Offset)
   audio + 0.1 # Shift waveform up (usually bad)
   audio + 0.0 # No change
   audio - 0.1 # Shift waveform down (usually bad)
3. Non-linear Functions (Distortion/Waveshaping)
   np.tanh(audio) # Soft saturation (smooth distortion)
   np.clip(audio, -x, x) # Hard clipping (harsh distortion)
   np.sin(audio) # Sine waveshaping (metallic)
   audio \*\* 3 # Cubic distortion (adds odd harmonics)
4. Delay/History (Echoes, Reverb)
   audio[i] + audio[i-1000] # Echo from 1000 samples ago
5. Filters (EQ, Tone)

# Moving average = low-pass filter (removes highs)

output[i] = (audio[i] + audio[i-1] + audio[i-2]) / 3
