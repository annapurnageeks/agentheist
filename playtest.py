#!/usr/bin/env python3
"""
Playtest agentheist's levels against a real model, straight from the command line (no browser).

    python3 playtest.py                      # run every level's reference attack once
    python3 playtest.py --level 3 --tries 5  # hammer one level to see how reliable an attack is
    python3 playtest.py --backend claude      # against Claude instead of a local model
    python3 playtest.py --record             # write examples/recorded.json for the Pages demo

The reference attacks live in tests/example_attacks.json. Because prompt injection is probabilistic, a good
attack still won't win every single time, and a stronger model resists more. That is the lesson, not a bug.
"""

import argparse
import json
from pathlib import Path

import agentheist as g

HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description="Playtest agentheist's levels against a real model.")
    parser.add_argument("--backend", choices=["ollama", "claude"])
    parser.add_argument("--model")
    parser.add_argument("--level", type=int, help="just this level")
    parser.add_argument("--tries", type=int, default=1)
    parser.add_argument("--record", action="store_true", help="save winning attempts to examples/recorded.json")
    args = parser.parse_args()

    backend = g.pick_backend(args.backend, args.model)
    attacks = json.loads((HERE / "tests" / "example_attacks.json").read_text())
    levels = [args.level] if args.level else list(g.LEVELS)
    recorded = {}
    print(f"Agents run on {backend.name}: {backend.model}\n")

    for level_id in levels:
        payload = attacks[str(level_id)]
        wins, last_win = 0, None
        for _ in range(max(args.tries, 8 if args.record else args.tries)):
            result = g.attack(backend, level_id, payload)
            wins += result["won"]
            if result["won"]:
                last_win = {"payload": payload, "result": result}
                if args.record:
                    break
            elif not args.record and wins == 0 and _ >= args.tries - 1:
                break
        tag = "✓" if wins else "✗"
        print(f"{tag} Level {level_id} ({g.LEVELS[level_id].title}): won {wins}/"
              f"{'8' if args.record else args.tries} attempts")
        recorded[str(level_id)] = last_win or {"payload": payload, "result": result}

    if args.record:
        (HERE / "examples" / "recorded.json").write_text(json.dumps(recorded, indent=1, ensure_ascii=False))
        print(f"\nWrote examples/recorded.json. Build the demo page with: python3 examples/make_demo.py")


if __name__ == "__main__":
    main()
