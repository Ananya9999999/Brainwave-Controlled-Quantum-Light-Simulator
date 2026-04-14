import numpy as np

class WaveSimulator:
    
    def __init__(self):
        x = np.linspace(-10, 10, 400)
        y = np.linspace(-10, 10, 400)
        
        self.X, self.Y = np.meshgrid(x, y)
    
    def generate_wave(self, amplitude, focus):
        
        coherence = focus * 5
        
        wave1 = amplitude * np.sin(
            coherence * np.sqrt(self.X**2 + self.Y**2)
        )
        
        wave2 = amplitude * np.cos(
            coherence * np.sqrt((self.X-2)**2 + (self.Y-2)**2)
        )
        
        interference = wave1 + wave2
        
        return interference