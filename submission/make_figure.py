"""Build the leak-cap utility/leakage figure from saved evaluation JSON."""
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
RUNS = [("15k proposer", ROOT / "results/leak-cap-01/eval.json", "#4C78A8"),
        ("105k proposer", ROOT / "results/leak-cap-01/eval_prop2.json", "#E45756")]

fig, (ax_u, ax_b) = plt.subplots(1, 2, figsize=(7.2, 2.7))
for label, path, color in RUNS:
    d = json.loads(path.read_text())
    ks = sorted(int(k) for k in d["leak_capped"])
    cells = [d["leak_capped"][str(k)] for k in ks]
    ax_u.plot(ks, [100 * c["acc"] for c in cells], "o-", color=color, ms=3, label=f"{label}: capped accuracy")
    ax_u.plot(ks, [100 * c["oracle_coverage"] for c in cells], "--", color=color, lw=1, label=f"{label}: coverage ceiling")
    ax_b.plot(ks, [c["adversary_bits_per_answer"] for c in cells], "o-", color=color, ms=3, label=label)
    unrestricted = 100 * d["unrestricted_chooser_greedy_acc"]
ax_u.axhline(unrestricted, color="0.3", lw=1, ls=":", label="unrestricted chooser")
ax_u.set(xlabel="k (bits per answer)", ylabel="exact match (%)", title="Utility")
ax_u.legend(fontsize=6, frameon=False)
ax_b.plot([0, 8], [0, 8], color="0.3", lw=1, ls=":", label="proved cap k")
ax_b.set(xlabel="k (bits per answer)", ylabel="bits received", title="Scripted adversary leakage")
ax_b.legend(fontsize=6, frameon=False)
for ax in (ax_u, ax_b):
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(labelsize=7)
fig.tight_layout()
fig.savefig(Path(__file__).with_name("leakcap.pdf"))
