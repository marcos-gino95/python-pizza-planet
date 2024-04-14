from flask import Blueprint, request

from app.common.http_methods import GET, POST, PUT

from ..controllers import BeverageController
from .base import create_service, get_all, get_by_id, update_service

beverage = Blueprint("beverage", __name__)


@beverage.route("/", methods=POST)
def create_beverage():
    return create_service(BeverageController, request)


@beverage.route("/", methods=PUT)
def update_beverage():
    return update_service(BeverageController, request)


@beverage.route("/id/<_id>", methods=GET)
def get_beverage_by_id(_id: int):
    return get_by_id(BeverageController, _id)


@beverage.route("/", methods=GET)
def get_beverages():
    return get_all(BeverageController)
