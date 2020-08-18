from base import Base
from sqlalchemy import Column, String, Integer, Date, Boolean, Numeric, ForeignKey, UniqueConstraint, PrimaryKeyConstraint

class WikiStocks(Base):
    __tablename__ = 'wiki_stocks'

    id=Column(Integer, primary_key=True)
    ticker=Column('ticker', String(8), unique=True)
    is_owned=Column('is_owned', Boolean)
    quantity=Column('quantity', Integer)
    price=Column('price', Numeric)

    def __init__(self, ticker, is_owned, quantity, price):
        self.ticker = ticker
        self.is_owned = is_owned
        self.quantity = quantity
        self.price = price

class TickerData(Base):
    __tablename__ = "ticker_data"

    #id = Column(Integer, primary_key=True)
    wiki_ticker = Column('wiki_ticker',String(8))

    financial_type = Column('type', String(256))
    record_date = Column('date', Date)
    record_value = Column('value', Numeric)

    __table_args__ = (
        UniqueConstraint('wiki_ticker', 'type', 'date', 'value', name='_data_unique'),
        PrimaryKeyConstraint('wiki_ticker', 'type', 'date', 'value'),
    )

    def __init__(self, wiki_ticker, financial_type, record_date, record_value):
        self.wiki_ticker = wiki_ticker
        self.financial_type = financial_type
        self.record_date = record_date
        self.record_value = record_value