"""Validate and assemble the editable PNG frames into a local v2 pet package."""

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
CELL = (192, 208)
SIZE = (1536, 2288)
COUNTS = [6, 8, 8, 4, 5, 8, 6, 6, 6, 8, 8]


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def assemble():
    spec = json.loads((ROOT / "source/frames.json").read_text(encoding="utf-8"))
    rows = spec["rows"]
    if [len(row["frames"]) for row in rows] != COUNTS:
        raise ValueError("Frame counts do not match the v2 contract.")
    atlas = Image.new("RGBA", SIZE)
    seen = set()
    for row_index, row in enumerate(rows):
        for column, relative in enumerate(row["frames"]):
            path = (ROOT / "source" / relative).resolve()
            if not path.is_relative_to((ROOT / "source/frames").resolve()):
                raise ValueError("Frame path escapes source/frames.")
            if path in seen:
                raise ValueError("Duplicate source frame path.")
            seen.add(path)
            with Image.open(path) as image:
                if image.size != CELL or image.mode != "RGBA":
                    raise ValueError(f"Expected 192x208 RGBA: {relative}")
                alpha = image.getchannel("A")
                bounds = alpha.point(lambda value: 255 if value > 16 else 0).getbbox()
                if bounds is None or alpha.getextrema()[0] != 0:
                    raise ValueError(f"Empty frame or missing transparency: {relative}")
                if bounds[0] == 0 or bounds[1] == 0 or bounds[2] == CELL[0] or bounds[3] == CELL[1]:
                    raise ValueError(f"Visible artwork touches a cell edge: {relative}")
                atlas.paste(image, (column * CELL[0], row_index * CELL[1]))
    return atlas


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check sources against the released atlas and hashes.")
    parser.add_argument("--output", type=Path, help="Write a new local pet package to this directory.")
    args = parser.parse_args()
    if not args.check and args.output is None:
        parser.error("Specify --check, --output, or both.")
    atlas = assemble()
    metadata = json.loads((ROOT / "pet.json").read_text(encoding="utf-8"))
    if metadata.get("id") != "ai-companion-trio" or metadata.get("spriteVersionNumber") != 2:
        raise ValueError("Unexpected pet manifest ID or sprite version.")
    if metadata.get("spritesheetPath") != "spritesheet.webp":
        raise ValueError("Unexpected sprite path.")
    report = {"ok": True, "frames": sum(COUNTS), "atlas_size": list(SIZE)}
    if args.check:
        released = ROOT / "spritesheet.webp"
        with Image.open(released) as image:
            if image.size != SIZE or image.convert("RGBA").tobytes() != atlas.tobytes():
                raise ValueError("Released atlas pixels differ from the editable source frames.")
        for line in (ROOT / "SHA256SUMS").read_text(encoding="ascii").splitlines():
            expected, relative = line.split("  ", 1)
            path = (ROOT / relative).resolve()
            if not path.is_relative_to(ROOT) or sha256(path) != expected:
                raise ValueError(f"Release hash mismatch: {relative}")
        report.update(release_rgba_matches=True, release_sha256=sha256(released))
    if args.output is not None:
        output = args.output.resolve()
        targets = [output / "pet.json", output / "spritesheet.webp"]
        if any(path.exists() for path in targets):
            raise ValueError("Output package already exists; choose a new directory.")
        output.mkdir(parents=True, exist_ok=True)
        atlas.save(targets[1], format="WEBP", lossless=True, quality=100, method=6, exact=True)
        with Image.open(targets[1]) as image:
            if image.convert("RGBA").tobytes() != atlas.tobytes():
                raise ValueError("Encoded output did not preserve source pixels.")
        targets[0].write_text(json.dumps(metadata, indent=2, ensure_ascii=True) + "\n", encoding="utf-8", newline="\n")
        report.update(build_rgba_matches=True, built_sha256=sha256(targets[1]))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
