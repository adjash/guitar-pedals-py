# import sounddevice as sd
# import numpy as np
# import time
# import threading

# # ===== AUDIO CONFIG =====
# SAMPLE_RATE = 48000
# BUFFER_SIZE = 128

# INPUT_DEVICE = 0
# OUTPUT_DEVICE = 0

# # ===== EFFECT PARAMETERS =====
# GAIN_BOOST = 10.0
# LPF_COEFF = 0.1
# prev_lpf = 0.0

# DIST_GAIN = 20.0

# # ==== ECHO PARAMETERS ====
# ECHO_DELAY_MS = 350
# ECHO_FEEDBACK = 0.35      # 0.0–0.99
# ECHO_MIX = 0.5            # 0 dry..1 wet
# ECHO_MAX_SECONDS = 2.0    # buffer allocation

# # Convert delay to samples
# echo_delay_samples = int(SAMPLE_RATE * (ECHO_DELAY_MS / 1000.0))
# echo_buffer_size = int(SAMPLE_RATE * ECHO_MAX_SECONDS)

# # Circular delay buffer + write pointer
# echo_buffer = np.zeros(echo_buffer_size, dtype="float32")
# echo_write_idx = 0

# # ===== CURRENT EFFECT =====
# current_fx = 0
# running = True


# # ===== AUDIO CALLBACK =====
# def audio_callback(indata, outdata, frames, time_data, status):
#     global prev_lpf, current_fx
#     global echo_buffer, echo_write_idx

#     audio = indata[:, 0]

#     if current_fx == 0:
#         # CLEAN
#         out = audio

#     elif current_fx == 1:
#         # GAIN BOOST
#         out = audio * GAIN_BOOST

#     elif current_fx == 2:
#         # LOW PASS FILTER
#         alpha = LPF_COEFF
#         out = np.empty_like(audio)

#         prev_lpf = prev_lpf + alpha * (audio[0] - prev_lpf)
#         out[0] = prev_lpf

#         for i in range(1, len(audio)):
#             prev_lpf = prev_lpf + alpha * (audio[i] - prev_lpf)
#             out[i] = prev_lpf

#     elif current_fx == 3:
#         # DISTORTION
#         boosted = audio * DIST_GAIN
#         out = np.tanh(boosted)

#     elif current_fx == 4:
#         # ===== ECHO / DELAY =====

#         out = np.zeros_like(audio)
#         for i in range(frames):

#             # Calculate read index (delay)
#             read_idx = (echo_write_idx - echo_delay_samples) % echo_buffer_size
#             delayed_sample = echo_buffer[read_idx]

#             dry = audio[i]
#             wet = delayed_sample

#             # Mix dry/wet
#             out_sample = (1.0 - ECHO_MIX) * dry + ECHO_MIX * wet
#             out[i] = out_sample

#             # Write to circular buffer: current + feedback portion
#             echo_buffer[echo_write_idx] = dry + delayed_sample * ECHO_FEEDBACK

#             # Advance pointer
#             echo_write_idx = (echo_write_idx + 1) % echo_buffer_size

#     else:
#         out = audio

#     outdata[:] = out.reshape(-1, 1)


# # ===== CLI MENU THREAD =====
# def cli_menu():
#     global current_fx, running
#     print("\n Guitar FX Menu")
#     print("1 = Clean")
#     print("2 = Gain Boost")
#     print("3 = Low-Pass Filter")
#     print("4 = Distortion")
#     print("5 = Echo")
#     print("q = Quit")
#     print("-----------------------------------")

#     while running:
#         choice = input("> ").strip()

#         if choice == "1":
#             current_fx = 0
#             print("→ Clean enabled")
#         elif choice == "2":
#             current_fx = 1
#             print("→ Gain Boost enabled")
#         elif choice == "3":
#             current_fx = 2
#             print("→ Low-Pass Filter enabled")
#         elif choice == "4":
#             current_fx = 3
#             print("→ Distortion enabled")
#         elif choice == "5":
#             current_fx = 4
#             print("→ Echo enabled")
#         elif choice == "q":
#             print("Exiting…")
#             running = False
#             break
#         else:
#             print("Unknown option")


# # ===== MAIN =====
# print("Starting real-time guitar FX…")

# # Run menu in parallel
# threading.Thread(target=cli_menu, daemon=True).start()

# try:
#     with sd.Stream(
#         samplerate=SAMPLE_RATE,
#         blocksize=BUFFER_SIZE,
#         dtype="float32",
#         channels=1,
#         callback=audio_callback,
#         device=(INPUT_DEVICE, OUTPUT_DEVICE),
#         latency="low",
#     ):
#         while running:
#             time.sleep(0.1)
# except KeyboardInterrupt:
#     running = False
#     print("\nStopped.")