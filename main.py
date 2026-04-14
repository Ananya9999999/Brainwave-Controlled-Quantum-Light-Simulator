from brain_signal import BrainSignal
from wave_simulator import WaveSimulator
from visualization import Visualizer

brain = BrainSignal()
wave = WaveSimulator()
visual = Visualizer()


def generator():
    
    amplitude, focus = brain.generate()
    
    interference = wave.generate_wave(amplitude, focus)
    
    return interference, amplitude, focus


visual.animate(generator)