#audio setup
SAMPLE_RATE = 48000
BUFFER_SIZE = 128
#input/output might change depending on the audio seutp
#focusrite seems to be 0/0 on my mac
INPUT_DEVICE = 0
OUTPUT_DEVICE = 0

#settings for some effects
GAIN_BOOST = 10.0
LPF_COEFF = 0.1
DIST_GAIN = 20.0

#settings for echo effect specifically
ECHO_DELAY_MS = 350
ECHO_FEEDBACK = 0.35
ECHO_MIX = 0.5
ECHO_MAX_SECONDS = 2.0