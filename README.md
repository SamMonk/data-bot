# data-bot

## Strategy
- **Mission**: Centralize data acquisition, enrichment, and publishing for all MonkCode properties so each Gatsby site stays fresh without manual exports.
- **Audience/Consumers**: `alphagaldata`, `climate-gatsby`, `gatsby`, `gatsby-investing`, and ad-hoc analyses inside `../scripts`.
- **North-star KPIs**: Successful scheduled runs, freshness of published datasets (<=24h drift for daily feeds), schema stability, and time-to-publish for new pipelines (<2 days).

### Automation & Observability
- Maintain the GitHub Action (`.github/workflows/pythonapp.yml`) as the single orchestrator. Add job-specific logs, dataset manifest checksums, and Slack/SNS notifications for failures.
- Introduce dataset metadata (`datasets/<name>/manifest.json`) describing source URLs, update cadence, and downstream repos; publish a summary artifact for the Gatsby READMEs to reference.
- Add unit/smoke tests for critical scrapers (e.g., Yahoo Finance, Census) and run them before committing refreshed data.

### Pipeline Roadmap
- **Dividends/Markets**: Finish migrating dividend + economic calendar scripts into modular packages consumed by `gatsby-investing`.
- **Climate Metrics**: Stage NOAA/NASA ingestion here (currently in `climate-gatsby/scripts`) and expose a CLI per metric so the Gatsby repo simply pulls committed JSON.
- **Alpha-Gal Map**: Convert the geojson/SQLite workflows into reproducible modules that output to `alphagaldata/src/data/` or S3 for map tiles.
- **Shared Assets**: Store reusable datasets (occupation stats, property records) with clear versioning and checksums so `gatsby` can showcase previews.

### Operations
- **Daily**: Scheduled workflow runs `main.py` to pull priority feeds; ensure idempotency and commit only when data changed.
- **Weekly**: Review pipeline health, update `.env.sample` / secrets guidance, and queue enhancements in this README.
- **Monthly**: Audit dependencies (`pip-tools` or `uv`), refresh API credentials, and archive obsolete datasets.

## Progress Log
- 2025-09-22 — Added data-bot roadmap, clarified ownership of pipelines feeding the four Gatsby sites, and outlined observability upgrades.

## Reference Notes

The data sources for the various monkcode.com sites.

Harvesting data automatically

Start with capturing data from the internet about subjects that matter to us:

I prefer to keep small data sets in json and sqlite for larger datasets. 

I also have some preference for postgres if I need a shared central database with the ability to search spatial data.


#### Geocoding
https://geocoding.geo.census.gov/geocoder/Geocoding_Services_API.html
https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?address=410+Voorhis+Ave+deland+fl&benchmark=9&format=json

# Build DataSets

craigslist and facebook markeplace analysis, marklet research
geojson
s and p stock valuation data

## Products

Name
Description
Price
Location
Photos []

photos should be shrunk and put into the sqlite database
https://stackoverflow.com/questions/9357668/how-to-store-image-in-sqlite-database

Get stocks running main
Populate database running `python wiki_stocks..`
SQLIte query to get CSV
Git push and pull

0 16 * * * /path/to/script.sh

{\displaystyle V^{*}=\mathrm {EPS} \times (8.5+2g)}


{\displaystyle V^{*}={\cfrac {\mathrm {EPS} \times (8.5+2g)\times 4.4}{Y}}}


V^{*} = the value expected from the growth formulas over the next 7 to 10 years
E P S {\displaystyle EPS} = the company’s last 12-month earnings per share
8.5 {\displaystyle 8.5} = P/E base for a no-growth company
g g = reasonably expected 7 to 10 Year Growth Rate of EPS
4.4 {\displaystyle 4.4} = the average yield of AAA corporate bonds in 1962 (Graham did not specify the duration of the bonds, though it has been asserted that he used 20 year AAA bonds as his benchmark for this variable[5])
Y Y = the current yield on AAA corporate bonds.

https://www.oldschoolvalue.com/stock-valuation/benjamin-graham-formula/

{\displaystyle V^{*}={\cfrac {\mathrm {EPS} \times (7+1g)\times 4.4}{Y}}}

=((EPS(7+1g))/(Y))

cd /home/shawnmonk/monk/data-bot
python3 wiki_stocks/get_sp_data.py
aws sns publish --topic-arn "arn:aws:sns:us-east-1:904524340593:tractors" --message "Cron Ran"

Fatal Python error: Py_Initialize: Unable to get the locale encoding
ModuleNotFoundError: No module named 'encodings'

requests.exceptions.JSONDecodeError: Expecting value: line 1 column 1 (char 0)

period1={int(time.time())}&period2={int(time.time())}&

<!-- 
cash_flow_annual = requests.get(f'https://query2.finance.yahoo.com/ws/fundamentals-timeseries/v1/finance/timeseries/{stock["ticker"]}?lang=en-US&region=US&symbol={stock["ticker"]}&padTimeSeries=true&type=annualFreeCashFlow%2CtrailingFreeCashFlow%2CannualCapitalExpenditure%2CtrailingCapitalExpenditure%2CannualOperatingCashFlow%2CtrailingOperatingCashFlow%2CannualEndCashPosition%2CtrailingEndCashPosition%2CannualBeginningCashPosition%2CtrailingBeginningCashPosition%2CannualChangeInCashSupplementalAsReported%2CtrailingChangeInCashSupplementalAsReported%2CannualCashFlowFromContinuingFinancingActivities%2CtrailingCashFlowFromContinuingFinancingActivities%2CannualNetOtherFinancingCharges%2CtrailingNetOtherFinancingCharges%2CannualCashDividendsPaid%2CtrailingCashDividendsPaid%2CannualRepurchaseOfCapitalStock%2CtrailingRepurchaseOfCapitalStock%2CannualCommonStockIssuance%2CtrailingCommonStockIssuance%2CannualRepaymentOfDebt%2CtrailingRepaymentOfDebt%2CannualInvestingCashFlow%2CtrailingInvestingCashFlow%2CannualNetOtherInvestingChanges%2CtrailingNetOtherInvestingChanges%2CannualSaleOfInvestment%2CtrailingSaleOfInvestment%2CannualPurchaseOfInvestment%2CtrailingPurchaseOfInvestment%2CannualPurchaseOfBusiness%2CtrailingPurchaseOfBusiness%2CannualOtherNonCashItems%2CtrailingOtherNonCashItems%2CannualChangeInAccountPayable%2CtrailingChangeInAccountPayable%2CannualChangeInInventory%2CtrailingChangeInInventory%2CannualChangesInAccountReceivables%2CtrailingChangesInAccountReceivables%2CannualChangeInWorkingCapital%2CtrailingChangeInWorkingCapital%2CannualStockBasedCompensation%2CtrailingStockBasedCompensation%2CannualDeferredIncomeTax%2CtrailingDeferredIncomeTax%2CannualDepreciationAndAmortization%2CtrailingDepreciationAndAmortization%2CannualNetIncome%2CtrailingNetIncome&merge=false&corsDomain=finance.yahoo.com')
-->

grep -R --exclude-dir=venv --include=\*.py 'yahoo' .

# convert volusia property appraiser data

java -jar access2csv.jar CAMA_DATA_EXPORT_WEB.accdb

sqlite3 database.db ".mode csv" ".import VCPA_CAMA_OWNER.csv VCPA_CAMA_OWNER" ".exit"

sqlite3 database.db ".mode csv" ".import VCPA_CAMA_PARCEL.csv VCPA_CAMA_PARCEL" ".exit"

# 
