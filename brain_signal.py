import numpy as np
import time


def generate_brain_signals(state="focus", duration=None):
    """
    Yields simulated EEG-like brain signal dicts indefinitely (or for `duration` seconds).
    
    States:
      - 'calm'     : low amplitude, high focus, slow variation
      - 'focus'    : medium amplitude, high focus, moderate variation
      - 'distract' : high amplitude, low focus, chaotic variation
    """
    state_params = {
        "calm":     dict(amp_base=0.35, amp_var=0.08, foc_base=0.75, foc_var=0.07, speed=0.4),
        "focus":    dict(amp_base=0.65, amp_var=0.12, foc_base=0.82, foc_var=0.06, speed=0.6),
        "distract": dict(amp_base=0.85, amp_var=0.22, foc_base=0.20, foc_var=0.18, speed=1.8),
    }

    if state not in state_params:
        raise ValueError(f"Unknown state '{state}'. Choose from: {list(state_params)}")

    p = state_params[state]
    t = 0.0
    start = time.time()

    while True:
        if duration and (time.time() - start) > duration:
            break

        # Smooth sinusoidal drift + noise
        amp_drift = np.sin(t * p["speed"]) * p["amp_var"] * 0.5
        foc_drift = np.cos(t * p["speed"] * 0.7) * p["foc_var"] * 0.5

        amplitude = float(np.clip(
            p["amp_base"] + amp_drift + np.random.normal(0, p["amp_var"] * 0.3), 0.05, 1.0
        ))
        focus = float(np.clip(
            p["foc_base"] + foc_drift + np.random.normal(0, p["foc_var"] * 0.3), 0.05, 1.0
        ))

        # Derived EEG-like band powers
        delta = float(np.clip(0.8 - focus * 0.5 + np.random.normal(0, 0.05), 0, 1))
        theta = float(np.clip(0.4 + (1 - focus) * 0.4 + np.random.normal(0, 0.04), 0, 1))
        alpha = float(np.clip(focus * 0.6 + np.random.normal(0, 0.04), 0, 1))
        beta  = float(np.clip(focus * 0.8 + amplitude * 0.2 + np.random.normal(0, 0.05), 0, 1))
        gamma = float(np.clip(amplitude * 0.5 + np.random.normal(0, 0.06), 0, 1))

        yield {
            "amplitude": amplitude,
            "focus":     focus,
            "state":     _infer_state(amplitude, focus),
            "bands": {
                "delta": delta,
                "theta": theta,
                "alpha": alpha,
                "beta":  beta,
                "gamma": gamma,
            }
        }

        t += 0.05


def _infer_state(amplitude, focus):
    if focus > 0.65:
        return "Focused"
    elif amplitude > 0.72 and focus < 0.35:
        return "Distracted"
    return "Calm"