from datetime import date
from datetime import datetime
from pony.orm import *
import os

database = Database()


class StockSymbol(database.Entity):
    id = PrimaryKey(int, auto=True)
    ticker = Required(str, unique=True)
    stock__prices = Set('StockPrices')


class StockPrices(database.Entity):
    id = PrimaryKey(int, auto=True)
    last_update = Required(datetime)
    close_price = Required(float)
    date = Required(date)
    fk_stock_id = Required(StockSymbol)


filename = os.path.join(os.getcwd(), 'stock_monitor.db')
database.bind(provider='sqlite', filename=filename, create_db=True)
database.generate_mapping(create_tables=True)

# class Storage:
#     def __init__(self, filename='database.sqlite'):
#         filename = os.path.join(os.getcwd(), filename)
#         db.bind(provider='sqlite', filename=filename, create_db=True)
#         db.generate_mapping(create_tables=True)
#
#     def create_stock(self, tckr):
#         with db_session:
#             stock = StockSymbol(ticker=tckr)
#
#     def define_price(self, stock: StockSymbol):
#         with db_session:
#             pass
#
#     def get_stock(self, ticker: str):
#         with db_session:
#             return StockSymbol.get(ticker=ticker)
#
#     def get_all_stocks(self):
#         result = []
#         with db_session:
#             for res in select(stock for stock in StockSymbol):
#                 result.append(res)
#         return result
#
#     def save_changes(self, ticker):
#         with db_session:
#             commit()


