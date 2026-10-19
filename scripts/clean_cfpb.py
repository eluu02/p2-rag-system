"""Strip the consumerfinance.gov page text that trafilatura left in the Ask CFPB documents.

Three patterns, none of them part of an answer:
- the "Page last modified <date> @ <time>" line at the end of a page
- the stray search-box hint "Searches are limited to 75 characters."
- the " | Consumer Financial Protection Bureau" suffix on a title (in the document and in manifest.tsv)

Usage, from the repo root: uv run python scripts/clean_cfpb.py
Then `uv run p2 ingest --report` rewrites corpora/own/INGEST.md with the new word counts.
It is safe to run twice.
"""

import re
from pathlib import Path

OWN = Path("corpora/own")
SUFFIX = " | Consumer Financial Protection Bureau"
DROP = re.compile(r"^(Page last modified\b.*|Searches are limited to 75 characters\.)$")


def clean_doc(text: str) -> str:
    lines = text.split("\n")
    if lines[0].endswith(SUFFIX):
        lines[0] = lines[0][: -len(SUFFIX)]
    kept = [line for line in lines if not DROP.match(line.strip())]
    body = "\n".join(kept)
    body = re.sub(r"\n{3,}", "\n\n", body)  # a dropped line can leave a double gap
    return body.rstrip("\n") + "\n"


def main() -> None:
    changed = 0
    for path in sorted((OWN / "docs").glob("*.md")):
        old = path.read_text(encoding="utf-8")
        new = clean_doc(old)
        if new != old:
            path.write_text(new, encoding="utf-8", newline="\n")
            changed += 1

    # plain line edits, so every other byte of the manifest stays as ingest wrote it
    manifest = OWN / "manifest.tsv"
    lines = manifest.read_text(encoding="utf-8").split("\n")
    titles = 0
    for i, line in enumerate(lines[1:], start=1):
        cells = line.split("\t")
        if len(cells) > 1 and cells[1].endswith(SUFFIX):
            cells[1] = cells[1][: -len(SUFFIX)]
            lines[i] = "\t".join(cells)
            titles += 1
    tmp = manifest.with_suffix(".tsv.tmp")  # write in full, then swap, so a crash cannot truncate it
    tmp.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    tmp.replace(manifest)

    print(f"cleaned {changed} documents and {titles} manifest titles")


if __name__ == "__main__":
    main()
