import bs4 as bs
import json
import requests

def save_sp500_tickers():
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = {"stocks":[]}
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text.strip()
        sector = row.findAll('td')[3].text.strip()
        industry = row.findAll('td')[4].text.strip()
        print(row.findAll('td')[2])
        reports = row.findAll('td')[2].find('a')['href'].strip()
        tickers['stocks'].append({"ticker":ticker,"sector":sector,"industry":industry,"reports":reports})
        print(ticker)
        
    with open("wiki_stocks/sp500tickers.json","w") as f:
        json.dump(tickers,f)
        
    return tickers

#save_sp500_tickers()