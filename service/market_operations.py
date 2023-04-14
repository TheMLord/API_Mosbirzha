import json
import requests
import pandas as pd


class StockMarket:
    @staticmethod
    def get_securities():
        url_get_all_securities = 'https://iss.moex.com/iss/' \
                                 'engines/stock/markets/shares' \
                                 '/boards/TQBR/securities.json'
        response = requests.get(url_get_all_securities)
        data = json.loads(response.text)
        securities = data['securities']['data']

        table_securities = pd.DataFrame(columns=["Ticker",
                                                 "Название акции",
                                                 "Стоимость",
                                                 "Статус"])
        counter = 0
        for security in securities:
            secid = security[0]
            name = security[2]
            last = security[3]
            status = security[6]
            table_securities.loc[counter] = [secid,
                                             name,
                                             last,
                                             status]
            counter += 1
        return table_securities

    @staticmethod
    def get_info_about_stock(ticker: str):
        url = f'https://iss.moex.com/iss/engines/stock/' \
              f'markets/shares/boards/tqbr/securities/{ticker}.json'
        response = requests.get(url)
        json_data = response.json()

        return json_data['securities']['data'][0][0], \
            json_data['securities']['data'][0][2], \
            json_data['securities']['data'][0][3]

    @staticmethod
    def get_stock_growth(ticker: str, period: int):
        end_date = pd.Timestamp.now().date()
        start_date = end_date - pd.Timedelta(days=period)

        url = f'https://iss.moex.com/iss/history/engines/stock/' \
              f'markets/shares/boards/TQBR/securities/' \
              f'{ticker}.json?from={start_date}&till={end_date}' \
              f'&iss.meta=off&iss.only=history&history.' \
              f'columns=SECID,TRADEDATE,CLOSE'
        response = requests.get(url)
        json_data = response.json()

        start_price = json_data["history"]["data"][0][-1]
        end_price = json_data["history"]["data"][-1][-1]
        profitability = "{:.2f}%".format((end_price * 100 / start_price - 100))

        return str(start_date), \
            str(end_date), \
            start_price, \
            end_price, \
            profitability
