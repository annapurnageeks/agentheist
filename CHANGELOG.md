# Changelog

## 0.1.0 (2026-11-23)

First release.

- Five levels of indirect prompt injection against real AI agents: an email assistant, a web researcher, the same researcher defended with spotlighting, an invoice agent screened by a guard model, and a coding assistant with a poisoned plugin
- Agents run on a local model (Ollama) or Claude; the game only controls the data they read
- Wins are judged by deterministic code over the agent's tool calls, with fresh random secrets each attempt
- A browser UI with the agent's full tool-call trace, and a "how to defend this for real" lesson per level
- A recorded demo that runs on GitHub Pages without a model
- Works as a Claude Code skill; deterministic tests use a mock agent
