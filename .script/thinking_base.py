#!/usr/bin/env python3

# Loads every spinning_* script and paints one of them. When the status
# line changes, a different spinner takes over. The reasoning stream and
# the token count do not. The tip is chosen once and stays up.
import importlib.util
import random
import sys
from pathlib import Path

from thinking_template import run


def load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        sys.stderr.write(f"thinking: {path}: could not load\n")
        raise SystemExit(1)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    render = getattr(module, "render", None)
    interval = getattr(module, "INTERVAL", None)
    if not callable(render) or not isinstance(interval, (int, float)):
        sys.stderr.write(f"thinking: {path.name}: render and INTERVAL are expected\n")
        raise SystemExit(1)
    return render, interval


def scripts():
    here = Path(__file__).resolve().parent
    found = sorted(here.glob("spinning_*.py"))
    if not found:
        sys.stderr.write("thinking: no spinners\n")
        raise SystemExit(1)
    return [load(path) for path in found]


class Roster:
    """One renderer at a time. A new status line picks a different script."""

    def __init__(self, renderers):
        self.renderers = renderers
        self.index = random.randrange(len(renderers))
        self.label = None

    def interval(self):
        return self.renderers[self.index][1]

    def render(self, elapsed, label):
        if self.label is not None and label != self.label:
            self._next()
        self.label = label
        paint, _interval = self.renderers[self.index]
        return paint(elapsed, label)

    def _next(self):
        count = len(self.renderers)
        if count < 2:
            return
        pick = random.randrange(count - 1)
        if pick >= self.index:
            pick += 1
        self.index = pick


def main():
    roster = Roster(scripts())
    run(roster.render, roster.interval)


if __name__ == "__main__":
    main()
