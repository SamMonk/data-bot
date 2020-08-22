# from base import Base
# from wikistock import WikiStocks, TickerData
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# engine = create_engine('sqlite:///wiki_stocks/wiki.db')
# Session = sessionmaker(bind=engine)

# import time
import requests
# from bs4 import BeautifulSoup
# import json
# import datetime

# Base.metadata.create_all(engine)
# session = Session()

#https://finance.yahoo.com/quote/AAPL
ticker = 'AAPL'
yahoo_data = requests.get(f'https://finance.yahoo.com/quote/{ticker}')
print(yahoo_data.content)
# session.flush()
# with open('./wiki_stocks/sp500tickers.json') as f:
# session.flush()
# session.commit()
