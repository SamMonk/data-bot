#!/usr/bin/env python3
"""Fetch MarketWatch Economic Calendar and publish to S3.

Uses Playwright (headless Chromium) to render the JavaScript-heavy page,
then extracts structured calendar data directly from the live DOM.

Runs every 4 hours on weekdays; writes s3://monkcode-market-data/data/econ_calendar.json
"""
import json
import os
from datetime import datetime, timezone

import boto3
from playwright.sync_api import sync_playwright

BUCKET = os.getenv("PUBLIC_BUCKET", "monkcode-market-data")
KEY = "data/econ_calendar.json"
URL = "https://www.marketwatch.com/economy-politics/calendar"


def fetch_calendar_items() -> list:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            user_agent=(
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
            )
        )
        page.goto(URL, wait_until="domcontentloaded", timeout=30000)

        # Wait for calendar tables to appear after JS renders
        try:
            page.wait_for_selector("table", timeout=15000)
        except Exception:
            pass

        # Dismiss cookie/consent overlay if present
        for selector in ["button[id*='consent']", "button[class*='consent']",
                          "button[id*='accept']", ".gdpr-accept"]:
            try:
                page.click(selector, timeout=1500)
                break
            except Exception:
                pass

        # Extract structured data from the live DOM via JS
        items = page.evaluate("""() => {
            const results = [];
            let currentDate = "";
            const dateRe = /(monday|tuesday|wednesday|thursday|friday|saturday|sunday)/i;
            const skipWords = new Set(["time", "report", "date", "period",
                                        "survey", "actual", "prior", "revised", ""]);

            // Walk all elements in document order to track date headers + tables
            const walker = document.createTreeWalker(
                document.body,
                NodeFilter.SHOW_ELEMENT,
                null
            );

            let node = walker.nextNode();
            while (node) {
                const tag = node.tagName;

                // Capture date section headers (h2/h3/h4 containing day-of-week)
                if (/^H[1-4]$/.test(tag)) {
                    const text = (node.innerText || node.textContent || "").trim();
                    if (dateRe.test(text)) {
                        currentDate = text;
                    }

                // Parse calendar tables
                } else if (tag === "TABLE") {
                    const rows = node.querySelectorAll("tr");
                    for (const row of rows) {
                        const cells = Array.from(row.querySelectorAll("td, th"))
                            .map(c => (c.innerText || c.textContent || "")
                                       .replace(/\\s+/g, " ").trim());

                        if (cells.length < 2) continue;

                        // Skip header rows
                        if (skipWords.has(cells[0].toLowerCase())) continue;

                        const event = cells[1] || "";
                        if (!event || !/[A-Za-z]/.test(event)) continue;

                        results.push({
                            date:     currentDate,
                            time:     cells[0] || "",
                            event:    cells[1] || "",
                            period:   cells[2] || "",
                            forecast: cells[3] || "",
                            previous: cells[5] || "",
                        });
                    }
                }

                node = walker.nextNode();
            }

            return results.slice(0, 200);
        }""")

        browser.close()
    return items


def main():
    items = fetch_calendar_items()

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
