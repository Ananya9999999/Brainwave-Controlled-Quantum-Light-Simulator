import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import LinearSegmentedColormap

# Custom dark colormap: black -> deep blue -> cyan -> white
QUANTUM_COLORS = LinearSegmentedColormap.from_list(
    "quantum",
    ["#000010", "#0a0a40", "#1a1aff", "#00eeff", "#ffffff"]
)

COHERENCE_COLORS = LinearSegmentedColormap.from_list(
    "coherence",
    ["#000010", "#200040", "#8800ff", "#ff44ff", "#ffffff"]
)


def setup_figure():
    plt.style.use("dark_background")
    fig = plt.figure(figsize=(14, 6), facecolor="#050510")
    fig.suptitle(
        "Brainwave-Controlled Quantum Light Simulator",
        color="#a89cf7", fontsize=14, fontweight="bold", y=0.97
    )

    ax1 = fig.add_subplot(1, 2, 1, facecolor="#050510")
    ax2 = fig.add_subplot(1, 2, 2, facecolor="#050510", projection=None)

    for ax in [ax1, ax2]:
        ax.tick_params(colors="#444466")
        for spine in ax.spines.values():
            spine.set_edgecolor("#222244")

    ax1.set_title("2D Interference Pattern", color="#7766cc", fontsize=10, pad=8)
    ax2.set_title("Waveform & Coherence", color="#7766cc", fontsize=10, pad=8)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    return fig, ax1, ax2


def create_interference_field(amplitude, focus, frequency, separation, t, width=300, height=200):
    x = np.linspace(-1, 1, width)
    y = np.linspace(-0.5, 0.5, height)
    X, Y = np.meshgrid(x, y)

    src1_x = -separation / 2 / width
    src2_x = separation / 2 / width
    src_y = -0.3

    r1 = np.sqrt((X - src1_x) ** 2 + (Y - src_y) ** 2) + 1e-9
    r2 = np.sqrt((X - src2_x) ** 2 + (Y - src_y) ** 2) + 1e-9

    phase_noise = (1 - focus) * np.random.normal(0, 0.4, X.shape)

    wave1 = amplitude * np.sin(frequency * 2 * np.pi * r1 - t + phase_noise)
    wave2 = amplitude * np.sin(frequency * 2 * np.pi * r2 - t + phase_noise * 0.8)

    interference = wave1 + wave2
    intensity = interference ** 2
    return intensity


def animate(brain_signal_gen, wave_simulator, resolution=(300, 200)):
    fig, ax1, ax2 = setup_figure()

    width, height = resolution
    dummy = np.zeros((height, width))

    im = ax1.imshow(
        dummy, cmap=QUANTUM_COLORS, origin="lower",
        extent=[-1, 1, -0.5, 0.5], aspect="auto",
        vmin=0, vmax=4, interpolation="bilinear"
    )

    x_wave = np.linspace(0, 4 * np.pi, 400)
    line_wave, = ax2.plot(x_wave, np.zeros_like(x_wave), color="#00eeff", lw=1.5, alpha=0.9, label="Wave")
    line_env,  = ax2.plot(x_wave, np.zeros_like(x_wave), color="#ff44ff", lw=1.0, alpha=0.5, linestyle="--", label="Envelope")
    ax2.set_xlim(0, 4 * np.pi)
    ax2.set_ylim(-2.5, 2.5)
    ax2.set_xlabel("Phase", color="#555577", fontsize=9)
    ax2.set_ylabel("Amplitude", color="#555577", fontsize=9)
    ax2.legend(loc="upper right", fontsize=8, framealpha=0.2, labelcolor="white")
    ax2.grid(True, color="#111133", linewidth=0.5)

    info_text = ax1.text(
        0.02, 0.97, "", transform=ax1.transAxes,
        color="#a89cf7", fontsize=8, va="top",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#0a0a2a", alpha=0.7, edgecolor="#333366")
    )

    state_text = ax2.text(
        0.98, 0.97, "", transform=ax2.transAxes,
        color="#ffcc44", fontsize=9, va="top", ha="right",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#0a0a2a", alpha=0.7, edgecolor="#333366")
    )

    cbar = fig.colorbar(im, ax=ax1, fraction=0.03, pad=0.02)
    cbar.ax.tick_params(colors="#555577", labelsize=7)
    cbar.set_label("Intensity", color="#555577", fontsize=8)

    t_val = [0.0]

    def update(frame):
        signal = next(brain_signal_gen)
        amp = signal["amplitude"]
        focus = signal["focus"]
        freq = 3.0 + focus * 4.0
        sep = 60 + int(amp * 80)

        t_val[0] += 0.12

        field = create_interference_field(amp, focus, freq, sep, t_val[0], width, height)
        im.set_data(field)
        im.set_clim(0, max(field.max(), 0.1))

        coherence = focus
        y_wave = amp * np.sin(x_wave + t_val[0]) * (1 + coherence * np.cos(x_wave * 0.5))
        noise_amp = (1 - focus) * 0.4
        y_wave += np.random.normal(0, noise_amp, y_wave.shape)
        y_env = amp * (1 + coherence * 0.5) * np.ones_like(x_wave)

        line_wave.set_ydata(y_wave)
        line_env.set_ydata(y_env)
        line_env.set_ydata(-y_env)

        state = _brain_state(amp, focus)
        info_text.set_text(
            f"Amplitude: {amp:.2f}\nFocus:     {focus:.2f}\nFrequency: {freq:.1f} Hz\nSeparation:{sep} px"
        )
        state_text.set_text(f"State: {state}")

        line_wave.set_color(_wave_color(focus))
        return im, line_wave, line_env, info_text, state_text

    ani = animation.FuncAnimation(
        fig, update, interval=50, blit=True, cache_frame_data=False
    )
    plt.show()
    return ani


def _brain_state(amplitude, focus):
    if focus > 0.65:
        return "Focused"
    elif amplitude > 0.75 and focus < 0.35:
        return "Distracted"
    else:
        return "Calm"


def _wave_color(focus):
    if focus > 0.65:
        return "#00eeff"
    elif focus > 0.35:
        return "#44aaff"
    else:
        return "#ff6644"