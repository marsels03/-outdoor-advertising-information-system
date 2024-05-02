import os
from itertools import takewhile

from string import Template


class SQLProvider:
    def __init__(self, sql_path: str) -> None:
        self.sql_scripts = {}
        for file in os.listdir(sql_path):
            self.sql_scripts[file[:-4]] = Template(open(f'{sql_path}/{file}').read())

    def get(self, name: str, params: dict = None) -> str:
        if params is None:
            params = {}
        return self.sql_scripts[name].substitute(**params)

