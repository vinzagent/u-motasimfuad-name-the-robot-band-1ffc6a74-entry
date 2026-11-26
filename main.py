#!/usr/bin/env python3
"""Deliver the robot band name entry for make.fun.

The competition asks for one funny name for a band made of robots,
plus a few words on the band's hit song, all in under 200 characters.
This script is deliberately tiny: it keeps the entry in one place,
checks it against the competition's gate before doing anything else,
and only then drops it into the output file the grader reads.

Why the checks run first: a line that is too long, empty, or split
across two lines would be judged against the wrong text, or not
judged at all. Failing loudly here is cheaper than discovering the
problem after the entry has already been shipped.

The entry itself is 111 characters long. The band is not named after
a robot part — it is named after the problem: the Wi-Fi dead zones.
Its hit single streamed 40 million times, all of it from the hallway,
because the band is famous but never actually makes it into the room.
"""

import os
import sys

# ---------------------------------------------------------------------------
# The submission. This exact string is what the judges score, so it must
# not be edited, re-wrapped, or reworded by any refactor of this file.
# ---------------------------------------------------------------------------
LINE = (
    "The Wi-Fi Dead Zones — hit single 'Can You Hear Me Now?' streamed 40 million times, all of it from the hallway."
)

# Competition gate: the entry has to be one line of 1 to 200 chars.
FLOOR = 1
CEILING = 200

# Where the graded file lands. Overridable for local runs.
OUTPUT_ENV_VAR = "MAKEFUN_OUTPUT_DIR"
DEFAULT_OUTPUT_DIR = "/output"
OUTPUT_FILENAME = "entry.txt"
OUTPUT_MODE = 0o644


def count_characters(line):
    """Return how many characters the entry holds (111 for this entry)."""
    return len(line)


def fail(message):
    """Abort the run with a clear reason instead of shipping bad output."""
    raise SystemExit(f"entry rejected: {message}")


def check_not_empty(line):
    """The entry must say something; a blank line is not an entry."""
    if not line.strip():
        fail("line is blank")


def check_single_line(line):
    """A one-line entry cannot contain a line break of any kind."""
    if "\n" in line or "\r" in line:
        fail("line must be a single line")


def check_length(line, low, high):
    """The entry must sit inside the competition's character gate."""
    size = count_characters(line)
    if size < low or size > high:
        fail(f"line is {size} characters, outside the {low}-{high} gate")
    return size


def validate_line(line, low=FLOOR, high=CEILING):
    """Run every gate check and return the verified character count."""
    check_not_empty(line)
    check_single_line(line)
    return check_length(line, low, high)


def resolve_output_path():
    """Work out the full path of the file the grader will read."""
    directory = os.environ.get(OUTPUT_ENV_VAR, DEFAULT_OUTPUT_DIR)
    os.makedirs(directory, exist_ok=True)
    return os.path.join(directory, OUTPUT_FILENAME)


def emit(line, size):
    """Write the entry out verbatim, then echo it for the run log."""
    destination = resolve_output_path()
    # The grader opens this file as a different user, so the file has
    # to be world-readable; without that it fails as "not readable".
    with open(destination, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)
    os.chmod(destination, OUTPUT_MODE)
    print(line)
    print(f"({size} characters)")


def run():
    """Validate the entry, then emit it. Nothing is written unchecked."""
    size = validate_line(LINE)
    emit(LINE, size)


if __name__ == "__main__":
    run()
