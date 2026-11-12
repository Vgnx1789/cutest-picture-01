"""Write this entry's picture to the output path.

The repository holds the picture as entry.png next to this script; the
program simply copies it to where the grader expects it: the entry.png
inside $MAKEFUN_OUTPUT_DIR when that is set, else /output/entry.png.
Copying the same file every run keeps both graded runs byte-identical.
"""

import os
import shutil
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "entry.png"
MAX_BYTES = 1_048_576  # the competition's 1 MiB cap
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
JPEG_SIGNATURE = b"\xff\xd8"


def check_source(data: bytes) -> None:
    """Fail loudly rather than write an entry the gate would refuse:
    over the byte cap, neither PNG nor JPEG, or a truncated file."""
    if len(data) > MAX_BYTES:
        raise SystemExit(f"entry.png is {len(data)} bytes, over the 1 MiB limit")
    if data.startswith(PNG_SIGNATURE):
        if b"IEND" not in data[-16:]:
            raise SystemExit("entry.png looks like a truncated PNG (no IEND)")
    elif data.startswith(JPEG_SIGNATURE):
        if not data.rstrip().endswith(b"\xff\xd9"):
            raise SystemExit("entry.png looks like a truncated JPEG (no EOI)")
    else:
        raise SystemExit("entry.png is neither a PNG nor a JPEG")


def output_path() -> Path:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return Path(out_dir) / "entry.png"


def main() -> None:
    check_source(SOURCE.read_bytes())
    dest = output_path()
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, dest)


if __name__ == "__main__":
    main()
