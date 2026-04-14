from brain_signal import BrainSignal
from wave_simulator import WaveSimulator
from visualization import Visualizer
from brain_signal import BrainSignal
from quantum_3d import Quantum3D

brain = BrainSignal()
quantum = Quantum3D()


def generator():
    
    amplitude, focus = brain.generate()
    
    return amplitude, focus


quantum.animate(generator)
brain = BrainSignal()
wave = WaveSimulator()
visual = Visualizer()


def generator():
    
    amplitude, focus = brain.generate()
    
    interference = wave.generate_wave(amplitude, focus)
    
    return interference, amplitude, focus


visual.animate(generator)