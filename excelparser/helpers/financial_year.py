import datetime
from typing import Any


def _start_date(q, y):
    if q == 4:
        y = y + 1
    return datetime.date(y, Quarter._start_months[q][0], 1)


def _end_date(q, y):
    if q == 4:
        y = y + 1
    return datetime.date(y, Quarter._end_months[q][0], Quarter._end_months[q][2])


class Quarter:
    """An object representing a financial quarter. This is mainly required for building
    a :py:class:`core.master.Master` object.

    Args:
        quarter (int): e.g.1, 2, 3 or 4
        year (int): e.g. 2013
    """
    _start_months = {
        1: (4, 'April'),
        2: (7, 'July'),
        3: (10, 'October'),
        4: (1, 'January')
    }

    _end_months = {
        1: (6, 'June', 30),
        2: (9, 'September', 30),
        3: (12, 'December', 31),
        4: (3, 'March', 31),
    }

    def __init__(self, year: int, quarter: int) -> None:

        if isinstance(quarter, int) and (quarter >= 1 and quarter <= 4):
            self.quarter = quarter
        else:
            raise ValueError("A quarter must be either 1, 2, 3 or 4")

        if isinstance(year, int) and (year in range(1950, 2100)):
            self.year = year
        else:
            raise ValueError("Year must be between 1950 and 2100 - surely that will do?")

        self.start_date = _start_date(self.quarter, self.year)
        self.end_date = _end_date(self.quarter, self.year)

    def __str__(self):
        return f"Q{self.quarter} {str(self.year)[2:]}/{str(self.year + 1)[2:]}"

    def __repr__(self):
        return f"Quarter({self.year}, {self.quarter})"

    @property
    def fy(self):
        """Return a :py:class:`core.temporal.FinancialYear` object.
        """
        return FinancialYear(self.year)


class FinancialYear:
    """An object representing a financial year.
    If parameter ``year`` must be in the range 150 - 2100.
    """

    def __init__(self, year):
        if isinstance(year, int) and (year in range(150, 2100)):
            self.year = year
        else:
            raise ValueError("A year must be an integer between 1950 and 2100")
        self._generate_quarters()
        self._q1 = self.quarters[0]
        self._q2 = self.quarters[1]
        self._q3 = self.quarters[2]
        self._q4 = self.quarters[3]

        self.start_date = self.q1.start_date
        self.end_date = self.q4.end_date

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, FinancialYear):
            raise ValueError("Can only compare FinancialYear object with another FinancialYear object")
        if other.year == self.year:
            return True
        else:
            return False

    @property
    def q1(self) -> Quarter:
        """Quarter 1 as a :py:class:`datetime.date` object
        """
        return self._q1

    @property
    def q2(self) -> Quarter:
        """Quarter 2 as a :py:class:`datetime.date` object
        """
        return self._q2

    @property
    def q3(self) -> Quarter:
        """Quarter 3 as a :py:class:`datetime.date` object
        """
        return self._q3

    @property
    def q4(self) -> Quarter:
        """Quarter 4 as a :py:class:`datetime.date` object
        """
        return self._q4

    def __str__(self):
        return f"FY{str(self.year)}/{str(self.year + 1)[2:]}"

    def _generate_quarters(self) -> None:
        self.quarters = [Quarter(self.year, x) for x in range(1, 5)]

    def __repr__(self):
        return f"FinancialYear({self.year})"