import argparse
from brain_signal import generate_brain_signals
from visualization import animate
from quantum_3d import animate_3d


def main():
    parser = argparse.ArgumentParser(description="Brainwave Quantum Light Simulator")
    parser.add_argument(
        "--state", choices=["calm", "focus", "distract"], default="focus",
        help="Initial brain state (default: focus)"
    )
    parser.add_argument(
        "--mode", choices=["2d", "3d", "both"], default="2d",
        help="Visualization mode (default: 2d)"
    )
    parser.add_argument(
        "--resolution", type=int, default=300,
        help="2D field resolution width (default: 300)"
    )
    args = parser.parse_args()

    print(f"Starting simulator | state={args.state} | mode={args.mode}")
    print("Close the plot window to exit.\n")

    if args.mode == "2d":
        sig = generate_brain_signals(state=args.state)
        animate(sig, wave_simulator=None, resolution=(args.resolution, args.resolution // 2))

    elif args.mode == "3d":
        sig = generate_brain_signals(state=args.state)
        animate_3d(sig)

    elif args.mode == "both":
        import threading
        sig1 = generate_brain_signals(state=args.state)
        sig2 = generate_brain_signals(state=args.state)

        t1 = threading.Thread(target=animate, args=(sig1, None, (args.resolution, args.resolution // 2)), daemon=True)
        t2 = threading.Thread(target=animate_3d, args=(sig2,), daemon=True)

        t1.start()
        t2.start()
        t1.join()
        t2.join()


if __name__ == "__main__":
    main()