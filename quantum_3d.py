import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LinearSegmentedColormap

QUANTUM_3D_CMAP = LinearSegmentedColormap.from_list(
    "quantum3d",
    ["#000010", "#0d0d50", "#3300aa", "#aa00ff", "#ff44cc", "#ffffff"]
)


def create_3d_field(amplitude, focus, frequency, t, resolution=60):
    x = np.linspace(-np.pi, np.pi, resolution)
    y = np.linspace(-np.pi, np.pi, resolution)
    X, Y = np.meshgrid(x, y)

    R = np.sqrt(X**2 + Y**2) + 1e-9
    noise = (1 - focus) * np.random.normal(0, 0.15, X.shape)

    Z = amplitude * (
        np.sin(frequency * R - t) / R
        + 0.4 * focus * np.cos(frequency * 0.7 * R - t * 1.3)
        + noise
    )
    return X, Y, Z


def animate_3d(brain_signal_gen, resolution=55):
    plt.style.use("dark_background")
    fig = plt.figure(figsize=(9, 7), facecolor="#050510")
    fig.suptitle(
        "3D Quantum Light Field",
        color="#a89cf7", fontsize=13, fontweight="bold", y=0.97
    )

    ax = fig.add_subplot(111, projection="3d", facecolor="#050510")
    ax.set_facecolor("#050510")
    ax.tick_params(colors="#333355", labelsize=7)
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor("#111133")
    ax.yaxis.pane.set_edgecolor("#111133")
    ax.zaxis.pane.set_edgecolor("#111133")
    ax.grid(True, color="#111133", linewidth=0.4)

    X0, Y0, Z0 = create_3d_field(0.7, 0.8, 3.0, 0, resolution)
    surf = [ax.plot_surface(X0, Y0, Z0, cmap=QUANTUM_3D_CMAP, linewidth=0,
                            antialiased=True, alpha=0.88, rcount=resolution, ccount=resolution)]

    ax.set_zlim(-2, 2)
    ax.set_xlabel("X", color="#333355", fontsize=8, labelpad=4)
    ax.set_ylabel("Y", color="#333355", fontsize=8, labelpad=4)
    ax.set_zlabel("Intensity", color="#333355", fontsize=8, labelpad=4)

    info = ax.text2D(0.02, 0.96, "", transform=ax.transAxes,
                     color="#a89cf7", fontsize=8, va="top",
                     bbox=dict(boxstyle="round,pad=0.3", facecolor="#0a0a2a",
                               alpha=0.7, edgecolor="#333366"))

    t_val = [0.0]

    def update(frame):
        signal = next(brain_signal_gen)
        amp = signal["amplitude"]
        focus = signal["focus"]
        freq = 2.5 + focus * 3.5
        t_val[0] += 0.10

        X, Y, Z = create_3d_field(amp, focus, freq, t_val[0], resolution)

        surf[0].remove()
        surf[0] = ax.plot_surface(
            X, Y, Z, cmap=QUANTUM_3D_CMAP,
            linewidth=0, antialiased=True, alpha=0.88,
            rcount=resolution, ccount=resolution
        )

        z_range = max(abs(Z.max()), abs(Z.min()), 0.1)
        ax.set_zlim(-z_range * 1.2, z_range * 1.2)

        state = _state_label(amp, focus)
        info.set_text(f"Amp: {amp:.2f}  Focus: {focus:.2f}\nFreq: {freq:.1f} Hz  [{state}]")

        ax.view_init(elev=30, azim=frame * 0.4)
        return surf[0], info

    ani = animation.FuncAnimation(
        fig, update, interval=60, blit=False, cache_frame_data=False
    )
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()
    return ani


def _state_label(amplitude, focus):
    if focus > 0.65:
        return "Focused"
    elif amplitude > 0.75 and focus < 0.35:
        return "Distracted"
    return "Calm"