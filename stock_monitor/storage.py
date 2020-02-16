from datetime import date
from datetime import datetime
from pony.orm import *
import os

db = Database()


class StockSymbol(db.Entity):
    id = PrimaryKey(int, auto=True)
    ticker = Required(str, unique=True)
    stock__prices = Set('StockPrices')


class StockPrices(db.Entity):
    id = PrimaryKey(int, auto=True)
    last_update = Required(datetime)
    close_price = Required(float)
    date = Required(date, unique=True)
    fk_stock_id = Required(StockSymbol)


class Storage:
    def __init__(self, filename='../database.sqlite'):
        filename = os.path.join(os.getcwd(), filename)
        db.bind(provider='sqlite', filename=filename, create_db=True)
        db.generate_mapping(create_tables=True)


    def create_stock(self, tckr):
        with db_session:
            stock = StockSymbol(ticker=tckr)

    def get_all_stocks(self):
        pass
