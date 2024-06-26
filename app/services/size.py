from flask import Blueprint, request

from app.common.http_methods import GET, POST, PUT

from ..controllers import SizeController
from .base import create_service, get_all, get_by_id, update_service

size = Blueprint("size", __name__)


@size.route("/", methods=POST)
def create_size():
    return create_service(SizeController, request)


@size.route("/", methods=PUT)
def update_size():
    return update_service(SizeController, request)


@size.route("/id/<_id>", methods=GET)
def get_size_by_id(_id: int):
    return get_by_id(SizeController, _id)


@size.route("/", methods=GET)
def get_sizes():
    return get_all(SizeController)
