from sqlalchemy.ext.asyncio import AsyncSession

from repository import get_month_orders, get_month_sales
from schemas import Statistic


async def get_statistic(db: AsyncSession) -> Statistic:
    orders = await get_month_orders(db)
    sales = await get_month_sales(db)
    statistic: Statistic = Statistic(orders=orders, sales=sales)
    return statistic
