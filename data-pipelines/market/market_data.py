import json
import os
import time
from datetime import datetime, timedelta

import boto3
import yfinance as yf
from botocore.exceptions import ClientError

PUBLIC_BUCKET = os.getenv("PUBLIC_BUCKET", "monkcode-market-data")
MARKET_KEY = "data/market_indicators.json"
FUNDS_KEY = "data/funds_performance.json"

# Safety margins
BOOTSTRAP_LOOKBACK_DAYS = int(os.getenv("BOOTSTRAP_LOOKBACK_DAYS", "365"))
SAFETY_LOOKBACK_DAYS = int(os.getenv("SAFETY_LOOKBACK_DAYS", "5"))
SLEEP_SECONDS = float(os.getenv("SLEEP_SECONDS", "1.5"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))

s3 = boto3.client("s3")

market_tickers = {
    "DOW": "^DJI",
    "S&P 500": "^GSPC",
    "Crude Oil": "CL=F",
    "Gold": "GC=F",
    "Bitcoin": "BTC-USD",
    "10Y T-Note": "^TNX",
}

funds = [
    "FZIPX", "FSUTX", "FSSNX", "FSPTX", "FSCSX", "FNILX",
    "FDCPX", "FBCVX", "FAMRX", "DGRO", "VIG", "SCHD"
]

def get_s3_json(bucket, key, default=None):
    try:
        resp = s3.get_object(Bucket=bucket, Key=key)
        return json.loads(resp["Body"].read().decode("utf-8"))
    except ClientError as e:
        if e.response["Error"]["Code"] in ("NoSuchKey", "404"):
            return default
        raise

def put_s3_json(bucket, key, payload):
    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=json.dumps(payload),
        ContentType="application/json",
    )

def max_date_in_history(history_dict):
    if not history_dict:
        return None
    # keys are 'YYYY-MM-DD'
    return max(history_dict.keys())

def parse_date(dstr):
    return datetime.strptime(dstr, "%Y-%m-%d").date()

def format_date(dt):
    return dt.strftime("%Y-%m-%d")

def fetch_with_retry(symbol, start_date, interval="1d"):
    # yfinance sometimes errors transiently; retry with backoff.
    last_exc = None
    for i in range(MAX_RETRIES):
        try:
            ticker = yf.Ticker(symbol)
            if start_date:
                hist = ticker.history(start=start_date, interval=interval)  # end=now implicit
            else:
                hist = ticker.history(period=f"{BOOTSTRAP_LOOKBACK_DAYS}d", interval=interval)
            if hist is None or hist.empty:
                return None
            hist = hist[["Close"]].dropna()
            hist.index = hist.index.tz_localize(None) if hasattr(hist.index, "tzinfo") else hist.index
            # Normalize to YYYY-MM-DD keys
            hist.index = [ts.strftime("%Y-%m-%d") for ts in hist.index]
            return hist["Close"].to_dict()
        except Exception as e:
            last_exc = e
            time.sleep(SLEEP_SECONDS * (2 ** i))
    # If we got here, all retries failed
    raise last_exc

def merge_histories(existing, incoming):
    if not existing:
        return dict(incoming) if incoming else {}
    if not incoming:
        return existing
    merged = dict(existing)
    merged.update(incoming)  # incoming overwrites same-date stale values
    return merged

def update_dataset(ticker_map, existing_payload):
    # existing_payload: {"timestamp": ..., "data": { name: {symbol, last_close, history} } }
    if not existing_payload:
        existing_payload = {"timestamp": None, "data": {}}

    updated = {"timestamp": datetime.utcnow().isoformat(), "data": {}}

    for name, symbol in ticker_map.items():
        prev = existing_payload["data"].get(name, {})
        prev_history = prev.get("history", {})
        last_date_str = max_date_in_history(prev_history)
        start_date = None

        if last_date_str:
            # Start a few days before the last date to cover weekends/holidays/bad bars.
            start_date = format_date(parse_date(last_date_str) - timedelta(days=SAFETY_LOOKBACK_DAYS))
        else:
            # First run: fetch a modest window to avoid heavy pulls
            start_date = None  # handled inside fetch_with_retry -> BOOTSTRAP_LOOKBACK_DAYS

        time.sleep(SLEEP_SECONDS)
        new_hist = fetch_with_retry(symbol, start_date=start_date, interval="1d")

        merged_history = merge_histories(prev_history, new_hist or {})
        last_close = round(float(merged_history[max(merged_history.keys())]), 2) if merged_history else None

        updated["data"][name] = {
            "symbol": symbol,
            "last_close": last_close,
            "history": merged_history,
        }

    return updated

def main():
    # Markets
    existing_market = get_s3_json(PUBLIC_BUCKET, MARKET_KEY, default=None)
    market_updated = update_dataset(market_tickers, existing_market)
    put_s3_json(PUBLIC_BUCKET, MARKET_KEY, market_updated)

    # Funds (symbol == name)
    fund_map = {f: f for f in funds}
    existing_funds = get_s3_json(PUBLIC_BUCKET, FUNDS_KEY, default=None)
    funds_updated = update_dataset(fund_map, existing_funds)
    put_s3_json(PUBLIC_BUCKET, FUNDS_KEY, funds_updated)

if __name__ == "__main__":
    main()
