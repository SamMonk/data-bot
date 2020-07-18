from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///data-bot.db')
Session = sessionmaker(bind=engine)

import base
import stock

base.Base.metadata.create_all(engine)
