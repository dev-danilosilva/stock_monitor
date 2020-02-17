from stock_monitor import AlphaVantageClient
from stock_monitor.models import *
from pony import *
import datetime
# from credentials import API_KEY


# Para coletar dados de outras ações, adicione o símbolo na lista STOCK_SYMBOLS
STOCK_SYMBOLS = ['PETR4.SAO', 'B3SA3.SAO']

# Caminho do arquivo que armazenará os dados das ações listadas em STOCK_SYMBOLS
DATABASE_FILE_PATH = 'database.db'

#Chave para uso da AlphaVantageAPI
API_KEY = ''


# Caso uma determinada ação não exista no BD, um registro no banco de dados é criado. Caso já existe, o registro é
# obtido do BD.
def get_or_create_ticker(symbol):
    ticker = StockSymbol.get(ticker=symbol)
    if ticker is None:
        ticker = StockSymbol(ticker=symbol)

    return ticker


def main():
    database_controller = connect_to_database(DATABASE_FILE_PATH)
    stock_api = AlphaVantageClient(API_KEY)

    with db_session:
        for ticker in STOCK_SYMBOLS:

            # Obtendo os dados dos ultimos 7 dias disponiveis na alphavantage api
            try:
                api_data = stock_api.get_time_series_daily(ticker, period=7)
            except Exception as e:
                print('Error:', ticker)
                continue

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
            print('Success:', ticker)


if __name__ == '__main__':
    main()
