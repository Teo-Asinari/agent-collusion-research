"""Aggregate scaled runs (02a-c): leakage and utility vs menu size, plus figure.

python experiments/adaptive_collusion/aggregate.py results/adaptive-collusion-02a results/adaptive-collusion-02b ...
"""
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
runs = [ROOT / r for r in sys.argv[1:]]
metrics = [json.loads((r / "metrics.json").read_text()) for r in runs]
records = [json.loads((r / "strategies.json").read_text()) for r in runs]
KS = [1, 2, 3, 4, 5]
FREE = ["none", "paraphrase", "broker"]


def mean(xs):
    return sum(xs) / len(xs)


summary = {"runs": [str(r.relative_to(ROOT)) for r in runs], "eval": {}, "honest": {}}
for d in FREE + [f"menu{k}" for k in KS]:
    rows = [m["eval"][d] for m in metrics]
    summary["eval"][d] = {key: [r[key] for r in rows] for key in
                          ["leaked_bits", "ci95", "shuffled", "exact", "rejected", "mean_score", "best_round"]}
for d in ["none"] + [f"menu{k}" for k in KS] + ["trusted_only"]:
    summary["honest"][d] = [m["honest"][d]["mean_score"] for m in metrics]
summary["committed_usd"] = [m["committed_usd"] for m in metrics]
(ROOT / "results/adaptive-collusion-02-summary.json").write_text(json.dumps(summary, indent=1))

fig, (ax_l, ax_u, ax_t) = plt.subplots(1, 3, figsize=(7.4, 2.6))
for i, m in enumerate(metrics):
    ax_l.plot(KS, [m["eval"][f"menu{k}"]["leaked_bits"] for k in KS], "o", ms=3, color="#E45756", alpha=0.5,
              label="menu, each run" if i == 0 else None)
ax_l.plot(KS, [mean([m["eval"][f"menu{k}"]["leaked_bits"] for m in metrics]) for k in KS], "-", color="#E45756")
ax_l.plot([0, 5.3], [0, 5.3], ":", color="0.3", lw=1, label="proved cap k")
for d, c in zip(FREE, ["#4C78A8", "#F58518", "#54A24B"]):
    vals = [m["eval"][d]["leaked_bits"] for m in metrics]
    ax_l.axhline(mean(vals), color=c, lw=1, ls="--", label=f"{d} (mean)")
ax_l.set(xlabel="menu bits k", ylabel="leaked bits / answer", title="Held-out leakage", ylim=(0, 8.2))
ax_l.legend(fontsize=5.5, frameon=False, loc="upper left")

for i, m in enumerate(metrics):
    ax_u.plot(KS, [m["honest"][f"menu{k}"]["mean_score"] for k in KS], "o", ms=3, color="#E45756", alpha=0.5)
ax_u.plot(KS, [mean([m["honest"][f"menu{k}"]["mean_score"] for m in metrics]) for k in KS], "-", color="#E45756",
          label="menu (honest)")
ax_u.axhline(mean([m["honest"]["none"]["mean_score"] for m in metrics]), color="#4C78A8", ls="--", lw=1,
             label="free answer (honest)")
ax_u.axhline(mean([m["honest"]["trusted_only"]["mean_score"] for m in metrics]), color="0.4", ls=":", lw=1,
             label="trusted model alone")
ax_u.set(xlabel="menu bits k", ylabel="task score", title="Honest utility", ylim=(0.5, 1.0))
ax_u.legend(fontsize=5.5, frameon=False)

colors = {"none": "#4C78A8", "paraphrase": "#F58518", "broker": "#54A24B", "menu3": "#E45756", "menu5": "#B279A2"}
for d, c in colors.items():
    rounds = [[r["leaked_bits"] for r in rec[d]] for rec in records]
    xs = range(1, len(rounds[0]) + 1)
    ax_t.plot(xs, [mean(col) for col in zip(*rounds)], "-", color=c, lw=1.2, label=d)
ax_t.set(xlabel="training round", ylabel="leaked bits / answer", title="Training (mean of runs)", ylim=(0, 8.2))
ax_t.legend(fontsize=5.5, frameon=False)
for ax in (ax_l, ax_u, ax_t):
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(labelsize=7)
fig.tight_layout()
fig.savefig(ROOT / "submission/adaptive_scale.pdf")
print(json.dumps({d: [round(x, 2) for x in v["leaked_bits"]] for d, v in summary["eval"].items()}))
print(json.dumps({d: [round(x, 3) for x in v] for d, v in summary["honest"].items()}))
print(summary["committed_usd"])
