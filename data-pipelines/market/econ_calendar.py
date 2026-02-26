#!/usr/bin/env python3
"""Fetch Yahoo Finance Economic Calendar and publish to S3.

Scrapes today's economic releases from Yahoo Finance (no JS rendering needed).
Runs every 4 hours on weekdays; writes s3://monkcode-market-data/data/econ_calendar.json
"""
import json
import os
from datetime import datetime, timezone

import boto3
import requests
from bs4 import BeautifulSoup

BUCKET = os.getenv("PUBLIC_BUCKET", "monkcode-market-data")
KEY = "data/econ_calendar.json"
URL = "https://finance.yahoo.com/calendar/economic"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

# Column indices in Yahoo Finance economic calendar table
# Event | Country | Event Time | For | Actual | Market Expectation | Prior to This | Revised from
COL_EVENT    = 0
COL_COUNTRY  = 1
COL_TIME     = 2
COL_PERIOD   = 3
COL_ACTUAL   = 4
COL_FORECAST = 5
COL_PREVIOUS = 6


def parse_calendar(html: str) -> list:
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    if not table:
        return []

    items = []
    seen = set()
    today = datetime.now(tz=timezone.utc).strftime("%b %-d, %Y")  # e.g. "Feb 25, 2026"

    for row in table.find_all("tr")[1:]:  # skip header row
        cells = [td.get_text(strip=True) for td in row.find_all(["td", "th"])]
        if len(cells) < 4:
            continue

        event    = cells[COL_EVENT]    if len(cells) > COL_EVENT    else ""
        country  = cells[COL_COUNTRY]  if len(cells) > COL_COUNTRY  else ""
        time_val = cells[COL_TIME]     if len(cells) > COL_TIME     else ""
        period   = cells[COL_PERIOD]   if len(cells) > COL_PERIOD   else ""
        actual   = cells[COL_ACTUAL]   if len(cells) > COL_ACTUAL   else ""
        forecast = cells[COL_FORECAST] if len(cells) > COL_FORECAST else ""
        previous = cells[COL_PREVIOUS] if len(cells) > COL_PREVIOUS else ""

        if not event:
            continue

        key = f"{time_val}|{event}|{country}"
        if key in seen:
            continue
        seen.add(key)

        # Format: "8:30 AM UTC (US)" for display
        time_display = f"{time_val} ({country})" if country else time_val

        items.append({
            "date":     today,
            "time":     time_display,
            "event":    event,
            "period":   period,
            "forecast": forecast if forecast not in ("-", "") else "",
            "previous": previous if previous not in ("-", "") else "",
            "actual":   actual   if actual   not in ("-", "") else "",
        })

    return items[:100]


def main():
    resp = requests.get(URL, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    items = parse_calendar(resp.text)

    payload = {
        "fetched_at": datetime.now(tz=timezone.utc).replace(microsecond=0).isoformat(),
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
