from calendar import month_name

from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

from ..repositories.models import Order, OrderDetail
from .ingredient import IngredientController


class ReportController:
    @staticmethod
    def get_most_requested_ingredient():
        request_ingredients = (
            OrderDetail.query.with_entities(
                OrderDetail.ingredient_id, func.count(OrderDetail.ingredient_id)
            )
            .group_by(OrderDetail.ingredient_id)
            .order_by(func.count(OrderDetail.ingredient_id).desc())
            .all()
        )
        most_requested_ingredient = request_ingredients[0]
        ingredient_name = IngredientController.get_by_id(most_requested_ingredient[0])[
            0
        ]["name"]
        ingredient_requested_times = most_requested_ingredient[1]
        return {
            "ingredient": ingredient_name,
            "requested_times": ingredient_requested_times,
        }

    @staticmethod
    def get_month_with_most_revenue():
        orders = Order.query.all()
        date_list = [(order.date.month, order.total_price) for order in orders]
        if date_list:
            monthly_revenue_report = {month: 0 for month, _ in date_list}
            for month_of_order, total_price in date_list:
                monthly_revenue_report.update(
                    {
                        month_of_order: total_price
                        + monthly_revenue_report.get(month_of_order)
                    }
                )
            sorted_report = sorted(
                monthly_revenue_report.items(), key=lambda x: x[1], reverse=True
            )
            month_with_high_revenue = sorted_report[0]
            return {
                "month": month_name[month_with_high_revenue[0]],
                "revenue": round(month_with_high_revenue[1], 2),
            }

    @staticmethod
    def get_best_costumers():
        best_clients = (
            Order.query.with_entities(Order.client_name, func.sum(Order.total_price))
            .group_by(Order.client_name)
            .order_by(func.sum(Order.total_price).desc())
            .limit(3)
            .all()
        )
        first = {"name": best_clients[0][0], "total": best_clients[0][1]}
        second = {"name": best_clients[1][0], "total": best_clients[1][1]}
        third = {"name": best_clients[2][0], "total": best_clients[2][1]}
        return {"first": first, "second": second, "third": third}

    @classmethod
    def create(cls):
        try:
            return {
                "most_requested_ingredient": cls.get_most_requested_ingredient(),
                "month_with_the_highest_revenue": cls.get_month_with_most_revenue(),
                "best_clients": cls.get_best_costumers(),
            }, None
        except (SQLAlchemyError, RuntimeError) as ex:
            return None, str(ex)
