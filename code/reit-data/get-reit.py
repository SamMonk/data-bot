
#https://finance.yahoo.com/screener/6039bb71-c189-4b62-ab6d-6dbd659495bb?count=200

import requests
from bs4 import BeautifulSoup
# import json

my_screener = requests.get(f'https://finance.yahoo.com/screener/6039bb71-c189-4b62-ab6d-6dbd659495bb?count=200')

#print(my_screener)

with open('code/reit-data/reits-screener.html','r') as ticker_report:
    ticker_table_string = ticker_report.read()
    soup = BeautifulSoup(ticker_table_string, "html.parser")
    tables = soup.find_all("table")
    #print(tables[0])
    tickers = tables[0].find_all("a")
    for ticker in tickers:
        print(ticker.text)
