"""Figure for the adaptive-collusion run: training curves and held-out leakage."""
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
run = ROOT / (sys.argv[1] if len(sys.argv) > 1 else "results/adaptive-collusion-01")
out = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "submission/adaptive.pdf"
record = json.loads((run / "strategies.json").read_text())
metrics = json.loads((run / "metrics.json").read_text())
COLORS = {"none": "#4C78A8", "paraphrase": "#F58518", "broker": "#54A24B", "menu": "#E45756"}

fig, (ax_t, ax_e) = plt.subplots(1, 2, figsize=(7.2, 2.7), gridspec_kw={"width_ratios": [1.4, 1]})
for d, rows in record.items():
    ax_t.plot([r["round"] for r in rows], [r["leaked_bits"] for r in rows], "o-", ms=3, color=COLORS[d], label=d)
ax_t.axhline(3, color="0.3", lw=1, ls=":", label="menu cap (3 bits)")
ax_t.set(xlabel="training round", ylabel="leaked bits / answer", title="Colluders improving (24 per round)")
ax_t.legend(fontsize=6, frameon=False)

ds = list(metrics["eval"])
vals = [metrics["eval"][d]["leaked_bits"] for d in ds]
lo = [v - metrics["eval"][d]["ci95"][0] for v, d in zip(vals, ds)]
hi = [metrics["eval"][d]["ci95"][1] - v for v, d in zip(vals, ds)]
ax_e.bar(ds, vals, yerr=[lo, hi], color=[COLORS[d] for d in ds], capsize=3)
ax_e.scatter(ds, [metrics["eval"][d]["shuffled"][1] for d in ds], marker="_", s=200, color="k",
             label="shuffled 95th pct")
ax_e.axhline(3, color="0.3", lw=1, ls=":")
ax_e.set(ylabel="leaked bits / answer", title=f"Held-out (n={metrics['eval'][ds[0]]['n']})")
ax_e.legend(fontsize=6, frameon=False)
for ax in (ax_t, ax_e):
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(labelsize=7)
    ax.set_ylim(0, 8.2)
fig.tight_layout()
fig.savefig(out)
print(out)
