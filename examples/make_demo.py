"""Build the static demo (docs/index.html) from recorded heists in examples/recorded.json.

The demo runs on GitHub Pages, which can't run Python, so it replays attempts captured earlier against a real
model. Regenerate the recordings with `python3 playtest.py --record` while the game server is running.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import agentheist as g

recorded = json.loads((ROOT / "examples" / "recorded.json").read_text())
model = next((v["result"].get("model") for v in recorded.values() if v.get("result")), "a local model")
config = {
    "mode": "demo",
    "model": model,
    "version": g.VERSION,
    "levels": [level.public() for level in g.LEVELS.values()],
    "recorded": {int(k): v for k, v in recorded.items()},
}
page = (ROOT / "game.html").read_text(encoding="utf-8")
page = page.replace("/*__CONFIG__*/null", json.dumps(config, ensure_ascii=False).replace("</", "<\\/"))
out = ROOT / "docs" / "index.html"
out.parent.mkdir(exist_ok=True)
out.write_text(page, encoding="utf-8")
print(f"wrote {out} ({sum(v['result']['won'] for v in recorded.values())}/{len(recorded)} recorded wins)")
