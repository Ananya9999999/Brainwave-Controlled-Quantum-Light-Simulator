import numpy as np

class BrainSignal:
    
    def __init__(self):
        self.amplitude = 1
        self.focus = 0.5
    
    def generate(self):
        
        # Simulated EEG amplitude
        self.amplitude = np.random.uniform(0.5, 2.0)
        
        # Simulated focus level
        self.focus = np.random.uniform(0.1, 1.0)
        
        return self.amplitude, self.focus