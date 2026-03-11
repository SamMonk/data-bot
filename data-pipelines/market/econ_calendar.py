#!/usr/bin/env python3
"""Fetch economic calendar from ForexFactory CDN and publish to S3.

Uses the ForexFactory CDN mirror (no auth required, no Cloudflare).
Filters to USD events only and normalises output to match the previous
MarketWatch-based schema so downstream consumers don't break.

Runs every 4 hours on weekdays; writes s3://monkcode-market-data/data/econ_calendar.json
"""
import json
import os
from datetime import datetime, timezone

import boto3
import requests

BUCKET = os.getenv("PUBLIC_BUCKET", "monkcode-market-data")
KEY = "data/econ_calendar.json"
FF_URL = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"

IMPACT_MAP = {"High": 3, "Medium": 2, "Low": 1, "Holiday": 0}


def fetch_calendar() -> list:
    resp = requests.get(
        FF_URL,
        headers={"User-Agent": "data-bot/1.0", "Accept": "application/json"},
        timeout=15,
    )
    resp.raise_for_status()
    raw = resp.json()

    items = []
    for event in raw:
        if event.get("country") != "USD":
            continue
        impact = event.get("impact", "")
        if impact == "Holiday":
            continue

        raw_date = event.get("date", "")
        try:
            dt = datetime.fromisoformat(raw_date)
            date_str = dt.strftime("%A, %b. %d").upper()
            time_str = dt.strftime("%-I:%M%p").lower()
        except ValueError:
            date_str = raw_date
            time_str = ""

        items.append({
            "date": date_str,
            "time": time_str,
            "event": event.get("title", ""),
            "period": "",
            "actual": "",
            "forecast": event.get("forecast", ""),
            "previous": event.get("previous", ""),
        })

    return items


def main():
    items = fetch_calendar()

    payload = {
        "fetched_at": datetime.now(tz=timezone.utc).replace(microsecond=0).isoformat(),
        "source_url": FF_URL,
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
