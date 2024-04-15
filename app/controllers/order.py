from sqlalchemy.exc import SQLAlchemyError

from ..repositories.managers import OrderManager
from .base import BaseController
from .concrete_order_builder import ConcreteOrderBuilder


class OrderController(BaseController):
    manager = OrderManager
    __required_info = (
        "client_name",
        "client_dni",
        "client_address",
        "client_phone",
        "size_id",
    )

    @staticmethod
    def calculate_order_price(size_price: float, ingredients: list, beverages: list):
        ingredients_price = sum(ingredient.price for ingredient in ingredients)
        beverages_price = sum(beverage.price for beverage in beverages)
        price = size_price + ingredients_price + beverages_price
        return round(price, 2)

    @classmethod
    def create(cls, order: dict):
        try:
            builder = ConcreteOrderBuilder()
            builder.set_data(order.copy())
            builder.check_required_info(cls.__required_info)
            builder.check_size()
            builder.calculate_order_price()
            return builder.create()
        except SQLAlchemyError as e:
            return None, str(e)
