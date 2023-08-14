# data-bot
Harvesting data automatically

Start with capturing data in both sqlite and JSON for https://finance.yahoo.com/screener/6039bb71-c189-4b62-ab6d-6dbd659495bb?count=25&offset=25

craigslist and facebook markeplace analysis, marklet research

#### Geocoding
https://geocoding.geo.census.gov/geocoder/Geocoding_Services_API.html
https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?address=410+Voorhis+Ave+deland+fl&benchmark=9&format=json

# Build DataSets


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

cash_flow_annual = requests.get(f'https://query2.finance.yahoo.com/ws/fundamentals-timeseries/v1/finance/timeseries/{stock["ticker"]}?lang=en-US&region=US&symbol={stock["ticker"]}&padTimeSeries=true&type=annualFreeCashFlow%2CtrailingFreeCashFlow%2CannualCapitalExpenditure%2CtrailingCapitalExpenditure%2CannualOperatingCashFlow%2CtrailingOperatingCashFlow%2CannualEndCashPosition%2CtrailingEndCashPosition%2CannualBeginningCashPosition%2CtrailingBeginningCashPosition%2CannualChangeInCashSupplementalAsReported%2CtrailingChangeInCashSupplementalAsReported%2CannualCashFlowFromContinuingFinancingActivities%2CtrailingCashFlowFromContinuingFinancingActivities%2CannualNetOtherFinancingCharges%2CtrailingNetOtherFinancingCharges%2CannualCashDividendsPaid%2CtrailingCashDividendsPaid%2CannualRepurchaseOfCapitalStock%2CtrailingRepurchaseOfCapitalStock%2CannualCommonStockIssuance%2CtrailingCommonStockIssuance%2CannualRepaymentOfDebt%2CtrailingRepaymentOfDebt%2CannualInvestingCashFlow%2CtrailingInvestingCashFlow%2CannualNetOtherInvestingChanges%2CtrailingNetOtherInvestingChanges%2CannualSaleOfInvestment%2CtrailingSaleOfInvestment%2CannualPurchaseOfInvestment%2CtrailingPurchaseOfInvestment%2CannualPurchaseOfBusiness%2CtrailingPurchaseOfBusiness%2CannualOtherNonCashItems%2CtrailingOtherNonCashItems%2CannualChangeInAccountPayable%2CtrailingChangeInAccountPayable%2CannualChangeInInventory%2CtrailingChangeInInventory%2CannualChangesInAccountReceivables%2CtrailingChangesInAccountReceivables%2CannualChangeInWorkingCapital%2CtrailingChangeInWorkingCapital%2CannualStockBasedCompensation%2CtrailingStockBasedCompensation%2CannualDeferredIncomeTax%2CtrailingDeferredIncomeTax%2CannualDepreciationAndAmortization%2CtrailingDepreciationAndAmortization%2CannualNetIncome%2CtrailingNetIncome&merge=false&corsDomain=finance.yahoo.com')

grep -R --exclude-dir=venv --include=\*.py 'yahoo' .

# convert volusia property appraiser data

java -jar access2csv.jar CAMA_DATA_EXPORT_WEB.accdb

sqlite3 database.db ".mode csv" ".import VCPA_CAMA_OWNER.csv VCPA_CAMA_OWNER" ".exit"

sqlite3 database.db ".mode csv" ".import VCPA_CAMA_PARCEL.csv VCPA_CAMA_PARCEL" ".exit"