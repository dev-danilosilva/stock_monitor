from stock_monitor import AlphaVantageClient
from stock_monitor.models import *
from credentials import API_KEY
from pony import *
import datetime

# Para coletar dados de outras ações, adicione o símbolo na lista STOCK_SYMBOLS
STOCK_SYMBOLS = ['PETR4.SAO', 'B3SA3.SAO']


def get_or_create_ticker(symbol):
    ticker = StockSymbol.get(ticker=symbol)
    if ticker is None:
        ticker = StockSymbol(ticker=symbol)

    return ticker


def main():
    stock_api = AlphaVantageClient(API_KEY)

    with db_session:
        for ticker in STOCK_SYMBOLS:

            # Obtendo os dados dos ultimos 7 dias disponiveis na alphavantage api
            api_data = stock_api.get_time_series_daily(ticker, period=7)

            # Obtendo os dados da acao do banco de dados
            db_stock = get_or_create_ticker(ticker)

            # Percorrendo os datas disponíveis na api
            for stock_date in api_data:
                stock_date_price = StockPrices.get(date=stock_date, fk_stock_id=db_stock)
                api_price = float(api_data[stock_date]['4. close'])

                if stock_date_price is None:
                    StockPrices(
                        last_update=datetime.datetime.utcnow(),
                        close_price=api_price,
                        date=stock_date,
                        fk_stock_id=db_stock
                    )
                elif stock_date_price != api_price:
                    stock_date_price.close_price = api_price


if __name__ == '__main__':
    main()
