# Stock Monitor

Para executar o projeto:

1 - instale as dependências com o comando

```
pip install -r requirements.txt
```


2 - execute o arquivo main.py com o comando

```
python main.py
```


### **stock_monitor**
Módulo para obtenção de dados de ações da Alpha Vantage API.

Para utilizar o módulo, basta instanciar um objeto da classe AlphaVantageClient e utilizar o método
get_time_series_daily para obter um dicionário com dados diários de uma determinada ação.


### `stock_monitor.AlphaVantageClient.get_time_series_daily(ticker: str, period: int)`

O método recebe como 2 informações como parâmetro

- ticker: símbolo da ação
- period: os dados o obtidos pelo método terão como data os últimos n dias, sendo n um número inteiro, e n sendo
o valor passado no parâmetro period. (O valor padrão desse parâmetro é 7).


### `stock_monitor.models`

Módulo que cria o banco de dados e contém as classes modelo para o mapeamento das entidades do
banco de dados utilizando o Pony ORM.

### `stock_monitor.models.connect_to_database(database_path : str)`
O método que cria e conecta-se à base de dados

## `main.py`

O script:

1. Contém uma lista de todos as ações no qual se deseja obter dados. Para modificar as ações monitoradas pelo script, basta
adicionar o símbolo dela a lista `STOCK_SYMBOLS`.

1. Cria um banco de dados (sqlite) caso ele ainda não exista. O caminho do arquivo deve ser incluído na variável global
`DATABASE_FILE_PATH`

1. Precisa receber a chave para ser utilizada para acessar os dados obtidos pela AlphaVantageAPI. A chave pode ser
armazenada na variável global `API_KEY`. *(Você pode optar por colocar a chave em um módulo diferente e importar esse módulo em
main.py)*

1. Uma vez que contém as constantes acima citadas, ele segue os passos descritos a seguir

1. Conecta-se com o banco de dados

1. Instacia um objeto da classe AlphaVantageClient

1. Percorre a lista de ações que se deseja monitorar. Os passos a seguir são realizados para cada uma dessas ações.

1. Obtém os dados da ação da AlphaVantageAPI

1. Obtém os dados dos últimos 7 dias disponíveis na AV API.

1. Para cada uma das datas obtidas na API, se verifica se o dado existe no BD. Caso não exista nenhum dado para a data,
cria-se um novo registro para a data. Caso já exista e o preco de fechamento no BD seja diferente do que veio da API,
esse valor é atualizado no BD.


## Banco de Dados

Se você precisa saber o como o banco de dados está modelado, segue o script com as definições das entidades e seus respectivos atributos:

```sqlite
CREATE TABLE "STOCK_SYMBOLS" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"ticker"	TEXT NOT NULL UNIQUE
);

CREATE TABLE "STOCK_PRICES" (
	id	INTEGER NOT NULL UNIQUE,
	fk_stock_id	INTEGER NOT NULL,
	close_price	REAL NOT NULL,
	"date"	TEXT NOT NULL,
	PRIMARY KEY(id),
	FOREIGN KEY(fk_stock_id) REFERENCES STOCK_SYMBOLS(id)
);
```

Segue também as definições das entidades utilizando-se o  [Pony ORM](https://ponyorm.org/)

```python
from pony import *

db = Database()

class StockSymbol(db.Entity):
    id = PrimaryKey(int, auto=True)
    ticker = Required(str, unique=True)
    stock__prices = Set('StockPrices')


class StockPrices(db.Entity):
    id = PrimaryKey(int, auto=True)
    last_update = Required(datetime)
    close_price = Required(float)
    date = Required(date)
    fk_stock_id = Required(StockSymbol)
```


*Obs: As anotações de tipo de dados no módulo stock_monitor foram utilizadas no desenvolvimento para
garantir que alguns tipos de erros fossem evitados em produção utilizando-se o type checker `mypy`*



