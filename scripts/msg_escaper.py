import argparse
import json
from pathlib import Path
from typing import List

'''
python3 scripts/msg_escaper.py scripts/scams.txt --json -o backend/data/seed_scams.json
'''

DELIMITER = "--------------------"

def normalize_newlines(msg: str) -> str:
    """Ensure messages use LF newlines only."""
    return msg.replace("\r\n", "\n")


def escape_message(msg: str) -> str:
    """Return JSON-safe string with newline escapes for seeding."""
    normalized = normalize_newlines(msg)
    return normalized.replace("\n", r"\n")


def split_messages(raw_text: str, delimiter: str = DELIMITER) -> List[str]:
    """Split a text blob into messages separated by a delimiter line."""
    parts = []
    current = []
    for line in raw_text.splitlines():
        if line.strip() == delimiter:
            chunk = "\n".join(current).strip()
            if chunk:
                parts.append(chunk)
            current = []
        else:
            current.append(line)
    chunk = "\n".join(current).strip()
    if chunk:
        parts.append(chunk)
    return parts or [raw_text.strip()]


def to_seed_json(messages: List[str]) -> str:
    entries = [{"text": normalize_newlines(m)} for m in messages]
    return json.dumps(entries, ensure_ascii=False, indent=2)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Escape raw SMS text for use in backend/data/seed_scams.json. "
            f"Separate multiple messages with a line containing {DELIMITER!r}."
        ),
    )
    parser.add_argument(
        "input",
        help="Path to a text file containing the raw message(s). Use '-' to read from stdin.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Wrap the escaped text in the seed JSON structure.",
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Optional path to write the escaped result (prints to stdout if omitted).",
    )
    parser.add_argument(
        "--delimiter",
        default=DELIMITER,
        help=f"Custom delimiter line (default: {DELIMITER!r}).",
    )
    args = parser.parse_args()

    raw_text = Path(args.input).read_text() if args.input != "-" else Path("/dev/stdin").read_text()
    messages = split_messages(raw_text, delimiter=args.delimiter)

    if args.json:
        result = to_seed_json(messages)
    else:
        result = "\n\n".join(escape_message(m) for m in messages)

    if args.output:
        Path(args.output).write_text(result)
    else:
        print(result)

if __name__ == "__main__":
    main()
