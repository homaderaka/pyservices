from behave import given, when, then

from src.predictor.predictor import Predictor


@given('there is a Predictor object')
def create_predictor(context):
    context.currency_predictor = Predictor()


@when('extrapolate_currency method is called')
def call_extrapolate_currency(context):
    context.result = context.currency_predictor.extrapolate_currency_rate([10, 20, 30])


@then('currency values list must be correct')
def check_x_labels(context):
    assert context.result == [10, 20, 30, 45.0, 67.5, 101.25, 151.875, 227.8125, 341.71875], \
        "Currency values list is not correct"


@then('currency values list must be at least 9 elements')
def check_x_labels(context):
    assert len(context.result) >= 9, \
        "Currency values list doesn't have enough elements"


@when('exchange_rates method is called')
def call_exchange_rate(context):
    context.result = context.currency_predictor.exchange_rate([10, 20, 30], [1, 2, 3], 4)


@then('exchange rate must be correct')
def check_x_labels(context):
    assert context.result == 0.1, \
        "Exchange rate is not correct"


