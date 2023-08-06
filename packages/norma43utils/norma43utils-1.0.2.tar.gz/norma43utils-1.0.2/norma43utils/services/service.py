import itertools
from abc import ABC, abstractmethod
from decimal import Decimal
from typing import List

from norma43parser import Norma43Document, DateFormat, Norma43Parser


class Service(ABC):
    @staticmethod
    def read_norma43_file(file_path: str, date_format: DateFormat) -> Norma43Document:
        n43: Norma43Document

        with open(file_path, "r") as file:
            n43 = Norma43Parser(date_format=date_format).parse(file.read())

        return n43

    @staticmethod
    def get_values_list(n43: Norma43Document) -> List[List[str]]:
        account_movements = list(itertools.chain.from_iterable([account.movement_lines for account in n43.accounts]))

        day_format: str = "%d/%m/%Y"
        two_places = Decimal(10) ** -2

        return [
            [
                line.value_date.strftime(day_format),
                line.transaction_date.strftime(day_format),
                line.description,
                ". ".join(line.extra_information),
                str(line.amount.quantize(two_places)),
                str(line.balance.quantize(two_places)),
            ]
            for line in account_movements
        ]

    @abstractmethod
    def write(self, n43: Norma43Document, output_id: str) -> None:
        pass
