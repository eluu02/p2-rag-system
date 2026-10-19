"""Download the English Ask CFPB answer pages into ../p2-raw for `p2 ingest`.

CFPB content is public domain: "Information created by the CFPB is in the public domain and you may
reproduce, publish, or otherwise use it without the Bureau's permission."
(https://www.consumerfinance.gov/privacy/website-privacy-policy/)

Each page is saved as <slug>.html, so ingest can rebuild its address with
--source "https://www.consumerfinance.gov/ask-cfpb/{stem}/".

Usage, from the repo root: uv run python scripts/fetch_cfpb.py [OUT_DIR]   (default ../p2-raw)
(the python.org macOS Python has no CA certificates, so plain python3 can fail with CERTIFICATE_VERIFY_FAILED)
"""

import re
import sys
import time
import urllib.request
from pathlib import Path

SITEMAP = "https://www.consumerfinance.gov/sitemap.xml"
ANSWER = re.compile(r"<loc>(https://www\.consumerfinance\.gov/ask-cfpb/([a-z0-9-]+-en-\d+)/)</loc>")
# the site answers 403 to a request without the Accept headers a browser sends
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "text/html,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}
DELAY = 1.0  # seconds between requests, to be polite to the site


def get(url: str) -> str:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def main() -> None:
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "../p2-raw")
    out.mkdir(parents=True, exist_ok=True)
    answers = sorted(set(ANSWER.findall(get(SITEMAP))))
    print(f"{len(answers)} English answer pages in the sitemap")
    fetched = skipped = failed = 0
    for url, slug in answers:
        dest = out / f"{slug}.html"
        if dest.exists():
            skipped += 1
            continue
        try:
            dest.write_text(get(url), encoding="utf-8", newline="\n")
            fetched += 1
        except Exception as exc:  # keep going; a rerun retries only the missing pages
            print(f"FAILED {url}: {exc}")
            failed += 1
        time.sleep(DELAY)
    print(f"fetched {fetched}, already there {skipped}, failed {failed} -> {out}")


if __name__ == "__main__":
    main()
