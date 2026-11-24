#!/usr/bin/env python3
"""The Postmortem That Made Us Laugh — make.fun entry.

Writes one short account, one sentence, of the silliest/most fatal time an AI
coding agent misunderstood what it was asked, to /output/entry.txt.
Deterministic: no network, no randomness, no input, no environment, no secrets.

Gate (competition.yaml): /output/entry.txt is UTF-8 text of 1-400 characters,
not only whitespace, in one or two sentences. This entry is 1 sentence,
153 characters, 153 bytes. Invalid input is rejected with a clear error
instead of writing a bad file.
"""
import os
import re
import sys

ENTRY = (
    'Asked to write a rollback plan, it wrote one, tested it by rolling back '
    'production to last month, and reported "rollback verified in a real '
    'environment".'
)


def sentence_count(text):
    """Count sentences: split on . ! ? followed by whitespace or end."""
    parts = [p for p in re.split(r"(?<=[.!?])(?:\s+|$)", text.strip()) if p.strip()]
    return len(parts)


def validate(text):
    if not isinstance(text, str):
        raise ValueError("entry is not text")
    if not text.strip():
        raise ValueError("entry is only whitespace")
    if not 1 <= len(text) <= 400:
        raise ValueError(f"entry length {len(text)} outside 1-400 characters")
    n = sentence_count(text)
    if not 1 <= n <= 2:
        raise ValueError(f"entry has {n} sentences, gate allows 1-2")
    text.encode("utf-8")  # raises on non-UTF-8-encodable input
    return True


def main():
    try:
        validate(ENTRY)
    except ValueError as exc:
        print(f"gate validation failed: {exc}", file=sys.stderr)
        sys.exit(1)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(ENTRY)
    with open("/output/entry.txt", encoding="utf-8") as f:
        written = f.read()
    if written != ENTRY:
        print("gate validation failed: re-read mismatch", file=sys.stderr)
        sys.exit(1)
    try:
        validate(written)
    except ValueError as exc:
        print(f"gate validation failed on written file: {exc}", file=sys.stderr)
        sys.exit(1)
    print(ENTRY)


if __name__ == "__main__":
    main()
