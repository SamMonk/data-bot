#!/usr/bin/env python3
"""Fetch MarketWatch Economic Calendar and publish to S3.

Uses cloudscraper to bypass Cloudflare protection; parses multi-week
calendar tables into structured events tagged with date headers.

Runs every 4 hours on weekdays; writes s3://monkcode-market-data/data/econ_calendar.json
"""
import json
import os
import re
from datetime import datetime, timezone

import boto3
import cloudscraper
from bs4 import BeautifulSoup

BUCKET = os.getenv("PUBLIC_BUCKET", "monkcode-market-data")
KEY = "data/econ_calendar.json"
URL = "https://www.marketwatch.com/economy-politics/calendar"

# Matches date header rows like "MONDAY, FEB. 23" or "FRIDAY, MARCH 6"
_DAY_RE = re.compile(
    r"^(MONDAY|TUESDAY|WEDNESDAY|THURSDAY|FRIDAY|SATURDAY|SUNDAY)",
    re.IGNORECASE,
)
# Parses "FEB. 26" → month + day for sorting
_MDY_RE = re.compile(
    r"(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)[A-Z.]*\s+(\d+)",
    re.IGNORECASE,
)
_MONTHS = {m: i for i, m in enumerate(
    ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"], 1
)}


def _date_sort_key(date_str: str) -> tuple:
    """Return (month, day) for sorting date header strings."""
    m = _MDY_RE.search(date_str)
    if not m:
        return (99, 99)
    month = _MONTHS.get(m.group(1).lower(), 99)
    return (month, int(m.group(2)))


def parse_calendar(html: str) -> list:
    soup = BeautifulSoup(html, "html.parser")
    items = []
    seen = set()
    current_date = ""

    for table in soup.find_all("table"):
        for row in table.find_all("tr"):
            cells = [
                td.get_text(separator=" ", strip=True)
                for td in row.find_all(["td", "th"])
            ]
            if not cells:
                continue

            first = cells[0]

            # Skip column-header rows
            if first.lower() in ("time (et)", "time"):
                continue

            # Date section header row (e.g. "THURSDAY, FEB. 26")
            if _DAY_RE.match(first):
                current_date = first
                continue

            if len(cells) < 2 or not current_date:
                continue

            event    = cells[1] if len(cells) > 1 else ""
            if not event:
                continue

            time_val = first
            period   = cells[2] if len(cells) > 2 else ""
            actual   = cells[3] if len(cells) > 3 else ""
            forecast = cells[4] if len(cells) > 4 else ""
            previous = cells[5] if len(cells) > 5 else ""

            key = f"{current_date}|{time_val}|{event}"
            if key in seen:
                continue
            seen.add(key)

            items.append({
                "date":     current_date,
                "time":     time_val,
                "event":    event,
                "period":   period,
                "actual":   actual,
                "forecast": forecast,
                "previous": previous,
            })

    return items


def main():
    scraper = cloudscraper.create_scraper(
        browser={"browser": "chrome", "platform": "linux", "desktop": True}
    )
    resp = scraper.get(URL, timeout=30)
    resp.raise_for_status()
    items = parse_calendar(resp.text)

    payload = {
        "fetched_at": datetime.now(tz=timezone.utc).replace(microsecond=0).isoformat(),
        "source_url": URL,
        "items": items,
    }

    boto3.client("s3").put_object(
        Bucket=BUCKET,
        Key=KEY,
        Body=json.dumps(payload),
        ContentType="application/json",
    )
    print(f"Wrote {len(items)} calendar items → s3://{BUCKET}/{KEY}")


if __name__ == "__main__":
    main()
