#!/usr/bin/env python3
"""Name the robot band, then hand the name to the grader.

The competition wants one funny line: a robot band's name plus a few
words about its hit song, squeezed under 200 characters. This program
keeps that line in BAND_LINE, refuses to ship it unless it clears the
gate, and then writes it out exactly as written — no trailing newline,
world-readable, so the grader can open it as any user.

The band is named after the problem, not after a robot part: the
Wi-Fi dead zones. Its single streamed 40 million times, every one of
those plays coming from the hallway, because the band is famous but
never actually makes it into the room. That is the whole joke — a
famous band that only ever plays the hallway.

Layout note: main() sits up top so the flow reads first and the
mechanics live underneath it. Nothing below this docstring edits the
entry text; the gate only ever says yes or no.
"""

import os

BAND_LINE = "The Wi-Fi Dead Zones — hit single 'Can You Hear Me Now?' streamed 40 million times, all of it from the hallway."

MIN_CHARS = 1
MAX_CHARS = 200
DIR_ENV = "MAKEFUN_OUTPUT_DIR"
DIR_FALLBACK = "/output"
FILE_NAME = "entry.txt"
FILE_MODE = 0o644


def main():
    """Validate the band line, then write it to the graded file."""
    verdict, length = inspect(BAND_LINE)
    if verdict is not None:
        raise SystemExit(f"entry rejected: {verdict}")
    store(BAND_LINE, length)


def inspect(text):
    """Return (problem, length): problem is None when the line passes.

    The gate is one line, 1-200 characters, with something in it. A
    blank line, a hidden line break, or a length outside the window
    all come back as a plain-English reason instead of a crash.
    """
    if not text.strip():
        return "band line is empty", 0
    for mark in ("\n", "\r"):
        if mark in text:
            return "band line must fit on one line", 0
    length = len(text)
    if length < MIN_CHARS or length > MAX_CHARS:
        return (
            f"band line is {length} characters, "
            f"allowed range is {MIN_CHARS}-{MAX_CHARS}"
        ), length
    return None, length


def store(text, length):
    """Write the line verbatim and echo it for the run log."""
    folder = os.environ.get(DIR_ENV, DIR_FALLBACK)
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, FILE_NAME)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    # The grader reads this file as another user, so it must be
    # world-readable; a private file would fail as "not readable".
    os.chmod(path, FILE_MODE)
    print(text)
    print(f"({length} characters)")


if __name__ == "__main__":
    main()
