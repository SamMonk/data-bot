#!/usr/bin/env python3
"""Fetch Yahoo Finance Originals articles and publish to S3.

Runs daily; writes s3://monkcode-market-data/data/yahoo_originals.json
"""
import json
import os
import re
from datetime import datetime, timezone

import boto3
import requests

BUCKET = os.getenv("PUBLIC_BUCKET", "monkcode-market-data")
KEY = "data/yahoo_originals.json"
URL = "https://finance.yahoo.com/topic/yahoo-finance-originals/"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

_strip = re.compile(r"<[^>]+>")
_space = re.compile(r"\s+")
_anchor = re.compile(
    r'<a[^>]+href="(https?://finance\.yahoo\.com/news/[^"#?]+)"[^>]*>([\s\S]*?)</a>',
    re.IGNORECASE,
)
_h3 = re.compile(r"<h3[^>]*>([\s\S]*?)</h3>", re.IGNORECASE)
_img = re.compile(r'<img[^>]+src="(https?://[^"]+)"', re.IGNORECASE)


def parse_articles(html: str) -> list:
    articles = []
    seen = set()
    for m in _anchor.finditer(html):
        if len(articles) >= 20:
            break
        link = m.group(1)
        inner = m.group(2) or ""
        h3 = _h3.search(inner)
        raw = h3.group(1) if h3 else inner
        title = _space.sub(" ", _strip.sub(" ", raw)).strip()
        img_m = _img.search(inner)
        image = img_m.group(1) if img_m else ""
        if title and len(title) > 10 and link not in seen:
            seen.add(link)
            articles.append({"title": title, "link": link, "image": image})
    return articles


def main():
    resp = requests.get(URL, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    articles = parse_articles(resp.text)

    payload = {
        "fetched_at": datetime.now(tz=timezone.utc).replace(microsecond=0).isoformat(),
        "articles": articles,
    }

    boto3.client("s3").put_object(
        Bucket=BUCKET,
        Key=KEY,
        Body=json.dumps(payload),
        ContentType="application/json",
    )
    print(f"Wrote {len(articles)} articles → s3://{BUCKET}/{KEY}")


if __name__ == "__main__":
    main()
