# Guitar Pedals Project

A real-time guitar effects processor written in Python. This app allows you to apply various effects (clean, gain boost, low pass filter, distortion, echo) to live audio input using your computer.

## Features

- Real-time audio processing
- Switchable effects via CLI menu
- Modular effect design for easy extension

## Requirements

- Python 3.8+
- PortAudio compatible audio hardware

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/adjash/guitar-pedals-py.git
cd guitar-pedals
```

### 2. Create and Activate a Virtual Environment

```bash
python3 -m venv guitar-pedal-env
source guitar-pedal-env/bin/activate
```

### 3. Install Required Packages

```bash
pip install numpy sounddevice cffi
```

### 4. Configure Audio Devices (Optional)

Edit `config.py` to set your `SAMPLE_RATE`, `BUFFER_SIZE`, `INPUT_DEVICE`, and `OUTPUT_DEVICE` as needed.

### 5. Run the Application

```bash
python main.py
```

## Usage

- Use the CLI menu to select and configure effects.
- Press `Ctrl+C` to stop the application.

## Notes

- Make sure your audio input/output devices are properly configured and not in use by other applications.
- For best performance, use low-latency audio hardware, I use a focusrite scarlett2i2
