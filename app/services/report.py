from flask import Blueprint

from app.common.http_methods import GET

from ..controllers import ReportController
from .base import get_report_service

report = Blueprint("report", __name__)


@report.route("/", methods=GET)
def get_report():
    return get_report_service(ReportController)
