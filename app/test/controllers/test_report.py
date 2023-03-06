import pytest
from app.controllers import ReportController


def test_get_report_when_called_the_method(app):
    report_controller = ReportController()
    pytest.assume(report_controller.get_report())

def test_get_month_with_more_revenue_when_called_the_method(app):
    report_controller = ReportController()
    pytest.assume(report_controller.get_month_with_more_revenue())

def test_get_most_request_ingredient_when_called_the_method(app):
    report_controller = ReportController()
    pytest.assume(report_controller.get_most_requested_ingredient())

def test_get_best_customers_when_called_the_method(app):
    report_controller = ReportController()
    pytest.assume(report_controller.get_best_customers())