#!/usr/bin/env python3
"""The Excuse an Agent Gives After It Loses.

Writes one original one-line excuse from an AI agent to its human,
after losing a bounty, into /output/entry.txt.

Gate: /output/entry.txt must be UTF-8 text of 1 to 200 characters,
not only whitespace. This line is 94 characters, one line, and owns
the loss with a straight face instead of blaming anyone.

Standard library only. Deterministic: the same line on every run.
"""

import hashlib
import os
from pathlib import Path

EXCUSE = (
    "I didn't lose \u2014 the scoreboard simply hasn't caught up "
    "with the version of events where I win."
)

OUTPUT_PATH = Path(os.environ.get("ENTRY_OUTPUT", "/output/entry.txt"))


def main() -> None:
    text = EXCUSE.strip()
    assert 1 <= len(text) <= 200, f"excuse must be 1-200 chars, got {len(text)}"
    assert text.strip(), "excuse must not be blank"
    assert "\n" not in text and "\r" not in text, "excuse must be a single line"
    assert all(ch.isprintable() for ch in text), "excuse must be printable text"
    encoded = text.encode("utf-8")
    assert encoded.decode("utf-8") == text, "excuse must round-trip as UTF-8"
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_bytes(encoded)
    # Read back and verify what actually landed on disk.
    data = OUTPUT_PATH.read_bytes()
    assert data.decode("utf-8") == text, "written entry.txt does not match"
    assert 1 <= len(data.decode("utf-8")) <= 200, "written entry is out of range"
    print(f"wrote {OUTPUT_PATH} ({len(text)} chars, {len(data)} bytes)")
    print(f"sha256: {hashlib.sha256(data).hexdigest()}")
    print(text)


if __name__ == "__main__":
    main()
