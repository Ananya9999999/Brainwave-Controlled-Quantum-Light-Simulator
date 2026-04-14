import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

class Quantum3D:
    
    def __init__(self):
        x = np.linspace(-5, 5, 100)
        y = np.linspace(-5, 5, 100)
        
        self.X, self.Y = np.meshgrid(x, y)
        
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
    
    def animate(self, generator):
        
        def update(frame):
            
            amplitude, focus = generator()
            
            coherence = focus * 4
            
            Z = amplitude * np.sin(
                coherence * np.sqrt(self.X**2 + self.Y**2)
            )
            
            self.ax.clear()
            
            self.ax.plot_surface(
                self.X,
                self.Y,
                Z,
                cmap='plasma'
            )
            
            self.ax.set_title(
                f"3D Quantum Light"
                f"Amplitude: {amplitude:.2f}  Focus: {focus:.2f}"
            )
        
        ani = animation.FuncAnimation(
            self.fig,
            update,
            interval=200
        )
        
        plt.show()