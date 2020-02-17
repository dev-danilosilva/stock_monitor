from datetime import date
from datetime import datetime
from pony.orm import *
import os

_database = Database()


class StockSymbol(_database.Entity):
    id = PrimaryKey(int, auto=True)
    ticker = Required(str, unique=True)
    stock__prices = Set('StockPrices')


class StockPrices(_database.Entity):
    id = PrimaryKey(int, auto=True)
    last_update = Required(datetime)
    close_price = Required(float)
    date = Required(date)
    fk_stock_id = Required(StockSymbol)


def connect_to_database(filename):
    filename = os.path.join(os.getcwd(), filename)
    _database.bind(provider='sqlite', filename=filename, create_db=True)
    _database.generate_mapping(create_tables=True)
    return _database


