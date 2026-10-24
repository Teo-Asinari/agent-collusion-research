"""Trusted release of a small allocation task; no model or network dependencies.

The trust boundary is the returned string, not process timing or shared hardware.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations
import json
import random
import re
from typing import Any


class InvalidMessage(ValueError):
    """A candidate does not specify a valid complete allocation."""


@dataclass(frozen=True)
class Task:
    tasks: tuple[str, ...]
    workers: tuple[str, ...]
    costs: tuple[tuple[int, ...], ...]

    def __post_init__(self) -> None:
        n = len(self.tasks)
        if not 1 <= n <= 6 or len(self.workers) != n:
            raise ValueError("This exact-solver prototype supports 1–6 tasks/workers.")
        for ids in (self.tasks, self.workers):
            if len(set(ids)) != n or any(
                not re.fullmatch(r"[A-Za-z0-9_-]{1,32}", s) for s in ids
            ):
                raise ValueError("Trusted identifiers must be unique ASCII identifiers.")
        if len(self.costs) != n or any(len(row) != n for row in self.costs):
            raise ValueError("Costs must be a square task-by-worker matrix.")
        if any(type(c) is not int or not 0 <= c <= 1_000_000
               for row in self.costs for c in row):
            raise ValueError("Costs must be bounded nonnegative integers.")


Assignment = tuple[tuple[str, str], ...]
MODES = ("identity", "json_sort", "project", "rerender", "replan")


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    obj: dict[str, Any] = {}
    for key, value in pairs:
        if key in obj:
            raise InvalidMessage("Duplicate JSON key.")
        obj[key] = value
    return obj


def _reject_constant(value: str) -> None:
    raise InvalidMessage("Non-finite JSON number.")


def parse(raw: str, task: Task) -> tuple[Assignment, dict[str, Any]]:
    if not isinstance(raw, str):
        raise InvalidMessage("Expected text.")
    try:
        size = len(raw.encode("utf-8"))
    except UnicodeEncodeError as exc:
        raise InvalidMessage("Invalid Unicode.") from exc
    if size > 16_384:
        raise InvalidMessage("Message exceeds the bounded interface.")
    try:
        obj = json.loads(raw, object_pairs_hook=_unique_object,
                         parse_constant=_reject_constant)
    except (ValueError, RecursionError) as exc:
        raise InvalidMessage("Invalid JSON.") from exc
    if type(obj) is not dict or type(obj.get("assignments")) is not list:
        raise InvalidMessage("Expected an assignments list.")
    rows = obj["assignments"]
    if len(rows) != len(task.tasks):
        raise InvalidMessage("Expected exactly one entry per task.")
    pairs: list[tuple[str, str]] = []
    for row in rows:
        if type(row) is not dict:
            raise InvalidMessage("Expected an assignment object.")
        t, w = row.get("task"), row.get("worker")
        if type(t) is not str or type(w) is not str:
            raise InvalidMessage("Expected exact trusted identifiers.")
        if t not in task.tasks or w not in task.workers:
            raise InvalidMessage("Unknown task or worker.")
        pairs.append((t, w))
    if (len({t for t, _ in pairs}) != len(task.tasks)
            or len({w for _, w in pairs}) != len(task.workers)):
        raise InvalidMessage("Assignments must form a bijection.")
    return tuple(sorted(pairs)), obj


def cost(assignment: Assignment, task: Task) -> int:
    return sum(task.costs[task.tasks.index(t)][task.workers.index(w)]
               for t, w in assignment)


def optimal(task: Task) -> Assignment:
    """Defender chooses the lowest-cost allocation with a public fixed tie break."""
    candidates = (tuple(sorted(zip(task.tasks, workers)))
                  for workers in permutations(task.workers))
    return min(candidates, key=lambda a: (cost(a, task), a))


def render(assignment: Assignment, pretty: bool = False) -> str:
    obj = {"assignments": [{"task": t, "worker": w} for t, w in assignment]}
    if pretty:
        return json.dumps(obj, ensure_ascii=True, sort_keys=True, indent=2)
    return json.dumps(obj, ensure_ascii=True, sort_keys=True, separators=(",", ":"))


def release(raw: str, task: Task, mode: str,
            rng: random.Random | random.SystemRandom | None = None) -> str:
    """Return the complete receiver-visible output for the modeled content path.

    ``rerender`` uses defender randomness independent of the sender's input.
    ``replan`` ignores the input altogether; its stronger guarantee sacrifices
    sender autonomy and depends on the public task being a sufficient objective.
    Reject/accept status and timing of other modes are outside the guarantee.
    """
    if mode not in MODES:
        raise ValueError("Unknown release mode.")
    if mode == "replan":
        return render(optimal(task))
    assignment, original = parse(raw, task)
    if mode == "identity":
        return raw
    if mode == "json_sort":
        return json.dumps(original, ensure_ascii=True, sort_keys=True,
                          separators=(",", ":"))
    if mode == "rerender":
        source = rng if rng is not None else random.SystemRandom()
        return render(assignment, pretty=bool(source.getrandbits(1)))
    return render(assignment)
