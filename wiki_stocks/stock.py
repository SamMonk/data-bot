from base import Base
from sqlalchemy import Column, String, Integer, Date, Boolean, Numeric, ForeignKey, UniqueConstraint, PrimaryKeyConstraint

class TickerData(Base):
    __tablename__ = "ticker_data"

    #id = Column(Integer, primary_key=True)
    sp_ticker = Column(String(8))

    financial_type = Column('type', String(256))
    period_type = Column('period', String(256))
    record_date = Column('date', Date)
    record_value = Column('value', String(256))

    __table_args__ = (
        UniqueConstraint('sp_ticker', 'type', 'period', 'date', 'value', name='_data_unique'),
        PrimaryKeyConstraint('sp_ticker', 'type', 'period', 'date', 'value'),
    )

    def __init__(self, sp_ticker, financial_type, period_type, record_date, record_value):
        # print('sp')
        # print(sp_ticker)
        # print(financial_type)
        # print(record_date)
        # print(record_value)
        self.sp_ticker = sp_ticker
        self.financial_type = financial_type
        self.period_type = period_type
        self.record_date = record_date
        self.record_value = record_value

