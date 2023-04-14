import json
from json import JSONDecodeError


class WorkingWithJson:
    @staticmethod
    def read_portfolio_dict_json():
        try:
            with open("portfolio.json", "r", encoding="UTF-8") as file_json:
                return json.load(file_json)
        except JSONDecodeError:
            return {}

    @staticmethod
    def write_portfolio_dict_json(portfolio_dict: dict):
        with open("portfolio.json", "w", encoding="UTF-8") as file_json:
            json.dump(portfolio_dict, file_json)
