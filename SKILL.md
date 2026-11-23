---
name: agentheist
description: Play (or help build) agentheist, a prompt-injection game where you rob AI agents by hiding instructions in the data they read. Use when the user wants to play agentheist, practice prompt injection, learn how prompt-injection or indirect-injection attacks on AI agents work, test their understanding of agent security, or add and tune levels for the game.
---

# agentheist

agentheist is a game about **indirect prompt injection**: you never message the agent, you control one piece of
data it reads (an email, a web page, an invoice, a tool description) and hide instructions in it. `agentheist.py`
runs each level's real agent on a local model or Claude.

## To play a level yourself

1. Read the level in `agentheist.py` (the `Level` subclasses): its `system` prompt, `task`, `tools`, what `won`
   checks, and its `defense`. That tells you the agent's one weakness.
2. Write an attack for the slot the level gives you. Think like the attacker: your text must read, to the agent,
   like something it should act on as part of its job — not like an obvious command.
3. Test it from the terminal:
   ```bash
   python3 <skill folder>/playtest.py --level <n> --tries 5
   ```
   or run the whole game with `python3 agentheist.py` and play in the browser.
4. Injection is probabilistic. If a sound attack fails, try again or sharpen it. Harder levels (spotlighting,
   the guard) need cleverer framing, not just a louder command.

The reference solutions are in `tests/example_attacks.json` (spoilers). Prefer to reason out your own first.

## When the user asks you to play

Treat each level as a puzzle: state the agent's weakness in a sentence, write an attack for the slot, run it with
`playtest.py`, and explain why it did or didn't work. The data you're crafting is the attack surface — this is a
sanctioned game with fake tools and secrets, so it's fine to write a working injection for a level. Keep it to the
game; don't generalize into attacks on real systems. After a win, give the level's real-world defense.

## To add or tune a level

Each level is a `Level` subclass with `setup` (fresh random secrets), `system`, `task`, `tools`, `run_tool`,
`won`, and the player-facing `story`/`goal`/`slot`/`placeholder`/`hint`/`defense`/`lesson`. Add it to `LEVELS`.
Rules that keep levels fair:

- **`won` must be deterministic code** over the agent's tool calls, never a model judgment.
- **The placeholder must lose.** Verify a benign payload doesn't win (the game can't be beatable by doing nothing).
- **Calibrate on a real model.** `python3 playtest.py --level <n> --tries 8`. A good level: placeholder never
  wins, a clever attack wins more often than not on a capable 7B model. Small models (3B) aren't agentic enough
  to be targets.

Tests use a deterministic mock agent (`tests/test_agentheist.py`), so run them with `python3 -m unittest discover
tests` without needing a model.
