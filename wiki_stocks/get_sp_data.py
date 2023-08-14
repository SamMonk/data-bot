import datetime
from bs4 import BeautifulSoup
import json
import requests
from base import Base
from wikistock import WikiStocks, SPData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import time

engine = create_engine('sqlite:///wiki_stocks/wiki.db')
Session = sessionmaker(bind=engine)


Base.metadata.create_all(engine)
session = Session()
with open('./wiki_stocks/sp500tickers.json') as f:
    sp_data = json.load(f)
    for stock in sp_data['stocks']:
        time.sleep(2)
        print(stock["ticker"])
        yahoo_data = requests.get(
            f'https://finance.yahoo.com/quote/{stock["ticker"]}', headers={'User-Agent': 'Custom'})
        print(yahoo_data)
        soup = BeautifulSoup(yahoo_data.content, "html.parser")
        tables = soup.find_all("table")
        for table in tables:
            trs = table.find_all("tr")
            for tr in trs:
                try:
                    print(stock)
                    print(tr)
                    session.merge(SPData(stock["ticker"], tr.find_all('td')[
                              0].text, datetime.datetime.now(), tr.find_all('td')[1].text))
                    print(datetime.datetime.now())
                    print("key:" + tr.find_all('td')[0].text)
                    print("value:" + tr.find_all('td')[1].text)
                except Exception as ex:
                    print(ex)
                    print(stock["ticker"])
            session.commit()
            
