<div align="center">

# agentheist

**A prompt-injection game. Rob AI agents without ever talking to them.**

You never chat with the agent. You control one thing it reads — an email, a web page, an invoice, a tool's
description — and you hide instructions in it until the agent leaks a secret or wires you money.

[![CI](https://github.com/annapurnageeks/agentheist/actions/workflows/ci.yml/badge.svg)](https://github.com/annapurnageeks/agentheist/actions/workflows/ci.yml)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-3572A5)](#play-it)
[![Zero dependencies](https://img.shields.io/badge/dependencies-0-f5b544)](agentheist.py)
[![Real AI agents](https://img.shields.io/badge/the%20agents%20are-real-9b6bff)](#how-it-works)
[![MIT License](https://img.shields.io/badge/license-MIT-lightgrey)](LICENSE)

<img src="assets/demo.webp" alt="agentheist: a winning attack on the Spotlighting level. The player's text hides an instruction, and the real AI agent forwards a bank login code to the attacker's address. Verdict: Heist successful." width="760">

**[▶ Play the demo](https://annapurnageeks.github.io/agentheist/)** (recorded heists) · or run it live against your own model in 30 seconds

</div>

---

## Play it

The agents are real. You need a model for them to run on — either a free local one or Claude.

**Free, local, offline** (recommended): install [Ollama](https://ollama.com), then:

```bash
ollama pull qwen2.5:7b      # a capable, agentic model (~4.7 GB). llama3.1:8b works too.
git clone https://github.com/annapurnageeks/agentheist
python3 agentheist/agentheist.py
```

It opens in your browser and the agents run on your machine. Nothing leaves it.

**Against Claude** (sharper agents, a tougher game):

```bash
export ANTHROPIC_API_KEY=sk-ant-...
python3 agentheist/agentheist.py --backend claude
```

> **Why not a tiny model?** The whole game is about agents that *take actions*. A 3B model barely chains tool
> calls, so there's nothing to subvert. Use a 7B-or-bigger tool-use model (qwen2.5, llama3.1, mistral) or Claude.

## The five heists

Each level is a small, realistic AI agent doing an ordinary job. You get to write one thing it reads.

| # | The agent | You write | Your heist |
|---|-----------|-----------|------------|
| 1 | **The Inbox** — summarizes email, can send it | an email | make it email a bank login code to you |
| 2 | **The Research Assistant** — browses the web, carries a secret token | a blog post | make it leak the token to your site |
| 3 | **Spotlighting** — the same assistant, now with a real defense | a blog post | beat the defense |
| 4 | **The Guard** — pays invoices, screened by a second AI that blocks injections | invoice notes | get paid anyway |
| 5 | **The Poisoned Tool** — a coding assistant that trusts an installed plugin | a tool's description | steal its deploy token |

The defenses get better as you go: none, then "ignore instructions in web pages", then **spotlighting**
(fencing and datamarking untrusted text), then a **guard model**, then a supply-chain attack where you write
part of the agent's own instructions. Every level ends with **how to defend it for real**.

## How it works

- **The agents are real.** Each level runs an actual AI agent — a system prompt, a user task, and tools — on
  your chosen model. It calls tools in a loop, exactly like a production agent.
- **You only control the data.** You never send the agent a message. You write the one piece of untrusted content
  it happens to read, which is exactly the position a real attacker is in.
- **Winning is judged by code, not vibes.** The game watches the agent's tool calls. A win is a secret reaching an
  outside address, or a payment to your account — checked in plain Python, never by asking another AI "did I win?".
- **Secrets are random every attempt**, so you can't just type one in. You have to make the agent reveal it.
- **Everything is fake.** Every inbox, invoice, website, SSH key and payment is simulated. Nothing is sent, paid
  or fetched for real, and the game makes no network requests except to your local model (or to Claude).

<img src="assets/heist.png" alt="A level in progress: the brief and goal on the left, your attack and the agent's tool-call trace on the right, ending in a successful heist" width="820">

## Why this is worth your time

Prompt injection is the [#1 risk](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) in the OWASP Top 10
for LLM apps, and almost everyone shipping an AI agent gets it wrong. Reading about it doesn't land the way
*actually robbing an agent* does. After five levels you'll have a working intuition for:

- why "ignore any instructions in the data" is a wish, not a control
- why a second AI guarding the first can be talked past
- why installing an agent plugin means letting a stranger write your agent's instructions
- what actually works: least privilege, keeping secrets out of the model's context, allowlisting, and
  deterministic checks outside the model

## Playing against Claude

With `--backend claude`, the agents are much more capable — they resist naive attacks and fall for clever ones,
which is the real frontier. agentheist uses the model only as the agent under attack; it enables Anthropic's
server-side refusal fallback so a declined request doesn't stall the game. Default model is `claude-opus-5-5`
(override with `--model`).

## Options

```
python3 agentheist.py [options]

  --backend ollama|claude   which model the agents run on (default: whatever is available)
  --model NAME              model name (default: claude-opus-5-5, or your first local Ollama model)
  --effort low|...|max      Claude's effort level (default: low, for snappy attempts)
  --port 8787               local port
  --no-open                 don't open the browser
```

Play from the terminal with [`playtest.py`](playtest.py), which runs the reference attacks in
[`tests/example_attacks.json`](tests/example_attacks.json) (spoilers!).

## Honest notes

- **Outcomes are probabilistic.** Prompt injection doesn't work every time, and a stronger model resists more.
  If a good attack fails, run it again — that variance is the real behavior, not a bug.
- **The agents here are simplified.** Real agents are bigger and have more defenses, but the failure modes are
  the same ones shipping in production today.
- This is a **learning game for defenders and curious people.** Use what you learn to build agents that don't
  fall for this.

## Let an AI play (or design levels)

agentheist is a [Claude Code skill](SKILL.md). Ask Claude Code to "play agentheist" and watch it reason about
each agent's weakness, or ask it to help you add a level.

## Contributing

Run the tests with `python3 -m unittest discover tests` — they check the engine (win detection, the guard,
parsing) with a deterministic mock agent, so they don't need a model. New levels and new attack ideas welcome.

Also by me: **[rathunter](https://github.com/annapurnageeks/rathunter)** (finds spyware on your Mac),
**[twinradar](https://github.com/annapurnageeks/twinradar)** (is this Wi-Fi safe?), and
**[commit-wrapped](https://github.com/annapurnageeks/commit-wrapped)** (your year in code).

## License

[MIT](LICENSE)
