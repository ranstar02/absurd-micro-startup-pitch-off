#!/usr/bin/env python3
"""Absurd Micro-Startup Pitch-Off — one-sentence pitch writer.

Writes a single pitch line (1-200 characters) to /output/entry.txt
(falling back to ./output/entry.txt when /output is not writable).
Standard library only, deterministic, no network.
"""

import os
import sys

LINE = (
    "A $12/month bookkeeper for lazy agents that reconciles last night's "
    "API spend, flags every hallucinated call, and emails your accountant "
    "a clean expense report before finance asks."
)

MAX_CHARS = 200


def validate(text: str) -> None:
    """Raise ValueError if the pitch breaks the gate rules."""
    if not text:
        raise ValueError("pitch is empty")
    if len(text) > MAX_CHARS:
        raise ValueError(f"pitch is {len(text)} chars, over the {MAX_CHARS} cap")
    text.encode("utf-8")  # must be encodable as UTF-8
    if not text.strip():
        raise ValueError("pitch is only whitespace")
    if text.endswith("\n"):
        raise ValueError("pitch must not end with a newline")


def write_atomic(path: str, text: str) -> None:
    """Write text atomically via a temp file in the same directory."""
    directory = os.path.dirname(path)
    os.makedirs(directory, exist_ok=True)
    tmp_path = path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    os.replace(tmp_path, path)


def main() -> int:
    validate(LINE)
    candidates = ["/output/entry.txt", os.path.join("output", "entry.txt")]
    last_error = None
    for target in candidates:
        try:
            write_atomic(target, LINE)
        except OSError as exc:  # /output not writable here; try the fallback
            last_error = exc
            continue
        print(f"Wrote {len(LINE)} characters to {target}")
        print(LINE)
        return 0
    print(f"error: could not write entry.txt: {last_error}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
