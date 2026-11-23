# Security

agentheist is a learning game about prompt injection. Every agent, tool, website, secret and payment in it is
simulated. It makes no network requests except to the model you run it against (a local Ollama model, or the
Anthropic API with `--backend claude`). The local server binds to `127.0.0.1` and refuses cross-site requests.

The attacks you write are scoped to the game's fake agents. Please don't use anything here against real systems
you don't own or aren't authorized to test.

**Found a vulnerability in agentheist itself** (e.g. the local server, or HTML injection in the game page)? Report
it privately via [GitHub's private vulnerability reporting](https://github.com/annapurnageeks/agentheist/security/advisories/new).
