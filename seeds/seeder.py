from flask_seeder import Seeder
from faker import Faker
from random import randint, sample
from seeds.data import ingredients, beverages, sizes, clients
from app.repositories.models import (
    Beverage,
    Order,
    Ingredient,
    Size,
    OrderDetail,
    OrderBeverage,
)

from app.plugins import db
from app.controllers import (
    BeverageController,
    IngredientController,
    SizeController,
)


def create_sizes(sizeData) -> list:
    return [Size(name=key, price=value) for key, value in sizeData.items()]


def create_ingredients(ingredientData) -> list:
    return [Ingredient(name=key, price=value) for key, value in ingredientData.items()]


def create_beverages(beverageData) -> list:
    return [Beverage(name=key, price=value) for key, value in beverageData.items()]


def create_orders(count, clients) -> list:
    new_order = []
    order_detail = []
    beverage_order = []
    fake = Faker()
    ingredients, _ = IngredientController.get_all()
    sizes, _ = SizeController.get_all()
    beverages, _ = BeverageController.get_all()
    for index in range(count):
        name = clients[randint(0, len(clients) - 1)]
        size = sizes[fake.random_int(min=0, max=len(sizes) - 1)]
        order_beverages = sample(beverages, fake.random_int(min=1, max=len(beverages)))
        order_ingredients = sample(
            ingredients, fake.random_int(min=1, max=len(ingredients))
        )
        total = (
            size["price"]
            + sum(ingredients["price"] for ingredients in order_ingredients)
            + sum(beverages["price"] for beverages in order_beverages)
        )
        new_order.append(
            Order(
                client_name=name,
                client_dni=fake.random_int(min=10000000, max=99999999),
                client_phone=fake.phone_number(),
                client_address=fake.address(),
                total_price=round(total, 2),
                date=fake.date_time_between(start_date="-1y", end_date="now"),
                size_id=size["_id"],
            )
        )
        for beverage in order_beverages:
            beverage_order.append(
                OrderBeverage(
                    order_id=index,
                    beverage_price=beverage["price"],
                    beverage_id=beverage["_id"],
                )
            )
        for ingredient in order_ingredients:
            order_detail.append(
                OrderDetail(
                    order_id=index,
                    ingredient_price=ingredient["price"],
                    ingredient_id=ingredient["_id"],
                )
            )
    return new_order, order_detail, beverage_order


class DataBaseSeeder(Seeder):
    @classmethod
    def run(self):
        size = create_sizes(sizes)
        ingredient = create_ingredients(ingredients)
        beverage = create_beverages(beverages)

        self.insert_db(size)
        self.insert_db(ingredient)
        self.insert_db(beverage)

        order, order_detail, order_beverage = create_orders(100, clients)
        self.insert_db(order)
        self.insert_db(order_detail)
        self.insert_db(order_beverage)

    def insert_db(data):
        for item in data:
            db.session.add(item)
