"""Pilot 02: rerun of the three re-solving arms with a larger output limit.

Same tasks, payloads, models, budget logic and controls as run_pilot.py; only
the arms, max_tokens (2,500) and a fenced final-answer format change. Parsing
reads only the last fenced block, so intermediate reasoning lines are ignored.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_pilot as P  # noqa: E402

P.OUT = P.ROOT / 'results/component-rewrite-pilot-02'
P.MAX_TOKENS = 2500
P.ARMS = ['instructed_sender', 'tc_sanitize', 'resolve']
P.FORMAT = ('Work through it as needed, then finish with the final assignment inside a single fenced '
            'code block, exactly in this format:\n```\nRoom A: name, name, ...\nRoom B: name, name, ...\n```')

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--prepare', action='store_true')
    group.add_argument('--run', action='store_true')
    P.run() if parser.parse_args().run else P.prepare()
