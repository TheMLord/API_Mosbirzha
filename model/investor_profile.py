import concurrent.futures
import pandas as pd

from service.market_operations import StockMarket


class InvestmentPortfolio:
    def __init__(self, portfolio: dict):
        self.portfolio = portfolio
        self.table_portfolio = pd.DataFrame(
            columns=["Secid", "Название", "Количество", "Стоимость",
                     "Общая стоимость", "Дата начала", "Стоимость на начало периода",
                     "Дата конца", "Стоимость на конец периода", "Рост за период"])

    def get_info_securities(self, i, period : int):
        count_stock = self.portfolio[i]
        secid, name, price = StockMarket.get_info_about_stock(i)
        start_date, end_date, price_start, price_end, profitability = StockMarket.get_stock_growth(i, period)
        total_cost = price * count_stock
        return [secid, name, count_stock, price, total_cost, start_date, price_start, end_date, price_end,
                profitability]

    def output_portfolio(self, period=30):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for i in self.portfolio:
                futures.append(executor.submit(self.get_info_securities, i, period))

            count = 0
            for future in concurrent.futures.as_completed(futures):
                self.table_portfolio.loc[count] = future.result()
                count += 1
        return self.table_portfolio
