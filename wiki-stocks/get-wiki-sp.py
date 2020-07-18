import bs4 as bs
import json
import requests

def save_sp500_tickers():
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text.strip()
        tickers.append(ticker)
        print(ticker)
        
    with open("wiki-stocks/sp500tickers.json","w") as f:
        json.dump(tickers,f)
        
    return tickers

save_sp500_tickers()