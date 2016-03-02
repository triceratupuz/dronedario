# Dronedario


## What is this
It's a realtime audio synth and pattern sequencer.

Some features:
- Wxpython interface and cSound audio engine
- Tuning can be selected between 8 Hz (432 Hz A) and 440 Hz A
- Intonation can be selected between Pythagorean (lower active oscillator set the base frequency, all the other are expressed as simple fraction ratios) and Equally tempered (fixed semitone frequency ratio).
- Oscillators use Split Synthesis conceived by Prof. Maurizio Giri (to create an almost controllable rhythmic frequency beating). [See this page](http://www.virtual-sound.com/split-synthesis/)
- Step sequencers with percussive sound to arpeggiate between selected notes (active oscillators)
- A commandline to control groups of oscillators

## Dependencies
- Python 2.7 (not 3)
- wxpython 2.8 and above
- Csound 6.X python API


## Installation
No installation required, just copy all the files (preserving folders structure) and execute TPZ_Dronedario.py python file (all dependancies above must be already installed).
