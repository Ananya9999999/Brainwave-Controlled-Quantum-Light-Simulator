import wave
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Visualizer:
    
    def __init__(self):
        
        self.fig, self.ax = plt.subplots()
    
    def animate(self, generator):
        
        def update(frame):
            
            wave, amplitude, focus = generator()
            
            self.ax.clear()
            
            self.ax.imshow(wave, cmap='plasma')
            
            self.ax.set_title(
                f"Brainwave Quantum Light Simulator\n"
                f"Amplitude: {amplitude:.2f}  Focus: {focus:.2f}"
            )
        
        ani = animation.FuncAnimation(
            self.fig,
            update,
            interval=200
        )
        self.ax.clear()
        self.ax.imshow(wave, cmap='viridis')
        plt.show()