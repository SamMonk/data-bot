import sqlalchemy
import datetime
import json
import decimal
import logging

def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()
    if isinstance(o, decimal.Decimal):
        return str(o)

engine = sqlalchemy.create_engine('sqlite:///wiki_stocks/wiki.db')
metadata = sqlalchemy.MetaData()
sqlalchemy.Table('ticker_data', metadata, autoload=True, autoload_with=engine)
table = metadata.tables['ticker_data']
conn = engine.connect()

select_statement = table.select().where(
    table.c.type.in_((
        'quarterlyBasicEPS'
        ,'quarterlyCurrentAssets'
        ,'quarterlyCurrentDebt'
        ,'quarterlyEbitda'
        ,'quarterlyNetIncome'
    )))
logging.warning(select_statement)
select_return = conn.execute(select_statement)

data = json.dumps([dict(r) for r in select_return], default=default)
with open('./wiki_stocks/ticker_data.json', 'w+') as outfile:
    outfile.write(data)