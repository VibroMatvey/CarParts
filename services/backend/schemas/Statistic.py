import datetime

from pydantic import BaseModel


class StatisticDetails(BaseModel):
    date: datetime.date
    count: int
    total: int


class Statistic(BaseModel):
    orders: list[StatisticDetails]
    sales: list[StatisticDetails]
