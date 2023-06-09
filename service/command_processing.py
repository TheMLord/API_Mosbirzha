import sys
import logging
import pandas as pd


from model.investor_profile import InvestmentPortfolio
from service.json_operations import WorkingWithJson
from service.market_operations import StockMarket

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
logging.basicConfig(level=logging.INFO)


class Command:
    def __init__(self, command: list):
        self.command = command
        self.execute()

    def execute(self):
        if len(self.command) == 2:
            if self.command[1] == "get_securities_info":
                logging.info(StockMarket.get_securities())
            elif self.command[1] == "change_portfolio":
                portfolio_dict = WorkingWithJson.read_portfolio_dict_json()
                logging.info("Введите количество акций, которые хотите добавить в портфель")
                count_stock = int(sys.stdin.readline().strip())
                for _ in range(count_stock):
                    logging.info("введите ticker и количество")
                    ticker, count = map(str, sys.stdin.readline().strip().split())
                    if ticker in portfolio_dict:
                        portfolio_dict[ticker] += int(count)
                    else:
                        portfolio_dict[ticker] = int(count)
                WorkingWithJson.write_portfolio_dict_json(portfolio_dict)
            elif self.command[1] == "view_portfolio":
                portfolio = InvestmentPortfolio(WorkingWithJson.read_portfolio_dict_json())
                logging.info(portfolio.output_portfolio())
            else:
                logging.warning("некорректная команда")
        elif len(self.command) == 3:
            if self.command[1] == "view_portfolio":
                try:
                    period = int(self.command[2])
                    portfolio = InvestmentPortfolio(WorkingWithJson.read_portfolio_dict_json())
                    logging.info(portfolio.output_portfolio(period))
                except ValueError:
                    logging.warning("некорректная команда")
            elif self.command[1] == "delete_stock":
                if WorkingWithJson.delete_stock(self.command[2]):
                    logging.info(f'акция {self.command[2]} удалена')
                else:
                    logging.warning("неверно указан ticker акции")
            else:
                logging.warning("некорректная команда")
        else:
            logging.warning("некорректная команда")
